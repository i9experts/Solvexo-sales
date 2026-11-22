// Usage: node render.js <input.html> <output.pdf> [preview.png]
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const [src, pdf, png] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(src), {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: path.resolve(pdf), width: '158.4mm', height: '158.4mm', printBackground: true, preferCSSPageSize: true});
  if (png) {
    const pp = await b.newPage({viewport: {width: 600, height: 600}, deviceScaleFactor: 2});
    await pp.goto('file://' + path.resolve(src), {waitUntil: 'networkidle'});
    await pp.evaluate(() => document.fonts.ready);
    await pp.locator('.sheet').screenshot({path: path.resolve(png)});
  }
  await b.close();
})();
