/* MiniPy: a small Python 3 interpreter for teaching numerical methods in the browser.
   Supports the subset used in this course: numbers (exact ints, IEEE doubles), strings, lists, tuples,
   dicts, functions, lambda, if/elif/else, for/while, break/continue, try/except, f-strings,
   list comprehensions, import math. Every course example is checked against real Python 3. */
(function (G) {
  'use strict';
  var NF = G.NumFmt;

  function PyErr(type, msg, line) { this.type = type; this.msg = msg; this.line = line; }
  function err(type, msg) { throw new PyErr(type, msg); }
  function Tuple(a) { this.a = a; }
  function Dict() { this.m = new Map(); }
  function keyOf(k) {
    if (typeof k === 'bigint') return 'n' + k.toString();
    if (typeof k === 'number') return Number.isInteger(k) && Math.abs(k) < 1e300 ? 'n' + BigInt(k).toString() : 'f' + k;
    if (typeof k === 'boolean') return 'n' + (k ? '1' : '0');
    if (typeof k === 'string') return 's' + k;
    if (k === null) return 'N';
    if (k instanceof Tuple) return 't(' + k.a.map(keyOf).join(',') + ')';
    err('TypeError', "unhashable type: '" + typeName(k) + "'");
  }
  Dict.prototype.get = function (k) { var e = this.m.get(keyOf(k)); return e; };
  Dict.prototype.set = function (k, v) { var kk = keyOf(k), e = this.m.get(kk); if (e) e[1] = v; else this.m.set(kk, [k, v]); };
  function Range(a, b, s) { this.a = a; this.b = b; this.s = s; }
  function Fn(name, params, body, closure, isLambda) { this.name = name; this.params = params; this.body = body; this.closure = closure; this.isLambda = isLambda; }
  function Builtin(name, f) { this.name = name; this.f = f; }
  function Module(name, attrs) { this.name = name; this.attrs = attrs; }
  function BoundMethod(self, name, f) { this.self = self; this.name = name; this.f = f; }
  function ExcType(name) { this.name = name; }
  function ExcVal(type, msg) { this.type = type; this.msg = msg; }

  /* ------------------------------------------------------------------ tokenizer */
  var KW = { 'False': 1, 'None': 1, 'True': 1, 'and': 1, 'as': 1, 'assert': 1, 'break': 1, 'class': 1, 'continue': 1, 'def': 1, 'del': 1,
    'elif': 1, 'else': 1, 'except': 1, 'finally': 1, 'for': 1, 'from': 1, 'global': 1, 'if': 1, 'import': 1, 'in': 1, 'is': 1,
    'lambda': 1, 'nonlocal': 1, 'not': 1, 'or': 1, 'pass': 1, 'raise': 1, 'return': 1, 'try': 1, 'while': 1, 'with': 1, 'yield': 1 };
  var OPS = ['**=', '//=', '>>=', '<<=', '!=', '==', '<=', '>=', '**', '//', '->', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<', '>>', ':=',
    '+', '-', '*', '/', '%', '<', '>', '=', '(', ')', '[', ']', '{', '}', ',', ':', '.', ';', '@', '&', '|', '^', '~'];

  function tokenize(src) {
    var toks = [], i = 0, line = 1, depth = 0, indents = [0], atLineStart = true, n = src.length;
    src = src.replace(/\r\n?/g, '\n').replace(/\t/g, '    ');
    n = src.length;
    function push(t, v, extra) { var o = { t: t, v: v, line: line }; if (extra) for (var k in extra) o[k] = extra[k]; toks.push(o); }
    while (i < n) {
      if (atLineStart && depth === 0) {
        var col = 0, j = i;
        while (j < n && src[j] === ' ') { col++; j++; }
        if (j >= n) { i = j; break; }
        if (src[j] === '\n' || src[j] === '#') {               // blank or comment-only line
          while (j < n && src[j] !== '\n') j++;
          i = j + 1; line++; continue;
        }
        if (col > indents[indents.length - 1]) { indents.push(col); push('INDENT'); }
        else {
          while (col < indents[indents.length - 1]) { indents.pop(); push('DEDENT'); }
          if (col !== indents[indents.length - 1]) { var e = new PyErr('IndentationError', 'unindent does not match any outer indentation level'); e.line = line; throw e; }
        }
        i = j; atLineStart = false;
      }
      var c = src[i];
      if (c === '\n') { if (depth === 0) { push('NEWLINE'); atLineStart = true; } i++; line++; continue; }
      if (c === ' ') { i++; continue; }
      if (c === '#') { while (i < n && src[i] !== '\n') i++; continue; }
      if (c === '\\' && src[i + 1] === '\n') { i += 2; line++; continue; }
      // strings (with prefixes)
      var pm = /^([rRfFbBuU]{0,2})('''|"""|'|")/.exec(src.slice(i, i + 5));
      if (pm && (pm[1] === '' || /^[rRfFbBuU]+$/.test(pm[1])) && (pm[1].length === 0 || /[A-Za-z]/.test(c))) {
        var pre = pm[1].toLowerCase(), q = pm[2], k = i + pm[0].length, s = '', raw = pre.indexOf('r') >= 0, startLine = line;
        while (true) {
          if (k >= n) { var e2 = new PyErr('SyntaxError', 'unterminated string literal'); e2.line = startLine; throw e2; }
          if (src.substr(k, q.length) === q) { k += q.length; break; }
          var ch = src[k];
          if (ch === '\n') { if (q.length === 1) { var e3 = new PyErr('SyntaxError', 'unterminated string literal'); e3.line = startLine; throw e3; } line++; }
          if (ch === '\\' && !raw) {
            var nx = src[k + 1]; k += 2;
            if (nx === 'n') s += '\n'; else if (nx === 't') s += '\t'; else if (nx === '\\') s += '\\'; else if (nx === "'") s += "'";
            else if (nx === '"') s += '"'; else if (nx === '\n') { line++; } else if (nx === 'r') s += '\r'; else if (nx === '0') s += '\0';
            else if (nx === 'u') { s += String.fromCharCode(parseInt(src.substr(k, 4), 16)); k += 4; }
            else if (nx === 'x') { s += String.fromCharCode(parseInt(src.substr(k, 2), 16)); k += 2; }
            else s += '\\' + nx;
            continue;
          }
          if (ch === '\\' && raw) { s += ch + src[k + 1]; k += 2; continue; }
          s += ch; k++;
        }
        push(pre.indexOf('f') >= 0 ? 'FSTR' : 'STR', s, { raw: raw });
        i = k; continue;
      }
      if (/[0-9]/.test(c) || (c === '.' && /[0-9]/.test(src[i + 1]))) {
        var m = /^(0[xX][0-9a-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+|(?:\d[\d_]*\.?[\d_]*|\.\d[\d_]*)(?:[eE][+-]?\d+)?)/.exec(src.slice(i));
        var txt = m[0].replace(/_/g, '');
        if (/^0[xXbBoO]/.test(txt)) push('NUM', BigInt(txt));
        else if (/[.eE]/.test(txt)) push('NUM', parseFloat(txt));
        else push('NUM', BigInt(txt));
        i += m[0].length;
        if (/[jJ]/.test(src[i] || '')) { var e4 = new PyErr('SyntaxError', 'complex numbers are not supported in MiniPy'); e4.line = line; throw e4; }
        continue;
      }
      if (/[A-Za-z_À-￿]/.test(c)) {
        var mm = /^[A-Za-z_À-￿][A-Za-z0-9_À-￿]*/.exec(src.slice(i));
        push(KW[mm[0]] ? 'KW' : 'NAME', mm[0]); i += mm[0].length; continue;
      }
      var op = null;
      for (var oi = 0; oi < OPS.length; oi++) if (src.substr(i, OPS[oi].length) === OPS[oi]) { op = OPS[oi]; break; }
      if (!op) { var e5 = new PyErr('SyntaxError', "invalid character '" + c + "'"); e5.line = line; throw e5; }
      if (op === '(' || op === '[' || op === '{') depth++;
      if (op === ')' || op === ']' || op === '}') depth = Math.max(0, depth - 1);
      push('OP', op); i += op.length;
    }
    if (toks.length && toks[toks.length - 1].t !== 'NEWLINE') push('NEWLINE');
    while (indents.length > 1) { indents.pop(); push('DEDENT'); }
    push('EOF');
    return toks;
  }

  /* ------------------------------------------------------------------ parser */
  function Parser(toks) { this.toks = toks; this.p = 0; }
  var P = Parser.prototype;
  P.peek = function (o) { return this.toks[this.p + (o || 0)]; };
  P.next = function () { return this.toks[this.p++]; };
  P.is = function (t, v) { var k = this.toks[this.p]; return k.t === t && (v === undefined || k.v === v); };
  P.isOp = function (v) { return this.is('OP', v); };
  P.isKw = function (v) { return this.is('KW', v); };
  P.fail = function (msg) { var k = this.peek(); var e = new PyErr('SyntaxError', msg || 'invalid syntax'); e.line = k.line; throw e; };
  P.expect = function (t, v) {
    if (!this.is(t, v)) {
      var k = this.peek();
      if (v === ':') this.fail("expected ':'");
      if (k.t === 'INDENT') this.fail('unexpected indent');
      this.fail(v ? "expected '" + v + "'" : 'invalid syntax');
    }
    return this.next();
  };
  P.program = function () {
    var body = [];
    while (!this.is('EOF')) { if (this.is('NEWLINE')) { this.next(); continue; } body.push.apply(body, this.statement()); }
    return body;
  };
  P.block = function () {
    if (!this.is('NEWLINE')) return this.simpleLine();
    this.next();
    if (!this.is('INDENT')) this.fail('expected an indented block');
    this.next();
    var body = [];
    while (!this.is('DEDENT') && !this.is('EOF')) { if (this.is('NEWLINE')) { this.next(); continue; } body.push.apply(body, this.statement()); }
    this.expect('DEDENT');
    return body;
  };
  P.statement = function () {
    var k = this.peek();
    if (k.t === 'INDENT') this.fail('unexpected indent');
    if (k.t === 'KW') {
      switch (k.v) {
        case 'if': return [this.ifStmt()];
        case 'while': { this.next(); var c = this.expr(); this.expect('OP', ':'); var b = this.block(), eb = null;
          if (this.isKw('else')) { this.next(); this.expect('OP', ':'); eb = this.block(); }
          return [{ k: 'while', test: c, body: b, orelse: eb, line: k.line }]; }
        case 'for': { this.next(); var tgt = this.targetList(); this.expect('KW', 'in'); var it = this.exprList(); this.expect('OP', ':');
          var fb = this.block(), fe = null; if (this.isKw('else')) { this.next(); this.expect('OP', ':'); fe = this.block(); }
          return [{ k: 'for', target: tgt, iter: it, body: fb, orelse: fe, line: k.line }]; }
        case 'def': return [this.defStmt()];
        case 'try': return [this.tryStmt()];
        case 'class': this.fail('classes are not supported in MiniPy');
      }
    }
    return this.simpleLine();
  };
  P.simpleLine = function () {
    var out = [this.simple()];
    while (this.isOp(';')) { this.next(); if (this.is('NEWLINE')) break; out.push(this.simple()); }
    if (!this.is('NEWLINE') && !this.is('EOF')) this.fail();
    if (this.is('NEWLINE')) this.next();
    return out;
  };
  P.ifStmt = function () {
    var line = this.next().line, test = this.expr(); this.expect('OP', ':');
    var body = this.block(), orelse = null;
    if (this.isKw('elif')) { orelse = [this.ifStmt()]; }
    else if (this.isKw('else')) { this.next(); this.expect('OP', ':'); orelse = this.block(); }
    return { k: 'if', test: test, body: body, orelse: orelse, line: line };
  };
  P.defStmt = function () {
    var line = this.next().line, name = this.expect('NAME').v; this.expect('OP', '(');
    var params = this.params(')'); this.expect('OP', ')');
    if (this.isOp('->')) { this.next(); this.expr(); }
    this.expect('OP', ':');
    return { k: 'def', name: name, params: params, body: this.block(), line: line };
  };
  P.params = function (end) {
    var ps = [];
    while (!this.isOp(end)) {
      var star = '';
      if (this.isOp('*')) { this.next(); star = '*'; } else if (this.isOp('**')) { this.next(); star = '**'; }
      var nm = this.expect('NAME').v, def = null;
      if (this.isOp(':') && end === ')') { this.next(); this.expr(); }
      if (this.isOp('=')) { this.next(); def = this.expr(); }
      ps.push({ name: nm, def: def, star: star });
      if (!this.isOp(',')) break; this.next();
    }
    return ps;
  };
  P.tryStmt = function () {
    var line = this.next().line; this.expect('OP', ':');
    var body = this.block(), handlers = [], fin = null, orelse = null;
    while (this.isKw('except')) {
      this.next(); var type = null, as = null;
      if (!this.isOp(':')) { type = this.expr(); if (this.isKw('as')) { this.next(); as = this.expect('NAME').v; } }
      this.expect('OP', ':'); handlers.push({ type: type, as: as, body: this.block() });
    }
    if (this.isKw('else')) { this.next(); this.expect('OP', ':'); orelse = this.block(); }
    if (this.isKw('finally')) { this.next(); this.expect('OP', ':'); fin = this.block(); }
    return { k: 'try', body: body, handlers: handlers, orelse: orelse, fin: fin, line: line };
  };
  P.simple = function () {
    var k = this.peek(), line = k.line;
    if (k.t === 'KW') {
      switch (k.v) {
        case 'pass': this.next(); return { k: 'pass', line: line };
        case 'break': this.next(); return { k: 'break', line: line };
        case 'continue': this.next(); return { k: 'continue', line: line };
        case 'return': this.next(); return { k: 'return', value: (this.is('NEWLINE') || this.isOp(';')) ? null : this.exprList(), line: line };
        case 'global': case 'nonlocal': { this.next(); var names = [this.expect('NAME').v]; while (this.isOp(',')) { this.next(); names.push(this.expect('NAME').v); } return { k: 'global', names: names, line: line }; }
        case 'import': { this.next(); var mods = []; do { if (mods.length) this.next(); var nm = this.dotted(), as = nm; if (this.isKw('as')) { this.next(); as = this.expect('NAME').v; } mods.push([nm, as]); } while (this.isOp(','));
          return { k: 'import', mods: mods, line: line }; }
        case 'from': { this.next(); var mod = this.dotted(); this.expect('KW', 'import'); var items = [];
          if (this.isOp('*')) { this.next(); items = '*'; }
          else { var par = this.isOp('('); if (par) this.next();
            do { if (items.length) this.next(); if (par && this.isOp(')')) break; var n2 = this.expect('NAME').v, a2 = n2; if (this.isKw('as')) { this.next(); a2 = this.expect('NAME').v; } items.push([n2, a2]); } while (this.isOp(','));
            if (par) this.expect('OP', ')'); }
          return { k: 'from', mod: mod, items: items, line: line }; }
        case 'raise': { this.next(); return { k: 'raise', exc: this.is('NEWLINE') ? null : this.expr(), line: line }; }
        case 'assert': { this.next(); var t = this.expr(), msg = null; if (this.isOp(',')) { this.next(); msg = this.expr(); } return { k: 'assert', test: t, msg: msg, line: line }; }
        case 'del': { this.next(); return { k: 'del', target: this.exprList(), line: line }; }
      }
    }
    var e = this.exprList();
    if (this.isOp('=')) {
      var targets = [e];
      while (this.isOp('=')) { this.next(); targets.push(this.exprList()); }
      var value = targets.pop();
      targets.forEach(function (t) { checkTarget(t, this); }, this);
      return { k: 'assign', targets: targets, value: value, line: line };
    }
    if (this.is('OP') && /^(\+|-|\*|\/|\/\/|%|\*\*|&|\||\^|<<|>>)=$/.test(this.peek().v)) {
      var op = this.next().v.slice(0, -1); checkTarget(e, this);
      return { k: 'aug', target: e, op: op, value: this.exprList(), line: line };
    }
    if (this.isOp(':')) { // annotation  x: int = 3
      this.next(); this.expr(); if (this.isOp('=')) { this.next(); return { k: 'assign', targets: [e], value: this.exprList(), line: line }; }
      return { k: 'pass', line: line };
    }
    return { k: 'expr', value: e, line: line };
  };
  function checkTarget(t, p) {
    if (t.k === 'name' || t.k === 'index' || t.k === 'attr') return;
    if (t.k === 'tuple' || t.k === 'list') { t.items.forEach(function (x) { checkTarget(x, p); }); return; }
    if (t.k === 'starred') return;
    var e = new PyErr('SyntaxError', t.k === 'call' ? 'cannot assign to function call' : 'cannot assign to expression'); e.line = t.line; throw e;
  }
  P.dotted = function () { var n = this.expect('NAME').v; while (this.isOp('.')) { this.next(); n += '.' + this.expect('NAME').v; } return n; };
  P.targetList = function () {
    var line = this.peek().line, items = [this.bitor()];
    if (!this.isOp(',')) return items[0];
    while (this.isOp(',')) { this.next(); if (this.isKw("in")) break; items.push(this.bitor()); }
    return { k: 'tuple', items: items, line: line };
  };
  P.exprList = function () {
    var line = this.peek().line, first = this.isOp('*') ? this.starred() : this.expr();
    if (!this.isOp(',')) return first;
    var items = [first];
    while (this.isOp(',')) { this.next(); if (this.endOfList()) break; items.push(this.isOp('*') ? this.starred() : this.expr()); }
    return { k: 'tuple', items: items, line: line };
  };
  P.starred = function () { var line = this.next().line; return { k: 'starred', value: this.orExpr(), line: line }; };
  P.endOfList = function () { var k = this.peek(); return k.t === 'NEWLINE' || k.t === 'EOF' || (k.t === 'OP' && /^[)\]}=:;]$/.test(k.v)) || (k.t === 'OP' && /=$/.test(k.v) && k.v.length > 1 && k.v !== '==' && k.v !== '!=' && k.v !== '<=' && k.v !== '>='); };
  P.expr = function () {
    if (this.isKw('lambda')) {
      var line = this.next().line, params = this.params(':'); this.expect('OP', ':');
      return { k: 'lambda', params: params, body: this.expr(), line: line };
    }
    var e = this.orExpr();
    if (this.isKw('if')) {
      var l2 = this.next().line, test = this.orExpr(); this.expect('KW', 'else');
      return { k: 'ifexp', test: test, body: e, orelse: this.expr(), line: l2 };
    }
    return e;
  };
  P.orExpr = function () { var e = this.andExpr(); while (this.isKw('or')) { var l = this.next().line; e = { k: 'or', a: e, b: this.andExpr(), line: l }; } return e; };
  P.andExpr = function () { var e = this.notExpr(); while (this.isKw('and')) { var l = this.next().line; e = { k: 'and', a: e, b: this.notExpr(), line: l }; } return e; };
  P.notExpr = function () { if (this.isKw('not')) { var l = this.next().line; return { k: 'not', a: this.notExpr(), line: l }; } return this.comparison(); };
  P.comparison = function () {
    var first = this.bitor(), ops = [], rest = [], line = this.peek().line;
    while (true) {
      var k = this.peek(), op = null;
      if (k.t === 'OP' && /^(<|>|==|>=|<=|!=)$/.test(k.v)) { op = k.v; this.next(); }
      else if (k.t === 'KW' && k.v === 'in') { op = 'in'; this.next(); }
      else if (k.t === 'KW' && k.v === 'not' && this.peek(1).t === 'KW' && this.peek(1).v === 'in') { op = 'not in'; this.next(); this.next(); }
      else if (k.t === 'KW' && k.v === 'is') { this.next(); if (this.isKw('not')) { this.next(); op = 'is not'; } else op = 'is'; }
      else break;
      ops.push(op); rest.push(this.bitor());
    }
    if (!ops.length) return first;
    return { k: 'compare', first: first, ops: ops, rest: rest, line: line };
  };
  function binLevel(ops, nextFn) {
    return function () {
      var e = this[nextFn]();
      while (this.is('OP') && ops.indexOf(this.peek().v) >= 0) { var t = this.next(); e = { k: 'bin', op: t.v, a: e, b: this[nextFn](), line: t.line }; }
      return e;
    };
  }
  P.bitor = binLevel(['|'], 'bitxor');
  P.bitxor = binLevel(['^'], 'bitand');
  P.bitand = binLevel(['&'], 'shift');
  P.shift = binLevel(['<<', '>>'], 'arith');
  P.arith = binLevel(['+', '-'], 'term');
  P.term = binLevel(['*', '/', '//', '%', '@'], 'factor');
  P.factor = function () {
    if (this.is('OP') && /^[-+~]$/.test(this.peek().v)) { var t = this.next(); return { k: 'unary', op: t.v, a: this.factor(), line: t.line }; }
    return this.power();
  };
  P.power = function () {
    var e = this.primary();
    if (this.isOp('**')) { var t = this.next(); return { k: 'bin', op: '**', a: e, b: this.factor(), line: t.line }; }
    return e;
  };
  P.primary = function () {
    var e = this.atom();
    while (true) {
      if (this.isOp('(')) { var l = this.next().line; var args = this.callArgs(); this.expect('OP', ')'); e = { k: 'call', fn: e, args: args.pos, kw: args.kw, line: l }; }
      else if (this.isOp('[')) { var l2 = this.next().line; var idx = this.subscript(); this.expect('OP', ']'); e = { k: 'index', obj: e, idx: idx, line: l2 }; }
      else if (this.isOp('.')) { var l3 = this.next().line; e = { k: 'attr', obj: e, name: this.expect('NAME').v, line: l3 }; }
      else break;
    }
    return e;
  };
  P.callArgs = function () {
    var pos = [], kw = [];
    while (!this.isOp(')')) {
      if (this.is('NAME') && this.peek(1).t === 'OP' && this.peek(1).v === '=') { var n = this.next().v; this.next(); kw.push([n, this.expr()]); }
      else if (this.isOp('*')) { this.next(); pos.push({ k: 'starred', value: this.expr() }); }
      else {
        var e = this.expr();
        if (this.isKw('for')) e = this.comprehension('gen', e);
        pos.push(e);
      }
      if (!this.isOp(',')) break; this.next();
    }
    return { pos: pos, kw: kw };
  };
  P.subscript = function () {
    var line = this.peek().line;
    function sl(self) {
      var a = null, b = null, c = null;
      if (!self.isOp(':')) { a = self.expr(); if (!self.isOp(':')) return a; }
      self.next();
      if (!self.isOp(']') && !self.isOp(':') && !self.isOp(',')) b = self.expr();
      if (self.isOp(':')) { self.next(); if (!self.isOp(']') && !self.isOp(',')) c = self.expr(); }
      return { k: 'slice', a: a, b: b, c: c, line: line };
    }
    var first = sl(this);
    if (!this.isOp(',')) return first;
    var items = [first]; while (this.isOp(',')) { this.next(); if (this.isOp(']')) break; items.push(sl(this)); }
    return { k: 'tuple', items: items, line: line };
  };
  P.comprehension = function (kind, elt, valExpr) {
    var gens = [];
    while (this.isKw('for')) {
      this.next(); var tgt = this.targetList(); this.expect('KW', 'in'); var it = this.orExpr(), ifs = [];
      while (this.isKw('if')) { this.next(); ifs.push(this.orExpr()); }
      gens.push({ target: tgt, iter: it, ifs: ifs });
    }
    return { k: 'comp', kind: kind, elt: elt, val: valExpr, gens: gens, line: elt.line };
  };
  P.atom = function () {
    var k = this.peek(), line = k.line;
    if (k.t === 'NUM') { this.next(); return { k: 'const', v: k.v, line: line }; }
    if (k.t === 'STR' || k.t === 'FSTR') {
      var parts = [];
      while (this.is('STR') || this.is('FSTR')) {
        var t = this.next();
        if (t.t === 'STR') parts.push({ k: 'const', v: t.v, line: line });
        else parts.push(parseFString(t.v, line));
      }
      if (parts.length === 1) return parts[0];
      return { k: 'concat', parts: parts, line: line };
    }
    if (k.t === 'NAME') { this.next(); return { k: 'name', id: k.v, line: line }; }
    if (k.t === 'KW') {
      if (k.v === 'True') { this.next(); return { k: 'const', v: true, line: line }; }
      if (k.v === 'False') { this.next(); return { k: 'const', v: false, line: line }; }
      if (k.v === 'None') { this.next(); return { k: 'const', v: null, line: line }; }
    }
    if (k.t === 'OP') {
      if (k.v === '(') {
        this.next();
        if (this.isOp(')')) { this.next(); return { k: 'tuple', items: [], line: line }; }
        var e = this.isOp('*') ? this.starred() : this.expr();
        if (this.isKw('for')) { e = this.comprehension('gen', e); this.expect('OP', ')'); return e; }
        if (this.isOp(',')) {
          var items = [e];
          while (this.isOp(',')) { this.next(); if (this.isOp(')')) break; items.push(this.isOp('*') ? this.starred() : this.expr()); }
          this.expect('OP', ')'); return { k: 'tuple', items: items, line: line };
        }
        this.expect('OP', ')'); return e;
      }
      if (k.v === '[') {
        this.next();
        if (this.isOp(']')) { this.next(); return { k: 'list', items: [], line: line }; }
        var f = this.isOp('*') ? this.starred() : this.expr();
        if (this.isKw('for')) { var c = this.comprehension('list', f); this.expect('OP', ']'); return c; }
        var li = [f];
        while (this.isOp(',')) { this.next(); if (this.isOp(']')) break; li.push(this.isOp('*') ? this.starred() : this.expr()); }
        this.expect('OP', ']'); return { k: 'list', items: li, line: line };
      }
      if (k.v === '{') {
        this.next();
        if (this.isOp('}')) { this.next(); return { k: 'dict', keys: [], vals: [], line: line }; }
        var k1 = this.expr();
        if (this.isOp(':')) {
          this.next(); var v1 = this.expr();
          if (this.isKw('for')) { var dc = this.comprehension('dict', k1, v1); this.expect('OP', '}'); return dc; }
          var keys = [k1], vals = [v1];
          while (this.isOp(',')) { this.next(); if (this.isOp('}')) break; keys.push(this.expr()); this.expect('OP', ':'); vals.push(this.expr()); }
          this.expect('OP', '}'); return { k: 'dict', keys: keys, vals: vals, line: line };
        }
        if (this.isKw('for')) { var sc = this.comprehension('set', k1); this.expect('OP', '}'); return sc; }
        var si = [k1]; while (this.isOp(',')) { this.next(); if (this.isOp('}')) break; si.push(this.expr()); }
        this.expect('OP', '}'); return { k: 'set', items: si, line: line };
      }
    }
    if (k.t === 'NEWLINE' || k.t === 'EOF') this.fail('invalid syntax (incomplete line)');
    if (k.t === 'INDENT') this.fail('unexpected indent');
    this.fail('invalid syntax');
  };
  function parseFString(s, line) {
    var parts = [], i = 0, lit = '';
    while (i < s.length) {
      var c = s[i];
      if (c === '{' && s[i + 1] === '{') { lit += '{'; i += 2; continue; }
      if (c === '}' && s[i + 1] === '}') { lit += '}'; i += 2; continue; }
      if (c === '{') {
        if (lit) { parts.push({ k: 'const', v: lit, line: line }); lit = ''; }
        var depth = 1, j = i + 1, exprEnd = -1, specStart = -1, conv = null, inStr = null;
        while (j < s.length && depth > 0) {
          var d = s[j];
          if (inStr) { if (d === inStr) inStr = null; j++; continue; }
          if (d === '"' || d === "'") { inStr = d; j++; continue; }
          if (d === '{' || d === '[' || d === '(') depth++;
          else if (d === '}' || d === ']' || d === ')') { depth--; if (depth === 0) break; }
          else if (d === ':' && depth === 1 && specStart < 0) { exprEnd = j; specStart = j + 1; }
          else if (d === '!' && depth === 1 && specStart < 0 && s[j + 1] !== '=') { exprEnd = j; conv = s[j + 1]; j++; }
          j++;
        }
        if (depth !== 0) { var e = new PyErr('SyntaxError', "f-string: expecting '}'"); e.line = line; throw e; }
        var exprSrc = s.slice(i + 1, exprEnd >= 0 ? exprEnd : j), spec = specStart >= 0 ? s.slice(specStart, j) : null;
        var selfDoc = false;
        if (/=\s*$/.test(exprSrc) && !/[=!<>]=\s*$/.test(exprSrc)) { selfDoc = exprSrc; exprSrc = exprSrc.replace(/=\s*$/, ''); }
        var toks = tokenize(exprSrc.trim()); toks = toks.filter(function (t) { return t.t !== 'NEWLINE' && t.t !== 'INDENT' && t.t !== 'DEDENT'; });
        toks.forEach(function (t) { t.line = line; });
        var pp = new Parser(toks), ex = pp.exprList();
        var specNode = spec === null ? null : (spec.indexOf('{') >= 0 ? parseFString(spec, line) : { k: 'const', v: spec, line: line });
        if (selfDoc) parts.push({ k: 'const', v: selfDoc, line: line });
        parts.push({ k: 'fmt', value: ex, spec: specNode, conv: conv || (selfDoc && !spec ? 'r' : null), line: line });
        i = j + 1; continue;
      }
      lit += c; i++;
    }
    if (lit) parts.push({ k: 'const', v: lit, line: line });
    return { k: 'fstring', parts: parts, line: line };
  }

  /* ------------------------------------------------------------------ values */
  function typeName(v) {
    if (v === null) return 'NoneType';
    switch (typeof v) {
      case 'bigint': return 'int'; case 'number': return 'float'; case 'string': return 'str'; case 'boolean': return 'bool';
    }
    if (Array.isArray(v)) return 'list';
    if (v instanceof Tuple) return 'tuple'; if (v instanceof Dict) return 'dict'; if (v instanceof Range) return 'range';
    if (v instanceof Fn) return 'function'; if (v instanceof Builtin || v instanceof BoundMethod) return 'builtin_function_or_method';
    if (v instanceof Module) return 'module'; if (v instanceof ExcType) return 'type'; if (v instanceof ExcVal) return v.type;
    if (v instanceof PySet) return 'set';
    return 'object';
  }
  function PySet(items) { this.m = new Map(); var self = this; (items || []).forEach(function (x) { self.m.set(keyOf(x), x); }); }
  function isNum(v) { return typeof v === 'number' || typeof v === 'bigint' || typeof v === 'boolean'; }
  function toInt(v) { return typeof v === 'boolean' ? (v ? 1n : 0n) : v; }
  function toF(v) { return typeof v === 'number' ? v : Number(toInt(v)); }
  function truthy(v) {
    if (v === null || v === false) return false;
    if (v === true) return true;
    if (typeof v === 'bigint') return v !== 0n;
    if (typeof v === 'number') return v !== 0;
    if (typeof v === 'string') return v.length > 0;
    if (Array.isArray(v)) return v.length > 0;
    if (v instanceof Tuple) return v.a.length > 0;
    if (v instanceof Dict || v instanceof PySet) return v.m.size > 0;
    if (v instanceof Range) return rangeLen(v) > 0;
    return true;
  }
  function repr(v) {
    if (v === null) return 'None';
    if (v === true) return 'True'; if (v === false) return 'False';
    if (typeof v === 'bigint') return v.toString();
    if (typeof v === 'number') return NF.pyRepr(v);
    if (typeof v === 'string') {
      var q = (v.indexOf("'") >= 0 && v.indexOf('"') < 0) ? '"' : "'";
      var body = v.replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/\t/g, '\\t').replace(/\r/g, '\\r');
      if (q === "'") body = body.replace(/'/g, "\\'");
      return q + body + q;
    }
    if (Array.isArray(v)) return '[' + v.map(repr).join(', ') + ']';
    if (v instanceof Tuple) return v.a.length === 1 ? '(' + repr(v.a[0]) + ',)' : '(' + v.a.map(repr).join(', ') + ')';
    if (v instanceof Dict) { var s = []; v.m.forEach(function (e) { s.push(repr(e[0]) + ': ' + repr(e[1])); }); return '{' + s.join(', ') + '}'; }
    if (v instanceof PySet) { if (!v.m.size) return 'set()'; var s2 = []; v.m.forEach(function (e) { s2.push(repr(e)); }); return '{' + s2.join(', ') + '}'; }
    if (v instanceof Range) return 'range(' + v.a + ', ' + v.b + (v.s !== 1n ? ', ' + v.s : '') + ')';
    if (v instanceof Fn) return '<function ' + v.name + '>';
    if (v instanceof Builtin) return '<built-in function ' + v.name + '>';
    if (v instanceof BoundMethod) return '<built-in method ' + v.name + '>';
    if (v instanceof Module) return "<module '" + v.name + "'>";
    if (v instanceof ExcType) return "<class '" + v.name + "'>";
    if (v instanceof ExcVal) return v.type + '(' + repr(v.msg) + ')';
    return '<object>';
  }
  function str(v) { if (typeof v === 'string') return v; if (v instanceof ExcVal) return v.msg; return repr(v); }
  function rangeLen(r) {
    var n = r.s > 0n ? (r.b - r.a + r.s - 1n) / r.s : (r.a - r.b - r.s - 1n) / (-r.s);
    return n < 0n ? 0 : Number(n);
  }
  function iterate(v) {   // returns a JS array (eager) for simplicity
    if (Array.isArray(v)) return v.slice();
    if (v instanceof Tuple) return v.a.slice();
    if (typeof v === 'string') return Array.from(v);
    if (v instanceof Range) { var out = [], n = rangeLen(v), x = v.a; if (n > 5e6) err('MemoryError', 'range too large for MiniPy'); for (var i = 0; i < n; i++) { out.push(x); x += v.s; } return out; }
    if (v instanceof Dict) { var k = []; v.m.forEach(function (e) { k.push(e[0]); }); return k; }
    if (v instanceof PySet) { var s = []; v.m.forEach(function (e) { s.push(e); }); return s; }
    err('TypeError', "'" + typeName(v) + "' object is not iterable");
  }
  function eq(a, b) {
    if (isNum(a) && isNum(b)) {
      if (typeof a === 'number' || typeof b === 'number') return toF(a) === toF(b);
      return toInt(a) === toInt(b);
    }
    if (typeof a === 'string' && typeof b === 'string') return a === b;
    if (a === null || b === null) return a === b;
    if (Array.isArray(a) && Array.isArray(b)) { if (a.length !== b.length) return false; for (var i = 0; i < a.length; i++) if (!eq(a[i], b[i])) return false; return true; }
    if (a instanceof Tuple && b instanceof Tuple) return eq(a.a, b.a);
    if (a instanceof Dict && b instanceof Dict) { if (a.m.size !== b.m.size) return false; var ok = true; a.m.forEach(function (e, k) { var f = b.m.get(k); if (!f || !eq(e[1], f[1])) ok = false; }); return ok; }
    return a === b;
  }
  function cmp(a, b, op) {
    if (isNum(a) && isNum(b)) {
      var x, y;
      if (typeof a === 'number' || typeof b === 'number') { x = toF(a); y = toF(b); } else { x = toInt(a); y = toInt(b); }
      return op === '<' ? x < y : op === '>' ? x > y : op === '<=' ? x <= y : x >= y;
    }
    if (typeof a === 'string' && typeof b === 'string') return op === '<' ? a < b : op === '>' ? a > b : op === '<=' ? a <= b : a >= b;
    if ((Array.isArray(a) && Array.isArray(b)) || (a instanceof Tuple && b instanceof Tuple)) {
      var A = Array.isArray(a) ? a : a.a, B = Array.isArray(b) ? b : b.a;
      for (var i = 0; i < Math.min(A.length, B.length); i++) if (!eq(A[i], B[i])) return cmp(A[i], B[i], op);
      return op === '<' ? A.length < B.length : op === '>' ? A.length > B.length : op === '<=' ? A.length <= B.length : A.length >= B.length;
    }
    err('TypeError', "'" + op + "' not supported between instances of '" + typeName(a) + "' and '" + typeName(b) + "'");
  }
  function floorDivBig(a, b) { var q = a / b; if ((a % b !== 0n) && ((a < 0n) !== (b < 0n))) q -= 1n; return q; }
  function modBig(a, b) { var r = a % b; if (r !== 0n && ((r < 0n) !== (b < 0n))) r += b; return r; }
  function pyFmod(a, b) { var r = a % b; if (r !== 0 && ((b < 0) !== (r < 0))) r += b; else if (r === 0) r = (b < 0 ? -0 : 0); return r; }
  function pyFloorDiv(u, v) {
    var m = u % v, d = (u - m) / v;
    if (m && ((v < 0) !== (m < 0))) d -= 1;
    if (d) { var fd = Math.floor(d); if (d - fd > 0.5) fd += 1; return fd; }
    return (u / v < 0) ? -0 : 0;
  }
  function binop(op, a, b) {
    if (isNum(a) && isNum(b)) {
      if (typeof a !== 'number' && typeof b !== 'number') {
        var x = toInt(a), y = toInt(b);
        switch (op) {
          case '+': return x + y; case '-': return x - y; case '*': return x * y;
          case '/': if (y === 0n) err('ZeroDivisionError', 'division by zero'); return divInts(x, y);
          case '//': if (y === 0n) err('ZeroDivisionError', 'integer division or modulo by zero'); return floorDivBig(x, y);
          case '%': if (y === 0n) err('ZeroDivisionError', 'integer modulo by zero'); return modBig(x, y);
          case '**': if (y < 0n) { if (x === 0n) err('ZeroDivisionError', '0.0 cannot be raised to a negative power'); return Math.pow(Number(x), Number(y)); }
            if (y > 100000n || (x !== 0n && x !== 1n && x !== -1n && y > 20000n)) err('OverflowError', 'number too large for MiniPy'); return x ** y;
          case '&': return x & y; case '|': return x | y; case '^': return x ^ y; case '<<': return x << y; case '>>': return x >> y;
        }
      } else {
        var u = toF(a), v = toF(b);
        switch (op) {
          case '+': return u + v; case '-': return u - v; case '*': return u * v;
          case '/': if (v === 0) err('ZeroDivisionError', 'float division by zero'); return u / v;
          case '//': if (v === 0) err('ZeroDivisionError', 'float floor division by zero'); return pyFloorDiv(u, v);
          case '%': if (v === 0) err('ZeroDivisionError', 'float modulo by zero'); return pyFmod(u, v);
          case '**':
            if (u === 0 && v < 0) err('ZeroDivisionError', 'zero to a negative power');
            if (u < 0 && !Number.isInteger(v)) err('ValueError', 'negative number to a fractional power gives a complex number (not supported in MiniPy)');
            var r = Math.pow(u, v); if (!isFinite(r) && isFinite(u) && isFinite(v)) err('OverflowError', "(34, 'Numerical result out of range')"); return r;
        }
        if (op === '&' || op === '|' || op === '^' || op === '<<' || op === '>>') err('TypeError', "unsupported operand type(s) for " + op + ": '" + typeName(a) + "' and '" + typeName(b) + "'");
      }
    }
    if (op === '+') {
      if (typeof a === 'string' && typeof b === 'string') return a + b;
      if (Array.isArray(a) && Array.isArray(b)) return a.concat(b);
      if (a instanceof Tuple && b instanceof Tuple) return new Tuple(a.a.concat(b.a));
      if (typeof a === 'string' || typeof b === 'string') err('TypeError', typeof a === 'string' ? 'can only concatenate str (not "' + typeName(b) + '") to str' : "unsupported operand type(s) for +: '" + typeName(a) + "' and 'str'");
    }
    if (op === '*') {
      var seq = null, n = null;
      if (isNum(b) && typeof b !== 'number') { seq = a; n = Number(toInt(b)); } else if (isNum(a) && typeof a !== 'number') { seq = b; n = Number(toInt(a)); }
      if (seq !== null) {
        if (typeof seq === 'string') return n > 0 ? seq.repeat(n) : '';
        if (Array.isArray(seq)) { var o = []; for (var i = 0; i < n; i++) o = o.concat(seq); return o; }
        if (seq instanceof Tuple) { var o2 = []; for (var j = 0; j < n; j++) o2 = o2.concat(seq.a); return new Tuple(o2); }
      }
    }
    if (op === '%' && typeof a === 'string') return percentFormat(a, b);
    err('TypeError', "unsupported operand type(s) for " + op + ": '" + typeName(a) + "' and '" + typeName(b) + "'");
  }
  function divInts(x, y) {
    var fx = Number(x), fy = Number(y);
    if (Math.abs(fx) < 9007199254740992 && Math.abs(fy) < 9007199254740992) return fx / fy;
    return Number(x * 1000000000000000000n / y) / 1e18;
  }
  function percentFormat(fmt, args) {
    var list = args instanceof Tuple ? args.a : [args];
    var conv = list.map(function (v) {
      if (typeof v === 'number') return { v: v, t: 'double' };
      if (typeof v === 'bigint' || typeof v === 'boolean') return { v: toInt(v), t: 'int' };
      return { v: str(v), t: 'str' };
    });
    // Python %s with numbers uses str(); %r repr
    fmt = fmt.replace(/%r/g, '%s');
    var k = 0, fixed = fmt.replace(/%([-+ #0]*\d*(?:\.\d+)?)([sdifeEgGxXoc%])/g, function (m0, f, c) {
      if (c === '%') return m0;
      var a = conv[k];
      if (c === 's' && a && a.t !== 'str') { conv[k] = { v: str(list[k]), t: 'str' }; }
      if ((c === 'd' || c === 'i') && a && a.t === 'double') conv[k] = { v: BigInt(Math.trunc(a.v)), t: 'int' };
      k++; return m0;
    });
    if (k < conv.length) err('TypeError', 'not all arguments converted during string formatting');
    if (k > conv.length) err('TypeError', 'not enough arguments for format string');
    return NF.cFormat(fixed, conv);
  }
  function formatValue(v, spec) {
    var kind = typeof v === 'bigint' ? 'int' : typeof v === 'number' ? 'float' : typeof v === 'boolean' ? 'bool' : typeof v === 'string' ? 'str' : 'obj';
    if (spec === '') return str(v);
    try { return NF.pyFormat(v, spec, kind, str); }
    catch (e) { var m = /^(\w+): (.*)$/.exec(e.message); if (m) err(m[1], m[2]); throw e; }
  }

  /* ------------------------------------------------------------------ interpreter */
  function Scope(parent, globals) { this.vars = new Map(); this.parent = parent; this.globals = globals || this; this.globalNames = null; }
  Scope.prototype.lookup = function (name) {
    var s = this;
    if (this.globalNames && this.globalNames.has(name)) s = this.globals;
    for (; s; s = s.parent) if (s.vars.has(name)) return s.vars.get(name);
    if (BUILTINS.has(name)) return BUILTINS.get(name);
    err('NameError', "name '" + name + "' is not defined");
  };
  Scope.prototype.assign = function (name, v) {
    if (this.globalNames && this.globalNames.has(name)) this.globals.vars.set(name, v); else this.vars.set(name, v);
  };
  var BREAK = { b: 1 }, CONTINUE = { c: 1 };
  function Return(v) { this.v = v; }

  function Interp(opts) {
    this.out = []; this.steps = 0; this.maxSteps = opts.maxSteps || 3000000; this.depth = 0;
    this.stdin = (opts.stdin || '').split('\n'); this.stdinPos = 0; this.line = 0; this.outLen = 0;
  }
  var I = Interp.prototype;
  I.write = function (s) {
    this.outLen += s.length;
    if (this.outLen > 200000) err('OutputLimit', 'too much output (over 200,000 characters); is a loop printing too often?');
    this.out.push(s);
  };
  I.tick = function (node) {
    if (node && node.line) this.line = node.line;
    if (++this.steps > this.maxSteps) err('Timeout', 'the program ran for too long (more than ' + this.maxSteps.toLocaleString() + ' steps). Is there an infinite loop?');
  };
  I.execBlock = function (body, sc) {
    for (var i = 0; i < body.length; i++) { var r = this.exec(body[i], sc); if (r !== undefined) return r; }
  };
  I.exec = function (s, sc) {
    this.tick(s);
    switch (s.k) {
      case 'expr': this.eval(s.value, sc); return;
      case 'assign': { var v = this.eval(s.value, sc); for (var i = 0; i < s.targets.length; i++) this.assignTo(s.targets[i], v, sc); return; }
      case 'aug': {
        var t = s.target, cur, rhs;
        if (t.k === 'name') { cur = sc.lookup(t.id); rhs = this.eval(s.value, sc); sc.assign(t.id, this.augOp(s.op, cur, rhs)); return; }
        if (t.k === 'index') {
          var obj = this.eval(t.obj, sc), idx = this.eval(t.idx, sc);
          cur = this.getIndex(obj, idx); rhs = this.eval(s.value, sc); this.setIndex(obj, idx, this.augOp(s.op, cur, rhs)); return;
        }
        err('SyntaxError', 'illegal target for augmented assignment');
      }
      case 'if': if (truthy(this.eval(s.test, sc))) return this.execBlock(s.body, sc); else if (s.orelse) return this.execBlock(s.orelse, sc); return;
      case 'while': {
        while (truthy(this.eval(s.test, sc))) {
          this.tick(s);
          var r = this.execBlock(s.body, sc);
          if (r === BREAK) return; if (r === CONTINUE) continue; if (r !== undefined) return r;
        }
        if (s.orelse) return this.execBlock(s.orelse, sc);
        return;
      }
      case 'for': {
        var items = iterate(this.eval(s.iter, sc));
        for (var j = 0; j < items.length; j++) {
          this.tick(s);
          this.assignTo(s.target, items[j], sc);
          var r2 = this.execBlock(s.body, sc);
          if (r2 === BREAK) return; if (r2 === CONTINUE) continue; if (r2 !== undefined) return r2;
        }
        if (s.orelse) return this.execBlock(s.orelse, sc);
        return;
      }
      case 'break': return BREAK;
      case 'continue': return CONTINUE;
      case 'pass': return;
      case 'return': return new Return(s.value ? this.eval(s.value, sc) : null);
      case 'def': {
        var self = this, defs = s.params.map(function (p) { return p.def ? self.eval(p.def, sc) : undefined; });
        sc.assign(s.name, new Fn(s.name, s.params.map(function (p, i) { return { name: p.name, def: defs[i], star: p.star }; }), s.body, sc, false));
        return;
      }
      case 'global': if (!sc.globalNames) sc.globalNames = new Set(); s.names.forEach(function (n) { sc.globalNames.add(n); }); return;
      case 'import': s.mods.forEach(function (m) { sc.assign(m[1].split('.')[0], getModule(m[0])); }); return;
      case 'from': {
        var mod = getModule(s.mod);
        if (s.items === '*') { Object.keys(mod.attrs).forEach(function (k) { if (k[0] !== '_') sc.assign(k, mod.attrs[k]); }); return; }
        s.items.forEach(function (it) { if (!(it[0] in mod.attrs)) err('ImportError', "cannot import name '" + it[0] + "' from '" + s.mod + "'"); sc.assign(it[1], mod.attrs[it[0]]); });
        return;
      }
      case 'raise': {
        if (!s.exc) err('RuntimeError', 'No active exception to reraise');
        var ex = this.eval(s.exc, sc);
        if (ex instanceof ExcType) err(ex.name, '');
        if (ex instanceof ExcVal) err(ex.type, ex.msg);
        err('TypeError', 'exceptions must derive from BaseException');
      }
      case 'assert': if (!truthy(this.eval(s.test, sc))) err('AssertionError', s.msg ? str(this.eval(s.msg, sc)) : ''); return;
      case 'del': {
        var tg = s.target;
        if (tg.k === 'name') { sc.vars.delete(tg.id); return; }
        if (tg.k === 'index') { var o = this.eval(tg.obj, sc), ix = this.eval(tg.idx, sc);
          if (Array.isArray(o)) { var n = normIdx(o.length, ix); o.splice(n, 1); return; }
          if (o instanceof Dict) { o.m.delete(keyOf(ix)); return; } }
        return;
      }
      case 'try': {
        var res;
        try { res = this.execBlock(s.body, sc); }
        catch (e) {
          if (!(e instanceof PyErr) || e.type === 'Timeout' || e.type === 'OutputLimit') throw e;
          var handled = false;
          for (var h = 0; h < s.handlers.length; h++) {
            var hd = s.handlers[h], match = !hd.type;
            if (hd.type) {
              var tv = this.eval(hd.type, sc), types = tv instanceof Tuple ? tv.a : [tv];
              match = types.some(function (T) { return T instanceof ExcType && excMatches(e.type, T.name); });
            }
            if (match) {
              if (hd.as) sc.assign(hd.as, new ExcVal(e.type, e.msg));
              res = this.execBlock(hd.body, sc); handled = true; break;
            }
          }
          if (!handled) { if (s.fin) this.execBlock(s.fin, sc); throw e; }
          if (s.fin) { var fr = this.execBlock(s.fin, sc); if (fr !== undefined) return fr; }
          return res;
        }
        if (s.orelse && res === undefined) res = this.execBlock(s.orelse, sc);
        if (s.fin) { var fr2 = this.execBlock(s.fin, sc); if (fr2 !== undefined) return fr2; }
        return res;
      }
    }
    err('SyntaxError', 'unsupported statement');
  };
  function excMatches(actual, wanted) {
    if (wanted === 'Exception' || wanted === 'BaseException') return true;
    if (actual === wanted) return true;
    if (wanted === 'ArithmeticError') return /ZeroDivision|Overflow|FloatingPoint/.test(actual);
    if (wanted === 'LookupError') return /IndexError|KeyError/.test(actual);
    return false;
  }
  I.augOp = function (op, a, b) {
    if (Array.isArray(a) && op === '+') { iterate(b).forEach(function (x) { a.push(x); }); return a; }
    return binop(op, a, b);
  };
  I.assignTo = function (t, v, sc) {
    switch (t.k) {
      case 'name': sc.assign(t.id, v); return;
      case 'index': this.setIndex(this.eval(t.obj, sc), this.eval(t.idx, sc), v); return;
      case 'tuple': case 'list': {
        var items = iterate(v), star = -1;
        for (var i = 0; i < t.items.length; i++) if (t.items[i].k === 'starred') star = i;
        if (star < 0) {
          if (items.length !== t.items.length) err('ValueError', items.length > t.items.length ? 'too many values to unpack (expected ' + t.items.length + ')' : 'not enough values to unpack (expected ' + t.items.length + ', got ' + items.length + ')');
          for (var j = 0; j < items.length; j++) this.assignTo(t.items[j], items[j], sc);
        } else {
          var after = t.items.length - star - 1;
          for (var a = 0; a < star; a++) this.assignTo(t.items[a], items[a], sc);
          this.assignTo(t.items[star].value, items.slice(star, items.length - after), sc);
          for (var b = 0; b < after; b++) this.assignTo(t.items[star + 1 + b], items[items.length - after + b], sc);
        }
        return;
      }
      case 'attr': err('AttributeError', 'cannot set attributes in MiniPy');
    }
    err('SyntaxError', 'cannot assign');
  };
  function normIdx(len, idx) {
    if (typeof idx === 'boolean') idx = idx ? 1n : 0n;
    if (typeof idx !== 'bigint') err('TypeError', 'list indices must be integers or slices, not ' + typeName(idx));
    var i = Number(idx); if (i < 0) i += len;
    if (i < 0 || i >= len) err('IndexError', 'list index out of range');
    return i;
  }
  function sliceIdx(len, sl) {
    var step = sl.c === null || sl.c === undefined ? 1 : Number(sl.c);
    if (step === 0) err('ValueError', 'slice step cannot be zero');
    function norm(v, def) {
      if (v === null || v === undefined) return def;
      var x = Number(v); if (x < 0) x += len;
      if (step > 0) return Math.max(0, Math.min(len, x));
      return Math.max(-1, Math.min(len - 1, x));
    }
    var a = norm(sl.a, step > 0 ? 0 : len - 1), b = norm(sl.b, step > 0 ? len : -1), out = [];
    if (step > 0) for (var i = a; i < b; i += step) out.push(i); else for (var j = a; j > b; j += step) out.push(j);
    return out;
  }
  function SliceVal(a, b, c) { this.a = a; this.b = b; this.c = c; }
  I.getIndex = function (o, idx) {
    if (idx instanceof SliceVal) {
      if (typeof o === 'string') { var ix = sliceIdx(o.length, idx); return ix.map(function (i) { return o[i]; }).join(''); }
      var arr = Array.isArray(o) ? o : o instanceof Tuple ? o.a : null;
      if (!arr) err('TypeError', "'" + typeName(o) + "' object is not subscriptable");
      var r = sliceIdx(arr.length, idx).map(function (i) { return arr[i]; });
      return Array.isArray(o) ? r : new Tuple(r);
    }
    if (Array.isArray(o)) return o[normIdx(o.length, idx)];
    if (o instanceof Tuple) { try { return o.a[normIdx(o.a.length, idx)]; } catch (e) { if (e.type === 'IndexError') err('IndexError', 'tuple index out of range'); throw e; } }
    if (typeof o === 'string') { try { return o[normIdx(o.length, idx)]; } catch (e2) { if (e2.type === 'IndexError') err('IndexError', 'string index out of range'); throw e2; } }
    if (o instanceof Dict) { var e3 = o.get(idx); if (!e3) err('KeyError', repr(idx)); return e3[1]; }
    if (o instanceof Range) { var n = normIdx(rangeLen(o), idx); return o.a + BigInt(n) * o.s; }
    err('TypeError', "'" + typeName(o) + "' object is not subscriptable");
  };
  I.setIndex = function (o, idx, v) {
    if (Array.isArray(o)) {
      if (idx instanceof SliceVal) { var ix = sliceIdx(o.length, idx), vals = iterate(v); if ((idx.c === null || idx.c === undefined)) { var a = ix.length ? ix[0] : Math.max(0, Math.min(o.length, idx.a === null ? 0 : Number(idx.a) < 0 ? Number(idx.a) + o.length : Number(idx.a))); o.splice.apply(o, [a, ix.length].concat(vals)); } else ix.forEach(function (i, k) { o[i] = vals[k]; }); return; }
      o[normIdx(o.length, idx)] = v; return;
    }
    if (o instanceof Dict) { o.set(idx, v); return; }
    if (o instanceof Tuple) err('TypeError', "'tuple' object does not support item assignment");
    if (typeof o === 'string') err('TypeError', "'str' object does not support item assignment");
    err('TypeError', "'" + typeName(o) + "' object does not support item assignment");
  };
  I.eval = function (e, sc) {
    switch (e.k) {
      case 'const': return e.v;
      case 'name': this.line = e.line || this.line; return sc.lookup(e.id);
      case 'bin': { this.tick(e); var a = this.eval(e.a, sc), b = this.eval(e.b, sc); return binop(e.op, a, b); }
      case 'unary': {
        var v = this.eval(e.a, sc);
        if (e.op === '-') { if (typeof v === 'number') return -v; if (isNum(v)) return -toInt(v); err('TypeError', "bad operand type for unary -: '" + typeName(v) + "'"); }
        if (e.op === '+') { if (isNum(v)) return typeof v === 'boolean' ? toInt(v) : v; err('TypeError', "bad operand type for unary +: '" + typeName(v) + "'"); }
        if (e.op === '~') return ~toInt(v);
      }
      case 'not': return !truthy(this.eval(e.a, sc));
      case 'and': { var l = this.eval(e.a, sc); return truthy(l) ? this.eval(e.b, sc) : l; }
      case 'or': { var l2 = this.eval(e.a, sc); return truthy(l2) ? l2 : this.eval(e.b, sc); }
      case 'compare': {
        var left = this.eval(e.first, sc);
        for (var i = 0; i < e.ops.length; i++) {
          var right = this.eval(e.rest[i], sc), op = e.ops[i], r;
          switch (op) {
            case '==': r = eq(left, right); break; case '!=': r = !eq(left, right); break;
            case 'in': r = contains(right, left); break; case 'not in': r = !contains(right, left); break;
            case 'is': r = left === right || (left === null && right === null); break;
            case 'is not': r = !(left === right || (left === null && right === null)); break;
            default: r = cmp(left, right, op);
          }
          if (!r) return false;
          left = right;
        }
        return true;
      }
      case 'ifexp': return truthy(this.eval(e.test, sc)) ? this.eval(e.body, sc) : this.eval(e.orelse, sc);
      case 'tuple': return new Tuple(this.evalItems(e.items, sc));
      case 'list': return this.evalItems(e.items, sc);
      case 'set': return new PySet(this.evalItems(e.items, sc));
      case 'dict': { var d = new Dict(); for (var k = 0; k < e.keys.length; k++) d.set(this.eval(e.keys[k], sc), this.eval(e.vals[k], sc)); return d; }
      case 'index': {
        var o = this.eval(e.obj, sc), idx;
        if (e.idx.k === 'slice') idx = new SliceVal(e.idx.a ? this.sliceNum(e.idx.a, sc) : null, e.idx.b ? this.sliceNum(e.idx.b, sc) : null, e.idx.c ? this.sliceNum(e.idx.c, sc) : null);
        else if (e.idx.k === 'tuple' && Array.isArray(o)) err('TypeError', 'list indices must be integers or slices, not tuple (use A[i][j] for a list of lists)');
        else idx = this.eval(e.idx, sc);
        return this.getIndex(o, idx);
      }
      case 'attr': { var ob = this.eval(e.obj, sc); return getAttr(ob, e.name); }
      case 'call': {
        this.tick(e);
        var fn = this.eval(e.fn, sc), args = [], self = this;
        e.args.forEach(function (a) { if (a.k === 'starred') args.push.apply(args, iterate(self.eval(a.value, sc))); else args.push(self.eval(a, sc)); });
        var kw = null;
        if (e.kw.length) { kw = {}; e.kw.forEach(function (p) { kw[p[0]] = self.eval(p[1], sc); }); }
        this.line = e.line;
        return this.call(fn, args, kw, e.line);
      }
      case 'lambda': {
        var self2 = this, defs = e.params.map(function (p) { return p.def ? self2.eval(p.def, sc) : undefined; });
        return new Fn('<lambda>', e.params.map(function (p, i) { return { name: p.name, def: defs[i], star: p.star }; }), e.body, sc, true);
      }
      case 'fstring': {
        var s = '';
        for (var j = 0; j < e.parts.length; j++) {
          var p = e.parts[j];
          if (p.k === 'const') { s += p.v; continue; }
          var val = this.eval(p.value, sc);
          if (p.conv === 'r') val = repr(val); else if (p.conv === 's') val = str(val);
          var spec = p.spec ? str(this.eval(p.spec, sc)) : '';
          s += formatValue(val, spec);
        }
        return s;
      }
      case 'fmt': return formatValue(this.eval(e.value, sc), '');
      case 'concat': { var out = ''; for (var c = 0; c < e.parts.length; c++) out += this.eval(e.parts[c], sc); return out; }
      case 'comp': return this.comp(e, sc);
      case 'starred': err('SyntaxError', 'can\'t use starred expression here');
      case 'slice': err('SyntaxError', 'invalid slice');
    }
    err('SyntaxError', 'unsupported expression ' + e.k);
  };
  I.sliceNum = function (n, sc) { var v = this.eval(n, sc); if (v === null) return null; if (!isNum(v) || typeof v === 'number') err('TypeError', 'slice indices must be integers or None'); return toInt(v); };
  I.evalItems = function (items, sc) {
    var out = [], self = this;
    items.forEach(function (it) { if (it.k === 'starred') out.push.apply(out, iterate(self.eval(it.value, sc))); else out.push(self.eval(it, sc)); });
    return out;
  };
  I.comp = function (e, sc) {
    var inner = new Scope(sc, sc.globals), out = [], d = new Dict(), self = this;
    function rec(gi) {
      if (gi === e.gens.length) {
        self.tick(e);
        if (e.kind === 'dict') d.set(self.eval(e.elt, inner), self.eval(e.val, inner));
        else out.push(self.eval(e.elt, inner));
        return;
      }
      var g = e.gens[gi], items = iterate(self.eval(g.iter, gi === 0 ? sc : inner));
      for (var i = 0; i < items.length; i++) {
        self.assignTo(g.target, items[i], inner);
        var ok = true;
        for (var j = 0; j < g.ifs.length; j++) if (!truthy(self.eval(g.ifs[j], inner))) { ok = false; break; }
        if (ok) rec(gi + 1);
      }
    }
    rec(0);
    if (e.kind === 'dict') return d;
    if (e.kind === 'set') return new PySet(out);
    return out;   // list or generator (eager)
  };
  I.call = function (fn, args, kw, line) {
    if (fn instanceof Builtin) return fn.f.call(this, args, kw || {});
    if (fn instanceof BoundMethod) return fn.f.call(this, fn.self, args, kw || {});
    if (fn instanceof ExcType) return new ExcVal(fn.name, args.length ? str(args[0]) : '');
    if (!(fn instanceof Fn)) err('TypeError', "'" + typeName(fn) + "' object is not callable");
    if (++this.depth > 900) { this.depth = 0; err('RecursionError', 'maximum recursion depth exceeded'); }
    var sc = new Scope(fn.closure, fn.closure.globals), ps = fn.params, used = {};
    var star = null;
    for (var i = 0; i < ps.length; i++) {
      var p = ps[i];
      if (p.star === '*') { star = p; sc.vars.set(p.name, new Tuple(args.slice(i))); used[p.name] = 1; break; }
      if (p.star === '**') continue;
      if (i < args.length) { sc.vars.set(p.name, args[i]); used[p.name] = 1; }
    }
    if (!star && args.length > ps.filter(function (p) { return !p.star; }).length) err('TypeError', fn.name + '() takes ' + ps.length + ' positional argument' + (ps.length === 1 ? '' : 's') + ' but ' + args.length + (args.length === 1 ? ' was' : ' were') + ' given');
    if (kw) for (var k in kw) {
      var found = ps.some(function (p) { return p.name === k && !p.star; });
      if (!found) err('TypeError', fn.name + "() got an unexpected keyword argument '" + k + "'");
      if (used[k]) err('TypeError', fn.name + "() got multiple values for argument '" + k + "'");
      sc.vars.set(k, kw[k]); used[k] = 1;
    }
    for (var j = 0; j < ps.length; j++) {
      if (ps[j].star) continue;
      if (!used[ps[j].name]) {
        if (ps[j].def === undefined) err('TypeError', fn.name + "() missing 1 required positional argument: '" + ps[j].name + "'");
        sc.vars.set(ps[j].name, ps[j].def);
      }
    }
    var result = null;
    try {
      if (fn.isLambda) result = this.eval(fn.body, sc);
      else { var r = this.execBlock(fn.body, sc); if (r instanceof Return) result = r.v; }
    } finally { this.depth--; }
    return result;
  };
  function contains(c, x) {
    if (typeof c === 'string') { if (typeof x !== 'string') err('TypeError', "'in <string>' requires string as left operand, not " + typeName(x)); return c.indexOf(x) >= 0; }
    if (c instanceof Dict) return c.m.has(keyOf(x));
    if (c instanceof PySet) return c.m.has(keyOf(x));
    if (c instanceof Range) { if (!isNum(x)) return false; var v = toInt(typeof x === 'number' ? (Number.isInteger(x) ? BigInt(x) : null) : x); if (v === null) return false; return c.s > 0n ? (v >= c.a && v < c.b && (v - c.a) % c.s === 0n) : (v <= c.a && v > c.b && (c.a - v) % (-c.s) === 0n); }
    return iterate(c).some(function (y) { return eq(x, y); });
  }

  /* ------------------------------------------------------------------ attributes & methods */
  function method(self, name, f) { return new BoundMethod(self, name, f); }
  function getAttr(o, name) {
    if (o instanceof Module) { if (name in o.attrs) return o.attrs[name]; err('AttributeError', "module '" + o.name + "' has no attribute '" + name + "'"); }
    if (Array.isArray(o)) {
      var LM = LIST_METHODS[name]; if (LM) return method(o, 'list.' + name, LM);
    } else if (typeof o === 'string') {
      var SM = STR_METHODS[name]; if (SM) return method(o, 'str.' + name, SM);
    } else if (o instanceof Dict) {
      var DM = DICT_METHODS[name]; if (DM) return method(o, 'dict.' + name, DM);
    } else if (o instanceof PySet) {
      if (name === 'add') return method(o, 'set.add', function (s, a) { s.m.set(keyOf(a[0]), a[0]); return null; });
    } else if (typeof o === 'number') {
      if (name === 'is_integer') return method(o, 'float.is_integer', function (s) { return Number.isInteger(s); });
      if (name === 'real') return o; if (name === 'imag') return 0;
    } else if (o instanceof ExcVal) { if (name === 'args') return new Tuple([o.msg]); }
    else if (o instanceof Tuple) {
      if (name === 'index') return method(o, 'tuple.index', function (s, a) { for (var i = 0; i < s.a.length; i++) if (eq(s.a[i], a[0])) return BigInt(i); err('ValueError', 'tuple.index(x): x not in tuple'); });
      if (name === 'count') return method(o, 'tuple.count', function (s, a) { return BigInt(s.a.filter(function (y) { return eq(y, a[0]); }).length); });
    }
    err('AttributeError', "'" + typeName(o) + "' object has no attribute '" + name + "'");
  }
  function sortKeyed(interp, arr, kw) {
    var key = kw.key || null, rev = kw.reverse ? truthy(kw.reverse) : false;
    var dec = arr.map(function (v, i) { return { v: v, k: key ? interp.call(key, [v]) : v, i: i }; });
    dec.sort(function (a, b) { if (eq(a.k, b.k)) return a.i - b.i; return cmp(a.k, b.k, '<') ? (rev ? 1 : -1) : (rev ? -1 : 1); });
    return dec.map(function (d) { return d.v; });
  }
  var LIST_METHODS = {
    append: function (s, a) { s.push(a[0]); return null; },
    extend: function (s, a) { iterate(a[0]).forEach(function (x) { s.push(x); }); return null; },
    insert: function (s, a) { var i = Number(toInt(a[0])); if (i < 0) i = Math.max(0, i + s.length); s.splice(Math.min(i, s.length), 0, a[1]); return null; },
    pop: function (s, a) { if (!s.length) err('IndexError', 'pop from empty list'); if (!a.length) return s.pop(); var i = normIdx(s.length, a[0]); return s.splice(i, 1)[0]; },
    remove: function (s, a) { for (var i = 0; i < s.length; i++) if (eq(s[i], a[0])) { s.splice(i, 1); return null; } err('ValueError', 'list.remove(x): x not in list'); },
    index: function (s, a) { for (var i = 0; i < s.length; i++) if (eq(s[i], a[0])) return BigInt(i); err('ValueError', repr(a[0]) + ' is not in list'); },
    count: function (s, a) { return BigInt(s.filter(function (y) { return eq(y, a[0]); }).length); },
    reverse: function (s) { s.reverse(); return null; },
    sort: function (s, a, kw) { var r = sortKeyed(this, s, kw); for (var i = 0; i < r.length; i++) s[i] = r[i]; return null; },
    copy: function (s) { return s.slice(); },
    clear: function (s) { s.length = 0; return null; }
  };
  var STR_METHODS = {
    upper: function (s) { return s.toUpperCase(); }, lower: function (s) { return s.toLowerCase(); },
    strip: function (s, a) { return a.length && a[0] !== null ? s.replace(new RegExp('^[' + esc(a[0]) + ']+|[' + esc(a[0]) + ']+$', 'g'), '') : s.trim(); },
    lstrip: function (s) { return s.replace(/^\s+/, ''); }, rstrip: function (s) { return s.replace(/\s+$/, ''); },
    split: function (s, a) { if (!a.length || a[0] === null) return s.trim() === '' ? [] : s.trim().split(/\s+/); return s.split(a[0]); },
    join: function (s, a) { return iterate(a[0]).map(function (x) { if (typeof x !== 'string') err('TypeError', 'sequence item: expected str instance, ' + typeName(x) + ' found'); return x; }).join(s); },
    replace: function (s, a) { return s.split(a[0]).join(a[1]); },
    startswith: function (s, a) { return s.indexOf(a[0]) === 0; }, endswith: function (s, a) { return s.slice(-a[0].length) === a[0] || a[0] === ''; },
    find: function (s, a) { return BigInt(s.indexOf(a[0])); }, count: function (s, a) { return BigInt(s.split(a[0]).length - 1); },
    center: function (s, a) { var w = Number(a[0]), f = a[1] || ' ', n = w - s.length; if (n <= 0) return s; var l = Math.floor(n / 2) + (n % 2 && w % 2 ? 1 : 0); l = Math.floor(n / 2) + ((n & w & 1) ? 1 : 0); return f.repeat(l) + s + f.repeat(n - l); },
    ljust: function (s, a) { return s + (a[1] || ' ').repeat(Math.max(0, Number(a[0]) - s.length)); },
    rjust: function (s, a) { return (a[1] || ' ').repeat(Math.max(0, Number(a[0]) - s.length)) + s; },
    zfill: function (s, a) { var w = Number(a[0]); var sign = /^[-+]/.test(s) ? s[0] : ''; var b = sign ? s.slice(1) : s; return sign + '0'.repeat(Math.max(0, w - s.length)) + b; },
    isdigit: function (s) { return /^\d+$/.test(s); }, isalpha: function (s) { return /^[A-Za-z]+$/.test(s); },
    title: function (s) { return s.replace(/\w\S*/g, function (w) { return w[0].toUpperCase() + w.slice(1).toLowerCase(); }); },
    capitalize: function (s) { return s ? s[0].toUpperCase() + s.slice(1).toLowerCase() : s; },
    format: function (s, a, kw) {
      var auto = 0;
      return s.replace(/\{\{|\}\}|\{([^{}:!]*)(?:!([rs]))?(?::([^{}]*))?\}/g, function (m0, f, conv, spec) {
        if (m0 === '{{') return '{'; if (m0 === '}}') return '}';
        var v = f === '' ? a[auto++] : /^\d+$/.test(f) ? a[parseInt(f, 10)] : kw[f];
        if (v === undefined) err('IndexError', 'Replacement index out of range for positional args tuple');
        if (conv === 'r') v = repr(v);
        return formatValue(v, spec || '');
      });
    }
  };
  function esc(s) { return s.replace(/[\]\\^-]/g, '\\$&'); }
  var DICT_METHODS = {
    get: function (s, a) { var e = s.get(a[0]); return e ? e[1] : (a.length > 1 ? a[1] : null); },
    keys: function (s) { var k = []; s.m.forEach(function (e) { k.push(e[0]); }); return k; },
    values: function (s) { var k = []; s.m.forEach(function (e) { k.push(e[1]); }); return k; },
    items: function (s) { var k = []; s.m.forEach(function (e) { k.push(new Tuple([e[0], e[1]])); }); return k; },
    update: function (s, a) { a[0].m.forEach(function (e) { s.set(e[0], e[1]); }); return null; },
    pop: function (s, a) { var e = s.get(a[0]); if (!e) { if (a.length > 1) return a[1]; err('KeyError', repr(a[0])); } s.m.delete(keyOf(a[0])); return e[1]; },
    setdefault: function (s, a) { var e = s.get(a[0]); if (e) return e[1]; s.set(a[0], a.length > 1 ? a[1] : null); return a.length > 1 ? a[1] : null; }
  };

  /* ------------------------------------------------------------------ builtins */
  var BUILTINS = new Map();
  function def(name, f) { BUILTINS.set(name, new Builtin(name, f)); }
  def('print', function (a, kw) {
    var sep = kw.sep === undefined || kw.sep === null ? ' ' : kw.sep, end = kw.end === undefined || kw.end === null ? '\n' : kw.end;
    this.write(a.map(str).join(sep) + end); return null;
  });
  def('input', function (a) { if (a.length) this.write(str(a[0])); if (this.stdinPos >= this.stdin.length || (this.stdinPos === this.stdin.length - 1 && this.stdin[this.stdinPos] === '')) err('EOFError', 'EOF when reading a line (type the input in the box below the code)'); var l = this.stdin[this.stdinPos++]; this.write(l + '\n'); return l; });
  def('range', function (a) {
    a = a.map(function (x) { if (typeof x === 'number') err('TypeError', "'float' object cannot be interpreted as an integer"); return toInt(x); });
    if (a.length === 1) return new Range(0n, a[0], 1n);
    if (a.length === 2) return new Range(a[0], a[1], 1n);
    if (a[2] === 0n) err('ValueError', 'range() arg 3 must not be zero');
    return new Range(a[0], a[1], a[2]);
  });
  def('len', function (a) {
    var o = a[0];
    if (typeof o === 'string' || Array.isArray(o)) return BigInt(o.length);
    if (o instanceof Tuple) return BigInt(o.a.length); if (o instanceof Dict || o instanceof PySet) return BigInt(o.m.size);
    if (o instanceof Range) return BigInt(rangeLen(o));
    err('TypeError', "object of type '" + typeName(o) + "' has no len()");
  });
  def('abs', function (a) { var v = a[0]; if (typeof v === 'number') return Math.abs(v); if (isNum(v)) { v = toInt(v); return v < 0n ? -v : v; } err('TypeError', "bad operand type for abs(): '" + typeName(v) + "'"); });
  function minmax(a, kw, isMax) {
    var items = a.length === 1 ? iterate(a[0]) : a;
    if (!items.length) { if ('default' in kw) return kw.default; err('ValueError', (isMax ? 'max' : 'min') + '() arg is an empty sequence'); }
    var best = items[0], bk = kw.key ? this.call(kw.key, [best]) : best;
    for (var i = 1; i < items.length; i++) { var k = kw.key ? this.call(kw.key, [items[i]]) : items[i]; if (cmp(k, bk, isMax ? '>' : '<')) { best = items[i]; bk = k; } }
    return best;
  }
  def('min', function (a, kw) { return minmax.call(this, a, kw, false); });
  def('max', function (a, kw) { return minmax.call(this, a, kw, true); });
  def('sum', function (a, kw) {   /* mirrors CPython 3.12+: exact int fast path, Neumaier-compensated float path */
    var items = iterate(a[0]), s = a.length > 1 ? a[1] : (kw.start !== undefined ? kw.start : 0n), i = 0, n = items.length;
    if (typeof s === 'bigint') {
      while (i < n && typeof items[i] === 'bigint') { s += items[i]; i++; }
      if (i === n) return s;
      if (typeof items[i] === 'number') { s = Number(s); } else { for (; i < n; i++) s = binop('+', s, items[i]); return s; }
    }
    if (typeof s === 'number') {
      var hi = s, c = 0;
      for (; i < n; i++) {
        var x = items[i];
        if (typeof x === 'number') { var t = hi + x; if (Math.abs(hi) >= Math.abs(x)) c += (hi - t) + x; else c += (x - t) + hi; hi = t; continue; }
        if (typeof x === 'bigint' && x >= -9223372036854775808n && x <= 9223372036854775807n) { hi += Number(x); continue; }
        break;
      }
      if (c && isFinite(c)) hi += c;
      s = hi;
      if (i === n) return s;
    }
    for (; i < n; i++) s = binop('+', s, items[i]);
    return s;
  });
  def('round', function (a) {
    var x = a[0];
    if (a.length < 2 || a[1] === null) { if (typeof x === 'number') { if (!isFinite(x)) err(x !== x ? 'ValueError' : 'OverflowError', x !== x ? 'cannot convert float NaN to integer' : 'cannot convert float infinity to integer'); return NF.roundInt(x); } return toInt(x); }
    var nd = Number(toInt(a[1]));
    if (typeof x === 'number') return NF.roundHalfEven(x, nd);
    if (nd >= 0) return toInt(x);
    var f = 10n ** BigInt(-nd), xi = toInt(x), q = floorDivBig(xi, f), r = xi - q * f;
    if (2n * r > f || (2n * r === f && (q & 1n) === 1n)) q += 1n; return q * f;
  });
  def('int', function (a) {
    if (!a.length) return 0n;
    var v = a[0];
    if (typeof v === 'number') { if (!isFinite(v)) err(v !== v ? 'ValueError' : 'OverflowError', v !== v ? 'cannot convert float NaN to integer' : 'cannot convert float infinity to integer'); return BigInt(Math.trunc(v)); }
    if (typeof v === 'string') { var t = v.trim().replace(/_/g, ''); var base = a.length > 1 ? Number(toInt(a[1])) : 10;
      if (base === 10 && !/^[-+]?\d+$/.test(t)) err('ValueError', "invalid literal for int() with base 10: " + repr(v));
      if (base === 10) return BigInt(t); var n = parseInt(t, base); if (isNaN(n)) err('ValueError', 'invalid literal for int() with base ' + base + ': ' + repr(v)); return BigInt(n); }
    if (isNum(v)) return toInt(v);
    err('TypeError', "int() argument must be a string or a number, not '" + typeName(v) + "'");
  });
  def('float', function (a) {
    if (!a.length) return 0;
    var v = a[0];
    if (typeof v === 'string') {
      var t = v.trim().toLowerCase().replace(/_/g, '');
      if (t === 'inf' || t === '+inf' || t === 'infinity') return Infinity; if (t === '-inf' || t === '-infinity') return -Infinity; if (t === 'nan') return NaN;
      if (!/^[-+]?(\d+\.?\d*|\.\d+)(e[-+]?\d+)?$/.test(t)) err('ValueError', 'could not convert string to float: ' + repr(v));
      return parseFloat(t);
    }
    if (isNum(v)) return toF(v);
    err('TypeError', "float() argument must be a string or a real number, not '" + typeName(v) + "'");
  });
  def('str', function (a) { return a.length ? str(a[0]) : ''; });
  def('repr', function (a) { return repr(a[0]); });
  def('bool', function (a) { return a.length ? truthy(a[0]) : false; });
  def('list', function (a) { return a.length ? iterate(a[0]) : []; });
  def('tuple', function (a) { return new Tuple(a.length ? iterate(a[0]) : []); });
  def('set', function (a) { return new PySet(a.length ? iterate(a[0]) : []); });
  def('dict', function (a, kw) { var d = new Dict(); if (a.length) { if (a[0] instanceof Dict) a[0].m.forEach(function (e) { d.set(e[0], e[1]); }); else iterate(a[0]).forEach(function (p) { var it = iterate(p); d.set(it[0], it[1]); }); } for (var k in kw) d.set(k, kw[k]); return d; });
  def('zip', function (a) { var ls = a.map(iterate), n = Math.min.apply(null, ls.map(function (l) { return l.length; })), out = []; if (!ls.length) return out; for (var i = 0; i < n; i++) out.push(new Tuple(ls.map(function (l) { return l[i]; }))); return out; });
  def('enumerate', function (a, kw) { var st = a.length > 1 ? toInt(a[1]) : (kw.start !== undefined ? toInt(kw.start) : 0n); return iterate(a[0]).map(function (x, i) { return new Tuple([st + BigInt(i), x]); }); });
  def('reversed', function (a) { return iterate(a[0]).reverse(); });
  def('sorted', function (a, kw) { return sortKeyed(this, iterate(a[0]), kw); });
  def('map', function (a) { var self = this, ls = a.slice(1).map(iterate), n = Math.min.apply(null, ls.map(function (l) { return l.length; })), out = []; for (var i = 0; i < n; i++) out.push(self.call(a[0], ls.map(function (l) { return l[i]; }))); return out; });
  def('filter', function (a) { var self = this; return iterate(a[1]).filter(function (x) { return a[0] === null ? truthy(x) : truthy(self.call(a[0], [x])); }); });
  def('any', function (a) { return iterate(a[0]).some(truthy); });
  def('all', function (a) { return iterate(a[0]).every(truthy); });
  def('pow', function (a) { return binop('**', a[0], a[1]); });
  def('divmod', function (a) { return new Tuple([binop('//', a[0], a[1]), binop('%', a[0], a[1])]); });
  def('isinstance', function (a) {
    var t = a[1], names = t instanceof Tuple ? t.a : [t], tn = typeName(a[0]);
    return names.some(function (b) { var n = b instanceof Builtin ? b.name : b instanceof ExcType ? b.name : ''; return n === tn || (n === 'int' && tn === 'bool'); });
  });
  def('type', function (a) { var tn = typeName(a[0]); return new ExcType(tn); });
  def('chr', function (a) { return String.fromCharCode(Number(toInt(a[0]))); });
  def('ord', function (a) { return BigInt(a[0].charCodeAt(0)); });
  def('hex', function (a) { var v = toInt(a[0]); return (v < 0n ? '-0x' + (-v).toString(16) : '0x' + v.toString(16)); });
  def('bin', function (a) { var v = toInt(a[0]); return (v < 0n ? '-0b' + (-v).toString(2) : '0b' + v.toString(2)); });
  def('format', function (a) { return formatValue(a[0], a.length > 1 ? a[1] : ''); });
  ['Exception', 'ValueError', 'ZeroDivisionError', 'TypeError', 'IndexError', 'KeyError', 'RuntimeError', 'OverflowError', 'ArithmeticError', 'NameError', 'AssertionError', 'StopIteration', 'NotImplementedError', 'LookupError', 'RecursionError']
    .forEach(function (n) { BUILTINS.set(n, new ExcType(n)); });

  /* ------------------------------------------------------------------ modules */
  function mf(name, f, check) {
    return new Builtin(name, function (a) {
      var xs = a.map(function (v) { if (!isNum(v)) err('TypeError', 'must be real number, not ' + typeName(v)); return toF(v); });
      return f.apply(null, xs);
    });
  }
  function dom() { err('ValueError', 'math domain error'); }
  function rng() { err('OverflowError', 'math range error'); }
  var MATH = {
    pi: Math.PI, e: Math.E, tau: 2 * Math.PI, inf: Infinity, nan: NaN,
    sqrt: mf('sqrt', function (x) { if (x < 0) dom(); return Math.sqrt(x); }),
    exp: mf('exp', function (x) { var r = Math.exp(x); if (r === Infinity && x !== Infinity) rng(); return r; }),
    log: mf('log', function (x, b) { if (x <= 0 || (b !== undefined && (b <= 0 || b === 1))) dom(); return b === undefined ? Math.log(x) : Math.log(x) / Math.log(b); }),
    log10: mf('log10', function (x) { if (x <= 0) dom(); return Math.log10(x); }),
    log2: mf('log2', function (x) { if (x <= 0) dom(); return Math.log2(x); }),
    log1p: mf('log1p', function (x) { if (x <= -1) dom(); return Math.log1p(x); }),
    expm1: mf('expm1', Math.expm1),
    sin: mf('sin', Math.sin), cos: mf('cos', Math.cos), tan: mf('tan', Math.tan),
    asin: mf('asin', function (x) { if (x < -1 || x > 1) dom(); return Math.asin(x); }),
    acos: mf('acos', function (x) { if (x < -1 || x > 1) dom(); return Math.acos(x); }),
    atan: mf('atan', Math.atan), atan2: mf('atan2', Math.atan2),
    sinh: mf('sinh', Math.sinh), cosh: mf('cosh', Math.cosh), tanh: mf('tanh', Math.tanh),
    fabs: mf('fabs', Math.abs), hypot: mf('hypot', Math.hypot),
    pow: mf('pow', function (x, y) { if (x < 0 && !Number.isInteger(y)) dom(); var r = Math.pow(x, y); if (!isFinite(r) && isFinite(x) && isFinite(y)) { if (x === 0) dom(); rng(); } return r; }),
    degrees: mf('degrees', function (x) { return x * 180 / Math.PI; }), radians: mf('radians', function (x) { return x * Math.PI / 180; }),
    isclose: new Builtin('isclose', function (a, kw) { var x = toF(a[0]), y = toF(a[1]), rt = kw.rel_tol !== undefined ? toF(kw.rel_tol) : 1e-9, at = kw.abs_tol !== undefined ? toF(kw.abs_tol) : 0; return x === y || Math.abs(x - y) <= Math.max(rt * Math.max(Math.abs(x), Math.abs(y)), at); }),
    isfinite: mf('isfinite', function (x) { return isFinite(x); }), isnan: mf('isnan', function (x) { return x !== x; }), isinf: mf('isinf', function (x) { return x === Infinity || x === -Infinity; }),
    floor: new Builtin('floor', function (a) { var v = a[0]; if (typeof v === 'number') { if (!isFinite(v)) err('OverflowError', 'cannot convert float infinity to integer'); return BigInt(Math.floor(v)); } return toInt(v); }),
    ceil: new Builtin('ceil', function (a) { var v = a[0]; if (typeof v === 'number') { if (!isFinite(v)) err('OverflowError', 'cannot convert float infinity to integer'); return BigInt(Math.ceil(v)); } return toInt(v); }),
    trunc: new Builtin('trunc', function (a) { var v = a[0]; return typeof v === 'number' ? BigInt(Math.trunc(v)) : toInt(v); }),
    factorial: new Builtin('factorial', function (a) { var v = a[0]; if (typeof v === 'number') err('TypeError', "'float' object cannot be interpreted as an integer"); v = toInt(v); if (v < 0n) err('ValueError', 'factorial() not defined for negative values'); var r = 1n; for (var i = 2n; i <= v; i++) r *= i; return r; }),
    comb: new Builtin('comb', function (a) { var n = toInt(a[0]), k = toInt(a[1]); if (k < 0n || k > n) return 0n; var r = 1n; for (var i = 1n; i <= k; i++) r = r * (n - k + i) / i; return r; }),
    gcd: new Builtin('gcd', function (a) { var x = toInt(a[0]), y = toInt(a[1]); if (x < 0n) x = -x; if (y < 0n) y = -y; while (y) { var t = x % y; x = y; y = t; } return x; }),
    fsum: new Builtin('fsum', function (a) {   /* Shewchuk exact summation, as in CPython math.fsum */
      var p = [];
      iterate(a[0]).forEach(function (v) {
        var x = toF(v), i = 0;
        for (var j = 0; j < p.length; j++) {
          var y = p[j];
          if (Math.abs(x) < Math.abs(y)) { var tmp = x; x = y; y = tmp; }
          var hi = x + y, lo = y - (hi - x);
          if (lo !== 0) p[i++] = lo;
          x = hi;
        }
        p.length = i; p.push(x);
      });
      var n = p.length, hi2 = 0, lo2 = 0;
      if (n > 0) {
        hi2 = p[--n];
        while (n > 0) { var x2 = hi2, y2 = p[--n]; hi2 = x2 + y2; var yr = hi2 - x2; lo2 = y2 - yr; if (lo2 !== 0) break; }
        if (n > 0 && ((lo2 < 0 && p[n - 1] < 0) || (lo2 > 0 && p[n - 1] > 0))) { var y3 = lo2 * 2, x3 = hi2 + y3, yr3 = x3 - hi2; if (y3 === yr3) hi2 = x3; }
      }
      return hi2;
    }),
    copysign: mf('copysign', function (x, y) { return (y < 0 || (y === 0 && 1 / y < 0)) ? -Math.abs(x) : Math.abs(x); }),
    ulp: mf('ulp', function (x) { x = Math.abs(x); if (!isFinite(x)) return x; if (x === 0) return 5e-324; var e = Math.floor(Math.log2(x)); var u = Math.pow(2, e - 52); while (x + u === x) u *= 2; while (u > 5e-324 && x + u / 2 !== x && (x + u / 2) - x === u / 2) u /= 2; return u; }),
    nextafter: mf('nextafter', function (x, y) { if (x === y) return y; var dv = new DataView(new ArrayBuffer(8)); if (x === 0) return y > 0 ? 5e-324 : -5e-324; dv.setFloat64(0, x); var b = dv.getBigUint64(0); b += ((y > x) === (x > 0)) ? 1n : -1n; dv.setBigUint64(0, b); return dv.getFloat64(0); })
  };
  var SYS = { float_info: null };
  var MODULES = {
    math: function () { return new Module('math', MATH); },
    sys: function () {
      var fi = new Module('sys.float_info', { epsilon: Math.pow(2, -52), max: Number.MAX_VALUE, min: 2.2250738585072014e-308, dig: 15n, mant_dig: 53n });
      return new Module('sys', { float_info: fi, maxsize: 9223372036854775807n });
    },
    random: function () {
      var seed = 12345;
      function rnd() { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; }
      return new Module('random', {
        seed: new Builtin('seed', function (a) { seed = Number(toInt(a[0] || 0n)) % 2147483648; return null; }),
        random: new Builtin('random', function () { return rnd(); }),
        uniform: new Builtin('uniform', function (a) { var lo = toF(a[0]), hi = toF(a[1]); return lo + (hi - lo) * rnd(); }),
        randint: new Builtin('randint', function (a) { var lo = Number(toInt(a[0])), hi = Number(toInt(a[1])); return BigInt(lo + Math.floor(rnd() * (hi - lo + 1))); }),
        gauss: new Builtin('gauss', function (a) { var u = rnd() || 1e-12, v = rnd(); return toF(a[0] || 0) + toF(a[1] === undefined ? 1 : a[1]) * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); })
      });
    }
  };
  var modCache = {};
  function getModule(name) {
    if (name === 'numpy' || name === 'scipy' || name === 'matplotlib' || name.indexOf('matplotlib') === 0 || name.indexOf('scipy') === 0 || name.indexOf('numpy') === 0)
      err('ModuleNotFoundError', "No module named '" + name + "' in the browser runner. Run this one in Jupyter on the lab PC; here, write the loops yourself with lists");
    if (!MODULES[name]) err('ModuleNotFoundError', "No module named '" + name + "'");
    return modCache[name] || (modCache[name] = MODULES[name]());
  }

  /* ------------------------------------------------------------------ public API */
  function run(src, opts) {
    opts = opts || {};
    var it = new Interp(opts), errorText = null, errLine = null, t0 = Date.now();
    try {
      var toks = tokenize(src), ast = new Parser(toks).program();
      var g = new Scope(null); g.globals = g;
      g.vars.set('__name__', '__main__');
      it.execBlock(ast, g);
    } catch (e) {
      if (e instanceof PyErr) {
        errLine = e.line || it.line;
        if (e.type === 'Timeout' || e.type === 'OutputLimit') errorText = 'Stopped: ' + e.msg;
        else errorText = (errLine ? 'Traceback (most recent call last):\n  line ' + errLine + '\n' : '') + e.type + (e.msg !== '' ? ': ' + e.msg : '');
      } else if (e instanceof RangeError) { errLine = it.line; errorText = 'RecursionError: maximum recursion depth exceeded'; }
      else { errorText = 'Internal error: ' + (e && e.message); }
    }
    return { out: it.out.join(''), error: errorText, line: errLine, ms: Date.now() - t0, steps: it.steps };
  }
  /* evaluate a single expression with variables (used by widgets: f(x) boxes) */
  function compileExpr(src, vars) {
    var toks = tokenize(src), p = new Parser(toks), ast = p.expr();
    return function (env) {
      var it = new Interp({ maxSteps: 100000 }), g = new Scope(null); g.globals = g;
      var m = getModule('math'); Object.keys(m.attrs).forEach(function (k) { g.vars.set(k, m.attrs[k]); });
      for (var k in env) g.vars.set(k, env[k]);
      var v = it.eval(ast, g); return toF(v);
    };
  }
  G.MiniPy = { run: run, compileExpr: compileExpr, version: '1.0' };
})(typeof window !== 'undefined' ? window : globalThis);
