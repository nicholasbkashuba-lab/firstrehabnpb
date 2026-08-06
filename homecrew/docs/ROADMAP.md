# Roadmap

Ordered. Each task lists where to work and how to know it's done.

Every task here is **done**. They are kept below with what actually shipped,
since the next person needs to know what the code does, not what it was going to
do. What is left is not engineering: crew accounts and client records
(`docs/SETUP.md` steps 4 and 5), a Resend key (step 6), a domain, and real
photography.

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

## 3. Photo upload to Storage — DONE

Bucket `inspection-photos`, private. Filed photos go to
`{property_id}/{inspection_id}/{uuid}.jpg`; draft photos to
`drafts/{crew_id}/{draft_id}/{uuid}.jpg` and are deleted when the inspection is
filed. Compressed in-browser to ~1600px long edge at JPEG 0.8 before either —
technicians shoot 4MB originals on cell data at the side of a house.

The important correction to the original plan: base64 in `localStorage` was never
going to work, and not only for the quota. **localStorage cannot hold a Blob at
all**, and its ~5MB cap is blown by one inspection with eight photos. Photos are
Blobs in IndexedDB, written the moment each is taken, and a backgrounded iOS tab
no longer takes the morning with it.

No per-file progress bar. Each photo is a couple of hundred KB after compression
and uploads in well under a second; a progress bar for that is chrome, not
information. Revisit if the compression target ever goes up.

**Done:** photos survive a refresh, a crash, a backgrounded tab, and now a
different device.

---

## 4. Report delivery — DONE (needs an API key, not code)

`supabase/functions/send-report/` is written, deployed and live. It verifies the
caller is an **active** crew member, reads the recipient off the property record,
downloads the visit's photos from the private bucket, attaches them inline, sends
via Resend and stamps `sent_at`. It is idempotent: a second tap returns the
original send rather than mailing the homeowner twice.

**No PDF, deliberately.** Edge Functions run on Deno Deploy with no headless
Chrome, so a server-rendered PDF means a second vendor (Browserless, DocRaptor) —
another account, another bill — to make a file the homeowner must download before
reading. The report is HTML already, so it *is* the email: readable the instant
it opens, on a phone. Save as PDF still exists in the portal for a filed copy.
If a PDF is ever genuinely wanted, add it alongside the body, never instead of it.

**Photos are attached, not linked.** The obvious move is a signed URL, and it is
wrong here — it expires, and these emails get kept and forwarded for years.

The template lives in `report.js` as a plain ES module so Deno imports it
natively *and* node can unit-test it with no Deno toolchain and no email key:
`node --input-type=module -e "import('./supabase/functions/send-report/report.test.js')"`.
27 checks, the first of which asserts that **no access code, key box combination,
alarm code or gate name appears in the report** — including when a caller wrongly
merges a property row into the inspection. That rule was a comment before; it is
a test now.

**Left to do, and it is not code:** a Resend account and two secrets. See
`docs/SETUP.md` step 6.

**Done when:** clicking "Send to client" delivers to a real inbox and stamps
`sent_at`. Verified as far as it can be without a key — the deployed function
boots, resolves its import and returns its own 401 to a non-crew caller, which is
distinguishable from the gateway's.

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

## 7. Cross-device draft sync — DONE

IndexedDB made a draft survive the tab. It did not make it survive the device: a
phone that died at house four took the morning with it until that phone charged.

`0006_draft_sync.sql` adds `inspection_drafts` — the structured half of a draft
in Postgres, the photos in the private bucket under `drafts/`. Every local save
schedules a push; signing in anywhere pulls back whatever is newer.

Three decisions worth not undoing:

- **Local is the source, the server is the copy.** Every keystroke still lands in
  IndexedDB within 400ms whether or not there is signal. The push is a slower
  second write that is allowed to fail, retried on a 30s tick, on `online`, and
  at next sign-in.
- **Drafts are private to the technician, including from the owner.** The only
  table here with no `is_owner()` branch. A draft is a half-formed thought — a
  note that says "ask Dave", a score that reads catastrophic because only the two
  broken things are entered so far. Surfacing that to a manager makes the tech
  write for an audience instead of writing what they saw.
- **Nothing is silently overwritten.** If the row moved under us and the edit
  came from another device, the push stops and asks which version to keep.
  Picking a winner on the tech's behalf is how you lose the one they cared about.

**Done:** verified by 50 browser scenarios (`test/durability.js`) and 12 RLS
scenarios run as SQL against the live project, fixtures deleted afterwards.

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
- ~~Offline mode~~ — done, and it turned out to be table stakes rather than a
  nice-to-have. Drafts, photos and submissions all survive no signal; the outbox
  retries by itself.

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
