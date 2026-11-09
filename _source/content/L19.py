LECTURE = dict(
    title='Numerical Differentiation',
    short='Numerical Differentiation',
    sub='Slopes from data and from black-box functions: forward, backward and central differences from Taylor series, derivative formulas from Newton\'s interpolation, Richardson extrapolation, and why differentiation is the one operation that amplifies noise.',
    slides=[
        dict(type='cover', id='cover', notes="Opening question: 'Your phone's GPS gives positions once a second. How does the map app know your speed?' It differentiates data. Today: how, and how accurately.\n\nThis lecture builds on Taylor series (Lecture 3), the error trade-off (Lecture 4) and the operators (Lectures 15–16)."),
        dict(type='bullets', id='hook', title='The problem: speed and braking from position data', kick='Why this lecture', rw=640,
             lead='A delivery robot is braking. Its position $y$ (metres) is logged every 0.1 s. What are its speed and deceleration at $t = 1.1$ s?',
             items=['Speed is $dy/dt$ and acceleration is $d^2y/dt^2$, but there is <b>no formula</b> for $y(t)$, only a table', 'A simple slope between neighbours gives one estimate; which neighbours, and how accurate?',
                    'Smaller steps should help, yet real sensors add noise: does a smaller step make it worse?', 'Same question in ML: the slope of a loss with respect to a weight'],
             frag=True,
             right=dict(table=[['$t$ (s)', '$y$ (m)'], [['1.0', '7.989'], ['1.1', '8.403'], ['1.2', '8.781'], ['1.3', '9.129'], ['1.4', '9.451'], ['1.5', '9.750'], ['1.6', '10.031']]]),
             notes="Classic textbook table, presented as robot data. Solved during the lecture: speed 3.952 m/s, deceleration 3.74 m/s² at t = 1.1 s (Problem 1).\n\nThe noise question is answered on the limitations slide: with 1 mm of noise, a second derivative can be completely wrong."),
        dict(type='goals', id='goals', items=[
            'Derive forward, backward and central difference formulas and their errors from <b>Taylor series</b>',
            'Differentiate tabulated data with <b>Newton\'s forward and backward formulas</b>',
            'Improve an estimate with <b>Richardson extrapolation</b>',
            'Choose the step size $h$, balancing truncation and round-off',
            'Explain why differentiation <b>amplifies noise</b>, and what to do about it'],
            prev='Interpolation: values between table entries.',
            today='Slopes and curvature from the same tables, and from functions we can only evaluate.',
            notes="Module 5 starts here. Next lecture (integration) is the 'friendly' twin: integration smooths errors, differentiation amplifies them."),
        dict(type='math', id='derive', title='Difference formulas from Taylor series',
             eqs=[dict(cap='Forward and backward: first order', eq='\\begin{aligned} f\'(x) &= \\frac{f(x+h) - f(x)}{h} - \\frac{h}{2}f\'\'(\\xi) \\\\ f\'(x) &= \\frac{f(x) - f(x-h)}{h} + \\frac{h}{2}f\'\'(\\xi) \\end{aligned}'),
                  dict(cap='Central: subtract the two Taylor series, the h² terms cancel', eq='f\'(x) = \\frac{f(x+h) - f(x-h)}{2h} - \\frac{h^2}{6}f\'\'\'(\\xi)', frag=True),
                  dict(cap='Second derivative: add the two series', eq='f\'\'(x) = \\frac{f(x+h) - 2f(x) + f(x-h)}{h^2} - \\frac{h^2}{12}f^{(4)}(\\xi)', frag=True)],
             items=['Forward and backward: error $O(h)$; central: $O(h^2)$, same number of evaluations', 'Halve $h$: forward error halves, central error quarters', 'Second derivative: the discrete Laplacian of Lecture 14\'s heat plate', 'All from Lecture 3: $f(x \\pm h) = f \\pm hf\' + \\tfrac{h^2}{2}f\'\' \\pm \\tfrac{h^3}{6}f\'\'\' + \\cdots$'],
             ifrag=True, rw=600,
             notes="Do the central derivation on the board: f(x+h) − f(x−h) = 2hf' + (h³/3)f''' + …, divide by 2h.\n\nOne-sided formulas are needed at the ends of a table, where no point exists on one side."),
        dict(type='math', id='ops', title='Derivatives from Newton\'s formulas (operators)',
             eqs=[dict(cap='Operator route (Lecture 15): take the logarithm of E = 1 + Δ', eq='hD = \\ln(1 + \\Delta) = \\Delta - \\frac{\\Delta^2}{2} + \\frac{\\Delta^3}{3} - \\frac{\\Delta^4}{4} + \\cdots'),
                  dict(cap='Square it for the second derivative', eq='h^2D^2 = \\Delta^2 - \\Delta^3 + \\frac{11}{12}\\Delta^4 - \\frac{5}{6}\\Delta^5 + \\cdots', frag=True),
                  dict(cap='Backward forms, for the end of a table', eq='hD = \\nabla + \\frac{\\nabla^2}{2} + \\frac{\\nabla^3}{3} + \\cdots, \\qquad h^2D^2 = \\nabla^2 + \\nabla^3 + \\frac{11}{12}\\nabla^4 + \\cdots', frag=True)],
             items=['Apply to $y_0$: $y\'(x_0) = \\frac1h\\big(\\Delta y_0 - \\tfrac12\\Delta^2y_0 + \\tfrac13\\Delta^3y_0 - \\cdots\\big)$', 'Equivalent: differentiate Newton\'s forward formula and put $p = 0$', 'Use the forward form near the start, backward near the end', 'The first term alone is the forward difference $\\Delta y_0/h$'],
             ifrag=True, rw=600,
             notes="Two routes, same result. Route 1 (operators): one line. Route 2 (calculus): dy/dx = (1/h) dy/dp, differentiate the forward formula term by term and set p = 0. Ask students to verify the Δ³ coefficient by route 2: d/dp [p(p−1)(p−2)/6] at p = 0 is 2/6 = 1/3."),
        dict(type='bullets', id='algo', title='Derivatives from a table, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Check equal spacing; note $h$', 'Build the difference table', 'Choose the formula: forward near the start, backward near the end, central in the middle', 'Read the diagonal through the point $x_0$ where the derivative is wanted',
                    'Add the series terms $\\frac1h(\\Delta - \\tfrac12\\Delta^2 + \\tfrac13\\Delta^3 - \\cdots)$ until they are negligible; for $y\'\'$ use $\\frac{1}{h^2}(\\Delta^2 - \\Delta^3 + \\tfrac{11}{12}\\Delta^4 - \\cdots)$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 26px/1.55 var(--mono);color:#f5f3ee">input y[0..n] (step h), i  # point x_i\nbuild differences d[k] = Δᵏ y_i\nd1 ← 0;  sign ← +1\nfor k = 1 … n−i:\n    d1 ← d1 + sign·d[k] / k\n    sign ← −sign\nd2 ← d[2] − d[3] + 11/12·d[4]\n      − 5/6·d[5]          # if present\nreturn d1/h,  d2/h²</pre></div><p class="small" style="margin-top:14px">For a point in the middle of the table, the two-point central formulas are usually enough.</p>'),
             notes="Step 5: the terms must shrink. If they do not (for example, they grow because the data are noisy), stop early: higher differences of noisy data are mostly noise."),
        dict(type='widget', id='explore', title='Explore: secants approaching the tangent', w='numdiff', o=dict(f='sin(x)', x0=1, logh=-1, height='260px',
             presets=[['sin x at 1', 'sin(x)', 1], ['eˣ at 0', 'e^x', 0], ['x³ at 2', 'x^3', 2], ['√x at 0.01', 'sqrt(x)', 0.01]]), lw=440,
             items=['Orange: forward secant; blue: central secant; green: the true tangent', 'Move $h$ from $10^{-1}$ to $10^{-5}$: compare how fast each error falls', 'Below $10^{-6}$ the errors grow again: round-off', 'Richardson combines two central estimates into a far better one'],
             notes="At h = 0.1 for sin at 1: forward error 4.3e-2, central 9.0e-4, Richardson 1.8e-6. At h = 1e-6: forward 4.2e-7, central 2.8e-11. At h = 1e-8 and below everything degrades (Lecture 4's V-shaped curve).\n\n√x at 0.01 shows a function whose derivatives are huge near 0: the central formula needs h much smaller than 0.01."),
        dict(type='worked', id='p1', title='Problem 1: speed and deceleration at $t = 1.1$',
             q='From the robot table, find $y\'(1.1)$ and $y\'\'(1.1)$ with Newton\'s forward formula ($h = 0.1$).',
             steps=['Forward differences at $t = 1.1$: $\\Delta y = 0.378$, $\\Delta^2 y = -0.030$, $\\Delta^3 y = 0.004$, $\\Delta^4 y = -0.001$, $\\Delta^5 y = 0.003$',
                    '$y\' = \\dfrac{1}{0.1}\\Big(0.378 + \\dfrac{0.030}{2} + \\dfrac{0.004}{3} + \\dfrac{0.001}{4} + \\dfrac{0.003}{5}\\Big) = 10(0.39518)$',
                    '$y\'\' = \\dfrac{1}{0.01}\\Big(-0.030 - 0.004 + \\dfrac{11}{12}(-0.001) - \\dfrac56(0.003)\\Big) = 100(-0.037417)$'],
             answer='Speed $y\'(1.1) \\approx 3.952$ m/s; acceleration $y\'\'(1.1) \\approx -3.74$ m/s² (braking).',
             right=dict(w='difftab', o=dict(y='8.403 8.781 9.129 9.451 9.75 10.031', x0=1.1, h=0.1, noerr=True, fixed=True, height='330px')), rw=760,
             notes="Point out that the Δ⁵ term (0.003) is larger than the Δ⁴ term (0.001): the data are rounded to 3 decimals, so the high differences are mostly rounding noise. A careful answer stops after Δ³ or Δ⁴: 3.946 or 3.950; textbooks quote 3.952.\n\nThe second derivative is much more sensitive: dividing by h² = 0.01 multiplies every rounding error in the third decimal by 100."),
        dict(type='worked', id='p2', title='Problem 2: central and backward formulas',
             q='From the same table, estimate $y\'(1.3)$ and $y\'\'(1.3)$ with the central formulas, and $y\'(1.6)$ with the backward formula.',
             steps=['Central: $y\'(1.3) \\approx \\dfrac{9.451 - 8.781}{0.2} = 3.350$', '$y\'\'(1.3) \\approx \\dfrac{9.451 - 2(9.129) + 8.781}{0.01} = -2.60$',
                    'Backward at 1.6: $\\nabla y = 0.281$, $\\nabla^2 y = -0.018$, $\\nabla^3 y = 0.005$: $\\;y\' \\approx 10\\big(0.281 - 0.009 + 0.0017\\big) = 2.74$'],
             answer='$y\'(1.3) \\approx 3.35$ m/s, $y\'\'(1.3) \\approx -2.6$ m/s², $y\'(1.6) \\approx 2.74$ m/s: the robot is slowing down.',
             notes="Using more backward terms gives 2.751; the extra terms are rounding noise again.\n\nCentral formulas use only two (or three) values and are usually as good as long forward series in the middle of a table."),
        dict(type='math', id='richardson', title='Richardson extrapolation: cancel the leading error',
             eqs=[dict(cap='Central difference with step h has error c·h² + O(h⁴)', eq='\\begin{aligned} D(h) &= f\'(x) + ch^2 + O(h^4) \\\\ D(h/2) &= f\'(x) + \\tfrac14 ch^2 + O(h^4) \\end{aligned}'),
                  dict(cap='Combine to remove the h² term', eq='f\'(x) \\approx D(h/2) + \\frac{D(h/2) - D(h)}{3} \\qquad (\\text{error } O(h^4))', frag=True)],
             items=['$\\sin$ at 1: $D(0.2) = 0.536707$, $D(0.1) = 0.539402$', '$R = 0.539402 + (0.539402 - 0.536707)/3 = 0.540301$; true $\\cos 1 = 0.540302$', 'Error drops from $9\\times10^{-4}$ to $1.8\\times10^{-6}$ for two extra evaluations',
                    'Same as the five-point formula $\\frac{-f_2 + 8f_1 - 8f_{-1} + f_{-2}}{12h}$; same idea gives Romberg integration (Lecture 20)'],
             ifrag=True,
             notes="General rule: if the error is c·h^p, then D(h/2) + (D(h/2) − D(h))/(2^p − 1). For central differences p = 2, so divide by 3.\n\nIt works only if the error really behaves like c·h^p, i.e. for smooth functions and h not too small (no round-off yet)."),
        dict(type='compare', id='classic', title='Same slope, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (differentiate the formula)', tag='Calculus', cls='blue', items=['$f(x) = x^x$: write $e^{x\\ln x}$, then $f\'(x) = x^x(1 + \\ln x)$', 'At $x = 2$: $4(1 + 0.693147) = 6.772589$', 'Exact, but needs a formula and the rules of calculus']),
             right=dict(h='Numerical (central difference)', tag='Algorithm', cls='key', items=['$\\dfrac{f(2.001) - f(1.999)}{0.002} = 6.772593$', 'Needs only values of $f$', 'Same code for any function, table or program']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>The robot\'s position table, or a simulation</h3><p>There is no formula for $y(t)$ to differentiate, only seven numbers. The same holds when $f$ is the output of a simulation or a trained model: finite differences work on values alone (and in ML they check the gradients computed by backpropagation).</p></div>'),
             notes="x^x numbers: (2.001^2.001 − 1.999^1.999)/0.002 = 6.772593 (error about 5e-6, consistent with h²/6 · f''')."),
        dict(type='code', id='code', title='Derivatives from a table, and Richardson, in Python and C', code='numdiff', lw=560,
             items=['Forward-series derivative from the difference table', 'Central first and second derivatives', 'Richardson extrapolation for $\\sin$ at 1', 'Prints each term, as in a written solution'],
             notes="Run both tabs. Lab: change h in the Richardson part to 1e-3, 1e-5, 1e-7 and watch the round-off appear."),
        dict(type='widget', id='fail', title='Limitations shown failing', kick='When differentiation goes wrong', w='numdiff', o=dict(f='sin(x)', x0=1, logh=-11, height='205px',
             presets=[['h too small', 'sin(x)', 1], ['steep: √x at 0.001', 'sqrt(x)', 0.001], ['kink: |x| at 0', 'abs(x)', 0]]), lw=560,
             items=['<b>Round-off</b>: at $h = 10^{-11}$ the central error is $10^{-6}$, worse than at $h = 10^{-5}$ ($10^{-11}$); the second derivative is useless (Lecture 4)', '<b>Noise</b>: positions with 1 mm noise (sampled every 0.01 s) give speed errors up to 0.2 m/s and acceleration errors larger than the acceleration itself (54 vs 39 m/s²)',
                    '<b>Kinks</b>: at a corner (|x| at 0) the derivative does not exist; the central formula quietly reports 0', 'Dividing by $h$ (or $h^2$) multiplies every data error by $1/h$ (or $1/h^2$)'],
             frag=True,
             notes="Noise numbers from a simulation: y = sin(2πt) sampled every 0.01 s with Gaussian noise of standard deviation 0.001. Central first derivative: max error 0.20 (true speeds up to 6.3). Central second derivative: max error 54, larger than the true maximum 39.\n\nFixes: smooth first (least-squares fit, Lecture 23; Savitzky–Golay filter), use a larger h, or avoid differentiating data at all (integrate instead, or use automatic differentiation for formulas)."),
        dict(type='exam', id='practice', src='Problem 3',
             q='"From the table $x$: 0, 1, 2, 3, 4, 5 and $y$: 4, 8, 15, 7, 6, 2, find $\\dfrac{dy}{dx}$ and $\\dfrac{d^2y}{dx^2}$ at $x = 0$."',
             tips=['Build the difference table; top diagonal: $\\Delta y_0 = 4$, $\\Delta^2 = 3$, $\\Delta^3 = -18$, $\\Delta^4 = 40$, $\\Delta^5 = -72$', 'State the formulas: $y\' = \\frac1h(\\Delta - \\frac{\\Delta^2}{2} + \\frac{\\Delta^3}{3} - \\frac{\\Delta^4}{4} + \\frac{\\Delta^5}{5})$ and $y\'\' = \\frac{1}{h^2}(\\Delta^2 - \\Delta^3 + \\frac{11}{12}\\Delta^4 - \\frac56\\Delta^5)$',
                   'Substitute with $h = 1$: $y\'(0) = 4 - 1.5 - 6 - 10 - 14.4 = -27.9$; $\\;y\'\'(0) = 3 + 18 + 36.67 + 60 = 117.67$', 'Comment: the differences grow, so the series converges badly and the answer is unreliable; the data are far from smooth'],
             notes=""),
        dict(type='profile', id='profile', title='Numerical differentiation: method profile',
             best=['Smooth functions you can evaluate anywhere: central difference with $h \\approx 10^{-5}$ gives about 10 digits', 'Richardson: $O(h^4)$ for two extra evaluations', 'Smooth, accurate tables: the difference series converges quickly'],
             worst=['Noisy measurements: errors grow like noise$/h$ or noise$/h^2$', '$h$ too small: round-off (Lecture 4)', 'Corners and jumps: the derivative does not exist'],
             suited=['Gradient checking in machine learning', 'Velocity and acceleration from smooth sensor data', 'Finite-difference methods for differential equations (heat, waves)', 'Jacobians for Newton\'s method when no formula is available'],
             avoid=['Raw noisy data (smooth or fit first, Lecture 23)', 'When an exact derivative is available cheaply (use it, or automatic differentiation)', 'High-order derivatives from tables'],
             verdict='Rule of thumb: <b>central differences with $h \\approx \\varepsilon^{1/3}|x|$; Richardson for more accuracy; smooth before differentiating data</b>.',
             notes="ε^{1/3} ≈ 6×10⁻⁶ for doubles: the optimum of truncation h² and round-off ε/h (Lecture 4)."),
        dict(type='table', id='compare', title='Comparative analysis: derivative formulas for $\\sin$ at 1, $h = 0.1$', cls='tb sm',
             head=['Formula', 'Points used', 'Order', 'Estimate', 'Error', 'Use'], tx=(0, 5), frag=True,
             rows=[['Forward $\\frac{f_1 - f_0}{h}$', '2', '$O(h)$', '0.497364', '$4.3\\times10^{-2}$', 'start of a table'], ['Backward $\\frac{f_0 - f_{-1}}{h}$', '2', '$O(h)$', '0.581441', '$4.1\\times10^{-2}$', 'end of a table, real-time data'],
                   ['Central $\\frac{f_1 - f_{-1}}{2h}$', '2', '$O(h^2)$', '0.539402', '$9.0\\times10^{-4}$', 'default inside'], ['Five-point / Richardson', '4', '$O(h^4)$', '0.540301', '$1.8\\times10^{-6}$', 'high accuracy, smooth $f$'],
                   ['Newton forward series', 'many', 'up to $O(h^n)$', '—', '—', 'tables, written problems']],
             note='True value $\\cos 1 = 0.540302$. More points buy higher order, but also more sensitivity to noise in the data.', notefrag=True,
             notes="All numbers computed with the lab widget at h = 0.1."),
        dict(type='bridge', id='bridge', lead='Differentiation works well for smooth functions and badly for noisy data. Its siblings fix or avoid the weaknesses:',
             keep=['Central differences: $O(h^2)$ for two evaluations', 'Richardson extrapolation', 'Formulas from Taylor or from Newton\'s series', 'Error control by the choice of $h$'],
             rows=[['Integration is the stable inverse: it averages noise', 'Trapezoidal, Simpson, Romberg', 20],
                   ['Derivatives appear inside equations: $y\' = f(x, y)$', 'ODE methods (Euler, Runge–Kutta)', 21],
                   ['Noisy data', 'Fit a smooth model first: least squares', 23],
                   ['Millions of derivatives of one loss', 'Automatic differentiation; gradient descent', 25]],
             notes="Automatic differentiation (as in PyTorch) is not finite differences: it applies the chain rule to the program and is exact up to rounding. Finite differences are used to check it."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see where a difference formula is applied.',
             items=[
                 dict(ic='🧠', h='Gradient checking in deep learning', t='Is my backpropagation correct?',
                      detail=dict(where='debugging neural-network code. Backpropagation computes $\\partial L/\\partial w$ analytically; a bug gives wrong gradients that still train badly. The check: compare with a central difference for a few weights.',
                                  eq='\\frac{\\partial L}{\\partial w} \\approx \\frac{L(w + \\epsilon) - L(w - \\epsilon)}{2\\epsilon}, \\qquad \\epsilon \\approx 10^{-4} \\text{ to } 10^{-6}',
                                  steps=['Example: $L(w) = (2w - 3)^2$ at $w = 1$; backprop says $\\partial L/\\partial w = 2(2w - 3)\\cdot 2 = -4$', 'Central difference with $\\epsilon = 10^{-4}$: $-3.9999999999996$', 'Relative difference below $10^{-7}$: the gradient code is right', 'Forward differences are not good enough here: their $O(\\epsilon)$ error hides small bugs'],
                                  note='Andrew Ng\'s deep-learning course and PyTorch\'s <code>torch.autograd.gradcheck</code> use exactly this test.')),
                 dict(ic='❤️', h='Heartbeat detection in ECG', t='The Pan–Tompkins derivative stage',
                      detail=dict(where='medical signal processing. The Pan–Tompkins QRS detector (1985), still the reference algorithm, differentiates the filtered ECG to emphasise the steep QRS slopes, then squares and averages.',
                                  eq='y[n] = \\frac{1}{8T}\\big(-x[n-2] - 2x[n-1] + 2x[n+1] + x[n+2]\\big)',
                                  steps=['Band-pass filter the ECG (removes drift and noise first: differentiation amplifies noise)', 'Apply the five-point derivative above (a smoothed central difference)', 'Square and integrate over a moving window', 'Peaks above an adaptive threshold are heartbeats'],
                                  note='Notice the order: smooth first, then differentiate. That is the remedy from the limitations slide.')),
                 dict(ic='🔥', h='Simulating heat flow', t='The finite-difference method',
                      detail=dict(where='engineering simulation of heat and diffusion, $u_t = \\alpha u_{xx}$. Replace the second derivative in space by the central formula and step forward in time.',
                                  eq='\\frac{u_i^{new} - u_i}{\\Delta t} = \\alpha\\,\\frac{u_{i+1} - 2u_i + u_{i-1}}{\\Delta x^2}',
                                  steps=['Divide the rod into points $\\Delta x$ apart', 'Second derivative at each point: central formula, error $O(\\Delta x^2)$', 'Step in time (Euler, Lecture 21): stable only if $\\alpha\\Delta t/\\Delta x^2 \\le \\tfrac12$', 'Implicit versions need a tridiagonal solve per step (Lecture 13)'],
                                  note='The same discrete Laplacian gave the plate equations of Lectures 12–14.')),
                 dict(ic='🛰️', h='Velocity from GPS and IMU', t='Phones, drones and sports trackers',
                      detail=dict(where='navigation. GPS gives positions once per second; differences give speed. Inertial sensors (IMU) give acceleration, which is integrated instead (Lecture 20). Fusion filters combine both.',
                                  steps=['Speed: backward difference of the latest positions (real time: no future points)', 'Raw GPS noise is a few metres, so one-second differences are noisy', 'Smoothing (moving average or Kalman filter) before or after differencing', 'Acceleration from GPS is too noisy; it comes from the accelerometer'],
                                  note='Real-time systems must use backward differences: the next sample has not arrived yet.'))],
             notes="The gradient-checking card is a good place to mention automatic differentiation again: exact gradients from the chain rule, checked by finite differences."),
        dict(type='check', id='check', q='$f(1.9) = 3.61$, $f(2.0) = 4.00$, $f(2.1) = 4.41$. What is the central-difference estimate of $f\'(2)$?',
             opts=['$4.0$', '$3.9$', '$4.1$', '$8.0$'], right=0,
             answer='A. $\\dfrac{4.41 - 3.61}{0.2} = 4.0$ (exact for $f = x^2$). Forward gives $4.1$, backward $3.9$.',
             notes="Option D divides 0.8 by h instead of 2h. Options B and C are the backward and forward differences."),
        dict(type='summary', id='summary', items=[
            'Forward/backward $O(h)$, central $O(h^2)$, second derivative $\\frac{f_1 - 2f_0 + f_{-1}}{h^2}$',
            'Tables: $y\' = \\frac1h(\\Delta - \\frac{\\Delta^2}{2} + \\frac{\\Delta^3}{3} - \\cdots)$, $y\'\' = \\frac{1}{h^2}(\\Delta^2 - \\Delta^3 + \\frac{11}{12}\\Delta^4 - \\cdots)$',
            'Richardson: $D(h/2) + \\frac{D(h/2) - D(h)}{3}$ gives $O(h^4)$',
            'Differentiation amplifies noise and round-off: choose $h$ carefully, smooth data first'],
            hw=['From $x$: 0, 0.1, 0.2, 0.3, 0.4 and $y = e^x$: 1.0000, 1.1052, 1.2214, 1.3499, 1.4918, find $y\'(0)$ and $y\'\'(0)$. Compare with 1.', 'Use Richardson extrapolation with $h = 0.2$ and $0.1$ to estimate the derivative of $\\ln x$ at $x = 2$.',
                'Derive the central second-derivative formula and its error term from Taylor series.', 'In the lab, find the best $h$ for the forward and the central formula for $e^x$ at $x = 1$. Compare with $\\sqrt{\\varepsilon}$ and $\\varepsilon^{1/3}$.'],
            solved='Forward series from the table: speed <b>3.952 m/s</b> and acceleration <b>−3.74 m/s²</b> at $t = 1.1$ s. Central formulas give 3.35 m/s and −2.6 m/s² at 1.3 s: the robot is braking.',
            next='<b>Numerical integration.</b> Areas, distances and probabilities from the same kind of tables: trapezoidal, Simpson, Romberg and Gauss.',
            notes="Homework answers: Q1: Δ: 0.1052, 0.1162, 0.1285, 0.1419; Δ²: 0.0110, 0.0123, 0.0134; Δ³: 0.0013, 0.0011; Δ⁴: −0.0002. y'(0) = 10(0.1052 − 0.0055 + 0.000433 + 0.00005) = 1.0018; y''(0) = 100(0.0110 − 0.0013 − 0.00018) = 0.952 (true 1; rounding to 4 decimals limits y''). Q2: D(0.2) = 0.501677, D(0.1) = 0.500417, R = 0.499997 (true 0.5). Q4: forward best near 1e-8, central near 1e-5."),
    ],
    code={
        'numdiff': dict(file='numerical_derivative', py='''# Derivatives from a table (Newton forward series) and Richardson extrapolation
import math

y = [7.989, 8.403, 8.781, 9.129, 9.451, 9.750, 10.031]   # t = 1.0, 1.1, ..., 1.6
h = 0.1
i = 1                                                     # derivative at t = 1.1

d = [y[i:]]                                               # d[k][0] = Delta^k y_i
while len(d[-1]) > 1:
    prev = d[-1]
    d.append([prev[j + 1] - prev[j] for j in range(len(prev) - 1)])
first = 0.0
for k in range(1, len(d)):
    term = (-1) ** (k + 1) * d[k][0] / k
    first += term
    print(f"k={k}  Delta^k y = {d[k][0]:8.4f}  term = {term:9.5f}")
second = d[2][0] - d[3][0] + 11 / 12 * d[4][0] - 5 / 6 * d[5][0]
print(f"y'(1.1)  = {first / h:.4f}")
print(f"y''(1.1) = {second / h**2:.4f}")

print("central at t = 1.3:", f"{(y[4] - y[2]) / (2 * h):.4f}", f"{(y[4] - 2 * y[3] + y[2]) / h**2:.4f}")

f = math.sin                                              # Richardson for sin at x = 1
x = 1.0
D1 = (f(x + 0.2) - f(x - 0.2)) / 0.4
D2 = (f(x + 0.1) - f(x - 0.1)) / 0.2
R = D2 + (D2 - D1) / 3
for name, v in [("D(0.2)", D1), ("D(0.1)", D2), ("Richardson", R)]:
    print(f"{name:10s} = {v:.8f}   error = {abs(v - math.cos(x)):.2e}")
''', c='''/* Derivatives from a table (Newton forward series) and Richardson extrapolation */
#include <stdio.h>
#include <math.h>
#define N 7

int main(void) {
    double y[N] = {7.989, 8.403, 8.781, 9.129, 9.451, 9.750, 10.031};   /* t = 1.0 ... 1.6 */
    double h = 0.1, d[N][N];
    int i = 1, m = N - i;                       /* derivative at t = 1.1 */
    for (int j = 0; j < m; j++) d[0][j] = y[i + j];
    for (int k = 1; k < m; k++)
        for (int j = 0; j < m - k; j++) d[k][j] = d[k - 1][j + 1] - d[k - 1][j];

    double first = 0, sign = 1;
    for (int k = 1; k < m; k++) {
        double term = sign * d[k][0] / k;
        first += term;
        printf("k=%d  Delta^k y = %8.4f  term = %9.5f\\n", k, d[k][0], term);
        sign = -sign;
    }
    double second = d[2][0] - d[3][0] + 11.0 / 12 * d[4][0] - 5.0 / 6 * d[5][0];
    printf("y'(1.1)  = %.4f\\n", first / h);
    printf("y''(1.1) = %.4f\\n", second / (h * h));
    printf("central at t = 1.3: %.4f %.4f\\n", (y[4] - y[2]) / (2 * h), (y[4] - 2 * y[3] + y[2]) / (h * h));

    double x = 1.0;                             /* Richardson for sin at x = 1 */
    double D1 = (sin(x + 0.2) - sin(x - 0.2)) / 0.4;
    double D2 = (sin(x + 0.1) - sin(x - 0.1)) / 0.2;
    double R = D2 + (D2 - D1) / 3;
    printf("%-10s = %.8f   error = %.2e\\n", "D(0.2)", D1, fabs(D1 - cos(x)));
    printf("%-10s = %.8f   error = %.2e\\n", "D(0.1)", D2, fabs(D2 - cos(x)));
    printf("%-10s = %.8f   error = %.2e\\n", "Richardson", R, fabs(R - cos(x)));
    return 0;
}
'''),
        'gradcheck': dict(file='gradient_check', py='''# Gradient checking: compare an analytic gradient with central differences
import math

def loss(w0, w1):                     # squared error of a tiny linear model on 3 points
    xs, ys = [1.0, 2.0, 3.0], [2.0, 2.5, 4.0]
    return sum((w0 + w1 * x - y) ** 2 for x, y in zip(xs, ys))

def grad(w0, w1):                     # analytic gradient (what backprop would compute)
    xs, ys = [1.0, 2.0, 3.0], [2.0, 2.5, 4.0]
    g0 = sum(2 * (w0 + w1 * x - y) for x, y in zip(xs, ys))
    g1 = sum(2 * (w0 + w1 * x - y) * x for x, y in zip(xs, ys))
    return g0, g1

w0, w1 = 0.5, 0.8
g0, g1 = grad(w0, w1)
for eps in [1e-2, 1e-4, 1e-6, 1e-9]:
    n0 = (loss(w0 + eps, w1) - loss(w0 - eps, w1)) / (2 * eps)
    n1 = (loss(w0, w1 + eps) - loss(w0, w1 - eps)) / (2 * eps)
    rel = math.hypot(n0 - g0, n1 - g1) / math.hypot(g0, g1)
    print(f"eps = {eps:.0e}:  numeric = ({n0:.8f}, {n1:.8f})  relative difference = {rel:.1e}")
print(f"analytic = ({g0:.8f}, {g1:.8f})")
''', c='''/* Gradient checking: compare an analytic gradient with central differences */
#include <stdio.h>
#include <math.h>

double xs[3] = {1, 2, 3}, ys[3] = {2, 2.5, 4};

double loss(double w0, double w1) {
    double s = 0;
    for (int i = 0; i < 3; i++) { double r = w0 + w1 * xs[i] - ys[i]; s += r * r; }
    return s;
}

int main(void) {
    double w0 = 0.5, w1 = 0.8, g0 = 0, g1 = 0;
    for (int i = 0; i < 3; i++) {                 /* analytic gradient */
        double r = w0 + w1 * xs[i] - ys[i];
        g0 += 2 * r; g1 += 2 * r * xs[i];
    }
    double eps[4] = {1e-2, 1e-4, 1e-6, 1e-9};
    for (int k = 0; k < 4; k++) {
        double e = eps[k];
        double n0 = (loss(w0 + e, w1) - loss(w0 - e, w1)) / (2 * e);
        double n1 = (loss(w0, w1 + e) - loss(w0, w1 - e)) / (2 * e);
        double rel = hypot(n0 - g0, n1 - g1) / hypot(g0, g1);
        printf("eps = %.0e:  numeric = (%.8f, %.8f)  relative difference = %.1e\\n", e, n0, n1, rel);
    }
    printf("analytic = (%.8f, %.8f)\\n", g0, g1);
    return 0;
}
'''),
    },
    lab=dict(title='Numerical Differentiation Lab',
             intro='Compare difference formulas, find the best step size, use Richardson extrapolation, and check a machine-learning gradient.',
             tabs=[
                 dict(name='Difference formulas', blocks=[
                     dict(p='Type any f(x) and point x₀, then move the step h. The table compares forward, backward, central, Richardson and the second-derivative formula with the exact derivative.'),
                     dict(w='numdiff', o=dict(f='e^x', x0=1, logh=-1, height='280px', presets=[['sin x at 1', 'sin(x)', 1], ['eˣ at 1', 'e^x', 1], ['ln x at 2', 'ln(x)', 2], ['xˣ at 2', 'x^x', 2], ['|x| at 0', 'abs(x)', 0]]))]),
                 dict(name='Table data', blocks=[
                     dict(p='The difference table of the robot data. Read the diagonal for the point you need.'),
                     dict(w='difftab', o=dict(y='7.989 8.403 8.781 9.129 9.451 9.75 10.031', x0=1, h=0.1, noerr=True, presets=[['robot', '7.989 8.403 8.781 9.129 9.451 9.75 10.031', 1, 0.1], ['Problem 3', '4 8 15 7 6 2', 0, 1], ['homework 1 (eˣ)', '1 1.1052 1.2214 1.3499 1.4918', 0, 0.1]]))]),
                 dict(name='Code', blocks=[
                     dict(h='Table derivatives and Richardson'), dict(code='numdiff', tasks=['Run it. Compare with Problems 1 and 2.', 'Stop the series after Δ³. How much does y\'(1.1) change?', 'Change the Richardson steps to 0.02 and 0.01.']),
                     dict(h='Gradient checking'), dict(code='gradcheck', tasks=['Run it. Which ε gives the smallest relative difference?', 'Introduce a bug: change 2 * r * x to 2 * r in the analytic gradient. Does the check catch it?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Derive the central-difference formula for $f\'(x)$ and its error.', 'Taylor: $f(x \\pm h) = f \\pm hf\' + \\frac{h^2}{2}f\'\' \\pm \\frac{h^3}{6}f\'\'\' + \\cdots$. Subtract: $f(x+h) - f(x-h) = 2hf\' + \\frac{h^3}{3}f\'\'\' + \\cdots$, so $f\' = \\frac{f(x+h) - f(x-h)}{2h} - \\frac{h^2}{6}f\'\'\'(\\xi)$: error $O(h^2)$.'),
                         ('Write the formulas for $y\'$ and $y\'\'$ at $x_0$ from Newton\'s forward formula.', '$y\' = \\frac1h\\big(\\Delta y_0 - \\frac12\\Delta^2y_0 + \\frac13\\Delta^3y_0 - \\frac14\\Delta^4y_0 + \\cdots\\big)$, $\\;y\'\' = \\frac{1}{h^2}\\big(\\Delta^2y_0 - \\Delta^3y_0 + \\frac{11}{12}\\Delta^4y_0 - \\frac56\\Delta^5y_0 + \\cdots\\big)$.'),
                         ('Why is numerical differentiation called ill-conditioned?', 'It divides small differences of data by small steps: a data error $\\delta$ produces a derivative error of about $\\delta/h$ (first derivative) or $4\\delta/h^2$ (second). Smaller $h$ reduces truncation error but magnifies noise and round-off.'),
                         ('Use Richardson extrapolation: $D(0.2) = 0.536707$, $D(0.1) = 0.539402$ for $(\\sin x)\'$ at 1.', '$R = 0.539402 + (0.539402 - 0.536707)/3 = 0.540300$; true value $0.540302$.'),
                         ('What is gradient checking?', 'Comparing a gradient computed analytically (e.g. by backpropagation) with central-difference estimates $\\frac{L(w+\\epsilon) - L(w-\\epsilon)}{2\\epsilon}$ for a few parameters; a relative difference around $10^{-7}$ or smaller means the gradient code is correct.')])])]),
)
