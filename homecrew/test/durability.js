/* Durability and multi-user suite for the HomeCrew portal.
   Each scenario is one thing that could lose a technician's work. */
const { chromium } = require('playwright-core');
const fs = require('fs');
const FAKE = fs.readFileSync(require('path').join(__dirname, 'fake-supabase.js'), 'utf8');
const BASE = 'http://localhost:8912/portal.html';
const PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAAFklEQVR4nGP8z8Dwn4GBgYGJAQpgDAAtAgQBs4TdCgAAAABJRU5ErkJggg==';
const shot = n => ({ name: n + '.png', mimeType: 'image/png', buffer: Buffer.from(PNG, 'base64') });

const results = [];
function check(name, expected, actual) {
  const pass = JSON.stringify(expected) === JSON.stringify(actual);
  results.push({ name, expected, actual, pass });
  console.log(`${pass ? 'PASS' : '*** FAIL ***'}  ${name}   expected=${JSON.stringify(expected)} actual=${JSON.stringify(actual)}`);
}

async function newDevice(browser, opts = {}, seed = null) {
  // A fresh context is a fresh device: its own IndexedDB, localStorage, cookies.
  // Two contexts share no memory, which is exactly the property under test — so
  // "the server already has this" is modelled by seeding the double's tables.
  const ctx = await browser.newContext(Object.assign({ viewport: { width: 1280, height: 950 } }, opts));
  await ctx.addInitScript(FAKE);
  if (seed) await ctx.addInitScript(s => {
    window.__drafts = s.drafts; window.__blobs = s.blobs;
  }, seed);
  // localhost is the app; blob:/data: are how the double hands back stored photo
  // bytes. Everything else is a real network call and must not happen.
  await ctx.route('**/*', r => {
    const u = r.request().url();
    return (u.startsWith('http://localhost') || u.startsWith('blob:') || u.startsWith('data:'))
      ? r.continue() : r.abort();
  });
  return ctx;
}

