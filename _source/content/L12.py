PLATE_SVG = ('<svg viewBox="0 0 420 400" width="400" height="380" role="img" aria-label="Square plate with four interior grid points">'
             '<rect x="60" y="40" width="300" height="300" fill="#fbeee2" stroke="#16324f" stroke-width="4"/>'
             '<g stroke="#9fb3c8" stroke-width="2" stroke-dasharray="6 6"><line x1="160" y1="40" x2="160" y2="340"/><line x1="260" y1="40" x2="260" y2="340"/><line x1="60" y1="140" x2="360" y2="140"/><line x1="60" y1="240" x2="360" y2="240"/></g>'
             '<g fill="#a64f15"><circle cx="160" cy="140" r="11"/><circle cx="260" cy="140" r="11"/><circle cx="160" cy="240" r="11"/><circle cx="260" cy="240" r="11"/></g>'
             '<g font-family="IBM Plex Sans, sans-serif" font-size="24" font-weight="600" fill="#16324f">'
             '<text x="172" y="128">T₁</text><text x="272" y="128">T₂</text><text x="172" y="228">T₃</text><text x="272" y="228">T₄</text>'
             '<text x="210" y="28" text-anchor="middle" fill="#b3261e">top 100°</text><text x="210" y="376" text-anchor="middle" fill="#2f6db5">bottom 0°</text>'
             '<text x="372" y="196" fill="#b85712">50°</text><text x="12" y="196" fill="#2f6db5">0°</text></g></svg>')

