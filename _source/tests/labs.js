const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1300, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(p.url().split('/').pop() + ': ' + e.message));
  const files = fs.readdirSync('site/labs').sort();
  for (const f of files) {
    await p.goto('file://' + process.cwd() + '/site/labs/' + f); await p.waitForTimeout(300);
    const nt = await p.$$eval('.tabs button', t => t.length);
    let bad = [];
    for (let i = 0; i < nt; i++) {
      await (await p.$$('.tabs button'))[i].click(); await p.waitForTimeout(350);
      const r = await p.evaluate(i => { const pane = document.querySelectorAll('.pane')[i];
        const w = [...pane.querySelectorAll('[data-w]')].filter(e => !e.classList.contains('wg') || e.textContent.startsWith('Widget error')).length;
        const rn = [...pane.querySelectorAll('[data-runner]')].filter(e => !e.classList.contains('runner') || !e.querySelector('.rn-ta').value.trim()).length;
        return [w, rn]; }, i);
      if (r[0] || r[1]) bad.push('tab ' + i + ': widgets bad ' + r[0] + ', runners bad ' + r[1]);
      // run every runner in this tab, both languages
      const runs = await p.$$('.pane:not([hidden]) .runner');
      for (const rn of runs) {
        const tabs = await rn.$$('.rn-tab');
        for (let t = 0; t < Math.max(1, tabs.length); t++) {
          if (tabs.length) await tabs[t].click();
          await (await rn.$('.rn-run')).click(); await p.waitForTimeout(120);
          const out = await rn.$eval('.rn-pre', e => e.textContent);
          const err = await rn.$('.rn-err, .rn-warn');
          if (err || !out.trim()) bad.push('runner error/empty: ' + (await rn.$eval('.rn-pre', e => e.textContent.slice(0, 120))));
        }
      }
    }
    console.log(f, nt + ' tabs', bad.length ? bad : 'ok');
  }
  console.log('page errors:', errs.length ? errs : 'none'); await b.close();
})();
