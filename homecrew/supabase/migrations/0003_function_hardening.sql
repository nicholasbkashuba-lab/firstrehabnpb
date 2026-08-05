-- HomeCrew — function hardening
-- Apply after 0002_client_directory.sql
--
-- Clears the security advisories Supabase's linter raises against the helper
-- functions, without breaking the policies that depend on them.
--
-- ---------------------------------------------------------------------------
-- WHAT THE LINTER WANTED, AND WHAT IS ACTUALLY SAFE
--
-- `is_owner()` and `is_active_crew()` are SECURITY DEFINER, and every table
-- policy calls one of them. The linter flags that both were callable straight
-- off the REST API as `/rest/v1/rpc/is_owner`, by anon and authenticated alike.
--
-- The obvious fix — revoke EXECUTE from everyone — breaks the whole database.
-- RLS policy expressions are evaluated with the *caller's* privileges, so a
-- role that cannot execute the function cannot read the table either: every
-- query comes back "permission denied for function is_owner" instead of an
-- empty result. Verified on this project before writing this migration.
--
-- Note also that revoking from `anon` and `authenticated` alone does nothing:
-- PUBLIC holds an EXECUTE grant on every new function by default and both
-- roles inherit it. The revoke has to name PUBLIC to have any effect.
--
-- So: revoke from PUBLIC (which closes anon), then grant back to authenticated
-- (which the policies need). Net effect — a signed-out visitor can no longer
-- call either function over REST, and a signed-in crew member can, which is
-- unavoidable and harmless: `is_owner()` tells them whether they are an owner,
-- which they already know. That residual advisory is accepted, not missed.
-- ---------------------------------------------------------------------------

revoke execute on function public.is_active_crew() from public;
revoke execute on function public.is_owner()       from public;

grant execute on function public.is_active_crew() to authenticated;
grant execute on function public.is_owner()       to authenticated;

-- ONE BEHAVIOUR CHANGE WORTH KNOWING
--
-- A signed-out request to a protected table now comes back
--   401 {"code":"42501","message":"permission denied for function is_owner"}
-- rather than a clean empty 200. Both deny the data; this one just says so
-- louder, and names a function in the message. The portal never reads as anon —
-- it queries only after sign-in — so nothing in the app sees this. If a future
-- public-facing read is ever added, grant EXECUTE back to anon for that path
-- rather than loosening any table policy.

-- `next_inspection_no()` runs as the inserting user (it is the column default
-- on inspections.inspection_no, and is deliberately not SECURITY DEFINER), so
-- PUBLIC keeps EXECUTE. It only needed its search_path pinned so a role cannot
-- shadow `nextval` or `to_char` with something of its own.
alter function public.next_inspection_no() set search_path = public, pg_temp;
