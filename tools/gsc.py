#!/usr/bin/env python3
"""Google Search Console client for firstrehabnpb.com.

Replaces the manual "owner exports the Performance ZIP and drops it here" flow
with direct Search Analytics API queries.

Auth is a Google Cloud service account that has been added as a user on the
Search Console property. No browser, no refresh-token expiry, so this works
unattended from a scheduled routine. See docs/SEARCH-CONSOLE-SETUP.md.

Credentials are read, in order, from:
  1. --key <path>
  2. $GSC_SERVICE_ACCOUNT_JSON   (raw JSON, or a path to the JSON file)
  3. ~/.config/gsc/service-account.json

Never commit the key file. .gitignore covers the conventional locations.

Usage:
  python3 tools/gsc.py verify
  python3 tools/gsc.py summary  --days 90
  python3 tools/gsc.py queries  --days 90 --limit 50
  python3 tools/gsc.py pages    --days 90 --limit 50
  python3 tools/gsc.py compare  --days 90
  python3 tools/gsc.py raw --dimensions query,page --days 28 --json

WHY THIS EXISTS / the trap it removes: the GSC CSV export truncates and
anonymises the query and page tables, so totals read off Queries.csv are wrong
(the 2026-08-06 export showed 123 clicks in Queries.csv vs 308 in Devices.csv).
`summary` asks the API for a zero-dimension row, which is the true total by
construction -- there is no table to truncate.
"""

import argparse
import base64
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://searchconsole.googleapis.com/webmasters/v3"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"

DEFAULT_PROPERTY = "sc-domain:firstrehabnpb.com"
# Search Console finalises data on a ~2-3 day lag. Ending the window at today
# would silently mix a partial day into every comparison.
DATA_LAG_DAYS = 3

MAX_ROW_LIMIT = 25000


# --------------------------------------------------------------------------
# auth
# --------------------------------------------------------------------------

def _b64url(raw: bytes) -> bytes:
    return base64.urlsafe_b64encode(raw).rstrip(b"=")


def load_credentials(key_arg=None):
    """Return the parsed service-account dict, or exit with a useful message."""
    candidates = []
    if key_arg:
        candidates.append(("--key", key_arg))
    env = os.environ.get("GSC_SERVICE_ACCOUNT_JSON")
    if env:
        candidates.append(("$GSC_SERVICE_ACCOUNT_JSON", env))
    candidates.append(
        ("default path", os.path.expanduser("~/.config/gsc/service-account.json"))
    )

    for source, value in candidates:
        blob = None
        stripped = value.strip()
        if stripped.startswith("{"):
            blob = stripped
        elif os.path.exists(os.path.expanduser(value)):
            with open(os.path.expanduser(value)) as fh:
                blob = fh.read()
        if blob is None:
            continue
        try:
            creds = json.loads(blob)
        except json.JSONDecodeError as exc:
            sys.exit(f"gsc: credentials from {source} are not valid JSON: {exc}")
        missing = {"client_email", "private_key"} - set(creds)
        if missing:
            sys.exit(
                f"gsc: credentials from {source} are missing {sorted(missing)}. "
                "Download the JSON key from the service account, not the OAuth client."
            )
        return creds

    sys.exit(
        "gsc: no service-account credentials found.\n"
        "  Set GSC_SERVICE_ACCOUNT_JSON, pass --key <path>, or place the key at\n"
        "  ~/.config/gsc/service-account.json\n"
        "  Setup steps: docs/SEARCH-CONSOLE-SETUP.md"
    )


def _sign_rs256(message: bytes, private_key_pem: str) -> bytes:
    """RS256-sign the JWT input using openssl.

    Deliberately NOT using `cryptography`: the system package imports at the top
    level but dies with a pyo3 PanicException when its Rust/cffi backend loads,
    and pip does not repair it. That panic subclasses BaseException, so it slips
    past a normal `except Exception` guard and can abort the process — not
    something to leave in the auth path of an unattended routine. openssl is on
    every box this runs on and needs no Python packages, which matters because
    each scheduled firing works from a fresh clone.
    """
    if not shutil.which("openssl"):
        sys.exit(
            "gsc: cannot sign the auth request — no working 'cryptography' package "
            "and no openssl binary on PATH."
        )
    with tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False) as fh:
        fh.write(private_key_pem)
        key_path = fh.name
    try:
        os.chmod(key_path, 0o600)
        proc = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", key_path],
            input=message,
            capture_output=True,
        )
        if proc.returncode != 0:
            sys.exit(f"gsc: openssl signing failed: {proc.stderr.decode('utf-8', 'replace')}")
        return proc.stdout
    finally:
        os.unlink(key_path)


