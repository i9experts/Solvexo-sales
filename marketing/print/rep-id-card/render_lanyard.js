const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, 'lanyard.html'), {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: path.join(__dirname, 'output', 'lanyard_20mm_tile.pdf'), width: '20mm', height: '450mm', printBackground: true, preferCSSPageSize: true});
  await b.close();
})();
