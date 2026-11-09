/* MiniC: a small C interpreter for teaching numerical methods in the browser.
   Subset: int/long/char/float/double, 1-D and 2-D arrays, functions (arrays passed by reference),
   if/else, for, while, do-while, switch, break/continue, #define (object and function-like macros),
   printf/scanf/puts, <math.h>. float variables are rounded to 32-bit like real C.
   Every course example is checked against gcc. */
(function (G) {
  'use strict';
  var NF = G.NumFmt;
  function CErr(kind, msg, line) { this.kind = kind; this.msg = msg; this.line = line; }
  function cerr(msg, line) { throw new CErr('error', msg, line); }
  function rerr(msg, line) { throw new CErr('runtime', msg, line); }

  /* ------------------------------------------------------------------ lexer + preprocessor */
  var KEYW = { 'int': 1, 'long': 1, 'short': 1, 'unsigned': 1, 'signed': 1, 'char': 1, 'float': 1, 'double': 1, 'void': 1, 'const': 1, 'static': 1,
    'if': 1, 'else': 1, 'for': 1, 'while': 1, 'do': 1, 'return': 1, 'break': 1, 'continue': 1, 'switch': 1, 'case': 1, 'default': 1, 'sizeof': 1,
    'struct': 1, 'typedef': 1, 'goto': 1, 'register': 1, 'auto': 1, 'extern': 1, 'volatile': 1, 'inline': 1, 'bool': 1, '_Bool': 1 };
  var COPS = ['<<=', '>>=', '...', '->', '++', '--', '<<', '>>', '<=', '>=', '==', '!=', '&&', '||', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=',
    '+', '-', '*', '/', '%', '<', '>', '=', '!', '~', '&', '|', '^', '?', ':', ';', ',', '.', '(', ')', '[', ']', '{', '}'];
  function lexLine(src, line, out) {
    var i = 0, n = src.length;
    while (i < n) {
      var c = src[i];
      if (c === ' ' || c === '\t' || c === '\r') { i++; continue; }
      if (c === '"' || c === "'") {
        var q = c, j = i + 1, s = '';
        while (j < n && src[j] !== q) {
          if (src[j] === '\\') { var e = src[j + 1]; j += 2; s += e === 'n' ? '\n' : e === 't' ? '\t' : e === '0' ? '\0' : e === '\\' ? '\\' : e === '"' ? '"' : e === "'" ? "'" : e === 'r' ? '\r' : e === 'a' ? '\x07' : e === 'b' ? '\b' : '\\' + e; continue; }
          s += src[j++];
        }
        if (j >= n) cerr('missing terminating ' + q + ' character', line);
        out.push(q === '"' ? { t: 'str', v: s, line: line } : { t: 'num', v: s.charCodeAt(0) || 0, ty: 'char', line: line });
        i = j + 1; continue;
      }
      if (/[0-9]/.test(c) || (c === '.' && /[0-9]/.test(src[i + 1]))) {
        var m = /^(0[xX][0-9a-fA-F]+|(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)([fFlLuU]*)/.exec(src.slice(i));
        var txt = m[1], suf = m[2].toLowerCase(), isF = /[.eE]/.test(txt) && !/^0[xX]/.test(txt);
        var ty = isF ? (suf.indexOf('f') >= 0 ? 'float' : 'double') : (suf.indexOf('l') >= 0 ? 'long' : 'int');
        var v = isF ? parseFloat(txt) : (/^0[xX]/.test(txt) ? parseInt(txt, 16) : (/^0\d/.test(txt) ? parseInt(txt, 8) : parseInt(txt, 10)));
        if (ty === 'int' && v > 2147483647) ty = 'long';
        if (ty === 'float') v = Math.fround(v);
        out.push({ t: 'num', v: v, ty: ty, line: line }); i += m[0].length; continue;
      }
      if (/[A-Za-z_]/.test(c)) {
        var mm = /^[A-Za-z_]\w*/.exec(src.slice(i));
        out.push({ t: KEYW[mm[0]] ? 'kw' : 'id', v: mm[0], line: line }); i += mm[0].length; continue;
      }
      var op = null;
      for (var k = 0; k < COPS.length; k++) if (src.substr(i, COPS[k].length) === COPS[k]) { op = COPS[k]; break; }
      if (!op) cerr("stray '" + c + "' in program", line);
      out.push({ t: 'op', v: op, line: line }); i += op.length;
    }
  }
  function stripComments(src) {
    var out = '', i = 0, n = src.length, inS = null;
    while (i < n) {
      var c = src[i];
      if (inS) { out += c; if (c === '\\') { out += src[i + 1] || ''; i += 2; continue; } if (c === inS || c === '\n') inS = null; i++; continue; }
      if (c === '"' || c === "'") { inS = c; out += c; i++; continue; }
      if (c === '/' && src[i + 1] === '/') { while (i < n && src[i] !== '\n') i++; continue; }
      if (c === '/' && src[i + 1] === '*') { i += 2; while (i < n && !(src[i] === '*' && src[i + 1] === '/')) { if (src[i] === '\n') out += '\n'; i++; } i += 2; continue; }
      out += c; i++;
    }
    return out;
  }
  function preprocess(src) {
    src = stripComments(src.replace(/\r\n?/g, '\n')).replace(/\\\n/g, ' ');
    var lines = src.split('\n'), macros = {}, toks = [];
    var predefined = { M_PI: '3.14159265358979323846', M_E: '2.7182818284590452354', M_SQRT2: '1.41421356237309504880', INFINITY: '(1.0/0.0)', NAN: '(0.0/0.0)',
      DBL_EPSILON: '2.2204460492503131e-16', FLT_EPSILON: '1.1920928955078125e-07F', DBL_MAX: '1.7976931348623157e+308', FLT_MAX: '3.40282346638528859811704183484516925e+38F',
      DBL_MIN: '2.2250738585072014e-308', FLT_MIN: '1.17549435082228750796873653722224568e-38F', INT_MAX: '2147483647', INT_MIN: '(-2147483647-1)', RAND_MAX: '2147483647',
      NULL: '0', true: '1', false: '0', EXIT_SUCCESS: '0', EXIT_FAILURE: '1', DBL_DIG: '15', FLT_DIG: '6' };
    for (var pn in predefined) { var pt = []; lexLine(predefined[pn], 0, pt); macros[pn] = { body: pt }; }
    for (var li = 0; li < lines.length; li++) {
      var L = lines[li], ln = li + 1, t = L.trim();
      if (t[0] === '#') {
        var m = /^#\s*(\w+)\s*(.*)$/.exec(t);
        if (!m) continue;
        if (m[1] === 'define') {
          var dm = /^([A-Za-z_]\w*)(\(([^)]*)\))?\s*(.*)$/.exec(m[2]);
          if (!dm) cerr('macro names must be identifiers', ln);
          var body = []; lexLine(dm[4], ln, body);
          macros[dm[1]] = { params: dm[2] ? dm[3].split(',').map(function (s) { return s.trim(); }).filter(Boolean) : null, body: body };
        } else if (m[1] === 'undef') delete macros[m[2].trim()];
        continue;   // #include and others ignored
      }
      var lt = []; lexLine(L, ln, lt);
      toks.push.apply(toks, lt);
    }
    // macro expansion
    function expand(list, hide) {
      var out = [];
      for (var i = 0; i < list.length; i++) {
        var tk = list[i], mac = tk.t === 'id' && macros[tk.v];
        if (!mac || hide[tk.v]) { out.push(tk); continue; }
        var nh = Object.assign({}, hide); nh[tk.v] = 1;
        if (!mac.params) { out.push.apply(out, expand(mac.body.map(function (b) { return Object.assign({}, b, { line: tk.line }); }), nh)); continue; }
        if (!(list[i + 1] && list[i + 1].v === '(')) { out.push(tk); continue; }
        var args = [[]], depth = 0, j = i + 2;
        for (; j < list.length; j++) {
          var a = list[j];
          if (a.v === '(' && a.t === 'op') depth++;
          if (a.v === ')' && a.t === 'op') { if (depth === 0) break; depth--; }
          if (a.v === ',' && a.t === 'op' && depth === 0) { args.push([]); continue; }
          args[args.length - 1].push(a);
        }
        if (j >= list.length) cerr("unterminated argument list invoking macro '" + tk.v + "'", tk.line);
        if (mac.params.length === 0 && args.length === 1 && args[0].length === 0) args = [];
        if (args.length !== mac.params.length) cerr("macro '" + tk.v + "' requires " + mac.params.length + ' arguments, but ' + args.length + ' given', tk.line);
        var exArgs = args.map(function (a) { return expand(a, hide); });
        var sub = [];
        mac.body.forEach(function (b) {
          var pi = b.t === 'id' ? mac.params.indexOf(b.v) : -1;
          if (pi >= 0) sub.push.apply(sub, exArgs[pi].map(function (x) { return Object.assign({}, x, { line: tk.line }); }));
          else sub.push(Object.assign({}, b, { line: tk.line }));
        });
        out.push.apply(out, expand(sub, nh));
        i = j;
      }
      return out;
    }
    var ex = expand(toks, {});
    ex.push({ t: 'eof', v: '', line: lines.length });
    return ex;
  }

  /* ------------------------------------------------------------------ types */
  function isArith(t) { return typeof t === 'string' && t !== 'void' && t !== 'str'; }
  function isFloatT(t) { return t === 'float' || t === 'double'; }
  function rank(t) { return { char: 1, int: 2, long: 3, float: 4, double: 5 }[t] || 0; }
  function common(a, b) { if (a === 'double' || b === 'double') return 'double'; if (a === 'float' || b === 'float') return 'float'; if (a === 'long' || b === 'long') return 'long'; return 'int'; }
  function conv(v, t) {
    switch (t) {
      case 'double': return +v;
      case 'float': return Math.fround(v);
      case 'int': if (typeof v === 'number' && !isFinite(v)) return -2147483648; return (Math.trunc(v) | 0);
      case 'long': { if (!isFinite(v)) return -9223372036854775808; var x = Math.trunc(v); return x; }
      case 'char': return ((Math.trunc(v) << 24) >> 24);
      case 'bool': return v ? 1 : 0;
    }
    return v;
  }
  function typeStr(t) { if (t && t.arr) return t.arr + '[]'.repeat(t.dims.length); return t; }

  /* ------------------------------------------------------------------ parser (with static typing) */
  function Parser(toks) { this.toks = toks; this.p = 0; this.scopes = [{}]; this.funcs = {}; this.curFn = null; this.loopDepth = 0; this.switchDepth = 0; }
  var P = Parser.prototype;
  P.peek = function (o) { return this.toks[this.p + (o || 0)]; };
  P.next = function () { return this.toks[this.p++]; };
  P.is = function (v, o) { var t = this.toks[this.p + (o || 0)]; return t.v === v && (t.t === 'op' || t.t === 'kw'); };
  P.accept = function (v) { if (this.is(v)) { this.p++; return true; } return false; };
  P.expect = function (v, what) {
    if (!this.is(v)) {
      var t = this.peek(), prev = this.toks[this.p - 1];
      if (v === ';') cerr("expected ';' before '" + (t.v || 'end of input') + "'", prev ? prev.line : t.line);
      cerr("expected '" + v + "'" + (what ? ' ' + what : '') + " before '" + (t.v === '' ? 'end of input' : t.v) + "'", t.line);
    }
    return this.next();
  };
  P.line = function () { return this.peek().line; };
  P.push = function () { this.scopes.push({}); };
  P.pop = function () { this.scopes.pop(); };
  P.declare = function (name, type, line) {
    var s = this.scopes[this.scopes.length - 1];
    if (s[name] && this.scopes.length > 1) cerr("redeclaration of '" + name + "'", line);
    var info = { name: name, type: type, global: this.scopes.length === 1, id: name + '#' + (++Parser.uid) };
    s[name] = info; return info;
  };
  Parser.uid = 0;
  P.lookup = function (name, line) {
    for (var i = this.scopes.length - 1; i >= 0; i--) if (this.scopes[i][name]) return this.scopes[i][name];
    return null;
  };
  P.isTypeStart = function () {
    var t = this.peek();
    return t.t === 'kw' && /^(int|long|short|unsigned|signed|char|float|double|void|const|static|register|bool|_Bool|volatile|extern|inline|auto)$/.test(t.v);
  };
  P.baseType = function () {
    var words = [];
    while (this.isTypeStart()) words.push(this.next().v);
    var w = words.filter(function (x) { return !/^(const|static|register|volatile|extern|inline|auto|signed)$/.test(x); });
    if (this.is('struct')) cerr('structs are not supported in MiniC', this.line());
    if (w.indexOf('double') >= 0) return 'double';
    if (w.indexOf('float') >= 0) return 'float';
    if (w.indexOf('char') >= 0) return 'char';
    if (w.indexOf('void') >= 0) return 'void';
    if (w.indexOf('bool') >= 0 || w.indexOf('_Bool') >= 0) return 'int';
    if (w.filter(function (x) { return x === 'long'; }).length) return 'long';
    return 'int';
  };
  P.program = function () {
    var globals = [], funcs = {};
    while (this.peek().t !== 'eof') {
      if (this.accept(';')) continue;
      if (this.is('typedef')) cerr('typedef is not supported in MiniC', this.line());
      if (!this.isTypeStart()) {
        var t = this.peek();
        if (t.t === 'id' && this.is('(', 1)) cerr("return type of '" + t.v + "' is missing (write int " + t.v + "(...))", t.line);
        cerr("expected a declaration, found '" + t.v + "'", t.line);
      }
      var line = this.line(), bt = this.baseType(), ptr = 0;
      while (this.accept('*')) ptr++;
      var nameTok = this.next();
      if (nameTok.t !== 'id') cerr('expected identifier', nameTok.line);
      if (this.is('(')) {
        var fn = this.funcDef(bt, nameTok.v, line, ptr);
        if (fn.body) funcs[fn.name] = fn;
      } else {
        this.p--; while (this.toks[this.p - 1] && this.toks[this.p - 1].v === '*') this.p--;
        globals.push.apply(globals, this.declRest(bt, line));
      }
    }
    for (var k in this.funcs) if (!funcs[k] && this.funcs[k].used) cerr("undefined reference to '" + k + "'", this.funcs[k].line);
    if (!funcs.main) cerr("undefined reference to 'main' (every C program needs int main(void))", 1);
    return { globals: globals, funcs: funcs };
  };
  P.funcDef = function (ret, name, line, ptr) {
    if (ptr) cerr('functions returning pointers are not supported in MiniC', line);
    this.expect('(');
    var params = [];
    this.push();
    if (this.is('void') && this.is(')', 1)) { this.next(); }
    while (!this.is(')')) {
      var pl = this.line(), bt = this.baseType(), stars = 0;
      while (this.accept('*')) stars++;
      var pname = this.peek().t === 'id' ? this.next().v : '_p' + params.length, type = bt;
      if (this.is('[') || stars) {
        var dims = [];
        if (stars) for (var s = 0; s < stars; s++) dims.push(0);
        while (this.accept('[')) { dims.push(this.is(']') ? 0 : this.constExpr()); this.expect(']'); }
        type = { arr: bt, dims: dims };
      }
      params.push(this.declare(pname, type, pl));
      if (!this.accept(',')) break;
    }
    this.expect(')');
    var sig = { name: name, ret: ret, params: params.map(function (p) { return p.type; }), line: line, used: this.funcs[name] ? this.funcs[name].used : false };
    this.funcs[name] = sig;
    if (this.accept(';')) { this.pop(); return { name: name, body: null }; }
    var prevFn = this.curFn; this.curFn = sig;
    var body = this.block(true);
    this.curFn = prevFn;
    this.pop();
    return { name: name, ret: ret, params: params, body: body, line: line };
  };
  P.constExpr = function () {
    var e = this.assign();
    var v = constEval(e);
    if (v === null) cerr('array size must be a constant', e.line);
    return v;
  };
  function constEval(e) {
    if (e.k === 'num') return e.v;
    if (e.k === 'bin') { var a = constEval(e.a), b = constEval(e.b); if (a === null || b === null) return null;
      switch (e.op) { case '+': return a + b; case '-': return a - b; case '*': return a * b; case '/': return Math.trunc(a / b); } }
    if (e.k === 'cast') return constEval(e.e);
    return null;
  }
  P.declRest = function (bt, line) {
    var decls = [];
    do {
      var stars = 0; while (this.accept('*')) stars++;
      var nt = this.next();
      if (nt.t !== 'id') cerr("expected identifier before '" + nt.v + "'", nt.line);
      var dims = [];
      while (this.accept('[')) { dims.push(this.is(']') ? -1 : this.constExpr()); this.expect(']'); }
      if (stars && !dims.length) cerr('pointer variables are not supported in MiniC (use an array)', nt.line);
      var type = dims.length ? { arr: bt, dims: dims } : bt, init = null;
      if (bt === 'void' && !dims.length) cerr("variable '" + nt.v + "' declared void", nt.line);
      if (this.accept('=')) {
        if (this.is('{')) init = this.initList();
        else if (this.peek().t === 'str' && dims.length) { init = { k: 'strinit', v: this.next().v }; }
        else init = this.assign();
      }
      if (dims.length && dims[0] === -1) {
        if (init && init.k === 'list') dims[0] = init.items.length;
        else if (init && init.k === 'strinit') dims[0] = init.v.length + 1;
        else cerr("array size missing in '" + nt.v + "'", nt.line);
      }
      if (init && !dims.length && init.k !== 'list' && !isArith(init.type)) cerr('incompatible types in initialization of ' + bt, nt.line);
      var info = this.declare(nt.v, type, nt.line);
      decls.push({ k: 'decl', info: info, init: init, line: nt.line });
    } while (this.accept(','));
    this.expect(';');
    return decls;
  };
  P.initList = function () {
    var line = this.line(); this.expect('{');
    var items = [];
    while (!this.is('}')) { items.push(this.is('{') ? this.initList() : this.assign()); if (!this.accept(',')) break; }
    this.expect('}');
    return { k: 'list', items: items, line: line };
  };
  P.block = function (noScope) {
    var line = this.line(); this.expect('{');
    if (!noScope) this.push();
    var body = [];
    while (!this.is('}')) {
      if (this.peek().t === 'eof') cerr("expected '}' at end of input", this.peek().line);
      body.push.apply(body, this.stmt());
    }
    this.expect('}');
    if (!noScope) this.pop();
    return { k: 'block', body: body, line: line };
  };
  P.stmt = function () {
    var t = this.peek(), line = t.line;
    if (this.isTypeStart()) { var bt = this.baseType(); return this.declRest(bt, line); }
    if (t.t === 'op' && t.v === '{') return [this.block()];
    if (t.t === 'op' && t.v === ';') { this.next(); return [{ k: 'empty', line: line }]; }
    if (t.t === 'kw') {
      switch (t.v) {
        case 'if': { this.next(); this.expect('('); var c = this.expr(); this.expect(')'); var th = this.sub(), el = null; if (this.accept('else')) el = this.sub(); return [{ k: 'if', c: c, th: th, el: el, line: line }]; }
        case 'while': { this.next(); this.expect('('); var wc = this.expr(); this.expect(')'); this.loopDepth++; var wb = this.sub(); this.loopDepth--; return [{ k: 'while', c: wc, body: wb, line: line }]; }
        case 'do': { this.next(); this.loopDepth++; var db = this.sub(); this.loopDepth--; this.expect('while'); this.expect('('); var dc = this.expr(); this.expect(')'); this.expect(';'); return [{ k: 'do', c: dc, body: db, line: line }]; }
        case 'for': {
          this.next(); this.expect('('); this.push();
          var init = null;
          if (this.isTypeStart()) { var fbt = this.baseType(); init = { k: 'block', body: this.declRest(fbt, line), line: line, noScope: true }; }
          else { if (!this.is(';')) init = { k: 'expr', e: this.expr(), line: line }; this.expect(';'); }
          var cond = this.is(';') ? null : this.expr(); this.expect(';');
          var step = this.is(')') ? null : this.expr(); this.expect(')');
          this.loopDepth++; var fb = this.sub(); this.loopDepth--;
          this.pop();
          return [{ k: 'for', init: init, c: cond, step: step, body: fb, line: line }];
        }
        case 'return': {
          this.next(); var v = this.is(';') ? null : this.expr(); this.expect(';');
          if (v && this.curFn.ret === 'void') cerr("'return' with a value, in function returning void", line);
          if (v && !isArith(v.type)) cerr('incompatible types when returning ' + typeStr(v.type), line);
          return [{ k: 'return', e: v, ret: this.curFn.ret, line: line }];
        }
        case 'break': this.next(); this.expect(';'); if (!this.loopDepth && !this.switchDepth) cerr('break statement not within loop or switch', line); return [{ k: 'break', line: line }];
        case 'continue': this.next(); this.expect(';'); if (!this.loopDepth) cerr('continue statement not within a loop', line); return [{ k: 'continue', line: line }];
        case 'switch': {
          this.next(); this.expect('('); var sv = this.expr(); this.expect(')'); this.expect('{'); this.push(); this.switchDepth++;
          var cases = [], cur = null;
          while (!this.is('}')) {
            if (this.accept('case')) { var cv = this.constExpr(); this.expect(':'); cur = { v: cv, body: [] }; cases.push(cur); continue; }
            if (this.accept('default')) { this.expect(':'); cur = { v: 'default', body: [] }; cases.push(cur); continue; }
            if (!cur) cerr("statement before first 'case' in switch", this.line());
            cur.body.push.apply(cur.body, this.stmt());
          }
          this.expect('}'); this.pop(); this.switchDepth--;
          return [{ k: 'switch', e: sv, cases: cases, line: line }];
        }
        case 'goto': cerr('goto is not supported in MiniC', line);
      }
    }
    var e = this.expr(); this.expect(';');
    return [{ k: 'expr', e: e, line: line }];
  };
  P.sub = function () { var s = this.stmt(); return s.length === 1 ? s[0] : { k: 'block', body: s, line: s.length ? s[0].line : 0 }; };
  P.expr = function () {
    var e = this.assign();
    while (this.is(',')) { var l = this.next().line; var b = this.assign(); e = { k: 'comma', a: e, b: b, type: b.type, line: l }; }
    return e;
  };
  function isLval(e) { return e.k === 'var' || e.k === 'idx'; }
  P.assign = function () {
    var e = this.cond(), t = this.peek();
    if (t.t === 'op' && /^(=|\+=|-=|\*=|\/=|%=|<<=|>>=|&=|\|=|\^=)$/.test(t.v)) {
      this.next();
      if (!isLval(e)) cerr('lvalue required as left operand of assignment', t.line);
      if (e.type && e.type.arr) cerr('assignment to expression with array type (copy arrays element by element)', t.line);
      var r = this.assign();
      if (!isArith(r.type)) cerr('incompatible types when assigning to type ' + typeStr(e.type) + ' from ' + typeStr(r.type), t.line);
      if (t.v === '%=' && (isFloatT(e.type) || isFloatT(r.type))) cerr("invalid operands to binary % (have '" + e.type + "' and '" + r.type + "')", t.line);
      return { k: 'assign', op: t.v, l: e, r: r, type: e.type, line: t.line };
    }
    return e;
  };
  P.cond = function () {
    var c = this.binary(0);
    if (this.is('?')) {
      var l = this.next().line, a = this.expr(); this.expect(':'); var b = this.cond();
      return { k: 'cond', c: c, a: a, b: b, type: (isArith(a.type) && isArith(b.type)) ? common(a.type, b.type) : a.type, line: l };
    }
    return c;
  };
  var BIN = [['||'], ['&&'], ['|'], ['^'], ['&'], ['==', '!='], ['<', '>', '<=', '>='], ['<<', '>>'], ['+', '-'], ['*', '/', '%']];
  P.binary = function (lv) {
    if (lv >= BIN.length) return this.unary();
    var e = this.binary(lv + 1);
    while (this.peek().t === 'op' && BIN[lv].indexOf(this.peek().v) >= 0) {
      var t = this.next(), b = this.binary(lv + 1), op = t.v;
      if (!isArith(e.type) || !isArith(b.type)) cerr("invalid operands to binary " + op + " (have '" + typeStr(e.type) + "' and '" + typeStr(b.type) + "')", t.line);
      var ty;
      if (/^(==|!=|<|>|<=|>=|&&|\|\|)$/.test(op)) ty = 'int';
      else {
        ty = common(e.type, b.type);
        if (/^(%|<<|>>|&|\||\^)$/.test(op) && isFloatT(ty)) cerr("invalid operands to binary " + op + " (have '" + e.type + "' and '" + b.type + "')", t.line);
      }
      e = { k: 'bin', op: op, a: e, b: b, type: ty, ct: common(e.type, b.type), line: t.line };
    }
    return e;
  };
  P.unary = function () {
    var t = this.peek(), line = t.line;
    if (t.t === 'op') {
      if (t.v === '++' || t.v === '--') { this.next(); var x = this.unary(); if (!isLval(x)) cerr('lvalue required as increment operand', line); return { k: 'pre', op: t.v, e: x, type: x.type, line: line }; }
      if (t.v === '-' || t.v === '+' || t.v === '!' || t.v === '~') { this.next(); var u = this.unary(); if (!isArith(u.type)) cerr('wrong type argument to unary ' + t.v, line);
        var ut = t.v === '!' ? 'int' : (u.type === 'char' ? 'int' : u.type); return { k: 'un', op: t.v, e: u, type: ut, line: line }; }
      if (t.v === '&') { this.next(); var a = this.unary(); if (!isLval(a)) cerr('lvalue required as unary & operand', line); return { k: 'addr', e: a, type: 'ptr', line: line }; }
      if (t.v === '*') { this.next(); var d = this.unary(); if (d.type && d.type.arr) return this.makeIdx(d, { k: 'num', v: 0, type: 'int', line: line }, line); cerr('pointers are not supported in MiniC (use array indexing a[i])', line); }
      if (t.v === '(' && this.peek(1).t === 'kw' && /^(int|long|short|unsigned|signed|char|float|double|const|void)$/.test(this.peek(1).v)) {
        this.next(); var ct = this.baseType(); while (this.accept('*')) cerr('pointer casts are not supported in MiniC', line); this.expect(')');
        var ce = this.unary(); if (ct === 'void') return { k: 'cast', to: 'void', e: ce, type: 'void', line: line };
        if (!isArith(ce.type)) cerr('cannot cast ' + typeStr(ce.type) + ' to ' + ct, line);
        return { k: 'cast', to: ct, e: ce, type: ct, line: line };
      }
    }
    if (t.t === 'kw' && t.v === 'sizeof') {
      this.next(); var sz;
      if (this.is('(') && this.peek(1).t === 'kw' && /^(int|long|char|float|double|short|unsigned)$/.test(this.peek(1).v)) { this.next(); var st = this.baseType(); this.expect(')'); sz = { char: 1, int: 4, long: 8, float: 4, double: 8 }[st]; }
      else { var se = this.unary(); sz = sizeOf(se.type); }
      return { k: 'num', v: sz, type: 'long', line: line };
    }
    return this.postfix();
  };
  function sizeOf(t) {
    if (t && t.arr) { var s = { char: 1, int: 4, long: 8, float: 4, double: 8 }[t.arr]; t.dims.forEach(function (d) { s *= (d || 1); }); if (t.dims[0] === 0) return 8; return s; }
    return { char: 1, int: 4, long: 8, float: 4, double: 8 }[t] || 8;
  }
  P.makeIdx = function (a, i, line) {
    if (!a.type || !a.type.arr) cerr('subscripted value is neither array nor pointer', line);
    if (!isArith(i.type) || isFloatT(i.type)) cerr('array subscript is not an integer', line);
    var rest = a.type.dims.slice(1);
    return { k: 'idx', a: a, i: i, type: rest.length ? { arr: a.type.arr, dims: rest } : a.type.arr, line: line };
  };
  P.postfix = function () {
    var e = this.primary();
    while (true) {
      var t = this.peek();
      if (t.t === 'op' && t.v === '[') { this.next(); var i = this.expr(); this.expect(']'); e = this.makeIdx(e, i, t.line); }
      else if (t.t === 'op' && (t.v === '++' || t.v === '--')) { this.next(); if (!isLval(e)) cerr('lvalue required as increment operand', t.line); e = { k: 'post', op: t.v, e: e, type: e.type, line: t.line }; }
      else break;
    }
    return e;
  };
  var LIB = {
    sqrt: 1, pow: 2, exp: 1, log: 1, log10: 1, log2: 1, log1p: 1, expm1: 1, sin: 1, cos: 1, tan: 1, asin: 1, acos: 1, atan: 1, atan2: 2, sinh: 1, cosh: 1, tanh: 1,
    fabs: 1, floor: 1, ceil: 1, round: 1, trunc: 1, fmod: 2, fmax: 2, fmin: 2, hypot: 2, cbrt: 1, sqrtf: 1, fabsf: 1, expf: 1, logf: 1, sinf: 1, cosf: 1, powf: 2, abs: 1, labs: 1, isnan: 1, isinf: 1
  };
  P.primary = function () {
    var t = this.next(), line = t.line;
    if (t.t === 'num') return { k: 'num', v: t.v, type: t.ty === 'char' ? 'int' : t.ty, line: line };
    if (t.t === 'str') { var s = t.v; while (this.peek().t === 'str') s += this.next().v; return { k: 'str', v: s, type: 'str', line: line }; }
    if (t.t === 'op' && t.v === '(') { var e = this.expr(); this.expect(')'); return e; }
    if (t.t === 'id') {
      if (this.is('(')) {
        this.next(); var args = [];
        while (!this.is(')')) { args.push(this.assign()); if (!this.accept(',')) break; }
        this.expect(')');
        var name = t.v;
        if (name === 'printf' || name === 'scanf' || name === 'puts' || name === 'putchar' || name === 'getchar' || name === 'rand' || name === 'srand' || name === 'exit' || name === 'system' || name === 'fflush' || name === 'time') {
          if ((name === 'printf' || name === 'scanf') && (!args.length || args[0].type !== 'str')) cerr('format string must be a string literal in MiniC', line);
          return { k: 'lib', name: name, args: args, type: name === 'getchar' || name === 'rand' || name === 'printf' || name === 'scanf' ? 'int' : 'void', line: line };
        }
        if (LIB[name] && !this.funcs[name]) {
          if (args.length !== LIB[name]) cerr("too " + (args.length < LIB[name] ? 'few' : 'many') + " arguments to function '" + name + "'", line);
          args.forEach(function (a) { if (!isArith(a.type)) cerr("incompatible type for argument of '" + name + "'", line); });
          var rt = /f$/.test(name) && name !== 'erf' ? 'float' : (name === 'abs' || name === 'isnan' || name === 'isinf' ? 'int' : name === 'labs' ? 'long' : 'double');
          return { k: 'math', name: name, args: args, type: rt, line: line };
        }
        var f = this.funcs[name];
        if (!f) cerr("implicit declaration of function '" + name + "' (define it above main, or add a prototype)", line);
        f.used = true;
        if (args.length !== f.params.length) cerr("too " + (args.length < f.params.length ? 'few' : 'many') + " arguments to function '" + name + "' (expects " + f.params.length + ')', line);
        args.forEach(function (a, i) {
          var pt = f.params[i];
          if (pt && pt.arr) { if (!a.type || !a.type.arr) cerr("argument " + (i + 1) + " of '" + name + "' must be an array", line); if (a.type.arr !== pt.arr) cerr("argument " + (i + 1) + " of '" + name + "': array of " + a.type.arr + ' passed where ' + pt.arr + ' array expected', line); }
          else if (!isArith(a.type)) cerr("argument " + (i + 1) + " of '" + name + "': cannot pass " + typeStr(a.type) + ' as ' + pt, line);
        });
        return { k: 'call', name: name, args: args, type: f.ret, ptypes: f.params, line: line };
      }
      var info = this.lookup(t.v);
      if (!info) cerr("'" + t.v + "' undeclared (first use in this function)", line);
      return { k: 'var', info: info, type: info.type, line: line };
    }
    if (t.t === 'eof') cerr('expected expression at end of input', line);
    cerr("expected expression before '" + t.v + "'", line);
  };

  /* ------------------------------------------------------------------ runtime */
  function makeArray(type, dims) {
    function mk(d) {
      var n = dims[d], a = new Array(n);
      if (d === dims.length - 1) { for (var i = 0; i < n; i++) a[i] = 0; }
      else for (var j = 0; j < n; j++) a[j] = mk(d + 1);
      a.elem = type; a.dimsLeft = dims.length - d;
      return a;
    }
    return mk(0);
  }
  var BRK = { brk: 1 }, CNT = { cnt: 1 };
  function Ret(v) { this.v = v; }
  function Machine(prog, opts) {
    this.prog = prog; this.out = []; this.outLen = 0; this.steps = 0; this.maxSteps = opts.maxSteps || 5000000; this.depth = 0; this.line = 0;
    this.stdin = opts.stdin || ''; this.inPos = 0; this.globals = {}; this.warnings = []; this.randSeed = 1;
  }
  var M = Machine.prototype;
  M.write = function (s) { this.outLen += s.length; if (this.outLen > 200000) throw new CErr('limit', 'too much output (over 200,000 characters). Is a loop printing too often?'); this.out.push(s); };
  M.warn = function (msg, line) { var w = 'warning (line ' + line + '): ' + msg; if (this.warnings.indexOf(w) < 0) this.warnings.push(w); };
  M.tick = function (line) { this.line = line; if (++this.steps > this.maxSteps) throw new CErr('limit', 'the program ran for too long (more than ' + this.maxSteps.toLocaleString() + ' steps). Is there an infinite loop?'); };
  M.run = function () {
    var g = this.globals, self = this, fr = { vars: g };
    this.prog.globals.forEach(function (d) { self.execDecl(d, fr); });
    var main = this.prog.funcs.main;
    return this.callFn(main, []);
  };
  M.initValue = function (type, init, fr, line) {
    if (type.arr) {
      var dims = type.dims.slice(), arr = makeArray(type.arr, dims), self = this;
      if (init && init.k === 'strinit') { for (var c = 0; c < init.v.length && c < dims[0]; c++) arr[c] = init.v.charCodeAt(c); return arr; }
      if (init) {
        if (init.k !== 'list') cerr('invalid initializer for array', line);
        (function fill(a, lst, depth) {
          if (lst.items.length > a.length) self.warn('excess elements in array initializer', line);
          var flat = depth === dims.length - 1;
          if (!flat && lst.items.length && lst.items[0].k !== 'list') {   // flat init of 2-D array
            var k = 0; (function flatFill(b, d) { for (var i = 0; i < b.length; i++) { if (d === dims.length - 1) { if (k < lst.items.length) b[i] = conv(self.eval(lst.items[k++], fr), type.arr); } else flatFill(b[i], d + 1); } })(a, depth);
            return;
          }
          lst.items.forEach(function (it, i) {
            if (i >= a.length) return;
            if (flat) a[i] = conv(self.eval(it, fr), type.arr); else fill(a[i], it, depth + 1);
          });
        })(arr, init, 0);
      }
      return arr;
    }
    if (init) { if (init.k === 'list') return conv(this.eval(init.items[0], fr), type); return conv(this.eval(init, fr), type); }
    return 0;
  };
  M.execDecl = function (d, fr) {
    var info = d.info;
    if (!d.init && !info.type.arr && !info.global) { fr.vars[info.id] = { v: undefined, t: info.type, name: info.name }; return; }   // uninitialised local
    fr.vars[info.id] = { v: this.initValue(info.type, d.init, fr, d.line), t: info.type };
  };
  M.callFn = function (fn, args) {
    if (++this.depth > 3000) throw new CErr('runtime', 'Segmentation fault (stack overflow: recursion too deep)', this.line);
    var fr = { vars: {} };
    for (var i = 0; i < fn.params.length; i++) {
      var p = fn.params[i];
      fr.vars[p.id] = { v: p.type.arr ? args[i] : conv(args[i], p.type), t: p.type };
    }
    var r;
    try { r = this.exec(fn.body, fr); } finally { this.depth--; }
    if (r instanceof Ret) return r.v;
    if (fn.ret !== 'void' && fn.name !== 'main') this.warn("control reaches end of non-void function '" + fn.name + "'", fn.line);
    return fn.name === 'main' ? 0 : 0;
  };
  M.cell = function (e, fr) {   // returns {get, set} for an lvalue
    if (e.k === 'var') {
      var c = fr.vars[e.info.id] || this.globals[e.info.id];
      if (!c) rerr('internal: variable not found', e.line);
      return { get: function () { return c.v; }, set: function (v) { c.v = v; }, cellRef: c, name: e.info.name };
    }
    if (e.k === 'idx') {
      var arr = this.eval(e.a, fr), i = this.eval(e.i, fr);
      if (!arr || !arr.length && arr.length !== 0) rerr('Segmentation fault (indexing something that is not an array)', e.line);
      if (i < 0 || i >= arr.length) rerr('Segmentation fault: index ' + i + ' is outside the array (valid: 0 to ' + (arr.length - 1) + '). Real C may not crash here; it silently reads or overwrites other memory.', e.line);
      return { get: function () { return arr[i]; }, set: function (v) { arr[i] = v; } };
    }
    rerr('lvalue required', e.line);
  };
  M.exec = function (s, fr) {
    this.tick(s.line);
    switch (s.k) {
      case 'decl': this.execDecl(s, fr); return;
      case 'expr': this.eval(s.e, fr); return;
      case 'empty': return;
      case 'block': for (var i = 0; i < s.body.length; i++) { var r = this.exec(s.body[i], fr); if (r !== undefined) return r; } return;
      case 'if': if (this.truth(s.c, fr)) return this.exec(s.th, fr); if (s.el) return this.exec(s.el, fr); return;
      case 'while': while (this.truth(s.c, fr)) { this.tick(s.line); var w = this.exec(s.body, fr); if (w === BRK) break; if (w === CNT) continue; if (w !== undefined) return w; } return;
      case 'do': do { this.tick(s.line); var dw = this.exec(s.body, fr); if (dw === BRK) break; if (dw === CNT) continue; if (dw !== undefined) return dw; } while (this.truth(s.c, fr)); return;
      case 'for': {
        if (s.init) this.exec(s.init, fr);
        while (!s.c || this.truth(s.c, fr)) {
          this.tick(s.line);
          var fb = this.exec(s.body, fr);
          if (fb === BRK) break;
          if (fb !== undefined && fb !== CNT) return fb;
          if (s.step) this.eval(s.step, fr);
        }
        return;
      }
      case 'return': return new Ret(s.e ? conv(this.eval(s.e, fr), s.ret) : 0);
      case 'break': return BRK;
      case 'continue': return CNT;
      case 'switch': {
        var v = this.eval(s.e, fr), start = -1;
        for (var k = 0; k < s.cases.length; k++) if (s.cases[k].v === v) { start = k; break; }
        if (start < 0) for (var k2 = 0; k2 < s.cases.length; k2++) if (s.cases[k2].v === 'default') { start = k2; break; }
        if (start < 0) return;
        for (var c = start; c < s.cases.length; c++) {
          var body = s.cases[c].body;
          for (var b = 0; b < body.length; b++) { var sr = this.exec(body[b], fr); if (sr === BRK) return; if (sr !== undefined) return sr; }
        }
        return;
      }
    }
  };
  M.truth = function (e, fr) { var v = this.eval(e, fr); return v !== 0 && v === v ? true : (v !== v); };
  M.eval = function (e, fr) {
    switch (e.k) {
      case 'num': return e.v;
      case 'str': return e.v;
      case 'var': {
        var c = fr.vars[e.info.id] || this.globals[e.info.id];
        if (c.v === undefined) { this.warn("'" + e.info.name + "' is used uninitialized (real C gives an unpredictable value; MiniC uses 0)", e.line); return 0; }
        return c.v;
      }
      case 'idx': { var cl = this.cell(e, fr), v = cl.get(); return v; }
      case 'assign': {
        var cell = this.cell(e.l, fr), t = e.l.type, r = this.eval(e.r, fr);
        if (e.op === '=') { var nv = conv(r, t); cell.set(nv); return nv; }
        var op = e.op.slice(0, -1), cur = cell.get();
        if (cur === undefined) { this.warn("'" + (cell.name || 'variable') + "' is used uninitialized", e.line); cur = 0; }
        var ct = common(t, e.r.type), res = this.arith(op, cur, r, ct, e.line);
        var nv2 = conv(res, t); cell.set(nv2); return nv2;
      }
      case 'pre': case 'post': {
        var pc = this.cell(e.e, fr), old = pc.get(); if (old === undefined) old = 0;
        var nw = conv(e.op === '++' ? old + 1 : old - 1, e.type === 'char' ? 'char' : e.type);
        if (e.type === 'int') nw = (e.op === '++' ? (old + 1) | 0 : (old - 1) | 0);
        pc.set(nw); return e.k === 'pre' ? nw : old;
      }
      case 'un': {
        var u = this.eval(e.e, fr);
        if (e.op === '-') return e.type === 'int' ? (-u) | 0 : -u;
        if (e.op === '+') return u;
        if (e.op === '!') return u === 0 ? 1 : 0;
        if (e.op === '~') return ~u;
      }
      case 'cast': { var cv = this.eval(e.e, fr); return e.to === 'void' ? 0 : conv(cv, e.to); }
      case 'bin': {
        if (e.op === '&&') return (this.truth(e.a, fr) && this.truth(e.b, fr)) ? 1 : 0;
        if (e.op === '||') return (this.truth(e.a, fr) || this.truth(e.b, fr)) ? 1 : 0;
        var a = this.eval(e.a, fr), b = this.eval(e.b, fr);
        switch (e.op) {
          case '==': return a === b ? 1 : 0; case '!=': return a !== b ? 1 : 0;
          case '<': return a < b ? 1 : 0; case '>': return a > b ? 1 : 0; case '<=': return a <= b ? 1 : 0; case '>=': return a >= b ? 1 : 0;
        }
        return this.arith(e.op, a, b, e.type, e.line);
      }
      case 'cond': return this.truth(e.c, fr) ? conv(this.eval(e.a, fr), e.type) : conv(this.eval(e.b, fr), e.type);
      case 'comma': this.eval(e.a, fr); return this.eval(e.b, fr);
      case 'addr': return this.cell(e.e, fr);
      case 'call': {
        this.tick(e.line);
        var fn = this.prog.funcs[e.name], self = this;
        var args = e.args.map(function (a) { return self.eval(a, fr); });
        var res = this.callFn(fn, args); this.line = e.line;
        return res;
      }
      case 'math': {
        var x = this.eval(e.args[0], fr), y = e.args.length > 1 ? this.eval(e.args[1], fr) : 0;
        switch (e.name) {
          case 'sqrt': return Math.sqrt(x); case 'sqrtf': return Math.fround(Math.sqrt(Math.fround(x)));
          case 'pow': return Math.pow(x, y); case 'powf': return Math.fround(Math.pow(Math.fround(x), Math.fround(y)));
          case 'exp': return Math.exp(x); case 'expf': return Math.fround(Math.exp(x));
          case 'log': return Math.log(x); case 'logf': return Math.fround(Math.log(x)); case 'log10': return Math.log10(x); case 'log2': return Math.log2(x);
          case 'log1p': return Math.log1p(x); case 'expm1': return Math.expm1(x);
          case 'sin': return Math.sin(x); case 'cos': return Math.cos(x); case 'tan': return Math.tan(x); case 'sinf': return Math.fround(Math.sin(x)); case 'cosf': return Math.fround(Math.cos(x));
          case 'asin': return Math.asin(x); case 'acos': return Math.acos(x); case 'atan': return Math.atan(x); case 'atan2': return Math.atan2(x, y);
          case 'sinh': return Math.sinh(x); case 'cosh': return Math.cosh(x); case 'tanh': return Math.tanh(x);
          case 'fabs': return Math.abs(x); case 'fabsf': return Math.fround(Math.abs(x)); case 'abs': return Math.abs(x) | 0; case 'labs': return Math.abs(x);
          case 'floor': return Math.floor(x); case 'ceil': return Math.ceil(x); case 'trunc': return Math.trunc(x);
          case 'round': return x < 0 ? -Math.round(-x) : Math.round(x) - ((x % 1 === -0.5) ? 1 : 0);
          case 'fmod': return x % y; case 'fmax': return Math.max(x, y); case 'fmin': return Math.min(x, y); case 'hypot': return Math.hypot(x, y); case 'cbrt': return Math.cbrt(x);
          case 'isnan': return x !== x ? 1 : 0; case 'isinf': return (x === Infinity || x === -Infinity) ? 1 : 0;
        }
      }
      case 'lib': return this.lib(e, fr);
    }
    rerr('internal: cannot evaluate ' + e.k, e.line);
  };
  M.arith = function (op, a, b, t, line) {
    if (t === 'int' || t === 'long' || t === 'char') {
      switch (op) {
        case '+': return t === 'int' ? (a + b) | 0 : a + b;
        case '-': return t === 'int' ? (a - b) | 0 : a - b;
        case '*': return t === 'int' ? Math.imul(a, b) : a * b;
        case '/': if (b === 0) rerr('Floating point exception (core dumped): integer division by zero', line); return t === 'int' ? (a / b) | 0 : Math.trunc(a / b);
        case '%': if (b === 0) rerr('Floating point exception (core dumped): integer modulo by zero', line); return a % b;
        case '<<': return a << b; case '>>': return a >> b; case '&': return a & b; case '|': return a | b; case '^': return a ^ b;
      }
    }
    var r;
    switch (op) { case '+': r = a + b; break; case '-': r = a - b; break; case '*': r = a * b; break; case '/': r = a / b; break; }
    return t === 'float' ? Math.fround(r) : r;
  };
  M.lib = function (e, fr) {
    var self = this, name = e.name;
    if (name === 'printf') {
      var args = e.args.slice(1).map(function (a) {
        var v = self.eval(a, fr), t = a.type;
        if (t === 'float') t = 'double';           // default argument promotion
        if (t === 'char') t = 'int';
        if (t && t.arr) { if (t.arr === 'char') { var s = ''; for (var i = 0; i < v.length && v[i]; i++) s += String.fromCharCode(v[i]); return { v: s, t: 'str' }; } return { v: 0, t: 'ptr' }; }
        return { v: v, t: t };
      });
      var fmt = e.args[0].v;
      if (typeof fmt !== 'string') { fmt = self.eval(e.args[0], fr); if (typeof fmt !== 'string') { var cs = ''; for (var ci = 0; fmt && ci < fmt.length && fmt[ci]; ci++) cs += String.fromCharCode(fmt[ci]); fmt = cs; } }
      var convs = (fmt.replace(/%%/g, '').match(/%[-+ #0]*(\*|\d+)?(\.(\*|\d*))?(hh|h|ll|l|L)?[diouxXfFeEgGcsp]/g) || []).length;
      if (convs > args.length) this.warn('printf: the format has more % conversions than arguments', e.line);
      var s2 = NF.cFormat(fmt, args, function (m) { self.warn(m, e.line); });
      this.write(s2); return s2.length;
    }
    if (name === 'puts') { var a0 = this.eval(e.args[0], fr); this.write((typeof a0 === 'string' ? a0 : '') + '\n'); return 0; }
    if (name === 'putchar') { this.write(String.fromCharCode(this.eval(e.args[0], fr))); return 0; }
    if (name === 'scanf') {
      var f = e.args[0].v, specs = f.match(/%l?[dfeg]|%c|%s/g) || [], count = 0;
      for (var k = 0; k < specs.length; k++) {
        var tgt = e.args[k + 1];
        if (!tgt || tgt.k !== 'addr') { if (tgt && tgt.type && tgt.type.arr) {} else rerr("scanf needs the address of a variable: write &x, not x", e.line); }
        var rest = this.stdin.slice(this.inPos), mm = /^\s*([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)/.exec(rest);
        if (!mm) break;
        this.inPos += mm[0].length;
        var cell = this.eval(tgt, fr), tt = tgt.e.type, val = parseFloat(mm[1]);
        if (specs[k] === '%f' && tt === 'double') this.warn("scanf: use %lf (not %f) to read a double", e.line);
        if (specs[k] === '%lf' && tt === 'float') this.warn("scanf: use %f (not %lf) to read a float", e.line);
        cell.set(conv(val, tt)); count++;
        this.write(mm[1] + (k === specs.length - 1 ? '\n' : ' '));      // echo input like a terminal
      }
      if (count === 0 && specs.length) this.warn('scanf found no input: type the numbers in the Input box', e.line);
      return count;
    }
    if (name === 'rand') { this.randSeed = (this.randSeed * 1103515245 + 12345) & 0x7fffffff; return this.randSeed; }
    if (name === 'srand') { this.randSeed = this.eval(e.args[0], fr) >>> 0; return 0; }
    if (name === 'time') return 0;
    if (name === 'exit') throw new CErr('exit', String(e.args.length ? this.eval(e.args[0], fr) : 0));
    if (name === 'getchar') { if (this.inPos >= this.stdin.length) return -1; return this.stdin.charCodeAt(this.inPos++); }
    return 0;
  };

  function run(src, opts) {
    opts = opts || {};
    var res = { out: '', error: null, line: null, warnings: [] }, t0 = Date.now(), m = null;
    try {
      var toks = preprocess(src), prog = new Parser(toks).program();
      m = new Machine(prog, opts);
      var code = m.run();
      res.exit = code;
    } catch (e) {
      if (e instanceof CErr) {
        if (e.kind === 'error') { res.error = 'Compile error (line ' + e.line + '): ' + e.msg; res.line = e.line; res.compile = true; }
        else if (e.kind === 'exit') { res.exit = +e.msg; }
        else if (e.kind === 'limit') { res.error = 'Stopped: ' + e.msg; res.line = m ? m.line : null; }
        else { res.error = 'Runtime error (line ' + (e.line || (m && m.line)) + '): ' + e.msg; res.line = e.line || (m && m.line); }
      } else if (e instanceof RangeError) { res.error = 'Segmentation fault (stack overflow: recursion too deep)'; }
      else res.error = 'Internal error: ' + (e && e.message);
    }
    if (m) { res.out = m.out.join(''); res.warnings = m.warnings; }
    res.ms = Date.now() - t0;
    return res;
  }
  G.MiniC = { run: run, version: '1.0' };
})(typeof window !== 'undefined' ? window : globalThis);
