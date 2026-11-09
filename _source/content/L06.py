LECTURE = dict(
    title='Root Finding and the Bisection Method',
    short='Root Finding and Bisection',
    sub='Trap the root between two points where f changes sign, then halve the interval again and again. Slow, but it never fails, and it tells you exactly how accurate it is.',
    slides=[
        dict(type='cover', id='cover', notes="Opening game: 'I am thinking of a number between 1 and 100. You may ask: is it bigger than n?' Students find it in at most 7 questions by always asking about the middle.\n\nThat is the bisection method. Every question halves the interval: 100 → 50 → 25 → ... → 1. Today we apply the same idea to equations."),
        dict(type='bullets', id='hook', title='The problem: when does the ball land?', kick='Why this lecture', rw=760,
             lead='A game engine throws a ball upward at 20 m/s from a 10 m roof, with air drag. When must it play the "bounce" sound?',
             items=['With drag, the height is $h(t) = 10 + 79.24\\,(1 - e^{-0.5t}) - 19.62\\,t$ (metres, seconds)',
                    'We need $t$ with $h(t) = 0$. Try to solve it with algebra: $t$ is trapped both inside and outside the exponential',
                    'No school formula works. Without drag, the quadratic formula gives 4.528 s; with drag the answer is different, and the game needs it <b>every frame</b>',
                    'Today: a method that finds it to any accuracy, using only the <b>sign</b> of $h(t)$'],
             frag=True,
             right=dict(table=[['$t$ (s)', '$h(t)$ (m)', 'sign'], [['0', '10.000', '+'], ['1', '21.559', '+'], ['2', '20.849', '+'], ['3', '12.699', '+'], ['4', '0.036', '+'], ['5', '−15.364', '<b>−</b>']]], frag=False),
             notes="Start the lecture with this problem, before any theory. Ask: how would you find t? Let students try for a minute. Some will try logarithms and get stuck because t appears both in e^(−0.5t) and on its own (the exact solution needs the Lambert W function, which nobody's calculator has).\\n\\nPoint at the table: the height changes sign between t = 4 and t = 5. So the landing time is in [4, 5]. The rest of the lecture turns that observation into an algorithm. We solve it in the summary slide: t = 4.002526 s.\\n\\nModel: linear drag, m = 1 kg, k = 0.5 kg/s, g = 9.81: h(t) = h0 + (m/k)(v0 + mg/k)(1 − e^(−kt/m)) − (mg/k)t."),
        dict(type='goals', id='goals', items=[
            'State the <b>root-finding problem</b> and rewrite any equation as $f(x) = 0$',
            'Use the <b>intermediate value theorem</b> to locate a bracket $[a, b]$',
            'Perform bisection <b>by hand</b> and present it as a clear iteration table',
            'Compute the <b>error bound</b> and the <b>number of iterations</b> needed',
            'Write bisection in <b>Python and C</b> (asked in past finals)',
            'Explain its <b>limitations</b> and which later methods remove them'],
            prev='Conditioning and stability: accuracy needs a well-posed problem and a careful algorithm.',
            today='The first of five root-finding methods. Bisection is the safest, the slowest, and the benchmark for all the others.',
            notes="Module 2 begins: Lectures 6–10 are all about solving f(x) = 0."),
        dict(type='bullets', id='problem', title='The root-finding problem', rw=760,
             items=['Find $x$ with $f(x) = 0$: a <b>root</b> of $f$, or a <b>zero</b>; graphically, where the curve crosses the $x$-axis',
                    'Any equation can be rewritten: $e^{x} = 3x \\;\\Rightarrow\\; f(x) = e^{x} - 3x = 0$',
                    'Polynomials of degree ≥ 5 and most transcendental equations ($\\sin$, $e^x$, $\\ln$ mixed with powers) have no formula for their roots',
                    'Two families of methods: <b>bracketing</b> (bisection, false position) and <b>open</b> (fixed point, Newton, secant)'],
             right=dict(w='root', o=dict(method='bisect', fixed=True, f='e^x - 3x', a=0, b=1, step=1, compact=True, height='300px', tableHeight='0px')),
             notes="Examples of root problems in CSE: where does a ray hit a surface (graphics), at what rate does an investment reach a target (finance, IRR), at what time does a projectile land (games), what threshold gives a 5% false-positive rate (ML).\n\nThe widget shows f(x) = e^x − 3x: two crossings, near 0.62 and 1.51. The bracket [0, 1] traps the first one."),
        dict(type='math', id='ivt', title='Trapping a root: the intermediate value theorem',
             eqs=[dict(cap='Intermediate value theorem: f continuous on [a, b]', eq='f(a)\\,f(b) < 0 \\;\\Longrightarrow\\; \\exists\\, r \\in (a,b) : f(r) = 0')],
             right=dict(table=[['$x$', '0', '1', '2', '3'], [['$f(x) = x^3 - x - 2$', '−2', '−2', '<b>+4</b>', '+22']]], cls='tb sm'), rw=760,
             below=dict(items=['A sign change guarantees at least one root (an <b>odd</b> number of roots)', 'Tabulate $f$ at a few points and look for a sign change: here $f(1) < 0 < f(2)$, so a root lies in $[1, 2]$', 'Continuity matters: $f(x) = 1/(x-1)$ changes sign on $[0, 2]$ but has no root', 'No sign change does not mean no root: $(x-1)^2$ touches zero without crossing'], frag=True),
             notes="The IVT is the whole theory behind bracketing methods. Draw it: a continuous curve going from below the axis to above it must cross the axis somewhere.\n\nThe last two bullets are the two classic failure cases; we come back to them later in the lecture."),
        dict(type='bullets', id='algo', title='The bisection algorithm', ordered=True, rw=780,
             items=['Start with $[a, b]$ where $f(a)\\,f(b) < 0$', 'Midpoint $c = \\dfrac{a + b}{2}$; compute $f(c)$', 'If $f(a)\\,f(c) < 0$, the root is in $[a, c]$: set $b = c$', 'Otherwise the root is in $[c, b]$: set $a = c$ (if $f(c) = 0$, stop: $c$ is the root)', 'Repeat until $\\dfrac{b - a}{2} < \\varepsilon$; the answer is the last midpoint'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input f, a, b, tol\nif f(a)·f(b) > 0: stop (no bracket)\nrepeat up to N times:\n    c ← (a + b) / 2\n    if f(c) = 0 or (b − a)/2 &lt; tol:\n        return c\n    if f(a)·f(c) &lt; 0:  b ← c\n    else:              a ← c</pre></div><p class="small" style="margin-top:14px">Each pass keeps the half of the bracket where the sign changes, so the root stays trapped while the bracket halves.</p>'),
             notes="Read the five steps, one per click. Stress step 3: we test f(a)·f(c) < 0, not f(c) < 0, so the algorithm works whether f increases or decreases.\n\nImplementation tip: store f(a) instead of recomputing it each time; a good bisection evaluates f only once per iteration."),
        dict(type='widget', id='bisw', title='Explore: bisection step by step', w='root', o=dict(method='bisect', fixed=True, f='x^3 - x - 2', a=1, b=2, height='330px', side=True, tableHeight='330px', dec=6), lw=420,
             items=['Press <b>Next step</b>; the shaded band is the current bracket', 'The table grows exactly as you would write it in a written solution', 'The error bound $(b-a)/2$ halves every step', 'Type your own $f(x)$, $a$ and $b$'],
             notes="Step through 4–5 iterations, asking the class to predict the sign of f(c) and which half is kept before pressing Next.\n\nThe plot zooms in automatically after a few steps so the bracket stays visible.\n\nThen let a student propose an equation from the homework sheet."),
        dict(type='table', id='table1', title='Problem 1: $x^3 - x - 2 = 0$ on $[1, 2]$',
             head=['$n$', '$a$', '$b$', '$c = \\tfrac{a+b}{2}$', '$f(c)$', 'new bracket', '$(b-a)/2$'], frag=True, ans=-1,
             rows=[[1, '1', '2', '1.5', '−0.125', '[1.5, 2]', '0.5'], [2, '1.5', '2', '1.75', '+1.609375', '[1.5, 1.75]', '0.25'], [3, '1.5', '1.75', '1.625', '+0.666016', '[1.5, 1.625]', '0.125'],
                   [4, '1.5', '1.625', '1.5625', '+0.252197', '[1.5, 1.5625]', '0.0625'], [5, '1.5', '1.5625', '1.53125', '+0.059113', '[1.5, 1.53125]', '0.03125'], [6, '1.5', '1.53125', '1.515625', '−0.034054', '[1.515625, 1.53125]', '0.015625']],
             note='$f(1) = -2 < 0$ and $f(2) = 4 > 0$. Each row keeps the half where $f$ changes sign. After 6 steps: root ≈ 1.5156 with error ≤ 0.0156. True root: 1.5213797.',
             answer='After 6 iterations $r \\approx 1.515625$, $|r - c_6| \\le 0.015625$. For 4 decimal places we need $(b-a)/2^n < 0.00005$, i.e. 15 iterations.',
             notes="Reveal one row at a time; ask for the next midpoint aloud.\n\nCheck the count: 1/2^n < 5e-5 → 2^n > 20000 → n ≥ 15 (2^15 = 32768; 2^14 = 16384 is not enough)."),
        dict(type='compare', id='classic', title='Same problem, two approaches: $x^2 - 2 = 0$', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (exact formula)', tag='Algebra', cls='blue', items=['Rearrange: $x^2 = 2 \\Rightarrow x = \\sqrt{2}$', 'Exact answer, one line of algebra', 'But to get digits you still need a square-root algorithm (inside the calculator)']),
             right=dict(h='Numerical (bisection)', tag='Algorithm', cls='key', items=['$f(1) < 0 < f(2)$: bracket $[1, 2]$', '20 halvings for $10^{-6}$: $x \\approx 1.414214$', 'Matches $\\sqrt2 = 1.4142136$: the method is validated on a problem we can check']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>Landing time with drag: $10 + 79.24(1 - e^{-0.5t}) - 19.62t = 0$</h3><p>$t$ appears inside and outside the exponential: no algebraic rearrangement isolates it (its exact form needs the Lambert W function, not an elementary function). Bisection: $t = 4.002526$ s.</p></div><p class="small frag fade">Good practice: <b>validate</b> a numerical method on a problem with a known answer before trusting it on one without.</p>'),
             notes="Use this slide to build a habit: test a numerical method first on a problem with a known answer (here √2), then trust it on problems without one.\n\nSquare roots are a nice twist: even the 'exact' answer needs a numerical algorithm to produce digits."),
        dict(type='math', id='bound', title='How accurate after $n$ steps? How many steps?',
             eqs=[dict(cap='Error bound after n bisections', eq='|r - c_n| \\le \\frac{b - a}{2^{n}}'),
                  dict(cap='Steps needed for tolerance ε', eq='\\frac{b-a}{2^n} < \\varepsilon \\;\\Longleftrightarrow\\; n > \\log_2\\frac{b - a}{\\varepsilon} = \\frac{\\ln\\big((b-a)/\\varepsilon\\big)}{\\ln 2}', frag=True)],
             items=['Example: $[1, 2]$, $\\varepsilon = 10^{-4}$: $n > \\log_2 10^4 = 13.29$, so <b>14 iterations</b>', 'Known in advance, independent of $f$: a rare luxury', 'Each step gains one binary digit; about <b>3.3 steps per decimal digit</b> ($\\log_2 10$)', 'Convergence is <b>linear</b> with rate ½: $e_{n+1} \\approx \\tfrac12 e_n$'],
             ifrag=True,
             notes="Derivation: the bracket width after n halvings is (b − a)/2^n, and both the root and the midpoint lie in the previous bracket of width (b − a)/2^(n−1), so their distance is at most half of it.\n\nThe iteration count does not depend on f at all: it only depends on the starting width and the tolerance. Neither Newton nor secant can promise this.\n\nThe widget's message line shows the same prediction."),
        dict(type='code', id='code', title='Bisection in Python and C', code='bisect', lw=560,
             items=['The loop stops when the error bound is below <code>tol</code>, or after 100 steps as a safety net', 'It checks the sign condition first and refuses a bad bracket', 'In C, <code>#define f(x)</code> is the classic textbook style; a function works too', 'Change <code>f</code>, <code>a</code>, <code>b</code> and <code>tol</code>, then run'],
             notes="Run Python then C. Both print the same table as the worked example and stop after 14 iterations with root 1.521362 (error bound 6.1e-5).\n\nThe 'for n in range(1, 101)' cap is good practice that most textbook codes omit."),
        dict(type='table', id='prob2', title='Problem 2: $x^3 + x - 1 = 0$ with $a = 0.6$, $b = 0.8$',
             src='Problem 2', q='"Write down the code for finding a real root of the equation $x^3 + x - 1 = 0$ using bisection method with initial value 0.6 and 0.8." Below: what the program prints, which you should also be able to produce by hand.',
             head=['$n$', '$a$', '$b$', '$c$', '$f(c)$', '$(b-a)/2$'], frag=True, cls='tb sm',
             rows=[[1, '0.6', '0.8', '0.7', '+0.043000', '0.1'], [2, '0.6', '0.7', '0.65', '−0.075375', '0.05'], [3, '0.65', '0.7', '0.675', '−0.017453', '0.025'], [4, '0.675', '0.7', '0.6875', '+0.012451', '0.0125'], [5, '0.675', '0.6875', '0.68125', '−0.002581', '0.00625']],
             right=dict(code='bisect_exam', lang='c', ed='420px', out='200px'), rw=820,
             notes="Run it: the root is 0.682327 (true 0.6823278).\n\nf(0.6) = −0.184 and f(0.8) = 0.312: opposite signs, so the bracket is valid."),
        dict(type='widget', id='fail', title='When bisection is fooled', w='root', o=dict(method='bisect', fixed=True, f='1/(x-1)', a=0, b=2.5, height='330px', side=True, tableHeight='330px',
             presets=[['pole: 1/(x−1)', '1/(x-1)', 0, 2.5], ['tan x on [1, 2]', 'tan(x)', 1, 2], ['double root (x−1)²', '(x-1)^2', 0, 3], ['three roots', 'x^3 - 3x', -2.5, 2.2]]), lw=460,
             items=['<b>Pole</b>: $1/(x-1)$ changes sign at $x = 1$ without a root; bisection "converges" to the pole, and $f(c)$ blows up', '<b>Double root</b>: $(x-1)^2 \\ge 0$, no sign change, bisection cannot start', '<b>Several roots</b>: it finds one of them, not necessarily the one you want', 'Defence: plot or tabulate $f$ first, and check that $|f(c)|$ really becomes small'],
             notes="Try each preset. For 1/(x − 1) step to convergence and point at the f(c) column: it grows instead of shrinking. That is the tell-tale sign of a pole.\n\nThe double root preset shows the error message: f(a) and f(b) have the same sign.\n\nThe moral: bisection guarantees convergence to a sign change, not to a root. Always check the residual |f(c)|."),
        dict(type='profile', id='profile', title='Bisection: method profile',
             best=['Any continuous $f$ with one sign change in $[a, b]$: success is <b>guaranteed</b>', 'Cost is the same for every $f$: $\\lceil\\log_2((b-a)/\\varepsilon)\\rceil$ steps (20 for $10^{-6}$ on a unit interval); only a lucky exact hit $f(c) = 0$ ends earlier', 'Noisy, step-like or black-box $f$: only the <b>sign</b> is used'],
             worst=['Even an easy, almost straight $f$ still takes 20 steps; false position needs 1 on a straight line', 'No sign change (double root $(x-1)^2$, both ends same sign): cannot start', 'A pole such as $1/(x-1)$: converges to the pole, not to a root'],
             suited=['Monotone functions from data: thresholds, rates, calibration', 'Hard real-time code that needs a <b>fixed, known</b> running time', 'The first, safe phase of a hybrid solver that hands over to Newton or secant'],
             avoid=['$f\'$ is cheap and you need many digits many times (use Newton, L9)', 'You need all roots of a polynomial, or roots of a system (L10)', '$f$ is discontinuous or you have not plotted it'],
             verdict='Rule of thumb: <b>use bisection when failure is not allowed</b>, and to get a safe starting bracket for a faster method.',
             notes="Go through the four cards. The key surprise for students: bisection's best case and worst case are the same. Its cost depends only on (b − a) and ε, never on f. That predictability is exactly why it is used in real-time systems and as a safety net.\n\nAll counts were measured with the course code (stopping when (b − a)/2 < 1e-6)."),
        dict(type='table', id='compare', title='Comparative analysis: bisection vs brute-force search', kick='Comparison',
             head=['Method', 'Idea', 'Evaluations for $10^{-6}$ on $[0, 1]$', 'Guaranteed?', 'Finds all roots in range?'], tx=(0, 1, 3, 4), frag=True,
             rows=[['Graph / guess', 'read the crossing off a plot', '—', 'no; about 2 digits', 'yes, roughly'], ['Incremental search', 'step $h = 10^{-6}$ from $a$, stop at the first sign change', 'up to 1,000,000', 'yes', 'yes (if $h$ is small enough)'], ['<b>Bisection</b>', 'halve the bracket', '<b>20</b>', 'yes', 'no: one root per bracket']],
             note='Best practice combines them: a coarse incremental search ($h = 0.1$, 10 evaluations) finds every sign change, then bisection refines each bracket in 20 more steps. Lectures 7–10 add faster refinement methods to this table.', notefrag=True,
             notes="Incremental search (tabulating f at small steps) is what students instinctively do; show why it is hopeless for accuracy (a million evaluations) but excellent for locating brackets. The combination 'coarse scan, then bisection' is the standard robust recipe.\n\nThis comparison table grows lecture by lecture; Lecture 10 has the full version."),
        dict(type='bridge', id='bridge', lead='Bisection is the benchmark: safe and predictable. Every later root-finding method keeps one of its strengths and removes one of its weaknesses.',
             keep=['Always converges once a sign change is found', 'Guaranteed error bound $(b-a)/2^n$ at every step', 'Iteration count known in advance', 'Needs only the <b>sign</b> of $f$: works on noisy or black-box functions'],
             rows=[['Slow: one binary digit per step (20 steps for $10^{-6}$)', 'Use the <b>values</b> $f(a), f(b)$, not just their signs: the chord method', 7],
                   ['Still linear; we want digits to multiply', 'Use the <b>slope</b>: tangent line (Newton), or a line through two recent points (secant, L10)', 9],
                   ['Needs a bracket with a sign change; cannot find double roots like $(x-1)^2$', '<b>Open</b> methods need only a starting guess: fixed point, Newton, secant', 8],
                   ['Solves one equation in one unknown', 'Newton for <b>systems</b> with the Jacobian matrix', 10],
                   ['Fooled by poles; finds only one of several roots', 'Tabulate or plot $f$ first; always check $|f(c)|$ (stopping rules, Lecture 1)', None]],
             notes="This slide is the map of Module 2. Reveal one row at a time and ask the class: what would fix this? before showing the answer.\\n\\nThe left card is important too: bisection is not 'the bad method'. Professional solvers (Brent's method, scipy.optimize.brentq) keep a bisection step as a safety net precisely because of these four strengths.\\n\\nThe last row is solved in this lecture: a sign table finds all sign changes in a range, and the residual |f(c)| exposes poles."),
        dict(type='apps', id='apps', lead='Click a card to see the exact step where bisection runs, with a small worked example.',
             items=[
                 dict(ic='🎮', h='Game physics: landing time', t='When does a falling object hit the ground?',
                      detail=dict(where='the collision step of the physics engine: find the time $t$ in the current frame at which the height function crosses zero, so the bounce happens at the right moment.',
                                  eq='h(t) = 10 + 79.24\\,(1 - e^{-0.5t}) - 19.62\\,t = 0', w='root', o=dict(method='bisect', fixed=True, f='10 + 79.24(1 - e^(-0.5x)) - 19.62x', a=4, b=5, tol='1e-6', height='260px', tableHeight='260px', side=True, dec=6),
                                  note='Press Run to tolerance: t = 4.002526 s (20 halvings for 10⁻⁶). Without drag it would be 4.528 s: half a second late.')),
                 dict(ic='🔍', h='git bisect', t='Which commit introduced the bug?',
                      detail=dict(where='version control. The "function" is the test result of a commit: good (old) or bad (new). The sign change is the first bad commit.',
                                  steps=['Mark commit 1 as good and commit 1000 as bad: the bug appeared somewhere in between', 'Git checks out the middle commit (500); you run the test and type <code>git bisect good</code> or <code>bad</code>', 'The range halves every time: 1000 → 500 → 250 → … → 1'],
                                  table=[['Commits to search', 'Tests needed'], [['1,000', '10'], ['100,000', '17'], ['1,000,000', '20']]],
                                  note='Same formula as today: tests needed = ⌈log₂ N⌉. Nobody tests 1,000 commits one by one.')),
                 dict(ic='🧠', h='t-SNE in machine learning', t='Choosing the Gaussian width for every data point',
                      detail=dict(where='the first stage of t-SNE (scikit-learn, the original implementation). For each point $i$, find the precision $\\beta_i = 1/(2\\sigma_i^2)$ so that the neighbour distribution has the chosen <b>perplexity</b>. Perplexity falls steadily as $\\beta$ grows, so bisection (binary search) on $\\beta$ always works.',
                                  eq='p_j = \\frac{e^{-\\beta d_j^2}}{\\sum_k e^{-\\beta d_k^2}}, \\qquad \\text{Perp}(\\beta) = 2^{-\\sum_j p_j\\log_2 p_j} \\overset{!}{=} \\text{target}',
                                  table=[['$\\beta$', '0', '0.5', '1', '2', '5'], [['Perp($\\beta$)', '4.000', '2.715', '2.046', '1.462', '1.041']]],
                                  note='Toy example: 4 neighbours at squared distances 1, 2, 4, 9 and target perplexity 2. Perp(1) > 2 > Perp(2), so the root is in [1, 2]; bisection gives β = 1.0508 (σ = 0.690). Real t-SNE repeats this for every one of thousands of points.')),
                 dict(ic='🎚️', h='Classifier threshold', t='Spam filter with exactly 5% false alarms',
                      detail=dict(where='deployment of a trained classifier. The false-positive rate FPR($t$) can only go down as the threshold $t$ goes up, so FPR($t$) − 0.05 changes sign once.',
                                  steps=['Bracket: at $t = 0$ every e-mail is flagged (FPR = 100%); at $t = 1$ none is (FPR = 0%)', 'Midpoint threshold, measure FPR on validation e-mails, keep the half where FPR − 0.05 changes sign', 'About 10 halvings fix $t$ to 0.001'],
                                  note='Bisection is ideal here because FPR(t) is a step function measured on data: there is no derivative, so Newton cannot be used.')),
                 dict(ic='🔊', h='Speech: filter cut-off frequency', t='Where does a smoothing filter lose half its power?',
                      detail=dict(where='speech pre-processing. A 5-point moving average at 8 kHz smooths a signal; its −3 dB cut-off frequency is where the gain $|H(f)|$ falls to $1/\\sqrt2$.',
                                  eq='|H(f)| = \\left|\\frac{\\sin(5\\pi f/8000)}{5\\sin(\\pi f/8000)}\\right| = \\frac{1}{\\sqrt2}',
                                  w='root', o=dict(method='bisect', fixed=True, f='abs(sin(5pi x/8000)/(5sin(pi x/8000))) - 0.70710678', a=1, b=1600, height='240px', tableHeight='240px', side=True, dec=3),
                                  note='Root: f ≈ 721.3 Hz. Telephone-band speech energy above this frequency is attenuated by more than half its power.')),
                 dict(ic='📈', h='Finance: internal rate of return', t='Which interest rate makes an investment break even?',
                      detail=dict(where='project appraisal: the IRR is the root of the net present value. NPV($r$) decreases as $r$ grows, so a sign change is easy to find.',
                                  eq='\\text{NPV}(r) = -1000 + \\frac{300}{1+r} + \\frac{300}{(1+r)^2} + \\frac{300}{(1+r)^3} + \\frac{300}{(1+r)^4} = 0',
                                  w='root', o=dict(method='bisect', fixed=True, f='-1000 + 300/(1+x) + 300/(1+x)^2 + 300/(1+x)^3 + 300/(1+x)^4', a=0, b=0.2, height='240px', tableHeight='240px', side=True, dec=6),
                                  note='NPV(0) = 200 > 0 and NPV(0.2) = −223.4 < 0. Root r = 0.077138: the IRR is 7.71%.'))],
             notes="Click one or two cards live (the game and t-SNE ones work best). Each pop-up has a working bisection widget or a numeric example.\\n\\nCommon thread: in every case the function is monotone or comes from data, has no usable derivative, or must never fail. That is when engineers choose bisection over faster methods."),
        dict(type='check', id='check', q='Bisection starts on $[0, 1]$. How many iterations guarantee an error below $10^{-6}$?',
             opts=['6', '10', '20', '1,000,000'], right=2,
             answer='C. $n > \\log_2(1/10^{-6}) = 6\\log_2 10 = 19.93$, so $n = 20$. (Each decimal digit costs about 3.3 halvings.)',
             notes="Quick mental check: 2^10 ≈ 1000, so 2^20 ≈ 10^6."),
        dict(type='summary', id='summary', items=[
            'Rewrite as $f(x) = 0$; a sign change of a continuous $f$ on $[a, b]$ traps a root (IVT)',
            'Bisection: $c = (a+b)/2$, keep the half where the sign changes',
            'Error bound $|r - c_n| \\le (b-a)/2^n$; iterations $n > \\log_2((b-a)/\\varepsilon)$',
            'Robust but slow (linear, rate ½); fails for double roots and is fooled by poles',
            'Code: sign check + halving + stopping rule + iteration cap'],
            hw=['Find the root of $e^{x} - 3x = 0$ in $[0, 1]$ by bisection, 6 iterations, as a table.', 'How many iterations are needed to find $\\sqrt{3}$ (root of $x^2 - 3$) in $[1, 2]$ to 6 decimal places?', 'Modify the C program to read $a$, $b$ and the tolerance with scanf and to print "no sign change" when needed.', 'Lab: use the solver tab to check your answer to Q1.'],
            solved='The ball lands at $t = 4.002526$ s: bisection on $[4, 5]$, 20 halvings for $10^{-6}$ (the drag-free formula would say 4.528 s).',
            next='<b>The false position method.</b> Replace the midpoint by the point where the chord crosses the axis: usually much faster, but with a surprising weakness.',
            notes="Homework answers: Q1: midpoints 0.5, 0.75, 0.625, 0.5625, 0.59375, 0.609375 (signs of f(c): +, −, −, +, +, +), root 0.619061. Q2: 1/2^n < 0.5e-6 → 2^n > 2e6 → n = 21."),
    ],
    code={
        'bisect': dict(file='bisection', py='''# Bisection method for f(x) = 0
def f(x):
    return x**3 - x - 2

a, b = 1.0, 2.0
tol = 1e-4

if f(a) * f(b) > 0:
    print("f(a) and f(b) have the same sign: choose another interval")
else:
    print(f"{'n':>2} {'a':>9} {'b':>9} {'c':>9} {'f(c)':>10} {'(b-a)/2':>9}")
    for n in range(1, 101):
        c = (a + b) / 2
        err = (b - a) / 2                 # |c - root| <= err
        print(f"{n:2d} {a:9.6f} {b:9.6f} {c:9.6f} {f(c):10.6f} {err:9.2e}")
        if f(c) == 0 or err < tol:
            break
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    print(f"root = {c:.6f} after {n} iterations (error <= {err:.1e})")
''', c='''/* Bisection method for f(x) = 0 */
#include <stdio.h>
#include <math.h>
#define f(x) ((x)*(x)*(x) - (x) - 2)

int main(void) {
    double a = 1.0, b = 2.0, tol = 1e-4, c = a, err = b - a;
    int n;

    if (f(a) * f(b) > 0) {
        printf("f(a) and f(b) have the same sign: choose another interval\\n");
        return 1;
    }
    printf("%2s %9s %9s %9s %10s %9s\\n", "n", "a", "b", "c", "f(c)", "(b-a)/2");
    for (n = 1; n <= 100; n++) {
        c = (a + b) / 2;
        err = (b - a) / 2;               /* |c - root| <= err */
        printf("%2d %9.6f %9.6f %9.6f %10.6f %9.2e\\n", n, a, b, c, f(c), err);
        if (f(c) == 0 || err < tol)
            break;
        if (f(a) * f(c) < 0)
            b = c;
        else
            a = c;
    }
    printf("root = %.6f after %d iterations (error <= %.1e)\\n", c, n, err);
    return 0;
}
'''),
        'bisect_exam': dict(file='bisection_exam', c='''/* Bisection: root of x^3 + x - 1 = 0, a = 0.6, b = 0.8 */
#include <stdio.h>
#include <math.h>
#define f(x) ((x)*(x)*(x) + (x) - 1)

int main(void) {
    double a = 0.6, b = 0.8, c, tol = 0.0001;
    int i = 0;
    if (f(a) * f(b) > 0) {
        printf("Invalid interval\\n");
        return 0;
    }
    do {
        c = (a + b) / 2;
        i++;
        printf("%d  a=%.6f  b=%.6f  c=%.6f  f(c)=%.6f\\n", i, a, b, c, f(c));
        if (f(a) * f(c) < 0)
            b = c;
        else
            a = c;
    } while (fabs(b - a) > tol);
    printf("Root = %.6f\\n", (a + b) / 2);
    return 0;
}
''', py='''# Bisection: root of x^3 + x - 1 = 0, a = 0.6, b = 0.8
def f(x):
    return x**3 + x - 1

a, b, tol = 0.6, 0.8, 0.0001
if f(a) * f(b) > 0:
    print("Invalid interval")
else:
    i = 0
    while True:
        c = (a + b) / 2
        i += 1
        print(f"{i}  a={a:.6f}  b={b:.6f}  c={c:.6f}  f(c)={f(c):.6f}")
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        if abs(b - a) <= tol:
            break
    print(f"Root = {(a + b) / 2:.6f}")
'''),
        'iters': dict(file='bisection_count', py='''import math

# iterations needed: n > log2((b - a) / tol)
for (a, b, tol) in [(1, 2, 1e-4), (0, 1, 1e-6), (0, 10, 1e-8), (1, 2, 0.5e-4)]:
    n = math.ceil(math.log2((b - a) / tol))
    print(f"[{a}, {b}], tol = {tol:g}:  n = {n}")
'''),
    },
    lab=dict(title='Bisection Lab',
             intro='Step through bisection, check your own hand calculations with the solver, and write the method in Python and C.',
             tabs=[
                 dict(name='Explore', blocks=[
                     dict(p='Step through bisection. The band is the current bracket; the table is the iteration table you write by hand.'),
                     dict(w='root', o=dict(method='bisect', fixed=True, f='x^3 - x - 2', a=1, b=2, height='320px', side=True, tableHeight='320px',
                                            presets=[['x³ − x − 2', 'x^3 - x - 2', 1, 2], ['eˣ − 3x', 'e^x - 3x', 0, 1], ['x³ + x − 1', 'x^3 + x - 1', 0.6, 0.8], ['cos x − x', 'cos(x) - x', 0, 1], ['pole 1/(x−1)', '1/(x-1)', 0, 2.5]]))]),
                 dict(name='Solver: your problem', blocks=[
                     dict(p='Type any equation f(x) = 0 in ordinary textbook notation (e.g. <code>x^3 - 2x - 5</code>, <code>3x + sin x - e^x</code>, <code>x log10(x) - 1.2</code>), choose a method and press <b>Run to tolerance</b>. Use it to check your homework tables, not to replace working them out.'),
                     dict(w='root', o=dict(method='bisect', f='x^3 - 2x - 5', a=2, b=3, height='300px', tableHeight='420px'))]),
                 dict(name='Code', blocks=[
                     dict(h='Bisection'), dict(code='bisect', tasks=['Run it. How many iterations for tol = 1e-4? Does it match log₂(1/tol)?', 'Change f to e^x − 3x (use math.exp or exp) with [0, 1].', 'Set tol = 1e-12. How many iterations now?', 'Try [3, 4]. What does the program print?']),
                     dict(h='The textbook program'), dict(code='bisect_exam', lang='c', tasks=['Run it. What root does it print?', 'Change the stopping test to fabs(f(c)) < 1e-6. Is the answer the same?', 'Rewrite it with a function double f(double x) instead of #define.']),
                     dict(h='Iteration count'), dict(code='iters', tasks=['Run it. Explain the last line (4 decimal places).'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Find a root of $x^3 - 2x - 5 = 0$ by bisection, correct to 2 decimal places.', 'Sign change: $f(2) = -1$, $f(3) = 16$. Midpoints: 2.5 (+5.625), 2.25 (+1.891), 2.125 (+0.346), 2.0625 (−0.351), 2.09375 (−0.009), 2.109375 (+0.167), 2.1015625 (+0.079). Root ≈ 2.09 (true 2.0945515).'),
                         ('Show that $\\cos x = x$ has a root in $[0, 1]$ and find it by 5 bisection steps.', '$f(x) = \\cos x - x$: $f(0) = 1 > 0$, $f(1) = -0.4597 < 0$. Midpoints 0.5, 0.75, 0.625, 0.6875, 0.71875 → bracket [0.71875, 0.75]; root ≈ 0.734 (true 0.739085).'),
                         ('How many bisection steps are needed on $[2, 3]$ for an error below $10^{-5}$?', '$n > \\log_2(1/10^{-5}) = 16.6$, so 17 steps.'),
                         ('State two advantages and two disadvantages of the bisection method.', 'Advantages: always converges with a valid bracket; known error bound and iteration count. Disadvantages: slow (linear); needs a sign change, so it cannot find double roots and can be fooled by discontinuities.'),
                         ('Why can bisection not find the root of $f(x) = (x - 2)^2$?', '$f(x) \\ge 0$ for all $x$: there is no interval with $f(a)f(b) < 0$, so no starting bracket exists.'),
                         ('Write a C program for bisection on $x^3 + x - 1 = 0$ with $a = 0.6$, $b = 0.8$.', 'See the "textbook program" in the Code tab: #define f(x), sign check, do-while loop with c = (a+b)/2, update a or b, stop when |b − a| ≤ tol, print the root (0.682327).')])])]),
)
