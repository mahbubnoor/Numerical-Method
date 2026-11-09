BOWL = '0.5*(x^2 + 10*y^2)'
TWO = 'x^4 - 4*x^2 + x + y^2'
ROS = '(1 - x)^2 + 100*(y - x^2)^2'
GPRE = [['bowl, η = 0.1', BOWL, 10, 1, -1, 'gd', [-12, 12, -4, 4]], ['bowl, η = 0.2 (stuck)', BOWL, 10, 1, -0.699, 'gd', [-12, 12, -4, 4]], ['bowl, η = 0.21 (diverges)', BOWL, 10, 1, -0.678, 'gd', [-12, 12, -4, 4]],
        ['bowl, momentum', BOWL, 10, 1, -1, 'mom', [-12, 12, -4, 4]], ['bowl, Newton', BOWL, 10, 1, -1, 'newton', [-12, 12, -4, 4]],
        ['two valleys', TWO, 2, 1, -1.3, 'gd', [-2.5, 2.5, -1.5, 1.5]], ['Rosenbrock, GD', ROS, -1.2, 1, -3, 'gd', [-2, 2, -1, 3]], ['Rosenbrock, Newton', ROS, -1.2, 1, -3, 'newton', [-2, 2, -1, 3]]]
LX = '0.5 1 1.5 2 2.5 3 3.5 4 4.5 5'
LY = '0 0 0 1 0 1 0 1 1 1'

