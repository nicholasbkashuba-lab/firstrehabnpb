# Setup — turning the portal on

Everything in the portal is built. It is running against sample data until the
Supabase project exists. These are the steps only the account owner can do.

Until step 3 is finished, `portal.html` shows a red **Sample data** banner and
three invented clients whose codes are all `0000`. Nothing typed into sample mode
is saved or protected. Do not put a real address or gate code in there.

---

## 1. Create the Supabase project

supabase.com → New project. Free tier is enough to start: a few dozen properties
and a few hundred inspections a year is nowhere near the limits.

Name it **HomeCrew**. Pick the region closest to Florida (`us-east-1`).

Save the database password somewhere real — it is shown once.

## 2. Run the migrations

Dashboard → SQL Editor → New query. Paste and run, in order:

1. `supabase/migrations/0001_init.sql`
2. `supabase/migrations/0002_client_directory.sql`

Then check Table Editor — you should see `crew`, `clients`, `properties` and
`inspections`, and a Storage bucket called `inspection-photos` marked private.

## 3. Wire the keys

Dashboard → Project Settings → API. Copy:

- **Project URL** → `SUPABASE_URL` in `config.js`
- **anon / public key** → `SUPABASE_ANON_KEY` in `config.js`

Commit that file. Both values are public identifiers and every table behind them
is protected by Row Level Security — that is the design, not a shortcut.

**Never put the `service_role` key in `config.js`.** It bypasses RLS entirely. It
belongs only in Edge Function secrets (step 6).

Reload `portal.html`. The sample banner is gone and the login is real.

## 4. Create the crew accounts

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

## 6. Report delivery (not built yet)

`supabase/functions/send-report/index.ts` is a skeleton — the PDF renderer and the
email send are unimplemented, so "Send to client" returns a visible error rather
than pretending. Until it is finished the working flow is **Save as PDF** in the
browser and attach it to an email by hand.

To finish it you will need a Resend account and:

```bash
supabase secrets set RESEND_API_KEY=... REPORT_FROM_EMAIL=reports@homecrewfl.com
supabase functions deploy send-report
```

See `docs/ROADMAP.md` task 4.

---

## Checking it worked

Sign in as yourself, search a client by name, open the profile, tap **Show** on
the gate code, hit **Start inspection**, clear all 25 lines and generate the
report. It should say "Saved" with an `HC-2026-0001` style number, and that visit
should then appear under Recent visits on the property.
