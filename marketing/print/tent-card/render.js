// Usage: node render.js <input.html> <output.pdf> <preview.png>
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const [src, pdf, png] = process.argv.slice(2).map(p => path.resolve(p));
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + src, {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: pdf, width: '111mm', height: '302mm', printBackground: true, preferCSSPageSize: true});
  if (png) {
    const pp = await b.newPage({viewport: {width: 420, height: 1142}, deviceScaleFactor: 2});
    await pp.goto('file://' + src, {waitUntil: 'networkidle'});
    await pp.evaluate(() => document.fonts.ready);
    await pp.locator('.sheet').screenshot({path: png});
  }
  await b.close();
})();
