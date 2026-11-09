// For every slide: reveal all fragments, report elements that overflow the 1920x1032 safe area.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const files = fs.readdirSync('site/lectures').filter(f => f.endsWith('.html')).sort();
  const only = process.argv[2]; const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1132 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  let problems = 0;
  for (const f of files) {
    if (only && !f.includes(only)) continue;
    await p.goto('file://' + process.cwd() + '/site/lectures/' + f); await p.waitForTimeout(300);
    const n = await p.evaluate(() => document.querySelectorAll('#stage > section').length);
    for (let i = 1; i <= n; i++) {
      await p.evaluate(i => { location.hash = '#' + i; }, i); await p.waitForTimeout(120);
      await p.keyboard.press('a'); await p.waitForTimeout(250);
      const bad = await p.evaluate(() => {
        const sec = [...document.querySelectorAll('#stage > section')].find(s => !s.classList.contains('off'));
        const st = document.getElementById('stage').getBoundingClientRect(), sc = st.width / 1920;
        const out = [];
        sec.querySelectorAll('*').forEach(el => {
          if (el.closest('.foot') || el.closest('svg.deco') || el.closest('.wg-scroll') || el.closest('.rn-pre') || el.closest('.rn-hl') || el.closest('.rn-ta') || el.closest('.rn-gut') || el.closest('.katex')) return;
          const r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
          const bottom = (r.bottom - st.top) / sc, right = (r.right - st.left) / sc;
          if (bottom > 1034 || right > 1922) out.push(el.tagName + '.' + (el.className.baseVal !== undefined ? el.className.baseVal : el.className) + ' b=' + Math.round(bottom) + ' r=' + Math.round(right) + ' "' + (el.textContent || '').trim().slice(0, 40) + '"');
        });
        sec.querySelectorAll('.cols, .col, .grid, .card, .qbox, .steps, .live, .eqbox, .answer').forEach(el => {
          if (el.closest('.foot')) return;
          if (el.scrollHeight > el.clientHeight + 24) out.push('SQUASHED ' + el.className + ' content ' + el.scrollHeight + ' > box ' + el.clientHeight);
          if (el.matches('.eqbox, .card, .qbox, .answer') && el.scrollWidth > el.clientWidth + 6) out.push('WIDE ' + el.className + ' content ' + el.scrollWidth + ' > box ' + el.clientWidth);
        });
        return [sec.id, out.slice(0, 3)];
      });
      if (bad[1].length) { problems++; console.log(f, '#' + i, bad[0], '\n   ' + bad[1].join('\n   ')); }
    }
  }
  console.log('slides with overflow:', problems, ' page errors:', errs.length ? errs.slice(0, 5) : 'none');
  await b.close();
})();
