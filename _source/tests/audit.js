// Readability audit for every slide (all fragments revealed):
//   SMALL  text whose font is below MIN px on the 1920-wide slide
//   CLASH  text boxes of different elements that overlap each other
//   OUT    text that sticks out of its card / box / column / widget
// usage: node tests/audit.js [L05] [--min=20]
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const args = process.argv.slice(2), only = args.find(a => !a.startsWith('--'));
  const MIN = +((args.find(a => a.startsWith('--min=')) || '--min=20').slice(6));
  const files = fs.readdirSync('site/lectures').filter(f => f.endsWith('.html')).sort();
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1132 } });
  let total = 0; const summary = {};
  for (const f of files) {
    if (only && !f.includes(only)) continue;
    await p.goto('file://' + process.cwd() + '/site/lectures/' + f); await p.waitForTimeout(300);
    const n = await p.evaluate(() => document.querySelectorAll('#stage > section').length);
    for (let i = 1; i <= n; i++) {
      await p.evaluate(i => { location.hash = '#' + i; }, i); await p.waitForTimeout(120);
      await p.keyboard.press('a'); await p.waitForTimeout(300);
      const res = await p.evaluate((MIN) => {
        const sec = [...document.querySelectorAll('#stage > section')].find(s => !s.classList.contains('off'));
        const st = document.getElementById('stage').getBoundingClientRect(), sc = st.width / 1920;
        const R = r => ({ l: (r.left - st.left) / sc, t: (r.top - st.top) / sc, r: (r.right - st.left) / sc, b: (r.bottom - st.top) / sc });
        const out = [], items = [];
        const vis = el => { for (let e = el; e && e !== sec; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false; } return true; };
        // text items: KaTeX formulas as one box; other text nodes per line rect
        sec.querySelectorAll('.katex').forEach(k => {
          if (k.closest('.foot') || !vis(k)) return; if (k.parentElement.closest('.katex')) return;
          const r = k.getBoundingClientRect(); if (!r.width) return;
          const html = k.querySelector('.katex-html') || k, fsk = parseFloat(getComputedStyle(k).fontSize), t = '[math] ' + ((k.querySelector('annotation') || k).textContent || '').slice(0, 34);
          const bases = html.querySelectorAll(':scope > .base');
          (bases.length ? [...bases] : [html]).forEach(bs => { const rr = bs.getBoundingClientRect(); if (rr.width > 1) items.push({ el: k, box: R(rr), fs: fsk, txt: t }); });
        });
        const tw = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = tw.nextNode())) {
          const s = node.textContent.trim(); if (!s) continue;
          const el = node.parentElement;
          if (!el || /^(SUB|SUP)$/.test(el.tagName) || el.closest('.katex') || el.closest('.foot') || el.closest('template') || el.closest('svg.deco') || el.closest('.rn-hl') || el.closest('.rn-gut') || el.closest('textarea') || el.closest('option') || el.closest('select')) continue;
          if (!vis(el)) continue;
          const rg = document.createRange(); rg.selectNodeContents(node);
          [...rg.getClientRects()].forEach(r => { if (r.width > 1 && r.height > 1) items.push({ el, box: R(r), fs: parseFloat(getComputedStyle(el).fontSize), txt: s.slice(0, 40) }); });
        }
        // SMALL
        const small = {};
        items.forEach(it => { if (it.fs < MIN - 0.01) { const k = (it.el.className && it.el.className.baseVal === undefined ? it.el.className : it.el.tagName) + ' ' + it.fs.toFixed(1) + 'px'; small[k] = small[k] || it.txt; } });
        Object.keys(small).slice(0, 6).forEach(k => out.push('SMALL ' + k + ' "' + small[k] + '"'));
        // CLASH: overlapping text from different elements (not nested in each other)
        const ov = (a, c) => Math.max(0, Math.min(a.r, c.r) - Math.max(a.l, c.l)) * Math.max(0, Math.min(a.b, c.b) - Math.max(a.t, c.t));
        let clashes = 0;
        for (let x = 0; x < items.length && clashes < 4; x++) for (let y = x + 1; y < items.length && clashes < 4; y++) {
          const A = items[x], B = items[y];
          if (A.el === B.el || A.el.contains(B.el) || B.el.contains(A.el)) continue;
          const area = ov(A.box, B.box), minA = Math.min((A.box.r - A.box.l) * (A.box.b - A.box.t), (B.box.r - B.box.l) * (B.box.b - B.box.t));
          if (area > 30 && area > 0.12 * minA) { out.push('CLASH "' + A.txt + '" × "' + B.txt + '"'); clashes++; }
        }
        // OUT: text outside its nearest container
        const C = '.card, .eqbox, .qbox, .answer, .opts > div, .wg, .runner, .app, .br, .steps > div, .ml, td, th';
        let outs = 0;
        items.forEach(it => {
          if (outs >= 4) return;
          const c = it.el.closest(C); if (!c || !sec.contains(c)) return;
          const cb = R(c.getBoundingClientRect()), bx = it.box, tol = 3;
          if (bx.r > cb.r + tol || bx.l < cb.l - tol || bx.b > cb.b + tol || bx.t < cb.t - tol) { out.push('OUT "' + it.txt + '" from ' + c.className.toString().split(' ')[0] + ' by ' + Math.round(Math.max(bx.r - cb.r, cb.l - bx.l, bx.b - cb.b, cb.t - bx.t)) + 'px'); outs++; }
        });
        sec.querySelectorAll('.katex-display').forEach(d => { const f = parseFloat(d.style.fontSize || '1'); if (d.style.fontSize && f < 0.8) out.push('SHRUNK x' + f.toFixed(2) + ' "' + ((d.querySelector('annotation') || d).textContent || '').slice(0, 50) + '"'); });
        // and anything past the slide's safe area
        items.forEach(it => { if (it.box.r > 1922 || it.box.b > 1034) out.push('EDGE "' + it.txt + '"'); });
        return [sec.id, out.slice(0, 12)];
      }, MIN);
      if (res[1].length) { total++; console.log(f + ' #' + i + ' ' + res[0]); res[1].forEach(x => { console.log('   ' + x); const k = x.split(' ')[0]; summary[k] = (summary[k] || 0) + 1; }); }
    }
  }
  console.log('slides with findings: ' + total, JSON.stringify(summary));
  await b.close();
})();
