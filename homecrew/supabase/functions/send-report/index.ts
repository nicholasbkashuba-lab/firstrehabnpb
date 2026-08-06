// supabase/functions/send-report/index.ts
//
// Emails a finished inspection to the homeowner.
// Deploy: supabase functions deploy send-report
//
// Secrets required (supabase secrets set ...):
//   RESEND_API_KEY      from resend.com
//   REPORT_FROM_EMAIL   e.g. "HomeCrew <reports@homecrewfl.com>"
// SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are injected by the platform.
//
// ---------------------------------------------------------------------------
// WHY THERE IS NO PDF
//
// The original plan was "render a PDF, attach it". Supabase Edge Functions run
// on Deno Deploy, which has no headless Chrome, so that means an external
// rendering API — Browserless or DocRaptor — which is a second vendor, a second
// account and a second bill, to produce a file the recipient has to download
// before they can read it.
//
// The report is HTML already. So it is sent AS the email: readable the instant
// it opens, on a phone, without downloading anything. "Save as PDF" in the
// portal still exists for anyone who wants a filed copy.
//
// If a PDF attachment is ever genuinely wanted, add it alongside this — do not
// replace the HTML body with a "your report is attached" stub. A report nobody
// opens is not a report.
//
// PHOTOS ARE ATTACHED, NOT LINKED
//
// A signed URL is the obvious move and it is wrong here: it expires, and this
// email gets kept and forwarded for years. Photos ride along as inline
// attachments referenced by cid, so the report still renders in 2030.
// ---------------------------------------------------------------------------

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
import { buildReportHtml, buildReportText } from './report.js';

const admin = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,   // service role: this function only
);

// Guard rails on the attachment payload. Resend's ceiling is 40MB; phone photos
// are ~200KB after the portal's client-side compression, so this is generous.
// Any drop is REPORTED, never silent — a report that quietly loses evidence is
// worse than one that says it did.
const MAX_PHOTOS = 16;
const MAX_TOTAL_BYTES = 18 * 1024 * 1024;

function bytesToBase64(bytes: Uint8Array): string {
  let bin = '';
  const CHUNK = 0x8000;   // chunked: String.fromCharCode(...big) blows the stack
  for (let i = 0; i < bytes.length; i += CHUNK) {
    bin += String.fromCharCode(...bytes.subarray(i, i + CHUNK));
  }
  return btoa(bin);
}

Deno.serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 });

  // Verify the caller is a signed-in, ACTIVE crew member. Do not skip either
  // half — this function holds the service role key and bypasses RLS, so it is
  // the only thing standing between a stale JWT and a client's home address.
  const jwt = req.headers.get('Authorization')?.replace('Bearer ', '');
  if (!jwt) return new Response('Unauthorized', { status: 401 });

  const { data: { user }, error: authErr } = await admin.auth.getUser(jwt);
  if (authErr || !user) return new Response('Unauthorized', { status: 401 });

  const { data: crew } = await admin
    .from('crew').select('active').eq('id', user.id).maybeSingle();
  if (!crew?.active) return new Response('Not an active crew member', { status: 403 });

  const { inspection_id } = await req.json();
  if (!inspection_id) return new Response('inspection_id required', { status: 400 });

  const { data: insp, error } = await admin
    .from('inspections')
    .select('*, properties(address, clients(full_name, email))')
    .eq('id', inspection_id)
    .single();

  if (error || !insp) return new Response('Inspection not found', { status: 404 });
  if (insp.status === 'sent') {
    // Idempotent on purpose: a double tap on a slow connection must not send a
    // homeowner two copies of the same visit.
    return Response.json({ ok: true, already_sent_at: insp.sent_at, to: insp.client_email });
  }

  // Recipient comes from the PROPERTY RECORD, never a client-supplied field.
  // These emails carry a home address and interior photos of a vacant house; a
  // typo in a form box must not be able to redirect one.
  const to = insp.properties?.clients?.email;
  if (!to) return new Response('No client email on file for this property', { status: 422 });

  // Pull the photos out of the private bucket and carry them with the message.
  const paths: string[] = (insp.photo_paths ?? []).slice(0, MAX_PHOTOS);
  const dropped = Math.max(0, (insp.photo_paths?.length ?? 0) - paths.length);
  const attachments: Array<Record<string, string>> = [];
  const inline: Array<{ cid: string; alt: string }> = [];
  let total = 0;
  let unreadable = 0;

  for (let i = 0; i < paths.length; i++) {
    const { data, error: dlErr } = await admin.storage
      .from('inspection-photos').download(paths[i]);
    if (dlErr || !data) { unreadable++; continue; }
    const buf = new Uint8Array(await data.arrayBuffer());
    if (total + buf.length > MAX_TOTAL_BYTES) { unreadable++; continue; }
    total += buf.length;
    const cid = `photo${i + 1}`;
    attachments.push({
      filename: `photo-${i + 1}.jpg`,
      content: bytesToBase64(buf),
      content_id: cid,
      content_type: 'image/jpeg',
    });
    inline.push({ cid, alt: `Inspection photo ${i + 1} of ${insp.property_addr ?? 'the property'}` });
  }

  const html = buildReportHtml(insp, inline);
  const text = buildReportText(insp);

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${Deno.env.get('RESEND_API_KEY')}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: Deno.env.get('REPORT_FROM_EMAIL'),
      to,
      subject: `HomeCrew inspection report — ${insp.property_addr} — ${insp.inspected_on}`,
      html,
      text,
      attachments,
    }),
  });

  if (!res.ok) {
    // Fail loudly. A silently unsent report is worse than a visible error,
    // because the owner believes the client was notified.
    const detail = await res.text();
    console.error('send failed', detail);
    return new Response(`Email provider rejected: ${detail}`, { status: 502 });
  }

  await admin.from('inspections')
    .update({ status: 'sent', sent_at: new Date().toISOString() })
    .eq('id', inspection_id);

  // Tell the caller what actually went, so the portal can say so out loud
  // rather than implying every photo made it.
  return Response.json({
    ok: true,
    to,
    photos_sent: attachments.length,
    photos_dropped: dropped + unreadable,
  });
});
