// Usage: node render.js  -> output/card.pdf (front + back) + output/front.png + output/back.png
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const src = 'file://' + path.join(__dirname, 'card.html');
  const out = f => path.join(__dirname, 'output', f);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto(src, {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: out('card.pdf'), width: '94.9mm', height: '56.8mm', printBackground: true, preferCSSPageSize: true});
  const pp = await b.newPage({viewport: {width: 400, height: 500}, deviceScaleFactor: 4});
  await pp.goto(src, {waitUntil: 'networkidle'});
  await pp.evaluate(() => document.fonts.ready);
  await pp.locator('.front').screenshot({path: out('front.png')});
  await pp.locator('.back').screenshot({path: out('back.png')});
  await b.close();
})();
