#!/usr/bin/env python3
"""Build the Numerical Methods course site from content/Lxx.py files.

  python3 build.py            build into site/
  python3 build.py --check    also run every code sample in real Python 3 / gcc and in MiniPy / MiniC and compare
"""
import importlib.util, json, os, re, shutil, subprocess, sys, html, hashlib, tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')
OUT = os.path.join(ROOT, 'site')
AUTHOR = 'Md Mahbub E Noor'
UNI = 'University of Barishal'
COURSE_TITLE = 'Numerical Methods'
CODE_NO = 'CSE-3107'

sys.path.insert(0, os.path.join(ROOT, 'content'))
from roadmap import ROADMAP, MODULES  # noqa: E402

# ------------------------------------------------------------------ math (KaTeX, rendered at build time)
MATH = []
def mathify(s):
    """Replace $$..$$ and $..$ with placeholders; rendered later in one KaTeX batch."""
    if not s or '$' not in s:
        return s
    def disp(m):
        MATH.append((m.group(1), True)); return '\x00M%d\x00' % (len(MATH) - 1)
    def inl(m):
        MATH.append((m.group(1), False)); return '\x00M%d\x00' % (len(MATH) - 1)
    s = re.sub(r'\$\$(.+?)\$\$', disp, s, flags=re.S)
    s = re.sub(r'(?<![\\$])\$(?!\s)(.+?)(?<![\\\s])\$', inl, s, flags=re.S)
    return s.replace('\\$', '$')

def render_math(texts):
    if not MATH:
        return texts
    js = os.path.join(ROOT, 'tools', 'katex_batch.js')
    p = subprocess.run(['node', js], input=json.dumps(MATH), capture_output=True, text=True, cwd=ROOT)
    if p.returncode:
        print(p.stderr); sys.exit('KaTeX failed')
    res = json.loads(p.stdout)
    bad = [MATH[i][0] for i, r in enumerate(res) if 'katex-error' in r]
    if bad:
        print('KaTeX errors in:', bad[:5]); sys.exit(1)
    def sub(t):
        return re.sub('\x00M(\\d+)\x00', lambda m: res[int(m.group(1))], t)
    return {k: sub(v) for k, v in texts.items()}

def M(s):
    return mathify(s) if isinstance(s, str) else s

# ------------------------------------------------------------------ helpers
def esc(s):
    return html.escape(s, quote=True)

def attr_json(o):
    return esc(json.dumps(o, separators=(',', ':')))

def ul(items, frag=False, cls='b', ordered=False):
    tag = 'ol' if ordered else 'ul'
    lis = ''.join('<li%s>%s</li>' % (' class="frag fade"' if frag else '', M(i)) for i in items)
    return '<%s class="%s">%s</%s>' % (tag, cls, lis, tag)

def fragc(on):
    return ' frag fade' if on else ''

def widget(w, o=None, height=None, cls=''):
    o = dict(o or {})
    return '<div class="live %s" style="%s"><div data-w="%s" data-o="%s"></div></div>' % (cls, ('height:%s' % height) if height else '', w, attr_json(o))

def runner(cid, lang=None, ed=None, out=None, title='', autorun=False):
    a = ' data-runner="%s"' % cid
    if lang: a += ' data-lang="%s"' % lang
    if ed: a += ' data-ed="%s"' % ed
    if out: a += ' data-out="%s"' % out
    if title: a += ' data-title="%s"' % esc(title)
    if autorun: a += ' data-autorun'
    return '<div class="live"><div%s></div></div>' % a

def table(head, rows, frag=False, ans=None, cls='tb', tx_cols=()):
    h = '<tr>' + ''.join('<th>%s</th>' % M(c) for c in head) + '</tr>'
    body = ''
    for i, r in enumerate(rows):
        c = []
        if frag: c.append('frag fade')
        if ans is not None and (i == ans or (ans == -1 and i == len(rows) - 1)): c.append('ans')
        tds = ''.join('<td%s>%s</td>' % (' class="tx"' if j in tx_cols else '', M(str(v))) for j, v in enumerate(r))
        body += '<tr%s>%s</tr>' % (' class="%s"' % ' '.join(c) if c else '', tds)
    return '<table class="%s"><thead>%s</thead><tbody>%s</tbody></table>' % (cls, h, body)

def block(b):
    """Right-hand / extra content blocks: dict with one of the keys below."""
    if b is None: return ''
    if isinstance(b, str): return M(b)
    k = b.get
    if k('w'): return widget(b['w'], b.get('o'), b.get('h'))
    if k('code'): return runner(b['code'], b.get('lang'), b.get('ed'), b.get('out'), b.get('title', ''), b.get('autorun', False))
    if k('table'): return table(b['table'][0], b['table'][1], b.get('frag', False), b.get('ans'), b.get('cls', 'tb'), b.get('tx', ()))
    if k('eq'): return '<div class="eqbox%s">%s%s</div>' % (fragc(b.get('frag')), ('<span class="cap">%s</span>' % M(b['cap'])) if b.get('cap') else '', M('$$' + b['eq'] + '$$'))
    if k('card'): return card(b['card'])
    if k('cards'): return '<div class="grid g%d">%s</div>' % (b.get('n', 2), ''.join(card(c) for c in b['cards']))
    if k('items'): return ul(b['items'], b.get('frag', False))
    if k('svg'): return '<figure class="fig">%s%s</figure>' % (b['svg'], ('<figcaption>%s</figcaption>' % M(b['cap'])) if b.get('cap') else '')
    if k('html'): return M(b['html'])
    if k('stack'): return '<div class="col">%s</div>' % ''.join(block(x) for x in b['stack'])
    raise ValueError('unknown block %r' % b)

