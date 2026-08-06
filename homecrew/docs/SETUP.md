# Setup — turning the portal on

Steps 1 to 3 are **done** — the project exists, the schema is applied and the
keys are wired. What is left is step 4 onward: the accounts and the data, which
only the owner can enter.

**Project:** `Home Crew` (`fuznycuqxbrwkaiuayjs`, us-west-2)

---

## 1. Create the Supabase project — DONE

Created 2026-08-05. Free tier: a few dozen properties and a few hundred
inspections a year is nowhere near the limits.

## 2. Run the migrations — DONE

All three applied:

1. `0001_init.sql` — tables, RLS, private storage bucket
2. `0002_client_directory.sql` — access-code columns, active-crew-only reads
3. `0003_function_hardening.sql` — closes the helper functions to signed-out callers

Table Editor shows `crew`, `clients`, `properties`, `inspections`, and a Storage
bucket `inspection-photos` marked private.

Two security advisories remain and are deliberate:
`is_owner()` and `is_active_crew()` stay executable by signed-in users because
every RLS policy calls them — revoking that permission makes every table return
"permission denied" instead of an empty result. See the header comment in
`0003_function_hardening.sql`.

## 3. Wire the keys — DONE

`config.js` carries the project URL and the anon key. Both are public
identifiers; every table behind them is protected by Row Level Security. That is
the design, not a shortcut.

**Never put the `service_role` key in `config.js`.** It bypasses RLS entirely. It
belongs only in Edge Function secrets (step 6).

## 4. Create the crew accounts — YOUR MOVE

Passwords should be set by you, not by me, so this one is yours.

There is deliberately **no public signup** — this app holds home addresses.

For each person, twice over:

1. Dashboard → Authentication → Users → Add user. Real work email, a password
   you hand them directly, "Auto Confirm User" on.
2. Copy the new user's UUID, then Table Editor → `crew` → Insert row:
   - `id` — that UUID
   - `full_name` — how it should read on a client report, e.g. `A. Cain`
   - `role` — `technician`, or `owner` for you
   - `active` — true

A person with an auth login but no `crew` row cannot get in; the portal signs
them back out with "not an active crew member". Same if `active` is false — which
is how you cut someone off: flip that one boolean and every address and code is
closed to them on their next request. Do that rather than deleting the row, so
their past inspections keep their author.

## 5. Add clients and properties

Table Editor → `clients`, one row per household. `email` is the address reports
are sent to, so get it right — the portal will not let a technician type over it.

Then `properties`, one row per home, with `client_id` pointing at the client.
Fill in whatever you have:

| Column | What goes in it |
| --- | --- |
| `address` | Full street address — this is what technicians search on |
| `property_type` | Single family / Condo / Townhome / Estate |
| `package` | `bronze`, `silver` or `gold` |
| `visit_frequency` | `weekly`, `biweekly`, `monthly` or `seasonal` |
| `community_gate_name` | Community or gate name, e.g. `Sailfish Point` |
| `gate_code` | Community or driveway gate code |
| `key_box_code` | Lock box combination |
| `key_box_location` | Where the box actually is — "hose bib, right of the garage" |
| `alarm_code` | Disarm code |
| `alarm_company` | Monitoring company, for the 2am call |
| `garage_code` | Keypad code |
| `water_shutoff` | Where the main is — the thing you want at 2am |
| `access_notes` | Dogs, elevators, quirks, anything else |
| `emergency_name` / `emergency_phone` | Local contact who is not the owner |

The four code fields render masked in the portal and reveal on tap. None of them
can reach a client report.

## 6. Report delivery — YOUR MOVE, about five minutes

The Edge Function is **written, deployed and live** on the Home Crew project. It
is not a skeleton any more: it builds the report, pulls the visit's photos out of
the private bucket, attaches them, and emails the whole thing to the address on
the **client record** (never a typed one). What it does not have is an email
provider account, because creating one needs a verification link sent to your
inbox. That part is yours.

**1. Make a Resend account** at <https://resend.com> with
`nicholasbkashuba@gmail.com`. Free tier is 3,000 emails a month, which is far
more than this will ever send. Hand it to the owner later — Resend supports
adding members, so you do not have to give up the login.

**2. Add a sending domain.** Resend → Domains → Add `homecrewfl.com`, then paste
the DKIM and SPF records it gives you into the DNS. Do this even though it is the
fiddly step: mail sent from an unverified domain lands in spam, and a home watch
report in a homeowner's junk folder is the same as no report at all.

If you want to test before the domain is live, Resend gives every account
`onboarding@resend.dev`, which can only send **to the account owner's own
address**. Good enough to see a real report land in your inbox.

**3. Set the two secrets.** Supabase dashboard → Project Settings → Edge
Functions → Secrets (or the CLI):

```bash
supabase secrets set RESEND_API_KEY=re_xxxxxxxx
supabase secrets set REPORT_FROM_EMAIL="HomeCrew <reports@homecrewfl.com>"
```

Nothing else needs deploying. The function picks the secrets up on its next
invocation.

**How to tell it worked.** File an inspection against a property whose client
email is your own, hit **Send to client**, and the portal will say
"Sent — delivered to … with N photos". If a photo could not be attached it says
so in a red banner instead of a green one, on purpose.

**Until the key is set**, "Send to client" returns a visible error naming the
missing key, and the working flow stays **Save as PDF** in the browser. That is
deliberate: a report that silently fails to send is worse than one that visibly
errors, because you would believe the client had been told.

### Why the report is an email and not a PDF attachment

Supabase Edge Functions run on Deno Deploy, which has no headless Chrome, so a
server-rendered PDF would mean a second vendor (Browserless or DocRaptor) —
another account, another bill — to produce a file the homeowner has to download
before reading. The report is HTML already, so it is sent as the email body:
readable the moment it opens, on a phone. Save as PDF still exists for anyone
who wants a filed copy.

Photos are **attached**, not linked. A signed URL expires; these emails get kept
and forwarded for years.

---

## Checking it worked

Sign in as yourself, search a client by name, open the profile, tap **Show** on
the gate code, hit **Start inspection**, clear all 25 lines and generate the
report. It should say "Saved" with an `HC-2026-0001` style number, and that visit
should then appear under Recent visits on the property.

If the login says "not an active crew member", the auth user exists but the
`crew` row does not — step 4, part 2.
