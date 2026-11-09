LECTURE = dict(
    title='Spline Interpolation and the Runge Phenomenon',
    short='Splines and the Runge Phenomenon',
    sub='Why one polynomial through many equally spaced points can be disastrous, how Chebyshev points and piecewise polynomials fix it, and how a natural cubic spline is built from one tridiagonal system.',
    slides=[
        dict(type='cover', id='cover', notes="Opening question: 'If 5 points give a decent curve, will 21 points give a better one?' Most students say yes. Today's first slide shows the opposite, then fixes it."),
        dict(type='bullets', id='hook', title='The problem: more data, worse curve', kick='Why this lecture', rw=620,
             lead='Interpolate the smooth bell-shaped $f(x) = \\dfrac{1}{1 + 25x^2}$ on $[-1, 1]$ with $n$ equally spaced points and one polynomial of degree $n - 1$.',
             items=['5 points: largest error 0.44, poor but tame', '11 points: the curve swings to <b>1.92</b> near the ends; the function itself never exceeds 1', '21 points: error <b>60</b>. More data made it worse',
                    'The same happens to any long data set (sensor logs, profiles, fonts): we need a different idea'],
             frag=True,
             right=dict(table=[['points $n$', 'largest error'], [['5', '0.44'], ['9', '1.05'], ['11', '1.92'], ['15', '7.19'], ['21', '59.8']]]),
             notes="This is Runge's example (1901). The function is perfectly smooth (infinitely differentiable); the problem is the method, not the data.\n\nSolved at the end: with 11 points, a natural cubic spline has error 0.022; with 21 points 0.003."),
        dict(type='goals', id='goals', items=[
            'Explain the <b>Runge phenomenon</b> from the interpolation error term',
            'Reduce it with <b>Chebyshev points</b> when the points can be chosen',
            'Build <b>linear</b> and <b>natural cubic splines</b> and state their conditions',
            'Set up and solve the <b>tridiagonal system</b> for the spline (Thomas, Lecture 13)',
            'Choose between polynomial, spline and least-squares fits'],
            prev='Lagrange and divided differences: one polynomial through all the points.',
            today='When one polynomial fails, use many small ones joined smoothly.',
            notes="This lecture ties Module 3 (tridiagonal solver) to Module 4."),
        dict(type='math', id='why', title='Why it happens: the node polynomial',
             eqs=[dict(cap='Interpolation error with n + 1 points (Lectures 16–17)', eq='\\begin{aligned} f(x) - P_n(x) &= \\frac{f^{(n+1)}(\\xi)}{(n+1)!}\\,\\omega(x) \\\\ \\omega(x) &= (x - x_0)(x - x_1)\\cdots(x - x_n) \\end{aligned}'),
                  dict(cap='Chebyshev points: crowd the points towards the ends', eq='x_i = \\cos\\frac{(2i+1)\\pi}{2(n+1)}, \\qquad i = 0, \\dots, n', frag=True)],
             items=['With equal spacing $|\\omega(x)|$ is <b>much larger near the ends</b> than in the middle', 'For Runge\'s $f$ the derivatives $f^{(n+1)}$ also grow very fast with $n$', 'Chebyshev points make $|\\omega|$ as small and even as possible: 11 points give error 0.11 instead of 1.92',
                    'But data usually come at fixed places: we cannot choose the points'],
             ifrag=True, rw=640,
             notes="Plot ω(x) for 11 equally spaced points on the board (or use the widget): it is tiny in the middle and about 100 times larger near ±1.\n\nChebyshev points are the projections onto the x-axis of equally spaced points on a semicircle."),
        dict(type='widget', id='explore', title='Explore: the Runge phenomenon', w='runge', o=dict(n=11, cheb=True, lin=False, cub=False, height='380px'), lw=460,
             items=['Increase $n$ for the equally spaced polynomial: the ends explode', 'Turn on <b>Chebyshev points</b> (hollow dots): the error now falls', 'Turn on the <b>splines</b>: small errors with equal spacing', 'Try $|x|$ and the step: polynomials struggle with corners and jumps'],
             notes="Keep the table visible: it gives the largest error for each method. Typical numbers at n = 11: equal spacing 1.92, Chebyshev 0.11, linear spline 0.067, cubic spline 0.022."),
        dict(type='math', id='linear', title='Piecewise idea 1: the linear spline',
             eqs=[dict(cap='On each interval [xᵢ, xᵢ₊₁], a straight line', eq='S(x) = y_i + \\frac{y_{i+1} - y_i}{x_{i+1} - x_i}(x - x_i)'),
                  dict(cap='Error on an interval of width h', eq='|f(x) - S(x)| \\le \\frac{h^2}{8}\\max|f\'\'|', frag=True)],
             items=['Each piece uses only its two neighbours: no wild swings', 'Error falls like $h^2$: halve the spacing, quarter the error', 'But the curve has <b>corners</b>: the slope jumps at every data point', 'Fine for tables and plots; not smooth enough for motion, fonts or physics'],
             ifrag=True,
             notes="The h²/8 bound comes from the error term with n = 1: |(x − x_i)(x − x_{i+1})| ≤ h²/4, divided by 2!."),
        dict(type='math', id='cubic', title='Piecewise idea 2: the cubic spline',
             eqs=[dict(cap='One cubic on each interval [xᵢ, xᵢ₊₁], joined smoothly', eq="S(x_i) = y_i, \\qquad S,\\; S',\\; S'' \\text{ continuous}"),
                  dict(cap='Unknowns Mᵢ = S″(xᵢ); for each inner point (spacings hᵢ = xᵢ₊₁ − xᵢ)', eq='h_{i-1}M_{i-1} + 2(h_{i-1} + h_i)M_i + h_iM_{i+1} = 6\\left(\\frac{y_{i+1} - y_i}{h_i} - \\frac{y_i - y_{i-1}}{h_{i-1}}\\right)', frag=True),
                  dict(cap='Natural spline: no curvature at the two ends', eq='M_0 = M_n = 0', frag=True)],
             items=['Each piece has 4 coefficients: $4n$ unknowns, and the joining rules give $4n - 2$ equations; two end conditions complete it', 'The $M_i$ equations are <b>tridiagonal</b> and diagonally dominant: Thomas algorithm, $O(n)$', 'Like a thin flexible ruler (a draughtsman\'s spline) bent through pins'],
             ifrag=True, rw=600,
             notes="Derivation (outline): S'' is linear on each interval, so S'' = M_i(x_{i+1} − x)/h_i + M_{i+1}(x − x_i)/h_i; integrate twice and fit S(x_i) = y_i, S(x_{i+1}) = y_{i+1}; then require S' to be continuous at x_i: that gives the M equation.\n\nOther end conditions: clamped (given slopes at the ends) or not-a-knot (used by SciPy's default)."),
        dict(type='bullets', id='algo', title='Natural cubic spline, step by step', kick='The method, step by step', ordered=True, rw=820,
             items=['Sort the points; compute the spacings $h_i = x_{i+1} - x_i$', 'Write one $M$-equation for each inner point $i = 1, \\dots, n-1$; set $M_0 = M_n = 0$', 'Solve the tridiagonal system for $M_1, \\dots, M_{n-1}$ (Thomas)',
                    'To evaluate at $x$: find the interval $[x_i, x_{i+1}]$ containing it', 'Use $S(x) = \\dfrac{M_i(x_{i+1}-x)^3 + M_{i+1}(x - x_i)^3}{6h_i} + \\Big(y_i - \\dfrac{M_ih_i^2}{6}\\Big)\\dfrac{x_{i+1}-x}{h_i} + \\Big(y_{i+1} - \\dfrac{M_{i+1}h_i^2}{6}\\Big)\\dfrac{x - x_i}{h_i}$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 25px/1.5 var(--mono);color:#f5f3ee">input x[0..n], y[0..n], X\nh[i] ← x[i+1] − x[i]\nfor i = 1 … n−1:          # tridiagonal rows\n    a[i] ← h[i−1];  c[i] ← h[i]\n    b[i] ← 2(h[i−1] + h[i])\n    d[i] ← 6((y[i+1]−y[i])/h[i]\n             − (y[i]−y[i−1])/h[i−1])\nM ← thomas(a, b, c, d);  M[0] ← M[n] ← 0\ni ← interval containing X\nreturn S_i(X)             # formula in step 5</pre></div><p class="small" style="margin-top:14px">Setup $O(n)$ once; each evaluation is one interval search and one cubic.</p>'),
             notes="Equal spacing h simplifies the equation to M_{i−1} + 4M_i + M_{i+1} = (6/h²)(y_{i+1} − 2y_i + y_{i−1}) = 6Δ²y_{i−1}/h²: the second differences of Lecture 15 appear on the right."),
        dict(type='worked', id='p1', title='Problem 1: a natural cubic spline by hand',
             q='Fit a natural cubic spline to $(1, 1)$, $(2, 2)$, $(3, 5)$, $(4, 11)$ and find $y(1.5)$ and $y(2.5)$.',
             steps=['$h = 1$, $M_0 = M_3 = 0$. Point 1: $M_0 + 4M_1 + M_2 = 6(1 - 2\\cdot2 + 5) = 12$; point 2: $M_1 + 4M_2 + M_3 = 6(2 - 2\\cdot5 + 11) = 18$',
                    'Solve $4M_1 + M_2 = 12$, $M_1 + 4M_2 = 18$: $\\;M_1 = 2$, $M_2 = 4$',
                    'On $[1, 2]$: $S = \\dfrac{2(x-1)^3}{6} + \\Big(1 - 0\\Big)(2 - x) + \\Big(2 - \\dfrac{2}{6}\\Big)(x - 1) = 1 + \\tfrac23(x-1) + \\tfrac13(x-1)^3$',
                    '$S(1.5) = 1 + \\tfrac13 + \\tfrac{1}{24} = 1.375$; on $[2, 3]$ the same recipe gives $S(2.5) = 3.125$'],
             answer='$M = (0, 2, 4, 0)$; $\\;y(1.5) \\approx 1.375$, $\\;y(2.5) \\approx 3.125$.',
             right=dict(w='interp', o=dict(method='spline', methods=['spline', 'lagrange'], x='1 2 3 4', y='1 2 5 11', at=1.5, height='240px', nof=True, side=True, tableHeight='240px')), rw=860,
             notes="Check S'(1) = 2/3 from the formula; for comparison the cubic through all four points (switch the widget to Lagrange) gives 1.3125 at x = 1.5.\n\nOn [2, 3]: S = 4(x−2)³/6 + 2(3−x)³/6 + (2 − 2/6)(3 − x) + (5 − 4/6)(x − 2); at 2.5: 0.0833 + 0.0417 + 0.8333 + 2.1667 = 3.125."),
        dict(type='compare', id='classic', title='Same data, two approaches: 11 points of Runge\'s function', kick='Classical vs numerical', mid='vs',
             left=dict(h='One polynomial (degree 10)', tag='Single formula', cls='blue', items=['Passes through all 11 points', 'Largest error <b>1.92</b>, near the ends', 'At $x = 0.9$: 1.58 instead of 0.047']),
             right=dict(h='Natural cubic spline', tag='Piecewise', cls='key', items=['Passes through all 11 points', 'Largest error <b>0.022</b>', 'Setup: one 9×9 tridiagonal solve']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When one polynomial cannot work</span><h3>1001 points</h3><p>A single polynomial of degree 1000 through equally spaced points is useless: astronomically large swings, and coefficients that cannot even be represented. The spline needs one tridiagonal solve ($\\approx 8000$ operations) and its largest error on Runge\'s function is $4\\times10^{-8}$.</p></div>'),
             notes="This is the decisive argument for splines: their error keeps falling as points are added (like h⁴ for smooth f), whereas a single equally spaced polynomial gets worse."),
        dict(type='code', id='code', title='A natural cubic spline in Python and C', code='cubicspline', lw=560,
             items=['Builds the tridiagonal system for $M_1, \\dots, M_{n-1}$', 'Thomas algorithm from Lecture 13', 'Evaluates $S$ with the step-5 formula', 'Prints $M$ and $S(1.5)$, $S(2.5)$ for Problem 1'],
             notes="Run both tabs. In SciPy: scipy.interpolate.CubicSpline(x, y, bc_type='natural')."),
        dict(type='widget', id='fail', title='Limitations shown failing', kick='When splines are not enough', w='runge', o=dict(f='step', n=11, equi=False, lin=True, cub=True, height='330px'), lw=520,
             items=['<b>Jumps</b>: at a step the cubic spline overshoots (about 11% here) and wiggles; the linear spline does not', '<b>End conditions</b>: "natural" ($M = 0$) is wrong if the true curve bends at the ends; errors are largest there',
                    '<b>Noise</b>: a spline still passes through every noisy point (use smoothing splines or least squares)', '<b>Extrapolation</b>: outside the data the end cubic is a guess'],
             frag=True,
             notes="With 11 points of the step function the natural cubic spline reaches about 1.11 and −0.11. Practical fixes: monotone (PCHIP) interpolation, or a linear spline near jumps.\n\nFor the end condition: in the practice problem below the true function x³ + 1 has f'' = 6x ≠ 0 at the ends, and the natural spline is off by 0.22 at x = 1.5."),
        dict(type='exam', id='practice', src='Problem 2',
             q='"Fit a natural cubic spline to the points $(0, 1)$, $(1, 2)$, $(2, 9)$, $(3, 28)$ and estimate $y(1.5)$."',
             tips=['State the conditions: $S$ cubic on each interval, $S, S\', S\'\'$ continuous, $M_0 = M_3 = 0$', '$M$-equations with $h = 1$: $4M_1 + M_2 = 6(1 - 4 + 9) = 36$, $\\;M_1 + 4M_2 = 6(2 - 18 + 28) = 72$',
                   'Solve: $M_1 = 4.8$, $M_2 = 16.8$', 'On $[1, 2]$ at $1.5$: $\\tfrac{4.8(0.125) + 16.8(0.125)}{6} + (2 - 0.8)(0.5) + (9 - 2.8)(0.5) = 4.15$; mention that the data are $x^3 + 1$ (true 4.375) and that the natural end condition causes the difference'],
             notes=""),
        dict(type='profile', id='profile', title='Cubic splines: method profile',
             best=['Many points, smooth underlying curve: error $\\sim h^4$, no Runge swings', 'Any spacing; setup $O(n)$ with the Thomas algorithm', 'Smooth slope and curvature: good for motion and shapes'],
             worst=['Jumps and sharp corners: overshoot', 'Noisy data: reproduces the noise exactly', 'Wrong end conditions: largest errors at the ends'],
             suited=['Fonts, CAD, animation paths, robot trajectories', 'Resampling signals and filling gaps in data', 'Smooth look-up tables (physical properties, calibration curves)'],
             avoid=['Data with errors (use least squares or smoothing splines, Lecture 23)', 'Monotone data that must stay monotone (use PCHIP)', 'Extrapolation'],
             verdict='Rule of thumb: <b>few points → one polynomial (or Chebyshev); many points → cubic spline; noisy points → least squares</b>.',
             notes="PCHIP: a piecewise cubic Hermite interpolant that keeps monotone data monotone (scipy.interpolate.PchipInterpolator)."),
        dict(type='table', id='compare', title='Comparative analysis: interpolating 11 points of Runge\'s function', cls='tb sm',
             head=['Method', 'Largest error ($n = 11$)', 'Largest error ($n = 21$)', 'Smoothness', 'Setup cost', 'Choose points?'], tx=(0, 3, 5), frag=True,
             rows=[['Polynomial, equal spacing', '1.92', '59.8', '$C^\\infty$ but wild', '$O(n^2)$', 'no'], ['Polynomial, Chebyshev points', '0.109', '0.015', '$C^\\infty$', '$O(n^2)$', 'yes (needed)'],
                   ['Linear spline', '0.067', '0.042', 'corners ($C^0$)', 'none', 'no'], ['Natural cubic spline', '0.022', '0.0032', '$C^2$', '$O(n)$ tridiagonal', 'no']],
             note='Errors measured on 4001 points in $[-1, 1]$ (lab tool). Only the spline gets better steadily with equally spaced data.', notefrag=True,
             notes="The linear-spline error does not fall monotonically at these small n because the peak of the bell sits between or on a data point depending on n; for larger n it falls like h²."),
        dict(type='bridge', id='bridge', title='End of Module 4: what comes next', kick='Roadmap', lead='We can now fill in values between data points in every common situation. Next we compute with them:',
             keep=['Difference tables and operators', 'Newton, Lagrange, divided differences', 'Runge phenomenon and Chebyshev points', 'Cubic splines from a tridiagonal solve'],
             rows=[['Slopes from tabulated data', 'Differentiate the interpolant', 19],
                   ['Areas from tabulated data', 'Integrate the interpolant (trapezoidal, Simpson)', 20],
                   ['Noisy data: do not pass through every point', 'Least squares and regression', 23],
                   ['Choosing smooth, non-wiggly models in ML', 'Overfitting and regularisation', 24]],
             notes="The last two rows connect Runge's phenomenon with overfitting: a model with as many parameters as data points fits the data exactly and generalises badly."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see splines at work.',
             items=[
                 dict(ic='🔤', h='Fonts and vector graphics', t='Every letter on this slide is a spline',
                      detail=dict(where='typography and vector graphics (TrueType, PostScript, SVG, PDF). Each glyph outline is a chain of polynomial pieces (quadratic or cubic Bézier curves) joined smoothly, so it can be scaled to any size without pixels.',
                                  steps=['A designer places a few control points', 'Each segment is a cubic; neighbouring segments share endpoints and tangent directions', 'At render time the curves are evaluated at the screen resolution', 'Same idea in CAD (car bodies, ship hulls) where splines were invented'],
                                  note='"Spline" was originally a thin wooden strip that shipbuilders bent through fixed points to draw smooth hull lines.')),
                 dict(ic='🤖', h='Robot and camera paths', t='Smooth motion through waypoints',
                      detail=dict(where='robotics, drones and animation. Waypoints are given; a cubic spline through them gives positions whose velocity and acceleration ($S\'$, $S\'\'$) are continuous, so motors and cameras move without jerks.',
                                  w='interp', o=dict(method='spline', methods=['spline', 'linear', 'lagrange'], x='0 1 2 3 4 5 6', y='0 1.5 1 2.5 2 3.5 3', at=2.5, height='200px', nof=True),
                                  note='Switch to "linear" to see the corners a robot would have to stop at; switch to Lagrange to see the swings of one polynomial.')),
                 dict(ic='🎵', h='Audio and speech resampling', t='Changing the sample rate',
                      detail=dict(where='speech and audio processing. Converting a recording from 44.1 kHz to 16 kHz (common for speech models) needs sample values at new, in-between times. Simple converters use cubic interpolation between neighbouring samples; high-quality ones use band-limited (sinc) interpolation.',
                                  steps=['Old samples are equally spaced in time', 'Each new sample time falls between two old ones', 'A local cubic through 4 neighbours estimates the value', 'A low-pass filter first prevents aliasing when the rate is reduced'],
                                  note='The same interpolation is used for pitch shifting and time-stretching in speech enhancement and data augmentation.')),
                 dict(ic='📊', h='Spline features in machine learning', t='Generalised additive models (GAMs)',
                      detail=dict(where='interpretable machine learning and statistics. A GAM models $y = \\beta_0 + s_1(x_1) + s_2(x_2) + \\cdots$, where each $s_j$ is a spline; the coefficients are fitted by penalised least squares.',
                                  steps=['Choose knots along each feature', 'Each spline is a sum of basis functions (B-splines)', 'Fit the weights by least squares with a smoothness penalty (Lecture 23)', 'Plot each $s_j$: the effect of every feature is visible'],
                                  note='Used in medicine and credit scoring where models must be explainable; pyGAM and R\'s mgcv implement it.'))],
             notes="The robot card has a live widget comparing spline, linear and single-polynomial paths through the same waypoints."),
        dict(type='check', id='check', q='For a natural cubic spline through equally spaced points ($h = 1$), what is the equation for $M_1$ when $y_0, y_1, y_2 = 0, 1, 4$?',
             opts=['$M_0 + 4M_1 + M_2 = 12$', '$M_0 + 4M_1 + M_2 = 6$', '$4M_1 = 4$', '$M_0 + 2M_1 + M_2 = 12$'], right=0,
             answer='A. $h_0M_0 + 2(h_0 + h_1)M_1 + h_1M_2 = 6\\big((4 - 1) - (1 - 0)\\big) = 12$, i.e. $M_0 + 4M_1 + M_2 = 12$.',
             notes="Option B forgets the factor 6; option D uses 2 instead of 2(h₀ + h₁) = 4 on the diagonal."),
        dict(type='summary', id='summary', items=[
            'Runge: one polynomial through many equally spaced points swings wildly near the ends',
            'Chebyshev points tame it, if the points can be chosen',
            'Splines: low-degree pieces joined smoothly; natural cubic spline from a tridiagonal system in $M_i$',
            'Cubic spline error falls like $h^4$; watch jumps, noise and end conditions'],
            hw=['Find the natural cubic spline through $(0, 0)$, $(1, 1)$, $(2, 8)$ and evaluate it at 0.5 and 1.5. Compare with $x^3$.', 'Use the lab tool: for which $n$ does the equally spaced polynomial error on Runge\'s function first exceed 1?',
                'Explain in words why Chebyshev points reduce the Runge phenomenon.', 'Show that the linear spline error is at most $\\tfrac{h^2}{8}\\max|f\'\'|$ on one interval.'],
            solved='With 11 equally spaced points the single polynomial has error <b>1.92</b>; the natural cubic spline has <b>0.022</b>, and with 21 points 0.003, while the polynomial grows to 60.',
            next='<b>Module 5: numerical differentiation.</b> Slopes from tabulated data, by differentiating the interpolation formulas.',
            notes="Homework answers: Q1: 4M1 = 6(0 − 2 + 8) = 36, M1 = 9; S(0.5) = −0.0625 (true 0.125), S(1.5) = 3.9375 (true 3.375): three points are too few for x³. Q2: n = 9 (error 1.05). For n = 6, 7, 8 the errors are 0.43, 0.62, 0.25: odd n put a point exactly on the peak at x = 0, which changes the pattern; the trend is still upwards. Q3: Chebyshev points cluster near the ends where ω(x) is large for equal spacing, making |ω| small and uniform. Q4: max |(x − x_i)(x − x_{i+1})| = h²/4 at the midpoint, divided by 2!."),
    ],
    code={
        'cubicspline': dict(file='natural_cubic_spline', py='''# Natural cubic spline: solve for M_i = S''(x_i), then evaluate
x = [1.0, 2.0, 3.0, 4.0]
y = [1.0, 2.0, 5.0, 11.0]
n = len(x) - 1
h = [x[i + 1] - x[i] for i in range(n)]

m = n - 1                                     # unknowns M_1 .. M_{n-1}
a = [h[i - 1] for i in range(1, n)]
b = [2 * (h[i - 1] + h[i]) for i in range(1, n)]
c = [h[i] for i in range(1, n)]
d = [6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1]) for i in range(1, n)]
for i in range(1, m):                         # Thomas: down sweep
    w = a[i] / b[i - 1]
    b[i] -= w * c[i - 1]
    d[i] -= w * d[i - 1]
M = [0.0] * (n + 1)                           # natural ends: M_0 = M_n = 0
M[m] = d[m - 1] / b[m - 1]
for i in range(m - 2, -1, -1):                # up sweep
    M[i + 1] = (d[i] - c[i] * M[i + 2]) / b[i]
print("M =", " ".join(f"{v:.4f}" for v in M))

def S(X):
    i = 0
    while i < n - 1 and X > x[i + 1]:
        i += 1
    A, B, hh = x[i + 1] - X, X - x[i], h[i]
    return (M[i] * A**3 + M[i + 1] * B**3) / (6 * hh) \\
        + (y[i] - M[i] * hh * hh / 6) * A / hh + (y[i + 1] - M[i + 1] * hh * hh / 6) * B / hh

for X in [1.5, 2.5, 3.5]:
    print(f"S({X}) = {S(X):.6f}")
''', c='''/* Natural cubic spline: solve for M_i = S''(x_i), then evaluate */
#include <stdio.h>
#define NP 4                                  /* number of points */

double x[NP] = {1, 2, 3, 4}, y[NP] = {1, 2, 5, 11}, h[NP], M[NP];

double S(double X) {
    int i = 0;
    while (i < NP - 2 && X > x[i + 1]) i++;
    double A = x[i + 1] - X, B = X - x[i], hh = h[i];
    return (M[i] * A * A * A + M[i + 1] * B * B * B) / (6 * hh)
         + (y[i] - M[i] * hh * hh / 6) * A / hh + (y[i + 1] - M[i + 1] * hh * hh / 6) * B / hh;
}

int main(void) {
    int n = NP - 1, m = n - 1;
    double a[NP], b[NP], c[NP], d[NP];
    for (int i = 0; i < n; i++) h[i] = x[i + 1] - x[i];
    for (int i = 1; i < n; i++) {             /* row i-1 of the tridiagonal system */
        a[i - 1] = h[i - 1]; b[i - 1] = 2 * (h[i - 1] + h[i]); c[i - 1] = h[i];
        d[i - 1] = 6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1]);
    }
    for (int i = 1; i < m; i++) {             /* Thomas: down sweep */
        double w = a[i] / b[i - 1];
        b[i] -= w * c[i - 1];
        d[i] -= w * d[i - 1];
    }
    for (int i = 0; i <= n; i++) M[i] = 0;    /* natural ends */
    M[m] = d[m - 1] / b[m - 1];
    for (int i = m - 2; i >= 0; i--) M[i + 1] = (d[i] - c[i] * M[i + 2]) / b[i];
    printf("M =");
    for (int i = 0; i <= n; i++) printf(" %.4f", M[i]);
    printf("\\n");
    double X[3] = {1.5, 2.5, 3.5};
    for (int k = 0; k < 3; k++) printf("S(%g) = %.6f\\n", X[k], S(X[k]));
    return 0;
}
'''),
        'runge': dict(file='runge_phenomenon', py='''# Runge phenomenon: one polynomial vs a linear spline on f(x) = 1/(1 + 25x^2)
def f(x):
    return 1.0 / (1.0 + 25.0 * x * x)

def lagrange(xs, ys, X):
    total = 0.0
    for i in range(len(xs)):
        L = 1.0
        for j in range(len(xs)):
            if j != i:
                L *= (X - xs[j]) / (xs[i] - xs[j])
        total += ys[i] * L
    return total

def linear(xs, ys, X):
    i = 0
    while i < len(xs) - 2 and X > xs[i + 1]:
        i += 1
    return ys[i] + (ys[i + 1] - ys[i]) * (X - xs[i]) / (xs[i + 1] - xs[i])

for n in [5, 9, 11, 15, 21]:
    xs = [-1.0 + 2.0 * i / (n - 1) for i in range(n)]
    ys = [f(v) for v in xs]
    ep = el = 0.0
    for k in range(401):
        X = -1.0 + 2.0 * k / 400
        ep = max(ep, abs(lagrange(xs, ys, X) - f(X)))
        el = max(el, abs(linear(xs, ys, X) - f(X)))
    print(f"n = {n:2d}: polynomial error {ep:10.4f}   linear spline error {el:.4f}")
''', c='''/* Runge phenomenon: one polynomial vs a linear spline on f(x) = 1/(1 + 25x^2) */
#include <stdio.h>
#include <math.h>

double f(double x) { return 1.0 / (1.0 + 25.0 * x * x); }

double lagrange(int n, double xs[], double ys[], double X) {
    double total = 0;
    for (int i = 0; i < n; i++) {
        double L = 1;
        for (int j = 0; j < n; j++) if (j != i) L *= (X - xs[j]) / (xs[i] - xs[j]);
        total += ys[i] * L;
    }
    return total;
}

double linear(int n, double xs[], double ys[], double X) {
    int i = 0;
    while (i < n - 2 && X > xs[i + 1]) i++;
    return ys[i] + (ys[i + 1] - ys[i]) * (X - xs[i]) / (xs[i + 1] - xs[i]);
}

int main(void) {
    int ns[5] = {5, 9, 11, 15, 21};
    double xs[21], ys[21];
    for (int r = 0; r < 5; r++) {
        int n = ns[r];
        for (int i = 0; i < n; i++) { xs[i] = -1.0 + 2.0 * i / (n - 1); ys[i] = f(xs[i]); }
        double ep = 0, el = 0;
        for (int k = 0; k <= 400; k++) {
            double X = -1.0 + 2.0 * k / 400;
            double e1 = fabs(lagrange(n, xs, ys, X) - f(X)), e2 = fabs(linear(n, xs, ys, X) - f(X));
            if (e1 > ep) ep = e1;
            if (e2 > el) el = e2;
        }
        printf("n = %2d: polynomial error %10.4f   linear spline error %.4f\\n", n, ep, el);
    }
    return 0;
}
'''),
    },
    lab=dict(title='Spline and Runge Lab',
             intro='See the Runge phenomenon, tame it with Chebyshev points and splines, and build natural cubic splines for your own data.',
             tabs=[
                 dict(name='Runge explorer', blocks=[
                     dict(p='Change the number of points and the methods. The table gives the largest error on [−1, 1].'),
                     dict(w='runge', o=dict(n=11, cheb=True, lin=True, cub=True, height='340px'))]),
                 dict(name='Spline solver', blocks=[
                     dict(p='Type your points (any spacing). The table lists Mᵢ = S″(xᵢ) of the natural cubic spline; switch to Lagrange to compare with one polynomial.'),
                     dict(w='interp', o=dict(method='spline', methods=['spline', 'lagrange', 'linear'], x='1 2 3 4', y='1 2 5 11', at=1.5, height='300px', side=True, tableHeight='300px',
                                             presets=[['Problem 1', '1 2 3 4', '1 2 5 11', 1.5, 'spline'], ['Problem 2', '0 1 2 3', '1 2 9 28', 1.5, 'spline', 'x^3+1'], ['homework 1', '0 1 2', '0 1 8', 0.5, 'spline', 'x^3'], ['waypoints', '0 1 2 3 4 5 6', '0 1.5 1 2.5 2 3.5 3', 2.5, 'spline']]))]),
                 dict(name='Code', blocks=[
                     dict(h='Natural cubic spline'), dict(code='cubicspline', tasks=['Run it. Compare M with Problem 1.', 'Change the data to Problem 2 (x = 0, 1, 2, 3; y = 1, 2, 9, 28).', 'Evaluate at 3.5. Is that interpolation or extrapolation?']),
                     dict(h='Runge phenomenon'), dict(code='runge', tasks=['Run it. How does the polynomial error grow with n?', 'Replace the equally spaced points by Chebyshev points cos((2i+1)π/(2n)). What happens?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('What is the Runge phenomenon?', 'Interpolating a smooth function by one polynomial through many equally spaced points can give large oscillations near the ends of the interval, and the error grows as more points are added (e.g. $1/(1+25x^2)$: error 1.92 with 11 points, 60 with 21).'),
                         ('State the conditions that define a natural cubic spline.', 'On each interval $S$ is a cubic; $S(x_i) = y_i$; $S$, $S\'$ and $S\'\'$ are continuous at the inner points; and $S\'\'(x_0) = S\'\'(x_n) = 0$.'),
                         ('Fit a natural cubic spline to $(1,1), (2,2), (3,5), (4,11)$; find $y(1.5)$.', '$4M_1 + M_2 = 12$, $M_1 + 4M_2 = 18$, so $M_1 = 2$, $M_2 = 4$; on $[1, 2]$: $S = 1 + \\tfrac23(x-1) + \\tfrac13(x-1)^3$, $S(1.5) = 1.375$.'),
                         ('Why are splines preferred to a single high-degree polynomial for long data sets?', 'Each piece is low degree and depends mainly on nearby data, so there are no wild end oscillations; the error falls steadily (like $h^4$) as points are added; and the setup is a tridiagonal system, $O(n)$ work.'),
                         ('Give two situations where a cubic spline is a poor choice.', 'Data with jumps or sharp corners (overshoot); noisy measurements (the spline passes through the noise; use least squares); also extrapolation beyond the data.')])])]),
)
