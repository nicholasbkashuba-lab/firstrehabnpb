#!/usr/bin/env python3
"""Upload a file to Dropbox from this sandbox, and verify it landed intact.

Replaces the "here is a PowerShell paste, run it on your PC" handoff that every
finished episode used to end with. The finished multicam now goes straight from
here to /Pain2Power/<Guest>/Final/.

WHY A SCRIPT AND NOT THE DROPBOX CONNECTOR: the Dropbox MCP server's create_file
writes UTF-8 text only, and its docs say uploading local or binary artifacts is
not supported. There is no binary write path through the connector at all. The
REST API has one, and both api.dropboxapi.com and content.dropboxapi.com are
reachable from this sandbox (an unauthenticated POST returns 400 from Dropbox,
not a 403 from the proxy), so a direct call works where the connector cannot.

Auth is an app key/secret plus a long-lived REFRESH token, exchanged for a short
access token on each run. Do not store a bare access token as the primary
credential: Dropbox access tokens expire after ~4 hours, which fails silently in
a scheduled routine days later. See docs/DROPBOX-SETUP.md.

Credentials are read, in order, from:
  1. --key <path>
  2. $DROPBOX_CREDENTIALS_JSON   (raw JSON, or a path to the JSON file)
  3. ~/.config/dropbox/credentials.json

Never commit the credentials. .gitignore covers the conventional locations.

Usage:
  python3 tools/dropbox-put.py whoami
  python3 tools/dropbox-put.py hash  <local>
  python3 tools/dropbox-put.py put   <local> "/Pain2Power/Susan Mann/Final/x.mp4"
  python3 tools/dropbox-put.py put   <local> <remote> --dry-run
  python3 tools/dropbox-put.py put   <local> <remote> --overwrite
  python3 tools/dropbox-put.py verify <local> <remote>

INTEGRITY IS CHECKED WITH DROPBOX'S content_hash, NOT A PLAIN sha256. Dropbox
defines content_hash as sha256 over the concatenated sha256 digests of each 4 MB
block. A plain sha256 of the whole file will never match what the API returns,
and reading that mismatch as a corrupt upload has cost time before.
"""

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.dropboxapi.com"
CONTENT = "https://content.dropboxapi.com"

# Dropbox's content_hash block size. Fixed by the API, not a tunable.
HASH_BLOCK = 4 * 1024 * 1024

# Anything at or below this goes up in one request. Dropbox caps a single
# /files/upload at 150 MB and tells you to use an upload session above it.
SINGLE_SHOT_MAX = 140 * 1024 * 1024

# Per-request chunk for a session upload. Small enough that one flaky transfer
# through the agent proxy costs seconds, not minutes -- sessions are resumable
# per chunk, so a retry never restarts the whole file.
CHUNK = 16 * 1024 * 1024

RETRIES = 4


# --------------------------------------------------------------------------
# auth
# --------------------------------------------------------------------------

def load_credentials(key_arg=None):
    """Return the parsed credentials dict, or exit with a useful message."""
    candidates = []
    if key_arg:
        candidates.append(("--key", key_arg))
    env = os.environ.get("DROPBOX_CREDENTIALS_JSON")
    if env:
        candidates.append(("$DROPBOX_CREDENTIALS_JSON", env))
    candidates.append(
        ("default path", os.path.expanduser("~/.config/dropbox/credentials.json"))
    )

    for source, value in candidates:
        blob = None
        if value.lstrip().startswith("{"):
            blob = value
        elif os.path.exists(os.path.expanduser(value)):
            with open(os.path.expanduser(value)) as fh:
                blob = fh.read()
        if blob is None:
            continue
        try:
            creds = json.loads(blob)
        except json.JSONDecodeError as exc:
            sys.exit(f"credentials from {source} are not valid JSON: {exc}")
        if not (creds.get("refresh_token") or creds.get("access_token")):
            sys.exit(
                f"credentials from {source} carry neither refresh_token nor "
                "access_token"
            )
        return creds

    sys.exit(
        "No Dropbox credentials found.\n"
        "  Looked at: --key, $DROPBOX_CREDENTIALS_JSON, "
        "~/.config/dropbox/credentials.json\n"
        "  Set one up with docs/DROPBOX-SETUP.md (one time, about 5 minutes)."
    )


