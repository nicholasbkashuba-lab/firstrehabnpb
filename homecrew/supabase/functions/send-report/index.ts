// supabase/functions/send-report/index.ts
//
// Renders an inspection as a PDF and emails it to the client.
// Deploy: supabase functions deploy send-report
//
// Secrets required (supabase secrets set ...):
//   SUPABASE_SERVICE_ROLE_KEY, RESEND_API_KEY, REPORT_FROM_EMAIL
//
// STATUS: skeleton. The PDF step is stubbed — see renderPdf() below.

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const admin = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,   // service role: this function only
);

Deno.serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 });

  // Verify the caller is a signed-in crew member. Do not skip this — the
  // function runs with the service role key and bypasses RLS.
  const jwt = req.headers.get('Authorization')?.replace('Bearer ', '');
  if (!jwt) return new Response('Unauthorized', { status: 401 });

  const { data: { user }, error: authErr } = await admin.auth.getUser(jwt);
  if (authErr || !user) return new Response('Unauthorized', { status: 401 });

  const { inspection_id } = await req.json();
  if (!inspection_id) return new Response('inspection_id required', { status: 400 });

  const { data: insp, error } = await admin
    .from('inspections')
    .select('*, properties(address, clients(full_name, email))')
    .eq('id', inspection_id)
    .single();

  if (error || !insp) return new Response('Inspection not found', { status: 404 });

  // Recipient comes from the property record, NOT a client-supplied field.
  // These emails contain a home address and interior photos of a vacant house.
  const to = insp.properties?.clients?.email;
  if (!to) return new Response('No client email on file for this property', { status: 422 });

  // Photos are in a private bucket — sign them so the PDF renderer can read them.
  const signed = await Promise.all(
    (insp.photo_paths ?? []).map(async (p: string) => {
      const { data } = await admin.storage
        .from('inspection-photos').createSignedUrl(p, 900);
      return data?.signedUrl;
    }),
  );

  const html = buildReportHtml(insp, signed.filter(Boolean) as string[]);
  const pdf = await renderPdf(html);

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
      html: `<p>Your latest HomeCrew inspection report is attached.</p>
             <p>Overall Home Health Score: <strong>${insp.overall_score}/100</strong></p>
             <p>Questions? Call 561-383-0882.</p>`,
      attachments: [{
        filename: `homecrew-report-${insp.inspection_no}.pdf`,
        content: pdf,   // base64
      }],
    }),
  });

  if (!res.ok) {
    // Fail loudly. A silently-unsent report is worse than a visible error,
    // because the owner believes the client was notified.
    const detail = await res.text();
    console.error('send failed', detail);
    return new Response(`Email provider rejected: ${detail}`, { status: 502 });
  }

  await admin.from('inspections')
    .update({ status: 'sent', sent_at: new Date().toISOString() })
    .eq('id', inspection_id);

  return Response.json({ ok: true, to });
});

// ---------------------------------------------------------------------------
// TODO: extract the real template from genRep() in portal.html into a shared
// module so the browser preview and this function can't drift apart.
function buildReportHtml(insp: any, photoUrls: string[]): string {
  throw new Error('buildReportHtml not implemented — see genRep() in portal.html');
}

// TODO: pick one — Puppeteer on Deno Deploy, Browserless, or DocRaptor.
// Must return base64. Watch the Edge Function memory ceiling with many photos;
// if it becomes a problem, move this to a queue-backed worker.
async function renderPdf(html: string): Promise<string> {
  throw new Error('renderPdf not implemented');
}
