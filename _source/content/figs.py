"""Animated concept figures ("The idea in one picture"), one per lecture.
Each figure is an SVG built from data coordinates; elements tagged with a step
appear one after another (deck.js runs the animation, click = pause/resume)."""
import math

NAVY, BLUE, ORANGE, GREEN, RED, GREY, INK = '#16324f', '#2f6db5', '#c2601c', '#2e7d4f', '#b3261e', '#7b8794', '#1d2733'
LIGHT = {BLUE: '#dbe8f6', ORANGE: '#fbe6d4', GREEN: '#dff0e5', RED: '#f8dcda', GREY: '#e7edf3', NAVY: '#e7edf3'}


class Fig:
    def __init__(s, x0, x1, y0, y1, W=1000, H=600, pad=(70, 30, 30, 60)):
        s.x0, s.x1, s.y0, s.y1, s.W, s.H = x0, x1, y0, y1, W, H
        s.l, s.t, s.r, s.b = pad
        s.el, s.caps, s.n, s.marks = [], {}, 0, set()

    def X(s, x): return s.l + (x - s.x0) / (s.x1 - s.x0) * (s.W - s.l - s.r)
    def Y(s, y): return s.H - s.b - (y - s.y0) / (s.y1 - s.y0) * (s.H - s.t - s.b)

    def _a(s, step, until=None, draw=False):
        if step is None: return ''
        s.n = max(s.n, step)
        return ' data-s="%d"%s%s' % (step, (' data-u="%d"' % until) if until else '', ' class="dr" pathLength="1"' if draw else '')

    def cap(s, step, text):
        s.caps[step] = text; s.n = max(s.n, step)

    def axes(s, xl='x', yl='', y=0, x=None, ticks=(), yticks=()):
        yy = s.Y(y); xx = s.X(s.x0 if x is None else x)
        s.marks.add(GREY)
        s.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3" marker-end="url(#m%s)"/>' % (s.l - 10, yy, s.W - s.r, yy, GREY, GREY[1:]))
        s.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3" marker-end="url(#m%s)"/>' % (xx, s.H - s.b + 10, xx, s.t, GREY, GREY[1:]))
        if xl: s.el.append('<text x="%.1f" y="%.1f" font-size="26" fill="%s" text-anchor="end" font-style="italic">%s</text>' % (s.W - s.r - 4, yy + 34, GREY, xl))
        if yl: s.el.append('<text x="%.1f" y="%.1f" font-size="26" fill="%s" font-style="italic">%s</text>' % (xx + 12, s.t + 22, GREY, yl))
        for t in ticks:
            v, lab = (t if isinstance(t, tuple) else (t, ('%g' % t)))
            s.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"/><text x="%.1f" y="%.1f" font-size="24" fill="%s" text-anchor="middle">%s</text>' % (s.X(v), yy - 7, s.X(v), yy + 7, GREY, s.X(v), yy + 34, GREY, lab))
        for t in yticks:
            v, lab = (t if isinstance(t, tuple) else (t, ('%g' % t)))
            s.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"/><text x="%.1f" y="%.1f" font-size="24" fill="%s" text-anchor="end">%s</text>' % (xx - 7, s.Y(v), xx + 7, s.Y(v), GREY, xx - 12, s.Y(v) + 8, GREY, lab))

    def curve(s, f, a, b, col=NAVY, w=5, step=None, until=None, n=90, dash=None, draw=True):
        pts = []
        for i in range(n + 1):
            x = a + (b - a) * i / n; y = f(x)
            y = max(min(y, s.y1 + (s.y1 - s.y0)), s.y0 - (s.y1 - s.y0))
            pts.append('%.1f,%.1f' % (s.X(x), s.Y(y)))
        s.el.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%g" stroke-linejoin="round" stroke-linecap="round"%s%s clip-path="url(#clip)"/>' % (' '.join(pts), col, w, (' stroke-dasharray="%s"' % dash) if dash else '', s._a(step, until, draw and not dash)))

    def poly(s, pts, col=NAVY, w=4, step=None, until=None, fill='none', op=1, dash=None, close=False):
        p = ' '.join('%.1f,%.1f' % (s.X(x), s.Y(y)) for x, y in pts)
        s.el.append('<%s points="%s" fill="%s" fill-opacity="%g" stroke="%s" stroke-width="%g" stroke-linejoin="round"%s%s/>' % ('polygon' if close else 'polyline', p, fill, op, col, w, (' stroke-dasharray="%s"' % dash) if dash else '', s._a(step, until)))

    def line(s, xa, ya, xb, yb, col=NAVY, w=4, step=None, until=None, dash=None, arrow=False, draw=True, px=False):
        if not px: xa, ya, xb, yb = s.X(xa), s.Y(ya), s.X(xb), s.Y(yb)
        m = ''
        if arrow:
            s.marks.add(col); m = ' marker-end="url(#m%s)"' % col[1:]
        s.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%g" stroke-linecap="round"%s%s%s/>' % (xa, ya, xb, yb, col, w, (' stroke-dasharray="%s"' % dash) if dash else '', m, s._a(step, until, draw and not dash)))

    def dot(s, x, y, col=NAVY, r=10, step=None, until=None, hollow=False, px=False):
        if not px: x, y = s.X(x), s.Y(y)
        s.el.append('<circle cx="%.1f" cy="%.1f" r="%g" fill="%s" stroke="%s" stroke-width="4"%s/>' % (x, y, r, '#fbfaf7' if hollow else col, col, s._a(step, until)))

    def text(s, x, y, t, col=INK, size=28, anchor='middle', dx=0, dy=0, step=None, until=None, bold=False, px=False, italic=False, bg=False):
        if not px: x, y = s.X(x), s.Y(y)
        x += dx; y += dy
        a = s._a(step, until)
        if bg:
            wd = len(t) * size * 0.56 + 16
            bx = x - wd / 2 if anchor == 'middle' else (x - 8 if anchor == 'start' else x - wd + 8)
            s.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="#fbfaf7" fill-opacity="0.92"%s/>' % (bx, y - size + 2, wd, size + 10, a))
        s.el.append('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s"%s%s%s>%s</text>' % (x, y, size, col, anchor, ' font-weight="700"' if bold else ' font-weight="500"', ' font-style="italic"' if italic else '', a, t))

    def band(s, xa, xb, col=BLUE, step=None, until=None, op=0.16, ya=None, yb=None):
        ya = s.y0 if ya is None else ya; yb = s.y1 if yb is None else yb
        s.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%g"%s/>' % (s.X(min(xa, xb)), s.Y(max(ya, yb)), abs(s.X(xb) - s.X(xa)), abs(s.Y(ya) - s.Y(yb)), col, op, s._a(step, until)))

    def box(s, x, y, w, h, label, col=NAVY, step=None, until=None, size=26, fill=None, sub=None, tc=None):
        """Rounded box in pixel coordinates with centred label."""
        a = s._a(step, until)
        s.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="14" fill="%s" stroke="%s" stroke-width="3"%s/>' % (x, y, w, h, fill or LIGHT.get(col, '#fff'), col, a))
        ty = y + h / 2 + size * 0.36 - (size * 0.55 if sub else 0)
        s.el.append('<text x="%.1f" y="%.1f" font-size="%d" font-weight="700" fill="%s" text-anchor="middle"%s>%s</text>' % (x + w / 2, ty, size, tc or col, a, label))
        if sub: s.el.append('<text x="%.1f" y="%.1f" font-size="%d" font-weight="500" fill="%s" text-anchor="middle"%s>%s</text>' % (x + w / 2, ty + size * 1.15, size - 4, INK, a, sub))

    def raw(s, svg, step=None, until=None):
        s.el.append('<g%s>%s</g>' % (s._a(step, until), svg))

    def svg(s):
        defs = '<clipPath id="clip"><rect x="%d" y="%d" width="%d" height="%d"/></clipPath>' % (s.l - 12, s.t - 4, s.W - s.l - s.r + 16, s.H - s.t - s.b + 16)
        for c in sorted(s.marks):
            defs += '<marker id="m%s" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>' % (c[1:], c)
        caps = ''.join('<span data-c="%d">%s</span>' % (k, s.caps.get(k, '')) for k in range(s.n + 1) if k in s.caps)
        return ('<div class="afig" data-n="%d"><svg viewBox="0 0 %d %d" width="%d" height="%d" font-family="IBM Plex Sans, sans-serif" role="img"><defs>%s</defs>%s</svg>'
                '<div class="afig-bar"><button type="button" class="afig-btn" aria-label="Pause or play the animation">❚❚</button><div class="afig-cap">%s</div><span class="afig-k"></span></div></div>') % (s.n, s.W, s.H, s.W, s.H, defs, ''.join(s.el), caps)


# ------------------------------------------------------------------ helpers
def cubic(x): return x ** 3 - x - 2


def natural_spline(xs, ys):
    n = len(xs) - 1; h = [xs[i + 1] - xs[i] for i in range(n)]
    a = [0.0] * (n + 1); b = [1.0] * (n + 1); c = [0.0] * (n + 1); d = [0.0] * (n + 1)
    for i in range(1, n):
        a[i], b[i], c[i] = h[i - 1], 2 * (h[i - 1] + h[i]), h[i]
        d[i] = 6 * ((ys[i + 1] - ys[i]) / h[i] - (ys[i] - ys[i - 1]) / h[i - 1])
    for i in range(1, n + 1):
        w = a[i] / b[i - 1]; b[i] -= w * c[i - 1]; d[i] -= w * d[i - 1]
    M = [0.0] * (n + 1)
    for i in range(n, -1, -1):
        M[i] = (d[i] - (c[i] * M[i + 1] if i < n else 0)) / b[i]
    def S(x):
        i = max(0, min(n - 1, max(k for k in range(n) if xs[k] <= x or k == 0)))
        t0, t1 = xs[i + 1] - x, x - xs[i]
        return (M[i] * t0 ** 3 + M[i + 1] * t1 ** 3) / (6 * h[i]) + (ys[i] / h[i] - M[i] * h[i] / 6) * t0 + (ys[i + 1] / h[i] - M[i + 1] * h[i] / 6) * t1
    return S


def lagrange(xs, ys):
    def P(x):
        s = 0.0
        for i in range(len(xs)):
            t = ys[i]
            for j in range(len(xs)):
                if j != i: t *= (x - xs[j]) / (xs[i] - xs[j])
            s += t
        return s
    return P


# ------------------------------------------------------------------ the figures
def f_iteration():
    F = Fig(0, 1, 0, 1)
    F.box(40, 60, 250, 110, 'Guess', NAVY, sub='x = 1')
    F.box(375, 60, 250, 110, 'Improve', ORANGE, step=1, sub='x ← ½(x + 2/x)')
    F.box(710, 60, 250, 110, 'Close enough?', BLUE, step=2, sub='did x stop changing?')
    F.line(290, 115, 368, 115, NAVY, 5, step=1, arrow=True, px=True)
    F.line(625, 115, 703, 115, ORANGE, 5, step=2, arrow=True, px=True)
    F.raw('<path d="M835,170 V250 H500 V178" fill="none" stroke="%s" stroke-width="5" marker-end="url(#m%s)"/>' % (RED, RED[1:]), step=3); F.marks.add(RED)
    F.text(668, 240, 'no: go round again', RED, 26, step=3, px=True, dy=-4, bold=True)
    vals = ['1', '1.5', '1.416667', '1.414216', '1.414214']
    F.text(40, 345, 'the guesses:', GREY, 26, 'start', px=True, step=1)
    for i, v in enumerate(vals):
        x = 40 + i * 190
        F.box(x, 365, 160, 70, v, GREEN if i == 4 else NAVY, step=(1 if i == 0 else i + 2 if i < 4 else 6), size=26)
        if i: F.line(x - 30, 400, x - 6, 400, GREY, 4, step=(i + 2 if i < 4 else 6), arrow=True, px=True)
    F.raw('<path d="M960,115 H985 V520 H700" fill="none" stroke="%s" stroke-width="5" marker-end="url(#m%s)"/>' % (GREEN, GREEN[1:]), step=7); F.marks.add(GREEN)
    F.box(420, 480, 280, 80, 'Answer: √2 ≈ 1.4142', GREEN, step=7, size=26)
    F.text(972, 300, 'yes', GREEN, 26, 'end', px=True, step=7, bold=True, dx=-6)
    for k, c in enumerate(['Start with any reasonable guess for √2.', 'Apply a rule that makes the guess better.', 'Check: has the value stopped changing?', 'Not yet, so go round the loop again.', 'Each trip round the loop adds correct digits.', 'Four trips: the digits have almost stopped moving.', 'Two guesses in a row now agree to 5 decimals.', 'Stop and report the answer. That loop is "iteration".']): F.cap(k, c)
    return F


def f_float():
    F = Fig(0.9, 2.1, -1, 1, pad=(40, 30, 40, 60))
    y = -0.25
    F.line(0.95, y, 2.06, y, GREY, 4, arrow=True)
    for i in range(9):
        x = 1 + i / 8
        F.line(x, y - 0.09, x, y + 0.09, NAVY, 5)
        F.text(x, y, ['1', '', '1.25', '', '1.5', '', '1.75', '', '2'][i], NAVY, 24, dy=62)
    F.text(1.5, 0.86, 'A computer can store only these numbers (toy example: steps of 1/8)', GREY, 25)
    F.dot(1.31, y, ORANGE, 11, step=1)
    F.text(1.31, y, 'real number 1.31', ORANGE, 26, dy=-150, step=1, bold=True)
    F.line(1.31, y + 0.42, 1.31, y + 0.08, ORANGE, 4, step=1, arrow=True)
    F.raw('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="5" marker-end="url(#m%s)"/>' % (F.X(1.31), F.Y(y) - 18, F.X(1.28), F.Y(y) - 70, F.X(1.252), F.Y(y) - 20, RED, RED[1:]), step=2); F.marks.add(RED)
    F.dot(1.25, y, GREEN, 12, step=2)
    F.text(1.2, y, 'stored as 1.25', GREEN, 26, dy=112, step=2, bold=True)
    F.line(1.25, y - 0.52, 1.31, y - 0.52, RED, 6, step=3)
    F.text(1.28, y - 0.52, 'round-off error 0.06', RED, 26, dy=40, step=3, bold=True, anchor='start', dx=-20)
    F.box(590, 420, 70, 60, '±', NAVY, step=4, size=26); F.box(668, 420, 130, 60, 'exponent', BLUE, step=4, size=22); F.box(806, 420, 160, 60, 'fraction', ORANGE, step=4, size=22)
    F.text(778, 520, '64 bits: about 16 decimal digits', INK, 24, px=True, step=4)
    for k, c in enumerate(['Between 1 and 2 this toy computer has only nine numbers.', 'A real number usually falls between two of them.', 'It is replaced by the nearest storable number.', 'The small difference is the round-off error.', 'Real computers do the same in base 2, with far more digits.']): F.cap(k, c)
    return F


def f_taylor():
    F = Fig(-3.6, 3.6, -1.8, 1.8)
    F.axes('x', '', ticks=[(-3.1416, '−π'), (3.1416, 'π')])
    F.curve(math.sin, -3.6, 3.6, NAVY, 6)
    F.text(-3.3, 0.55, 'sin x', NAVY, 28, 'start', bold=True)
    F.dot(0, 0, NAVY, 9)
    F.curve(lambda x: x, -1.9, 1.9, ORANGE, 4, step=1)
    F.text(1.75, 1.6, '1 term:  x', ORANGE, 26, 'start', step=1, bold=True, dx=10)
    F.curve(lambda x: x - x ** 3 / 6, -3.3, 3.3, GREEN, 4, step=2)
    F.text(2.3, -1.45, '2 terms:  x − x³/6', GREEN, 26, 'end', step=2, bold=True, bg=True)
    F.curve(lambda x: x - x ** 3 / 6 + x ** 5 / 120, -3.6, 3.6, RED, 4, step=3)
    F.text(-1.3, 1.5, '3 terms:  x − x³/6 + x⁵/120', RED, 26, step=3, bold=True, bg=True)
    F.band(-1, 1, GREEN, step=4, op=0.12)
    F.text(0, -1.0, 'near the centre:', GREEN, 25, step=4, bold=True, bg=True, dy=-34)
    F.text(0, -1.0, 'excellent', GREEN, 25, step=4, bold=True, bg=True)
    for k, c in enumerate(['The true curve sin x: hard to compute directly.', 'One term: a straight line. Good only very close to 0.', 'Two terms: the curve is followed further out.', 'Three terms: almost exact from −π/2 to π/2.', 'More terms = wider good zone. The part we cut off is the truncation error.']): F.cap(k, c)
    return F


def f_errors():
    F = Fig(-16.5, 0.5, -17, 1)
    F.axes('', '', y=-17, x=-16.5)
    F.text(-8, -17, 'step size h  (smaller ←        → larger)', GREY, 25, dy=44)
    F.text(-16.5, -8, 'error', GREY, 25, dx=-36, dy=0)
    F.line(-1, -1, -15.5, -15.5, BLUE, 5, step=1)
    F.text(-8, -1.0, 'truncation error: shrinks when h shrinks', BLUE, 25, step=1, bold=True)
    F.line(-15.5, -0.5, -1, -15, ORANGE, 5, step=2)
    F.text(-8, -2.7, 'round-off error: grows when h shrinks', ORANGE, 25, step=2, bold=True)
    F.poly([(-15.5, -0.5), (-8, -8), (-1, -1)], RED, 9, step=3)
    F.text(-8, -4.6, 'we get the larger one', RED, 25, step=3, bold=True)
    F.dot(-8, -8, RED, 13, step=4)
    F.text(-8, -12.6, 'best step size:', RED, 26, step=4, bold=True)
    F.text(-8, -14.0, 'the two errors are equal', RED, 26, step=4, bold=True)
    F.line(-8, -11.4, -8, -8.9, RED, 4, step=4, arrow=True)
    for k, c in enumerate(['Every numerical answer has two kinds of error.', 'Truncation: we stopped a process early. A smaller step helps.', 'Round-off: the computer keeps limited digits. A smaller step hurts.', 'What we actually get is the red V: the bigger of the two.', 'So "smaller h" is not always better: there is a best step size.']): F.cap(k, c)
    return F


def f_condition():
    F = Fig(0, 20, 0, 10, pad=(30, 60, 30, 40))
    for x0, name, col in ((0, 'well-conditioned', GREEN), (10.6, 'ill-conditioned', RED)):
        F.raw('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="16" fill="#fbfaf7" stroke="#d5dbe1" stroke-width="3"/>' % (F.X(x0 + 0.1), F.Y(9.6), F.X(9.3) - F.X(0), F.Y(0.3) - F.Y(9.6)))
        F.text(x0 + 4.75, 10, name, col, 28, bold=True, dy=-10)
    F.line(1, 1.5, 8.5, 8.5, NAVY, 5); F.line(1, 8.5, 8.5, 1.5, BLUE, 5); F.dot(4.75, 5, NAVY, 11)
    F.line(11.6, 3.2, 19.1, 6.8, NAVY, 5); F.line(11.6, 3.9, 19.1, 6.1, BLUE, 5); F.dot(15.35, 5, NAVY, 11)
    F.line(1, 9.1, 8.5, 2.1, ORANGE, 4, step=1, dash='10 8'); F.line(11.6, 4.5, 19.1, 6.7, ORANGE, 4, step=1, dash='10 8')
    F.text(2.2, 8.9, 'nudge', ORANGE, 24, step=1, anchor='start', dx=44); F.text(12.4, 5.3, 'same nudge', ORANGE, 24, step=1, dy=-22)
    F.dot(5.07, 5.3, ORANGE, 11, step=2); F.dot(18.6, 6.55, ORANGE, 11, step=3)
    F.text(4.75, 1.0, 'crossing barely moves', GREEN, 25, step=2, bold=True, bg=True)
    F.line(15.6, 5.0, 18.3, 6.3, RED, 5, step=3, arrow=True)
    F.text(15.35, 1.0, 'crossing jumps far away', RED, 25, step=3, bold=True)
    for k, c in enumerate(['Solving two equations = finding where two lines cross.', 'Change one line a tiny bit (a small data error).', 'Lines at a wide angle: the answer hardly changes.', 'Nearly parallel lines: the same tiny change moves the answer a long way.']): F.cap(k, c)
    return F


def f_bisection():
    F = Fig(0.8, 2.25, -3.2, 5)
    F.axes('x', 'f(x)', ticks=[1, 2])
    F.curve(cubic, 0.85, 2.15, NAVY, 6)
    F.band(1, 2, BLUE, step=1, until=3)
    F.dot(1, cubic(1), RED, 10, step=1); F.text(1, cubic(1), 'f(a) < 0', RED, 25, 'middle', dy=44, step=1, bold=True)
    F.dot(2, cubic(2), GREEN, 10, step=1); F.text(2, cubic(2), 'f(b) > 0', GREEN, 25, 'end', dx=-22, dy=8, step=1, bold=True)
    F.line(1.5, 4.2, 1.5, -2.8, ORANGE, 4, step=2, until=4, dash='10 8'); F.dot(1.5, cubic(1.5), ORANGE, 10, step=2, until=4)
    F.text(1.5, 4.5, 'middle c = 1.5: f(c) < 0', ORANGE, 25, step=2, until=4, bold=True)
    F.band(1.5, 2, BLUE, step=3, until=5); F.text(1.25, 2.4, 'throw away', GREY, 25, step=3, until=5); F.line(1.02, 2.0, 1.48, 2.0, GREY, 4, step=3, until=5, arrow=True)
    F.line(1.75, 4.2, 1.75, -2.8, ORANGE, 4, step=4, until=6, dash='10 8'); F.dot(1.75, cubic(1.75), ORANGE, 10, step=4, until=6)
    F.text(1.75, 4.5, 'c = 1.75: f(c) > 0', ORANGE, 25, step=4, until=6, bold=True)
    F.band(1.5, 1.75, BLUE, step=5, op=0.22)
    F.dot(1.5214, 0, GREEN, 12, step=6); F.text(1.62, -1.9, 'root is trapped here', GREEN, 26, 'start', step=6, bold=True)
    F.line(1.66, -1.55, 1.535, -0.2, GREEN, 4, step=6, arrow=True)
    for k, c in enumerate(['The curve crosses the axis somewhere: that x is the root.', 'f is negative at a and positive at b, so the root is between them.', 'Look at the middle point c. Which sign does f have there?', 'Negative, like a. So the root is in the right half: keep it.', 'Halve again: now f(c) is positive.', 'Keep the left part. The bracket is 4 times smaller than at the start.', 'Each step halves the bracket. The root can never escape.']): F.cap(k, c)
    return F


def f_falsepos():
    F = Fig(0.8, 2.25, -3.2, 5)
    F.axes('x', 'f(x)', ticks=[1, 2])
    F.curve(cubic, 0.85, 2.15, NAVY, 6)
    F.dot(1, -2, RED, 10, step=1); F.text(1, -2, 'A (1, −2)', RED, 25, 'start', dx=16, dy=28, step=1, bold=True)
    F.dot(2, 4, GREEN, 10, step=1); F.text(2, 4, 'B (2, 4)', GREEN, 25, 'end', dx=-18, dy=6, step=1, bold=True)
    F.line(1, -2, 2, 4, ORANGE, 4, step=2, until=5)
    F.dot(1.3333, 0, ORANGE, 10, step=3); F.text(1.3333, 0, 'c₁ = 1.333', ORANGE, 25, 'end', dy=-14, dx=-14, step=3, bold=True)
    F.line(1.3333, 0, 1.3333, cubic(1.3333), GREY, 3, step=4, dash='8 7'); F.dot(1.3333, cubic(1.3333), RED, 10, step=4)
    F.line(1.3333, cubic(1.3333), 2, 4, ORANGE, 4, step=5)
    F.dot(1.4627, 0, ORANGE, 10, step=6); F.text(1.4627, 0, 'c₂ = 1.463', ORANGE, 25, 'start', dy=-46, dx=-150, step=6, bold=True, bg=True)
    F.line(1.40, 0.62, 1.455, 0.12, ORANGE, 3, step=6, arrow=True)
    F.dot(1.5214, 0, GREEN, 8, step=7, hollow=True); F.text(1.66, -1.5, 'true root 1.521', GREEN, 25, 'start', step=7, bold=True)
    F.line(1.68, -1.25, 1.535, -0.14, GREEN, 3, step=7, arrow=True)
    for k, c in enumerate(['Same start as bisection: a bracket with a sign change.', 'But now look at the sizes: A is 2 below the axis, B is 4 above.', 'Join A and B with a straight line (a chord).', 'Where the chord crosses the axis is our estimate: nearer to A.', 'f(c₁) is negative, so c₁ replaces A.', 'Draw the new chord from the new point to B.', 'Its crossing c₂ is closer again.', 'The estimates creep towards the root from one side.']): F.cap(k, c)
    return F


def f_fixedpoint():
    F = Fig(0, 1.5, 0, 1.25)
    F.axes('x', 'y', ticks=[(0.7391, '0.739')])
    F.curve(lambda x: x, 0, 1.22, GREY, 4); F.text(1.12, 1.12, 'y = x', GREY, 26, 'start', dx=14)
    F.curve(math.cos, 0, 1.45, NAVY, 6); F.text(1.3, math.cos(1.3), 'y = cos x', NAVY, 26, 'start', dy=-16, bold=True)
    x = 0.2; F.dot(x, 0, ORANGE, 10, step=1); F.text(x, 0, 'start x₀', ORANGE, 25, dy=-16, dx=58, step=1, bold=True)
    st = 2
    for i in range(4):
        y = math.cos(x)
        F.line(x, x if i else 0, x, y, ORANGE, 4, step=st, arrow=True); st += 1
        F.line(x, y, y, y, ORANGE, 4, step=st, arrow=True); st += 1
        x = y
    F.dot(0.7391, 0.7391, GREEN, 12, step=st); F.text(0.82, 0.14, 'x = cos x here', GREEN, 26, 'start', step=st, bold=True)
    F.line(0.9, 0.2, 0.75, 0.7, GREEN, 4, step=st, arrow=True)
    caps = ['We want the x where the curve y = cos x meets the line y = x.', 'Pick a starting value x₀.', 'Go up to the curve: that height is cos x₀.', 'Go across to the line y = x: this turns the height into the next x.', 'Up (or down) to the curve again …', '… and across to the line again.', 'The path winds inwards like a spiral.', 'Every loop lands closer.', 'Up to the curve …', '… across to the line.', 'It settles at 0.739: the fixed point, where x = cos x.']
    for k, c in enumerate(caps): F.cap(k, c)
    return F


def f_newton():
    f = lambda x: 0.35 * x ** 3 - 1
    df = lambda x: 1.05 * x * x
    F = Fig(0.6, 3.35, -1.6, 9.6)
    F.axes('x', 'f(x)')
    F.curve(f, 0.65, 3.12, NAVY, 6)
    xs = [3.0]
    for _ in range(2): xs.append(xs[-1] - f(xs[-1]) / df(xs[-1]))
    st = 1
    for i, x in enumerate(xs[:2]):
        F.dot(x, 0, ORANGE, 9, step=st); F.text(x, 0, 'x%s' % '₀₁₂'[i], ORANGE, 27, dy=42, step=st, bold=True)
        F.line(x, 0, x, f(x), GREY, 3, step=st, dash='8 7'); F.dot(x, f(x), ORANGE, 10, step=st); st += 1
        F.line(x + 0.12, f(x) + 0.12 * df(x), xs[i + 1], 0, RED, 4, step=st, arrow=True); st += 1
    F.dot(xs[2], 0, ORANGE, 9, step=st); F.text(xs[2], 0, 'x₂', ORANGE, 27, dy=42, step=st, bold=True)
    F.text(1.0, 7.6, 'tangent: the curve seen up close', RED, 25, 'start', step=2, bold=True)
    F.line(2.2, 7.1, 2.72, 5.0, RED, 3, step=2, arrow=True)
    F.dot(1.4188, 0, GREEN, 7, step=st + 1, hollow=True)
    F.text(0.75, 3.4, 'root 1.419', GREEN, 26, 'start', step=st + 1, bold=True); F.line(1.05, 2.9, 1.39, 0.25, GREEN, 3, step=st + 1, arrow=True)
    for k, c in enumerate(['We want the x where the curve crosses the axis.', 'Start at a guess x₀ and go up to the curve.', 'Slide down the tangent line until it hits the axis.', 'That point is the new guess x₁. Go up to the curve again.', 'Slide down the new tangent.', 'x₂ = 1.619 is already close.', 'Two steps: 3 → 2.106 → 1.619. The next gives 1.444, then 1.419. Very fast.']): F.cap(k, c)
    return F


def f_secant():
    F = Fig(0.8, 2.25, -3.2, 5)
    F.axes('x', 'f(x)', ticks=[1, 2])
    F.curve(cubic, 0.85, 2.15, NAVY, 6)
    P = [1, 2, 1.3333, 1.4627, 1.5312]
    F.dot(1, cubic(1), ORANGE, 10, step=1); F.text(1, cubic(1), 'x₀', ORANGE, 26, dx=-8, dy=-22, step=1, bold=True)
    F.dot(2, cubic(2), ORANGE, 10, step=1); F.text(2, cubic(2), 'x₁', ORANGE, 26, dx=34, dy=8, step=1, bold=True)
    F.line(1, -2, 2, 4, RED, 4, step=2, until=5)
    F.dot(P[2], 0, RED, 9, step=3); F.line(P[2], 0, P[2], cubic(P[2]), GREY, 3, step=3, dash='8 7'); F.dot(P[2], cubic(P[2]), ORANGE, 10, step=3)
    F.text(P[2], cubic(P[2]), 'x₂', ORANGE, 26, dx=-12, dy=46, step=3, bold=True)
    F.dot(1, cubic(1), GREY, 10, step=4); F.text(1.0, -2.75, 'oldest point: dropped', GREY, 24, 'start', step=4, dx=-6)
    F.line(2, 4, 1.38, cubic(1.3333) + (1.38 - 1.3333) * (4 - cubic(1.3333)) / (2 - 1.3333), RED, 4, step=5, until=8)
    F.dot(P[3], 0, RED, 9, step=6); F.line(P[3], 0, P[3], cubic(P[3]), GREY, 3, step=6, dash='8 7'); F.dot(P[3], cubic(P[3]), ORANGE, 10, step=6)
    F.text(P[3], cubic(P[3]), 'x₃', ORANGE, 26, dx=30, dy=44, step=6, bold=True)
    s34 = (cubic(P[3]) - cubic(P[2])) / (P[3] - P[2])
    F.line(P[2] - 0.12, cubic(P[2]) - 0.12 * s34, P[4] + 0.1, 0.1 * s34, RED, 4, step=8)
    F.dot(P[4], 0, GREEN, 11, step=9); F.text(1.2, 1.7, 'x₄ = 1.531', GREEN, 26, 'start', step=9, bold=True)
    F.line(1.42, 1.45, 1.52, 0.2, GREEN, 3, step=9, arrow=True)
    for k, c in enumerate(['Like Newton, but we do not know the slope (derivative).', 'Take two starting points on the curve.', 'Draw the straight line through them.', 'Where it crosses the axis is the next point x₂.', 'Forget the oldest point; keep the two newest.', 'Line through the two newest points …', '… gives x₃.', 'Drop the oldest again.', 'The line through x₂ and x₃ is almost the tangent.', 'x₄ = 1.531 (root 1.521): nearly as fast as Newton, with no derivative.']): F.cap(k, c)
    return F


def f_linsys():
    F = Fig(0, 30, 0, 10, pad=(20, 70, 20, 60))
    names = [('one crossing', 'exactly one solution', GREEN), ('parallel', 'no solution', RED), ('same line', 'infinitely many', BLUE)]
    for i, (a, b2, col) in enumerate(names):
        x0 = i * 10.2
        F.raw('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="16" fill="#fbfaf7" stroke="#d5dbe1" stroke-width="3"/>' % (F.X(x0 + 0.1), F.Y(9.7), F.X(9.4) - F.X(0), F.Y(0.2) - F.Y(9.7)), step=i if i else None)
        st = i if i else None
        F.text(x0 + 4.8, 10, a, col, 28, bold=True, dy=-18, step=st)
        F.text(x0 + 4.8, 0, b2, col, 26, bold=True, dy=40, step=st)
    F.line(1, 2, 8.6, 8, NAVY, 5); F.line(1, 8, 8.6, 2.5, ORANGE, 5); F.dot(4.98, 5.13, GREEN, 12)
    F.line(11.2, 2, 18.8, 6.5, NAVY, 5, step=1); F.line(11.2, 4.5, 18.8, 9, ORANGE, 5, step=1)
    F.line(21.4, 2.5, 29, 8, NAVY, 9, step=2); F.line(21.4, 2.5, 29, 8, ORANGE, 4, step=2, dash='14 12')
    F.text(4.8, 1.2, 'det A ≠ 0', GREEN, 25, step=3, bold=True); F.text(15, 1.2, 'det A = 0', RED, 25, step=3, bold=True); F.text(25.2, 1.2, 'det A = 0', BLUE, 25, step=3, bold=True)
    for k, c in enumerate(['Each linear equation in x and y is a straight line. Solving = finding the crossing.', 'Parallel lines never meet: the equations contradict each other.', 'The same line twice: every point on it is a solution.', 'One number, the determinant, tells the cases apart.']): F.cap(k, c)
    return F


def _matrix(F, x, y, cells, step_of=None, cs=62, label=None, colf=None):
    """cells: list of rows of strings; step_of(i, j) -> (step, until) or None."""
    n = len(cells); m = len(cells[0])
    F.raw('<path d="M%d,%d h-12 v%d h12 M%d,%d h12 v%d h-12" fill="none" stroke="%s" stroke-width="4"/>' % (x, y - 6, n * cs + 12, x + m * cs, y - 6, n * cs + 12, NAVY))
    for i in range(n):
        for j in range(m):
            st = step_of(i, j) if step_of else None
            col = colf(i, j) if colf else NAVY
            F.text(x + j * cs + cs / 2, y + i * cs + cs / 2 + 10, cells[i][j], col, 30, px=True, bold=True, step=st[0] if st else None, until=st[1] if st else None)
    if label: F.text(x + m * cs / 2, y + n * cs + 46, label, GREY, 24, px=True)


def f_gauss():
    F = Fig(0, 1, 0, 1)
    full = [['×'] * 3 + ['b'] for _ in range(3)]
    _matrix(F, 50, 150, full, label='3 equations, mixed up', colf=lambda i, j: BLUE if j == 3 else NAVY)
    F.line(318, 243, 372, 243, ORANGE, 6, step=1, arrow=True, px=True); F.text(345, 128, 'eliminate', ORANGE, 24, px=True, step=1, bold=True)
    tri = [['×', '×', '×', 'b'], ['0', '×', '×', 'b'], ['0', '0', '×', 'b']]
    def st(i, j):
        if j < i: return (2 if j == 0 else 3, None)
        return (1, None)
    _matrix(F, 400, 150, tri, step_of=st, colf=lambda i, j: RED if j < i else (BLUE if j == 3 else NAVY))
    F.text(524, 382, 'triangle of zeros', RED, 24, px=True, step=3, bold=True)
    F.line(668, 243, 730, 243, GREEN, 6, step=4, arrow=True, px=True); F.text(700, 128, 'solve upwards', GREEN, 24, px=True, step=4, bold=True)
    for i, (lab, s_) in enumerate([('x₁ = …', 6), ('x₂ = …', 5), ('x₃ = …', 4)]):
        F.box(760, 150 + i * 62 + 4, 190, 54, lab, GREEN, step=s_, size=26)
    F.raw('<path d="M970,315 V185" fill="none" stroke="%s" stroke-width="5" marker-end="url(#m%s)"/>' % (GREEN, GREEN[1:]), step=5); F.marks.add(GREEN)
    F.text(500, 60, 'Gaussian elimination: make zeros, then solve from the bottom', NAVY, 28, px=True, bold=True)
    F.text(500, 470, 'Last row has one unknown → put it in the row above → and so on.', INK, 25, px=True, step=4)
    for k, c in enumerate(['Three equations with all the unknowns mixed together.', 'Subtract multiples of row 1 from the rows below …', '… so that column 1 gets zeros below the top entry.', 'Do the same with column 2. Now the matrix is a triangle.', 'The last row has only one unknown: solve it directly.', 'Put that value into the row above: one unknown again.', 'Work upwards to the top. This is back substitution.']): F.cap(k, c)
    return F


def f_lu():
    F = Fig(0, 1, 0, 1)
    def sq(x, y, kind, col, label, step=None):
        a = (' data-s="%d"' % step) if step else ''
        if step: F.n = max(F.n, step)
        F.raw('<rect x="%d" y="%d" width="150" height="150" fill="#fbfaf7" stroke="%s" stroke-width="4"%s/>' % (x, y, NAVY, a))
        if kind == 'L': F.raw('<polygon points="%d,%d %d,%d %d,%d" fill="%s"%s/>' % (x, y, x, y + 150, x + 150, y + 150, col, a))
        if kind == 'U': F.raw('<polygon points="%d,%d %d,%d %d,%d" fill="%s"%s/>' % (x, y, x + 150, y, x + 150, y + 150, col, a))
        if kind == 'A': F.raw('<rect x="%d" y="%d" width="150" height="150" fill="%s"%s/>' % (x, y, col, a))
        F.text(x + 75, y + 190, label, NAVY, 30, px=True, bold=True, step=step)
    sq(80, 60, 'A', '#c9d6e3', 'A  (full)')
    F.text(280, 150, '=', NAVY, 54, px=True, step=1, bold=True)
    sq(330, 60, 'L', '#f2c9a5', 'L  (lower)', 1)
    F.text(530, 150, '×', NAVY, 48, px=True, step=1, bold=True)
    sq(580, 60, 'U', '#b9d3ee', 'U  (upper)', 1)
    F.text(860, 110, 'done once', ORANGE, 26, px=True, step=1, bold=True); F.text(860, 146, '(the costly part)', GREY, 23, px=True, step=1)
    y = 400
    F.box(40, y, 90, 80, 'b', BLUE, step=2, size=34)
    F.line(130, y + 40, 196, y + 40, ORANGE, 6, step=3, arrow=True, px=True)
    F.box(204, y, 220, 80, 'solve L y = b', ORANGE, step=3, size=25)
    F.line(424, y + 40, 490, y + 40, ORANGE, 6, step=3, arrow=True, px=True)
    F.box(498, y, 80, 80, 'y', ORANGE, step=3, size=34)
    F.line(578, y + 40, 644, y + 40, BLUE, 6, step=4, arrow=True, px=True)
    F.box(652, y, 220, 80, 'solve U x = y', BLUE, step=4, size=25)
    F.line(872, y + 40, 908, y + 40, BLUE, 6, step=4, arrow=True, px=True)
    F.box(914, y, 70, 80, 'x', GREEN, step=4, size=34)
    F.text(500, 345, 'for every new right-hand side b: two easy triangular solves', INK, 25, px=True, step=2)
    F.raw('<path d="M949,485 V545 H85 V490" fill="none" stroke="%s" stroke-width="4" stroke-dasharray="10 8" marker-end="url(#m%s)"/>' % (GREEN, GREEN[1:]), step=5); F.marks.add(GREEN)
    F.text(520, 580, 'new b? reuse L and U', GREEN, 25, px=True, step=5, bold=True)
    for k, c in enumerate(['A full matrix is hard to solve with.', 'Split it once into a lower triangle L times an upper triangle U.', 'Now take a right-hand side b.', 'Triangle 1: solve L y = b from the top down (easy).', 'Triangle 2: solve U x = y from the bottom up (easy).', 'Another b? Skip the splitting: L and U are reused.']): F.cap(k, c)
    return F


def f_jacobi():
    F = Fig(0, 1, 0, 1)
    cx, cy, d = 330, 300, 170
    pts = {'top': (cx, cy - d, '100'), 'bottom': (cx, cy + d, '0'), 'left': (cx - d, cy, '50'), 'right': (cx + d, cy, '50')}
    F.raw('<path d="M%d,%d H%d M%d,%d V%d" stroke="#d5dbe1" stroke-width="5" fill="none"/>' % (cx - d, cy, cx + d, cx, cy - d, cy + d))
    for k, (x, y, v) in pts.items():
        F.raw('<circle cx="%d" cy="%d" r="46" fill="%s" stroke="%s" stroke-width="4"/>' % (x, y, '#dbe8f6', BLUE))
        F.text(x, y + 11, v, NAVY, 32, px=True, bold=True)
    F.raw('<circle cx="%d" cy="%d" r="52" fill="#fbe6d4" stroke="%s" stroke-width="5"/>' % (cx, cy, ORANGE))
    F.text(cx, cy + 12, '?', ORANGE, 40, px=True, bold=True, step=1, until=3)
    for (x, y, v) in pts.values():
        ux, uy = (cx - x) / d, (cy - y) / d
        F.line(x + ux * 52, y + uy * 52, cx - ux * 62, cy - uy * 62, ORANGE, 5, step=2, arrow=True, px=True)
    F.text(cx, cy + 12, '50', ORANGE, 36, px=True, bold=True, step=3)
    F.text(760, 150, 'new value =', INK, 28, px=True, step=2)
    F.text(760, 200, 'average of the 4 neighbours', ORANGE, 28, px=True, step=2, bold=True)
    F.text(760, 262, '(100 + 0 + 50 + 50) / 4 = 50', NAVY, 28, px=True, step=3, bold=True)
    F.box(580, 330, 360, 70, 'do this at every point', BLUE, step=4, size=25)
    F.box(580, 430, 360, 70, 'repeat until nothing changes', GREEN, step=5, size=23)
    F.line(760, 400, 760, 426, BLUE, 5, step=5, arrow=True, px=True)
    F.raw('<path d="M940,465 H975 V365 H948" fill="none" stroke="%s" stroke-width="5" marker-end="url(#m%s)"/>' % (GREEN, GREEN[1:]), step=5); F.marks.add(GREEN)
    for k, c in enumerate(['A point on a heated plate, surrounded by four neighbours.', 'We do not know its temperature yet: start with any guess.', 'Rule: a point is the average of its neighbours.', 'So replace the guess by that average.', 'One "sweep" applies the rule at every point of the grid.', 'Sweep again and again. The numbers settle to the solution of Ax = b.']): F.cap(k, c)
    return F


def f_difftable():
    F = Fig(0, 1, 0, 1)
    cols = [('x', ['1', '2', '3', '4'], GREY), ('y', ['1', '8', '27', '64'], NAVY), ('Δy', ['7', '19', '37'], ORANGE), ('Δ²y', ['12', '18'], BLUE), ('Δ³y', ['6'], GREEN)]
    X0, dx, Y0, dy = 110, 190, 150, 100
    for c, (name, vals, col) in enumerate(cols):
        st = None if c < 2 else c - 1 + (c - 2)
        F.text(X0 + c * dx, 80, name, col, 32, px=True, bold=True, step=st, italic=True)
        for r, v in enumerate(vals):
            y = Y0 + r * dy + (c - 1) * dy / 2 if c >= 1 else Y0 + r * dy
            F.text(X0 + c * dx, y + 10, v, col, 34, px=True, bold=True, step=st)
            if c >= 2:
                x1 = X0 + (c - 1) * dx + 44; x2 = X0 + c * dx - 40
                F.line(x1, y - dy / 2 + 4, x2, y - 6, col, 3, step=st, arrow=True, px=True)
                F.line(x1, y + dy / 2 - 4, x2, y + 6, col, 3, step=st, arrow=True, px=True)
    F.raw('<line x1="60" y1="105" x2="940" y2="105" stroke="#d5dbe1" stroke-width="3"/>')
    F.text(X0 + 2 * dx, 540, '8 − 1 = 7,  27 − 8 = 19, …', ORANGE, 26, px=True, step=1, bold=True)
    F.text(X0 + 3 * dx + 60, 540, '19 − 7 = 12, …', BLUE, 26, px=True, step=3, bold=True)
    F.text(X0 + 4 * dx, 300, 'constant!', GREEN, 26, px=True, step=6, bold=True, dy=70)
    for k, c in enumerate(['A table of values: here y = x³ at equally spaced x.', 'Subtract each value from the one below it: first differences Δy.', 'Each difference sits between the two numbers it came from.', 'Do the same to the Δy column: second differences.', 'The arrows always point from a pair to its difference.', 'Once more: third differences.', 'For a cubic the third differences are constant. The table reveals the pattern in the data.']): F.cap(k, c)
    return F


def f_newtoninterp():
    xs = [0, 1, 2, 3, 4]; ys = [1.0, 1.8, 3.4, 4.0, 3.1]
    P = lagrange(xs, ys)
    F = Fig(-0.5, 4.6, 0, 5.2)
    F.axes('x', 'y', ticks=[0, 1, 2, 3, 4])
    for x, y in zip(xs, ys): F.dot(x, y, NAVY, 11)
    F.text(2, 4.95, 'known: only the five dots', NAVY, 26, bold=True, bg=True)
    F.dot(0.5, 0, RED, 9, step=1); F.text(0.5, 0, 'x = 0.5 ?', RED, 26, dy=-18, dx=64, step=1, bold=True)
    F.curve(P, -0.2, 4.3, ORANGE, 5, step=2)
    F.line(0.5, 0, 0.5, P(0.5), RED, 4, step=3, dash='8 7'); F.dot(0.5, P(0.5), RED, 11, step=3)
    F.line(0.5, P(0.5), 0, P(0.5), RED, 4, step=3, arrow=True)
    F.band(-0.1, 1.5, GREEN, step=4, op=0.13); F.text(0.7, 3.2, 'near the start:', GREEN, 25, step=4, bold=True); F.text(0.7, 2.85, 'forward formula', GREEN, 25, step=4, bold=True)
    F.band(2.5, 4.1, BLUE, step=5, op=0.13); F.text(3.3, 1.5, 'near the end:', BLUE, 25, step=5, bold=True); F.text(3.3, 1.15, 'backward formula', BLUE, 25, step=5, bold=True)
    for k, c in enumerate(['We measured y only at five equally spaced x values.', 'What is y between the dots, for example at x = 0.5?', 'Draw one smooth polynomial through all five dots.', 'Read the value off the curve. That is interpolation.', 'Near the top of the table, build the curve from the first row of differences.', 'Near the bottom, build it from the last row. Same curve, smaller error.']): F.cap(k, c)
    return F


def f_lagrange():
    xs = [0, 1.5, 3]; ys = [1.0, 2.6, 1.6]
    def basis(i):
        return lambda x: ys[i] * math.prod((x - xs[j]) / (xs[i] - xs[j]) for j in range(3) if j != i)
    F = Fig(-0.5, 3.6, -0.9, 3.4)
    F.axes('x', 'y', ticks=[(0, 'x₀'), (1.5, 'x₁'), (3, 'x₂')])
    cols = [ORANGE, BLUE, GREEN]
    for i in range(3): F.dot(xs[i], ys[i], NAVY, 12)
    for i in range(3):
        F.curve(basis(i), -0.3, 3.3, cols[i], 4, step=i + 1)
        F.dot(xs[i], ys[i], cols[i], 8, step=i + 1)
        for j in range(3):
            if j != i: F.dot(xs[j], 0, cols[i], 7, step=i + 1, hollow=True)
    F.text(1.5, -0.78, 'orange: right at dot 0, zero at x₁ and x₂', ORANGE, 23, step=1, bold=True)
    F.curve(lagrange(xs, ys), -0.3, 3.3, NAVY, 7, step=4)
    F.text(2.35, 2.75, 'sum of the three', NAVY, 26, step=4, bold=True, anchor='start', dx=10)
    for k, c in enumerate(['Three dots, not necessarily equally spaced.', 'Build a small curve that passes through dot 0 and is zero at the other x values.', 'Another one for dot 1: correct there, zero at x₀ and x₂.', 'And one for dot 2.', 'Add the three curves. At each x only one of them is non-zero, so the sum passes through every dot.']): F.cap(k, c)
    return F


def f_spline():
    xs = [-1 + 0.25 * i for i in range(9)]; ys = [1 / (1 + 25 * x * x) for x in xs]
    P = lagrange(xs, ys); S = natural_spline(xs, ys)
    F = Fig(-1.12, 1.12, -1.25, 1.35)
    F.axes('x', '', x=-1.12)
    for x, y in zip(xs, ys): F.dot(x, y, NAVY, 10)
    F.curve(P, -1, 1, RED, 5, step=1, n=160)
    F.text(0, -0.95, 'one degree-8 polynomial: wild at the ends', RED, 25, step=1, bold=True)
    F.curve(S, -1, 1, GREEN, 6, step=2, n=160)
    F.text(0.3, 0.95, 'spline: small cubic pieces', GREEN, 26, 'start', step=2, bold=True)
    for x in xs[1:-1]: F.line(x, -0.08, x, 0.08, GREEN, 4, step=3)
    F.text(0, -0.42, 'pieces join smoothly at every dot', GREEN, 24, step=3, bold=True, bg=True)
    for k, c in enumerate(['Nine dots from a bell-shaped curve.', 'One polynomial through all nine: it swings wildly near the ends (Runge phenomenon).', 'A spline: a separate small cubic between each pair of dots.', 'At each dot the pieces agree in value, slope and bending, so the join is invisible.']): F.cap(k, c)
    return F


def f_numdiff():
    f = lambda x: 0.5 * math.exp(x)
    x, h = 1.0, 0.75
    F = Fig(-0.1, 2.2, -0.4, 4.2)
    F.axes('x', 'f(x)', ticks=[(x - h, 'x − h'), (x, 'x'), (x + h, 'x + h')])
    F.curve(f, 0, 2.05, NAVY, 6)
    F.dot(x, f(x), NAVY, 11)
    t = lambda u: f(x) + f(x) * (u - x)
    F.line(0.35, t(0.35), 1.75, t(1.75), GREEN, 4, step=1); F.text(0.45, 0.2, 'tangent (true slope)', GREEN, 25, 'start', step=1, bold=True)
    F.dot(x + h, f(x + h), ORANGE, 10, step=2); F.line(x, f(x), x + h, f(x + h), ORANGE, 4, step=2)
    F.text(1.2, 3.3, 'forward: too steep', ORANGE, 25, 'end', step=2, bold=True)
    F.dot(x - h, f(x - h), BLUE, 10, step=3); F.line(x - h, f(x - h), x + h, f(x + h), BLUE, 4, step=3, dash='12 9')
    F.text(0.02, 2.75, 'central: almost parallel', BLUE, 25, 'start', step=3, bold=True)
    F.text(0.02, 2.42, 'to the tangent', BLUE, 25, 'start', step=3, bold=True)
    F.line(x, f(x), x + h, f(x), GREY, 3, step=4, dash='6 6'); F.line(x + h, f(x), x + h, f(x + h), GREY, 3, step=4, dash='6 6')
    F.text(x + h / 2, f(x), 'run h', GREY, 24, dy=30, step=4, italic=True); F.text(x + h, (f(x) + f(x + h)) / 2, 'rise', GREY, 24, 'start', dx=12, step=4, italic=True)
    for k, c in enumerate(['The derivative at x is the slope of the tangent there.', 'We cannot see the tangent directly: we only have values of f.', 'Forward difference: the slope of the line to the next point.', 'Central difference: the slope between the two neighbours. Much closer to the tangent.', 'Slope = rise ÷ run. Shrink h and the line turns into the tangent.']): F.cap(k, c)
    return F


def f_integration():
    f = lambda x: 2.2 + 1.3 * math.sin(1.25 * x) + 0.12 * x
    F = Fig(-0.3, 4.5, 0, 4.4)
    F.axes('x', 'f(x)', ticks=[(0, 'a'), (4, 'b')])
    F.curve(f, 0, 4, NAVY, 6)
    F.line(0, 0, 0, f(0), NAVY, 3); F.line(4, 0, 4, f(4), NAVY, 3)
    F.text(2, 0.55, 'area under the curve = ?', NAVY, 28, bold=True, step=0, until=1)
    for i in range(4):
        F.poly([(i, 0), (i, f(i)), (i + 1, f(i + 1)), (i + 1, 0)], ORANGE, 3, step=1 + (i > 0) * 1, until=4, fill=ORANGE, op=0.2, close=True)
    F.text(2.0, 4.05, '4 strips with straight tops (trapezoids)', ORANGE, 25, step=2, until=4, bold=True)
    F.text(0.5, f(0.5), 'gap', RED, 23, dy=-6, step=3, until=4, bold=True, dx=4); F.text(2.6, f(2.6), 'gap', RED, 23, dy=44, dx=10, step=3, until=4, bold=True)
    for a in (0, 2):
        P = lagrange([a, a + 1, a + 2], [f(a), f(a + 1), f(a + 2)])
        pts = [(a, 0)] + [(a + 2 * j / 30, P(a + 2 * j / 30)) for j in range(31)] + [(a + 2, 0)]
        F.poly(pts, GREEN, 3, step=4, fill=GREEN, op=0.2, close=True)
    F.text(2.0, 4.05, 'curved tops (parabolas): Simpson. Gaps almost gone', GREEN, 25, step=4, bold=True)
    for k, c in enumerate(['An integral is the area under a curve.', 'Cut the area into strips. One strip with a straight top is a trapezoid: easy area.', 'Add the strips: that is the trapezoidal rule.', 'Small gaps remain where the curve bends. More strips make them smaller.', 'Simpson\'s rule uses curved tops (parabolas over two strips): far more accurate for the same work.']): F.cap(k, c)
    return F


def f_euler():
    F = Fig(-0.15, 2.25, 0, 8)
    F.axes('x', 'y', ticks=[0.5, 1, 1.5, 2])
    F.curve(math.exp, 0, 2.02, NAVY, 6); F.text(1.62, math.exp(1.62), 'true solution', NAVY, 26, 'end', dx=-16, dy=-8, bold=True)
    x, y = 0.0, 1.0
    F.dot(x, y, ORANGE, 11, step=1); F.text(x, y, 'start', ORANGE, 25, dy=-18, dx=42, step=1, bold=True)
    for i in range(4):
        yn = y + 0.5 * y
        F.line(x, y, x + 0.5, yn, ORANGE, 5, step=i + 2, arrow=True); F.dot(x + 0.5, yn, ORANGE, 9, step=i + 2)
        x += 0.5; y = yn
    F.line(2, y, 2, math.exp(2), RED, 5, step=6); F.text(2, (y + math.exp(2)) / 2, 'error', RED, 26, 'start', dx=12, step=6, bold=True)
    F.text(0.8, 7.1, 'each arrow: follow the slope y′', ORANGE, 25, step=2, bold=True); F.text(0.8, 6.5, 'for one step h', ORANGE, 25, step=2, bold=True)
    for k, c in enumerate(['A differential equation gives the slope y′ at every point, not y itself.', 'We know one point: the starting value.', 'Compute the slope there and walk along it for one step h.', 'At the new point compute the slope again and take another step.', 'Repeat: a chain of short straight pieces.', 'Each piece leaves the true curve a little …', '… and the errors pile up. Smaller steps (or a smarter method) reduce the gap.']): F.cap(k, c)
    return F


def f_rk4():
    F = Fig(-0.12, 1.42, 0.7, 3.6)
    F.axes('x', 'y', y=0.7, x=-0.12, ticks=[(0, 'xₙ'), (0.5, 'xₙ + h/2'), (1, 'xₙ + h')])
    F.curve(math.exp, 0, 1.12, NAVY, 6); F.text(0.3, 1.02, 'true solution', NAVY, 25, 'start', bold=True); F.line(0.36, 1.1, 0.32, 1.33, NAVY, 3, arrow=True)
    F.dot(0, 1, NAVY, 11)
    def slope(x, y, k, col, name, st, dxl, dyl, anchor='start'):
        d = 0.2
        F.line(x, y, x + d, y + d * k, col, 6, step=st, arrow=True)
        F.dot(x, y, col, 9, step=st)
        F.text(x, y, name, col, 25, anchor, dx=dxl, dy=dyl, step=st, bold=True)
    slope(0, 1, 1, ORANGE, 'k₁: slope at the start', 1, 26, 40)
    slope(0.5, 1.5, 1.5, BLUE, 'k₂: slope at the middle', 2, 30, 34)
    slope(0.5, 1.75, 1.75, GREEN, 'k₃: middle again', 3, -16, -14, 'end')
    slope(1, 2.75, 2.75, RED, 'k₄: slope at the end', 4, -18, -16, 'end')
    F.line(0, 1, 0.985, 2.69, NAVY, 4, step=5, arrow=True, dash='12 8'); F.dot(1, 2.7083, GREEN, 12, step=5)
    F.text(0.02, 3.3, 'one step with the average slope (k₁ + 2k₂ + 2k₃ + k₄)/6', NAVY, 24, 'start', step=5, bold=True)
    F.dot(1, 2.0, ORANGE, 9, step=6, hollow=True); F.text(1, 2.0, 'Euler lands at 2.00', ORANGE, 24, 'start', dx=16, dy=8, step=6, bold=True)
    F.text(1, 2.7083, 'RK4: 2.708', GREEN, 24, 'start', dx=20, dy=24, step=6, bold=True)
    for k, c in enumerate(['Euler used one slope, measured only at the start of the step.', 'RK4 samples four slopes. k₁: the slope at the start.', 'k₂: the slope at the middle of the step, reached using k₁.', 'k₃: the middle again, reached using the better slope k₂.', 'k₄: the slope at the end, reached using k₃.', 'Take one step with a weighted average: the middle slopes count double.', 'Result 2.708 against the true 2.718. Euler with the same step: 2.00.']): F.cap(k, c)
    return F


def f_leastsq():
    xs = [2, 4, 5, 7, 9, 11]; ys = [14, 21, 24, 30, 37, 42]
    yv = [11.5, 24.5, 21, 34, 33.5, 45]
    a, b = 0, 0
    n = len(xs); sx, sy = sum(xs), sum(yv); sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, yv))
    b = (n * sxy - sx * sy) / (n * sxx - sx * sx); a = (sy - b * sx) / n
    F = Fig(0, 12.5, 0, 52)
    F.axes('x', 'y', ticks=[2, 4, 6, 8, 10, 12])
    for x, y in zip(xs, yv): F.dot(x, y, NAVY, 11)
    F.line(1, 20, 12, 36, GREY, 4, step=1, until=3, dash='10 8'); F.text(11.6, 34, 'this line?', GREY, 24, 'end', step=1, until=3, dy=30)
    F.line(1, 3, 12, 50, GREY, 4, step=1, until=3, dash='10 8'); F.text(9, 47.5, 'or this one?', GREY, 24, 'end', step=1, until=3, dx=-12)
    F.line(1, a + b, 12, a + 12 * b, ORANGE, 6, step=3)
    for x, y in zip(xs, yv):
        F.line(x, y, x, a + b * x, RED, 5, step=4)
    F.text(4.0, 30.5, 'residual = miss', RED, 25, 'end', step=4, bold=True, dx=-8)
    for x, y in zip(xs, yv):
        r = y - (a + b * x); side = abs(r) / 52 * (F.Y(0) - F.Y(52))
        yt = F.Y(max(y, a + b * x))
        F.raw('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="0.22" stroke="%s" stroke-width="2"/>' % (F.X(x), yt, side, side, RED, RED), step=5)
    F.text(8.2, 8, 'best line: total area of the squares is smallest', ORANGE, 25, step=5, bold=True)
    for k, c in enumerate(['Measured data never lie exactly on a line.', 'Many lines look reasonable. Which one is "best"?', 'We need a rule to score a line.', 'Take a candidate line.', 'For each dot, measure the vertical miss (the residual).', 'Square each miss and add them up. Least squares picks the line with the smallest total.']): F.cap(k, c)
    return F


def f_linearise():
    t = [0, 1, 2, 3, 4, 5]; N = [100, 150, 230, 340, 510, 770]
    F = Fig(0, 20, 0, 10, pad=(20, 50, 20, 50))
    # left panel: N against t
    def L(x, y): return (1.2 + x * 1.3, 0.8 + y / 800 * 8)
    def R(x, y): return (12.2 + x * 1.3, 0.8 + (y - 4.4) / 2.5 * 8)
    for (ox, name) in ((1.2, 'count N'), (12.2, 'ln N')):
        F.line(ox - 0.2, 0.8, ox + 7.4, 0.8, GREY, 3, arrow=True, step=None if ox < 5 else 2); F.line(ox, 0.6, ox, 9.4, GREY, 3, arrow=True, step=None if ox < 5 else 2)
        F.text(ox + 0.2, 9.5, name, GREY, 25, 'start', step=None if ox < 5 else 2, italic=True); F.text(ox + 7.3, 0.8, 'time t', GREY, 24, 'end', dy=34, step=None if ox < 5 else 2, italic=True)
    for x, y in zip(t, N): F.dot(*L(x, y), NAVY, 10)
    F.poly([L(x / 10, 100.3 * math.exp(0.4077 * x / 10)) for x in range(51)], ORANGE, 5, step=1)
    F.text(4.0, 8.3, 'a curve: N = a·eᵇᵗ', ORANGE, 25, step=1, bold=True)
    F.raw('<path d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="6" marker-end="url(#m%s)"/>' % (F.X(8.6), F.Y(5.3), F.X(9.6), F.Y(6.3), F.X(10.4), F.Y(6.3), F.X(11.4), F.Y(5.3), RED, RED[1:]), step=2); F.marks.add(RED)
    F.text(10, 7.0, 'take ln', RED, 27, step=2, bold=True)
    for x, y in zip(t, N): F.dot(*R(x, math.log(y)), NAVY, 10, step=3)
    p0, p1 = R(-0.2, 4.608 - 0.2 * 0.4077), R(5.3, 4.608 + 5.3 * 0.4077)
    F.line(p0[0], p0[1], p1[0], p1[1], GREEN, 5, step=4)
    F.text(16.6, 3.2, 'a straight line!', GREEN, 26, step=4, bold=True); F.text(16.6, 2.4, 'ln N = ln a + b·t', GREEN, 25, step=4, bold=True)
    F.text(16.6, 1.5, 'slope = b,  intercept = ln a', INK, 23, step=5)
    for k, c in enumerate(['Bacteria counts: they grow faster and faster.', 'The model is an exponential curve. A line fit (Lecture 23) cannot handle it directly.', 'Trick: take the logarithm of every count.', 'Plot ln N against t …', '… the dots now lie on a straight line.', 'Fit that line with last lecture\'s formulas, then read b and a from its slope and intercept.']): F.cap(k, c)
    return F


def f_descent():
    F = Fig(-10, 10, -5.2, 5.2, pad=(30, 30, 30, 30))
    for r in (1.2, 2.4, 3.6, 4.8, 6.0, 7.4):
        F.raw('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-opacity="0.45" stroke-width="3"/>' % (F.X(0), F.Y(0), (F.X(r * 1.3) - F.X(0)), (F.Y(0) - F.Y(r * 0.65)), BLUE))
    F.dot(0, 0, GREEN, 9); F.text(0, 0, 'lowest point', GREEN, 24, dy=42, bold=True, bg=True)
    F.text(-9.7, -4.9, 'rings = contour lines, like a map of a valley', BLUE, 24, 'start', bg=True)
    def gd(x, y, eta, n):
        pts = [(x, y)]
        for _ in range(n):
            x, y = x - eta * x / 1.69, y - eta * y / 0.4225
            pts.append((x, y))
        return pts
    x, y = -8.6, 3.6
    F.dot(x, y, ORANGE, 12, step=1); F.text(x, y, 'start', ORANGE, 25, dy=-22, step=1, bold=True)
    good = gd(x, y, 0.35, 12)
    for i in range(12):
        F.line(good[i][0], good[i][1], good[i + 1][0], good[i + 1][1], ORANGE, 5, step=min(i // 2 + 2, 6), arrow=(i < 6))
    F.text(9.7, 4.7, 'each step: straight downhill (−gradient),', ORANGE, 24, 'end', step=2, bold=True, bg=True)
    F.text(9.7, 4.0, 'length = learning rate η × slope', ORANGE, 24, 'end', step=2, bold=True, bg=True)
    bad = gd(-8.6, 3.6, 0.88, 4)
    for i in range(4):
        F.line(bad[i][0], bad[i][1], bad[i + 1][0], bad[i + 1][1], RED, 4, step=7, arrow=True, dash='10 8')
    F.text(9.7, -4.2, 'η too large: jumps across the valley,', RED, 24, 'end', step=7, bold=True, bg=True)
    F.text(9.7, -4.9, 'each time landing higher', RED, 24, 'end', step=7, bold=True, bg=True)
    for k, c in enumerate(['A function of two variables drawn as a map: each ring is one height.', 'Start anywhere. We want the bottom of the valley.', 'Feel which way is steepest downhill and take a step that way.', 'Look again from the new place, step again.', 'The steps get shorter as the ground flattens.', 'Keep going …', '… until the bottom: the minimum.', 'If the steps are too long, each one jumps across the valley and lands higher. The learning rate matters.']): F.cap(k, c)
    return F


FIGS = {1: f_iteration, 2: f_float, 3: f_taylor, 4: f_errors, 5: f_condition, 6: f_bisection, 7: f_falsepos, 8: f_fixedpoint, 9: f_newton, 10: f_secant,
        11: f_linsys, 12: f_gauss, 13: f_lu, 14: f_jacobi, 15: f_difftable, 16: f_newtoninterp, 17: f_lagrange, 18: f_spline, 19: f_numdiff, 20: f_integration,
        21: f_euler, 22: f_rk4, 23: f_leastsq, 24: f_linearise, 25: f_descent}
