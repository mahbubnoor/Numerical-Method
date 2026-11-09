LECTURE = dict(
    title='Numerical Integration',
    short='Numerical Integration',
    sub='Areas, distances and probabilities from tables and from functions with no antiderivative: the trapezoidal rule, Simpson\'s 1/3 and 3/8 rules, their errors, Romberg integration and Gauss quadrature.',
    slides=[
        dict(type='cover', id='cover', notes="Opening question: 'A speedometer is read every 10 seconds. How far did the car travel?' Distance is the area under the speed curve, but we only have seven numbers.\n\nThis lecture integrates the interpolation formulas of Lectures 16–17, the reverse of last lecture, and it is far better behaved."),
        dict(type='bullets', id='hook', title='The problem: distance from speedometer readings', kick='Why this lecture', rw=620,
             lead='A car accelerates from rest. Its speed is read every 10 seconds for one minute. How far did it travel?',
             items=['Distance $= \\int_0^{60} v(t)\\,dt$, the <b>area under the speed curve</b>', 'There is no formula for $v(t)$: only the readings', 'The same need appears for $\\int_0^1 e^{-x^2}dx$ (normal probabilities): a formula exists but <b>no antiderivative</b>',
                    'We need rules that turn a few function values into an accurate area, with an error estimate'],
             frag=True,
             right=dict(table=[['$t$ (s)', '$v$ (m/s)'], [['0', '0'], ['10', '12'], ['20', '22'], ['30', '30'], ['40', '36'], ['50', '40'], ['60', '42']]]),
             notes="Solved at the end: trapezoidal 1610 m, Simpson 1620 m. The two agree to within 1%: a quick reliability check that students should always do."),
        dict(type='goals', id='goals', items=[
            'Derive the <b>trapezoidal</b>, <b>Simpson 1/3</b> and <b>3/8</b> rules from Newton\'s forward formula',
            'Apply the composite rules to tables and functions, and present the working clearly',
            'State and use their <b>error terms</b>: $O(h^2)$ and $O(h^4)$',
            'Improve accuracy with <b>Romberg</b> integration; understand <b>Gauss quadrature</b>',
            'Choose a rule for a given problem, and recognise when rules fail'],
            prev='Differentiation from tables: sensitive to noise and round-off.',
            today='Integration from tables: stable, accurate, and the basis of the ODE methods that follow.',
            notes="Contrast with Lecture 19 early: integration averages errors instead of amplifying them."),
        dict(type='math', id='idea', title='The idea: integrate the interpolating polynomial',
             eqs=[dict(cap='Integrate Newton\'s forward formula over n steps (x = x₀ + ph, dx = h dp)', eq='\\int_{x_0}^{x_0+nh} y\\,dx = h\\int_0^n \\Big(y_0 + p\\,\\Delta y_0 + \\frac{p(p-1)}{2}\\Delta^2 y_0 + \\cdots\\Big)dp'),
                  dict(cap='General quadrature formula (Newton–Cotes)', eq='= nh\\Big[y_0 + \\frac n2\\Delta y_0 + \\frac{n(2n-3)}{12}\\Delta^2y_0 + \\frac{n(n-2)^2}{24}\\Delta^3 y_0 + \\cdots\\Big]', frag=True)],
             items=['$n = 1$ (straight line): $\\frac h2(y_0 + y_1)$, the <b>trapezoidal rule</b>', '$n = 2$ (parabola): $\\frac h3(y_0 + 4y_1 + y_2)$, <b>Simpson\'s 1/3 rule</b>', '$n = 3$ (cubic): $\\frac{3h}{8}(y_0 + 3y_1 + 3y_2 + y_3)$, <b>Simpson\'s 3/8 rule</b>',
                    'Then repeat the small rule along the table: the <b>composite</b> rules'],
             ifrag=True, rw=580,
             notes="Check n = 2 on the board: 2h[y0 + Δy0 + (1/6)Δ²y0] = 2h[y0 + (y1 − y0) + (y2 − 2y1 + y0)/6] = (h/3)(y0 + 4y1 + y2). The Δ³ term has coefficient n(n − 2)²/24 = 0 for n = 2, which is why Simpson is exact for cubics."),
        dict(type='math', id='rules', title='The composite rules and their errors',
             eqs=[dict(cap='Trapezoidal (any n): ends once, inside points twice, times h/2', eq='T = \\frac h2\\big[y_0 + 2(y_1 + \\cdots + y_{n-1}) + y_n\\big], \\qquad E_T = -\\frac{(b-a)h^2}{12}f\'\'(\\xi)'),
                  dict(cap='Simpson 1/3 (n even): weights 1, 4, 2, 4, …, 2, 4, 1 times h/3', eq='\\begin{aligned} S &= \\frac h3\\big[y_0 + 4(y_1 + y_3 + \\cdots) + 2(y_2 + y_4 + \\cdots) + y_n\\big] \\\\ E_S &= -\\frac{(b-a)h^4}{180}f^{(4)}(\\xi) \\end{aligned}', frag=True),
                  dict(cap='Simpson 3/8 (n a multiple of 3): weights 1, 3, 3, 2, 3, 3, 2, …, 1 times 3h/8', eq='S_{3/8} = \\frac{3h}{8}\\big[y_0 + 3(y_1 + y_2 + y_4 + y_5 + \\cdots) + 2(y_3 + y_6 + \\cdots) + y_n\\big]', frag=True)],
             items=['Trapezoidal: halve $h$, error $\\div 4$; exact for straight lines', 'Simpson: halve $h$, error $\\div 16$; exact for <b>cubics</b>', 'Same number of function values, much better accuracy: Simpson is the default for smooth data'],
             ifrag=True, rw=560,
             notes="The 3/8 rule has error −(b − a)h⁴/80 f⁽⁴⁾, slightly larger than Simpson 1/3; it is used when n is odd (combine one 3/8 block with 1/3 blocks).\n\nWeddle's rule (n multiple of 6, weights 1, 5, 1, 6, 1, 5, 1 times 3h/10) appears in some syllabi; it gives 1.3735 in Problem 1."),
        dict(type='bullets', id='algo', title='Trapezoidal and Simpson\'s rules, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Choose $n$ (even for Simpson 1/3) and $h = (b - a)/n$', 'Tabulate $x_i = a + ih$ and $y_i = f(x_i)$ for $i = 0, \\dots, n$', 'Trapezoidal: sum = ends + 2 × inside; multiply by $h/2$', 'Simpson: sum = ends + 4 × odd + 2 × even (inside); multiply by $h/3$',
                    'Check: repeat with $n$ doubled; the change estimates the error'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input f, a, b, n   # n even\nh ← (b − a) / n\nT ← (f(a) + f(b)) / 2\nS ← f(a) + f(b)\nfor i = 1 … n−1:\n    y ← f(a + i·h)\n    T ← T + y\n    S ← S + (4 if i odd else 2)·y\nreturn h·T,  h·S / 3</pre></div><p class="small" style="margin-top:14px">One loop, $n + 1$ function values, both rules at once.</p>'),
             notes="Step 5 is the practical error estimate: Richardson again. For Simpson, error(n) ≈ (S_{2n} − S_n)/15; for the trapezoidal rule, (T_{2n} − T_n)/3."),
        dict(type='widget', id='explore', title='Explore: panels under the curve', w='quad', o=dict(f='e^(-x^2)', a=0, b=1, n=4, height='245px', methods=['trap', 'simp', 's38', 'mid'],
             presets=[['e^(−x²) on [0, 1]', 'e^(-x^2)', 0, 1, '', 4], ['1/(1+x²) on [0, 6]', '1/(1+x^2)', 0, 6, '', 6], ['sin x on [0, π]', 'sin(x)', 0, 3.14159265358979, '2', 6], ['x eˣ on [0, 1]', 'x*e^x', 0, 1, '1', 2]]), lw=440,
             items=['Shaded shapes: what each rule actually integrates (trapezoids or parabolas)', 'Slide $n$: watch the trapezoidal error fall by 4 per doubling, Simpson by 16', 'Simpson 3/8 needs $n$ divisible by 3', 'The table compares all rules with the same points'],
             notes="With e^(−x²) on [0, 1]: n = 4 gives trapezoidal error 3.8e-3, Simpson 3.1e-5. Doubling to n = 8: 9.6e-4 and 2.0e-6 (ratios 4 and 16).\n\nThe x e^x preset has exact value 1 (integration by parts): a good check."),
        dict(type='worked', id='p1', title='Problem 1: $\\int_0^6 \\frac{dx}{1+x^2}$ with $h = 1$',
             q='Evaluate $\\displaystyle\\int_0^6 \\frac{dx}{1+x^2}$ by the trapezoidal rule and both Simpson rules with $h = 1$. Compare with $\\tan^{-1}6 = 1.405648$.',
             steps=['Table: $y = 1,\\ 0.5,\\ 0.2,\\ 0.1,\\ 0.058824,\\ 0.038462,\\ 0.027027$',
                    'Trapezoidal: $\\tfrac12\\big[1 + 0.027027 + 2(0.5 + 0.2 + 0.1 + 0.058824 + 0.038462)\\big] = 1.410799$',
                    'Simpson 1/3: $\\tfrac13\\big[1.027027 + 4(0.5 + 0.1 + 0.038462) + 2(0.2 + 0.058824)\\big] = 1.366173$',
                    'Simpson 3/8: $\\tfrac38\\big[1.027027 + 3(0.5 + 0.2 + 0.058824 + 0.038462) + 2(0.1)\\big] = 1.357081$'],
             answer='Errors: trapezoidal 0.005, Simpson 1/3 0.039, Simpson 3/8 0.049. With $h = 1$ the curve bends sharply near 0, so the parabolas fit badly: Simpson is not automatically better when $h$ is too large.',
             right=dict(w='quad', o=dict(f='1/(1+x^2)', a=0, b=6, n=6, methods=['trap', 'simp', 's38'], height='220px', noexact=True, compact=True)), rw=760,
             notes="This classic textbook problem is a useful warning: the error terms contain f''(ξ) and f⁽⁴⁾(ξ), and f⁽⁴⁾ of 1/(1 + x²) is 24 at x = 0, so h⁴f⁽⁴⁾ is not small for h = 1. Slide n to 12 and 24 in the widget: n = 12 gives trapezoidal 1.7e-4, Simpson 1.9e-3; at n = 24 Simpson (3.7e-6) finally beats the trapezoidal rule (4.6e-5). The trapezoidal rule is unusually good here because 1/(1 + x²) decays smoothly at the far end.\n\nWeddle's rule gives 1.373447 here."),
        dict(type='table', id='p2', title='Problem 2: the error falls as predicted',
             q='Compute $\\int_0^1 e^{-x^2}dx = 0.746824133$ with $n = 2, 4, 8, 16$. How does the error change when $n$ doubles?',
             head=['$n$', 'Trapezoidal', 'error', 'ratio', 'Simpson', 'error', 'ratio'], frag=True,
             rows=[['2', '0.731370', '$1.55\\times10^{-2}$', '—', '0.74718043', '$3.56\\times10^{-4}$', '—'], ['4', '0.742984', '$3.84\\times10^{-3}$', '4.0', '0.74685538', '$3.12\\times10^{-5}$', '11.4'],
                   ['8', '0.745866', '$9.59\\times10^{-4}$', '4.0', '0.74682612', '$1.99\\times10^{-6}$', '15.7'], ['16', '0.746585', '$2.40\\times10^{-4}$', '4.0', '0.74682426', '$1.25\\times10^{-7}$', '15.9']],
             note='Ratios of 4 and 16 confirm the orders $h^2$ and $h^4$. With 17 function values Simpson already gives 7 correct digits.',
             notes="This is how to verify an implementation: compute the observed order p = log2(ratio). It also shows Richardson's idea: if the error is known to fall by 16, then (16S_{2n} − S_n)/15 removes it."),
        dict(type='math', id='romberg', title='Romberg integration: Richardson applied to the trapezoidal rule',
             eqs=[dict(cap='Halve h repeatedly, then remove the h², h⁴, … error terms', eq='\\begin{aligned} R_{k,0} &= T(h/2^k) \\\\ R_{k,j} &= R_{k,j-1} + \\frac{R_{k,j-1} - R_{k-1,j-1}}{4^j - 1} \\end{aligned}')],
             right=dict(table=[['$k$', '$R_{k,0}$ (trap)', '$R_{k,1}$', '$R_{k,2}$', '$R_{k,3}$'], [['0', '0.683940', '', '', ''], ['1', '0.731370', '0.747180', '', ''], ['2', '0.742984', '0.746855', '0.746834', ''], ['3', '0.745866', '0.746826', '0.746824', '0.7468240']]], frag=True), rw=820,
             below=dict(html='<ul class="b" style="margin-top:18px"><li class="frag fade">Column 1 is exactly Simpson\'s rule</li><li class="frag fade">$R_{3,3}$ has 7 correct digits from only 9 function values</li><li class="frag fade">The same trick as Lecture 19, now in the stable direction</li></ul>'),
             notes="For e^(−x²) on [0, 1]. R_{4,4} = 0.74682413 agrees with the exact value to 8 digits from 17 function values.\n\nRomberg needs a smooth integrand; with singularities (√x near 0) the error expansion breaks down and the extrapolation does not help."),
        dict(type='math', id='gauss', title='Gauss quadrature: choose the points as well as the weights',
             eqs=[dict(cap='Two-point Gauss–Legendre on [−1, 1]: exact for every cubic', eq='\\int_{-1}^{1} f(t)\\,dt \\approx f\\Big(-\\frac{1}{\\sqrt3}\\Big) + f\\Big(\\frac{1}{\\sqrt3}\\Big)'),
                  dict(cap='Map [a, b] to [−1, 1]', eq='\\int_a^b f(x)\\,dx = \\frac{b-a}{2}\\int_{-1}^{1} f\\Big(\\frac{a+b}{2} + \\frac{b-a}{2}t\\Big)dt', frag=True)],
             items=['Newton–Cotes fixes equally spaced points; Gauss also chooses <b>where</b> to sample', '$n$ points are exact for polynomials of degree $2n - 1$ (Simpson: 3 points, degree 3; Gauss: 2 points, degree 3)', '$\\int_0^1 e^{-x^2}dx$: 2-point Gauss 0.746595 (error $2.3\\times10^{-4}$); 3-point (weights $\\tfrac59, \\tfrac89, \\tfrac59$) error $9.5\\times10^{-6}$',
                    'Needs $f$ at irrational points: fine for formulas, impossible for tables'],
             ifrag=True,
             notes="Why 1/√3: require exactness for 1, t, t², t³ with two symmetric points ±c and equal weights w: 2w = 2 and 2wc² = 2/3 give w = 1, c = 1/√3.\n\nThe points are the roots of the Legendre polynomials; library routines (scipy.integrate.quad) use adaptive Gauss–Kronrod rules."),
        dict(type='compare', id='classic', title='Same area, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (antiderivative)', tag='Calculus', cls='blue', items=['$\\int_0^1 xe^x dx$: integrate by parts', '$= [xe^x - e^x]_0^1 = 1$', 'Exact, if an antiderivative can be found']),
             right=dict(h='Numerical (Simpson, $n = 4$)', tag='Algorithm', cls='key', items=['Five values of $xe^x$', '$S = 1.000169$ (error $1.7\\times10^{-4}$)', 'Same code for any integrand or table']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>$\\int_0^1 e^{-x^2}dx$ and the speedometer table</h3><p>$e^{-x^2}$ has no elementary antiderivative (Liouville\'s theorem): every normal-distribution table and every <code>erf</code> routine is computed numerically. The speed readings have no formula at all. Simpson: 0.7468554 with 5 values; distance 1620 m from 7 readings.</p></div>'),
             notes="Liouville (1835) proved that e^(−x²), sin(x)/x and e^x/x have no elementary antiderivatives. This is the integration counterpart of Abel–Ruffini for equations."),
        dict(type='code', id='code', title='Trapezoidal, Simpson and Romberg in Python and C', code='quadrature', lw=560,
             items=['One loop computes both composite rules', 'Romberg table built row by row', 'Applied to $e^{-x^2}$ on $[0, 1]$', 'Lab: integrate the speedometer table'],
             notes="Run both tabs and compare the Romberg table with the slide."),
        dict(type='widget', id='fail', title='Limitations shown failing', kick='When quadrature goes wrong', w='quad',
             o=dict(f='sin(20*x)^2', a=0, b=3.14159265358979, n=20, exact='1.5707963267949', methods=['trap', 'simp'], height='260px',
                    presets=[['aliasing: sin²(20x), n = 20', 'sin(20*x)^2', 0, 3.14159265358979, '1.5707963267949', 20, 'simp'], ['singular: √x', 'sqrt(x)', 0, 1, '0.666666666666667', 16, 'simp'], ['odd n for Simpson', 'e^(-x^2)', 0, 1, '', 5, 'simp']]), lw=540,
             items=['<b>Aliasing</b>: $\\sin^2(20x)$ on $[0, \\pi]$ with $n = 10$ or $20$ samples only its zeros: every rule says 0 (true $\\pi/2$)', '<b>Singular derivatives</b>: $\\sqrt{x}$ near 0; Simpson\'s error falls only like $h^{1.5}$, not $h^4$',
                    '<b>Simpson needs even $n$</b>; 3/8 needs a multiple of 3', '<b>Jumps</b> inside a panel break the polynomial assumption: split the integral at the jump'],
             frag=True,
             notes="Aliasing is the same phenomenon as in signal sampling: too few samples per oscillation. The fix is more points (at least several per period) or an oscillation-aware method.\n\nFor √x: n = 16 Simpson error 1.3e-3, n = 64 1.6e-4: a factor 8 per factor 4 in n (h^1.5), not 256."),
        dict(type='exam', id='practice', src='Problem 3',
             q='"Evaluate $\\displaystyle\\int_0^1 \\frac{dx}{1+x}$ using the trapezoidal rule, Simpson\'s 1/3 rule and Simpson\'s 3/8 rule with $h = 1/6$. Hence obtain an approximate value of $\\ln 2$."',
             tips=['Tabulate $y = 1/(1+x)$ at $x = 0, \\tfrac16, \\dots, 1$: 1, 0.857143, 0.75, 0.666667, 0.6, 0.545455, 0.5', 'Trapezoidal: 0.694877; Simpson 1/3: 0.693170; Simpson 3/8: 0.693195',
                   'Since $\\int_0^1 \\frac{dx}{1+x} = \\ln 2 = 0.693147$, state the errors: $1.7\\times10^{-3}$, $2.3\\times10^{-5}$, $4.8\\times10^{-5}$', 'Write each rule\'s formula before substituting; show the grouped sums (ends, odds, evens)'],
             notes=""),
        dict(type='profile', id='profile', title='Numerical integration: method profile',
             best=['Smooth integrands: Simpson gains a factor 16 per halving of $h$', 'Tabulated data at equal steps: trapezoidal or Simpson directly', 'Romberg or Gauss: many digits from few function values'],
             worst=['Singularities or infinite derivatives at an end point', 'Fast oscillations with too few samples (aliasing)', 'Jumps inside a panel'],
             suited=['Areas, distances, energies and probabilities from measurements', 'Statistics and ML: AUC, expectations, normalising constants', 'Inside ODE methods (Heun = trapezoid, Milne = Simpson: Lectures 21–22)'],
             avoid=['Simpson with odd $n$ (use 3/8 for one block)', 'Very high-order Newton–Cotes rules (negative weights, Runge-like trouble)', 'Integrals over many dimensions (use Monte Carlo)'],
             verdict='Rule of thumb: <b>tables → Simpson (trapezoidal for unequal or rough data); formulas → Gauss or an adaptive library routine; always compare two step sizes</b>.',
             notes="Monte Carlo integration (random sampling) has error ~ 1/√N in any dimension; quadrature rules become impractical beyond a few dimensions."),
        dict(type='table', id='compare', title='Comparative analysis: $\\int_0^1 e^{-x^2}dx$ with about 5 function values', cls='tb sm',
             head=['Rule', 'Function values', 'Exact for degree', 'Error order', 'Value', 'Error'], tx=(0,), frag=True,
             rows=[['Trapezoidal, $n = 4$', '5', '1', '$h^2$', '0.742984', '$3.8\\times10^{-3}$'], ['Simpson 1/3, $n = 4$', '5', '3', '$h^4$', '0.746855', '$3.1\\times10^{-5}$'],
                   ['Gauss 2-point, 2 panels', '4', '3 per panel', '$h^4$', '0.746803', '$2.1\\times10^{-5}$'], ['Gauss 3-point, 1 panel', '3', '5', '—', '0.746815', '$9.5\\times10^{-6}$'], ['Romberg $R_{2,2}$', '5', '5', '$h^6$', '0.746834', '$9.6\\times10^{-6}$']],
             note='Same small budget of function values, accuracy differing by a factor of about 400. Gauss needs $f$ at irrational points; the others work on tables.', notefrag=True,
             notes="Gauss 2-point with 2 panels: computed by the lab code (4 evaluations)."),
        dict(type='bridge', id='bridge', title='End of Module 5: from areas to differential equations', kick='Roadmap', lead='Integration rules are accurate and stable. Their next job is to step differential equations forward in time:',
             keep=['Trapezoidal $O(h^2)$, Simpson $O(h^4)$', 'Error estimate by halving $h$', 'Romberg and Gauss for high accuracy', 'Stable: errors in data are averaged, not amplified'],
             rows=[['$y\' = f(x, y)$: the integrand depends on the unknown', 'Euler (rectangle) and Heun (trapezoid)', 21],
                   ['Higher accuracy for ODEs', 'Runge–Kutta (Simpson-like weights); Milne uses Simpson', 22],
                   ['Integrals of noisy data with a model', 'Fit first, then integrate: least squares', 23],
                   ['Long simulations must not blow up', 'Stability of ODE methods; stiff solvers', 22]],
             notes="Point out the correspondence: Euler ↔ left rectangle, Heun ↔ trapezoid, RK4 ↔ Simpson weights 1, 2, 2, 1 (= 1, 4, 1 with the middle split)."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see the integration rule at work.',
             items=[
                 dict(ic='📈', h='ROC AUC in machine learning', t='The trapezoidal rule inside scikit-learn',
                      detail=dict(where='evaluating classifiers. The ROC curve plots true-positive rate against false-positive rate; the area under it (AUC) is the standard score. <code>sklearn.metrics.auc</code> computes it with the trapezoidal rule on unequally spaced points.',
                                  table=[['FPR', '0', '0.1', '0.2', '0.4', '1.0'], [['TPR', '0', '0.5', '0.7', '0.9', '1.0']]],
                                  steps=['Each segment: width × average height', '$0.1(0.25) + 0.1(0.6) + 0.2(0.8) + 0.6(0.95)$', 'AUC $= 0.025 + 0.06 + 0.16 + 0.57 = 0.815$'],
                                  note='Trapezoids work with any spacing, which is why they are used here rather than Simpson.')),
                 dict(ic='⚡', h='Energy from power readings', t='How many kWh did the house use?',
                      detail=dict(where='smart meters and battery management. Energy is the integral of power; a meter samples power and integrates.',
                                  table=[['hour', '0', '1', '2', '3', '4', '5', '6'], [['power (kW)', '2.0', '3.5', '5.0', '4.2', '3.0', '2.6', '1.8']]],
                                  note='Trapezoidal: 20.2 kWh; Simpson: 20.33 kWh. A battery\'s state of charge is computed the same way from current readings (coulomb counting).')),
                 dict(ic='💊', h='Drug exposure (pharmacokinetics)', t='Area under the concentration curve',
                      detail=dict(where='medicine and drug approval. The area under the blood-concentration curve (AUC, mg·h/L) measures total exposure to a drug; regulators require it to compare medicines.',
                                  table=[['time (h)', '0', '2', '4', '6', '8'], [['conc. (mg/L)', '0', '8.2', '6.1', '3.9', '2.4']]],
                                  steps=['Trapezoidal (the standard "linear trapezoidal method"): $2[\\tfrac12(0 + 2.4) + 8.2 + 6.1 + 3.9] = 38.8$', 'Simpson: $\\tfrac23[0 + 4(8.2 + 3.9) + 2(6.1) + 2.4] = 42.0$', 'The difference (8%) shows the sampling is too coarse near the peak'],
                                  note='Clinical studies sample more densely around the expected peak for exactly this reason.')),
                 dict(ic='📊', h='Normal probabilities', t='Where the z-table comes from',
                      detail=dict(where='statistics and ML (Gaussian models, p-values). $P(0 < Z < 1) = \\int_0^1 \\frac{1}{\\sqrt{2\\pi}}e^{-z^2/2}dz$ has no closed form; tables and <code>scipy.stats.norm.cdf</code> compute it numerically.',
                                  w='quad', o=dict(f='e^(-x^2/2)/sqrt(2*pi)', a=0, b=1, n=4, methods=['trap', 'simp', 'g2'], height='200px', exact='0.341344746068543'),
                                  note='Simpson with $n = 4$: 0.341355 (true 0.341345). With $n = 10$ the error is $3\\times10^{-7}$.'))],
             notes="Students can type the power readings into the 'Integrating a table' lab code."),
        dict(type='check', id='check', q='Simpson\'s 1/3 rule with $h = 1$ and $y = 1, 3, 9$. What is the value?',
             opts=['$\\tfrac{22}{3}$', '$8$', '$\\tfrac{16}{3}$', '$13$'], right=0,
             answer='A. $\\tfrac13[1 + 4(3) + 9] = \\tfrac{22}{3} \\approx 7.333$. (Trapezoidal gives $\\tfrac12[1 + 2(3) + 9] = 8$.)',
             notes="Option B is the trapezoidal value; option D adds the values without weights."),
        dict(type='summary', id='summary', items=[
            'Newton–Cotes: integrate the interpolating polynomial; $n = 1, 2, 3$ give trapezoidal, Simpson 1/3, 3/8',
            'Trapezoidal error $-\\frac{(b-a)h^2}{12}f\'\'$; Simpson $-\\frac{(b-a)h^4}{180}f^{(4)}$ (exact for cubics)',
            'Romberg: Richardson on the trapezoidal rule; Gauss: optimal points, $n$ points exact to degree $2n - 1$',
            'Check by halving $h$; beware singularities, aliasing, jumps and odd $n$'],
            hw=['Evaluate $\\int_0^{\\pi} \\sin x\\,dx$ with $n = 6$ by the trapezoidal and Simpson rules; compare with 2.', 'Derive Simpson\'s 1/3 rule from the general quadrature formula with $n = 2$.',
                'Integrate the speedometer table with Simpson\'s 3/8 rule (two blocks). Compare with 1610 m and 1620 m.', 'Build the Romberg table for $\\int_0^1 \\frac{4}{1+x^2}dx$ up to $R_{2,2}$. Which famous number appears?'],
            solved='Trapezoidal: <b>1610 m</b>; Simpson: <b>1620 m</b>. They differ by 0.6%, so the distance is about 1.6 km to within about 10 m.',
            next='<b>ODEs I: Taylor, Picard and Euler.</b> When the rate of change depends on the unknown itself: stepping $y\' = f(x, y)$ forward.',
            notes="Homework answers: Q1: trapezoidal 1.954097, Simpson 2.000863. Q3: 3/8 rule on two blocks: (30/8)[0 + 3(12 + 22) + 30] + (30/8)[30 + 3(36 + 40) + 42] = 495 + 1125 = 1620 m. Q4: T: 3, 3.1, 3.131176; R11 = 3.133333, R21 = 3.141569; R22 = 3.142118 → π (3.141593)."),
    ],
    code={
        'quadrature': dict(file='quadrature', py='''# Trapezoidal, Simpson and Romberg integration of f on [a, b]
import math

def f(x):
    return math.exp(-x * x)

a, b = 0.0, 1.0
exact = 0.7468241328124270

def trap_simp(n):                      # n must be even for Simpson
    h = (b - a) / n
    T = (f(a) + f(b)) / 2
    S = f(a) + f(b)
    for i in range(1, n):
        y = f(a + i * h)
        T += y
        S += (4 if i % 2 else 2) * y
    return h * T, h * S / 3

for n in [2, 4, 8, 16]:
    T, S = trap_simp(n)
    print(f"n = {n:2d}: trapezoidal {T:.8f} (error {abs(T - exact):.1e})   Simpson {S:.10f} (error {abs(S - exact):.1e})")

R = []                                 # Romberg table
for k in range(5):
    if k == 0:
        row = [(b - a) * (f(a) + f(b)) / 2]
    else:
        row = [trap_simp(2 ** k)[0]]
    for j in range(1, k + 1):
        row.append(row[j - 1] + (row[j - 1] - R[k - 1][j - 1]) / (4 ** j - 1))
    R.append(row)
    print(" ".join(f"{v:.8f}" for v in row))
''', c='''/* Trapezoidal, Simpson and Romberg integration of f on [a, b] */
#include <stdio.h>
#include <math.h>

double f(double x) { return exp(-x * x); }

double a = 0.0, b = 1.0, exact = 0.7468241328124270;

double trap(int n) {
    double h = (b - a) / n, t = (f(a) + f(b)) / 2;
    for (int i = 1; i < n; i++) t += f(a + i * h);
    return h * t;
}

double simp(int n) {                              /* n must be even */
    double h = (b - a) / n, s = f(a) + f(b);
    for (int i = 1; i < n; i++) s += (i % 2 ? 4 : 2) * f(a + i * h);
    return h * s / 3;
}

int main(void) {
    double R[5][5];
    for (int n = 2; n <= 16; n *= 2) {
        double T = trap(n), S = simp(n);
        printf("n = %2d: trapezoidal %.8f (error %.1e)   Simpson %.10f (error %.1e)\\n", n, T, fabs(T - exact), S, fabs(S - exact));
    }
    for (int k = 0; k < 5; k++) {                 /* Romberg table */
        R[k][0] = trap(1 << k);
        for (int j = 1; j <= k; j++) R[k][j] = R[k][j - 1] + (R[k][j - 1] - R[k - 1][j - 1]) / (pow(4, j) - 1);
        for (int j = 0; j <= k; j++) printf(j ? " %.8f" : "%.8f", R[k][j]);
        printf("\\n");
    }
    return 0;
}
'''),
        'tablequad': dict(file='integrate_table', py='''# Integrate tabulated data: distance from speedometer readings
t = [0, 10, 20, 30, 40, 50, 60]          # seconds
v = [0, 12, 22, 30, 36, 40, 42]          # metres per second
h = t[1] - t[0]
n = len(v) - 1

trap = h / 2 * (v[0] + 2 * sum(v[1:-1]) + v[-1])
print(f"trapezoidal: {trap:.1f} m")

if n % 2 == 0:
    simp = h / 3 * (v[0] + 4 * sum(v[1:-1:2]) + 2 * sum(v[2:-1:2]) + v[-1])
    print(f"Simpson 1/3: {simp:.1f} m")

if n % 3 == 0:
    s38 = 0.0
    for i in range(1, n):
        s38 += (2 if i % 3 == 0 else 3) * v[i]
    s38 = 3 * h / 8 * (v[0] + s38 + v[-1])
    print(f"Simpson 3/8: {s38:.1f} m")
''', c='''/* Integrate tabulated data: distance from speedometer readings */
#include <stdio.h>
#define NP 7

int main(void) {
    double v[NP] = {0, 12, 22, 30, 36, 40, 42};   /* m/s at t = 0, 10, ..., 60 s */
    double h = 10, inner = 0, odd = 0, even = 0, s38 = 0;
    int n = NP - 1;
    for (int i = 1; i < n; i++) {
        inner += v[i];
        if (i % 2) odd += v[i]; else even += v[i];
        s38 += (i % 3 == 0 ? 2 : 3) * v[i];
    }
    printf("trapezoidal: %.1f m\\n", h / 2 * (v[0] + 2 * inner + v[n]));
    if (n % 2 == 0) printf("Simpson 1/3: %.1f m\\n", h / 3 * (v[0] + 4 * odd + 2 * even + v[n]));
    if (n % 3 == 0) printf("Simpson 3/8: %.1f m\\n", 3 * h / 8 * (v[0] + s38 + v[n]));
    return 0;
}
'''),
    },
    lab=dict(title='Numerical Integration Lab',
             intro='See what each rule integrates, measure how fast the error falls, and integrate your own data tables.',
             tabs=[
                 dict(name='Quadrature explorer', blocks=[
                     dict(p='Type f(x), a and b. Choose the rule and the number of panels; give the exact value if you know it (otherwise a reference value is computed).'),
                     dict(w='quad', o=dict(f='1/(1+x)', a=0, b=1, n=6, exact='0.693147180559945', methods=['trap', 'simp', 's38', 'mid', 'g2', 'g3'], height='300px',
                                           presets=[['Problem 3 (ln 2)', '1/(1+x)', 0, 1, '0.693147180559945', 6], ['Problem 1', '1/(1+x^2)', 0, 6, '1.40564764938027', 6], ['e^(−x²)', 'e^(-x^2)', 0, 1, '0.746824132812427', 4], ['homework 4 (π)', '4/(1+x^2)', 0, 1, '3.14159265358979', 4], ['√x (singular)', 'sqrt(x)', 0, 1, '0.666666666666667', 8]]))]),
                 dict(name='Code', blocks=[
                     dict(h='Trapezoidal, Simpson, Romberg'), dict(code='quadrature', tasks=['Run it. Check the error ratios 4 and 16.', 'Change f to sqrt(x) (exact 2/3). What happens to the ratios?', 'Change f to 4/(1+x*x) and look at the Romberg table.']),
                     dict(h='Integrating a table'), dict(code='tablequad', tasks=['Run it. Do the three rules agree?', 'Remove the last reading (n = 5). Which rules still run?', 'Enter your own data: power readings in kW every hour.'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Derive the trapezoidal rule from the general quadrature formula.', 'With $n = 1$: $\\int_{x_0}^{x_1} y\\,dx = h[y_0 + \\frac12\\Delta y_0] = \\frac h2(y_0 + y_1)$. Adding over all intervals gives $\\frac h2[y_0 + 2(y_1 + \\cdots + y_{n-1}) + y_n]$.'),
                         ('Why is Simpson\'s 1/3 rule exact for cubics, though it uses parabolas?', 'In the general formula with $n = 2$, the $\\Delta^3 y_0$ coefficient $n(n-2)^2/24$ is zero. Equivalently, its error term involves $f^{(4)}$, which is zero for cubics.'),
                         ('Evaluate $\\int_0^1 \\frac{dx}{1+x}$ by Simpson\'s rule with $h = 1/6$.', '$\\frac{1}{18}[1 + 4(0.857143 + 0.666667 + 0.545455) + 2(0.75 + 0.6) + 0.5] = 0.693170$ (true $\\ln 2 = 0.693147$).'),
                         ('What is Romberg integration?', 'Repeated Richardson extrapolation of trapezoidal values $T(h), T(h/2), T(h/4), \\dots$: $R_{k,j} = R_{k,j-1} + (R_{k,j-1} - R_{k-1,j-1})/(4^j - 1)$, removing the $h^2, h^4, \\dots$ error terms in turn.'),
                         ('State one advantage and one disadvantage of Gauss quadrature.', 'Advantage: $n$ points integrate polynomials of degree $2n - 1$ exactly, so very few function values are needed. Disadvantage: the points are irrational, so it cannot be used on equally spaced tabulated data.')])])]),
)
