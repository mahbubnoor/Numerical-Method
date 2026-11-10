// screenshot the picture slide of given lectures with all steps shown (final state) or at a step
const { chromium } = require('playwright');
(async () => {
  const lecs = process.argv[2].split(',').map(Number), step = process.argv[3];
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1130 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  for (const n of lecs) {
    const f = 'L' + String(n).padStart(2, '0');
    await p.goto('file://' + __dirname + '/../site/lectures/' + f + '.html', { waitUntil: 'load' });
    const idx = await p.evaluate(() => [...document.querySelectorAll('section.s')].findIndex(s => s.id === 'picture') + 1);
    await p.goto('file://' + __dirname + '/../site/lectures/' + f + '.html#' + idx, { waitUntil: 'load' }); await p.reload(); await p.waitForTimeout(400);
    await p.evaluate((st) => { const f = document.querySelector('#picture .afig'); f.click(); const n = +f.dataset.n, k = st === undefined ? n : +st;
      f.querySelectorAll('[data-s]').forEach(e => { const a = +e.dataset.s, u = e.dataset.u; e.classList.toggle('on', a <= k && (!u || k < +u)); });
      f.querySelectorAll('.afig-cap span').forEach(e => e.classList.toggle('on', +e.dataset.c === k)); }, step);
    await p.waitForTimeout(1300);
    await p.locator(process.env.FULL ? '#picture' : '#picture .afig').screenshot({ path: __dirname + '/shots/fig_' + f + (step !== undefined ? '_' + step : '') + '.png' });
  }
  console.log('errors', errs); await b.close();
})();
