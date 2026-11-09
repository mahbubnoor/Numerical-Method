LECTURE = dict(
    title='Lagrange and Divided-Difference Interpolation',
    short='Lagrange and Divided Differences',
    sub='Interpolation when the data are not equally spaced: Lagrange\'s formula built from basis polynomials, Newton\'s divided differences that grow one point at a time, inverse interpolation, and why both beat solving for the coefficients.',
    slides=[
        dict(type='cover', id='cover', notes="Recap question: 'Newton's forward formula needs what?' (Equal spacing.) 'What if a sensor misses some readings?' Today's two methods work for any spacing."),
        dict(type='bullets', id='hook', title='The problem: a sensor that skipped some readings', kick='Why this lecture', rw=620,
             lead='A data logger was supposed to record every second, but readings at $t = 3$ and $4$ were lost. We need the value at $t = 3$.',
             items=['The remaining times 0, 1, 2, 5 are <b>not equally spaced</b>', 'Newton\'s forward and backward formulas (Lecture 16) do not apply', 'We still want the polynomial through all the points, and a quick way to update it when a reading is recovered',
                    'Two answers: <b>Lagrange</b> (one formula, any spacing) and <b>divided differences</b> (a table that grows)'],
             frag=True,
             right=dict(table=[['$t$ (s)', '0', '1', '2', '5'], [['$y$', '2', '3', '12', '147']]]),
             notes="The data are y = t³ + t² − t + 2 (do not reveal). Solved during the lecture: y(3) = 35 by both methods. Later the reading at t = 4 (78) is 'recovered' and added with one extra divided difference."),
        dict(type='goals', id='goals', items=[
            'Build <b>Lagrange basis polynomials</b> and interpolate with any spacing',
            'Build a <b>divided-difference table</b> and use Newton\'s general formula',
            'Add a new data point without starting again',
            'Use <b>inverse interpolation</b> to find $x$ for a given $y$',
            'Explain why these formulas beat solving the Vandermonde system'],
            prev='Newton forward and backward: equal spacing only.',
            today='Same polynomial, any spacing: two ways to write it.',
            notes="Emphasise from the start: with n + 1 points there is exactly one polynomial of degree ≤ n through them. Lagrange, divided differences, forward and backward are different ways to write that one polynomial."),
        dict(type='math', id='lagrange', title="Lagrange's formula",
             eqs=[dict(cap='Basis polynomial: 1 at its own point, 0 at all the others', eq='L_i(x) = \\prod_{j \\ne i}\\frac{x - x_j}{x_i - x_j}, \\qquad L_i(x_j) = \\begin{cases} 1 & j = i \\\\ 0 & j \\ne i \\end{cases}'),
                  dict(cap='Interpolating polynomial', eq='P(x) = \\sum_{i=0}^{n} y_i\\,L_i(x) = y_0L_0(x) + y_1L_1(x) + \\cdots + y_nL_n(x)', frag=True)],
             items=['At $x = x_k$ every term vanishes except $y_kL_k(x_k) = y_k$: the curve passes through every point', 'Each $L_i$ has degree $n$, so $P$ has degree at most $n$', 'No equal spacing needed, no table needed', 'Same polynomial as Newton\'s formulas whenever both apply'],
             ifrag=True, rw=620,
             notes="Build L_0 for the opening data on the board: L_0(x) = (x − 1)(x − 2)(x − 5)/((0 − 1)(0 − 2)(0 − 5)) = −(x − 1)(x − 2)(x − 5)/10. Check L_0(0) = 1, L_0(1) = L_0(2) = L_0(5) = 0."),
        dict(type='bullets', id='algo', title="Lagrange interpolation, step by step", kick='The method, step by step', ordered=True, rw=780,
             items=['List the points $(x_0, y_0), \\dots, (x_n, y_n)$; all $x_i$ must be different', 'For each $i$: numerator $\\prod_{j\\ne i}(x - x_j)$, denominator $\\prod_{j\\ne i}(x_i - x_j)$',
                    'Compute $L_i(x)$ = numerator / denominator', 'Add up $y_iL_i(x)$', 'Check: the $L_i(x)$ must add up to 1'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input x[0..n], y[0..n], X\nsum ← 0\nfor i = 0 … n:\n    L ← 1\n    for j = 0 … n, j ≠ i:\n        L ← L·(X − x[j]) / (x[i] − x[j])\n    sum ← sum + y[i]·L\nreturn sum</pre></div><p class="small" style="margin-top:14px">Two nested loops: $O(n^2)$ work for every new $X$.</p>'),
             notes="Step 5 is a free check students rarely use: Σ L_i(x) = 1 for every x, because interpolating the constant 1 gives 1."),
        dict(type='worked', id='p1', title='Problem 1: $y(3)$ by Lagrange',
             q='Points $(0, 2)$, $(1, 3)$, $(2, 12)$, $(5, 147)$. Find $y(3)$.',
             steps=['$L_0(3) = \\dfrac{(3-1)(3-2)(3-5)}{(0-1)(0-2)(0-5)} = \\dfrac{-4}{-10} = 0.4$, $\\quad L_1(3) = \\dfrac{(3)(1)(-2)}{(1)(-1)(-4)} = -1.5$',
                    '$L_2(3) = \\dfrac{(3)(2)(-2)}{(2)(1)(-3)} = 2$, $\\quad L_3(3) = \\dfrac{(3)(2)(1)}{(5)(4)(3)} = 0.1$; check: $0.4 - 1.5 + 2 + 0.1 = 1$ ✓',
                    '$y(3) = 2(0.4) + 3(-1.5) + 12(2) + 147(0.1) = 0.8 - 4.5 + 24 + 14.7$'],
             answer='$y(3) = 35$.',
             right=dict(w='interp', o=dict(method='lagrange', methods=['lagrange'], x='0 1 2 5', y='2 3 12 147', at=3, height='240px', nof=True, fixed=True, side=True, tableHeight='240px')), rw=860,
             notes="Point out the negative L_1(3) = −1.5: basis polynomials can be negative and larger than 1 between the points. That is how high-degree interpolation can amplify data errors."),
        dict(type='math', id='dd', title="Newton's divided differences",
             eqs=[dict(cap='Divided differences: differences divided by the x-gap they span', eq='\\begin{aligned} f[x_i, x_{i+1}] &= \\frac{f[x_{i+1}] - f[x_i]}{x_{i+1} - x_i} \\\\ f[x_i, \\dots, x_{i+k}] &= \\frac{f[x_{i+1}, \\dots, x_{i+k}] - f[x_i, \\dots, x_{i+k-1}]}{x_{i+k} - x_i} \\end{aligned}'),
                  dict(cap="Newton's divided-difference formula", eq='\\begin{aligned} P(x) = {} & f[x_0] + f[x_0,x_1](x - x_0) \\\\ & + f[x_0,x_1,x_2](x - x_0)(x - x_1) + \\cdots \\end{aligned}', frag=True)],
             items=['Equal spacing: $f[x_0, \\dots, x_k] = \\Delta^k y_0/(k!\\,h^k)$, giving the forward formula back', 'Order of the points does not matter: divided differences are symmetric', '<b>Adding a point adds one term</b>; nothing else changes', 'Evaluate with nested multiplication (Horner): $O(n)$ per $x$'],
             ifrag=True, rw=600,
             notes="The top edge of the divided-difference table supplies the coefficients, just as the top diagonal of the ordinary difference table did in Lecture 16."),
        dict(type='bullets', id='algo2', title='Divided differences, step by step', kick='The method, step by step', ordered=True, rw=860,
             items=['Column 0: the $y_i$', 'Column $k$: $\\dfrac{\\text{(lower entry)} - \\text{(upper entry)}}{x_{i+k} - x_i}$, where the denominator spans all points involved', 'Read the coefficients $f[x_0], f[x_0,x_1], \\dots$ from the top edge',
                    'Evaluate $P(x)$ by nested multiplication', 'New point? Add it at the bottom: one new entry per column, one new term'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 25px/1.55 var(--mono);color:#f5f3ee">input x[0..n], y[0..n], X\nc ← copy of y\nfor k = 1 … n:               # build table\n    for i = n … k:\n        c[i] ← (c[i] − c[i−1]) / (x[i] − x[i−k])\n# c[k] = f[x0, …, xk]\np ← c[n]\nfor k = n−1 … 0:             # Horner\n    p ← c[k] + (X − x[k])·p\nreturn p</pre></div><p class="small" style="margin-top:14px">$O(n^2)$ once for the table, then $O(n)$ for each $X$.</p>'),
             notes="The commonest mistake: dividing by the gap between neighbouring x values in higher columns. The denominator must be x_{i+k} − x_i, the full span."),
        dict(type='table', id='p2', title='Problem 2: the same data by divided differences',
             q='Build the divided-difference table for $t = 0, 1, 2, 5$ and find $y(3)$. Then add the recovered reading $y(4) = 78$.',
             head=['$x_i$', '$f[x_i]$', 'first', 'second', 'third', 'fourth (with $x = 4$)'], frag=True,
             rows=[['0', '2', '$\\frac{3-2}{1-0} = 1$', '$\\frac{9-1}{2-0} = 4$', '$\\frac{9-4}{5-0} = 1$', '$\\frac{1-1}{4-0} = 0$'], ['1', '3', '$\\frac{12-3}{2-1} = 9$', '$\\frac{45-9}{5-1} = 9$', '$\\frac{12-9}{4-1} = 1$', ''],
                   ['2', '12', '$\\frac{147-12}{5-2} = 45$', '$\\frac{69-45}{4-2} = 12$', '', ''], ['5', '147', '$\\frac{78-147}{4-5} = 69$', '', '', ''], ['4', '78', '', '', '', '']],
             note='$P(x) = 2 + 1\\cdot x + 4x(x-1) + 1\\cdot x(x-1)(x-2)$, so $P(3) = 2 + 3 + 24 + 6 = 35$. The new point adds one entry per column; the fourth divided difference is 0, so the data are a cubic.',
             notes="The last row and column appear only after the new point is added: draw them in a different colour.\n\nThe polynomial expands to x³ + x² − x + 2, the hidden formula."),
        dict(type='widget', id='explore', title='Explore: Lagrange and divided differences', w='interp',
             o=dict(method='divided', methods=['lagrange', 'divided'], x='0 1 2 5', y='2 3 12 147', at=3, height='320px', side=True, tableHeight='320px',
                    presets=[['opening data', '0 1 2 5', '2 3 12 147', 3, 'divided'], ['with t = 4', '0 1 2 5 4', '2 3 12 147 78', 3, 'divided'], ['Problem 4', '5 7 11 13 17', '150 392 1452 2366 5202', 9, 'lagrange'], ['√x, unequal', '1 4 9 16', '1 2 3 4', 10, 'lagrange', 'sqrt(x)']]), lw=440,
             items=['Switch the method: the curve and the estimate do not change', 'Lagrange table: each $L_i(x)$; divided table: each coefficient and term', 'Add a point to the lists and watch only the last row change (divided)', 'The $\\sqrt{x}$ preset shows a real interpolation error'],
             notes="Use the 'with t = 4' preset: the divided-difference table gets one more row with coefficient 0, confirming the cubic."),
        dict(type='worked', id='p3', title='Problem 3: inverse interpolation',
             q='From $x$: 2, 3, 4 and $y = x^2$: 4, 9, 16, estimate the $x$ at which $y = 10$ (that is, $\\sqrt{10}$).',
             steps=['Swap roles: treat $x$ as a function of $y$, with points $(4, 2)$, $(9, 3)$, $(16, 4)$', 'Lagrange in $y$ at $y = 10$: $\\;L_0 = \\dfrac{(10-9)(10-16)}{(4-9)(4-16)} = -0.1$, $\\;L_1 = \\dfrac{(10-4)(10-16)}{(9-4)(9-16)} = \\dfrac{36}{35}$, $\\;L_2 = \\dfrac{(10-4)(10-9)}{(16-4)(16-9)} = \\dfrac{1}{14}$',
                    '$x = 2(-0.1) + 3\\left(\\tfrac{36}{35}\\right) + 4\\left(\\tfrac{1}{14}\\right) = 3.1714$'],
             answer='$x \\approx 3.1714$ (true $\\sqrt{10} = 3.1623$, error 0.009). Inverse interpolation works when $y$ is monotonic in the range.',
             notes="Inverse interpolation is a root finder without iteration: to solve f(x) = c, interpolate x as a function of y and evaluate at c. Inverse quadratic interpolation is one ingredient of Brent's method (Lecture 10 applications)."),
        dict(type='compare', id='classic', title='Same polynomial, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (solve for the coefficients)', tag='Linear algebra', cls='blue', items=['Write $P(x) = a_0 + a_1x + a_2x^2 + a_3x^3$', 'Four conditions $P(x_i) = y_i$: a 4×4 Vandermonde system (Lecture 12)', 'Get $a = (2, -1, 1, 1)$, then $P(3) = 35$']),
             right=dict(h='Numerical (Lagrange / divided differences)', tag='Formula', cls='key', items=['No system to solve', 'Divided differences: one small table, $P(3) = 35$', 'A new point: one more row, not a new system']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>20 points on [0, 1]</h3><p>The Vandermonde matrix has condition number about $10^{16}$ (Lecture 11): all 16 digits of double precision can be lost and the coefficients are garbage. Lagrange (in barycentric form) and divided differences never form that matrix and stay accurate.</p></div>'),
             notes="Condition numbers of the Vandermonde matrix on equally spaced points in [0, 1]: 5 points 6.9×10², 10 points 1.5×10⁷, 15 points 4×10¹¹, 20 points 1.2×10¹⁶."),
        dict(type='code', id='code', title='Lagrange and divided differences in Python and C', code='lagdiv', lw=560,
             items=['Lagrange: the two nested loops of the pseudocode', 'Divided differences built in place, then Horner', 'Both print $y(3) = 35$', 'Lab: add the point $(4, 78)$ and compare'],
             notes="Run both tabs. In SciPy: scipy.interpolate.lagrange (fine for a few points) and scipy.interpolate.BarycentricInterpolator (stable for many)."),
        dict(type='widget', id='fail', title='Limitations shown failing', kick='When polynomial interpolation goes wrong', w='interp',
             o=dict(method='lagrange', methods=['lagrange', 'spline'], x='-1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1', y='0.038462 0.058824 0.1 0.2 0.5 1 0.5 0.2 0.1 0.058824 0.038462', at=0.9, f='1/(1+25x^2)', height='300px', side=True, tableHeight='300px',
                    presets=[['11 equal points', '-1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1', '0.038462 0.058824 0.1 0.2 0.5 1 0.5 0.2 0.1 0.058824 0.038462', 0.9, 'lagrange', '1/(1+25x^2)'], ['noisy data', '0 1 2 3 4 5 6', '0.1 0.9 2.2 2.8 4.1 5.0 5.9', 5.5, 'lagrange', 'x'], ['inverse fails', '1 8 27 64', '1 2 3 4', 50, 'lagrange', 'x^(1/3)']]), lw=540,
             items=['<b>Many points, high degree</b>: wild swings near the ends (Runge); look at the $L_i$ values: some are huge', '<b>Noisy data</b>: the polynomial passes exactly through every error', '<b>Inverse interpolation</b> far from the points is unreliable',
                    'Lagrange costs $O(n^2)$ per evaluation and restarts when a point is added'],
             frag=True,
             notes="With 11 equally spaced points of the Runge function, some |L_i(0.9)| values exceed 5, so data errors are multiplied by that much. Switch the method to 'natural cubic spline' to preview Lecture 18: error 0.02 instead of 1.5.\n\nThe noisy preset: the true trend is y = x, but the degree-6 polynomial wiggles to pass through every noisy point."),
        dict(type='exam', id='practice', src='Problem 4',
             q='"Using Lagrange\'s interpolation formula, find $f(9)$ from the table: $x$: 5, 7, 11, 13, 17; $f(x)$: 150, 392, 1452, 2366, 5202. Verify with Newton\'s divided-difference formula."',
             tips=['Write the formula with all five basis polynomials evaluated at $x = 9$, then add', 'Answer $f(9) = 810$', 'Divided differences: first 121, 265, 457, 709; second 24, 32, 42; third 1, 1; fourth 0',
                   'Newton: $150 + 121(4) + 24(4)(2) + 1(4)(2)(-2) = 810$ ✓; the zero fourth difference shows the data are a cubic'],
             notes=""),
        dict(type='profile', id='profile', title='Lagrange and divided differences: method profile',
             best=['A handful of points with <b>any spacing</b>', 'Divided differences: points arriving one at a time', 'Exact for polynomial data; elegant formulas for theory'],
             worst=['Many equally spaced points (Runge oscillation)', 'Noisy data: the curve chases the noise', 'Lagrange evaluated naively at many $x$: $O(n^2)$ each'],
             suited=['Irregular samples, few points', 'Deriving quadrature rules (Simpson, Gauss: Lecture 20)', 'Exact algebra over finite fields: secret sharing, error-correcting codes'],
             avoid=['Long data sets (splines, Lecture 18)', 'Noisy measurements (least squares, Lecture 23)', 'Solving for the monomial coefficients (Vandermonde)'],
             verdict='Rule of thumb: <b>few points, any spacing → divided differences (or barycentric Lagrange); many points → splines; noisy points → least squares</b>.',
             notes="Barycentric Lagrange (used inside the widgets) rewrites the formula so that each evaluation is O(n) and numerically stable."),
        dict(type='table', id='compare', title='Comparative analysis: four ways to write one polynomial', cls='tb sm',
             head=['Form', 'Spacing', 'Setup', 'Each new $x$', 'New point', 'Main use'], tx=(0, 5), frag=True,
             rows=[['Monomial (Vandermonde)', 'any', '$O(n^3)$ solve, ill-conditioned', '$O(n)$', 'resolve', 'avoid'], ['Newton forward/backward', 'equal', '$O(n^2)$ table', '$O(n)$', 'one term', 'tables, hand work'],
                   ['Lagrange', 'any', 'none', '$O(n^2)$ (barycentric $O(n)$)', 'restart (barycentric: update)', 'theory, few points'], ['Divided differences', 'any', '$O(n^2)$ table', '$O(n)$', 'one row, one term', 'irregular data']],
             note='All four give the same polynomial through the same points; only cost and rounding differ.', notefrag=True,
             notes="A good written answer to 'compare Lagrange and Newton divided differences' uses these columns: spacing, effort, adding points, numerical behaviour."),
        dict(type='bridge', id='bridge', lead='Both methods handle any spacing, but one polynomial through many points behaves badly.',
             keep=['Any spacing', 'Exact through the data', 'Divided differences grow one point at a time', 'Inverse interpolation for quick root estimates'],
             rows=[['Oscillation with many points (Runge)', 'Piecewise cubics: splines', 18],
                   ['Noise is reproduced exactly', 'Fit instead of interpolate: least squares', 23],
                   ['We need derivatives or integrals of tabulated data', 'Differentiate or integrate the interpolant', 19],
                   ['Quadrature rules with unequal points', 'Gauss quadrature from Lagrange basis', 20]],
             notes="Lecture 18 answers the first row and closes Module 4."),
        dict(type='apps', id='apps', n=2, lead='Click a card: each uses the Lagrange or divided-difference formula at a specific step.',
             items=[
                 dict(ic='🔑', h="Shamir's secret sharing", t='Split a password among people; any 3 can rebuild it',
                      detail=dict(where='cryptography (key management, crypto wallets). The secret is $P(0)$ of a random polynomial; each person receives one point. Any 3 points determine the quadratic, and Lagrange at $x = 0$ recovers the secret.',
                                  eq='P(x) = 1234 + 166x + 94x^2; \\quad \\text{shares } (1, 1494), (2, 1942), (3, 2578)',
                                  steps=['At $x = 0$: $L_1(0) = \\dfrac{(0-2)(0-3)}{(1-2)(1-3)} = 3$, $L_2(0) = \\dfrac{(0-1)(0-3)}{(2-1)(2-3)} = -3$, $L_3(0) = \\dfrac{(0-1)(0-2)}{(3-1)(3-2)} = 1$', 'Secret $= 3(1494) - 3(1942) + 1(2578) = 1234$ ✓', 'With only 2 shares, every secret is still possible: nothing leaks'],
                                  note='Real systems do the same arithmetic modulo a large prime, so the shares reveal nothing about the size of the secret.')),
                 dict(ic='📀', h='Reed–Solomon codes', t='Why scratched CDs and dirty QR codes still work',
                      detail=dict(where='error-correcting codes in QR codes, CDs, DVDs, deep-space links and RAID storage. The message is the coefficients of a polynomial; the stored data are its values at many points. Lost values are rebuilt by interpolation from the surviving ones.',
                                  steps=['Message of $k$ symbols defines a polynomial of degree $k - 1$', 'Store $n > k$ values: the extra $n - k$ are redundancy', 'Any $k$ correct values determine the polynomial (Lagrange)', 'Decoders also locate wrong values, not only missing ones'],
                                  note='A QR code with level H error correction survives about 30% damage.')),
                 dict(ic='⏱️', h='Irregular time stamps', t='Merging sensors that sample at different times',
                      detail=dict(where='sensor fusion (phones, drones, wearables). The accelerometer and the GPS report at different, irregular times; to combine them, each signal is interpolated to common time stamps.',
                                  w='interp', o=dict(method='divided', methods=['divided', 'lagrange', 'linear'], x='0 0.13 0.31 0.52 0.66', y='0 0.380 0.802 1.000 0.917', at=0.4, f='sin(3x)', height='200px'),
                                  note='Here the samples are of $\\sin 3t$ at irregular times; the estimate at $t = 0.4$ is compared with the true value. Low degree (3–4 points around $t$) is the safe choice.')),
                 dict(ic='∫', h="Where Simpson's rule comes from", t='Integrate the Lagrange polynomial',
                      detail=dict(where='numerical integration (Lecture 20). Interpolate $f$ at $a$, $m = (a+b)/2$, $b$ by the Lagrange quadratic and integrate it exactly: the weights are the integrals of the $L_i$.',
                                  eq='\\int_a^b f\\,dx \\approx \\sum_i f(x_i)\\int_a^b L_i(x)\\,dx = \\frac{b - a}{6}\\big[f(a) + 4f(m) + f(b)\\big]',
                                  note='Every Newton–Cotes and Gauss rule is built this way: interpolate, then integrate the interpolant.'))],
             notes="The secret-sharing numbers are the classic Wikipedia example; let students verify the three shares from P(x)."),
        dict(type='check', id='check', q='Lagrange basis for $x_0 = 1$, $x_1 = 3$, $x_2 = 4$. What is $L_0(2)$?',
             opts=['$\\tfrac{1}{3}$', '$-\\tfrac{1}{3}$', '$\\tfrac{2}{3}$', '$1$'], right=0,
             answer='A. $L_0(2) = \\dfrac{(2-3)(2-4)}{(1-3)(1-4)} = \\dfrac{(-1)(-2)}{(-2)(-3)} = \\dfrac{2}{6} = \\tfrac13$.',
             notes="Common slip: a sign error in one factor gives −1/3. Remind students to count the negative factors in numerator and denominator separately."),
        dict(type='summary', id='summary', items=[
            'Lagrange: $P(x) = \\sum y_iL_i(x)$, $L_i(x) = \\prod_{j\\ne i}\\frac{x - x_j}{x_i - x_j}$; any spacing',
            'Divided differences: a table divided by spans; Newton\'s general formula, one term per new point',
            'Same polynomial as Newton forward/backward; never solve the Vandermonde system',
            'Inverse interpolation: swap $x$ and $y$; many points or noisy data need other tools'],
            hw=['Find $f(2)$ by Lagrange from $x$: 0, 1, 3, 4 and $f$: $-12$, $-9$, 3, 12.', 'Build the divided-difference table for $x$: 1, 2, 4, 7 and $f$: 2, 8, 62, 338 and find $f(5)$.',
                'From $x$: 1, 2, 3 and $y = x^3$: 1, 8, 27, find by inverse interpolation the $x$ with $y = 10$. Compare with $\\sqrt[3]{10}$.', 'Make your own secret-sharing example with a quadratic and check that any 3 shares recover the secret.'],
            solved='$y(3) = 35$ by Lagrange and by divided differences; adding the recovered reading $y(4) = 78$ needed one new row, and its zero fourth divided difference showed the data are a cubic.',
            next='<b>Splines and the Runge phenomenon.</b> Why one polynomial through many points fails, and how piecewise cubics fix it.',
            notes="Homework answers: Q1: f(2) = −4 (the data are x² + 2x − 12). Q2: divided differences 6, 27, 92; 7, 13; 1; f(5) = 122. Q3: inverse Lagrange gives x ≈ 2.2233; true 10^(1/3) = 2.1544 (error 0.07: x(y) = y^{1/3} is far from quadratic). Q4: any quadratic works."),
    ],
    code={
        'lagdiv': dict(file='lagrange_divided', py='''# Lagrange and Newton divided-difference interpolation (any spacing)
x = [0.0, 1.0, 2.0, 5.0]
y = [2.0, 3.0, 12.0, 147.0]
X = 3.0
n = len(x)

total = 0.0                                   # Lagrange
for i in range(n):
    L = 1.0
    for j in range(n):
        if j != i:
            L *= (X - x[j]) / (x[i] - x[j])
    print(f"L{i}({X:g}) = {L:8.4f}")
    total += y[i] * L
print(f"Lagrange: y({X:g}) = {total:.4f}")

c = y[:]                                      # divided differences, in place
for k in range(1, n):
    for i in range(n - 1, k - 1, -1):
        c[i] = (c[i] - c[i - 1]) / (x[i] - x[i - k])
print("coefficients:", " ".join(f"{v:g}" for v in c))
p = c[n - 1]
for k in range(n - 2, -1, -1):                # nested (Horner) evaluation
    p = c[k] + (X - x[k]) * p
print(f"Divided differences: y({X:g}) = {p:.4f}")
''', c='''/* Lagrange and Newton divided-difference interpolation (any spacing) */
#include <stdio.h>
#define N 4

int main(void) {
    double x[N] = {0, 1, 2, 5}, y[N] = {2, 3, 12, 147}, c[N], X = 3, total = 0;

    for (int i = 0; i < N; i++) {                 /* Lagrange */
        double L = 1;
        for (int j = 0; j < N; j++)
            if (j != i) L *= (X - x[j]) / (x[i] - x[j]);
        printf("L%d(%g) = %8.4f\\n", i, X, L);
        total += y[i] * L;
    }
    printf("Lagrange: y(%g) = %.4f\\n", X, total);

    for (int i = 0; i < N; i++) c[i] = y[i];      /* divided differences */
    for (int k = 1; k < N; k++)
        for (int i = N - 1; i >= k; i--) c[i] = (c[i] - c[i - 1]) / (x[i] - x[i - k]);
    printf("coefficients:");
    for (int i = 0; i < N; i++) printf(" %g", c[i]);
    printf("\\n");
    double p = c[N - 1];
    for (int k = N - 2; k >= 0; k--) p = c[k] + (X - x[k]) * p;   /* Horner */
    printf("Divided differences: y(%g) = %.4f\\n", X, p);
    return 0;
}
'''),
    },
    lab=dict(title='Lagrange and Divided Difference Lab',
             intro='Interpolate data with any spacing, compare Lagrange with divided differences, and try inverse interpolation.',
             tabs=[
                 dict(name='Interpolation solver', blocks=[
                     dict(p='Type any x values (all different) and y values. The table shows each Lagrange basis value or each divided-difference term: use it to check your hand work.'),
                     dict(w='interp', o=dict(method='lagrange', methods=['lagrange', 'divided', 'spline', 'linear'], x='0 1 2 5', y='2 3 12 147', at=3, height='320px', side=True, tableHeight='320px',
                                             presets=[['opening data', '0 1 2 5', '2 3 12 147', 3, 'lagrange'], ['Problem 4', '5 7 11 13 17', '150 392 1452 2366 5202', 9, 'divided'], ['homework 1', '0 1 3 4', '-12 -9 3 12', 2, 'lagrange'], ['homework 2', '1 2 4 7', '2 8 62 338', 5, 'divided'], ['inverse √10', '4 9 16', '2 3 4', 10, 'lagrange', 'sqrt(x)']]))]),
                 dict(name='Code', blocks=[
                     dict(h='Lagrange and divided differences'), dict(code='lagdiv', tasks=['Run it. Do both methods give 35?', 'Add the point (4, 78). Which coefficient appears, and what is its value?', 'Change X to 10 (extrapolation). Is the answer believable? Compare with 10³ + 10² − 10 + 2.'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Write Lagrange\'s interpolation formula for three points.', '$P(x) = y_0\\frac{(x-x_1)(x-x_2)}{(x_0-x_1)(x_0-x_2)} + y_1\\frac{(x-x_0)(x-x_2)}{(x_1-x_0)(x_1-x_2)} + y_2\\frac{(x-x_0)(x-x_1)}{(x_2-x_0)(x_2-x_1)}$.'),
                         ('Give one advantage of divided differences over Lagrange.', 'Adding a new point only adds one row to the table and one term to the formula; Lagrange must recompute every basis polynomial.'),
                         ('Find $f(2)$ from $x$: 0, 1, 3, 4 and $f$: $-12$, $-9$, 3, 12.', '$L_0(2) = \\frac{(1)(-1)(-2)}{(-1)(-3)(-4)} = -\\tfrac16$, $L_1(2) = \\tfrac23$, $L_2(2) = \\tfrac23$, $L_3(2) = -\\tfrac16$; $f(2) = 2 - 6 + 2 - 2 = -4$.'),
                         ('What is inverse interpolation?', 'Finding the $x$ that gives a known $y$ by interpolating $x$ as a function of $y$ (swap the columns of the table). It works when $y$ is monotonic over the data.'),
                         ('Why not find the coefficients by solving the Vandermonde system?', 'It costs $O(n^3)$ and the Vandermonde matrix is badly ill-conditioned (about $10^{16}$ for 20 equally spaced points on $[0, 1]$), so the coefficients lose all their digits.')])])]),
)
