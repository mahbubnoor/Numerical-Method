BT = '0 1 2 3 4 5'
BN = '100 150 230 340 510 770'
PX = '1 2 3 4 5 6'
PY = '2.1 3.9 8.2 15.8 26.1 37.7'
TH = '0 3 6 9 12 15 18 21'
TT = '24 22.5 23 27.5 32 33.5 30.5 26.5'
OVY = [-0.13, 0.61, 1.32, 1.0, 0.01, -0.34, -0.99, -0.96, -0.96, 0.05]
PRE = [['bacteria (exponential)', BT, BN, 'exp', 2, 8], ['Problem 1 (parabola)', PX, PY, 'poly', 2, ''], ['pendulum (power)', '0.25 0.5 1 1.5 2', '1 1.42 2.01 2.46 2.84', 'power', 2, 3],
       ['temperature (trig)', TH, TT, 'trig', 2, ''], ['planets (Kepler)', '0.387 0.723 1 1.524 5.203 9.537', '0.241 0.615 1 1.881 11.86 29.46', 'power', 2, '']]

LECTURE = dict(
    title='Polynomial, Exponential and Trigonometric Fitting',
    short='Polynomial, exponential and trigonometric fits',
    sub='Curved trends with the same least-squares machinery: polynomial regression, straightening growth and power laws with logarithms, fitting periodic data, and choosing a model that follows the trend without memorising the noise.',
    slides=[
        dict(type='cover', id='cover', notes="Recap question: 'Lecture 23 fitted y = a + bx. What happens to the normal equations if the model is y = a + bx + cx²?' (one more unknown, one more equation)."),
        dict(type='bullets', id='hook', title='The problem: how fast do the bacteria double?', kick='Why this lecture', rw=600,
             lead='A lab counts bacteria every hour. Each hour the count is multiplied by about 1.5. When does the culture double, and how many cells will there be after 8 hours?',
             items=['A straight line misses the curve: residuals $+74, -5, -55, -76, -36, +96$, and it predicts only 1063 cells at 8 h', 'The model is $N = ae^{bt}$: $b$ is <b>inside</b> the exponential, not linear in the unknowns',
                    'Least squares from Lecture 23 needs a model linear in its coefficients', 'Idea: take logarithms, and the curve becomes a straight line'],
             frag=True,
             right=dict(table=[['time $t$ (h)', 'count $N$'], [['0', '100'], ['1', '150'], ['2', '230'], ['3', '340'], ['4', '510'], ['5', '770'], ['8', '?']]]),
             notes="Straight-line fit to these counts: N = 25.7 + 129.7t, R² = 0.923: a high R² but a clear residual pattern. Solved at the end: doubling time 1.70 h, about 2600 cells at 8 h."),
        dict(type='goals', id='goals', items=[
            'Fit a <b>polynomial</b> of degree $m$ by least squares (normal equations of size $m + 1$)',
            '<b>Linearise</b> $y = ae^{bx}$ and $y = ax^{b}$ with logarithms and fit them',
            'Fit a <b>trigonometric</b> model to periodic data',
            'Recognise <b>overfitting</b> and choose the degree by test error',
            'Know what linearisation changes, and when a direct nonlinear fit is needed'],
            prev='Least squares for $y = a + bx$; matrix form $A^{T}A\\mathbf{c} = A^{T}\\mathbf{y}$; conditioning (Lecture 23).',
            today='Same normal equations with new columns: $x^2, x^3, \\dots$, $\\cos\\omega x$, $\\sin\\omega x$; and logarithms for growth laws.',
            notes=""),
        dict(type='math', id='poly', title='Polynomial least squares: more columns, same method',
             eqs=[dict(cap='Model of degree m, and its least-squares criterion', eq='\\hat y = a_0 + a_1x + a_2x^2 + \\cdots + a_mx^m, \\qquad S = \\sum_{i}\\big(y_i - \\hat y_i\\big)^2'),
                  dict(cap='Parabola (m = 2): set ∂S/∂a₀ = ∂S/∂a₁ = ∂S/∂a₂ = 0', eq='\\begin{bmatrix} n & \\sum x & \\sum x^2 \\\\ \\sum x & \\sum x^2 & \\sum x^3 \\\\ \\sum x^2 & \\sum x^3 & \\sum x^4 \\end{bmatrix} \\begin{bmatrix} a_0 \\\\ a_1 \\\\ a_2 \\end{bmatrix} = \\begin{bmatrix} \\sum y \\\\ \\sum xy \\\\ \\sum x^2y \\end{bmatrix}', frag=True)],
             items=['Still <b>linear</b> in the unknowns $a_0, \\dots, a_m$: the curve is nonlinear, the problem is not', 'Entry $(j, k)$ is $\\sum x^{j+k}$: this is $A^{T}A$ with columns $1, x, x^2$',
                    'Need $n > m + 1$ points (with $n = m + 1$ it is interpolation)', 'Solve by Gaussian elimination or Cholesky (Lectures 12–13)'],
             ifrag=True, rw=600,
             notes="Pattern for the board: each row multiplies the model by 1, x, x² and sums. Students can write the m = 3 system by the same pattern."),
        dict(type='bullets', id='algo', title='Polynomial fitting, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Choose the degree $m$ (plot the data first; start low)', 'Tabulate the powers: $\\sum x^k$ for $k = 0, \\dots, 2m$ and $\\sum x^ky$ for $k = 0, \\dots, m$', 'Fill the $(m + 1) \\times (m + 1)$ normal equations: entry $(j, k) = \\sum x^{j+k}$',
                    'Solve for $a_0, \\dots, a_m$ (Gauss with pivoting)', 'Compute residuals, $S$, $R^2$; check the pattern; for new $x$ evaluate by Horner'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input x[1..n], y[1..n], degree m\nfor k = 0 … 2m:  P[k] ← Σ x^k\nfor k = 0 … m:   r[k] ← Σ x^k·y\nfor j, k = 0 … m:\n    M[j][k] ← P[j + k]\na ← solve(M, r)      # Gauss / Cholesky\nS ← Σ (y − poly(a, x))²\nreturn a, S</pre></div><p class="small" style="margin-top:14px">For large $m$ use QR on centred, scaled $x$ instead (see the limitations).</p>'),
             notes=""),
        dict(type='table', id='p1', title='Problem 1: fit a parabola $y = a_0 + a_1x + a_2x^2$', cls='tb sm',
             q='Data: $x$ = 1, 2, 3, 4, 5, 6; $\\;y$ = 2.1, 3.9, 8.2, 15.8, 26.1, 37.7. A straight line leaves the residual pattern $+, -, -, -, -, +$.',
             head=['sum', 'value', 'sum', 'value'], frag=True,
             rows=[['$n$', '6', '$\\sum y$', '93.8'], ['$\\sum x$', '21', '$\\sum xy$', '454.4'], ['$\\sum x^2$', '91', '$\\sum x^2y$', '2354'], ['$\\sum x^3$', '441', '', ''], ['$\\sum x^4$', '2275', '', '']],
             answer='Normal equations: $6a_0 + 21a_1 + 91a_2 = 93.8$, $\\;21a_0 + 91a_1 + 441a_2 = 454.4$, $\\;91a_0 + 441a_1 + 2275a_2 = 2354$. Solving: <b>$a_0 = 2.580$, $a_1 = -1.9193$, $a_2 = 1.3036$</b>.',
             right=dict(w='lsq', o=dict(x=PX, y=PY, models=['line', 'poly'], model='poly', deg=2, height='330px', compact=True, notable=True)), rw=700,
             notes="Solution by elimination: a₂ = 1.303571, a₁ = −1.919286, a₀ = 2.580000. S = 0.5123 (line: 63.95), R² = 0.99947. Residuals now have no pattern."),
        dict(type='widget', id='explore', title='Explore: choose the model and the degree', w='lsq',
             o=dict(x=PX, y=PY, model='poly', deg=2, height='340px', side=True, tableHeight='340px', presets=PRE), lw=440,
             items=['Raise the degree: $S$ always falls, but does the curve still look sensible?', 'Bacteria preset: compare "polynomial" with "exponential"', 'Pendulum: the power law $T = aL^{b}$ gives $b \\approx 0.5$',
                    'Temperature: one sine wave per day'],
             notes="With the parabola data: degree 1 S = 63.95, degree 2 S = 0.51, degree 3 S = 0.17, degree 5 S = 0 (interpolation through all six points). The big drop is from 1 to 2; after that S falls only because the curve starts following the noise."),
        dict(type='math', id='linearise', title='Linearisation: straighten the curve, then fit a line',
             eqs=[dict(cap='Exponential: plot ln y against x', eq='y = ae^{bx} \\;\\Longrightarrow\\; \\underbrace{\\ln y}_{Y} = \\underbrace{\\ln a}_{A} + b\\,x'),
                  dict(cap='Power law: plot ln y against ln x', eq='y = ax^{b} \\;\\Longrightarrow\\; \\underbrace{\\ln y}_{Y} = \\underbrace{\\ln a}_{A} + b\\,\\underbrace{\\ln x}_{X}', frag=True),
                  dict(cap='Saturation (Michaelis–Menten): plot 1/y against 1/x', eq='y = \\frac{ax}{b + x} \\;\\Longrightarrow\\; \\frac1y = \\frac1a + \\frac ba\\cdot\\frac1x', frag=True)],
             items=['Fit $Y = A + bX$ with Lecture 23\'s formulas, then $a = e^{A}$', 'Test: if the transformed points lie on a line, the model is right', 'Needs $y > 0$ (and $x > 0$ for the power law)',
                    'Caution: this minimises errors in $\\ln y$, not in $y$, so large $y$ get less weight'],
             ifrag=True, rw=560,
             notes="Semi-log paper (exponential) and log-log paper (power law) were the paper-and-pencil versions of this idea."),
        dict(type='worked', id='p2', title='Problem 2: fit $N = ae^{bt}$ to the bacteria counts',
             steps=['$Y = \\ln N$: 4.6052, 5.0106, 5.4381, 5.8289, 6.2344, 6.6464', '$\\sum t = 15$, $\\sum t^2 = 55$, $\\sum Y = 33.76363$, $\\sum tY = 91.54323$, $n = 6$',
                    '$b = \\dfrac{6(91.54323) - 15(33.76363)}{6(55) - 15^2} = \\dfrac{42.80493}{105} = 0.407666$', '$A = \\dfrac{33.76363 - 15(0.407666)}{6} = 4.608108$, $\\;a = e^{A} = 100.29$',
                    'Doubling time $\\ln 2/b = 1.70$ h; $\\;N(8) = 100.29\\,e^{0.407666 \\times 8} \\approx 2616$'],
             answer='$N = 100.3\\,e^{0.4077t}$: the count grows 50.3% per hour ($e^{b} = 1.503$) and doubles every 1.70 hours.',
             right=dict(w='lsq', o=dict(x=BT, y=BN, models=['exp', 'line'], model='exp', at=8, height='340px', compact=True, notable=True)), rw=740,
             notes="Direct nonlinear least squares in N (Gauss–Newton, Lecture 25) gives a = 100.436, b = 0.407153: almost the same here because the data are nearly exact. With noisy data the two can differ noticeably."),
        dict(type='worked', id='p3', title='Problem 3: a power law for the pendulum, $T = aL^{b}$',
             q='Lengths $L$ (m) = 0.25, 0.5, 1, 1.5, 2; periods $T$ (s) = 1.00, 1.42, 2.01, 2.46, 2.84. Find $a$ and $b$.',
             steps=['$X = \\ln L$: $-1.3863, -0.6931, 0, 0.4055, 0.6931$', '$Y = \\ln T$: $0, 0.3507, 0.6981, 0.9002, 1.0438$', 'Line fit of $Y$ on $X$: $b = 0.5018$, $\\;A = 0.6970$',
                    '$a = e^{0.6970} = 2.0077$'],
             answer='$T = 2.008\\,L^{0.502}$. Theory: $T = \\dfrac{2\\pi}{\\sqrt g}L^{1/2} = 2.006\\,L^{0.5}$: the fit recovers the physics, and $g = (2\\pi/a)^2 = 9.79$ m/s².',
             right=dict(w='lsq', o=dict(x='0.25 0.5 1 1.5 2', y='1 1.42 2.01 2.46 2.84', models=['power'], at=3, height='330px', compact=True, notable=True)), rw=740,
             notes="The exponent tells the law: b = 0.5 means 'quadruple the length, double the period'. Kepler's third law (apps) is the same calculation with b = 1.5."),
        dict(type='math', id='trig', title='Periodic data: a trigonometric fit',
             eqs=[dict(cap='Known period P, ω = 2π/P; still linear in a₀, a₁, b₁', eq='\\hat y = a_0 + a_1\\cos\\omega x + b_1\\sin\\omega x'),
                  dict(cap='n points equally spaced over one period: the normal equations decouple', eq='a_0 = \\frac1n\\sum y_i, \\quad a_1 = \\frac2n\\sum y_i\\cos\\omega x_i, \\quad b_1 = \\frac2n\\sum y_i\\sin\\omega x_i', frag=True),
                  dict(cap='Amplitude and time of the peak', eq='C = \\sqrt{a_1^2 + b_1^2}, \\qquad \\hat y = a_0 + C\\cos\\big(\\omega(x - x_{\\text{peak}})\\big)', frag=True)],
             items=['Temperature every 3 h over a day ($P = 24$): $a_0 = 27.44$, $a_1 = -4.12$, $b_1 = -3.64$', 'Amplitude $C = 5.50$ °C; peak at $\\omega x = \\text{atan2}(b_1, a_1)$: about <b>14.8 h</b> (2:45 pm)',
                    'More harmonics ($\\cos 2\\omega x$, …) give the Fourier series: the FFT does this fast', 'Tides, seasons, electricity demand, heart rhythms'],
             ifrag=True, rw=600,
             notes="Why they decouple: over a full period, Σcos ωxᵢ = Σ sin ωxᵢ = Σ cos·sin = 0 and Σcos² = Σsin² = n/2, so AᵀA is diagonal.\n\natan2(−3.643, −4.121) = −138.5° = 221.5°; 221.5 / 15° per hour = 14.76 h."),
        dict(type='widget', id='overfit', title='Overfitting: a perfect fit to the training data, a bad model', kick='Choosing the degree', w='overfit',
             o=dict(y=OVY, deg=3, height='360px'), lw=460,
             items=['Ten noisy samples of $\\sin 2\\pi x$; "test error" compares the fit with the true curve', 'Degree 1: underfits (train 0.62, test 0.46)', 'Degree 3–5: test error lowest (about 0.12)',
                    'Degree 9: passes through every point (train 0) but test error <b>0.58</b>: it memorised the noise', 'Choose the degree by error on data <b>not used</b> for fitting'],
             frag=True,
             notes="Numbers with these ten points (RMS): degree 1 train 0.619 / test 0.464; degree 3: 0.160 / 0.127; degree 5: 0.152 / 0.113; degree 9: 0.000 / 0.581.\n\nThis is the bias–variance trade-off. In ML practice: split data into training and validation sets, or use cross-validation."),
        dict(type='compare', id='classic', title='Same growth data, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (linearise by hand)', tag='Logarithms', cls='blue', items=['Take $\\ln N$, fit a line with the sums formulas', '$a = 100.29$, $b = 0.407666$', 'Works only for models that can be straightened']),
             right=dict(h='Numerical (minimise $S$ directly)', tag='Algorithm', cls='key', items=['Minimise $\\sum (N_i - ae^{bt_i})^2$ by Gauss–Newton', '$a = 100.44$, $b = 0.407153$ in 3 iterations', 'Any model, errors measured in the original units']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>Logistic growth $N = \\dfrac{K}{1 + e^{-r(t - t_0)}}$ with unknown capacity $K$</h3><p>No logarithm turns this into a straight line in $K$, $r$ and $t_0$ together. The only way is to minimise $S(K, r, t_0)$ iteratively: Gauss–Newton or gradient descent (Lecture 25). This is how epidemic and market-adoption curves are fitted.</p></div>'),
             notes=""),
        dict(type='code', id='code', title='Polynomial and exponential fits in code', code='polyfit', lw=560,
             items=['Builds the $(m+1) \\times (m+1)$ normal equations from power sums', 'Gaussian elimination with pivoting', 'Prints coefficients, $S$ and $R^2$', 'Lab: the exponential fit through logarithms'],
             notes="Expected output for m = 2: a0 = 2.580000, a1 = −1.919286, a2 = 1.303571, S = 0.512286."),
        dict(type='table', id='fail', title='Limitations shown failing', kick='When curve fitting misleads', cls='tb sm',
             head=['problem', 'what happens', 'remedy'], tx=(0, 1, 2), frag=True,
             rows=[['High degree, normal equations', 'cond($A^{T}A$) for 10 points in $[0, 1]$: degree 3: $10^{4}$, degree 5: $10^{7}$, degree 9: $2\\times10^{14}$', 'centre and scale $x$; QR; orthogonal polynomials'],
                   ['Overfitting', 'degree 9 through 10 noisy points: train error 0, test error 0.58', 'choose the degree by validation; regularise (ridge)'],
                   ['Extrapolating a polynomial', 'Lecture 23 data, degree 5: 40.4 min at 12 km, 32.9 at 13 km', 'use a model with physical meaning; do not extrapolate far'],
                   ['Log transform', 'needs $y > 0$; a count of 0 gives $\\ln 0 = -\\infty$', 'add a small constant, or fit directly'],
                   ['Log transform weights', 'minimises relative error: small $y$ dominate, large $y$ fit worse', 'weights $w_i = y_i^2$, or Gauss–Newton (L25)']],
             right=dict(w='lsq', o=dict(x='2 4 5 7 9 11', y='14 21 24 30 37 42', models=['poly'], deg=5, at=13, height='360px', compact=True, notable=True)), rw=600,
             notes="The widget: Lecture 23's delivery data with a degree-5 polynomial (interpolation) evaluated at 13 km.\n\nRidge regression adds λΣaₖ² to S: the normal equations become (AᵀA + λI)c = Aᵀy, which is better conditioned and keeps the coefficients small. Try λ = 10^−3 with degree 9 in the lab's overfitting tab: the wild curve calms down."),
        dict(type='exam', id='practice', src='Problem 4',
             q='"Fit a second-degree parabola $y = a + bx + cx^2$ to the data $x$: 0, 1, 2, 3, 4 and $y$: 1, 1.8, 1.3, 2.5, 6.3 by the method of least squares."',
             tips=['Sums: $\\sum x = 10$, $\\sum x^2 = 30$, $\\sum x^3 = 100$, $\\sum x^4 = 354$, $\\sum y = 12.9$, $\\sum xy = 37.1$, $\\sum x^2y = 130.3$',
                   'Normal equations: $5a + 10b + 30c = 12.9$; $\\;10a + 30b + 100c = 37.1$; $\\;30a + 100b + 354c = 130.3$', 'Eliminate: $c = 0.55$, $\\;b = -1.07$, $\\;a = 1.42$',
                   'Answer $y = 1.42 - 1.07x + 0.55x^2$; check one residual, e.g. at $x = 4$: $1.42 - 4.28 + 8.8 = 5.94$ vs 6.3'],
             notes="Shortcut for equally spaced x: substitute u = x − 2 so that Σu = Σu³ = 0; the system splits into easier pieces."),
        dict(type='profile', id='profile', title='Polynomial, exponential and trigonometric fitting: method profile',
             best=['Smooth trends with noise; low degree (1–3)', 'Growth and decay (exponential) or scaling laws (power) seen as straight lines on log axes', 'Periodic data with a known period'],
             worst=['High-degree polynomials: ill-conditioned, wiggly, extrapolate badly', 'Log transforms with zeros or very noisy small values', 'Models that cannot be made linear in the parameters'],
             suited=['Growth of populations, investments, epidemics (early phase)', 'Physics and engineering laws ($T \\propto L^{1/2}$, Kepler $T \\propto a^{3/2}$)', 'Seasonal and daily cycles'],
             avoid=['Choosing the degree by $R^2$ on the same data', 'Predicting far beyond the data with polynomials', 'Fitting $\\ln y$ when errors in $y$ matter (use a direct fit)'],
             verdict='Rule of thumb: <b>pick the model from the physics or from the shape on log axes, keep the degree low, and check it on data not used for fitting</b>.',
             notes=""),
        dict(type='table', id='compare', title='Comparative analysis: models for curved data', cls='tb sm',
             head=['Model', 'Linear in unknowns?', 'How to fit', 'Size of system', 'Typical use'], tx=(0,), frag=True,
             rows=[['$a + bx$', 'yes', 'sums formulas (L23)', '2 × 2', 'trends'], ['$a_0 + a_1x + \\dots + a_mx^m$', 'yes', 'normal equations / QR', '$(m+1)$ square', 'smooth curves, low $m$'],
                   ['$ae^{bx}$', 'no, but linearisable', 'line fit to $(x, \\ln y)$', '2 × 2', 'growth, decay, cooling'], ['$ax^{b}$', 'no, but linearisable', 'line fit to $(\\ln x, \\ln y)$', '2 × 2', 'scaling laws'],
                   ['$a_0 + a_1\\cos\\omega x + b_1\\sin\\omega x$', 'yes (ω known)', 'decoupled formulas', '3 diagonal', 'cycles, seasons'], ['$\\dfrac{K}{1 + e^{-r(t - t_0)}}$', 'no', 'Gauss–Newton (L25)', 'iterative', 'saturation, adoption']],
             note='"Linear least squares" means linear in the <b>coefficients</b>, not a straight-line curve.', notefrag=True,
             notes=""),
        dict(type='bridge', id='bridge', title='Limitations, and where we fix them', lead='Every fit so far was a single linear solve. The last lecture replaces the linear solve with an iteration that can minimise anything.',
             keep=['Any model linear in its coefficients: one linear solve', 'Logarithms straighten growth and power laws', 'Trigonometric terms for cycles', 'Validation error picks the degree'],
             rows=[['Linearisation fits $\\ln y$, not $y$', 'Fit the original model directly: Gauss–Newton', 25], ['Models that cannot be linearised (logistic, neural networks)', 'Minimise $S$ by gradient descent', 25],
                   ['Choosing a regularisation λ and a degree', 'Minimise validation error: a 1-D optimisation (golden section)', 25], ['Huge data sets: forming $A^{T}A$ is too costly', 'Stochastic gradient descent, one batch at a time', 25]],
             notes=""),
        dict(type='apps', id='apps', n=2, lead='Click a card to fit real-world laws.',
             items=[
                 dict(ic='🪐', h="Kepler's third law", t='Planet periods from orbit sizes',
                      detail=dict(where='astronomy. Orbit size $a$ (AU) and period $T$ (years) for Mercury to Saturn. Fit $T = ca^{b}$ on log–log axes.',
                                  w='lsq', o=dict(x='0.387 0.723 1 1.524 5.203 9.537', y='0.241 0.615 1 1.881 11.86 29.46', models=['power'], height='210px', compact=True, notable=True),
                                  note='$b = 1.4997$, $c = 1.0003$: $T^2 = a^3$, the law Kepler found by hand in 1619.')),
                 dict(ic='💻', h="Moore's law", t='Transistors double every two years',
                      detail=dict(where='the chip industry. Transistor counts of processors 1971–2018 grow from 2300 to 20 billion; a straight line fits $\\ln(\\text{count})$ against the year.',
                                  w='lsq', o=dict(x='0 7 14 22 29 35 41 47', y='2300 29000 275000 3100000 42000000 290000000 1400000000 20000000000', models=['exp'], height='210px', compact=True, notable=True, logy=True),
                                  note='Logarithmic vertical axis: the exponential is a straight line. $b = 0.332$ per year (years counted from 1971): doubling time $\\ln 2/0.332 = 2.1$ years. Rough counts for typical chips, rounded.')),
                 dict(ic='🌡️', h='Daily and seasonal cycles', t='Temperature, tides, electricity demand',
                      detail=dict(where='weather and power-grid planning. Readings every 3 hours over a day, fitted with one cosine and one sine of period 24 h.',
                                  w='lsq', o=dict(x=TH, y=TT, models=['trig'], period=24, height='210px', compact=True, notable=True),
                                  note='Mean 27.4 °C, amplitude 5.5 °C, warmest at about 2:45 pm. Grid operators add weekly and yearly terms the same way.')),
                 dict(ic='💊', h='Drug concentration in blood', t='Half-life from a few blood samples',
                      detail=dict(where='pharmacokinetics. After a dose, concentration decays like $C = C_0e^{-kt}$; the half-life $\\ln 2/k$ sets how often a medicine is taken.',
                                  steps=['Measure $C$ at several times after the dose', 'Fit a line to $\\ln C$ against $t$: slope $-k$', 'Half-life $t_{1/2} = 0.693/k$', 'Two-compartment models (sum of two exponentials) need a nonlinear fit (Lecture 25)'],
                                  note='Same calculation as the bacteria, with $b < 0$.'))],
             notes="The first three cards are interactive inside the pop-up."),
        dict(type='check', id='check', q='To fit $y = ae^{bx}$ by linearisation, which pairs do you put into the straight-line formulas?',
             opts=['$(x_i, \\ln y_i)$', '$(\\ln x_i, \\ln y_i)$', '$(\\ln x_i, y_i)$', '$(x_i, y_i)$, then take logs of $a$ and $b$'], right=0,
             answer='A. $\\ln y = \\ln a + bx$ is a line in $x$ and $\\ln y$; the slope is $b$ and $a = e^{\\text{intercept}}$. Option B is for the power law $y = ax^{b}$.',
             notes=""),
        dict(type='summary', id='summary', items=[
            'Polynomial of degree $m$: $(m+1)$ normal equations with entries $\\sum x^{j+k}$; keep $m$ low',
            '$y = ae^{bx}$: line through $(x, \\ln y)$; $\\;y = ax^{b}$: line through $(\\ln x, \\ln y)$',
            'Periodic: $a_0 + a_1\\cos\\omega x + b_1\\sin\\omega x$; equally spaced data decouple',
            'Choose the model by validation error, not by training error'],
            hw=['Fit $y = a + bx + cx^2$ to $x$: 1, 2, 3, 4, 5, 6 and $y$: 2.1, 3.9, 8.2, 15.8, 26.1, 37.7 and verify Problem 1.', 'Fit $y = ae^{bx}$ to $x$: 0, 1, 2, 3 and $y$: 2.0, 3.3, 5.4, 9.0.',
                'Fit $y = ax^{b}$ to $x$: 1, 2, 4, 8 and $y$: 3.0, 4.2, 6.1, 8.4.', 'With the overfitting widget, record train and test error for degrees 0–9 and explain the shape of both curves.'],
            solved='$N = 100.3\\,e^{0.4077t}$: the bacteria <b>double every 1.70 hours</b>, and after 8 hours there will be about <b>2600</b> cells (direct nonlinear fit: 2609).',
            next='<b>Lecture 25: numerical optimisation for machine learning.</b> Golden-section search, gradient descent, Newton and Gauss–Newton: minimising any error function.',
            notes="Homework answers: Q1: a = 2.58, b = −1.9193, c = 1.3036. Q2: ln y = 0.6920 + 0.5005x → y = 1.998 e^{0.5005x}. Q3: b = 0.4995, a = 2.999 → y = 3.00 x^0.4995. Q4: see the overfitting slide notes."),
    ],
    code={
        'polyfit': dict(file='polynomial_fit', py='''# Least-squares polynomial of degree m via the normal equations
x = [1, 2, 3, 4, 5, 6]
y = [2.1, 3.9, 8.2, 15.8, 26.1, 37.7]
m = 2
n, k = len(x), m + 1

P = [sum(xi ** p for xi in x) for p in range(2 * m + 1)]            # power sums
M = [[P[i + j] for j in range(k)] for i in range(k)]
r = [sum(xi ** i * yi for xi, yi in zip(x, y)) for i in range(k)]
print("power sums:", " ".join(f"{v:.0f}" for v in P))
print("right side:", " ".join(f"{v:.1f}" for v in r))

for j in range(k):                                                  # Gauss with pivoting
    p = max(range(j, k), key=lambda i: abs(M[i][j]))
    M[j], M[p] = M[p], M[j]
    r[j], r[p] = r[p], r[j]
    for i in range(j + 1, k):
        f = M[i][j] / M[j][j]
        for q in range(j, k):
            M[i][q] -= f * M[j][q]
        r[i] -= f * r[j]
a = [0.0] * k
for j in range(k - 1, -1, -1):
    a[j] = (r[j] - sum(M[j][q] * a[q] for q in range(j + 1, k))) / M[j][j]
print("coefficients:", "  ".join(f"a{i} = {a[i]:.6f}" for i in range(k)))

def poly(t):                                                        # Horner
    s = 0.0
    for c in reversed(a):
        s = s * t + c
    return s

ybar = sum(y) / n
S = sum((yi - poly(xi)) ** 2 for xi, yi in zip(x, y))
St = sum((yi - ybar) ** 2 for yi in y)
print(f"S = {S:.6f}   R^2 = {1 - S / St:.6f}")
''', c='''/* Least-squares polynomial of degree m via the normal equations */
#include <stdio.h>
#include <math.h>
#define N 6
#define MDEG 2
#define K (MDEG + 1)

double a[K];

double poly(double t) {                           /* Horner */
    double s = 0;
    for (int i = K - 1; i >= 0; i--) s = s * t + a[i];
    return s;
}

int main(void) {
    double x[N] = {1, 2, 3, 4, 5, 6}, y[N] = {2.1, 3.9, 8.2, 15.8, 26.1, 37.7};
    double P[2 * MDEG + 1], M[K][K], r[K];
    for (int p = 0; p <= 2 * MDEG; p++) { P[p] = 0; for (int i = 0; i < N; i++) P[p] += pow(x[i], p); }
    for (int i = 0; i < K; i++) {
        r[i] = 0;
        for (int t = 0; t < N; t++) r[i] += pow(x[t], i) * y[t];
        for (int j = 0; j < K; j++) M[i][j] = P[i + j];
    }
    printf("power sums:");
    for (int p = 0; p <= 2 * MDEG; p++) printf(" %.0f", P[p]);
    printf("\\nright side:");
    for (int i = 0; i < K; i++) printf(" %.1f", r[i]);
    printf("\\n");

    for (int j = 0; j < K; j++) {                   /* Gauss with pivoting */
        int p = j;
        for (int i = j + 1; i < K; i++) if (fabs(M[i][j]) > fabs(M[p][j])) p = i;
        for (int q = 0; q < K; q++) { double t = M[j][q]; M[j][q] = M[p][q]; M[p][q] = t; }
        double t = r[j]; r[j] = r[p]; r[p] = t;
        for (int i = j + 1; i < K; i++) {
            double f = M[i][j] / M[j][j];
            for (int q = j; q < K; q++) M[i][q] -= f * M[j][q];
            r[i] -= f * r[j];
        }
    }
    for (int j = K - 1; j >= 0; j--) {
        double s = r[j];
        for (int q = j + 1; q < K; q++) s -= M[j][q] * a[q];
        a[j] = s / M[j][j];
    }
    printf("coefficients:");
    for (int i = 0; i < K; i++) printf("%sa%d = %.6f", i ? "  " : " ", i, a[i]);
    printf("\\n");

    double ybar = 0, S = 0, St = 0;
    for (int i = 0; i < N; i++) ybar += y[i] / N;
    for (int i = 0; i < N; i++) {
        S += (y[i] - poly(x[i])) * (y[i] - poly(x[i]));
        St += (y[i] - ybar) * (y[i] - ybar);
    }
    printf("S = %.6f   R^2 = %.6f\\n", S, 1 - S / St);
    return 0;
}
'''),
        'expfit': dict(file='exponential_fit', py='''# Fit N = a*e^(b t) by a straight line through (t, ln N)
import math
t = [0, 1, 2, 3, 4, 5]
N = [100, 150, 230, 340, 510, 770]
n = len(t)
Y = [math.log(v) for v in N]

St, SY = sum(t), sum(Y)
Stt = sum(ti * ti for ti in t)
StY = sum(ti * yi for ti, yi in zip(t, Y))
print(f"sum t = {St}, sum t^2 = {Stt}, sum lnN = {SY:.5f}, sum t lnN = {StY:.5f}")

b = (n * StY - St * SY) / (n * Stt - St * St)
A = (SY - b * St) / n
a = math.exp(A)
print(f"b = {b:.6f}   ln a = {A:.6f}   a = {a:.3f}")
print(f"growth per hour: {math.exp(b):.4f}   doubling time: {math.log(2) / b:.3f} h")
for ti, Ni in zip(t, N):
    print(f"t = {ti}  N = {Ni:4d}  model = {a * math.exp(b * ti):8.2f}")
print(f"prediction at t = 8 h: {a * math.exp(8 * b):.0f}")
''', c='''/* Fit N = a*e^(b t) by a straight line through (t, ln N) */
#include <stdio.h>
#include <math.h>
#define NP 6

int main(void) {
    double t[NP] = {0, 1, 2, 3, 4, 5}, N[NP] = {100, 150, 230, 340, 510, 770};
    double St = 0, SY = 0, Stt = 0, StY = 0;
    for (int i = 0; i < NP; i++) {
        double Y = log(N[i]);
        St += t[i]; SY += Y; Stt += t[i] * t[i]; StY += t[i] * Y;
    }
    printf("sum t = %.0f, sum t^2 = %.0f, sum lnN = %.5f, sum t lnN = %.5f\\n", St, Stt, SY, StY);

    double b = (NP * StY - St * SY) / (NP * Stt - St * St);
    double A = (SY - b * St) / NP, a = exp(A);
    printf("b = %.6f   ln a = %.6f   a = %.3f\\n", b, A, a);
    printf("growth per hour: %.4f   doubling time: %.3f h\\n", exp(b), log(2) / b);
    for (int i = 0; i < NP; i++)
        printf("t = %.0f  N = %4.0f  model = %8.2f\\n", t[i], N[i], a * exp(b * t[i]));
    printf("prediction at t = 8 h: %.0f\\n", a * exp(8 * b));
    return 0;
}
'''),
    },
    lab=dict(title='Curve Fitting Lab',
             intro='Fit polynomials, exponentials, power laws and periodic models to your own data, and see overfitting happen.',
             tabs=[
                 dict(name='Curve fit', blocks=[
                     dict(p='Choose the model; for a polynomial set the degree, for the trigonometric model the period. The table lists fitted values and residuals.'),
                     dict(w='lsq', o=dict(x=BT, y=BN, model='exp', at=8, height='320px', side=True, tableHeight='320px', presets=PRE + [['homework 2', '0 1 2 3', '2 3.3 5.4 9', 'exp', 2, ''], ['homework 3', '1 2 4 8', '3 4.2 6.1 8.4', 'power', 2, ''], ['Problem 4', '0 1 2 3 4', '1 1.8 1.3 2.5 6.3', 'poly', 2, '']]))]),
                 dict(name='Overfitting', blocks=[
                     dict(p='Ten noisy samples of sin 2πx. Move the degree; the right plot shows training and test error for every degree. Turn on ridge regularisation (λ) to tame high degrees.'),
                     dict(w='overfit', o=dict(y=OVY, deg=3, height='300px', ridge=True))]),
                 dict(name='Code', blocks=[
                     dict(h='Polynomial fit'), dict(code='polyfit', tasks=['Run it. Compare with Problem 1.', 'Set m = 1 and m = 3: how much does S change?', 'Use the data of Problem 4 and check a = 1.42, b = −1.07, c = 0.55.']),
                     dict(h='Exponential fit'), dict(code='expfit', tasks=['Run it. Compare with Problem 2.', 'Change the data to homework 2.', 'Change the program to fit a power law (use ln t; drop t = 0).'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Write the normal equations for fitting $y = a + bx + cx^2$.', '$na + b\\sum x + c\\sum x^2 = \\sum y$; $\\;a\\sum x + b\\sum x^2 + c\\sum x^3 = \\sum xy$; $\\;a\\sum x^2 + b\\sum x^3 + c\\sum x^4 = \\sum x^2y$.'),
                         ('How do you fit $y = ae^{bx}$ by least squares?', 'Take logarithms: $\\ln y = \\ln a + bx$. Fit a straight line to the points $(x_i, \\ln y_i)$; the slope is $b$ and $a = e^{\\text{intercept}}$.'),
                         ('How do you fit $y = ax^{b}$?', '$\\ln y = \\ln a + b\\ln x$: fit a straight line to $(\\ln x_i, \\ln y_i)$.'),
                         ('Why is fitting $\\ln y$ not the same as fitting $y$?', 'It minimises the squared errors of $\\ln y$, i.e. roughly relative errors, so small values of $y$ get more weight; the result differs slightly from minimising $\\sum (y_i - ae^{bx_i})^2$.'),
                         ('What is overfitting and how is it detected?', 'A model with too many parameters fits the noise of the training data: training error is tiny but error on new data is large. It is detected by measuring the error on data not used for fitting (validation or test data).')])])]),
)
