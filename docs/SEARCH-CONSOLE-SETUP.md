# Connecting Google Search Console

Search Console has **no Claude connector** — it is not in the MCP registry, so there is
nothing to toggle on. The supported way to read it programmatically is the Search Console
API, authenticated with a Google Cloud **service account** that you add as a user on the
property.

`tools/gsc.py` is that client. Once the one-time setup below is done, the manual
"export the Performance ZIP and drop it in the chat" flow is no longer needed — the data
can be pulled on demand, including from an unattended scheduled routine.

## Why a service account, not a normal Google sign-in

A service account is a robot Google account with its own email address. You add that
address as a user on the Search Console property exactly like you'd add a colleague.

- No browser consent screen, so it works headless.
- **No refresh-token expiry.** An OAuth "Testing"-mode app expires its refresh token
  after 7 days, which would silently break the routine every week.
- Read-only scope, and revocable in one click by removing the user from the property.

The property stays owner-locked; you are delegating read access, not moving ownership.

---

## One-time setup (~10 minutes, owner only)

### 1. Create a Google Cloud project
<https://console.cloud.google.com/projectcreate> — name it e.g. `firstrehab-seo`.
A billing account is **not** required; Search Console API usage is free.

### 2. Enable the Search Console API
<https://console.cloud.google.com/apis/library/searchconsole.googleapis.com> →
make sure the new project is selected in the top bar → **Enable**.

### 3. Create the service account and download its key
1. <https://console.cloud.google.com/iam-admin/serviceaccounts> → **Create service account**
2. Name: `claude-gsc-reader`. Skip the optional role/access steps — it needs no
   project IAM roles at all, because its access comes from Search Console, not Cloud IAM.
3. Open the account → **Keys** → **Add key** → **Create new key** → **JSON** → Create.
4. A `.json` file downloads. **This is a secret.** Keep it out of the repo — this
   repository is public and `.gitignore` already blocks the usual filenames, but the
   safest place is outside the project entirely.
5. Copy the `client_email` value from inside that file. It looks like
   `claude-gsc-reader@firstrehab-seo.iam.gserviceaccount.com`.

### 4. Add that email as a user in Search Console
<https://search.google.com/search-console> → select the property →
**Settings** → **Users and permissions** → **Add user** →
paste the `client_email` → permission **Full** (or **Restricted**; read-only is enough) → Add.

> This step is the one people miss. Without it the key authenticates fine but sees zero
> properties, and every query returns 403.

### 5. Point the tool at the key

```bash
export GSC_SERVICE_ACCOUNT_JSON=/path/to/claude-gsc-reader.json
```

Or place it at `~/.config/gsc/service-account.json`, or pass `--key <path>` per call.
The variable may also hold the raw JSON itself, which is what a CI/routine secret wants.

### 6. Confirm it works

```bash
python3 tools/gsc.py verify
```

Expected:

```
Properties visible to this service account:
  sc-domain:firstrehabnpb.com  [siteFullUser]  <- default
```

Whatever string it prints is the exact `--property` value. A domain property reads
`sc-domain:firstrehabnpb.com`; a URL-prefix property reads
`https://www.firstrehabnpb.com/`. They are different properties with different data.

---

## Usage

```bash
python3 tools/gsc.py summary --days 90       # totals + device/country/query/page
python3 tools/gsc.py queries --days 90 --limit 50
python3 tools/gsc.py pages   --days 90 --limit 50 --sort impressions
python3 tools/gsc.py compare --days 90       # vs the previous, non-overlapping 90 days
python3 tools/gsc.py raw --dimensions query,page --days 28 --json
```

Flags: `--days`, `--end YYYY-MM-DD`, `--limit`, `--sort {clicks,impressions,ctr,position}`,
`--json`, `--property`, `--key`.

### Two reporting traps this removes

**Truncated totals.** The CSV export anonymises and truncates the query and page tables,
so totals read off `Queries.csv` are simply wrong — the 2026-08-06 export showed 123
clicks there against 308 in `Devices.csv`. `summary` asks the API for a zero-dimension
row, which is the true total by construction. There is no table to truncate, and no
"read it off the right CSV" rule to remember.

**Overlapping windows.** The first two exports overlapped by ~80% of their days, so the
"before/after" wasn't one. `compare` builds the previous window as the N days ending the
day before the current window starts, so the two never share a day.

### Date handling

Search Console finalises data on a ~2–3 day lag, so the default window ends
**3 days ago**, not today. Otherwise a partial final day gets mixed into every
comparison and quietly drags the numbers down. Override with `--end`.

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| `no service-account credentials found` | `GSC_SERVICE_ACCOUNT_JSON` unset and no key at the default path. |
| `account not found` | The `client_email` in the key no longer exists — deleted service account or a stale key. |
| `invalid_client` / `unauthorized_client` | Step 2 skipped: Search Console API not enabled on the project. |
| Empty property list from `verify` | Step 4 skipped: the service account isn't a user on the property. |
| `403` on a query | Same as above, or the key is for a different property. |
| `404` on a query | `--property` string doesn't match. Run `verify` and copy what it prints. |

### Signing dependency

The tool signs its auth request by shelling out to `openssl` and otherwise uses only the
Python standard library — no `pip install` step, which is what makes it safe to run from
a routine that starts from a fresh clone. It deliberately does **not** use the
`cryptography` package: the system copy imports at the top level but dies with a pyo3
panic when its Rust backend loads, and that panic subclasses `BaseException`, so it
slips past ordinary error handling instead of failing cleanly.

## Revoking access

Search Console → Settings → Users and permissions → remove the service account.
Or delete the key in Cloud Console → Service accounts → Keys. Either one is immediate.