def access_token(creds) -> str:
    """Mint an OAuth access token from the service-account key (JWT bearer flow)."""
    now = int(time.time())
    header = {"alg": "RS256", "typ": "JWT", "kid": creds.get("private_key_id")}
    claims = {
        "iss": creds["client_email"],
        "scope": SCOPE,
        "aud": creds.get("token_uri", TOKEN_URL),
        "iat": now,
        "exp": now + 3600,
    }
    signing_input = (
        _b64url(json.dumps(header).encode()) + b"." + _b64url(json.dumps(claims).encode())
    )
    assertion = signing_input + b"." + _b64url(_sign_rs256(signing_input, creds["private_key"]))

    body = urllib.parse.urlencode(
        {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion.decode(),
        }
    ).encode()
    req = urllib.request.Request(
        creds.get("token_uri", TOKEN_URL),
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)["access_token"]
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        hint = ""
        if "account not found" in detail:
            hint = (
                "\n  'account not found' means the client_email in the key does not "
                "exist.\n  The service account was deleted, or this is a stale/hand-edited key."
            )
        elif "invalid_grant" in detail:
            hint = (
                "\n  invalid_grant usually means the key was revoked, or the machine "
                "clock is skewed."
            )
        elif "invalid_client" in detail or "unauthorized_client" in detail:
            hint = "\n  Check the Search Console API is enabled on the Cloud project."
        sys.exit(f"gsc: token request failed ({exc.code}): {detail}{hint}")


# --------------------------------------------------------------------------
# api
# --------------------------------------------------------------------------

def api_call(token, path, payload=None):
    url = f"{API}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST" if data else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        if exc.code == 403:
            detail += (
                "\n  403 here almost always means the service account is not yet a user "
                "on the property.\n  Search Console -> Settings -> Users and permissions "
                "-> Add user -> the client_email from the key, Full or Restricted."
            )
        if exc.code == 404:
            detail += (
                "\n  404 means the property string does not match. Run "
                "`python3 tools/gsc.py verify` to list the exact strings."
            )
        sys.exit(f"gsc: API error ({exc.code}) on {path}: {detail}")


def date_window(days, end=None):
    end_date = (
        dt.date.fromisoformat(end)
        if end
        else dt.date.today() - dt.timedelta(days=DATA_LAG_DAYS)
    )
    start_date = end_date - dt.timedelta(days=days - 1)
    return start_date.isoformat(), end_date.isoformat()


def search_analytics(token, prop, start, end, dimensions=None, limit=None,
                     search_type="web", filters=None):
    """Query Search Analytics, paging through startRow until exhausted."""
    dimensions = dimensions or []
    rows = []
    start_row = 0
    while True:
        page_size = MAX_ROW_LIMIT
        if limit is not None:
            remaining = limit - len(rows)
            if remaining <= 0:
                break
            page_size = min(MAX_ROW_LIMIT, remaining)
        payload = {
            "startDate": start,
            "endDate": end,
            "dimensions": dimensions,
            "rowLimit": page_size,
            "startRow": start_row,
            "type": search_type,
        }
        if filters:
            payload["dimensionFilterGroups"] = [{"filters": filters}]
        resp = api_call(
            token,
            f"/sites/{urllib.parse.quote(prop, safe='')}/searchAnalytics/query",
            payload,
        )
        batch = resp.get("rows", [])
        rows.extend(batch)
        # A zero-dimension query returns exactly one row and must not page.
        if not dimensions or len(batch) < page_size:
            break
        start_row += len(batch)
    return rows


# --------------------------------------------------------------------------
# formatting
# --------------------------------------------------------------------------

