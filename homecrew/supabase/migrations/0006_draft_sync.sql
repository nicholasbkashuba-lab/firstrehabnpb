-- HomeCrew — server-side draft sync
-- Apply after 0005_assignment.sql
--
-- Closes the last hole in the durability story. Until now a half-finished
-- inspection lived in one browser's IndexedDB and nowhere else. Nothing was
-- lost — but "your work is safe, it's on the phone in your truck" is not the
-- same promise as "your work is safe", and a technician whose phone dies at
-- house four re-walks four houses.
--
-- ---------------------------------------------------------------------------
-- WHY A SEPARATE TABLE AND NOT A DRAFT ROW IN `inspections`
--
-- An inspections row is a filed record: it has a number, it can be sent to a
-- client, and the owner reads it. A draft is neither. Putting them in one table
-- means every count, every report list and every "how many inspections did we
-- do" query has to remember to exclude the half-typed ones, and one day it
-- won't. Separate table, separate lifecycle, deleted on submit.
--
-- ---------------------------------------------------------------------------
-- DRAFTS ARE PRIVATE TO THE TECHNICIAN — INCLUDING FROM THE OWNER
--
-- Deliberately no is_owner() branch in these policies, which is the opposite of
-- every other table here. A draft is a half-formed thought: boxes ticked in the
-- wrong order, a note that says "ask Dave", a score that reads catastrophic
-- because only the two broken things have been entered so far. Surfacing that
-- to a manager invites acting on it, and the tech starts writing for an
-- audience instead of writing what they saw. The owner sees the filed
-- inspection, which is the thing that is actually true.
--
-- If the owner ever needs a stuck draft recovered, that is a support action
-- through the dashboard, not a standing read grant.
--
-- ---------------------------------------------------------------------------
-- CONFLICT POLICY: LAST WRITE WINS, LOUDLY
--
-- Two devices on one draft is a real scenario (phone in hand, tablet on the
-- seat). The row keeps `device` and `updated_at`; the client compares them and
-- REFUSES to silently overwrite a newer edit made somewhere else — it tells the
-- technician and lets them pick. The database does not arbitrate, because it
-- cannot know which version is right. It only records enough for the client to
-- ask a sensible question.
-- ---------------------------------------------------------------------------

create table if not exists inspection_drafts (
  id            text primary key,
  crew_id       uuid not null default auth.uid() references crew(id) on delete cascade,
  property_id   uuid references properties(id) on delete cascade,
  address       text,
  marked        int  not null default 0,
  payload       jsonb not null,
  photos        jsonb not null default '[]'::jsonb,
  device        text,
  updated_at    timestamptz not null default now(),
  created_at    timestamptz not null default now()
);

comment on table inspection_drafts is
  'Work in progress, one row per technician per property. Private to the '
  'technician who owns it, deleted when the inspection is filed. Never counted '
  'as an inspection.';
comment on column inspection_drafts.photos is
  'Manifest of draft photos already pushed to Storage: [{path, cap, rid}]. The '
  'bytes live in the inspection-photos bucket under drafts/<crew_id>/<draft_id>/.';
comment on column inspection_drafts.device is
  'Opaque per-browser id. Only used so the client can tell "my other device '
  'edited this" from "I edited this here", and warn instead of clobbering.';
comment on column inspection_drafts.marked is
  'How many of the 25 lines are answered. Denormalised so the resume list can '
  'render without unpacking payload.';

create index if not exists inspection_drafts_crew_idx
  on inspection_drafts (crew_id, updated_at desc);

-- Keep updated_at honest even if a client forgets to send it — or lies about it.
--
-- SECURITY INVOKER on purpose, unlike is_owner()/is_active_crew(). Those have to
-- be DEFINER because policies call them for users who cannot read `crew`. This
-- one touches no table at all; it only rewrites NEW. Making it DEFINER bought
-- nothing and cost two linter warnings, so it isn't.
--
-- The grants go too. Postgres checks EXECUTE on a trigger function when the
-- TRIGGER is created, not on every INSERT, so a role with no EXECUTE still
-- fires it normally — while /rest/v1/rpc/touch_draft stops being a thing anyone
-- can call. Note the revoke has to name anon and authenticated explicitly:
-- Supabase's default privileges grant to them directly, so revoking PUBLIC
-- alone leaves the function exposed. Same trap as 0003, opposite direction.
create or replace function touch_draft()
returns trigger language plpgsql set search_path = public as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

revoke execute on function touch_draft() from public, anon, authenticated;

-- INSERT as well as UPDATE. The column default covers a normal insert, but a
-- default is only a default: a client that sends updated_at far in the future
-- would make every other device read as stale forever, and the conflict guard
-- compares exactly this value. The stamp is the server's to set, always.
drop trigger if exists inspection_drafts_touch on inspection_drafts;
create trigger inspection_drafts_touch
  before insert or update on inspection_drafts
  for each row execute function touch_draft();

-- ------------------------------------------------------------------- RLS
alter table inspection_drafts enable row level security;

drop policy if exists "tech owns own drafts" on inspection_drafts;

-- One policy for all four verbs: a draft belongs to exactly one active crew
-- member and nobody else touches it. is_active_crew() is what makes a
-- deactivated account stop syncing on its very next request, same as 0002.
create policy "tech owns own drafts" on inspection_drafts
  for all
  using      (crew_id = auth.uid() and is_active_crew())
  with check (crew_id = auth.uid() and is_active_crew());

-- ------------------------------------------------- draft photos in Storage
-- Draft photos land in the existing private bucket under a drafts/ prefix.
-- Insert and select are already covered by the 0001 policies. What was missing
-- is DELETE: without it every abandoned draft leaks its photos into the bucket
-- forever, and a bucket that only grows is a bill that only grows.
--
-- Scoped to the caller's own draft folder rather than the whole bucket, so this
-- cannot become a way to delete a filed inspection's evidence.
drop policy if exists "crew deletes own draft photos" on storage.objects;
create policy "crew deletes own draft photos" on storage.objects
  for delete using (
    bucket_id = 'inspection-photos'
    and auth.uid() is not null
    and name like 'drafts/' || auth.uid()::text || '/%'
  );