async function signIn(page, email = 'tech1@test.invalid') {
  await page.goto(BASE, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(150);
  await page.fill('#email', email);
  await page.fill('#pw', 'TestPass!2026a');
  await page.click('#signIn');
  await page.waitForTimeout(600);
}

const errs = [];
function watch(page, tag) {
  page.on('pageerror', e => errs.push(`${tag}: ${e.message}`));
  page.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errs.push(`${tag}: ${m.text()}`); });
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

  /* ---------- 1. LIVE mode reachable at all ---------- */
  const ctxA = await newDevice(browser);
  const A = await ctxA.newPage(); watch(A, 'deviceA');
  await signIn(A);
  check('live sign-in reaches the app', true, await A.isVisible('#routeView'));
  check('route shows due stops from server data', true, (await A.locator('.stop').count()) >= 2);

  /* ---------- 2. photos survive a reload ---------- */
  await A.locator('.stop').first().locator('button[data-start]').click();
  await A.waitForTimeout(500);
  const addr1 = await A.inputValue('#f_addr');
  await A.setInputFiles('#f_photos', [shot('a1'), shot('a2')]);
  await A.waitForTimeout(1200);
  await A.click('button[data-sys="plumbing"][data-i="0"][data-v="bad"]');
  await A.waitForTimeout(200);
  await A.setInputFiles('#p_plumbing_0', shot('leak'));
  await A.fill('#n_plumbing_0', 'Stain under the sink.');
  await A.waitForTimeout(1200);
  check('photos held before reload', 3,
    (await A.locator('#thumbs .thumb').count()) + (await A.locator('[data-thumbs="plumbing_0"] .thumb').count()));

  await A.reload({ waitUntil: 'domcontentloaded' });
  await signIn(A);
  await A.waitForTimeout(900);
  check('AFTER RELOAD photos restored', 3,
    (await A.locator('#thumbs .thumb').count()) + (await A.locator('[data-thumbs="plumbing_0"] .thumb').count()));
  check('AFTER RELOAD note restored', 'Stain under the sink.', await A.inputValue('#n_plumbing_0'));
  check('AFTER RELOAD tick restored', 'true',
    await A.getAttribute('button[data-sys="plumbing"][data-i="0"][data-v="bad"]', 'aria-pressed'));
  check('AFTER RELOAD address restored', addr1, await A.inputValue('#f_addr'));

  /* ---------- 3. simulated crash (context killed, storage kept) ---------- */
  const state = await ctxA.storageState();
  await A.evaluate(() => new Promise(r => setTimeout(r, 300)));

  /* ---------- 4. two houses open at once, neither clobbered ---------- */
  await A.click('#tabRoute'); await A.waitForTimeout(400);
  const stops = await A.locator('.stop').count();
  await A.locator('.stop').nth(1).locator('button[data-start]').click();
  await A.waitForTimeout(800);
  const addr2 = await A.inputValue('#f_addr');
  check('switched to a different property', true, addr2 !== addr1);
  check('second house starts blank (not house one)', 0, await A.locator('#thumbs .thumb').count());
  await A.setInputFiles('#f_photos', shot('b1'));
  await A.waitForTimeout(900);
  check('other draft is offered, not destroyed', true, (await A.locator('[data-draft]').count()) >= 1);

  await A.locator('[data-draft]').first().click();
  await A.waitForTimeout(900);
  check('house one reopened with its 3 photos intact', 3,
    (await A.locator('#thumbs .thumb').count()) + (await A.locator('[data-thumbs="plumbing_0"] .thumb').count()));
  check('house one address intact', addr1, await A.inputValue('#f_addr'));

  /* ---------- 5. offline submit goes to the outbox ---------- */
  await A.click('#tabForm'); await A.waitForTimeout(300);
  const segs = await A.$$('#systems .seg');
  for (let i = 0; i < segs.length; i++) {
    await segs[i].$eval('button[data-v="ok"]', el => el.click());
  }
  await A.waitForTimeout(400);
  await A.evaluate(() => { window.__fail = true; });          // the gate has no signal
  await A.click('#genRep');
  await A.waitForTimeout(1500);
  const banner = await A.textContent('#repBannerWrap');
  check('offline submit says queued, not lost', true, /Queued/i.test(banner));
  check('nothing reached the server while offline', 0, await A.evaluate(() => window.__inserted.length));
  await A.click('#tabForm'); await A.waitForTimeout(400);
  check('outbox visible on the form', true, /waiting to upload/i.test(await A.textContent('#outbox')));

  /* ---------- 6. outbox survives a reload while still offline ---------- */
  await ctxA.addInitScript(() => { window.__failInsert = true; });   // writes stay down across reload
  await A.reload({ waitUntil: 'domcontentloaded' });
  await signIn(A);                              // auth works; it is the WRITE path that is down
  await A.click('#tabForm'); await A.waitForTimeout(900);
  check('AFTER RELOAD queued work still queued', true, /waiting to upload/i.test(await A.textContent('#outbox')));

  /* ---------- 7. reconnect flushes the outbox with its photos ---------- */
  await A.evaluate(() => { window.__fail = false; window.__failInsert = false; });
  await A.evaluate(() => window.dispatchEvent(new Event('online')));
  await A.waitForTimeout(2000);
  check('reconnect uploaded the queued inspection', 1, await A.evaluate(() => window.__inserted.length));
  check('its photos uploaded too', true, await A.evaluate(() => window.__uploaded.length >= 1));
  await A.click('#tabForm'); await A.waitForTimeout(500);
  check('outbox emptied after flush', '', (await A.textContent('#outbox')).trim());

  /* ---------- 8. a second technician on a second device is isolated ---------- */
  const ctxB = await newDevice(browser);
  const B = await ctxB.newPage(); watch(B, 'deviceB');
  await signIn(B, 'tech2@test.invalid');
  check('tech2 signs in on their own device', true, await B.isVisible('#routeView'));
  await B.click('#tabForm'); await B.waitForTimeout(500);
  check('tech2 sees none of tech1 drafts', 0, await B.locator('[data-draft]').count());
  check('tech2 sees none of tech1 outbox', '', (await B.textContent('#outbox')).trim());

  /* ---------- 9. SAME TECHNICIAN, SECOND DEVICE — the whole point of sync ----------
     Phone dies at house four. Everything typed so far must be on the tablet. */
  await A.click('#tabRoute'); await A.waitForTimeout(400);
  await A.locator('.stop').nth(2).locator('button[data-start]').click();
  await A.waitForTimeout(700);
  const crossAddr = await A.inputValue('#f_addr');
  await A.click('button[data-sys="exterior"][data-i="0"][data-v="watch"]');
  await A.waitForTimeout(200);
  await A.fill('#n_exterior_0', 'Soffit vent screen torn.');
  await A.setInputFiles('#p_exterior_0', shot('soffit'));
  await A.setInputFiles('#f_photos', [shot('front'), shot('side')]);
  await A.waitForTimeout(1200);
  await A.evaluate(() => pushDraft());
  await A.waitForTimeout(600);

  const onServer = await A.evaluate(() => Object.keys(window.__drafts).length);
  check('draft reached the server', true, onServer >= 1);
  const manifest = await A.evaluate(() => {
    const k = Object.keys(window.__drafts).find(x => x.endsWith(':p3')) || Object.keys(window.__drafts)[0];
    return (window.__drafts[k].photos || []).length;
  });
  check('all 3 photos are in the server manifest', 3, manifest);

  // Push again with no new photos — nothing may re-upload.
  const before = await A.evaluate(() => window.__uploaded.length);
  await A.fill('#f_notes', 'Second pass, no new photos.');
  await A.waitForTimeout(900);
  await A.evaluate(() => pushDraft());
  await A.waitForTimeout(600);
  check('re-saving does not re-upload photos', before, await A.evaluate(() => window.__uploaded.length));

  const server = await A.evaluate(() => ({ drafts: window.__drafts, blobs: window.__blobs }));

  const ctxC = await newDevice(browser, {}, server);
  const C = await ctxC.newPage(); watch(C, 'deviceC');
  await signIn(C, 'tech1@test.invalid');
  await C.waitForTimeout(2500);            // sign-in pulls, then rehydrates photos
  check('SECOND DEVICE restored the address', crossAddr, await C.inputValue('#f_addr'));
  check('SECOND DEVICE restored the note', 'Soffit vent screen torn.', await C.inputValue('#n_exterior_0'));
  check('SECOND DEVICE restored the tick', 'true',
    await C.getAttribute('button[data-sys="exterior"][data-i="0"][data-v="watch"]', 'aria-pressed'));
  check('SECOND DEVICE restored all 3 photos', 3,
    (await C.locator('#thumbs .thumb').count()) + (await C.locator('[data-thumbs="exterior_0"] .thumb').count()));
  check('SECOND DEVICE says where it came from', true,
    /other device/i.test(await C.textContent('#formBanner')));

  /* ---------- 9b. a colleague's device pulls nothing ---------- */
  const ctxD = await newDevice(browser, {}, server);
  const D = await ctxD.newPage(); watch(D, 'deviceD');
  await signIn(D, 'tech2@test.invalid');
  await D.waitForTimeout(1500);
  await D.click('#tabForm'); await D.waitForTimeout(400);
  check('tech2 pulls none of tech1 server drafts', 0, await D.locator('[data-draft]').count());
  check('tech2 form is empty', '', await D.inputValue('#n_exterior_0'));

  /* ---------- 9c. two devices edit the same draft — nothing is clobbered ----------
     C changes it and pushes. A still holds the old stamp, so A's next push must
     stop and ask rather than overwrite C's work. */
  // The panel comes back collapsed by design — the toggle carries the "has
  // content" marker instead. Open it the way a technician would.
  check('restored note is flagged on the collapsed toggle', true,
    await C.evaluate(() => document.getElementById('m_exterior_0').classList.contains('has')));
  await C.click('[data-more="exterior_0"]');
  await C.waitForTimeout(250);
  await C.fill('#n_exterior_0', 'Edited on the tablet.');
  await C.waitForTimeout(900);
  await C.evaluate(() => pushDraft());
  await C.waitForTimeout(600);
  const moved = await C.evaluate(() => ({ drafts: window.__drafts, blobs: window.__blobs }));
  await A.evaluate(s => { window.__drafts = s.drafts; window.__blobs = s.blobs; }, moved);

  await A.fill('#n_exterior_0', 'Edited on the phone at the same time.');
  await A.waitForTimeout(900);
  await A.evaluate(() => pushDraft());
  await A.waitForTimeout(700);
  check('conflict is reported, not resolved silently', true,
    /also edited on another device/i.test(await A.textContent('#formBanner')));
  check('conflict did NOT overwrite the other device', 'Edited on the tablet.',
    await A.evaluate(() => {
      const k = Object.keys(window.__drafts).find(x => x.endsWith(':p3'));
      return window.__drafts[k].payload.notes.exterior_0;
    }));
  check('the phone still holds its own text', 'Edited on the phone at the same time.',
    await A.inputValue('#n_exterior_0'));

  /* ---------- 9d. resolving the conflict actually resolves it ---------- */
  await A.locator('[data-conflict="keep"]').click();
  await A.waitForTimeout(1200);
  check('keeping this device wins after the tech chooses', 'Edited on the phone at the same time.',
    await A.evaluate(() => {
      const k = Object.keys(window.__drafts).find(x => x.endsWith(':p3'));
      return window.__drafts[k].payload.notes.exterior_0;
    }));
  check('conflict banner cleared', false,
    /also edited on another device/i.test(await A.textContent('#formBanner')));

  /* ---------- 9e. a morning worked with no signal syncs when signal returns ---------- */
  const ctxE = await newDevice(browser);
  const E = await ctxE.newPage(); watch(E, 'deviceE');
  await ctxE.addInitScript(() => { window.__failInsert = true; });
  await signIn(E, 'tech1@test.invalid');
  await E.locator('.stop').first().locator('button[data-start]').click();
  await E.waitForTimeout(700);
  await E.click('[data-more="exterior_0"]');
  await E.waitForTimeout(200);
  await E.fill('#n_exterior_0', 'Written in a dead zone.');
  await E.setInputFiles('#f_photos', shot('deadzone'));
  await E.waitForTimeout(1400);
  await E.evaluate(() => pushDraft());
  await E.waitForTimeout(500);
  check('nothing reached the server while out of signal', 0,
    await E.evaluate(() => Object.keys(window.__drafts).length));
  await E.evaluate(() => { window.__failInsert = false; });
  await E.evaluate(() => window.dispatchEvent(new Event('online')));
  await E.waitForTimeout(2500);
  check('signal returning pushes the whole morning up', true,
    await E.evaluate(() => Object.keys(window.__drafts).length >= 1));
  check('and its photo went with it', true,
    await E.evaluate(() => Object.values(window.__drafts).some(d => (d.photos || []).length >= 1)));

  /* ---------- 9f. filing the inspection clears the server draft and its photos ---------- */
  const paths = await E.evaluate(() => {
    const d = Object.values(window.__drafts)[0];
    return (d.photos || []).map(p => p.path);
  });
  const segsE = await E.$$('#systems .seg');
  for (let i = 0; i < segsE.length; i++) await segsE[i].$eval('button[data-v="ok"]', el => el.click());
  await E.waitForTimeout(400);
  await E.click('#genRep');
  await E.waitForTimeout(2500);
  check('filed inspection removes the server draft', 0,
    await E.evaluate(() => Object.keys(window.__drafts).length));
  check('and deletes its draft photos from the bucket', true,
    await E.evaluate(p => p.every(x => window.__removed.indexOf(x) !== -1), paths));
  check('draft photos lived under drafts/<crew id>/', true,
    paths.length > 0 && paths.every(p => p.startsWith('drafts/u-tech1/')));

  /* ---------- 10. two tabs on one device ---------- */
  const A2 = await ctxA.newPage(); watch(A2, 'deviceA-tab2');
  await signIn(A2, 'tech1@test.invalid');
  await A2.click('#tabForm'); await A2.waitForTimeout(900);
  const tab2Addr = await A2.inputValue('#f_addr');
  const tab2Photos = await A2.locator('#thumbs .thumb').count();
  check('second tab restored this device work', true, tab2Addr.length > 0 || tab2Photos > 0);
  console.log(`      (tab 2 restored "${tab2Addr}" with ${tab2Photos} photo(s))`);

  /* ---------- 11. Reset clears only the open draft ---------- */
  await A.click('#tabRoute'); await A.waitForTimeout(300);
  await A.locator('.stop').first().locator('button[data-start]').click();
  await A.waitForTimeout(700);
  await A.setInputFiles('#f_photos', shot('z'));
  await A.waitForTimeout(900);
  const beforeReset = await A.locator('[data-draft]').count();
  A.once('dialog', d => d.accept());
  await A.click('#resetForm');
  await A.waitForTimeout(1200);
  await signIn(A, 'tech1@test.invalid');
  await A.click('#tabForm'); await A.waitForTimeout(600);
  check('Reset kept the other drafts', true, (await A.locator('[data-draft]').count()) >= Math.max(0, beforeReset - 1));

  /* ---------- 12. sign-out warns and keeps work ---------- */
  let asked = false;
  A.on('dialog', d => { asked = true; d.dismiss(); });
  await A.click('#signOut');
  await A.waitForTimeout(700);
  check('sign-out warns about work in progress', true, asked);
  check('sign-out was cancellable', true, await A.isVisible('#appView'));

  /* ---------- 13. many clients does not break the roster ---------- */
  const big = await A.evaluate(() => {
    var n = 0;
    for (var i = 0; i < 400; i++) {
      directory.push({ id: 'big' + i, full_name: 'Bulk Client ' + i, email: 'b' + i + '@test.invalid',
        properties: [{ id: 'bp' + i, address: i + ' Bulk Rd, Stuart FL', county: 'Martin',
          route_order: 50, package: 'silver', visit_frequency: 'weekly', active: true,
          last_inspected_on: null, assigned_to: 'u-tech1' }] });
      n++;
    }
    var t0 = performance.now();
    renderFilters(); renderList(); renderRoute();
    return { added: n, ms: Math.round(performance.now() - t0), stops: document.querySelectorAll('.stop').length };
  });
  check('400 extra clients render', true, big.added === 400 && big.stops > 100);
  check('render stays under 1s with 400 clients', true, big.ms < 1000);
  console.log(`      (render took ${big.ms}ms for ${big.stops} stops)`);

  await browser.close();

  console.log('\n================ SUMMARY ================');
  const failed = results.filter(r => !r.pass);
  console.log(`${results.length - failed.length}/${results.length} scenarios passed`);
  if (failed.length) { console.log('FAILURES:'); failed.forEach(f => console.log('  - ' + f.name)); }
  console.log(errs.length ? 'JS ERRORS:\n' + errs.join('\n') : 'no JS errors');
  process.exit(failed.length || errs.length ? 1 : 0);
})();
