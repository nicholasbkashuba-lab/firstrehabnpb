// Rack card (4 x 9 in trim). Renders each side WITH 0.125in print bleed (4.25 x 9.25 in) at 400 DPI
// -> <out>/rack-{1,2}.png (1700 x 3700). Canva Print stretches a no-bleed image to cover the bleed,
// which drops it under 300 DPI and crops the top/bottom edges, so the bleed is built in here.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 408, height: 888 }, deviceScaleFactor: 400 / 96 });
  await p.goto('file://' + process.argv[2], { waitUntil: 'networkidle' });
  await p.evaluate(() => document.body.classList.add('bleed'));
  await p.evaluate(() => document.fonts.ready);
  const pages = await p.$$('.page');
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: `${process.argv[3]}/rack-${i + 1}.png` });
  await b.close();
})();
