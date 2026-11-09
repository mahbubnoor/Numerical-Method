const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1140, height: 900 } });
  const errs=[]; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.goto('file:///home/claude/nm/tests/wtest.html'); await p.waitForTimeout(500);
  // click "All steps" on every linsys
  const r = await p.evaluate(() => {
    const out=[];
    document.querySelectorAll('.wg-linsys').forEach(w => { const bs=[...w.querySelectorAll('button')]; bs.find(x=>x.textContent==='All steps').click(); out.push(w.querySelector('.wg-op').textContent + ' || ' + w.querySelector('.wg-note').textContent); });
    document.querySelectorAll('.wg-cramer,.wg-cost,.wg-iter2d,.wg-plate').forEach(w=>out.push(w.innerText.slice(0,400).replace(/\s+/g,' ')));
    return out; });
  r.forEach(x=>console.log('---',x));
  await p.screenshot({ path: 'tests/shots/wtest.png', fullPage: true });
  console.log('errors', errs); await b.close();
})();
