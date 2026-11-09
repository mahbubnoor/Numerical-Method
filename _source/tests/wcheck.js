// usage: node tests/wcheck.js '<json list of linsys option objects>'
const { chromium } = require('playwright');
(async () => {
  const cfgs = JSON.parse(process.argv[2]);
  const b = await chromium.launch(); const p = await b.newPage();
  const html = '<!doctype html><html><head><meta charset="utf-8"></head><body>' + cfgs.map(c => `<div data-w="${c.w||'linsys'}" data-o='${JSON.stringify(c).replace(/'/g,"&#39;")}'></div>`).join('') +
    '<script src="file:///home/claude/nm/src/assets/expr.js"></script><script src="file:///home/claude/nm/src/assets/widgets.js"></script><script>Widgets.mountAll()</script></body></html>';
  require('fs').writeFileSync('/tmp/claude-0/-home-claude/2efc50c0-2b79-5d47-94ab-feefdcdd1406/scratchpad/wc.html', html);
  await p.goto('file:///tmp/claude-0/-home-claude/2efc50c0-2b79-5d47-94ab-feefdcdd1406/scratchpad/wc.html');
  const r = await p.evaluate(() => [...document.querySelectorAll('[data-w]')].map(w => {
    const all = [...w.querySelectorAll('button')].find(x => x.textContent === 'All steps'); if (all) all.click();
    const op = w.querySelector('.wg-op'), note = w.querySelector('.wg-note');
    return (op ? op.textContent : '') + ' || ' + (note ? note.textContent : '') + (op ? '' : ' || ' + w.innerText.replace(/\s+/g, ' ').slice(0, 600));
  }));
  r.forEach(x => console.log('---', x)); await b.close();
})();
