const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: 2 });
  await p.goto('file://' + process.argv[2], { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.addStyleTag({content:'html,body{background:none}'});
  await p.pdf({ path: process.argv[3] + '/First-Rehab-Flyer.pdf', width: '8.5in', height: '11in', printBackground: true, preferCSSPageSize: true });
  const pages = await p.$$('.page');
  const names = ['front','back'];
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: `${process.argv[3]}/flyer-${names[i]}.png` });
  await b.close();
})();