def card(c):
    cls = c.get('cls', '')
    inner = ''
    if c.get('tag'): inner += '<span class="tag">%s</span>' % M(c['tag'])
    if c.get('h'): inner += '<h3>%s</h3>' % M(c['h'])
    if c.get('t'): inner += '<p>%s</p>' % M(c['t'])
    if c.get('items'): inner += '<ul>%s</ul>' % ''.join('<li>%s</li>' % M(i) for i in c['items'])
    if c.get('eq'): inner += '<div class="eq">%s</div>' % M('$$' + c['eq'] + '$$')
    if c.get('body'): inner += block(c['body'])
    return '<div class="card %s%s">%s</div>' % (cls, fragc(c.get('frag')), inner)

# ------------------------------------------------------------------ slide renderers
def s_cover(L, s):
    return ('<span class="kick">%s · Lecture %d</span><h1>%s</h1><p class="sub">%s</p><p class="meta">%s<br>%s %s · %s<br>%s</p>%s' %
            (esc(L['module_name']), L['n'], M(L['title']), M(L.get('sub', '')), AUTHOR + ' · Assistant Professor', CODE_NO, COURSE_TITLE, 'B.Sc. 3rd Year 1st Semester', 'Department of CSE, ' + UNI, cover_deco(L['n']))), 'cover'

def cover_deco(n):
    # decorative curve; orange dots converge on the place where it crosses the axis
    import math
    a = 0.6 + (n % 5) * 0.15
    f = lambda x: math.sin(a * x * 1.7) * 0.9 + 0.25 * x
    X = lambda x: 60 + (x + 0.5) / 4 * 800
    pts = [(X(x), 300 - f(x) * 150) for x in [i / 180 * 4 - 0.5 for i in range(181)]]
    # find a sign change of f on the plotted range (rightmost)
    root = None
    xs = [i / 400 * 4 - 0.5 for i in range(401)]
    for x0, x1 in zip(xs, xs[1:]):
        if f(x0) * f(x1) <= 0:
            lo, hi = x0, x1
            for _ in range(40):
                mid = (lo + hi) / 2
                if f(lo) * f(mid) <= 0: hi = mid
                else: lo = mid
            root = (lo + hi) / 2
    rx = X(root) if root is not None else 600
    path = 'M ' + ' L '.join('%.1f %.1f' % p for p in pts)
    dots = ''.join('<circle cx="%.1f" cy="300" r="%d" fill="#f0a35e" opacity="%.2f"/>' % (rx - 260 / (2 ** k) * (1 if k % 2 else -1), 6 if k < 5 else 9, 0.35 + k * 0.12) for k in range(6))
    return ('<svg class="deco" width="900" height="520" viewBox="0 0 900 520" aria-hidden="true"><line x1="40" y1="300" x2="880" y2="300" stroke="#3a6189" stroke-width="2"/>'
            '<path d="%s" fill="none" stroke="#6fa3dc" stroke-width="5" stroke-linecap="round"/>%s</svg>') % (path, dots)

def s_section(L, s):
    return '<span class="kick">%s</span><h2 class="t">%s</h2>%s' % (M(s.get('kick', '')), M(s['title']), ('<p class="lead">%s</p>' % M(s['lead'])) if s.get('lead') else ''), 'section'

def head(s):
    h = ''
    if s.get('kick'): h += '<span class="kick">%s</span>' % M(s['kick'])
    h += '<h2 class="t">%s</h2>' % M(s['title'])
    if s.get('lead'): h += '<p class="lead">%s</p>' % M(s['lead'])
    return h

READY = set()
def module_strip(n):
    """'You are here' chain of the lectures in this lecture's module, plus what it builds on."""
    mod = next(m for m in MODULES if n in m[2])
    chips = ''
    for k in mod[2]:
        r = next(x for x in ROADMAP if x['n'] == k)
        label = 'L%d · %s' % (k, esc(r['title'].replace('The ', '').split(':')[0]))
        if k == n: chips += '<span class="chip cur">%s</span>' % label
        elif k in READY: chips += '<a class="chip" href="L%02d.html">%s</a>' % (k, label)
        else: chips += '<span class="chip">%s</span>' % label
        if k != mod[2][-1]: chips += '<i>→</i>'
    me = next(x for x in ROADMAP if x['n'] == n)
    needs = ', '.join(('<a href="L%02d.html">L%d</a>' % (k, k)) if k in READY else 'L%d' % k for k in me.get('needs', []))
    return ('<div class="strip"><span class="strip-h">%s · you are here</span><div class="chips">%s</div>%s</div>'
            % (esc(mod[0]), chips, ('<span class="strip-n">Builds on: %s</span>' % needs) if needs else ''))