def fmt_row(row):
    return {
        "clicks": int(row.get("clicks", 0)),
        "impressions": int(row.get("impressions", 0)),
        "ctr": row.get("ctr", 0.0),
        "position": row.get("position", 0.0),
    }


def totals_line(row):
    m = fmt_row(row)
    return (
        f"{m['clicks']:,} clicks / {m['impressions']:,} impressions / "
        f"CTR {m['ctr']*100:.2f}% / avg position {m['position']:.1f}"
    )


def print_table(rows, dimensions, limit=None):
    if not rows:
        print("  (no rows)")
        return
    shown = rows[:limit] if limit else rows
    width = max(len(" | ".join(r.get("keys", []))) for r in shown)
    width = min(max(width, 20), 70)
    header = " | ".join(d for d in dimensions)
    print(f"  {header:<{width}}  {'clicks':>7} {'impr':>9} {'CTR':>7} {'pos':>6}")
    print(f"  {'-' * width}  {'-'*7} {'-'*9} {'-'*7} {'-'*6}")
    for r in shown:
        key = " | ".join(r.get("keys", []))
        if len(key) > width:
            key = key[: width - 1] + "…"
        m = fmt_row(r)
        print(
            f"  {key:<{width}}  {m['clicks']:>7,} {m['impressions']:>9,} "
            f"{m['ctr']*100:>6.2f}% {m['position']:>6.1f}"
        )


def delta(new, old, pct=False, invert=False):
    """Human-readable change. invert=True for position, where lower is better."""
    if old == 0:
        return "n/a"
    change = new - old
    arrow = "+" if change >= 0 else ""
    good = (change < 0) if invert else (change > 0)
    mark = "" if abs(change) < 1e-9 else (" ✓" if good else " ✗")
    if pct:
        return f"{arrow}{change*100:.2f}pp{mark}"
    rel = change / old * 100
    return f"{arrow}{change:,.1f} ({arrow}{rel:.0f}%){mark}"


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_verify(args, token):
    resp = api_call(token, "/sites")
    entries = resp.get("siteEntry", [])
    if not entries:
        print(
            "No properties visible to this service account.\n"
            "The key authenticates fine, but it has not been added as a user on any\n"
            "Search Console property yet. See docs/SEARCH-CONSOLE-SETUP.md step 4."
        )
        return 1
    print("Properties visible to this service account:")
    for e in entries:
        marker = "  <- default" if e["siteUrl"] == DEFAULT_PROPERTY else ""
        print(f"  {e['siteUrl']}  [{e['permissionLevel']}]{marker}")
    if not any(e["siteUrl"] == args.property for e in entries):
        print(
            f"\nNote: --property {args.property} is not in that list. "
            "Pass one of the strings above."
        )
        return 1
    print("\nConnected. Try: python3 tools/gsc.py summary --days 90")
    return 0


def cmd_summary(args, token):
    start, end = date_window(args.days, args.end)
    print(f"Search Console — {args.property}")
    print(f"Window: {start} to {end} ({args.days} days)\n")

    totals = search_analytics(token, args.property, start, end)
    if not totals:
        print("No data in this window.")
        return 0
    print(f"TOTALS  {totals_line(totals[0])}")
    print("  (zero-dimension query — the true total, not a truncated table)\n")

    for dim in ("device", "country"):
        rows = search_analytics(token, args.property, start, end, [dim], limit=8)
        rows.sort(key=lambda r: -r.get("clicks", 0))
        print(f"By {dim}:")
        print_table(rows, [dim])
        print()

    print("Top queries:")
    q = search_analytics(token, args.property, start, end, ["query"], limit=15)
    q.sort(key=lambda r: -r.get("clicks", 0))
    print_table(q, ["query"])
    print()

    print("Top pages:")
    p = search_analytics(token, args.property, start, end, ["page"], limit=15)
    p.sort(key=lambda r: -r.get("clicks", 0))
    print_table(p, ["page"])
    return 0


