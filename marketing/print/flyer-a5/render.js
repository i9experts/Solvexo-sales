const {chromium} = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + __dirname + '/flyer.html', {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({path: __dirname + '/flyer.pdf', width: '154mm', height: '216mm', printBackground: true, preferCSSPageSize: true});
  const pp = await b.newPage({viewport: {width: 582, height: 816}, deviceScaleFactor: 2});
  await pp.goto('file://' + __dirname + '/flyer.html', {waitUntil: 'networkidle'});
  await pp.evaluate(() => document.fonts.ready);
  const els = await pp.locator('.page').all();
  for (let i = 0; i < els.length; i++) await els[i].screenshot({path: __dirname + '/side' + (i + 1) + '.png'});
  await b.close();
})();
