// Usage: node render.js -> output/quick-start-guide.pdf (8 pages, reading order) + output/page-N.png previews
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const src = 'file://' + path.join(__dirname, 'guide.html');
  const out = f => path.join(__dirname, 'output', f);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto(src, {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: out('quick-start-guide.pdf'), width: '154mm', height: '216mm', printBackground: true, preferCSSPageSize: true});
  const pp = await b.newPage({viewport: {width: 600, height: 900}, deviceScaleFactor: 2});
  await pp.goto(src, {waitUntil: 'networkidle'});
  await pp.evaluate(() => document.fonts.ready);
  const pages = await pp.locator('.page').all();
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({path: out('page-' + (i + 1) + '.png')});
  await b.close();
})();