LECTURE = dict(
    title='Gaussian and Gauss–Jordan Elimination',
    short='Gaussian and Gauss–Jordan Elimination',
    sub='The school method of eliminating unknowns, made systematic: forward elimination and back substitution, Gauss–Jordan and the inverse, the operation count, and partial pivoting to keep rounding errors under control.',
    slides=[
        dict(type='cover', id='cover', notes="Recap: Cramer's rule costs about e·(n + 1)! operations. Today's method costs about 2n³/3. Ask: for n = 20, how big is that difference? (1.4×10²⁰ against 5910.)\n\nThe idea is the one students used in school: eliminate one unknown at a time. What is new: doing it in a fixed order that a computer can follow, counting the work, and protecting it against rounding."),
        dict(type='bullets', id='hook', title='The problem: temperatures inside a metal plate', kick='Why this lecture', rw=520,
             lead='The edges of a square plate are held at fixed temperatures. What is the temperature at the four marked interior points?',
             items=['In steady heat flow, each interior temperature is the <b>average of its four neighbours</b>',
                    'Point 1: $T_1 = \\tfrac14(100 + 0 + T_2 + T_3)$, so $4T_1 - T_2 - T_3 = 100$',
                    'Four points give four linear equations; Cramer could manage this one',
                    'But engineers use a 100 × 100 grid: <b>10 000 unknowns</b>. We need a method whose work grows like $n^3$, not $n!$'],
             frag=True,
             right=dict(svg=PLATE_SVG, cap='Edges: 100° (top), 50° (right), 0° (bottom and left)'),
             notes="The averaging rule comes from the discrete Laplace equation (heat equation at steady state); students do not need the derivation now. It returns in Lecture 14, where the same rule becomes an iterative method.\n\nThe four equations: 4T1 − T2 − T3 = 100; −T1 + 4T2 − T4 = 150; −T1 + 4T3 − T4 = 0; −T2 − T3 + 4T4 = 50. Solved at the end: (43.75, 56.25, 18.75, 31.25)."),
        dict(type='goals', id='goals', items=[
            'Solve $A\\mathbf{x} = \\mathbf{b}$ by <b>Gaussian elimination</b> and back substitution',
            'Use <b>Gauss–Jordan</b> elimination, and find $A^{-1}$ from $[A \\mid I]$',
            'Count the operations: about $\\tfrac23 n^3$, compared with $n!$ for Cramer',
            'Explain why a small pivot ruins the answer, and fix it with <b>partial pivoting</b>',
            'Choose between elimination methods for a given problem'],
            prev='Cramer and the inverse: exact formulas, but the cost grows like $n!$.',
            today='Eliminate unknowns column by column; count the cost; add pivoting for safety.',
            notes="This is the most important algorithm of Module 3: LU (Lecture 13) is a reorganisation of it, and every library solver (NumPy, MATLAB, LAPACK) uses it."),
        dict(type='math', id='idea', title='The idea: reduce to a triangle, then solve upwards',
             eqs=[dict(cap='Elementary row operations do not change the solution', eq='R_i \\leftrightarrow R_j, \\qquad R_i \\leftarrow c\\,R_i \\;(c \\ne 0), \\qquad R_i \\leftarrow R_i - m\\,R_k'),
                  dict(cap='Forward elimination, column k: multiplier and row update', eq='m_{ik} = \\frac{a_{ik}}{a_{kk}}, \\qquad R_i \\leftarrow R_i - m_{ik}R_k \\quad (i = k+1, \\dots, n)', frag=True),
                  dict(cap='Back substitution on the triangular system', eq='x_n = \\frac{b_n}{a_{nn}}, \\qquad x_i = \\frac{1}{a_{ii}}\\Big(b_i - \\sum_{j=i+1}^{n} a_{ij}x_j\\Big)', frag=True)],
             items=['$a_{kk}$ is the <b>pivot</b>: it must not be zero', 'After column $k$, every entry below the pivot is 0', 'After $n - 1$ columns the matrix is upper triangular, $U$', 'The last equation has one unknown, the one above it two, and so on'],
             ifrag=True,
             notes="Stress that the operations act on whole rows of the augmented matrix, including b. Students often forget to update the last column.\n\nThe multiplier m_ik is worth writing down: in Lecture 13 the multipliers become the matrix L."),
        dict(type='bullets', id='algo', title='Gaussian elimination, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Write the augmented matrix $[A \\mid \\mathbf{b}]$', 'For column $k = 1, \\dots, n-1$: check the pivot $a_{kk} \\ne 0$', 'For each row $i$ below it: $m_{ik} = a_{ik}/a_{kk}$, then $R_i \\leftarrow R_i - m_{ik}R_k$',
                    'Now the system is upper triangular: $x_n = b_n/a_{nn}$', 'Back substitution: $x_i = (b_i - \\sum_{j>i} a_{ij}x_j)/a_{ii}$ for $i = n-1, \\dots, 1$; check by substituting'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input A (n×n), b\nfor k = 1 … n−1:              # forward\n    if a[k][k] = 0: stop (pivot)\n    for i = k+1 … n:\n        m ← a[i][k] / a[k][k]\n        for j = k … n:\n            a[i][j] ← a[i][j] − m·a[k][j]\n        b[i] ← b[i] − m·b[k]\nfor i = n … 1:                # backward\n    s ← b[i] − Σ_{j&gt;i} a[i][j]·x[j]\n    x[i] ← s / a[i][i]</pre></div><p class="small" style="margin-top:14px">Three nested loops in the forward part: that is where the $n^3$ comes from.</p>'),
             notes="Walk through the loops with the 3×3 example on the next slides. The 'stop (pivot)' line is a weakness we fix later today with pivoting."),
        dict(type='widget', id='explore', title='Explore: elimination, one row operation at a time', w='linsys', o=dict(mat='2 1 -1 8; -3 -1 2 -11; -2 1 2 -3', modes=['gauss', 'gj'], nodigits=True, height='300px',
             presets=[['Problem 1', '2 1 -1 8; -3 -1 2 -11; -2 1 2 -3', 'gauss', False], ['plate', '4 -1 -1 0 100; -1 4 0 -1 150; -1 0 4 -1 0; 0 -1 -1 4 50', 'gauss', False], ['zero pivot', '0 1 1 2; 1 1 1 3; 2 1 3 6', 'gauss', False]]), lw=480,
             items=['Each <b>Next step</b> is one row operation; the orange box is the pivot', 'Shaded row: the one that just changed', 'Faded zeros: entries already eliminated', 'Try the <b>plate</b> and the <b>zero pivot</b> presets'],
             notes="Step through Problem 1 with the class predicting each multiplier before you click. Then the plate (4×4): the zeros in the matrix stay zero for a while, a hint of the sparsity used in Lectures 13–14.\n\nThe zero pivot preset stops at step 1 with an explanation: that is the cliffhanger for the pivoting part of the lecture."),
        dict(type='worked', id='p1', title='Problem 1: three equations by Gaussian elimination',
             q='Solve $2x + y - z = 8$, $\\;-3x - y + 2z = -11$, $\\;-2x + y + 2z = -3$.',
             steps=['Column 1: $m_{21} = -3/2$, $m_{31} = -2/2 = -1$. $\\;R_2 \\leftarrow R_2 + 1.5R_1$, $R_3 \\leftarrow R_3 + R_1$: $\\;\\left(\\begin{array}{ccc|c} 2 & 1 & -1 & 8 \\\\ 0 & 0.5 & 0.5 & 1 \\\\ 0 & 2 & 1 & 5\\end{array}\\right)$',
                    'Column 2: $m_{32} = 2/0.5 = 4$. $\\;R_3 \\leftarrow R_3 - 4R_2$: $\\;\\left(\\begin{array}{ccc|c} 2 & 1 & -1 & 8 \\\\ 0 & 0.5 & 0.5 & 1 \\\\ 0 & 0 & -1 & 1\\end{array}\\right)$',
                    'Back substitution: $z = 1/(-1) = -1$; $\\;y = (1 - 0.5(-1))/0.5 = 3$; $\\;x = (8 - 3 - (-1)(-1))/2 = 2$'],
             answer='$x = 2$, $y = 3$, $z = -1$. Check eq. 2: $-6 - 3 - 2 = -11$ ✓',
             notes="Point out that m21 is negative: R2 − (−1.5)R1 = R2 + 1.5R1. Students who write the multiplier with the wrong sign get 0.5 → −2.5 in row 2.\n\nOperation count for this example: 28 (19 in elimination, 9 in back substitution)."),
        dict(type='bullets', id='gj', title='Gauss–Jordan elimination, step by step', kick='The method, step by step', ordered=True, rw=780,
             lead='Eliminate <b>above and below</b> each pivot and scale it to 1. The left part becomes $I$ and the right part is the answer.',
             items=['Write $[A \\mid \\mathbf{b}]$ (or $[A \\mid I]$ to get the inverse)', 'For column $k = 1, \\dots, n$: divide row $k$ by the pivot so that $a_{kk} = 1$', 'Clear column $k$ in <b>every other row</b>: $R_i \\leftarrow R_i - a_{ik}R_k$, for all $i \\ne k$',
                    'After column $n$: $[I \\mid \\mathbf{x}]$, so read off $\\mathbf{x}$ (no back substitution)', 'With $[A \\mid I]$ you end with $[I \\mid A^{-1}]$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input M = [A | B]   # B = b or I\nfor k = 1 … n:\n    if m[k][k] = 0: stop (pivot)\n    R_k ← R_k / m[k][k]\n    for i = 1 … n, i ≠ k:\n        R_i ← R_i − m[i][k]·R_k\nreturn right part of M</pre></div><p class="small" style="margin-top:14px">About $n^3$ operations: 50% more than Gaussian elimination, because it also clears the entries above the pivots.</p>'),
             notes="Gauss–Jordan on Problem 1 gives, after each column: [1, 0.5, −0.5 | 4; 0, 0.5, 0.5 | 1; 0, 2, 1 | 5], then [1, 0, −1 | 3; 0, 1, 1 | 2; 0, 0, −1 | 1], then [I | 2, 3, −1].\n\nUse: computing inverses, and reduced row echelon form (RREF) in theory and in the chemistry application."),
        dict(type='worked', id='p2', title='Problem 2: the inverse by Gauss–Jordan',
             q='Find $A^{-1}$ for $A = \\begin{pmatrix} 1 & 2 & 3 \\\\ 0 & 1 & 4 \\\\ 5 & 6 & 0\\end{pmatrix}$ by reducing $[A \\mid I]$.',
             steps=['Column 1 (pivot 1): $R_3 \\leftarrow R_3 - 5R_1$ gives row 3 $= (0, -4, -15 \\mid -5, 0, 1)$',
                    'Column 2 (pivot 1): $R_1 \\leftarrow R_1 - 2R_2$, $R_3 \\leftarrow R_3 + 4R_2$: rows $(1, 0, -5 \\mid 1, -2, 0)$ and $(0, 0, 1 \\mid -5, 4, 1)$',
                    'Column 3 (pivot 1): $R_1 \\leftarrow R_1 + 5R_3$, $R_2 \\leftarrow R_2 - 4R_3$'],
             answer='$A^{-1} = \\begin{pmatrix} -24 & 18 & 5 \\\\ 20 & -15 & -4 \\\\ -5 & 4 & 1\\end{pmatrix}$; check $AA^{-1} = I$.',
             right=dict(w='linsys', o=dict(mat='1 2 3; 0 1 4; 5 6 0', mode='inv', modes=['inv'], nodigits=True, nopivot=True, hint='Square matrix A (the tool appends I)')), rw=860,
             notes="All three pivots happen to be 1 here, so no division is needed: a good first example. det A = 1, which is why the inverse has integer entries.\n\nCompare with the adjugate method (Lecture 11): nine 2×2 cofactors and a transpose. Gauss–Jordan is the method computers use when an inverse is really needed."),
        dict(type='math', id='count', title='How much work? The operation count',
             eqs=[dict(cap='Column k: (n − k) rows, each 1 division and n − k + 1 multiply–subtract pairs', eq='\\sum_{k=1}^{n-1}(n-k)\\big(2(n-k) + 3\\big) + \\underbrace{n^2}_{\\text{back subst.}} = \\frac{2n^3}{3} + \\frac{3n^2}{2} - \\frac{7n}{6}'),
                  dict(cap='For large n only the first term matters', eq='\\begin{aligned} \\text{Gauss} &\\approx \\tfrac23 n^3 \\\\ \\text{Gauss–Jordan} &\\approx n^3 \\\\ \\text{Cramer} &\\approx e\\,(n+1)! \\end{aligned}', frag=True)],
             right=dict(table=[['$n$', 'Gauss: operations', 'time', 'matrix memory'], [['3', '28', '28 ns', '72 B'], ['100', '$6.8\\times10^5$', '0.7 ms', '80 KB'], ['1000', '$6.7\\times10^8$', '0.67 s', '8 MB'], ['10 000', '$6.7\\times10^{11}$', '11 min', '800 MB']]], frag=True), rw=760,
             notes="The sum: Σ j(2j + 3) for j = 1 … n − 1 = 2(n − 1)n(2n − 1)/6 + 3(n − 1)n/2. Check n = 3: 19 + 9 = 28.\n\nTimes at 10⁹ operations per second. Doubling n multiplies the work by 8: that cubic growth, and the n² memory, are why Lecture 14 needs iterative methods for 10⁶ unknowns."),
        dict(type='compare', id='classic', title='Same plate, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (Cramer\'s rule)', tag='Formula', cls='blue', items=['Five 4×4 determinants', '319 operations', '$T = (43.75, 56.25, 18.75, 31.25)$']),
             right=dict(h='Numerical (Gaussian elimination)', tag='Algorithm', cls='key', items=['Six row operations, then back substitution', '62 operations', '$T = (43.75, 56.25, 18.75, 31.25)$']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>A 10 × 10 grid of points: 100 unknowns</h3><p>Cramer\'s rule: about $2.6\\times10^{160}$ operations, far beyond any computer that could ever be built. Gaussian elimination: 681 550 operations, under a millisecond.</p></div>'),
             notes="Same answer, but one method scales and the other does not. The 100-unknown grid is still small for engineering; 10⁶ unknowns are routine in heat, fluid and structural simulation."),
        dict(type='widget', id='fail', title='The weakness: a tiny pivot destroys the answer', kick='Limitation shown failing', w='linsys',
             o=dict(mat='0.0001 1 1; 1 1 2', digits=3, modes=['gauss'], height='200px', presets=[['3 digits, no pivoting', '0.0001 1 1; 1 1 2', 'gauss', False, 3], ['3 digits, with pivoting', '0.0001 1 1; 1 1 2', 'gauss', True, 3], ['zero pivot', '0 1 1; 1 1 2', 'gauss', False, 0]]), lw=560,
             items=['$0.0001x + y = 1$, $\\;x + y = 2$: exact $x = 1.0001$, $y = 0.9999$', 'Pivot 0.0001, so $m_{21} = 10\\,000$: row 2 becomes $1 - 10\\,000 = -9999 \\to -10\\,000$ in 3 digits', 'Back substitution: $y = 1$, then $x = (1 - 1)/0.0001 = 0$. <b>Completely wrong</b>',
                    'In double precision the same happens with a pivot of $10^{-20}$: $x = 0$, $y = 1$'],
             frag=True,
             notes="Press All steps on the first preset: x = 0. The information in row 2 (x + y = 2) has been swamped by 10 000 × row 1. Then select the pivoting preset: x = 1, y = 1, correct to 3 digits.\n\nThe matrix is perfectly well-conditioned (κ∞ ≈ 4): the failure is caused by the algorithm, not by the problem. That distinction (Lecture 5) is the point of the slide."),
        dict(type='bullets', id='pivot', title='The fix: partial pivoting', kick='The method, step by step', ordered=True, rw=780,
             lead='Before eliminating column $k$, bring the <b>largest</b> $|a_{ik}|$ ($i \\ge k$) into the pivot position.',
             items=['For column $k$: find the row $p \\ge k$ with the largest $|a_{pk}|$', 'Swap $R_k \\leftrightarrow R_p$ (whole rows, including $\\mathbf{b}$)', 'Eliminate as before; now every $|m_{ik}| \\le 1$', 'If the largest $|a_{pk}|$ is 0, the matrix is singular: stop',
                    'Back substitution as before'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Added to the pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">for k = 1 … n−1:\n    p ← argmax_{i ≥ k} |a[i][k]|\n    if a[p][k] = 0: stop (singular)\n    swap rows k and p of [A | b]\n    for i = k+1 … n:\n        m ← a[i][k] / a[k][k]   # |m| ≤ 1\n        R_i ← R_i − m·R_k</pre></div><p class="small" style="margin-top:14px">Multipliers at most 1 in size keep rounding errors from growing. It costs only comparisons, no extra arithmetic.</p>'),
             notes="Partial pivoting is what every practical solver does (NumPy, MATLAB, LAPACK's dgesv). Full pivoting (searching rows and columns) is safer still but slower and rarely needed.\n\nScaled partial pivoting compares |a_ik| / (largest entry of row i); mention it if a textbook in your department uses it."),
        dict(type='table', id='p3', title='Problem 3: the same system with 3-digit arithmetic',
             q='Solve $0.0001x + y = 1$, $\\;x + y = 2$ keeping 3 significant digits after every operation, without and with pivoting.',
             head=['', 'Without pivoting', 'With partial pivoting'], tx=(0,), frag=True,
             rows=[['pivot row', '$0.0001x + y = 1$', 'swap: $x + y = 2$ first'], ['multiplier', '$m = 1/0.0001 = 10\\,000$', '$m = 0.0001/1 = 0.0001$'],
                   ['new row 2', '$-10\\,000\\,y = -10\\,000$', '$1.00\\,y = 1.00$'], ['$y$', '1.00', '1.00'], ['$x$', '$(1 - 1)/0.0001 = 0$', '$2 - 1 = 1.00$'],
                   ['error in $x$', '<b style="color:#b3261e">100%</b>', '<b style="color:#2e7d4f">0.01%</b>']],
             note='With pivoting, $1 - 0.0001 = 0.9999 \\to 1.00$ and $1 - 0.0002 \\to 1.00$: the rounding only touches digits that do not matter.',
             notes="Write both columns on the board side by side. The key line is 'new row 2': without pivoting, 1 − 10 000 = −9999 rounds to −10 000 and the information that the coefficient was 1 (not 0) is lost."),
        dict(type='code', id='code', title='Gaussian elimination with partial pivoting', code='gausspp', lw=560,
             items=['Works for any $n$: the matrix is a list of rows (C: a 2-D array)', 'Pivot search, row swap, elimination, back substitution', 'Prints the triangular system and the solution', 'Try the plate (lab task) and a singular matrix'],
             notes="Run both tabs. NumPy's np.linalg.solve(A, b) does exactly this (LAPACK dgesv: LU with partial pivoting), in compiled code.\n\nLab: the program 'pivotfail' shows the 10⁻²⁰ pivot failing in ordinary double precision without pivoting."),
        dict(type='exam', id='practice', src='Problem 4',
             q='"Solve by Gaussian elimination with partial pivoting: $2x + 3y - z = 5$, $\\;4x + 4y - 3z = 3$, $\\;-2x + 3y - z = 1$."',
             tips=['Column 1: largest $|a_{i1}|$ is 4 (row 2): swap $R_1 \\leftrightarrow R_2$. Then $m_{21} = 0.5$, $m_{31} = -0.5$', 'Column 2: entries 1 and 5 below the pivot: swap again so 5 is the pivot; $m_{32} = 0.2$',
                   'Triangular system $4x + 4y - 3z = 3$, $5y - 2.5z = 2.5$, $z = 3$', 'Back substitution: $z = 3$, $y = 2$, $x = 1$; check in an original equation and state every swap you made'],
             notes=""),
        dict(type='profile', id='profile', title='Gaussian elimination: method profile',
             best=['Dense systems up to a few thousand unknowns: $\\tfrac23 n^3$, under a second for $n = 1000$', 'With partial pivoting: reliable for almost every nonsingular matrix met in practice', 'Exact (up to rounding) in a fixed number of steps; no starting guess, no convergence question'],
             worst=['A zero or tiny pivot without pivoting: failure or garbage', 'Ill-conditioned $A$: pivoting cannot recover digits the problem itself loses', '$n = 10^6$: $6.7\\times10^{17}$ operations and 8 TB of memory'],
             suited=['One system with a dense matrix', 'Inside other algorithms: each Newton step for a system (Lecture 10), least squares (Lecture 23)', 'Gauss–Jordan: inverses, RREF, rank'],
             avoid=['The same $A$ with many right-hand sides (factor once: LU, Lecture 13)', 'Banded or tridiagonal matrices with the full algorithm (Thomas, Lecture 13)', 'Huge sparse systems (iterative methods, Lecture 14)'],
             verdict='Rule of thumb: <b>for one dense system, Gaussian elimination with partial pivoting is the default</b>; switch only when the matrix has special structure.',
             notes="'Almost every': there are artificial matrices where partial pivoting lets entries grow like 2^(n−1) (growth factor), but they essentially never appear in applications."),
        dict(type='table', id='compare', title='Comparative analysis: elimination methods', cls='tb sm',
             head=['Method', 'Operations', '$n = 1000$', 'Stable?', 'Gives $A^{-1}$?', 'Typical use'], tx=(0, 5), frag=True,
             rows=[['Cramer (cofactors)', '$e\\,(n+1)!$', 'impossible', 'no', 'via adjugate', '2×2, 3×3 by hand'], ['Gauss, no pivoting', '$\\tfrac23 n^3$', '0.67 s', '<span class="bad">no</span> (tiny pivots)', 'no', 'diagonally dominant or SPD matrices'],
                   ['Gauss, partial pivoting', '$\\tfrac23 n^3$ + comparisons', '0.67 s', '<span class="gr">yes</span> (in practice)', 'no', 'the default solver'], ['Gauss–Jordan', '$n^3$', '1.0 s', 'yes, with pivoting', '<span class="gr">yes</span>', 'inverses, RREF'],
                   ['Inverse, then $A^{-1}\\mathbf{b}$', '$2n^3$', '2.0 s', 'less accurate', 'yes', 'avoid for solving']],
             note='Without pivoting, elimination is still safe for diagonally dominant and for symmetric positive definite matrices: the pivots can never become small. Lecture 13 uses this.', notefrag=True,
             notes="Times at 10⁹ operations per second. The note prepares Cholesky (no pivoting needed) and the Thomas algorithm (Lecture 13)."),
        dict(type='bridge', id='bridge', lead='Elimination is the workhorse, but it treats every matrix as dense and every right-hand side as new.',
             keep=['$\\tfrac23 n^3$ operations, a fixed number of steps', 'Partial pivoting: multipliers $|m| \\le 1$', 'Gauss–Jordan for inverses and RREF', 'Works for any nonsingular matrix'],
             rows=[['Same $A$, many right-hand sides: repeats all the work', 'Keep the multipliers: $A = LU$, then $2n^2$ per new $\\mathbf{b}$', 13],
                   ['Symmetric positive definite $A$: half the work is wasted', 'Cholesky, $A = LL^T$: $\\tfrac13 n^3$', 13],
                   ['Tridiagonal $A$: almost all entries are 0', 'Thomas algorithm: $8n$ operations', 13],
                   ['$10^6$ unknowns: memory and $n^3$ time', 'Iterative methods: Jacobi, Gauss–Seidel, SOR', 14]],
             notes="Each row of this table is one section of Lecture 13 or 14."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see elimination at work inside a real computation.',
             items=[
                 dict(ic='🌡️', h='Heat in a metal plate', t='The opening problem, step by step',
                      detail=dict(where='steady-state heat simulation. Each interior grid point gives one equation (the average of its neighbours); elimination solves them all at once.',
                                  w='linsys', o=dict(mat='4 -1 -1 0 100; -1 4 0 -1 150; -1 0 4 -1 0; 0 -1 -1 4 50', modes=['gauss'], nodigits=True),
                                  note='Press All steps: $T = (43.75, 56.25, 18.75, 31.25)$. The point next to the hot top edge and the 50° right edge is warmest.')),
                 dict(ic='📉', h='A curve through data points', t='Fitting a parabola exactly through three points',
                      detail=dict(where='polynomial interpolation (Lecture 17). Requiring $p(x) = a + bx + cx^2$ to pass through $(1, 2)$, $(2, 3)$, $(3, 6)$ gives a 3×3 linear system.',
                                  eq='\\begin{pmatrix} 1 & 1 & 1 \\\\ 1 & 2 & 4 \\\\ 1 & 3 & 9\\end{pmatrix}\\begin{pmatrix} a \\\\ b \\\\ c\\end{pmatrix} = \\begin{pmatrix} 2 \\\\ 3 \\\\ 6\\end{pmatrix}',
                                  w='linsys', o=dict(mat='1 1 1 2; 1 2 4 3; 1 3 9 6', modes=['gauss'], nodigits=True),
                                  note='Solution $a = 3$, $b = -2$, $c = 1$: $p(x) = x^2 - 2x + 3$. Lecture 17 gives formulas that avoid solving this system.')),
                 dict(ic='⚗️', h='Balancing a chemical equation', t='Gauss–Jordan on a homogeneous system',
                      detail=dict(where='stoichiometry. For $a\\,\\mathrm{C_3H_8} + b\\,\\mathrm{O_2} \\to c\\,\\mathrm{CO_2} + d\\,\\mathrm{H_2O}$, each element gives one equation; set $a = 1$ and solve.',
                                  steps=['Carbon: $3a = c$; hydrogen: $8a = 2d$; oxygen: $2b = 2c + d$', 'With $a = 1$: $c = 3$, $d = 4$, then $2b = 6 + 4$, so $b = 5$', 'Balanced: $\\mathrm{C_3H_8} + 5\\,\\mathrm{O_2} \\to 3\\,\\mathrm{CO_2} + 4\\,\\mathrm{H_2O}$',
                                         'For large reaction networks, software reduces the element matrix to RREF by Gauss–Jordan to find all balanced combinations'],
                                  note='The system has a free variable (any multiple of a balanced equation is balanced): Gauss–Jordan reveals that directly.')),
                 dict(ic='🐍', h='numpy.linalg.solve', t='What happens when you call it',
                      detail=dict(where='NumPy, MATLAB and R. <code>np.linalg.solve(A, b)</code> calls LAPACK\'s <code>dgesv</code>, which is Gaussian elimination with partial pivoting, organised as an LU factorisation.',
                                  steps=['Factor: elimination with row swaps, storing the multipliers (PA = LU)', 'Forward substitution with L, back substitution with U', 'Blocked loops so the matrix stays in fast cache memory', 'A 1000 × 1000 system takes a few milliseconds on a laptop'],
                                  note='Today\'s algorithm, with Lecture 13\'s bookkeeping, is literally what runs.'))],
             notes="The plate and parabola cards have live elimination steppers in the pop-up."),
        dict(type='check', id='check', q='Eliminate $x$ from $3x + 6y = 9$, $\\;2x + 5y = 8$. What is the new second row?',
             opts=['$(0, \\; 1 \\mid 2)$', '$(0, \\; 9 \\mid 14)$', '$(0, \\; 1 \\mid -1)$', '$(0, \\; -1 \\mid 2)$'], right=0,
             answer='A. $m_{21} = 2/3$: $5 - \\tfrac23(6) = 1$ and $8 - \\tfrac23(9) = 2$. So $y = 2$ and $x = (9 - 12)/3 = -1$.',
             notes="Option B comes from adding instead of subtracting; option C from forgetting to update b."),
        dict(type='summary', id='summary', items=[
            'Forward elimination with multipliers $m_{ik} = a_{ik}/a_{kk}$, then back substitution',
            'Gauss–Jordan clears above and below: $[I \\mid \\mathbf{x}]$, or $[I \\mid A^{-1}]$ from $[A \\mid I]$',
            'Cost about $\\tfrac23 n^3$ (Gauss–Jordan $n^3$), compared with $e(n+1)!$ for Cramer',
            'Partial pivoting (largest pivot, $|m| \\le 1$) prevents small pivots from destroying the answer'],
            hw=['Solve $x + 2y + 3z = 14$, $\\;2x + 5y + 2z = 18$, $\\;3x + y + 5z = 20$ by Gaussian elimination.', 'Find the inverse of $\\begin{pmatrix} 2 & 1 & 1 \\\\ 1 & 3 & 2 \\\\ 1 & 0 & 0\\end{pmatrix}$ by Gauss–Jordan.',
                'Solve $0.00001x + y = 1$, $x + y = 2$ with 4-digit arithmetic, without and with partial pivoting. Check with the lab tool.', 'How long does Gaussian elimination take for $n = 5000$ at $10^9$ operations per second?'],
            solved='Elimination of the plate system gives $T_1 = 43.75°$, $T_2 = 56.25°$, $T_3 = 18.75°$, $T_4 = 31.25°$ in 62 operations. A 100 × 100 grid (10 000 unknowns) takes about 11 minutes this way: Lecture 14 does better.',
            next='<b>LU, Cholesky and tridiagonal systems.</b> Keep the multipliers and solve for many right-hand sides cheaply; exploit symmetry and sparsity.',
            notes="Homework answers: Q1: m21 = 2, m31 = 3, m32 = −5; triangular rows (1, 2, 3 | 14), (0, 1, −4 | −10), (0, 0, −24 | −72); x = (1, 2, 3). Q2: [[0, 0, 1], [−2, 1, 3], [3, −1, −5]]. Q3: without pivoting x = 0, y = 1 (wrong); with pivoting x = 1, y = 1 (exact: 1.00001, 0.99999). Q4: 8.34×10¹⁰ operations, about 83 s."),
    ],
    code={
        'gausspp': dict(file='gauss_pivot', py='''# Gaussian elimination with partial pivoting
A = [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]]
b = [8.0, -11.0, -3.0]
n = len(b)

for k in range(n - 1):
    p = max(range(k, n), key=lambda i: abs(A[i][k]))   # pivot row
    if A[p][k] == 0:
        raise SystemExit("matrix is singular")
    if p != k:
        A[k], A[p] = A[p], A[k]
        b[k], b[p] = b[p], b[k]
        print(f"swap rows {k+1} and {p+1}")
    for i in range(k + 1, n):
        m = A[i][k] / A[k][k]
        for j in range(k, n):
            A[i][j] -= m * A[k][j]
        b[i] -= m * b[k]

print("upper triangular system:")
for i in range(n):
    print(" ".join(f"{A[i][j]:9.4f}" for j in range(n)), "|", f"{b[i]:9.4f}")

x = [0.0] * n
for i in range(n - 1, -1, -1):                        # back substitution
    s = b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))
    x[i] = s / A[i][i]
for i in range(n):
    print(f"x{i+1} = {x[i]:.6f}")
''', c='''/* Gaussian elimination with partial pivoting */
#include <stdio.h>
#include <math.h>
#define N 3

int main(void) {
    double A[N][N] = {{2, 1, -1}, {-3, -1, 2}, {-2, 1, 2}};
    double b[N] = {8, -11, -3}, x[N];

    for (int k = 0; k < N - 1; k++) {
        int p = k;                                    /* pivot row */
        for (int i = k + 1; i < N; i++)
            if (fabs(A[i][k]) > fabs(A[p][k])) p = i;
        if (A[p][k] == 0) { printf("matrix is singular\\n"); return 1; }
        if (p != k) {
            for (int j = 0; j < N; j++) { double t = A[k][j]; A[k][j] = A[p][j]; A[p][j] = t; }
            double t = b[k]; b[k] = b[p]; b[p] = t;
            printf("swap rows %d and %d\\n", k + 1, p + 1);
        }
        for (int i = k + 1; i < N; i++) {
            double m = A[i][k] / A[k][k];
            for (int j = k; j < N; j++) A[i][j] -= m * A[k][j];
            b[i] -= m * b[k];
        }
    }
    printf("upper triangular system:\\n");
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) printf(j ? " %9.4f" : "%9.4f", A[i][j]);
        printf(" | %9.4f\\n", b[i]);
    }
    for (int i = N - 1; i >= 0; i--) {                /* back substitution */
        double s = b[i];
        for (int j = i + 1; j < N; j++) s -= A[i][j] * x[j];
        x[i] = s / A[i][i];
    }
    for (int i = 0; i < N; i++) printf("x%d = %.6f\\n", i + 1, x[i]);
    return 0;
}
'''),
        'pivotfail': dict(file='pivot_failure', py='''# A tiny pivot without pivoting, in ordinary double precision
#   eps*x + y = 1
#     x   + y = 2      exact solution: x = 1/(1 - eps) ~ 1, y ~ 1
eps = 1e-20

# without pivoting: use eps as the pivot
m = 1 / eps
a22 = 1 - m * 1
b2 = 2 - m * 1
y = b2 / a22
x = (1 - y) / eps
print(f"no pivoting:   x = {x:.6f}  y = {y:.6f}")

# with pivoting: swap the rows first, pivot = 1
m = eps / 1
a22 = 1 - m * 1
b2 = 1 - m * 2
y = b2 / a22
x = (2 - y) / 1
print(f"with pivoting: x = {x:.6f}  y = {y:.6f}")
''', c='''/* A tiny pivot without pivoting, in ordinary double precision
     eps*x + y = 1
       x   + y = 2      exact solution: x = 1/(1 - eps) ~ 1, y ~ 1 */
#include <stdio.h>

int main(void) {
    double eps = 1e-20, m, a22, b2, x, y;

    m = 1 / eps;                       /* without pivoting */
    a22 = 1 - m * 1;
    b2 = 2 - m * 1;
    y = b2 / a22;
    x = (1 - y) / eps;
    printf("no pivoting:   x = %.6f  y = %.6f\\n", x, y);

    m = eps / 1;                       /* with pivoting: rows swapped */
    a22 = 1 - m * 1;
    b2 = 1 - m * 2;
    y = b2 / a22;
    x = (2 - y) / 1;
    printf("with pivoting: x = %.6f  y = %.6f\\n", x, y);
    return 0;
}
'''),
    },
    lab=dict(title='Elimination Lab',
             intro='Step through Gaussian and Gauss–Jordan elimination on your own systems, see what pivoting and limited precision do, and write the solver in Python and C.',
             tabs=[
                 dict(name='Elimination stepper', blocks=[
                     dict(p='Type any system as [A | b], one row per line. Choose the method, then step through the row operations. Use it to check every line of a hand calculation.'),
                     dict(w='linsys', o=dict(mat='2 3 -1 5; 4 4 -3 3; -2 3 -1 1', modes=['gauss', 'gj', 'inv'], pivot=True, height='280px',
                                             presets=[['Problem 1', '2 1 -1 8; -3 -1 2 -11; -2 1 2 -3', 'gauss', False], ['Problem 4', '2 3 -1 5; 4 4 -3 3; -2 3 -1 1', 'gauss', True], ['plate', '4 -1 -1 0 100; -1 4 0 -1 150; -1 0 4 -1 0; 0 -1 -1 4 50', 'gauss', False], ['inverse', '1 2 3; 0 1 4; 5 6 0', 'inv', False], ['singular', '1 2 3 4; 2 4 6 8; 1 1 1 1', 'gauss', True]]))]),
                 dict(name='Pivoting and precision', blocks=[
                     dict(p='Set the arithmetic to 3 or 4 significant digits to imitate a calculator. Compare the answers with and without partial pivoting. The textbook 2×2 (exact answer x = 10, y = 1) gives x = −10 without pivoting in 4-digit arithmetic.'),
                     dict(w='linsys', o=dict(mat='0.0001 1 1; 1 1 2', modes=['gauss'], digits=3, height='220px',
                                             presets=[['Problem 3', '0.0001 1 1; 1 1 2', 'gauss', False, 3], ['homework 3', '0.00001 1 1; 1 1 2', 'gauss', False, 4], ['textbook 2×2', '0.003 59.14 59.17; 5.291 -6.13 46.78', 'gauss', False, 4]]))]),
                 dict(name='Cost', blocks=[
                     dict(p='Operation counts: elimination against Gauss–Jordan, the inverse and Cramer.'),
                     dict(w='cost', o=dict(n=1000, methods=['cramer', 'inv', 'gj', 'gauss'], height='320px'))]),
                 dict(name='Code', blocks=[
                     dict(h='Gaussian elimination with partial pivoting'), dict(code='gausspp', tasks=['Run it. Which rows are swapped?', 'Solve the plate system (n = 4): change A, b and N.', 'Make A singular (row 3 = row 1 + row 2). What happens?']),
                     dict(h='A tiny pivot in double precision'), dict(code='pivotfail', tasks=['Run it. Which answer is right?', 'Try eps = 1e-10 and 1e-15. When does the version without pivoting start to fail?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Solve $x + 2y + 3z = 14$, $2x + 5y + 2z = 18$, $3x + y + 5z = 20$ by Gaussian elimination.', '$m_{21} = 2$, $m_{31} = 3$: rows $(0, 1, -4 \\mid -10)$, $(0, -5, -4 \\mid -22)$. $m_{32} = -5$: $(0, 0, -24 \\mid -72)$. So $z = 3$, $y = -10 + 12 = 2$, $x = 14 - 4 - 9 = 1$.'),
                         ('Find the inverse of $\\begin{pmatrix} 2 & 1 & 1 \\\\ 1 & 3 & 2 \\\\ 1 & 0 & 0\\end{pmatrix}$ by Gauss–Jordan.', '$A^{-1} = \\begin{pmatrix} 0 & 0 & 1 \\\\ -2 & 1 & 3 \\\\ 3 & -1 & -5\\end{pmatrix}$ (det $A = -1$). Check $AA^{-1} = I$.'),
                         ('What is partial pivoting and why is it needed?', 'Before eliminating column $k$, swap rows so that the entry of largest absolute value in column $k$ (rows $k$ to $n$) becomes the pivot. Then all multipliers satisfy $|m| \\le 1$, so rounding errors are not magnified; a tiny pivot (like 0.0001) would otherwise give multipliers like 10 000 and destroy the answer.'),
                         ('Show that Gaussian elimination needs about $\\tfrac23 n^3$ operations.', 'Column $k$: $n - k$ rows, each needs about $2(n - k)$ operations, so about $\\sum_{k} 2(n-k)^2 \\approx 2 \\cdot n^3/3$. Back substitution adds only $n^2$.'),
                         ('Compare Gaussian elimination and Gauss–Jordan elimination.', 'Gauss: zeros below the pivots, then back substitution; about $\\tfrac23 n^3$. Gauss–Jordan: zeros above and below, pivots scaled to 1, no back substitution; about $n^3$. Gauss–Jordan is convenient for inverses and RREF; Gauss is cheaper for solving.')])])]),
)
