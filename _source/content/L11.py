LECTURE = dict(
    title="Linear Systems, Cramer's Rule and the Inverse",
    short="Cramer's Rule and the Inverse",
    sub='Writing many equations as $A\\mathbf{x} = \\mathbf{b}$, solving them with the two formulas from school, measuring vectors and matrices with norms, and discovering why the formulas break down for real problems.',
    slides=[
        dict(type='cover', id='cover', notes="Opening question: 'Who has solved three equations in three unknowns? How?' Most will say substitution, elimination, or Cramer's rule.\n\nToday we take the formula students already know (Cramer) and the inverse matrix, and ask the numerical-methods question: how much work does it take, and what happens in floating point?"),
        dict(type='bullets', id='hook', title='The problem: currents in a circuit', kick='Why this lecture', rw=760,
             lead='Kirchhoff\'s voltage law around each loop of a three-loop circuit gives three equations for the loop currents $I_1, I_2, I_3$ (amperes).',
             items=['Every loop equation is <b>linear</b> in the currents: resistances times currents add up to the source voltage',
                    'Three loops: three equations. A phone charger board: dozens. A chip: millions',
                    'School gives two formulas: <b>Cramer\'s rule</b> and $\\mathbf{x} = A^{-1}\\mathbf{b}$',
                    'Today: use them, count their cost, and see where they fail. A 25-loop circuit by Cramer\'s rule would take longer than the age of the universe'],
             frag=True,
             right=dict(stack=[dict(eq='\\begin{aligned} 7I_1 - 2I_2 \\phantom{{}-3I_3} &= 12 \\\\ -2I_1 + 9I_2 - 3I_3 &= 2 \\\\ -3I_2 + 6I_3 &= 3 \\end{aligned}', cap='Loop equations (volts)'),
                               dict(card=dict(cls='blue', tag='The question', t='Find $I_1, I_2, I_3$. Then ask: how would the same method cope with 25 loops, or 25 000?'))]),
             notes="The coefficients come from the resistances: loop 1 has 7 Ω in total and shares 2 Ω with loop 2; loop 2 has 9 Ω and shares 3 Ω with loop 3; loop 3 has 6 Ω. Sources: 12 V, 2 V, 3 V.\n\nDo not solve it yet: ask students to guess which method they would use. Solved on slide 7 (Cramer) and slide 10 (inverse): I = (2, 1, 1) A."),
        dict(type='goals', id='goals', items=[
            'Write a system of linear equations as $A\\mathbf{x} = \\mathbf{b}$ and recognise the three possible outcomes',
            'Solve a system by <b>Cramer\'s rule</b> and by the <b>inverse</b> (adjugate) method',
            'Count the operations each method needs and explain why both fail for large $n$',
            'Compute <b>vector and matrix norms</b> and the <b>condition number</b> $\\kappa(A)$',
            'Predict how many digits of a computed solution can be trusted'],
            prev='Module 2: Newton for systems needs a linear solve $J\\Delta = -F$ at every step.',
            today='Linear systems on their own: the school formulas, their cost, and how sensitive the answer is.',
            notes="Module 3 starts here. Remind students of slide 'Newton for systems' (Lecture 10): every step was a linear system. That is one of many reasons linear systems are the most important problem in numerical computing."),
        dict(type='math', id='form', title='Many equations, one matrix equation',
             eqs=[dict(cap='The circuit in matrix form', eq='\\underbrace{\\begin{pmatrix} 7 & -2 & 0 \\\\ -2 & 9 & -3 \\\\ 0 & -3 & 6 \\end{pmatrix}}_{A}\\underbrace{\\begin{pmatrix} I_1 \\\\ I_2 \\\\ I_3 \\end{pmatrix}}_{\\mathbf{x}} = \\underbrace{\\begin{pmatrix} 12 \\\\ 2 \\\\ 3 \\end{pmatrix}}_{\\mathbf{b}}'),
                  dict(cap='Augmented matrix: all the data in one table', eq='[A \\mid \\mathbf{b}] = \\left(\\begin{array}{ccc|c} 7 & -2 & 0 & 12 \\\\ -2 & 9 & -3 & 2 \\\\ 0 & -3 & 6 & 3 \\end{array}\\right)', frag=True)],
             items=['$a_{ij}$ = coefficient of unknown $j$ in equation $i$', '<b>Unique solution</b> exactly when $\\det A \\ne 0$ (A is <i>nonsingular</i>)', '$\\det A = 0$: either <b>no solution</b> (parallel lines) or <b>infinitely many</b> (the same line twice)',
                    'Geometry for 2 unknowns: two lines that cross once, never, or everywhere'],
             ifrag=True,
             notes="Draw three pictures for 2×2: crossing lines (unique), parallel lines (none), coincident lines (infinitely many). The last two both have det A = 0.\n\nThe augmented matrix is the form we will manipulate from now on; every method in this module works on it."),
        dict(type='math', id='cramer', title="Cramer's rule",
             eqs=[dict(cap='2×2: eliminate y, then x (school algebra)', eq='x = \\frac{b_1 a_{22} - a_{12} b_2}{a_{11}a_{22} - a_{12}a_{21}} = \\frac{\\begin{vmatrix} b_1 & a_{12} \\\\ b_2 & a_{22}\\end{vmatrix}}{\\begin{vmatrix} a_{11} & a_{12} \\\\ a_{21} & a_{22}\\end{vmatrix}}'),
                  dict(cap='General rule: Aᵢ is A with column i replaced by b', eq='x_i = \\frac{D_i}{D}, \\qquad D = \\det A, \\qquad D_i = \\det A_i', frag=True),
                  dict(cap='3×3 determinant by cofactor expansion along row 1', eq='\\det A = a_{11}\\begin{vmatrix} a_{22} & a_{23} \\\\ a_{32} & a_{33}\\end{vmatrix} - a_{12}\\begin{vmatrix} a_{21} & a_{23} \\\\ a_{31} & a_{33}\\end{vmatrix} + a_{13}\\begin{vmatrix} a_{21} & a_{22} \\\\ a_{31} & a_{32}\\end{vmatrix}', frag=True)],
             items=['A closed formula: no iteration, no stopping rule', 'Needs $D \\ne 0$', '$n$ unknowns: $n + 1$ determinants of size $n \\times n$', 'Each $n\\times n$ determinant by cofactors needs $n$ determinants of size $n - 1$: the work multiplies by $n$ at every level'],
             ifrag=True,
             notes="Derive the 2×2 formula on the board: multiply eq. 1 by a22 and eq. 2 by a12, subtract to eliminate y. The numerator and denominator are both determinants: that is Cramer's rule.\n\nThe last bullet is the seed of the cost problem: cofactor expansion of an n×n determinant calls n determinants of size n − 1, so the work grows like n!."),
        dict(type='bullets', id='algo', title="Cramer's rule, step by step", kick='The method, step by step', ordered=True, rw=780,
             items=['Write the system as $[A \\mid \\mathbf{b}]$', 'Compute $D = \\det A$. If $D = 0$, stop: no unique solution', 'For each $i = 1, \\dots, n$: copy $A$, replace column $i$ by $\\mathbf{b}$, compute its determinant $D_i$', 'Set $x_i = D_i / D$',
                    'Check: substitute $\\mathbf{x}$ into every equation'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input A (n×n), b\nD ← det(A)\nif D = 0: stop (singular)\nfor i = 1 … n:\n    Aᵢ ← A with column i := b\n    x[i] ← det(Aᵢ) / D\nreturn x\n\ndet(M):  # cofactor expansion\n    if size 1: return m₁₁\n    return Σⱼ (−1)^(1+j) m₁ⱼ det(M₁ⱼ)</pre></div><p class="small" style="margin-top:14px">The recursion in <code>det</code> is where all the work goes: one call of size $n$ makes $n$ calls of size $n - 1$.</p>'),
             notes="Steps 1–5 are what a full written solution should show: D first (and the check D ≠ 0), then each D_i with the replaced column clearly marked, then the division, then the check.\n\nThe pseudocode makes the cost visible: det calls itself n times on matrices one size smaller."),
        dict(type='worked', id='p1', title='Problem 1: the circuit by Cramer\'s rule',
             q='Solve $7I_1 - 2I_2 = 12$, $\\;-2I_1 + 9I_2 - 3I_3 = 2$, $\\;-3I_2 + 6I_3 = 3$.',
             steps=['$D = 7(9\\cdot 6 - (-3)(-3)) - (-2)((-2)\\cdot 6 - 0) + 0 = 7(45) - 24 = 291 \\ne 0$',
                    '$D_1 = \\begin{vmatrix} 12 & -2 & 0 \\\\ 2 & 9 & -3 \\\\ 3 & -3 & 6\\end{vmatrix} = 12(45) + 2(12 + 9) = 582$',
                    'In the same way (columns 2 and 3 replaced): $D_2 = 7(12 + 9) - 12(-12) = 291$ and $D_3 = 291$',
                    '$I_1 = 582/291 = 2$, $\\;I_2 = 291/291 = 1$, $\\;I_3 = 291/291 = 1$. Check eq. 2: $-4 + 9 - 3 = 2$ ✓'],
             answer='$I_1 = 2$ A, $I_2 = 1$ A, $I_3 = 1$ A, using four 3×3 determinants.',
             right=dict(w='cramer', o=dict(mat='7 -2 0 12; -2 9 -3 2; 0 -3 6 3', fixed=True, noinput=True)), rw=920,
             notes="Work D on the board in full; let students do D1, D2, D3 in pairs (one each), then check with the widget.\n\nD3 in full: 7(27 + 6) − (−2)(−6 − 0) + 12(6 − 0) = 231 − 12 + 72 = 291."),
        dict(type='math', id='inverse', title='The inverse method: $\\mathbf{x} = A^{-1}\\mathbf{b}$',
             eqs=[dict(cap='If A⁻¹ exists', eq='A\\mathbf{x} = \\mathbf{b} \\;\\Longrightarrow\\; A^{-1}A\\mathbf{x} = A^{-1}\\mathbf{b} \\;\\Longrightarrow\\; \\mathbf{x} = A^{-1}\\mathbf{b}'),
                  dict(cap='Adjugate formula', eq='A^{-1} = \\frac{1}{\\det A}\\,\\operatorname{adj} A, \\qquad \\operatorname{adj}A = C^{T}', frag=True),
                  dict(cap='2×2: swap the diagonal, negate the rest', eq='\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}^{-1} = \\frac{1}{ad - bc}\\begin{pmatrix} d & -b \\\\ -c & a \\end{pmatrix}', frag=True)],
             items=['$M_{ij}$ (minor) = determinant of $A$ without row $i$ and column $j$', '$C_{ij}$ (cofactor) = minor with the sign pattern $\\begin{smallmatrix} + & - & + \\\\ - & + & - \\\\ + & - & + \\end{smallmatrix}$',
                    'Exists only when $\\det A \\ne 0$', 'Once $A^{-1}$ is known, any new $\\mathbf{b}$ costs only a matrix–vector product'],
             ifrag=True,
             notes="The last bullet is the inverse method's selling point (many right-hand sides). Lecture 13 shows that LU gives the same benefit more cheaply and more accurately."),
        dict(type='bullets', id='algo2', title='The inverse method, step by step', kick='The method, step by step', ordered=True, rw=780,
             items=['Compute $D = \\det A$; if $D = 0$, stop', 'Compute all $n^2$ cofactors $C_{ij} = (-1)^{i+j}M_{ij}$', 'Transpose: $\\operatorname{adj}A = C^{T}$', 'Divide: $A^{-1} = \\operatorname{adj}A / D$; check $AA^{-1} = I$', 'Multiply: $\\mathbf{x} = A^{-1}\\mathbf{b}$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input A (n×n), b\nD ← det(A)\nif D = 0: stop (singular)\nfor i, j = 1 … n:\n    C[i][j] ← (−1)^(i+j) · det(minor(A, i, j))\nAinv ← transpose(C) / D\nfor i = 1 … n:\n    x[i] ← Σⱼ Ainv[i][j] · b[j]\nreturn x</pre></div><p class="small" style="margin-top:14px">$n^2$ cofactors, each a determinant of size $n - 1$: even more work than Cramer for one right-hand side.</p>'),
             notes="Common mistake in step 3: forgetting to transpose. For a symmetric A (like our circuit) the cofactor matrix is symmetric too, so the mistake is invisible; warn students to transpose anyway."),
        dict(type='worked', id='p2', title='Problem 2: the circuit by the inverse',
             q='Find $A^{-1}$ for the circuit matrix and use it to find the currents.',
             steps=['Cofactors: $C_{11} = 45$, $C_{12} = -\\begin{vmatrix} -2 & -3 \\\\ 0 & 6\\end{vmatrix} = 12$, $C_{13} = 6$, $C_{22} = 42$, $C_{23} = 21$, $C_{33} = 59$, and $C_{ji} = C_{ij}$ here',
                    '$A^{-1} = \\dfrac{1}{291}\\begin{pmatrix} 45 & 12 & 6 \\\\ 12 & 42 & 21 \\\\ 6 & 21 & 59\\end{pmatrix}$ (symmetric, because $A$ is)',
                    '$\\mathbf{x} = A^{-1}\\mathbf{b} = \\dfrac{1}{291}\\begin{pmatrix} 45(12) + 12(2) + 6(3) \\\\ 12(12) + 42(2) + 21(3) \\\\ 6(12) + 21(2) + 59(3)\\end{pmatrix} = \\dfrac{1}{291}\\begin{pmatrix} 582 \\\\ 291 \\\\ 291\\end{pmatrix}$'],
             answer='$\\mathbf{x} = (2, 1, 1)$, as before. Nine 2×2 cofactors plus one 3×3 determinant.',
             right=dict(w='cramer', o=dict(mat='7 -2 0 12; -2 9 -3 2; 0 -3 6 3', view='inv', fixed=True, noinput=True)), rw=840,
             notes="Ask: if the sources change to b = (0, 0, 9), what are the currents? With A⁻¹ known: x = (1/291)(54, 189, 531) = (0.1856, 0.6495, 1.8247). That reuse is the advantage of having the inverse."),
        dict(type='widget', id='cost', title='Limitation 1: the cost explodes', w='cost', o=dict(n=20, height='380px'), lw=600,
             items=['Cofactor determinants: one $n\\times n$ determinant costs about $e \\cdot n!$ operations', 'Cramer: $n + 1$ of them. $n = 3$: 59 operations; $n = 10$: $1.1\\times10^8$ (0.1 s)',
                    '$n = 20$: $1.4 \\times 10^{20}$ operations, <b>4400 years</b>; elimination (Lecture 12): 5910 operations, 6 µs', '$n = 25$: $3.5\\times10^{10}$ years, more than the age of the universe'],
             frag=True,
             notes="Drag the slider slowly from 3 to 25 and let the class watch the red curve leave the chart. Then move to 1000: elimination still takes under a second.\n\nCount used: T(n) = n·T(n − 1) + 2n − 1 operations for one cofactor determinant (T(2) = 3, T(3) = 14), Cramer = (n + 1)T(n) + n divisions. Elimination: 2n³/3 + 3n²/2 − 7n/6 (exact count, Lecture 12)."),
        dict(type='cards', id='fp', title='Limitations 2 and 3: determinants and inverses in floating point', kick='Limitations shown failing', n=3,
             cards=[dict(cls='bad', tag='Underflow', h='$\\det(0.1\\,I_{400}) = 10^{-400}$', t='Below the smallest double ($4.9\\times10^{-324}$, Lecture 2), so the computer stores 0 and Cramer reports "singular". Yet the system is trivial: $\\mathbf{x} = 10\\,\\mathbf{b}$.'),
                    dict(cls='bad', tag='Overflow', h='$\\det(10\\,I_{400}) = 10^{400}$', t='Overflows to infinity, and every $x_i = D_i/D$ becomes $\\infty/\\infty$ = NaN. The size of the determinant says nothing useful about the system.'),
                    dict(cls='key', tag='Waste', h='$A^{-1}$ then $A^{-1}\\mathbf{b}$', t='Even with a good method for the inverse, it costs about $2n^3$ operations, three times elimination, and adds extra rounding errors. Numerical analysts rarely form $A^{-1}$.')],
             frag=True,
             below=dict(html='<p class="small frag fade" style="margin-top:22px">A small determinant does <b>not</b> mean trouble, and a large one does not mean safety. What does measure trouble? The <b>condition number</b>, next.</p>'),
             notes="These three are the classic objections to determinant-based methods. Try det(0.1·I) in NumPy: np.linalg.det(0.1*np.eye(400)) returns 0.0.\n\nThe first two cards prepare the condition-number idea: we need a measure that does not change when A is multiplied by a constant."),
        dict(type='math', id='norms', title='Measuring size: vector and matrix norms',
             eqs=[dict(cap='Vector norms', eq='\\|\\mathbf{v}\\|_1 = \\sum_i |v_i|, \\quad \\|\\mathbf{v}\\|_2 = \\sqrt{\\textstyle\\sum_i v_i^2}, \\quad \\|\\mathbf{v}\\|_\\infty = \\max_i |v_i|'),
                  dict(cap='Matrix norms: largest column sum, largest row sum', eq='\\|A\\|_1 = \\max_j \\sum_i |a_{ij}|, \\qquad \\|A\\|_\\infty = \\max_i \\sum_j |a_{ij}|', frag=True),
                  dict(cap='Key property', eq='\\|A\\mathbf{x}\\| \\le \\|A\\|\\,\\|\\mathbf{x}\\|', frag=True)],
             items=['$\\mathbf{v} = (3, -4, 1)$: $\\|\\mathbf{v}\\|_1 = 8$, $\\|\\mathbf{v}\\|_2 = \\sqrt{26} = 5.099$, $\\|\\mathbf{v}\\|_\\infty = 4$', 'Circuit $A$: row sums 9, 14, 9, so $\\|A\\|_\\infty = 14$; column sums give $\\|A\\|_1 = 14$ too',
                    'A norm is a single number for "how big": used for errors, stopping rules and convergence', 'Same idea as $|x|$ for numbers (Lecture 4), extended to vectors and matrices'],
             ifrag=True,
             notes="The ∞-norm is the easiest by hand and the one most textbooks use for condition numbers in written problems. The 2-norm of a matrix (largest singular value) is mentioned only: 11.517 for the circuit matrix.\n\nStopping rules from Lectures 6–10 become ‖x_new − x_old‖ < tol in Lecture 14."),
        dict(type='math', id='cond', title='The condition number of a matrix',
             eqs=[dict(cap='Definition', eq='\\kappa(A) = \\|A\\|\\,\\|A^{-1}\\| \\;\\ge\\; 1'),
                  dict(cap='Error bound: relative error in b is amplified by at most κ', eq='\\frac{\\|\\delta\\mathbf{x}\\|}{\\|\\mathbf{x}\\|} \\;\\le\\; \\kappa(A)\\,\\frac{\\|\\delta\\mathbf{b}\\|}{\\|\\mathbf{b}\\|}', frag=True)],
             items=['Same idea as $\\kappa_f$ in Lecture 5, now for systems', 'Rule of thumb: about $\\log_{10}\\kappa$ significant digits are lost', 'Circuit: $\\|A^{-1}\\|_\\infty = 86/291 = 0.2955$, so $\\kappa_\\infty = 14 \\times 0.2955 = 4.14$: <b>well-conditioned</b>',
                    '$\\kappa(cA) = \\kappa(A)$ for any $c \\ne 0$: unlike the determinant, it is not fooled by scaling'],
             ifrag=True,
             notes="Derivation (optional): A(x + δx) = b + δb gives δx = A⁻¹δb, so ‖δx‖ ≤ ‖A⁻¹‖‖δb‖; and ‖b‖ ≤ ‖A‖‖x‖. Divide the two inequalities.\n\nThe last bullet answers the floating-point cards: 0.1·I and 10·I both have κ = 1, perfectly conditioned, whatever their determinants."),
        dict(type='worked', id='p3', title='Problem 3: an ill-conditioned system',
             q='Find $\\kappa_\\infty(A)$ for $A = \\begin{pmatrix} 1 & 1 \\\\ 1 & 1.0001\\end{pmatrix}$. Solve with $\\mathbf{b} = (2, 2.0001)$, then with $b_2 = 2.0002$.',
             steps=['$\\det A = 0.0001$, $\\;A^{-1} = \\dfrac{1}{0.0001}\\begin{pmatrix} 1.0001 & -1 \\\\ -1 & 1 \\end{pmatrix} = \\begin{pmatrix} 10001 & -10000 \\\\ -10000 & 10000\\end{pmatrix}$',
                    '$\\|A\\|_\\infty = 2.0001$, $\\;\\|A^{-1}\\|_\\infty = 20001$, $\\;\\kappa_\\infty = 40004$: about 4–5 digits can be lost',
                    '$\\mathbf{b} = (2, 2.0001)$ gives $\\mathbf{x} = (1, 1)$; $\\;b_2 = 2.0002$ gives $\\mathbf{x} = (0, 2)$',
                    'Input changed by $5\\times10^{-5}$, answer by 100%: amplified 20000 times (bound: 40004)'],
             answer='Nearly parallel lines: a tiny change in the data moves the crossing point a long way.',
             right=dict(w='illcond', o=dict(preset='ill', height='230px')), rw=760,
             notes="Move the slider in the widget: the red crossing point runs along the lines.\n\nNo method can fix this; it is a property of the problem (Lecture 5). Good methods (pivoting, Lecture 12) only avoid adding extra error of their own."),
        dict(type='compare', id='classic', title='Same circuit, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Classical (Cramer\'s rule)', tag='Formula', cls='blue', items=['Four 3×3 determinants: 291, 582, 291, 291', '59 operations, exact fractions by hand', '$\\mathbf{x} = (2, 1, 1)$']),
             right=dict(h='Numerical (Gaussian elimination, Lecture 12)', tag='Algorithm', cls='key', items=['Eliminate $I_1$, then $I_2$, then back-substitute', '28 operations', '$\\mathbf{x} = (2, 1, 1)$']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the classical approach cannot work</span><h3>A circuit with 25 loops</h3><p>Cramer\'s rule: $1.1\\times10^{27}$ operations, $3.5\\times10^{10}$ years at $10^9$ operations per second. Elimination: 11 325 operations, about 11 µs. Real circuit simulators (SPICE) solve systems with thousands of unknowns many times per second.</p></div>'),
             notes="For n = 3 both are fine; the difference is how the work grows. Cramer's rule remains useful for theory and for 2×2 or 3×3 by hand."),
        dict(type='code', id='code', title='Cramer, the inverse and κ in Python and C', code='cramer3', lw=560,
             items=['<code>det3</code> is cofactor expansion along row 1', 'Cramer: replace column $i$ by $\\mathbf{b}$, divide by $D$', 'Inverse from cofactors (note the transpose: <code>inv[j][i]</code>)', 'Then $\\kappa_\\infty = \\|A\\|_\\infty\\|A^{-1}\\|_\\infty$'],
             notes="Run both tabs. Then change b to (0, 0, 9) and A to the ill-conditioned 2×2 embedded in 3×3 (lab task).\n\nIn real code: numpy.linalg.solve(A, b) (elimination with pivoting) and numpy.linalg.cond(A)."),
        dict(type='exam', id='practice', src='Problem 4',
             q='"Solve by Cramer\'s rule: $x + y + z = 6$, $\\;2x - y + z = 3$, $\\;x + 2y - z = 2$. Explain why Cramer\'s rule is not used for large systems."',
             tips=['Write $[A \\mid \\mathbf{b}]$; compute $D$ and state $D = 7 \\ne 0$ before anything else', 'Show each $D_i$ with the replaced column: $D_1 = 7$, $D_2 = 14$, $D_3 = 21$',
                   'Answer $x = 1$, $y = 2$, $z = 3$, and substitute back as a check', 'Cost: $n + 1$ determinants, each about $e\\cdot n!$ operations by cofactors; give a number (e.g. $n = 20$: 4400 years) and name the alternative (Gaussian elimination, $\\approx 2n^3/3$)'],
             notes=""),
        dict(type='profile', id='profile', title="Cramer's rule and the adjugate inverse: method profile",
             best=['2×2 and 3×3 systems by hand, with exact fractions', 'When a <b>formula</b> is needed, e.g. the slope of a regression line', 'Theory: shows the solution depends continuously on the data when $\\det A \\ne 0$'],
             worst=['$n \\ge 10$: cost grows like $n!$', 'Very large or very small determinants: overflow, underflow', 'Nearly singular $A$: huge $A^{-1}$, digits lost'],
             suited=['Hand calculation and small symbolic systems', 'Closed-form formulas: regression coefficients, 2×2 Newton steps (Lecture 10), small graphics transforms', 'Teaching what a solution means'],
             avoid=['Any program with $n > 3$', 'Several right-hand sides (use LU, Lecture 13)', 'Ill-conditioned problems: these methods add rounding of their own'],
             verdict='Rule of thumb: <b>formulas for 2×2 and 3×3 on paper; elimination for everything a computer solves</b>.',
             notes="Students often ask: then why learn Cramer? Because closed formulas are useful (the regression slope on the applications slide is Cramer's rule), and because it makes the cost question concrete."),
        dict(type='table', id='compare', title='Comparative analysis: methods for $A\\mathbf{x} = \\mathbf{b}$', cls='tb sm',
             head=['Method', 'Operations (about)', '$n = 3$', '$n = 1000$', 'New $\\mathbf{b}$ costs', 'Best for'], tx=(0, 5), frag=True,
             rows=[["Cramer (cofactors)", '$e\\,(n+1)!$', '59', 'impossible', 'everything again', '2×2, 3×3 by hand'], ['Adjugate inverse', '$e\\,n^2 (n-1)!$', '≈ 65', 'impossible', '$2n^2$', 'tiny matrices, formulas'],
                   ['Gaussian elimination', '$\\tfrac23 n^3$', '28', '0.67 s', '$\\tfrac23 n^3$', 'one system (L12)'], ['LU factorisation', '$\\tfrac23 n^3$ once', '28', '0.67 s', '$2n^2$', 'many right-hand sides (L13)'],
                   ['Jacobi, Gauss–Seidel', 'per sweep $\\approx 2\\cdot$nonzeros', '—', 'fast if sparse', 'iterate again', 'huge sparse systems (L14)']],
             note='Times assume $10^9$ operations per second. "Impossible" means more than $10^{2500}$ years.', notefrag=True,
             notes="The bottom three rows preview the rest of Module 3. Ask students to copy this table and fill in a 'stable?' column as we go."),
        dict(type='bridge', id='bridge', lead='The formulas are exact but hopelessly slow, and blind to floating point. Each limitation has a fix:',
             keep=['Matrix form $A\\mathbf{x} = \\mathbf{b}$ and the augmented matrix', 'Existence: unique solution iff $\\det A \\ne 0$', 'Norms and the condition number $\\kappa(A)$', 'Closed formulas for 2×2 and 3×3'],
             rows=[['Cost grows like $n!$', 'Elimination: $\\tfrac23 n^3$ operations, with pivoting for safety', 12],
                   ['Many right-hand sides, same $A$', 'Factor once ($A = LU$), then $2n^2$ per $\\mathbf{b}$', 13],
                   ['Millions of unknowns, mostly zeros', 'Iterative methods that never store the full matrix', 14],
                   ['Ill-conditioned $A$ (large $\\kappa$)', 'Cannot be cured by any solver; reformulate (e.g. least squares)', 23]],
             notes="The last row is honest: κ is a property of the problem. Lecture 23 shows how least squares and good modelling choices avoid squaring κ."),
        dict(type='apps', id='apps', n=2, lead='Click a card: each one solves a small linear system, or inverts a matrix, at a specific step.',
             items=[
                 dict(ic='⚡', h='Circuit analysis', t='Loop (mesh) currents from Kirchhoff\'s law',
                      detail=dict(where='the mesh-current method of circuit analysis. Each loop gives one linear equation; the coefficient matrix is symmetric (shared resistors appear twice).',
                                  w='cramer', o=dict(mat='7 -2 0 12; -2 9 -3 2; 0 -3 6 3', fixed=True),
                                  note='Change the 12 V source (top-right number) and watch all three currents change. Real simulators do the same with elimination (Lecture 12).')),
                 dict(ic='📈', h='Regression slope (machine learning)', t='The formula for the best-fit line is Cramer\'s rule',
                      detail=dict(where='fitting $y = a + bx$ to data. Least squares (Lecture 23) gives a 2×2 system, the <i>normal equations</i>; solving it by Cramer gives the formula in every statistics book.',
                                  eq='\\begin{pmatrix} n & \\sum x \\\\ \\sum x & \\sum x^2\\end{pmatrix}\\begin{pmatrix} a \\\\ b\\end{pmatrix} = \\begin{pmatrix} \\sum y \\\\ \\sum xy\\end{pmatrix} \\;\\Rightarrow\\; b = \\frac{n\\sum xy - \\sum x\\sum y}{n\\sum x^2 - (\\sum x)^2}',
                                  table=[['data $x$', '1', '2', '3', '4'], [['data $y$', '2', '3', '5', '6']]],
                                  note='$n = 4$, $\\sum x = 10$, $\\sum x^2 = 30$, $\\sum y = 16$, $\\sum xy = 47$. $D = 120 - 100 = 20$, $b = (188 - 160)/20 = 1.4$, $a = (480 - 470)/20 = 0.5$: the line $y = 0.5 + 1.4x$.')),
                 dict(ic='🖼️', h='Computer graphics: undo a transform', t='Which input pixel lands at this output pixel?',
                      detail=dict(where='image warping (rotate, shear, scale). To fill output pixel $\\mathbf{p}$, the program looks up input pixel $M^{-1}\\mathbf{p}$; the 2×2 inverse formula is applied for every pixel.',
                                  eq='M = \\begin{pmatrix} 2 & 1 \\\\ 1 & 1\\end{pmatrix}, \\quad M^{-1} = \\frac{1}{1}\\begin{pmatrix} 1 & -1 \\\\ -1 & 2\\end{pmatrix}',
                                  steps=['Output pixel $(3, 2)$', 'Source: $M^{-1}(3, 2) = (3 - 2, \\; -3 + 4) = (1, 1)$', 'Check: $M(1, 1) = (2 + 1, \\; 1 + 1) = (3, 2)$ ✓', 'Copy the colour of input pixel $(1, 1)$ to output $(3, 2)$'],
                                  note='Here the inverse is worth computing: the same tiny matrix is used millions of times.')),
                 dict(ic='🔐', h='Hill cipher (cryptography)', t='Decrypt by multiplying with the inverse key, mod 26',
                      detail=dict(where='the Hill cipher, a classic matrix cipher. Letters become numbers (A = 0, …, Z = 25); pairs are multiplied by a key matrix $K$ mod 26. Decryption needs $K^{-1}$ mod 26, built with the adjugate formula.',
                                  eq='K = \\begin{pmatrix} 3 & 3 \\\\ 2 & 5\\end{pmatrix}, \\; \\det K = 9, \\; 9^{-1} \\equiv 3 \\pmod{26}, \\; K^{-1} \\equiv 3\\begin{pmatrix} 5 & -3 \\\\ -2 & 3\\end{pmatrix} \\equiv \\begin{pmatrix} 15 & 17 \\\\ 20 & 9\\end{pmatrix}',
                                  steps=['Encrypt "HI" = (7, 8): $K(7, 8) = (45, 54) \\equiv (19, 2)$ = "TC"', 'Decrypt: $K^{-1}(19, 2) = (319, 398) \\equiv (7, 8)$ = "HI" ✓', 'Division by $\\det K$ becomes multiplication by $9^{-1} \\bmod 26$'],
                                  note='The adjugate formula works in modular arithmetic, where Gaussian elimination with decimals would not.'))],
             notes="The regression card connects to machine learning: the slope formula students memorise in statistics is Cramer's rule applied to the normal equations."),
        dict(type='check', id='check', q='Cramer\'s rule for $2x + 3y = 8$, $\\;4x - y = 2$. What is $D_y$?',
             opts=['$-28$', '$28$', '$-14$', '$2$'], right=0,
             answer='A. $D = (2)(-1) - (3)(4) = -14$. $D_y = \\begin{vmatrix} 2 & 8 \\\\ 4 & 2\\end{vmatrix} = 4 - 32 = -28$, so $y = 2$; $D_x = -8 - 6 = -14$, so $x = 1$.',
             notes="Common wrong answer: 28 (computing 8·4 − 2·2). Remind: replace the y column by b, keep the order of the rows."),
        dict(type='summary', id='summary', items=[
            '$A\\mathbf{x} = \\mathbf{b}$ has a unique solution exactly when $\\det A \\ne 0$',
            'Cramer: $x_i = D_i/D$; inverse: $A^{-1} = \\operatorname{adj}A/\\det A$; both fine for 2×2 and 3×3',
            'Cofactor determinants cost about $e\\cdot n!$: hopeless beyond $n \\approx 12$',
            'Norms measure size; $\\kappa(A) = \\|A\\|\\|A^{-1}\\|$ measures sensitivity; about $\\log_{10}\\kappa$ digits are lost'],
            hw=['Solve $2x + y + z = 7$, $\\;x - y + 2z = 5$, $\\;3x + 2y - z = 4$ by Cramer\'s rule.', 'Find the inverses of $\\begin{pmatrix} 2 & 1 \\\\ 5 & 3\\end{pmatrix}$ and $\\begin{pmatrix} 1 & 0 & 2 \\\\ 2 & -1 & 3 \\\\ 4 & 1 & 8\\end{pmatrix}$.',
                'For $A = \\begin{pmatrix} 4 & 1 \\\\ 2 & 3\\end{pmatrix}$ find $\\|A\\|_1$, $\\|A\\|_\\infty$, $A^{-1}$ and $\\kappa_\\infty(A)$.', 'With the cost explorer (or the lab program), find the smallest $n$ for which Cramer\'s rule takes more than one hour.'],
            solved='Cramer: $D = 291$, $D_1 = 582$, $D_2 = D_3 = 291$, so $I = (2, 1, 1)$ A. The inverse gives the same. For 25 loops, Cramer would need $3.5\\times10^{10}$ years: we need elimination.',
            next='<b>Gaussian and Gauss–Jordan elimination.</b> The systematic version of school elimination: $\\tfrac23 n^3$ operations, and pivoting to protect against rounding.',
            notes="Homework answers: Q1: D = 6, D1 = 6, D2 = 12, D3 = 18, so (1, 2, 3). Q2: [[3, −1], [−5, 2]] (det 1); 3×3: det = 1, inverse [[−11, 2, 2], [−4, 0, 1], [6, −1, −1]]. Q3: ‖A‖1 = 6, ‖A‖∞ = 5, A⁻¹ = (1/10)[[3, −1], [−2, 4]], ‖A⁻¹‖∞ = 0.6, κ∞ = 3. Q4: n = 15 (5.7×10¹³ operations, about 16 hours); n = 14 takes 59 minutes."),
    ],
    code={
        'cramer3': dict(file='cramer_inverse', py='''# Cramer's rule, inverse by cofactors, and the condition number (3x3)
def det3(M):
    return (M[0][0] * (M[1][1]*M[2][2] - M[1][2]*M[2][1])
          - M[0][1] * (M[1][0]*M[2][2] - M[1][2]*M[2][0])
          + M[0][2] * (M[1][0]*M[2][1] - M[1][1]*M[2][0]))

A = [[7.0, -2.0, 0.0], [-2.0, 9.0, -3.0], [0.0, -3.0, 6.0]]
b = [12.0, 2.0, 3.0]

D = det3(A)
print(f"D = {D:.6f}")
for i in range(3):                       # Cramer's rule
    Ai = [row[:] for row in A]
    for r in range(3):
        Ai[r][i] = b[r]
    Di = det3(Ai)
    print(f"D{i+1} = {Di:.6f}   x{i+1} = {Di / D:.6f}")

inv = [[0.0] * 3 for _ in range(3)]      # inverse = adj(A) / D
for i in range(3):
    for j in range(3):
        rows = [r for r in range(3) if r != i]
        cols = [c for c in range(3) if c != j]
        m = A[rows[0]][cols[0]] * A[rows[1]][cols[1]] - A[rows[0]][cols[1]] * A[rows[1]][cols[0]]
        inv[j][i] = (-1) ** (i + j) * m / D   # transpose!
for row in inv:
    print(" ".join(f"{v:10.6f}" for v in row))

normA = max(sum(abs(v) for v in row) for row in A)
normI = max(sum(abs(v) for v in row) for row in inv)
print(f"||A|| = {normA:.4f}  ||A^-1|| = {normI:.4f}  kappa = {normA * normI:.4f}")
''', c='''/* Cramer's rule, inverse by cofactors, and the condition number (3x3) */
#include <stdio.h>
#include <math.h>

double det3(double M[3][3]) {
    return M[0][0] * (M[1][1]*M[2][2] - M[1][2]*M[2][1])
         - M[0][1] * (M[1][0]*M[2][2] - M[1][2]*M[2][0])
         + M[0][2] * (M[1][0]*M[2][1] - M[1][1]*M[2][0]);
}

int main(void) {
    double A[3][3] = {{7, -2, 0}, {-2, 9, -3}, {0, -3, 6}};
    double b[3] = {12, 2, 3}, Ai[3][3], inv[3][3];
    double D = det3(A);
    printf("D = %.6f\\n", D);
    for (int i = 0; i < 3; i++) {                 /* Cramer's rule */
        for (int r = 0; r < 3; r++)
            for (int c = 0; c < 3; c++) Ai[r][c] = (c == i) ? b[r] : A[r][c];
        double Di = det3(Ai);
        printf("D%d = %.6f   x%d = %.6f\\n", i + 1, Di, i + 1, Di / D);
    }
    for (int i = 0; i < 3; i++)                   /* inverse = adj(A) / D */
        for (int j = 0; j < 3; j++) {
            int r0 = (i == 0) ? 1 : 0, r1 = (i == 2) ? 1 : 2;
            int c0 = (j == 0) ? 1 : 0, c1 = (j == 2) ? 1 : 2;
            double m = A[r0][c0] * A[r1][c1] - A[r0][c1] * A[r1][c0];
            inv[j][i] = (((i + j) % 2) ? -m : m) / D;   /* transpose! */
        }
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) printf(j ? " %10.6f" : "%10.6f", inv[i][j]);
        printf("\\n");
    }
    double normA = 0, normI = 0;
    for (int i = 0; i < 3; i++) {
        double s = 0, t = 0;
        for (int j = 0; j < 3; j++) { s += fabs(A[i][j]); t += fabs(inv[i][j]); }
        if (s > normA) normA = s;
        if (t > normI) normI = t;
    }
    printf("||A|| = %.4f  ||A^-1|| = %.4f  kappa = %.4f\\n", normA, normI, normA * normI);
    return 0;
}
'''),
        'cramercost': dict(file='cramer_cost', py='''# How many operations does Cramer's rule need? (cofactor determinants)
# One n x n determinant: T(n) = n*T(n-1) + 2n - 1, with T(1) = 0
# Cramer: (n + 1) determinants plus n divisions
speed = 1e9                      # operations per second
T = 0.0
for n in range(2, 26):
    T = n * T + 2 * n - 1
    ops = (n + 1) * T + n
    gauss = 2 * n**3 / 3 + 1.5 * n**2 - 7 * n / 6
    seconds = ops / speed
    print(f"n = {n:2d}  Cramer {ops:10.3e} ops = {seconds:10.3e} s   elimination {gauss:7.0f} ops")
''', c='''/* How many operations does Cramer's rule need? (cofactor determinants)
   One n x n determinant: T(n) = n*T(n-1) + 2n - 1, with T(1) = 0
   Cramer: (n + 1) determinants plus n divisions */
#include <stdio.h>

int main(void) {
    double speed = 1e9, T = 0.0;     /* operations per second */
    for (int n = 2; n <= 25; n++) {
        T = n * T + 2 * n - 1;
        double ops = (n + 1) * T + n;
        double gauss = 2.0 * n * n * n / 3 + 1.5 * n * n - 7.0 * n / 6;
        double seconds = ops / speed;
        printf("n = %2d  Cramer %10.3e ops = %10.3e s   elimination %7.0f ops\\n", n, ops, seconds, gauss);
    }
    return 0;
}
'''),
    },
    lab=dict(title='Cramer and Inverse Lab',
             intro='Solve your own systems by Cramer\'s rule and the adjugate inverse, measure conditioning, and see how fast the cost grows.',
             tabs=[
                 dict(name='Cramer solver', blocks=[
                     dict(p='Type any 2×2, 3×3 or 4×4 system as an augmented matrix [A | b]. The tool shows D, every Dᵢ with the replaced column shaded, and the solution: use it to check your hand calculations.'),
                     dict(w='cramer', o=dict(mat='1 1 1 6; 2 -1 1 3; 1 2 -1 2', presets=[['circuit', '7 -2 0 12; -2 9 -3 2; 0 -3 6 3'], ['Problem 4', '1 1 1 6; 2 -1 1 3; 1 2 -1 2'], ['2×2', '2 3 8; 4 -1 2'], ['singular', '1 2 3; 2 4 6']]))]),
                 dict(name='Inverse and κ', blocks=[
                     dict(p='Switch "Show" between the adjugate inverse and the norms. Try the nearly parallel system and compare κ with the circuit.'),
                     dict(w='cramer', o=dict(mat='7 -2 0 12; -2 9 -3 2; 0 -3 6 3', view='inv', presets=[['circuit', '7 -2 0 12; -2 9 -3 2; 0 -3 6 3'], ['nearly parallel', '1 1 2; 1 1.0001 2.0001'], ['homework 3', '4 1 1; 2 3 1'], ['homework 2', '1 0 2 1; 2 -1 3 1; 4 1 8 1']])),
                     dict(h='Ill-conditioning in pictures'),
                     dict(w='illcond', o=dict(preset='ill', height='300px'))]),
                 dict(name='Cost explorer', blocks=[
                     dict(p='Operation counts on a log scale. Move n and compare Cramer with elimination.'),
                     dict(w='cost', o=dict(n=10, height='340px'))]),
                 dict(name='Code', blocks=[
                     dict(h='Cramer, inverse and κ'), dict(code='cramer3', tasks=['Run it. Check D and x against Problem 1.', 'Change b to (0, 0, 9). Which currents change most?', 'Replace A by the homework 1 system (2 1 1 / 1 −1 2 / 3 2 −1, b = 7 5 4).']),
                     dict(h='Cost of Cramer\'s rule'), dict(code='cramercost', tasks=['Run it. For which n does Cramer first take more than one second? one hour?', 'Change speed to 1e12 (a fast GPU). Does that rescue Cramer for n = 25?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Solve $x + y + z = 6$, $2x - y + z = 3$, $x + 2y - z = 2$ by Cramer\'s rule.', '$D = 1(1 - 2) - 1(-2 - 1) + 1(4 + 1) = 7$. $D_1 = 7$, $D_2 = 14$, $D_3 = 21$. So $x = 1$, $y = 2$, $z = 3$.'),
                         ('Find the inverse of $\\begin{pmatrix} 1 & 2 & 3 \\\\ 0 & 1 & 4 \\\\ 5 & 6 & 0\\end{pmatrix}$.', '$\\det = 1(0 - 24) - 2(0 - 20) + 3(0 - 5) = 1$. $A^{-1} = \\begin{pmatrix} -24 & 18 & 5 \\\\ 20 & -15 & -4 \\\\ -5 & 4 & 1\\end{pmatrix}$.'),
                         ('Find $\\|\\mathbf{v}\\|_1$, $\\|\\mathbf{v}\\|_2$, $\\|\\mathbf{v}\\|_\\infty$ for $\\mathbf{v} = (3, -4, 1)$, and $\\|A\\|_1$, $\\|A\\|_\\infty$ for $A = \\begin{pmatrix} 1 & -2 \\\\ 3 & 4\\end{pmatrix}$.', '$8$, $\\sqrt{26} = 5.099$, $4$. Column sums 4 and 6: $\\|A\\|_1 = 6$. Row sums 3 and 7: $\\|A\\|_\\infty = 7$.'),
                         ('Why is Cramer\'s rule not used for a system of 20 equations?', 'It needs 21 determinants of size 20; by cofactor expansion that is about $1.4\\times10^{20}$ operations (about 4400 years at $10^9$ per second). Gaussian elimination needs about $\\tfrac23 20^3 \\approx 5900$ operations.'),
                         ('A matrix has $\\kappa(A) = 10^6$ and the data $\\mathbf{b}$ are correct to 8 significant digits. How many digits of $\\mathbf{x}$ can you trust?', 'About $8 - \\log_{10}10^6 = 2$ significant digits.')])])]),
)