def access_token(creds):
    """Exchange the refresh token for a short-lived access token."""
    if not creds.get("refresh_token"):
        # A bare access token is accepted for a one-off manual run, but it will
        # be dead within hours -- never rely on this in the scheduled routine.
        return creds["access_token"]

    body = urllib.parse.urlencode(
        {
            "grant_type": "refresh_token",
            "refresh_token": creds["refresh_token"],
            "client_id": creds["app_key"],
            "client_secret": creds["app_secret"],
        }
    ).encode()
    req = urllib.request.Request(
        f"{API}/oauth2/token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)["access_token"]
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:400]
        sys.exit(
            f"Dropbox refused the refresh token ({exc.code}): {detail}\n"
            "  If this reads invalid_grant the token was revoked -- re-run the "
            "setup in docs/DROPBOX-SETUP.md."
        )


# --------------------------------------------------------------------------
# requests
# --------------------------------------------------------------------------

def _call(url, token, *, api_args=None, data=None, json_body=None, retries=RETRIES):
    headers = {"Authorization": f"Bearer {token}"}
    if json_body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(json_body).encode()
    if api_args is not None:
        headers["Dropbox-API-Arg"] = json.dumps(api_args)
        headers["Content-Type"] = "application/octet-stream"

    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:500]
            # 429 and 5xx are worth another go; 4xx means the request is wrong
            # and retrying just repeats the same mistake.
            if exc.code not in (429, 500, 502, 503, 504):
                raise RuntimeError(f"Dropbox {exc.code}: {detail}") from exc
            last = f"{exc.code}: {detail}"
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last = str(exc)
        wait = 2 ** attempt
        print(f"    retry in {wait}s ({last})", file=sys.stderr)
        time.sleep(wait)
    raise RuntimeError(f"Dropbox call failed after {retries} tries: {last}")


# --------------------------------------------------------------------------
# hashing
# --------------------------------------------------------------------------

def content_hash(path):
    """Dropbox content_hash: sha256 over the concatenated sha256 of 4 MB blocks.

    NOT a plain sha256 of the file. See the module docstring.
    """
    blocks = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(HASH_BLOCK)
            if not block:
                break
            blocks.update(hashlib.sha256(block).digest())
    return blocks.hexdigest()


def remote_metadata(token, remote):
    try:
        return _call(f"{API}/2/files/get_metadata", token, json_body={"path": remote})
    except RuntimeError as exc:
        if "not_found" in str(exc):
            return None
        raise


# --------------------------------------------------------------------------
# upload
# --------------------------------------------------------------------------

def _human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024


def upload(token, local, remote, *, overwrite=False):
    size = os.path.getsize(local)
    mode = "overwrite" if overwrite else "add"
    commit = {
        "path": remote,
        "mode": mode,
        "autorename": not overwrite,
        "mute": True,
    }

    if size <= SINGLE_SHOT_MAX:
        with open(local, "rb") as fh:
            return _call(f"{CONTENT}/2/files/upload", token,
                         api_args=commit, data=fh.read())

    with open(local, "rb") as fh:
        first = fh.read(CHUNK)
        session = _call(f"{CONTENT}/2/files/upload_session/start", token,
                        api_args={"close": False}, data=first)
        sid = session["session_id"]
        offset = len(first)
        print(f"    session {sid[:12]}… {_human(offset)} / {_human(size)}")

        while True:
            chunk = fh.read(CHUNK)
            if not chunk:
                break
            _call(
                f"{CONTENT}/2/files/upload_session/append_v2", token,
                api_args={"cursor": {"session_id": sid, "offset": offset},
                          "close": False},
                data=chunk,
            )
            offset += len(chunk)
            pct = 100.0 * offset / size
            print(f"    {_human(offset)} / {_human(size)}  ({pct:.0f}%)")

        return _call(
            f"{CONTENT}/2/files/upload_session/finish", token,
            api_args={"cursor": {"session_id": sid, "offset": offset},
                      "commit": commit},
            data=b"",
        )


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_whoami(args):
    token = access_token(load_credentials(args.key))
    who = _call(f"{API}/2/users/get_current_account", token, json_body=None,
                data=b"")
    name = who.get("name", {}).get("display_name", "?")
    print(f"{name}  <{who.get('email','?')}>  account {who.get('account_id','?')}")


def cmd_hash(args):
    print(content_hash(args.local))


def cmd_verify(args):
    token = access_token(load_credentials(args.key))
    local = content_hash(args.local)
    meta = remote_metadata(token, args.remote)
    if meta is None:
        sys.exit(f"NOT FOUND in Dropbox: {args.remote}")
    ok = meta.get("content_hash") == local
    print(f"local  {local}")
    print(f"remote {meta.get('content_hash')}")
    print(f"size   {meta.get('size')} bytes")
    print("MATCH" if ok else "MISMATCH")
    sys.exit(0 if ok else 1)


