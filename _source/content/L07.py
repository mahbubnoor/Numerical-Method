LECTURE = dict(
    title='The False Position Method',
    short='False Position (Regula Falsi)',
    sub='Bisection ignores how big f(a) and f(b) are. False position draws the straight line between them and takes its crossing: usually much faster, still safely bracketed.',
    slides=[
        dict(type='cover', id='cover', notes="Opening question: \"f(1) = −0.01 and f(2) = 100. Where would you guess the root is?\" Everyone says: very close to 1. Bisection would still try 1.5.\n\nToday's method uses that common sense: it weighs the endpoints by the size of f. Regula falsi is Latin for 'rule of false position': guess, measure the error, correct proportionally. It is over 3,000 years old (Egyptian papyri)."),
        dict(type='bullets', id='hook', title='The problem: bisection throws information away', kick='Why this lecture', rw=760,
             lead='Bisection needed 20 steps for $x^3 - x - 2 = 0$ on $[1, 2]$. Look at what it ignored.',
             items=['$f(1) = -2$ and $f(2) = 4$: the function is twice as far from zero at $x = 2$ as at $x = 1$', 'Common sense: the root should be about one third of the way from 1 to 2, not in the middle', 'Bisection used only the <b>signs</b> $-$ and $+$; the sizes 2 and 4 were thrown away', 'Today: use the sizes too, and see whether that is always a good idea'],
             frag=True,
             right=dict(table=[['$x$', '$f(x)$'], [['1', '−2'], ['2', '+4'], ['bisection guess', '1.5'], ['"proportional" guess', '$1 + \\tfrac{2}{2+4} = 1.333$'], ['true root', '1.5214']]]),
             notes="Ask the class to guess the root from f(1) = −2 and f(2) = 4 before showing the table. Most will say 'closer to 1'. That instinct is linear interpolation, and it is today's method.\n\nThe last bullet foreshadows the twist: the proportional guess is great on nearly straight functions and poor on strongly curved ones."),
        dict(type='goals', id='goals', items=[
            'Derive the <b>false position</b> formula from the chord through $(a, f(a))$ and $(b, f(b))$',
            'Carry out false position by hand and present the iteration table',
            'Give an honest <b>error bound</b> after $n$ iterations',
            'Compare false position with bisection, including its <b>one-sided</b> weakness and the Illinois fix',
            'Know its <b>best and worst cases</b>, and which later methods remove its limitations'],
            prev='Bisection: halve the bracket each time. Safe, error bound $(b-a)/2^n$, but only one bit per step.',
            today='Keep the bracket (safety) but choose a smarter point inside it (speed).',
            notes=""),
        dict(type='math', id='derive', title='The idea: follow the chord',
             lead='Join $(a, f(a))$ and $(b, f(b))$ with a straight line; take the point $c$ where it crosses the $x$-axis.',
             eqs=[dict(cap='Line through the two points', eq='y - f(b) = \\frac{f(b) - f(a)}{b - a}\\,(x - b)'),
                  dict(cap='Set y = 0 and solve for x', eq='c = b - f(b)\\,\\frac{b - a}{f(b) - f(a)} \\;=\\; \\frac{a\\,f(b) - b\\,f(a)}{f(b) - f(a)}', frag=True)],
             items=['Same bracketing rule as bisection: keep the sub-interval where $f$ changes sign', 'If $|f(a)| \\ll |f(b)|$, then $c$ lands close to $a$, as common sense suggests', 'The second form is easiest by calculator; the first is safer in code (less cancellation)', 'It is linear interpolation: we pretend $f$ is a straight line between $a$ and $b$'],
             ifrag=True,
             notes="Derive on the board: slope m = (f(b) − f(a))/(b − a); line y = f(b) + m(x − b); set y = 0: x = b − f(b)/m.\n\nCheck the symmetric form: c = (a f(b) − b f(a))/(f(b) − f(a)). Memorise one of them; both appear in textbooks.\n\nSimilar-triangles derivation (alternative): (c − a)/(−f(a)) = (b − c)/f(b)."),
        dict(type='bullets', id='algo', title='The false position algorithm', kick='The method, step by step', ordered=True, rw=780,
             items=['Start with $[a, b]$ where $f(a)\\,f(b) < 0$', 'Chord point $c = \\dfrac{a\\,f(b) - b\\,f(a)}{f(b) - f(a)}$; compute $f(c)$', 'If $f(a)\\,f(c) < 0$, the root is in $[a, c]$: set $b = c$', 'Otherwise the root is in $[c, b]$: set $a = c$ (if $f(c) = 0$, stop: $c$ is the root)', 'Repeat until two successive $c$ agree: $|c_n - c_{n-1}| < \\varepsilon$; the answer is the last $c$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 25px/1.55 var(--mono);color:#f5f3ee">input f, a, b, tol\nfa ← f(a);  fb ← f(b)\nif fa·fb &gt; 0: stop (no bracket)\nc_old ← a\nrepeat up to N times:\n    c  ← (a·fb − b·fa) / (fb − fa)\n    fc ← f(c)\n    if fc = 0 or |c − c_old| &lt; tol:\n        return c\n    if fa·fc &lt; 0:  b ← c;  fb ← fc\n    else:          a ← c;  fa ← fc\n    c_old ← c</pre></div><p class="small" style="margin-top:14px">Only step 2 differs from bisection. The stopping test changes too, because one end of the bracket may never move, so $(b - a)$ need not shrink.</p>'),
             notes='Put this beside the bisection algorithm from the last lecture: steps 1, 3, 4 are identical; only the formula for c and the stopping rule change.\n\nStore fa and fb: false position, like bisection, should evaluate f once per iteration.\n\nThen go straight to the widget and the worked problems.'),
        dict(type='widget', id='fpw', title='Explore: chord after chord', w='root', o=dict(method='falsi', fixed=True, f='x^3 - x - 2', a=1, b=2, height='420px', side=True, tableHeight='420px', dec=6), lw=420,
             items=['The orange chord joins the current endpoints', 'Its crossing is the new point $c$', 'Watch which endpoint moves: here only $a$ moves, $b = 2$ never changes', 'Compare the speed with bisection (previous lecture)'],
             notes="Step through 5–6 iterations. Point out that the right endpoint stays fixed at b = 2 for every step: the function is convex (curving upward) on [1, 2], so every chord lies above the curve and every c falls on the left of the root.\n\nThis 'one-sided' behaviour is the key weakness we discuss later. Here it is harmless: the iterates still approach 1.5214 quickly."),
        dict(type='table', id='q3b', title='Problem 1: $x^3 - x - 2 = 0$ on $[1, 2]$, three iterations',
             src='Problem 1', q='"Using the False Position method, find the root of $f(x) = x^3 - x - 2 = 0$, taking the initial bracketing interval $[1, 2]$. Perform three iterations, tabulating $x_1, x_2, x_3$ and $f(x)$ at each step, and report the absolute error bound after the third iteration."',
             head=['$n$', '$a$', '$b$', '$f(a)$', '$f(b)$', '$x_n = \\dfrac{af(b) - bf(a)}{f(b) - f(a)}$', '$f(x_n)$'], frag=True, cls='tb sm',
             rows=[[1, '1', '2', '−2', '4', '$\\frac{1(4) - 2(-2)}{4 + 2} = 1.333333$', '−0.962963'], [2, '1.333333', '2', '−0.962963', '4', '1.462687', '−0.333339'], [3, '1.462687', '2', '−0.333339', '4', '1.504019', '−0.101818']],
             note='Every $f(x_n) < 0$, so $a$ moves and $b = 2$ stays. Next slide: the error bound.',
             notes="Arithmetic for x2: (1.333333 × 4 − 2 × (−0.962963)) / (4 + 0.962963) = (5.333333 + 1.925926) / 4.962963 = 7.259259 / 4.962963 = 1.462687.\n\nx3: (1.462687 × 4 + 2 × 0.333339) / 4.333339 = (5.850746 + 0.666678) / 4.333339 = 6.517424 / 4.333339 = 1.504019."),
        dict(type='worked', id='bound', title='The error bound after three iterations',
             src='Problem 2', q='After $x_3 = 1.504019$ with $f(x_3) = -0.101818$, how far can we be from the true root?',
             steps=['<b>Bracket bound</b> (always valid): the root is in $[x_3, 2]$, so $|r - x_3| \\le 2 - 1.504019 = 0.496$. True, but useless: the bracket does not shrink to zero',
                    '<b>Change between iterates</b> (an estimate, not a guarantee): $|x_3 - x_2| = 0.041$',
                    '<b>Mean value bound</b> (rigorous and sharp): $f(x_3) = f(x_3) - f(r) = f\'(\\xi)(x_3 - r)$, so $|r - x_3| \\le \\dfrac{|f(x_3)|}{\\min |f\'|}$ on $[x_3, 2]$',
                    '$f\'(x) = 3x^2 - 1$ is increasing, so $\\min f\' = f\'(1.504019) = 5.786$: $\\;|r - x_3| \\le \\dfrac{0.101818}{5.786} = 0.0176$'],
             answer='Absolute error bound ≈ 0.018 (true root 1.5213797, actual error 0.01736 ✓). The bracket width alone (0.496) would be a very poor bound.',
             notes="Most students write |x3 − x2| = 0.0413 and call it an error bound; it is an estimate, and here it happens to be larger than the true error, but it is not guaranteed.\n\nThe mean value theorem bound is rigorous: f(x3) − f(r) = f'(ξ)(x3 − r) for some ξ between them, and |f'(ξ)| ≥ min|f'| on the bracket."),
        dict(type='table', id='mid', title='Problem 3: $e^{x} - 3x = 0$ on $[0, 1]$',
             src='Problem 3', q='"Find out the root of the following equation using the false position method: $e^{x} - 3x = 0$ in $[0, 1]$."',
             head=['$n$', '$a$', '$b$', '$f(a)$', '$f(b)$', '$x_n$', '$f(x_n)$'], frag=True, cls='tb sm', ans=-1,
             rows=[[1, '0', '1', '1', '−0.281718', '0.780203', '−0.158694'], [2, '0', '0.780203', '1', '−0.158694', '0.673347', '−0.059252'], [3, '0', '0.673347', '1', '−0.059252', '0.635682', '−0.018736'],
                   [4, '0', '0.635682', '1', '−0.018736', '0.623991', '−0.005611'], [5, '0', '0.623991', '1', '−0.005611', '0.620509', '−0.001653'], [6, '0', '0.620509', '1', '−0.001653', '0.619485', '−0.000484']],
             note='Here $b$ moves and $a = 0$ is stuck. Root ≈ 0.6195 after 6 steps (true 0.6190613). Converging, but only about one digit every two steps.',
             notes="Note the mirror image of the previous example: f is convex here too, but decreasing, so now the left endpoint is the stuck one.\n\nPoint out the first step: x1 = (0 × (−0.281718) − 1 × 1)/(−0.281718 − 1) = −1/−1.281718 = 0.780203."),
        dict(type='table', id='q1b', title='Problem 4: $x^3 + x^2 - 3x - 3 = 0$ between 1 and 2',
             src='Problem 4', q='"Establish the method of false position for finding roots of algebraic equations. Find by the method of Regula Falsi a root of $x^3 + x^2 - 3x - 3 = 0$ lying between 1 and 2."',
             head=['$n$', '$a$', '$b$', '$f(a)$', '$f(b)$', '$x_n$', '$f(x_n)$'], frag=True, cls='tb sm', ans=-1,
             rows=[[1, '1', '2', '−4', '3', '1.571429', '−1.364431'], [2, '1.571429', '2', '−1.364431', '3', '1.705411', '−0.247745'], [3, '1.705411', '2', '−0.247745', '3', '1.727883', '−0.039340'],
                   [4, '1.727883', '2', '−0.039340', '3', '1.731405', '−0.006111'], [5, '1.731405', '2', '−0.006111', '3', '1.731951', '−0.000946']],
             note='Bonus check: $x^3 + x^2 - 3x - 3 = (x + 1)(x^2 - 3)$, so the exact root is $\\sqrt{3} = 1.7320508$. After 5 steps: 1.7320 (4 correct decimals).',
             notes="'Establish the method' means derive the formula (slide 4) before computing. Spend one line on the chord, one on the formula."),
        dict(type='compare', id='classic', title='Same problem, two approaches: $x^3 + x^2 - 3x - 3 = 0$', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (exact formula)', tag='Algebra', cls='blue', items=['Spot the factor: $x^2(x+1) - 3(x+1) = (x+1)(x^2 - 3)$', 'Roots $-1$ and $\\pm\\sqrt3$; in $[1, 2]$: $x = \\sqrt3$', 'Works only because a factorisation happens to exist']),
             right=dict(h='Numerical (false position)', tag='Algorithm', cls='key', items=['Bracket $[1, 2]$: $f(1) = -4$, $f(2) = 3$', '9 iterations for $10^{-6}$: $x \\approx 1.732051$', 'Matches $\\sqrt3 = 1.7320508$, and needed no clever factoring']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>$e^{x} = 3x$ (Problem 3)</h3><p>Mixing $e^x$ with a polynomial in $x$ leaves no algebraic route; the root has no expression in elementary functions. False position: $x = 0.619061$ in 12 iterations.</p></div>'),
             notes='Factoring is a lucky shortcut: change one coefficient (x³ + x² − 3x − 2.9) and it disappears, but false position works exactly the same.'),
        dict(type='code', id='code', title='False position in Python and C', code='falsi', lw=560,
             items=['Same structure as bisection; only the formula for $c$ changes', 'Stops when two successive $c$ agree within <code>tol</code>, or when $f(c) = 0$', 'The C version stores $f(a)$ and $f(b)$ so each step costs one evaluation', 'Try $x^{10} - 1$ on $[0, 1.3]$ and count the iterations'],
             notes="Run both tabs.\n\nThe stopping rule |c_n − c_{n−1}| < tol is the usual practical choice for false position, since (b − a) does not shrink."),
        dict(type='exam', id='practice', src='Problem 5',
             q='"Discuss the method of False Position to find an approximate root of an equation $f(x) = 0$."',
             tips=['Start from a bracket $[a, b]$ with $f(a)f(b) < 0$ (IVT guarantees a root)', 'Replace the curve by the chord; derive $c = \\dfrac{af(b) - bf(a)}{f(b) - f(a)}$ with a small sketch', 'Keep the sub-interval with the sign change; repeat until $|c_n - c_{n-1}| < \\varepsilon$',
                   'Advantages: always converges, usually faster than bisection. Limitation: one endpoint can stay fixed, convergence becomes slow (linear) for strongly curved $f$'],
             notes=""),
        dict(type='widget', id='slow', title='The weakness: one endpoint gets stuck', w='root', o=dict(method='falsi', fixed=True, f='x^10 - 1', a=0, b=1.3, height='420px', side=True, tableHeight='420px', dec=6,
             presets=[['x¹⁰ − 1 on [0, 1.3]', 'x^10 - 1', 0, 1.3], ['x³ − x − 2 on [1, 2]', 'x^3 - x - 2', 1, 2], ['eˣ − 3x on [0, 1]', 'e^x - 3x', 0, 1]]), lw=470,
             items=['$f(x) = x^{10} - 1$ on $[0, 1.3]$: root at 1', '$f(1.3) = 12.8$ is huge, $f(0) = -1$; the chords all cross far left', 'False position needs <b>57</b> iterations for $10^{-6}$; bisection needs <b>21</b>', 'Fix (<b>Illinois method</b>): when the same end is kept twice, halve its stored $f$ value; this restores fast convergence (14 steps here instead of 57)'],
             notes="Press Run to tolerance and show the iteration count, then switch the preset back to x³ − x − 2 for contrast.\n\nWhy it happens: for a convex function the chord always lies above the curve, so c is always on the same side of the root; the far endpoint b = 1.3 never moves and keeps dragging the chord.\n\nThe Illinois modification is a one-line change; modern safeguarded methods (Brent's method, used by scipy.optimize.brentq) go further and mix bisection, secant and inverse quadratic steps."),
        dict(type='profile', id='profile', title='False position: method profile',
             best=['$f$ nearly <b>straight</b> on the bracket: on a straight line it is exact in <b>1 step</b> (bisection needs 20)', 'Smooth, gently curved $f$: $x^3 - x - 2$ and $e^x - 3x$ need 12 steps for $10^{-6}$, bisection 20', 'Keeps the bracket: it can never lose the root'],
             worst=['Strong curvature with the root near one end: $x^{10} - 1$ on $[0, 1.3]$ needs <b>57</b> steps (bisection 21)', 'One endpoint stays fixed, so the bracket never shrinks and gives no useful error bound', 'Same as bisection: needs a sign change, fooled by poles'],
             suited=['Smooth monotone functions where a bracket is available', 'Inverting tables and calibration curves (one step = linear interpolation)', 'The <b>Illinois</b> variant: a cheap, safe default for 1-D problems'],
             avoid=['$f$ is strongly convex or concave on the bracket', 'You need an error bound at every step (use bisection)', '$f\'$ is available and you want quadratic speed (use Newton)'],
             verdict='Rule of thumb: <b>prefer Illinois to plain false position</b>; it keeps the speed on easy problems and fixes the stall on hard ones.',
             notes="All counts measured with the course code, stopping when successive estimates differ by less than 1e-6.\n\nStraight-line case: for f(x) = 2x − 1 on [0, 0.8], the first false-position point is exactly 0.5, because the chord is the function itself."),
        dict(type='table', id='compare', title='Comparative analysis: bisection, false position, Illinois', kick='Comparison',
             head=['$f(x)$, bracket', 'Bisection', 'False position', 'Illinois', 'Winner'], tx=(0, 4), frag=True,
             rows=[['$x^3 - x - 2$, $[1, 2]$', '20', '12', '<b>8</b>', 'Illinois'], ['$e^x - 3x$, $[0, 1]$', '20', '12', '<b>8</b>', 'Illinois'], ['$x^2 - 4x - 10$, $[5, 6]$', '20', '<b>5</b>', '<b>5</b>', 'false position / Illinois'], ['$x^{10} - 1$, $[0, 1.3]$', '21', '57', '<b>14</b>', 'Illinois (plain FP loses)']],
             note='Iterations to reach $10^{-6}$. Bisection never wins on speed but never loses badly; plain false position can be the best or the worst; Illinois is never bad on these problems.', notefrag=True,
             notes="This is the measured comparative analysis. The pattern to teach: plain false position has high variance; Illinois has the speed without the stall; bisection has no variance at all.\n\nThe Illinois rule: when the same endpoint is retained twice in a row, halve its stored function value."),
        dict(type='bridge', id='bridge', lead='False position keeps bisection\'s safety and adds speed on easy problems. What is still missing:',
             keep=['Bracketing: always converges', 'Uses function values, so fast on nearly linear $f$', 'No derivative needed', 'Exact in one step for linear $f$'],
             rows=[['One endpoint gets stuck (slow on curved $f$)', 'Illinois: halve the stuck $f$ value', None],
                   ['Still linear convergence', 'Use the tangent: quadratic convergence', 9],
                   ['Needs a bracket with a sign change', 'Open methods start from a guess: fixed point', 8],
                   ['Keeping old points slows it down', 'Always use the two newest points: the secant method', 10],
                   ['One equation only', 'Newton for systems', 10]],
             notes="The fourth row is the key insight for Lecture 10: false position and secant use the same formula; secant simply drops the bracket and always keeps the newest two points."),
        dict(type='apps', id='apps', n=3, lead='Click a card to see where "follow the chord" is used.',
             items=[
                 dict(ic='🧮', h='Ancient algebra: double false position', t='Solving problems before algebra existed',
                      detail=dict(where='Chinese <i>Nine Chapters on the Mathematical Art</i> (chapter 7, about 200 BCE), later Arabic and European arithmetic books. For a linear problem, two wrong guesses and their errors give the exact answer by the chord formula.',
                                  steps=['Problem: people buy an item together. If each pays 8, there is 3 too much; if each pays 7, there is 4 too little. How many people, and what is the price?', 'Let $f(p)$ = surplus when each pays $p$: $f(8) = +3$, $f(7) = -4$', 'False position: $p = \\dfrac{7\\cdot 3 - 8\\cdot(-4)}{3 - (-4)} = \\dfrac{53}{7}$; the number of people is $\\dfrac{3 + 4}{8 - 7} = 7$', 'Price $= 8\\times 7 - 3 = 53$. Exact, because the surplus is a linear function of the payment'],
                                  note='This is why the method is called "rule of false position": you start from deliberately false guesses.')),
                 dict(ic='🖼️', h='Graphics: parallax occlusion mapping', t='Making a flat wall look bumpy in games',
                      detail=dict(where='the pixel shader. For each pixel, march along the view ray in a few steps until it passes below the height map; the crossing lies between the last two samples.',
                                  steps=['Sample the ray depth $d$ and the height-map value at, say, 16 steps; stop when the ray goes below the surface', 'Now $g(t) = \\text{ray}(t) - \\text{height}(t)$ changes sign between the last two samples $t_a$, $t_b$', 'One false-position (linear interpolation) step: $t^* = \\dfrac{t_a g(t_b) - t_b g(t_a)}{g(t_b) - g(t_a)}$', 'Read the texture at $t^*$: smooth bumps with no visible stair-steps'],
                                  note='One chord step is cheap enough to run for millions of pixels per frame; a full bisection would be too slow.')),
                 dict(ic='🐍', h='SciPy brentq', t='The root finder most Python code really uses',
                      detail=dict(where='<code>scipy.optimize.brentq(f, a, b)</code>. Brent\'s method keeps a bracket like bisection, but tries an interpolation step (secant or inverse quadratic) first and falls back to bisection when that step is poor.',
                                  steps=['Start: $f(a)f(b) < 0$, exactly as today', 'Each step: try the interpolated point (the false-position idea, refined)', 'If it falls outside the bracket or progress is too slow, take a bisection step instead', 'Result: never slower than bisection, usually as fast as secant'],
                                  note='This is the professional answer to the question "bisection or false position?": combine them, with safeguards.'))],
             notes="The Nine Chapters example is a lovely historical hook and an exact illustration of false position on a linear function.\n\nBrent's method connects Lectures 6, 7 and 10: students who understand those three lectures understand what scipy.optimize.brentq does internally."),
        dict(type='check', id='check', q='False position on $[1, 2]$ with $f(1) = -3$ and $f(2) = 1$. What is the first estimate $x_1$?',
             opts=['1.25', '1.5', '1.75', '1.333'], right=2,
             answer='C. $x_1 = \\dfrac{1(1) - 2(-3)}{1 - (-3)} = \\dfrac{7}{4} = 1.75$. The root is closer to $b$ because $|f(b)| < |f(a)|$.',
             notes="Quick calculation. Ask a follow-up: what would bisection choose? (1.5.)"),
        dict(type='summary', id='summary', items=[
            'False position: $c = \\dfrac{af(b) - bf(a)}{f(b) - f(a)}$, the root of the chord; keep the sign-change half',
            'Always converges (bracketing), usually faster than bisection',
            'One endpoint often stays fixed: the bracket does not shrink to zero; error bound via $|f(c)|/\\min|f\'|$',
            'Very slow for strongly curved $f$ (e.g. $x^{10} - 1$); the Illinois fix halves the stuck $f$ value'],
            hw=['Find the root of $x \\log_{10} x - 1.2 = 0$ in $[2, 3]$ by false position, 4 iterations.', 'Repeat Problem 1 by bisection for 3 iterations. Which method is closer to the true root 1.52138 after 3 steps?', 'Implement the Illinois modification in the Python code and count iterations for $x^{10} - 1$ on $[0, 1.3]$.', 'Lab: solve $x^3 - 5x + 1 = 0$ in $[0, 1]$ with both methods in the solver tab.'],
            solved='The proportional guess 1.333 was the first false-position point. Continuing gives the root 1.521380 in 12 steps (bisection: 20; Illinois: 8).',
            next='<b>Fixed-point iteration.</b> Rewrite $f(x) = 0$ as $x = g(x)$ and simply repeat. When does that work? (Often called the "iteration method".)',
            notes="Homework answers: Q1: f(2) = −0.59794, f(3) = 0.23136; x1 = 2.721014, f = −0.01709; x2 = 2.740206, f = −0.00038; x3 = 2.740636; root 2.7406462. Q2: bisection gives 1.5, 1.75, 1.625 (error 0.10) vs false position 1.504019 (error 0.017): false position is closer. Q3: 14 iterations (stopping when successive estimates differ by less than 1e-6)."),
    ],
    code={
        'falsi': dict(file='false_position', py='''# False position (Regula Falsi) for f(x) = 0
def f(x):
    return x**3 - x - 2

a, b = 1.0, 2.0
tol = 1e-6
fa, fb = f(a), f(b)

if fa * fb > 0:
    print("f(a) and f(b) have the same sign")
else:
    c_old = None
    for n in range(1, 101):
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        print(f"{n:2d}  a={a:.6f}  b={b:.6f}  c={c:.6f}  f(c)={fc: .6f}")
        if fc == 0 or (c_old is not None and abs(c - c_old) < tol):
            break
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        c_old = c
    print(f"root = {c:.6f} after {n} iterations")
''', c='''/* False position (Regula Falsi) for f(x) = 0 */
#include <stdio.h>
#include <math.h>

double f(double x) { return x * x * x - x - 2; }

int main(void) {
    double a = 1.0, b = 2.0, tol = 1e-6;
    double fa = f(a), fb = f(b), c = a, c_old = a, fc;
    int n;
    if (fa * fb > 0) { printf("f(a) and f(b) have the same sign\\n"); return 1; }
    for (n = 1; n <= 100; n++) {
        c = (a * fb - b * fa) / (fb - fa);
        fc = f(c);
        printf("%2d  a=%.6f  b=%.6f  c=%.6f  f(c)=% .6f\\n", n, a, b, c, fc);
        if (fc == 0 || (n > 1 && fabs(c - c_old) < tol)) break;
        if (fa * fc < 0) { b = c; fb = fc; }
        else             { a = c; fa = fc; }
        c_old = c;
    }
    printf("root = %.6f after %d iterations\\n", c, n);
    return 0;
}
'''),
        'race2': dict(file='bisect_vs_falsi', py='''import math

def count(method, f, a, b, tol=1e-6):
    fa, fb = f(a), f(b)
    prev = None
    for n in range(1, 1000):
        if method == "bisection":
            c = (a + b) / 2
            done = (b - a) / 2 < tol
        else:
            c = (a * fb - b * fa) / (fb - fa)
            done = prev is not None and abs(c - prev) < tol
        if done:
            return n, c
        fc = f(c)
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        prev = c

tests = [("x^3 - x - 2", lambda x: x**3 - x - 2, 1, 2),
         ("e^x - 3x", lambda x: math.exp(x) - 3*x, 0, 1),
         ("x^10 - 1", lambda x: x**10 - 1, 0, 1.3)]
for name, f, a, b in tests:
    nb, rb = count("bisection", f, a, b)
    nf, rf = count("false position", f, a, b)
    print(f"{name:12s} bisection: {nb:3d} iterations   false position: {nf:3d} iterations")
'''),
    },
    lab=dict(title='False Position Lab',
             intro='Watch chords converge, compare with bisection, and see when false position stalls.',
             tabs=[
                 dict(name='Explore', blocks=[
                     dict(p='Each step draws the chord between the current endpoints. Watch which endpoint moves.'),
                     dict(w='root', o=dict(method='falsi', fixed=True, f='x^3 - x - 2', a=1, b=2, height='330px', side=True, tableHeight='330px',
                                            presets=[['x³ − x − 2', 'x^3 - x - 2', 1, 2], ['eˣ − 3x', 'e^x - 3x', 0, 1], ['x³ + x² − 3x − 3', 'x^3 + x^2 - 3x - 3', 1, 2], ['x¹⁰ − 1 (slow!)', 'x^10 - 1', 0, 1.3]]))]),
                 dict(name='Solver: your problem', blocks=[
                     dict(p='Choose bisection or false position, type your equation and interval, and build the table step by step.'),
                     dict(w='root', o=dict(method='falsi', f='x log10(x) - 1.2', a=2, b=3, height='300px', tableHeight='420px'))]),
                 dict(name='Code', blocks=[
                     dict(h='False position'), dict(code='falsi', tasks=['Run it. Compare rows 1–3 with the Problem 1 table.', 'Change f to e^x − 3x on [0, 1] (Python: import math).', 'Add the Illinois fix: when the same endpoint is kept twice in a row, halve its stored f value.']),
                     dict(h='Bisection vs false position'), dict(code='race2', tasks=['Run it. Which method wins on each function?', 'Add cos(x) − x on [0, 1]. Prediction first, then run.'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Derive the false position formula.', 'The chord through $(a, f(a))$ and $(b, f(b))$ is $y - f(b) = \\frac{f(b)-f(a)}{b-a}(x - b)$. Setting $y = 0$: $c = b - f(b)\\frac{b-a}{f(b)-f(a)} = \\frac{af(b) - bf(a)}{f(b) - f(a)}$.'),
                         ('Find the root of $x^3 - 5x + 1 = 0$ in $[0, 1]$ by false position, 3 iterations.', '$f(0) = 1$, $f(1) = -3$. $x_1 = 0.25$, $f = -0.234375$; $x_2 = 0.202532$, $f = -0.004351$; $x_3 = 0.201654$, $f = -0.000072$. Root ≈ 0.20164 (true 0.2016397).'),
                         ('Find a root of $x e^{x} = 1$ between 0 and 1 by Regula Falsi, 3 iterations.', '$f(x) = xe^x - 1$: $f(0) = -1$, $f(1) = 1.718282$. $x_1 = 0.367879$ ($f = -0.468536$), $x_2 = 0.503314$ ($f = -0.167420$), $x_3 = 0.547412$ ($f = -0.053649$). Root 0.5671433.'),
                         ('Why does the bracket in false position usually not shrink to zero?', 'If $f$ is convex (or concave) on the bracket, every chord lies on the same side of the curve, so every new point falls on the same side of the root. One endpoint is replaced every time; the other never moves.'),
                         ('Compare false position and bisection (three points).', 'Both bracket the root and always converge. Bisection uses only signs, has the guaranteed bound $(b-a)/2^n$, and is slow but steady. False position uses function values, is usually faster, but has no simple bound and can stall when one endpoint gets stuck.')])])]),
)
