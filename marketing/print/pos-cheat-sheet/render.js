// Usage: node render.js -> output/pos-cheat-sheet.pdf (front + back) + output/front.png + output/back.png
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const src = 'file://' + path.join(__dirname, 'sheet.html');
  const out = f => path.join(__dirname, 'output', f);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto(src, {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: out('pos-cheat-sheet.pdf'), width: '216mm', height: '154mm', printBackground: true, preferCSSPageSize: true});
  const pp = await b.newPage({viewport: {width: 820, height: 1200}, deviceScaleFactor: 2});
  await pp.goto(src, {waitUntil: 'networkidle'});
  await pp.evaluate(() => document.fonts.ready);
  const pages = await pp.locator('.page').all();
  await pages[0].screenshot({path: out('front.png')});
  await pages[1].screenshot({path: out('back.png')});
  await b.close();
})();