def cmd_put(args):
    if not os.path.exists(args.local):
        sys.exit(f"no such file: {args.local}")
    size = os.path.getsize(args.local)
    local_hash = content_hash(args.local)

    print(f"  {os.path.basename(args.local)}  {_human(size)}")
    print(f"  content_hash {local_hash}")
    print(f"  -> {args.remote}")

    if args.dry_run:
        print("  dry run, nothing uploaded")
        return

    creds = load_credentials(args.key)
    token = access_token(creds)

    # Idempotent: a re-run after a completed upload is a no-op, so the routine
    # can retry without producing "file (1).mp4" beside the real one.
    existing = remote_metadata(token, args.remote)
    if existing and existing.get("content_hash") == local_hash:
        print("  already in Dropbox with a matching content_hash, skipping")
        return
    if existing and not args.overwrite:
        print("  a DIFFERENT file already exists at that path; "
              "uploading alongside it (pass --overwrite to replace)")

    meta = upload(token, args.local, args.remote, overwrite=args.overwrite)

    landed = meta.get("path_display", args.remote)
    if meta.get("content_hash") != local_hash:
        sys.exit(
            f"UPLOAD VERIFY FAILED for {landed}\n"
            f"  local  {local_hash}\n"
            f"  remote {meta.get('content_hash')}\n"
            "  The bytes in Dropbox do not match the local file. Do not treat "
            "this as done."
        )
    print(f"  OK  {landed}")
    print(f"  {meta.get('size')} bytes, content_hash verified")



# --------------------------------------------------------------------------
# one-time setup helper
# --------------------------------------------------------------------------

def cmd_auth(args):
    """Turn an app key/secret into the credentials file this script wants.

    Dropbox only hands out a refresh token when the authorize URL carries
    token_access_type=offline. Leave it off and you get a 4-hour access token
    instead, which works today and fails silently next week.
    """
    if not args.code:
        url = (
            "https://www.dropbox.com/oauth2/authorize"
            f"?client_id={args.app_key}"
            "&response_type=code&token_access_type=offline"
        )
        print("1. Open this and click Allow:\n")
        print(f"   {url}\n")
        print("2. Copy the code Dropbox shows you, then run:\n")
        print(f"   python3 tools/dropbox-put.py auth --app-key {args.app_key} \\")
        print("       --app-secret <secret> --code <code>")
        return

    body = urllib.parse.urlencode({
        "code": args.code,
        "grant_type": "authorization_code",
        "client_id": args.app_key,
        "client_secret": args.app_secret,
    }).encode()
    req = urllib.request.Request(
        f"{API}/oauth2/token", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            got = json.load(resp)
    except urllib.error.HTTPError as exc:
        sys.exit(f"exchange failed ({exc.code}): "
                 f"{exc.read().decode(errors='replace')[:400]}")

    if "refresh_token" not in got:
        sys.exit("Dropbox returned no refresh_token. The authorize URL was "
                 "missing token_access_type=offline -- start over.")

    creds = {
        "app_key": args.app_key,
        "app_secret": args.app_secret,
        "refresh_token": got["refresh_token"],
    }
    dest = os.path.expanduser(args.out)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as fh:
        json.dump(creds, fh, indent=2)
    os.chmod(dest, 0o600)
    print(f"wrote {dest}")
    print("\nPaste this into the environment Setup script box so every future "
          "session has it:\n")
    print("mkdir -p ~/.config/dropbox && cat > ~/.config/dropbox/credentials.json <<'EOF'")
    print(json.dumps(creds, indent=2))
    print("EOF")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--key", help="path to the credentials JSON")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("auth", help="one-time: turn an app key/secret into credentials")
    p.add_argument("--app-key", required=True)
    p.add_argument("--app-secret")
    p.add_argument("--code", help="the code Dropbox showed you after Allow")
    p.add_argument("--out", default="~/.config/dropbox/credentials.json")
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser("whoami", help="confirm the credentials work")
    p.set_defaults(func=cmd_whoami)

    p = sub.add_parser("hash", help="print a file's Dropbox content_hash")
    p.add_argument("local")
    p.set_defaults(func=cmd_hash)

    p = sub.add_parser("put", help="upload a file")
    p.add_argument("local")
    p.add_argument("remote", help='full Dropbox path, e.g. "/Pain2Power/X/Final/y.mp4"')
    p.add_argument("--overwrite", action="store_true",
                   help="replace an existing file instead of uploading alongside it")
    p.add_argument("--dry-run", action="store_true",
                   help="hash and report, upload nothing")
    p.set_defaults(func=cmd_put)

    p = sub.add_parser("verify", help="compare a local file against Dropbox")
    p.add_argument("local")
    p.add_argument("remote")
    p.set_defaults(func=cmd_verify)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
