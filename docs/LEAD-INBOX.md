# Lead inbox — `/staff/leads.html`

Where the front desk marks what happened to every website lead: **Needs a call → Contacted →
Booked**, or **No-show / Not a fit**, with an optional note. Until 2026-10-05 every lead in
`intake_leads` sat at `status = 'new'` forever, so there was no way to tell which pages or
channels produced patients rather than form fills.

## Giving someone access

Staff sign in with their existing **First Rehabilitation app** account (same Supabase project,
email + password). Signing in is not enough on its own; the email must also be on the lead
list. Run this in Supabase → SQL Editor (project "First Rehabilitation App"):

```sql
insert into public.lead_staff (email) values ('frontdesk@example.com');   -- lowercase
-- remove someone:
delete from public.lead_staff where email = 'frontdesk@example.com';
-- who has access:
select * from public.lead_staff;
```

The list starts **empty**, so nobody can see a lead until an owner adds them. Someone signed
in but not on the list sees "No leads are visible to this account".

## How it is secured

The page itself is static, holds no data, and ships only the publishable key `intake.js`
already ships. Everything is enforced in Postgres:

| who | can read leads | can change a lead |
|---|---|---|
| website visitor (anon) | no | insert a new lead only (unchanged) |
| signed-in app user NOT on `lead_staff` | no (0 rows) | no |
| signed-in user ON `lead_staff` | yes | outcome only, via `set_lead_status()` |

- RLS policy `staff read leads` on `intake_leads` (SELECT, authenticated, `private.is_lead_staff()`).
- `authenticated` has **no** INSERT / UPDATE / DELETE on `intake_leads`. The only write path is
  `public.set_lead_status(lead_id, new_status, note)`, a SECURITY DEFINER function that checks the
  allow-list, accepts only `new|contacted|booked|no_show|not_a_fit`, caps the note at 500 chars,
  refuses `test` rows, and stamps `status_updated_at` and `status_by` server-side, so the record
  of who changed what cannot be faked from the browser.
- `public.lead_staff` has RLS on and no policies, so it is invisible to everyone except
  the dashboard and service role.
- Lead fields are visitor-typed, so the page renders them with `textContent` only.
- `/staff/*` is noindex (meta and `X-Robots-Tag`), `no-store`, cannot be framed, is absent from
  the sitemap and `llms.txt`, and carries no GA4 / Vercel analytics and no chat widget.

Verified 2026-10-05 by impersonating each role inside a rolled-back transaction: anon read 0,
non-staff read 0 and was refused on both the RPC and a direct UPDATE, staff read 79 and could
set `contacted`, staff was refused an invalid status, a direct edit of `full_name`, and reading
`lead_staff`.

## Schema added (applied 2026-10-05)

- `public.lead_staff (email text pk, added_at timestamptz)`
- `intake_leads.status_note`, `status_updated_at`, `status_by`
- constraint `intake_leads_status_allowed` (alongside the existing length check)
- `private.is_lead_staff()`, `public.set_lead_status(uuid, text, text)`
- `private.stamp_lead_status()` exists but is **unused**. It was meant for a trigger that the
  Supabase MCP connector would not create (it timed out on trigger DDL, and again on dropping
  the function). It is harmless: nothing calls it and only the owner can execute it. Drop it
  from the SQL Editor whenever convenient: `drop function private.stamp_lead_status();`

## Reporting

With outcomes recorded, "which pages produce patients" is one query (exclude test rows):

```sql
select page,
       count(*)                                    as leads,
       count(*) filter (where status = 'booked')   as booked,
       count(*) filter (where status = 'new')      as not_yet_called
from intake_leads
where status <> 'test' and created_at >= now() - interval '90 days'
group by page order by leads desc;
```
