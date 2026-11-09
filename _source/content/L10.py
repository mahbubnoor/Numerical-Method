LECTURE = dict(
    title='Secant Method and Nonlinear Systems',
    short='Secant Method and Nonlinear Systems',
    sub='Newton without derivatives, a final comparison of all five root-finding methods, and Newton\'s method for several equations at once: the idea behind GPS.',
    slides=[
        dict(type='cover', id='cover', notes="Recap question: 'What does Newton need that bisection does not?' (The derivative.) 'What if f is a black box, a simulation, or a measured curve, with no formula to differentiate?'\n\nToday: the secant method answers that. Then we compare all five methods and finish the module by solving two equations in two unknowns."),
        dict(type='bullets', id='hook', title='The problem: a function with no formula', kick='Why this lecture', rw=760,
             lead='The game designer from Lecture 6 asks: at what launch speed $v$ does the ball land after exactly 3 seconds?',
             items=['Define $T(v)$ = landing time for launch speed $v$. We need $T(v) - 3 = 0$', 'But $T(v)$ has no formula: every evaluation is a whole bisection run (Lecture 6)', 'So there is no derivative $T\'(v)$ for Newton, and each evaluation is expensive', 'We need a fast method that uses only values of the function'],
             frag=True,
             right=dict(table=[['$v$ (m/s)', '$T(v)$ (s)'], [['10', '2.7752'], ['15', '3.3912'], ['20', '4.0025']]]),
             notes="This is a realistic situation: f is the output of another algorithm (a simulation, a solver, a trained model). Ask: which of our methods can we use? Bisection (yes, slow), false position (yes), Newton (no derivative), fixed point (which g?). Today: secant. Solved at the end: v = 11.8267 m/s in 4 secant steps."),
        dict(type='goals', id='goals', items=[
            'Derive the <b>secant method</b> from Newton\'s method and from the chord', 'Carry out the secant method by hand and compare it with false position',
            'Compare all five methods: order, cost, safety; choose one for a given problem', 'Apply <b>Newton\'s method to systems</b> using the <b>Jacobian</b> matrix',
            'Choose the right root-finding method for a problem: best and worst cases of all five'],
            prev='Newton: $x_{n+1} = x_n - f(x_n)/f\'(x_n)$, quadratic, but needs $f\'$ and a good start.',
            today='Replace $f\'$ by a slope through two points (secant), then generalise Newton to vectors.',
            notes="This lecture closes Module 2."),
        dict(type='math', id='derive', title='The secant method',
             eqs=[dict(cap='Replace the derivative by a slope through the last two points', eq='f\'(x_n) \\approx \\frac{f(x_n) - f(x_{n-1})}{x_n - x_{n-1}}'),
                  dict(cap='Secant iteration', eq='x_{n+1} = x_n - f(x_n)\\,\\frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}', frag=True)],
             items=['Same formula as false position, but <b>no bracket</b>: always use the two most recent points', 'Needs two starting values $x_0$, $x_1$ (they need not bracket the root)', 'One new function evaluation per step (Newton needs $f$ and $f\'$)', 'Order $\\phi = \\frac{1 + \\sqrt5}{2} \\approx 1.618$: superlinear'],
             ifrag=True,
             notes="Emphasise the single difference from false position: false position keeps whichever old point gives a sign change; secant simply discards the oldest point. That loses the guarantee but removes the stuck-endpoint problem.\n\nThe golden-ratio order comes from the error relation e_{n+1} ≈ C e_n e_{n−1}; trying e_{n+1} ~ e_n^p gives p² = p + 1."),
        dict(type='bullets', id='algo', title='The secant algorithm', kick='The method, step by step', ordered=True, rw=780,
             items=['Choose two starting values $x_0$, $x_1$ near the root (they need not bracket it)', 'Compute $x_{n+1} = x_n - f(x_n)\\,\\dfrac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$', 'If $f(x_n) = f(x_{n-1})$ (flat secant), stop', 'Drop the oldest point: the pair $(x_{n-1}, x_n)$ becomes $(x_n, x_{n+1})$', 'Repeat until $|x_{n+1} - x_n| < \\varepsilon$; the answer is the last $x$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input f, x0, x1, tol, N\nf0 ← f(x0);  f1 ← f(x1)\nrepeat up to N times:\n    if f1 = f0: stop (flat secant)\n    x2 ← x1 − f1·(x1 − x0) / (f1 − f0)\n    if |x2 − x1| &lt; tol:\n        return x2\n    x0, f0 ← x1, f1\n    x1, f1 ← x2, f(x2)\nstop: no convergence</pre></div><p class="small" style="margin-top:14px">Step 4 is the only difference from false position: no sign test, just keep the newest two points.</p>'),
             notes='Compare line by line with false position: same formula, but the update keeps the two most recent points instead of the two that bracket the root.\n\nOne new f evaluation per step (f(x2)); the old value is reused.'),
        dict(type='widget', id='sw', title='Explore: secant lines', w='root', o=dict(method='secant', fixed=True, f='x^3 - x - 2', a=1, b=2, height='440px', side=True, tableHeight='440px', dec=8), lw=420,
             items=['The dashed line passes through the last two points', 'Its crossing is the next point; the oldest point is dropped', 'The first two steps equal false position; from step 3 the secant pulls ahead', 'Try $x_0 = 0$, $x_1 = 0.5$: both on the same side of the root'],
             notes="Step through. Steps 1–2 coincide with the false position table from Lecture 7 (1.333333, 1.462687), then secant jumps to 1.531169 (overshooting the root, which false position never does) and converges: 1.520926, 1.521376, 1.521380.\n\nWith starting points on the same side, false position could not even start; secant does not care."),
        dict(type='table', id='tab', title='Problem 1: $x^3 - x - 2 = 0$, $x_0 = 1$, $x_1 = 2$',
             head=['$n$', '$x_{n-1}$', '$x_n$', '$f(x_{n-1})$', '$f(x_n)$', '$x_{n+1}$', '$f(x_{n+1})$'], frag=True, ans=-1,
             rows=[[1, '1', '2', '−2', '4', '1.333333', '−0.962963'], [2, '2', '1.333333', '4', '−0.962963', '1.462687', '−0.333339'], [3, '1.333333', '1.462687', '−0.962963', '−0.333339', '1.531169', '+0.058626'],
                   [4, '1.462687', '1.531169', '−0.333339', '+0.058626', '1.520926', '−0.002693'], [5, '1.531169', '1.520926', '+0.058626', '−0.002693', '1.521376', '−0.000020'], [6, '1.520926', '1.521376', '−0.002693', '−0.000020', '1.521380', '0.000000']],
             note='Row 3 uses two points with $f < 0$: false position would never do that. Root 1.521380 after 6 steps (false position: 12 steps for the same accuracy).',
             notes="Check row 3: x = 1.462687 − (−0.333339)(1.462687 − 1.333333)/(−0.333339 + 0.962963) = 1.462687 + 0.333339 × 0.129354/0.629624 = 1.462687 + 0.068483 = 1.531170 (1.531169 with full precision)."),
        dict(type='bullets', id='order', title='How fast is "superlinear"?', rw=800,
             items=['Secant on $e^{x} - 3x$ from $0, 1$: errors $1.6\\times10^{-1}$, $1.2\\times10^{-1}$, $1.7\\times10^{-2}$, $1.5\\times10^{-3}$, $2.1\\times10^{-5}$, $2.6\\times10^{-8}$, $4.4\\times10^{-13}$',
                    'Each error ≈ (previous)<sup>1.6</sup>: between linear (×constant) and quadratic (squared)',
                    '<b>Efficiency per function evaluation</b>: Newton gains order 2 per 2 evaluations ($\\sqrt2 = 1.41$ per evaluation); secant gains 1.618 per evaluation',
                    'So when $f\'$ costs as much as $f$, <b>secant is often faster than Newton</b> in practice'],
             frag=True,
             right=dict(w='race', o=dict(f='x^3 - x - 2', a=1, b=2, height='420px')),
             notes="The race widget plots log|error| against iteration for all four methods on the same problem: bisection is a straight line (linear), false position a shallower or similar line, secant and Newton curve down steeply."),
        dict(type='math', id='sys', title='Systems: Newton\'s method in two variables',
             lead='Solve $f_1(x, y) = 0$, $f_2(x, y) = 0$ simultaneously. Linearise both with Taylor series:',
             eqs=[dict(cap='Jacobian matrix', eq='J = \\begin{pmatrix} \\partial f_1/\\partial x & \\partial f_1/\\partial y \\\\ \\partial f_2/\\partial x & \\partial f_2/\\partial y \\end{pmatrix}'),
                  dict(cap='Newton step', eq='J(\\mathbf{x}_n)\\,\\Delta = -\\mathbf{F}(\\mathbf{x}_n), \\qquad \\mathbf{x}_{n+1} = \\mathbf{x}_n + \\Delta', frag=True)],
             items=['One-variable Newton: divide by $f\'$. Many variables: <b>solve a linear system</b> with $J$', 'For 2×2, solve $J\\Delta = -F$ with the school formula (Cramer\'s rule); larger systems: Lectures 11–14', 'Still quadratic near a solution where $\\det J \\ne 0$', 'For $n$ unknowns, each step costs an $n\\times n$ solve (Lectures 11–14)'],
             ifrag=True,
             notes="The structure is identical to one variable: f(x + Δ) ≈ f(x) + J Δ = 0. The derivative becomes the Jacobian, the division becomes a linear solve.\n\nThis links Module 2 (nonlinear equations) to Module 3 (linear systems): every Newton step for a system is a linear system."),
        dict(type='bullets', id='algo2', title='Newton for systems, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Write $\\mathbf{F} = (f_1, f_2)$ and the Jacobian $J$ (four partial derivatives)', 'Choose a starting guess $(x_0, y_0)$', 'Evaluate $\\mathbf{F}$ and $J$ at the current point', "Solve the linear system $J\\,\\Delta = -\\mathbf{F}$ (2×2: Cramer's rule)", 'Update $\\mathbf{x}_{n+1} = \\mathbf{x}_n + \\Delta$', 'Repeat until $\\|\\Delta\\| < \\varepsilon$; the answer is the last $\\mathbf{x}$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input F, J, x0, tol, N\nx ← x0\nrepeat up to N times:\n    solve J(x)·Δ = −F(x)\n    x ← x + Δ\n    if ‖Δ‖ &lt; tol:\n        return x\nstop: no convergence</pre></div><p class="small" style="margin-top:14px">Same loop as one-variable Newton; "divide by $f\'$" became "solve with $J$" (step 4).</p>'),
             notes='Point at step 4: this is where Module 3 enters. For 2 unknowns Cramer is fine; for 100 unknowns step 4 needs Gaussian elimination or LU (Lectures 12–13).\n\nThe next slide carries out steps 3–5 once by hand.'),
        dict(type='worked', id='syswork', title='Problem 2: one Newton step for $x^2 + y^2 = 4$, $xy = 1$',
             q='Start from $(x_0, y_0) = (2, 0.5)$. Do one Newton step.',
             steps=['$F = \\begin{pmatrix} x^2 + y^2 - 4 \\\\ xy - 1 \\end{pmatrix} = \\begin{pmatrix} 0.25 \\\\ 0 \\end{pmatrix}$, $\\quad J = \\begin{pmatrix} 2x & 2y \\\\ y & x \\end{pmatrix} = \\begin{pmatrix} 4 & 1 \\\\ 0.5 & 2 \\end{pmatrix}$',
                    'Solve $\\begin{pmatrix} 4 & 1 \\\\ 0.5 & 2 \\end{pmatrix}\\begin{pmatrix} \\Delta x \\\\ \\Delta y\\end{pmatrix} = \\begin{pmatrix} -0.25 \\\\ 0 \\end{pmatrix}$; $\\det J = 8 - 0.5 = 7.5$',
                    'Cramer: $\\Delta x = \\dfrac{(-0.25)(2) - (1)(0)}{7.5} = -0.066667$, $\\;\\Delta y = \\dfrac{(4)(0) - (0.5)(-0.25)}{7.5} = 0.016667$',
                    '$(x_1, y_1) = (1.933333, 0.516667)$; two more steps give $\\left(\\sqrt{2+\\sqrt3}, \\sqrt{2-\\sqrt3}\\right)$'],
             answer='Solution $(1.931852, 0.517638)$ in three steps: quadratic convergence again.',
             right=dict(w='newton2d', o=dict(f1='x^2 + y^2 - 4', f2='x y - 1', x0=2, y0=0.5, height='300px', range=[-3, 3, -3, 3])), rw=760,
             notes="The widget on the right shows the circle and the hyperbola; they meet in four points. Change the start to (−2, −0.5) or (0.5, 2) to reach the other solutions: which solution Newton finds depends on the start, just as in one variable."),
        dict(type='compare', id='classic', title='Same system, two approaches: $x^2 + y^2 = 4$, $xy = 1$', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (exact formula)', tag='Algebra', cls='blue', items=['Substitute $y = 1/x$: $x^2 + 1/x^2 = 4 \\Rightarrow x^4 - 4x^2 + 1 = 0$', 'Quadratic in $x^2$: $x^2 = 2 \\pm \\sqrt3$', '$(x, y) = \\left(\\sqrt{2+\\sqrt3}, \\sqrt{2-\\sqrt3}\\right) = (1.931852, 0.517638)$']),
             right=dict(h='Numerical (Newton for systems)', tag='Algorithm', cls='key', items=['Jacobian $\\begin{pmatrix} 2x & 2y \\\\ y & x\\end{pmatrix}$, start $(2, 0.5)$', '3 iterations: $(1.931852, 0.517638)$', 'No substitution trick needed: the same code works for any 2×2 system']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>Landing time $T(v) = 3$: a function with no formula</h3><p>Each value of $T(v)$ comes from running bisection; there is nothing to substitute or rearrange. Secant: $v = 11.8267$ m/s in 4 steps. Most real systems (circuits, GPS, robots) are like this: many equations, no substitution trick.</p></div>'),
             notes='The substitution trick works because the system is tiny and has special structure. With 3 or more nonlinear equations (GPS has 4) such tricks almost never exist.'),
        dict(type='code', id='code', title='Newton for systems in Python and C', code='newtonsys', lw=560,
             items=['Each step: evaluate $F$ and $J$, solve the 2×2 system by Cramer\'s rule', 'Stop when the step $\\|\\Delta\\|$ is tiny', 'Try the start $(0.5, 2)$: a different solution', 'Change to $x^2 + y = 11$, $x + y^2 = 7$ from $(3.5, 1.5)$: converges to $(3, 2)$'],
             notes="Run both. For larger systems we replace Cramer by Gaussian elimination (Lecture 12); NumPy users write np.linalg.solve(J, -F).\n\nThe second system (Himmelblau's function) has four solutions; (3, 2) is the integer one."),
        dict(type='exam', id='practice', src='Problem 3',
             q='"Explain how the Secant method removes the requirement of an analytical derivative and identify one drawback it introduces in exchange." Also: compare the iteration methods for solving $f(x) = 0$.',
             tips=['Secant replaces $f\'(x_n)$ by the finite-difference slope $\\dfrac{f(x_n) - f(x_{n-1})}{x_n - x_{n-1}}$ through the last two iterates', 'Drawbacks (any one): needs two starting values; order drops from 2 to 1.618; no bracket, so it can diverge; $f(x_n) \\approx f(x_{n-1})$ causes division by a tiny number',
                   'Comparison: use the five-row table (needs, order, cost, guarantee)', 'Mention the efficiency index: per function evaluation, secant (1.618) beats Newton (1.414)'],
             notes=""),
        dict(type='widget', id='fail', title='When the secant method fails', w='root', o=dict(method='secant', fixed=True, f='atan(x)', a=2, b=3, height='400px', side=True, tableHeight='400px', dec=4,
             presets=[['divergence: atan x from 2, 3', 'atan(x)', 2, 3], ['flat secant: cos x from −1, 1', 'cos(x)', -1, 1], ['wandering: x³ − 2x + 2 from 0, 0.5', 'x^3 - 2x + 2', 0, 0.5], ['good start: x³ − x − 2 from 1, 2', 'x^3 - x - 2', 1, 2]]), lw=460,
             items=['<b>Divergence</b>: $\\tan^{-1}x$ from 2, 3 jumps to −5.80, −1.15, 6.15, … 38.6', '<b>Flat secant</b>: $\\cos(-1) = \\cos(1)$, the line is horizontal: division by zero', '<b>Wandering</b>: $x^3 - 2x + 2$ from 0, 0.5 jumps around for many steps before settling', 'No bracket means no guarantee: same weakness as Newton'],
             notes="Try each preset. The flat-secant case is the secant version of Newton's horizontal tangent. In practice secant steps are used inside a bracket (Brent's method) so that a bad step is replaced by a bisection step."),
        dict(type='profile', id='profile', title='Secant method: method profile',
             best=['Smooth $f$, two good starting values: superlinear, order 1.618; $x^3 - x - 2$ in 7 steps', '<b>Expensive $f$ with no derivative</b>: one evaluation per step, the most efficient per evaluation', 'The ball problem: 4 steps, each a full simulation'],
             worst=['$f(x_n) \\approx f(x_{n-1})$: a nearly flat secant throws the next point far away', 'Poor starting values: divergence ($\\tan^{-1}x$ from 2, 3)', 'Cancellation in $f(x_n) - f(x_{n-1})$ near convergence limits the final accuracy slightly'],
             suited=['Black-box functions: simulations, measurements, outputs of other solvers', 'Inside hybrid solvers (Brent\'s method, <code>scipy.optimize.brentq</code>)', 'When $f\'$ costs as much as $f$'],
             avoid=['A guaranteed result is needed (bracket it, or use Brent)', 'The function is noisy (secant slopes amplify noise; use bisection)', 'A cheap derivative is available and starts are good (Newton is slightly faster per iteration)'],
             verdict='Rule of thumb: <b>no derivative → secant; no guarantee needed → plain; guarantee needed → Brent</b> (bracket + secant + bisection).',
             notes="Efficiency index: order^(1/evaluations per step). Newton: 2^(1/2) = 1.414. Secant: 1.618^(1/1) = 1.618. Bisection: 2^(1/1) in error-halving terms but only linear."),
        dict(type='table', id='compare', title='All five methods side by side', cls='tb sm',
             head=['Method', 'Needs', 'Order', 'Per step', 'Guaranteed?', 'Iterations for $x^3 - x - 2$, $10^{-6}$'], tx=(0, 1, 4), frag=True,
             rows=[['Bisection', 'bracket', '1 (rate ½)', '1 eval', '<span class="gr">yes</span>', '20 from [1, 2]'], ['False position', 'bracket', '1 (often fast)', '1 eval', '<span class="gr">yes</span> (can be slow)', '12 from [1, 2]'],
                   ['Fixed point', '$x = g(x)$, $x_0$', '1 (rate $|g\'(r)|$)', '1 eval', 'only if $|g\'| < 1$', '7 with $g = (x+2)^{1/3}$'], ['Newton–Raphson', "$f'$, $x_0$", '2', '2 evals', 'no (needs good $x_0$)', '3 from 1.5'],
                   ['Secant', '$x_0$, $x_1$', '1.618', '1 eval', 'no', '7 from 1, 2']],
             note='Practical choice: bracketing when safety matters or $f$ is noisy; Newton when $f\'$ is cheap and $x_0$ is good; secant when $f\'$ is unavailable. Libraries (e.g. Brent\'s method, <code>scipy.optimize.brentq</code>) combine bisection\'s safety with secant-like speed.', notefrag=True,
             notes="All iteration counts were computed with the lab code, stopping when successive estimates differ by less than 1e-6 (bisection: error bound below 1e-6)."),
        dict(type='bridge', id='bridge', title='End of Module 2: what is still missing', lead='We can now solve any single equation, and small systems. Large systems need new tools:',
             keep=['Five root-finding methods with known best and worst cases', 'Hybrid strategy: bracket, then a fast method', 'Newton for systems: linearise, solve, repeat', 'Convergence orders 1, 1.618 and 2'],
             rows=[['Each Newton step for $n$ equations needs an $n\\times n$ linear solve', 'Gaussian elimination, LU and Cholesky', 12],
                   ['Cramer\'s rule is far too slow beyond 3×3', 'Cost analysis of Cramer and the inverse', 11],
                   ['Huge sparse systems (millions of unknowns)', 'Iterative methods: Jacobi, Gauss–Seidel (fixed point with matrices)', 14],
                   ['Finding the best parameters for data, not a root', 'Least squares, then optimisation for ML', 23]],
             notes="This slide closes the module and opens Module 3: every nonlinear solver for systems spends most of its time solving linear systems."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see Newton\'s method for systems, or the secant idea, inside a real system.',
             items=[
                 dict(ic='📍', h='Positioning from distances (GPS idea)', t='Where am I, given distances to known beacons?',
                      detail=dict(where='positioning. Each measured distance gives one nonlinear equation; GPS uses 4 satellites for $(x, y, z)$ and the clock error. Here is the 2-D version with two beacons.',
                                  eq='x^2 + y^2 = 25 ;;(\\text{beacon at } (0,0)),\\qquad (x-6)^2 + y^2 = 25 ;;(\\text{beacon at } (6,0))',
                                  w='newton2d', o=dict(f1='x^2 + y^2 - 25', f2='(x-6)^2 + y^2 - 25', x0=2, y0=2, height='260px', side=True, range=[-2, 8, -3, 7]),
                                  note='From the guess (2, 2): (3, 5.25), (3, 4.1488), (3, 4.0027) → (3, 4). Real receivers do this with 4 unknowns at every position update.')),
                 dict(ic='🤖', h='Robot arm: inverse kinematics', t='Which joint angles put the hand at a target?',
                      detail=dict(where='robot control. A two-link arm with unit links reaches $(1.2, 0.8)$ when the shoulder angle $x$ and elbow angle $y$ satisfy two trigonometric equations.',
                                  eq='\\cos x + \\cos(x+y) = 1.2,\\qquad \\sin x + \\sin(x+y) = 0.8',
                                  w='newton2d', o=dict(f1='cos(x) + cos(x+y) - 1.2', f2='sin(x) + sin(x+y) - 0.8', x0=0.3, y0=1.0, height='260px', side=True, range=[-1.5, 2.5, -0.5, 3]),
                                  note='From (0.3, 1.0) Newton converges to x = −0.1774 rad (−10.2°), y = 1.5308 rad (87.7°). The other crossing is the "elbow-down" solution.')),
                 dict(ic='🐍', h='SciPy brentq', t='Secant steps with a safety net',
                      detail=dict(where='<code>scipy.optimize.brentq</code>, the default bracketed root finder in Python. It mixes secant (and inverse quadratic) steps with bisection.',
                                  steps=['Keep a bracket $[a, b]$ with a sign change (Lecture 6)', 'Try a secant step from the two latest points (today)', 'Reject it if it leaves the bracket or shrinks too slowly; take a bisection step instead', 'Result: guaranteed like bisection, usually superlinear like secant'],
                                  note='This combination is exactly the "rule of thumb" from the profile slides of Lectures 6–10.')),
                 dict(ic='⚡', h='Circuit simulation (SPICE)', t='Solving a circuit with diodes and transistors',
                      detail=dict(where='every analogue circuit simulator. Kirchhoff\'s current law at each node gives one equation; diodes make them nonlinear ($I = I_s(e^{V/V_T} - 1)$).',
                                  steps=['Unknowns: the node voltages; equations: currents sum to zero at each node', 'Newton: linearise each diode around the current voltages (its Jacobian entry is the diode conductance)', 'Solve the linear system, update voltages, repeat until the currents balance', 'Repeated at every time step of a transient simulation'],
                                  note='Large circuits mean large sparse Jacobians: the linear algebra of Lectures 11–14 is where the time goes.'))],
             notes="The positioning and robot cards have live 2-D Newton widgets. Click Next step in the pop-up to show convergence."),
        dict(type='check', id='check', q='Secant method with $x_0 = 1$, $x_1 = 2$ for $f(x) = x^2 - 3$. What is $x_2$?',
             opts=['1.5', '1.6667', '1.7321', '1.75'], right=1,
             answer='B. $f(1) = -2$, $f(2) = 1$: $x_2 = 2 - 1\\cdot\\dfrac{2 - 1}{1 - (-2)} = 2 - \\tfrac13 = 1.6667$. Then $x_3 = 1.7273$, $x_4 = 1.7321 = \\sqrt3$.',
             notes="Point out that x2 equals the false position value here (the first step of both methods is identical)."),
        dict(type='summary', id='summary', items=[
            'Secant: $x_{n+1} = x_n - f(x_n)\\dfrac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$; no derivative, order 1.618',
            'Like false position but uses the latest two points: faster, not guaranteed',
            'Choose: bracketing for safety; Newton when $f\'$ is cheap; secant otherwise; hybrids in libraries',
            'Systems: solve $J\\Delta = -F$ each step; quadratic near a solution with $\\det J \\ne 0$'],
            hw=['Solve $x^3 - 5x + 1 = 0$ by the secant method with $x_0 = 0$, $x_1 = 1$, to 5 decimal places.', 'Do two Newton steps for $x^2 + y = 11$, $x + y^2 = 7$ from $(3.5, 1.5)$ by hand.', 'Modify the secant program to stop when $|f(x_n)| < 10^{-10}$ and count evaluations. Compare with Newton.', 'Write a one-page comparison of the five root-finding methods (use the table and your own examples).'],
            solved='Secant on $T(v) - 3$ from $v = 10, 20$: 11.8317, 11.8267, 11.826709 m/s. Four steps, each a full bisection run inside; no derivative was needed.',
            next='<b>Module 3: systems of linear equations.</b> $A\\mathbf{x} = \\mathbf{b}$ with Cramer\'s rule and the inverse, and why both are too slow for real problems.',
            notes="Homework answers: Q1: f(0) = 1, f(1) = −3; x2 = 0.25, x3 = 0.186441, x4 = 0.201736, x5 = 0.201640, x6 = 0.201640 → 0.20164. Q2: step 1: F = (2.75, −1.25), J = [[7, 1], [1, 3]], det = 20, Δ = (−0.475, 0.575), giving (3.025, 2.075); step 2: (2.999874, 2.001386)."),
    ],
    code={
        'secant': dict(file='secant', py='''# Secant method for f(x) = 0
def f(x):
    return x**3 - x - 2

x0, x1 = 1.0, 2.0
tol = 1e-6
for n in range(1, 51):
    f0, f1 = f(x0), f(x1)
    if f1 == f0:
        print("f(x1) = f(x0): secant line is horizontal")
        break
    x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
    print(f"{n:2d}  x = {x2:.10f}   f(x) = {f(x2): .3e}")
    if abs(x2 - x1) < tol:
        break
    x0, x1 = x1, x2
print(f"root = {x2:.6f}")
''', c='''/* Secant method for f(x) = 0 */
#include <stdio.h>
#include <math.h>

double f(double x) { return x * x * x - x - 2; }

int main(void) {
    double x0 = 1.0, x1 = 2.0, x2 = x1, tol = 1e-6;
    for (int n = 1; n <= 50; n++) {
        double f0 = f(x0), f1 = f(x1);
        if (f1 == f0) { printf("f(x1) = f(x0): secant line is horizontal\\n"); return 1; }
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0);
        printf("%2d  x = %.10f   f(x) = % .3e\\n", n, x2, f(x2));
        if (fabs(x2 - x1) < tol) break;
        x0 = x1; x1 = x2;
    }
    printf("root = %.6f\\n", x2);
    return 0;
}
'''),
        'newtonsys': dict(file='newton_system', py='''# Newton's method for the system  x^2 + y^2 = 4,  x*y = 1
def F(x, y):
    return x*x + y*y - 4, x*y - 1

def J(x, y):                     # Jacobian [[df1/dx, df1/dy], [df2/dx, df2/dy]]
    return 2*x, 2*y, y, x

x, y = 2.0, 0.5
for n in range(1, 21):
    f1, f2 = F(x, y)
    a, b, c, d = J(x, y)
    det = a*d - b*c
    dx = (-f1*d + f2*b) / det    # Cramer's rule for J * delta = -F
    dy = (-f2*a + f1*c) / det
    x, y = x + dx, y + dy
    print(f"{n:2d}  x = {x:.10f}  y = {y:.10f}  step = {abs(dx) + abs(dy):.2e}")
    if abs(dx) + abs(dy) < 1e-10:
        break
''', c='''/* Newton's method for the system  x^2 + y^2 = 4,  x*y = 1 */
#include <stdio.h>
#include <math.h>

int main(void) {
    double x = 2.0, y = 0.5;
    for (int n = 1; n <= 20; n++) {
        double f1 = x*x + y*y - 4, f2 = x*y - 1;
        double a = 2*x, b = 2*y, c = y, d = x;     /* Jacobian */
        double det = a*d - b*c;
        double dx = (-f1*d + f2*b) / det;          /* Cramer's rule */
        double dy = (-f2*a + f1*c) / det;
        x += dx; y += dy;
        printf("%2d  x = %.10f  y = %.10f  step = %.2e\\n", n, x, y, fabs(dx) + fabs(dy));
        if (fabs(dx) + fabs(dy) < 1e-10) break;
    }
    return 0;
}
'''),
        'allmethods': dict(file='compare_root_methods', py='''import math

def f(x):  return x**3 - x - 2
def df(x): return 3*x*x - 1

def bisection(a, b, tol=1e-6):
    n = 0
    while (b - a) / 2 >= tol:
        n += 1
        c = (a + b) / 2
        if f(a) * f(c) < 0: b = c
        else: a = c
    return (a + b) / 2, n + 1

def false_position(a, b, tol=1e-6):
    prev = None
    for n in range(1, 500):
        c = (a*f(b) - b*f(a)) / (f(b) - f(a))
        if prev is not None and abs(c - prev) < tol: return c, n
        if f(a) * f(c) < 0: b = c
        else: a = c
        prev = c

def newton(x, tol=1e-6):
    for n in range(1, 100):
        x_new = x - f(x) / df(x)
        if abs(x_new - x) < tol: return x_new, n
        x = x_new

def secant(x0, x1, tol=1e-6):
    for n in range(1, 100):
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        if abs(x2 - x1) < tol: return x2, n
        x0, x1 = x1, x2

for name, (r, n) in [("bisection", bisection(1, 2)), ("false position", false_position(1, 2)),
                     ("Newton (x0=1.5)", newton(1.5)), ("secant (1, 2)", secant(1.0, 2.0))]:
    print(f"{name:16s} root = {r:.8f}  iterations = {n}")
'''),
    },
    lab=dict(title='Secant and Systems Lab',
             intro='Race the root-finding methods, try the secant method on your own problems, and solve two equations with Newton\'s method.',
             tabs=[
                 dict(name='Method race', blocks=[
                     dict(p='All four methods on the same equation: log of the error against the iteration number. Straight lines are linear convergence; curves bending down are superlinear or quadratic.'),
                     dict(w='race', o=dict(f='x^3 - x - 2', a=1, b=2, height='320px'))]),
                 dict(name='Secant explorer', blocks=[
                     dict(w='root', o=dict(method='secant', fixed=True, f='e^x - 3x', a=0, b=1, height='330px', side=True, tableHeight='330px', dec=8,
                                            presets=[['x³ − x − 2', 'x^3 - x - 2', 1, 2], ['eˣ − 3x', 'e^x - 3x', 0, 1], ['x³ − 5x + 1', 'x^3 - 5x + 1', 0, 1], ['x² − 3', 'x^2 - 3', 1, 2]]))]),
                 dict(name='Newton for systems', blocks=[
                     dict(p='Blue and green curves are f₁ = 0 and f₂ = 0; their crossings are the solutions. Change the starting point to reach a different solution.'),
                     dict(w='newton2d', o=dict(f1='x^2 + y^2 - 4', f2='x y - 1', x0=2, y0=0.5, height='380px', side=True, range=[-3, 3, -3, 3]))]),
                 dict(name='Code', blocks=[
                     dict(h='Secant'), dict(code='secant', tasks=['Run it. Compare with the table on slide 7.', 'Start from x0 = 0, x1 = 0.5 (same side of the root). Does it still converge?', 'Count function evaluations and compare with Newton.']),
                     dict(h='All methods'), dict(code='allmethods', tasks=['Run it. Which method needs the fewest iterations? The fewest function evaluations?', 'Change f to e^x − 3x (and df) with bracket [0, 1] and Newton start 0.5.']),
                     dict(h='Newton for systems'), dict(code='newtonsys', tasks=['Run it. How many steps to 1e-10?', 'Start from (0.5, 2). Which solution do you get?', 'Change to x² + y = 11, x + y² = 7 from (3.5, 1.5).'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Derive the secant formula from Newton\'s formula.', 'Replace $f\'(x_n)$ by $\\frac{f(x_n) - f(x_{n-1})}{x_n - x_{n-1}}$ in $x_{n+1} = x_n - f(x_n)/f\'(x_n)$, giving $x_{n+1} = x_n - f(x_n)\\frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$.'),
                         ('Find the root of $e^{x} - 3x = 0$ near 0.6 by the secant method with $x_0 = 0$, $x_1 = 1$.', '$x_2 = 0.780203$, $x_3 = 0.496679$, $x_4 = 0.635952$, $x_5 = 0.620560$, $x_6 = 0.619040$, $x_7 = 0.619061$. Root ≈ 0.619061.'),
                         ('Distinguish the secant method from false position.', 'Both use the chord formula. False position keeps the pair of points that brackets the root (always converges, may stall); secant always uses the two latest points (no bracket, faster, may diverge).'),
                         ('Write the Newton iteration for the system $f_1 = x^2 - y - 1 = 0$, $f_2 = x - y^2 + 1 = 0$.', '$J = \\begin{pmatrix} 2x & -1 \\\\ 1 & -2y\\end{pmatrix}$. Solve $J\\Delta = -\\begin{pmatrix} f_1 \\\\ f_2\\end{pmatrix}$ and set $(x, y) \\leftarrow (x, y) + \\Delta$.'),
                         ('Which method would you choose, and why: (a) $f$ is a noisy measurement; (b) $f$ is a polynomial with an easy derivative and a good guess is known; (c) $f$ comes from a slow simulation with no derivative?', '(a) Bisection: needs only signs, robust to noise. (b) Newton: quadratic, $f\'$ cheap. (c) Secant (or Brent): no derivative, one evaluation per step, superlinear.')])])]),
)
