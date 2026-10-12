// Rack card (4 x 9 in): 300 DPI PNG per side -> flyer/rack-{1,2}.png. Canva gets these flattened.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 384, height: 864 }, deviceScaleFactor: 3.125 });
  await p.goto('file://' + process.argv[2], { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const pages = await p.$$('.page');
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: `${process.argv[3]}/rack-${i + 1}.png` });
  await b.close();
})();
