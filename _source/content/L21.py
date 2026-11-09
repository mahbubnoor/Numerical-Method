LECTURE = dict(
    title='ODEs I: Taylor, Picard and Euler Methods',
    short='ODEs I: Taylor, Picard, Euler, Heun',
    sub='Differential equations tell us how a quantity changes, not what it is. Stepping $y\' = f(x, y)$ forward: the Taylor series and Picard methods, Euler\'s method, the modified Euler (Heun) method, and the difference between local and global error.',
    slides=[
        dict(type='cover', id='cover', notes="Opening question: 'A cup of tea is at 90 °C in a 25 °C room. It cools faster when it is hotter. How hot is it after 10 minutes?' The physics gives the rate, not the temperature.\n\nModule 6 begins. Everything rests on Taylor series (Lecture 3) and the integration rules of Lecture 20."),
        dict(type='bullets', id='hook', title='The problem: a law of change, not a formula', kick='Why this lecture', rw=640,
             lead='Newton\'s law of cooling: the temperature $T$ (°C) of tea in a 25 °C room changes at a rate proportional to the difference.',
             items=['$\\dfrac{dT}{dt} = -0.1\\,(T - 25)$ per minute, with $T(0) = 90$', 'We know the <b>rate</b> at every moment, not the temperature itself', 'This one can be solved by hand; most real models (epidemics, circuits, orbits, neural ODEs) cannot',
                    'Idea: start from the known value and take small steps, using the rate to predict each next value'],
             frag=True,
             right=dict(table=[['$t$ (min)', '$T$ (°C)', 'rate $dT/dt$'], [['0', '90', '−6.5'], ['1', '?', '?'], ['2', '?', '?'], ['…', '…', '…'], ['10', '?', '']]]),
             notes="Exact solution: T = 25 + 65e^{−0.1t}, T(10) = 48.91 °C. Solved at the end: Euler with 1-minute steps gives 47.66 °C (error 1.25); Heun gives 48.96 °C (error 0.04)."),
        dict(type='goals', id='goals', items=[
            'State an <b>initial value problem</b> and read its slope field',
            'Solve by the <b>Taylor series</b> method and by <b>Picard\'s</b> successive approximations',
            'Apply <b>Euler\'s method</b> and the <b>modified Euler (Heun)</b> method by hand and in code',
            'Distinguish <b>local</b> and <b>global</b> error; predict how the error changes with $h$',
            'Recognise when a step size is too large (instability)'],
            prev='Integration rules: rectangle, trapezoid, Simpson.',
            today='Integrate an equation whose integrand depends on the unknown: $y(x+h) = y(x) + \\int f(t, y(t))\\,dt$.',
            notes="The key link: y(x + h) = y(x) + ∫ f(t, y(t)) dt. Euler is the left-rectangle rule for this integral, Heun is the trapezoidal rule."),
        dict(type='math', id='ivp', title='Initial value problems and slope fields',
             eqs=[dict(cap='First-order initial value problem', eq='\\frac{dy}{dx} = f(x, y), \\qquad y(x_0) = y_0'),
                  dict(cap='Integrated form: every method approximates this integral', eq='y(x_{n+1}) = y(x_n) + \\int_{x_n}^{x_{n+1}} f\\big(t, y(t)\\big)\\,dt', frag=True)],
             items=['$f(x, y)$ is the <b>slope</b> of the solution through the point $(x, y)$', 'Drawing short slope segments everywhere gives the <b>slope field</b>; solutions follow it', 'One initial value picks one solution curve', 'Unique solution if $f$ is smooth (Lipschitz in $y$) near $(x_0, y_0)$'],
             ifrag=True,
             notes="Show the slope field in the explore widget before computing anything: students can sketch the solution by following the dashes. That intuition is exactly Euler's method."),
        dict(type='math', id='taylor', title='The Taylor series method',
             eqs=[dict(cap='Expand the solution about x₀ (Lecture 3)', eq='y(x_0 + h) = y_0 + h\\,y_0\' + \\frac{h^2}{2!}y_0\'\' + \\frac{h^3}{3!}y_0\'\'\' + \\frac{h^4}{4!}y_0^{(4)} + \\cdots'),
                  dict(cap='Get the derivatives by differentiating the ODE itself. For y′ = x + y:', eq='y\' = x + y, \\quad y\'\' = 1 + y\', \\quad y\'\'\' = y\'\', \\quad y^{(4)} = y\'\'\'', frag=True)],
             items=['At $(0, 1)$: $y\' = 1$, $y\'\' = 2$, $y\'\'\' = 2$, $y^{(4)} = 2$', '$y(0.1) = 1 + 0.1 + \\tfrac{0.01}{2}(2) + \\tfrac{0.001}{6}(2) + \\tfrac{0.0001}{24}(2) = 1.110342$', 'Exact: $2e^{0.1} - 1.1 = 1.110342$',
                    'Accurate, but each new ODE needs its own derivative formulas, which quickly become messy'],
             ifrag=True,
             notes="With four terms the local error is O(h⁵); this is the accuracy that Runge–Kutta (Lecture 22) reaches without any derivatives of f."),
        dict(type='math', id='picard', title="Picard's method of successive approximations",
             eqs=[dict(cap='Iterate on the integral equation (a fixed-point iteration for functions, Lecture 8)', eq='y^{(k+1)}(x) = y_0 + \\int_{x_0}^{x} f\\big(t, y^{(k)}(t)\\big)\\,dt, \\qquad y^{(0)}(x) = y_0'),
                  dict(cap='For y′ = x + y, y(0) = 1', eq='\\begin{aligned} y^{(1)} &= 1 + x + \\tfrac{x^2}{2} \\\\ y^{(2)} &= 1 + x + x^2 + \\tfrac{x^3}{6} \\\\ y^{(3)} &= 1 + x + x^2 + \\tfrac{x^3}{3} + \\tfrac{x^4}{24} \\end{aligned}', frag=True)],
             items=['At $x = 0.1$: 1.105, 1.110167, 1.110337 → exact 1.110342', 'Each iteration adds one correct power of $x$', 'Needs the integrals in closed form: only for simple $f$', 'Its real value is theoretical: it proves that solutions exist'],
             ifrag=True,
             notes="Compute y⁽²⁾ on the board: y⁽²⁾ = 1 + ∫₀ˣ (t + 1 + t + t²/2) dt = 1 + x + x² + x³/6."),
        dict(type='math', id='euler', title="Euler's method",
             eqs=[dict(cap='Follow the slope at the current point for one step', eq='y_{n+1} = y_n + h\\,f(x_n, y_n), \\qquad x_{n+1} = x_n + h'),
                  dict(cap='Error per step (local) and after reaching a fixed x (global)', eq='\\text{local: } \\frac{h^2}{2}y\'\'(\\xi) = O(h^2), \\qquad \\text{global: } O(h)', frag=True)],
             items=['= first two Taylor terms; = left-rectangle rule for the integral', 'One evaluation of $f$ per step', '$1/h$ steps, each with an $O(h^2)$ error, add up to $O(h)$', 'Halve $h$: the error at the end halves (and the work doubles)'],
             ifrag=True,
             notes="Draw the geometry: from (x_n, y_n) follow the tangent of the solution through that point; you land slightly off the true curve and continue from the wrong point on a neighbouring solution curve. Errors accumulate."),
        dict(type='bullets', id='algo', title="Euler's method, step by step", kick='The method, step by step', ordered=True, rw=780,
             items=['Write the problem as $y\' = f(x, y)$, $y(x_0) = y_0$; choose $h$', 'Evaluate the slope $f(x_n, y_n)$ at the current point', 'Step: $y_{n+1} = y_n + h\\,f(x_n, y_n)$, $\\;x_{n+1} = x_n + h$', 'Repeat until $x$ reaches the target',
                    'Check: repeat with $h/2$; the change estimates the error'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input f, x0, y0, h, x_end\nx ← x0;  y ← y0\nwhile x &lt; x_end − h/2:\n    y ← y + h·f(x, y)\n    x ← x + h\n    print x, y\nreturn y</pre></div><p class="small" style="margin-top:14px">The loop condition avoids an extra step caused by rounding in $x + h$.</p>'),
             notes="Step 5 is Richardson again (Lecture 19): for a first-order method, error(h/2) ≈ y(h/2) − y(h)."),
        dict(type='widget', id='explore', title='Explore: stepping along the slope field', w='ode', o=dict(f='x + y', x0=0, y0=1, h=0.1, xend=1, exact='2*e^x - x - 1', methods=['euler'], height='320px', side=True, tableHeight='320px',
             presets=[['y′ = x + y', 'x + y', 0, 1, 0.1, 1, '2*e^x - x - 1'], ['tea cooling', '-0.1*(y - 25)', 0, 90, 1, 10, '25 + 65*e^(-0.1*x)'], ['y′ = x² + y²', 'x^2 + y^2', 0, 0, 0.1, 1, ''], ['y′ = −2xy²', '-2*x*y^2', 0, 1, 0.1, 2, '1/(1 + x^2)']]), lw=440,
             items=['Grey dashes: the slope field $f(x, y)$', 'Red: Euler\'s polygon; dashed: the exact solution', 'Press $h \\div 2$ and watch the final error halve', 'Tick Heun and RK4 to preview the better methods'],
             notes="Euler for y′ = x + y with h = 0.1 gives y(1) = 3.187485 (error 0.249). With h = 0.05: 3.306595 (0.130), h = 0.025: 3.370128 (0.066). Each halving halves the error: first order."),
        dict(type='table', id='p1', title="Problem 1: Euler's method for $y' = x + y$, $y(0) = 1$",
             q='Use Euler\'s method with $h = 0.1$ to find $y(0.4)$. Compare with the exact solution $y = 2e^x - x - 1$.',
             head=['$n$', '$x_n$', '$y_n$', '$f(x_n, y_n) = x_n + y_n$', '$y_{n+1} = y_n + 0.1f$', 'exact $y(x_{n+1})$', 'error'], frag=True, ans=-1,
             rows=[[0, '0.0', '1.0000', '1.0000', '1.1000', '1.110342', '0.0103'], [1, '0.1', '1.1000', '1.2000', '1.2200', '1.242806', '0.0228'], [2, '0.2', '1.2200', '1.4200', '1.3620', '1.399718', '0.0377'], [3, '0.3', '1.3620', '1.6620', '1.5282', '1.583649', '0.0554']],
             note='$y(0.4) \\approx 1.5282$; the error grows step by step because each step starts from a point that is already wrong.',
             notes="Ask students to predict the error at x = 0.4 with h = 0.05 (about half: 0.029)."),
        dict(type='math', id='heun', title='Modified Euler (Heun): predict, then correct with the average slope',
             eqs=[dict(cap='Predictor (Euler) and corrector (trapezoidal rule)', eq='\\begin{aligned} y^{*}_{n+1} &= y_n + h\\,f(x_n, y_n) \\\\ y_{n+1} &= y_n + \\frac h2\\big[f(x_n, y_n) + f(x_{n+1}, y^{*}_{n+1})\\big] \\end{aligned}'),
                  dict(cap='Error', eq='\\text{local } O(h^3), \\qquad \\text{global } O(h^2)', frag=True)],
             items=['Slope at the start and an estimated slope at the end, averaged', 'Two evaluations of $f$ per step; second order: halve $h$, error $\\div 4$', 'Some textbooks repeat the corrector until it settles (iterated modified Euler)', 'It is the trapezoidal rule of Lecture 20 with a predicted end value'],
             ifrag=True,
             notes="The iterated version converges to the implicit trapezoidal rule y_{n+1} = y_n + (h/2)[f_n + f_{n+1}], which is a fixed-point iteration (Lecture 8) on y_{n+1}."),
        dict(type='bullets', id='algo2', title='Modified Euler (Heun), step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Slope at the start: $k_1 = f(x_n, y_n)$', 'Predict with Euler: $y^{*} = y_n + h\\,k_1$', 'Slope at the predicted end point: $k_2 = f(x_n + h, y^{*})$', 'Correct: $y_{n+1} = y_n + \\dfrac h2(k_1 + k_2)$',
                    '(Optional) recompute $k_2$ with the corrected value and repeat step 4 until two values agree'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input f, x0, y0, h, x_end\nx ← x0;  y ← y0\nwhile x &lt; x_end − h/2:\n    k1 ← f(x, y)\n    yp ← y + h·k1          # predictor\n    k2 ← f(x + h, yp)\n    y ← y + h/2·(k1 + k2)  # corrector\n    x ← x + h\nreturn y</pre></div><p class="small" style="margin-top:14px">Twice the work of Euler per step, but far fewer steps for the same accuracy.</p>'),
             notes="State clearly in written answers whether the corrector is applied once (Heun) or iterated; the numbers differ slightly (1.110000 vs 1.110526 in the first step of Problem 2)."),
        dict(type='worked', id='p2', title='Problem 2: modified Euler for $y\' = x + y$, $y(0) = 1$',
             q='Find $y(0.1)$ and $y(0.2)$ with $h = 0.1$. Then iterate the corrector in the first step.',
             steps=['Step 1: $k_1 = 0 + 1 = 1$; $\\;y^* = 1 + 0.1(1) = 1.1$; $\\;k_2 = 0.1 + 1.1 = 1.2$; $\\;y_1 = 1 + 0.05(1 + 1.2) = 1.11$',
                    'Step 2: $k_1 = 0.1 + 1.11 = 1.21$; $\\;y^* = 1.231$; $\\;k_2 = 0.2 + 1.231 = 1.431$; $\\;y_2 = 1.11 + 0.05(2.641) = 1.24205$',
                    'Iterated corrector in step 1: $1.11 \\to 1 + 0.05(1 + 0.1 + 1.11) = 1.1105 \\to 1.110525 \\to 1.110526$'],
             answer='$y(0.2) \\approx 1.24205$ (exact 1.242806, error $7.6\\times10^{-4}$; Euler\'s error was $2.3\\times10^{-2}$).',
             right=dict(w='ode', o=dict(f='x + y', x0=0, y0=1, h=0.1, xend=0.4, exact='2*e^x - x - 1', methods=['heun', 'euler'], main='heun', only=['euler', 'heun'], height='260px', noexact=True, field=False, compact=True, maxRows=6)), rw=760,
             notes="The iterated corrector converges to 1.110526, which is not the exact 1.110342: iterating removes the predictor error, not the trapezoidal rule's own O(h³) error."),
        dict(type='table', id='error', title='Local and global error: what halving $h$ does', cls='tb',
             head=['$h$', 'Euler $y(1)$', 'error', 'Heun $y(1)$', 'error', 'RK4 (Lecture 22)', 'error'], frag=True,
             rows=[['0.2', '2.976640', '0.460', '3.405416', '$3.1\\times10^{-2}$', '3.43650227', '$6.1\\times10^{-5}$'], ['0.1', '3.187485', '0.249', '3.428162', '$8.4\\times10^{-3}$', '3.43655949', '$4.2\\times10^{-6}$'],
                   ['0.05', '3.306595', '0.130', '3.434382', '$2.2\\times10^{-3}$', '3.43656339', '$2.7\\times10^{-7}$'], ['0.025', '3.370128', '0.066', '3.436008', '$5.6\\times10^{-4}$', '3.43656364', '$1.7\\times10^{-8}$']],
             note='$y\' = x + y$, $y(0) = 1$, exact $y(1) = 3.436564$. Halving $h$ divides the global error by 2 (Euler, order 1), 4 (Heun, order 2) and 16 (RK4, order 4).', notefrag=True,
             notes="Local error = the error made in one step from an exact starting value. Global error = the accumulated error at a fixed x. Global order = local order − 1, because the number of steps is proportional to 1/h."),
        dict(type='compare', id='classic', title='Same kind of problem, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (solve exactly)', tag='Calculus', cls='blue', items=['$y\' = x + y$: linear, integrating factor $e^{-x}$', '$(ye^{-x})\' = xe^{-x}$, so $y = 2e^x - x - 1$', '$y(1) = 3.436564$, exactly']),
             right=dict(h='Numerical (Heun, $h = 0.1$)', tag='Algorithm', cls='key', items=['10 steps, 20 evaluations of $f$', '$y(1) = 3.428162$ (error 0.008)', 'Same code for any $f(x, y)$']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>$y\' = x^2 + y^2$, $y(0) = 0$ (a Riccati equation)</h3><p>No elementary formula exists (the solution involves Bessel functions). Numerically: Euler ($h = 0.1$) 0.2925, Heun 0.3518, RK4 0.350234; very accurate value $y(1) = 0.350232$. Most models in science and engineering are like this.</p></div>'),
             notes="Riccati: the exact solution can be written with Bessel functions of order ±1/4 and ±3/4, which have to be computed numerically anyway."),
        dict(type='code', id='code', title='Euler and modified Euler in Python and C', code='eulerheun', lw=560,
             items=['Both methods for $y\' = x + y$, $h = 0.1$', 'Prints each step with the exact value', 'Change <code>f</code> for any other equation', 'Lab: the tea-cooling model'],
             notes="Run both tabs and compare with Problems 1 and 2."),
        dict(type='widget', id='fail', title='Limitations shown failing', kick='When Euler goes wrong', w='ode',
             o=dict(f='-20*y', x0=0, y0=1, h=0.12, xend=1, exact='e^(-20*x)', methods=['euler'], only=['euler', 'heun', 'rk4'], height='280px', side=True, tableHeight='280px',
                    presets=[['h = 0.02 (fine)', '-20*y', 0, 1, 0.02, 1, 'e^(-20*x)'], ['h = 0.08 (oscillates)', '-20*y', 0, 1, 0.08, 1, 'e^(-20*x)'], ['h = 0.12 (explodes)', '-20*y', 0, 1, 0.12, 1, 'e^(-20*x)'], ['long run drifts', 'x + y', 0, 1, 0.5, 3, '2*e^x - x - 1']]), lw=520,
             items=['$y\' = -20y$: the true solution decays to 0 almost at once', 'Euler multiplies $y$ by $(1 - 20h)$ each step: $h = 0.12$ gives $-1.4$, so the numbers <b>explode</b>', '<b>Stability</b> needs $|1 + h\\lambda| < 1$, i.e. $h < 0.1$ here, whatever the accuracy',
                    'First order is slow: halving the error doubles the work'],
             frag=True,
             notes="h = 0.02: factor 0.6, smooth decay. h = 0.08: factor −0.6, decaying oscillation (wrong shape). h = 0.12: factor −1.4, grows like 1.4ⁿ.\n\nThis is the first glimpse of stiffness, treated properly in Lecture 22. Tick RK4 on the h = 0.12 preset: RK4 is stable up to h ≈ 0.139 here (|hλ| < 2.785)."),
        dict(type='exam', id='practice', src='Problem 3',
             q='"Given $\\dfrac{dy}{dx} = y - x$, $y(0) = 2$, find $y(0.2)$ by Euler\'s method with $h = 0.1$, then improve the result with the modified Euler method. Compare with the exact solution $y = e^x + x + 1$."',
             tips=['Euler: $y_1 = 2 + 0.1(2) = 2.2$; $\\;y_2 = 2.2 + 0.1(2.2 - 0.1) = 2.41$', 'Modified Euler step 1: $k_1 = 2$, $y^* = 2.2$, $k_2 = 2.1$, $y_1 = 2 + 0.05(4.1) = 2.205$',
                   'Step 2: $k_1 = 2.105$, $y^* = 2.4155$, $k_2 = 2.2155$, $y_2 = 2.205 + 0.05(4.3205) = 2.421025$', 'Exact $e^{0.2} + 1.2 = 2.421403$: errors 0.0114 (Euler) and 0.00038 (modified Euler); present both as tables'],
             notes=""),
        dict(type='profile', id='profile', title='Euler and modified Euler: method profile',
             best=['Teaching, quick sketches, very simple models', 'Heun: modest accuracy (3–4 digits) with little code', 'Euler inside game physics and real-time loops, where speed matters more than accuracy'],
             worst=['Long time spans: errors accumulate (first order)', 'Stiff equations: unstable unless $h$ is tiny', 'Oscillations and orbits: Euler adds energy and spirals outwards (Lecture 22)'],
             suited=['Prototyping a model', 'Heun as a building block: predictor–corrector schemes', 'Taylor and Picard: deriving series solutions by hand; existence proofs'],
             avoid=['Production simulations (use RK4 or adaptive solvers)', 'Stiff problems (use implicit methods)', 'When 6+ digits are needed'],
             verdict='Rule of thumb: <b>Euler to understand, Heun for a quick improvement, RK4 (Lecture 22) for real work</b>.',
             notes="scipy.integrate.solve_ivp uses an adaptive Runge–Kutta pair (RK45) by default, not Euler."),
        dict(type='table', id='compare', title='Comparative analysis: methods for $y\' = f(x, y)$', cls='tb sm',
             head=['Method', 'Needs', 'Evaluations per step', 'Global order', '$y(1)$ error ($y\' = x+y$, $h = 0.1$)', 'Best use'], tx=(0, 1, 5), frag=True,
             rows=[['Taylor (4 terms)', 'derivatives of $f$', 'several formulas', '4', '$\\approx 4\\times10^{-6}$', 'simple $f$, hand work'], ['Picard', 'integrals in closed form', '—', 'series', 'depends on iterations', 'theory, series solutions'],
                   ['Euler', '$f$ only', '1', '1', '0.249', 'teaching, real-time loops'], ['Heun (modified Euler)', '$f$ only', '2', '2', '$8.4\\times10^{-3}$', 'quick, modest accuracy'], ['RK4 (Lecture 22)', '$f$ only', '4', '4', '$4.2\\times10^{-6}$', 'general purpose']],
             note='RK4 matches the Taylor method\'s accuracy using only values of $f$: that is the subject of the next lecture.', notefrag=True,
             notes="Taylor with four terms per step at h = 0.1: local error about h⁵/120 · y⁽⁵⁾ ≈ 1.7e-7 per step; global about 4e-6 at x = 1."),
        dict(type='bridge', id='bridge', lead='Euler and Heun show the principle; real problems need more accuracy, more stability and systems of equations.',
             keep=['Step along the slope: $y_{n+1} = y_n + h \\cdot$(slope)', 'Predictor–corrector idea', 'Local $O(h^{p+1})$ vs global $O(h^p)$', 'Check by halving $h$'],
             rows=[['Low order: many steps for few digits', 'Runge–Kutta: several slopes per step, order 4', 22],
                   ['Slopes from earlier steps are thrown away', 'Multistep: Milne, Adams–Bashforth–Moulton', 22],
                   ['Instability with large steps (stiff problems)', 'Stability regions; implicit methods', 22],
                   ['Real models have several unknowns', 'Systems: the same methods with vectors', 22]],
             notes="All four rows are covered in Lecture 22."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see an ODE being stepped in a real system.',
             items=[
                 dict(ic='🧠', h='ResNets are Euler steps', t='Deep learning meets ODEs',
                      detail=dict(where='deep learning. A residual network block computes $x_{k+1} = x_k + F(x_k, \\theta_k)$: exactly Euler\'s method with $h = 1$ for the ODE $dx/dt = F(x, \\theta(t))$. "Neural ODEs" (2018) replace the stack of layers by an ODE solver.',
                                  steps=['Layer $k$: input $x_k$, learned function $F$ (convolutions + activation)', 'Output $x_k + F(x_k)$: the skip connection is the "$y_n +$" of Euler', 'Many thin layers ≈ small steps; stability of the forward pass ≈ stability of Euler', 'Neural ODEs use adaptive Runge–Kutta solvers and fewer parameters'],
                                  note='This view explains why very deep ResNets train well: each block makes only a small change, like a small Euler step.')),
                 dict(ic='🎮', h='Game physics', t='Moving every object, 60 times a second',
                      detail=dict(where='game engines. Each frame ($h = 1/60$ s) the engine updates velocity from forces and position from velocity: Euler\'s method for Newton\'s second law.',
                                  eq='v_{n+1} = v_n + h\\,\\frac{F_n}{m}, \\qquad x_{n+1} = x_n + h\\,v_{n+1}',
                                  steps=['Using the <i>new</i> velocity for the position ("semi-implicit Euler") keeps orbits and springs from gaining energy', 'Cheap: one force evaluation per object per frame', 'Stiff springs or very fast objects need smaller sub-steps, or they explode: the instability on the limitations slide', 'Accuracy matters less than stability and speed'],
                                  note='Physics engines such as Box2D use semi-implicit Euler for exactly these reasons.')),
                 dict(ic='🔌', h='Charging a capacitor (RC circuit)', t='Circuit simulation with Euler and Heun',
                      detail=dict(where='circuit simulation. A capacitor charging through a resistor from a 5 V source obeys $V\' = (5 - V)/(RC)$; with $RC = 1$ ms and time in ms: $V\' = 5 - V$, $V(0) = 0$.',
                                  w='ode', o=dict(f='5 - y', x0=0, y0=0, h=0.5, xend=5, exact='5 - 5*e^(-x)', methods=['euler', 'heun'], height='220px', noexact=True),
                                  note='With $h = 0.5$ ms Euler runs ahead of the exact curve (2.5 V instead of 1.97 V after the first step); Heun (1.88 V) stays close. SPICE uses implicit trapezoidal steps, the stable relative of Heun.')),
                 dict(ic='🕵️', h='Forensics: time of death', t="Newton's law of cooling, run backwards",
                      detail=dict(where='forensic science. Body temperature cools roughly by Newton\'s law toward the room temperature; measuring the temperature and the cooling rate gives an estimate of the time since death.',
                                  steps=['Model: $T\' = -k(T - T_{room})$, with $k$ estimated from two measurements an hour apart', 'Step the ODE <i>backwards</i> (negative $h$) from the measured temperature until $T$ reaches 37 °C', 'Real models (Henssge\'s nomogram) add body mass and clothing: no closed form, solved numerically', 'Uncertainty in $k$ dominates the numerical error'],
                                  note='A good example of the model error being much larger than the method error: no need for RK4 here.'))],
             notes="The ResNet card is a strong link to the ML course: Euler's method is in every modern image classifier."),
        dict(type='check', id='check', q='One Euler step for $y\' = 2y$, $y(0) = 1$, $h = 0.1$. What is $y_1$?',
             opts=['$1.2$', '$1.1$', '$1.2214$', '$0.2$'], right=0,
             answer='A. $y_1 = 1 + 0.1 \\times 2(1) = 1.2$. The exact value is $e^{0.2} = 1.2214$ (option C); Heun gives $1 + 0.05(2 + 2.4) = 1.22$.',
             notes="Option D is only the increment h·f."),
        dict(type='summary', id='summary', items=[
            'IVP $y\' = f(x, y)$, $y(x_0) = y_0$; every method approximates $\\int f(t, y(t))dt$ over each step',
            'Taylor: expand and differentiate the ODE; Picard: $y^{(k+1)} = y_0 + \\int f(t, y^{(k)})dt$',
            'Euler $y_{n+1} = y_n + hf_n$, global $O(h)$; Heun: predictor + trapezoidal corrector, $O(h^2)$',
            'Too large $h$ can make the solution explode: stability, not only accuracy'],
            hw=['Solve $y\' = -2xy^2$, $y(0) = 1$ to $x = 0.2$ by Euler and by modified Euler ($h = 0.1$). Compare with $y = 1/(1 + x^2)$.', 'Find the first three Picard approximations for $y\' = 1 + xy$, $y(0) = 1$.',
                'Use the Taylor series method (4 terms) to find $y(0.1)$ for $y\' = x^2 + y^2$, $y(0) = 1$.', 'For $y\' = -50y$, find the largest $h$ for which Euler\'s method does not grow. Check it in the lab.'],
            solved='Tea after 10 minutes: Euler ($h = 1$) gives <b>47.66 °C</b>, Heun <b>48.96 °C</b>; the exact value is 48.91 °C. Heun\'s error is 30 times smaller for twice the work.',
            next='<b>ODEs II: Runge–Kutta and predictor–corrector methods.</b> Fourth-order accuracy, multistep methods, stability, stiff equations and systems.',
            notes="Homework answers: Q1: Euler y(0.1) = 1, y(0.2) = 0.98; modified Euler y(0.1) = 0.99, y(0.2) = 0.961366; exact 0.961538. Q2: y1 = 1 + x + x²/2; y2 = 1 + x + x²/2 + x³/3 + x⁴/8. Q3: y' = 1, y'' = 2x + 2yy' = 2, y''' = 2 + 2y'² + 2yy'' = 8, y'''' = 6y'y'' + 2yy''' = 28: y(0.1) = 1 + 0.1 + 0.01 + 0.001333 + 0.000117 = 1.111450. Q4: |1 − 50h| ≤ 1 → h ≤ 0.04."),
    ],
    code={
        'eulerheun': dict(file='euler_heun', py='''# Euler and modified Euler (Heun) for y' = f(x, y)
import math

def f(x, y):
    return x + y

def exact(x):
    return 2 * math.exp(x) - x - 1

x0, y0, h, x_end = 0.0, 1.0, 0.1, 0.4
n = round((x_end - x0) / h)

print(" n    x      Euler       Heun        exact")
xe, ye, xh, yh = x0, y0, x0, y0
for i in range(n):
    ye = ye + h * f(xe, ye)                  # Euler
    k1 = f(xh, yh)                           # Heun: predictor ...
    yp = yh + h * k1
    k2 = f(xh + h, yp)
    yh = yh + h / 2 * (k1 + k2)              # ... and corrector
    xe = xh = x0 + (i + 1) * h
    print(f"{i+1:2d}  {xe:.1f}  {ye:10.6f}  {yh:10.6f}  {exact(xe):10.6f}")
''', c='''/* Euler and modified Euler (Heun) for y' = f(x, y) */
#include <stdio.h>
#include <math.h>

double f(double x, double y) { return x + y; }
double exact(double x) { return 2 * exp(x) - x - 1; }

int main(void) {
    double x0 = 0, y0 = 1, h = 0.1, x_end = 0.4;
    int n = (int)((x_end - x0) / h + 0.5);
    double x = x0, ye = y0, yh = y0;
    printf(" n    x      Euler       Heun        exact\\n");
    for (int i = 0; i < n; i++) {
        ye = ye + h * f(x, ye);                  /* Euler */
        double k1 = f(x, yh);                    /* Heun: predictor ... */
        double yp = yh + h * k1;
        double k2 = f(x + h, yp);
        yh = yh + h / 2 * (k1 + k2);             /* ... and corrector */
        x = x0 + (i + 1) * h;
        printf("%2d  %.1f  %10.6f  %10.6f  %10.6f\\n", i + 1, x, ye, yh, exact(x));
    }
    return 0;
}
'''),
        'cooling': dict(file='tea_cooling', py='''# Tea cooling: dT/dt = -k (T - T_room), T(0) = 90; how does the step size matter?
import math

k, T_room, T0, t_end = 0.1, 25.0, 90.0, 10.0

def f(t, T):
    return -k * (T - T_room)

exact = T_room + (T0 - T_room) * math.exp(-k * t_end)
print(f"exact T(10) = {exact:.4f}")
for h in [2.0, 1.0, 0.5, 0.25]:
    n = round(t_end / h)
    Te, Th, t = T0, T0, 0.0
    for i in range(n):
        Te = Te + h * f(t, Te)
        k1 = f(t, Th)
        k2 = f(t + h, Th + h * k1)
        Th = Th + h / 2 * (k1 + k2)
        t += h
    print(f"h = {h:4.2f}: Euler {Te:8.4f} (error {abs(Te - exact):.4f})   Heun {Th:8.4f} (error {abs(Th - exact):.5f})")
''', c='''/* Tea cooling: dT/dt = -k (T - T_room), T(0) = 90; how does the step size matter? */
#include <stdio.h>
#include <math.h>

double k = 0.1, T_room = 25.0;
double f(double t, double T) { return -k * (T - T_room); }

int main(void) {
    double T0 = 90, t_end = 10, hs[4] = {2.0, 1.0, 0.5, 0.25};
    double exact = T_room + (T0 - T_room) * exp(-k * t_end);
    printf("exact T(10) = %.4f\\n", exact);
    for (int r = 0; r < 4; r++) {
        double h = hs[r], Te = T0, Th = T0, t = 0;
        int n = (int)(t_end / h + 0.5);
        for (int i = 0; i < n; i++) {
            Te = Te + h * f(t, Te);
            double k1 = f(t, Th), k2 = f(t + h, Th + h * k1);
            Th = Th + h / 2 * (k1 + k2);
            t += h;
        }
        printf("h = %4.2f: Euler %8.4f (error %.4f)   Heun %8.4f (error %.5f)\\n", h, Te, fabs(Te - exact), Th, fabs(Th - exact));
    }
    return 0;
}
'''),
    },
    lab=dict(title='Euler and Heun Lab',
             intro='Step your own differential equations with Euler and modified Euler, see the slope field, and measure how the error depends on h.',
             tabs=[
                 dict(name='ODE solver', blocks=[
                     dict(p='Type y′ = f(x, y) (use x and y), the initial point, the step h and the end point. Give the exact solution if you know it. The table shows every step of the first ticked method.'),
                     dict(w='ode', o=dict(f='y - x', x0=0, y0=2, h=0.1, xend=0.2, exact='e^x + x + 1', methods=['euler', 'heun'], height='320px', side=True, tableHeight='320px',
                                          presets=[['Problem 3', 'y - x', 0, 2, 0.1, 0.2, 'e^x + x + 1'], ['y′ = x + y', 'x + y', 0, 1, 0.1, 1, '2*e^x - x - 1'], ['homework 1', '-2*x*y^2', 0, 1, 0.1, 0.2, '1/(1 + x^2)'], ['tea', '-0.1*(y - 25)', 0, 90, 1, 10, '25 + 65*e^(-0.1*x)'], ['stiff', '-50*y', 0, 1, 0.05, 0.5, 'e^(-50*x)']]))]),
                 dict(name='Code', blocks=[
                     dict(h='Euler and Heun'), dict(code='eulerheun', tasks=['Run it. Compare with Problems 1 and 2.', 'Change f to y - x with y0 = 2 (Problem 3).', 'Halve h. By what factor does each error shrink?']),
                     dict(h='Step size study'), dict(code='cooling', tasks=['Run it. Confirm the orders 1 and 2 from the error ratios.', 'Set k = 2 and h = 1.5. What happens to Euler, and why?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Derive Euler\'s method from Taylor\'s series and state its error.', '$y(x+h) = y(x) + hy\'(x) + \\frac{h^2}{2}y\'\'(\\xi)$; dropping the last term and using $y\' = f(x, y)$ gives $y_{n+1} = y_n + hf(x_n, y_n)$. Local error $O(h^2)$, global $O(h)$.'),
                         ('Find the first two Picard approximations for $y\' = x + y$, $y(0) = 1$.', '$y^{(1)} = 1 + \\int_0^x(t + 1)dt = 1 + x + \\frac{x^2}{2}$; $y^{(2)} = 1 + \\int_0^x(t + 1 + t + \\frac{t^2}{2})dt = 1 + x + x^2 + \\frac{x^3}{6}$.'),
                         ('Explain the modified Euler method.', 'Predict $y^* = y_n + hf(x_n, y_n)$ with Euler, then correct with the average of the slopes at the two ends: $y_{n+1} = y_n + \\frac h2[f(x_n, y_n) + f(x_{n+1}, y^*)]$. It is the trapezoidal rule for $\\int f\\,dx$; global error $O(h^2)$.'),
                         ('What is the difference between local and global truncation error?', 'Local: the error made in a single step starting from the exact value. Global: the total error at a given $x$ after all steps. With $n \\propto 1/h$ steps, a local error $O(h^{p+1})$ accumulates to a global error $O(h^p)$.'),
                         ('Why does Euler\'s method blow up for $y\' = -20y$ with $h = 0.12$?', 'Each step multiplies $y$ by $1 - 20h = -1.4$, whose size exceeds 1, so $|y_n|$ grows like $1.4^n$ although the true solution decays. Euler is stable for this equation only when $|1 - 20h| < 1$, i.e. $h < 0.1$.')])])]),
)
