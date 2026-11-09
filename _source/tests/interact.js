const { chromium } = require('playwright');
(async () => {
  const [,, url, actions, out, w, h] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +(w||1600), height: +(h||952) } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file:///home/claude/nm/site/' + url, { waitUntil: 'load' }); await p.waitForTimeout(400);
  for (const a of JSON.parse(actions)) {
    if (a[0] === 'click') await p.click(a[1]);
    else if (a[0] === 'clickn') { const els = await p.$$(a[1]); await els[a[2]].click(); }
    else if (a[0] === 'fill') await p.fill(a[1], a[2]);
    else if (a[0] === 'key') await p.keyboard.press(a[1]);
    else if (a[0] === 'wait') await p.waitForTimeout(a[1]);
    else if (a[0] === 'eval') console.log(await p.evaluate(a[1]));
    await p.waitForTimeout(150);
  }
  await p.screenshot({ path: 'tests/shots/' + out + '.png', fullPage: !!process.env.FULL });
  console.log('errors:', errs.length ? errs : 'none'); await b.close();
})();
