-- HomeCrew — route planning
-- Apply after 0003_function_hardening.sql
--
-- Adds what the portal needs to build a day's route out of the property list.
--
-- ---------------------------------------------------------------------------
-- WHY THERE IS NO LATITUDE AND LONGITUDE HERE
--
-- True route optimisation needs coordinates, and coordinates need a geocoding
-- API with a key and a billing account. That is a real cost and a real decision,
-- and it is not one to make on the owner's behalf.
--
-- It also turns out to buy very little here. The entire service area is a
-- single line: five counties stacked north to south along I-95 and US-1, from
-- Sebastian to Fort Lauderdale. For a corridor that shape, "drive the stops in
-- geographic order" is within a few minutes of the true optimum, and a
-- technician can beat any solver anyway by knowing that two houses share a gate.
--
-- So: `county` gives the north-to-south band, `route_order` orders stops within
-- it, and the technician can drag to override. Navigation itself hands off to
-- Google or Apple Maps, which already know the roads and the traffic. If real
-- optimisation is ever wanted, add lat/lon here and the ordering function in
-- portal.html is the only thing that has to change.
-- ---------------------------------------------------------------------------

alter table properties add column if not exists county text
  check (county is null or county in (
    'Indian River','St. Lucie','Martin','Palm Beach','Broward'));

-- Lower sorts earlier within a county. Ties fall back to address.
alter table properties add column if not exists route_order int not null default 100;

comment on column properties.county is
  'North-to-south band for route ordering. Indian River is northmost, Broward southmost.';
comment on column properties.route_order is
  'Manual ordering within a county. Lower drives first; ties break on address.';

create index if not exists properties_route_idx on properties (county, route_order);

-- ------------------------------------------------------------ visit tracking
-- "When was this property last actually inspected" drives the due list. Reading
-- it from inspections keeps one source of truth rather than a column that can
-- drift out of step with the visits themselves.
create or replace view property_last_visit
with (security_invoker = true) as
  select p.id as property_id,
         max(i.inspected_on) as last_inspected_on,
         count(i.id)         as visit_count
  from properties p
  left join inspections i on i.property_id = p.id
  group by p.id;

comment on view property_last_visit is
  'security_invoker: the caller''s RLS applies, so a technician sees only what '
  'the properties and inspections policies already allow them to see.';

grant select on property_last_visit to authenticated;
