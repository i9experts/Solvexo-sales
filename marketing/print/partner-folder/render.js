// Renders each folder part as its own PDF (different sizes) + previews + a closed/open mock-up.
const {chromium} = require('playwright');
const path = require('path');
const parts = [
  {id: 'outside', w: '451mm', h: '316mm'},
  {id: 'inside', w: '451mm', h: '316mm'},
  {id: 'pocket', w: '226mm', h: '106mm'},
];
(async () => {
  const src = 'file://' + path.join(__dirname, 'folder.html');
  const out = f => path.join(__dirname, 'output', f);
  const b = await chromium.launch();
  for (const part of parts) {
    const p = await b.newPage();
    await p.goto(src, {waitUntil: 'networkidle'});
    await p.evaluate(id => {
      document.querySelectorAll('.sheet').forEach(s => { if (s.id !== id) s.remove(); });
      // hide print guides (pocket zone label, card-slot outline) in the print file
      document.querySelectorAll('.pocketzone, .slot').forEach(e => e.style.visibility = 'hidden');
    }, part.id);
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({path: out(`folder_${part.id}.pdf`), width: part.w, height: part.h, printBackground: true});
    await p.close();
  }
  const pp = await b.newPage({viewport: {width: 1800, height: 1300}, deviceScaleFactor: 1});
  await pp.goto(src, {waitUntil: 'networkidle'});
  await pp.evaluate(() => document.fonts.ready);
  for (const part of parts) await pp.locator('#' + part.id).screenshot({path: out(`preview_${part.id}.png`)});
  await b.close();
})();
