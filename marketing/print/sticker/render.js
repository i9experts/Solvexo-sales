// Renders the single-sticker PDF, previews, and A4 sticker sheets.
const {chromium} = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const dir = __dirname, out = path.join(dir, 'output');
  fs.mkdirSync(out, {recursive: true});
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.join(dir, 'sticker.html'), {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: path.join(out, 'sticker_single_ring_clean_cutline.pdf'), width: '54.8mm', height: '54.8mm', printBackground: true, preferCSSPageSize: true});
  // previews (cut to the circle)
  const pv = await b.newPage({viewport: {width: 300, height: 300}, deviceScaleFactor: 3});
  await pv.goto('file://' + path.join(dir, 'sticker.html'), {waitUntil: 'networkidle'});
  await pv.evaluate(() => document.fonts.ready);
  for (const id of ['ring', 'clean']) await pv.locator('#' + id).screenshot({path: path.join(out, 'preview_' + id + '.png')});
  // A4 sheets: 3 x 4 stickers per sheet, 2 in circles, 10 mm gaps, centred
  const svgs = await p.evaluate(() => Object.fromEntries(['ring', 'clean'].map(id => [id, document.querySelector('#' + id + ' svg').outerHTML])));
  const head = fs.readFileSync(path.join(dir, 'sticker.html'), 'utf8').match(/<style>[\s\S]*?<\/style>/)[0].replace(/@page\{[^}]*\}/, '@page{size:210mm 297mm;margin:0}');
  for (const id of ['ring', 'clean']) {
    let cells = '';
    for (let r = 0; r < 4; r++) for (let c = 0; c < 3; c++) {
      const x = 22.6 + c * 60.8, y = 26.1 + r * 60.8;  // 50.8 mm + 10 mm gap
      cells += `<div style="position:absolute;left:${x - 2}mm;top:${y - 2}mm;width:54.8mm;height:54.8mm;clip-path:circle(27.4mm)">${svgs[id].replace('<svg ', '<svg style="width:54.8mm;height:54.8mm;display:block" ')}</div>`;
      cells += `<div style="position:absolute;left:${x}mm;top:${y}mm;width:50.8mm;height:50.8mm;border-radius:50%;border:0.2pt solid #FF00FF"></div>`;
    }
    const html = `<!doctype html><html><head><meta charset="utf-8">${head}</head><body><div style="position:relative;width:210mm;height:297mm">${cells}<p style="position:absolute;left:22.6mm;bottom:10mm;font:600 7pt Poppins;color:#999">Solvexo · Powered by sticker · ${id} · 12 per A4 · magenta = cut line (do not print)</p></div></body></html>`;
    const f = path.join(out, 'sheet_' + id + '.html');
    fs.writeFileSync(f, html.replaceAll('href="solvexo-', 'href="../solvexo-').replaceAll('url(../tent-card', 'url(../../tent-card'));
    const sp = await b.newPage();
    await sp.goto('file://' + f, {waitUntil: 'networkidle'});
    await sp.evaluate(() => document.fonts.ready);
    await sp.pdf({path: path.join(out, 'A4_sheet_' + id + '.pdf'), width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true});
  }
  await b.close();
})();
