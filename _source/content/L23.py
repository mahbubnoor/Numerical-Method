DX = '2 4 5 7 9 11'
DY = '14 21 24 30 37 42'
PRESETS = [['delivery data', DX, DY, 'line', 1, 15], ['one outlier (y₆ = 70)', DX, '14 21 24 30 37 70', 'line', 1, 15], ['Problem 3 data', '1 2 3 4 5', '3 5 6 9 11', 'line', 1, ''],
           ['spring (Hooke)', '0 1 2 3 4', '10 10.9 12.1 13 13.9', 'line', 1, 2.5], ['curved data', '1 2 3 4 5 6', '2.1 3.9 8.2 15.8 26.1 37.7', 'line', 1, '']]

LECTURE = dict(
    title='Least Squares and Linear Regression',
    short='Least squares and linear regression',
    sub='When there are more data points than unknowns, no curve passes through all of them. Least squares picks the curve that makes the total squared error smallest: the normal equations, their matrix form, how to judge a fit, and where the method breaks.',
    slides=[
        dict(type='cover', id='cover', notes="Start with a question to the class: 'If six measurements do not lie on a line, which line is the best one?' Collect two or three answers (through the first and last point, by eye, average of slopes) before showing the method."),
        dict(type='bullets', id='hook', title='The problem: predicting a delivery time', kick='Why this lecture', rw=620,
             lead='A food-delivery company records six orders: distance $x$ (km) and delivery time $y$ (minutes). How long will a 15 km order take?',
             items=['The points lie <b>almost</b> on a line, but no line passes through all six', 'Interpolation (Lectures 16–18) forces a curve through every point: degree 5 here',
                    'That curve predicts 40.4 min at 12 km and <b>32.9 min at 13 km</b>: a longer trip that is faster. Nonsense', 'Data have <b>noise</b>; we want the trend, not every wiggle'],
             frag=True,
             right=dict(table=[['distance $x$ (km)', 'time $y$ (min)'], [['2', '14'], ['4', '21'], ['5', '24'], ['7', '30'], ['9', '37'], ['11', '42'], ['15', '?']]]),
             notes="Degree-5 interpolant through the six points: 33.40 at x = 8 (fine, inside the data), 40.44 at 12, 32.86 at 13. Outside the data the interpolating polynomial turns over. Solved at the end: least squares gives 55.1 min."),
        dict(type='goals', id='goals', items=[
            'Define the <b>residual</b> and the least-squares criterion',
            'Derive and solve the <b>normal equations</b> for a straight line',
            'Write least squares in <b>matrix form</b> $A^{T}A\\mathbf{c} = A^{T}\\mathbf{y}$ and fit models with several inputs',
            'Judge a fit with $S$, $R^2$ and the residual plot',
            'Recognise when least squares misleads: outliers, extrapolation, ill-conditioning'],
            prev='Interpolation: a polynomial through every data point (Lectures 16–18); solving linear systems (Lectures 12–13).',
            today='A simple curve that passes <b>close to</b> all points, chosen by minimising the sum of squared errors.',
            notes="First lecture of Module 7. Least squares links Module 3 (linear systems) with machine learning."),
        dict(type='math', id='idea', title='Working principle: make the squared residuals as small as possible',
             eqs=[dict(cap='Model, and the residual of point i (vertical distance from the line)', eq='\\hat y = a + bx, \\qquad e_i = y_i - (a + bx_i)'),
                  dict(cap='Least-squares criterion: choose a and b to minimise', eq='S(a, b) = \\sum_{i=1}^{n} e_i^2 = \\sum_{i=1}^{n} \\big(y_i - a - bx_i\\big)^2', frag=True)],
             items=['$n$ equations $a + bx_i = y_i$, only 2 unknowns: <b>overdetermined</b>, no exact solution', 'Why squares? Positive and negative errors cannot cancel, big errors count more, and $S$ is smooth, so calculus finds its minimum',
                    'Sum of $|e_i|$ is more robust but has no simple formula', 'Gauss (1795) and Legendre (1805) invented it to fit planetary orbits'],
             ifrag=True, rw=620,
             notes="Draw three candidate lines on the board with the vertical residuals. Ask why we use vertical distances: because we predict y from x, the error is in y.\n\nGauss used least squares in 1801 to predict where the asteroid Ceres would reappear."),
        dict(type='math', id='normal', title='The normal equations for a straight line',
             eqs=[dict(cap='Set both partial derivatives of S to zero', eq='\\frac{\\partial S}{\\partial a} = -2\\sum (y_i - a - bx_i) = 0, \\quad \\frac{\\partial S}{\\partial b} = -2\\sum x_i(y_i - a - bx_i) = 0'),
                  dict(cap='Normal equations: a 2 × 2 linear system', eq='\\begin{aligned} na + b\\textstyle\\sum x_i &= \\textstyle\\sum y_i \\\\ a\\textstyle\\sum x_i + b\\textstyle\\sum x_i^2 &= \\textstyle\\sum x_iy_i \\end{aligned}', frag=True),
                  dict(cap='Solution', eq='b = \\frac{n\\sum x_iy_i - \\sum x_i\\sum y_i}{n\\sum x_i^2 - (\\sum x_i)^2}, \\qquad a = \\bar y - b\\,\\bar x', frag=True)],
             items=['Only four sums are needed: $\\sum x$, $\\sum y$, $\\sum x^2$, $\\sum xy$', 'The fitted line always passes through the mean point $(\\bar x, \\bar y)$', 'The denominator is zero only if all $x_i$ are equal', '$S$ is a convex bowl in $(a, b)$: this stationary point is the minimum'],
             ifrag=True, rw=520,
             notes="Point out the first normal equation divided by n: a + b x̄ = ȳ, so the line passes through the centroid. The residuals add up to zero."),
        dict(type='bullets', id='algo', title='Fitting a straight line, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Tabulate $x_i$, $y_i$, $x_i^2$, $x_iy_i$ and add each column', 'Write the two normal equations with these sums', 'Solve for $b$, then $a = (\\sum y - b\\sum x)/n$',
                    'Compute the residuals $e_i = y_i - a - bx_i$ and $S = \\sum e_i^2$', 'Check: $\\sum e_i \\approx 0$; look at the residual pattern; predict $\\hat y = a + bx$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input x[1..n], y[1..n]\nSx ← Σ x;   Sy ← Σ y\nSxx ← Σ x²; Sxy ← Σ x·y\nD ← n·Sxx − Sx²\nb ← (n·Sxy − Sx·Sy) / D\na ← (Sy − b·Sx) / n\nS ← Σ (y − a − b·x)²\nR² ← 1 − S / Σ (y − ȳ)²\nreturn a, b, S, R²</pre></div><p class="small" style="margin-top:14px">One pass over the data: $O(n)$ work.</p>'),
             notes="For large data with big values of x, use the centred form b = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)², which avoids cancellation (Lecture 3)."),
        dict(type='table', id='p1', title='Problem 1: the table of sums for the delivery data',
             q='Fit $y = a + bx$ to the six orders. First build the table of sums.',
             head=['$i$', '$x_i$', '$y_i$', '$x_i^2$', '$x_iy_i$'], frag=True, cls='tb sm',
             rows=[['1', '2', '14', '4', '28'], ['2', '4', '21', '16', '84'], ['3', '5', '24', '25', '120'], ['4', '7', '30', '49', '210'], ['5', '9', '37', '81', '333'], ['6', '11', '42', '121', '462'],
                   ['$\\sum$', '<b>38</b>', '<b>168</b>', '<b>296</b>', '<b>1237</b>']],
             right=dict(html='<div class="card key"><span class="tag">Normal equations</span><p style="font-size:34px;line-height:1.7">$6a + 38b = 168$<br>$38a + 296b = 1237$</p></div><p class="small">$n = 6$. Every number on the right comes from the bottom row of the table.</p>'), rw=620,
             notes="Ask students to fill one row each and check the column sums with their neighbour."),
        dict(type='worked', id='p1b', title='Problem 1 (continued): solve, check and predict',
             steps=['$D = n\\sum x^2 - (\\sum x)^2 = 6(296) - 38^2 = 1776 - 1444 = 332$', '$b = \\dfrac{6(1237) - 38(168)}{332} = \\dfrac{7422 - 6384}{332} = \\dfrac{1038}{332} = 3.126506$',
                    '$a = \\dfrac{168 - 38(3.126506)}{6} = \\dfrac{168 - 118.8072}{6} = 8.198795$', 'Residuals: $-0.45,\\ 0.30,\\ 0.17,\\ -0.08,\\ 0.66,\\ -0.59$ (sum 0); $\\;S = 1.1145$',
                    'Prediction: $\\hat y(15) = 8.1988 + 3.1265(15) = 55.10$ min'],
             answer='$y = 8.20 + 3.13x$: about 8 minutes to collect the order plus 3.1 minutes per km. $R^2 = 0.998$.',
             right=dict(w='lsq', o=dict(x=DX, y=DY, models=['line'], at=15, height='400px', compact=True, notable=True)), rw=760,
             notes="The intercept has a meaning: the fixed time to pick up the food. The slope: minutes per km (average speed about 19 km/h).\n\nThe prediction at 15 km is an extrapolation beyond the data (largest x = 11): state it with a warning."),
        dict(type='widget', id='explore', title='Explore: edit the data, watch the best line and its residuals', w='lsq',
             o=dict(x=DX, y=DY, models=['line'], at=15, height='360px', side=True, tableHeight='360px', presets=PRESETS), lw=440,
             items=['Red dashed segments are the residuals; the line minimises the sum of their squares', 'Change one $y$ value and see the whole line move', 'Outlier preset: one wrong value tilts the line from slope 3.1 to 5.5',
                    'Curved data: a line gives a <b>pattern</b> in the residuals (+, −, −, −, −, +)'],
             notes="Outlier: y₆ = 70 instead of 42 gives a = −2.09, b = 5.49: the prediction at 15 km jumps from 55 to 80 minutes. Curved data: R² = 0.934 looks high, but the residual signs show the model is wrong."),
        dict(type='math', id='matrix', title='Matrix form: any model that is linear in its coefficients',
             eqs=[dict(cap='n equations, k unknown coefficients (n > k): A c ≈ y', eq='\\underbrace{\\begin{bmatrix} 1 & x_1 \\\\ 1 & x_2 \\\\ \\vdots & \\vdots \\\\ 1 & x_n \\end{bmatrix}}_{A\\;(n\\times 2)} \\begin{bmatrix} a \\\\ b \\end{bmatrix} \\approx \\begin{bmatrix} y_1 \\\\ y_2 \\\\ \\vdots \\\\ y_n \\end{bmatrix}'),
                  dict(cap='Minimise ‖y − Ac‖²: the normal equations', eq='A^{T}A\\,\\mathbf{c} = A^{T}\\mathbf{y}', frag=True)],
             items=['$A^{T}A$ is $k \\times k$, symmetric and positive definite: solve by <b>Cholesky</b> (Lecture 13)', 'Geometry: $A\\mathbf{c}$ is the <b>projection</b> of $\\mathbf{y}$ onto the columns of $A$; the residual is perpendicular to every column',
                    'More inputs = more columns: $y = \\beta_0 + \\beta_1x_1 + \\beta_2x_2$ (multiple regression)', 'Columns may be any functions of $x$: $x^2$, $\\cos x$, … (Lecture 24)'],
             ifrag=True, rw=640,
             notes="Check with the straight line: AᵀA = [[n, Σx], [Σx, Σx²]], Aᵀy = [Σy, Σxy]: exactly the normal equations of the previous slide.\n\nOrthogonality: Aᵀ(y − Ac) = 0 is the same equation as the normal equations."),
        dict(type='worked', id='p2', title='Problem 2: multiple regression for house prices',
             q='Five flats: size $x_1$ (m²) = 50, 70, 80, 100, 120; rooms $x_2$ = 1, 2, 2, 3, 3; price $y$ (lakh Tk) = 30, 42, 47, 60, 68. Fit $y = \\beta_0 + \\beta_1x_1 + \\beta_2x_2$.',
             steps=['Rows of $A$: $(1, x_1, x_2)$, e.g. $(1, 50, 1)$; five rows, three columns', '$A^{T}A = \\begin{bmatrix} 5 & 420 & 11 \\\\ 420 & 38200 & 1010 \\\\ 11 & 1010 & 27 \\end{bmatrix}, \\quad A^{T}\\mathbf{y} = \\begin{bmatrix} 247 \\\\ 22360 \\\\ 592 \\end{bmatrix}$',
                    'Solve the 3 × 3 system by Gaussian elimination or Cholesky', '$\\beta_0 = 4.179$, $\\;\\beta_1 = 0.4282$ per m², $\\;\\beta_2 = 4.205$ per room'],
             answer='Price $\\approx 4.18 + 0.428x_1 + 4.21x_2$; a 90 m², 3-room flat: <b>55.3 lakh Tk</b>. $R^2 = 0.9994$.',
             right=dict(w='linsys', o=dict(mat='5 420 11 247; 420 38200 1010 22360; 11 1010 27 592', mode='chol', modes=['chol', 'gauss'], nodigits=True, nopivot=True, hint='[AᵀA | Aᵀy]')), rw=760,
             notes="Interpretation: each extra m² adds about 0.43 lakh; an extra room, at the same size, adds 4.2 lakh. Residuals 0.21, −0.56, 0.15, 0.38, −0.18; S = 0.564."),
        dict(type='math', id='fit', title='How good is the fit?',
             eqs=[dict(cap='Residual sum of squares, and its spread around the mean', eq='S = \\sum e_i^2, \\qquad S_t = \\sum (y_i - \\bar y)^2'),
                  dict(cap='Coefficient of determination and standard error (k coefficients)', eq='R^2 = 1 - \\frac{S}{S_t}, \\qquad s = \\sqrt{\\frac{S}{n - k}}', frag=True)],
             items=['$R^2$: fraction of the variation in $y$ explained by the model ($0 \\le R^2 \\le 1$)', 'Delivery data: $R^2 = 0.998$, $s = 0.53$ min: typical prediction error about half a minute',
                    'High $R^2$ is <b>not</b> proof: curved data fitted with a line still gives $R^2 = 0.93$', 'Always plot the residuals: random scatter = good model; a pattern = wrong model'],
             ifrag=True, rw=640,
             notes="s uses n − k because k coefficients were estimated (here 6 − 2 = 4): s = √(1.1145/4) = 0.528 min."),
        dict(type='compare', id='classic', title='Same question, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (hand formula)', tag='Algebra', cls='blue', items=['Straight line: two sums formulas for $a$ and $b$', 'Delivery data: $y = 8.20 + 3.13x$ in five minutes', 'One input variable, small $n$']),
             right=dict(h='Numerical (linear algebra)', tag='Algorithm', cls='key', items=['Build $A$, solve $A^{T}A\\mathbf{c} = A^{T}\\mathbf{y}$ or use QR', 'Any number of inputs and basis functions', 'Same code for 6 points or 6 million']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>Predicting a house price from 80 features and 1.5 million sales</h3><p>There is no hand formula for 81 coefficients. Numerically: an 81 × 81 system $A^{T}A\\mathbf{c} = A^{T}\\mathbf{y}$, or a QR factorisation of $A$, solved in well under a second. This is linear regression as used in industry.</p></div>'),
             notes="Even the 3 × 3 system of Problem 2 is tedious by hand. With many features, forming AᵀA costs about n·k² operations and solving it k³/3."),
        dict(type='code', id='code', title='Linear regression in code', code='linreg', lw=560,
             items=['Accumulates the four sums in one loop', 'Solves the normal equations; prints $a$, $b$', 'Residuals, $S$, $R^2$ and a prediction', 'Lab: multiple regression with Gaussian elimination'],
             notes="Expected output: a = 8.198795, b = 3.126506, S = 1.114458, R² = 0.997944, prediction 55.10."),
        dict(type='widget', id='fail', title='Limitations shown failing', kick='When least squares misleads', w='lsq',
             o=dict(x=DX, y='14 21 24 30 37 70', models=['line'], at=15, height='280px', side=True, tableHeight='280px', presets=PRESETS), lw=560,
             items=['<b>Outliers</b>: squaring gives a wrong point huge weight; one typo changes the 15 km prediction from 55 to 80 min', '<b>Extrapolation</b>: the line says nothing about traffic beyond 11 km',
                    '<b>Wrong model</b>: a line through curved data leaves a residual pattern', '<b>Ill-conditioning</b>: forming $A^{T}A$ squares the condition number (next slide)'],
             frag=True,
             notes="Remedies: robust losses (sum of |e|, Huber) minimised iteratively (Lecture 25); validate on new data; choose the model from the residual plot (Lecture 24)."),
        dict(type='table', id='cond', title='Limitation: the normal equations square the condition number', kick='When least squares misleads',
             q='Fit sales against the year $x = 2015, 2016, \\dots, 2020$. The columns of $A$ are $(1, \\dots, 1)$ and $(2015, \\dots, 2020)$: almost parallel.',
             head=['matrix', 'condition number', 'digits lost (of 16)'], tx=(0,), frag=True,
             rows=[['$A$ (years as given)', '$2.4\\times10^{6}$', 'about 6'], ['$A^{T}A$ (normal equations)', '$5.7\\times10^{12}$', 'about 13'], ['$A^{T}A$ with centred $x - 2017.5$', '2.9', 'none']],
             note='Fixes: <b>centre and scale</b> the inputs, or solve by <b>QR</b> ($A = QR$, then $R\\mathbf{c} = Q^{T}\\mathbf{y}$), which works with cond($A$) instead of its square. Library routines (numpy.linalg.lstsq) use QR or the SVD.', notefrag=True, rw=600,
             right=dict(html='<div class="card key frag fade"><span class="tag">Why centring helps</span><p>Years as given:</p><p style="font-size:32px">$A^{T}A = \\begin{bmatrix} 6 & 12105 \\\\ 12105 & 24421855 \\end{bmatrix}$</p><p>determinant $105$ out of numbers near $10^{8}$: nearly singular.</p><p>Centred, $x - 2017.5 = -2.5, \\dots, 2.5$:</p><p style="font-size:32px">$A^{T}A = \\begin{bmatrix} 6 & 0 \\\\ 0 & 17.5 \\end{bmatrix}$</p></div>'),
             notes="cond(AᵀA) = cond(A)² for the 2-norm. Rule of thumb from Lecture 11: you lose about log₁₀(cond) digits. Our widgets solve least squares by QR (modified Gram–Schmidt) on centred x for this reason."),
        dict(type='exam', id='practice', src='Problem 3',
             q='"Fit a straight line $y = a + bx$ to the data $x$: 1, 2, 3, 4, 5 and $y$: 3, 5, 6, 9, 11 by the method of least squares. Estimate $y$ at $x = 6$."',
             tips=['Make the table: $\\sum x = 15$, $\\sum y = 34$, $\\sum x^2 = 55$, $\\sum xy = 122$', 'Normal equations: $5a + 15b = 34$, $\\;15a + 55b = 122$',
                   'Solve: $b = \\dfrac{5(122) - 15(34)}{5(55) - 225} = \\dfrac{100}{50} = 2$, $\\;a = \\dfrac{34 - 30}{5} = 0.8$', 'Answer $y = 0.8 + 2x$; $\\;y(6) = 12.8$; residuals $0.2, 0.2, -0.8, 0.2, 0.2$ add to 0 (a quick check)'],
             notes=""),
        dict(type='profile', id='profile', title='Linear least squares: method profile',
             best=['Many noisy measurements, a model linear in its coefficients', 'Errors roughly equal in size and independent (then least squares is statistically optimal)', 'Closed-form answer: one linear solve, no iteration'],
             worst=['Outliers or heavy-tailed errors', 'Nearly parallel columns (ill-conditioning)', 'Models nonlinear in the parameters, e.g. $ae^{bx}$ fitted directly'],
             suited=['Calibration of sensors and instruments', 'Trend lines in economics and science', 'Linear regression in machine learning (the first model to try)'],
             avoid=['Exact data with no noise (interpolate instead)', 'Predictions far outside the data range', 'Data with gross errors (use robust regression)'],
             verdict='Rule of thumb: <b>fit, then look at the residuals before trusting $R^2$</b>; solve by QR, not by forming $A^{T}A$, when columns are nearly dependent.',
             notes=""),
        dict(type='table', id='compare', title='Comparative analysis: interpolation vs least squares, and ways to solve it', cls='tb sm',
             head=['Approach', 'Passes through points?', 'Work ($n$ points, $k$ coefficients)', 'Accuracy', 'Use when'], tx=(0,), frag=True,
             rows=[['Interpolation (L16–18)', 'yes, all', '$O(n^2)$', 'exact at data', 'data exact, few points'], ['Least-squares line by sums', 'no', '$O(n)$', 'sums may cancel', 'one input, by hand'],
                   ['Normal equations + Cholesky', 'no', '$nk^2 + k^3/3$', 'loses $\\log_{10}\\text{cond}(A)^2$ digits', 'well-conditioned, $n \\gg k$'], ['QR factorisation', 'no', '$2nk^2$', 'loses $\\log_{10}\\text{cond}(A)$ digits', 'default in libraries'],
                   ['Gradient descent (L25)', 'no', 'per pass $O(nk)$', 'iterative', 'huge $n$ and $k$']],
             note='Interpolation trusts every point; least squares trusts the trend. With noisy data, least squares predicts better.', notefrag=True,
             notes="SVD (singular value decomposition) is the most robust option, used when A may be rank-deficient."),
        dict(type='bridge', id='bridge', title='Limitations, and where we fix them', lead='Least squares is the foundation of data fitting. Its weak points lead to the last two lectures.',
             keep=['Closed form: one linear solve', 'Works for any model linear in its coefficients', 'Statistical meaning: best fit under random errors', 'Matrix form scales to many inputs'],
             rows=[['Data follow a curve, not a line', 'Polynomial least squares (more columns)', 24], ['Growth and power laws: $ae^{bx}$, $ax^b$', 'Linearise with logarithms', 24],
                   ['Too many coefficients fit the noise', 'Overfitting; choose the degree by test error', 24], ['Parameters inside a nonlinear model', 'Gauss–Newton iteration', 25],
                   ['Millions of rows or features; robust losses', 'Gradient descent on $S$', 25]],
             notes=""),
        dict(type='apps', id='apps', n=2, lead='Click a card to see least squares at work.',
             items=[
                 dict(ic='🤖', h='Linear regression in machine learning', t='The first model in every ML course',
                      detail=dict(where='scikit-learn\'s LinearRegression and numpy.linalg.lstsq. Training means solving $\\min \\|A\\mathbf{c} - \\mathbf{y}\\|^2$; the "features" are the columns of $A$.',
                                  w='lsq', o=dict(x=DX, y=DY, models=['line'], at=15, height='220px', compact=True, notable=True, presets=PRESETS),
                                  note='The loss used to train it, mean squared error, is $S/n$.')),
                 dict(ic='⚖️', h='Calibrating a sensor', t='A spring balance, a thermistor, a strain gauge',
                      detail=dict(where='instrument labs. Load a spring with known forces $F$ = 0, 1, 2, 3, 4 N and read the length $L$ = 10.0, 10.9, 12.1, 13.0, 13.9 cm. Fit $L = L_0 + F/k$.',
                                  w='lsq', o=dict(x='0 1 2 3 4', y='10 10.9 12.1 13 13.9', models=['line'], at=2.5, height='220px', compact=True, notable=True),
                                  note='$L = 10.0 + 0.99F$: natural length 10.0 cm, stiffness $k = 1/0.99 = 1.01$ N/cm. The calibration line then converts readings into forces.')),
                 dict(ic='🛰️', h='GPS positioning', t='More satellites than unknowns',
                      detail=dict(where='every phone. The unknowns are the position $(x, y, z)$ and the receiver clock error: 4 unknowns. With 8–12 satellites in view there are more equations than unknowns.',
                                  steps=['Each satellite gives one range equation, with measurement noise', 'Linearise about a guess (Newton, Lecture 10)', 'Solve the overdetermined linear system by least squares', 'Repeat 2–3 times: the Gauss–Newton method (Lecture 25)'],
                                  note='Extra satellites reduce the error: least squares averages the noise.')),
                 dict(ic='📈', h='Trend lines in science and economics', t='Hubble\'s law, Moore\'s law, inflation',
                      detail=dict(where='any scatter plot with a trend line, e.g. Excel\'s "Add trendline" or a regression in a research paper.',
                                  steps=['Hubble (1929): galaxy speed ∝ distance; the slope is the Hubble constant', 'Moore\'s law: fit a line to log(transistor count) against year (Lecture 24)', 'Economics: demand against price; the slope estimates elasticity', 'Always report $R^2$ and look at the residuals'],
                                  note='A trend line describes the data; it does not prove cause and effect.'))],
             notes="Both widget cards are fully interactive inside the pop-up."),
        dict(type='check', id='check', q='For the points $(0, 1)$, $(1, 3)$, $(2, 4)$, what is the slope $b$ of the least-squares line?',
             opts=['$1.5$', '$1.5\\overline{6}$', '$2$', '$1.25$'], right=0,
             answer='A. $n = 3$, $\\sum x = 3$, $\\sum y = 8$, $\\sum x^2 = 5$, $\\sum xy = 11$: $\\;b = \\dfrac{3(11) - 3(8)}{3(5) - 9} = \\dfrac{9}{6} = 1.5$, $\\;a = \\dfrac{8 - 4.5}{3} = 1.1\\overline{6}$.',
             notes="Option C (2) is the slope through the first two points only; D is a guess. Here the line through the end points happens to have the same slope 1.5, because the middle residual (+1/3) balances the two end residuals (−1/6 each)"),
        dict(type='summary', id='summary', items=[
            'Residual $e_i = y_i - \\hat y_i$; least squares minimises $S = \\sum e_i^2$',
            'Line: $na + b\\sum x = \\sum y$, $\\;a\\sum x + b\\sum x^2 = \\sum xy$',
            'Matrix form $A^{T}A\\mathbf{c} = A^{T}\\mathbf{y}$; any number of inputs; QR when ill-conditioned',
            'Judge with $R^2$, $s$ and the residual plot; beware outliers and extrapolation'],
            hw=['Fit $y = a + bx$ to $x$: 0, 1, 2, 3 and $y$: 1.1, 2.9, 5.2, 6.8. Find $S$ and $R^2$.', 'A spring: $F$ = 0, 1, 2, 3, 4 N, $L$ = 10.0, 10.9, 12.1, 13.0, 13.9 cm. Fit $L = L_0 + cF$ and find the length at 2.5 N.',
                'Show that the least-squares line passes through $(\\bar x, \\bar y)$ and that $\\sum e_i = 0$.', 'Write $A$, $A^{T}A$ and $A^{T}\\mathbf{y}$ for fitting $y = \\beta_0 + \\beta_1x_1 + \\beta_2x_2$ to four data points of your choice, and solve it in the lab.'],
            solved='Least squares gives $y = 8.20 + 3.13x$ ($R^2 = 0.998$), so a 15 km order takes about <b>55 minutes</b>, an extrapolation to be checked with new data. The degree-5 interpolant\'s 32.9 min at 13 km shows why we do not interpolate noisy data.',
            next='<b>Lecture 24: polynomial, exponential and trigonometric fitting.</b> Curved trends, growth laws, periodic data, and the danger of too many coefficients.',
            notes="Homework answers: Q1: Σx = 6, Σy = 16, Σx² = 14, Σxy = 33.7; y = 1.09 + 1.94x. Q2: L = 10.0 + 0.99F; L(2.5) = 12.475 cm. Q3: divide the first normal equation by n. Q4: any data; check with the lab."),
    ],
    code={
        'linreg': dict(file='linear_regression', py='''# Least-squares straight line y = a + b x
x = [2, 4, 5, 7, 9, 11]
y = [14, 21, 24, 30, 37, 42]
n = len(x)

Sx = Sy = Sxx = Sxy = 0.0
for xi, yi in zip(x, y):
    Sx += xi
    Sy += yi
    Sxx += xi * xi
    Sxy += xi * yi
print(f"sums: n = {n}, Sx = {Sx:.0f}, Sy = {Sy:.0f}, Sxx = {Sxx:.0f}, Sxy = {Sxy:.0f}")

D = n * Sxx - Sx * Sx
b = (n * Sxy - Sx * Sy) / D
a = (Sy - b * Sx) / n
print(f"a = {a:.6f}   b = {b:.6f}")

ybar = Sy / n
S = St = 0.0
for xi, yi in zip(x, y):
    e = yi - (a + b * xi)
    S += e * e
    St += (yi - ybar) ** 2
    print(f"x = {xi:2d}  y = {yi:2d}  fitted = {a + b * xi:7.3f}  residual = {e:7.3f}")
print(f"S = {S:.6f}   R^2 = {1 - S / St:.6f}")
print(f"prediction at 15 km: {a + b * 15:.2f} min")
''', c='''/* Least-squares straight line y = a + b x */
#include <stdio.h>
#define N 6

int main(void) {
    double x[N] = {2, 4, 5, 7, 9, 11}, y[N] = {14, 21, 24, 30, 37, 42};
    double Sx = 0, Sy = 0, Sxx = 0, Sxy = 0;
    for (int i = 0; i < N; i++) {
        Sx += x[i]; Sy += y[i];
        Sxx += x[i] * x[i]; Sxy += x[i] * y[i];
    }
    printf("sums: n = %d, Sx = %.0f, Sy = %.0f, Sxx = %.0f, Sxy = %.0f\\n", N, Sx, Sy, Sxx, Sxy);

    double D = N * Sxx - Sx * Sx;
    double b = (N * Sxy - Sx * Sy) / D;
    double a = (Sy - b * Sx) / N;
    printf("a = %.6f   b = %.6f\\n", a, b);

    double ybar = Sy / N, S = 0, St = 0;
    for (int i = 0; i < N; i++) {
        double e = y[i] - (a + b * x[i]);
        S += e * e;
        St += (y[i] - ybar) * (y[i] - ybar);
        printf("x = %2.0f  y = %2.0f  fitted = %7.3f  residual = %7.3f\\n", x[i], y[i], a + b * x[i], e);
    }
    printf("S = %.6f   R^2 = %.6f\\n", S, 1 - S / St);
    printf("prediction at 15 km: %.2f min\\n", a + b * 15);
    return 0;
}
'''),
        'multireg': dict(file='multiple_regression', py='''# Multiple regression y = b0 + b1*x1 + b2*x2 via the normal equations
x1 = [50, 70, 80, 100, 120]          # size (m^2)
x2 = [1, 2, 2, 3, 3]                 # rooms
y = [30, 42, 47, 60, 68]             # price (lakh Tk)
n, k = len(y), 3
A = [[1.0, x1[i], x2[i]] for i in range(n)]

# form M = A^T A and r = A^T y
M = [[sum(A[i][p] * A[i][q] for i in range(n)) for q in range(k)] for p in range(k)]
r = [sum(A[i][p] * y[i] for i in range(n)) for p in range(k)]
for p in range(k):
    print("[" + " ".join(f"{v:8.0f}" for v in M[p]) + " ] | " + f"{r[p]:6.0f}")

# Gaussian elimination with partial pivoting (Lecture 12)
for j in range(k):
    m = max(range(j, k), key=lambda i: abs(M[i][j]))
    M[j], M[m] = M[m], M[j]
    r[j], r[m] = r[m], r[j]
    for i in range(j + 1, k):
        f = M[i][j] / M[j][j]
        for q in range(j, k):
            M[i][q] -= f * M[j][q]
        r[i] -= f * r[j]
beta = [0.0] * k
for j in range(k - 1, -1, -1):
    s = r[j] - sum(M[j][q] * beta[q] for q in range(j + 1, k))
    beta[j] = s / M[j][j]
print(f"b0 = {beta[0]:.5f}  b1 = {beta[1]:.5f}  b2 = {beta[2]:.5f}")

S = sum((y[i] - sum(A[i][q] * beta[q] for q in range(k))) ** 2 for i in range(n))
print(f"S = {S:.6f}")
print(f"price of 90 m^2, 3 rooms: {beta[0] + 90 * beta[1] + 3 * beta[2]:.2f} lakh Tk")
''', c='''/* Multiple regression y = b0 + b1*x1 + b2*x2 via the normal equations */
#include <stdio.h>
#include <math.h>
#define N 5
#define K 3

int main(void) {
    double x1[N] = {50, 70, 80, 100, 120}, x2[N] = {1, 2, 2, 3, 3}, y[N] = {30, 42, 47, 60, 68};
    double A[N][K], M[K][K], r[K], beta[K];
    for (int i = 0; i < N; i++) { A[i][0] = 1; A[i][1] = x1[i]; A[i][2] = x2[i]; }

    for (int p = 0; p < K; p++) {               /* M = A^T A, r = A^T y */
        for (int q = 0; q < K; q++) {
            M[p][q] = 0;
            for (int i = 0; i < N; i++) M[p][q] += A[i][p] * A[i][q];
        }
        r[p] = 0;
        for (int i = 0; i < N; i++) r[p] += A[i][p] * y[i];
    }
    for (int p = 0; p < K; p++) {
        printf("[");
        for (int q = 0; q < K; q++) printf(" %8.0f", M[p][q]);
        printf(" ] | %6.0f\\n", r[p]);
    }

    for (int j = 0; j < K; j++) {               /* elimination with partial pivoting */
        int m = j;
        for (int i = j + 1; i < K; i++) if (fabs(M[i][j]) > fabs(M[m][j])) m = i;
        for (int q = 0; q < K; q++) { double t = M[j][q]; M[j][q] = M[m][q]; M[m][q] = t; }
        double t = r[j]; r[j] = r[m]; r[m] = t;
        for (int i = j + 1; i < K; i++) {
            double f = M[i][j] / M[j][j];
            for (int q = j; q < K; q++) M[i][q] -= f * M[j][q];
            r[i] -= f * r[j];
        }
    }
    for (int j = K - 1; j >= 0; j--) {
        double s = r[j];
        for (int q = j + 1; q < K; q++) s -= M[j][q] * beta[q];
        beta[j] = s / M[j][j];
    }
    printf("b0 = %.5f  b1 = %.5f  b2 = %.5f\\n", beta[0], beta[1], beta[2]);

    double S = 0;
    for (int i = 0; i < N; i++) {
        double e = y[i] - (beta[0] + beta[1] * x1[i] + beta[2] * x2[i]);
        S += e * e;
    }
    printf("S = %.6f\\n", S);
    printf("price of 90 m^2, 3 rooms: %.2f lakh Tk\\n", beta[0] + 90 * beta[1] + 3 * beta[2]);
    return 0;
}
'''),
    },
    lab=dict(title='Least Squares Lab',
             intro='Fit straight lines to your own data, see the residuals, and solve multiple regression problems through the normal equations.',
             tabs=[
                 dict(name='Line fit', blocks=[
                     dict(p='Type the x and y values (spaces or commas). The table lists fitted values and residuals; the note gives S, R² and the prediction.'),
                     dict(w='lsq', o=dict(x=DX, y=DY, models=['line'], at=15, height='320px', side=True, tableHeight='320px', presets=PRESETS + [['homework 1', '0 1 2 3', '1.1 2.9 5.2 6.8', 'line', 1, '']]))]),
                 dict(name='Normal equations', blocks=[
                     dict(p='Solve AᵀA c = Aᵀy for Problem 2 (house prices). AᵀA is symmetric positive definite, so Cholesky works; try Gaussian elimination too.'),
                     dict(w='linsys', o=dict(mat='5 420 11 247; 420 38200 1010 22360; 11 1010 27 592', mode='chol', modes=['chol', 'gauss', 'lu'], hint='[AᵀA | Aᵀy]'))]),
                 dict(name='Code', blocks=[
                     dict(h='Straight line'), dict(code='linreg', tasks=['Run it. Compare a, b, S with Problem 1.', 'Change the data to Problem 3 and check y = 0.8 + 2x.', 'Make the last y equal to 70: how much does the prediction at 15 km change?']),
                     dict(h='Multiple regression'), dict(code='multireg', tasks=['Run it. Compare with Problem 2.', 'Add a sixth flat (size 90, 3 rooms, price 56) and refit.', 'Replace x1 by the year 2015…2019 and look at the size of the entries of AᵀA.'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('What is the principle of least squares?', 'Choose the parameters of the model so that the sum of the squares of the residuals $S = \\sum (y_i - \\hat y_i)^2$ is as small as possible.'),
                         ('Write the normal equations for fitting $y = a + bx$.', '$na + b\\sum x = \\sum y$ and $a\\sum x + b\\sum x^2 = \\sum xy$.'),
                         ('How does least squares differ from interpolation?', 'Interpolation passes through every data point (as many coefficients as points); least squares uses fewer coefficients than points and passes close to them, smoothing the noise.'),
                         ('What does $R^2 = 0.95$ mean?', '95% of the variation of $y$ about its mean is explained by the model; it does not prove that the model is correct, so look at the residuals too.'),
                         ('Why can solving the normal equations be inaccurate?', 'cond($A^{T}A$) = cond($A$)², so nearly dependent columns (e.g. x = years) lose about twice as many digits; centre the data or use QR.')])])]),
)
