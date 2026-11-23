// Usage: node render.js -> output/setup-checklist.pdf + output/preview.png
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const src = 'file://' + path.join(__dirname, 'checklist.html');
  const out = f => path.join(__dirname, 'output', f);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto(src, {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: out('setup-checklist.pdf'), width: '216mm', height: '303mm', printBackground: true, preferCSSPageSize: true});
  const pp = await b.newPage({viewport: {width: 816, height: 1145}, deviceScaleFactor: 2});
  await pp.goto(src, {waitUntil: 'networkidle'});
  await pp.evaluate(() => document.fonts.ready);
  await pp.locator('.page').screenshot({path: out('preview.png')});
  await b.close();
})();
