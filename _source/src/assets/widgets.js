/* Interactive widgets for the Numerical Methods course. Each widget: W[name](host, opts).
   Shared helpers: Plot (canvas charts), ui (controls), fmt (number display). */
(function (G) {
  'use strict';
  var W = {};
  /* ------------------------------------------------------------- helpers */
  function css(el, name, def) { var v = getComputedStyle(el).getPropertyValue(name).trim(); return v || def; }
  function h(tag, attrs, kids) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === 'class') e.className = attrs[k]; else if (k === 'html') e.innerHTML = attrs[k]; else if (k === 'text') e.textContent = attrs[k];
      else if (k.slice(0, 2) === 'on') e.addEventListener(k.slice(2), attrs[k]); else if (k === 'style') e.style.cssText = attrs[k]; else e.setAttribute(k, attrs[k]);
    }
    (kids || []).forEach(function (c) { if (c != null) e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return e;
  }
  function fmt(x, d) {
    if (x === undefined || x === null) return '';
    if (typeof x !== 'number') return String(x);
    if (!isFinite(x)) return x !== x ? 'NaN' : (x > 0 ? '∞' : '−∞');
    d = d === undefined ? 6 : d;
    var a = Math.abs(x);
    if (a !== 0 && (a < Math.pow(10, -d + 1) / 10 || a >= 1e9)) return x.toExponential(Math.min(d, 4)).replace('-', '−').replace('e−', 'e−').replace('e+', 'e+');
    return x.toFixed(d).replace('-', '−');
  }
  function sci(x, d) { if (!isFinite(x)) return fmt(x); if (x === 0) return '0'; return x.toExponential(d === undefined ? 2 : d).replace('-', '−').replace('e-', 'e−'); }
  function num(input, def) { var v = parseFloat(String(input.value).replace('−', '-')); return isFinite(v) ? v : def; }
  function field(label, value, opts) {
    opts = opts || {};
    var inp = h('input', { type: opts.type || 'text', value: value, 'aria-label': label, class: opts.wide ? 'wide' : '' });
    if (opts.size) inp.style.width = opts.size;
    var lab = h('label', { class: 'wg-f' }, [h('span', { html: label }), inp]);
    return { el: lab, input: inp };
  }
  function slider(label, min, max, step, value, onInput, show) {
    var inp = h('input', { type: 'range', min: min, max: max, step: step, value: value, 'aria-label': label.replace(/<[^>]+>/g, '') });
    var out = h('output', { html: show ? show(+value) : String(value) });
    var lab = h('label', { class: 'wg-s' }, [h('span', { html: label }), inp, out]);
    function upd() { out.innerHTML = show ? show(+inp.value) : inp.value; if (onInput) onInput(+inp.value); }
    inp.addEventListener('input', upd);
    return { el: lab, input: inp, update: upd, get value() { return +inp.value; } };
  }
  function btn(label, onclick, cls) { return h('button', { type: 'button', class: 'wg-b ' + (cls || ''), html: label, onclick: onclick }); }
  function select(label, options, value, onchange) {
    var s = h('select', { 'aria-label': label });
    options.forEach(function (o) { var op = h('option', { value: o[0], html: o[1] }); if (o[0] === value) op.selected = true; s.appendChild(op); });
    s.addEventListener('change', function () { onchange(s.value); });
    return { el: h('label', { class: 'wg-f' }, [h('span', { html: label }), s]), input: s };
  }
  function tex(s) { if (G.katex) { try { return G.katex.renderToString(s, { throwOnError: false }); } catch (e) {} } return s.replace(/\\cdot/g, '·').replace(/[{}\\]/g, ''); }

  /* ------------------------------------------------------------- Plot */
  function Plot(host, o) {
    o = o || {};
    this.host = host; this.o = o;
    this.cv = h('canvas', { class: 'wg-cv', role: 'img', 'aria-label': o.label || 'chart' });
    host.appendChild(this.cv);
    this.ctx = this.cv.getContext('2d');
    this.x0 = o.xmin === undefined ? -1 : o.xmin; this.x1 = o.xmax === undefined ? 1 : o.xmax;
    this.y0 = o.ymin === undefined ? -1 : o.ymin; this.y1 = o.ymax === undefined ? 1 : o.ymax;
    var self = this;
    if (G.ResizeObserver) new ResizeObserver(function () { if (self.onresize) self.onresize(); }).observe(this.cv);
  }
  Plot.prototype.begin = function () {
    var cv = this.cv, r = cv.getBoundingClientRect(), w = cv.clientWidth || 600, hh = cv.clientHeight || 360;
    var scale = r.width && w ? r.width / w : 1, dpr = (G.devicePixelRatio || 1) * scale;
    if (dpr < 1) dpr = 1;
    cv.width = Math.round(w * dpr); cv.height = Math.round(hh * dpr);
    var c = this.ctx; c.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.W = w; this.H = hh;
    this.fs = parseFloat(css(this.host, '--w-fs', '14')) || 14;
    var fs = this.fs;
    this.pad = { l: this.o.padL || fs * 4.2, r: fs * 1.2, t: fs * 1.2, b: fs * 2.6 };
    this.col = { ink: css(this.host, '--w-ink', '#1d2733'), mut: css(this.host, '--w-mut', '#5b6672'), grid: css(this.host, '--w-grid', '#e5e8eb'), bg: css(this.host, '--w-plot', '#ffffff'),
      c1: css(this.host, '--w-c1', '#2f6db5'), c2: css(this.host, '--w-c2', '#b85712'), c3: css(this.host, '--w-c3', '#2e7d4f'), c4: css(this.host, '--w-c4', '#7b3fb8'), c5: css(this.host, '--w-c5', '#c0392b') };
    c.fillStyle = this.col.bg; c.fillRect(0, 0, w, hh);
    return c;
  };
  Plot.prototype.range = function (x0, x1, y0, y1) { this.x0 = x0; this.x1 = x1; this.y0 = y0; this.y1 = y1; };
  Plot.prototype.X = function (x) { return this.pad.l + (x - this.x0) / (this.x1 - this.x0) * (this.W - this.pad.l - this.pad.r); };
  Plot.prototype.Y = function (y) { if (this.o.logy) y = Math.log10(Math.max(y, 1e-300)); return this.H - this.pad.b - (y - this.y0) / (this.y1 - this.y0) * (this.H - this.pad.t - this.pad.b); };
  Plot.prototype.invX = function (px) { return this.x0 + (px - this.pad.l) / (this.W - this.pad.l - this.pad.r) * (this.x1 - this.x0); };
  function nice(span, n) {
    var raw = span / n, p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p;
    return (m < 1.5 ? 1 : m < 3 ? 2 : m < 7 ? 5 : 10) * p;
  }
  function tickLabel(v, step) {
    if (Math.abs(v) < step * 1e-6) return '0';
    var d = Math.max(0, -Math.floor(Math.log10(step) + 1e-9));
    if (Math.abs(v) >= 1e5 || (Math.abs(v) < 1e-3)) return v.toExponential(1).replace('-', '−');
    return v.toFixed(d).replace('-', '−');
  }
  Plot.prototype.axes = function (xl, yl) {
    var c = this.ctx, self = this, fs = this.fs;
    c.save(); c.font = (fs * 0.98) + 'px ' + css(this.host, '--w-font', 'IBM Plex Sans, system-ui, sans-serif');
    c.lineWidth = 1;
    var xs = this.o.xstep || nice(this.x1 - this.x0, Math.max(3, Math.round(this.W / (fs * 6)))), ys = nice(this.y1 - this.y0, Math.max(3, Math.round(this.H / (fs * 3.2))));
    if (this.o.logy) ys = Math.max(1, Math.round(ys));
    c.strokeStyle = this.col.grid; c.fillStyle = this.col.mut; c.textAlign = 'center'; c.textBaseline = 'top';
    for (var x = Math.ceil(this.x0 / xs) * xs; x <= this.x1 + xs * 1e-9; x += xs) {
      var px = this.X(x); c.beginPath(); c.moveTo(px, this.pad.t); c.lineTo(px, this.H - this.pad.b); c.stroke();
      c.fillText(this.o.xfmt ? this.o.xfmt(x) : tickLabel(x, xs), px, this.H - this.pad.b + fs * 0.35);
    }
    c.textAlign = 'right'; c.textBaseline = 'middle';
    for (var y = Math.ceil(this.y0 / ys) * ys; y <= this.y1 + ys * 1e-9; y += ys) {
      var py = this.H - this.pad.b - (y - this.y0) / (this.y1 - this.y0) * (this.H - this.pad.t - this.pad.b);
      c.beginPath(); c.moveTo(this.pad.l, py); c.lineTo(this.W - this.pad.r, py); c.stroke();
      c.fillText(this.o.logy ? '1e' + Math.round(y) : (this.o.yfmt ? this.o.yfmt(y) : tickLabel(y, ys)), this.pad.l - fs * 0.4, py);
    }
    c.strokeStyle = this.col.mut; c.lineWidth = 1.4;
    if (!this.o.logy && this.y0 < 0 && this.y1 > 0) { var zy = this.Y(0); c.beginPath(); c.moveTo(this.pad.l, zy); c.lineTo(this.W - this.pad.r, zy); c.stroke(); }
    if (this.x0 < 0 && this.x1 > 0) { var zx = this.X(0); c.beginPath(); c.moveTo(zx, this.pad.t); c.lineTo(zx, this.H - this.pad.b); c.stroke(); }
    c.fillStyle = this.col.ink;
    if (xl) { c.textAlign = 'right'; c.textBaseline = 'bottom'; c.fillText(xl, this.W - this.pad.r, this.H - this.pad.b - fs * 0.3); }
    if (yl) { c.textAlign = 'left'; c.textBaseline = 'top'; c.fillText(yl, this.pad.l + fs * 0.4, this.pad.t + fs * 0.2); }
    c.restore();
  };
  Plot.prototype.clip = function () { var c = this.ctx; c.save(); c.beginPath(); c.rect(this.pad.l, this.pad.t, this.W - this.pad.l - this.pad.r, this.H - this.pad.t - this.pad.b); c.clip(); };
  Plot.prototype.unclip = function () { this.ctx.restore(); };
  Plot.prototype.fn = function (f, color, width, dash) {
    var c = this.ctx, n = Math.max(200, Math.round(this.W)), started = false, lastY = null;
    this.clip(); c.strokeStyle = color; c.lineWidth = width || 2.5; c.setLineDash(dash || []); c.beginPath();
    for (var i = 0; i <= n; i++) {
      var x = this.x0 + (this.x1 - this.x0) * i / n, y;
      try { y = f(x); } catch (e) { y = NaN; }
      if (!isFinite(y)) { started = false; continue; }
      var py = this.Y(y);
      if (started && lastY !== null && Math.abs(py - lastY) > this.H * 3) started = false;
      if (!started) { c.moveTo(this.X(x), py); started = true; } else c.lineTo(this.X(x), py);
      lastY = py;
    }
    c.stroke(); c.setLineDash([]); this.unclip();
  };
  Plot.prototype.poly = function (pts, color, width, dash, close, fill) {
    var c = this.ctx; this.clip(); c.beginPath();
    pts.forEach(function (p, i) { var X = this.X(p[0]), Y = this.Y(p[1]); if (i) c.lineTo(X, Y); else c.moveTo(X, Y); }, this);
    if (close) c.closePath();
    if (fill) { c.fillStyle = fill; c.fill(); }
    if (color) { c.strokeStyle = color; c.lineWidth = width || 2; c.setLineDash(dash || []); c.stroke(); c.setLineDash([]); }
    this.unclip();
  };
  Plot.prototype.seg = function (x1, y1, x2, y2, color, width, dash) { this.poly([[x1, y1], [x2, y2]], color, width, dash); };
  Plot.prototype.dot = function (x, y, r, color, hollow) {
    var c = this.ctx, X = this.X(x), Y = this.Y(y); if (!isFinite(X) || !isFinite(Y)) return;
    c.beginPath(); c.arc(X, Y, r || 5, 0, 7);
    if (hollow) { c.fillStyle = this.col.bg; c.fill(); c.strokeStyle = color; c.lineWidth = 2.5; c.stroke(); } else { c.fillStyle = color; c.fill(); }
  };
  Plot.prototype.label = function (x, y, s, color, align, dy, bold) {
    var c = this.ctx; c.save(); c.font = (bold ? '600 ' : '') + this.fs + 'px ' + css(this.host, '--w-font', 'IBM Plex Sans, system-ui, sans-serif');
    c.fillStyle = color || this.col.ink; c.textAlign = align || 'left'; c.textBaseline = 'bottom';
    var X = typeof x === 'string' ? parseFloat(x) : this.X(x), Y = typeof y === 'string' ? parseFloat(y) : this.Y(y);
    c.fillText(s, X, Y + (dy || 0)); c.restore();
  };
  Plot.prototype.vband = function (a, b, color) {
    var c = this.ctx; this.clip(); c.fillStyle = color; c.fillRect(this.X(a), this.pad.t, this.X(b) - this.X(a), this.H - this.pad.t - this.pad.b); this.unclip();
  };
  Plot.prototype.legend = function (items) {
    var c = this.ctx, fs = this.fs, x = this.pad.l + fs * 0.8, y = this.pad.t + fs * 0.6;
    c.save(); c.font = (fs * 1.0) + 'px ' + css(this.host, '--w-font', 'IBM Plex Sans, system-ui, sans-serif'); c.textBaseline = 'middle';
    var wmax = 0; items.forEach(function (it) { wmax = Math.max(wmax, c.measureText(it[0]).width); });
    c.fillStyle = this.col.bg; c.globalAlpha = 0.88; c.fillRect(x - fs * 0.5, y - fs * 0.6, wmax + fs * 3.4, items.length * fs * 1.45 + fs * 0.2); c.globalAlpha = 1;
    items.forEach(function (it, i) {
      var yy = y + i * fs * 1.45 + fs * 0.3;
      c.strokeStyle = it[1]; c.lineWidth = 3; c.setLineDash(it[2] || []); c.beginPath(); c.moveTo(x, yy); c.lineTo(x + fs * 1.8, yy); c.stroke(); c.setLineDash([]);
      c.fillStyle = this.col.ink; c.fillText(it[0], x + fs * 2.3, yy);
    }, this);
    c.restore();
  };
  function autoRange(f, x0, x1, pts) {
    var lo = Infinity, hi = -Infinity, vals = [];
    for (var i = 0; i <= 200; i++) { var x = x0 + (x1 - x0) * i / 200, y; try { y = f(x); } catch (e) { y = NaN; } if (isFinite(y)) vals.push(y); }
    (pts || []).forEach(function (y) { if (isFinite(y)) vals.push(y); });
    vals.sort(function (a, b) { return a - b; });
    if (!vals.length) return [-1, 1];
    lo = vals[Math.floor(vals.length * 0.02)]; hi = vals[Math.ceil(vals.length * 0.98) - 1];
    if (pts) pts.forEach(function (y) { if (isFinite(y)) { lo = Math.min(lo, y); hi = Math.max(hi, y); } });
    if (lo > 0) lo = Math.min(0, lo); if (hi < 0) hi = Math.max(0, hi);
    if (hi - lo < 1e-9) { hi += 1; lo -= 1; }
    var m = (hi - lo) * 0.08; return [lo - m, hi + m];
  }
  function card(host, cls) { host.classList.add('wg'); if (cls) host.classList.add(cls); host.setAttribute('data-widget', 'w'); host.innerHTML = ''; return host; }
  function row(kids, cls) { return h('div', { class: 'wg-row ' + (cls || '') }, kids); }
  function table(headers, rows, opts) {
    opts = opts || {};
    var t = h('table', { class: 'wg-t' }), th = h('tr');
    headers.forEach(function (x) { th.appendChild(h('th', { html: x })); });
    t.appendChild(h('thead', null, [th]));
    var tb = h('tbody');
    rows.forEach(function (r, i) {
      var tr = h('tr', { class: (opts.hi === i ? 'hi' : '') + (r.cls ? ' ' + r.cls : '') });
      (r.cells || r).forEach(function (cval) { tr.appendChild(h('td', { html: cval })); });
      tb.appendChild(tr);
    });
    t.appendChild(tb);
    return t;
  }
  function errBox(msg) { return h('div', { class: 'wg-err', text: msg }); }
  function redrawOnTheme(f) { G.addEventListener('nm-theme', f); }
  W._h = { h: h, fmt: fmt, sci: sci, Plot: Plot, field: field, slider: slider, btn: btn, select: select, table: table, row: row, card: card, autoRange: autoRange, tex: tex, num: num };

  /* ============================================================= L1: iteration machine (Babylonian square root) */
  W.babylon = function (host, o) {
    card(host, 'wg-babylon');
    var N = field('Number N', o.N || 2, { size: '6em' }), x0 = field('Guess x<sub>0</sub>', o.x0 || 1, { size: '6em' });
    var out = h('div', { class: 'wg-scroll' }), note = h('p', { class: 'wg-note' });
    var k = 1;
    function draw() {
      var n = num(N.input, 2), x = num(x0.input, 1), rows = [], exact = Math.sqrt(n);
      if (n <= 0 || x <= 0) { out.innerHTML = ''; out.appendChild(errBox('Use N > 0 and x0 > 0')); return; }
      rows.push([0, x.toFixed(15), sci(Math.abs(x - exact), 2), digits(x, exact)]);
      for (var i = 1; i <= k; i++) { x = 0.5 * (x + n / x); rows.push([i, x.toFixed(15), sci(Math.abs(x - exact), 2), digits(x, exact)]); }
      out.innerHTML = ''; out.appendChild(table(['k', 'x<sub>k</sub> = ½(x<sub>k−1</sub> + N / x<sub>k−1</sub>)', '|error|', 'correct digits'], rows, { hi: rows.length - 1 }));
      note.innerHTML = '√' + n + ' = ' + exact.toFixed(15) + ' (from the computer\'s own sqrt). Each step roughly <b>doubles</b> the number of correct digits.';
    }
    function digits(x, ex) { var e = Math.abs(x - ex) / Math.abs(ex); if (e === 0) return '<b>16 (all)</b>'; var d = Math.max(0, Math.floor(-Math.log10(e))); return '<span class="bar" style="width:' + (d * 0.9) + 'em"></span> ' + d; }
    host.appendChild(row([N.el, x0.el, btn('Next step ▶', function () { if (k < 8) k++; draw(); }, 'pri'), btn('Reset', function () { k = 1; draw(); })]));
    host.appendChild(out); host.appendChild(note);
    [N.input, x0.input].forEach(function (i) { i.addEventListener('input', draw); });
    draw();
  };

  /* ============================================================= L2: IEEE 754 bit explorer */
  function exactDecimal(x) {   // exact decimal expansion of a double (string)
    if (!isFinite(x)) return String(x);
    if (x === 0) return '0';
    var dv = new DataView(new ArrayBuffer(8)); dv.setFloat64(0, Math.abs(x));
    var hi = dv.getUint32(0), lo = dv.getUint32(4), ex = (hi >>> 20) & 0x7ff, man = (BigInt(hi & 0xfffff) << 32n) | BigInt(lo);
    var M = ex === 0 ? man : man | (1n << 52n), E = ex === 0 ? -1074 : ex - 1075, s;
    if (E >= 0) s = (M << BigInt(E)).toString();
    else { var digits = (M * (5n ** BigInt(-E))).toString(), k = -E; while (digits.length <= k) digits = '0' + digits; s = digits.slice(0, digits.length - k) + '.' + digits.slice(digits.length - k); s = s.replace(/0+$/, '').replace(/\.$/, ''); }
    return (x < 0 ? '-' : '') + s;
  }
  W._exactDecimal = exactDecimal;
  W.fpbits = function (host, o) {
    card(host, 'wg-fpbits');
    var prec = o.prec || 'single';
    var inp = field('Decimal number', o.value || '0.1', { size: '9em' });
    var sel = select('Format', [['single', 'single (float, 32-bit)'], ['double', 'double (64-bit)']], prec, function (v) { prec = v; draw(); });
    var presets = row(['0.1', '0.5', '1/3', '-6.25', '1e-8', '16777217', '0.1+0.2'].map(function (p) { return btn(p, function () { inp.input.value = p; draw(); }, 'chip'); }), 'wg-chips');
    var bits = h('div', { class: 'wg-bits' }), info = h('div', { class: 'wg-info' });
    host.appendChild(row([inp.el, sel.el])); host.appendChild(presets); host.appendChild(bits); host.appendChild(info);
    inp.input.addEventListener('input', draw);
    function parseVal(s) {
      s = s.replace(/\s/g, '').replace('−', '-');
      var m = /^(-?[\d.eE+-]+)\/([\d.eE+-]+)$/.exec(s); if (m) return parseFloat(m[1]) / parseFloat(m[2]);
      m = /^(-?[\d.eE]+)\+([\d.eE]+)$/.exec(s); if (m) return parseFloat(m[1]) + parseFloat(m[2]);
      var v = Number(s); return v;
    }
    function draw() {
      var v = parseVal(inp.input.value);
      bits.innerHTML = ''; info.innerHTML = '';
      if (!isFinite(v) && inp.input.value.trim() !== 'Infinity') { bits.appendChild(errBox('Type a number such as 0.1, 1/3 or 6.02e23')); return; }
      var single = prec === 'single', eb = single ? 8 : 11, mb = single ? 23 : 52, bias = single ? 127 : 1023;
      var stored = single ? Math.fround(v) : v;
      var dv = new DataView(new ArrayBuffer(8)), bitstr = '';
      if (single) { dv.setFloat32(0, stored); var u = dv.getUint32(0); bitstr = u.toString(2).padStart(32, '0'); }
      else { dv.setFloat64(0, stored); bitstr = dv.getUint32(0).toString(2).padStart(32, '0') + dv.getUint32(4).toString(2).padStart(32, '0'); }
      var s = bitstr[0], e = bitstr.slice(1, 1 + eb), m = bitstr.slice(1 + eb);
      function grp(str, cls, title) {
        var d = h('div', { class: 'wg-bitgrp ' + cls }), lab = h('div', { class: 'wg-bitlab', html: title }), cells = h('div', { class: 'wg-bitcells' });
        for (var i = 0; i < str.length; i++) cells.appendChild(h('span', { class: str[i] === '1' ? 'one' : '', text: str[i] }));
        d.appendChild(lab); d.appendChild(cells); return d;
      }
      bits.appendChild(grp(s, 'sgn', 'sign')); bits.appendChild(grp(e, 'exp', 'exponent (' + eb + ' bits)')); bits.appendChild(grp(m, 'man', 'fraction (' + mb + ' bits)'));
      var E = parseInt(e, 2), sub = E === 0, special = E === (1 << eb) - 1;
      var exact = exactDecimal(stored), err = stored - v;
      var rows = [];
      if (special) rows.push(['Special value', m.indexOf('1') >= 0 ? 'NaN' : (s === '1' ? '−∞' : '+∞')]);
      else {
        rows.push(['Exponent field', E + (sub ? ' (subnormal)' : '') + '  →  2<sup>' + (sub ? 1 - bias : E - bias) + '</sup>  (bias ' + bias + ')']);
        rows.push(['Value', '(−1)<sup>' + s + '</sup> × ' + (sub ? '0.' : '1.') + '<span class="mono">' + m.replace(/0+$/, '').slice(0, 30) + (m.replace(/0+$/, '').length > 30 ? '…' : '') + '</span><sub>2</sub> × 2<sup>' + (sub ? 1 - bias : E - bias) + '</sup>']);
      }
      rows.push(['You typed', '<span class="mono">' + inp.input.value + '</span>']);
      rows.push(['Actually stored', '<span class="mono brk">' + exact + '</span>']);
      rows.push(['Rounding error', '<span class="mono">' + (err === 0 ? '0 (exact!)' : sci(err, 3)) + '</span>' + (v !== 0 && err !== 0 ? '  (relative ' + sci(Math.abs(err / v), 2) + ')' : '')]);
      rows.push(['Machine epsilon', single ? '2<sup>−23</sup> ≈ 1.19e−7 (about 7 decimal digits)' : '2<sup>−52</sup> ≈ 2.22e−16 (about 16 decimal digits)']);
      info.appendChild(table(['', ''], rows));
    }
    draw();
  };

  /* ============================================================= L2: toy floating-point number line */
  W.fpline = function (host, o) {
    card(host, 'wg-fpline');
    var t = slider('Mantissa bits t', 1, 5, 1, o.t || 3, draw), emin = -2, emax = 2;
    var xsl = slider('Real number x', 0, 1000, 1, 610, draw, function (v) { return ''; });
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '220px') }), P = new Plot(pl, { label: 'toy floating point number line' });
    var info = h('p', { class: 'wg-note' });
    host.appendChild(row([t.el, xsl.el])); host.appendChild(pl); host.appendChild(info);
    P.onresize = draw;
    function draw() {
      var T = t.value, nums = [];
      for (var e = emin; e <= emax; e++) for (var k = 0; k < (1 << T); k++) nums.push((1 + k / (1 << T)) * Math.pow(2, e));
      var maxv = (2 - 1 / (1 << T)) * Math.pow(2, emax), x = Math.pow(2, emin) + (maxv - Math.pow(2, emin)) * xsl.value / 1000;
      var near = nums.reduce(function (b, v) { return Math.abs(v - x) < Math.abs(b - x) ? v : b; }, nums[0]);
      t.el.querySelector('output').textContent = T;
      xsl.el.querySelector('output').textContent = x.toFixed(4);
      var c = P.begin(); P.range(0, maxv * 1.04, -1, 1); P.o.xstep = maxv > 8 ? 1 : 0.5;
      P.axes();
      var col = P.col;
      nums.forEach(function (v) { var e = Math.floor(Math.log2(v)); var cc = [col.c1, col.c2, col.c3, col.c4, col.c5][(e - emin) % 5]; P.seg(v, -0.45, v, 0.45, cc, 2.5); });
      P.seg(x, -0.9, x, 0.9, col.ink, 2, [6, 4]); P.dot(near, 0, 7, col.c5);
      P.label(x, 0.95, 'x', col.ink, 'center');
      var gapAt = function (v) { var e = Math.floor(Math.log2(v)); return Math.pow(2, e - T); };
      info.innerHTML = 'Base 2, ' + T + ' fraction bits, exponents ' + emin + '…' + emax + ': <b>' + nums.length + '</b> positive numbers. x = ' + x.toFixed(4) + ' is stored as <b>' + near + '</b>; error ' + Math.abs(near - x).toFixed(4) +
        ', relative ' + (Math.abs(near - x) / x * 100).toFixed(2) + '%. The gap here is ' + gapAt(near) + ': gaps <b>double</b> at every power of 2, but the relative gap stays ≈ 2<sup>−' + T + '</sup> = ' + Math.pow(2, -T) + ' (machine epsilon).';
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L3: catastrophic cancellation */
  W.cancel = function (host, o) {
    card(host, 'wg-cancel');
    var modes = {
      cos: { name: '(1 − cos x) / x²', naive: function (x) { return (1 - Math.cos(x)) / (x * x); }, good: function (x) { var s = Math.sin(x / 2); return 2 * s * s / (x * x); }, goodName: '2 sin²(x/2) / x²', exact: function (x) { var s = Math.sin(x / 2); return 2 * s * s / (x * x); }, lo: -9, hi: -0.5 },
      sqrt: { name: '√(x+1) − √x', naive: function (x) { return Math.sqrt(x + 1) - Math.sqrt(x); }, good: function (x) { return 1 / (Math.sqrt(x + 1) + Math.sqrt(x)); }, goodName: '1 / (√(x+1) + √x)', exact: function (x) { return 1 / (Math.sqrt(x + 1) + Math.sqrt(x)); }, lo: 1, hi: 16, big: true },
      quad: { name: 'smaller root of x² + bx + 1 (−b + √(b²−4))/2', naive: function (b) { return (-b + Math.sqrt(b * b - 4)) / 2; }, good: function (b) { return 2 / (-b - Math.sqrt(b * b - 4)); }, goodName: '2 / (−b − √(b²−4))', exact: function (b) { return 2 / (-b - Math.sqrt(b * b - 4)); }, lo: 1, hi: 9, big: true, quad: true }
    };
    var mode = o.mode || 'cos';
    var sel = select('Expression', [['cos', '(1 − cos x)/x²'], ['sqrt', '√(x+1) − √x'], ['quad', 'quadratic formula, small root']], mode, function (v) { mode = v; setup(); });
    var sl = slider('x', 0, 100, 1, 60, draw);
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '260px') }), P = new Plot(pl, { logy: true, label: 'relative error' });
    var tb = h('div');
    host.appendChild(row([sel.el, sl.el])); host.appendChild(pl); host.appendChild(tb);
    P.onresize = draw;
    function xv() { var m = modes[mode]; return Math.pow(10, m.lo + (m.hi - m.lo) * sl.value / 100) * (m.big ? 1 : 1) * (m.big ? 1 : 1) * (m.quad ? -1 : 1); }
    function setup() { draw(); }
    function draw() {
      var m = modes[mode], x = xv();
      var exactFn = function (x) { return m.exact(x); };
      var lbl = m.quad ? 'b = ' : 'x = ';
      sl.el.querySelector('output').textContent = lbl + sci(x, 1);
      var c = P.begin(); P.range(m.lo, m.hi, -17, 1);
      P.o.xfmt = function (v) { return '1e' + Math.round(v); }; P.o.xstep = m.hi - m.lo > 10 ? 2 : 1;
      P.axes(m.quad ? 'log₁₀|b|' : 'log₁₀ x', 'relative error');
      function relErr(f) { return function (lx) { var xx = Math.pow(10, lx) * (m.quad ? -1 : 1), ex = exactFn(xx), v = f(xx); var r = Math.abs((v - ex) / ex); return r === 0 ? 1e-17 : r; }; }
      P.fn(relErr(m.naive), P.col.c5, 2.5);
      P.fn(relErr(m.good), P.col.c3, 2.5);
      var lx = Math.log10(Math.abs(x)); P.seg(lx, -17, lx, 1, P.col.ink, 1.5, [5, 4]);
      P.legend([['naive: ' + m.name, P.col.c5], ['rewritten: ' + m.goodName, P.col.c3]]);
      var a = m.naive(x), b = m.good(x), ex = exactFn(x);
      tb.innerHTML = '';
      tb.appendChild(table(['', 'value', 'relative error'], [
        ['Naive formula', '<span class="mono">' + a.toPrecision(16) + '</span>', '<b style="color:var(--w-c5)">' + sci(Math.abs((a - ex) / ex) || 0, 1) + '</b>'],
        ['Rewritten formula', '<span class="mono">' + b.toPrecision(16) + '</span>', '<b style="color:var(--w-c3)">' + sci(Math.abs((b - ex) / ex) || 0, 1) + '</b>']
      ]));
    }
    setup(); redrawOnTheme(draw);
  };

  /* ============================================================= L4: Taylor polynomials */
  W.taylor = function (host, o) {
    card(host, 'wg-taylor');
    var F = {
      exp: { n: 'eˣ', f: Math.exp, d: function (k, a) { return Math.exp(a); }, r: [-3, 3, -1, 12] },
      sin: { n: 'sin x', f: Math.sin, d: function (k, a) { return [Math.sin(a), Math.cos(a), -Math.sin(a), -Math.cos(a)][k % 4]; }, r: [-7, 7, -2.2, 2.2] },
      cos: { n: 'cos x', f: Math.cos, d: function (k, a) { return [Math.cos(a), -Math.sin(a), -Math.cos(a), Math.sin(a)][k % 4]; }, r: [-7, 7, -2.2, 2.2] },
      ln: { n: 'ln(1 + x)', f: function (x) { return Math.log(1 + x); }, d: function (k, a) { if (k === 0) return Math.log(1 + a); var s = (k % 2 ? 1 : -1), f = 1; for (var i = 2; i < k; i++) f *= i; return s * f / Math.pow(1 + a, k); }, r: [-0.95, 3, -3, 2] },
      inv: { n: '1 / (1 − x)', f: function (x) { return 1 / (1 - x); }, d: function (k, a) { var f = 1; for (var i = 2; i <= k; i++) f *= i; return f / Math.pow(1 - a, k + 1); }, r: [-2, 0.95, -1, 8] }
    };
    var key = o.f || 'exp';
    var sel = select('f(x)', Object.keys(F).map(function (k) { return [k, F[k].n]; }), key, function (v) { key = v; draw(); });
    var nsl = slider('Degree n', 0, 12, 1, o.n || 2, draw);
    var xsl = slider('Evaluate at x', -100, 100, 1, 50, draw, function () { return ''; });
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '300px') }), P = new Plot(pl);
    var info = h('div', { class: 'wg-info' });
    host.appendChild(row([sel.el, nsl.el, xsl.el])); host.appendChild(pl); host.appendChild(info);
    P.onresize = draw;
    function fact(k) { var f = 1; for (var i = 2; i <= k; i++) f *= i; return f; }
    function draw() {
      var Fn = F[key], n = nsl.value, a = 0, r = Fn.r;
      var coef = []; for (var k = 0; k <= n; k++) coef.push(Fn.d(k, a) / fact(k));
      var p = function (x) { var s = 0, t = 1; for (var k = 0; k <= n; k++) { s += coef[k] * t; t *= (x - a); } return s; };
      var x = r[0] + (r[1] - r[0]) * (xsl.value + 100) / 200;
      xsl.el.querySelector('output').textContent = x.toFixed(2);
      var c = P.begin(); P.range(r[0], r[1], r[2], r[3]); P.axes('x', '');
      P.fn(Fn.f, P.col.c1, 3); P.fn(p, P.col.c2, 2.5, [8, 5]);
      P.seg(x, r[2], x, r[3], P.col.mut, 1.2, [4, 4]); P.dot(x, Fn.f(x), 6, P.col.c1); P.dot(x, p(x), 6, P.col.c2);
      P.legend([[Fn.n, P.col.c1], ['Taylor polynomial P' + sub(n) + '(x) about 0', P.col.c2, [8, 5]]]);
      var terms = []; for (var k2 = 0; k2 <= Math.min(n, 5); k2++) { var cf = coef[k2]; if (Math.abs(cf) < 1e-15) continue; terms.push(fmtC(cf, k2)); }
      var next = Fn.d(n + 1, a) / fact(n + 1) * Math.pow(x - a, n + 1);
      info.innerHTML = '<p><b>P' + sub(n) + '(x)</b> = ' + (terms.join(' ').replace(/^\+ /, '') || '0') + (n > 5 ? ' + …' : '') + '</p>' +
        '<p>At x = ' + x.toFixed(2) + ': f(x) = ' + Fn.f(x).toFixed(6) + ', P' + sub(n) + '(x) = ' + p(x).toFixed(6) + ', <b>error = ' + sci(Math.abs(Fn.f(x) - p(x)), 2) + '</b>. First neglected term ≈ ' + sci(Math.abs(next), 2) + '.</p>';
    }
    function sub(n) { return String(n).split('').map(function (d) { return '₀₁₂₃₄₅₆₇₈₉'[+d]; }).join(''); }
    function fmtC(cf, k) {
      var s = cf < 0 ? '− ' : '+ ', a = Math.abs(cf), f = fact(k), frac = Math.abs(a * f - Math.round(a * f)) < 1e-9 && k > 1 ? (Math.round(a * f) === 1 ? 'x' + sup(k) + '/' + k + '!' : Math.round(a * f) + 'x' + sup(k) + '/' + k + '!') : null;
      if (frac) return s + frac;
      var cs = Math.abs(a - 1) < 1e-12 && k > 0 ? '' : +a.toPrecision(4) + '';
      return s + cs + (k === 0 ? '' : k === 1 ? 'x' : 'x' + sup(k));
    }
    function sup(n) { return String(n).split('').map(function (d) { return '⁰¹²³⁴⁵⁶⁷⁸⁹'[+d]; }).join(''); }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L4 / L21: step size trade-off (truncation vs round-off) */
  W.stepsize = function (host, o) {
    card(host, 'wg-stepsize');
    var fx = field('f(x) =', o.f || 'sin(x)', { size: '8em' }), xx = field('at x =', o.x || 1, { size: '4em' });
    var meth = { fwd: true, ctr: true };
    var hs = slider('Step h', -16, -1, 0.25, -5, draw, function (v) { return '10<sup>' + v + '</sup>'; });
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '300px') }), P = new Plot(pl, { logy: true });
    var info = h('div', { class: 'wg-info' });
    host.appendChild(row([fx.el, xx.el, hs.el])); host.appendChild(pl); host.appendChild(info);
    [fx.input, xx.input].forEach(function (i) { i.addEventListener('input', draw); });
    P.onresize = draw;
    function draw() {
      var f, d, x = num(xx.input, 1);
      try { f = G.Expr.make(fx.input.value); d = f.deriv(); } catch (e) { info.innerHTML = ''; info.appendChild(errBox(e.message)); return; }
      var ex = d(x);
      var ef = function (lh) { var hh = Math.pow(10, lh); return Math.abs((f(x + hh) - f(x)) / hh - ex) || 1e-17; };
      var ec = function (lh) { var hh = Math.pow(10, lh); return Math.abs((f(x + hh) - f(x - hh)) / (2 * hh) - ex) || 1e-17; };
      var c = P.begin(); P.range(-16, -1, -16, 1); P.o.xfmt = function (v) { return '1e' + Math.round(v); }; P.o.xstep = 2;
      P.axes('step size h', '|error|');
      P.fn(ef, P.col.c2, 2.5); P.fn(ec, P.col.c1, 2.5);
      var lh = hs.value; P.seg(lh, -16, lh, 1, P.col.ink, 1.3, [5, 4]); P.dot(lh, ef(lh), 6, P.col.c2); P.dot(lh, ec(lh), 6, P.col.c1);
      P.legend([['forward  (f(x+h) − f(x)) / h      error ~ h', P.col.c2], ['central  (f(x+h) − f(x−h)) / 2h   error ~ h²', P.col.c1]]);
      var hh = Math.pow(10, lh);
      info.innerHTML = "<p>Exact f′(" + x + ") = " + ex.toPrecision(12) + " (f′(x) = " + d.text + "). At h = " + sci(hh, 1) + ": forward error " + sci(ef(lh), 1) + ", central error " + sci(ec(lh), 1) + ".</p><p>Right side: <b>truncation error</b> shrinks as h shrinks. Left side: <b>round-off error</b> ≈ ε/h grows. The best h is near √ε ≈ 1e−8 (forward) or ∛ε ≈ 1e−5 (central).</p>";
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L5: ill-conditioned 2x2 system */
  W.illcond = function (host, o) {
    card(host, 'wg-illcond');
    var presets = { well: [1, 1, 2, 1, -1, 0], ill: [1, 1, 2, 1, 1.0001, 2.0001] };
    var pre = o.preset || 'ill', A = presets[pre].slice();
    var sel = select('System', [['well', 'well-conditioned'], ['ill', 'ill-conditioned (nearly parallel)']], pre, function (v) { A = presets[v].slice(); dsl.input.value = 0; draw(); });
    var dsl = slider('Change b₂ by δ', -100, 100, 1, 0, draw, function (v) { return (v * 1e-5).toFixed(5); });
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '300px') }), P = new Plot(pl);
    var info = h('div', { class: 'wg-info' });
    host.appendChild(row([sel.el, dsl.el])); host.appendChild(pl); host.appendChild(info);
    P.onresize = draw;
    function solve(a, b, e, c, d, f) { var det = a * d - b * c; return [(e * d - b * f) / det, (a * f - e * c) / det, det]; }
    function draw() {
      var dl = dsl.value * 1e-5, a = A[0], b = A[1], e = A[2], c = A[3], d = A[4], f = A[5] + dl;
      var s0 = solve(a, b, e, c, d, A[5]), s = solve(a, b, e, c, d, f);
      var n1 = Math.max(Math.abs(a) + Math.abs(b), Math.abs(c) + Math.abs(d)), det = s0[2];
      var inv = [d / det, -b / det, -c / det, a / det], n2 = Math.max(Math.abs(inv[0]) + Math.abs(inv[1]), Math.abs(inv[2]) + Math.abs(inv[3])), kappa = n1 * n2;
      var cx = s[0], cy = s[1], span = Math.max(3, Math.abs(cx - s0[0]) * 2.4, Math.abs(cy - s0[1]) * 2.4);
      var P0 = P.begin(); P.range(s0[0] - span, s0[0] + span, s0[1] - span * 0.62, s0[1] + span * 0.62); P.axes('x', 'y');
      P.fn(function (x) { return (e - a * x) / b; }, P.col.c1, 2.5);
      P.fn(function (x) { return (f - c * x) / d; }, P.col.c2, 2.5);
      P.dot(s0[0], s0[1], 6, P.col.mut, true); P.dot(cx, cy, 7, P.col.c5);
      P.legend([[a + 'x + ' + b + 'y = ' + e, P.col.c1], [c + 'x + ' + d + 'y = ' + (+f.toFixed(6)), P.col.c2]]);
      var relIn = Math.abs(dl) / Math.max(Math.abs(e), Math.abs(A[5])), relOut = Math.max(Math.abs(cx - s0[0]), Math.abs(cy - s0[1])) / Math.max(Math.abs(s0[0]), Math.abs(s0[1]));
      info.innerHTML = '<p>Solution: x = <b>' + fmt(cx, 5) + '</b>, y = <b>' + fmt(cy, 5) + '</b> (was ' + fmt(s0[0], 5) + ', ' + fmt(s0[1], 5) + ').</p>' +
        '<p>Condition number κ(A) = ‖A‖ ‖A⁻¹‖ ≈ <b>' + fmt(kappa, 1) + '</b>. ' + (dl ? 'Input changed by ' + sci(relIn, 1) + ' (relative); answer changed by <b>' + sci(relOut, 1) + '</b>, an amplification of ' + fmt(relOut / relIn, 0) + '×.' : 'Move the slider: a tiny change in b₂ moves the crossing point.') + '</p>';
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L5: stable vs unstable recurrence */
  W.unstable = function (host, o) {
    card(host, 'wg-unstable');
    var nsl = slider('Up to n =', 5, 25, 1, o.n || 20, draw);
    var out = h('div', { class: 'wg-scroll' }), note = h('p', { class: 'wg-note' });
    host.appendChild(row([nsl.el])); host.appendChild(out); host.appendChild(note);
    function draw() {
      var N = nsl.value, fw = [1 - 1 / Math.E], bw = new Array(N + 1);
      for (var n = 1; n <= N; n++) fw.push(1 - n * fw[n - 1]);
      var M = N + 20, v = 0; for (var m = M; m > N; m--) v = (1 - v) / m; bw[N] = v;
      for (var k = N; k > 0; k--) bw[k - 1] = (1 - bw[k]) / k;
      var rows = []; for (var i = 0; i <= N; i++) rows.push([i, '<span class="mono">' + fw[i].toPrecision(10) + '</span>', '<span class="mono">' + bw[i].toPrecision(10) + '</span>', Math.abs(fw[i]) > 1 || fw[i] < 0 ? '<b style="color:var(--w-c5)">✗ impossible</b>' : '']);
      out.innerHTML = ''; out.appendChild(table(['n', 'forward: I<sub>n</sub> = 1 − n·I<sub>n−1</sub>', 'backward: I<sub>n−1</sub> = (1 − I<sub>n</sub>)/n', ''], rows));
      note.innerHTML = 'I<sub>n</sub> = ∫<sub>0</sub><sup>1</sup> xⁿ e<sup>x−1</sup> dx must lie between 0 and 1/(n+1). Both columns use the <b>same exact formula</b>. Forward, the tiny error in I₀ is multiplied by n at every step (total ≈ n!); backward, it is divided by n. Same problem, two algorithms: one <b>unstable</b>, one <b>stable</b>.';
      var tb = out.querySelector('tbody'); if (tb) tb.lastChild.scrollIntoView && false;
    }
    draw();
  };

  /* ============================================================= L6-L10: root finder (bisection, false position, Newton, secant, fixed point) */
  var ROOT_INFO = {
    bisect: { name: 'Bisection', two: true }, falsi: { name: 'False position (Regula Falsi)', two: true },
    newton: { name: 'Newton–Raphson', two: false }, secant: { name: 'Secant', two: true }
  };
  function rootSteps(method, f, df, a, b, tol, maxIt) {
    var rows = [], fa = f(a), fb = f(b), x0 = a, x1 = b, x, fx;
    if (method === 'bisect' || method === 'falsi') {
      if (fa * fb > 0) return { error: 'f(a) and f(b) have the same sign (f(' + a + ') = ' + fmt(fa, 4) + ', f(' + b + ') = ' + fmt(fb, 4) + '). Choose a bracket where the sign changes.' };
      for (var i = 1; i <= maxIt; i++) {
        x = method === 'bisect' ? (a + b) / 2 : (a * fb - b * fa) / (fb - fa);
        fx = f(x);
        var prev = rows.length ? rows[rows.length - 1].x : null;
        rows.push({ n: i, a: a, b: b, fa: fa, fb: fb, x: x, fx: fx, err: method === 'bisect' ? (b - a) / 2 : (prev === null ? null : Math.abs(x - prev)) });
        if (fx === 0) break;
        if (fa * fx < 0) { b = x; fb = fx; } else { a = x; fa = fx; }
        var last = rows[rows.length - 1];
        if (last.err !== null && last.err < tol) break;
      }
      return { rows: rows };
    }
    if (method === 'newton') {
      x = a;
      for (var j = 1; j <= maxIt; j++) {
        fx = f(x); var d = df(x);
        if (d === 0 || !isFinite(d)) { rows.push({ n: j, x0: x, fx0: fx, d: d, x: NaN, err: null, fail: "f′(x) = 0: the tangent is horizontal and never meets the x-axis" }); break; }
        var xn = x - fx / d;
        rows.push({ n: j, x0: x, fx0: fx, d: d, x: xn, fx: f(xn), err: Math.abs(xn - x) });
        if (!isFinite(xn) || Math.abs(xn) > 1e12) { rows[rows.length - 1].fail = 'the iterates run away (divergence)'; break; }
        x = xn;
        if (Math.abs(rows[rows.length - 1].err) < tol) break;
      }
      return { rows: rows };
    }
    if (method === 'secant') {
      var f0 = f(x0), f1 = f(x1);
      for (var k = 1; k <= maxIt; k++) {
        if (f1 === f0) { rows.push({ n: k, x0: x0, x1: x1, f0: f0, f1: f1, x: NaN, err: null, fail: 'f(xₙ) = f(xₙ₋₁): the secant line is horizontal' }); break; }
        var x2 = x1 - f1 * (x1 - x0) / (f1 - f0), f2 = f(x2);
        rows.push({ n: k, x0: x0, x1: x1, f0: f0, f1: f1, x: x2, fx: f2, err: Math.abs(x2 - x1) });
        x0 = x1; f0 = f1; x1 = x2; f1 = f2;
        if (!isFinite(x2) || Math.abs(x2) > 1e12) { rows[rows.length - 1].fail = 'the iterates run away (divergence)'; break; }
        if (rows[rows.length - 1].err < tol) break;
      }
      return { rows: rows };
    }
  }
  W._rootSteps = rootSteps;
  W.root = function (host, o) {
    card(host, 'wg-root');
    var method = o.method || 'bisect', fixedMethod = !!o.fixed;
    var fF = field('f(x) =', o.f || 'x^3 - x - 2', { size: o.big ? '11em' : '13em' });
    var aF = field(ROOT_INFO[method].two ? 'a =' : 'x₀ =', o.a !== undefined ? o.a : 1, { size: '4.5em' }), bF = field('b =', o.b !== undefined ? o.b : 2, { size: '4.5em' });
    var dec = o.dec || 6;
    var msel = select('Method', Object.keys(ROOT_INFO).map(function (k) { return [k, ROOT_INFO[k].name]; }), method, function (v) { method = v; relabel(); step = 1; draw(); });
    var step = o.step || 1;
    var next = btn('Next step ▶', function () { step++; draw(); }, 'pri'), back = btn('◀', function () { if (step > 1) step--; draw(); }), all = btn('Run to tolerance', function () { step = 999; draw(); }), reset = btn('Reset', function () { step = 1; draw(); });
    var tolF = field('tol', o.tol || '1e-4', { size: '4.5em' });
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '300px') }), P = new Plot(pl);
    var tbl = h('div', { class: 'wg-scroll', style: o.tableHeight ? 'max-height:' + o.tableHeight : '' }), info = h('div', { class: 'wg-note' });
    var ctr = [fF.el, aF.el, bF.el];
    if (!fixedMethod) ctr.unshift(msel.el);
    if (!o.compact) ctr.push(tolF.el);
    host.appendChild(row(ctr));
    if (o.presets) host.appendChild(row(o.presets.map(function (p) { return btn(p[0], function () { fF.input.value = p[1]; aF.input.value = p[2]; bF.input.value = p[3] === undefined ? '' : p[3]; if (p[4]) { method = p[4]; msel.input.value = p[4]; relabel(); } step = 1; draw(); }, 'chip'); }), 'wg-chips'));
    host.appendChild(row([back, next, all, reset], 'wg-steps'));
    var layout = h('div', { class: o.side ? 'wg-side' : '' }, [pl, tbl]);
    host.appendChild(layout); host.appendChild(info);
    [fF.input, aF.input, bF.input, tolF.input].forEach(function (i) { i.addEventListener('input', function () { step = Math.max(1, step); draw(); }); });
    P.onresize = draw;
    function relabel() {
      var two = ROOT_INFO[method].two;
      aF.el.querySelector('span').innerHTML = method === 'newton' ? 'x₀ =' : method === 'secant' ? 'x₀ =' : 'a =';
      bF.el.querySelector('span').innerHTML = method === 'secant' ? 'x₁ =' : 'b =';
      bF.el.style.display = two ? '' : 'none';
    }
    relabel();
    function D(x) { return fmt(x, dec); }
    function draw() {
      var f, df;
      try { f = G.Expr.make(fF.input.value); df = f.deriv(); } catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox('Formula problem: ' + e.message)); return; }
      var a = num(aF.input, 1), b = num(bF.input, 2), tol = num(tolF.input, 1e-4);
      var res = rootSteps(method, f, df, a, b, tol, 60);
      tbl.innerHTML = '';
      if (res.error) { tbl.appendChild(errBox(res.error)); drawPlot(f, a, b, [], null); info.innerHTML = ''; return; }
      var rows = res.rows, shown = rows.slice(0, Math.min(step, rows.length)), cur = shown[shown.length - 1];
      var hdr, body;
      if (method === 'bisect' || method === 'falsi') {
        if (o.side) {
          hdr = ['n', 'a', 'b', 'c', 'f(c)', method === 'bisect' ? '(b−a)/2' : '|cₙ − cₙ₋₁|'];
          body = shown.map(function (r) { return [r.n, D(r.a), D(r.b), '<b>' + D(r.x) + '</b>', fmt(r.fx, 4), r.err === null ? '—' : sci(r.err, 2)]; });
        } else {
          hdr = ['n', 'a', 'b', 'f(a)', 'f(b)', method === 'bisect' ? 'c = (a+b)/2' : 'c = (a f(b) − b f(a)) / (f(b) − f(a))', 'f(c)', method === 'bisect' ? 'error bound (b−a)/2' : '|cₙ − cₙ₋₁|'];
          body = shown.map(function (r) { return [r.n, D(r.a), D(r.b), fmt(r.fa, 4), fmt(r.fb, 4), '<b>' + D(r.x) + '</b>', fmt(r.fx, 4), r.err === null ? '—' : sci(r.err, 2)]; });
        }
      } else if (method === 'newton') {
        hdr = ['n', 'xₙ', 'f(xₙ)', "f′(xₙ)", o.side ? 'xₙ₊₁' : 'xₙ₊₁ = xₙ − f(xₙ)/f′(xₙ)', o.side ? '|Δx|' : '|xₙ₊₁ − xₙ|'];
        body = shown.map(function (r) { return [r.n - 1, D(r.x0), fmt(r.fx0, 6), fmt(r.d, 6), r.fail ? '<b style="color:var(--w-c5)">fails</b>' : '<b>' + D(r.x) + '</b>', r.err === null ? '—' : sci(r.err, 2)]; });
      } else {
        hdr = o.side ? ['n', 'xₙ₋₁', 'xₙ', 'f(xₙ)', 'xₙ₊₁', '|Δx|'] : ['n', 'xₙ₋₁', 'xₙ', 'f(xₙ₋₁)', 'f(xₙ)', 'xₙ₊₁', '|xₙ₊₁ − xₙ|'];
        body = shown.map(function (r) { var nx = r.fail ? '<b style="color:var(--w-c5)">fails</b>' : '<b>' + D(r.x) + '</b>', er = r.err === null ? '—' : sci(r.err, 2);
          return o.side ? [r.n, D(r.x0), D(r.x1), fmt(r.f1, 5), nx, er] : [r.n, D(r.x0), D(r.x1), fmt(r.f0, 5), fmt(r.f1, 5), nx, er]; });
      }
      tbl.appendChild(table(hdr, body, { hi: body.length - 1 }));
      var done = shown.length === rows.length, lastR = rows[rows.length - 1];
      var msg = method === 'newton' ? "f′(x) = " + df.text + '. ' : '';
      if (cur.fail) msg += '<b style="color:var(--w-c5)">Stopped: ' + cur.fail + '.</b>';
      else if (done) msg += 'Converged: root ≈ <b>' + D(lastR.x) + '</b> after ' + rows.length + ' iteration' + (rows.length > 1 ? 's' : '') + ' (stopping when the error estimate < ' + tol + ').';
      else msg += 'Step ' + shown.length + ' of ' + rows.length + ' needed for tol = ' + tol + '. Current estimate ' + D(cur.x) + '.';
      if (method === 'bisect' && !res.error) msg += ' Iterations predicted by n ≥ log₂((b−a)/tol): <b>' + Math.ceil(Math.log2((b - a) / tol)) + '</b>.';
      info.innerHTML = msg;
      drawPlot(f, a, b, shown, cur, df);
    }
    function drawPlot(f, a, b, shown, cur, df) {
      var xs = [a, b]; shown.forEach(function (r) { if (isFinite(r.x)) xs.push(r.x); if (r.x0 !== undefined) xs.push(r.x0); });
      var lo = Math.min.apply(null, xs), hi = Math.max.apply(null, xs);
      if (o.xrange) { lo = o.xrange[0]; hi = o.xrange[1]; } else { var m = Math.max((hi - lo) * 0.25, 0.5); lo -= m; hi += m; }
      if (cur && !o.xrange && step > 3 && isFinite(cur.x)) {   // zoom in as we converge
        var w = Math.max(Math.abs((cur.b !== undefined ? cur.b - cur.a : (cur.x0 !== undefined ? cur.x - cur.x0 : 1))) * 3, 1e-6);
        lo = cur.x - w; hi = cur.x + w;
      }
      var yr = autoRange(f, lo, hi);
      var c = P.begin(); P.range(lo, hi, yr[0], yr[1]); P.axes('x', 'f(x)');
      if (cur && (method === 'bisect' || method === 'falsi')) P.vband(cur.a, cur.b, 'rgba(47,109,181,0.10)');
      P.fn(f, P.col.c1, 3);
      if (cur) {
        if (method === 'bisect') { P.seg(cur.a, 0, cur.a, cur.fa, P.col.mut, 1.5, [4, 4]); P.seg(cur.b, 0, cur.b, cur.fb, P.col.mut, 1.5, [4, 4]); P.dot(cur.a, cur.fa, 5, P.col.c1); P.dot(cur.b, cur.fb, 5, P.col.c1); }
        if (method === 'falsi') { P.seg(cur.a, cur.fa, cur.b, cur.fb, P.col.c2, 2.2); P.dot(cur.a, cur.fa, 5, P.col.c1); P.dot(cur.b, cur.fb, 5, P.col.c1); }
        if (method === 'newton' && isFinite(cur.x0)) {
          var x0 = cur.x0, y0 = cur.fx0, d = cur.d; P.seg(x0, 0, x0, y0, P.col.mut, 1.5, [4, 4]); P.dot(x0, y0, 6, P.col.c1);
          if (isFinite(cur.x)) { P.fn(function (x) { return y0 + d * (x - x0); }, P.col.c2, 2, [8, 5]); }
          else P.seg(lo, y0, hi, y0, P.col.c5, 2, [8, 5]);
        }
        if (method === 'secant') { P.fn(function (x) { return cur.f1 + (cur.f1 - cur.f0) / (cur.x1 - cur.x0) * (x - cur.x1); }, P.col.c2, 2, [8, 5]); P.dot(cur.x0, cur.f0, 5, P.col.c1); P.dot(cur.x1, cur.f1, 5, P.col.c1); }
        shown.forEach(function (r, i) { if (isFinite(r.x) && i < shown.length - 1) P.dot(r.x, 0, 4, P.col.mut); });
        if (isFinite(cur.x)) { P.dot(cur.x, 0, 7, P.col.c5); P.label(cur.x, 0, method === 'bisect' || method === 'falsi' ? 'c' + sub(cur.n) : 'x' + sub(cur.n), P.col.c5, 'center', -P.fs * 0.5, true); }
      }
    }
    function sub(n) { return String(n).split('').map(function (d) { return '₀₁₂₃₄₅₆₇₈₉'[+d]; }).join(''); }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L8: fixed point iteration (cobweb) */
  W.cobweb = function (host, o) {
    card(host, 'wg-cobweb');
    var gF = field('g(x) =', o.g || 'sqrt(4x + 10)', { size: '10em' }), xF = field('x₀ =', o.x0 !== undefined ? o.x0 : 5, { size: '4em' });
    var step = 1;
    var presets = o.presets || [['√(4x+10)', 'sqrt(4x+10)', 5], ['(x²−10)/4', '(x^2-10)/4', 5], ['10/(x−4)', '10/(x-4)', 5], ['4 + 10/x', '4 + 10/x', 5]];
    var chips = row(presets.map(function (p) { return btn(p[0], function () { gF.input.value = p[1]; xF.input.value = p[2]; step = 1; draw(); }, 'chip'); }), 'wg-chips');
    var ctrls = row([btn('◀', function () { if (step > 1) step--; draw(); }), btn('Next step ▶', function () { step++; draw(); }, 'pri'), btn('10 steps', function () { step += 10; draw(); }), btn('Reset', function () { step = 1; draw(); })], 'wg-steps');
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '320px') }), P = new Plot(pl);
    var tbl = h('div', { class: 'wg-scroll', style: o.tableHeight ? 'max-height:' + o.tableHeight : '' }), info = h('div', { class: 'wg-note' });
    host.appendChild(row([gF.el, xF.el])); host.appendChild(chips); host.appendChild(ctrls);
    host.appendChild(h('div', { class: o.side ? 'wg-side' : '' }, [pl, tbl])); host.appendChild(info);
    [gF.input, xF.input].forEach(function (i) { i.addEventListener('input', draw); });
    P.onresize = draw;
    function draw() {
      var g, dg;
      try { g = G.Expr.make(gF.input.value); dg = g.deriv(); } catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox(e.message)); return; }
      var x = num(xF.input, 5), xs = [x];
      for (var i = 0; i < step; i++) { var y = g(x); xs.push(y); x = y; if (!isFinite(y)) break; }
      var fin = xs.filter(isFinite), lo = Math.min.apply(null, fin), hi = Math.max.apply(null, fin);
      if (o.range) { lo = o.range[0]; hi = o.range[1]; } else { var m = Math.max((hi - lo) * 0.3, 1.5); lo -= m; hi += m; if (hi - lo > 60) { var c0 = fin[0]; lo = c0 - 30; hi = c0 + 30; } }
      var c = P.begin(); P.range(lo, hi, lo, hi); P.axes('x', '');
      P.fn(function (t) { return t; }, P.col.mut, 1.8, [6, 4]); P.fn(g, P.col.c1, 3);
      var pts = [[xs[0], lo < 0 && hi > 0 ? 0 : lo]];
      for (var k = 0; k < xs.length - 1; k++) { pts.push([xs[k], xs[k + 1]]); pts.push([xs[k + 1], xs[k + 1]]); }
      P.poly(pts, P.col.c2, 2);
      P.dot(xs[0], xs[0], 5, P.col.c2); P.dot(xs[xs.length - 1], xs[xs.length - 1], 7, P.col.c5);
      P.legend([['y = g(x)', P.col.c1], ['y = x', P.col.mut, [6, 4]], ['iterates', P.col.c2]]);
      tbl.innerHTML = '';
      var rows = xs.slice(0, -1).map(function (v, i) { return [i, fmt(v, 6), fmt(xs[i + 1], 6), i ? sci(Math.abs(xs[i + 1] - v), 2) : sci(Math.abs(xs[i + 1] - v), 2)]; });
      tbl.appendChild(table(['n', 'xₙ', 'xₙ₊₁ = g(xₙ)', '|xₙ₊₁ − xₙ|'], rows, { hi: rows.length - 1 }));
      var xl = xs[xs.length - 1], slope = dg(xl);
      info.innerHTML = 'g′(x) = ' + dg.text + '. At the latest point |g′(' + fmt(xl, 4) + ')| = <b>' + (isFinite(slope) ? Math.abs(slope).toFixed(4) : '—') + '</b> ' +
        (isFinite(slope) ? (Math.abs(slope) < 1 ? '< 1: the map pulls points together, so the iteration <b style="color:var(--w-c3)">converges</b>' + (slope < 0 ? ' (spiralling, since g′ < 0)' : ' (staircase, since g′ > 0)') + '.' : '> 1: the map pushes points apart, so the iteration <b style="color:var(--w-c5)">diverges</b> from this root.') : '');
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L10: race of root methods */
  W.race = function (host, o) {
    card(host, 'wg-race');
    var fF = field('f(x) =', o.f || 'x^3 - x - 2', { size: '11em' }), aF = field('a =', o.a || 1, { size: '4em' }), bF = field('b =', o.b || 2, { size: '4em' });
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '300px') }), P = new Plot(pl, { logy: true });
    var info = h('div');
    host.appendChild(row([fF.el, aF.el, bF.el, h('span', { class: 'wg-hint', html: 'Newton starts at x₀ = b; secant at x₀ = a, x₁ = b' })])); host.appendChild(pl); host.appendChild(info);
    [fF.input, aF.input, bF.input].forEach(function (i) { i.addEventListener('input', draw); });
    P.onresize = draw;
    function draw() {
      var f, df; try { f = G.Expr.make(fF.input.value); df = f.deriv(); } catch (e) { info.innerHTML = ''; info.appendChild(errBox(e.message)); return; }
      var a = num(aF.input, 1), b = num(bF.input, 2);
      var ref = rootSteps('newton', f, df, b, 0, 1e-15, 100); var root = ref.rows && ref.rows.length ? ref.rows[ref.rows.length - 1].x : NaN;
      var bis = rootSteps('bisect', f, df, a, b, 1e-14, 50); if (bis.rows) root = isFinite(root) && Math.abs(f(root)) < 1e-10 ? root : bis.rows[bis.rows.length - 1].x;
      var c = P.begin(); P.range(0, 25, -16, 1); P.o.xstep = 5; P.axes('iteration n', '|xₙ − root|');
      var M = [['bisect', 'Bisection', P.col.c1, a, b], ['falsi', 'False position', P.col.c3, a, b], ['secant', 'Secant', P.col.c4, a, b], ['newton', 'Newton–Raphson', P.col.c2, b, 0]];
      var lines = [], tbody = [];
      M.forEach(function (m) {
        var r = rootSteps(m[0], f, df, m[3], m[4], 1e-15, 25);
        if (r.error || !r.rows) { tbody.push([m[1], '—', r.error ? 'needs a sign change' : '']); return; }
        var pts = [[0, Math.abs((m[0] === 'newton' ? m[3] : (m[3] + m[4]) / 2) - root) || 1e-16]];
        r.rows.forEach(function (row) { if (isFinite(row.x)) pts.push([row.n, Math.max(Math.abs(row.x - root), 1e-16)]); });
        P.poly(pts.map(function (p) { return [p[0], Math.log10(p[1])]; }).map(function (p) { return [p[0], Math.pow(10, p[1])]; }), m[2], 2.8);
        pts.forEach(function (p) { P.dot(p[0], p[1], 3.5, m[2]); });
        var k = pts.findIndex(function (p) { return p[1] < 1e-6; });
        tbody.push([m[1], k < 0 ? '> 25' : String(k), { bisect: 'linear, error halves', falsi: 'linear (one end can stay fixed)', secant: 'superlinear, order ≈ 1.618', newton: 'quadratic, order 2' }[m[0]]]);
        lines.push([m[1], m[2]]);
      });
      P.legend(lines);
      info.innerHTML = ''; info.appendChild(table(['Method', 'steps to error < 10⁻⁶', 'convergence'], tbody));
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L10: Newton's method for two equations */
  W.newton2d = function (host, o) {
    card(host, 'wg-newton2d');
    var f1F = field('f₁(x, y) =', o.f1 || 'x^2 + y^2 - 4', { size: '10em' }), f2F = field('f₂(x, y) =', o.f2 || 'x y - 1', { size: '10em' });
    var xF = field('x₀ =', o.x0 !== undefined ? o.x0 : 2, { size: '4em' }), yF = field('y₀ =', o.y0 !== undefined ? o.y0 : 0.5, { size: '4em' });
    var step = 1, R = o.range || [-3, 3, -3, 3];
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '360px') }), P = new Plot(pl);
    var tbl = h('div', { class: 'wg-scroll' }), info = h('div', { class: 'wg-note' });
    host.appendChild(row([f1F.el, f2F.el])); host.appendChild(row([xF.el, yF.el, btn('◀', function () { if (step > 1) step--; draw(); }), btn('Next step ▶', function () { step++; draw(); }, 'pri'), btn('Reset', function () { step = 1; draw(); })]));
    host.appendChild(h('div', { class: o.side ? 'wg-side' : '' }, [pl, tbl])); host.appendChild(info);
    [f1F.input, f2F.input, xF.input, yF.input].forEach(function (i) { i.addEventListener('input', draw); });
    P.onresize = draw;
    function contour(f, color) {   // zero level set by marching squares on a grid
      var N = 90, c = P.ctx, dx = (R[1] - R[0]) / N, dy = (R[3] - R[2]) / N, v = [];
      for (var i = 0; i <= N; i++) { v.push([]); for (var j = 0; j <= N; j++) { var val; try { val = f(R[0] + i * dx, R[2] + j * dy); } catch (e) { val = NaN; } v[i].push(val); } }
      P.clip(); c.strokeStyle = color; c.lineWidth = 2.6; c.beginPath();
      function lerp(a, b, fa, fb) { return a + (b - a) * fa / (fa - fb); }
      for (var i2 = 0; i2 < N; i2++) for (var j2 = 0; j2 < N; j2++) {
        var x0 = R[0] + i2 * dx, y0 = R[2] + j2 * dy, a = v[i2][j2], b = v[i2 + 1][j2], cc = v[i2 + 1][j2 + 1], d = v[i2][j2 + 1], pts = [];
        if (!isFinite(a) || !isFinite(b) || !isFinite(cc) || !isFinite(d)) continue;
        if ((a < 0) !== (b < 0)) pts.push([lerp(x0, x0 + dx, a, b), y0]);
        if ((b < 0) !== (cc < 0)) pts.push([x0 + dx, lerp(y0, y0 + dy, b, cc)]);
        if ((cc < 0) !== (d < 0)) pts.push([lerp(x0 + dx, x0, cc, d), y0 + dy]);
        if ((d < 0) !== (a < 0)) pts.push([x0, lerp(y0 + dy, y0, d, a)]);
        for (var k = 0; k + 1 < pts.length; k += 2) { c.moveTo(P.X(pts[k][0]), P.Y(pts[k][1])); c.lineTo(P.X(pts[k + 1][0]), P.Y(pts[k + 1][1])); }
      }
      c.stroke(); P.unclip();
    }
    function draw() {
      var F1, F2;
      try { F1 = G.Expr.make2(f1F.input.value); F2 = G.Expr.make2(f2F.input.value); } catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox(e.message)); return; }
      var a1 = F1.dx(), b1 = F1.dy(), a2 = F2.dx(), b2 = F2.dy();
      var x = num(xF.input, 2), y = num(yF.input, 0.5), pts = [[x, y]], rows = [];
      for (var n = 0; n < step; n++) {
        var f1 = F1(x, y), f2 = F2(x, y), J11 = a1(x, y), J12 = b1(x, y), J21 = a2(x, y), J22 = b2(x, y), det = J11 * J22 - J12 * J21;
        if (!det || !isFinite(det)) { rows.push([n, fmt(x, 6), fmt(y, 6), fmt(f1, 5), fmt(f2, 5), '<b style="color:var(--w-c5)">det J = 0</b>', '']); break; }
        var ddx = (-f1 * J22 + f2 * J12) / det, ddy = (-f2 * J11 + f1 * J21) / det;
        rows.push([n, fmt(x, 6), fmt(y, 6), fmt(f1, 5), fmt(f2, 5), fmt(det, 4), sci(Math.hypot(ddx, ddy), 2)]);
        x += ddx; y += ddy; pts.push([x, y]);
      }
      var c = P.begin();
      P.range(R[0], R[1], R[2], R[3]); P.axes('x', 'y');
      contour(function (x, y) { return F1(x, y); }, P.col.c1); contour(function (x, y) { return F2(x, y); }, P.col.c3);
      P.poly(pts, P.col.c2, 2, [6, 4]); pts.forEach(function (p, i) { P.dot(p[0], p[1], i === pts.length - 1 ? 7 : 4.5, i === pts.length - 1 ? P.col.c5 : P.col.c2); });
      P.legend([['f₁ = 0', P.col.c1], ['f₂ = 0', P.col.c3], ['Newton iterates', P.col.c2, [6, 4]]]);
      tbl.innerHTML = ''; tbl.appendChild(table(['n', 'xₙ', 'yₙ', 'f₁', 'f₂', 'det J', '|Δ|'], rows, { hi: rows.length - 1 }));
      info.innerHTML = 'Each step solves J·Δ = −F (a 2×2 linear system) and moves to (x, y) + Δ. Current point (' + fmt(pts[pts.length - 1][0], 6) + ', ' + fmt(pts[pts.length - 1][1], 6) + ').';
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= Module 3 helpers: matrices */
  var SUBS = '₀₁₂₃₄₅₆₇₈₉';
  function sb(n) { return String(n).split('').map(function (d) { return SUBS[+d]; }).join(''); }
  function sigRound(x, k) {
    if (!k || !isFinite(x) || x === 0) return x;
    var e = Math.floor(Math.log10(Math.abs(x)));
    var p = Math.pow(10, k - 1 - e), r = Math.round(Math.abs(x) * p) / p;
    return (x < 0 ? -r : r);
  }
  function fmtN(x, k) {
    if (!isFinite(x)) return fmt(x);
    if (Math.abs(x) < 1e-12) return '0';
    if (k) { var s = (+x.toPrecision(k)); return String(s).replace('-', '−'); }
    var r = Math.round(x * 1e4) / 1e4;
    if (Math.abs(r - Math.round(r)) < 1e-9 && Math.abs(x - Math.round(x)) < 1e-9) return String(Math.round(x)).replace('-', '−');
    if (Math.abs(x) >= 1e5 || Math.abs(x) < 1e-3) return sci(x, 3);
    return String(r).replace('-', '−');
  }
  function parseMat(s) {
    var rows = String(s).replace(/−/g, '-').split(/[;\n]+/).map(function (r) { return r.trim(); }).filter(function (r) { return r.length; });
    if (!rows.length) throw new Error('Type the matrix: one row per line (or rows separated by ;)');
    var M = rows.map(function (r) {
      var nums = r.replace(/\|/g, ' ').split(/[\s,]+/).filter(function (t) { return t.length; }).map(function (t) {
        var v = Number(t); if (!isFinite(v)) { if (/^-?\d+\/\d+$/.test(t)) { var q = t.split('/'); v = +q[0] / +q[1]; } else throw new Error('Not a number: ' + t); } return v;
      });
      return nums;
    });
    var w = M[0].length; M.forEach(function (r) { if (r.length !== w) throw new Error('Every row needs the same number of entries'); });
    return M;
  }
  function matHTML(M, o) {
    o = o || {};
    var k = o.k, sep = o.sep, t = '<table class="wg-mat' + (o.cls ? ' ' + o.cls : '') + '"><tbody>';
    M.forEach(function (r, i) {
      t += '<tr' + (o.rows && o.rows.indexOf(i) >= 0 ? ' class="chg"' : '') + '>';
      r.forEach(function (v, j) {
        var c = [];
        if (sep && j === sep) c.push('sep');
        if (o.piv && o.piv[0] === i && o.piv[1] === j) c.push('piv');
        if (o.cells && o.cells.some(function (q) { return q[0] === i && q[1] === j; })) c.push('new');
        if (o.colhi !== undefined && o.colhi === j) c.push('colhi');
        if (v === null || v === undefined) { t += '<td class="' + c.concat('emp').join(' ') + '">·</td>'; return; }
        if (Math.abs(v) < 1e-12 && !o.keepzero) c.push('z');
        t += '<td class="' + c.join(' ') + '">' + fmtN(v, k) + '</td>';
      });
      t += '</tr>';
    });
    return t + '</tbody></table>';
  }
  function fmtP(x, k) { var t = fmtN(x, k); return x < 0 ? '(' + t + ')' : t; }
  function labeled(name, html) { return '<div class="wg-matbox"><div class="wg-matlab">' + name + '</div>' + html + '</div>'; }
  function vecCol(v, k, hi) { return matHTML(v.map(function (x) { return [x]; }), { k: k, rows: hi }); }

  /* ============================================================= L12–13: elimination, Gauss–Jordan, LU and Cholesky stepper */
  W.linsys = function (host, o) {
    card(host, 'wg-linsys');
    var modes = o.modes || ['gauss', 'gj', 'inv', 'lu', 'chol'];
    var names = { gauss: 'Gaussian elimination', gj: 'Gauss–Jordan', inv: 'Inverse by Gauss–Jordan', lu: 'LU (Doolittle)', chol: 'Cholesky' };
    var mode = o.mode || modes[0], step = 0, states = [];
    var ta = h('textarea', { class: 'wg-ta', rows: o.rows || 3, spellcheck: 'false', 'aria-label': 'Matrix' }); ta.value = String(o.mat || '2 1 -1 8; -3 -1 2 -11; -2 1 2 -3').split(';').map(function (r) { return r.trim(); }).join('\n');
    var mSel = modes.length > 1 ? select('Method', modes.map(function (m) { return [m, names[m]]; }), mode, function (v) { mode = v; step = 0; build(); }) : null;
    var pivChk = h('input', { type: 'checkbox' }); pivChk.checked = !!o.pivot;
    var pivLab = h('label', { class: 'wg-f' }, [pivChk, h('span', { html: 'partial pivoting' })]);
    var dSel = select('Arithmetic', [['0', 'full precision'], ['3', '3 significant digits'], ['4', '4 significant digits'], ['5', '5 significant digits']], String(o.digits || 0), function () { step = 0; build(); });
    var ctr = h('span', { class: 'wg-hint' });
    var ctrls = row([btn('◀', function () { if (step > 0) step--; show(); }), btn('Next step ▶', function () { if (step < states.length - 1) step++; show(); }, 'pri'), btn('All steps', function () { step = states.length - 1; show(); }), btn('Reset', function () { step = 0; show(); }), ctr], 'wg-steps');
    var presets = o.presets ? row(o.presets.map(function (p) { return btn(p[0], function () { ta.value = p[1].split(';').map(function (r) { return r.trim(); }).join('\n'); if (p[2]) { mode = p[2]; if (mSel) mSel.input.value = mode; } if (p[3] !== undefined) pivChk.checked = !!p[3]; if (p[4] !== undefined) dSel.input.value = String(p[4]); step = 0; build(); }, 'chip'); }), 'wg-chips') : null;
    var opsTxt = h('div', { class: 'wg-op' }), view = h('div', { class: 'wg-matview', style: o.height ? 'min-height:' + o.height : '' }), info = h('div', { class: 'wg-note' });
    var top = [h('div', { class: 'wg-inbox' }, [h('span', { class: 'wg-hint', html: o.hint || 'Augmented matrix [A | b], one row per line' }), ta])];
    var opts = []; if (mSel) opts.push(mSel.el); if (!o.nopivot) opts.push(pivLab); if (!o.nodigits) opts.push(dSel.el);
    host.appendChild(row([top[0], h('div', { class: 'wg-col' }, [row(opts), presets])].filter(Boolean), 'wg-top'));
    host.appendChild(ctrls); host.appendChild(opsTxt); host.appendChild(view); host.appendChild(info);
    ta.addEventListener('input', function () { step = 0; build(); }); pivChk.addEventListener('change', function () { step = 0; build(); });
    function cp(M) { return M.map(function (r) { return r.slice(); }); }
    function build() {
      var M;
      try { M = parseMat(ta.value); } catch (e) { states = []; view.innerHTML = ''; view.appendChild(errBox(e.message)); opsTxt.textContent = ''; info.textContent = ''; ctr.textContent = ''; return; }
      var k = +dSel.input.value, piv = pivChk.checked, n = M.length;
      var R = function (x) { return sigRound(x, k); };
      M = M.map(function (r) { return r.map(R); });
      states = [];
      try {
        if (mode === 'gauss' || mode === 'gj' || mode === 'inv') elim(M, n, k, R, piv);
        else if (mode === 'lu') lu(M, n, k, R, piv);
        else chol(M, n, k, R);
      } catch (e) { states.push({ html: states.length ? states[states.length - 1].html : '', text: '<span class="bad">' + e.message + '</span>' }); }
      if (step > states.length - 1) step = states.length - 1;
      show();
    }
    function push(text, html, extra) { states.push({ text: text, html: html, info: extra || '' }); }
    function elim(M0, n, k, R, piv) {
      var A0 = M0.map(function (r) { return r.slice(); }), M = cp(M0), w = M[0].length, sep;
      if (mode === 'inv') {
        if (w !== n && w !== n + 1) throw new Error('For the inverse, type a square matrix A');
        M = M.map(function (r, i) { return r.slice(0, n).concat(Array.from({ length: n }, function (_, j) { return i === j ? 1 : 0; })); }); w = 2 * n; sep = n;
      } else {
        if (w !== n + 1) throw new Error('Type ' + n + ' rows of ' + (n + 1) + ' numbers: the coefficients and then b');
        sep = n;
      }
      push(mode === 'inv' ? 'Start: [A | I]. Reduce the left half to I; the right half becomes A⁻¹.' : 'Start: the augmented matrix [A | b].', matHTML(M, { k: k, sep: sep }));
      for (var c = 0; c < n; c++) {
        if (piv) {
          var p = c; for (var i = c + 1; i < n; i++) if (Math.abs(M[i][c]) > Math.abs(M[p][c])) p = i;
          if (p !== c) { var t = M[c]; M[c] = M[p]; M[p] = t; push('Pivoting: the largest |entry| in column ' + (c + 1) + ' (rows ' + (c + 1) + '–' + n + ') is ' + fmtN(M[c][c], k) + ' in row ' + (p + 1) + '. Swap R' + sb(c + 1) + ' ↔ R' + sb(p + 1) + '.', matHTML(M, { k: k, sep: sep, rows: [c, p], piv: [c, c] })); }
        }
        if (Math.abs(M[c][c]) < 1e-14) {
          var other = -1; for (var r2 = c + 1; r2 < n; r2++) if (Math.abs(M[r2][c]) > 1e-14) { other = r2; break; }
          if (other < 0) throw new Error('Column ' + (c + 1) + ' has no nonzero pivot: the matrix is singular (det A = 0). There is no unique solution.');
          throw new Error('Zero pivot: a' + sb(c + 1) + sb(c + 1) + ' = 0, so the multipliers a' + 'ᵢ' + sb(c + 1) + ' / a' + sb(c + 1) + sb(c + 1) + ' are undefined. Turn on partial pivoting (swap rows).');
        }
        if (mode === 'gauss') {
          for (var i2 = c + 1; i2 < n; i2++) {
            if (M[i2][c] === 0) continue;
            var m = R(M[i2][c] / M[c][c]);
            for (var j = c; j < w; j++) M[i2][j] = j === c ? 0 : R(M[i2][j] - R(m * M[c][j]));
            push('R' + sb(i2 + 1) + ' ← R' + sb(i2 + 1) + ' − (' + fmtN(m, k) + ')·R' + sb(c + 1) + '   with multiplier m' + sb(i2 + 1) + sb(c + 1) + ' = a' + sb(i2 + 1) + sb(c + 1) + ' / a' + sb(c + 1) + sb(c + 1) + ' = ' + fmtN(m, k), matHTML(M, { k: k, sep: sep, rows: [i2], piv: [c, c] }));
          }
        } else {
          var pv = M[c][c];
          if (Math.abs(pv - 1) > 1e-15) { for (var j2 = c; j2 < w; j2++) M[c][j2] = j2 === c ? 1 : R(M[c][j2] / pv); push('Normalise: R' + sb(c + 1) + ' ← R' + sb(c + 1) + ' / ' + fmtN(pv, k) + ' so that the pivot becomes 1.', matHTML(M, { k: k, sep: sep, rows: [c], piv: [c, c] })); }
          var ops = [], chg = [];
          for (var i3 = 0; i3 < n; i3++) {
            if (i3 === c || M[i3][c] === 0) continue;
            var m2 = M[i3][c]; ops.push('R' + sb(i3 + 1) + ' ← R' + sb(i3 + 1) + ' − (' + fmtN(m2, k) + ')·R' + sb(c + 1)); chg.push(i3);
            for (var j3 = c; j3 < w; j3++) M[i3][j3] = j3 === c ? 0 : R(M[i3][j3] - R(m2 * M[c][j3]));
          }
          if (ops.length) push('Clear column ' + (c + 1) + ' above and below the pivot: ' + ops.join(';  '), matHTML(M, { k: k, sep: sep, rows: chg, piv: [c, c] }));
        }
      }
      if (mode === 'gauss') {
        push('Forward elimination finished: the left part is upper triangular. Now back substitution, from the last row up.', matHTML(M, { k: k, sep: sep }));
        var x = new Array(n).fill(null);
        for (var i4 = n - 1; i4 >= 0; i4--) {
          var s = M[i4][n], terms = [];
          for (var j4 = i4 + 1; j4 < n; j4++) { terms.push(fmtP(M[i4][j4], k) + '·' + fmtP(x[j4], k)); s = R(s - R(M[i4][j4] * x[j4])); }
          x[i4] = R(s / M[i4][i4]);
          push('x' + sb(i4 + 1) + ' = (' + fmtN(M[i4][n], k) + (terms.length ? ' − ' + terms.join(' − ') : '') + ') / ' + fmtN(M[i4][i4], k) + ' = <b>' + fmtN(x[i4], k) + '</b>',
            '<div class="wg-mats">' + labeled('[U | c]', matHTML(M, { k: k, sep: sep, rows: [i4] })) + labeled('x', vecCol(x, k, [i4])) + '</div>');
        }
        finish(A0, x, k);
      } else if (mode === 'gj') {
        var xs = M.map(function (r) { return r[n]; });
        push('The left part is the identity, so the last column is the solution: x = (' + xs.map(function (v) { return fmtN(v, k); }).join(', ') + '). No back substitution needed.', matHTML(M, { k: k, sep: sep }));
        finish(A0, xs, k);
      } else {
        var inv = M.map(function (r) { return r.slice(n); });
        var A = A0.map(function (r) { return r.slice(0, n); }), res = 0;
        for (var a = 0; a < n; a++) for (var b2 = 0; b2 < n; b2++) { var sum = 0; for (var q = 0; q < n; q++) sum += A[a][q] * inv[q][b2]; res = Math.max(res, Math.abs(sum - (a === b2 ? 1 : 0))); }
        push('Done: A⁻¹ is the right half. Check: the largest entry of A·A⁻¹ − I is ' + sci(res, 1) + '.', '<div class="wg-mats">' + labeled('A⁻¹', matHTML(inv, { k: k })) + '</div>');
      }
    }
    function finish(A0, x, k) {
      var n = x.length, A = A0.map(function (r) { return r.slice(0, n); }), b = A0.map(function (r) { return r[n]; });
      var res = 0; for (var i = 0; i < n; i++) { var s = b[i]; for (var j = 0; j < n; j++) s -= A[i][j] * x[j]; res = Math.max(res, Math.abs(s)); }
      var extra = 'Residual check: max |b − A x| = ' + sci(res, 2) + '.';
      if (k) { try { var ex = exactSolve(A, b); var err = 0; for (var q = 0; q < n; q++) err = Math.max(err, Math.abs(ex[q] - x[q])); extra += ' Full-precision answer: (' + ex.map(function (v) { return fmt(v, 6).replace(/\.?0+$/, ''); }).join(', ') + '); error of the ' + k + '-digit answer: <b>' + fmt(err, 4) + '</b>' + (err > 1e-2 * Math.max(1, Math.max.apply(null, ex.map(Math.abs))) ? ' <span class="bad">(wrong!)</span>' : '') + '.'; } catch (e) {} }
      states[states.length - 1].info = extra;
    }
    function exactSolve(A, b) {
      var n = b.length, M = A.map(function (r, i) { return r.concat([b[i]]); });
      for (var c = 0; c < n; c++) { var p = c; for (var i = c + 1; i < n; i++) if (Math.abs(M[i][c]) > Math.abs(M[p][c])) p = i; var t = M[c]; M[c] = M[p]; M[p] = t; for (var i2 = c + 1; i2 < n; i2++) { var m = M[i2][c] / M[c][c]; for (var j = c; j <= n; j++) M[i2][j] -= m * M[c][j]; } }
      var x = new Array(n); for (var i3 = n - 1; i3 >= 0; i3--) { var s = M[i3][n]; for (var j2 = i3 + 1; j2 < n; j2++) s -= M[i3][j2] * x[j2]; x[i3] = s / M[i3][i3]; } return x;
    }
    function lu(M0, n, k, R, piv) {
      var w = M0[0].length; if (w !== n && w !== n + 1) throw new Error('Type a square matrix A, or [A | b]');
      var U = M0.map(function (r) { return r.slice(0, n); }), b = w > n ? M0.map(function (r) { return r[n]; }) : null;
      var L = U.map(function (r, i) { return r.map(function (_, j) { return i === j ? 1 : (j > i ? 0 : null); }); }), P = U.map(function (_, i) { return i; });
      function pic(rowsU, cellsL, pv) {
        return '<div class="wg-mats">' + labeled('L', matHTML(L, { k: k, cells: cellsL, keepzero: false })) + labeled('U', matHTML(U, { k: k, rows: rowsU, piv: pv })) + (piv ? labeled('P (row order)', vecCol(P.map(function (v) { return v + 1; }), 0)) : '') + '</div>';
      }
      push('Start: U = A, and L = I with the multipliers still to be filled in (·).', pic([], []));
      for (var c = 0; c < n; c++) {
        if (piv) {
          var p = c; for (var i = c + 1; i < n; i++) if (Math.abs(U[i][c]) > Math.abs(U[p][c])) p = i;
          if (p !== c) { var t = U[c]; U[c] = U[p]; U[p] = t; for (var j0 = 0; j0 < c; j0++) { var tl = L[c][j0]; L[c][j0] = L[p][j0]; L[p][j0] = tl; } var tp = P[c]; P[c] = P[p]; P[p] = tp;
            push('Pivoting: swap rows ' + (c + 1) + ' and ' + (p + 1) + ' of U, of the multipliers already in L, and of P. (So we factor PA = LU.)', pic([c, p], [], [c, c])); }
        }
        if (Math.abs(U[c][c]) < 1e-14) {
          if (c === n - 1) throw new Error('u' + sb(n) + sb(n) + ' = 0: A is singular, so U has a zero on the diagonal and Ux = y cannot be solved.');
          throw new Error('Zero pivot u' + sb(c + 1) + sb(c + 1) + ' = 0: this A has no LU factorisation without row swaps. Turn on partial pivoting (PA = LU).');
        }
        var cells = [], rowsU = [];
        for (var i2 = c + 1; i2 < n; i2++) {
          var m = R(U[i2][c] / U[c][c]); L[i2][c] = m; cells.push([i2, c]);
          for (var j = c; j < n; j++) U[i2][j] = j === c ? 0 : R(U[i2][j] - R(m * U[c][j]));
          rowsU.push(i2);
          push('l' + sb(i2 + 1) + sb(c + 1) + ' = u' + sb(i2 + 1) + sb(c + 1) + ' / u' + sb(c + 1) + sb(c + 1) + ' = ' + fmtN(m, k) + ' goes into L;  then R' + sb(i2 + 1) + ' ← R' + sb(i2 + 1) + ' − (' + fmtN(m, k) + ')·R' + sb(c + 1) + ' in U.', pic([i2], [[i2, c]], [c, c]));
        }
      }
      for (var a = 0; a < n; a++) for (var b0 = 0; b0 < n; b0++) if (L[a][b0] === null) L[a][b0] = 0;
      push('Factorisation finished: ' + (piv ? 'PA' : 'A') + ' = LU. L holds the multipliers, U is the result of elimination. This part costs about 2n³/3 operations and is done once.', pic([], []));
      if (!b) return;
      var pb = P.map(function (i) { return b[i]; }), y = new Array(n).fill(null), x = new Array(n).fill(null);
      for (var i3 = 0; i3 < n; i3++) {
        var s = pb[i3], terms = []; for (var j3 = 0; j3 < i3; j3++) { terms.push(fmtP(L[i3][j3], k) + '·' + fmtP(y[j3], k)); s = R(s - R(L[i3][j3] * y[j3])); }
        y[i3] = s;
        push('Forward substitution, L y = ' + (piv ? 'Pb' : 'b') + ':  y' + sb(i3 + 1) + ' = ' + fmtN(pb[i3], k) + (terms.length ? ' − ' + terms.join(' − ') : '') + ' = <b>' + fmtN(y[i3], k) + '</b>', '<div class="wg-mats">' + labeled('L', matHTML(L, { k: k, rows: [i3] })) + labeled(piv ? 'Pb' : 'b', vecCol(pb, k, [i3])) + labeled('y', vecCol(y, k, [i3])) + '</div>');
      }
      for (var i4 = n - 1; i4 >= 0; i4--) {
        var s2 = y[i4], terms2 = []; for (var j4 = i4 + 1; j4 < n; j4++) { terms2.push(fmtP(U[i4][j4], k) + '·' + fmtP(x[j4], k)); s2 = R(s2 - R(U[i4][j4] * x[j4])); }
        x[i4] = R(s2 / U[i4][i4]);
        push('Back substitution, U x = y:  x' + sb(i4 + 1) + ' = (' + fmtN(y[i4], k) + (terms2.length ? ' − ' + terms2.join(' − ') : '') + ') / ' + fmtN(U[i4][i4], k) + ' = <b>' + fmtN(x[i4], k) + '</b>', '<div class="wg-mats">' + labeled('U', matHTML(U, { k: k, rows: [i4] })) + labeled('y', vecCol(y, k)) + labeled('x', vecCol(x, k, [i4])) + '</div>');
      }
      push('Solution x = (' + x.map(function (v) { return fmtN(v, k); }).join(', ') + '). A new right-hand side b needs only the two substitutions: about 2n² operations.', '<div class="wg-mats">' + labeled('L', matHTML(L, { k: k })) + labeled('U', matHTML(U, { k: k })) + labeled('x', vecCol(x, k)) + '</div>');
      finish(M0, x, k);
    }
    function chol(M0, n, k, R) {
      var w = M0[0].length; if (w !== n && w !== n + 1) throw new Error('Type a square symmetric matrix A, or [A | b]');
      var A = M0.map(function (r) { return r.slice(0, n); }), b = w > n ? M0.map(function (r) { return r[n]; }) : null;
      for (var i = 0; i < n; i++) for (var j = 0; j < i; j++) if (Math.abs(A[i][j] - A[j][i]) > 1e-12) throw new Error('Cholesky needs a symmetric matrix: a' + sb(i + 1) + sb(j + 1) + ' ≠ a' + sb(j + 1) + sb(i + 1) + '.');
      var L = A.map(function (r, i) { return r.map(function (_, j) { return j > i ? 0 : null; }); });
      function pic(cells) { return '<div class="wg-mats">' + labeled('A', matHTML(A, { k: k, colhi: cells.length ? cells[0][1] : undefined })) + labeled('L', matHTML(L, { k: k, cells: cells })) + '</div>'; }
      push('Start: find lower-triangular L with A = L Lᵀ, one column at a time.', pic([]));
      for (var c = 0; c < n; c++) {
        var s = A[c][c], terms = []; for (var q = 0; q < c; q++) { s = R(s - R(L[c][q] * L[c][q])); terms.push(fmtP(L[c][q], k) + '²'); }
        if (!(s > 0)) { L[c][c] = NaN; throw new Error('l' + sb(c + 1) + sb(c + 1) + ' = √(' + fmtN(s, k) + '): the number under the root is not positive, so A is not positive definite. Cholesky stops here (use LU instead).'); }
        L[c][c] = R(Math.sqrt(s));
        var txt = 'l' + sb(c + 1) + sb(c + 1) + ' = √(a' + sb(c + 1) + sb(c + 1) + (terms.length ? ' − ' + terms.join(' − ') : '') + ') = √' + fmtN(s, k) + ' = <b>' + fmtN(L[c][c], k) + '</b>';
        var cells = [[c, c]], parts = [];
        for (var i2 = c + 1; i2 < n; i2++) {
          var s2 = A[i2][c]; for (var q2 = 0; q2 < c; q2++) s2 = R(s2 - R(L[i2][q2] * L[c][q2]));
          L[i2][c] = R(s2 / L[c][c]); cells.push([i2, c]); parts.push('l' + sb(i2 + 1) + sb(c + 1) + ' = ' + fmtN(L[i2][c], k));
        }
        push(txt + (parts.length ? ';  below it: ' + parts.join(', ') + '  (from l' + 'ᵢ' + sb(c + 1) + ' = (a' + 'ᵢ' + sb(c + 1) + ' − Σ l' + 'ᵢ' + '·l' + sb(c + 1) + '·) / l' + sb(c + 1) + sb(c + 1) + ')' : ''), pic(cells));
      }
      push('A = L Lᵀ. Only one triangle is computed: about n³/3 operations, half the cost of LU.', pic([]));
      if (!b) return;
      var y = new Array(n).fill(null), x = new Array(n).fill(null), LT = L.map(function (r, i) { return r.map(function (_, j) { return L[j][i]; }); });
      for (var i3 = 0; i3 < n; i3++) { var s3 = b[i3]; for (var j3 = 0; j3 < i3; j3++) s3 = R(s3 - R(L[i3][j3] * y[j3])); y[i3] = R(s3 / L[i3][i3]); }
      push('Forward substitution L y = b:  y = (' + y.map(function (v) { return fmtN(v, k); }).join(', ') + ')', '<div class="wg-mats">' + labeled('L', matHTML(L, { k: k })) + labeled('b', vecCol(b, k)) + labeled('y', vecCol(y, k)) + '</div>');
      for (var i4 = n - 1; i4 >= 0; i4--) { var s4 = y[i4]; for (var j4 = i4 + 1; j4 < n; j4++) s4 = R(s4 - R(LT[i4][j4] * x[j4])); x[i4] = R(s4 / LT[i4][i4]); }
      push('Back substitution Lᵀ x = y:  x = (<b>' + x.map(function (v) { return fmtN(v, k); }).join(', ') + '</b>)', '<div class="wg-mats">' + labeled('Lᵀ', matHTML(LT, { k: k })) + labeled('y', vecCol(y, k)) + labeled('x', vecCol(x, k)) + '</div>');
      finish(M0, x, k);
    }
    function show() {
      if (!states.length) return;
      var s = states[step];
      opsTxt.innerHTML = s.text; view.innerHTML = s.html; info.innerHTML = s.info || '';
      ctr.textContent = 'step ' + step + ' of ' + (states.length - 1);
    }
    build();
  };

  /* ============================================================= L11: Cramer's rule, adjugate inverse, norms and condition number */
  function detRec(A) {
    var n = A.length; if (n === 1) return A[0][0]; if (n === 2) return A[0][0] * A[1][1] - A[0][1] * A[1][0];
    var d = 0; for (var j = 0; j < n; j++) { if (A[0][j] === 0) continue; d += (j % 2 ? -1 : 1) * A[0][j] * detRec(minor(A, 0, j)); } return d;
  }
  function minor(A, r, c) { return A.filter(function (_, i) { return i !== r; }).map(function (row) { return row.filter(function (_, j) { return j !== c; }); }); }
  W.cramer = function (host, o) {
    card(host, 'wg-cramer');
    var ta = h('textarea', { class: 'wg-ta', rows: 3, spellcheck: 'false', 'aria-label': 'Augmented matrix' }); ta.value = String(o.mat || '7 -2 0 12; -2 9 -3 2; 0 -3 6 3').split(';').map(function (r) { return r.trim(); }).join('\n');
    var view = o.view || 'cramer';
    var vSel = select('Show', [['cramer', "Cramer's rule"], ['inv', 'Inverse by the adjugate'], ['cond', 'Norms and condition number']], view, function (v) { view = v; draw(); });
    var presets = o.presets ? row(o.presets.map(function (p) { return btn(p[0], function () { ta.value = p[1].split(';').map(function (r) { return r.trim(); }).join('\n'); draw(); }, 'chip'); }), 'wg-chips') : null;
    var out = h('div', { class: 'wg-matview' });
    if (!o.noinput) host.appendChild(row([h('div', { class: 'wg-inbox' }, [h('span', { class: 'wg-hint', html: 'Augmented matrix [A | b], one row per line (2×2 to 4×4)' }), ta]), h('div', { class: 'wg-col' }, [o.fixed ? null : vSel.el, presets].filter(Boolean))], 'wg-top'));
    host.appendChild(out);
    ta.addEventListener('input', draw);
    function draw() {
      var M; try { M = parseMat(ta.value); } catch (e) { out.innerHTML = ''; out.appendChild(errBox(e.message)); return; }
      var n = M.length; if (n < 2 || n > 4 || M[0].length !== n + 1) { out.innerHTML = ''; out.appendChild(errBox('Type n rows of n + 1 numbers (n = 2, 3 or 4)')); return; }
      var A = M.map(function (r) { return r.slice(0, n); }), b = M.map(function (r) { return r[n]; }), D = detRec(A), html = '';
      if (view === 'cramer') {
        html += '<div class="wg-mats">' + labeled('D = det A = <b>' + fmtN(D) + '</b>', matHTML(A, {})) + '</div>';
        if (Math.abs(D) < 1e-12) { out.innerHTML = html + '<p class="bad">D = 0: Cramer\'s rule cannot be used (no unique solution).</p>'; return; }
        var boxes = '', xs = [];
        for (var i = 0; i < n; i++) {
          var Ai = A.map(function (r, rr) { var c = r.slice(); c[i] = b[rr]; return c; }), Di = detRec(Ai); xs.push(Di / D);
          boxes += labeled('D' + sb(i + 1) + ' = ' + fmtN(Di) + ' → x' + sb(i + 1) + ' = ' + fmtN(Di) + ' / ' + fmtN(D) + ' = <b>' + fmtN(Di / D) + '</b>', matHTML(Ai, { colhi: i }));
        }
        html += '<div class="wg-mats">' + boxes + '</div><p class="wg-note">Each Dᵢ is det A with column i replaced by b (shaded). ' + (n + 1) + ' determinants of size ' + n + '×' + n + '.</p>';
      } else {
        if (Math.abs(D) < 1e-12) { out.innerHTML = '<p class="bad">det A = 0: A has no inverse.</p>'; return; }
        var C = A.map(function (r, i) { return r.map(function (_, j) { return ((i + j) % 2 ? -1 : 1) * detRec(minor(A, i, j)); }); });
        var adj = C.map(function (r, i) { return r.map(function (_, j) { return C[j][i]; }); }), inv = adj.map(function (r) { return r.map(function (v) { return v / D; }); });
        if (view === 'inv') {
          var x = inv.map(function (r) { return r.reduce(function (s, v, j) { return s + v * b[j]; }, 0); });
          html += '<div class="wg-mats">' + labeled('Cofactors Cᵢⱼ', matHTML(C, {})) + labeled('adj A = Cᵀ', matHTML(adj, {})) + labeled('A⁻¹ = adj A / ' + fmtN(D), matHTML(inv, {})) + labeled('x = A⁻¹b', vecCol(x)) + '</div>';
          html += '<p class="wg-note">Cᵢⱼ = (−1)<sup>i+j</sup> × (determinant of A without row i and column j). det A = ' + fmtN(D) + '.</p>';
        } else {
          var rs = function (X) { return Math.max.apply(null, X.map(function (r) { return r.reduce(function (s, v) { return s + Math.abs(v); }, 0); })); };
          var cs = function (X) { return Math.max.apply(null, X[0].map(function (_, j) { return X.reduce(function (s, r) { return s + Math.abs(r[j]); }, 0); })); };
          var nA = rs(A), nI = rs(inv), n1 = cs(A), n1i = cs(inv);
          var bn = Math.max.apply(null, b.map(Math.abs)), xs2 = inv.map(function (r) { return r.reduce(function (s, v, j) { return s + v * b[j]; }, 0); }), xn = Math.max.apply(null, xs2.map(Math.abs));
          html += '<div class="wg-mats">' + labeled('A', matHTML(A, {})) + labeled('A⁻¹', matHTML(inv, {})) + '</div>';
          html += '<div class="wg-info">' + table(['quantity', 'value'], [
            ['‖A‖∞ (largest row sum of |aᵢⱼ|)', fmt(nA, 4)], ['‖A⁻¹‖∞', fmt(nI, 4)], ['<b>κ∞(A) = ‖A‖∞ ‖A⁻¹‖∞</b>', '<b>' + fmt(nA * nI, 2) + '</b>'], ['‖A‖₁ (largest column sum), κ₁(A)', fmt(n1, 4) + ',  ' + fmt(n1 * n1i, 2)],
            ['meaning', nA * nI < 100 ? 'well-conditioned: relative errors in b grow by at most ' + fmt(nA * nI, 1) + '×' : 'ill-conditioned: a relative error in b can grow up to ' + fmt(nA * nI, 0) + '× in x (about ' + Math.round(Math.log10(nA * nI)) + ' digits lost)'],
            ['solution', '(' + xs2.map(function (v) { return fmtN(v); }).join(', ') + '),  ‖x‖∞ = ' + fmt(xn, 4) + ',  ‖b‖∞ = ' + fmt(bn, 4)]]).outerHTML + '</div>';
        }
      }
      out.innerHTML = html;
    }
    draw();
  };

  /* ============================================================= L11–13: operation counts */
  function log10Cramer(n) {   // (n+1)·T(n) + n, with T(n) = n·T(n−1) + 2n − 1 operations for one cofactor determinant
    if (n <= 150) { var t = 0; for (var k = 2; k <= n; k++) t = k * t + 2 * k - 1; return Math.log10((n + 1) * t + n); }
    var lf = (n * Math.log(n) - n + 0.5 * Math.log(2 * Math.PI * n) + 1 / (12 * n)) / Math.LN10;   // Stirling: log10 n!
    return Math.log10(Math.E) + lf + Math.log10(n + 1);   // T(n)/n! tends to e
  }
  var COST = {
    cramer: { name: "Cramer (cofactor determinants)", f: function (n) { return log10Cramer(n); }, col: 'c5' },
    inv: { name: 'Inverse, then x = A⁻¹b', f: function (n) { return Math.log10(2 * n * n * n + 2 * n * n); }, col: 'c4' },
    gj: { name: 'Gauss–Jordan', f: function (n) { return Math.log10(n * n * n + n * n / 2 - n / 2); }, col: 'c1' },
    gauss: { name: 'Gaussian elimination', f: function (n) { return Math.log10(2 * n * n * n / 3 + 1.5 * n * n - 7 * n / 6); }, col: 'c2' },
    chol: { name: 'Cholesky (symmetric positive definite)', f: function (n) { return Math.log10(n * n * n / 3 + 2 * n * n); }, col: 'c3' },
    lusolve: { name: 'LU: each extra right-hand side', f: function (n) { return Math.log10(2 * n * n - n); }, col: 'mut' },
    thomas: { name: 'Thomas (tridiagonal)', f: function (n) { return Math.log10(8 * n - 7); }, col: 'c3' }
  };
  function human(sec) {
    if (sec < 1e-6) return fmt(sec * 1e9, 1) + ' ns'; if (sec < 1e-3) return fmt(sec * 1e6, 1) + ' µs'; if (sec < 1) return fmt(sec * 1e3, 1) + ' ms';
    if (sec < 120) return fmt(sec, 1) + ' s'; if (sec < 7200) return fmt(sec / 60, 1) + ' min'; if (sec < 172800) return fmt(sec / 3600, 1) + ' hours'; if (sec < 3.156e7 * 2) return fmt(sec / 86400, 0) + ' days';
    var y = sec / 3.156e7; if (y < 1e6) return fmt(y, 0) + ' years'; if (y < 1.38e10) return sci(y, 1) + ' years'; return sci(y, 1) + ' years (' + sci(y / 1.38e10, 1) + ' × the age of the universe)';
  }
  W.cost = function (host, o) {
    card(host, 'wg-cost');
    var keys = o.methods || ['cramer', 'inv', 'gj', 'gauss'];
    var NS = o.ns || [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 100000, 1000000];
    var start = NS.indexOf(o.n || 20); if (start < 0) start = 9;
    var sl = slider('Unknowns n', 0, NS.length - 1, 1, start, draw, function (i) { return NS[i].toLocaleString('en-US'); });
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '300px') }), P = new Plot(pl), tbl = h('div');
    host.appendChild(row([sl.el, h('span', { class: 'wg-hint', html: 'time assumes a computer doing 10⁹ operations per second' })])); host.appendChild(pl); host.appendChild(tbl);
    P.onresize = draw;
    function draw() {
      var n = NS[sl.value], c = P.begin();
      var xmax = Math.min(6, Math.max(2, Math.ceil(Math.log10(n) + 0.5)));
      var ymax = 10; keys.forEach(function (key) { if (key !== 'cramer') ymax = Math.max(ymax, COST[key].f(Math.pow(10, xmax))); });
      ymax = Math.ceil((ymax + 4) / 5) * 5;
      P.o.xfmt = function (v) { return Math.abs(v - Math.round(v)) < 1e-9 ? (Math.round(v) <= 3 ? String(Math.pow(10, Math.round(v))) : '10^' + Math.round(v)) : ''; };
      P.o.yfmt = function (v) { return '10^' + Math.round(v); }; P.o.xstep = 1;
      P.range(Math.log10(2), xmax, 0, ymax); P.axes('n (log scale)', 'operations');
      var leg = [];
      keys.forEach(function (key) {
        var C = COST[key], col = P.col[C.col], pts = [];
        var ns = []; for (var i = 0; i <= 240; i++) { var nn = Math.pow(10, Math.log10(2) + (xmax - Math.log10(2)) * i / 240); if (key === 'cramer') nn = Math.round(nn); if (!ns.length || nn !== ns[ns.length - 1]) ns.push(nn); }
        ns.forEach(function (nn) { pts.push([Math.log10(nn), Math.min(C.f(nn), 200)]); });
        P.poly(pts, col, 2.8); leg.push([C.name, col]);
        P.dot(Math.log10(n), Math.min(C.f(n), 200), 5, col);
      });
      P.seg(Math.log10(n), 0, Math.log10(n), 200, P.col.mut, 1.2, [4, 4]);
      P.legend(leg);
      var rows = keys.map(function (key) { var lg = COST[key].f(n); return [COST[key].name, lg < 15 ? Math.round(Math.pow(10, lg)).toLocaleString('en-US') : '≈ ' + sci(Math.pow(10, lg % 1), 2).replace(/e\+?0$/, '') + ' × 10^' + Math.floor(lg), human(Math.pow(10, lg - 9))]; });
      tbl.innerHTML = ''; tbl.appendChild(table(['method (n = ' + n.toLocaleString('en-US') + ')', 'operations', 'time'], rows));
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L14: Jacobi / Gauss–Seidel / SOR in two unknowns */
  function eqStr(a, b, e) {
    function t(c, v, first) { if (c === 0) return ''; var s = Math.abs(c) === 1 ? v : fmtN(Math.abs(c)) + v; return first ? (c < 0 ? '−' : '') + s : (c < 0 ? ' − ' : ' + ') + s; }
    var l = t(a, 'x', true); l += t(b, 'y', !l); return (l || '0') + ' = ' + fmtN(e);
  }
  W.iter2d = function (host, o) {
    card(host, 'wg-iter2d');
    var mF = field('System', o.mat || '4 -1 3; -2 5 3', { size: '12em' });
    var meth = o.method || 'jacobi';
    var mSel = select('Method', [['jacobi', 'Jacobi'], ['gs', 'Gauss–Seidel'], ['sor', 'SOR']], meth, function (v) { meth = v; wS.el.style.display = v === 'sor' ? '' : 'none'; draw(); });
    var wS = slider('ω', 0.1, 1.9, 0.05, o.omega || 1.1, draw, function (v) { return v.toFixed(2); }); wS.el.style.display = meth === 'sor' ? '' : 'none';
    var xF = field('x₀ =', o.x0 !== undefined ? o.x0 : 0, { size: '3.5em' }), yF = field('y₀ =', o.y0 !== undefined ? o.y0 : 0, { size: '3.5em' });
    var step = o.step || 1;
    var presets = o.presets ? row(o.presets.map(function (p) { return btn(p[0], function () { mF.input.value = p[1]; if (p[2]) { meth = p[2]; mSel.input.value = meth; wS.el.style.display = meth === 'sor' ? '' : 'none'; } step = 1; draw(); }, 'chip'); }), 'wg-chips') : null;
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '330px') }), P = new Plot(pl);
    var tbl = h('div', { class: 'wg-scroll', style: o.tableHeight ? 'max-height:' + o.tableHeight : '' }), info = h('div', { class: 'wg-note' });
    host.appendChild(row([mF.el, o.fixed ? null : mSel.el, wS.el].filter(Boolean))); if (presets) host.appendChild(presets);
    host.appendChild(row([xF.el, yF.el, btn('◀', function () { if (step > 1) step--; draw(); }), btn('Next step ▶', function () { step++; draw(); }, 'pri'), btn('+10', function () { step += 10; draw(); }), btn('Reset', function () { step = 1; draw(); })]));
    host.appendChild(h('div', { class: o.side ? 'wg-side' : '' }, [pl, tbl])); host.appendChild(info);
    [mF.input, xF.input, yF.input].forEach(function (i) { i.addEventListener('input', function () { step = 1; draw(); }); });
    P.onresize = draw;
    function eig2(T) { var tr = T[0][0] + T[1][1], dt = T[0][0] * T[1][1] - T[0][1] * T[1][0], disc = tr * tr / 4 - dt; return disc >= 0 ? Math.max(Math.abs(tr / 2 + Math.sqrt(disc)), Math.abs(tr / 2 - Math.sqrt(disc))) : Math.sqrt(Math.abs(dt)); }
    function draw() {
      var M; try { M = parseMat(mF.input.value); if (M.length !== 2 || M[0].length !== 3) throw new Error('Type two rows: a₁₁ a₁₂ b₁; a₂₁ a₂₂ b₂'); } catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox(e.message)); return; }
      var a = M[0][0], b = M[0][1], e1 = M[0][2], c = M[1][0], d = M[1][1], e2 = M[1][2];
      if (!a || !d) { tbl.innerHTML = ''; tbl.appendChild(errBox('The diagonal entries a₁₁ and a₂₂ must be nonzero (each equation is solved for its own unknown).')); return; }
      var det = a * d - b * c, xs = (e1 * d - b * e2) / det, ys = (a * e2 - e1 * c) / det, w = meth === 'sor' ? wS.value : 1;
      var x = num(xF.input, 0), y = num(yF.input, 0), path = [[x, y]], rows = [[0, fmt(x, 6), fmt(y, 6), '', sci(Math.max(Math.abs(x - xs), Math.abs(y - ys)), 2)]];
      for (var k = 1; k <= step; k++) {
        var xn, yn;
        if (meth === 'jacobi') { xn = (e1 - b * y) / a; yn = (e2 - c * x) / d; path.push([xn, yn]); }
        else { xn = (1 - w) * x + w * (e1 - b * y) / a; path.push([xn, y]); yn = (1 - w) * y + w * (e2 - c * xn) / d; path.push([xn, yn]); }
        var ch = Math.max(Math.abs(xn - x), Math.abs(yn - y)); x = xn; y = yn;
        rows.push([k, fmt(x, 6), fmt(y, 6), sci(ch, 2), sci(Math.max(Math.abs(x - xs), Math.abs(y - ys)), 2)]);
        if (!isFinite(x) || Math.abs(x) > 1e12) break;
      }
      var fin = path.filter(function (p) { return isFinite(p[0]) && isFinite(p[1]) && Math.abs(p[0]) < 1e6 && Math.abs(p[1]) < 1e6; });
      var xsAll = fin.map(function (p) { return p[0]; }).concat([xs]), ysAll = fin.map(function (p) { return p[1]; }).concat([ys]);
      var x0 = Math.min.apply(null, xsAll), x1 = Math.max.apply(null, xsAll), y0 = Math.min.apply(null, ysAll), y1 = Math.max.apply(null, ysAll);
      var span = Math.max(x1 - x0, y1 - y0, 1) * 0.6, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
      P.begin(); P.range(cx - span * 1.25, cx + span * 1.25, cy - span, cy + span); P.axes('x', 'y');
      if (b !== 0) P.fn(function (t) { return (e1 - a * t) / b; }, P.col.c1, 2.6); else P.seg(e1 / a, cy - 1e3, e1 / a, cy + 1e3, P.col.c1, 2.6);
      if (d !== 0) P.fn(function (t) { return (e2 - c * t) / d; }, P.col.c3, 2.6);
      P.poly(fin, P.col.c2, 2, [6, 4]);
      fin.forEach(function (p, i) { if (meth === 'jacobi' || i % 2 === 0) P.dot(p[0], p[1], i === fin.length - 1 ? 7 : 4, i === fin.length - 1 ? P.col.c5 : P.col.c2); });
      P.dot(xs, ys, 7, P.col.ink, true);
      P.legend([['eq. 1: ' + eqStr(a, b, e1), P.col.c1], ['eq. 2: ' + eqStr(c, d, e2), P.col.c3], [{ jacobi: 'Jacobi', gs: 'Gauss–Seidel', sor: 'SOR (ω = ' + w.toFixed(2) + ')' }[meth] + ' iterates', P.col.c2, [6, 4]]]);
      tbl.innerHTML = ''; tbl.appendChild(table(['k', 'xₖ', 'yₖ', 'change', 'error'], rows, { hi: rows.length - 1 }));
      var TJ = [[0, -b / a], [-c / d, 0]], rho;
      if (meth === 'jacobi') rho = eig2(TJ);
      else { var Tw = [[1 - w, -w * b / a], [-(w * c / d) * (1 - w), (w * c / d) * (w * b / a) + 1 - w]]; rho = eig2(Tw); }
      var dd1 = Math.abs(a) > Math.abs(b), dd2 = Math.abs(d) > Math.abs(c);
      info.innerHTML = 'Diagonal dominance: |' + a + '| ' + (dd1 ? '>' : '≤') + ' |' + b + '| and |' + d + '| ' + (dd2 ? '>' : '≤') + ' |' + c + '| → ' + (dd1 && dd2 ? '<b style="color:var(--w-c3)">yes</b> (convergence guaranteed)' : '<b style="color:var(--w-c5)">no</b>') +
        '. Spectral radius of the iteration matrix ρ = <b>' + fmt(rho, 4) + '</b>: ' + (rho < 1 ? 'each step multiplies the error by about ' + fmt(rho, 3) + ', so it <b style="color:var(--w-c3)">converges</b> (≈ ' + Math.ceil(-6 / Math.log10(rho)) + ' steps per 6 digits).' : 'the error grows, so it <b style="color:var(--w-c5)">diverges</b>.') +
        (meth !== 'jacobi' ? ' Gauss–Seidel moves horizontally to line 1, then vertically to line 2.' : ' Jacobi updates x and y together from the old values.');
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L14: heat plate by Jacobi, Gauss–Seidel and SOR */
  var HEAT = [[43, 76, 155], [111, 163, 220], [243, 227, 160], [240, 163, 94], [192, 57, 43]];
  function heatCol(t) { t = Math.max(0, Math.min(1, t)) * 4; var i = Math.min(3, Math.floor(t)), f = t - i, a = HEAT[i], b = HEAT[i + 1]; return 'rgb(' + [0, 1, 2].map(function (k) { return Math.round(a[k] + (b[k] - a[k]) * f); }).join(',') + ')'; }
  W.plate = function (host, o) {
    card(host, 'wg-plate');
    var Nsl = slider('Grid N × N', 2, 40, 1, o.N || 10, draw, function (v) { return v + '×' + v + ' = ' + v * v + ' unknowns'; });
    var bc = o.bc || [100, 50, 0, 0];
    var tF = field('top', bc[0], { size: '3.2em' }), rF = field('right', bc[1], { size: '3.2em' }), bF = field('bottom', bc[2], { size: '3.2em' }), lF = field('left', bc[3], { size: '3.2em' });
    var wsl = slider('SOR ω', 1, 1.98, 0.01, o.omega || 1.5, draw, function (v) { return v.toFixed(2); });
    var plW = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '300px') }), P = new Plot(plW, { logy: true });
    var hm = h('canvas', { class: 'wg-heat', width: 240, height: 240 }), tbl = h('div'), info = h('div', { class: 'wg-note' });
    host.appendChild(row([Nsl.el, wsl.el, btn('use best ω', function () { var N = Nsl.value; wsl.input.value = (2 / (1 + Math.sin(Math.PI / (N + 1)))).toFixed(2); wsl.update(); }, 'chip')]));
    host.appendChild(row([h('span', { class: 'wg-hint', html: 'Edge temperatures:' }), tF.el, rF.el, bF.el, lF.el]));
    host.appendChild(h('div', { class: 'wg-heatrow' }, [plW, h('div', { class: 'wg-heatbox' }, [hm, h('span', { class: 'wg-hint', text: 'SOR solution' })])]));
    host.appendChild(tbl); host.appendChild(info);
    [tF.input, rF.input, bF.input, lF.input].forEach(function (i) { i.addEventListener('input', draw); });
    P.onresize = draw;
    function solve(N, B, kind, w, tol, maxit) {
      var T = []; for (var i = 0; i < N + 2; i++) { T.push(new Float64Array(N + 2)); }
      for (var j = 1; j <= N; j++) { T[0][j] = B[0]; T[N + 1][j] = B[2]; } for (var i2 = 1; i2 <= N; i2++) { T[i2][0] = B[3]; T[i2][N + 1] = B[1]; }
      var hist = [], it, old = kind === 'jacobi' ? T.map(function (r) { return Float64Array.from(r); }) : null;
      for (it = 1; it <= maxit; it++) {
        var ch = 0;
        if (kind === 'jacobi') {
          for (var a = 1; a <= N; a++) for (var b = 1; b <= N; b++) { var v = 0.25 * (old[a - 1][b] + old[a + 1][b] + old[a][b - 1] + old[a][b + 1]); ch = Math.max(ch, Math.abs(v - old[a][b])); T[a][b] = v; }
          for (var a2 = 1; a2 <= N; a2++) old[a2].set(T[a2]);
        } else {
          for (var c = 1; c <= N; c++) for (var d = 1; d <= N; d++) { var gs = 0.25 * (T[c - 1][d] + T[c + 1][d] + T[c][d - 1] + T[c][d + 1]), nv = T[c][d] + w * (gs - T[c][d]); ch = Math.max(ch, Math.abs(nv - T[c][d])); T[c][d] = nv; }
        }
        hist.push(Math.max(ch, 1e-16));
        if (ch < tol) break;
      }
      return { T: T, it: it > maxit ? null : it, hist: hist };
    }
    function draw() {
      var N = Nsl.value, B = [num(tF.input, 100), num(rF.input, 50), num(bF.input, 0), num(lF.input, 0)], w = wsl.value, tol = o.tol || 1e-4, maxit = 20000;
      var J = solve(N, B, 'jacobi', 1, tol, maxit), G2 = solve(N, B, 'gs', 1, tol, maxit), S = solve(N, B, 'sor', w, tol, maxit);
      var mx = Math.max(J.hist.length, G2.hist.length, S.hist.length);
      var c = P.begin(); P.range(0, mx, -5, Math.ceil(Math.log10(Math.max(J.hist[0], G2.hist[0], S.hist[0], 1)))); P.axes('iteration', 'largest change');
      [[J, P.col.c1, 'Jacobi'], [G2, P.col.c2, 'Gauss–Seidel'], [S, P.col.c3, 'SOR ω = ' + w.toFixed(2)]].forEach(function (r) { P.poly(r[0].hist.map(function (v, i) { return [i + 1, v]; }), r[1], 2.4); });
      P.legend([['Jacobi', P.col.c1], ['Gauss–Seidel', P.col.c2], ['SOR ω = ' + w.toFixed(2), P.col.c3]]);
      // heat map
      var ctx = hm.getContext('2d'), sz = hm.width, cell = sz / (N + 2), lo = Math.min.apply(null, B), hi = Math.max.apply(null, B);
      for (var i = 0; i < N + 2; i++) for (var j = 0; j < N + 2; j++) {
        var corner = (i === 0 || i === N + 1) && (j === 0 || j === N + 1);
        var v = S.T[i][j], t = hi > lo ? (v - lo) / (hi - lo) : 0.5;
        ctx.fillStyle = corner ? '#ffffff' : heatCol(t);
        ctx.fillRect(j * cell, i * cell, Math.ceil(cell), Math.ceil(cell));
      }
      var rJ = Math.cos(Math.PI / (N + 1)), wopt = 2 / (1 + Math.sin(Math.PI / (N + 1)));
      tbl.innerHTML = ''; tbl.appendChild(table(['method', 'iterations until the largest change < ' + sci(tol, 0), 'spectral radius ρ'], [
        ['Jacobi', J.it ? String(J.it) : '> ' + maxit, fmt(rJ, 5)], ['Gauss–Seidel', G2.it ? String(G2.it) : '> ' + maxit, fmt(rJ * rJ, 5)],
        ['SOR, ω = ' + w.toFixed(2), S.it ? String(S.it) : '> ' + maxit, Math.abs(w - wopt) < 0.005 ? fmt(wopt - 1, 5) + ' (best ω)' : '—']]));
      var mid = N % 2 ? S.T[(N + 1) / 2][(N + 1) / 2] : (S.T[N / 2][N / 2] + S.T[N / 2 + 1][N / 2] + S.T[N / 2][N / 2 + 1] + S.T[N / 2 + 1][N / 2 + 1]) / 4;
      info.innerHTML = 'Each interior temperature is the average of its four neighbours. Best ω = 2 / (1 + sin(π/(N+1))) = <b>' + fmt(wopt, 3) + '</b>. Centre temperature ≈ ' + fmt(mid, 3) + '. One sweep costs about 5 operations per unknown; a direct solve of the full matrix would cost about ' + sci(2 * Math.pow(N * N, 3) / 3, 1) + '.';
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= Module 4 helpers: interpolation */
  function parseList(s) {
    var v = String(s).replace(/−/g, '-').split(/[\s,;]+/).filter(function (t) { return t.length; }).map(function (t) { var n = Number(t); if (!isFinite(n)) throw new Error('Not a number: ' + t); return n; });
    if (!v.length) throw new Error('Type some numbers, separated by spaces or commas');
    return v;
  }
  function diffTable(y) { var t = [y.slice()]; while (t[t.length - 1].length > 1) { var p = t[t.length - 1], q = []; for (var i = 0; i < p.length - 1; i++) q.push(p[i + 1] - p[i]); t.push(q); } return t; }
  function clean(v) { return Math.abs(v) < 1e-11 * (1 + Math.abs(v)) ? 0 : +v.toPrecision(12); }
  function fmtD(v) { v = clean(v); if (Math.abs(v - Math.round(v)) < 1e-9) return String(Math.round(v)).replace('-', '−'); var a = Math.abs(v); return (a >= 1e5 || a < 1e-4 ? sci(v, 3) : String(+v.toFixed(6))).replace('-', '−'); }
  function naturalSpline(xs, ys) {
    var n = xs.length, h = [], M = new Array(n).fill(0);
    for (var i = 0; i < n - 1; i++) { h.push(xs[i + 1] - xs[i]); if (!(h[i] > 0)) throw new Error('x values must increase'); }
    if (n > 2) {
      var m = n - 2, a = [], b = [], c = [], d = [];
      for (var k = 1; k <= m; k++) { a.push(h[k - 1]); b.push(2 * (h[k - 1] + h[k])); c.push(h[k]); d.push(6 * ((ys[k + 1] - ys[k]) / h[k] - (ys[k] - ys[k - 1]) / h[k - 1])); }
      for (var j = 1; j < m; j++) { var w = a[j] / b[j - 1]; b[j] -= w * c[j - 1]; d[j] -= w * d[j - 1]; }
      var sol = new Array(m); sol[m - 1] = d[m - 1] / b[m - 1];
      for (var j2 = m - 2; j2 >= 0; j2--) sol[j2] = (d[j2] - c[j2] * sol[j2 + 1]) / b[j2];
      for (var k2 = 0; k2 < m; k2++) M[k2 + 1] = sol[k2];
    }
    function S(x) {
      var i = 0; while (i < n - 2 && x > xs[i + 1]) i++;
      var hh = h[i], A = xs[i + 1] - x, B = x - xs[i];
      return M[i] * A * A * A / (6 * hh) + M[i + 1] * B * B * B / (6 * hh) + (ys[i] - M[i] * hh * hh / 6) * A / hh + (ys[i + 1] - M[i + 1] * hh * hh / 6) * B / hh;
    }
    S.M = M; S.h = h; return S;
  }
  function lagrangeEval(xs, ys, x) { var s = 0; for (var i = 0; i < xs.length; i++) { var L = 1; for (var j = 0; j < xs.length; j++) if (j !== i) L *= (x - xs[j]) / (xs[i] - xs[j]); s += ys[i] * L; } return s; }
  function baryWeights(xs) { return xs.map(function (xi, i) { var w = 1; xs.forEach(function (xj, j) { if (j !== i) w *= (xi - xj); }); return 1 / w; }); }
  function baryEval(xs, ys, w, x) { var num = 0, den = 0; for (var i = 0; i < xs.length; i++) { if (x === xs[i]) return ys[i]; var t = w[i] / (x - xs[i]); num += t * ys[i]; den += t; } return num / den; }

  /* ============================================================= L15: difference table */
  W.difftab = function (host, o) {
    card(host, 'wg-difftab');
    var x0F = field('x₀ =', o.x0 !== undefined ? o.x0 : 0, { size: '4em' }), hF = field('h =', o.h || 1, { size: '3.5em' }), yF = field('y =', o.y || '1 0 5 22 57 116 205', { size: '16em' });
    var mode = o.mode || 'forward';
    var mSel = select('Show', [['forward', 'forward differences Δ (top diagonal)'], ['backward', 'backward differences ∇ (bottom diagonal)'], ['none', 'plain table']], mode, function (v) { mode = v; draw(); });
    var eF = field('add error ε =', o.eps || 0, { size: '3.5em' }), kF = field('to entry k =', o.k !== undefined ? o.k : 3, { size: '3em' });
    var presets = o.presets ? row(o.presets.map(function (p) { return btn(p[0], function () { yF.input.value = p[1]; if (p[2] !== undefined) x0F.input.value = p[2]; if (p[3] !== undefined) hF.input.value = p[3]; if (p[4] !== undefined) eF.input.value = p[4]; draw(); }, 'chip'); }), 'wg-chips') : null;
    var out = h('div', { class: 'wg-scroll wg-dt', style: o.height ? 'max-height:' + o.height : 'max-height:none' }), info = h('div', { class: 'wg-note' });
    host.appendChild(row([x0F.el, hF.el, yF.el])); host.appendChild(row([o.fixed ? null : mSel.el, o.noerr ? null : eF.el, o.noerr ? null : kF.el].filter(Boolean))); if (presets) host.appendChild(presets);
    host.appendChild(out); host.appendChild(info);
    [x0F.input, hF.input, yF.input, eF.input, kF.input].forEach(function (i) { i.addEventListener('input', draw); });
    function draw() {
      var y; try { y = parseList(yF.input.value); } catch (e) { out.innerHTML = ''; out.appendChild(errBox(e.message)); info.textContent = ''; return; }
      var x0 = num(x0F.input, 0), hh = num(hF.input, 1), eps = num(eF.input, 0), k = Math.round(num(kF.input, 0)), n = y.length;
      var y2 = y.slice(); if (eps && k >= 0 && k < n) y2[k] += eps;
      var T = diffTable(y2), T0 = diffTable(y), sym = mode === 'backward' ? '∇' : 'Δ';
      var head = '<tr><th>x</th><th>y</th>' + T.slice(1).map(function (_, j) { return '<th>' + sym + (j ? '<sup>' + (j + 1) + '</sup>' : '') + 'y</th>'; }).join('') + '</tr>';
      var body = '';
      for (var r = 0; r < 2 * n - 1; r++) {
        body += '<tr>';
        body += r % 2 === 0 ? '<td class="xv">' + fmtD(x0 + (r / 2) * hh) + '</td>' : '<td></td>';
        for (var c = 0; c < T.length; c++) {
          var i = (r - c) / 2, cls = [];
          if (i === Math.floor(i) && i >= 0 && i < T[c].length) {
            if (mode === 'forward' && i === 0) cls.push('dg');
            if (mode === 'backward' && i === T[c].length - 1) cls.push('dg');
            if (eps && Math.abs(T[c][i] - T0[c][i]) > 1e-12) cls.push('err');
            body += '<td class="' + cls.join(' ') + '">' + fmtD(T[c][i]) + '</td>';
          } else body += '<td></td>';
        }
        body += '</tr>';
      }
      out.innerHTML = '<table class="wg-t wg-dtab"><thead>' + head + '</thead><tbody>' + body + '</tbody></table>';
      var deg = -1;
      for (var c2 = 1; c2 < T.length; c2++) { var col = T[c2]; if (col.length >= 2 && col.every(function (v) { return Math.abs(v - col[0]) < 1e-9 * (1 + Math.abs(col[0])); })) { deg = c2; break; } }
      var msg = '';
      if (deg >= 0) msg = 'The ' + (deg === 1 ? 'first' : deg === 2 ? 'second' : deg === 3 ? 'third' : deg + 'th') + ' differences are constant (' + fmtD(T[deg][0]) + '), so the data fit a polynomial of degree ' + deg + '.' + (hh ? ' Leading coefficient = ' + fmtD(T[deg][0]) + ' / (' + deg + '! · h<sup>' + deg + '</sup>) = <b>' + fmtD(T[deg][0] / (fact(deg) * Math.pow(hh, deg))) + '</b>.' : '');
      else msg = 'No column of differences is constant: the data are not exactly a low-degree polynomial (or contain an error).';
      if (eps) msg += ' <span class="bad">Red cells changed because of the error ε = ' + fmtD(eps) + ' in y<sub>' + k + '</sub>:</span> in the column of order m it spreads as ε × (binomial coefficients with alternating signs), e.g. ε, −3ε, 3ε, −ε in the third differences.';
      info.innerHTML = msg;
    }
    function fact(m) { var f = 1; for (var i = 2; i <= m; i++) f *= i; return f; }
    draw();
  };

  /* ============================================================= L16–18: interpolation explorer */
  W.interp = function (host, o) {
    card(host, 'wg-interp');
    var methods = o.methods || ['forward', 'backward', 'lagrange', 'divided', 'spline', 'linear'];
    var names = { forward: 'Newton forward', backward: 'Newton backward', lagrange: 'Lagrange', divided: 'Newton divided differences', spline: 'natural cubic spline', linear: 'linear (connect the dots)' };
    var meth = o.method || methods[0];
    var xF = field('x data', o.x || '1891 1901 1911 1921 1931', { size: '15em' }), yF = field('y data', o.y || '46 66 81 93 101', { size: '15em' });
    var atF = field('estimate at x =', o.at !== undefined ? o.at : 1895, { size: '5em' }), fF = field('true f(x) (optional)', o.f || '', { size: '9em' });
    var mSel = select('Method', methods.map(function (m) { return [m, names[m]]; }), meth, function (v) { meth = v; draw(); });
    var presets = o.presets ? row(o.presets.map(function (p) { return btn(p[0], function () { xF.input.value = p[1]; yF.input.value = p[2]; if (p[3] !== undefined) atF.input.value = p[3]; if (p[4]) { meth = p[4]; mSel.input.value = meth; } fF.input.value = p[5] || ''; draw(); }, 'chip'); }), 'wg-chips') : null;
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '280px') }), P = new Plot(pl);
    var tbl = h('div', { class: 'wg-scroll', style: o.tableHeight ? 'max-height:' + o.tableHeight : '' }), info = h('div', { class: 'wg-note' });
    host.appendChild(row([xF.el, yF.el])); host.appendChild(row([atF.el, methods.length > 1 && !o.fixed ? mSel.el : null, o.nof ? null : fF.el].filter(Boolean))); if (presets) host.appendChild(presets);
    host.appendChild(h('div', { class: o.side ? 'wg-side' : '' }, [pl, tbl])); host.appendChild(info);
    [xF.input, yF.input, atF.input, fF.input].forEach(function (i) { i.addEventListener('input', draw); });
    P.onresize = draw;
    function draw() {
      var xs, ys; try { xs = parseList(xF.input.value); ys = parseList(yF.input.value); if (xs.length !== ys.length) throw new Error('x data and y data need the same number of values (' + xs.length + ' and ' + ys.length + ')'); if (xs.length < 2) throw new Error('Give at least two points'); } catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox(e.message)); info.textContent = ''; return; }
      var n = xs.length, X = num(atF.input, xs[0]), ftrue = null;
      if (fF.input.value.trim()) { try { ftrue = G.Expr.make(fF.input.value); } catch (e) { ftrue = null; } }
      for (var i = 1; i < n; i++) if (xs[i] === xs[i - 1]) { tbl.innerHTML = ''; tbl.appendChild(errBox('Two data points have the same x')); return; }
      var hh = xs[1] - xs[0], equal = xs.every(function (v, i) { return Math.abs(v - (xs[0] + i * hh)) < 1e-9 * (1 + Math.abs(v)); });
      var fn, rows = [], head = [], est, note = '';
      if ((meth === 'forward' || meth === 'backward') && !equal) { tbl.innerHTML = ''; tbl.appendChild(errBox('Newton\'s forward and backward formulas need equally spaced x. Use Lagrange or divided differences for these data.')); info.textContent = ''; return; }
      if (meth === 'forward' || meth === 'backward') {
        var T = diffTable(ys), fwd = meth === 'forward', base = fwd ? xs[0] : xs[n - 1];
        fn = function (x) { var p = (x - base) / hh, s = 0, c = 1; for (var k = 0; k < n; k++) { s += c * (fwd ? T[k][0] : T[k][T[k].length - 1]); c *= (fwd ? (p - k) : (p + k)) / (k + 1); } return s; };
        var p = (X - base) / hh, c = 1, sum = 0, sym = fwd ? 'Δ' : '∇';
        head = ['k', 'coefficient', sym + '<sup>k</sup>y' + (fwd ? '₀' : 'ₙ'), 'term', 'sum'];
        for (var k = 0; k < n; k++) { var d = fwd ? T[k][0] : T[k][T[k].length - 1]; sum += c * d; rows.push([k, fmtD(c), fmtD(d), fmtD(c * d), fmtD(sum)]); c *= (fwd ? (p - k) : (p + k)) / (k + 1); }
        est = sum; note = 'p = (x − ' + (fwd ? 'x₀' : 'xₙ') + ')/h = (' + fmtD(X) + ' − ' + fmtD(base) + ')/' + fmtD(hh) + ' = <b>' + fmtD(p) + '</b>. ';
        if (fwd && p > (n - 1) / 2) note += 'x is nearer the end of the table: the backward formula would use the nearby differences. ';
        if (!fwd && p < -(n - 1) / 2) note += 'x is nearer the start of the table: the forward formula would suit better. ';
      } else if (meth === 'lagrange') {
        fn = function (x) { return lagrangeEval(xs, ys, x); };
        head = ['i', 'xᵢ', 'yᵢ', 'Lᵢ(x)', 'yᵢ·Lᵢ(x)']; est = 0;
        for (var i2 = 0; i2 < n; i2++) { var L = 1; for (var j = 0; j < n; j++) if (j !== i2) L *= (X - xs[j]) / (xs[i2] - xs[j]); est += ys[i2] * L; rows.push([i2, fmtD(xs[i2]), fmtD(ys[i2]), fmtD(L), fmtD(ys[i2] * L)]); }
        rows.push(['', '', '', 'sum', '<b>' + fmtD(est) + '</b>']);
      } else if (meth === 'divided') {
        var dd = [ys.slice()];
        for (var k2 = 1; k2 < n; k2++) { var prev = dd[k2 - 1], col = []; for (var i3 = 0; i3 < n - k2; i3++) col.push((prev[i3 + 1] - prev[i3]) / (xs[i3 + k2] - xs[i3])); dd.push(col); }
        fn = function (x) { var s = dd[n - 1][0]; for (var k = n - 2; k >= 0; k--) s = dd[k][0] + (x - xs[k]) * s; return s; };
        head = ['k', 'f[x₀…xₖ]', 'product', 'term', 'sum'];
        var prod = 1, s2 = 0;
        for (var k3 = 0; k3 < n; k3++) { s2 += dd[k3][0] * prod; rows.push([k3, fmtD(dd[k3][0]), fmtD(prod), fmtD(dd[k3][0] * prod), fmtD(s2)]); prod *= (X - xs[k3]); }
        est = s2;
      } else if (meth === 'spline') {
        var S; try { S = naturalSpline(xs, ys); } catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox(e.message)); return; }
        fn = S; est = S(X); head = ['i', 'xᵢ', 'yᵢ', 'Mᵢ = S″(xᵢ)'];
        for (var i4 = 0; i4 < n; i4++) rows.push([i4, fmtD(xs[i4]), fmtD(ys[i4]), fmtD(S.M[i4])]);
        var seg = 0; while (seg < n - 2 && X > xs[seg + 1]) seg++;
        note = 'Natural spline: M₀ = Mₙ = 0; the inner Mᵢ solve a tridiagonal system (Thomas algorithm). x = ' + fmtD(X) + ' lies in [' + fmtD(xs[seg]) + ', ' + fmtD(xs[seg + 1]) + '], where S is one cubic. ';
      } else {
        fn = function (x) { var i = 0; while (i < n - 2 && x > xs[i + 1]) i++; return ys[i] + (ys[i + 1] - ys[i]) * (x - xs[i]) / (xs[i + 1] - xs[i]); };
        est = fn(X); head = ['i', 'xᵢ', 'yᵢ']; for (var i5 = 0; i5 < n; i5++) rows.push([i5, fmtD(xs[i5]), fmtD(ys[i5])]);
      }
      // plot
      var lo = Math.min(xs[0], X), hi = Math.max(xs[n - 1], X), pad = (hi - lo) * 0.08 || 1;
      lo -= pad; hi += pad;
      var vals = []; for (var q = 0; q <= 160; q++) { var xx = lo + (hi - lo) * q / 160, v = fn(xx); if (isFinite(v)) vals.push(v); }
      ys.forEach(function (v) { vals.push(v); }); vals.push(est);
      vals.sort(function (a, b) { return a - b; });
      var ylo = vals[0], yhi = vals[vals.length - 1], span = yhi - ylo || 1; ylo -= span * 0.1; yhi += span * 0.12;
      P.begin(); P.range(lo, hi, ylo, yhi); P.axes('x', 'y');
      if (ftrue) P.fn(function (x) { return ftrue(x); }, P.col.mut, 2, [5, 5]);
      P.vband(xs[0], xs[n - 1], 'rgba(47,109,181,0.06)');
      P.fn(fn, P.col.c1, 2.8);
      ys.forEach(function (v, i) { P.dot(xs[i], v, 6, P.col.ink); });
      P.seg(X, ylo, X, est, P.col.c2, 1.5, [4, 4]); P.dot(X, est, 7, P.col.c5);
      var leg = [[names[meth], P.col.c1]]; if (ftrue) leg.push(['true f(x)', P.col.mut, [5, 5]]); P.legend(leg);
      tbl.innerHTML = ''; tbl.appendChild(table(head, rows, { hi: meth === 'lagrange' ? rows.length - 1 : rows.length - 1 }));
      var msg = note + 'Estimate at x = ' + fmtD(X) + ': <b>' + fmtD(est) + '</b>.';
      if (ftrue) { var tv = ftrue(X); msg += ' True value ' + fmtD(tv) + ', error ' + sci(Math.abs(est - tv), 2) + '.'; }
      if (X < xs[0] || X > xs[n - 1]) msg += ' <span class="bad">This is extrapolation (outside the data): treat it with suspicion.</span>';
      info.innerHTML = msg;
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L18: Runge phenomenon and splines */
  W.runge = function (host, o) {
    card(host, 'wg-runge');
    var FN = { runge: ['1/(1+25x²)', function (x) { return 1 / (1 + 25 * x * x); }], abs: ['|x|', function (x) { return Math.abs(x); }], sin: ['sin(πx)', function (x) { return Math.sin(Math.PI * x); }], step: ['step at 0', function (x) { return x < 0 ? 0 : 1; }] };
    var fk = o.f || 'runge', nS = slider('points n', 3, 25, 1, o.n || 11, draw);
    var fSel = select('Function', Object.keys(FN).map(function (k) { return [k, FN[k][0]]; }), fk, function (v) { fk = v; draw(); });
    var M = { equi: ['polynomial, equal spacing', 'c5', o.equi !== false], cheb: ['polynomial, Chebyshev points', 'c4', !!o.cheb], lin: ['linear spline', 'c3', !!o.lin], cub: ['natural cubic spline', 'c1', o.cub !== false] };
    var checks = Object.keys(M).map(function (k) { var c = h('input', { type: 'checkbox' }); c.checked = M[k][2]; c.addEventListener('change', function () { M[k][2] = c.checked; draw(); }); return h('label', { class: 'wg-f' }, [c, h('span', { html: M[k][0] })]); });
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '300px') }), P = new Plot(pl), tbl = h('div');
    host.appendChild(row([fSel.el, nS.el])); host.appendChild(row(checks)); host.appendChild(pl); host.appendChild(tbl);
    P.onresize = draw;
    function draw() {
      var f = FN[fk][1], n = nS.value, leg = [], rows = [];
      var xe = [], xc = []; for (var i = 0; i < n; i++) { xe.push(-1 + 2 * i / (n - 1)); xc.push(Math.cos((2 * i + 1) * Math.PI / (2 * n))); }
      xc.reverse();
      var ye = xe.map(f), yc = xc.map(f), we = baryWeights(xe), wc = baryWeights(xc), S = naturalSpline(xe, ye);
      var fns = { equi: function (x) { return baryEval(xe, ye, we, x); }, cheb: function (x) { return baryEval(xc, yc, wc, x); }, lin: function (x) { var i = 0; while (i < n - 2 && x > xe[i + 1]) i++; return ye[i] + (ye[i + 1] - ye[i]) * (x - xe[i]) / (xe[i + 1] - xe[i]); }, cub: S };
      var yl = fk === 'sin' ? [-1.6, 1.6] : [-0.6, 1.6];
      P.begin(); P.range(-1.05, 1.05, yl[0], yl[1]); P.axes('x', '');
      P.fn(f, P.col.mut, 2.4, [6, 5]); leg.push(['f(x) = ' + FN[fk][0], P.col.mut, [6, 5]]);
      Object.keys(M).forEach(function (k) {
        if (!M[k][2]) return; var g = fns[k], col = P.col[M[k][1]]; P.fn(g, col, 2.6); leg.push([M[k][0], col]);
        var err = 0; for (var q = 0; q <= 4000; q++) { var x = -1 + 2 * q / 4000; err = Math.max(err, Math.abs(g(x) - f(x))); }
        rows.push([M[k][0], fmt(err, 4), err > 0.5 ? '<b style="color:var(--w-c5)">poor</b>' : err > 0.05 ? 'fair' : '<b style="color:var(--w-c3)">good</b>']);
      });
      xe.forEach(function (x, i) { P.dot(x, ye[i], 4.5, P.col.ink); });
      if (M.cheb[2]) xc.forEach(function (x, i) { P.dot(x, yc[i], 4, P.col.c4, true); });
      P.legend(leg);
      tbl.innerHTML = ''; tbl.appendChild(table(['method (n = ' + n + ' points)', 'largest error on [−1, 1]', ''], rows));
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L19: numerical differentiation */
  W.numdiff = function (host, o) {
    card(host, 'wg-numdiff');
    var fF = field('f(x) =', o.f || 'sin(x)', { size: '10em' }), xF = field('x₀ =', o.x0 !== undefined ? o.x0 : 1, { size: '4em' });
    var hS = slider('step h', -12, 0, 0.25, o.logh !== undefined ? o.logh : -1, draw, function (v) { return sci(Math.pow(10, v), 1); });
    var presets = o.presets ? row(o.presets.map(function (p) { return btn(p[0], function () { fF.input.value = p[1]; xF.input.value = p[2]; draw(); }, 'chip'); }), 'wg-chips') : null;
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '260px') }), P = new Plot(pl), tbl = h('div'), info = h('div', { class: 'wg-note' });
    host.appendChild(row([fF.el, xF.el, hS.el])); if (presets) host.appendChild(presets);
    host.appendChild(pl); host.appendChild(tbl); host.appendChild(info);
    [fF.input, xF.input].forEach(function (i) { i.addEventListener('input', draw); });
    P.onresize = draw;
    function draw() {
      var f, df, d2;
      try { f = G.Expr.make(fF.input.value); df = f.deriv(); d2 = function (x) { return (df(x + 1e-5) - df(x - 1e-5)) / 2e-5; }; } catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox(e.message)); return; }
      var x0 = num(xF.input, 1), hh = Math.pow(10, hS.value), ex = df(x0), ex2 = d2(x0);
      var fw = (f(x0 + hh) - f(x0)) / hh, bw = (f(x0) - f(x0 - hh)) / hh, ce = (f(x0 + hh) - f(x0 - hh)) / (2 * hh);
      var ce2 = (f(x0 + 2 * hh) - f(x0 - 2 * hh)) / (4 * hh), ri = ce + (ce - ce2) / 3, sd = (f(x0 + hh) - 2 * f(x0) + f(x0 - hh)) / (hh * hh);
      var w = Math.max(hh * 2.5, 0.6), lo = x0 - w, hi = x0 + w;
      var vals = []; for (var q = 0; q <= 100; q++) { var v = f(lo + (hi - lo) * q / 100); if (isFinite(v)) vals.push(v); }
      var ylo = Math.min.apply(null, vals), yhi = Math.max.apply(null, vals), sp = (yhi - ylo) || 1; ylo -= sp * 0.25; yhi += sp * 0.25;
      P.begin(); P.range(lo, hi, ylo, yhi); P.axes('x', '');
      P.fn(f, P.col.ink, 2.8);
      var y0 = f(x0);
      P.fn(function (x) { return y0 + ex * (x - x0); }, P.col.c3, 2, [3, 3]);
      P.fn(function (x) { return y0 + fw * (x - x0); }, P.col.c2, 2);
      P.fn(function (x) { return f(x0 - hh) + ce * (x - x0 + hh); }, P.col.c1, 2);
      P.dot(x0, y0, 6, P.col.c5); P.dot(x0 + hh, f(x0 + hh), 5, P.col.c2); P.dot(x0 - hh, f(x0 - hh), 5, P.col.c1);
      P.legend([['f(x)', P.col.ink], ['true tangent', P.col.c3, [3, 3]], ['forward secant', P.col.c2], ['central secant', P.col.c1]]);
      var rows = [['forward (f(x+h) − f(x))/h', fmt(fw, 10), sci(Math.abs(fw - ex), 2), 'O(h)'], ['backward (f(x) − f(x−h))/h', fmt(bw, 10), sci(Math.abs(bw - ex), 2), 'O(h)'],
        ['central (f(x+h) − f(x−h))/2h', fmt(ce, 10), sci(Math.abs(ce - ex), 2), 'O(h²)'], ['Richardson from h and 2h', fmt(ri, 10), sci(Math.abs(ri - ex), 2), 'O(h⁴)'],
        ['second derivative (central)', fmt(sd, 8), sci(Math.abs(sd - ex2), 2), 'O(h²)']];
      tbl.innerHTML = ''; tbl.appendChild(table(['formula (h = ' + sci(hh, 1) + ')', 'estimate', 'error', 'order'], rows));
      info.innerHTML = 'Exact f′(' + fmt(x0, 4) + ') = ' + fmt(ex, 10) + ', f″ = ' + fmt(ex2, 8) + '. ' + (hh < 1e-6 ? '<span class="bad">For very small h round-off takes over: f(x+h) − f(x) cancels (Lecture 4), and the second derivative is worst.</span>' : 'Move h down: errors shrink like h (forward) and h² (central), until round-off takes over below about 10⁻⁵.');
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L20: numerical integration */
  var GAUSS = { 2: [[-0.5773502691896258, 1], [0.5773502691896258, 1]], 3: [[-0.7745966692414834, 5 / 9], [0, 8 / 9], [0.7745966692414834, 5 / 9]] };
  function quadRule(f, a, b, n, m) {
    var hh = (b - a) / n, s = 0, i;
    if (m === 'trap') { for (i = 1; i < n; i++) s += f(a + i * hh); return hh * (0.5 * f(a) + s + 0.5 * f(b)); }
    if (m === 'simp') { if (n % 2) return NaN; for (i = 1; i < n; i++) s += (i % 2 ? 4 : 2) * f(a + i * hh); return hh / 3 * (f(a) + s + f(b)); }
    if (m === 's38') { if (n % 3) return NaN; for (i = 1; i < n; i++) s += (i % 3 ? 3 : 2) * f(a + i * hh); return 3 * hh / 8 * (f(a) + s + f(b)); }
    if (m === 'mid') { for (i = 0; i < n; i++) s += f(a + (i + 0.5) * hh); return hh * s; }
    if (m === 'g2' || m === 'g3') { var nodes = GAUSS[m === 'g2' ? 2 : 3]; for (i = 0; i < n; i++) { var c = a + (i + 0.5) * hh; nodes.forEach(function (nw) { s += nw[1] * f(c + nw[0] * hh / 2); }); } return s * hh / 2; }
    return NaN;
  }
  W.quad = function (host, o) {
    card(host, 'wg-quad');
    var names = { trap: 'trapezoidal', simp: 'Simpson 1/3', s38: 'Simpson 3/8', mid: 'midpoint', g2: 'Gauss 2-point', g3: 'Gauss 3-point' };
    var meths = o.methods || ['trap', 'simp', 's38', 'g2'];
    var meth = o.method || meths[0];
    var fF = field('f(x) =', o.f || 'e^(-x^2)', { size: '10em' }), aF = field('a =', o.a !== undefined ? o.a : 0, { size: '3.5em' }), bF = field('b =', o.b !== undefined ? o.b : 1, { size: '3.5em' });
    var exF = field('exact (optional)', o.exact || '', { size: '7em' });
    var nS = slider('panels n', 1, 24, 1, o.n || 4, draw);
    var mSel = select('Rule', meths.map(function (m) { return [m, names[m]]; }), meth, function (v) { meth = v; draw(); });
    var presets = o.presets ? row(o.presets.map(function (p) { return btn(p[0], function () { fF.input.value = p[1]; aF.input.value = p[2]; bF.input.value = p[3]; exF.input.value = p[4] || ''; if (p[5]) { nS.input.value = p[5]; nS.update(); } if (p[6]) { meth = p[6]; mSel.input.value = meth; } draw(); }, 'chip'); }), 'wg-chips') : null;
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '260px') }), P = new Plot(pl), tbl = h('div'), info = h('div', { class: 'wg-note' });
    if (!o.compact) host.appendChild(row([fF.el, aF.el, bF.el, o.noexact ? null : exF.el].filter(Boolean))); host.appendChild(row([o.fixed || o.compact ? null : mSel.el, nS.el].filter(Boolean))); if (presets) host.appendChild(presets);
    host.appendChild(pl); host.appendChild(tbl); host.appendChild(info);
    [fF.input, aF.input, bF.input, exF.input].forEach(function (i) { i.addEventListener('input', draw); });
    P.onresize = draw;
    function draw() {
      var f; try { f = G.Expr.make(fF.input.value); } catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox(e.message)); return; }
      var a = num(aF.input, 0), b = num(bF.input, 1), n = nS.value, ex = NaN;
      if (exF.input.value.trim()) { try { ex = G.Expr.make(exF.input.value)(0); } catch (e) { ex = NaN; } }
      if (!isFinite(ex)) { ex = quadRule(f, a, b, 4096, 'simp'); var exNote = '(reference value from Simpson with 4096 panels)'; }
      var span = b - a, lo = a - span * 0.06, hi = b + span * 0.06;
      var vals = []; for (var q = 0; q <= 200; q++) { var v = f(lo + (hi - lo) * q / 200); if (isFinite(v)) vals.push(v); }
      var ylo = Math.min(0, Math.min.apply(null, vals)), yhi = Math.max(0, Math.max.apply(null, vals)), sp = (yhi - ylo) || 1; yhi += sp * 0.12; if (ylo < 0) ylo -= sp * 0.08;
      P.begin(); P.range(lo, hi, ylo, yhi); P.axes('x', '');
      var hh = span / n, shade = 'rgba(184,87,18,0.18)', edge = P.col.c2;
      if (meth === 'trap') for (var i = 0; i < n; i++) { var x1 = a + i * hh, x2 = x1 + hh; P.poly([[x1, 0], [x1, f(x1)], [x2, f(x2)], [x2, 0]], edge, 1.6, null, true, shade); }
      else if (meth === 'mid') for (var i2 = 0; i2 < n; i2++) { var m1 = a + i2 * hh, fm = f(m1 + hh / 2); P.poly([[m1, 0], [m1, fm], [m1 + hh, fm], [m1 + hh, 0]], edge, 1.6, null, true, shade); }
      else if ((meth === 'simp' && n % 2 === 0) || (meth === 's38' && n % 3 === 0)) {
        var k = meth === 'simp' ? 2 : 3;
        for (var j = 0; j < n; j += k) {
          var xs = [], ys = []; for (var t = 0; t <= k; t++) { xs.push(a + (j + t) * hh); ys.push(f(a + (j + t) * hh)); }
          var pts = [[xs[0], 0]]; for (var s2 = 0; s2 <= 30; s2++) { var xx = xs[0] + (xs[k] - xs[0]) * s2 / 30; pts.push([xx, lagrangeEval(xs, ys, xx)]); } pts.push([xs[k], 0]);
          P.poly(pts, edge, 1.6, null, true, shade);
        }
      } else if (meth === 'g2' || meth === 'g3') {
        for (var i3 = 0; i3 < n; i3++) { var c = a + (i3 + 0.5) * hh; GAUSS[meth === 'g2' ? 2 : 3].forEach(function (nw) { var xg = c + nw[0] * hh / 2; P.seg(xg, 0, xg, f(xg), edge, 2); P.dot(xg, f(xg), 4.5, edge); }); P.seg(a + i3 * hh, ylo, a + i3 * hh, yhi, P.col.grid, 1); }
      }
      P.fn(f, P.col.c1, 2.8);
      if (meth !== 'g2' && meth !== 'g3') for (var i4 = 0; i4 <= n; i4++) P.dot(a + i4 * hh, f(a + i4 * hh), 3.5, P.col.ink);
      var cur = quadRule(f, a, b, n, meth);
      var rows = meths.map(function (m) { var v = quadRule(f, a, b, n, m); return [names[m] + (m === meth ? ' ◀' : ''), isFinite(v) ? fmt(v, 8) : '<span class="bad">needs n divisible by ' + (m === 'simp' ? 2 : 3) + '</span>', isFinite(v) ? sci(Math.abs(v - ex), 2) : '', m === 'g2' || m === 'g3' ? (m === 'g2' ? 2 : 3) * n : n + 1]; });
      tbl.innerHTML = ''; tbl.appendChild(table(['rule (n = ' + n + ')', 'value', 'error', 'f-evaluations'], rows));
      info.innerHTML = 'Reference value ' + fmt(ex, 10) + ' ' + (exNote || '') + '. ' + (isFinite(cur) ? 'Doubling n divides the error by about 4 (trapezoidal) or 16 (Simpson).' : '<span class="bad">' + names[meth] + ' needs n to be a multiple of ' + (meth === 'simp' ? 2 : 3) + '.</span>');
      exNote = '';
    }
    var exNote = '';
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L21–22: ODE solver for y' = f(x, y) */
  W.ode = function (host, o) {
    card(host, 'wg-ode');
    var M = { euler: ['Euler', 'c5'], heun: ['Heun (modified Euler)', 'c2'], mid: ['midpoint RK2', 'c4'], rk4: ['RK4', 'c3'] };
    var on = {}; (o.methods || ['euler', 'heun', 'rk4']).forEach(function (m) { on[m] = true; });
    var fF = field("y′ = f(x, y) =", o.f || 'x + y', { size: '10em' }), x0F = field('x₀ =', o.x0 !== undefined ? o.x0 : 0, { size: '3em' }), y0F = field('y₀ =', o.y0 !== undefined ? o.y0 : 1, { size: '3em' });
    var hF = field('h =', o.h || 0.1, { size: '3.5em' }), xeF = field('to x =', o.xend !== undefined ? o.xend : 1, { size: '3em' }), exF = field('exact y(x) (optional)', o.exact || '', { size: '9em' });
    var main = o.main || Object.keys(on)[0];
    var checks = Object.keys(M).filter(function (k) { return !o.only || o.only.indexOf(k) >= 0; }).map(function (k) { var c = h('input', { type: 'checkbox' }); c.checked = !!on[k]; c.addEventListener('change', function () { on[k] = c.checked; if (c.checked) main = k; draw(); }); return h('label', { class: 'wg-f' }, [c, h('span', { html: M[k][0] })]); });
    var presets = o.presets ? row(o.presets.map(function (p) { return btn(p[0], function () { fF.input.value = p[1]; x0F.input.value = p[2]; y0F.input.value = p[3]; hF.input.value = p[4]; xeF.input.value = p[5]; exF.input.value = p[6] || ''; draw(); }, 'chip'); }), 'wg-chips') : null;
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '280px') }), P = new Plot(pl);
    var tbl = h('div', { class: 'wg-scroll', style: o.tableHeight ? 'max-height:' + o.tableHeight : '' }), info = h('div', { class: 'wg-note' });
    if (!o.compact) host.appendChild(row([fF.el, x0F.el, y0F.el])); if (!o.compact) host.appendChild(row([hF.el, btn('h ÷ 2', function () { hF.input.value = +(num(hF.input, 0.1) / 2).toPrecision(6); draw(); }, 'chip'), btn('h × 2', function () { hF.input.value = +(num(hF.input, 0.1) * 2).toPrecision(6); draw(); }, 'chip'), xeF.el, o.noexact ? null : exF.el].filter(Boolean)));
    if (!o.compact) host.appendChild(row(checks)); if (presets) host.appendChild(presets);
    host.appendChild(h('div', { class: o.side ? 'wg-side' : '' }, [pl, tbl])); host.appendChild(info);
    [fF.input, x0F.input, y0F.input, hF.input, xeF.input, exF.input].forEach(function (i) { i.addEventListener('input', draw); });
    P.onresize = draw;
    function step(m, f, x, y, hh) {
      if (m === 'euler') return y + hh * f(x, y);
      if (m === 'heun') { var k1 = f(x, y), k2 = f(x + hh, y + hh * k1); return y + hh / 2 * (k1 + k2); }
      if (m === 'mid') { var m1 = f(x, y); return y + hh * f(x + hh / 2, y + hh / 2 * m1); }
      var a = f(x, y), b = f(x + hh / 2, y + hh / 2 * a), c = f(x + hh / 2, y + hh / 2 * b), d = f(x + hh, y + hh * c); return y + hh / 6 * (a + 2 * b + 2 * c + d);
    }
    function draw() {
      var f, ex = null;
      try { f = G.Expr.make2(fF.input.value); } catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox(e.message)); return; }
      if (exF.input.value.trim()) { try { ex = G.Expr.make(exF.input.value); } catch (e) { ex = null; } }
      var x0 = num(x0F.input, 0), y0 = num(y0F.input, 1), hh = num(hF.input, 0.1), xe = num(xeF.input, 1);
      if (!(hh > 0) || !(xe > x0)) { tbl.innerHTML = ''; tbl.appendChild(errBox('Need h > 0 and an end point beyond x₀')); return; }
      var N = Math.round((xe - x0) / hh); if (N > 5000) { tbl.innerHTML = ''; tbl.appendChild(errBox('Too many steps (more than 5000): increase h')); return; }
      var runs = {}, allY = [];
      Object.keys(M).forEach(function (m) { if (!on[m]) return; var pts = [[x0, y0]], x = x0, y = y0; for (var i = 0; i < N; i++) { y = step(m, f, x, y, hh); x = x0 + (i + 1) * hh; pts.push([x, y]); if (!isFinite(y) || Math.abs(y) > 1e9) break; } runs[m] = pts; pts.forEach(function (p) { if (isFinite(p[1]) && Math.abs(p[1]) < 1e8) allY.push(p[1]); }); });
      if (ex) for (var q = 0; q <= 100; q++) { var v = ex(x0 + (xe - x0) * q / 100); if (isFinite(v)) allY.push(v); }
      var ylo = Math.min.apply(null, allY), yhi = Math.max.apply(null, allY), sp = (yhi - ylo) || 1; ylo -= sp * 0.1; yhi += sp * 0.15;
      if (o.ylim) { ylo = o.ylim[0]; yhi = o.ylim[1]; }
      P.begin(); P.range(x0, xe, ylo, yhi); P.axes('x', 'y');
      if (o.field !== false) { var c = P.ctx; c.save(); c.strokeStyle = P.col.grid; c.lineWidth = 1.4; for (var gi = 0; gi <= 14; gi++) for (var gj = 0; gj <= 9; gj++) { var gx = x0 + (xe - x0) * (gi + 0.5) / 15, gy = ylo + (yhi - ylo) * (gj + 0.5) / 10, sl = f(gx, gy); if (!isFinite(sl)) continue; var X = P.X(gx), Y = P.Y(gy), dd = (xe - x0) * 0.01, dxp = P.X(gx + dd) - X, dyp = P.Y(gy + sl * dd) - Y, L = Math.hypot(dxp, dyp), r = 9 / L; if (!isFinite(r)) continue; c.beginPath(); c.moveTo(X - dxp * r, Y - dyp * r); c.lineTo(X + dxp * r, Y + dyp * r); c.stroke(); } c.restore(); }
      var leg = [];
      if (ex) { P.fn(function (x) { return ex(x); }, P.col.ink, 2.4, [6, 4]); leg.push(['exact', P.col.ink, [6, 4]]); }
      Object.keys(runs).forEach(function (m) { var col = P.col[M[m][1]]; P.poly(runs[m], col, 2.4); runs[m].forEach(function (p) { P.dot(p[0], p[1], 3.2, col); }); leg.push([M[m][0], col]); });
      P.legend(leg);
      var mm = runs[main] ? main : Object.keys(runs)[0], rows = [];
      if (mm) {
        var pts = runs[mm], every = Math.max(1, Math.ceil(pts.length / (o.maxRows || 12)));
        pts.forEach(function (p, i) { if (i % every && i !== pts.length - 1) return; var r = [i, fmt(p[0], 4), fmt(p[1], 6)]; if (ex) r.push(sci(Math.abs(p[1] - ex(p[0])), 2)); rows.push(r); });
      }
      tbl.innerHTML = ''; if (mm) tbl.appendChild(table(['n', 'xₙ', 'yₙ (' + M[mm][0] + ')'].concat(ex ? ['error'] : []), rows, { hi: rows.length - 1 }));
      var msg = [];
      Object.keys(runs).forEach(function (m) { var last = runs[m][runs[m].length - 1]; msg.push(M[m][0] + ': y(' + fmt(last[0], 3) + ') = <b>' + (isFinite(last[1]) && Math.abs(last[1]) < 1e9 ? fmt(last[1], 6) : 'blew up') + '</b>' + (ex && isFinite(last[1]) ? ' (error ' + sci(Math.abs(last[1] - ex(last[0])), 1) + ')' : '')); });
      info.innerHTML = msg.join(' · ') + '. Grey dashes: the slope field f(x, y).';
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L22: systems x' = f(x, y), y' = g(x, y) */
  W.odesys = function (host, o) {
    card(host, 'wg-odesys');
    var fF = field("x′ =", o.f || 'y', { size: '9em' }), gF = field("y′ =", o.g || '-x', { size: '9em' }), x0F = field('x₀ =', o.x0 !== undefined ? o.x0 : 1, { size: '3em' }), y0F = field('y₀ =', o.y0 !== undefined ? o.y0 : 0, { size: '3em' });
    var hF = field('h =', o.h || 0.1, { size: '3.5em' }), TF = field('to t =', o.T || 62.83, { size: '4em' }), invF = field('conserved quantity (optional)', o.inv !== undefined ? o.inv : 'x^2 + y^2', { size: '9em' });
    var meth = o.method || 'euler', M = { euler: 'Euler', heun: 'Heun', rk4: 'RK4' };
    var mSel = select('Method', Object.keys(M).map(function (k) { return [k, M[k]]; }), meth, function (v) { meth = v; draw(); });
    var presets = o.presets ? row(o.presets.map(function (p) { return btn(p[0], function () { fF.input.value = p[1]; gF.input.value = p[2]; x0F.input.value = p[3]; y0F.input.value = p[4]; hF.input.value = p[5]; TF.input.value = p[6]; invF.input.value = p[7] || ''; if (p[8]) { meth = p[8]; mSel.input.value = meth; } draw(); }, 'chip'); }), 'wg-chips') : null;
    var ph = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '260px') }), tp = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '260px') });
    var P1 = new Plot(ph), P2 = new Plot(tp), info = h('div', { class: 'wg-note' });
    host.appendChild(row([fF.el, gF.el, x0F.el, y0F.el])); host.appendChild(row([mSel.el, hF.el, TF.el, o.noinv ? null : invF.el].filter(Boolean))); if (presets) host.appendChild(presets);
    host.appendChild(h('div', { class: 'wg-two' }, [ph, tp])); host.appendChild(info);
    [fF.input, gF.input, x0F.input, y0F.input, hF.input, TF.input, invF.input].forEach(function (i) { i.addEventListener('input', draw); });
    P1.onresize = draw; P2.onresize = draw;
    function draw() {
      var F, Gf, I = null;
      try { F = G.Expr.make2(fF.input.value); Gf = G.Expr.make2(gF.input.value); } catch (e) { info.innerHTML = ''; info.appendChild(errBox(e.message)); return; }
      if (invF.input.value.trim()) { try { I = G.Expr.make2(invF.input.value); } catch (e) { I = null; } }
      var x = num(x0F.input, 1), y = num(y0F.input, 0), hh = num(hF.input, 0.1), T = num(TF.input, 10), N = Math.min(20000, Math.round(T / hh));
      var pts = [[0, x, y]];
      for (var i = 0; i < N; i++) {
        var nx, ny;
        if (meth === 'euler') { nx = x + hh * F(x, y); ny = y + hh * Gf(x, y); }
        else if (meth === 'heun') { var a1 = F(x, y), b1 = Gf(x, y), a2 = F(x + hh * a1, y + hh * b1), b2 = Gf(x + hh * a1, y + hh * b1); nx = x + hh / 2 * (a1 + a2); ny = y + hh / 2 * (b1 + b2); }
        else { var k1 = F(x, y), l1 = Gf(x, y), k2 = F(x + hh / 2 * k1, y + hh / 2 * l1), l2 = Gf(x + hh / 2 * k1, y + hh / 2 * l1), k3 = F(x + hh / 2 * k2, y + hh / 2 * l2), l3 = Gf(x + hh / 2 * k2, y + hh / 2 * l2), k4 = F(x + hh * k3, y + hh * l3), l4 = Gf(x + hh * k3, y + hh * l3); nx = x + hh / 6 * (k1 + 2 * k2 + 2 * k3 + k4); ny = y + hh / 6 * (l1 + 2 * l2 + 2 * l3 + l4); }
        x = nx; y = ny; pts.push([(i + 1) * hh, x, y]); if (!isFinite(x) || Math.abs(x) + Math.abs(y) > 1e6) break;
      }
      var xs = pts.map(function (p) { return p[1]; }), ys = pts.map(function (p) { return p[2]; });
      function rng(v) { var lo = Math.min.apply(null, v), hi = Math.max.apply(null, v), s = (hi - lo) || 1; return [lo - s * 0.08, hi + s * 0.08]; }
      var rx = rng(xs), ry = rng(ys), rr = [Math.min(rx[0], ry[0]), Math.max(rx[1], ry[1])];
      P1.begin(); P1.range(rx[0], rx[1], ry[0], ry[1]); P1.axes('x', 'y'); P1.poly(pts.map(function (p) { return [p[1], p[2]]; }), P1.col.c1, 2); P1.dot(pts[0][1], pts[0][2], 6, P1.col.c3); P1.dot(x, y, 6, P1.col.c5); P1.legend([['phase path (x, y)', P1.col.c1]]);
      P2.begin(); P2.range(0, pts[pts.length - 1][0] || 1, rr[0], rr[1]); P2.axes('t', ''); P2.poly(pts.map(function (p) { return [p[0], p[1]]; }), P2.col.c2, 2); P2.poly(pts.map(function (p) { return [p[0], p[2]]; }), P2.col.c4, 2); P2.legend([['x(t)', P2.col.c2], ['y(t)', P2.col.c4]]);
      var msg = M[meth] + ', h = ' + hh + ', ' + (pts.length - 1) + ' steps. End point (' + fmt(x, 5) + ', ' + fmt(y, 5) + ').';
      if (I) { var i0 = I(pts[0][1], pts[0][2]), i1 = I(x, y); msg += ' Conserved quantity: start ' + fmt(i0, 5) + ', end <b>' + fmt(i1, 5) + '</b>' + (Math.abs(i1 - i0) > 1e-3 * (1 + Math.abs(i0)) ? ' <span class="bad">(drifted by ' + fmt(i1 - i0, 4) + ')</span>' : ' (kept)') + '.'; }
      info.innerHTML = msg;
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= Module 7 helpers: least squares by QR (modified Gram–Schmidt) */
  function lstsq(A, y) {           // A: m×n (array of rows), returns coefficients
    var m = A.length, n = A[0].length, Q = [], R = [], j, k, i;
    for (j = 0; j < n; j++) { var v = A.map(function (r) { return r[j]; }); R.push(new Array(n).fill(0));
      for (k = 0; k < j; k++) { var d = 0; for (i = 0; i < m; i++) d += Q[k][i] * v[i]; R[k][j] = d; for (i = 0; i < m; i++) v[i] -= d * Q[k][i]; }
      var nr = Math.sqrt(v.reduce(function (s, t) { return s + t * t; }, 0)); R[j][j] = nr; Q.push(v.map(function (t) { return nr ? t / nr : 0; })); }
    var qy = Q.map(function (q) { return q.reduce(function (s, t, ii) { return s + t * y[ii]; }, 0); }), c = new Array(n).fill(0);
    for (j = n - 1; j >= 0; j--) { var s = qy[j]; for (k = j + 1; k < n; k++) s -= R[j][k] * c[k]; c[j] = R[j][j] ? s / R[j][j] : 0; }
    return c;
  }
  function fmtC(v) { var a = Math.abs(v); return (a !== 0 && (a < 1e-3 || a >= 1e5) ? sci(v, 3) : String(+v.toPrecision(6))).replace('-', '−'); }
  function fitModel(model, xs, ys, deg, period) {
    var n = xs.length, f, coef, eq, cols;
    if (model === 'line' || model === 'poly') {
      var d = model === 'line' ? 1 : deg, lo = Math.min.apply(null, xs), hi = Math.max.apply(null, xs), c0 = (lo + hi) / 2, s0 = (hi - lo) / 2 || 1;
      var A = xs.map(function (x) { var t = (x - c0) / s0, r = []; for (var k = 0; k <= d; k++) r.push(Math.pow(t, k)); return r; });
      var ct = lstsq(A, ys);
      // convert to coefficients in powers of x (for display; small degrees)
      var px = new Array(d + 1).fill(0);
      for (var k2 = 0; k2 <= d; k2++) { var bin = 1; for (var j2 = 0; j2 <= k2; j2++) { if (j2 > 0) bin = bin * (k2 - j2 + 1) / j2; px[j2] += ct[k2] * bin * Math.pow(-c0, k2 - j2) / Math.pow(s0, k2); } }
      f = function (x) { var t = (x - c0) / s0, s = 0; for (var k = d; k >= 0; k--) s = s * t + ct[k]; return s; };
      coef = px; eq = 'y = ' + px.map(function (c, k) { return (k ? (c < 0 ? ' − ' : ' + ') + fmtC(Math.abs(c)) : fmtC(c)) + (k ? 'x' + (k > 1 ? '<sup>' + k + '</sup>' : '') : ''); }).join('');
      if (d > 4) eq = 'polynomial of degree ' + d;
      return { f: f, eq: eq, coef: px, k: d + 1 };
    }
    if (model === 'exp' || model === 'power') {
      var ok = ys.every(function (v) { return v > 0; }) && (model === 'exp' || xs.every(function (v) { return v > 0; }));
      if (!ok) throw new Error(model === 'exp' ? 'y = a·e^(bx) needs all y > 0 (we take ln y)' : 'y = a·x^b needs all x > 0 and y > 0 (we take logs)');
      var X = model === 'exp' ? xs : xs.map(Math.log), Y = ys.map(Math.log);
      var c2 = lstsq(X.map(function (x) { return [1, x]; }), Y), a = Math.exp(c2[0]), b = c2[1];
      f = model === 'exp' ? function (x) { return a * Math.exp(b * x); } : function (x) { return a * Math.pow(x, b); };
      return { f: f, eq: model === 'exp' ? 'y = ' + fmtC(a) + ' e<sup>' + fmtC(b) + 'x</sup>  (from ln y = ' + fmtC(c2[0]) + ' + ' + fmtC(b) + 'x)' : 'y = ' + fmtC(a) + ' x<sup>' + fmtC(b) + '</sup>  (from ln y = ' + fmtC(c2[0]) + ' + ' + fmtC(b) + ' ln x)', coef: [a, b], k: 2, lin: true };
    }
    var w = 2 * Math.PI / (period || 24);
    var c3 = lstsq(xs.map(function (x) { return [1, Math.cos(w * x), Math.sin(w * x)]; }), ys);
    f = function (x) { return c3[0] + c3[1] * Math.cos(w * x) + c3[2] * Math.sin(w * x); };
    return { f: f, eq: 'y = ' + fmtC(c3[0]) + (c3[1] < 0 ? ' − ' : ' + ') + fmtC(Math.abs(c3[1])) + ' cos ωx' + (c3[2] < 0 ? ' − ' : ' + ') + fmtC(Math.abs(c3[2])) + ' sin ωx, ω = 2π/' + (period || 24), coef: c3, k: 3 };
  }

  /* ============================================================= L23–24: least-squares fitting */
  W.lsq = function (host, o) {
    card(host, 'wg-lsq');
    var names = { line: 'straight line', poly: 'polynomial', exp: 'exponential a·e^(bx)', power: 'power a·x^b', trig: 'trigonometric (one period)' };
    var models = o.models || ['line', 'poly', 'exp', 'power', 'trig'], model = o.model || models[0];
    var xF = field('x', o.x || '2 4 5 7 9 11', { size: '14em' }), yF = field('y', o.y || '14 21 24 30 37 42', { size: '14em' });
    var mSel = select('Model', models.map(function (m) { return [m, names[m]]; }), model, function (v) { model = v; dS.el.style.display = model === 'poly' ? '' : 'none'; pF.el.style.display = model === 'trig' ? '' : 'none'; draw(); });
    var dS = slider('degree', 1, 9, 1, o.deg || 2, draw); dS.el.style.display = model === 'poly' ? '' : 'none';
    var pF = field('period', o.period || 24, { size: '3.5em' }); pF.el.style.display = model === 'trig' ? '' : 'none';
    var atF = field('predict at x =', o.at !== undefined ? o.at : '', { size: '4em' });
    var presets = o.presets ? row(o.presets.map(function (p) { return btn(p[0], function () { xF.input.value = p[1]; yF.input.value = p[2]; if (p[3]) { model = p[3]; mSel.input.value = model; } if (p[4]) { dS.input.value = p[4]; dS.update(); } if (p[5] !== undefined) atF.input.value = p[5]; dS.el.style.display = model === 'poly' ? '' : 'none'; pF.el.style.display = model === 'trig' ? '' : 'none'; draw(); }, 'chip'); }), 'wg-chips') : null;
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '280px') }), P = new Plot(pl, { logy: !!o.logy }), tbl = h('div', { class: 'wg-scroll', style: o.tableHeight ? 'max-height:' + o.tableHeight : '' }), info = h('div', { class: 'wg-note' });
    if (!o.compact) { host.appendChild(row([xF.el, yF.el])); host.appendChild(row([o.fixed || models.length < 2 ? null : mSel.el, dS.el, pF.el, atF.el].filter(Boolean))); }
    if (presets) host.appendChild(presets);
    host.appendChild(h('div', { class: o.side ? 'wg-side' : '' }, o.notable ? [pl] : [pl, tbl])); host.appendChild(info);
    [xF.input, yF.input, atF.input, pF.input].forEach(function (i) { i.addEventListener('input', draw); });
    P.onresize = draw;
    function draw() {
      var xs, ys, fit;
      try { xs = parseList(xF.input.value); ys = parseList(yF.input.value); if (xs.length !== ys.length) throw new Error('x and y need the same number of values'); fit = fitModel(model, xs, ys, dS.value, num(pF.input, 24)); if (fit.k > xs.length) throw new Error('Need at least ' + fit.k + ' points for this model'); }
      catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox(e.message)); info.textContent = ''; return; }
      var n = xs.length, lo = Math.min.apply(null, xs), hi = Math.max.apply(null, xs), X = atF.input.value.trim() ? num(atF.input, NaN) : NaN;
      if (isFinite(X)) { lo = Math.min(lo, X); hi = Math.max(hi, X); }
      var pad = (hi - lo) * 0.08 || 1; lo -= pad; hi += pad;
      var vals = ys.slice(); for (var q = 0; q <= 100; q++) { var v = fit.f(lo + (hi - lo) * q / 100); if (isFinite(v)) vals.push(v); }
      vals.sort(function (a, b) { return a - b; });
      var ylo = Math.min(vals[0], Math.min.apply(null, ys)), yhi = Math.max(vals[vals.length - 1], Math.max.apply(null, ys)), sp = (yhi - ylo) || 1;
      var ymin = Math.min.apply(null, ys), ymax = Math.max.apply(null, ys), ysp = (ymax - ymin) || 1;
      ylo = Math.max(ylo, ymin - 1.5 * ysp); yhi = Math.min(yhi, ymax + 1.5 * ysp); sp = yhi - ylo; ylo -= sp * 0.08; yhi += sp * 0.12;
      if (o.logy) { var lv = vals.concat(ys).filter(function (v) { return v > 0; }).map(Math.log10); ylo = Math.min.apply(null, lv) - 0.3; yhi = Math.max.apply(null, lv) + 0.8; }
      P.begin(); P.range(lo, hi, ylo, yhi); P.axes('x', 'y');
      var sse = 0, my = ys.reduce(function (s, t) { return s + t; }, 0) / n, sst = 0, rows = [];
      xs.forEach(function (x, i) { var fx = fit.f(x), r = ys[i] - fx; sse += r * r; sst += (ys[i] - my) * (ys[i] - my); P.seg(x, ys[i], x, fx, P.col.c5, 1.6, [3, 3]); rows.push([i + 1, fmtD(x), fmtD(ys[i]), fmt(fx, 4), fmt(r, 4)]); });
      P.fn(fit.f, P.col.c1, 2.8); xs.forEach(function (x, i) { P.dot(x, ys[i], 5.5, P.col.ink); });
      if (isFinite(X)) { var fX = fit.f(X); P.seg(X, ylo, X, fX, P.col.c2, 1.5, [4, 4]); P.dot(X, fX, 7, P.col.c2); }
      P.legend([[names[model] + (model === 'poly' ? ' (degree ' + dS.value + ')' : ''), P.col.c1], ['residuals', P.col.c5, [3, 3]]]);
      tbl.innerHTML = ''; tbl.appendChild(table(['i', 'xᵢ', 'yᵢ', 'fitted', 'residual'], rows));
      var r2 = sst ? 1 - sse / sst : 1;
      info.innerHTML = '<b>' + fit.eq + '</b>. Sum of squared residuals S = ' + fmt(sse, 5) + ', R² = ' + fmt(r2, 5) + (fit.lin ? ' (fitted to the logarithms, so S is not the smallest possible in the original y)' : '') + '.' + (isFinite(X) ? ' Prediction at x = ' + fmtD(X) + ': <b>' + fmt(fit.f(X), 4) + '</b>' + (X < Math.min.apply(null, xs) || X > Math.max.apply(null, xs) ? ' <span class="bad">(extrapolation)</span>' : '') + '.' : '');
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L24: overfitting (train vs test error) */
  W.overfit = function (host, o) {
    card(host, 'wg-overfit');
    var xs = o.x ? o.x : null, ys = o.y;
    var truth = o.f ? G.Expr.make(o.f) : function (x) { return Math.sin(2 * Math.PI * x); };
    if (!xs) { xs = []; for (var i = 0; i < ys.length; i++) xs.push(i / (ys.length - 1)); }
    var dS = slider('polynomial degree', 0, Math.min(9, xs.length - 1), 1, o.deg || 3, draw);
    var lamS = slider('ridge λ (log₁₀)', -9, 1, 0.5, o.loglam !== undefined ? o.loglam : -9, draw, function (v) { return v <= -9 ? '0' : '10^' + v; });
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '240px') }), P = new Plot(pl), pl2 = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '240px') }), P2 = new Plot(pl2, { logy: true }), info = h('div', { class: 'wg-note' });
    host.appendChild(row([dS.el, o.ridge ? lamS.el : null].filter(Boolean))); host.appendChild(h('div', { class: 'wg-two' }, [pl, pl2])); host.appendChild(info);
    P.onresize = draw; P2.onresize = draw;
    function fitDeg(d, lam) {
      var A = xs.map(function (x) { var t = 2 * x - 1, r = []; for (var k = 0; k <= d; k++) r.push(Math.pow(t, k)); return r; }), yy = ys.slice();
      if (lam > 0) { for (var k = 1; k <= d; k++) { var r = new Array(d + 1).fill(0); r[k] = Math.sqrt(lam); A.push(r); yy.push(0); } }
      var c = lstsq(A, yy); return function (x) { var t = 2 * x - 1, s = 0; for (var k = d; k >= 0; k--) s = s * t + c[k]; return s; };
    }
    function errs(g) { var tr = 0, te = 0, i; for (i = 0; i < xs.length; i++) tr += Math.pow(g(xs[i]) - ys[i], 2); for (i = 0; i <= 200; i++) { var x = i / 200; te += Math.pow(g(x) - truth(x), 2); } return [Math.sqrt(tr / xs.length), Math.sqrt(te / 201)]; }
    function draw() {
      var d = dS.value, lam = o.ridge && lamS.value > -9 ? Math.pow(10, lamS.value) : 0, g = fitDeg(d, lam);
      P.begin(); P.range(0, 1, -1.7, 2.6); P.axes('x', 'y'); P.fn(truth, P.col.mut, 2, [6, 4]); P.fn(g, P.col.c1, 2.8); xs.forEach(function (x, i) { P.dot(x, ys[i], 5, P.col.ink); });
      P.legend([['true curve', P.col.mut, [6, 4]], ['degree ' + d + ' fit', P.col.c1]]);
      var tr = [], te = [];
      for (var k = 0; k <= Math.min(9, xs.length - 1); k++) { var e = errs(fitDeg(k, lam)); tr.push([k, Math.max(e[0], 1e-4)]); te.push([k, Math.max(e[1], 1e-4)]); }
      P2.begin(); P2.o.xstep = 1; P2.range(0, Math.min(9, xs.length - 1), -2.5, 1.6); P2.axes('degree', '');
      P2.poly(tr, P2.col.c3, 2.6); P2.poly(te, P2.col.c5, 2.6); tr.forEach(function (p) { P2.dot(p[0], p[1], 4, P2.col.c3); }); te.forEach(function (p) { P2.dot(p[0], p[1], 4, P2.col.c5); });
      P2.seg(d, 1e-2, d, 10, P2.col.mut, 1.2, [4, 4]); P2.legend([['training error (RMS)', P2.col.c3], ['test error (RMS)', P2.col.c5]]);
      var cur = errs(g), best = te.reduce(function (b, p) { return p[1] < b[1] ? p : b; }, te[0]);
      info.innerHTML = 'Degree ' + d + (lam ? ', λ = ' + sci(lam, 0) : '') + ': training error <b>' + (cur[0] < 5e-4 ? '0.000' : fmt(cur[0], 3)) + '</b>, test error <b>' + fmt(cur[1], 3) + '</b>. Lowest test error at degree ' + best[0] + '. ' + (cur[0] < 0.05 && cur[1] > 2 * best[1] ? '<span class="bad">Overfitting: the curve passes (almost) through every noisy point but misses the true shape.</span>' : d <= 1 ? 'Underfitting: too simple to follow the curve.' : '');
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L25: golden-section search */
  W.golden = function (host, o) {
    card(host, 'wg-golden');
    var fF = field('f(x) =', o.f || 'x^4 - 3x^3 + 2', { size: '11em' }), aF = field('a =', o.a !== undefined ? o.a : 0, { size: '3.5em' }), bF = field('b =', o.b !== undefined ? o.b : 3, { size: '3.5em' });
    var step = o.step || 1;
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '260px') }), P = new Plot(pl), tbl = h('div', { class: 'wg-scroll', style: o.tableHeight ? 'max-height:' + o.tableHeight : '' }), info = h('div', { class: 'wg-note' });
    host.appendChild(row([fF.el, aF.el, bF.el, btn('◀', function () { if (step > 0) step--; draw(); }), btn('Next step ▶', function () { step++; draw(); }, 'pri'), btn('Reset', function () { step = 0; draw(); })]));
    host.appendChild(h('div', { class: o.side ? 'wg-side' : '' }, [pl, tbl])); host.appendChild(info);
    [fF.input, aF.input, bF.input].forEach(function (i) { i.addEventListener('input', function () { step = 0; draw(); }); });
    P.onresize = draw;
    function draw() {
      var f; try { f = G.Expr.make(fF.input.value); } catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox(e.message)); return; }
      var a0 = num(aF.input, 0), b0 = num(bF.input, 3), g = (Math.sqrt(5) - 1) / 2, a = a0, b = b0, c = b - g * (b - a), d = a + g * (b - a), fc = f(c), fd = f(d), rows = [[0, fmt(a, 4), fmt(b, 4), fmt(c, 4), fmt(d, 4), fmt(fc, 4), fmt(fd, 4), '']];
      for (var k = 1; k <= step; k++) {
        var keep;
        if (fc < fd) { b = d; d = c; fd = fc; c = b - g * (b - a); fc = f(c); keep = '[a, d]'; } else { a = c; c = d; fc = fd; d = a + g * (b - a); fd = f(d); keep = '[c, b]'; }
        rows[rows.length - 1][7] = keep; rows.push([k, fmt(a, 4), fmt(b, 4), fmt(c, 4), fmt(d, 4), fmt(fc, 4), fmt(fd, 4), '']);
      }
      var vals = []; for (var q = 0; q <= 120; q++) { var v = f(a0 + (b0 - a0) * q / 120); if (isFinite(v)) vals.push(v); }
      var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals), sp = (hi - lo) || 1;
      P.begin(); P.range(a0 - (b0 - a0) * 0.05, b0 + (b0 - a0) * 0.05, lo - sp * 0.1, hi + sp * 0.1); P.axes('x', '');
      P.vband(a, b, 'rgba(47,109,181,0.12)'); P.fn(f, P.col.c1, 2.8);
      P.dot(c, fc, 6, P.col.c2); P.dot(d, fd, 6, P.col.c5); P.label(c, fc, 'c', P.col.c2, 'center', -8, true); P.label(d, fd, 'd', P.col.c5, 'center', -8, true);
      tbl.innerHTML = ''; tbl.appendChild(table(['k', 'a', 'b', 'c', 'd', 'f(c)', 'f(d)', 'keep'], rows, { hi: rows.length - 1 }));
      info.innerHTML = 'Bracket width ' + fmt(b - a, 6) + ' = ' + fmt((b - a) / (b0 - a0), 5) + ' of the start (×0.618 per step, one new f-value each). Estimate of the minimiser: <b>' + fmt((a + b) / 2, 6) + '</b>.';
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L25: gradient descent, momentum and Newton on f(x, y) */
  W.gd2d = function (host, o) {
    card(host, 'wg-gd2d');
    var fF = field('f(x, y) =', o.f || '0.5*(x^2 + 10*y^2)', { size: '12em' }), xF = field('x₀ =', o.x0 !== undefined ? o.x0 : 10, { size: '3.5em' }), yF = field('y₀ =', o.y0 !== undefined ? o.y0 : 1, { size: '3.5em' });
    var meth = o.method || 'gd', M = { gd: 'gradient descent', mom: 'gradient descent + momentum', newton: "Newton's method" };
    var mSel = select('Method', Object.keys(M).map(function (k) { return [k, M[k]]; }), meth, function (v) { meth = v; draw(); });
    var eS = slider('learning rate η', -3, 0.3, 0.01, o.logeta !== undefined ? o.logeta : -1, draw, function (v) { return (+Math.pow(10, v).toPrecision(3)) + ''; });
    var bS = slider('momentum β', 0, 0.95, 0.05, o.beta || 0.5, draw, function (v) { return v.toFixed(2); });
    var NS = slider('steps', 1, 300, 1, o.steps || 30, draw);
    var R = o.range || [-12, 12, -4, 4];
    var presets = o.presets ? row(o.presets.map(function (p) { return btn(p[0], function () { fF.input.value = p[1]; xF.input.value = p[2]; yF.input.value = p[3]; if (p[4] !== undefined) { eS.input.value = p[4]; eS.update(); } if (p[5]) { meth = p[5]; mSel.input.value = meth; } if (p[6]) R = p[6]; draw(); }, 'chip'); }), 'wg-chips') : null;
    var pl = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '300px') }), P = new Plot(pl), tbl = h('div', { class: 'wg-scroll', style: o.tableHeight ? 'max-height:' + o.tableHeight : '' }), info = h('div', { class: 'wg-note' });
    host.appendChild(row([fF.el, xF.el, yF.el, o.fixed ? null : mSel.el].filter(Boolean))); host.appendChild(row([eS.el, bS.el, NS.el])); if (presets) host.appendChild(presets);
    host.appendChild(h('div', { class: o.side ? 'wg-side' : '' }, o.notable ? [pl] : [pl, tbl])); host.appendChild(info);
    [fF.input, xF.input, yF.input].forEach(function (i) { i.addEventListener('input', draw); });
    P.onresize = draw;
    function levels(F, f0) {
      var N = 80, c = P.ctx, dx = (R[1] - R[0]) / N, dy = (R[3] - R[2]) / N, v = [], all = [];
      for (var i = 0; i <= N; i++) { v.push([]); for (var j = 0; j <= N; j++) { var t = F(R[0] + i * dx, R[2] + j * dy); v[i].push(t); if (isFinite(t)) all.push(t); } }
      all.sort(function (a, b) { return a - b; }); var mn = all[0], mx = all[Math.floor(all.length * 0.9)];
      for (var L = 1; L <= 9; L++) {
        var lev = mn + (mx - mn) * Math.pow(L / 10, 2); c.save(); P.clip(); c.strokeStyle = P.col.c1; c.globalAlpha = 0.35; c.lineWidth = 1.5; c.beginPath();
        for (var i2 = 0; i2 < N; i2++) for (var j2 = 0; j2 < N; j2++) {
          var x0 = R[0] + i2 * dx, y0 = R[2] + j2 * dy, a = v[i2][j2] - lev, b = v[i2 + 1][j2] - lev, cc = v[i2 + 1][j2 + 1] - lev, d = v[i2][j2 + 1] - lev, pts = [];
          if (!isFinite(a + b + cc + d)) continue;
          var lerp = function (p, q, fp, fq) { return p + (q - p) * fp / (fp - fq); };
          if ((a < 0) !== (b < 0)) pts.push([lerp(x0, x0 + dx, a, b), y0]); if ((b < 0) !== (cc < 0)) pts.push([x0 + dx, lerp(y0, y0 + dy, b, cc)]);
          if ((cc < 0) !== (d < 0)) pts.push([lerp(x0 + dx, x0, cc, d), y0 + dy]); if ((d < 0) !== (a < 0)) pts.push([x0, lerp(y0 + dy, y0, d, a)]);
          for (var k = 0; k + 1 < pts.length; k += 2) { c.moveTo(P.X(pts[k][0]), P.Y(pts[k][1])); c.lineTo(P.X(pts[k + 1][0]), P.Y(pts[k + 1][1])); }
        }
        c.stroke(); P.unclip(); c.restore();
      }
    }
    function draw() {
      var F, Fx, Fy;
      try { F = G.Expr.make2(fF.input.value); Fx = F.dx(); Fy = F.dy(); } catch (e) { tbl.innerHTML = ''; tbl.appendChild(errBox(e.message)); return; }
      bS.el.style.display = meth === 'mom' ? '' : 'none'; eS.el.style.display = meth === 'newton' ? 'none' : '';
      var eta = Math.pow(10, eS.value), beta = bS.value, N = NS.value, x = num(xF.input, 10), y = num(yF.input, 1), vx = 0, vy = 0, pts = [[x, y]], rows = [[0, fmt(x, 5), fmt(y, 5), fmt(F(x, y), 6)]], hE = 1e-5;
      for (var k = 1; k <= N; k++) {
        var gx = Fx(x, y), gy = Fy(x, y);
        if (meth === 'gd') { x -= eta * gx; y -= eta * gy; }
        else if (meth === 'mom') { vx = beta * vx - eta * gx; vy = beta * vy - eta * gy; x += vx; y += vy; }
        else {
          var hxx = (Fx(x + hE, y) - Fx(x - hE, y)) / (2 * hE), hxy = (Fx(x, y + hE) - Fx(x, y - hE)) / (2 * hE), hyy = (Fy(x, y + hE) - Fy(x, y - hE)) / (2 * hE), det = hxx * hyy - hxy * hxy;
          if (!det) break; x -= (hyy * gx - hxy * gy) / det; y -= (-hxy * gx + hxx * gy) / det;
        }
        pts.push([x, y]); if (k <= 8 || k === N || k % Math.ceil(N / 8) === 0) rows.push([k, fmt(x, 5), fmt(y, 5), fmt(F(x, y), 6)]);
        if (!isFinite(x) || Math.abs(x) + Math.abs(y) > 1e9) break;
      }
      P.begin(); P.range(R[0], R[1], R[2], R[3]); P.axes('x', 'y'); levels(function (a, b) { return F(a, b); });
      var vis = pts.filter(function (p) { return isFinite(p[0]) && Math.abs(p[0]) < 1e6; });
      P.poly(vis, P.col.c2, 2.2); vis.forEach(function (p, i) { P.dot(p[0], p[1], i === vis.length - 1 ? 7 : 3.5, i === vis.length - 1 ? P.col.c5 : P.col.c2); });
      P.legend([[M[meth] + (meth === 'newton' ? '' : ', η = ' + (+eta.toPrecision(3))), P.col.c2]]);
      tbl.innerHTML = ''; tbl.appendChild(table(['k', 'x', 'y', 'f(x, y)'], rows, { hi: rows.length - 1 }));
      var fend = F(x, y), blow = !isFinite(fend) || Math.abs(x) + Math.abs(y) > 1e6;
      info.innerHTML = (blow ? '<span class="bad">Diverged: the learning rate is too large for the steepest direction (η must be below 2/λ<sub>max</sub> of the Hessian).</span>' : 'After ' + (pts.length - 1) + ' steps: f = <b>' + (Math.abs(fend) >= 1e-3 && Math.abs(fend) < 1e5 ? fmt(fend, 5) : sci(fend, 2)) + '</b> at (' + fmt(x, 4) + ', ' + fmt(y, 4) + ').') + (meth === 'newton' ? ' Newton uses the Hessian (curvature): one step is exact for a quadratic.' : '');
    }
    draw(); redrawOnTheme(draw);
  };

  /* ============================================================= L25: why stochastic (mini-batch) gradient descent */
  W.sgd = function (host, o) {
    card(host, 'wg-sgd');
    var nSel = select('data size N', [['1000', '1,000'], ['10000', '10,000'], ['100000', '100,000'], ['1000000', '1,000,000']], String(o.N || 100000), function () { draw(); });
    var bSel = select('batch size B', [['1', '1 (pure SGD)'], ['8', '8'], ['32', '32'], ['256', '256'], ['4096', '4096']], String(o.B || 32), function () { draw(); });
    var cSel = select('compute budget', [['100000', '100,000 gradients'], ['1000000', '1,000,000 gradients'], ['5000000', '5,000,000 gradients']], String(o.budget || 1000000), function () { draw(); });
    var eS = slider('learning rate η', -2.5, 0.3, 0.05, o.logeta !== undefined ? o.logeta : Math.log10(0.5), draw, function (v) { return String(+Math.pow(10, v).toPrecision(2)); });
    var dChk = h('input', { type: 'checkbox' }); dChk.checked = !!o.decay; dChk.addEventListener('change', draw);
    var dLab = h('label', { class: 'wg-f' }, [dChk, h('span', { html: 'decrease η for mini-batches' })]);
    var p1 = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '300px') }), P1 = new Plot(p1, { logy: true });
    var p2 = h('div', { class: 'wg-plot', style: 'height:' + (o.height || '300px') }), P2 = new Plot(p2);
    var tbl = h('div'), info = h('div', { class: 'wg-note' });
    host.appendChild(row([nSel.el, bSel.el, cSel.el])); host.appendChild(row([eS.el, dLab]));
    host.appendChild(h('div', { class: 'wg-two' }, [p1, p2])); host.appendChild(tbl); host.appendChild(info);
    var cache = {}, EV = 20000, res = null;
    function sig(z) { return 1 / (1 + Math.exp(-z)); }
    function data(N) {
      if (cache[N]) return cache[N];
      var s = 12345, rnd = function () { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
      var x = new Float64Array(N), y = new Float64Array(N), i;
      for (i = 0; i < N; i++) { x[i] = 5 * rnd(); y[i] = rnd() < sig(1.35 * x[i] - 3.72) ? 1 : 0; }
      var m = Math.min(N, EV), w = 0, b = 0;                     // optimum of the evaluation set by Newton
      for (var it = 0; it < 30; it++) {
        var gw = 0, gb = 0, hww = 0, hwb = 0, hbb = 0;
        for (i = 0; i < m; i++) { var p = sig(w * x[i] + b), e = p - y[i], q = p * (1 - p); gw += e * x[i]; gb += e; hww += q * x[i] * x[i]; hwb += q * x[i]; hbb += q; }
        var det = hww * hbb - hwb * hwb; w -= (hbb * gw - hwb * gb) / det; b -= (-hwb * gw + hww * gb) / det;
      }
      var d = { x: x, y: y, m: m, w: w, b: b }; d.Ls = loss(d, w, b);
      var G = 40, grid = [];                                      // loss surface on a coarse grid (2000 points)
      for (var a = 0; a <= G; a++) { grid.push([]); for (var c = 0; c <= G; c++) grid[a].push(loss(d, -0.5 + 3.5 * a / G, -7 + 8 * c / G, 2000)); }
      d.grid = grid; cache[N] = d; return d;
    }
    function loss(d, w, b, mm) {
      var m = Math.min(mm || d.m, d.m), s = 0;
      for (var i = 0; i < m; i++) { var z = w * d.x[i] + b; s += (z > 0 ? z + Math.log(1 + Math.exp(-z)) : Math.log(1 + Math.exp(z))) - d.y[i] * z; }
      return s / m;
    }
    function train(d, N, B, eta, budget, decay) {
      var w = 0, b = 0, used = 0, i = 0, k = 0, nck = 60, next = 0, curve = [], path = [[w, b]];
      var sd = 777, rnd = function () { sd = (sd * 16807) % 2147483647; return sd / 2147483647; };
      var mark = function () { curve.push([used / 1e3, Math.max(loss(d, w, b) - d.Ls, 1e-5)]); path.push([w, b]); next += budget / nck; };
      mark();
      while (used + B <= budget) {
        var gw = 0, gb = 0;
        if (B < N) i = Math.floor(rnd() * N);                    // random batch (data are in random order)
        else i = 0;
        for (var j = 0; j < B; j++) { if (i >= N) i = 0; var e = sig(w * d.x[i] + b) - d.y[i]; gw += e * d.x[i]; gb += e; i++; }
        var et = decay && B < N ? eta / Math.sqrt(1 + k / 1000) : eta;
        w -= et * gw / B; b -= et * gb / B; used += B; k++;
        if (!isFinite(w) || Math.abs(w) > 1e6) break;
        if (used >= next || used + B > budget) mark();
      }
      return { w: w, b: b, steps: k, used: used, curve: curve, path: path, ex: Math.max(loss(d, w, b) - d.Ls, 0) };
    }
    P1.onresize = function () { if (res) plot(); }; P2.onresize = P1.onresize;
    function draw() {
      var N = +nSel.input.value, B = Math.min(+bSel.input.value, N), budget = +cSel.input.value, eta = Math.pow(10, eS.value), d = data(N);
      res = { d: d, N: N, B: B, budget: budget, full: train(d, N, N, eta, budget, false), mini: train(d, N, B, eta, budget, dChk.checked) };
      plot();
    }
    function plot() {
      var r = res, d = r.d, F = r.full, Mn = r.mini;
      P1.begin(); P1.o.yfmt = null; P1.range(0, r.budget / 1e3, -5, 0.5); P1.axes('gradients computed (thousands)', '');
      var fc = F.curve.length > 1 ? F.curve : [[0, F.curve[0][1]], [r.budget / 1e3, F.curve[0][1]]];
      P1.poly(fc, P1.col.mut, 2.6); P1.poly(Mn.curve, P1.col.c2, 2.6);
      if (F.steps <= 60) F.curve.slice(1).forEach(function (p) { P1.dot(p[0], p[1], 4.5, P1.col.mut); });
      P1.legend([['full batch (N = ' + r.N.toLocaleString('en-US') + ')', P1.col.mut], ['mini-batch B = ' + r.B, P1.col.c2]]);
      P2.begin(); P2.range(-0.5, 3, -7, 1.5); P2.axes('w', 'b');
      var c = P2.ctx, G = d.grid.length - 1, lv = [0.45, 0.5, 0.6, 0.75, 1, 1.5, 2.5, 4];
      c.save(); P2.clip(); c.strokeStyle = P2.col.c1; c.globalAlpha = 0.3; c.lineWidth = 1.4; c.beginPath();
      lv.forEach(function (L) {
        for (var a = 0; a < G; a++) for (var bb = 0; bb < G; bb++) {
          var x0 = -0.5 + 3.5 * a / G, y0 = -7 + 8 * bb / G, dx = 3.5 / G, dy = 8 / G, v = [d.grid[a][bb] - L, d.grid[a + 1][bb] - L, d.grid[a + 1][bb + 1] - L, d.grid[a][bb + 1] - L], q = [];
          var cr = function (p, s, vp, vs) { return p + (s - p) * vp / (vp - vs); };
          if ((v[0] < 0) !== (v[1] < 0)) q.push([cr(x0, x0 + dx, v[0], v[1]), y0]); if ((v[1] < 0) !== (v[2] < 0)) q.push([x0 + dx, cr(y0, y0 + dy, v[1], v[2])]);
          if ((v[2] < 0) !== (v[3] < 0)) q.push([cr(x0 + dx, x0, v[2], v[3]), y0 + dy]); if ((v[3] < 0) !== (v[0] < 0)) q.push([x0, cr(y0 + dy, y0, v[3], v[0])]);
          for (var t = 0; t + 1 < q.length; t += 2) { c.moveTo(P2.X(q[t][0]), P2.Y(q[t][1])); c.lineTo(P2.X(q[t + 1][0]), P2.Y(q[t + 1][1])); }
        }
      });
      c.stroke(); P2.unclip(); c.restore();
      P2.poly(F.path, P2.col.mut, 2.4); P2.poly(Mn.path, P2.col.c2, 1.8);
      P2.dot(d.w, d.b, 7, P2.col.c3); P2.dot(F.w, F.b, 6, P2.col.mut); P2.dot(Mn.w, Mn.b, 6, P2.col.c2);
      P2.legend([['full-batch path', P2.col.mut], ['mini-batch path', P2.col.c2], ['best (w, b)', P2.col.c3]]);
      var fmtL = function (v) { return v < 1e-4 ? '< 0.0001' : fmt(v, 4); };
      tbl.innerHTML = ''; tbl.appendChild(table(['method', 'gradients per step', 'steps within budget', 'w', 'b', 'excess loss'], [
        ['full-batch GD', r.N.toLocaleString('en-US'), String(F.steps), fmt(F.w, 3), fmt(F.b, 3), fmtL(F.ex)],
        ['mini-batch SGD', String(r.B), Mn.steps.toLocaleString('en-US'), fmt(Mn.w, 3), fmt(Mn.b, 3), fmtL(Mn.ex)]]));
      var msg = 'Best fit on this data: w = ' + fmt(d.w, 3) + ', b = ' + fmt(d.b, 3) + '. ';
      msg += 'Same budget: mini-batch takes <b>' + (r.N / r.B >= 10 ? Math.round(r.N / r.B).toLocaleString('en-US') : (r.N / r.B).toFixed(1)) + ' steps</b> for every full-batch step. ';
      if (F.steps === 0) msg += '<span class="bad">Full-batch GD cannot take even one step: a single step needs all ' + r.N.toLocaleString('en-US') + ' gradients.</span> ';
      else if (F.ex > 10 * Math.max(Mn.ex, 1e-4)) msg += '<span class="bad">With the same compute, full-batch GD is still far from the minimum: it took only ' + F.steps + ' step' + (F.steps > 1 ? 's' : '') + '.</span> ';
      if (r.B < 32 && Mn.ex > 0.01 && !dChk.checked) msg += 'Small batches are noisy: lower η or tick "decrease η". ';
      if (!isFinite(Mn.w) || !isFinite(F.w)) msg += '<span class="bad">Diverged: η too large.</span> ';
      info.innerHTML = msg + (d.m < r.N ? 'Loss measured on the first ' + d.m.toLocaleString('en-US') + ' points.' : '');
    }
    draw(); redrawOnTheme(plot);
  };

  /* ------------------------------------------------------------- mount */
  function mountAll(root) {
    [].forEach.call((root || document).querySelectorAll('[data-w]'), function (el) {
      if (el._w) return; el._w = true;
      var name = el.getAttribute('data-w'), opts = {};
      try { opts = JSON.parse(el.getAttribute('data-o') || '{}'); } catch (e) {}
      if (!W[name]) { el.textContent = 'Unknown widget ' + name; return; }
      try { W[name](el, opts); } catch (e) { el.textContent = 'Widget error: ' + e.message; if (G.console) console.error(e); }
    });
  }
  G.W = W; G.Widgets = { mountAll: mountAll };
})(window);