def s_goals(L, s):
    prev = s.get('prev', '')
    side = ''
    if prev or s.get('today'):
        side = '<div class="col fix" style="width:720px"><div class="card">'
        if prev: side += '<span class="tag">Last time</span><p>%s</p><hr style="border:0;border-top:2px solid #d5dbe1;width:100%%">' % M(prev)
        side += '<span class="tag">Today</span><p>%s</p>' % M(s.get('today', ''))
        if s.get('reading'): side += '<p class="small">%s</p>' % M(s['reading'])
        side += '</div></div>'
    return head({'title': s.get('title', "Today's goals")}) + '<div class="cols"><div class="col">%s</div>%s</div>' % (ul(s['items'], s.get('frag', False)), side) + module_strip(L['n']), 'goals'

def s_bullets(L, s):
    left = ''
    if s.get('items'): left += ul(s['items'], s.get('frag', False), ordered=s.get('ordered', False))
    if s.get('below'): left += block(s['below'])
    right = block(s.get('right'))
    if right:
        w = s.get('rw', 820)
        return head(s) + '<div class="cols%s"><div class="col">%s</div><div class="col fix" style="width:%dpx">%s</div></div>' % (' c' if s.get('center') else '', left, w, right), ''
    return head(s) + '<div class="col">%s</div>' % left, ''

def s_cards(L, s):
    n = s.get('n', len(s['cards']) if len(s['cards']) <= 4 else 3)
    cards = ''.join(card(dict(c, frag=c.get('frag', s.get('frag', False)))) for c in s['cards'])
    extra = block(s.get('below')) if s.get('below') else ''
    return head(s) + '<div class="grid g%d">%s</div>%s' % (n, cards, extra), ''

def s_compare(L, s):
    def side(d):
        return card({'h': d['h'], 'items': d.get('items'), 't': d.get('t'), 'cls': d.get('cls', ''), 'eq': d.get('eq'), 'body': d.get('body'), 'tag': d.get('tag')})
    mid = '<div class="col fix" style="width:80px;align-self:center;text-align:center;font-size:56px;color:#a64f15">%s</div>' % s.get('mid', 'vs') if s.get('mid', 'vs') else ''
    extra = block(s.get('below')) if s.get('below') else ''
    return head(s) + '<div class="cols"><div class="col">%s</div>%s<div class="col%s">%s</div></div>%s' % (side(s['left']), mid, fragc(s.get('frag')), side(s['right']), extra), ''

def s_math(L, s):
    eqs = ''.join(block(dict(e, eq=e['eq'], frag=e.get('frag', s.get('frag', False)))) for e in s['eqs'])
    left = '<div class="col">%s%s</div>' % (eqs, block(s.get('below')) if s.get('below') else '')
    if s.get('items') or s.get('right'):
        right = ul(s['items'], s.get('ifrag', False)) if s.get('items') else block(s['right'])
        return head(s) + '<div class="cols"><div class="col">%s</div><div class="col fix" style="width:%dpx">%s</div></div>' % (left, s.get('rw', 760), right), ''
    return head(s) + left, ''

def s_worked(L, s):
    q = ''
    if s.get('q'):
        q = '<div class="qbox">%s%s</div>' % (('<span class="src">%s</span>' % M(s['src'])) if s.get('src') else '', M(s['q']))
    steps = '<div class="steps">' + ''.join('<div class="frag fade"><span class="n">%d</span><div>%s</div></div>' % (i + 1, M(t)) for i, t in enumerate(s.get('steps', []))) + '</div>'
    ans = '<div class="answer frag fade">%s</div>' % M(s['answer']) if s.get('answer') else ''
    right = block(s.get('right'))
    if right:
        return head(s) + q + '<div class="cols"><div class="col">%s%s</div><div class="col fix" style="width:%dpx">%s</div></div>' % (steps, ans, s.get('rw', 860), right), ''
    return head(s) + q + steps + ans, ''

def s_table(L, s):
    t = table(s['head'], s['rows'], s.get('frag', False), s.get('ans'), s.get('cls', 'tb'), s.get('tx', ()))
    left = (('<div class="qbox">%s%s</div>' % (('<span class="src">%s</span>' % M(s['src'])) if s.get('src') else '', M(s['q']))) if s.get('q') else '') + '<div>%s</div>' % t
    if s.get('note'): left += '<p class="small%s">%s</p>' % (fragc(s.get('notefrag')), M(s['note']))
    if s.get('answer'): left += '<div class="answer frag fade">%s</div>' % M(s['answer'])
    right = block(s.get('right'))
    if right:
        return head(s) + '<div class="cols"><div class="col">%s</div><div class="col fix" style="width:%dpx">%s</div></div>' % (left, s.get('rw', 700), right), ''
    return head(s) + left, ''

def s_code(L, s):
    r = runner(s['code'], s.get('lang'), s.get('ed', '440px'), s.get('out', '285px'), s.get('ctitle', ''), s.get('autorun', False))
    if s.get('items') or s.get('left'):
        left = (ul(s['items'], s.get('frag', False)) if s.get('items') else '') + (block(s['left']) if s.get('left') else '')
        return head(s) + '<div class="cols"><div class="col fix" style="width:%dpx">%s</div><div class="col">%s</div></div>' % (s.get('lw', 620), left, r), ''
    return head(s) + r, ''

