/* Expr: parse textbook-style formulas (x^3 - 2x + 3sin(x), e^x, ln x), evaluate fast,
   differentiate symbolically, and print as text or LaTeX. Used by the widgets' f(x) boxes. */
(function (G) {
  'use strict';
  var FUN = { sin: Math.sin, cos: Math.cos, tan: Math.tan, asin: Math.asin, acos: Math.acos, atan: Math.atan, sinh: Math.sinh, cosh: Math.cosh, tanh: Math.tanh,
    exp: Math.exp, ln: Math.log, log: Math.log, log10: Math.log10, sqrt: Math.sqrt, abs: Math.abs, cbrt: Math.cbrt,
    sec: function (x) { return 1 / Math.cos(x); }, cot: function (x) { return 1 / Math.tan(x); }, csc: function (x) { return 1 / Math.sin(x); } };
  function tokenize(s) {
    s = s.replace(/\*\*/g, '^').replace(/·|×/g, '*').replace(/−/g, '-').replace(/π/g, 'pi').replace(/math\./g, '');
    var t = [], i = 0;
    while (i < s.length) {
      var c = s[i];
      if (/\s/.test(c)) { i++; continue; }
      var m = /^(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?/.exec(s.slice(i));
      if (m) { t.push({ t: 'n', v: parseFloat(m[0]) }); i += m[0].length; continue; }
      m = /^[A-Za-z_][A-Za-z_0-9]*/.exec(s.slice(i));
      if (m) {
        var w = m[0];
        // split juxtaposed names like "xsin" or "pix" greedily into known pieces
        var parts = splitName(w);
        parts.forEach(function (p) { t.push({ t: 'id', v: p }); });
        i += w.length; continue;
      }
      if ('+-*/^(),'.indexOf(c) >= 0) { t.push({ t: 'op', v: c }); i++; continue; }
      throw new Error("I don't understand '" + c + "'");
    }
    return t;
  }
  var KNOWN = Object.keys(FUN).concat(['pi', 'e', 'x', 'y', 't', 'h', 'n']);
  function splitName(w) {
    if (KNOWN.indexOf(w) >= 0) return [w];
    var out = [], i = 0;
    while (i < w.length) {
      var best = null;
      KNOWN.forEach(function (k) { if (w.substr(i, k.length) === k && (!best || k.length > best.length)) best = k; });
      if (!best) return [w];
      out.push(best); i += best.length;
    }
    return out;
  }
  function parse(src) {
    var t = tokenize(src), p = 0;
    function peek() { return t[p]; }
    function isOp(v) { return t[p] && t[p].t === 'op' && t[p].v === v; }
    function expr() {
      var e = term();
      while (isOp('+') || isOp('-')) { var o = t[p++].v; e = { k: o, a: e, b: term() }; }
      return e;
    }
    function startsFactor() { var k = peek(); return k && (k.t === 'n' || k.t === 'id' || (k.t === 'op' && k.v === '(')); }
    function term() {
      var e = unary();
      while (true) {
        if (isOp('*') || isOp('/')) { var o = t[p++].v; e = { k: o, a: e, b: unary() }; }
        else if (startsFactor()) e = { k: '*', a: e, b: power() };       // implicit multiplication: 2x, 3sin(x), (x+1)(x-1)
        else break;
      }
      return e;
    }
    function unary() { if (isOp('-')) { p++; return { k: 'neg', a: unary() }; } if (isOp('+')) { p++; return unary(); } return power(); }
    function power() {
      var b = atom();
      if (isOp('^')) { p++; var ex = unaryPow(); return { k: '^', a: b, b: ex }; }
      return b;
    }
    function unaryPow() { if (isOp('-')) { p++; return { k: 'neg', a: unaryPow() }; } return power(); }
    function atom() {
      var k = t[p++];
      if (!k) throw new Error('the formula ends too early');
      if (k.t === 'n') return { k: 'num', v: k.v };
      if (k.t === 'op' && k.v === '(') { var e = expr(); if (!isOp(')')) throw new Error("missing ')'"); p++; return e; }
      if (k.t === 'id') {
        if (FUN[k.v]) {
          var arg;
          if (isOp('(')) { p++; arg = expr(); if (!isOp(')')) throw new Error("missing ')' after " + k.v); p++; }
          else if (isOp('^')) {             // sin^2(x)
            p++; var pw = atom(); var a2; if (isOp('(')) { p++; a2 = expr(); p++; } else a2 = power();
            return { k: '^', a: { k: 'fn', f: k.v, a: a2 }, b: pw };
          }
          else arg = power();               // ln x, sin x
          return { k: 'fn', f: k.v, a: arg };
        }
        if (k.v === 'pi') return { k: 'num', v: Math.PI, name: 'π' };
        if (k.v === 'e') return { k: 'num', v: Math.E, name: 'e' };
        return { k: 'var', n: k.v };
      }
      throw new Error("unexpected '" + k.v + "'");
    }
    var e = expr();
    if (p < t.length) throw new Error("unexpected '" + t[p].v + "'");
    return e;
  }
  function compile(e) {
    switch (e.k) {
      case 'num': var v = e.v; return function () { return v; };
      case 'var': var n = e.n; return function (s) { var x = s[n]; if (x === undefined) throw new Error('unknown variable ' + n); return x; };
      case 'neg': var a = compile(e.a); return function (s) { return -a(s); };
      case 'fn': var f = FUN[e.f], g = compile(e.a); return function (s) { return f(g(s)); };
      case '^': {
        var A = compile(e.a), B = compile(e.b);
        if (e.b.k === 'num' && Number.isInteger(e.b.v)) { var k = e.b.v; return function (s) { return Math.pow(A(s), k); }; }
        return function (s) { return Math.pow(A(s), B(s)); };
      }
      default: {
        var L = compile(e.a), R = compile(e.b), op = e.k;
        if (op === '+') return function (s) { return L(s) + R(s); };
        if (op === '-') return function (s) { return L(s) - R(s); };
        if (op === '*') return function (s) { return L(s) * R(s); };
        return function (s) { return L(s) / R(s); };
      }
    }
  }
  /* ---------- symbolic derivative with light simplification ---------- */
  function N(v) { return { k: 'num', v: v }; }
  function isN(e, v) { return e.k === 'num' && (v === undefined || e.v === v); }
  function add(a, b) { if (isN(a, 0)) return b; if (isN(b, 0)) return a; if (isN(a) && isN(b) && !a.name && !b.name) return N(a.v + b.v); return { k: '+', a: a, b: b }; }
  function sub(a, b) { if (isN(b, 0)) return a; if (isN(a, 0)) return neg(b); if (isN(a) && isN(b) && !a.name && !b.name) return N(a.v - b.v); return { k: '-', a: a, b: b }; }
  function mul(a, b) {
    if (isN(a, 0) || isN(b, 0)) return N(0); if (isN(a, 1)) return b; if (isN(b, 1)) return a;
    if (isN(a) && isN(b) && !a.name && !b.name) return N(a.v * b.v);
    if (isN(b) && !isN(a)) return mul(b, a);
    if (isN(a) && b.k === '*' && isN(b.a) && !a.name && !b.a.name) return mul(N(a.v * b.a.v), b.b);
    if (a.k === 'neg') return neg(mul(a.a, b)); if (b.k === 'neg') return neg(mul(a, b.a));
    if (a.k === '/' && isN(a.a, 1)) return div(b, a.b);
    if (b.k === '/' && isN(b.a, 1)) return div(a, b.b);
    if (isN(a) && b.k === '/' && isN(b.a) && !a.name && !b.a.name) return div(N(a.v * b.a.v), b.b);
    return { k: '*', a: a, b: b };
  }
  function div(a, b) {
    if (isN(a, 0)) return N(0); if (isN(b, 1)) return a;
    if (b.k === '*' && isN(b.a) && a.k === '*' && isN(a.a) && !a.a.name && !b.a.name && a.a.v % b.a.v === 0) return div(mul(N(a.a.v / b.a.v), a.b), b.b);
    if (b.k === '*' && isN(b.a) && isN(a) && !a.name && !b.a.name && a.v % b.a.v === 0) return div(N(a.v / b.a.v), b.b);
    if (a.k === 'neg') return neg(div(a.a, b));
    return { k: '/', a: a, b: b };
  }
  function neg(a) { if (isN(a) && !a.name) return N(-a.v); if (a.k === 'neg') return a.a; return { k: 'neg', a: a }; }
  function pow(a, b) { if (isN(b, 1)) return a; if (isN(b, 0)) return N(1); return { k: '^', a: a, b: b }; }
  function fn(f, a) { return { k: 'fn', f: f, a: a }; }
  function dep(e, x) { if (e.k === 'var') return e.n === x; if (e.k === 'num') return false; return (e.a ? dep(e.a, x) : false) || (e.b ? dep(e.b, x) : false); }
  function d(e, x) {
    if (!dep(e, x)) return N(0);
    switch (e.k) {
      case 'var': return N(1);
      case 'neg': return neg(d(e.a, x));
      case '+': return add(d(e.a, x), d(e.b, x));
      case '-': return sub(d(e.a, x), d(e.b, x));
      case '*': return add(mul(d(e.a, x), e.b), mul(e.a, d(e.b, x)));
      case '/': return div(sub(mul(d(e.a, x), e.b), mul(e.a, d(e.b, x))), pow(e.b, N(2)));
      case '^':
        if (!dep(e.b, x)) { var nb = isN(e.b) ? N(e.b.v - 1) : sub(e.b, N(1)); return mul(mul(e.b, pow(e.a, nb)), d(e.a, x)); }
        if (e.a.k === 'num' && e.a.name === 'e') return mul(d(e.b, x), e);
        if (!dep(e.a, x)) return mul(mul(e, fn('ln', e.a)), d(e.b, x));
        return mul(e, add(mul(d(e.b, x), fn('ln', e.a)), div(mul(e.b, d(e.a, x)), e.a)));
      case 'fn': {
        var u = e.a, du = d(u, x), r;
        switch (e.f) {
          case 'sin': r = fn('cos', u); break;
          case 'cos': r = neg(fn('sin', u)); break;
          case 'tan': r = pow(fn('sec', u), N(2)); break;
          case 'exp': r = fn('exp', u); break;
          case 'ln': case 'log': r = div(N(1), u); break;
          case 'log10': r = div(N(1), mul(u, fn('ln', N(10)))); break;
          case 'sqrt': r = div(N(1), mul(N(2), fn('sqrt', u))); break;
          case 'asin': r = div(N(1), fn('sqrt', sub(N(1), pow(u, N(2))))); break;
          case 'acos': r = neg(div(N(1), fn('sqrt', sub(N(1), pow(u, N(2)))))); break;
          case 'atan': r = div(N(1), add(N(1), pow(u, N(2)))); break;
          case 'sinh': r = fn('cosh', u); break; case 'cosh': r = fn('sinh', u); break;
          case 'tanh': r = sub(N(1), pow(fn('tanh', u), N(2))); break;
          case 'abs': r = div(u, fn('abs', u)); break;
          case 'cbrt': r = div(N(1), mul(N(3), pow(fn('cbrt', u), N(2)))); break;
          case 'sec': r = mul(fn('sec', u), fn('tan', u)); break;
          default: throw new Error('cannot differentiate ' + e.f);
        }
        return mul(r, du);
      }
    }
  }
  /* ---------- printing ---------- */
  var PREC = { '+': 1, '-': 1, '*': 2, '/': 2, neg: 3, '^': 4, fn: 5, num: 6, var: 6 };
  function fmtNum(v) { if (Number.isInteger(v)) return String(v); var s = String(+v.toPrecision(10)); return s; }
  function toText(e, parentP) {
    parentP = parentP || 0; var s, p = PREC[e.k];
    switch (e.k) {
      case 'num': s = e.name || fmtNum(e.v); if (e.v < 0 && !e.name) p = 3; break;
      case 'var': s = e.n; break;
      case 'neg': s = '-' + toText(e.a, 3); break;
      case 'fn': s = (e.f === 'log' ? 'ln' : e.f) + '(' + toText(e.a) + ')'; break;
      case '^': s = toText(e.a, 5) + '^' + toText(e.b, 4); break;
      case '*': {
        var A = toText(e.a, 2), B = toText(e.b, 2.1);
        s = (isN(e.a) && !isN(e.b) && /^[a-zA-Z(]/.test(B)) ? A + B : A + '*' + B; break;
      }
      case '/': s = toText(e.a, 2) + '/' + toText(e.b, 2.1); break;
      case '+': s = toText(e.a, 1) + ' + ' + toText(e.b, 1.1); break;
      case '-': s = toText(e.a, 1) + ' - ' + toText(e.b, 1.1); break;
    }
    return p < parentP ? '(' + s + ')' : s;
  }
  function toTex(e, parentP) {
    parentP = parentP || 0; var s, p = PREC[e.k];
    switch (e.k) {
      case 'num': s = e.name === 'π' ? '\\pi' : (e.name || fmtNum(e.v)); if (e.v < 0 && !e.name) p = 3; break;
      case 'var': s = e.n; break;
      case 'neg': s = '-' + toTex(e.a, 3); break;
      case 'fn': {
        var nm = { ln: '\\ln', log: '\\ln', sin: '\\sin', cos: '\\cos', tan: '\\tan', exp: '', sqrt: '', sec: '\\sec', sinh: '\\sinh', cosh: '\\cosh', tanh: '\\tanh', atan: '\\tan^{-1}', asin: '\\sin^{-1}', acos: '\\cos^{-1}', abs: '' }[e.f];
        if (e.f === 'exp') s = 'e^{' + toTex(e.a) + '}';
        else if (e.f === 'sqrt') s = '\\sqrt{' + toTex(e.a) + '}';
        else if (e.f === 'abs') s = '\\left|' + toTex(e.a) + '\\right|';
        else s = (nm === undefined ? '\\operatorname{' + e.f + '}' : nm) + (e.a.k === 'var' || e.a.k === 'num' ? ' ' + toTex(e.a) : '\\left(' + toTex(e.a) + '\\right)');
        break;
      }
      case '^': s = (e.a.k === 'fn' && e.a.f !== 'exp' && e.a.f !== 'sqrt' ? '\\left(' + toTex(e.a) + '\\right)' : toTex(e.a, 5)) + '^{' + toTex(e.b) + '}'; break;
      case '*': {
        var A = toTex(e.a, 2), B = toTex(e.b, 2.1);
        s = (isN(e.a) && !isN(e.b)) ? A + B : A + ' \\cdot ' + B; break;
      }
      case '/': s = '\\frac{' + toTex(e.a) + '}{' + toTex(e.b) + '}'; p = 6; break;
      case '+': s = toTex(e.a, 1) + ' + ' + toTex(e.b, 1.1); break;
      case '-': s = toTex(e.a, 1) + ' - ' + toTex(e.b, 1.1); break;
    }
    return p < parentP ? '\\left(' + s + '\\right)' : s;
  }
  function make(src, v) {
    v = v || 'x';
    var ast = parse(src), f = compile(ast);
    var api = function (x) { var s = {}; s[v] = x; return f(s); };
    api.ast = ast; api.src = src; api.text = toText(ast); api.tex = toTex(ast);
    api.deriv = function () { var da = d(ast, v); var g = compile(da); var r = function (x) { var s = {}; s[v] = x; return g(s); }; r.ast = da; r.text = toText(da); r.tex = toTex(da); return r; };
    return api;
  }
  /* two-variable f(x, y) for ODEs */
  function make2(src) {
    var ast = parse(src), f = compile(ast);
    var api = function (x, y) { return f({ x: x, y: y, t: x }); };
    api.ast = ast; api.text = toText(ast); api.tex = toTex(ast);
    api.dx = function () { var g = compile(d(ast, 'x')); return function (x, y) { return g({ x: x, y: y }); }; };
    api.dy = function () { var g = compile(d(ast, 'y')); return function (x, y) { return g({ x: x, y: y }); }; };
    return api;
  }
  G.Expr = { make: make, make2: make2, parse: parse };
})(typeof window !== 'undefined' ? window : globalThis);