LECTURE = dict(
    title='Numerical Optimization for Machine Learning',
    short='Optimization for machine learning',
    sub='Finding the minimum of a function when no formula gives it: golden-section search in one variable, gradient descent and the learning rate, Newton\'s method with curvature, and Gauss–Newton for nonlinear least squares. This is how machine-learning models are trained.',
    slides=[
        dict(type='cover', id='cover', notes="Recap question: 'In Lecture 23 we minimised S(a, b) by setting the derivatives to zero and solving a linear system. What if the derivative equations are nonlinear?' Answer: solve them iteratively (Lectures 6–10) or walk downhill. Today: both."),
        dict(type='bullets', id='hook', title='The problem: who will pass the exam?', kick='Why this lecture', rw=560,
             lead='Ten students: hours of study $x$ and result $y$ (1 = pass, 0 = fail). Predict the probability of passing with a model $p = \\sigma(wx + b)$, where $\\sigma(z) = 1/(1 + e^{-z})$.',
             items=['Best $w$, $b$: minimise the <b>cross-entropy loss</b> $L(w, b) = -\\frac1n\\sum \\big[y_i\\ln p_i + (1 - y_i)\\ln(1 - p_i)\\big]$', 'Setting $\\partial L/\\partial w = \\partial L/\\partial b = 0$ gives <b>nonlinear</b> equations with no closed-form solution',
                    'Least squares (Lectures 23–24) does not apply: the model is not linear in $w$, $b$', 'Neural networks: the same problem with millions of parameters'],
             frag=True,
             right=dict(table=[['hours $x$', 'result $y$'], [['0.5, 1.0, 1.5', '0, 0, 0'], ['2.0, 2.5', '1, 0'], ['3.0, 3.5', '1, 0'], ['4.0, 4.5, 5.0', '1, 1, 1'], ['$w$, $b$ = ?', 'boundary = ?']]]),
             notes="Logistic regression is the simplest classifier and the last layer of most neural networks. Solved at the end: w = 1.353, b = −3.722, decision boundary 2.75 hours."),
        dict(type='goals', id='goals', items=[
            'State optimality conditions and the link between <b>minimisation and root finding</b>',
            'Apply <b>golden-section search</b> to a one-variable function',
            'Apply <b>gradient descent</b>; explain the learning rate through stability',
            'Apply <b>Newton\'s method</b> for minimisation and <b>Gauss–Newton</b> for nonlinear least squares',
            'Train a logistic-regression classifier; choose a method for a given problem'],
            prev='Root finding (bisection, Newton, Lectures 6–10); iteration and convergence (Lecture 14); Euler stability (Lectures 21–22); least squares (Lectures 23–24).',
            today='Minimise any smooth function by iteration: bracket it, walk downhill, or use curvature.',
            notes="Last lecture. Almost every earlier module reappears here: say so as each method appears."),
        dict(type='math', id='basics', title='Working principle: a minimum is where the slope is zero and the curve bends up',
             eqs=[dict(cap='One variable: necessary and sufficient conditions', eq='f\'(x^{*}) = 0, \\qquad f\'\'(x^{*}) > 0'),
                  dict(cap='Several variables: gradient zero, Hessian positive definite', eq='\\nabla f(\\mathbf{x}^{*}) = \\mathbf{0}, \\qquad H = \\Big[\\frac{\\partial^2 f}{\\partial x_i\\partial x_j}\\Big] \\text{ positive definite}', frag=True)],
             items=['Minimising $f$ = finding a root of $f\'$: bisection and Newton (Lectures 6–10) apply to $f\'$', 'But $f\'$ may be unknown or expensive: <b>golden section</b> uses only values of $f$',
                    'Many variables: walk downhill along $-\\nabla f$ (<b>gradient descent</b>)', '<b>Local</b> minimum ≠ <b>global</b> minimum unless $f$ is convex'],
             ifrag=True, rw=640,
             notes="Maximising f is minimising −f. Machine learning calls f the loss or cost function."),
        dict(type='math', id='golden', title='Golden-section search: shrink a bracket without derivatives',
             eqs=[dict(cap='f unimodal on [a, b]; two interior points, g = (√5 − 1)/2 ≈ 0.618', eq='c = b - g(b - a), \\qquad d = a + g(b - a)'),
                  dict(cap='Keep the part that must contain the minimum', eq='f(c) < f(d) \\;\\Rightarrow\\; [a, d], \\qquad f(c) \\ge f(d) \\;\\Rightarrow\\; [c, b]', frag=True)],
             items=['Like bisection (Lecture 6), but compares two values instead of checking a sign', 'The kept interior point is reused: <b>one new $f$ value per step</b>, because $g^2 = 1 - g$',
                    'Bracket width × 0.618 each step: from 3 to $10^{-4}$ in 22 steps', 'Needs only a unimodal $f$ (one dip): no derivatives, very robust'],
             ifrag=True, rw=620,
             notes="Why 0.618: after keeping [a, d], the old c must sit where the new d belongs: g·g(b − a) = (1 − g)(b − a), so g² + g − 1 = 0, g = 0.618 (the golden ratio minus one)."),
        dict(type='bullets', id='algo', title='Golden-section search, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Choose a bracket $[a, b]$ in which $f$ has a single minimum', 'Place $c = b - 0.618(b - a)$ and $d = a + 0.618(b - a)$; evaluate $f(c)$, $f(d)$',
                    'If $f(c) < f(d)$: $b \\leftarrow d$, $d \\leftarrow c$, new $c$; otherwise $a \\leftarrow c$, $c \\leftarrow d$, new $d$', 'Evaluate $f$ only at the new point', 'Stop when $b - a <$ tolerance; answer $(a + b)/2$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input f, a, b, tol\ng ← (√5 − 1)/2\nc ← b − g(b − a);  d ← a + g(b − a)\nwhile b − a > tol:\n    if f(c) &lt; f(d):\n        b ← d;  d ← c\n        c ← b − g(b − a)\n    else:\n        a ← c;  c ← d\n        d ← a + g(b − a)\nreturn (a + b)/2</pre></div><p class="small" style="margin-top:14px">Store $f(c)$ and $f(d)$ so that each step costs one evaluation.</p>'),
             notes=""),
        dict(type='worked', id='p1', title='Problem 1: minimise $f(x) = x^4 - 3x^3 + 2$ on $[0, 3]$',
             steps=['$c = 3 - 0.618(3) = 1.1459$, $\\;d = 1.8541$; $\\;f(c) = -0.790$, $f(d) = -5.304$', '$f(c) > f(d)$: keep $[1.1459, 3]$; new $d = 2.2918$, $f(d) = -6.525$',
                    'Again $f(c) > f(d)$: keep $[1.8541, 3]$; new $d = 2.5623$, $f = -5.363$', '$f(c) < f(d)$: keep $[1.8541, 2.5623]$, then $[2.1246, 2.5623]$, …', 'After 22 steps: $x^{*} = 2.2500$, $f(x^{*}) = -6.5430$'],
             answer='Check: $f\'(x) = 4x^3 - 9x^2 = x^2(4x - 9) = 0$ at $x = 2.25$, $f\'\'(2.25) = 20.25 > 0$: the method found the minimum using values of $f$ only.',
             right=dict(w='golden', o=dict(f='x^4 - 3x^3 + 2', a=0, b=3, step=1, height='260px', tableHeight='230px')), rw=800,
             notes="Newton applied to f′ from x₀ = 3 converges much faster: 2.5, 2.291667, 2.251462, 2.250002, 2.25 (next slides)."),
        dict(type='math', id='gd', title='Gradient descent: step downhill, scaled by the learning rate',
             eqs=[dict(cap='Learning rate (step size) η > 0', eq='\\mathbf{x}_{k+1} = \\mathbf{x}_k - \\eta\\,\\nabla f(\\mathbf{x}_k)'),
                  dict(cap='On f(w) = (w − 3)² + 1 the error is multiplied by (1 − 2η) each step', eq='w_{k+1} - 3 = (1 - 2\\eta)(w_k - 3)', frag=True)],
             items=['$-\\nabla f$ is the direction of steepest descent', 'From $w_0 = 0$: $\\eta = 0.1$: $0.6, 1.08, 1.46, \\dots$ (slow); $\\eta = 0.5$: 3 in one step; $\\eta = 0.9$: overshoots but converges',
                    '$\\eta = 1$: jumps $0, 6, 0, 6$ for ever; $\\eta = 1.1$: <b>diverges</b>', 'It is Euler\'s method (Lecture 21) for $\\mathbf{x}\' = -\\nabla f$; stable when $\\eta < 2/\\lambda_{\\max}(H)$, as in Lecture 22'],
             ifrag=True, rw=660,
             notes="Here f″ = 2 = λ, so the stability limit is η < 2/2 = 1. In ML the same limit explains why a too-large learning rate makes the loss explode."),
        dict(type='bullets', id='algo2', title='Gradient descent, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Start at $\\mathbf{x}_0$; choose $\\eta$ (try 0.1, then adjust by factors of 3)', 'Compute the gradient $\\mathbf{g} = \\nabla f(\\mathbf{x}_k)$', 'Step: $\\mathbf{x}_{k+1} = \\mathbf{x}_k - \\eta\\mathbf{g}$',
                    'Stop when $\\|\\mathbf{g}\\|$ or the change in $f$ is below a tolerance', 'If $f$ increases, $\\eta$ is too large: halve it. Momentum: $\\mathbf{v} \\leftarrow \\beta\\mathbf{v} - \\eta\\mathbf{g}$, $\\;\\mathbf{x} \\leftarrow \\mathbf{x} + \\mathbf{v}$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input ∇f, x0, η, tol, kmax\nx ← x0;  v ← 0\nfor k = 1 … kmax:\n    g ← ∇f(x)\n    if ‖g‖ &lt; tol: stop\n    v ← β·v − η·g    # β = 0: plain GD\n    x ← x + v\nreturn x</pre></div><p class="small" style="margin-top:14px">Machine learning: $\\nabla f$ from a random mini-batch of data = <b>stochastic</b> gradient descent.</p>'),
             notes="The gradient of a neural network's loss is computed by backpropagation, which is the chain rule organised efficiently (automatic differentiation)."),
        dict(type='worked', id='p2', title='Problem 2: gradient descent on a long, narrow valley',
             q='Minimise $f(x, y) = \\tfrac12(x^2 + 10y^2)$ from $(10, 1)$. $\\nabla f = (x, 10y)$; the Hessian has eigenvalues 1 and 10.',
             steps=['$\\eta = 0.1$: $(10, 1) \\to (10 - 1, 1 - 1) = (9, 0) \\to (8.1, 0) \\to (7.29, 0) \\dots$', 'Along $x$ the error shrinks only by $1 - 0.1(1) = 0.9$ per step: <b>153 steps</b> to $\\|\\mathbf{x}\\| < 10^{-6}$',
                    'Larger $\\eta$ is limited by the steep direction: $|1 - 10\\eta| < 1 \\Rightarrow \\eta < 0.2$; at 0.2 $y$ flips sign for ever, at 0.21 it diverges', 'Best fixed rate $\\eta = 2/(1 + 10)$: 81 steps. Momentum ($\\eta = 0.1$, $\\beta = 0.5$): 41 steps'],
             answer='Slow convergence is set by the <b>condition number</b> $\\lambda_{\\max}/\\lambda_{\\min} = 10$ of the Hessian, just as for iterative linear solvers (Lecture 14).',
             right=dict(w='gd2d', o=dict(f=BOWL, x0=10, y0=1, logeta=-1, steps=30, method='gd', height='300px', fixed=True, notable=True, range=[-12, 12, -4, 4])), rw=760,
             notes="Iteration counts to reach ‖x‖ < 1e−6: η = 0.05: 315; 0.1: 153; 0.15: 100; 0.19: 132; 0.2: never; 0.21: diverges. Momentum β = 0.5: 41; β = 0.7: 70 (too much momentum overshoots)."),
        dict(type='widget', id='explore', title='Explore: gradient descent, momentum and Newton', w='gd2d',
             o=dict(f=BOWL, x0=10, y0=1, logeta=-1, steps=40, method='gd', height='340px', side=True, tableHeight='340px', presets=GPRE, range=[-12, 12, -4, 4]), lw=420,
             items=['Move η: zig-zag across the valley, then divergence above 0.2', 'Momentum smooths the zig-zag', 'Newton jumps to the minimum of a quadratic in one step',
                    'Rosenbrock\'s banana valley: GD crawls; Newton reaches $(1, 1)$ in 6 steps'],
             notes="Rosenbrock from (−1.2, 1): plain GD with η = 0.001 after 300 steps is still at (−0.76, 0.58), f = 3.1; momentum β = 0.9 reaches (0.89, 0.79); Newton converges in 6 iterations."),
        dict(type='math', id='newton', title="Newton's method for minimisation: use the curvature",
             eqs=[dict(cap='One variable: Newton (Lecture 9) applied to f′', eq='x_{k+1} = x_k - \\frac{f\'(x_k)}{f\'\'(x_k)}'),
                  dict(cap='Several variables: solve a linear system with the Hessian each step', eq='H(\\mathbf{x}_k)\\,\\boldsymbol{\\delta} = -\\nabla f(\\mathbf{x}_k), \\qquad \\mathbf{x}_{k+1} = \\mathbf{x}_k + \\boldsymbol{\\delta}', frag=True)],
             items=['Fits a parabola (quadratic model) at $\\mathbf{x}_k$ and jumps to its minimum', '<b>Quadratic convergence</b>: $f = x^4 - 3x^3 + 2$ from 3: $2.5,\\ 2.291667,\\ 2.251462,\\ 2.250002,\\ 2.25$',
                    'Exact in one step for a quadratic $f$ (any condition number)', 'Cost: second derivatives and an $n \\times n$ solve; can head for a maximum or saddle if $H$ is not positive definite'],
             ifrag=True, rw=640,
             notes="Compare with golden section: 22 steps for 4 digits; Newton: 4 steps for 6 digits, but it needed f′ and f″.\n\nQuasi-Newton methods (BFGS, L-BFGS) build an approximation of H from gradients only: the default in scipy.optimize.minimize."),
        dict(type='math', id='gn', title='Gauss–Newton: nonlinear least squares by repeated linear least squares',
             eqs=[dict(cap='Minimise S(p) = Σ rᵢ², residuals rᵢ = yᵢ − f(xᵢ; p); Jacobian Jᵢⱼ = ∂f(xᵢ; p)/∂pⱼ', eq='\\big(J^{T}J\\big)\\,\\boldsymbol{\\delta} = J^{T}\\mathbf{r}, \\qquad \\mathbf{p} \\leftarrow \\mathbf{p} + \\boldsymbol{\\delta}'),
                  dict(cap='Bacteria (Lecture 24): f = a e^{bt}, columns of J', eq='\\frac{\\partial f}{\\partial a} = e^{bt_i}, \\qquad \\frac{\\partial f}{\\partial b} = a\\,t_i\\,e^{bt_i}', frag=True)],
             items=['Each step: linearise the model (Newton, Lecture 10), solve the <b>normal equations</b> (Lecture 23)', 'From the log-fit start $(100.29, 0.40767)$: $(100.436, 0.407153)$ in 2 steps',
                    'From a poor start $(50, 0.3)$: 94.7, 85.4, 96.4, 100.32, 100.436: converged by step 5', 'Levenberg–Marquardt adds $\\lambda I$ to $J^{T}J$ for safety far from the answer'],
             ifrag=True, rw=620,
             notes="S falls from 17.36 (log fit) to 16.43 (direct fit): the direct fit is better in the original units, as Lecture 24 promised.\n\nUsed in GPS (Lecture 23 apps), camera calibration, curve_fit in SciPy (Levenberg–Marquardt)."),
        dict(type='worked', id='p3', title='Problem 3: train the pass/fail classifier by gradient descent',
             steps=['Gradients: $\\dfrac{\\partial L}{\\partial w} = \\frac1n\\sum (p_i - y_i)x_i$, $\\;\\dfrac{\\partial L}{\\partial b} = \\frac1n\\sum (p_i - y_i)$ (simple, like least squares)', 'Start $w = b = 0$: all $p_i = 0.5$, $L = \\ln 2 = 0.6931$; gradient $(-0.475, 0)$',
                    'Step 1 ($\\eta = 0.5$): $w = 0.2375$, $b = 0$, $L = 0.6458$', 'After 100 steps $L = 0.445$; after 1000: $w = 1.3533$, $b = -3.7214$, $L = 0.4335$', 'Newton\'s method on the same loss: 5 iterations to $w = 1.35341$, $b = -3.72188$'],
             answer='$p = \\sigma(1.353x - 3.722)$: 50% chance at <b>$x = 3.722/1.353 \\approx 2.75$ hours</b>; 27% after 2 hours, 73% after 3.5 hours.',
             right=dict(html='<div class="card key"><span class="tag">Training log, learning rate 0.5</span><table class="tb sm" style="width:100%"><thead><tr><th>step</th><th>$w$</th><th>$b$</th><th>loss</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>0</td><td>0.6931</td></tr><tr><td>1</td><td>0.2375</td><td>0</td><td>0.6458</td></tr><tr><td>10</td><td>0.3493</td><td>−0.5260</td><td>0.5802</td></tr><tr><td>100</td><td>1.0211</td><td>−2.6795</td><td>0.4450</td></tr><tr><td>1000</td><td>1.3533</td><td>−3.7214</td><td>0.4335</td></tr></tbody></table></div><p class="small">Gradient descent: cheap steps, many of them. Newton: 5 expensive steps.</p>'), rw=700,
             notes="Gradient-norm tolerance 1e−6 is reached after 1260 steps. In the lab the code prints these values."),
        dict(type='compare', id='classic', title='Same goal, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (solve ∇f = 0 by hand)', tag='Calculus', cls='blue', items=['$f = x^4 - 3x^3 + 2$: $x^2(4x - 9) = 0 \\Rightarrow x = 2.25$', 'Least squares: $\\nabla S = 0$ is linear (Lecture 23)', 'Needs equations that can be solved exactly']),
             right=dict(h='Numerical (iterate downhill)', tag='Algorithm', cls='key', items=['Golden section: 22 values of $f$, no derivatives', 'Gradient descent or Newton: any differentiable $f$', 'Same code for 2 or $10^{9}$ parameters']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>Training a neural network: minimise a loss over millions of weights</h3><p>$\\nabla L = 0$ is a huge system of nonlinear equations with many solutions; nobody writes it down. Stochastic gradient descent (with momentum: Adam) takes millions of small steps, each using the gradient of a small batch of data computed by backpropagation.</p></div>'),
             notes="Even logistic regression (Problem 3) has no closed form."),
        dict(type='code', id='code', title='Golden section, Newton and gradient descent in code', code='golden', lw=560,
             items=['Golden section on $[0, 3]$ with one new $f$ per step', 'Newton\'s method on $f\'$ from $x_0 = 3$', 'Lab: logistic regression trained by gradient descent', 'Compare steps and accuracy of the two methods'],
             notes="Expected: golden 22 steps, x = 2.250016; Newton 2.5, 2.291667, 2.251462, 2.250002, 2.250000."),
        dict(type='widget', id='fail', title='Limitations shown failing', kick='When optimisation goes wrong', w='gd2d',
             o=dict(f=TWO, x0=2, y0=1, logeta=-1.3, steps=60, method='gd', height='300px', side=True, tableHeight='300px', presets=GPRE, range=[-2.5, 2.5, -1.5, 1.5]), lw=500,
             items=['<b>Local minima</b>: from $(2, 1)$ GD stops at $x = 1.347$, $f = -2.62$; the deeper valley at $x = -1.473$ has $f = -5.44$', '<b>Learning rate</b>: too small crawls, too large diverges (bowl presets)',
                    '<b>Ill-conditioning</b>: narrow valleys (Rosenbrock) make GD zig-zag for thousands of steps', '<b>Newton</b> finds any stationary point, including maxima and saddles; golden section needs a single dip'],
             frag=True,
             notes="Remedies: several random starts, momentum and adaptive learning rates (Adam), line searches, trust regions; convex models (least squares, logistic regression) have a single minimum."),
        dict(type='exam', id='practice', src='Problem 4',
             q='"For $f(x, y) = x^2 + 3y^2 - 2x$, perform two steps of gradient descent from $(0, 1)$ with $\\eta = 0.1$, then one step of Newton\'s method from $(0, 1)$. Compare with the exact minimum."',
             tips=['$\\nabla f = (2x - 2,\\; 6y)$; at $(0, 1)$: $(-2, 6)$', 'Step 1: $(0, 1) - 0.1(-2, 6) = (0.2, 0.4)$, $f = 0.12$; $\\;$Step 2: gradient $(-1.6, 2.4)$ → $(0.36, 0.16)$, $f = -0.5136$',
                   'Newton: $H = \\begin{bmatrix} 2 & 0 \\\\ 0 & 6 \\end{bmatrix}$, $\\;\\boldsymbol{\\delta} = -H^{-1}\\nabla f = (1, -1)$ → $(1, 0)$', 'Exact minimum $(1, 0)$, $f = -1$: Newton is exact in one step because $f$ is quadratic; GD needs many steps'],
             notes=""),
        dict(type='profile', id='profile', title='Optimisation methods: profile',
             best=['Golden section: one variable, no derivatives, guaranteed for unimodal $f$', 'Gradient descent: huge numbers of parameters, cheap steps, works with noisy (stochastic) gradients', 'Newton / Gauss–Newton: few parameters, high accuracy in few steps'],
             worst=['Golden section: several variables, functions with many dips', 'Gradient descent: ill-conditioned valleys; sensitive to η', 'Newton: Hessian too large to form; non-convex regions'],
             suited=['Tuning one hyperparameter (golden section on validation error)', 'Training ML models: linear, logistic, neural networks (SGD, Adam)', 'Curve fitting and calibration (Gauss–Newton, Levenberg–Marquardt)'],
             avoid=['Problems with a closed-form solution (linear least squares)', 'Non-smooth or discrete objectives (use specialised methods)', 'Constrained problems without modification (Lagrange multipliers, linear programming)'],
             verdict='Rule of thumb: <b>few variables and smooth: Newton or quasi-Newton; many variables or huge data: (stochastic) gradient descent with a tuned learning rate</b>.',
             notes=""),
        dict(type='table', id='compare', title='Comparative analysis: optimisation methods', cls='tb sm',
             head=['Method', 'Uses', 'Convergence', 'Cost per step ($n$ variables)', 'Problem 1/2 result'], tx=(0,), frag=True,
             rows=[['Golden section', '$f$ only', 'linear, ×0.618', '1 evaluation', '22 steps to $10^{-4}$'], ['Newton (1-D)', '$f\'$, $f\'\'$', 'quadratic', '2 derivative values', '4 steps to $10^{-6}$'],
                   ['Gradient descent', '$\\nabla f$', 'linear, set by condition number', '$O(n)$', '153 steps (bowl, $\\eta = 0.1$)'], ['GD + momentum', '$\\nabla f$', 'faster linear', '$O(n)$', '41 steps'],
                   ['Newton ($n$-D)', '$\\nabla f$, $H$', 'quadratic', '$O(n^3)$ solve', '1 step (quadratic $f$)'], ['Gauss–Newton', 'residuals, $J$', 'near quadratic (small residuals)', '$O(mn^2)$', '2–5 steps (bacteria)']],
             note='The trade-off is the same as in root finding (Lecture 10): cheap, slow, robust steps against expensive, fast, fragile ones.', notefrag=True,
             notes=""),
        dict(type='ml', id='map', title='The whole course inside a machine-learning library', kick='Beyond the classroom', n=3,
             items=[dict(ic='🔢', h='Floating point (L2–5)', t='Training in 16-bit precision; loss of significance in softmax; why log-sum-exp is used'),
                    dict(ic='🎯', h='Roots and Newton (L6–10)', t='Newton and quasi-Newton optimisers; solving $\\nabla f = 0$'),
                    dict(ic='🧮', h='Linear systems (L11–14)', t='Least squares, Cholesky in Gaussian processes, conditioning of features'),
                    dict(ic='📈', h='Interpolation (L15–18)', t='Splines for features and learning-rate schedules; Runge = overfitting'),
                    dict(ic='∫', h='Derivatives and integrals (L19–20)', t='Gradient checking with finite differences; expectations by quadrature'),
                    dict(ic='🌀', h='ODEs (L21–22)', t='Gradient descent = Euler; learning-rate limit = stability; neural ODEs')],
             notes="Use this as the closing overview: every module reappears in a modern ML toolkit."),
        dict(type='bridge', id='bridge', title='End of the course: where these methods lead', kick='Roadmap', lead='Every method in this course has a bigger sibling. These are the natural next steps.',
             keeptitle='What you can now do', keep=['Know how computers store numbers and lose digits', 'Solve equations, linear systems and ODEs', 'Interpolate, differentiate and integrate data', 'Fit models and minimise functions'],
             rows=[['Millions of parameters, noisy gradients', 'SGD, Adam, backpropagation', 'Machine learning'], ['Constraints ($x \\ge 0$, budgets)', 'Lagrange multipliers, linear programming', 'Operations research'],
                   ['Equations in space and time (heat, waves, fluids)', 'Finite differences and finite elements', 'Numerical PDEs'], ['Huge sparse matrices and eigenvalues', 'Krylov methods (CG, GMRES), SVD', 'Numerical linear algebra']],
             notes="Suggest one follow-up for each interest: ML (Goodfellow et al., Deep Learning, ch. 4 and 8), optimisation (Nocedal and Wright), PDEs (LeVeque)."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see optimisation at work.',
             items=[
                 dict(ic='🧠', h='Training neural networks', t='Gradient descent on millions of weights',
                      detail=dict(where='every deep-learning framework (PyTorch, TensorFlow). The loss surface is like the contour map below, in millions of dimensions; optimisers walk downhill along gradients computed by backpropagation.',
                                  w='gd2d', o=dict(f=ROS, x0=-1.2, y0=1, logeta=-3, steps=200, method='mom', beta=0.9, height='210px', fixed=True, notable=True, range=[-2, 2, -1, 3]),
                                  note='Momentum ($\\beta = 0.9$) on Rosenbrock\'s valley. Adam, the default optimiser, adds a per-parameter learning rate.')),
                 dict(ic='🎛️', h='Tuning a hyperparameter', t='Golden section on validation error',
                      detail=dict(where='model selection. The validation error as a function of the ridge parameter $\\log_{10}\\lambda$ usually has one dip; golden-section search finds it with few (expensive) training runs.',
                                  w='golden', o=dict(f='(x + 3)^2/4 + 0.3*sin(x) + 1', a=-8, b=2, step=4, height='190px', tableHeight='150px'),
                                  note='Each evaluation of $f$ is one full training run, so needing only one new value per step matters.')),
                 dict(ic='✉️', h='Spam filters and medical tests', t='Logistic regression',
                      detail=dict(where='email filters, credit scoring, medical risk scores. The probability of "spam" is $\\sigma(\\mathbf{w}\\cdot\\mathbf{x} + b)$, where $\\mathbf{x}$ counts words; $\\mathbf{w}$ is trained exactly as in Problem 3, with thousands of features.',
                                  steps=['Features: word counts, sender, links', 'Loss: cross-entropy, as in Problem 3', 'Optimiser: L-BFGS (quasi-Newton) or stochastic gradient descent', 'Threshold the probability (e.g. 0.5) to decide'],
                                  note='The same model forms the last layer of most neural-network classifiers.')),
                 dict(ic='📷', h='Camera calibration and 3-D reconstruction', t='Gauss–Newton / Levenberg–Marquardt',
                      detail=dict(where='phone panoramas, AR apps, photogrammetry. Unknown camera positions and 3-D points are adjusted so that predicted image positions match the observed ones ("bundle adjustment").',
                                  steps=['Residuals: predicted minus observed pixel positions (thousands)', 'Parameters: camera poses and 3-D points', 'Gauss–Newton with Levenberg–Marquardt damping', 'Sparse Cholesky (Lecture 13) solves $J^{T}J\\boldsymbol\\delta = J^{T}\\mathbf{r}$ each step'],
                                  note='Least squares + Newton + linear systems: three modules of this course in one algorithm.'))],
             notes="Two widget cards are interactive inside the pop-up."),
        dict(type='check', id='check', q='Gradient descent on $f(w) = 2w^2$ ($f\'(w) = 4w$). For which learning rates does it converge?',
             opts=['$0 < \\eta < 0.5$', '$0 < \\eta < 1$', '$0 < \\eta < 2$', 'every $\\eta > 0$'], right=0,
             answer='A. $w_{k+1} = w_k - 4\\eta w_k = (1 - 4\\eta)w_k$; converges when $|1 - 4\\eta| < 1$, i.e. $0 < \\eta < 0.5$. At $\\eta = 0.25$ it reaches 0 in one step ($\\eta = 1/f\'\'$, the Newton step).',
             notes="General rule: η < 2/λ_max, with λ_max the largest eigenvalue of the Hessian (here f″ = 4)."),
        dict(type='summary', id='summary', items=[
            'Minimum: $\\nabla f = 0$ and $H$ positive definite; local ≠ global',
            'Golden section: bracket × 0.618 per step, values of $f$ only',
            'Gradient descent $\\mathbf{x} \\leftarrow \\mathbf{x} - \\eta\\nabla f$; needs $\\eta < 2/\\lambda_{\\max}$; speed set by the condition number; momentum helps',
            'Newton: $H\\boldsymbol\\delta = -\\nabla f$, quadratic convergence; Gauss–Newton: $(J^{T}J)\\boldsymbol\\delta = J^{T}\\mathbf{r}$ for nonlinear least squares'],
            hw=['Golden-section search for the minimum of $f(x) = x^2 - 4\\sin x$ on $[0, 3]$: three steps by hand, then finish in the lab.', 'Gradient descent on $f(x, y) = (x - 1)^2 + 4(y + 2)^2$ from $(0, 0)$: two steps with $\\eta = 0.1$. What is the largest stable $\\eta$?',
                'Newton\'s method for the minimum of $f(x) = e^{x} - 2x$ from $x_0 = 0$: three iterations.', 'Train the classifier of Problem 3 in the lab with $\\eta = 0.1$, 0.5 and 2: compare the loss after 100 steps.'],
            solved='Gradient descent finds $w = 1.353$, $b = -3.722$: $p = \\sigma(1.353x - 3.722)$. A student needs about <b>2.75 hours</b> of study for a 50% chance of passing, and 73% after 3.5 hours.',
            nexttitle='After this course', next='Machine learning, optimisation, numerical PDEs and numerical linear algebra all build on these 25 lectures. Keep the labs: every method here is a few lines of code you can now read, check and trust.',
            notes="Homework answers: Q1: f′ = 2x − 4cos x = 0 at x = 1.0299 (f = −2.3683); golden steps: c = 1.1459, d = 1.8541, f(c) = −2.3312, f(d) = −0.4029 → keep [0, 1.8541]. Q2: ∇f = (2(x − 1), 8(y + 2)); (0, 0) → (0.2, −1.6) → (0.36, −1.92); largest stable η = 2/8 = 0.25. Q3: x₁ = 1, x₂ = 0.735759, x₃ = 0.694042 (→ ln 2 = 0.693147). Q4: in the lab."),
    ],
    code={
        'golden': dict(file='golden_section_newton', py='''# Minimise f(x) = x^4 - 3x^3 + 2: golden-section search, then Newton's method
import math

def f(x):
    return x ** 4 - 3 * x ** 3 + 2

a, b = 0.0, 3.0
g = (math.sqrt(5) - 1) / 2
c, d = b - g * (b - a), a + g * (b - a)
fc, fd = f(c), f(d)
k = 0
while b - a > 1e-4:
    if fc < fd:                      # minimum in [a, d]
        b, d, fd = d, c, fc
        c = b - g * (b - a)
        fc = f(c)
    else:                            # minimum in [c, b]
        a, c, fc = c, d, fd
        d = a + g * (b - a)
        fd = f(d)
    k += 1
    if k <= 4:
        print(f"step {k}: [{a:.4f}, {b:.4f}]  width {b - a:.4f}")
xm = (a + b) / 2
print(f"golden section: {k} steps, x = {xm:.6f}, f = {f(xm):.6f}")

x = 3.0                              # Newton on f'(x) = 0
for k in range(1, 6):
    d1 = 4 * x ** 3 - 9 * x ** 2
    d2 = 12 * x ** 2 - 18 * x
    x = x - d1 / d2
    print(f"Newton {k}: x = {x:.6f}")
''', c='''/* Minimise f(x) = x^4 - 3x^3 + 2: golden-section search, then Newton's method */
#include <stdio.h>
#include <math.h>

double f(double x) { return pow(x, 4) - 3 * pow(x, 3) + 2; }

int main(void) {
    double a = 0, b = 3, g = (sqrt(5.0) - 1) / 2;
    double c = b - g * (b - a), d = a + g * (b - a), fc = f(c), fd = f(d);
    int k = 0;
    while (b - a > 1e-4) {
        if (fc < fd) {                     /* minimum in [a, d] */
            b = d; d = c; fd = fc;
            c = b - g * (b - a); fc = f(c);
        } else {                           /* minimum in [c, b] */
            a = c; c = d; fc = fd;
            d = a + g * (b - a); fd = f(d);
        }
        k++;
        if (k <= 4) printf("step %d: [%.4f, %.4f]  width %.4f\\n", k, a, b, b - a);
    }
    double xm = (a + b) / 2;
    printf("golden section: %d steps, x = %.6f, f = %.6f\\n", k, xm, f(xm));

    double x = 3;                          /* Newton on f'(x) = 0 */
    for (k = 1; k <= 5; k++) {
        double d1 = 4 * pow(x, 3) - 9 * x * x, d2 = 12 * x * x - 18 * x;
        x = x - d1 / d2;
        printf("Newton %d: x = %.6f\\n", k, x);
    }
    return 0;
}
'''),
        'minibatch': dict(file='minibatch_sgd', py='''# Full-batch gradient descent vs mini-batch SGD with the same compute budget
import math

seed = 12345
def rnd():                                   # reproducible random numbers in [0, 1)
    global seed
    seed = (seed * 16807) % 2147483647
    return seed / 2147483647

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

N = 2000                                     # students generated from p = sigmoid(1.35x - 3.72)
x = []
y = []
for i in range(N):
    xi = 5 * rnd()
    x.append(xi)
    y.append(1 if rnd() < sigmoid(1.35 * xi - 3.72) else 0)

def loss(w, b):
    s = 0.0
    for i in range(N):
        p = sigmoid(w * x[i] + b)
        s -= y[i] * math.log(p) + (1 - y[i]) * math.log(1 - p)
    return s / N

def train(B, eta, budget):
    w = b = 0.0
    used = steps = 0
    while used + B <= budget:
        start = 0 if B == N else int(rnd() * N)  # random batch
        gw = gb = 0.0
        for j in range(B):
            i = (start + j) % N
            e = sigmoid(w * x[i] + b) - y[i]
            gw += e * x[i]
            gb += e
        w -= eta * gw / B
        b -= eta * gb / B
        used += B
        steps += 1
    return w, b, steps

budget = 40000                               # gradients of single data points
for B in [N, 200, 20]:
    w, b, steps = train(B, 0.2, budget)
    print(f"B = {B:4d}: {steps:5d} steps   w = {w:7.4f}  b = {b:8.4f}  loss = {loss(w, b):.4f}")
''', c='''/* Full-batch gradient descent vs mini-batch SGD with the same compute budget */
#include <stdio.h>
#include <math.h>
#define N 2000

long long seed = 12345;
double rnd(void) {                           /* reproducible random numbers in [0, 1) */
    seed = (seed * 16807) % 2147483647;
    return (double)seed / 2147483647;
}
double sigmoid(double z) { return 1 / (1 + exp(-z)); }

double x[N], y[N];

double loss(double w, double b) {
    double s = 0;
    for (int i = 0; i < N; i++) {
        double p = sigmoid(w * x[i] + b);
        s -= y[i] * log(p) + (1 - y[i]) * log(1 - p);
    }
    return s / N;
}

int main(void) {
    for (int i = 0; i < N; i++) {            /* students generated from p = sigmoid(1.35x - 3.72) */
        x[i] = 5 * rnd();
        y[i] = rnd() < sigmoid(1.35 * x[i] - 3.72) ? 1 : 0;
    }
    int sizes[3] = {N, 200, 20};
    int budget = 40000;                      /* gradients of single data points */
    for (int t = 0; t < 3; t++) {
        int B = sizes[t], used = 0, steps = 0;
        double w = 0, b = 0, eta = 0.2;
        while (used + B <= budget) {
            int start = (B == N) ? 0 : (int)(rnd() * N);   /* random batch */
            double gw = 0, gb = 0;
            for (int j = 0; j < B; j++) {
                int i = (start + j) % N;
                double e = sigmoid(w * x[i] + b) - y[i];
                gw += e * x[i];
                gb += e;
            }
            w -= eta * gw / B;
            b -= eta * gb / B;
            used += B;
            steps++;
        }
        printf("B = %4d: %5d steps   w = %7.4f  b = %8.4f  loss = %.4f\\n", B, steps, w, b, loss(w, b));
    }
    return 0;
}
'''),
        'logreg': dict(file='logistic_regression_gd', py='''# Logistic regression p = sigmoid(w x + b) trained by gradient descent
import math
x = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]     # hours of study
y = [0, 0, 0, 1, 0, 1, 0, 1, 1, 1]                         # 1 = pass
n = len(x)
eta = 0.5

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def loss(w, b):
    s = 0.0
    for xi, yi in zip(x, y):
        p = sigmoid(w * xi + b)
        s -= yi * math.log(p) + (1 - yi) * math.log(1 - p)
    return s / n

w = b = 0.0
print(f"step    0: w = {w:7.4f}  b = {b:8.4f}  loss = {loss(w, b):.4f}")
for k in range(1, 1001):
    gw = gb = 0.0
    for xi, yi in zip(x, y):
        e = sigmoid(w * xi + b) - yi
        gw += e * xi
        gb += e
    w -= eta * gw / n
    b -= eta * gb / n
    if k in [1, 10, 100, 1000]:
        print(f"step {k:4d}: w = {w:7.4f}  b = {b:8.4f}  loss = {loss(w, b):.4f}")
print(f"decision boundary (p = 0.5): x = {-b / w:.3f} hours")
print(f"P(pass) after 2 h: {sigmoid(2 * w + b):.3f}   after 3.5 h: {sigmoid(3.5 * w + b):.3f}")
''', c='''/* Logistic regression p = sigmoid(w x + b) trained by gradient descent */
#include <stdio.h>
#include <math.h>
#define N 10

double x[N] = {0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0};   /* hours */
double y[N] = {0, 0, 0, 1, 0, 1, 0, 1, 1, 1};                      /* 1 = pass */

double sigmoid(double z) { return 1 / (1 + exp(-z)); }

double loss(double w, double b) {
    double s = 0;
    for (int i = 0; i < N; i++) {
        double p = sigmoid(w * x[i] + b);
        s -= y[i] * log(p) + (1 - y[i]) * log(1 - p);
    }
    return s / N;
}

int main(void) {
    double w = 0, b = 0, eta = 0.5;
    printf("step    0: w = %7.4f  b = %8.4f  loss = %.4f\\n", w, b, loss(w, b));
    for (int k = 1; k <= 1000; k++) {
        double gw = 0, gb = 0;
        for (int i = 0; i < N; i++) {
            double e = sigmoid(w * x[i] + b) - y[i];
            gw += e * x[i];
            gb += e;
        }
        w -= eta * gw / N;
        b -= eta * gb / N;
        if (k == 1 || k == 10 || k == 100 || k == 1000)
            printf("step %4d: w = %7.4f  b = %8.4f  loss = %.4f\\n", k, w, b, loss(w, b));
    }
    printf("decision boundary (p = 0.5): x = %.3f hours\\n", -b / w);
    printf("P(pass) after 2 h: %.3f   after 3.5 h: %.3f\\n", sigmoid(2 * w + b), sigmoid(3.5 * w + b));
    return 0;
}
'''),
    },
    lab=dict(title='Optimization Lab',
             intro='Minimise functions of one and two variables, watch gradient descent and Newton\'s method on contour maps, see why large data sets need mini-batch (stochastic) gradient descent, and train a small classifier.',
             tabs=[
                 dict(name='Golden section', blocks=[
                     dict(p='Type f(x) and a bracket [a, b] containing one minimum. Each step keeps the part that must contain the minimum.'),
                     dict(w='golden', o=dict(f='x^4 - 3x^3 + 2', a=0, b=3, step=0, height='300px', side=True, tableHeight='300px'))]),
                 dict(name='Gradient descent', blocks=[
                     dict(p='Choose a function of x and y, a start, the method and the learning rate. The contour lines are levels of f; the path shows the iterates.'),
                     dict(w='gd2d', o=dict(f=BOWL, x0=10, y0=1, logeta=-1, steps=40, method='gd', height='340px', side=True, tableHeight='340px', presets=GPRE + [['homework 2', '(x - 1)^2 + 4*(y + 2)^2', 0, 0, -1, 'gd', [-1, 3, -3, 1]]], range=[-12, 12, -4, 4]))]),
                 dict(name='Mini-batch SGD', blocks=[
                     dict(p='Why does machine learning use <b>stochastic</b> gradient descent? The classifier of Problem 3 is trained on N students generated from the same model. Both methods get the same compute budget, counted in gradients of single data points: one full-batch step costs N of them, one mini-batch step only B.'),
                     dict(w='sgd', o=dict(N=100000, B=32, budget=1000000, logeta=-0.7, height='300px')),
                     dict(p='<b>Try:</b> (1) N = 1,000: both methods reach the minimum. (2) Raise N to 100,000 and 1,000,000 with the budget fixed: full-batch GD takes only 10 steps, then 1 step, while mini-batch SGD is unaffected by N. (3) B = 1 with η = 0.2 or 0.5: the path jitters around the minimum (noise floor); lower η or tick "decrease η". (4) B = 4096: smoother but fewer steps. Real training uses B = 32–512.')]),
                 dict(name='Code', blocks=[
                     dict(h='Golden section and Newton'), dict(code='golden', tasks=['Run it. Compare with Problem 1.', 'Change f to x^2 - 4 sin x on [0, 3] (homework 1).', 'Count the steps for tolerances 1e-4 and 1e-8: about 22 and 41.']),
                     dict(h='Logistic regression'), dict(code='logreg', tasks=['Run it. Compare with Problem 3.', 'Try eta = 0.1 and eta = 2: what happens to the loss?', 'Add a student with 6 hours who failed: how does the boundary move?']),
                     dict(h='Full batch vs mini-batch'), dict(code='minibatch', tasks=['Run it: with the same 40,000 gradients, which batch size ends with the lowest loss?', 'Make N = 20000 (keep the budget): what happens to the full-batch result, and why?', 'Try B = 1 with eta = 0.2 and eta = 0.02.'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Why is the ratio 0.618 used in golden-section search?', 'With $g = (\\sqrt5 - 1)/2$, $g^2 = 1 - g$, so one interior point of the old bracket is exactly an interior point of the new one; only one new function value is needed per step.'),
                         ('Write the gradient-descent update and explain the learning rate.', '$\\mathbf{x}_{k+1} = \\mathbf{x}_k - \\eta\\nabla f(\\mathbf{x}_k)$. $\\eta$ is the step size: too small gives slow progress, too large (above $2/\\lambda_{\\max}$ of the Hessian) makes the iteration oscillate or diverge.'),
                         ('How is gradient descent related to Euler\'s method?', 'It is Euler\'s method with step $\\eta$ for the ODE $\\mathbf{x}\' = -\\nabla f(\\mathbf{x})$ (gradient flow); its stability limit is the learning-rate limit.'),
                         ('Compare Newton\'s method and gradient descent for minimisation.', 'Newton uses second derivatives (the Hessian) and converges quadratically, exactly in one step for a quadratic, but each step costs an $n \\times n$ solve; gradient descent uses only the gradient, steps are cheap, convergence is linear and slow when the problem is ill-conditioned.'),
                         ('What is the Gauss–Newton method?', 'For nonlinear least squares: linearise the model about the current parameters with the Jacobian $J$, solve the linear least-squares problem $(J^{T}J)\\boldsymbol\\delta = J^{T}\\mathbf{r}$ for the correction, update and repeat.')])])]),
)
