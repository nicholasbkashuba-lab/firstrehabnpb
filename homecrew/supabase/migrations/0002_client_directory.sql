-- HomeCrew — client directory + access credentials
-- Apply after 0001_init.sql:  supabase db push   (or paste into the SQL editor)
--
-- What this adds:
--   1. The access-credential fields a technician actually needs to get into a
--      house: key box combination and location, alarm code, garage code,
--      community gate name, water shutoff location, on-site emergency contact.
--   2. A deliberate RLS change — see the note below.
--   3. Inspection numbers from a sequence instead of a random client-side guess.
--
-- ---------------------------------------------------------------------------
-- RLS CHANGE — READ THIS BEFORE "FIXING" IT
--
-- 0001 treated gate_code and alarm_notes as owner-only and exposed a
-- properties_field view to technicians. That protection never actually held:
-- the "crew reads properties" policy allowed select on the base table for any
-- authenticated user, so the view was decoration.
--
-- More importantly the requirement is the opposite. A field technician
-- standing at a locked gate at 7am needs the gate code — that is the job.
-- Withholding it means it lives in a group text instead, which is strictly
-- worse. So credentials are readable by ACTIVE CREW, and this migration
-- replaces the honour-system policies with ones that enforce exactly that:
--
--   read  — active crew only (not merely "any authenticated user", which
--           included deactivated accounts and any future non-crew signup)
--   write — owner only
--
-- Deactivating a crew member in the crew table now genuinely cuts their access
-- to every address and code on the next request. That is the security control
-- here; the view was not one.
-- ---------------------------------------------------------------------------

-- ------------------------------------------------- access credential columns
alter table properties add column if not exists key_box_code        text;
alter table properties add column if not exists key_box_location    text;
alter table properties add column if not exists alarm_code          text;
alter table properties add column if not exists alarm_company       text;
alter table properties add column if not exists garage_code         text;
alter table properties add column if not exists community_gate_name text;
alter table properties add column if not exists water_shutoff       text;
alter table properties add column if not exists emergency_name      text;
alter table properties add column if not exists emergency_phone     text;
alter table properties add column if not exists visit_frequency     text
  check (visit_frequency is null or visit_frequency in ('weekly','biweekly','monthly','seasonal'));

comment on column properties.gate_code    is 'Community/driveway gate. Crew-readable, owner-writable. Never rendered into a client report.';
comment on column properties.key_box_code is 'Lock box combination. Same handling as gate_code.';
comment on column properties.alarm_code   is 'Disarm code. Same handling as gate_code.';

-- Nothing in this set may ever reach a client-facing report. The report
-- template pulls address and owner name only — keep it that way.

-- --------------------------------------------------------- active crew check
create or replace function is_active_crew()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from crew where id = auth.uid() and active);
$$;

-- ------------------------------------------------------------- replace RLS
-- The properties_field view was never a boundary (see note above) and is now
-- misleading. Drop it rather than leave a false sense of protection in place.
drop view if exists properties_field;

drop policy if exists "crew reads clients"      on clients;
drop policy if exists "crew reads properties"   on properties;
drop policy if exists "tech reads own"          on inspections;
drop policy if exists "crew uploads photos"     on storage.objects;
drop policy if exists "crew reads photos"       on storage.objects;

create policy "active crew reads clients"    on clients    for select using (is_active_crew());
create policy "active crew reads properties" on properties for select using (is_active_crew());

-- A technician sees their own inspections; the owner sees everything. Unchanged
-- from 0001 apart from requiring the account to still be active.
create policy "crew reads inspections" on inspections for select
  using ((technician_id = auth.uid() and is_active_crew()) or is_owner());

create policy "active crew uploads photos" on storage.objects for insert
  with check (bucket_id = 'inspection-photos' and is_active_crew());
create policy "active crew reads photos"   on storage.objects for select
  using (bucket_id = 'inspection-photos' and is_active_crew());

-- ------------------------------------------------------- inspection numbers
-- 0001 declared inspection_no unique but the portal generated HC-YYYY-{random
-- 4 digits} in the browser, which collides. Server-side sequence instead.
create sequence if not exists inspection_no_seq;

create or replace function next_inspection_no()
returns text language sql volatile as $$
  select 'HC-' || to_char(current_date, 'YYYY') || '-'
      || lpad(nextval('inspection_no_seq')::text, 4, '0');
$$;

alter table inspections alter column inspection_no set default next_inspection_no();

-- ------------------------------------------------------------------ search
-- The roster is small enough that the portal filters client-side, but these
-- keep the Supabase table editor usable as it grows.
create index if not exists clients_name_idx    on clients (lower(full_name));
create index if not exists properties_addr_idx on properties (lower(address));