def s_widget(L, s):
    w = widget(s['w'], s.get('o'), None)
    if s.get('items') or s.get('left'):
        left = (ul(s['items'], s.get('frag', False)) if s.get('items') else '') + (block(s['left']) if s.get('left') else '')
        return head(s) + '<div class="cols"><div class="col fix" style="width:%dpx">%s</div><div class="col">%s</div></div>' % (s.get('lw', 560), left, w), ''
    return head(s) + w, ''

def s_check(L, s):
    body = '<div class="qbox"><span class="src">%s</span>%s</div>' % (M(s.get('src', 'Checkpoint · think, then discuss with your neighbour')), M(s['q']))
    if s.get('opts'):
        body += '<div class="opts">' + ''.join('<div class="%s"><b>%s</b>%s</div>' % ('right frag' if i == s['right'] else '', 'ABCD'[i], M(o)) for i, o in enumerate(s['opts'])) + '</div>'
    if s.get('answer'):
        body += '<div class="answer frag fade">%s</div>' % M(s['answer'])
    right = block(s.get('right_block'))
    if right:
        return head({'title': s.get('title', 'Checkpoint'), 'kick': s.get('kick')}) + '<div class="cols"><div class="col">%s</div><div class="col fix" style="width:%dpx">%s</div></div>' % (body, s.get('rw', 760), right), ''
    return head({'title': s.get('title', 'Checkpoint'), 'kick': s.get('kick')}) + body, ''

def s_exam(L, s):
    body = '<div class="qbox"><span class="src">%s</span>%s</div>' % (M(s['src']), M(s['q']))
    if s.get('tips'):
        body += '<div class="card key"><span class="tag">%s</span>%s</div>' % (M(s.get('tiptitle', 'How to write a complete answer')), ul(s['tips'], True))
    right = block(s.get('right'))
    t = {'title': s.get('title', 'Practice problem'), 'kick': s.get('kick', 'Practice')}
    if right:
        return head(t) + '<div class="cols"><div class="col">%s</div><div class="col fix" style="width:%dpx">%s</div></div>' % (body, s.get('rw', 760), right), ''
    return head(t) + body, ''

def s_ml(L, s):
    items = ''.join('<div class="ml%s"><span class="ic">%s</span><div><h3>%s</h3><p>%s</p></div></div>' % (fragc(s.get('frag', True)), i.get('ic', '◆'), M(i['h']), M(i['t'])) for i in s['items'])
    return head({'title': s.get('title', 'Where this shows up in CSE and machine learning'), 'kick': s.get('kick', 'Beyond the classroom'), 'lead': s.get('lead')}) + '<div class="grid g%d">%s</div>' % (s.get('n', 2), items), ''

def s_summary(L, s):
    left = '<div class="card key"><span class="tag">Key points</span>%s</div>' % ul(s['items'])
    if s.get('solved'):
        left += '<div class="card ok"><span class="tag">Opening problem: solved</span><p>%s</p></div>' % M(s['solved'])
    right = ''
    if s.get('hw'):
        right += '<div class="card blue"><span class="tag">Homework</span>%s</div>' % ul(s['hw'], ordered=True, cls='')
    if s.get('next'):
        right += '<div class="card"><span class="tag">%s</span><p>%s</p></div>' % (M(s.get('nexttitle', 'Next lecture')), M(s['next']))
    return head({'title': s.get('title', 'Summary')}) + '<div class="cols"><div class="col">%s</div><div class="col">%s</div></div>' % (left, right), ''

def s_html(L, s):
    return head(s) + M(s['html']), s.get('cls', '')

def s_bridge(L, s):
    keep = '<div class="card ok"><span class="tag">%s</span>%s</div>' % (M(s.get('keeptitle', 'What it does well (keep this)')), ul(s['keep'], cls='')) if s.get('keep') else ''
    rows = ''
    for lim, fix, lec in s['rows']:
        if isinstance(lec, str): link = '<span class="go soon">%s</span>' % M(lec)
        elif lec and lec in READY: link = '<a class="go" href="L%02d.html">Lecture %d →</a>' % (lec, lec)
        elif lec: link = '<span class="go soon">Lecture %d</span>' % lec
        else: link = '<span class="go here">this lecture</span>'
        rows += '<div class="br frag fade"><div class="lim">%s</div><i>→</i><div class="fix">%s</div>%s</div>' % (M(lim), M(fix), link)
    body = '<div class="cols"><div class="col fix" style="width:%dpx">%s</div><div class="col"><div class="bridge"><div class="bh"><span>Limitation</span><span></span><span>How it is overcome</span><span>Where</span></div>%s</div></div></div>' % (s.get('lw', 540), keep, rows)
    return head({'title': s.get('title', 'Limitations, and where we fix them'), 'kick': s.get('kick', 'Roadmap'), 'lead': s.get('lead')}) + body, ''

