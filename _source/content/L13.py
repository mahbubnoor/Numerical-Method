LECTURE = dict(
    title='LU, Cholesky and Tridiagonal Systems',
    short='LU, Cholesky and Tridiagonal Systems',
    sub='Elimination done once and reused: LU factorisation (Doolittle and Crout) for many right-hand sides, Cholesky for symmetric positive definite matrices at half the cost, and the Thomas algorithm that solves tridiagonal systems in linear time.',
    slides=[
        dict(type='cover', id='cover', notes="Recap question: 'In Gaussian elimination, which numbers did we compute and then throw away?' (The multipliers m_ik.) Today we keep them, and that small change gives LU.\n\nThen two special structures that appear everywhere: symmetric positive definite matrices (Cholesky) and tridiagonal matrices (Thomas)."),
        dict(type='bullets', id='hook', title='The problem: same plate, a new temperature every minute', kick='Why this lecture', rw=720,
             lead='The top edge of the plate from Lecture 12 is heated and cooled during the day. The matrix $A$ never changes; only the right-hand side $\\mathbf{b}$ does.',
             items=['One reading per minute for a day: <b>1440 right-hand sides</b>, one matrix', 'Gaussian elimination repeats the $\\tfrac23 n^3$ elimination every time, although $A$ is the same',
                    'A realistic model with $n = 1000$ unknowns: $1440 \\times 0.67$ s = <b>16 minutes</b>', 'Can we do the expensive part once and reuse it?'],
             frag=True,
             right=dict(table=[['top edge', '$T_1$', '$T_2$', '$T_3$', '$T_4$'], [['100°', '43.75', '56.25', '18.75', '31.25'], ['80°', '?', '?', '?', '?'], ['60°', '?', '?', '?', '?']]]),
             notes="The table on the right is filled in at the end of the lecture using a single LU factorisation (summary slide).\n\nThe elimination steps depend only on A: the multipliers and the triangular U are the same for every b. Only the operations on b differ. That observation is the whole idea of LU."),
        dict(type='goals', id='goals', items=[
            'Explain why Gaussian elimination is a <b>factorisation</b> $A = LU$',
            'Compute $L$ and $U$ by <b>Doolittle</b> and <b>Crout</b>, and solve with forward and back substitution',
            'Recognise <b>symmetric positive definite</b> matrices and factor them by <b>Cholesky</b>, $A = LL^T$',
            'Solve <b>tridiagonal</b> systems with the Thomas algorithm in $O(n)$ operations',
            'Choose the cheapest safe solver for a given matrix'],
            prev='Gaussian elimination with partial pivoting: $\\tfrac23 n^3$ for each system.',
            today='Factor once, solve many times; exploit symmetry and zeros.',
            notes="All three methods are Gaussian elimination in disguise: the skill is recognising when a cheaper version applies."),
        dict(type='math', id='idea', title='The idea: elimination is a factorisation',
             eqs=[dict(cap='Keep the multipliers in L; the eliminated matrix is U', eq='\\underbrace{\\begin{pmatrix} 2 & 1 & 1 \\\\ 4 & 3 & 3 \\\\ 8 & 7 & 9\\end{pmatrix}}_{A} = \\underbrace{\\begin{pmatrix} 1 & 0 & 0 \\\\ 2 & 1 & 0 \\\\ 4 & 3 & 1\\end{pmatrix}}_{L \\text{ (multipliers)}}\\underbrace{\\begin{pmatrix} 2 & 1 & 1 \\\\ 0 & 1 & 1 \\\\ 0 & 0 & 2\\end{pmatrix}}_{U}'),
                  dict(cap='Then Ax = b splits into two triangular solves', eq='L\\mathbf{y} = \\mathbf{b} \\;\\;(\\text{forward}), \\qquad U\\mathbf{x} = \\mathbf{y} \\;\\;(\\text{backward})', frag=True)],
             items=['$l_{ik} = m_{ik}$: exactly the multipliers of Lecture 12', 'Factor once: $\\tfrac23 n^3$ operations', 'Each new $\\mathbf{b}$: two triangular solves, $2n^2$ operations', '$n = 1000$: 2 ms per right-hand side instead of 0.67 s'],
             ifrag=True,
             notes="Check one entry on the board: row 3 of LU = 4·(2, 1, 1) + 3·(0, 1, 1) + 1·(0, 0, 2) = (8, 7, 9). ✓\n\nForward substitution is back substitution upside down: y1 first, then y2, and so on. Because L has ones on its diagonal there are no divisions."),
        dict(type='bullets', id='algo', title="Doolittle's LU method, step by step", kick='The method, step by step', ordered=True, rw=860,
             lead='Doolittle: $L$ has ones on its diagonal. Compute row $i$ of $U$, then column $i$ of $L$, for $i = 1, 2, \\dots, n$.',
             items=['Row $i$ of $U$: $\\;u_{ij} = a_{ij} - \\sum_{k<i} l_{ik}u_{kj}$ for $j \\ge i$', 'Column $i$ of $L$: $\\;l_{ji} = \\big(a_{ji} - \\sum_{k<i} l_{jk}u_{ki}\\big)/u_{ii}$ for $j > i$ (needs $u_{ii} \\ne 0$)',
                    'Forward: $y_i = b_i - \\sum_{k<i} l_{ik}y_k$', 'Backward: $x_i = \\big(y_i - \\sum_{k>i} u_{ik}x_k\\big)/u_{ii}$', 'For another $\\mathbf{b}$, repeat only steps 3 and 4'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 21px/1.5 var(--mono);color:#f5f3ee">for i = 1 … n:              # factor once\n    for j = i … n:\n        u[i][j] ← a[i][j] − Σ_{k&lt;i} l[i][k]·u[k][j]\n    l[i][i] ← 1\n    for j = i+1 … n:\n        l[j][i] ← (a[j][i] − Σ_{k&lt;i} l[j][k]·u[k][i]) / u[i][i]\nfor each right-hand side b:   # solve often\n    y ← forward(L, b)\n    x ← backward(U, y)</pre></div><p class="small" style="margin-top:14px">Same operations as elimination, organised so that each entry of $L$ and $U$ is computed once.</p>'),
             notes="The formulas come from multiplying out LU = A entry by entry and solving for the one unknown entry each time. Students who prefer elimination can instead do Gaussian elimination and record the multipliers: both give the same L and U.\n\nWithout pivoting this needs every u_ii ≠ 0; with pivoting we factor PA = LU (the widget shows P)."),
        dict(type='worked', id='p1', title='Problem 1: Doolittle LU, then solve',
             q='Factor $A = \\begin{pmatrix} 2 & 1 & 1 \\\\ 4 & 3 & 3 \\\\ 8 & 7 & 9\\end{pmatrix}$ as $LU$ and solve $A\\mathbf{x} = (3, 7, 19)^T$.',
             steps=['Row 1 of $U$: $(2, 1, 1)$. Column 1 of $L$: $l_{21} = 4/2 = 2$, $l_{31} = 8/2 = 4$',
                    '$u_{22} = 3 - 2(1) = 1$, $u_{23} = 3 - 2(1) = 1$; $\\;l_{32} = (7 - 4(1))/1 = 3$; $\\;u_{33} = 9 - 4(1) - 3(1) = 2$',
                    'Forward $L\\mathbf{y} = \\mathbf{b}$: $y_1 = 3$, $y_2 = 7 - 2(3) = 1$, $y_3 = 19 - 4(3) - 3(1) = 4$',
                    'Backward $U\\mathbf{x} = \\mathbf{y}$: $x_3 = 4/2 = 2$, $x_2 = 1 - 2 = -1$, $x_1 = (3 - (-1) - 2)/2 = 1$'],
             answer='$L = \\begin{pmatrix} 1 & 0 & 0 \\\\ 2 & 1 & 0 \\\\ 4 & 3 & 1\\end{pmatrix}$, $U = \\begin{pmatrix} 2 & 1 & 1 \\\\ 0 & 1 & 1 \\\\ 0 & 0 & 2\\end{pmatrix}$, $\\mathbf{x} = (1, -1, 2)$.',
             right=dict(w='linsys', o=dict(mat='2 1 1 3; 4 3 3 7; 8 7 9 19', mode='lu', modes=['lu'], nodigits=True, hint='[A | b]: L and U fill in step by step')), rw=820,
             notes="Ask: if b changes to (1, 2, 3), what must be redone? Only the two substitutions: y = (1, 0, −1), x = (0.75, 0.5, −0.5). Students can check with the widget by editing b."),
        dict(type='compare', id='crout', title='Doolittle or Crout? Where the ones go', mid='',
             left=dict(h='Doolittle: $l_{ii} = 1$', tag='Ones on the diagonal of L', cls='blue', eq='\\begin{pmatrix} 1 & 0 & 0 \\\\ 2 & 1 & 0 \\\\ 4 & 3 & 1\\end{pmatrix}\\begin{pmatrix} 2 & 1 & 1 \\\\ 0 & 1 & 1 \\\\ 0 & 0 & 2\\end{pmatrix}',
                       items=['$U$ = the matrix left by Gaussian elimination', 'Rows of $U$ first, then columns of $L$']),
             right=dict(h='Crout: $u_{ii} = 1$', tag='Ones on the diagonal of U', cls='key', eq='\\begin{pmatrix} 2 & 0 & 0 \\\\ 4 & 1 & 0 \\\\ 8 & 3 & 2\\end{pmatrix}\\begin{pmatrix} 1 & 0.5 & 0.5 \\\\ 0 & 1 & 1 \\\\ 0 & 0 & 1\\end{pmatrix}',
                        items=['$l_{ij} = a_{ij} - \\sum_{k<j} l_{ik}u_{kj}$ (column of $L$ first)', '$u_{ij} = (a_{ij} - \\sum_{k<i} l_{ik}u_{kj})/l_{ii}$ (then row of $U$)']),
             below=dict(html='<p class="small" style="margin-top:20px">Both cost the same and solve the same way. Crout\'s $L$ is Doolittle\'s $L$ with each column multiplied by the pivot; Crout\'s $U$ is Doolittle\'s $U$ with each row divided by it. A problem that names a method expects that placement of the ones.</p>'),
             notes="Crout for this matrix: column 1 of L = (2, 4, 8); row 1 of U = (1, 1/2, 1/2); l22 = 3 − 4(1/2) = 1, l32 = 7 − 8(1/2) = 3; u23 = (3 − 4(1/2))/1 = 1; l33 = 9 − 8(1/2) − 3(1) = 2."),
        dict(type='math', id='chol', title='Symmetric positive definite matrices and Cholesky',
             eqs=[dict(cap='Symmetric positive definite (SPD)', eq='A = A^T \\quad\\text{and}\\quad \\mathbf{x}^T A\\mathbf{x} > 0 \\;\\text{ for every } \\mathbf{x} \\ne \\mathbf{0}'),
                  dict(cap='Then A has a "square root" factorisation', eq='A = LL^T: \\quad l_{jj} = \\sqrt{a_{jj} - \\sum_{k<j} l_{jk}^2}, \\quad l_{ij} = \\frac{a_{ij} - \\sum_{k<j} l_{ik}l_{jk}}{l_{jj}}', frag=True)],
             items=['Where SPD matrices come from: energies, covariance matrices, least squares $A^TA$ (Lecture 23), the plate and circuit matrices', 'Quick test: symmetric, positive diagonal, all pivots (or all $l_{jj}^2$) positive',
                    'Only one triangle is computed: $\\tfrac13 n^3$ operations, <b>half of LU</b>', 'No pivoting needed: the square roots are of positive numbers and stay well-behaved'],
             ifrag=True,
             notes="Cholesky is also the cheapest test for positive definiteness: try the factorisation; if a number under a square root is ≤ 0, the matrix is not SPD.\n\nThe circuit matrix of Lecture 11 and the plate matrix of Lecture 12 are both SPD."),
        dict(type='bullets', id='algo2', title='Cholesky, step by step', kick='The method, step by step', ordered=True, rw=860,
             items=['Check $A = A^T$', 'For column $j = 1, \\dots, n$: $\\;l_{jj} = \\sqrt{a_{jj} - \\sum_{k<j} l_{jk}^2}$; if the number under the root is $\\le 0$, stop: not SPD',
                    'Below it: $l_{ij} = \\big(a_{ij} - \\sum_{k<j} l_{ik}l_{jk}\\big)/l_{jj}$ for $i > j$', 'Forward: $L\\mathbf{y} = \\mathbf{b}$', 'Backward: $L^T\\mathbf{x} = \\mathbf{y}$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 21px/1.55 var(--mono);color:#f5f3ee">for j = 1 … n:\n    s ← a[j][j] − Σ_{k&lt;j} l[j][k]²\n    if s ≤ 0: stop (not SPD)\n    l[j][j] ← √s\n    for i = j+1 … n:\n        l[i][j] ← (a[i][j] − Σ_{k&lt;j} l[i][k]·l[j][k]) / l[j][j]\ny ← forward(L, b)\nx ← backward(Lᵀ, y)</pre></div><p class="small" style="margin-top:14px">$n$ square roots, about $\\tfrac13 n^3$ other operations.</p>'),
             notes="Step 2 doubles as the SPD test. Students should state 'A is symmetric' explicitly in a written answer before starting."),
        dict(type='worked', id='p2', title='Problem 2: Cholesky factorisation',
             q='Factor $A = \\begin{pmatrix} 4 & 2 & -2 \\\\ 2 & 10 & 2 \\\\ -2 & 2 & 6\\end{pmatrix}$ as $LL^T$ and solve $A\\mathbf{x} = (-2, -4, 8)^T$.',
             steps=['$A$ is symmetric. Column 1: $l_{11} = \\sqrt4 = 2$, $l_{21} = 2/2 = 1$, $l_{31} = -2/2 = -1$',
                    'Column 2: $l_{22} = \\sqrt{10 - 1^2} = 3$, $l_{32} = (2 - (-1)(1))/3 = 1$; $\\;$column 3: $l_{33} = \\sqrt{6 - 1 - 1} = 2$',
                    'Forward $L\\mathbf{y} = \\mathbf{b}$: $y_1 = -2/2 = -1$, $y_2 = (-4 - 1(-1))/3 = -1$, $y_3 = (8 - (-1)(-1) - 1(-1))/2 = 4$',
                    'Backward $L^T\\mathbf{x} = \\mathbf{y}$: $x_3 = 4/2 = 2$, $x_2 = (-1 - 1(2))/3 = -1$, $x_1 = (-1 - 1(-1) - (-1)(2))/2 = 1$'],
             answer='$\\mathbf{x} = (1, -1, 2)$. Every square root was of a positive number, so $A$ is SPD.',
             right=dict(w='linsys', o=dict(mat='4 2 -2 -2; 2 10 2 -4; -2 2 6 8', mode='chol', modes=['chol'], nodigits=True, nopivot=True, hint='[A | b] with A symmetric')), rw=780,
             notes="Change a33 from 6 to 1 in the widget: the number under the last square root becomes 1 − 1 − 1 = −1, so the matrix is not positive definite and Cholesky stops."),
        dict(type='math', id='tri', title='Tridiagonal systems',
             eqs=[dict(cap='Only three diagonals are nonzero', eq='\\begin{pmatrix} b_1 & c_1 & & \\\\ a_2 & b_2 & c_2 & \\\\ & \\ddots & \\ddots & \\ddots \\\\ & & a_n & b_n\\end{pmatrix}\\begin{pmatrix} x_1 \\\\ x_2 \\\\ \\vdots \\\\ x_n\\end{pmatrix} = \\begin{pmatrix} d_1 \\\\ d_2 \\\\ \\vdots \\\\ d_n\\end{pmatrix}'),
                  dict(cap='Elimination touches only one entry per row (Thomas algorithm)', eq='\\begin{aligned} c\'_1 &= \\frac{c_1}{b_1}, & d\'_1 &= \\frac{d_1}{b_1} \\\\ c\'_i &= \\frac{c_i}{b_i - a_i c\'_{i-1}}, & d\'_i &= \\frac{d_i - a_i d\'_{i-1}}{b_i - a_i c\'_{i-1}} \\\\ x_n &= d\'_n, & x_i &= d\'_i - c\'_i\\,x_{i+1} \\end{aligned}', frag=True)],
             items=['Where they come from: heat in a rod, cubic splines (Lecture 18), implicit ODE methods', 'Store three vectors, not $n^2$ numbers', 'Cost $8n - 7$ operations instead of $\\tfrac23 n^3$', 'Safe without pivoting when $|b_i| > |a_i| + |c_i|$ (diagonally dominant)'],
             ifrag=True,
             notes="Derive on the board: in row i, the only entry below the diagonal is a_i, and eliminating it changes only b_i and d_i. Dividing each row by its new pivot gives the primed quantities.\n\nOperation count: 2 + 5(n − 1) + (n − 2) + 2(n − 1) = 8n − 7."),
        dict(type='bullets', id='algo3', title='The Thomas algorithm, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Store the sub-, main and super-diagonals $a_i$, $b_i$, $c_i$ and the right side $d_i$', 'Start: $c\'_1 = c_1/b_1$, $d\'_1 = d_1/b_1$', 'Sweep down $i = 2, \\dots, n$: $\\;w = b_i - a_i c\'_{i-1}$, $\\;c\'_i = c_i/w$, $\\;d\'_i = (d_i - a_i d\'_{i-1})/w$',
                    'Sweep up: $x_n = d\'_n$, then $x_i = d\'_i - c\'_i x_{i+1}$ for $i = n-1, \\dots, 1$', 'Check one equation'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input a, b, c, d (length n)\nc′[1] ← c[1]/b[1];  d′[1] ← d[1]/b[1]\nfor i = 2 … n:            # down\n    w ← b[i] − a[i]·c′[i−1]\n    if w = 0: stop\n    c′[i] ← c[i]/w\n    d′[i] ← (d[i] − a[i]·d′[i−1])/w\nx[n] ← d′[n]\nfor i = n−1 … 1:          # up\n    x[i] ← d′[i] − c′[i]·x[i+1]</pre></div><p class="small" style="margin-top:14px">Two loops, no nested loop: the work grows like $n$.</p>'),
             notes="This is Gaussian elimination (down sweep) and back substitution (up sweep) with all the zero arithmetic removed. It is also LU for a tridiagonal matrix: L and U are bidiagonal."),
        dict(type='table', id='p3', title='Problem 3: heat in a rod by the Thomas algorithm',
             q='A rod has ends at 100° and 0°; four interior points satisfy $-T_{i-1} + 2T_i - T_{i+1} = 0$. So $2T_1 - T_2 = 100$, $-T_1 + 2T_2 - T_3 = 0$, $-T_2 + 2T_3 - T_4 = 0$, $-T_3 + 2T_4 = 0$.',
             head=['$i$', '$a_i$', '$b_i$', '$c_i$', '$d_i$', '$w = b_i - a_ic\'_{i-1}$', '$c\'_i$', '$d\'_i$', '$T_i$'], frag=True,
             rows=[[1, '—', '2', '−1', '100', '2', '−0.5', '50', '80'], [2, '−1', '2', '−1', '0', '1.5', '−0.666667', '33.333333', '60'],
                   [3, '−1', '2', '−1', '0', '1.333333', '−0.75', '25', '40'], [4, '−1', '2', '—', '0', '1.25', '—', '20', '20']],
             note='Down sweep fills $c\'$ and $d\'$; up sweep: $T_4 = 20$, $T_3 = 25 + 0.75(20) = 40$, $T_2 = 33.33 + 0.6667(40) = 60$, $T_1 = 50 + 0.5(60) = 80$. A straight line from 100° to 0°, as physics predicts.',
             notes="Row 2 in full: w = 2 − (−1)(−0.5) = 1.5; c′ = −1/1.5 = −0.666667; d′ = (0 − (−1)(50))/1.5 = 33.333333.\n\nWith a heat source along the rod the right-hand side becomes nonzero and the profile curves; that is a lab task."),
        dict(type='compare', id='classic', title='Same problems, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (inverse matrix)', tag='Formula', cls='blue', items=['Compute $A^{-1}$ once ($2n^3$), then $\\mathbf{x} = A^{-1}\\mathbf{b}$ ($2n^2$) per reading', 'Plate, 3 readings: same temperatures', 'Tridiagonal $A$: $A^{-1}$ is <b>full</b>, so the zeros are lost']),
             right=dict(h='Numerical (LU, Thomas)', tag='Algorithm', cls='key', items=['Factor once ($\\tfrac23 n^3$), then $2n^2$ per reading: three times cheaper, more accurate', 'Plate, 3 readings: one factorisation, three pairs of substitutions', 'Tridiagonal $A$: Thomas keeps the zeros, $8n$ operations']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>A rod with a million grid points</h3><p>A full matrix of $10^6 \\times 10^6$ doubles needs 8 TB of memory, and dense elimination $6.7\\times10^{17}$ operations (21 years at $10^9$ per second). The Thomas algorithm: $8\\times10^6$ operations (8 ms) and four vectors (32 MB).</p></div>'),
             notes="Even the inverse of a tridiagonal matrix is full: try it in the lab with the inverse tool. Never invert a sparse matrix."),
        dict(type='code', id='code', title='LU once, many right-hand sides', code='lu3rhs', lw=560,
             items=['Doolittle factorisation of the plate matrix ($4\\times4$)', 'Then three right-hand sides: top edge 100°, 80°, 60°', 'Each solve is a forward and a backward substitution', 'The factorisation loop runs once'],
             notes="Run both tabs. The output fills in the table from the opening slide.\n\nIn SciPy: lu, piv = scipy.linalg.lu_factor(A); then scipy.linalg.lu_solve((lu, piv), b) for each b."),
        dict(type='code', id='code2', title='The Thomas algorithm in Python and C', code='thomas', lw=560,
             items=['Three diagonals and $d$ stored as vectors', 'Down sweep: $c\'$ and $d\'$; up sweep: $x$', 'Change $n$ to 9 or 99: the code is unchanged', 'Lab: add a heat source (nonzero $d_i$)'],
             notes="With n = 99 interior points the answer is still a straight line from 100 to 0: T_i = 100(1 − i/100)."),
        dict(type='widget', id='fail', title='Limitations shown failing', kick='When the factorisations break', w='linsys',
             o=dict(mat='0 1 1; 1 1 2', mode='lu', modes=['lu', 'chol'], nodigits=True, height='240px',
                    presets=[['LU: zero pivot', '0 1 1; 1 1 2', 'lu', False], ['LU with pivoting', '0 1 1; 1 1 2', 'lu', True], ['Cholesky: not SPD', '1 2 3; 2 1 3', 'chol', False], ['Cholesky: SPD', '2 1 3; 1 2 3', 'chol', False]]), lw=560,
             items=['<b>LU without pivoting</b>: $\\begin{pmatrix} 0 & 1 \\\\ 1 & 1\\end{pmatrix}$ has no $LU$ at all ($u_{11} = 0$); with row swaps $PA = LU$ works', '<b>Cholesky</b> on $\\begin{pmatrix} 1 & 2 \\\\ 2 & 1\\end{pmatrix}$: $l_{22} = \\sqrt{1 - 4}$, not SPD', '<b>Thomas</b> without diagonal dominance can meet $w = 0$, just like a zero pivot', 'None of them helps when $A$ is ill-conditioned: the factors inherit $\\kappa(A)$'],
             frag=True,
             notes="Click through the four presets. The symmetric matrix [[1, 2], [2, 1]] has eigenvalues 3 and −1, so it is not positive definite even though its entries are positive.\n\nThomas fails, for example, on the matrix with rows (1, 1, 0), (1, 1, 1), (0, 1, 1): w = 1 − 1·1 = 0 at row 2."),
        dict(type='exam', id='practice', src='Problem 4',
             q='"Factorise $A = \\begin{pmatrix} 1 & 1 & 1 \\\\ 4 & 3 & -1 \\\\ 3 & 5 & 3\\end{pmatrix}$ as $LU$ by Doolittle\'s method and solve $A\\mathbf{x} = (1, 6, 4)^T$."',
             tips=['State the form: $L$ unit lower triangular, $U$ upper triangular', 'Row 1 of $U$ = $(1, 1, 1)$; $l_{21} = 4$, $l_{31} = 3$; then $u_{22} = -1$, $u_{23} = -5$, $l_{32} = -2$, $u_{33} = -10$',
                   'Forward: $\\mathbf{y} = (1, 2, 5)$; backward: $x_3 = -\\tfrac12$, $x_2 = \\tfrac12$, $x_1 = 1$', 'Verify $LU = A$ (one row is enough) and substitute $\\mathbf{x}$ into one equation'],
             notes=""),
        dict(type='profile', id='profile', title='LU, Cholesky and Thomas: method profile',
             best=['LU: one matrix, <b>many right-hand sides</b> (time steps, load cases, Newton with a frozen Jacobian)', 'Cholesky: SPD matrices, half the work and no pivoting', 'Thomas: tridiagonal systems in $O(n)$, millions of unknowns in milliseconds'],
             worst=['LU without pivoting: zero or tiny $u_{ii}$', 'Cholesky on a matrix that is not SPD: a negative number under the root', 'Sparse matrices that are not tridiagonal: LU fills the zeros in ("fill-in")'],
             suited=['Implicit time stepping (the same $A$ every step)', 'Statistics and ML: covariance matrices, least squares, Gaussian processes (Cholesky)', 'Splines and 1-D heat or diffusion problems (Thomas)'],
             avoid=['Just one system (plain elimination is equally good)', 'Huge 2-D or 3-D grids: fill-in makes LU too big; use iterative methods (Lecture 14)', 'Forming $A^{-1}$ "to save time": LU does the same job better'],
             verdict='Rule of thumb: <b>tridiagonal → Thomas; SPD → Cholesky; many right-hand sides → LU once; otherwise Gaussian elimination with pivoting</b>.',
             notes="Fill-in: for the 2-D plate with an N × N grid, the band of the matrix has width N, and LU fills the whole band, needing about N⁴ operations and N³ memory. That is the bridge to iterative methods."),
        dict(type='table', id='compare', title='Comparative analysis: direct solvers', cls='tb sm',
             head=['Method', 'Needs', 'Factor', 'Each new $\\mathbf{b}$', 'Memory', '$n = 1000$, 1440 b\'s'], tx=(0, 1), frag=True,
             rows=[['Gauss each time', 'any nonsingular $A$', '—', '$\\tfrac23 n^3$', '$n^2$', '16 min'], ['Inverse, then multiply', 'any nonsingular $A$', '$2n^3$', '$2n^2$', '$n^2$', '4.9 s'],
                   ['LU (with pivoting)', 'any nonsingular $A$', '$\\tfrac23 n^3$', '$2n^2$', '$n^2$', '3.5 s'], ['Cholesky', 'SPD', '$\\tfrac13 n^3$', '$2n^2$', '$\\tfrac12 n^2$', '3.2 s'],
                   ['Thomas', 'tridiagonal, diag. dominant', '$\\approx 3n$', '$\\approx 5n$', '$4n$', '7 ms (if tridiagonal)']],
             note='Times at $10^9$ operations per second. The inverse row is slower and less accurate than LU for the same job.', notefrag=True,
             notes="Numbers: Gauss 0.668 s × 1440 = 962 s = 16 min. Inverse: 2×10⁹ + 1440 × 2×10⁶ = 4.9 s. LU: 0.666 + 1440 × 0.002 = 3.5 s. Cholesky: 0.333 + 2.88 = 3.2 s. Thomas (if the matrix were tridiagonal): 8n per system ≈ 8×10³ × 1440 ≈ 1.2×10⁷, about 12 ms; the factor/solve split is 3n and 5n, giving about 7 ms."),
        dict(type='bridge', id='bridge', lead='Direct factorisations are fast for dense, banded and tridiagonal matrices. Some problems are still out of reach:',
             keep=['Factor once, solve many times', 'Cholesky for SPD: half the work, no pivoting', 'Thomas: $O(n)$ for tridiagonal systems', 'Exact up to rounding, in a known number of steps'],
             rows=[['2-D and 3-D grids: fill-in, memory grows like $n^{1.5}$ or worse', 'Iterative methods: only the nonzeros are stored', 14],
                   ['Splines need a tridiagonal solve', 'Thomas, used directly', 18],
                   ['Least squares gives SPD normal equations $A^TA\\mathbf{x} = A^T\\mathbf{y}$', 'Cholesky (and QR for better conditioning)', 23],
                   ['Implicit ODE methods solve a system every step', 'Factor once, reuse each step', 22]],
             notes="The 2-D plate is the turning point: its matrix is sparse (5 nonzeros per row) but not tridiagonal, and direct methods waste most of their effort on zeros that fill in."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see where the factorisation happens in a real computation.',
             items=[
                 dict(ic='🔥', h='Heat flow in time (implicit method)', t='One tridiagonal solve per time step',
                      detail=dict(where='simulating how a rod cools over time. The implicit (backward Euler) method is stable for any time step, but each step needs a tridiagonal solve; the matrix is the same every step.',
                                  eq='(1 + 2r)T_i^{new} - rT_{i-1}^{new} - rT_{i+1}^{new} = T_i^{old}, \\qquad r = \\frac{\\alpha\\,\\Delta t}{\\Delta x^2}',
                                  steps=['Build the three diagonals once: $-r$, $1 + 2r$, $-r$ (diagonally dominant, so Thomas is safe)', 'Each step: right-hand side = the old temperatures', 'Thomas down sweep and up sweep: $8n$ operations', 'With $n = 10^6$ points and 1000 steps: about $8\\times10^9$ operations, a few seconds'],
                                  note='The same structure appears in option pricing (Black–Scholes, Crank–Nicolson scheme) and in diffusion in images.')),
                 dict(ic='🎲', h='Correlated random numbers (Monte Carlo, ML)', t='Cholesky turns independent noise into correlated noise',
                      detail=dict(where='simulation and probabilistic machine learning. To sample a random vector with covariance $\\Sigma$, factor $\\Sigma = LL^T$ and set $\\mathbf{x} = L\\mathbf{z}$, where $\\mathbf{z}$ has independent standard normal entries.',
                                  eq='\\Sigma = \\begin{pmatrix} 4 & 2 \\\\ 2 & 2\\end{pmatrix} = \\begin{pmatrix} 2 & 0 \\\\ 1 & 1\\end{pmatrix}\\begin{pmatrix} 2 & 1 \\\\ 0 & 1\\end{pmatrix}',
                                  steps=['Draw $z_1, z_2$ independently', '$x_1 = 2z_1$, $\\;x_2 = z_1 + z_2$', 'Then $\\operatorname{var}(x_1) = 4$, $\\operatorname{var}(x_2) = 2$, $\\operatorname{cov}(x_1, x_2) = 2$, correlation $2/\\sqrt{8} = 0.707$', 'Gaussian processes and Kalman filters use the same Cholesky factor to solve and to sample'],
                                  note='Covariance matrices are SPD, so Cholesky always applies (and is the standard choice in NumPy: <code>np.linalg.cholesky</code>).')),
                 dict(ic='〰️', h='Smooth curves through points (splines)', t='Each cubic spline needs one tridiagonal solve',
                      detail=dict(where='cubic spline interpolation (Lecture 18), used in fonts, CAD, animation paths and data smoothing. Continuity of the slope and curvature at the data points gives one equation per point, involving only its two neighbours.',
                                  eq='h_{i-1}M_{i-1} + 2(h_{i-1} + h_i)M_i + h_iM_{i+1} = 6\\left(\\frac{y_{i+1} - y_i}{h_i} - \\frac{y_i - y_{i-1}}{h_{i-1}}\\right)',
                                  steps=['Unknowns $M_i$: the second derivatives at the data points', 'Each equation links $M_{i-1}$, $M_i$, $M_{i+1}$: a tridiagonal system', 'The diagonal $2(h_{i-1} + h_i)$ beats the off-diagonals: diagonally dominant, Thomas is safe', 'A spline through 10 000 points costs about 80 000 operations'],
                                  note='This is why splines are cheap enough to use everywhere.')),
                 dict(ic='🏗️', h='Bridges and buildings: many load cases', t='One stiffness matrix, hundreds of loads',
                      detail=dict(where='structural analysis by the finite element method. The stiffness matrix $K$ (SPD) depends only on the structure; each load case (wind, traffic, snow, earthquake) is a new right-hand side $\\mathbf{f}$ in $K\\mathbf{u} = \\mathbf{f}$.',
                                  steps=['Assemble $K$ once from the beams and joints', 'Cholesky factor $K = LL^T$ once', 'For each of hundreds of load cases: two triangular solves for the displacements $\\mathbf{u}$', 'Check the stresses for every case and report the worst'],
                                  note='Exactly the opening problem: the factorisation is paid once, every extra case is cheap.'))],
             notes="The Monte Carlo card is a good place to mention that numpy.random.multivariate_normal uses a factorisation of the covariance matrix internally."),
        dict(type='check', id='check', q='Doolittle LU of $A = \\begin{pmatrix} 2 & 1 \\\\ 6 & 8\\end{pmatrix}$. What are $l_{21}$ and $u_{22}$?',
             opts=['$l_{21} = 3$, $u_{22} = 5$', '$l_{21} = 3$, $u_{22} = 8$', '$l_{21} = \\tfrac13$, $u_{22} = 5$', '$l_{21} = 6$, $u_{22} = 2$'], right=0,
             answer='A. $l_{21} = a_{21}/u_{11} = 6/2 = 3$; $u_{22} = a_{22} - l_{21}u_{12} = 8 - 3(1) = 5$. Check: $\\begin{pmatrix} 1 & 0 \\\\ 3 & 1\\end{pmatrix}\\begin{pmatrix} 2 & 1 \\\\ 0 & 5\\end{pmatrix} = A$.',
             notes="Option C divides the wrong way round; option B forgets to subtract."),
        dict(type='summary', id='summary', items=[
            'Gaussian elimination is $A = LU$: $L$ holds the multipliers, $U$ the eliminated matrix',
            'Factor once ($\\tfrac23 n^3$), then $L\\mathbf{y} = \\mathbf{b}$, $U\\mathbf{x} = \\mathbf{y}$ ($2n^2$) per right-hand side',
            'SPD matrices: Cholesky $A = LL^T$, half the cost, no pivoting, and a test for positive definiteness',
            'Tridiagonal: the Thomas algorithm, $8n - 7$ operations'],
            hw=['Factor $\\begin{pmatrix} 3 & 2 & 1 \\\\ 6 & 6 & 3 \\\\ 9 & 10 & 6\\end{pmatrix}$ by Doolittle\'s method and solve with $\\mathbf{b} = (6, 15, 25)$. Then repeat with Crout\'s method.', 'Find the Cholesky factor of $\\begin{pmatrix} 4 & -2 & 0 \\\\ -2 & 5 & -2 \\\\ 0 & -2 & 5\\end{pmatrix}$.',
                'Solve $2x_1 - x_2 = 1$, $-x_{i-1} + 2x_i - x_{i+1} = 0$ ($i = 2, 3$), $-x_3 + 2x_4 = 1$ by the Thomas algorithm.', 'A model has $n = 2000$ and 500 right-hand sides. Compare the time of Gaussian elimination for each with one LU factorisation.'],
            solved='One LU of the plate matrix, then three solves: top 100° gives $(43.75, 56.25, 18.75, 31.25)$; 80° gives $(36.25, 48.75, 16.25, 28.75)$; 60° gives $(28.75, 41.25, 13.75, 26.25)$. For $n = 1000$ and 1440 readings: 3.5 s instead of 16 minutes.',
            next='<b>Iterative methods: Jacobi, Gauss–Seidel and SOR.</b> When the matrix is huge and sparse, stop factoring and start iterating, just like fixed-point iteration in Lecture 8.',
            notes="Homework answers: Q1: Doolittle L = [[1, 0, 0], [2, 1, 0], [3, 2, 1]], U = [[3, 2, 1], [0, 2, 1], [0, 0, 1]]; y = (6, 3, 1), x = (1, 1, 1). Crout: L = [[3, 0, 0], [6, 2, 0], [9, 4, 1]], U = [[1, 2/3, 1/3], [0, 1, 1/2], [0, 0, 1]]. Q2: L = [[2, 0, 0], [−1, 2, 0], [0, −1, 2]]. Q3: x = (1, 1, 1, 1). Q4: Gauss 5.34 s each, 2670 s (44.5 min) in total; LU 5.33 s + 500 × 4.0 ms = 9.3 s."),
    ],
    code={
        'lu3rhs': dict(file='lu_many_rhs', py='''# Doolittle LU once, then several right-hand sides (the plate)
A = [[4.0, -1.0, -1.0, 0.0], [-1.0, 4.0, 0.0, -1.0],
     [-1.0, 0.0, 4.0, -1.0], [0.0, -1.0, -1.0, 4.0]]
n = len(A)
L = [[0.0] * n for _ in range(n)]
U = [[0.0] * n for _ in range(n)]
for i in range(n):                                  # factor once
    for j in range(i, n):
        U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
    L[i][i] = 1.0
    for j in range(i + 1, n):
        L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]

def lu_solve(b):
    y = [0.0] * n
    for i in range(n):                              # forward: L y = b
        y[i] = b[i] - sum(L[i][k] * y[k] for k in range(i))
    x = [0.0] * n
    for i in range(n - 1, -1, -1):                  # backward: U x = y
        x[i] = (y[i] - sum(U[i][k] * x[k] for k in range(i + 1, n))) / U[i][i]
    return x

for top in [100.0, 80.0, 60.0]:
    b = [top, top + 50.0, 0.0, 50.0]               # edges: top, right 50, bottom 0, left 0
    T = lu_solve(b)
    print(f"top = {top:5.1f}:  " + "  ".join(f"{t:8.4f}" for t in T))
''', c='''/* Doolittle LU once, then several right-hand sides (the plate) */
#include <stdio.h>
#define N 4

double L[N][N], U[N][N];

void lu_solve(double b[N], double x[N]) {
    double y[N];
    for (int i = 0; i < N; i++) {                   /* forward: L y = b */
        y[i] = b[i];
        for (int k = 0; k < i; k++) y[i] -= L[i][k] * y[k];
    }
    for (int i = N - 1; i >= 0; i--) {              /* backward: U x = y */
        double s = y[i];
        for (int k = i + 1; k < N; k++) s -= U[i][k] * x[k];
        x[i] = s / U[i][i];
    }
}

int main(void) {
    double A[N][N] = {{4, -1, -1, 0}, {-1, 4, 0, -1}, {-1, 0, 4, -1}, {0, -1, -1, 4}};
    for (int i = 0; i < N; i++) {                   /* factor once */
        for (int j = i; j < N; j++) {
            double s = A[i][j];
            for (int k = 0; k < i; k++) s -= L[i][k] * U[k][j];
            U[i][j] = s;
        }
        L[i][i] = 1.0;
        for (int j = i + 1; j < N; j++) {
            double s = A[j][i];
            for (int k = 0; k < i; k++) s -= L[j][k] * U[k][i];
            L[j][i] = s / U[i][i];
        }
    }
    double tops[3] = {100, 80, 60}, b[N], T[N];
    for (int r = 0; r < 3; r++) {
        b[0] = tops[r]; b[1] = tops[r] + 50; b[2] = 0; b[3] = 50;
        lu_solve(b, T);
        printf("top = %5.1f:  %8.4f  %8.4f  %8.4f  %8.4f\\n", tops[r], T[0], T[1], T[2], T[3]);
    }
    return 0;
}
'''),
        'thomas': dict(file='thomas', py='''# Thomas algorithm for a tridiagonal system (heat in a rod)
n = 4
a = [0.0] + [-1.0] * (n - 1)      # sub-diagonal   (a[0] unused)
b = [2.0] * n                     # main diagonal
c = [-1.0] * (n - 1) + [0.0]      # super-diagonal (c[n-1] unused)
d = [0.0] * n
d[0] += 100.0                     # left end at 100 degrees
d[n - 1] += 0.0                   # right end at 0 degrees

cp = [0.0] * n
dp = [0.0] * n
cp[0] = c[0] / b[0]
dp[0] = d[0] / b[0]
for i in range(1, n):             # down sweep
    w = b[i] - a[i] * cp[i - 1]
    cp[i] = c[i] / w
    dp[i] = (d[i] - a[i] * dp[i - 1]) / w

x = [0.0] * n
x[n - 1] = dp[n - 1]
for i in range(n - 2, -1, -1):    # up sweep
    x[i] = dp[i] - cp[i] * x[i + 1]

for i in range(n):
    print(f"T{i+1} = {x[i]:.6f}")
''', c='''/* Thomas algorithm for a tridiagonal system (heat in a rod) */
#include <stdio.h>
#define N 4

int main(void) {
    double a[N], b[N], c[N], d[N], cp[N], dp[N], x[N];
    for (int i = 0; i < N; i++) { a[i] = -1; b[i] = 2; c[i] = -1; d[i] = 0; }
    a[0] = 0; c[N - 1] = 0;           /* unused corners */
    d[0] += 100;                      /* left end at 100 degrees */
    d[N - 1] += 0;                    /* right end at 0 degrees */

    cp[0] = c[0] / b[0];
    dp[0] = d[0] / b[0];
    for (int i = 1; i < N; i++) {     /* down sweep */
        double w = b[i] - a[i] * cp[i - 1];
        cp[i] = c[i] / w;
        dp[i] = (d[i] - a[i] * dp[i - 1]) / w;
    }
    x[N - 1] = dp[N - 1];
    for (int i = N - 2; i >= 0; i--)  /* up sweep */
        x[i] = dp[i] - cp[i] * x[i + 1];

    for (int i = 0; i < N; i++) printf("T%d = %.6f\\n", i + 1, x[i]);
    return 0;
}
'''),
        'cholesky': dict(file='cholesky', py='''# Cholesky factorisation A = L L^T, then solve A x = b
import math
A = [[4.0, 2.0, -2.0], [2.0, 10.0, 2.0], [-2.0, 2.0, 6.0]]
b = [-2.0, -4.0, 8.0]
n = len(A)
L = [[0.0] * n for _ in range(n)]
for j in range(n):
    s = A[j][j] - sum(L[j][k] ** 2 for k in range(j))
    if s <= 0:
        raise SystemExit("A is not positive definite")
    L[j][j] = math.sqrt(s)
    for i in range(j + 1, n):
        L[i][j] = (A[i][j] - sum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]
for row in L:
    print(" ".join(f"{v:8.4f}" for v in row))

y = [0.0] * n
for i in range(n):                                  # L y = b
    y[i] = (b[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]
x = [0.0] * n
for i in range(n - 1, -1, -1):                      # L^T x = y
    x[i] = (y[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]
print("x =", " ".join(f"{v:.6f}" for v in x))
''', c='''/* Cholesky factorisation A = L L^T, then solve A x = b */
#include <stdio.h>
#include <math.h>
#define N 3

int main(void) {
    double A[N][N] = {{4, 2, -2}, {2, 10, 2}, {-2, 2, 6}};
    double b[N] = {-2, -4, 8}, L[N][N] = {{0}}, y[N], x[N];
    for (int j = 0; j < N; j++) {
        double s = A[j][j];
        for (int k = 0; k < j; k++) s -= L[j][k] * L[j][k];
        if (s <= 0) { printf("A is not positive definite\\n"); return 1; }
        L[j][j] = sqrt(s);
        for (int i = j + 1; i < N; i++) {
            double t = A[i][j];
            for (int k = 0; k < j; k++) t -= L[i][k] * L[j][k];
            L[i][j] = t / L[j][j];
        }
    }
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) printf(j ? " %8.4f" : "%8.4f", L[i][j]);
        printf("\\n");
    }
    for (int i = 0; i < N; i++) {                   /* L y = b */
        double s = b[i];
        for (int k = 0; k < i; k++) s -= L[i][k] * y[k];
        y[i] = s / L[i][i];
    }
    for (int i = N - 1; i >= 0; i--) {              /* L^T x = y */
        double s = y[i];
        for (int k = i + 1; k < N; k++) s -= L[k][i] * x[k];
        x[i] = s / L[i][i];
    }
    printf("x = %.6f %.6f %.6f\\n", x[0], x[1], x[2]);
    return 0;
}
'''),
    },
    lab=dict(title='LU Cholesky Thomas Lab',
             intro='Factor your own matrices step by step (LU with or without pivoting, Cholesky), then solve many right-hand sides and tridiagonal systems in code.',
             tabs=[
                 dict(name='LU stepper', blocks=[
                     dict(p='Type [A | b] (or just A). Watch L fill with the multipliers while U is eliminated, then the forward and backward substitutions. Turn on pivoting to see PA = LU.'),
                     dict(w='linsys', o=dict(mat='1 1 1 1; 4 3 -1 6; 3 5 3 4', mode='lu', modes=['lu', 'chol', 'gauss'], height='300px',
                                             presets=[['Problem 1', '2 1 1 3; 4 3 3 7; 8 7 9 19', 'lu', False], ['Problem 4', '1 1 1 1; 4 3 -1 6; 3 5 3 4', 'lu', False], ['plate', '4 -1 -1 0 100; -1 4 0 -1 150; -1 0 4 -1 0; 0 -1 -1 4 50', 'lu', False], ['zero pivot', '0 1 1; 1 1 2', 'lu', True], ['homework 1', '3 2 1 6; 6 6 3 15; 9 10 6 25', 'lu', False]]))]),
                 dict(name='Cholesky', blocks=[
                     dict(p='Cholesky works only for symmetric positive definite matrices. Try changing one diagonal entry until it fails.'),
                     dict(w='linsys', o=dict(mat='4 2 -2 -2; 2 10 2 -4; -2 2 6 8', mode='chol', modes=['chol'], nopivot=True, height='260px',
                                             presets=[['Problem 2', '4 2 -2 -2; 2 10 2 -4; -2 2 6 8', 'chol'], ['homework 2', '4 -2 0; -2 5 -2; 0 -2 5', 'chol'], ['circuit (L11)', '7 -2 0 12; -2 9 -3 2; 0 -3 6 3', 'chol'], ['not SPD', '1 2 3; 2 1 3', 'chol']]))]),
                 dict(name='Code', blocks=[
                     dict(h='LU once, many right-hand sides'), dict(code='lu3rhs', tasks=['Run it. Fill in the table from the opening slide.', 'Add a fourth reading: top edge 120°.', 'Print L and U and compare with the stepper.']),
                     dict(h='Thomas algorithm'), dict(code='thomas', tasks=['Run it: is the profile a straight line?', 'Set n = 9. Predict the answer first.', 'Add a heat source: d[i] += 10 for every i. How does the profile change?']),
                     dict(h='Cholesky'), dict(code='cholesky', tasks=['Run it. Compare L with Problem 2.', 'Change A[2][2] to 1. What message do you get, and why?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Factor $\\begin{pmatrix} 3 & 2 & 1 \\\\ 6 & 6 & 3 \\\\ 9 & 10 & 6\\end{pmatrix}$ by Doolittle and solve with $\\mathbf{b} = (6, 15, 25)$.', '$L = \\begin{pmatrix} 1 & 0 & 0 \\\\ 2 & 1 & 0 \\\\ 3 & 2 & 1\\end{pmatrix}$, $U = \\begin{pmatrix} 3 & 2 & 1 \\\\ 0 & 2 & 1 \\\\ 0 & 0 & 1\\end{pmatrix}$; $\\mathbf{y} = (6, 3, 1)$; $\\mathbf{x} = (1, 1, 1)$.'),
                         ('Why is LU better than Gaussian elimination when there are many right-hand sides?', 'Elimination costs $\\tfrac23 n^3$ and depends only on $A$; LU stores its result (L and U). Each further $\\mathbf{b}$ needs only forward and back substitution, $2n^2$ operations, instead of repeating the $\\tfrac23 n^3$.'),
                         ('When can Cholesky be used, and what does it cost?', 'When $A$ is symmetric positive definite. $A = LL^T$ costs about $\\tfrac13 n^3$ operations (half of LU) and needs no pivoting. If a number under a square root is $\\le 0$, $A$ is not positive definite.'),
                         ('Find the Cholesky factor of $\\begin{pmatrix} 4 & -2 & 0 \\\\ -2 & 5 & -2 \\\\ 0 & -2 & 5\\end{pmatrix}$.', '$l_{11} = 2$, $l_{21} = -1$, $l_{31} = 0$, $l_{22} = \\sqrt{5 - 1} = 2$, $l_{32} = (-2 - 0)/2 = -1$, $l_{33} = \\sqrt{5 - 1} = 2$.'),
                         ('Solve $2x_1 - x_2 = 1$, $-x_1 + 2x_2 - x_3 = 0$, $-x_2 + 2x_3 - x_4 = 0$, $-x_3 + 2x_4 = 1$ by the Thomas algorithm.', '$c\' = (-0.5, -0.6667, -0.75)$, $d\' = (0.5, 0.3333, 0.25, 1)$; back: $x_4 = 1$, $x_3 = 0.25 + 0.75 = 1$, $x_2 = 1$, $x_1 = 1$.')])])]),
)
