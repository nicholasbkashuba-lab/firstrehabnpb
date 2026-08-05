/* HomeCrew — portal configuration
 * ---------------------------------------------------------------------------
 * Fill these in from Supabase → Project Settings → API, then redeploy.
 *
 * Both values are SAFE to commit. The anon key is a public identifier; every
 * table it can reach is protected by Row Level Security (see
 * supabase/migrations/). It is the SERVICE ROLE key that must never appear
 * here or anywhere else in this folder — that one lives in Edge Function
 * secrets only.
 *
 * While these are blank the portal runs in SAMPLE MODE: it loads three
 * obviously-fake demo clients so the flow can be clicked through, and refuses
 * to store anything. Never type a real address, gate code or key box
 * combination into sample mode — none of it is protected and none of it is
 * saved.
 */
window.HOMECREW_CONFIG = {
  SUPABASE_URL: '',
  SUPABASE_ANON_KEY: '',
};