def app_detail(d):
    h = ''
    if d.get('where'): h += '<p class="m-where"><b>Where exactly:</b> %s</p>' % M(d['where'])
    if d.get('eq'): h += '<div class="m-eq">%s</div>' % M('$$' + d['eq'] + '$$')
    if d.get('steps'): h += '<ol class="m-steps">%s</ol>' % ''.join('<li>%s</li>' % M(x) for x in d['steps'])
    if d.get('table'): h += table(d['table'][0], d['table'][1], cls='m-tb')
    if d.get('w'): h += '<div class="m-w"><div data-w="%s" data-o="%s"></div></div>' % (d['w'], attr_json(d.get('o', {})))
    if d.get('note'): h += '<p class="m-note">%s</p>' % M(d['note'])
    return h

def s_apps(L, s):
    cards, tpls = '', ''
    for i, a in enumerate(s['items']):
        mid = 'app-%d-%s-%d' % (L['n'], s.get('id', 'apps'), i)
        cards += ('<button type="button" class="app%s" data-modal="%s"><span class="ic">%s</span><span class="ab"><b>%s</b><span>%s</span><em>Click: see it in action ▸</em></span></button>'
                  % (fragc(s.get('frag', False)), mid, a.get('ic', '◆'), M(a['h']), M(a['t'])))
        tpls += '<template id="%s"><h2>%s %s</h2>%s</template>' % (mid, a.get('ic', ''), M(a['h']), app_detail(a['detail']))
    return head({'title': s.get('title', 'Where this method runs in the real world'), 'kick': s.get('kick', 'Applications'), 'lead': s.get('lead')}) + '<div class="grid g%d apps">%s</div>%s' % (s.get('n', 3), cards, tpls), ''

def s_profile(L, s):
    def c(key, tag, cls):
        if not s.get(key): return ''
        return '<div class="card %s pf%s"><span class="tag">%s</span>%s</div>' % (cls, fragc(s.get('frag', True)), tag, ul(s[key], cls=''))
    body = '<div class="grid g2 profile">%s%s%s%s</div>' % (c('best', 'Best case', 'ok'), c('worst', 'Worst case', 'bad'), c('suited', 'Best suited for', 'blue'), c('avoid', 'Avoid when', 'key'))
    if s.get('verdict'): body += '<p class="verdict frag fade">%s</p>' % M(s['verdict'])
    return head({'title': s.get('title', 'Method profile'), 'kick': s.get('kick', 'When to use it'), 'lead': s.get('lead')}) + body, ''

RENDER = {'cover': s_cover, 'section': s_section, 'goals': s_goals, 'bullets': s_bullets, 'cards': s_cards, 'compare': s_compare, 'math': s_math,
          'worked': s_worked, 'table': s_table, 'code': s_code, 'widget': s_widget, 'check': s_check, 'exam': s_exam, 'ml': s_ml, 'summary': s_summary, 'html': s_html, 'bridge': s_bridge, 'apps': s_apps, 'profile': s_profile}

# ------------------------------------------------------------------ pages
def load(n):
    p = os.path.join(ROOT, 'content', 'L%02d.py' % n)
    if not os.path.exists(p): return None
    spec = importlib.util.spec_from_file_location('L%02d' % n, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.LECTURE

def plain(s):
    s = re.sub(r'\$+([^$]*)\$+', lambda m: m.group(1).replace('\\', ''), s or '')
    return re.sub(r'<[^>]+>', '', s)

def course_js(lectures):
    data = []
    for r in ROADMAP:
        L = lectures.get(r['n'])
        data.append({'n': r['n'], 'title': r['title'], 'lab': (L or {}).get('lab_file'), 'ready': L is not None})
    return 'window.COURSE=' + json.dumps(data) + ';'

def deck_page(L, total_slides_html, notes):
    t = esc(plain(L['title']))
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>Lecture %d: %s · Numerical Methods</title>\n'
            '<link rel="stylesheet" href="../assets/fonts.css"><link rel="stylesheet" href="../assets/katex/katex.min.css"><link rel="stylesheet" href="../assets/deck.css"><link rel="stylesheet" href="../assets/widgets.css">\n'
            '</head><body>\n'
            '<div id="bar" role="toolbar" aria-label="Lecture navigation">\n'
            ' <a href="../index.html" title="Course home">⌂ <span class="wide">Course</span></a>\n'
            ' <a id="prevlec" href="#" class="mid">◀ <span>Lecture</span></a>\n'
            ' <select id="lecsel" aria-label="Go to lecture"></select>\n'
            ' <a id="nextlec" href="#" class="mid"><span>Lecture</span> ▶</a>\n'
            ' <a id="labbtn" class="lab" href="#" title="Open this lecture\'s lab (L)">Lab</a>\n'
            ' <span class="sp"></span>\n'
            ' <button type="button" id="listbtn" class="wide" title="All slides (S)">☰ Slides</button>\n'
            ' <div class="grp"><button type="button" id="prevs" aria-label="Previous step">‹</button><span id="count" class="count"></span><button type="button" id="nexts" aria-label="Next step">›</button></div>\n'
            ' <button type="button" id="notesbtn" class="wide" title="Speaker notes (N)">Notes</button>\n'
            ' <button type="button" id="fsbtn" title="Full screen (F)">⛶<span class="wide">&nbsp;Full screen</span></button>\n'
            ' <button type="button" id="helpbtn" class="wide" title="Keys">?</button>\n'
            '</div>\n<div id="view"><div id="stage">\n%s\n</div></div>\n'
            '<div id="notes" hidden></div><div id="list" hidden></div>\n'
            '<div id="help" hidden><b>Keys</b><br><kbd>→</kbd> <kbd>Space</kbd> next step · <kbd>←</kbd> back<br><kbd>A</kbd> reveal the whole slide<br>number + <kbd>Enter</kbd> jump to slide<br><kbd>S</kbd> slide list · <kbd>F</kbd> full screen · <kbd>N</kbd> notes<br><kbd>[</kbd> <kbd>]</kbd> previous / next lecture · <kbd>L</kbd> lab<br>In a code box: <kbd>Ctrl</kbd>+<kbd>Enter</kbd> runs the code</div>\n'
            '<script src="../assets/course.js"></script><script>window.LECTURE=%d;</script>\n'
            '<script>window.CODE=%s;</script>\n'
            '<script src="../assets/numfmt.js"></script><script src="../assets/minipy.js"></script><script src="../assets/minic.js"></script><script src="../assets/expr.js"></script>\n'
            '<script src="../assets/katex/katex.min.js"></script><script src="../assets/runner.js"></script><script src="../assets/widgets.js"></script>\n'
            '<script src="../notes/L%02d.js" onerror="this.remove()"></script>\n'
            '<script src="../assets/deck.js"></script>\n</body></html>\n') % (L['n'], t, total_slides_html, L['n'], json.dumps(L.get('code', {})), L['n'])

