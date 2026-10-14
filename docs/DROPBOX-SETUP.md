# Dropbox upload — one-time setup

Do this once. After it, every finished episode goes from the sandbox straight into
`/Pain2Power/<Guest>/Final/` with nothing to run on your own machine.

**Time: about five minutes. Owner only — it needs your Dropbox login.**

## Why this exists

The Dropbox connector in a Claude session can browse, search, read text and make
folders, but it **cannot write a binary file**. Its own documentation lists
"uploading local/binary artifacts" as unsupported. That is why every finished
episode used to end with a PowerShell paste: there was no way to move the mp4
from here into Dropbox, so the bytes went to GitHub in 45 MB chunks and you
reassembled them on your PC.

The Dropbox REST API does have a binary upload, and both of its hosts answer from
this sandbox. `tools/dropbox-put.py` uses it. It just needs a credential.

## Step 1 — create the app

1. Go to https://www.dropbox.com/developers/apps and click **Create app**.
2. Choose **Scoped access**.
3. Choose **Full Dropbox**, not App folder. The episodes live at `/Pain2Power/…`,
   which sits at the root of your Dropbox — an App folder app cannot see it.
4. Name it something obvious, e.g. `first-rehab-episode-uploader`.

## Step 2 — give it permissions

On the new app's **Permissions** tab, tick:

- `files.metadata.read`
- `files.content.read`
- `files.content.write`
- `account_info.read`

Click **Submit** at the bottom. This is the step people skip, and skipping it
produces a token that authenticates fine and then gets refused on every upload.

## Step 3 — get a refresh token

From the app's **Settings** tab, copy the **App key** and **App secret**.

In a Claude session on this repo, run:

    python3 tools/dropbox-put.py auth --app-key <APP KEY>

It prints a Dropbox URL. Open it, click **Allow**, copy the code Dropbox shows
you, then run:

    python3 tools/dropbox-put.py auth --app-key <APP KEY> \
        --app-secret <APP SECRET> --code <CODE>

That writes `~/.config/dropbox/credentials.json` and prints a heredoc block.

**Why a refresh token and not an access token:** a Dropbox access token dies after
about four hours. It would work while you were setting it up and then fail in the
scheduled routine days later, with no obvious cause. The refresh token does not
expire unless you revoke it.

## Step 4 — make it survive a new session

Each cloud session starts from a fresh clone, so a file written in one session is
gone in the next. Paste the heredoc block from step 3 into the environment's
**Setup script** box.

Use the **Setup script** box, not the **Environment variables** box. That second
one is `.env` format, one `KEY=value` per line, and it rejects multi-line JSON
outright with "Couldn't parse". This is the same trap the Search Console key hit.

## Step 5 — confirm

    python3 tools/dropbox-put.py whoami

Should print your name and email.

## Using it

    python3 tools/dropbox-put.py put final.mp4 "/Pain2Power/Susan Mann/Final/Pain to Power - Susan Mann - multicam.mp4"

- Files over 140 MB upload in a resumable session, 16 MB at a time, so a dropped
  connection retries one chunk rather than the whole file.
- Every upload is verified against Dropbox's **content_hash**, which is a sha256
  over the concatenated sha256 digests of each 4 MB block — **not** a plain
  sha256 of the file. A plain sha256 will never match; reading that as corruption
  has wasted time before.
- Re-running a completed upload is a no-op. The script compares hashes first, so a
  routine can retry without leaving `file (1).mp4` next to the real one.

## Security

The repo is public. `.gitignore` covers `credentials.json` and the other
conventional names, the same way it covers the Search Console key. If the token
is ever pasted somewhere public, revoke the app at
https://www.dropbox.com/account/connected_apps and redo step 3.
