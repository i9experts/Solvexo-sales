// Usage: node render.js -> output/letterhead_print.pdf (page 1 first sheet, page 2 continuation) + previews
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const src = 'file://' + path.join(__dirname, 'letterhead.html');
  const out = f => path.join(__dirname, 'output', f);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto(src, {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: out('letterhead_print.pdf'), width: '216mm', height: '303mm', printBackground: true, preferCSSPageSize: true});
  const pp = await b.newPage({viewport: {width: 816, height: 2400}, deviceScaleFactor: 2});
  await pp.goto(src, {waitUntil: 'networkidle'});
  await pp.evaluate(() => { document.body.classList.add('showguide'); return document.fonts.ready; });
  const pages = await pp.locator('.page').all();
  await pages[0].screenshot({path: out('preview_page1.png')});
  await pages[1].screenshot({path: out('preview_continuation.png')});
  await b.close();
})();