def build_deck(L):
    secs, notes = [], {}
    n_slides = len(L['slides'])
    for i, s in enumerate(L['slides']):
        sid = s.get('id') or 's%d' % (i + 1)
        body, cls = RENDER[s['type']](L, s)
        if s['type'] != 'cover':
            body += ('<div class="foot"><div class="f1">%s</div><div class="f2">Lecture %d: %s</div><div class="f3">%s</div><div class="f4">%d / %d</div></div>'
                     % (AUTHOR, L['n'], esc(plain(L['short'] if L.get('short') else L['title'])), UNI, i + 1, n_slides))
        title = plain(s.get('title') or {'cover': 'Title', 'exam': 'Practice problem', 'check': 'Checkpoint', 'summary': 'Summary', 'goals': 'Objectives', 'apps': 'Applications', 'bridge': 'Roadmap', 'ml': 'Beyond the classroom'}.get(s['type'], s['type'].capitalize()))
        secs.append('<section id="%s" class="s %s" data-title="%s">%s</section>' % (sid, cls, esc(title), body))
        if s.get('notes'): notes[sid] = s['notes']
    return '\n'.join(secs), notes

# ------------------------------------------------------------------ labs
def lab_page(L, lectures):
    lab = L['lab']
    tabs_html, panes = '', ''
    for ti, tab in enumerate(lab['tabs']):
        tabs_html += '<button type="button" role="tab" data-tab="%d"%s>%s</button>' % (ti, ' class="on"' if ti == 0 else '', esc(tab['name']))
        content = ''
        for b in tab['blocks']:
            if 'p' in b: content += '<p class="lp">%s</p>' % M(b['p'])
            elif 'h' in b: content += '<h3 class="lh">%s</h3>' % M(b['h'])
            elif 'w' in b: content += '<div class="lw"><div data-w="%s" data-o="%s"></div></div>' % (b['w'], attr_json(b.get('o', {})))
            elif 'code' in b:
                tasks = ''
                if b.get('tasks'):
                    tasks = '<div class="tasks"><b>Try this</b><ol>%s</ol></div>' % ''.join('<li><label><input type="checkbox"> <span>%s</span></label></li>' % M(t) for t in b['tasks'])
                content += '<div class="lcode"><div data-runner="%s"%s data-ed="%s" data-out="%s"></div>%s</div>' % (b['code'], (' data-lang="%s"' % b['lang']) if b.get('lang') else '', b.get('ed', '380px'), b.get('out', '220px'), tasks)
            elif 'qa' in b:
                for qi, (q, a) in enumerate(b['qa']):
                    content += '<details class="qa"><summary><span>Q%d</span> %s</summary><div>%s</div></details>' % (qi + 1, M(q), M(a))
            elif 'html' in b: content += M(b['html'])
        panes += '<section class="pane" data-pane="%d"%s>%s</section>' % (ti, '' if ti == 0 else ' hidden', content)
    ready = [l for l in ROADMAP if lectures.get(l['n']) and lectures[l['n']].get('lab_file')]
    opts = ''.join('<option value="%s"%s>Lab %d: %s</option>' % (lectures[l['n']]['lab_file'], ' selected' if l['n'] == L['n'] else '', l['n'], esc(lectures[l['n']]['lab']['title'])) for l in ready)
    idx = [l['n'] for l in ready].index(L['n'])
    prev_lab = lectures[ready[idx - 1]['n']]['lab_file'] if idx > 0 else None
    next_lab = lectures[ready[idx + 1]['n']]['lab_file'] if idx + 1 < len(ready) else None
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>Lab %d: %s · Numerical Methods</title>\n<link rel="stylesheet" href="../assets/fonts.css"><link rel="stylesheet" href="../assets/katex/katex.min.css"><link rel="stylesheet" href="../assets/widgets.css"><link rel="stylesheet" href="../assets/lab.css">\n'
            '<script src="../assets/theme.js"></script></head><body>\n'
            '<div class="dcbar" role="navigation" aria-label="Course navigation"><a href="../index.html" title="Course home">⌂<span class="wide">&nbsp;Course</span></a>'
            '<a class="slides" href="../lectures/L%02d.html">◀ Lecture %d slides</a><span class="sp"></span>'
            '<a class="%s wide" href="%s">◀ Lab</a><select aria-label="Go to lab" onchange="location.href=this.value">%s</select><a class="%s wide" href="%s">Lab ▶</a>'
            '<button type="button" data-theme-toggle>☾ Dark</button></div>\n'
            '<main class="lab"><header><p class="eyebrow">Lab %d · Lecture %d · %s</p><h1>%s</h1><p class="intro">%s</p></header>\n'
            '<div class="tabs" role="tablist">%s</div>\n%s\n'
            '<footer>Everything on this page runs in your browser, offline. The Python and C boxes use small built-in interpreters (MiniPy and MiniC); '
            'every program here was also run in real Python 3 and gcc with identical output. Use ⤓ to download a program and run it in Jupyter or gcc on the lab PC.</footer></main>\n'
            '<script>window.CODE=%s;</script>\n'
            '<script src="../assets/numfmt.js"></script><script src="../assets/minipy.js"></script><script src="../assets/minic.js"></script><script src="../assets/expr.js"></script>\n'
            '<script src="../assets/katex/katex.min.js"></script><script src="../assets/runner.js"></script><script src="../assets/widgets.js"></script><script src="../assets/lab.js"></script>\n</body></html>\n') % (
        L['n'], esc(lab['title']), L['n'], L['n'],
        '' if prev_lab else 'dis', prev_lab or '#', opts, '' if next_lab else 'dis', next_lab or '#',
        L['n'], L['n'], esc(plain(L['title'])), esc(lab['title']), M(lab.get('intro', '')), tabs_html, panes, json.dumps(L.get('code', {})))

