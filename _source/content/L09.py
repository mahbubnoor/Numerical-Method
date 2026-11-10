LECTURE = dict(
    title='The Newton–Raphson Method',
    short='Newton–Raphson Method',
    sub='Replace the curve by its tangent line and jump to where the tangent crosses the axis. Near a simple root the number of correct digits doubles every step; far from it, anything can happen.',
    slides=[
        dict(type='cover', id='cover', notes="Recall the Babylonian square-root loop from Lecture 1: digits doubled every step. Today we discover that it was Newton's method all along, applied to f(x) = x² − N.\n\nNewton's method is the workhorse behind square roots in hardware, optimisation in machine learning, and most nonlinear solvers."),
        dict(type='bullets', id='hook', title='The problem: divide without dividing', kick='Why this lecture', rw=760,
             lead='Division is the slowest arithmetic operation in hardware. Can a chip compute $1/7$ using only multiplication and subtraction?',
             items=['We want $x = 1/7$: the root of $f(x) = \\dfrac{1}{x} - 7$', 'Some rule $x_{n+1} = (\\text{something})$ that improves a guess using only $\\times$ and $-$', 'Bisection would need 20 steps for 6 digits; fixed-point iteration needs the right $g$', 'Today\'s method gives the rule $x_{n+1} = x_n(2 - 7x_n)$, and the digits <b>double</b> every step'],
             frag=True,
             right=dict(table=[['$n$', '$x_n$', 'correct digits'], [['0', '0.1', '0'], ['1', '0.13', '1'], ['2', '0.1417', '2'], ['3', '0.14284777', '5'], ['4', '0.14285714', '10+']]]),
             notes="Present the problem; hide the table at first (it is not a fragment, so cover it or just point later). Students will not see how to get the rule; the derivation is on the slide \"Newton inside your computer\" (Newton applied to f(x) = 1/x − N gives x(2 − Nx)). The summary returns to it.\n\nTrue value 1/7 = 0.142857142857..."),
        dict(type='goals', id='goals', items=[
            'Derive the Newton–Raphson formula geometrically and from Taylor series',
            'Carry out Newton\'s method by hand to a required accuracy (iteration tables)',
            'Explain <b>quadratic convergence</b>: errors square, digits double',
            'Recognise the <b>failure cases</b>: $f\'(x) \\approx 0$, cycles, divergence, multiple roots',
            'Implement Newton in Python and C with proper safeguards',
            'Know its <b>best and worst cases</b>, and when to choose it over the other methods'],
            prev='Fixed-point iteration converges linearly with rate $|g\'(r)|$; if $g\'(r) = 0$ it is much faster.',
            today='Newton\'s method is the fixed-point iteration whose $g\'(r) = 0$, built from the tangent line.',
            notes="Bridge from Lecture 8: the table of rearrangements for x³ + x − 1 ended with a 'magic' g that had g'(r) = 0. Today we see where that g comes from."),
        dict(type='math', id='derive', title='Deriving the formula',
             eqs=[dict(cap='Tangent line at x_n', eq='y = f(x_n) + f\'(x_n)(x - x_n)'),
                  dict(cap='Set y = 0', eq='x_{n+1} = x_n - \\frac{f(x_n)}{f\'(x_n)}', frag=True),
                  dict(cap='Same thing from Taylor (Lecture 3)', eq='0 = f(r) \\approx f(x_n) + f\'(x_n)(r - x_n) \\;\\Rightarrow\\; r \\approx x_n - \\frac{f(x_n)}{f\'(x_n)}', frag=True)],
             items=['Geometric: follow the tangent down to the axis', 'Analytic: keep the first two Taylor terms, solve the linear equation', 'Needs $f\'(x)$ and one starting value $x_0$; no bracket', 'Fixed-point view: $g(x) = x - f/f\'$ has $g\'(r) = \\dfrac{f(r)f\'\'(r)}{f\'(r)^2} = 0$'],
             ifrag=True,
             notes="Draw the picture: curve, point (x_n, f(x_n)), tangent, its x-intercept x_{n+1}.\n\nThe third derivation (fixed-point view) links to last lecture: g'(x) = 1 − (f'² − f f'')/f'² = f f''/f'², which vanishes at a root. That single fact explains the speed."),
        dict(type='bullets', id='algo', title='The Newton–Raphson algorithm', kick='The method, step by step', ordered=True, rw=780,
             items=["Find $f'(x)$; choose $x_0$ near the root (from a sketch or a sign change)", "Compute $x_{n+1} = x_n - \\dfrac{f(x_n)}{f'(x_n)}$", "If $f'(x_n) = 0$ (flat tangent), stop and choose another $x_0$", 'Repeat until $|x_{n+1} - x_n| < \\varepsilon$ (the required digits stop changing)', 'Answer: the last $x_{n+1}$; check that $f(x_{n+1}) \\approx 0$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input f, df, x0, tol, N\nx ← x0\nrepeat up to N times:\n    d ← df(x)\n    if d = 0: stop (flat tangent)\n    x_new ← x − f(x) / d\n    if |x_new − x| &lt; tol:\n        return x_new\n    x ← x_new\nstop: no convergence</pre></div><p class="small" style="margin-top:14px">One function value and one derivative value per step. No bracket, so nothing guarantees convergence: the cap $N$ matters.</p>'),
             notes="Step 1 is where a written solution should show f'(x) explicitly and say why x0 was chosen (for example f(1) < 0 < f(2), so start at an end point or the midpoint).\n\nStep 5: substituting back into f is the cheapest error check there is."),
        dict(type='widget', id='nw', title='Explore: tangent after tangent', w='root', o=dict(method='newton', fixed=True, f='x^3 - x - 2', a=1.5, height='440px', side=True, tableHeight='440px', dec=9), lw=420,
             items=['The dashed orange line is the tangent at $x_n$', 'Its crossing gives $x_{n+1}$', 'Look at the $|x_{n+1} - x_n|$ column: $2\\times10^{-2}$, $4\\times10^{-4}$, $10^{-7}$, $10^{-14}$', 'Compare: bisection needed 14 steps for $10^{-4}$; Newton needs 3'],
             notes="Step through. The table shows 9 decimals so the doubling of correct digits is visible: 1.521739130, 1.521379806, 1.521379707.\n\nThen type x0 = 0.6 (near the local minimum of x³ − x − 2 at x = 0.577): the first tangent is almost flat and throws x1 far away (to about 30). Newton recovers here, slowly, but it shows the sensitivity to x0."),
        dict(type='table', id='mid', title='Problem 1: $f(x) = 2x^3 - 2x - 5$',
             src='Problem 1', q='"Find out the root of the following equation using the Newton–Raphson method: $f(x) = 2x^3 - 2x - 5$." Here $f\'(x) = 6x^2 - 2$; $f(1) = -5$, $f(2) = 7$, so start at $x_0 = 1.5$.',
             head=['$n$', '$x_n$', '$f(x_n)$', "$f'(x_n)$", '$x_{n+1} = x_n - f/f\'$', '$|x_{n+1} - x_n|$'], frag=True, ans=-1,
             rows=[[0, '1.500000', '−1.250000', '11.500000', '1.608696', '0.108696'], [1, '1.608696', '0.108901', '13.527410', '1.600645', '0.008050'], [2, '1.600645', '0.000625', '13.372391', '1.600599', '0.000047'], [3, '1.600599', '0.000000', '13.371494', '1.600599', '0.000000']],
             note='Root ≈ 1.600599 (correct to 6 decimals after 3 iterations). Check: $f(1.600599) = 2(4.100667) - 3.201198 - 5 \\approx 0$.',
             notes="Arithmetic for row 0: x1 = 1.5 − (−1.25)/11.5 = 1.5 + 0.108696 = 1.608696.\n\nThe last column shrinks 0.1 → 0.008 → 0.00005: each roughly the square of the previous (times a constant). That is quadratic convergence."),
        dict(type='worked', id='sinexp', title='Problem 2: $3x + \\sin x = e^{x}$ to 5 decimal places',
             src='Problem 2', q='"Use Newton–Raphson method to find a real root of the equation $3x + \\sin x = e^{x}$ correct up to 5 decimal places."',
             steps=['$f(x) = 3x + \\sin x - e^{x}$, $\\;f\'(x) = 3 + \\cos x - e^{x}$; $f(0) = -1$, $f(1) = 1.123189$: root in $(0, 1)$; take $x_0 = 0$',
                    '$x_1 = 0 - \\dfrac{-1}{3} = 0.333333$',
                    '$x_2 = 0.333333 - \\dfrac{-0.068418}{2.549345} = 0.360171$',
                    '$x_3 = 0.360171 - \\dfrac{-0.000628}{2.502263} = 0.360422$; $\\;x_4 = 0.360422$ (change $< 10^{-6}$)'],
             answer='$x = 0.36042$ (to 5 decimal places). Radians! A calculator in degree mode gives nonsense.',
             notes="Common mistakes: forgetting radian mode; writing f'(x) = 3 + cos x + e^x (sign error).\n\nThere is a second root near 1.89 (f(1.8) > 0 > f(2)). If asked for 'a real root', one is enough; mention the other for full credit if time permits."),
        dict(type='compare', id='classic', title='Same problem, two approaches: $x^3 - x - 2 = 0$', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (exact formula)', tag='Algebra', cls='blue', items=['Cardano (1545): $x = \\sqrt[3]{1 + \\sqrt{26/27}} + \\sqrt[3]{1 - \\sqrt{26/27}}$', '$= 1.2559834 + 0.2653963 = 1.5213797$', 'Needs square and cube roots (computed by Newton inside the calculator!), and $1 - \\sqrt{26/27} = 0.0187$ is a cancellation that loses about 2 digits']),
             right=dict(h='Numerical (Newton)', tag='Algorithm', cls='key', items=['$x_{n+1} = x_n - \\dfrac{x_n^3 - x_n - 2}{3x_n^2 - 1}$ from 1.5', '3 iterations: $1.521739$, $1.521380$, $1.5213797$', 'Same answer, simpler, and the same code works for any cubic']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>The quintic $x^5 - x - 1 = 0$</h3><p>Abel–Ruffini theorem (1824): there is no formula in radicals for general degree-5 equations, and this one is a standard example. Newton from $x_0 = 1$: $x = 1.167304$ in 5 iterations.</p></div><p class="small frag fade">Even where a formula exists, numerical methods are often <b>simpler and more accurate</b>; beyond degree 4 they are the only general option.</p>'),
             notes="Cardano's formula is a lovely historical result, but in practice nobody uses it for computation: it involves cancellation and nested roots. Numerical libraries (numpy.roots) compute polynomial roots as matrix eigenvalues, a numerical method.\n\nx^5 − x − 1 is the textbook example of a quintic whose Galois group is S5, so it is not solvable by radicals."),
        dict(type='math', id='quad', title='Why so fast? Quadratic convergence',
             eqs=[dict(cap='Error relation (from Taylor about x_n)', eq='e_{n+1} \\approx \\frac{f\'\'(r)}{2f\'(r)}\\,e_n^{2}, \\qquad e_n = x_n - r')],
             right=dict(table=[['$n$', '$x_n$ for $x^3 - x - 2$', '$|e_n|$', '$|e_{n+1}|/e_n^2$'], [[0, '1.5', '2.1e−2', '0.786'], [1, '1.521739130', '3.6e−4', '0.768'], [2, '1.521379806', '9.9e−8', '0.768'], [3, '1.521379707', '7.6e−15', '—']]], cls='tb sm', frag=True), rw=820,
             below=dict(items=['Errors are <b>squared</b> each step: $10^{-2} \\to 10^{-4} \\to 10^{-8} \\to 10^{-16}$', 'Correct digits roughly <b>double</b> each step', 'Measured ratio 0.768 matches theory $\\dfrac{6r}{2(3r^2 - 1)} = 0.768$ ✓', 'Only <b>near</b> a <b>simple</b> root ($f\'(r) \\ne 0$); far away, no promise'], frag=True),
             notes="Derivation sketch: 0 = f(r) = f(x_n) + f'(x_n)(r − x_n) + ½f''(ξ)(r − x_n)². Divide by f'(x_n) and use the Newton formula: x_{n+1} − r = (f''(ξ)/(2f'(x_n)))(x_n − r)².\n\nCompare orders: bisection, fixed point: linear (order 1). Secant: order 1.618 (Lecture 10). Newton: order 2."),
        dict(type='cards', id='sqrt', title='Newton inside your computer', n=2,
             cards=[dict(tag='Square root', h='$f(x) = x^2 - N$', eq='x_{n+1} = x_n - \\frac{x_n^2 - N}{2x_n} = \\frac12\\left(x_n + \\frac{N}{x_n}\\right)', t='Exactly the Babylonian method of Lecture 1. $\\sqrt{10}$ from $x_0 = 3$: 3.166667, 3.162281, 3.162278.'),
                    dict(tag='Division without dividing', h='$f(x) = \\dfrac{1}{x} - N$', eq='x_{n+1} = x_n(2 - N x_n)', t='Only multiplications! CPUs and GPUs compute $1/N$ like this. $1/7$ from $x_0 = 0.1$: 0.13, 0.1417, 0.142848, 0.14285714.', cls='key'),
                    dict(tag='Cube root', h='$f(x) = x^3 - N$', eq='x_{n+1} = \\frac{1}{3}\\left(2x_n + \\frac{N}{x_n^2}\\right)', t='$\\sqrt[3]{17}$ from $x_0 = 2.5$: 2.573333, 2.571283, 2.571282.'),
                    dict(tag='Graphics', h='Fast inverse square root', t='The famous Quake III code computes $1/\\sqrt{x}$ with a bit-trick guess followed by one Newton step $y(1.5 - 0.5xy^2)$.', cls='blue')],
             notes="The division card surprises students: you can divide using only multiplication. Hardware dividers use this (or a close relative) because multiplications are fast.\n\nAsk the class to derive the cube-root formula themselves (f' = 3x²)."),
        dict(type='code', id='code', title='Newton–Raphson in Python and C', code='newton', lw=560,
             items=['Supply both $f$ and $f\'$', 'Stops when $|x_{n+1} - x_n| < \\text{tol}$', 'Guards: $f\'(x) = 0$ check and an iteration cap', 'Try $x_0 = 0.6$ (near the minimum of $f$) and see the big first jump'],
             notes="Run both tabs: 1.521380 after 3 iterations from 1.5.\n\nThen x0 = 0.6: f'(0.6) = 0.08, so x1 = 30.4; Newton needs 13 iterations in total to come back and converge. Show that the derivative guard does not trigger (f' is small, not zero): in production code also cap the step size."),
        dict(type='exam', id='practice', src='Problem 3',
             q='"Newton–Raphson\'s method can fail to converge, or converge to an unintended root, for certain functions or starting points. Describe two distinct scenarios in which this happens, each with a brief illustrative example. Then explain how the Secant method removes the requirement of an analytical derivative and identify one drawback it introduces in exchange."',
             tips=['Scenario 1, stationary point: $f(x) = x^2 - 1$, $x_0 = 0$: $f\'(0) = 0$, the tangent never meets the axis',
                   'Scenario 2, cycle: $f(x) = x^3 - 2x + 2$, $x_0 = 0$: $x_1 = 1$, $x_2 = 0$, … forever (or divergence: $\\tan^{-1}x$ from 1.5)',
                   'Unintended root: starting near a local extremum throws $x_1$ far away, possibly into another root\'s basin',
                   'Secant: replace $f\'(x_n)$ by $\\dfrac{f(x_n) - f(x_{n-1})}{x_n - x_{n-1}}$ (Lecture 10)',
                   'Drawback: needs two starting values, order drops to 1.618, and can still diverge (no bracket)'],
             notes=""),
        dict(type='widget', id='fail', title='When Newton fails', w='root', o=dict(method='newton', fixed=True, f='x^3 - 2x + 2', a=0, height='420px', side=True, tableHeight='420px', dec=6,
             presets=[['cycle: x³ − 2x + 2, x₀ = 0', 'x^3 - 2x + 2', 0], ['flat tangent: x² − 1, x₀ = 0', 'x^2 - 1', 0], ['divergence: atan x, x₀ = 1.5', 'atan(x)', 1.5], ['double root: (x − 1)², x₀ = 2', '(x-1)^2', 2], ['good start: x³ − 2x + 2, x₀ = −2', 'x^3 - 2x + 2', -2]]), lw=460,
             items=['<b>Stationary point</b>: $f\'(x_n) = 0$, horizontal tangent, division by zero', '<b>Cycle</b>: $x^3 - 2x + 2$ from $x_0 = 0$ jumps $0 \\to 1 \\to 0 \\to 1 \\dots$ forever', '<b>Divergence</b>: $\\tan^{-1}x$ from $x_0 = 1.5$: $-1.69, 2.32, -5.11, 32.3 \\dots$', '<b>Double root</b> $(x-1)^2$: only linear, the error halves each step', 'Same cubic from $x_0 = -2$: converges in 4 steps to $-1.769292$'],
             notes="Go through the presets. For atan the tangents get flatter as |x| grows, so each jump is longer: classic divergence.\n\nFix: start closer (use a few bisection steps first), or use a safeguarded method that falls back to bisection when a Newton step leaves the bracket."),
        dict(type='profile', id='profile', title='Newton–Raphson: method profile',
             best=['Simple root, good start, cheap $f\'$: digits double; $x^3 - x - 2$ from 1.5 in <b>3</b> steps, $x^2 - 4x - 10$ from 5 in 4', 'Square roots, reciprocals and Kepler\'s equation: 3–6 steps to full precision', 'Extends directly to systems (L10) and optimisation (L25)'],
             worst=['Start near $f\'(x) = 0$: from $x_0 = 0.6$ the first step jumps to 30.4; 13 steps in total', 'Cycles ($x^3 - 2x + 2$ from 0) or divergence ($\\tan^{-1}x$ from 1.5)', 'Double root $(x - 1)^2$: only linear, the error just halves', 'No formula for $f\'$, or $f$ is noisy'],
             suited=['Smooth $f$ with an easy derivative, when a good starting value is known', 'Refining an estimate from bisection (hybrid methods)', 'Hardware: square root, division, inverse square root; ML: second-order optimisers'],
             avoid=['$f\'$ unavailable or expensive (use secant, L10)', 'No idea where the root is (bracket first)', 'Multiple roots, unless you use $x - m f/f\'$ with known multiplicity $m$'],
             verdict='Rule of thumb: <b>bracket first, then Newton</b>. Safety from bisection, speed from the tangent.',
             notes="Counts measured with the course code (stop when |x_{n+1} − x_n| < 1e-6). Modified Newton for a root of multiplicity m: x_{n+1} = x_n − m f(x_n)/f'(x_n) restores quadratic convergence; for (x − 1)² with m = 2 it lands on 1 in one step."),
        dict(type='table', id='compare', title='Comparative analysis: $x^3 - x - 2 = 0$ (root 1.521380)', kick='Comparison',
             head=['Method', 'Start', 'Iterations for $10^{-6}$', 'Evaluations', 'Order', 'Guaranteed?'], tx=(0, 5), frag=True,
             rows=[['Bisection', '$[1, 2]$', '20', '≈ 22 of $f$', '1 (rate ½)', 'yes'], ['False position', '$[1, 2]$', '12', '≈ 14 of $f$', '1', 'yes'], ['Fixed point, $g = (x+2)^{1/3}$', '1.5', '7', '7 of $g$', '1 (rate 0.14)', 'if $|g\'| < 1$'], ['<b>Newton</b>', '1.5', '<b>3</b>', '3 of $f$ + 3 of $f\'$', '<b>2</b>', 'no'], ['Newton from a poor start', '0.6', '13', '13 + 13', '2 (eventually)', 'no']],
             note='Kepler\'s equation, $e = 0.9$: fixed point 11 iterations, Newton 6. Newton wins on iterations, but each iteration costs two evaluations, and it needs a good start.', notefrag=True,
             notes="Point out the evaluations column: Newton's cost per iteration is f plus f'. When f' is as expensive as f, the fair comparison is 6 evaluations for Newton versus 7 for this good fixed-point g. Lecture 10 turns that observation into the efficiency index."),
        dict(type='bridge', id='bridge', lead='Newton is the fastest classical method near a simple root. Its weaknesses are exactly the topics that follow:',
             keep=['Quadratic convergence: digits double', 'One starting value, no bracket', 'Systematic: no guessing a $g$', 'Generalises to systems and to optimisation'],
             rows=[['Needs the derivative $f\'$', 'Replace the tangent by a secant through two recent points', 10],
                   ['May diverge or cycle from a poor start', 'Hybrid: keep a bracket and fall back to bisection (Brent)', 10],
                   ['Linear at multiple roots', 'Modified Newton $x - m\\,f/f\'$', None],
                   ['Several equations, several unknowns', 'Jacobian matrix and a linear solve per step', 10],
                   ['Finding a minimum instead of a root', 'Apply Newton to $f\'(x) = 0$ (Hessian in many dimensions)', 25]],
             notes="The last row is the bridge to machine learning: Newton's method for optimisation, compared with gradient descent in Lecture 25."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see the exact Newton step inside each system.',
             items=[
                 dict(ic='🖥️', h='Division in hardware', t='How chips compute 1/b',
                      detail=dict(where='floating-point division units in many processors and GPUs. A small table gives a first guess for $1/b$; then Newton steps on $f(x) = 1/x - b$ refine it using only multiplications.',
                                  eq='x_{n+1} = x_n\\,(2 - b\\,x_n)',
                                  table=[['$n$', '0', '1', '2', '3', '4'], [['$x_n$ for $b = 7$', '0.1', '0.13', '0.1417', '0.14284777', '0.14285714']]],
                                  note='The error squares each step: 2 or 3 steps from a table look-up give full single precision. Then a/b = a × (1/b).')),
                 dict(ic='🎮', h='Fast inverse square root', t='The famous trick in Quake III graphics',
                      detail=dict(where='normalising vectors for lighting: $1/\\sqrt{x}$ for millions of vectors per frame. A bit-level trick gives a rough guess $y_0$; one Newton step on $f(y) = 1/y^2 - x$ makes it accurate.',
                                  eq='y_1 = y_0\\left(1.5 - 0.5\\,x\\,y_0^2\\right)',
                                  steps=['Example $x = 2$, rough guess $y_0 = 0.7$', '$y_1 = 0.7\\,(1.5 - 0.5\\cdot 2\\cdot 0.49) = 0.707$', 'True value $1/\\sqrt2 = 0.7071068$: one step took the error from 1% to 0.015%'],
                                  note='No division and no square root: only multiplications. Modern CPUs have a hardware rsqrt estimate followed by exactly this Newton step.')),
                 dict(ic='🛰️', h='Kepler\'s equation, Newton style', t='Fast satellite positions',
                      detail=dict(where='orbit computation (GPS, satellite tracking): solve $f(E) = E - e\\sin E - M = 0$ with $f\'(E) = 1 - e\\cos E$.',
                                  table=[['eccentricity $e$', '0.1', '0.5', '0.9'], [['fixed point (L8)', '5', '6', '11'], ['Newton', '3', '4', '6']]],
                                  w='root', o=dict(method='newton', fixed=True, f='x - 0.9sin(x) - 1', a=1, height='220px', tableHeight='220px', side=True, dec=8),
                                  note='Iterations to 10⁻⁶ from E₀ = M = 1. Newton\'s advantage grows as the orbit becomes more elliptical.')),
                 dict(ic='📊', h='Logistic regression (IRLS)', t='Training a classifier with Newton steps',
                      detail=dict(where='statistics packages and scikit-learn\'s <code>newton-cg</code> solver. To maximise the log-likelihood, apply Newton to its gradient: each step solves a weighted least-squares problem (iteratively reweighted least squares).',
                                  eq='\\mathbf{w}_{k+1} = \\mathbf{w}_k - H^{-1}\\nabla \\ell(\\mathbf{w}_k), \\qquad H = X^T S X,; S = \\mathrm{diag}\\big(p_i(1-p_i)\\big)',
                                  note='Typically converges in under 10 iterations, where gradient descent may need thousands. The cost is solving a linear system with H each step (Lectures 11–13), and the idea is developed in Lecture 25.'))],
             notes="The Kepler card has a live Newton widget for e = 0.9. The hardware and Quake cards show that Newton's method is running in students' own laptops and GPUs."),
        dict(type='check', id='check', q='Newton\'s method for $f(x) = x^2 - 5$ starting from $x_0 = 2$. What is $x_1$?',
             opts=['2.5', '2.25', '2.2361', '1.75'], right=1,
             answer='B. $x_1 = 2 - \\dfrac{4 - 5}{4} = 2 + 0.25 = 2.25$. Next: $x_2 = 2.236111$, $x_3 = 2.236068 = \\sqrt5$.',
             notes="Same numbers as the Lecture 1 homework (Babylonian √5)."),
        dict(type='summary', id='summary', items=[
            '$x_{n+1} = x_n - f(x_n)/f\'(x_n)$: the tangent\'s crossing; from first-order Taylor',
            'Quadratic convergence near a simple root: $e_{n+1} \\approx \\frac{f\'\'}{2f\'}e_n^2$, digits double',
            'Square root, reciprocal and cube root algorithms are Newton\'s method',
            'Failures: $f\' \\approx 0$, cycles, divergence from poor $x_0$; only linear at multiple roots',
            'In practice: bracket first, then Newton, with safeguards'],
            hw=['Find the root of $x\\log_{10}x = 1.2$ by Newton\'s method starting at $x_0 = 2.5$, to 5 decimal places.', 'Derive the Newton iteration for $\\sqrt[3]{N}$ and compute $\\sqrt[3]{17}$ from $x_0 = 2.5$.', 'Find the positive root of $\\cos x = xe^{x}$ by Newton\'s method, 4 decimal places.', 'Lab: find a starting value for $x^3 - 2x + 2$ that leads to the cycle, and one that converges. Explain using the graph.'],
            solved='Newton on $f(x) = 1/x - 7$ gives $x_{n+1} = x_n - \\dfrac{1/x_n - 7}{-1/x_n^2} = x_n(2 - 7x_n)$: only multiplication. From 0.1: 0.13, 0.1417, 0.14284777, 0.14285714.',
            next='<b>Secant method and nonlinear systems.</b> Newton without derivatives, a comparison of all five methods, and Newton for several equations at once.',
            notes="Homework answers: Q1: f = x log10 x − 1.2, f' = log10 x + 0.434294; x1 = 2.746505, x2 = 2.740649, x3 = 2.740646. Q2: x1 = 2.573333, x2 = 2.571283, x3 = 2.571282. Q3: f = cos x − xe^x, f' = −sin x − e^x(1 + x); from 0.5: 0.518026, 0.517757, 0.517757 → 0.5178."),
    ],
    code={
        'newton': dict(file='newton_raphson', py='''# Newton-Raphson method for f(x) = 0
def f(x):
    return x**3 - x - 2

def df(x):
    return 3*x**2 - 1

x = 1.5            # starting value; try 0.6
tol = 1e-6
for n in range(1, 51):
    d = df(x)
    if d == 0:
        print("f'(x) = 0: horizontal tangent, choose another x0")
        break
    x_new = x - f(x) / d
    print(f"{n:2d}  x = {x_new:.10f}   f(x) = {f(x_new): .3e}   change = {abs(x_new - x):.2e}")
    if abs(x_new - x) < tol:
        break
    x = x_new
print(f"root = {x_new:.6f}")
''', c='''/* Newton-Raphson method for f(x) = 0 */
#include <stdio.h>
#include <math.h>
#define f(x)  ((x)*(x)*(x) - (x) - 2)
#define df(x) (3*(x)*(x) - 1)

int main(void) {
    double x = 1.5, x_new = x, tol = 1e-6;     /* try x = 0.6 */
    for (int n = 1; n <= 50; n++) {
        if (df(x) == 0) { printf("f'(x) = 0: choose another x0\\n"); return 1; }
        x_new = x - f(x) / df(x);
        printf("%2d  x = %.10f   f(x) = % .3e   change = %.2e\\n", n, x_new, f(x_new), fabs(x_new - x));
        if (fabs(x_new - x) < tol) break;
        x = x_new;
    }
    printf("root = %.6f\\n", x_new);
    return 0;
}
'''),
        'sqrtnewton': dict(file='newton_sqrt_reciprocal', py='''# Newton inside the computer: square root and reciprocal
N = 10.0
x = 3.0
print("sqrt(10):")
for n in range(4):
    x = 0.5 * (x + N / x)
    print(f"  {x:.12f}")

N = 7.0
y = 0.1                      # 1/7 using only multiplication
print("1/7 without dividing:")
for n in range(5):
    y = y * (2 - N * y)
    print(f"  {y:.12f}")
''', c='''#include <stdio.h>
int main(void) {
    double N = 10.0, x = 3.0;
    printf("sqrt(10):\\n");
    for (int n = 0; n < 4; n++) { x = 0.5 * (x + N / x); printf("  %.12f\\n", x); }
    double M = 7.0, y = 0.1;          /* 1/7 using only multiplication */
    printf("1/7 without dividing:\\n");
    for (int n = 0; n < 5; n++) { y = y * (2 - M * y); printf("  %.12f\\n", y); }
    return 0;
}
'''),
        'newtonfail': dict(file='newton_failures', py='''import math

def newton(f, df, x, steps=6):
    out = []
    for _ in range(steps):
        d = df(x)
        if d == 0:
            out.append("f'=0!")
            break
        x = x - f(x) / d
        out.append(round(x, 4))
    return out

print("cycle     :", newton(lambda x: x**3 - 2*x + 2, lambda x: 3*x*x - 2, 0.0))
print("flat      :", newton(lambda x: x*x - 1,       lambda x: 2*x,       0.0))
print("diverge   :", newton(math.atan,                lambda x: 1/(1+x*x), 1.5))
print("double    :", newton(lambda x: (x-1)**2,       lambda x: 2*(x-1),   2.0))
print("good start:", newton(lambda x: x**3 - 2*x + 2, lambda x: 3*x*x - 2, -2.0))
'''),
    },
    lab=dict(title='Newton–Raphson Lab',
             intro='Watch tangents converge, measure quadratic convergence, and explore the ways Newton can fail.',
             tabs=[
                 dict(name='Explore', blocks=[
                     dict(p='Each step draws the tangent at xₙ. Try the failure presets and a good start for comparison. The derivative f′(x) is computed for you and shown below the table.'),
                     dict(w='root', o=dict(method='newton', fixed=True, f='2x^3 - 2x - 5', a=1.5, height='330px', side=True, tableHeight='330px', dec=8,
                                            presets=[['2x³ − 2x − 5', '2x^3 - 2x - 5', 1.5], ['3x + sin x − eˣ', '3x + sin(x) - e^x', 0], ['x³ − 2x + 2 (cycle)', 'x^3 - 2x + 2', 0], ['atan x (diverge)', 'atan(x)', 1.5], ['(x − 1)² (slow)', '(x-1)^2', 2], ['x² − 10 (√10)', 'x^2 - 10', 3]]))]),
                 dict(name='Solver: your problem', blocks=[
                     dict(p='Type your equation and starting value. Switch methods to compare bisection, false position, Newton and secant on the same problem.'),
                     dict(w='root', o=dict(method='newton', f='x log10(x) - 1.2', a=2.5, b=3, height='300px', tableHeight='420px', dec=7))]),
                 dict(name='Code', blocks=[
                     dict(h='Newton–Raphson'), dict(code='newton', tasks=['Run it from 1.5, then from 0.6. How many iterations each?', 'Change f and df to 2x³ − 2x − 5 (Problem 1) and check the table.', 'Replace df by a central difference (f(x+h) − f(x−h))/(2h) with h = 1e-6. Does it still converge as fast?']),
                     dict(h='Square root and reciprocal'), dict(code='sqrtnewton', tasks=['Run it. How many correct digits after each step?', 'Change y = 0.1 to y = 0.3. What happens? (Hint: reciprocal iteration needs 0 < y₀ < 2/N.)']),
                     dict(h='Failure gallery'), dict(code='newtonfail', tasks=['Run it and match each line to a failure type.', 'Find a starting value for the cycle function that converges (try −1, −1.5).'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Derive the Newton–Raphson formula and explain its geometrical meaning.', 'The tangent at $(x_n, f(x_n))$ is $y = f(x_n) + f\'(x_n)(x - x_n)$. Setting $y = 0$: $x_{n+1} = x_n - f(x_n)/f\'(x_n)$. Geometrically, $x_{n+1}$ is where the tangent line meets the $x$-axis.'),
                         ('Find a root of $2x^3 - 2x - 5 = 0$ by Newton–Raphson.', 'Root in (1, 2). $x_0 = 1.5$: $x_1 = 1.608696$, $x_2 = 1.600645$, $x_3 = 1.600599$, $x_4 = 1.600599$. Root ≈ 1.600599.'),
                         ('Find $\\sqrt{12}$ by Newton\'s method from $x_0 = 3.5$, 6 decimal places.', '$x_{n+1} = \\tfrac12(x_n + 12/x_n)$: 3.464286, 3.464102, 3.464102.'),
                         ('Show that Newton\'s method for $f(x) = x^3 - 2x + 2$ from $x_0 = 0$ never converges.', '$f\'(x) = 3x^2 - 2$. $x_1 = 0 - 2/(-2) = 1$; $x_2 = 1 - 1/1 = 0$; so the iterates alternate 0, 1, 0, 1, … forever.'),
                         ('Why does Newton converge only linearly for $f(x) = (x-1)^2$?', '$f\'(1) = 0$ (double root). The iteration becomes $x_{n+1} = x_n - (x_n-1)/2$, so $e_{n+1} = e_n/2$: linear with rate ½. The quadratic error formula needs $f\'(r) \\ne 0$.'),
                         ('Give two advantages and two disadvantages of Newton–Raphson.', 'Advantages: quadratic convergence; one starting point and extends to systems. Disadvantages: needs $f\'(x)$; may diverge or cycle, and fails when $f\'(x) \\approx 0$.')])])]),
)
