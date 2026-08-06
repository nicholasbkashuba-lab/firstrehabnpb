/* Tests for the emailed report body.  node supabase/functions/send-report/report.test.js
 *
 * Runs without Deno, without a Supabase project and without an email key,
 * because the template is a pure function. The point is that the one rule that
 * really matters — no access codes in a client report — is checked by a machine
 * rather than by whoever last edited the file remembering it.
 */
import { buildReportHtml, buildReportText, band, esc, fmtDate } from './report.js';

let pass = 0, fail = 0;
function check(name, expected, actual) {
  const ok = JSON.stringify(expected) === JSON.stringify(actual);
  ok ? pass++ : fail++;
  console.log(`${ok ? 'PASS' : '*** FAIL ***'}  ${name}` +
    (ok ? '' : `\n      expected=${JSON.stringify(expected)}\n      actual  =${JSON.stringify(actual)}`));
}

const INSPECTION = {
  inspection_no: 'HC-2026-0042',
  property_addr: '18 Sailfish Point Blvd, Stuart FL 34996',
  inspected_on: '2026-08-04',
  arrival_at: '09:12',
  departure_at: '09:48',
  weather: 'Clear, 88F',
  overall_score: 82,
  scores: { security: 100, plumbing: 65, hvac: 100, exterior: 80, storm: 100 },
  flags: [
    { system: 'Plumbing', item: 'No visible leaks', state: 'bad',
      note: 'Stain under the kitchen sink, dry to the touch.', photo_count: 2 },
    { system: 'Exterior', item: 'Pool & spa', state: 'watch',
      note: 'Water line about two inches low.', photo_count: 1 },
    { system: 'Security', item: 'Doors & locks', state: 'ok' },
  ],
  notes: 'Mail collected and left on the counter.',
  actions: ['Have a plumber look at the sink trap', 'Top up the pool'],
};

/* The credentials that must never reach a client. Every one of these lives on
   the property record, and the function is deliberately never handed that row. */
const SECRETS = {
  gate_code: '4417',
  key_box_code: '9082',
  key_box_location: 'Left of the garage door',
  alarm_code: '1379',
  alarm_company: 'Sailfish Security',
  garage_code: '2244',
  community_gate: 'Sailfish Point North Gate',
};

const html = buildReportHtml(INSPECTION, [
  { cid: 'shot1', alt: 'Stain under the sink' },
  { cid: 'shot2', alt: 'Pool water line' },
]);
const text = buildReportText(INSPECTION);

/* ---------- 1. the rule that matters ---------- */
const leaked = Object.entries(SECRETS)
  .filter(([, v]) => html.includes(v) || text.includes(v))
  .map(([k]) => k);
check('NO ACCESS CODE OR CREDENTIAL APPEARS IN THE REPORT', [], leaked);

/* Belt and braces: a caller who wrongly merges a property row into the
   inspection must still not leak, because the template reads named fields
   only and never spreads unknown keys. */
const contaminated = buildReportHtml(Object.assign({}, INSPECTION, SECRETS), []);
const leaked2 = Object.entries(SECRETS)
  .filter(([, v]) => contaminated.includes(v)).map(([k]) => k);
check('still no leak when a property row is wrongly merged in', [], leaked2);

/* ---------- 2. the report says what happened ---------- */
check('carries the overall score', true, html.includes('82'));
check('carries the report number', true, html.includes('HC-2026-0042'));
check('carries the address', true, html.includes('18 Sailfish Point Blvd, Stuart FL 34996'));
check('date is written out, not ISO', true, html.includes('August 4, 2026'));
check('lists both attention items', true,
  html.includes('No visible leaks') && html.includes('Pool &amp; spa'));
check('does NOT list the cleared item as an attention item', false,
  html.includes('Doors &amp; locks'));
check('carries the technician note', true, html.includes('Mail collected'));
check('carries both recommended actions', true,
  html.includes('plumber look at the sink trap') && html.includes('Top up the pool'));
check('references photos by content id, not a signed URL', true,
  html.includes('cid:shot1') && !html.includes('supabase.co'));

/* ---------- 3. it is an email, not a web page ---------- */
check('no <style> block (Gmail strips them)', false, /<style[\s>]/i.test(html));
check('no CSS custom properties (mail clients resolve them to nothing)', false,
  html.includes('var(--'));
check('no flex or grid layout', false, /display:\s*(flex|grid)/.test(html));
check('has a plain-text alternative', true, text.length > 200);

/* ---------- 4. colours are the light-background family ---------- */
check('uses the AA-safe green, never the bright one', true,
  !html.includes('#2E9E5B') && !html.includes('#D89A2B'));
check('band thresholds match the portal', ['Excellent','Very Good','Good','Monitor','Needs Attention'],
  [95, 82, 74, 60, 20].map((s) => band(s).t));
check('band colours are the deep family', ['#246F41','#246F41','#8F6611','#8F6611','#C0392B'],
  [95, 82, 74, 60, 20].map((s) => band(s).c));

/* ---------- 5. hostile input ---------- */
const nasty = buildReportHtml({
  inspection_no: '<script>alert(1)</script>',
  property_addr: '12 "Quote" & <b>Bold</b> Rd',
  inspected_on: '2026-08-04', overall_score: 90, scores: {},
  flags: [{ system: 'X', item: '<img src=x onerror=alert(1)>', state: 'bad' }],
  notes: null, actions: [],
}, []);
check('script tags are escaped, not emitted', false, /<script>alert/.test(nasty));
check('img onerror is escaped, not emitted', false, /<img src=x onerror/.test(nasty));
check('ampersands and quotes survive as entities', true,
  nasty.includes('&quot;Quote&quot; &amp; &lt;b&gt;Bold&lt;/b&gt;'));

/* ---------- 6. degenerate but legal rows ---------- */
const bare = buildReportHtml({ overall_score: 100, scores: {}, flags: [], actions: [] }, []);
check('a perfect visit renders and says so', true,
  bare.includes('Nothing needed attention'));
check('a row with no photos omits the photo block', false, bare.includes('cid:'));
check('a row with no notes omits the notes block', false, bare.includes('Technician notes'));
check('empty score set does not crash', true, bare.includes('100'));
check('missing date renders empty, not "Invalid Date"', '', fmtDate(null));
check('esc handles null', '', esc(null));

console.log(`\n${pass}/${pass + fail} checks passed`);
process.exit(fail ? 1 : 0);
