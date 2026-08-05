-- HomeCrew — property assignment
-- Apply after 0004_routing.sql
--
-- Lets the owner put a property on a particular technician, so "show me my
-- houses" is a real question the app can answer once the roster is bigger than
-- one person's day.
--
-- ---------------------------------------------------------------------------
-- ASSIGNMENT IS A FILTER, NOT A PERMISSION
--
-- Deliberately no RLS policy keyed to assigned_to. Any active crew member can
-- still read any property, because home watch does not work otherwise: someone
-- covers a sick colleague, a storm reshuffles the whole week, and the 2am call
-- goes to whoever is nearest rather than whoever is on the sheet. A technician
-- locked out of a house they were sent to at midnight is a worse failure than
-- one who can see a colleague's list.
--
-- The security boundary stays where 0002 put it: active crew see client data,
-- deactivated accounts see nothing. This column only decides what the app shows
-- first.
-- ---------------------------------------------------------------------------

alter table properties add column if not exists assigned_to uuid references crew(id) on delete set null;

comment on column properties.assigned_to is
  'Default technician for this property. A display filter only — every active '
  'crew member can still read every property, because cover and storms happen.';

create index if not exists properties_assigned_idx on properties (assigned_to);