def cmd_dimension(args, token, dim):
    start, end = date_window(args.days, args.end)
    rows = search_analytics(token, args.property, start, end, [dim], limit=args.limit)
    rows.sort(key=lambda r: -r.get(args.sort, 0))
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0
    print(f"{dim} — {start} to {end}, sorted by {args.sort}\n")
    print_table(rows, [dim])
    return 0


def cmd_compare(args, token):
    end_cur = (
        dt.date.fromisoformat(args.end)
        if args.end
        else dt.date.today() - dt.timedelta(days=DATA_LAG_DAYS)
    )
    start_cur = end_cur - dt.timedelta(days=args.days - 1)
    end_prev = start_cur - dt.timedelta(days=1)
    start_prev = end_prev - dt.timedelta(days=args.days - 1)

    cur = search_analytics(token, args.property, start_cur.isoformat(), end_cur.isoformat())
    prev = search_analytics(token, args.property, start_prev.isoformat(), end_prev.isoformat())
    if not cur or not prev:
        print("Not enough data to compare.")
        return 0
    c, p = fmt_row(cur[0]), fmt_row(prev[0])

    print(f"Search Console — {args.property}")
    print(f"Current : {start_cur} to {end_cur}")
    print(f"Previous: {start_prev} to {end_prev}")
    print("  (non-overlapping windows, unlike the stacked CSV exports)\n")
    print(f"{'metric':<13} {'previous':>12} {'current':>12}   change")
    print(f"{'-'*13} {'-'*12} {'-'*12}   {'-'*20}")
    print(f"{'clicks':<13} {p['clicks']:>12,} {c['clicks']:>12,}   {delta(c['clicks'], p['clicks'])}")
    print(f"{'impressions':<13} {p['impressions']:>12,} {c['impressions']:>12,}   {delta(c['impressions'], p['impressions'])}")
    print(f"{'CTR':<13} {p['ctr']*100:>11.2f}% {c['ctr']*100:>11.2f}%   {delta(c['ctr'], p['ctr'], pct=True)}")
    print(f"{'avg position':<13} {p['position']:>12.1f} {c['position']:>12.1f}   {delta(c['position'], p['position'], invert=True)}")
    return 0


def cmd_raw(args, token):
    start, end = date_window(args.days, args.end)
    dims = [d.strip() for d in args.dimensions.split(",") if d.strip()]
    rows = search_analytics(token, args.property, start, end, dims, limit=args.limit)
    if args.json:
        print(json.dumps({"start": start, "end": end, "dimensions": dims, "rows": rows}, indent=2))
        return 0
    print(f"{'+'.join(dims) or 'totals'} — {start} to {end}\n")
    print_table(rows, dims or ["(totals)"])
    return 0


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Query Google Search Console for firstrehabnpb.com.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Setup: docs/SEARCH-CONSOLE-SETUP.md",
    )
    ap.add_argument("--key", help="path to the service-account JSON key")
    ap.add_argument("--property", default=DEFAULT_PROPERTY,
                    help=f"Search Console property (default: {DEFAULT_PROPERTY})")
    ap.add_argument("--days", type=int, default=90, help="window length in days (default 90)")
    ap.add_argument("--end", help="end date YYYY-MM-DD (default: today minus 3-day data lag)")
    ap.add_argument("--limit", type=int, default=50, help="max rows (default 50)")
    ap.add_argument("--sort", default="clicks",
                    choices=["clicks", "impressions", "ctr", "position"])
    ap.add_argument("--json", action="store_true", help="emit raw JSON")
    ap.add_argument("--dimensions", default="query",
                    help="raw: comma-separated dimensions (query,page,device,country,date,searchAppearance)")
    ap.add_argument("command",
                    choices=["verify", "summary", "queries", "pages", "compare", "raw"])

    args = ap.parse_args()
    token = access_token(load_credentials(args.key))

    if args.command == "verify":
        return cmd_verify(args, token)
    if args.command == "summary":
        return cmd_summary(args, token)
    if args.command == "queries":
        return cmd_dimension(args, token, "query")
    if args.command == "pages":
        return cmd_dimension(args, token, "page")
    if args.command == "compare":
        return cmd_compare(args, token)
    if args.command == "raw":
        return cmd_raw(args, token)
    return 1


if __name__ == "__main__":
    sys.exit(main())
