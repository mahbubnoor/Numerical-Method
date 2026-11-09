LECTURE = dict(
    title='Finite Differences and Operators',
    short='Finite Differences and Operators',
    sub='Data in a table, no formula in sight: difference tables, the operators Δ, ∇, δ, E, μ and D, where each one comes from, how they are related, and why E = e^{hD} is the key to every interpolation, differentiation and integration formula that follows.',
    slides=[
        dict(type='cover', id='cover', notes="Opening question: 'A sensor records a value every second. Is there a formula behind the numbers? How would you tell from the numbers alone?' Today's answer: take differences.\n\nThis lecture is a foundation lecture for Module 4: it builds the language (operators) that generates the formulas of Lectures 16–20."),
        dict(type='bullets', id='hook', title='The problem: a table with no formula', kick='Why this lecture', rw=620,
             lead='A machine logs one reading per second. We have only the numbers.',
             items=['Is there a <b>polynomial</b> behind the data? Of which degree?', 'What was the value at $t = 2.5$ s, between two readings?', 'One entry looks odd. Is it a <b>recording error</b>? Which one?',
                    'All three questions are answered by one tool: <b>repeated subtraction</b> of neighbouring values'],
             frag=True,
             right=dict(table=[['$t$ (s)', '0', '1', '2', '3', '4', '5', '6'], [['$y$', '1', '0', '5', '22', '57', '116', '205']]]),
             notes="The data are y = t³ − 2t + 1, but do not say so. Students should discover the degree from the table (slide 6) and the leading coefficient from the constant third difference.\n\nSolved at the end: cubic with leading coefficient 1; y(2.5) = 11.625; changing 22 to 23 is detected by the pattern 1, −3, 3, −1 in the third differences."),
        dict(type='goals', id='goals', items=[
            'Build a <b>forward difference table</b> and read the forward and backward diagonals',
            'Use the fact that the $n$-th differences of a degree-$n$ polynomial are constant',
            'Define the operators $\\Delta, \\nabla, \\delta, E, \\mu, D$ and <b>derive the relations</b> between them',
            'Show why $E = e^{hD}$ connects differences with derivatives',
            'Find missing entries and locate errors in a table'],
            prev='Module 3: linear systems. Interpolation will need them (splines, Lecture 18).',
            today='A new kind of data: values at equally spaced points. A small algebra of operators makes them easy to handle.',
            notes="Students often memorise the operator relations as a list. Today's aim: every relation follows in one line from the definitions, mostly from E."),
        dict(type='math', id='table', title='The forward difference table',
             eqs=[dict(cap='Equally spaced points and their values', eq='x_i = x_0 + ih, \\qquad y_i = f(x_i)'),
                  dict(cap='Forward differences, applied again and again', eq='\\begin{aligned} \\Delta y_i &= y_{i+1} - y_i, \\qquad \\Delta^2 y_i = \\Delta y_{i+1} - \\Delta y_i \\\\ \\Delta^{k} y_i &= \\Delta^{k-1}y_{i+1} - \\Delta^{k-1}y_i \\end{aligned}', frag=True)],
             items=['Write each difference <b>between</b> the two numbers it came from', 'Each column is one entry shorter than the one before', 'The <b>top diagonal</b> $y_0, \\Delta y_0, \\Delta^2 y_0, \\dots$ feeds the forward formula (Lecture 16)',
                    'The <b>bottom diagonal</b> feeds the backward formula'],
             ifrag=True,
             notes="Draw the staggered layout on the board for 4 values. Many students lose marks by writing the differences in the wrong rows; the staggered layout makes the structure obvious."),
        dict(type='widget', id='explore', title='Explore: the difference table', w='difftab', o=dict(y='1 0 5 22 57 116 205', noerr=True, height='380px',
             presets=[['opening data', '1 0 5 22 57 116 205', 0, 1], ['squares', '0 1 4 9 16 25', 0, 1], ['y = 2ˣ', '1 2 4 8 16 32', 0, 1], ['census', '46 66 81 93 101', 1891, 10]]), lw=500,
             items=['Type any equally spaced data', 'Orange cells: the diagonal a formula would use', 'The tool reports when a column becomes constant', 'Try $2^x$: the differences never become constant'],
             notes="With the opening data: third differences 6, 6, 6, 6 and then zeros. With the squares: second differences all 2. With 2^x: every column is again 1, 2, 4, …: Δ2^x = 2^x (an operator 'eigenfunction', a nice aside)."),
        dict(type='table', id='p1', title='Problem 1: the difference table of the opening data',
             q='Build the forward difference table for $y = 1, 0, 5, 22, 57, 116, 205$ at $t = 0, 1, \\dots, 6$.',
             head=['$t$', '$y$', '$\\Delta y$', '$\\Delta^2 y$', '$\\Delta^3 y$', '$\\Delta^4 y$'], frag=True,
             rows=[[0, '1', '−1', '6', '6', '0'], [1, '0', '5', '12', '6', '0'], [2, '5', '17', '18', '6', '0'], [3, '22', '35', '24', '6', '—'], [4, '57', '59', '30', '—', '—'], [5, '116', '89', '—', '—', '—'], [6, '205', '—', '—', '—', '—']],
             note='Shown in "row" layout: row $i$ holds $\\Delta^k y_i$. Third differences are all 6 and fourth differences are 0: <b>the data come from a cubic</b>.',
             notes="Row layout (each Δ^k y_i in row i) is easier to typeset; the staggered layout is easier to read. Both are acceptable in a written answer if labelled.\n\nCheck one: Δ²y_1 = Δy_2 − Δy_1 = 17 − 5 = 12."),
        dict(type='math', id='poly', title='Differences of a polynomial',
             eqs=[dict(cap='For a polynomial of degree n with leading coefficient a', eq='\\Delta^{n}\\big(a x^n + \\cdots\\big) = a\\,n!\\,h^n \\;(\\text{a constant}), \\qquad \\Delta^{n+1} = 0'),
                  dict(cap='Why: each Δ lowers the degree by one', eq='\\Delta x^n = (x+h)^n - x^n = n h\\,x^{n-1} + \\cdots', frag=True)],
             items=['Opening data: $\\Delta^3 y = 6 = a \\cdot 3! \\cdot 1^3$, so $a = 1$: a cubic $t^3 + \\cdots$', 'This is how we "see" the degree in a table', 'Real data: differences become small and noisy rather than exactly zero',
                    'Example: with $h = 1$, $\\Delta x^3 = 3x^2 + 3x + 1$ and $\\Delta^2 x^3 = 6x + 6$'],
             ifrag=True,
             notes="The binomial expansion (x + h)^n − x^n leaves n h x^{n−1} as the leading term. Repeating n times gives n! h^n times the leading coefficient.\n\nΔ²x³: Δ(3x² + 3x + 1) = 3(2x + 1) + 3 = 6x + 6."),
        dict(type='math', id='ops', title='Six operators, all defined on $f(x)$',
             eqs=[dict(cap='Shift and the three differences', eq='\\begin{aligned} E f(x) &= f(x+h) & \\Delta f(x) &= f(x+h) - f(x) \\\\ \\nabla f(x) &= f(x) - f(x-h) & \\delta f(x) &= f(x+\\tfrac h2) - f(x-\\tfrac h2) \\end{aligned}'),
                  dict(cap='Average and derivative', eq='\\mu f(x) = \\tfrac12\\big[f(x+\\tfrac h2) + f(x-\\tfrac h2)\\big], \\qquad D f(x) = f\'(x)', frag=True)],
             items=['$E$: shift one step forward; $E^{-1}$ one step back; $E^{p}$: shift by $ph$', '$\\Delta$ forward, $\\nabla$ backward, $\\delta$ central difference', '$\\mu$: mean of the two half-step neighbours', 'All are <b>linear</b>: $\\Delta(af + bg) = a\\Delta f + b\\Delta g$, so they can be added, multiplied and inverted like numbers'],
             ifrag=True, rw=620,
             notes="Names used in older textbooks: E shift (or displacement) operator, Δ forward difference, ∇ backward difference, δ central difference, μ averaging (mean) operator, D differential operator.\n\nThe last bullet is the important one: operators that commute and are linear obey ordinary algebra, which is why the relations on the next slides can be derived like algebraic identities."),
        dict(type='worked', id='derive', title='Where the relations come from',
             q='Express every operator in terms of $E$, using only the definitions.',
             steps=['$\\Delta f(x) = f(x+h) - f(x) = Ef(x) - f(x)$, so $\\boxed{\\Delta = E - 1}$, i.e. $E = 1 + \\Delta$',
                    '$\\nabla f(x) = f(x) - f(x-h) = f(x) - E^{-1}f(x)$, so $\\boxed{\\nabla = 1 - E^{-1}}$',
                    '$\\delta f(x) = E^{1/2}f(x) - E^{-1/2}f(x)$, so $\\boxed{\\delta = E^{1/2} - E^{-1/2}}$; $\\;$ similarly $\\boxed{\\mu = \\tfrac12(E^{1/2} + E^{-1/2})}$',
                    'Taylor: $Ef(x) = f(x+h) = f + hf\' + \\tfrac{h^2}{2!}f\'\' + \\cdots = \\big(1 + hD + \\tfrac{(hD)^2}{2!} + \\cdots\\big)f$, so $\\boxed{E = e^{hD}}$'],
             answer='Everything is a function of $E$, and $E = e^{hD}$ links the differences with derivatives: $hD = \\ln E = \\ln(1 + \\Delta)$.',
             notes="Step 4 is the most important line of Module 4: the Taylor series (Lecture 3) written as an operator identity.\n\nConsequences to state (and use in Lectures 19–20): hD = ln(1 + Δ) = Δ − Δ²/2 + Δ³/3 − …, the forward-difference formula for the derivative; and hD = −ln(1 − ∇) = ∇ + ∇²/2 + ∇³/3 + …"),
        dict(type='table', id='rel', title='The relations at a glance', cls='tb',
             head=['', 'in terms of $E$', 'in terms of $\\Delta$', 'in terms of $hD$'], tx=(0,), frag=True,
             rows=[['$E$', '$E$', '$1 + \\Delta$', '$e^{hD}$'], ['$\\Delta$', '$E - 1$', '$\\Delta$', '$e^{hD} - 1$'], ['$\\nabla$', '$1 - E^{-1}$', '$1 - (1+\\Delta)^{-1}$', '$1 - e^{-hD}$'],
                   ['$\\delta$', '$E^{1/2} - E^{-1/2}$', '$\\Delta(1+\\Delta)^{-1/2}$', '$2\\sinh(hD/2)$'], ['$\\mu$', '$\\tfrac12(E^{1/2} + E^{-1/2})$', '$(1 + \\tfrac12\\Delta)(1+\\Delta)^{-1/2}$', '$\\cosh(hD/2)$']],
             note='Useful identities that follow: $\\Delta = E\\nabla = \\nabla E = \\delta E^{1/2}$; $\\;\\Delta - \\nabla = \\Delta\\nabla = \\delta^2$; $\\;\\mu^2 = 1 + \\tfrac14\\delta^2$; $\\;(1 + \\Delta)(1 - \\nabla) = 1$.', notefrag=True,
             notes="Ask students to derive one row each. The hD column uses E = e^{hD}: δ = e^{hD/2} − e^{−hD/2} = 2 sinh(hD/2), μ = cosh(hD/2)."),
        dict(type='worked', id='p2', title='Problem 2: proving operator identities',
             q='Prove (a) $\\Delta - \\nabla = \\Delta\\nabla = \\delta^2$, (b) $\\mu^2 = 1 + \\tfrac14\\delta^2$, (c) $(1 + \\Delta)(1 - \\nabla) = 1$.',
             steps=['(a) $\\Delta - \\nabla = (E - 1) - (1 - E^{-1}) = E - 2 + E^{-1}$', '$\\;\\;\\Delta\\nabla = (E - 1)(1 - E^{-1}) = E - 1 - 1 + E^{-1} = E - 2 + E^{-1}$, and $\\delta^2 = (E^{1/2} - E^{-1/2})^2 = E - 2 + E^{-1}$ ✓',
                    '(b) $\\mu^2 = \\tfrac14(E + 2 + E^{-1}) = \\tfrac14(E - 2 + E^{-1}) + 1 = \\tfrac14\\delta^2 + 1$ ✓', '(c) $(1 + \\Delta)(1 - \\nabla) = E \\cdot E^{-1} = 1$ ✓'],
             answer='Method: rewrite both sides in terms of $E$, then compare. It works for every identity of this kind.',
             notes="Students should always state the definitions used (Δ = E − 1, etc.) at the start of a proof. A common error is to treat ∇ as E^{−1} − 1 (sign)."),
        dict(type='worked', id='p3', title='Problem 3: a missing entry',
             q='The table $y = 1, 3, 9, \\;?, 81$ (at equal steps) comes from a cubic. Find the missing value.',
             steps=['A cubic has $\\Delta^4 y = 0$, i.e. $(E - 1)^4 y_0 = 0$', 'Expand: $(E^4 - 4E^3 + 6E^2 - 4E + 1)\\,y_0 = y_4 - 4y_3 + 6y_2 - 4y_1 + y_0 = 0$',
                    'Substitute: $81 - 4y_3 + 6(9) - 4(3) + 1 = 0$, so $4y_3 = 124$'],
             answer='$y_3 = 31$. (Check: the differences 2, 6, 22, 50; 4, 16, 28; 12, 12 are constant at third order.)',
             notes="With two missing values, use two equations: Δ⁴y_0 = 0 and Δ⁴y_1 = 0 (needs at least six entries).\n\nCheck table: 1, 3, 9, 31, 81 → Δ: 2, 6, 22, 50 → Δ²: 4, 16, 28 → Δ³: 12, 12. ✓"),
        dict(type='widget', id='error', title='Finding an error in a table', kick='Using differences to check data', w='difftab',
             o=dict(y='1 0 5 22 57 116 205', eps=1, k=3, height='380px', presets=[['22 → 23', '1 0 5 22 57 116 205', 0, 1, 1], ['no error', '1 0 5 22 57 116 205', 0, 1, 0]]), lw=520,
             items=['Add an error $\\varepsilon$ to one entry: it spreads through the table', 'In the $k$-th differences it appears as $\\varepsilon$ times binomial coefficients with alternating signs', 'Third differences become $6 + \\varepsilon(1, -3, 3, -1) = 7, 3, 9, 5$',
                    'The pattern points to the wrong entry; subtract $\\varepsilon$ to correct it'],
             frag=True,
             notes="This was how printed mathematical tables (logarithms, sines) were checked before computers. Today it is a quick sanity check for sensor and laboratory data.\n\nTo locate: the largest |Δ^k| deviation is in the middle of the pattern; the alternating signs give it away."),
        dict(type='compare', id='classic', title='Same question, two approaches: "what is $y$ at $t = 2.5$?"', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (find the formula)', tag='Algebra', cls='blue', items=['Guess a cubic $y = at^3 + bt^2 + ct + d$ and solve a 4×4 system (Lecture 12)', 'Get $y = t^3 - 2t + 1$', '$y(2.5) = 15.625 - 5 + 1 = 11.625$']),
             right=dict(h='Numerical (operators)', tag='Differences', cls='key', items=['$y(2.5) = E^{2.5}y_0 = (1 + \\Delta)^{2.5}y_0$', 'Expand with the top diagonal $1, -1, 6, 6$ (Lecture 16)', '$= 1 + 2.5(-1) + \\tfrac{2.5(1.5)}{2}(6) + \\tfrac{2.5(1.5)(0.5)}{6}(6) = 11.625$']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>Real measurements: no formula exists</h3><p>Census counts, temperatures or stock prices are not a polynomial; guessing "the formula" is impossible. The difference table works directly on the numbers, tells us how smooth the data are, and gives interpolation (Lecture 16), derivatives (Lecture 19) and integrals (Lecture 20).</p></div>'),
             notes="The right column previews Newton's forward formula: E^p = (1 + Δ)^p expanded by the binomial series. Next lecture derives it properly."),
        dict(type='code', id='code', title='The difference table in Python and C', code='difftable', lw=560,
             items=['Each column is computed from the previous one', 'Prints the table in row layout', 'Reports the first column that is constant', 'Change the data: try the census or $2^x$'],
             notes="Run both. Lab task: add an error to one entry and print the third differences."),
        dict(type='exam', id='practice', src='Problem 4',
             q='"Define the operators $E$, $\\Delta$, $\\nabla$ and $\\delta$. Show that $E = e^{hD}$ and hence that $hD = \\log(1 + \\Delta)$. Prove that $\\Delta - \\nabla = \\Delta\\nabla$."',
             tips=['Give each definition as a formula acting on $f(x)$ with step $h$', 'Expand $f(x + h)$ by Taylor\'s series and factor out $f$: $Ef = e^{hD}f$', 'Then $1 + \\Delta = E = e^{hD}$, so $hD = \\log(1 + \\Delta) = \\Delta - \\tfrac{\\Delta^2}{2} + \\tfrac{\\Delta^3}{3} - \\cdots$',
                   'For the identity, write both sides in terms of $E$: each equals $E - 2 + E^{-1}$'],
             notes=""),
        dict(type='bridge', id='bridge', title='What the operators will do for us', kick='Roadmap', lead='Every formula of Module 4 and 5 is an operator identity expanded as a series:',
             keep=['Difference tables reveal smoothness and degree', 'Operators obey ordinary algebra', '$E = e^{hD}$ links differences and derivatives', 'Errors in tables leave a recognisable pattern'],
             rows=[['Values between table points', '$E^p = (1+\\Delta)^p$: Newton forward; $(1-\\nabla)^{-p}$: backward', 16],
                   ['Unequally spaced data', 'Divided differences and Lagrange', 17],
                   ['Derivatives from a table', '$hD = \\ln(1 + \\Delta)$, central forms with $\\delta$', 19],
                   ['Areas under tabulated data', 'Integrate $E^p$ term by term: trapezoidal, Simpson', 20]],
             notes="Point at each row: the left column is a question students already have; the right column is the operator recipe that answers it."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see differences at work.',
             items=[
                 dict(ic='⚙️', h="Babbage's difference engine", t='Printing polynomial tables using only addition',
                      detail=dict(where='the first mechanical computer design (1820s). Because the $n$-th differences of a polynomial are constant, every new table value can be produced by additions alone, running the difference table backwards.',
                                  steps=['Start with the top diagonal of $y = t^3 - 2t + 1$: $1, -1, 6, 6$', 'Next third difference: 6 (constant). Next second: $6 + 6 = 12$', 'Next first difference: $-1 + 6 = 5$; next value: $1 + (-1) = 0$, then $0 + 5 = 5$, …',
                                         'No multiplication anywhere: just columns of adders, one per difference order'],
                                  note='Babbage\'s engine evaluated 7th-degree polynomials to 31 digits; a working model was finally built in 1991 (Science Museum, London).')),
                 dict(ic='📉', h='Time series: differencing to remove a trend', t='ARIMA models, forecasting, ML pipelines',
                      detail=dict(where='data science and forecasting. Before fitting a model, a trend is removed by differencing: $\\Delta y_t = y_t - y_{t-1}$ removes a linear trend; $\\Delta^2$ removes a quadratic one. The "I" in ARIMA is the number of differences taken.',
                                  table=[['month', '1', '2', '3', '4', '5'], [['sales', '120', '135', '152', '171', '192'], ['$\\Delta y$', '—', '15', '17', '19', '21'], ['$\\Delta^2 y$', '—', '—', '2', '2', '2']]],
                                  note='Constant second differences: a quadratic trend. The model is fitted to the leftover variation, then the forecast is "un-differenced" by adding back, like the difference engine.')),
                 dict(ic='🖼️', h='Edges in images', t='Differences of neighbouring pixels',
                      detail=dict(where='computer vision. An edge is where brightness changes quickly. The simplest edge detector is the difference of neighbouring pixels, $\\Delta I = I_{x+1} - I_x$; Sobel and Prewitt filters are smoothed central differences $\\delta$.',
                                  table=[['pixel $x$', '1', '2', '3', '4', '5', '6'], [['brightness $I$', '20', '22', '21', '180', '182', '181'], ['$\\Delta I$', '2', '−1', '159', '2', '−1', '—']]],
                                  note='The huge difference 159 between pixels 3 and 4 marks the edge. Second differences $\\delta^2 I$ (the discrete Laplacian of Lecture 14) mark edges by a sign change.')),
                 dict(ic='🎙️', h='Speech features: delta coefficients', t='How fast the spectrum changes',
                      detail=dict(where='speech recognition and speaker identification. Besides the MFCC features of each frame, systems add "delta" and "delta-delta" features: differences across neighbouring frames that capture how the sound is changing.',
                                  eq='\\Delta c_t = \\frac{\\sum_{k=1}^{K} k\\,(c_{t+k} - c_{t-k})}{2\\sum_{k=1}^{K} k^2}',
                                  note='With $K = 1$ this is exactly the central difference $\\tfrac12(c_{t+1} - c_{t-1}) = \\mu\\delta\\,c_t$. Delta-deltas are second differences.'))],
             notes="The speech card connects with the department's speech-processing research; the MFCC delta formula is a smoothed central difference."),
        dict(type='check', id='check', q='For $y = 2, 5, 10, 17$ (equal steps), what is $\\Delta^2 y_0$?',
             opts=['$2$', '$3$', '$5$', '$0$'], right=0,
             answer='A. $\\Delta y = 3, 5, 7$; $\\Delta^2 y = 2, 2$. Constant second differences: the data come from a quadratic ($y = x^2 + 1$ at $x = 1, 2, 3, 4$).',
             notes="Option B is Δy_0; option D would be Δ³."),
        dict(type='summary', id='summary', items=[
            '$\\Delta^k y$ of a degree-$n$ polynomial: constant for $k = n$, zero for $k > n$',
            '$\\Delta = E - 1$, $\\nabla = 1 - E^{-1}$, $\\delta = E^{1/2} - E^{-1/2}$, $\\mu = \\tfrac12(E^{1/2} + E^{-1/2})$',
            '$E = e^{hD}$ (Taylor), so $hD = \\ln(1+\\Delta) = -\\ln(1-\\nabla)$',
            'Prove identities by writing everything in terms of $E$; find missing values from $\\Delta^{n+1} = 0$'],
            hw=['Build the difference table for $y = 2, 9, 28, 65, 126$ ($x = 1, \\dots, 5$). What is the degree? Find $y(6)$ by extending the table.', 'Prove $\\nabla = 1 - E^{-1}$, $\\delta = \\Delta E^{-1/2}$ and $E\\nabla = \\Delta$.',
                'Find the missing term: $y = 2, 4, 8, \\;?, 32$ (assume a cubic).', 'Evaluate $\\Delta^2(x^3)$ with $h = 1$ and $\\Delta(e^{ax})$ with step $h$.'],
            solved='Third differences are constant (6), so the data are a cubic with leading coefficient 1 ($y = t^3 - 2t + 1$); $y(2.5) = 11.625$; an error of +1 in 22 shows up as $7, 3, 9, 5$ in the third differences.',
            next='<b>Newton\'s forward and backward interpolation.</b> Expand $E^p$ to find values between the table entries.',
            notes="Homework answers: Q1: y = x³ + 1; Δ: 7, 19, 37, 61; Δ²: 12, 18, 24; Δ³: 6, 6 → cubic; extend: Δ² 30, Δ 91, y(6) = 217. Q2: δ = E^{1/2} − E^{−1/2} = (E − 1)E^{−1/2} = ΔE^{−1/2}; E∇ = E(1 − E^{−1}) = E − 1 = Δ. Q3: y4 − 4y3 + 6y2 − 4y1 + y0 = 0 → 32 − 4y3 + 48 − 16 + 2 = 0 → y3 = 16.5. Q4: Δ²x³ = 6x + 6; Δe^{ax} = e^{ax}(e^{ah} − 1)."),
    ],
    code={
        'difftable': dict(file='difference_table', py='''# Forward difference table and the degree test
y = [1.0, 0.0, 5.0, 22.0, 57.0, 116.0, 205.0]   # values at t = 0, 1, 2, ...

table = [y]
while len(table[-1]) > 1:
    prev = table[-1]
    table.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])

n = len(y)
for i in range(n):                       # row i holds Delta^k y_i
    row = [f"{table[k][i]:8.2f}" for k in range(n - i)]
    print(f"i={i}: " + " ".join(row))

for k in range(1, len(table)):
    col = table[k]
    if len(col) >= 2 and all(abs(v - col[0]) < 1e-9 for v in col):
        print(f"order-{k} differences are constant ({col[0]:.2f}): degree {k} polynomial")
        break
''', c='''/* Forward difference table and the degree test */
#include <stdio.h>
#include <math.h>
#define N 7

int main(void) {
    double d[N][N];                         /* d[k][i] = Delta^k y_i */
    double y[N] = {1, 0, 5, 22, 57, 116, 205};
    for (int i = 0; i < N; i++) d[0][i] = y[i];
    for (int k = 1; k < N; k++)
        for (int i = 0; i < N - k; i++) d[k][i] = d[k - 1][i + 1] - d[k - 1][i];

    for (int i = 0; i < N; i++) {
        printf("i=%d:", i);
        for (int k = 0; k < N - i; k++) printf(" %8.2f", d[k][i]);
        printf("\\n");
    }
    for (int k = 1; k < N; k++) {
        int len = N - k, same = len >= 2;
        for (int i = 1; i < len; i++) if (fabs(d[k][i] - d[k][0]) >= 1e-9) same = 0;
        if (same) { printf("order-%d differences are constant (%.2f): degree %d polynomial\\n", k, d[k][0], k); break; }
    }
    return 0;
}
'''),
    },
    lab=dict(title='Difference Table Lab',
             intro='Build difference tables for your own data, read off the degree, and find errors and missing values.',
             tabs=[
                 dict(name='Difference table', blocks=[
                     dict(p='Type equally spaced data. Switch between the forward diagonal (Δ, used near the start) and the backward diagonal (∇, used near the end).'),
                     dict(w='difftab', o=dict(y='2 9 28 65 126', x0=1, noerr=True, presets=[['opening data', '1 0 5 22 57 116 205', 0, 1], ['homework 1', '2 9 28 65 126', 1, 1], ['census', '46 66 81 93 101', 1891, 10], ['y = 2ˣ', '1 2 4 8 16 32', 0, 1]]))]),
                 dict(name='Find the error', blocks=[
                     dict(p='Add an error ε to one entry and watch how it spreads. Then hide it: can a classmate find which entry you changed?'),
                     dict(w='difftab', o=dict(y='1 0 5 22 57 116 205', eps=1, k=3))]),
                 dict(name='Code', blocks=[
                     dict(h='Difference table'), dict(code='difftable', tasks=['Run it. Which order is constant?', 'Change y to the homework data 2, 9, 28, 65, 126.', 'Change 22 to 23 and look at the third differences.'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Show that $E = e^{hD}$.', 'By Taylor\'s series, $Ef(x) = f(x+h) = f(x) + hf\'(x) + \\tfrac{h^2}{2!}f\'\'(x) + \\cdots = (1 + hD + \\tfrac{(hD)^2}{2!} + \\cdots)f(x) = e^{hD}f(x)$.'),
                         ('Prove that $\\Delta - \\nabla = \\Delta\\nabla$.', 'Both sides equal $E - 2 + E^{-1}$: $\\Delta - \\nabla = (E - 1) - (1 - E^{-1})$ and $\\Delta\\nabla = (E - 1)(1 - E^{-1})$.'),
                         ('Prove that $\\mu^2 = 1 + \\tfrac14\\delta^2$.', '$\\mu^2 = \\tfrac14(E^{1/2} + E^{-1/2})^2 = \\tfrac14(E + 2 + E^{-1})$ and $\\delta^2 = E - 2 + E^{-1}$, so $\\mu^2 - \\tfrac14\\delta^2 = \\tfrac14 \\cdot 4 = 1$.'),
                         ('Find the missing term in $1, 3, 9, \\;?, 81$ assuming a cubic.', '$\\Delta^4 y_0 = 0$: $81 - 4y_3 + 54 - 12 + 1 = 0$, so $y_3 = 31$.'),
                         ('Evaluate $\\Delta^2(x^3)$ with $h = 1$.', '$\\Delta x^3 = (x+1)^3 - x^3 = 3x^2 + 3x + 1$; $\\Delta^2 x^3 = 3(2x + 1) + 3 = 6x + 6$.')])])]),
)
