// The client-facing inspection report, as an email body.
//
// Plain ES module on purpose: Deno imports it natively inside the Edge
// Function, and node can import it directly so the output is unit-testable
// without a Deno toolchain or a live email key. See report.test.js.
//
// ---------------------------------------------------------------------------
// TWO RULES THIS FILE EXISTS TO ENFORCE
//
// 1. NO ACCESS CODES. Not the gate code, key box combination, alarm code,
//    garage code or community gate name. This document is emailed and then
//    forwarded on from there; a code in it is a code in somebody's inbox
//    forever. This module is handed ONLY the inspection row, never the
//    property's credential columns, so there is nothing here to leak — keep
//    it that way when adding fields.
//
// 2. IT IS AN EMAIL, NOT A WEB PAGE. Tables and inline styles, because Gmail
//    strips <style> blocks and Outlook ignores flex and grid. Every colour is
//    literal for the same reason: a CSS custom property resolves to nothing in
//    a mail client, which would silently render black text on black.
//
// Colours are the light-background family (#246F41 green, #8F6611 amber),
// never the brighter #2E9E5B / #D89A2B — those are 3.4:1 and 2.5:1 on white
// and fail WCAG AA. Same split as the site.
// ---------------------------------------------------------------------------

const NAVY = '#0B1D2D';
const GOLD_TEXT = '#7E5F27';
const INK = '#16232E';
const GRAY = '#5A6167';
const LINE = '#DDE1E5';
const PAPER = '#F4F5F6';

const SYSTEM_NAMES = {
  security: 'Security',
  plumbing: 'Plumbing',
  hvac: 'HVAC',
  exterior: 'Exterior',
  storm: 'Storm Readiness',
};

const STATE_LABEL = { ok: 'OK', watch: 'Watch', bad: 'Issue' };

