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
 *
 * The key below is the legacy `anon` key rather than the newer
 * `sb_publishable_...` one. Both work; the anon key is used because the
 * Supabase client loads from a CDN tag pinned only to major version 2, and the
 * anon key is accepted by every v2 build. If that tag is ever pinned to an
 * exact version >= 2.49, switching to the publishable key is a one-line change.
 */
window.HOMECREW_CONFIG = {
  SUPABASE_URL: 'https://fuznycuqxbrwkaiuayjs.supabase.co',
  SUPABASE_ANON_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ1em55Y3VxeGJyd2thaXVheWpzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU5NDE0MzksImV4cCI6MjEwMTUxNzQzOX0.mc2yFYWDQfG3dJ7VmqQ43oDrSRCxpuD9K1BNv9HJWKM',
};
