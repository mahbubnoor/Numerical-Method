/* Live code box: edit Python or C, press Run, see the output. Works offline (MiniPy / MiniC). */
(function (G) {
  'use strict';
  var PYKW = /^(False|None|True|and|as|assert|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)$/;
  var PYBI = /^(print|range|len|abs|min|max|sum|round|int|float|str|list|tuple|dict|zip|enumerate|sorted|reversed|input|math|map|filter|isinstance|pow|any|all|format)$/;
  var CKW = /^(int|long|short|unsigned|signed|char|float|double|void|const|static|if|else|for|while|do|return|break|continue|switch|case|default|sizeof|struct)$/;
  var CBI = /^(printf|scanf|puts|sqrt|pow|exp|log|log10|sin|cos|tan|atan|fabs|floor|ceil|main|M_PI|abs)$/;
  function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function highlight(src, lang) {
    var out = '', i = 0, n = src.length, py = lang === 'py';
    while (i < n) {
      var rest = src.slice(i), m;
      if (py && (m = /^#[^\n]*/.exec(rest))) { out += '<span class="c-cm">' + esc(m[0]) + '</span>'; i += m[0].length; continue; }
      if (!py && (m = /^(\/\/[^\n]*|\/\*[\s\S]*?(\*\/|$))/.exec(rest))) { out += '<span class="c-cm">' + esc(m[0]) + '</span>'; i += m[0].length; continue; }
      if (!py && (m = /^#\s*\w+[^\n]*/.exec(rest)) && (i === 0 || src[i - 1] === '\n')) { out += '<span class="c-pp">' + esc(m[0]) + '</span>'; i += m[0].length; continue; }
      if ((m = py ? /^[rRfFbB]{0,2}("""[\s\S]*?("""|$)|'''[\s\S]*?('''|$)|"(\\.|[^"\\\n])*"?|'(\\.|[^'\\\n])*'?)/.exec(rest) : /^("(\\.|[^"\\\n])*"?|'(\\.|[^'\\\n])*'?)/.exec(rest)) && m[0].length && /["']/.test(m[0])) {
        out += '<span class="c-str">' + esc(m[0]) + '</span>'; i += m[0].length; continue;
      }
      if ((m = /^(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?[fFlL]?/.exec(rest)) && (i === 0 || !/[\w]/.test(src[i - 1]))) { out += '<span class="c-num">' + esc(m[0]) + '</span>'; i += m[0].length; continue; }
      if ((m = /^[A-Za-z_]\w*/.exec(rest))) {
        var w = m[0], cls = py ? (PYKW.test(w) ? 'c-kw' : PYBI.test(w) ? 'c-bi' : '') : (CKW.test(w) ? 'c-kw' : CBI.test(w) ? 'c-bi' : '');
        if (!cls && src[i + w.length] === '(') cls = 'c-fn';
        out += cls ? '<span class="' + cls + '">' + w + '</span>' : w; i += w.length; continue;
      }
      out += esc(src[i]); i++;
    }
    return out + '\n';
  }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }

  function mount(host, opts) {
    opts = opts || {};
    var langs = [];
    if (opts.py !== undefined) langs.push('py');
    if (opts.c !== undefined) langs.push('c');
    var orig = { py: opts.py || '', c: opts.c || '' }, code = { py: orig.py, c: orig.c }, lang = opts.lang && langs.indexOf(opts.lang) >= 0 ? opts.lang : langs[0];
    host.classList.add('runner'); host.setAttribute('data-widget', 'runner');
    host.innerHTML = '';
    var bar = el('div', 'rn-bar'), tabs = el('div', 'rn-tabs');
    langs.forEach(function (L) {
      var b = el('button', 'rn-tab', L === 'py' ? 'Python' : 'C'); b.type = 'button'; b.dataset.lang = L;
      b.addEventListener('click', function () { switchLang(L); }); tabs.appendChild(b);
    });
    bar.appendChild(tabs);
    if (opts.title) bar.appendChild(el('span', 'rn-title', opts.title));
    var sp = el('span', 'rn-sp'); bar.appendChild(sp);
    var runB = el('button', 'rn-run', '▶ Run'); runB.type = 'button'; runB.title = 'Run (Ctrl+Enter)';
    var resetB = el('button', 'rn-btn', '↺ Reset'); resetB.type = 'button'; resetB.title = 'Put the original code back';
    var dlB = el('button', 'rn-btn rn-dl', '⤓'); dlB.type = 'button'; dlB.title = 'Download this code as a file (to run in Jupyter / gcc)';
    bar.appendChild(resetB); bar.appendChild(dlB); bar.appendChild(runB);
    var edWrap = el('div', 'rn-ed'), gutter = el('pre', 'rn-gut'), hl = el('pre', 'rn-hl'), ta = el('textarea', 'rn-ta');
    ta.spellcheck = false; ta.setAttribute('autocapitalize', 'off'); ta.setAttribute('autocomplete', 'off'); ta.setAttribute('aria-label', 'Code editor');
    edWrap.appendChild(gutter); var inner = el('div', 'rn-inner'); inner.appendChild(hl); inner.appendChild(ta); edWrap.appendChild(inner);
    var inWrap = el('div', 'rn-in'), inLab = el('label', '', 'Input'), inTa = el('textarea', 'rn-inta');
    inTa.rows = 1; inTa.spellcheck = false; inTa.value = opts.stdin || ''; inTa.placeholder = 'numbers typed here are read by input() / scanf()';
    inWrap.appendChild(inLab); inWrap.appendChild(inTa);
    var outWrap = el('div', 'rn-out'), outHead = el('div', 'rn-outhead', '<span>Output</span><span class="rn-meta"></span>'), out = el('pre', 'rn-pre');
    outWrap.appendChild(outHead); outWrap.appendChild(out);
    host.appendChild(bar); host.appendChild(edWrap); host.appendChild(inWrap); host.appendChild(outWrap);
    if (opts.edHeight) edWrap.style.height = opts.edHeight;
    if (opts.outHeight) outWrap.style.height = opts.outHeight;
    var errLine = null;
    function render() {
      hl.innerHTML = highlight(ta.value, lang);
      var nl = ta.value.split('\n').length, g = '';
      for (var i = 1; i <= nl; i++) g += (i === errLine ? '<b>' + i + '</b>' : i) + '\n';
      gutter.innerHTML = g;
      var needIn = /\binput\s*\(|scanf\s*\(|getchar\s*\(/.test(ta.value);
      inWrap.style.display = needIn ? '' : 'none';
    }
    function sync() { hl.scrollTop = ta.scrollTop; hl.scrollLeft = ta.scrollLeft; gutter.scrollTop = ta.scrollTop; }
    var started = false;
    function switchLang(L) {
      if (started) code[lang] = ta.value; started = true; lang = L; ta.value = code[L]; errLine = null; out.textContent = ''; out.className = 'rn-pre'; outHead.querySelector('.rn-meta').textContent = '';
      [].forEach.call(tabs.children, function (b) { b.classList.toggle('on', b.dataset.lang === L); });
      dlB.title = 'Download as ' + (L === 'py' ? '.py' : '.c') + ' file';
      render(); sync();
    }
    function run() {
      code[lang] = ta.value;
      var r = lang === 'py' ? G.MiniPy.run(ta.value, { stdin: inTa.value }) : G.MiniC.run(ta.value, { stdin: inTa.value });
      var txt = r.out;
      out.innerHTML = '';
      out.appendChild(document.createTextNode(txt));
      if (r.warnings && r.warnings.length) { var w = el('span', 'rn-warn'); w.textContent = (txt && !/\n$/.test(txt) ? '\n' : '') + r.warnings.join('\n') + '\n'; out.appendChild(w); }
      if (r.error) { var e = el('span', 'rn-err'); e.textContent = (txt && !/\n$/.test(txt) ? '\n' : '') + r.error; out.appendChild(e); }
      if (!txt && !r.error && !(r.warnings && r.warnings.length)) out.appendChild(el('span', 'rn-dim', '(the program printed nothing)'));
      errLine = r.error ? r.line : null; render();
      outHead.querySelector('.rn-meta').textContent = (r.error ? '✗ ' : '✓ ') + (lang === 'py' ? 'Python' : 'C') + ' · ' + (r.ms || 0) + ' ms';
      out.scrollTop = 0;
      if (opts.onRun) opts.onRun(r, lang);
    }
    ta.addEventListener('input', function () { errLine = null; render(); sync(); });
    ta.addEventListener('scroll', sync);
    ta.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey || e.shiftKey) && e.key === 'Enter') { e.preventDefault(); run(); return; }
      if (e.key === 'Tab') {
        e.preventDefault();
        var s = ta.selectionStart, en = ta.selectionEnd, v = ta.value;
        if (s !== en && v.slice(s, en).indexOf('\n') >= 0) {   // indent / outdent block
          var ls = v.lastIndexOf('\n', s - 1) + 1, block = v.slice(ls, en);
          var nb = e.shiftKey ? block.replace(/^ {1,4}/gm, '') : block.replace(/^/gm, '    ');
          ta.value = v.slice(0, ls) + nb + v.slice(en); ta.selectionStart = ls; ta.selectionEnd = ls + nb.length;
        } else if (!e.shiftKey) { ta.value = v.slice(0, s) + '    ' + v.slice(en); ta.selectionStart = ta.selectionEnd = s + 4; }
        render(); return;
      }
      if (e.key === 'Enter') {
        var p = ta.selectionStart, val = ta.value, ls2 = val.lastIndexOf('\n', p - 1) + 1, curLine = val.slice(ls2, p);
        var ind = /^\s*/.exec(curLine)[0];
        if (/[:{]\s*$/.test(curLine)) ind += '    ';
        e.preventDefault();
        ta.value = val.slice(0, p) + '\n' + ind + val.slice(ta.selectionEnd); ta.selectionStart = ta.selectionEnd = p + 1 + ind.length;
        render(); sync(); return;
      }
      if (e.key === '}' && lang === 'c') {
        var p2 = ta.selectionStart, v2 = ta.value, ls3 = v2.lastIndexOf('\n', p2 - 1) + 1;
        if (/^\s+$/.test(v2.slice(ls3, p2))) { e.preventDefault(); var cut = Math.max(ls3, p2 - 4); ta.value = v2.slice(0, cut) + '}' + v2.slice(p2); ta.selectionStart = ta.selectionEnd = cut + 1; render(); }
      }
      e.stopPropagation();
    });
    runB.addEventListener('click', run);
    resetB.addEventListener('click', function () { ta.value = orig[lang]; code[lang] = orig[lang]; errLine = null; render(); sync(); out.textContent = ''; outHead.querySelector('.rn-meta').textContent = ''; });
    dlB.addEventListener('click', function () {
      var name = (opts.file || 'program') + (lang === 'py' ? '.py' : '.c');
      var blob = new Blob([ta.value], { type: 'text/plain' }), a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    });
    switchLang(lang);
    if (opts.autorun) run();
    return { run: run, setCode: function (L, s) { code[L] = s; orig[L] = s; if (L === lang) { ta.value = s; render(); } } };
  }
  function mountAll(root) {
    [].forEach.call((root || document).querySelectorAll('[data-runner]'), function (h) {
      if (h._mounted) return; h._mounted = true;
      var id = h.getAttribute('data-runner'), src = (G.CODE || {})[id] || {};
      mount(h, { py: src.py, c: src.c, stdin: src.stdin, lang: h.getAttribute('data-lang') || undefined, title: h.getAttribute('data-title') || '', file: src.file || id, autorun: h.hasAttribute('data-autorun'),
        edHeight: h.getAttribute('data-ed') || null, outHeight: h.getAttribute('data-out') || null });
    });
  }
  G.Runner = { mount: mount, mountAll: mountAll, highlight: highlight };
})(window);
