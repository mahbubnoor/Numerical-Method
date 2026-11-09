/* Exact number formatting shared by MiniPy and MiniC.
   Rounds from the exact binary value of a double (round-half-even on exact ties),
   which is what CPython's format() and glibc's printf() do. */
(function (G) {
  'use strict';
  var buf = new DataView(new ArrayBuffer(8));
  /* x (finite, non-zero) = M * 2^E exactly, M a BigInt >= 0 */
  function decompose(x) {
    buf.setFloat64(0, Math.abs(x));
    var hi = buf.getUint32(0), lo = buf.getUint32(4);
    var ex = (hi >>> 20) & 0x7ff;
    var man = (BigInt(hi & 0xfffff) << 32n) | BigInt(lo);
    if (ex === 0) return { M: man, E: -1074 };
    return { M: man | (1n << 52n), E: ex - 1075 };
  }
  var P10 = [1n];
  function p10(n) { while (P10.length <= n) P10.push(P10[P10.length - 1] * 10n); return P10[n]; }
  /* round num/den (BigInt, positive) to an integer, half to even */
  function rdiv(num, den) {
    var q = num / den, r = num % den, t = 2n * r;
    if (t > den || (t === den && (q & 1n) === 1n)) q += 1n;
    return q;
  }
  /* digits of |x| scaled by 10^p, rounded: returns BigInt */
  function scaledInt(x, p) {
    var d = decompose(x), num = d.M, den = 1n;
    if (d.E >= 0) num = num << BigInt(d.E); else den = 1n << BigInt(-d.E);
    if (p >= 0) num *= p10(p); else den *= p10(-p);
    return rdiv(num, den);
  }
  function special(x, upper) {
    if (x !== x) return upper ? 'NAN' : 'nan';
    return (x < 0 ? '-' : '') + (upper ? 'INF' : 'inf');
  }
  /* fixed notation, p digits after the point, no sign */
  function fixedAbs(x, p) {
    if (x === 0) return p > 0 ? '0.' + '0'.repeat(p) : '0';
    var s = scaledInt(x, p).toString();
    if (p === 0) return s;
    while (s.length <= p) s = '0' + s;
    return s.slice(0, s.length - p) + '.' + s.slice(s.length - p);
  }
  /* scientific: returns {m: 'd.ddd', e: int} for |x| with p digits after point */
  function sciParts(x, p) {
    if (x === 0) return { m: p > 0 ? '0.' + '0'.repeat(p) : '0', e: 0 };
    var ax = Math.abs(x);
    var k = Math.floor(Math.log10(ax));
    if (!isFinite(k)) k = -324;
    for (var tries = 0; tries < 3; tries++) {
      var q = scaledInt(ax, p - k);               // ~ ax * 10^(p-k), should have p+1 digits
      var s = q.toString();
      if (s.length > p + 1) { k += 1; continue; }
      if (s.length < p + 1) { k -= 1; continue; }
      return { m: p > 0 ? s[0] + '.' + s.slice(1) : s, e: k };
    }
    var s2 = scaledInt(ax, p - k).toString();
    return { m: p > 0 ? s2[0] + '.' + s2.slice(1, p + 1) : s2[0], e: k + (s2.length - p - 1) };
  }
  function expStr(e, upper) {
    var a = Math.abs(e), s = (a < 10 ? '0' : '') + a;
    return (upper ? 'E' : 'e') + (e < 0 ? '-' : '+') + s;
  }
  function sciAbs(x, p, upper) { var r = sciParts(x, p); return r.m + expStr(r.e, upper); }
  function stripZeros(s) {
    var i = s.search(/[eE]/), mant = i < 0 ? s : s.slice(0, i), tail = i < 0 ? '' : s.slice(i);
    if (mant.indexOf('.') >= 0) mant = mant.replace(/0+$/, '').replace(/\.$/, '');
    return mant + tail;
  }
  /* %g / 'g' : precision P significant digits */
  function genAbs(x, P, upper, alt) {
    if (P === 0) P = 1;
    var X = x === 0 ? 0 : sciParts(x, P - 1).e, s;
    if (X >= -4 && X < P) s = fixedAbs(x, P - 1 - X); else s = sciAbs(x, P - 1, upper);
    if (!alt) s = stripZeros(s);
    else if (s.indexOf('.') < 0) s = s.replace(/^(\d+)/, '$1.');
    return s;
  }
  /* Python repr(float): shortest round-trip digits */
  function pyRepr(x) {
    if (!isFinite(x)) return special(x);
    if (x === 0) return (1 / x < 0) ? '-0.0' : '0.0';
    var t = Math.abs(x).toExponential();             // shortest unique digits
    var m = t.split('e'), digs = m[0].replace('.', ''), e = parseInt(m[1], 10);
    var sign = x < 0 ? '-' : '', s;
    if (e >= -5 + 1 && e < 16) {                     // -4 <= e < 16 : fixed
      if (e >= 0) {
        if (digs.length <= e + 1) s = digs + '0'.repeat(e + 1 - digs.length) + '.0';
        else s = digs.slice(0, e + 1) + '.' + digs.slice(e + 1);
      } else s = '0.' + '0'.repeat(-e - 1) + digs;
    } else {
      s = digs[0] + (digs.length > 1 ? '.' + digs.slice(1) : '') + expStr(e);
    }
    return sign + s;
  }
  function groupInt(s, sep) {   // s digits only
    var out = '';
    for (var i = 0; i < s.length; i++) { if (i && (s.length - i) % 3 === 0) out += sep; out += s[i]; }
    return out;
  }
  function pad(body, sign, width, align, fill, zero) {
    var len = body.length + sign.length;
    if (width <= len) return sign + body;
    var n = width - len;
    if (zero) return sign + '0'.repeat(n) + body;
    if (align === '<') return sign + body + fill.repeat(n);
    if (align === '^') { var l = Math.floor(n / 2); return fill.repeat(l) + sign + body + fill.repeat(n - l); }
    if (align === '=') return sign + fill.repeat(n) + body;
    return fill.repeat(n) + sign + body;
  }
  /* C printf with JS argument list (each {v:number|string, t:'int'|'double'|'str'|'char'}) */
  function cFormat(fmt, args, warn) {
    var out = '', ai = 0, re = /%([-+ #0]*)(\*|\d+)?(?:\.(\*|\d*))?(hh|h|ll|l|L|z|j|t)?([diouxXfFeEgGcsp%])/g, last = 0, m;
    while ((m = re.exec(fmt))) {
      out += fmt.slice(last, m.index); last = re.lastIndex;
      var flags = m[1], conv = m[5];
      if (conv === '%') { out += '%'; continue; }
      var width = m[2] === '*' ? Number(args[ai++].v) : (m[2] ? parseInt(m[2], 10) : 0);
      var prec = m[3] === undefined ? -1 : (m[3] === '*' ? Number(args[ai++].v) : (m[3] === '' ? 0 : parseInt(m[3], 10)));
      var a = args[ai++];
      if (!a) { out += ''; if (warn) warn('printf: too few arguments for the format'); continue; }
      var left = flags.indexOf('-') >= 0, plus = flags.indexOf('+') >= 0, space = flags.indexOf(' ') >= 0,
          alt = flags.indexOf('#') >= 0, zero = flags.indexOf('0') >= 0 && !left;
      var v = a.v, body, sign = '';
      if ('diouxX'.indexOf(conv) >= 0) {
        if (a.t === 'double' || a.t === 'float') { if (warn) warn("format '%" + conv + "' expects an int, but the argument is " + a.t); }
        var iv = typeof v === 'bigint' ? v : BigInt(Math.trunc(Number(v)) || 0);
        if (conv === 'u' && iv < 0n) iv += 1n << 32n;
        if (iv < 0n && 'di'.indexOf(conv) >= 0) { sign = '-'; iv = -iv; } else if ('di'.indexOf(conv) >= 0) sign = plus ? '+' : (space ? ' ' : '');
        if (iv < 0n) iv += 1n << 32n;
        body = conv === 'x' ? iv.toString(16) : conv === 'X' ? iv.toString(16).toUpperCase() : conv === 'o' ? iv.toString(8) : iv.toString();
        if (prec >= 0) { zero = false; while (body.length < prec) body = '0' + body; if (prec === 0 && iv === 0n) body = ''; }
        if (alt && conv === 'x' && iv !== 0n) body = '0x' + body;
      } else if ('fFeEgG'.indexOf(conv) >= 0) {
        if (a.t === 'int' || a.t === 'char' || a.t === 'long') { if (warn) warn("format '%" + conv + "' expects a double, but the argument is int (real C prints garbage here)"); }
        var x = Number(v), up = conv === conv.toUpperCase();
        if (prec < 0) prec = 6;
        if (x < 0 || (x === 0 && 1 / x < 0)) sign = '-'; else sign = plus ? '+' : (space ? ' ' : '');
        if (!isFinite(x)) { body = special(Math.abs(x), up).replace('-', ''); zero = false; }
        else if (conv === 'f' || conv === 'F') { body = fixedAbs(x, prec); if (alt && prec === 0) body += '.'; }
        else if (conv === 'e' || conv === 'E') body = sciAbs(x, prec, up);
        else body = genAbs(x, prec, up, alt);
      } else if (conv === 'c') { body = typeof v === 'string' ? v : String.fromCharCode(Number(v)); zero = false; }
      else if (conv === 's') { body = String(v); if (prec >= 0) body = body.slice(0, prec); zero = false; }
      else if (conv === 'p') { body = '0x7ffc0000'; }
      out += left ? sign + body + ' '.repeat(Math.max(0, width - body.length - sign.length)) : pad(body, sign, width, '>', ' ', zero);
    }
    return out + fmt.slice(last);
  }
  /* Python format-spec mini language. kind: 'int' (BigInt), 'float', 'str', 'bool' */
  function pyFormat(val, spec, kind, strFn) {
    var m = /^(?:(.)?([<>=^]))?([-+ ])?(z)?(#)?(0)?(\d+)?([,_])?(?:\.(\d+))?([bcdeEfFgGnosxX%])?$/.exec(spec);
    if (!m) throw new Error('ValueError: Invalid format specifier \'' + spec + '\'');
    var fill = m[1] || ' ', align = m[2], sgn = m[3] || '-', alt = !!m[5], zero = !!m[6] && !m[2],
        width = m[7] ? parseInt(m[7], 10) : 0, grp = m[8], prec = m[9] !== undefined ? parseInt(m[9], 10) : -1, type = m[10] || '';
    if (m[6] && !m[2]) { fill = '0'; align = '='; zero = false; }
    if (kind === 'bool' && type === '') { kind = 'str'; val = val ? 'True' : 'False'; }
    if (kind === 'bool') { kind = 'int'; val = val ? 1n : 0n; }
    if (kind === 'str' || (kind !== 'int' && kind !== 'float')) {
      var s = kind === 'str' ? val : strFn(val);
      if (type && type !== 's') throw new Error("ValueError: Unknown format code '" + type + "' for object of type 'str'");
      if (prec >= 0) s = s.slice(0, prec);
      return pad(s, '', width, align || '<', fill, false);
    }
    var sign = '', body;
    if (kind === 'int' && 'eEfFgG%'.indexOf(type) >= 0 && type) { kind = 'float'; val = Number(val); }
    if (kind === 'int') {
      if (type === 'c') return pad(String.fromCharCode(Number(val)), '', width, align || '<', fill, false);
      if (prec >= 0) throw new Error('ValueError: Precision not allowed in integer format specifier');
      var iv = val; if (iv < 0n) { sign = '-'; iv = -iv; } else if (sgn === '+') sign = '+'; else if (sgn === ' ') sign = ' ';
      body = type === 'x' ? iv.toString(16) : type === 'X' ? iv.toString(16).toUpperCase() : type === 'b' ? iv.toString(2) : type === 'o' ? iv.toString(8) : iv.toString();
      if (alt && type === 'x') sign += '0x'; if (alt && type === 'b') sign += '0b';
      if (grp && (type === '' || type === 'd' || type === 'n')) body = groupInt(body, grp);
    } else {
      var x = Number(val);
      if (x < 0 || (x === 0 && 1 / x < 0)) sign = '-'; else if (sgn === '+') sign = '+'; else if (sgn === ' ') sign = ' ';
      var ax = Math.abs(x);
      if (!isFinite(x)) body = (x !== x) ? 'nan' : 'inf';
      else if (type === 'f' || type === 'F') body = fixedAbs(ax, prec < 0 ? 6 : prec);
      else if (type === 'e' || type === 'E') body = sciAbs(ax, prec < 0 ? 6 : prec, type === 'E');
      else if (type === '%') body = isFinite(ax * 100) ? fixedAbs(ax * 100, prec < 0 ? 6 : prec) + '%' : 'inf%';
      else if (type === 'g' || type === 'G' || type === 'n') body = genAbs(ax, prec < 0 ? 6 : prec, type === 'G', alt);
      else { // no type
        if (prec < 0) body = pyRepr(ax);
        else {
          var P = prec || 1, X = ax === 0 ? 0 : sciParts(ax, P - 1).e;
          if (X >= -4 && X < P - 1) { body = stripZeros(fixedAbs(ax, P - 1 - X)); if (body.indexOf('.') < 0) body += '.0'; }
          else body = stripZeros(sciAbs(ax, P - 1, false));
        }
      }
      if (type === 'F' || type === 'E' || type === 'G') body = body.toUpperCase();
      if (grp && isFinite(x)) { var parts = body.split('.'); if (/^\d+$/.test(parts[0])) { parts[0] = groupInt(parts[0], grp); body = parts.join('.'); } }
    }
    if (align === '=' || (!align && fill === '0')) return pad(body, sign, width, '=', fill, false);
    return pad(body, sign, width, align || '>', fill, false);
  }
  function roundHalfEven(x, nd) {   // Python round(x, nd) for floats
    if (!isFinite(x)) return x;
    if (nd >= 0) { var s = fixedAbs(Math.abs(x), nd); var r = parseFloat(s); return x < 0 ? -r : r; }
    var f = Math.pow(10, -nd); var q = Number(scaledInt(Math.abs(x), nd)); var r2 = q * f; return x < 0 ? -r2 : r2;
  }
  function roundInt(x) {  // Python round(x) -> BigInt
    var s = fixedAbs(Math.abs(x), 0); var b = BigInt(s); return x < 0 ? -b : b;
  }
  G.NumFmt = { cFormat: cFormat, pyFormat: pyFormat, pyRepr: pyRepr, fixed: fixedAbs, sci: sciAbs, gen: genAbs,
    roundHalfEven: roundHalfEven, roundInt: roundInt };
})(typeof window !== 'undefined' ? window : globalThis);