# ------------------------------------------------------------------ home
def home_page(lectures):
    parts = ''
    nready = sum(1 for r in ROADMAP if lectures.get(r['n']))
    for mi, (mname, msub, rng) in enumerate(MODULES):
        lis = ''
        for r in ROADMAP:
            if r['n'] not in rng: continue
            L = lectures.get(r['n'])
            if L:
                acts = '<a class="pri" href="lectures/L%02d.html">Slides</a>' % r['n']
                acts += ('<a href="labs/%s">Lab</a>' % L['lab_file']) if L.get('lab_file') else '<span>No lab</span>'
                files = '%d slides · %d live code boxes · %d interactive widgets' % (len(L['slides']), L['_ncode'], L['_nw'])
            else:
                acts = '<span>Coming soon</span>'; files = 'in preparation'
            if r.get('needs'):
                used = [q['n'] for q in ROADMAP if r['n'] in q.get('needs', [])]
                files += ' · builds on ' + ', '.join('L%d' % k for k in r['needs'])
                if used: files += ' · used in ' + ', '.join('L%d' % k for k in used)
            lis += ('<li class="l%s"><span class="num">%02d</span><div class="t"><b>%s</b><small>%s</small><span class="files">%s</span></div><div class="acts">%s</div></li>'
                    % ('' if L else ' soon', r['n'], esc(r['title']), esc(r['topics']), files, acts))
        parts += '<section class="part part-%s"><h2>%s<span>%s</span></h2><ol class="lec">%s</ol></section>' % (['blue', 'orange', 'navy', 'green', 'blue', 'orange', 'navy'][mi % 7], esc(mname), esc(msub), lis)
    with open(os.path.join(SRC, 'home_template.html')) as f:
        tpl = f.read()
    return tpl.replace('{{PARTS}}', parts).replace('{{NREADY}}', str(nready)).replace('{{NTOTAL}}', str(len(ROADMAP)))

