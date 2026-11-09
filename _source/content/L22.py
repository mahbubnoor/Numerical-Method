STIFF_EXACT = '(2500*cos(x) + 50*sin(x))/2501 - 2500/2501*e^(-50*x)'

LECTURE = dict(
    title='ODEs II: Runge–Kutta and Predictor–Corrector Methods',
    short='ODEs II: Runge–Kutta, Milne, Adams',
    sub='Fourth-order accuracy from values of $f$ alone (Runge–Kutta), reusing past slopes (Milne and Adams–Bashforth–Moulton), systems of equations, and the stability limits that decide which method survives a stiff problem.',
    slides=[
        dict(type='cover', id='cover', notes="Recap: 'Euler for y' = x + y with h = 0.1 is off by 0.25 at x = 1, Heun by 0.008. How small must h be for six digits?' (Euler: about 10⁻⁷, ten million steps.) Today: RK4 does it with h = 0.1."),
        dict(type='bullets', id='hook', title='The problem: a spring that must not gain energy', kick='Why this lecture', rw=640,
             lead='A mass on a spring: position $x$, velocity $y$. Without friction it should oscillate for ever with the same energy $x^2 + y^2 = 1$.',
             items=['Equations: $x\' = y$, $\\;y\' = -x$, start $(1, 0)$: two unknowns, a <b>system</b>', 'Euler, $h = 0.1$, ten periods: energy grows from 1 to <b>517</b>; the mass flies off', 'Heun: 1.016 (better, still drifting)',
                    'Orbits, circuits, molecules and epidemics need methods that stay accurate over thousands of steps'],
             frag=True,
             right=dict(table=[['method ($h = 0.1$)', 'energy after 10 periods'], [['exact', '1'], ['Euler', '517.4'], ['Heun', '1.0158'], ['RK4', '?']]]),
             notes="Euler multiplies x² + y² by exactly 1 + h² = 1.01 every step: 1.01^628 = 517. Solved at the end: RK4 gives 0.999991."),
        dict(type='goals', id='goals', items=[
            'Derive the idea of <b>Runge–Kutta</b> methods and apply <b>RK4</b> by hand and in code',
            'Solve <b>systems</b> and second-order equations by the same methods',
            'Apply <b>Milne\'s</b> and <b>Adams–Bashforth–Moulton</b> predictor–corrector methods',
            'Explain <b>stability</b>, stiff equations and why implicit methods exist',
            'Choose a solver for a given problem'],
            prev='Euler (order 1) and Heun (order 2); instability when $h$ is too large.',
            today='Higher order with more slopes per step, or with slopes from earlier steps.',
            notes="Last lecture of Module 6."),
        dict(type='math', id='rk2', title='The Runge–Kutta idea: average several slopes inside the step',
             eqs=[dict(cap='Second order: two slopes, weights chosen to match Taylor up to h²', eq='\\begin{aligned} k_1 &= hf(x_n, y_n), \\qquad k_2 = hf(x_n + ah,\\, y_n + ak_1) \\\\ y_{n+1} &= y_n + \\Big(1 - \\tfrac{1}{2a}\\Big)k_1 + \\tfrac{1}{2a}k_2 \\end{aligned}'),
                  dict(cap='Two members of the family', eq='\\begin{aligned} a = 1:&\\;\\; y_{n+1} = y_n + \\tfrac12(k_1 + k_2) \\;\\;(\\text{Heun}) \\\\ a = \\tfrac12:&\\;\\; y_{n+1} = y_n + k_2 \\;\\;(\\text{midpoint}) \\end{aligned}', frag=True)],
             items=['Same accuracy as the Taylor method of order 2, but <b>no derivatives of $f$</b>', 'Each $k$ is a trial slope × $h$; later slopes use earlier ones', 'Matching more Taylor terms needs more slopes: four slopes give order 4', 'Heun from Lecture 21 is RK2'],
             ifrag=True, rw=580,
             notes="Derivation sketch: expand k2 in a Taylor series in two variables and compare with y + hy' + (h²/2)y''. The condition is w1 + w2 = 1, w2·a = 1/2, which leaves one free parameter a."),
        dict(type='math', id='rk4', title='The classical fourth-order Runge–Kutta method (RK4)',
             eqs=[dict(cap='Four slopes per step', eq='\\begin{aligned} k_1 &= hf(x_n, y_n) & k_2 &= hf\\big(x_n + \\tfrac h2,\\, y_n + \\tfrac{k_1}{2}\\big) \\\\ k_3 &= hf\\big(x_n + \\tfrac h2,\\, y_n + \\tfrac{k_2}{2}\\big) & k_4 &= hf(x_n + h,\\, y_n + k_3) \\end{aligned}'),
                  dict(cap='Weighted average: weights 1, 2, 2, 1', eq='y_{n+1} = y_n + \\tfrac16\\big(k_1 + 2k_2 + 2k_3 + k_4\\big), \\qquad \\text{global error } O(h^4)', frag=True)],
             items=['Slopes at the start, twice at the middle, at the end', 'Weights 1, 2, 2, 1 = Simpson\'s 1, 4, 1 with the middle split in two (Lecture 20)', 'Halve $h$: error $\\div 16$', 'Four evaluations per step, but huge steps are allowed: the workhorse of scientific computing'],
             ifrag=True, rw=600,
             notes="If f depends on x only, RK4 reduces exactly to Simpson's rule on [x_n, x_n + h]. That is the cleanest way to remember the weights."),
        dict(type='bullets', id='algo', title='RK4, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['$k_1 = h\\,f(x_n, y_n)$: slope at the start', '$k_2 = h\\,f(x_n + h/2,\\; y_n + k_1/2)$: midpoint, using $k_1$', '$k_3 = h\\,f(x_n + h/2,\\; y_n + k_2/2)$: midpoint again, using $k_2$', '$k_4 = h\\,f(x_n + h,\\; y_n + k_3)$: end point, using $k_3$',
                    '$y_{n+1} = y_n + (k_1 + 2k_2 + 2k_3 + k_4)/6$; $\\;x_{n+1} = x_n + h$; repeat'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input f, x0, y0, h, x_end\nx ← x0;  y ← y0\nwhile x &lt; x_end − h/2:\n    k1 ← h·f(x, y)\n    k2 ← h·f(x + h/2, y + k1/2)\n    k3 ← h·f(x + h/2, y + k2/2)\n    k4 ← h·f(x + h, y + k3)\n    y ← y + (k1 + 2k2 + 2k3 + k4)/6\n    x ← x + h\nreturn y</pre></div><p class="small" style="margin-top:14px">Works unchanged for systems if $y$ and the $k$\'s are vectors.</p>'),
             notes="Common mistakes: using k1 instead of k1/2 in k2; using k2 at the end instead of k3; forgetting the factor h in each k (some textbooks define k without h, then multiply by h at the end: say which convention you use)."),
        dict(type='worked', id='p1', title='Problem 1: one RK4 step for $y\' = x + y$, $y(0) = 1$, $h = 0.1$',
             q='Compute $y(0.1)$ by RK4 and compare with the exact value $2e^{0.1} - 1.1$.',
             steps=['$k_1 = 0.1(0 + 1) = 0.1$', '$k_2 = 0.1\\big(0.05 + 1 + 0.05\\big) = 0.11$', '$k_3 = 0.1\\big(0.05 + 1 + 0.055\\big) = 0.1105$', '$k_4 = 0.1\\big(0.1 + 1 + 0.1105\\big) = 0.12105$',
                    '$y_1 = 1 + \\tfrac16(0.1 + 0.22 + 0.221 + 0.12105) = 1.1103417$'],
             answer='Exact $1.1103418$: RK4 is correct to 7 digits after one step (Euler: 1.1, Heun: 1.11).',
             right=dict(w='ode', o=dict(f='x + y', x0=0, y0=1, h=0.1, xend=0.4, exact='2*e^x - x - 1', methods=['rk4'], main='rk4', height='240px', noexact=True, field=False, compact=True, maxRows=6)), rw=700,
             notes="Continue with the widget: y(0.2) = 1.242805, y(0.3) = 1.399717, y(0.4) = 1.583648, each within 1e-6 of the exact values."),
        dict(type='widget', id='explore', title='Explore: Euler, Heun and RK4 side by side', w='ode', o=dict(f='x + y', x0=0, y0=1, h=0.2, xend=2, exact='2*e^x - x - 1', methods=['euler', 'heun', 'rk4'], main='rk4', height='320px', side=True, tableHeight='320px',
             presets=[['y′ = x + y', 'x + y', 0, 1, 0.2, 2, '2*e^x - x - 1'], ['y′ = x² + y²', 'x^2 + y^2', 0, 0, 0.1, 1, ''], ['y′ = cos x · y', 'cos(x)*y', 0, 1, 0.5, 10, 'e^(sin(x))'], ['logistic growth', 'y*(1 - y)', 0, 0.05, 0.5, 12, '1/(1 + 19*e^(-x))']]), lw=440,
             items=['With $h = 0.2$ RK4 sits on the exact curve; Euler falls far behind', 'Halve $h$ and compare how fast each error falls (2, 4, 16)', 'Periodic example $y\' = y\\cos x$: RK4 stays on track with $h = 0.5$', 'Logistic growth: the S-curve of populations and of sigmoid units'],
             notes="Errors at x = 2 with h = 0.2: Euler 2.39, Heun 0.17, RK4 3.3e-4. The table lists the RK4 steps."),
        dict(type='math', id='systems', title='Systems and higher-order equations',
             eqs=[dict(cap='Several unknowns: the same formulas with vectors', eq='\\begin{aligned} \\mathbf{y}\' &= \\mathbf{F}(x, \\mathbf{y}), \\qquad \\mathbf{k}_1 = h\\mathbf{F}(x_n, \\mathbf{y}_n), \\;\\dots \\\\ \\mathbf{y}_{n+1} &= \\mathbf{y}_n + \\tfrac16(\\mathbf{k}_1 + 2\\mathbf{k}_2 + 2\\mathbf{k}_3 + \\mathbf{k}_4) \\end{aligned}'),
                  dict(cap='A second-order equation becomes a first-order system', eq='y\'\' = g(x, y, y\') \\;\\Longrightarrow\\; u\' = v,\\;\\; v\' = g(x, u, v)', frag=True)],
             items=['Spring $x\'\' = -x$: $x\' = y$, $y\' = -x$', 'Pendulum $\\theta\'\' = -\\tfrac gL\\sin\\theta$: no closed-form solution for large swings', 'Compute all components of $\\mathbf{k}_1$ before any of $\\mathbf{k}_2$', 'Every ODE solver library works with systems in this form'],
             ifrag=True, rw=600,
             notes="Typical slip: updating x before computing y's slope with the old x. In code: compute the whole vector k1, then k2, etc."),
        dict(type='widget', id='sysw', title='Explore: systems in the phase plane', w='odesys', o=dict(f='y', g='-x', x0=1, y0=0, h=0.1, T=62.83, inv='x^2 + y^2', method='euler', height='300px',
             presets=[['spring, Euler', 'y', '-x', 1, 0, 0.1, 62.83, 'x^2 + y^2', 'euler'], ['spring, RK4', 'y', '-x', 1, 0, 0.1, 62.83, 'x^2 + y^2', 'rk4'], ['predator–prey', '1.1*x - 0.4*x*y', '0.1*x*y - 0.4*y', 10, 10, 0.05, 50, '0.1*x - 0.4*ln(x) + 0.4*y - 1.1*ln(y)', 'rk4'], ['pendulum (θ, ω)', 'y', '-sin(x)', 2.5, 0, 0.1, 40, 'y^2/2 - cos(x)', 'rk4']]),
             items=['Left: the path in the $(x, y)$ plane; right: $x(t)$ and $y(t)$', 'Euler on the spring spirals outwards; RK4 stays on the circle', 'Predator–prey: the conserved quantity tests the solver', 'Switch methods and step sizes and watch the "conserved quantity" line'],
             lw=420,
             notes="Predator–prey (Lotka–Volterra) with h = 0.05 for 50 time units: Euler's conserved quantity drifts from 1.546 to 3.65 and the cycle spirals out; RK4 keeps it at 1.54611.\n\nPendulum starting at 2.5 rad (143°): energy y²/2 − cos x is conserved; no elementary formula for the motion."),
        dict(type='math', id='multistep', title='Predictor–corrector methods: reuse earlier slopes',
             eqs=[dict(cap="Milne: predictor (open Newton–Cotes) and corrector (Simpson's rule)", eq='\\begin{aligned} y^{P}_{n+1} &= y_{n-3} + \\frac{4h}{3}\\big(2f_n - f_{n-1} + 2f_{n-2}\\big) \\\\ y^{C}_{n+1} &= y_{n-1} + \\frac h3\\big(f_{n-1} + 4f_n + f_{n+1}\\big) \\end{aligned}'),
                  dict(cap='Adams–Bashforth (predictor) and Adams–Moulton (corrector), fourth order', eq='\\begin{aligned} y^{P}_{n+1} &= y_n + \\frac{h}{24}\\big(55f_n - 59f_{n-1} + 37f_{n-2} - 9f_{n-3}\\big) \\\\ y^{C}_{n+1} &= y_n + \\frac{h}{24}\\big(9f_{n+1} + 19f_n - 5f_{n-1} + f_{n-2}\\big) \\end{aligned}', frag=True)],
             items=['$f_k = f(x_k, y_k)$ are slopes already computed: about <b>2 new evaluations per step</b> (RK4 needs 4)', 'Not self-starting: the first 3 steps come from RK4', 'Predictor − corrector difference estimates the error for free', 'Milne can be unstable for decaying solutions; Adams is the standard choice'],
             ifrag=True, rw=560,
             notes="Origins: integrate the Newton backward interpolation polynomial through the last few slopes (Lecture 16): over one step → Adams; over four steps → Milne's predictor; Simpson over two steps → Milne's corrector."),
        dict(type='bullets', id='algo2', title='A predictor–corrector method, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Get $y_0, y_1, y_2, y_3$ (starting values) by RK4; compute $f_0, \\dots, f_3$', 'Predict $y^{P}_{n+1}$ with the predictor formula', 'Evaluate $f^{P}_{n+1} = f(x_{n+1}, y^{P}_{n+1})$', 'Correct: $y^{C}_{n+1}$ with the corrector formula (optionally repeat steps 3–4 once)',
                    'Store $f_{n+1} = f(x_{n+1}, y^{C}_{n+1})$, shift the window of four slopes, repeat'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode (Adams–Bashforth–Moulton)</span><pre style="margin:0;font:500 25px/1.5 var(--mono);color:#f5f3ee">y[0..3] ← RK4 starting values\nF[k] ← f(x[k], y[k]),  k = 0 … 3\nfor n = 3, 4, …:\n    yp ← y[n] + h/24·(55F[n] − 59F[n−1]\n                     + 37F[n−2] − 9F[n−3])\n    fp ← f(x[n+1], yp)\n    y[n+1] ← y[n] + h/24·(9fp + 19F[n]\n                          − 5F[n−1] + F[n−2])\n    F[n+1] ← f(x[n+1], y[n+1])\n    err ≈ (19/270)·|y[n+1] − yp|</pre></div><p class="small" style="margin-top:14px">Two new $f$ values per step; the error estimate costs nothing.</p>'),
             notes="The error estimate 19/270 |y_C − y_P| (Milne's device for ABM) lets a program change h automatically."),
        dict(type='table', id='p2', title='Problem 2: Milne and Adams for $y\' = x + y$ at $x = 0.4$',
             q='Starting values from RK4 ($h = 0.1$): $y_0 = 1$, $y_1 = 1.110342$, $y_2 = 1.242805$, $y_3 = 1.399717$. Find $y(0.4)$ by Milne\'s and by Adams\' method.',
             head=['quantity', 'Milne', 'Adams–Bashforth–Moulton'], tx=(0,), frag=True,
             rows=[['slopes $f_0, f_1, f_2, f_3$', '1, 1.210342, 1.442805, 1.699717', 'same'], ['predictor', '$1 + \\tfrac{0.4}{3}(2.420684 - 1.442805 + 3.399434) = 1.583642$', '$1.399717 + \\tfrac{0.1}{24}(\\ldots) = 1.583640$'],
                   ['$f^{P} = 0.4 + y^{P}$', '1.983642', '1.983640'], ['corrector', '$1.242805 + \\tfrac{0.1}{3}(1.442805 + 6.798868 + 1.983642) = 1.583649$', '$1.399717 + \\tfrac{0.1}{24}(\\ldots) = 1.583649$'],
                   ['exact $2e^{0.4} - 1.4$', '1.583649', '1.583649']],
             note='Both correctors agree with the exact value to 6 decimals, using only 2 new evaluations of $f$ (RK4 would use 4).',
             notes="Adams predictor in full: 1.399717 + (0.1/24)(55·1.699717 − 59·1.442805 + 37·1.210342 − 9·1) = 1.583640. Corrector: 1.399717 + (0.1/24)(9·1.983640 + 19·1.699717 − 5·1.442805 + 1.210342) = 1.583649."),
        dict(type='math', id='stability', title='Stability and stiff equations',
             eqs=[dict(cap='Test equation y′ = λy; amplification factor per step, z = hλ', eq='\\begin{aligned} \\text{Euler: } y_{n+1} &= (1 + z)\\,y_n \\\\ \\text{RK4: } y_{n+1} &= \\Big(1 + z + \\frac{z^2}{2} + \\frac{z^3}{6} + \\frac{z^4}{24}\\Big)y_n \\end{aligned}'),
                  dict(cap='Implicit (backward) Euler: stable for every h > 0 when λ < 0', eq='y_{n+1} = y_n + h\\,f(x_{n+1}, y_{n+1}) \\;\\Rightarrow\\; y_{n+1} = \\frac{y_n}{1 - z}', frag=True)],
             items=['Stable when |factor| ≤ 1: Euler needs $-2 \\le h\\lambda \\le 0$; RK4 about $-2.79 \\le h\\lambda$', '<b>Stiff</b>: a fast decaying part (large $|\\lambda|$) forces a tiny $h$ even after it has died out', 'Implicit methods solve an equation each step (Newton, Lecture 9–10) but take large steps safely', 'Milne\'s corrector has a parasitic root of size $> 1$: errors grow for decaying solutions'],
             ifrag=True, rw=600,
             notes="Numbers for y' = −y with h = 0.1: at t = 20, exact 2.1e-9, Adams 2.1e-9, Milne −9.5e-6 (wrong sign, growing): Milne's instability.\n\nRK4 amplification at z = −2.78 is 0.992, at −2.8 it is 1.022: the boundary is about −2.785."),
        dict(type='compare', id='classic', title='Same kind of system, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (solve exactly)', tag='Calculus', cls='blue', items=['Spring $x\'\' = -x$: characteristic roots $\\pm i$', '$x = \\cos t$, $y = -\\sin t$', 'Energy exactly 1 for ever']),
             right=dict(h='Numerical (RK4, $h = 0.1$)', tag='Algorithm', cls='key', items=['628 steps over ten periods', 'Largest error in $x$: $5\\times10^{-5}$', 'Energy 0.999991 (Euler: 517)']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>An epidemic (SIR model): $S\' = -0.3SI$, $\\;I\' = 0.3SI - 0.1I$</h3><p>No formula gives $I(t)$. RK4 with a step of one day: the infected fraction peaks at <b>30.4% on day 27</b>, and about 94% of people are eventually infected. This is how epidemic forecasts were computed in 2020.</p></div>'),
             notes="SIR numbers: S(0) = 0.99, I(0) = 0.01, β = 0.3, γ = 0.1 (R₀ = 3). RK4 h = 1: peak 0.3036 at day 27; h = 0.1: 0.3038 at day 26.6. Final susceptible fraction 0.0588, so about 94% infected over the epidemic."),
        dict(type='code', id='code', title='RK4 for a single equation and for a system', code='rk4', lw=560,
             items=['A reusable <code>rk4_step</code> for $y\' = f(x, y)$', 'The same steps for the spring system $(x, y)$', 'Compares the energy after 10 periods with Euler', 'Lab: Adams–Bashforth–Moulton and the epidemic model'],
             notes="Run both tabs. The energy after ten periods: Euler 517.395605, RK4 0.999991."),
        dict(type='widget', id='fail', title='Limitations shown failing', kick='When explicit methods break', w='ode',
             o=dict(f='-50*(y - cos(x))', x0=0, y0=0, h=0.05, xend=2, exact=STIFF_EXACT, methods=['rk4'], main='rk4', only=['euler', 'heun', 'rk4'], height='280px', side=True, tableHeight='280px', ylim=[-1.5, 1.5],
                    presets=[['stiff, RK4 h = 0.05', '-50*(y - cos(x))', 0, 0, 0.05, 2, STIFF_EXACT], ['stiff, RK4 h = 0.06', '-50*(y - cos(x))', 0, 0, 0.06, 2, STIFF_EXACT], ['stiff, Euler h = 0.05', '-50*(y - cos(x))', 0, 0, 0.05, 2, STIFF_EXACT], ['blow-up: y′ = y²', 'y^2', 0, 1, 0.1, 1.2, '1/(1 - x)']]), lw=520,
             items=['<b>Stiff</b>: $y\' = -50(y - \\cos x)$ follows $\\cos x$ smoothly, yet RK4 explodes for $h = 0.06$ ($h\\lambda = -3 < -2.79$)', 'Euler already fails at $h = 0.05$; backward Euler is fine even with $h = 0.1$',
                    '<b>Singularities</b>: $y\' = y^2$ blows up at $x = 1$; a fixed-step method steps right past it', 'Fixed $h$ wastes work where the solution is smooth: real solvers adapt $h$'],
             frag=True,
             notes="Values at x = 2 (exact −0.397802): RK4 h = 0.05 → −0.39748; h = 0.06 → about −36725 (exploded). Euler h = 0.04 → −1.398 (wrong), h = 0.05 → overflow. Backward Euler h = 0.1 → −0.39745.\n\nStiff solvers: scipy.integrate.solve_ivp(method='BDF' or 'Radau'), MATLAB ode15s."),
        dict(type='exam', id='practice', src='Problem 3',
             q='"Use the fourth-order Runge–Kutta method to find $y(0.1)$ and $y(0.2)$ for $\\dfrac{dy}{dx} = y - x$, $y(0) = 2$, with $h = 0.1$."',
             tips=['Write the four formulas and say whether the $k$\'s include $h$', 'Step 1: $k_1 = 0.2$, $k_2 = 0.205$, $k_3 = 0.20525$, $k_4 = 0.210525$; $\\;y_1 = 2.205171$',
                   'Step 2 from $(0.1, 2.205171)$: $y_2 = 2.421403$', 'Compare with the exact $e^{0.2} + 1.2 = 2.421403$: correct to 6 decimals; give a one-line comparison with Euler (2.41) and modified Euler (2.421025)'],
             notes=""),
        dict(type='profile', id='profile', title='Runge–Kutta and predictor–corrector methods: method profile',
             best=['RK4: smooth non-stiff problems; 6–8 digits with moderate $h$; self-starting, easy step changes', 'Adams–Bashforth–Moulton: expensive $f$ (2 evaluations per step) with a free error estimate', 'Systems of any size, written once in vector form'],
             worst=['Stiff problems: explicit methods need tiny steps', 'Milne for decaying solutions: unstable', 'Solutions with singularities or sudden jumps (fixed $h$)'],
             suited=['Orbits, mechanics, circuits, chemical kinetics (non-stiff), epidemics', 'Adaptive pairs (RK45 / Dormand–Prince) in SciPy and MATLAB', 'Multistep methods in long simulations where $f$ is costly'],
             avoid=['Stiff systems (use implicit methods: backward Euler, BDF, Radau)', 'Very long Hamiltonian simulations (use symplectic integrators)', 'Fixed $h$ when the solution changes scale (use adaptive step size)'],
             verdict='Rule of thumb: <b>start with an adaptive RK (RK45); if it takes absurdly small steps, the problem is stiff: switch to an implicit solver</b>.',
             notes="Symplectic integrators (leapfrog / velocity Verlet) keep energy bounded for ever; they are used in molecular dynamics and astronomy."),
        dict(type='table', id='compare', title='Comparative analysis: ODE methods', cls='tb sm',
             head=['Method', 'Order', '$f$ per step', 'Self-starting?', 'Stability ($h\\lambda$ real)', 'Error at $x = 1$ ($y\' = x+y$, $h = 0.1$)'], tx=(0,), frag=True,
             rows=[['Euler', '1', '1', 'yes', '$[-2, 0]$', '0.249'], ['Heun / RK2', '2', '2', 'yes', '$[-2, 0]$', '$8.4\\times10^{-3}$'], ['RK4', '4', '4', 'yes', '$[-2.79, 0]$', '$4.2\\times10^{-6}$'],
                   ['Milne P–C', '4', '2', 'no (needs RK4 start)', 'weakly unstable', '$6\\times10^{-7}$'], ['Adams–Bashforth–Moulton', '4', '2', 'no (needs RK4 start)', 'about $[-1.25, 0]$', '$3.6\\times10^{-6}$'], ['Backward Euler (implicit)', '1', '1 + equation solve', 'yes', 'all $h\\lambda < 0$', '0.30']],
             note='No method wins everywhere: RK4 for general use, Adams when $f$ is expensive, implicit methods when the problem is stiff.', notefrag=True,
             notes="ABM (PECE mode) is stable on the real axis for hλ down to about −1.25 (checked numerically: stable at −1.2, unstable at −1.3). Backward Euler error for y' = x + y at h = 0.1 is 0.30 (first order). Milne and ABM errors at x = 1: 6.2e-7 and 3.6e-6."),
        dict(type='bridge', id='bridge', title='End of Module 6: from solving to fitting', kick='Roadmap', lead='We can now simulate models. The last module asks the reverse question: given data, which model and which parameters?',
             keep=['RK4: order 4 from function values alone', 'Systems and higher-order equations', 'Predictor–corrector with a free error estimate', 'Stability limits and stiffness'],
             rows=[['Model parameters (e.g. $\\beta$, $\\gamma$ of an epidemic) are unknown', 'Fit them to data: least squares', 23],
                   ['Choosing a model that fits without overfitting', 'Polynomial, exponential fits; validation', 24],
                   ['Training is itself an ODE: $w\' = -\\nabla L(w)$', 'Gradient descent = Euler on the gradient flow', 25],
                   ['Step size too large makes training explode', 'Learning rate vs stability (today\'s $|1 + h\\lambda| < 1$)', 25]],
             notes="The last two rows are the payoff for the ML course: gradient descent is Euler's method, and the learning-rate limit is today's stability condition."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see an RK or multistep solver in action.',
             items=[
                 dict(ic='🦠', h='Epidemic forecasting (SIR)', t='How the 2020 curves were made',
                      detail=dict(where='public-health modelling. Susceptible ($x$) and infected ($y$) fractions obey $x\' = -\\beta xy$, $y\' = \\beta xy - \\gamma y$; forecasts step this system with RK4 or an adaptive solver.',
                                  w='odesys', o=dict(f='-0.3*x*y', g='0.3*x*y - 0.1*y', x0=0.99, y0=0.01, h=1, T=160, inv='', method='rk4', height='200px', noinv=True),
                                  note='Peak about 30% infected around day 27. Lockdowns lower $\\beta$: try 0.2 in the first two formulas and watch the peak flatten and move later.')),
                 dict(ic='🛰️', h='Satellite and planet orbits', t='GPS satellites, Mars missions',
                      detail=dict(where='orbit prediction. Newton\'s law of gravitation gives a system of six first-order ODEs (position and velocity in 3-D); mission design integrates it with high-order Runge–Kutta or multistep (Adams) methods over months.',
                                  steps=['State $\\mathbf{y} = (x, y, z, v_x, v_y, v_z)$; $\\mathbf{y}\' = (\\mathbf{v}, -GM\\mathbf{r}/|\\mathbf{r}|^3 + \\text{perturbations})$', 'Perturbations: Earth\'s oblateness, Moon, Sun, solar pressure: no closed form', 'Adams–Bashforth–Moulton of high order: few force evaluations per step', 'Errors must stay below metres after weeks: the reason for high order'],
                                  note='JPL\'s planetary ephemerides are produced with variable-order Adams methods.')),
                 dict(ic='🐍', h='SciPy solve_ivp and MATLAB ode45', t='Adaptive Runge–Kutta in one line',
                      detail=dict(where='every scientific Python or MATLAB program that solves ODEs. The default method (RK45, Dormand–Prince) computes a 4th- and a 5th-order RK result from the same six slopes; their difference estimates the error and sets the next step size.',
                                  steps=['Take a step with both formulas (6 evaluations, shared)', 'Error estimate = |5th − 4th| order result', 'Too big? Reject and retry with a smaller $h$; very small? Enlarge $h$', 'Stiff problem detected by tiny steps: switch to method="BDF" or "Radau" (implicit)'],
                                  note='Today\'s two ideas, RK and stability, are exactly the two choices a user makes when calling solve_ivp.')),
                 dict(ic='🦊', h='Predator and prey (Lotka–Volterra)', t='Rabbits, foxes and conserved quantities',
                      detail=dict(where='ecology and economics. Prey $x$ grow and are eaten; predators $y$ grow by eating and die otherwise: $x\' = 1.1x - 0.4xy$, $y\' = 0.1xy - 0.4y$. The populations cycle; a quantity $V(x, y)$ stays constant on each cycle.',
                                  w='odesys', o=dict(f='1.1*x - 0.4*x*y', g='0.1*x*y - 0.4*y', x0=10, y0=10, h=0.05, T=50, inv='0.1*x - 0.4*ln(x) + 0.4*y - 1.1*ln(y)', method='rk4', height='200px'),
                                  note='Switch to Euler: the cycles spiral outwards and $V$ drifts from 1.546 to 3.65, a numerical artefact that would wrongly predict extinction.'))],
             notes="Both widget cards are fully interactive inside the pop-up."),
        dict(type='check', id='check', q='RK4 for $y\' = y$, $y(0) = 1$, $h = 0.1$: $k_1 = 0.1$. What is $k_2$?',
             opts=['$0.105$', '$0.11$', '$0.1$', '$0.1105$'], right=0,
             answer='A. $k_2 = hf(y_0 + k_1/2) = 0.1(1 + 0.05) = 0.105$. Then $k_3 = 0.10525$, $k_4 = 0.110525$, $y_1 = 1.1051708$ (exact $e^{0.1} = 1.1051709$).',
             notes="Option B uses y0 + k1 instead of y0 + k1/2."),
        dict(type='summary', id='summary', items=[
            'RK4: $k_1, \\dots, k_4$ at start, middle, middle, end; $y_{n+1} = y_n + \\frac16(k_1 + 2k_2 + 2k_3 + k_4)$; order 4',
            'Systems: same formulas with vectors; $y\'\' = g$ becomes $u\' = v$, $v\' = g$',
            'Milne and Adams–Bashforth–Moulton: predictor + corrector from past slopes, 2 evaluations per step, need RK4 starting values',
            'Stability: $|$amplification$| \\le 1$; stiff problems need implicit methods'],
            hw=['Use RK4 with $h = 0.1$ to find $y(0.2)$ for $y\' = x^2 + y^2$, $y(0) = 1$.', 'Write $y\'\' + 0.5y\' + 4y = 0$, $y(0) = 1$, $y\'(0) = 0$ as a system and take one RK4 step with $h = 0.1$.',
                'Using the RK4 values of Problem 3 at $x = 0, 0.1, 0.2, 0.3$, find $y(0.4)$ by the Adams–Bashforth–Moulton method.', 'For $y\' = -100y$, find the largest stable $h$ for Euler and for RK4. Check in the lab.'],
            solved='RK4 with $h = 0.1$ keeps the spring\'s energy at <b>0.999991</b> after ten periods (Euler: 517, Heun: 1.016). The largest position error is $5\\times10^{-5}$.',
            next='<b>Module 7: least squares and linear regression.</b> From solving models to fitting them to data, the core of machine learning.',
            notes="Homework answers: Q1: y(0.1) = 1.111463, y(0.2) = 1.253015. Q2: u' = v, v' = −4u − 0.5v; one RK4 step: u(0.1) = 0.980396, v(0.1) = −0.387565. Q3: starting values 2, 2.205171, 2.421403, 2.649858; slopes f = y − x: 2, 2.105171, 2.221403, 2.349858; predictor 2.891820, corrector 2.891825; exact e^{0.4} + 1.4 = 2.891825. Q4: Euler h ≤ 0.02, RK4 h ≤ 0.0279."),
    ],
    code={
        'rk4': dict(file='runge_kutta4', py='''# RK4 for y' = f(x, y), and for the spring system x' = y, y' = -x
import math

def f(x, y):
    return x + y

def rk4_step(f, x, y, h):
    k1 = h * f(x, y)
    k2 = h * f(x + h / 2, y + k1 / 2)
    k3 = h * f(x + h / 2, y + k2 / 2)
    k4 = h * f(x + h, y + k3)
    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6

x, y, h = 0.0, 1.0, 0.1
for n in range(4):
    y = rk4_step(f, x, y, h)
    x = (n + 1) * h
    print(f"x = {x:.1f}  y = {y:.7f}  exact = {2 * math.exp(x) - x - 1:.7f}")

def F(u, v):                                  # spring: u' = v, v' = -u
    return v, -u

def run(method, h, T):
    u, v = 1.0, 0.0
    for _ in range(round(T / h)):
        if method == "euler":
            a = F(u, v)
            u, v = u + h * a[0], v + h * a[1]
        else:
            a = F(u, v)
            b = F(u + h / 2 * a[0], v + h / 2 * a[1])
            c = F(u + h / 2 * b[0], v + h / 2 * b[1])
            d = F(u + h * c[0], v + h * c[1])
            u += h / 6 * (a[0] + 2 * b[0] + 2 * c[0] + d[0])
            v += h / 6 * (a[1] + 2 * b[1] + 2 * c[1] + d[1])
    return u * u + v * v

T = 20 * math.pi                              # ten periods
print(f"energy after ten periods: Euler {run('euler', 0.1, T):.6f}   RK4 {run('rk4', 0.1, T):.6f}")
''', c='''/* RK4 for y' = f(x, y), and for the spring system x' = y, y' = -x */
#include <stdio.h>
#include <math.h>

double f(double x, double y) { return x + y; }

double rk4_step(double x, double y, double h) {
    double k1 = h * f(x, y);
    double k2 = h * f(x + h / 2, y + k1 / 2);
    double k3 = h * f(x + h / 2, y + k2 / 2);
    double k4 = h * f(x + h, y + k3);
    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
}

double energy(int rk, double h, double T) {     /* spring: u' = v, v' = -u */
    double u = 1, v = 0;
    int n = (int)(T / h + 0.5);
    for (int i = 0; i < n; i++) {
        if (!rk) { double du = v, dv = -u; u += h * du; v += h * dv; }
        else {
            double a1 = v, a2 = -u;
            double b1 = v + h / 2 * a2, b2 = -(u + h / 2 * a1);
            double c1 = v + h / 2 * b2, c2 = -(u + h / 2 * b1);
            double d1 = v + h * c2, d2 = -(u + h * c1);
            u += h / 6 * (a1 + 2 * b1 + 2 * c1 + d1);
            v += h / 6 * (a2 + 2 * b2 + 2 * c2 + d2);
        }
    }
    return u * u + v * v;
}

int main(void) {
    double x = 0, y = 1, h = 0.1;
    for (int n = 0; n < 4; n++) {
        y = rk4_step(x, y, h);
        x = (n + 1) * h;
        printf("x = %.1f  y = %.7f  exact = %.7f\\n", x, y, 2 * exp(x) - x - 1);
    }
    double T = 20 * M_PI;                        /* ten periods */
    printf("energy after ten periods: Euler %.6f   RK4 %.6f\\n", energy(0, 0.1, T), energy(1, 0.1, T));
    return 0;
}
'''),
        'abm': dict(file='adams_predictor_corrector', py='''# Adams-Bashforth-Moulton predictor-corrector, started with RK4
import math

def f(x, y):
    return x + y

h, n_steps = 0.1, 10
xs = [i * h for i in range(n_steps + 1)]
ys = [1.0]
for i in range(3):                            # starting values by RK4
    x, y = xs[i], ys[i]
    k1 = h * f(x, y); k2 = h * f(x + h / 2, y + k1 / 2)
    k3 = h * f(x + h / 2, y + k2 / 2); k4 = h * f(x + h, y + k3)
    ys.append(y + (k1 + 2 * k2 + 2 * k3 + k4) / 6)
F = [f(x, y) for x, y in zip(xs, ys)]

for n in range(3, n_steps):
    yp = ys[n] + h / 24 * (55 * F[n] - 59 * F[n - 1] + 37 * F[n - 2] - 9 * F[n - 3])
    fp = f(xs[n + 1], yp)
    yc = ys[n] + h / 24 * (9 * fp + 19 * F[n] - 5 * F[n - 1] + F[n - 2])
    ys.append(yc)
    F.append(f(xs[n + 1], yc))
    exact = 2 * math.exp(xs[n + 1]) - xs[n + 1] - 1
    print(f"x = {xs[n+1]:.1f}  predictor {yp:.6f}  corrector {yc:.6f}  exact {exact:.6f}  estimate of error {19 / 270 * abs(yc - yp):.1e}")
''', c='''/* Adams-Bashforth-Moulton predictor-corrector, started with RK4 */
#include <stdio.h>
#include <math.h>
#define NS 10

double f(double x, double y) { return x + y; }

int main(void) {
    double h = 0.1, x[NS + 1], y[NS + 1], F[NS + 1];
    for (int i = 0; i <= NS; i++) x[i] = i * h;
    y[0] = 1;
    for (int i = 0; i < 3; i++) {                 /* starting values by RK4 */
        double k1 = h * f(x[i], y[i]), k2 = h * f(x[i] + h / 2, y[i] + k1 / 2);
        double k3 = h * f(x[i] + h / 2, y[i] + k2 / 2), k4 = h * f(x[i] + h, y[i] + k3);
        y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
    }
    for (int i = 0; i <= 3; i++) F[i] = f(x[i], y[i]);
    for (int n = 3; n < NS; n++) {
        double yp = y[n] + h / 24 * (55 * F[n] - 59 * F[n - 1] + 37 * F[n - 2] - 9 * F[n - 3]);
        double fp = f(x[n + 1], yp);
        y[n + 1] = y[n] + h / 24 * (9 * fp + 19 * F[n] - 5 * F[n - 1] + F[n - 2]);
        F[n + 1] = f(x[n + 1], y[n + 1]);
        double exact = 2 * exp(x[n + 1]) - x[n + 1] - 1;
        printf("x = %.1f  predictor %.6f  corrector %.6f  exact %.6f  estimate of error %.1e\\n", x[n + 1], yp, y[n + 1], exact, 19.0 / 270 * fabs(y[n + 1] - yp));
    }
    return 0;
}
'''),
    },
    lab=dict(title='Runge-Kutta and Predictor-Corrector Lab',
             intro='Compare Euler, Heun and RK4 on your own equations, solve systems in the phase plane, and run Adams\' predictor–corrector method.',
             tabs=[
                 dict(name='ODE solver', blocks=[
                     dict(p='Type y′ = f(x, y), the start, h and the end. Tick the methods to compare; the table lists the steps of the first one (RK4 by default).'),
                     dict(w='ode', o=dict(f='y - x', x0=0, y0=2, h=0.1, xend=0.2, exact='e^x + x + 1', methods=['rk4', 'heun', 'euler'], main='rk4', height='320px', side=True, tableHeight='320px',
                                          presets=[['Problem 3', 'y - x', 0, 2, 0.1, 0.2, 'e^x + x + 1'], ['homework 1', 'x^2 + y^2', 0, 1, 0.1, 0.2, ''], ['stiff y′ = −100y', '-100*y', 0, 1, 0.025, 0.5, 'e^(-100*x)'], ['logistic', 'y*(1 - y)', 0, 0.05, 0.5, 12, '1/(1 + 19*e^(-x))']]))]),
                 dict(name='Systems', blocks=[
                     dict(p='Two equations x′ = f(x, y), y′ = g(x, y). Use the conserved quantity to judge the method.'),
                     dict(w='odesys', o=dict(f='y', g='-x', x0=1, y0=0, h=0.1, T=62.83, inv='x^2 + y^2', method='rk4', height='300px',
                                             presets=[['spring', 'y', '-x', 1, 0, 0.1, 62.83, 'x^2 + y^2', 'rk4'], ['damped (homework 2)', 'y', '-4*x - 0.5*y', 1, 0, 0.1, 20, '', 'rk4'], ['predator–prey', '1.1*x - 0.4*x*y', '0.1*x*y - 0.4*y', 10, 10, 0.05, 50, '0.1*x - 0.4*ln(x) + 0.4*y - 1.1*ln(y)', 'euler'], ['epidemic (SIR)', '-0.3*x*y', '0.3*x*y - 0.1*y', 0.99, 0.01, 1, 160, '', 'rk4']]))]),
                 dict(name='Code', blocks=[
                     dict(h='RK4 and the spring'), dict(code='rk4', tasks=['Run it. Compare y(0.1) with Problem 1.', 'Halve h in the spring: how much closer to 1 is the RK4 energy?', 'Change f to y - x with y = 2 (Problem 3).']),
                     dict(h='Adams–Bashforth–Moulton'), dict(code='abm', tasks=['Run it. Compare the value at x = 0.4 with Problem 2.', 'How does the error estimate compare with the true error?', 'Change f to -y (exact e^(-x)) and run to x = 1.'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Write the fourth-order Runge–Kutta formulas.', '$k_1 = hf(x_n, y_n)$, $k_2 = hf(x_n + \\frac h2, y_n + \\frac{k_1}{2})$, $k_3 = hf(x_n + \\frac h2, y_n + \\frac{k_2}{2})$, $k_4 = hf(x_n + h, y_n + k_3)$, $y_{n+1} = y_n + \\frac16(k_1 + 2k_2 + 2k_3 + k_4)$.'),
                         ('Why are Runge–Kutta methods preferred to the Taylor series method?', 'They reach the same order using only values of $f$, so no derivatives of $f$ have to be derived and coded for each new equation.'),
                         ('State Milne\'s predictor and corrector formulas.', 'Predictor $y_{n+1} = y_{n-3} + \\frac{4h}{3}(2f_n - f_{n-1} + 2f_{n-2})$; corrector $y_{n+1} = y_{n-1} + \\frac h3(f_{n-1} + 4f_n + f_{n+1})$ (Simpson\'s rule).'),
                         ('Why are predictor–corrector methods not self-starting?', 'Their formulas use values at several previous points ($y_{n-3}, \\dots, y_n$); at the start only $y_0$ is known, so the first few values must come from a one-step method such as RK4.'),
                         ('What is a stiff differential equation?', 'One with components that decay at very different rates, so that explicit methods must use a step size set by the fastest (already negligible) component to stay stable, e.g. $y\' = -50(y - \\cos x)$. Implicit methods remove this restriction.')])])]),
)
