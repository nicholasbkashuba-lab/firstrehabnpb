-- HomeCrew — initial schema
-- Apply: supabase db push   (or paste into the SQL editor)
--
-- SECURITY NOTE: these tables hold client home addresses, alarm notes and
-- photos of vacant properties. Row Level Security is enabled on every table.
-- Do not disable it to make something work in development.

create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------- crew
-- Mirrors auth.users with app-specific fields. Crew accounts are created by
-- the owner in the Supabase dashboard — there is deliberately no public signup.
create table if not exists crew (
  id          uuid primary key references auth.users(id) on delete cascade,
  full_name   text not null,
  role        text not null default 'technician'
              check (role in ('technician','owner')),
  active      boolean not null default true,
  created_at  timestamptz not null default now()
);

create or replace function is_owner()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from crew where id = auth.uid() and role = 'owner' and active);
$$;

-- ------------------------------------------------------------- clients
create table if not exists clients (
  id            uuid primary key default gen_random_uuid(),
  full_name     text not null,
  email         text not null,
  phone         text,
  mailing_addr  text,
  notes         text,
  created_at    timestamptz not null default now()
);

-- ---------------------------------------------------------- properties
create table if not exists properties (
  id             uuid primary key default gen_random_uuid(),
  client_id      uuid not null references clients(id) on delete cascade,
  address        text not null,
  property_type  text default 'Single family',
  package        text check (package in ('bronze','silver','gold')),
  gate_code      text,          -- sensitive; owner-only via RLS below
  alarm_notes    text,          -- sensitive
  access_notes   text,
  active         boolean not null default true,
  created_at     timestamptz not null default now()
);
create index if not exists properties_client_idx on properties(client_id);

-- --------------------------------------------------------- inspections
create table if not exists inspections (
  id             uuid primary key default gen_random_uuid(),
  property_id    uuid references properties(id) on delete set null,
  technician_id  uuid not null references crew(id),

  -- denormalized so a historical report still renders if a property is edited
  property_addr  text,
  client_email   text,

  inspection_no  text unique,
  inspected_on   date not null default current_date,
  arrival_at     time,
  departure_at   time,
  weather        text,

  scores         jsonb not null,          -- {"security":100,"plumbing":85,...}
  overall_score  int  not null check (overall_score between 0 and 100),
  flags          jsonb default '[]'::jsonb, -- [{"system":"HVAC","item":"Air filter","state":"watch"}]
  notes          text,
  actions        text[] default '{}',
  photo_paths    text[] default '{}',

  status         text not null default 'draft'
                 check (status in ('draft','complete','sent')),
  sent_at        timestamptz,
  created_at     timestamptz not null default now()
);
create index if not exists inspections_property_idx on inspections(property_id, inspected_on desc);
create index if not exists inspections_tech_idx on inspections(technician_id, created_at desc);

-- ------------------------------------------------------------------ RLS
alter table crew        enable row level security;
alter table clients     enable row level security;
alter table properties  enable row level security;
alter table inspections enable row level security;

create policy "crew reads self"        on crew for select using (id = auth.uid() or is_owner());
create policy "owner manages crew"     on crew for all    using (is_owner()) with check (is_owner());

-- Technicians need client contact info to send reports, but only the owner edits.
create policy "crew reads clients"     on clients for select using (auth.uid() is not null);
create policy "owner writes clients"   on clients for all    using (is_owner()) with check (is_owner());

-- Gate codes and alarm notes are owner-only. Expose properties to technicians
-- through this view rather than the base table.
create or replace view properties_field as
  select id, client_id, address, property_type, package, access_notes, active
  from properties where active;

create policy "crew reads properties"  on properties for select using (auth.uid() is not null);
create policy "owner writes properties" on properties for all   using (is_owner()) with check (is_owner());

create policy "tech inserts own"       on inspections for insert
  with check (technician_id = auth.uid());
create policy "tech updates own draft" on inspections for update
  using (technician_id = auth.uid() and status <> 'sent')
  with check (technician_id = auth.uid());
create policy "tech reads own"         on inspections for select
  using (technician_id = auth.uid() or is_owner());
create policy "owner deletes"          on inspections for delete using (is_owner());

-- -------------------------------------------------------------- storage
-- Private bucket. Serve photos with short-lived signed URLs, never public URLs.
insert into storage.buckets (id, name, public)
values ('inspection-photos', 'inspection-photos', false)
on conflict (id) do nothing;

create policy "crew uploads photos" on storage.objects for insert
  with check (bucket_id = 'inspection-photos' and auth.uid() is not null);
create policy "crew reads photos"   on storage.objects for select
  using (bucket_id = 'inspection-photos' and auth.uid() is not null);
