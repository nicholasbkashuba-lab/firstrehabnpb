/* Axe over EVERY signed-in portal view.
   The earlier sweep hit portal.html cold, where every view but the login screen
   is display:none — and axe skips hidden elements. So "the portal is clean"
   really meant "the login screen is clean". This walks the actual app. */
const { chromium } = require('playwright-core');
const fs = require('fs');
const AXE  = fs.readFileSync(process.env.AXE_PATH || require.resolve('axe-core/axe.min.js'),'utf8');
const FAKE = fs.readFileSync(require('path').join(__dirname,'fake-supabase.js'),'utf8');
const PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAAFklEQVR4nGP8z8Dwn4GBgYGJAQpgDAAtAgQBs4TdCgAAAABJRU5ErkJggg==';
const shot = n => ({ name:n+'.png', mimeType:'image/png', buffer:Buffer.from(PNG,'base64') });
const W = Number(process.argv[2] || 1440);
const PORT = process.env.PORT || 8912;

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const ctx = await b.newContext({ viewport:{width:W,height:1000} });
  await ctx.addInitScript(FAKE);
  await ctx.route('**/*', r => {
    const u = r.request().url();
    return (u.startsWith('http://localhost')||u.startsWith('blob:')||u.startsWith('data:')) ? r.continue() : r.abort();
  });
  const p = await ctx.newPage();
  const out = [];
  let total = 0;

  async function scan(label){
    await p.addStyleTag({content:'*{animation:none!important;transition:none!important}'});
    await p.addScriptTag({ content: AXE });
    const r = await p.evaluate(async () => await axe.run(document, {
      runOnly:{ type:'tag', values:['wcag2a','wcag2aa','wcag21a','wcag21aa'] } }));
    total += r.violations.length;
    if (r.violations.length) {
      out.push(label + ':');
      r.violations.forEach(v => out.push(`   [${v.impact}] ${v.id} — ${v.help} (${v.nodes.length})\n      `
        + v.nodes.slice(0,3).map(n=>n.target.join(' ')).join('\n      ')));
    } else out.push('clean: ' + label);
  }

  await p.goto('http://localhost:' + PORT + '/portal.html', { waitUntil:'domcontentloaded' });
  await scan('login');

  await p.fill('#email','tech1@test.invalid'); await p.fill('#pw','x'); await p.click('#signIn');
  await p.waitForTimeout(900);
  await scan('route');

  await p.click('#tabClients'); await p.waitForTimeout(500);
  await scan('clients list + filters');
  await p.locator('#dirList button[data-id]').first().click(); await p.waitForTimeout(400);
  await scan('client profile (codes masked)');
  const rev = await p.$('[data-reveal]');
  if (rev) { await rev.click(); await p.waitForTimeout(300); await scan('client profile (code revealed)'); }

  await p.click('#tabRoute'); await p.waitForTimeout(300);
  await p.locator('.stop').first().locator('button[data-start]').click();
  await p.waitForTimeout(600);
  await p.click('button[data-sys="plumbing"][data-i="0"][data-v="bad"]');
  await p.click('button[data-sys="exterior"][data-i="1"][data-v="watch"]');
  await p.waitForTimeout(300);
  await p.setInputFiles('#p_plumbing_0', shot('leak'));
  await p.setInputFiles('#f_photos', shot('front'));
  await p.waitForTimeout(1000);
  await scan('inspection form, panels open, photos attached');

  // second house so the resume list renders
  await p.click('#tabRoute'); await p.waitForTimeout(300);
  await p.locator('.stop').nth(1).locator('button[data-start]').click();
  await p.waitForTimeout(800);
  await scan('resume list (other inspections in progress)');

  await p.evaluate(() => conflictBanner());
  await p.waitForTimeout(200);
  await scan('conflict banner');
  await p.evaluate(() => warnBanner('<b>2 photos could not be downloaded</b>Re-take them before you file this inspection.'));
  await p.waitForTimeout(200);
  await scan('missing-photo warning');
  await p.evaluate(() => hideBanner());

  // full report
  const segs = await p.$$('#systems .seg');
  for (let i = 0; i < segs.length; i++) await segs[i].$eval('button[data-v="ok"]', el => el.click());
  await p.waitForTimeout(300);
  await p.click('#genRep');
  await p.waitForTimeout(2200);
  await scan('generated report');

  console.log(out.join('\n'));
  console.log(`TOTAL VIOLATIONS @${W}px: ${total}`);
  await b.close();
  process.exit(total ? 1 : 0);
})();
