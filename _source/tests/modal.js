const { chromium } = require('playwright');
(async () => {
  const [,, page, slide, idx, out] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file:///home/claude/nm/site/lectures/' + page + '#' + slide); await p.waitForTimeout(500);
  await p.keyboard.press('a'); await p.waitForTimeout(200);
  const btns = await p.$$('section:not(.off) .app'); await btns[+idx].click(); await p.waitForTimeout(600);
  const all = await p.$('#modal button.wg-b:has-text("All steps")'); if (all) { await all.click(); await p.waitForTimeout(200); }
  await p.screenshot({ path: 'tests/shots/' + out + '.png' }); console.log('errors', errs); await b.close();
})();