# ------------------------------------------------------------------ code checking
def check_code(lectures):
    """Run every program in real Python/gcc and in MiniPy/MiniC; outputs must match exactly."""
    tmp = tempfile.mkdtemp()
    jobs = []
    for n, L in sorted(lectures.items()):
        for cid, c in L.get('code', {}).items():
            for lang in ('py', 'c'):
                if c.get(lang) is None: continue
                if c.get('nocheck'): continue
                jobs.append((n, cid, lang, c[lang], c.get('stdin', '')))
    real = {}
    for n, cid, lang, src, stdin in jobs:
        ext = '.py' if lang == 'py' else '.c'
        path = os.path.join(tmp, '%s_%s%s' % (cid, lang, ext))
        with open(path, 'w') as f: f.write(src)
        if lang == 'py':
            p = subprocess.run([sys.executable, path], input=stdin, capture_output=True, text=True, timeout=60)
            out = p.stdout + (('\n<<ERR>> ' + p.stderr.strip().splitlines()[-1]) if p.returncode else '')
        else:
            exe = path[:-2]
            cp = subprocess.run(['gcc', '-std=gnu11', '-O0', '-Wall', '-o', exe, path, '-lm'], capture_output=True, text=True)
            if cp.returncode:
                out = '<<COMPILE ERROR>> ' + cp.stderr
            else:
                warn = [l for l in cp.stderr.splitlines() if 'warning' in l]
                if warn: print('  gcc warning in %s: %s' % (cid, warn[0]))
                p = subprocess.run([exe], input=stdin, capture_output=True, text=True, timeout=60)
                out = p.stdout
        real[(n, cid, lang)] = out
    payload = [{'k': '%d|%s|%s' % (n, cid, lang), 'lang': lang, 'src': src, 'stdin': stdin} for n, cid, lang, src, stdin in jobs]
    p = subprocess.run(['node', os.path.join(ROOT, 'tools', 'mini_batch.js')], input=json.dumps(payload), capture_output=True, text=True, cwd=ROOT)
    if p.returncode: print(p.stderr); sys.exit('mini runner failed')
    mini = json.loads(p.stdout)
    bad = 0
    for n, cid, lang, src, stdin in jobs:
        k = '%d|%s|%s' % (n, cid, lang)
        r, m = real[(n, cid, lang)], mini[k]
        mo = m['out'] + (('\n<<ERR>> ' + m['error'].splitlines()[-1]) if m.get('error') else '')
        if r.strip() != mo.strip() or (lang == 'c' and m.get('warnings')):
            bad += 1
            print('MISMATCH L%02d %s [%s]' % (n, cid, lang))
            import difflib
            for line in list(difflib.unified_diff(r.splitlines(), mo.splitlines(), 'real', 'mini', lineterm=''))[:20]: print('   ', line)
            if m.get('warnings'): print('    warnings:', m['warnings'])
    print('code check: %d programs, %d mismatches' % (len(jobs), bad))
    shutil.rmtree(tmp)
    return bad == 0

# ------------------------------------------------------------------ main
def main():
    check = '--check' in sys.argv
    lectures = {}
    for r in ROADMAP:
        L = load(r['n'])
        if L is None: continue
        L['n'] = r['n']
        L.setdefault('title', r['title'])
        L['module_name'] = next(m[0] for m in MODULES if r['n'] in m[2])
        if L.get('lab'): L['lab_file'] = 'L%02d_%s.html' % (r['n'], re.sub(r'[^A-Za-z0-9]+', '_', L['lab']['title']).strip('_'))
        lectures[r['n']] = L
    if check and not check_code(lectures):
        sys.exit(1)
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(SRC, 'assets'), os.path.join(OUT, 'assets'))
    kd = os.path.join(ROOT, 'node_modules', 'katex', 'dist')
    os.makedirs(os.path.join(OUT, 'assets', 'katex'))
    shutil.copy(os.path.join(kd, 'katex.min.css'), os.path.join(OUT, 'assets', 'katex'))
    shutil.copy(os.path.join(kd, 'katex.min.js'), os.path.join(OUT, 'assets', 'katex'))
    os.makedirs(os.path.join(OUT, 'assets', 'katex', 'fonts'))
    for fn in os.listdir(os.path.join(kd, 'fonts')):
        if fn.endswith('.woff2'): shutil.copy(os.path.join(kd, 'fonts', fn), os.path.join(OUT, 'assets', 'katex', 'fonts'))
    shutil.copy(os.path.join(kd, '..', 'LICENSE'), os.path.join(OUT, 'assets', 'katex', 'LICENSE'))
    for d in ('lectures', 'labs', 'notes'): os.makedirs(os.path.join(OUT, d))
    READY.update(lectures.keys())
    pages = {}
    for n, L in sorted(lectures.items()):
        sl, notes = build_deck(L)
        L['_ncode'] = sl.count('data-runner=')
        L['_nw'] = sl.count('data-w=')
        pages['lectures/L%02d.html' % n] = deck_page(L, sl, notes)
        pages['notes/L%02d.js' % n] = 'window.DECK_NOTES=' + json.dumps(notes, ensure_ascii=False) + ';\n'
        if L.get('lab'): pages['labs/' + L['lab_file']] = lab_page(L, lectures)
    pages['index.html'] = home_page(lectures)
    pages = render_math(pages)
    for p, t in pages.items():
        with open(os.path.join(OUT, p), 'w') as f: f.write(t)
    with open(os.path.join(OUT, 'assets', 'course.js'), 'w') as f: f.write(course_js(lectures))
    for fn in ('README.md', 'LICENSE.md', 'LICENSE-CODE.txt', 'THIRD-PARTY-NOTICES.md'):
        sp = os.path.join(SRC, fn)
        if os.path.exists(sp): shutil.copy(sp, os.path.join(OUT, fn))
    print('built %d lectures, %d pages, %d formulas -> %s' % (len(lectures), len(pages), len(MATH), OUT))

if __name__ == '__main__':
    main()
