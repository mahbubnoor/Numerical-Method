LECTURE = dict(
    title="Newton's Forward and Backward Interpolation",
    short="Newton's Forward and Backward Interpolation",
    sub='Estimating values between the entries of an equally spaced table: Newton\'s forward formula from $E^p = (1+\\Delta)^p$, the backward formula from $(1-\\nabla)^{-p}$, how to choose between them, how big the error is, and when interpolation goes wrong.',
    slides=[
        dict(type='cover', id='cover', notes="Recap question: 'Last lecture, how did we get y(2.5) from the table?' (E^{2.5} = (1 + Δ)^{2.5}.) Today: that idea becomes a formula, with its error, its limits and a backward twin."),
        dict(type='bullets', id='hook', title='The problem: the census is every ten years', kick='Why this lecture', rw=640,
             lead='A town\'s population (thousands) was counted every ten years. A planner needs the values for 1895 and 1925, when no count was taken.',
             items=['The data are <b>equally spaced</b> ($h = 10$ years) but there is no formula', '1895 is near the <b>start</b> of the table; 1925 is near the <b>end</b>',
                    'Straight-line interpolation ignores the curvature that the differences show', 'We need a formula that uses the whole table, and an idea of its error'],
             frag=True,
             right=dict(table=[['year $x$', 'population $y$'], [['1891', '46'], ['1901', '66'], ['1911', '81'], ['1921', '93'], ['1931', '101']]]),
             notes="Classic textbook data. Solved during the lecture: 1895 → 54.8528 thousand (forward), 1925 → 96.8368 thousand (backward). Linear interpolation would give 54.0 and 96.2."),
        dict(type='goals', id='goals', items=[
            'Derive <b>Newton\'s forward formula</b> from $E^p = (1+\\Delta)^p$ and the <b>backward formula</b> from $(1-\\nabla)^{-p}$',
            'Compute $p$ and evaluate the formulas from a difference table',
            'Choose forward or backward according to where $x$ lies',
            'Estimate the <b>interpolation error</b> and recognise the danger of extrapolation',
            'Compare Newton\'s formulas with linear interpolation and with Lagrange'],
            prev='Difference tables, operators, $E = 1 + \\Delta = e^{hD}$.',
            today='Expand $E^p$ to get values between the table entries.',
            notes="Students have used linear interpolation in school (e.g. log tables). Today's formulas are its higher-degree generalisation."),
        dict(type='math', id='derive', title="Deriving Newton's forward formula",
             eqs=[dict(cap='Write x in steps from x₀', eq='x = x_0 + ph \\;\\Longrightarrow\\; p = \\frac{x - x_0}{h}, \\qquad y(x) = E^{p}y_0 = (1 + \\Delta)^{p}y_0'),
                  dict(cap='Binomial series (any real p)', eq='\\begin{aligned} y(x_0 + ph) = {} & y_0 + p\\,\\Delta y_0 + \\frac{p(p-1)}{2!}\\Delta^2 y_0 \\\\ & + \\frac{p(p-1)(p-2)}{3!}\\Delta^3 y_0 + \\cdots \\end{aligned}', frag=True)],
             items=['Uses the <b>top diagonal</b> $y_0, \\Delta y_0, \\Delta^2 y_0, \\dots$', 'For integer $p$ it reproduces the table exactly', 'With $n + 1$ points: stops after $\\Delta^n$; it is the degree-$n$ polynomial through all of them', 'Best when $x$ is near the <b>start</b> ($0 < p < 1$)'],
             ifrag=True, rw=620,
             notes="Derivation without operators (for students who prefer it): assume P(x) = a0 + a1(x − x0) + a2(x − x0)(x − x1) + …, substitute x0, x1, … in turn, and find a_k = Δ^k y0/(k! h^k). Both routes give the same formula."),
        dict(type='bullets', id='algo', title="Newton's forward interpolation, step by step", kick='The method, step by step', ordered=True, rw=780,
             items=['Check the $x$ values are equally spaced; note $h$', 'Build the forward difference table', 'Take $x_0$ as the table entry just below $x$ (near the start); compute $p = (x - x_0)/h$',
                    'Add terms $\\dfrac{p(p-1)\\cdots(p-k+1)}{k!}\\,\\Delta^k y_0$ for $k = 0, 1, 2, \\dots$', 'Stop when the terms become negligible (or the table ends); the last term used estimates the error'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 26px/1.55 var(--mono);color:#f5f3ee">input x[0..n], y[0..n] (equal steps), X\nh ← x[1] − x[0];  p ← (X − x[0]) / h\nd ← copy of y          # top diagonal\nsum ← d[0];  c ← 1\nfor k = 1 … n:\n    for i = 0 … n−k:\n        d[i] ← d[i+1] − d[i]\n    c ← c·(p − k + 1) / k\n    sum ← sum + c·d[0]\nreturn sum</pre></div><p class="small" style="margin-top:14px">Each pass makes the next column of differences in place; only $d_0$ is used.</p>'),
             notes="Step 3: x0 does not have to be the first entry of the table. Choosing the entry just below x keeps p between 0 and 1, where the formula is most accurate."),
        dict(type='worked', id='p1', title='Problem 1: the population in 1895 (forward)',
             q='Use the census table to estimate the population in 1895.',
             steps=['Differences: $\\Delta y_0 = 20$, $\\Delta^2 y_0 = -5$, $\\Delta^3 y_0 = 2$, $\\Delta^4 y_0 = -3$ (top diagonal); $p = (1895 - 1891)/10 = 0.4$',
                    '$y = 46 + 0.4(20) + \\dfrac{0.4(-0.6)}{2}(-5) + \\dfrac{0.4(-0.6)(-1.6)}{6}(2) + \\dfrac{0.4(-0.6)(-1.6)(-2.6)}{24}(-3)$',
                    '$= 46 + 8 + 0.6 + 0.128 + 0.1248$'],
             answer='$y(1895) \\approx 54.85$ thousand. The terms shrink fast (8, 0.6, 0.13, 0.12), so the estimate is reliable to about 0.1.',
             right=dict(w='interp', o=dict(method='forward', methods=['forward'], at=1895, height='240px', nof=True, fixed=True, side=True, tableHeight='240px')), rw=860,
             notes="Full difference table: Δ: 20, 15, 12, 8; Δ²: −5, −3, −4; Δ³: 2, −1; Δ⁴: −3.\n\nLinear interpolation (first two terms only) gives 54.0: the curvature adds 0.85 thousand people."),
        dict(type='math', id='back', title="Newton's backward formula",
             eqs=[dict(cap='Measure from the last entry', eq='x = x_n + ph \\;(p < 0), \\qquad y(x) = E^{p}y_n = (1 - \\nabla)^{-p}y_n'),
                  dict(cap='Binomial series again', eq='\\begin{aligned} y(x_n + ph) = {} & y_n + p\\,\\nabla y_n + \\frac{p(p+1)}{2!}\\nabla^2 y_n \\\\ & + \\frac{p(p+1)(p+2)}{3!}\\nabla^3 y_n + \\cdots \\end{aligned}', frag=True)],
             items=['$E = (1 - \\nabla)^{-1}$ from $\\nabla = 1 - E^{-1}$ (Lecture 15)', 'Uses the <b>bottom diagonal</b> $y_n, \\nabla y_n, \\nabla^2 y_n, \\dots$', 'Best when $x$ is near the <b>end</b> ($-1 < p < 0$)', 'Same numbers as the forward table: $\\nabla y_i = \\Delta y_{i-1}$'],
             ifrag=True, rw=620,
             notes="Students can use one difference table for both formulas: the forward formula reads the top edge, the backward formula the bottom edge.\n\nAlgorithm: identical to the forward one with p = (x − x_n)/h, coefficients p(p+1)…(p+k−1)/k! and the bottom diagonal."),
        dict(type='worked', id='p2', title='Problem 2: the population in 1925 (backward)',
             q='Estimate the population in 1925.',
             steps=['Bottom diagonal: $\\nabla y_n = 8$, $\\nabla^2 y_n = -4$, $\\nabla^3 y_n = -1$, $\\nabla^4 y_n = -3$; $\\;p = (1925 - 1931)/10 = -0.6$',
                    '$y = 101 + (-0.6)(8) + \\dfrac{(-0.6)(0.4)}{2}(-4) + \\dfrac{(-0.6)(0.4)(1.4)}{6}(-1) + \\dfrac{(-0.6)(0.4)(1.4)(2.4)}{24}(-3)$',
                    '$= 101 - 4.8 + 0.48 + 0.056 + 0.1008$'],
             answer='$y(1925) \\approx 96.84$ thousand.',
             right=dict(w='interp', o=dict(method='backward', methods=['backward', 'forward'], at=1925, height='240px', nof=True, side=True, tableHeight='240px')), rw=860,
             notes="Switch the widget to the forward formula for 1925: with all five points both formulas give the same polynomial and the same value 96.8368. The choice matters when the table is long and only a few terms are used, or when rounding the differences."),
        dict(type='math', id='error', title='How accurate? The interpolation error',
             eqs=[dict(cap='Remainder after the term in Δⁿ (forward form); ξ lies in the data range', eq='y(x) - P_n(x) = \\frac{p(p-1)\\cdots(p-n)}{(n+1)!}\\,h^{n+1}f^{(n+1)}(\\xi)'),
                  dict(cap='Practical estimate: the first neglected term', eq='\\text{error} \\approx \\frac{p(p-1)\\cdots(p-n)}{(n+1)!}\\,\\Delta^{n+1}y_0', frag=True)],
             items=['Small when $p$ is small: $x$ close to $x_0$', 'The product $p(p-1)\\cdots(p-n)$ grows quickly <b>outside</b> the table: extrapolation is risky', 'Smooth data (small high differences) interpolate well', 'Same structure as the Taylor remainder (Lecture 3)'],
             ifrag=True, rw=620,
             notes="For 1895 with 4 terms (cubic), the first neglected term is the Δ⁴ term, 0.1248: the cubic estimate 54.728 is off by about 0.12, consistent with the true difference to the quartic value 54.853."),
        dict(type='widget', id='explore', title='Explore: forward, backward and the danger zone', w='interp',
             o=dict(method='forward', methods=['forward', 'backward', 'linear'], at=1895, height='330px', side=True, tableHeight='330px',
                    presets=[['census 1895', '1891 1901 1911 1921 1931', '46 66 81 93 101', 1895, 'forward'], ['census 1925', '1891 1901 1911 1921 1931', '46 66 81 93 101', 1925, 'backward'], ['extrapolate 1960', '1891 1901 1911 1921 1931', '46 66 81 93 101', 1960, 'backward'], ['sin x table', '0 0.2 0.4 0.6 0.8 1', '0 0.198669 0.389418 0.564642 0.717356 0.841471', 0.1, 'forward', 'sin(x)']]), lw=440,
             items=['Each table row is one term of the formula', 'Blue band: the data range', 'Try <b>1960</b>: the polynomial bends away; the estimate is meaningless', 'The <b>sin x</b> preset compares with the true function'],
             notes="Extrapolation to 1960 gives about 51.5 thousand: the quartic turns sharply down after 1931, though nothing in the data says the population fell. Interpolation is safe inside the table only.\n\nWith the sin x table, the error at 0.1 is about 10⁻⁶."),
        dict(type='compare', id='classic', title='Same question, two approaches: population in 1895', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (fit a formula)', tag='Algebra', cls='blue', items=['Assume $y = a + bx + cx^2 + dx^3 + ex^4$', 'Solve a 5×5 Vandermonde system with entries up to $1931^4 \\approx 1.4\\times10^{13}$', 'Badly conditioned: digits are lost before we start']),
             right=dict(h='Numerical (Newton forward)', tag='Algorithm', cls='key', items=['Difference table: subtractions only', '$p = 0.4$, five short terms', '$54.8528$ thousand, with a built-in error estimate']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>Data from experiments and records</h3><p>Population, rainfall or sensor logs have no formula to find. Even fitting one through the points with $x$ as large as 1931 makes a severely ill-conditioned system (Lecture 11). Newton\'s formula works in the shifted variable $p$, where all numbers are small.</p></div>'),
             notes="The Vandermonde matrix with x = 1891 … 1931 has a condition number beyond 10¹⁶ in double precision; with p = 0 … 4 instead it is about 10³. Shifting and scaling (p = (x − x0)/h) is what makes Newton's formula numerically sensible."),
        dict(type='code', id='code', title='Newton forward and backward in Python and C', code='newtonfb', lw=560,
             items=['Builds the difference table once', 'Forward: top diagonal, $p = (x - x_0)/h$', 'Backward: bottom diagonal, $p = (x - x_n)/h$', 'Prints every term, as in a written solution'],
             notes="Run both. Lab: change the year to 1960 and see the extrapolation problem."),
        dict(type='widget', id='fail', title='Limitations shown failing', kick='When interpolation goes wrong', w='interp',
             o=dict(method='forward', methods=['forward', 'linear'], x='-1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1', y='0.038462 0.058824 0.1 0.2 0.5 1 0.5 0.2 0.1 0.058824 0.038462', at=0.9, f='1/(1+25x^2)', height='300px', side=True, tableHeight='300px',
                    presets=[['11 equal points, x = 0.9', '-1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1', '0.038462 0.058824 0.1 0.2 0.5 1 0.5 0.2 0.1 0.058824 0.038462', 0.9, 'forward', '1/(1+25x^2)'], ['extrapolation', '1891 1901 1911 1921 1931', '46 66 81 93 101', 1960, 'forward'], ['unequal spacing', '0 1 2 5', '2 3 12 147', 3, 'forward']]), lw=540,
             items=['<b>High degree on equal spacing</b>: 11 points of $1/(1 + 25x^2)$; near the ends the degree-10 polynomial swings far from the data', '<b>Extrapolation</b>: outside the table the error term grows without control',
                    '<b>Unequal spacing</b>: the formulas do not apply at all', 'Noisy data: high differences are mostly noise, so extra terms add error'],
             frag=True,
             notes="At x = 0.9 the degree-10 polynomial gives about 1.58 against the true 0.047. This is the Runge phenomenon, the opening problem of Lecture 18. The 'unequal spacing' preset shows the error message: Lecture 17 fixes it."),
        dict(type='exam', id='practice', src='Problem 3',
             q='"From the table $x$: 1, 2, 3, 4, 5 and $y$: 1, 8, 27, 64, 125, find $y(1.5)$ by Newton\'s forward formula and $y(4.5)$ by Newton\'s backward formula."',
             tips=['Difference table: $\\Delta$: 7, 19, 37, 61; $\\Delta^2$: 12, 18, 24; $\\Delta^3$: 6, 6; $\\Delta^4$: 0', 'Forward, $p = 0.5$: $1 + 0.5(7) + \\tfrac{0.5(-0.5)}{2}(12) + \\tfrac{0.5(-0.5)(-1.5)}{6}(6) = 3.375$',
                   'Backward, $p = -0.5$: $125 - 0.5(61) + \\tfrac{(-0.5)(0.5)}{2}(24) + \\tfrac{(-0.5)(0.5)(1.5)}{6}(6) = 91.125$', 'Both exact ($1.5^3$, $4.5^3$), because $\\Delta^4 = 0$: say so as your check'],
             notes=""),
        dict(type='profile', id='profile', title="Newton's forward and backward formulas: method profile",
             best=['Smooth, equally spaced tables; $x$ close to the start (forward) or end (backward)', 'Low-degree data: exact once the differences vanish', 'Hand calculation: the difference table organises all the work'],
             worst=['Extrapolation far outside the table', 'Many equally spaced points with a high-degree polynomial (Runge, Lecture 18)', 'Noisy measurements: high differences amplify noise'],
             suited=['Tables of functions, physical properties (steam tables), census-type records', 'Deriving differentiation and integration formulas (Lectures 19–20)', 'Resampling equally spaced signals'],
             avoid=['Unequally spaced data (use Lagrange or divided differences, Lecture 17)', 'Long tables needing a smooth curve everywhere (use splines, Lecture 18)', 'Data with errors (use least squares, Lecture 23)'],
             verdict='Rule of thumb: <b>forward near the top, backward near the bottom, central formulas in the middle; never far outside the table</b>.',
             notes="Central-difference formulas (Gauss, Stirling, Bessel) exist for points in the middle of the table; they are mentioned in many syllabi but the same estimates follow from the forward or backward formula with a shifted x0."),
        dict(type='table', id='compare', title='Comparative analysis: interpolation methods', cls='tb sm',
             head=['Method', 'Spacing', 'Uses', 'Cost per $x$', 'Add a point', 'Best for'], tx=(0, 2, 5), frag=True,
             rows=[['Linear', 'any', 'two neighbours', '$O(1)$', 'trivial', 'quick look-ups, dense tables'], ['Newton forward', 'equal', 'top diagonal', '$O(n)$ after table', 'append a term', '$x$ near the start'],
                   ['Newton backward', 'equal', 'bottom diagonal', '$O(n)$ after table', 'append a term', '$x$ near the end'], ['Lagrange (L17)', 'any', 'all points', '$O(n^2)$', 'start again', 'theory, few points'],
                   ['Divided differences (L17)', 'any', 'divided-difference table', '$O(n)$ after table', 'append a term', 'unequal data'], ['Cubic spline (L18)', 'any', 'tridiagonal solve', '$O(\\log n)$ after setup', 'redo solve', 'many points, smooth curves']],
             note='All polynomial methods through the same $n + 1$ points give the <b>same polynomial</b>; they differ in convenience and rounding.', notefrag=True,
             notes="Stress the note: forward, backward, Lagrange and divided differences are four ways of writing one polynomial."),
        dict(type='bridge', id='bridge', lead='Newton\'s formulas are exact for polynomials and simple to use, but they need equal spacing and they misbehave at high degree.',
             keep=['Difference table organises the work', 'Forward/backward choice by position', 'Error estimate from the next term', 'Basis for differentiation and integration formulas'],
             rows=[['Needs equally spaced $x$', 'Lagrange and divided differences', 17],
                   ['High degree oscillates near the ends', 'Piecewise cubics: splines', 18],
                   ['We want slopes, not values', 'Differentiate the formula', 19],
                   ['We want areas under the data', 'Integrate the formula: trapezoidal, Simpson', 20]],
             notes="Lectures 19 and 20 differentiate and integrate exactly today's forward formula."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see table interpolation in use.',
             items=[
                 dict(ic='🌡️', h='Engineering property tables', t='Steam tables, material data sheets',
                      detail=dict(where='thermodynamics and materials engineering. Properties such as saturation pressure are published at equal temperature steps; values in between are interpolated.',
                                  table=[['$T$ (°C)', '100', '110', '120', '130'], [['$p$ (kPa)', '101.42', '143.38', '198.67', '270.28']]],
                                  w='interp', o=dict(x='100 110 120 130', y='101.42 143.38 198.67 270.28', at=105, method='forward', methods=['forward', 'linear'], height='200px', nof=True),
                                  note='At 105 °C the forward formula gives about 120.9 kPa; straight-line interpolation gives 122.4 kPa (too high, because the curve bends upward).')),
                 dict(ic='📟', h='Look-up tables in embedded systems', t='A microcontroller reading a thermistor',
                      detail=dict(where='firmware for sensors. Evaluating $\\ln$ or $e^x$ on a tiny chip is slow, so the curve is stored as a table at equal steps and the firmware interpolates between entries.',
                                  steps=['Measure the voltage, compute the table index $i = \\lfloor (V - V_0)/h \\rfloor$ and $p = (V - V_0)/h - i$', 'Use the first two or three terms of Newton\'s forward formula from entry $i$', 'Only a few multiplications: fast enough for every reading', 'Accuracy is set by the table spacing $h$ and the number of terms'],
                                  note='The same trick evaluates sine and cosine in older graphics hardware and in audio synthesisers (wavetables).')),
                 dict(ic='🔭', h='Astronomical tables', t='Planet positions at noon each day',
                      detail=dict(where='ephemerides (tables of planet and moon positions), published at equal time steps. Navigators interpolated them for the time of their observation, and Newton developed his formulas largely for this purpose.',
                                  steps=['Positions are tabulated once a day', 'A navigator\'s observation is at, say, 14:24, so $p = 0.6$ of a day', 'Second differences correct for the curvature of the orbit', 'Modern ephemerides store Chebyshev polynomial pieces, a refinement of the same idea'],
                                  note='Newton\'s interpolation work (1670s) came from exactly these tables.')),
                 dict(ic='🎞️', h='Frames, pixels and samples', t='Filling in between equally spaced samples',
                      detail=dict(where='image zoom, video frame-rate conversion and audio resampling. Pixels and samples are equally spaced; new ones are interpolated from their neighbours.',
                                  steps=['Linear (bilinear in 2-D): first two terms of Newton\'s formula', 'Quadratic or cubic: two or three more terms, sharper images', 'Cubic convolution (bicubic) in Photoshop and OpenCV is a local cubic interpolant', 'Speech and music resampling (e.g. 44.1 kHz → 16 kHz) uses interpolation filters built on the same principle'],
                                  note='Higher degree looks sharper but can create overshoot ("ringing") near edges, a cousin of the Runge effect.'))],
             notes="The steam-table pop-up has a live interpolation widget; switch it to linear to compare."),
        dict(type='check', id='check', q='Newton\'s forward formula with $x_0 = 2$, $h = 0.5$. What is $p$ for $x = 2.3$?',
             opts=['$0.6$', '$0.3$', '$1.15$', '$4.6$'], right=0,
             answer='A. $p = (x - x_0)/h = (2.3 - 2)/0.5 = 0.6$.',
             notes="Option B forgets to divide by h; option D divides x by h."),
        dict(type='summary', id='summary', items=[
            'Forward: $y = y_0 + p\\Delta y_0 + \\tfrac{p(p-1)}{2!}\\Delta^2 y_0 + \\cdots$, $p = (x - x_0)/h$',
            'Backward: $y = y_n + p\\nabla y_n + \\tfrac{p(p+1)}{2!}\\nabla^2 y_n + \\cdots$, $p = (x - x_n)/h$',
            'Forward near the start, backward near the end; the first neglected term estimates the error',
            'Only for equal spacing; extrapolation and high degree are dangerous'],
            hw=['From $x$: 0, 1, 2, 3, 4 and $y$: 1, 7, 23, 55, 109, find $y(0.5)$ and $y(3.5)$.', 'The values of $\\sin x$ at $x = 0.1, 0.2, 0.3, 0.4, 0.5$ are 0.09983, 0.19867, 0.29552, 0.38942, 0.47943. Find $\\sin 0.15$ and $\\sin 0.45$ and compare with a calculator.',
                'Derive Newton\'s backward formula from $E = (1 - \\nabla)^{-1}$.', 'Use the lab tool to extrapolate the census to 1941 and 1951. Comment.'],
            solved='Forward with $p = 0.4$: <b>54.85 thousand</b> in 1895. Backward with $p = -0.6$: <b>96.84 thousand</b> in 1925. Linear interpolation would have said 54.0 and 96.2.',
            next='<b>Lagrange and divided-difference interpolation.</b> The same polynomial when the data are <i>not</i> equally spaced.',
            notes="Homework answers: Q1: y = x³ + 2x² + 3x + 1 (Δ: 6, 16, 32, 54; Δ²: 10, 16, 22; Δ³: 6, 6); y(0.5) = 3.125, y(3.5) = 78.875. Q2: sin 0.15 ≈ 0.14944 (true 0.149438), sin 0.45 ≈ 0.43497 (true 0.434966). Q4: extrapolation gives 1941 ≈ 101.0, 1951 ≈ 86.0 (and 1960 ≈ 51.5) thousand: the curve dives, nonsense for a growing town, which is the point."),
    ],
    code={
        'newtonfb': dict(file='newton_interpolation', py='''# Newton forward and backward interpolation (equally spaced data)
x = [1891.0, 1901.0, 1911.0, 1921.0, 1931.0]
y = [46.0, 66.0, 81.0, 93.0, 101.0]
n = len(x)
h = x[1] - x[0]

table = [y]                                   # table[k][i] = Delta^k y_i
while len(table[-1]) > 1:
    prev = table[-1]
    table.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])

def forward(X):
    p = (X - x[0]) / h
    total, c = 0.0, 1.0
    for k in range(n):
        term = c * table[k][0]
        total += term
        print(f"  k={k}  coefficient={c:9.5f}  diff={table[k][0]:6.1f}  term={term:9.5f}")
        c = c * (p - k) / (k + 1)
    return total

def backward(X):
    p = (X - x[-1]) / h
    total, c = 0.0, 1.0
    for k in range(n):
        term = c * table[k][-1]
        total += term
        print(f"  k={k}  coefficient={c:9.5f}  diff={table[k][-1]:6.1f}  term={term:9.5f}")
        c = c * (p + k) / (k + 1)
    return total

print("forward, x = 1895")
print(f"y(1895) = {forward(1895.0):.4f}")
print("backward, x = 1925")
print(f"y(1925) = {backward(1925.0):.4f}")
''', c='''/* Newton forward and backward interpolation (equally spaced data) */
#include <stdio.h>
#define N 5

double x[N] = {1891, 1901, 1911, 1921, 1931};
double d[N][N];                               /* d[k][i] = Delta^k y_i */

double forward(double X, double h) {
    double p = (X - x[0]) / h, total = 0, c = 1;
    for (int k = 0; k < N; k++) {
        double term = c * d[k][0];
        total += term;
        printf("  k=%d  coefficient=%9.5f  diff=%6.1f  term=%9.5f\\n", k, c, d[k][0], term);
        c = c * (p - k) / (k + 1);
    }
    return total;
}

double backward(double X, double h) {
    double p = (X - x[N - 1]) / h, total = 0, c = 1;
    for (int k = 0; k < N; k++) {
        double term = c * d[k][N - 1 - k];
        total += term;
        printf("  k=%d  coefficient=%9.5f  diff=%6.1f  term=%9.5f\\n", k, c, d[k][N - 1 - k], term);
        c = c * (p + k) / (k + 1);
    }
    return total;
}

int main(void) {
    double y[N] = {46, 66, 81, 93, 101}, h = x[1] - x[0];
    for (int i = 0; i < N; i++) d[0][i] = y[i];
    for (int k = 1; k < N; k++)
        for (int i = 0; i < N - k; i++) d[k][i] = d[k - 1][i + 1] - d[k - 1][i];
    printf("forward, x = 1895\\n");
    printf("y(1895) = %.4f\\n", forward(1895, h));
    printf("backward, x = 1925\\n");
    printf("y(1925) = %.4f\\n", backward(1925, h));
    return 0;
}
'''),
    },
    lab=dict(title='Newton Interpolation Lab',
             intro='Interpolate your own equally spaced tables with Newton\'s forward and backward formulas, see every term, and test the limits.',
             tabs=[
                 dict(name='Interpolation solver', blocks=[
                     dict(p='Type the x values (equally spaced) and the y values, then the point x. The table lists every term, exactly as a written solution would show it. Add a true f(x) to see the actual error.'),
                     dict(w='interp', o=dict(method='forward', methods=['forward', 'backward', 'linear'], at=1895, height='320px', side=True, tableHeight='320px',
                                             presets=[['census 1895', '1891 1901 1911 1921 1931', '46 66 81 93 101', 1895, 'forward'], ['census 1925', '1891 1901 1911 1921 1931', '46 66 81 93 101', 1925, 'backward'], ['Problem 3', '1 2 3 4 5', '1 8 27 64 125', 1.5, 'forward', 'x^3'], ['homework 2', '0.1 0.2 0.3 0.4 0.5', '0.09983 0.19867 0.29552 0.38942 0.47943', 0.15, 'forward', 'sin(x)']]))]),
                 dict(name='Difference table', blocks=[
                     dict(p='The difference table behind the formulas.'),
                     dict(w='difftab', o=dict(y='46 66 81 93 101', x0=1891, h=10, noerr=True))]),
                 dict(name='Code', blocks=[
                     dict(h='Newton forward and backward'), dict(code='newtonfb', tasks=['Run it. Compare every term with Problems 1 and 2.', 'Interpolate 1915 with both formulas. Do they agree?', 'Try 1960. What happens, and why?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Derive Newton\'s forward interpolation formula.', 'Put $x = x_0 + ph$. Then $y(x) = E^p y_0 = (1 + \\Delta)^p y_0$; expanding by the binomial theorem gives $y_0 + p\\Delta y_0 + \\frac{p(p-1)}{2!}\\Delta^2 y_0 + \\cdots$.'),
                         ('When do you use the backward formula instead of the forward one?', 'When $x$ lies near the end of the table: the backward formula uses differences at the end ($\\nabla^k y_n$) and keeps $|p| < 1$, so fewer terms are needed and the error is smaller.'),
                         ('From $x$: 1, 2, 3, 4, 5 and $y$: 1, 8, 27, 64, 125 find $y(1.5)$.', 'Forward with $p = 0.5$: $1 + 3.5 - 1.5 + 0.375 = 3.375$ (exactly $1.5^3$).'),
                         ('Why is extrapolation dangerous?', 'The error term contains $p(p-1)\\cdots(p-n)$, which grows rapidly when $x$ is outside the table; nothing in the data controls the polynomial there.'),
                         ('Find $y(0.5)$ for $x$: 0, 1, 2, 3, 4 and $y$: 1, 7, 23, 55, 109.', '$\\Delta y_0 = 6$, $\\Delta^2 y_0 = 10$, $\\Delta^3 y_0 = 6$, $\\Delta^4 y_0 = 0$; $p = 0.5$: $1 + 3 - 1.25 + 0.375 = 3.125$.')])])]),
)
