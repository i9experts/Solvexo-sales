// Usage: node render.js <input.html> <output.pdf> <preview-prefix>
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const [src, pdf, prefix] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(src), {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: path.resolve(pdf), width: '58mm', height: '89.6mm', printBackground: true, preferCSSPageSize: true});
  const pp = await b.newPage({viewport: {width: 260, height: 700}, deviceScaleFactor: 4});
  await pp.goto('file://' + path.resolve(src), {waitUntil: 'networkidle'});
  await pp.evaluate(() => document.fonts.ready);
  await pp.locator('.front').screenshot({path: path.resolve(prefix + '_front.png')});
  await pp.locator('.back').screenshot({path: path.resolve(prefix + '_back.png')});
  await b.close();
})();
