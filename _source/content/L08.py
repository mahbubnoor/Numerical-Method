LECTURE = dict(
    title='Fixed-Point Iteration',
    short='Fixed-Point Iteration',
    sub='Rewrite f(x) = 0 as x = g(x), then just repeat x ← g(x). It works beautifully, or explodes, depending on one number: the slope of g at the root.',
    slides=[
        dict(type='cover', id='cover', notes="Calculator demo to open: set radians, type 1, then press cos repeatedly. The display settles at 0.7390851332. Every student can do this on their phone.\n\nAsk: why does it settle? And would it settle if we pressed 'tan' repeatedly? (No.) Today we find the rule that decides."),
        dict(type='bullets', id='hook', title='The problem: why does the cos button settle?', kick='Why this lecture', rw=760,
             lead='Set your calculator to radians, type 1, and press <b>cos</b> again and again.',
             items=['1 → 0.5403 → 0.8576 → 0.6543 → 0.7935 → 0.7014 → … → <b>0.739085</b>, then it stops changing', 'That number solves $x = \\cos x$, an equation with no formula', 'Now try the <b>tan</b> button from 1: 1.557, 74.69, −0.84, … it never settles', 'Why does one repeated function find an answer and the other does not? Today\'s theorem answers it'],
             frag=True,
             right=dict(table=[['press', '$x$'], [['0', '1.000000'], ['1', '0.540302'], ['2', '0.857553'], ['3', '0.654290'], ['…', '…'], ['36', '0.739085']]]),
             notes="Let every student do this on their phone (radian mode). Then ask for a guess why tan behaves differently. The answer, revealed at the end: |d/dx cos x| = |sin x| ≈ 0.67 < 1 near the answer, while the slope of tan is always ≥ 1."),
        dict(type='goals', id='goals', items=[
            'Rewrite $f(x) = 0$ in the form $x = g(x)$, in several ways',
            'Carry out the <b>method of iteration</b> by hand',
            'State and use the <b>convergence condition</b> $|g\'(x)| < 1$ near the root',
            'Read <b>cobweb diagrams</b>: staircase vs spiral, convergence vs divergence',
            'Explain <b>linear convergence</b> and estimate the number of iterations',
            'Know its <b>best and worst cases</b>, and which methods remove its limitations'],
            prev='Bracketing methods (bisection, false position) trap the root and never lose it.',
            today='The first <b>open</b> method: one starting point, no bracket, very simple; it may converge or diverge.',
            notes=""),
        dict(type='math', id='idea', title='The idea: a fixed point of $g$',
             eqs=[dict(cap='Rewrite', eq='f(x) = 0 \\;\\Longleftrightarrow\\; x = g(x)'), dict(cap='Iterate', eq='x_{n+1} = g(x_n), \\qquad n = 0, 1, 2, \\dots', frag=True)],
             items=['A <b>fixed point</b> $r$ satisfies $r = g(r)$: $g$ leaves it unchanged', 'Geometrically: where $y = g(x)$ meets the line $y = x$', 'If the iterates converge to some $r$ and $g$ is continuous, then $r = g(r)$, so $f(r) = 0$', 'Example: $x = \\cos x$ is already in this form; $g(x) = \\cos x$'],
             ifrag=True,
             notes="The proof in the third bullet is one line: take limits on both sides of x_{n+1} = g(x_n).\n\nBut convergence is not automatic: that is the whole lecture."),
        dict(type='table', id='rewrite', title='One equation, many rearrangements: $x^2 - 4x - 10 = 0$',
             head=['Rearrangement $x = g(x)$', 'how', "$g'(x)$", "$|g'(r)|$ at $r = 5.7417$", 'verdict'], tx=(0, 1, 4), frag=True,
             rows=[['$x = \\sqrt{4x + 10}$', 'move $x^2$, take root', '$\\dfrac{2}{\\sqrt{4x+10}}$', '0.348', '<span class="gr">converges</span>'],
                   ['$x = \\dfrac{x^2 - 10}{4}$', 'solve for the $4x$ term', '$\\dfrac{x}{2}$', '2.871', '<span class="rd">diverges</span>'],
                   ['$x = \\dfrac{10}{x - 4}$', 'factor $x(x-4) = 10$', '$\\dfrac{-10}{(x-4)^2}$', '3.297', '<span class="rd">diverges</span> (goes to the other root)'],
                   ['$x = 4 + \\dfrac{10}{x}$', 'divide by $x$', '$\\dfrac{-10}{x^2}$', '0.303', '<span class="gr">converges</span> (spirals)']],
             note='Roots: $x = 2 \\pm \\sqrt{14}$, i.e. $5.741657$ and $-1.741657$. Every rearrangement has the same fixed points, but only some lead there.',
             notes="Reveal row by row; ask students to compute g' themselves before revealing.\n\nKey message: the equation does not decide convergence, the rearrangement does.\n\nRow 3 is interesting: 10/(x − 4) diverges from the positive root but converges to the negative root −1.7417, where |g'| = 0.303."),
        dict(type='math', id='theorem', title='When does it converge?',
             eqs=[dict(cap='Error recursion (mean value theorem)', eq='x_{n+1} - r = g(x_n) - g(r) = g\'(\\xi_n)(x_n - r)'),
                  dict(cap='Convergence condition', eq='|g\'(x)| \\le L < 1 \\text{ near } r \\;\\Longrightarrow\\; |x_n - r| \\le L^{n}\\,|x_0 - r| \\to 0', frag=True)],
             items=['Each step multiplies the error by about $g\'(r)$: <b>linear convergence</b>, rate $|g\'(r)|$', '$|g\'(r)| > 1$: errors grow, the iteration moves away from $r$', 'Smaller $|g\'(r)|$ = faster; $g\'(r) = 0$ is very fast (that is Newton, next lecture)', 'Sign of $g\'$: positive → staircase (one-sided); negative → spiral (alternating sides)'],
             ifrag=True,
             notes="Sufficient condition (Banach contraction theorem, informally): if g maps an interval I into itself and |g'| ≤ L < 1 on I, then the iteration converges for any x0 in I and the fixed point is unique in I."),
        dict(type='bullets', id='algo', title='The fixed-point iteration algorithm', kick='The method, step by step', ordered=True, rw=780,
             items=['Rewrite $f(x) = 0$ as $x = g(x)$ (there are many ways)', "Pick a $g$ with $|g'(x)| < 1$ near the root; choose a starting value $x_0$", 'Compute $x_{n+1} = g(x_n)$', 'Repeat until $|x_{n+1} - x_n| < \\varepsilon$; the answer is the last $x$', 'If the values grow or jump about, stop and choose a different $g$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input g, x0, tol, N\nx ← x0\nrepeat up to N times:\n    x_new ← g(x)\n    if |x_new − x| &lt; tol:\n        return x_new\n    x ← x_new\nstop: no convergence (try another g)</pre></div><p class="small" style="margin-top:14px">The loop is the shortest in the course. All the skill is in step 2: choosing a $g$ that contracts.</p>'),
             notes="Steps 1 and 2 are where students lose the problem: they iterate the first rearrangement they find. Insist that they compute g'(x0) and write |g'(x0)| < 1 before the table.\n\nStep 5 is the practical safety net: a cap on iterations N and a different g."),
        dict(type='widget', id='cob', title='Explore: cobweb diagrams', w='cobweb', o=dict(g='sqrt(4x + 10)', x0=5, height='440px', side=True, tableHeight='440px'), lw=420,
             items=['From $x_n$ go <b>up</b> to the curve $y = g(x)$, then <b>across</b> to $y = x$: that is $x_{n+1}$', 'Try the four rearrangements of $x^2 - 4x - 10 = 0$ (chips)', '$|g\'| < 1$: the web closes in; $|g\'| > 1$: it opens out', 'Watch $4 + 10/x$ spiral, $\\sqrt{4x+10}$ climb a staircase'],
             notes="Use the chips in order. √(4x+10): staircase into 5.7417. (x² − 10)/4: the web jumps away immediately. 10/(x − 4): wanders off to the negative root. 4 + 10/x: a spiral, because g' < 0.\n\nThe status line under the plot reads |g'| at the current point and says converge/diverge: the theorem live."),
        dict(type='worked', id='mid', title='Problem 1: $x^2 - 4x - 10 = 0$ by the iteration method',
             src='Problem 1', q='"Find out the root of the following equation using the iteration method: $x^2 - 4x - 10 = 0$."',
             steps=['Locate: $f(5) = -5$, $f(6) = 2$: a root lies in $(5, 6)$. Take $x_0 = 5$',
                    'Choose $g(x) = \\sqrt{4x + 10}$; check $|g\'(x)| = \\dfrac{2}{\\sqrt{4x+10}} \\le \\dfrac{2}{\\sqrt{30}} = 0.365 < 1$ on $[5, 6]$ ✓',
                    'Iterate: $x_1 = \\sqrt{30} = 5.477226$, $x_2 = \\sqrt{31.908904} = 5.648797$, $x_3 = 5.709219$, …',
                    'Continue until $|x_{n+1} - x_n| < 0.00005$: $x_{10} = 5.741637$'],
             answer='$x \\approx 5.7416$ (true $2 + \\sqrt{14} = 5.7416574$). Ten iterations: convergence is linear with rate 0.348.',
             right=dict(table=[['$n$', '$x_n$', '$|x_n - x_{n-1}|$'], [[0, '5.000000', '—'], [1, '5.477226', '0.477'], [2, '5.648797', '0.172'], [3, '5.709219', '0.0604'], [4, '5.730347', '0.0211'], [5, '5.737716', '0.00737'], [6, '5.740284', '0.00257'], [7, '5.741179', '0.000895'], [8, '5.741491', '0.000312'], [9, '5.741599', '0.000109'], [10, '5.741637', '0.0000378']]], cls='tb sm'), rw=560,
             notes="Model answer layout: (1) locate the root, (2) choose g and verify |g'| < 1, (3) iteration table, (4) final answer with stopping criterion.\n\nLook at the difference column: each entry is about 0.35 times the previous one. That ratio is g'(r) = 0.348: the theory of the slide \"When does it converge?\" visible in the table."),
        dict(type='compare', id='classic', title='Same problem, two approaches: $x^2 - 4x - 10 = 0$', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (exact formula)', tag='Algebra', cls='blue', items=['Quadratic formula: $x = \\dfrac{4 \\pm \\sqrt{16 + 40}}{2} = 2 \\pm \\sqrt{14}$', 'Both roots at once: $5.741657$ and $-1.741657$', 'Exists for degree 2 (and, with effort, degrees 3 and 4)']),
             right=dict(h='Numerical (fixed point)', tag='Algorithm', cls='key', items=['$x = \\sqrt{4x+10}$ from $x_0 = 5$', '14 iterations for $10^{-6}$: $5.741657$', 'One root per run; the other root needs a different $g$ ($10/(x-4)$)']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>$x = \\cos x$ and Kepler’s equation $E = M + e\\sin E$</h3><p>No formula gives $x$ or $E$ in closed form. Fixed-point iteration: $x = 0.739085$ (36 iterations for 6 decimals); Kepler with $M = 1$, $e = 0.1$: $E = 1.088598$ in 5.</p></div><p class="small frag fade">When a closed form exists and is cheap, <b>use it</b>. Numerical methods are for the (much larger) set of problems without one.</p>'),
             notes="Honest message: when a formula exists (quadratics), use it; it is faster. Fixed-point iteration earns its place on equations like x = cos x and Kepler's equation, which no formula solves."),
        dict(type='bullets', id='rate', title='Linear convergence: how many iterations?', rw=760,
             items=['Errors shrink by the factor $L = |g\'(r)|$ each step: $e_n \\approx L^n e_0$', 'For $\\sqrt{4x+10}$: measured ratios $e_{n+1}/e_n$ = 0.351, 0.349, 0.349, 0.348, … → $g\'(r) = 0.3483$ ✓',
                    'Steps for tolerance $\\varepsilon$: $n \\approx \\dfrac{\\ln(\\varepsilon / e_0)}{\\ln L}$; here $\\dfrac{\\ln(0.00005/0.742)}{\\ln 0.348} \\approx 9.1$ → 10 ✓',
                    'Compare: $x = \\cos x$ has $L = \\sin(0.739) = 0.674$: 36 iterations for 6 decimals', '$L$ close to 1 means painfully slow; $L > 1$ means divergence'],
             frag=True,
             right=dict(card=dict(tag='Rule of thumb', h='Digits per iteration', t='Each iteration gains about $-\\log_{10} L$ correct decimal digits.<br>$L = 0.348$: 0.46 digits per step.<br>$L = 0.1$: one digit per step.<br>Bisection ($L = \\tfrac12$): 0.3 digits per step.', cls='key')),
             notes="This is why fixed-point iteration is usually only a teaching tool and a building block: it is linear, often slower than bisection. Its power is in the idea: Newton's method is a fixed-point iteration with g'(r) = 0."),
        dict(type='code', id='code', title='Fixed-point iteration in Python and C', code='fixed', lw=560,
             items=['A guard on $|x|$ stops runaway (divergent) iterations', 'Change <code>g</code> to the other three rearrangements', 'Print the ratio of successive differences: it approaches $g\'(r)$', 'Try $g(x) = \\cos x$ and $g(x) = e^{-x}$'],
             notes="Run with each rearrangement. (x² − 10)/4 from 5 gives 3.75, 1.016, −2.242, −1.243, −2.114, ...: it does not blow up but wanders around the negative root without converging (|g'| = 0.87 there, so it actually converges slowly to −1.7417; let it run 100 steps to see).\n\nThe 'ratio' column is a neat practical diagnostic: if it hovers below 1, convergence is linear and you can predict the remaining iterations."),
        dict(type='table', id='cubic', title='Choosing $g$ for $x^3 + x - 1 = 0$ (root 0.6823)',
             head=['$g(x)$', "$|g'(r)|$", 'result from $x_0 = 0.5$'], frag=True, tx=(2,),
             rows=[['$1 - x^3$', '1.397', '<span class="rd">diverges</span> (oscillates and grows)'], ['$\\dfrac{1}{1 + x^2}$', '0.635', '<span class="gr">converges</span>: 21 iterations to 4 dp'], ['$(1 - x)^{1/3}$', '0.716', '<span class="gr">converges</span>, slower'], ['Newton: $x - \\dfrac{x^3 + x - 1}{3x^2 + 1}$', '0', '<span class="gr">converges fast</span>: 4 iterations']],
             note='The last row is a sneak preview: choosing $g$ cleverly makes $g\'(r) = 0$. That choice is Newton\'s method (Lecture 9).', notefrag=True,
             notes="Fixed-point iteration with 1/(1+x²) needs 21 iterations for 4 decimals, bisection about 12 from [0.6, 0.8], Newton 4.\n\nAsk: how would you discover the Newton row yourself? (Look for g with g'(r) = 0.)"),
        dict(type='profile', id='profile', title='Fixed-point iteration: method profile',
             best=['$|g\'(r)|$ small: Kepler\'s equation $E = 1 + 0.1\\sin E$ converges in <b>5</b> steps', '$g\'(r) = 0$: much faster than linear (this is Newton\'s method, L9)', 'The problem is <b>already</b> in the form $x = g(x)$: no derivative, one line of code'],
             worst=['$|g\'(r)|$ close to 1: $x = \\cos x$ needs <b>36</b> steps; Kepler with $e = 0.9$ needs 11', '$|g\'(r)| > 1$: diverges, e.g. $x = (x^2 - 10)/4$ for the root 5.7417', 'The choice of $g$ is guesswork without the $|g\'| < 1$ test'],
             suited=['Equilibrium problems: PageRank, Bellman value iteration, EM, Kepler\'s equation', 'Large linear systems (Jacobi, Gauss–Seidel are fixed-point iterations, L14)', 'Quick prototypes where a contraction $g$ is obvious'],
             avoid=['No rearrangement with $|g\'| < 1$ is known', 'High accuracy is needed quickly (linear convergence)', 'You need a guarantee from any start (use bracketing)'],
             verdict='Rule of thumb: <b>check $|g\'|$ before iterating</b>; the smaller it is, the fewer steps you need (about $-1/\\log_{10}|g\'|$ steps per digit).',
             notes="Kepler counts measured with M = 1, from E0 = 1, stopping at 1e-6: e = 0.1 → 5 steps, e = 0.5 → 6, e = 0.9 → 11. Newton needs 3, 4 and 6 (shown in Lecture 9)."),
        dict(type='table', id='compare', title='Comparative analysis so far: $x^2 - 4x - 10 = 0$ (root 5.741657)', kick='Comparison',
             head=['Method', 'Start', 'Iterations for $10^{-6}$', 'Needs', 'Guaranteed?'], tx=(0, 3, 4), frag=True,
             rows=[['Bisection', '$[5, 6]$', '20', 'sign change', 'yes'], ['False position', '$[5, 6]$', '5', 'sign change', 'yes'], ['Fixed point, $g = \\sqrt{4x+10}$', '$x_0 = 5$', '14', 'a good $g$', 'only if $|g\'| < 1$'], ['Fixed point, $g = (x^2 - 10)/4$', '$x_0 = 5$', 'diverges from 5.74', 'a good $g$', 'no']],
             note='Fixed-point iteration is not faster here than false position, and it can fail. Its value is the idea: Lecture 9 builds the best possible $g$, with $g\'(r) = 0$.', notefrag=True,
             notes="Honest comparison: for a single 1-D equation, fixed-point iteration is rarely the fastest choice. Its importance is conceptual (contraction, linear convergence rate) and practical for large problems that are naturally in fixed-point form."),
        dict(type='bridge', id='bridge', lead='Fixed-point iteration introduced open methods and the convergence rate $|g\'(r)|$. Its weaknesses point to the next lectures:',
             keep=['No bracket: one starting value', 'Very simple: one line per step', 'Convergence test $|g\'(r)| < 1$ predicts the speed', 'The same idea scales to huge systems'],
             rows=[['The choice of $g$ is guesswork; may diverge', 'Build $g$ systematically from the tangent: $g = x - f/f\'$', 9],
                   ['Only linear convergence', 'Make $g\'(r) = 0$: quadratic convergence (Newton)', 9],
                   ['Converges only near the root', 'Start with a few bisection steps, then switch (hybrid)', 10],
                   ['Large linear systems', 'Jacobi and Gauss–Seidel: fixed-point iteration with matrices', 14]],
             notes="The last row is the forward link students will meet in Lecture 14: the matrix version of |g'(r)| < 1 is the spectral radius condition ρ(G) < 1."),
        dict(type='apps', id='apps', n=2, lead='Click a card: each one is literally $x \\leftarrow g(x)$ repeated until it stops changing.',
             items=[
                 dict(ic='🌐', h='PageRank', t='Ranking web pages',
                      detail=dict(where='the core of Google\'s original ranking. The rank vector is the fixed point of $\\mathbf{r} \\leftarrow d\\,M\\mathbf{r} + \\frac{1-d}{N}$, with damping $d = 0.85$ acting as the contraction factor.',
                                  steps=['Three pages: A links to B and C; B links to C; C links to A', 'Start with $\\mathbf{r} = (1/3, 1/3, 1/3)$ and apply the update repeatedly', 'Each page gives its rank, times 0.85, equally to the pages it links to; everyone gets 0.05'],
                                  table=[['Page', 'A', 'B', 'C'], [['rank after convergence', '0.3878', '0.2148', '0.3974']]],
                                  note='28 iterations to 10⁻⁶. C ranks highest: two pages link to it. Google ran the same iteration on billions of pages.')),
                 dict(ic='🛰️', h='Kepler\'s equation: satellite positions', t='Where is a GPS satellite right now?',
                      detail=dict(where='every GPS receiver computes satellite positions from broadcast orbit data. The key step solves Kepler\'s equation for the eccentric anomaly $E$, given the mean anomaly $M$ and eccentricity $e$.',
                                  eq='E = M + e\\sin E \\qquad (g(E) = M + e\\sin E,\\; |g\'(E)| \\le e < 1)',
                                  table=[['iteration', '1', '2', '3', '4', '5'], [['$E$ ($M = 1$, $e = 0.1$)', '1.084147', '1.088390', '1.088588', '1.088597', '1.088598']]],
                                  note='Since |g′| ≤ e, the iteration always converges for an orbit (e < 1); GPS orbits have e < 0.02, so a few iterations suffice. For very elliptical orbits (e = 0.9) it needs 11 steps; Newton needs 6 (Lecture 9).')),
                 dict(ic='🎮', h='Reinforcement learning: value iteration', t='How an agent learns the value of every state',
                      detail=dict(where='planning in Markov decision processes. The value function is the fixed point of the Bellman operator.',
                                  eq='V(s) \\leftarrow \\max_a \\Big[\\, R(s,a) + \\gamma \\sum_{s\'} P(s\'\\mid s,a)\\, V(s\') \\Big]',
                                  steps=['The Bellman operator is a contraction with factor $\\gamma$ (the discount): exactly our $|g\'| \\le L < 1$', 'So the error shrinks like $\\gamma^n$: with $\\gamma = 0.9$, each digit costs about 22 iterations', 'This is why RL becomes slow as $\\gamma \\to 1$'],
                                  note='Same theorem as today, applied to a vector of state values instead of a single number.')),
                 dict(ic='🧮', h='Jacobi iteration for big linear systems', t='Preview of Lecture 14',
                      detail=dict(where='solving $A\\mathbf{x} = \\mathbf{b}$ with millions of unknowns (heat flow, circuits, PageRank). Rewrite each equation for its own unknown and iterate.',
                                  eq='x_i \\leftarrow \\frac{1}{a_{ii}}\\Big(b_i - \\sum_{j \\ne i} a_{ij}x_j\\Big)',
                                  note='It converges when the matrix version of |g′| < 1 holds: the spectral radius of the iteration matrix is below 1 (for example when A is diagonally dominant).'))],
             notes="Spend most time on PageRank and Kepler. Kepler's equation is a classic: since |g'(E)| = |e cos E| ≤ e < 1, the simple iteration always converges for orbits."),
        dict(type='exam', id='practice', src='Problem 2',
             q='"State the condition of convergence of the iteration method $x_{n+1} = g(x_n)$ and explain why the choice of $g$ matters. Illustrate with $x^2 - 4x - 10 = 0$."',
             tips=['Condition: $|g\'(x)| < 1$ in an interval around the root containing all iterates (sufficient)', 'Reason in one line: $e_{n+1} = g\'(\\xi)e_n$ (mean value theorem)', 'Illustrate: $\\sqrt{4x+10}$ ($|g\'| = 0.35$, converges) vs $(x^2-10)/4$ ($|g\'| = 2.87$, diverges)', 'Mention: convergence is linear; the smaller $|g\'(r)|$, the faster'],
             notes=""),
        dict(type='check', id='check', q='For $x = g(x)$ with $g(x) = \\dfrac{x^2 + 2}{3}$, does iteration converge to the root $r = 1$?',
             opts=['Yes, $|g\'(1)| = 2/3 < 1$', 'No, $|g\'(1)| = 2/3$', 'Yes, $g(1) = 1$', 'No, $|g\'(1)| > 1$'], right=0,
             answer='A. $g\'(x) = 2x/3$, so $|g\'(1)| = 2/3 < 1$: converges (staircase, since $g\' > 0$). The other root $r = 2$ has $g\'(2) = 4/3 > 1$: iteration moves away from it.',
             notes="C is a trap: g(1) = 1 only says that 1 is a fixed point, not that iteration reaches it."),
        dict(type='summary', id='summary', items=[
            'Rewrite $f(x) = 0$ as $x = g(x)$ and iterate $x_{n+1} = g(x_n)$',
            'Converges if $|g\'(x)| < 1$ near the root; diverges if $|g\'(r)| > 1$',
            'Linear convergence: error × $|g\'(r)|$ per step; steps ≈ $\\ln(\\varepsilon/e_0)/\\ln L$',
            'The rearrangement decides everything; always check $|g\'|$ before iterating',
            'Choosing $g$ with $g\'(r) = 0$ gives fast convergence: Newton\'s method'],
            hw=['Solve $x = e^{-x}$ by iteration from $x_0 = 0.5$ to 4 decimal places. How many iterations?', 'Find two rearrangements of $x^3 - 2x - 5 = 0$: one that converges near $x = 2.09$ and one that does not. Justify with $g\'$.', 'Write a C program that reads $x_0$ and prints the iterates of $g(x) = \\cos x$ until 6 decimals agree.', 'Lab: in the cobweb tab, find a $g$ whose iterates oscillate between two values forever.'],
            solved='cos settles because near 0.739 its slope is $|-\\sin x| = 0.674 < 1$ (a contraction); tan never settles because its slope $\\sec^2 x \\ge 1$ everywhere.',
            next='<b>Newton–Raphson.</b> Use the tangent line: the fastest of the classical methods, with digits doubling each step, and some spectacular failures.',
            notes="Homework answers: Q1: 15 iterations, x = 0.5672 (root 0.5671433; rate 0.567). Q2: x = (2x + 5)^(1/3) has g' = (2/3)(2x+5)^(−2/3) ≈ 0.15 (converges); x = (x³ − 5)/2 has g' = 3x²/2 ≈ 6.6 (diverges). Q4: e.g. g(x) = 3.3x(1 − x) (logistic map) settles into a 2-cycle."),
    ],
    code={
        'fixed': dict(file='fixed_point', py='''# Fixed-point iteration x_(n+1) = g(x_n) for x^2 - 4x - 10 = 0
import math

def g(x):
    return math.sqrt(4*x + 10)       # try (x*x - 10)/4,  10/(x - 4),  4 + 10/x

x = 5.0
tol = 0.5e-4                          # 4 decimal places
prev_diff = None
for n in range(1, 101):
    x_new = g(x)
    diff = abs(x_new - x)
    ratio = diff / prev_diff if prev_diff else float("nan")
    print(f"{n:3d}  x = {x_new:.6f}   |change| = {diff:.2e}   ratio = {ratio:.3f}")
    if diff < tol or abs(x_new) > 1e6:
        break
    x, prev_diff = x_new, diff
print("root ~", round(x_new, 4))
''', c='''/* Fixed-point iteration x_(n+1) = g(x_n) for x^2 - 4x - 10 = 0 */
#include <stdio.h>
#include <math.h>

double g(double x) { return sqrt(4 * x + 10); }   /* try (x*x - 10)/4,  4 + 10/x */

int main(void) {
    double x = 5.0, x_new = x, tol = 0.5e-4, diff, prev = 0;
    for (int n = 1; n <= 100; n++) {
        x_new = g(x);
        diff = fabs(x_new - x);
        printf("%3d  x = %.6f   |change| = %.2e   ratio = %.3f\\n", n, x_new, diff, n > 1 ? diff / prev : NAN);
        if (diff < tol || fabs(x_new) > 1e6) break;
        x = x_new; prev = diff;
    }
    printf("root ~ %.4f\\n", x_new);
    return 0;
}
'''),
        'gcheck': dict(file='check_g_prime', py='''import math

r = 2 + math.sqrt(14)                  # root of x^2 - 4x - 10
forms = {
    "sqrt(4x+10)": lambda x: math.sqrt(4*x + 10),
    "(x^2-10)/4":  lambda x: (x*x - 10) / 4,
    "10/(x-4)":    lambda x: 10 / (x - 4),
    "4 + 10/x":    lambda x: 4 + 10 / x,
}
h = 1e-6
for name, g in forms.items():
    slope = (g(r + h) - g(r - h)) / (2 * h)      # central difference, Lecture 3
    verdict = "converges" if abs(slope) < 1 else "diverges"
    print(f"{name:12s} g'(r) = {slope: .4f}  -> {verdict}")
'''),
    },
    lab=dict(title='Fixed-Point Lab',
             intro='Draw cobwebs, test rearrangements, and see linear convergence in numbers.',
             tabs=[
                 dict(name='Cobweb explorer', blocks=[
                     dict(p='Type g(x) or pick a rearrangement. Step the iteration and watch the cobweb. The note below the plot checks |g′| at the current point.'),
                     dict(w='cobweb', o=dict(g='sqrt(4x + 10)', x0=5, height='330px', side=True, tableHeight='330px',
                                              presets=[['√(4x+10)', 'sqrt(4x+10)', 5], ['(x²−10)/4', '(x^2-10)/4', 5], ['10/(x−4)', '10/(x-4)', 5], ['4 + 10/x', '4 + 10/x', 5], ['cos x', 'cos(x)', 1], ['e⁻ˣ', 'e^(-x)', 0.5], ['1/(1+x²)', '1/(1+x^2)', 0.5], ['3.3x(1−x)', '3.3x(1-x)', 0.2]]))]),
                 dict(name='Code', blocks=[
                     dict(h='Fixed-point iteration'), dict(code='fixed', tasks=['Run it. How many iterations to 4 decimal places?', 'Switch to 4 + 10/x. Compare the ratio column with g′(r) = −0.303 (absolute value).', 'Switch to (x*x − 10)/4 and run 100 steps. Where does it end up?']),
                     dict(h="Check g′ before iterating"), dict(code='gcheck', tasks=['Run it. Which forms converge to 5.7417?', 'Change r to the negative root 2 − √14. Which forms converge there?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Find a root of $x^2 - 4x - 10 = 0$ by the iteration method, correct to 4 decimal places.', 'Root in (5, 6). $g(x) = \\sqrt{4x+10}$, $|g\'| \\le 0.365$. From $x_0 = 5$: 5.477226, 5.648797, 5.709219, 5.730347, 5.737716, 5.740284, 5.741179, 5.741491, 5.741599, 5.741637. Root ≈ 5.7416.'),
                         ('State the condition for convergence of the iteration method and prove it briefly.', '$|g\'(x)| \\le L < 1$ near the root. Proof: $x_{n+1} - r = g(x_n) - g(r) = g\'(\\xi)(x_n - r)$, so $|x_{n+1} - r| \\le L|x_n - r| \\le L^{n+1}|x_0 - r| \\to 0$.'),
                         ('Solve $\\cos x = 3x - 1$ by iteration, 4 decimal places.', '$x = (1 + \\cos x)/3$, $|g\'| = |\\sin x|/3 \\le 1/3$. From $x_0 = 0.6$: 0.608445, 0.606846, 0.607150, 0.607092, 0.607103, 0.607101 → 0.6071.'),
                         ('Why does $x = (x^2 - 10)/4$ fail for the root 5.7417 of $x^2 - 4x - 10 = 0$?', '$g\'(x) = x/2$, so $|g\'(5.7417)| = 2.87 > 1$: each step multiplies the error by about 2.87, so the iterates move away.'),
                         ('Fixed-point iteration has errors 0.08, 0.024, 0.0072. Estimate $g\'(r)$ and the number of further steps to reach $10^{-6}$.', 'Ratio 0.3, so $|g\'(r)| \\approx 0.3$. Need $0.0072 \\times 0.3^k < 10^{-6}$: $k > \\ln(1.39\\times10^{-4})/\\ln 0.3 = 7.4$, so 8 more steps.')])])]),
)
