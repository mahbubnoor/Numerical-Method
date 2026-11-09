const { chromium } = require('playwright');
(async () => {
  const [,, page, slides, prefix, w, h] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +(w||1600), height: +(h||952) } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  for (const s of slides.split(',')) {
    await p.goto('file:///home/claude/nm/site/' + page + (s ? '#' + s : ''), { waitUntil: 'load' });
    await p.waitForTimeout(400);
    if (s && page.includes('lectures')) { await p.keyboard.press('a'); await p.waitForTimeout(300); }
    await p.screenshot({ path: `tests/shots/${prefix}_${s || 'x'}.png` });
  }
  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
})();
