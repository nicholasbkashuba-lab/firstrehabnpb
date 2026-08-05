# Roadmap

Ordered. Each task lists where to work and how to know it's done.

Tasks 1, 2 and 5 are **done** — kept below with what actually shipped, since the
next person needs to know what the code does, not what it was going to do. Tasks
3 and 4 are the remaining work. Before any of it runs against real data the owner
has to create the Supabase project: `docs/SETUP.md`.

---

## 1. Real authentication — DONE

Supabase Auth via the CDN client. `signInWithPassword`, `getSession` restore on
load, real `signOut`. The `DEMO` object is gone.

Two things worth knowing:

- Signing in is not enough. `loadCrewAndStart()` reads the `crew` row and signs
  the session straight back out unless it exists and `active` is true. An auth
  user who is not crew never sees an address.
- With `config.js` blank the portal runs in **sample mode** — three invented
  clients, codes all `0000`, nothing written. It exists so the flow can be
  demoed before the backend does; it is not a fallback for real data, and the
  directory screen says so in red.

There is still no public signup, deliberately. Accounts are made by the owner.

---

## 2. Persist inspections — DONE

Both migrations are written; apply them per `docs/SETUP.md`.

- Draft autosave to `localStorage` on every keystroke and every tick, restored
  after a reload with the ticks intact. Cleared on save, on reset and on sign-out
  so a shared phone does not keep a client address sitting around. Photos are
  excluded — base64 blows past the quota.
- "Generate report" inserts into `inspections` and keeps the id. A failed insert
  shows a red banner telling the technician to save a PDF rather than silently
  losing the visit.
- `inspection_no` now comes from a Postgres sequence (`next_inspection_no()`).
  The old browser-side `HC-YYYY-{random}` collided against a unique column.
- Recent visits per property show on the client profile. There is no separate
  "my recent inspections" list — reopening a past inspection to edit it is not
  built, and the RLS policy blocks updates once a report is `sent`.

---

## 3. Photo upload to Storage — NEXT

Still `FileReader` → base64 → memory. Fine for a demo, will not survive a real
route with 8 photos per house. This is the biggest remaining gap: right now a
refresh mid-visit loses every photo taken so far.

- Bucket `inspection-photos`, **private**.
- Path convention: `{property_id}/{inspection_id}/{uuid}.jpg`.
- Compress client-side before upload — technicians shoot 4MB phone photos and often work on cell data. Target ~1600px on the long edge, JPEG q80. Canvas is enough; no library needed.
- Show per-file upload progress. On a bad connection this is the slowest thing in the app.
- Serve back via signed URLs, ~1 hour expiry.

**Done when:** photos survive a refresh and load into a generated report from Storage.

---

## 4. PDF generation + email delivery

Skeleton: `supabase/functions/send-report/index.ts`.

The report HTML is already fully assembled in `genRep()` in `portal.html`. Extract that into a shared template both the browser preview and the Edge Function can use — don't maintain two copies that drift.

- Render to PDF server-side (Puppeteer on Deno Deploy, or an API like Browserless/DocRaptor).
- Send via Resend or SendGrid. Resend is simpler for this volume.
- Log `sent_at` on the inspection row.
- The portal already calls this function and surfaces whatever it returns, so the
  only work left is server-side. Until it lands, "Send to client" shows a red
  banner and the crew sends the PDF by hand — which is the honest failure mode.
- Handle bounces — a report that silently fails to send is worse than one that visibly errors, because the owner believes the client was notified.

**Done when:** clicking "Send to client" delivers a PDF to a real inbox and stamps `sent_at`.

---

## 5. Properties and clients as real records — DONE

The directory screen. Search by client name or address, profile per client with
every property under it, "Start inspection" prefills the form and links the
inspection to the property.

`0002_client_directory.sql` added the fields a technician actually needs at the
door: key box code and location, alarm code and company, garage code, community
gate name, water shutoff, on-site emergency contact, visit frequency.

Two decisions to not undo:

- **Codes are crew-readable.** 0001 treated them as owner-only behind a
  `properties_field` view, which never worked (the base-table policy allowed the
  same select) and was backwards anyway — the tech at the gate is who needs the
  code. 0002 drops the view and restricts reads to *active crew*, so
  deactivating someone is a real revocation.
- **Codes never enter a report.** Masked in the UI, revealed on tap, re-hidden
  after 30 seconds, and absent from `renderReport()`. Keep them out.

Report recipient accuracy came with it: "Send to client" refuses an inspection
with no `property_id`, and the Edge Function reads the address from the property
row, not the request.

---

## 6. Deploy

- Vercel, static. No build command; output directory is the repo root.
- Point `homecrewfl.com` at it, verify HTTPS.
- Add `vercel.json` with security headers (`X-Frame-Options`, `Referrer-Policy`, HSTS) — the portal has session tokens and shouldn't be iframeable.
- Submit `sitemap.xml` in Google Search Console.

---

## Later, if asked

- Client-facing portal to browse past reports (owner wanted email first)
- Recurring visit scheduling / route planning
- SMS notification on report delivery
- Owner dashboard: visits per property, technician activity
- Offline mode — genuinely useful, since some of these properties have no wifi and poor cell

---

## Known placeholder content

- ~~Stats bar numbers are invented.~~ Replaced with facts about the service (25
  points, 5 systems, 24/7, insured & bonded). Do not put a home count or star
  rating back without real figures.
- `firefighter-turnout-gear.jpg` is a low-res placeholder (upscaled from 547×365). Owner is shooting a real photo of himself in gear. Needs ≥1200×800, subject on the right.
- Facebook is the only social link. Add others if they exist, and update `sameAs` in the JSON-LD.
- The `#report` section's mock document is hand-built HTML mirroring
  `renderReport()`. When a real report exists, consider screenshotting one with
  fake-but-plausible data instead — but never with a real client's address.