export function esc(v) {
  return String(v == null ? '' : v)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/** Same thresholds and the same deep colours as band() in portal.html. */
export function band(score) {
  const s = Number(score);
  if (s >= 90) return { t: 'Excellent', c: '#246F41' };
  if (s >= 80) return { t: 'Very Good', c: '#246F41' };
  if (s >= 70) return { t: 'Good', c: '#8F6611' };
  if (s >= 55) return { t: 'Monitor', c: '#8F6611' };
  return { t: 'Needs Attention', c: '#C0392B' };
}

export function fmtDate(v) {
  if (!v) return '';
  const d = new Date(String(v).slice(0, 10) + 'T00:00:00Z');
  if (isNaN(d.getTime())) return String(v);
  return d.toLocaleDateString('en-US',
    { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
}

function systemRows(scores) {
  const keys = Object.keys(scores || {});
  if (!keys.length) return '';
  return keys.map((k) => {
    const b = band(scores[k]);
    return `<tr>
      <td style="padding:11px 0;border-bottom:1px solid ${LINE};font-family:Arial,sans-serif;font-size:14px;color:${INK}">
        ${esc(SYSTEM_NAMES[k] || k)}</td>
      <td align="right" style="padding:11px 0;border-bottom:1px solid ${LINE};font-family:Arial,sans-serif;font-size:14px;font-weight:bold;color:${b.c}">
        ${esc(scores[k])}<span style="color:${GRAY};font-weight:normal">/100</span>
        &nbsp;<span style="font-size:11px;letter-spacing:.08em;text-transform:uppercase">${esc(b.t)}</span></td>
    </tr>`;
  }).join('');
}

function attentionRows(flags) {
  const list = (flags || []).filter((f) => f && f.state && f.state !== 'ok');
  if (!list.length) {
    return `<p style="margin:0;font-family:Arial,sans-serif;font-size:14px;line-height:1.6;color:${GRAY}">
      Nothing needed attention on this visit. Every one of the 25 checks cleared.</p>`;
  }
  return `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
    ${list.map((f) => {
      const c = f.state === 'bad' ? '#C0392B' : '#8F6611';
      const note = f.note
        ? `<div style="margin-top:5px;font-family:Arial,sans-serif;font-size:13.5px;line-height:1.6;color:${GRAY}">${esc(f.note)}</div>`
        : '';
      const shots = f.photo_count
        ? `<div style="margin-top:4px;font-family:Arial,sans-serif;font-size:12px;color:${GRAY}">${esc(f.photo_count)} photo${f.photo_count > 1 ? 's' : ''} attached</div>`
        : '';
      return `<tr><td style="padding:0 0 14px">
        <div style="font-family:Arial,sans-serif;font-size:11px;font-weight:bold;letter-spacing:.12em;text-transform:uppercase;color:${c}">
          ${esc(STATE_LABEL[f.state] || f.state)} &middot; ${esc(f.system || '')}</div>
        <div style="margin-top:3px;font-family:Arial,sans-serif;font-size:14.5px;font-weight:bold;color:${INK}">${esc(f.item || '')}</div>
        ${note}${shots}
      </td></tr>`;
    }).join('')}
  </table>`;
}

function actionRows(actions) {
  const list = (actions || []).filter((a) => a && String(a).trim());
  if (!list.length) return '';
  return `<tr><td style="padding:0 32px 30px">
    <h2 style="margin:0 0 12px;font-family:Arial,sans-serif;font-size:12px;font-weight:bold;letter-spacing:.16em;text-transform:uppercase;color:${GOLD_TEXT}">
      Recommended next steps</h2>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
      ${list.map((a) => `<tr><td style="padding:0 0 8px;font-family:Arial,sans-serif;font-size:14px;line-height:1.6;color:${INK}">
        &bull;&nbsp; ${esc(a)}</td></tr>`).join('')}
    </table></td></tr>`;
}

function photoBlock(photos) {
  if (!photos || !photos.length) return '';
  // cid: references resolve against the inline attachments the caller sends.
  // Attachments rather than signed URLs on purpose: a signed URL dies on its
  // expiry, and this email gets kept and forwarded for years.
  return `<tr><td style="padding:0 32px 30px">
    <h2 style="margin:0 0 12px;font-family:Arial,sans-serif;font-size:12px;font-weight:bold;letter-spacing:.16em;text-transform:uppercase;color:${GOLD_TEXT}">
      Photos from this visit</h2>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
      ${photos.map((p, i) => `${i > 0 && i % 2 === 0 ? '</tr><tr>' : ''}
        <td width="50%" valign="top" style="padding:0 6px 12px 0">
          <img src="cid:${esc(p.cid)}" alt="${esc(p.alt || 'Inspection photo')}"
               width="248" style="width:100%;max-width:248px;height:auto;display:block;border:1px solid ${LINE}">
        </td>`).join('')}
    </tr></table></td></tr>`;
}

/**
 * @param {object} insp   an `inspections` row (never a `properties` row — see rule 1)
 * @param {Array<{cid:string, alt?:string}>} photos  inline attachments, by content id
 * @returns {string} a full HTML document suitable for an email body
 */
export function buildReportHtml(insp, photos = []) {
  const b = band(insp.overall_score);
  const addr = insp.property_addr || '';
  const when = fmtDate(insp.inspected_on);
  const window_ = [insp.arrival_at, insp.departure_at].filter(Boolean).join(' &ndash; ');

  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HomeCrew inspection report</title></head>
<body style="margin:0;padding:0;background:${PAPER}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${PAPER}">
<tr><td align="center" style="padding:24px 12px">
  <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"
         style="width:600px;max-width:100%;background:#ffffff;border:1px solid ${LINE}">

    <tr><td style="padding:26px 32px;background:${NAVY}">
      <div style="font-family:Arial,sans-serif;font-size:19px;font-weight:bold;letter-spacing:.16em;color:#ffffff">HOMECREW</div>
      <div style="margin-top:3px;font-family:Arial,sans-serif;font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:#CBA15A">
        Professional Residential Asset Protection</div>
    </td></tr>

    <tr><td style="padding:28px 32px 6px">
      <h1 style="margin:0;font-family:Arial,sans-serif;font-size:21px;color:${INK}">Inspection Report</h1>
      <p style="margin:8px 0 0;font-family:Arial,sans-serif;font-size:14px;line-height:1.6;color:${GRAY}">
        ${esc(addr)}<br>${esc(when)}${window_ ? ' &nbsp;&middot;&nbsp; ' + window_ : ''}${insp.weather ? ' &nbsp;&middot;&nbsp; ' + esc(insp.weather) : ''}
      </p>
    </td></tr>

    <tr><td style="padding:22px 32px 8px">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
             style="background:${PAPER};border:1px solid ${LINE}">
        <tr><td align="center" style="padding:22px 16px">
          <div style="font-family:Arial,sans-serif;font-size:40px;font-weight:bold;line-height:1;color:${b.c}">${esc(insp.overall_score)}<span style="font-size:17px;color:${GRAY}">/100</span></div>
          <div style="margin-top:7px;font-family:Arial,sans-serif;font-size:12px;font-weight:bold;letter-spacing:.16em;text-transform:uppercase;color:${b.c}">${esc(b.t)}</div>
          <div style="margin-top:3px;font-family:Arial,sans-serif;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:${GRAY}">Overall home health score</div>
        </td></tr>
      </table>
    </td></tr>

    <tr><td style="padding:22px 32px 8px">
      <h2 style="margin:0 0 4px;font-family:Arial,sans-serif;font-size:12px;font-weight:bold;letter-spacing:.16em;text-transform:uppercase;color:${GOLD_TEXT}">
        The five systems</h2>
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">${systemRows(insp.scores)}</table>
    </td></tr>

    <tr><td style="padding:24px 32px 8px">
      <h2 style="margin:0 0 12px;font-family:Arial,sans-serif;font-size:12px;font-weight:bold;letter-spacing:.16em;text-transform:uppercase;color:${GOLD_TEXT}">
        Attention items</h2>
      ${attentionRows(insp.flags)}
    </td></tr>

    ${insp.notes ? `<tr><td style="padding:20px 32px 8px">
      <h2 style="margin:0 0 8px;font-family:Arial,sans-serif;font-size:12px;font-weight:bold;letter-spacing:.16em;text-transform:uppercase;color:${GOLD_TEXT}">
        Technician notes</h2>
      <p style="margin:0;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:${INK}">${esc(insp.notes)}</p>
    </td></tr>` : ''}

    ${actionRows(insp.actions)}
    ${photoBlock(photos)}

    <tr><td style="padding:22px 32px 26px;border-top:1px solid ${LINE}">
      <p style="margin:0;font-family:Arial,sans-serif;font-size:13px;line-height:1.65;color:${GRAY}">
        Report ${esc(insp.inspection_no || '')} &middot; generated by HomeCrew.<br>
        Questions about anything in here? Call <a href="tel:+15613830882" style="color:${GOLD_TEXT}">561-383-0882</a>.
      </p>
    </td></tr>

    <tr><td style="padding:16px 32px;background:${NAVY}">
      <p style="margin:0;font-family:Arial,sans-serif;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.72)">
        Professional. Reliable. Local. &nbsp;&middot;&nbsp; Firefighter owned &amp; operated</p>
    </td></tr>

  </table>
</td></tr></table>
</body></html>`;
}

/** Plain-text alternative. Some clients show it, and spam filters like it. */
export function buildReportText(insp) {
  const b = band(insp.overall_score);
  const lines = [
    'HOMECREW INSPECTION REPORT',
    '',
    insp.property_addr || '',
    fmtDate(insp.inspected_on),
    '',
    `Overall home health score: ${insp.overall_score}/100 (${b.t})`,
    '',
    'THE FIVE SYSTEMS',
  ];
  Object.keys(insp.scores || {}).forEach((k) => {
    lines.push(`  ${SYSTEM_NAMES[k] || k}: ${insp.scores[k]}/100`);
  });
  const flags = (insp.flags || []).filter((f) => f && f.state && f.state !== 'ok');
  lines.push('', 'ATTENTION ITEMS');
  if (!flags.length) lines.push('  Nothing needed attention on this visit.');
  flags.forEach((f) => {
    lines.push(`  [${STATE_LABEL[f.state] || f.state}] ${f.system || ''} - ${f.item || ''}`);
    if (f.note) lines.push(`      ${f.note}`);
  });
  if (insp.notes) lines.push('', 'TECHNICIAN NOTES', '  ' + insp.notes);
  const actions = (insp.actions || []).filter((a) => a && String(a).trim());
  if (actions.length) {
    lines.push('', 'RECOMMENDED NEXT STEPS');
    actions.forEach((a) => lines.push('  - ' + a));
  }
  lines.push('', `Report ${insp.inspection_no || ''}`, 'Questions? Call 561-383-0882.');
  return lines.join('\n');
}
