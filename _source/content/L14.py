LECTURE = dict(
    title='Iterative Methods: Jacobi, Gauss–Seidel and SOR',
    short='Jacobi, Gauss–Seidel and SOR',
    sub='When the matrix is huge and mostly zeros, stop eliminating and start iterating: Jacobi and Gauss–Seidel as fixed-point iteration with matrices, diagonal dominance, eigenvalues and the spectral radius, and over-relaxation (SOR).',
    slides=[
        dict(type='cover', id='cover', notes="Recap: direct methods cost about n³ and store n² numbers. Ask: what is 10⁶ cubed? (10¹⁸.) And how much memory is 10¹² doubles? (8 TB.)\n\nToday's methods never form the full matrix. They take a guess and improve it, exactly like fixed-point iteration in Lecture 8."),
        dict(type='bullets', id='hook', title='The problem: a plate with a million grid points', kick='Why this lecture', rw=700,
             lead='The plate from Lecture 12, now on a fine grid so that the temperature map is smooth.',
             items=['A 100 × 100 grid: 10 000 unknowns; the full matrix has $10^8$ entries (800 MB) but only 5 per row are nonzero: <b>99.95% zeros</b>',
                    'A 1000 × 1000 grid: $10^6$ unknowns; dense elimination needs 8 TB and about 21 years',
                    'Yet each equation is tiny: <b>"each temperature is the average of its four neighbours"</b>',
                    'Idea: guess all temperatures, then keep replacing each one by the average of its neighbours'],
             frag=True,
             right=dict(stack=[dict(eq='T_{i,j} = \\tfrac14\\big(T_{i-1,j} + T_{i+1,j} + T_{i,j-1} + T_{i,j+1}\\big)', cap='One equation per grid point'),
                               dict(card=dict(cls='blue', tag='The question', t='Does repeated averaging converge to the solution? How fast? Can we make it faster?'))]),
             notes="Ask the class to imagine doing the averaging by hand on the 4-point plate from Lecture 12, starting from all zeros: after one sweep T1 = (100 + 0 + 0 + 0)/4 = 25. That is exactly Jacobi's method, the first row of today's table.\n\nSolved at the end: the 4-point plate in 19 Jacobi sweeps or 11 Gauss–Seidel sweeps; the million-point plate by SOR in about 2200 sweeps (11 s)."),
        dict(type='goals', id='goals', items=[
            'Derive <b>Jacobi</b> and <b>Gauss–Seidel</b> as fixed-point iteration $\\mathbf{x} = T\\mathbf{x} + \\mathbf{c}$',
            'Carry out both by hand and present the iteration table',
            'Test convergence with <b>diagonal dominance</b>, and explain it with <b>eigenvalues</b> and the <b>spectral radius</b> $\\rho(T)$',
            'Speed up Gauss–Seidel with <b>SOR</b> and choose the relaxation factor $\\omega$',
            'Decide between direct and iterative solvers'],
            prev='LU, Cholesky, Thomas: exact after a fixed number of steps, but fill-in and $n^3$ for big 2-D problems.',
            today='Guess, improve, repeat: the matrix version of Lecture 8.',
            notes="The eigenvalue recap is part of today: students met eigenvalues in linear algebra; here they finally see what they are for."),
        dict(type='math', id='idea', title='The idea: solve each equation for its own unknown',
             eqs=[dict(cap='Jacobi: every update uses only the old values', eq='x_i^{(k+1)} = \\frac{1}{a_{ii}}\\Big(b_i - \\sum_{j \\ne i} a_{ij}\\,x_j^{(k)}\\Big), \\qquad i = 1, \\dots, n'),
                  dict(cap='Matrix form, with A = D + L + U (diagonal, strictly lower, strictly upper)', eq='\\mathbf{x}^{(k+1)} = \\underbrace{-D^{-1}(L + U)}_{T_J}\\,\\mathbf{x}^{(k)} + D^{-1}\\mathbf{b}', frag=True)],
             items=['Exactly fixed-point iteration $\\mathbf{x} = g(\\mathbf{x})$ from Lecture 8, with vectors', 'Needs every $a_{ii} \\ne 0$', 'One sweep costs about 2 × (number of nonzeros): the zeros are never touched',
                    'The order of the equations matters: each one is solved for <b>its diagonal</b> unknown'],
             ifrag=True,
             notes="For the plate, a_ii = 4 and the off-diagonal entries are −1, so the Jacobi formula is literally 'average of the four neighbours'.\n\nL and U here are the strictly lower and upper parts of A, not the LU factors of Lecture 13. Point this out to avoid confusion."),
        dict(type='bullets', id='algo', title="Jacobi's method, step by step", kick='The method, step by step', ordered=True, rw=780,
             items=['Check (or arrange) that the system is diagonally dominant', 'Rewrite equation $i$ as $x_i = (b_i - \\sum_{j\\ne i} a_{ij}x_j)/a_{ii}$', 'Choose a start, usually $\\mathbf{x}^{(0)} = \\mathbf{0}$',
                    'Compute <b>all</b> new $x_i$ from the old vector', 'Stop when $\\|\\mathbf{x}^{(k+1)} - \\mathbf{x}^{(k)}\\|_\\infty < \\varepsilon$; otherwise repeat step 4'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input A, b, x (start), tol, N\nrepeat up to N times:\n    for i = 1 … n:\n        s ← b[i] − Σ_{j≠i} a[i][j]·x[j]\n        x_new[i] ← s / a[i][i]\n    if max |x_new − x| &lt; tol:\n        return x_new\n    x ← x_new\nstop: no convergence</pre></div><p class="small" style="margin-top:14px">Two vectors: old and new. Every $x_i$ can be updated at the same time, so Jacobi runs well in parallel (GPUs).</p>'),
             notes="Step 1 is the one students skip. A written solution should state: |4| > |−1| + |1|, |−8| > |4| + |1|, |5| > |−2| + |1|, so the system is diagonally dominant and the iteration converges."),
        dict(type='table', id='p1', title='Problem 1: Jacobi iteration',
             q='Solve $4x - y + z = 7$, $\\;4x - 8y + z = -21$, $\\;-2x + y + 5z = 15$ from $(0, 0, 0)$. Iterate $x = \\frac{7 + y - z}{4}$, $\\;y = \\frac{21 + 4x + z}{8}$, $\\;z = \\frac{15 + 2x - y}{5}$.',
             head=['$k$', '$x^{(k)}$', '$y^{(k)}$', '$z^{(k)}$', 'largest change'], frag=True, ans=-1,
             rows=[[1, '1.750000', '2.625000', '3.000000', '3.00'], [2, '1.656250', '3.875000', '3.175000', '1.25'], [3, '1.925000', '3.850000', '2.887500', '0.288'],
                   [4, '1.990625', '3.948438', '3.000000', '0.112'], [5, '1.987109', '3.995313', '3.006563', '0.0469'], [6, '1.997188', '3.994375', '2.995781', '0.0108'],
                   [7, '1.999648', '3.998066', '3.000000', '0.00422'], [8, '1.999517', '3.999824', '3.000246', '0.00176']],
             note='Diagonally dominant, so it converges to $(2, 4, 3)$: 11 iterations for a change below $10^{-4}$, 15 for $10^{-6}$. Every row uses only the row above it.',
             notes="Row 2 in full: x = (7 + 2.625 − 3)/4 = 1.65625; y = (21 + 4(1.75) + 3)/8 = 31/8 = 3.875; z = (15 + 3.5 − 2.625)/5 = 3.175.\n\nNotice z returns to exactly 3 at k = 4 and k = 7: coincidences of this system, not a pattern."),
        dict(type='bullets', id='algo2', title='Gauss–Seidel, step by step', kick='The method, step by step', ordered=True, rw=780,
             lead='Use each new value <b>as soon as it is computed</b>: $\\;x_i^{(k+1)} = \\dfrac{1}{a_{ii}}\\Big(b_i - \\sum_{j<i} a_{ij}x_j^{(k+1)} - \\sum_{j>i} a_{ij}x_j^{(k)}\\Big)$',
             items=['Arrange the system so that it is diagonally dominant', 'Start with $\\mathbf{x}^{(0)}$ (often $\\mathbf{0}$)', 'Update $x_1$; then $x_2$ using the <b>new</b> $x_1$; then $x_3$ using the new $x_1, x_2$; …',
                    'Stop when the largest change in a sweep is below $\\varepsilon$', 'Matrix form: $(D + L)\\mathbf{x}^{(k+1)} = \\mathbf{b} - U\\mathbf{x}^{(k)}$'],
             frag=True,
             right=dict(html='<div class="card navy"><span class="tag" style="color:#f0a35e">Pseudocode</span><pre style="margin:0;font:500 27px/1.55 var(--mono);color:#f5f3ee">input A, b, x (start), tol, N\nrepeat up to N times:\n    change ← 0\n    for i = 1 … n:\n        s ← b[i] − Σ_{j≠i} a[i][j]·x[j]\n        new ← s / a[i][i]\n        change ← max(change, |new − x[i]|)\n        x[i] ← new        # overwrite now\n    if change &lt; tol: return x\nstop: no convergence</pre></div><p class="small" style="margin-top:14px">One vector, overwritten in place: less memory and usually about twice as fast as Jacobi.</p>'),
             notes="The only code difference from Jacobi: there is no x_new array. That one line changes the speed.\n\nDisadvantage: the updates are sequential, so Gauss–Seidel is harder to parallelise (red–black ordering fixes that)."),
        dict(type='table', id='p2', title='Problem 2: the same system by Gauss–Seidel',
             q='Same equations and start. Now each formula uses the newest values: $y$ uses the new $x$; $z$ uses the new $x$ and $y$.',
             head=['$k$', '$x^{(k)}$', '$y^{(k)}$', '$z^{(k)}$', 'largest change'], frag=True, ans=-1,
             rows=[[1, '1.750000', '3.500000', '3.000000', '3.50'], [2, '1.875000', '3.937500', '2.962500', '0.438'], [3, '1.993750', '3.992188', '2.999063', '0.119'],
                   [4, '1.998281', '3.999023', '2.999508', '0.00683'], [5, '1.999879', '3.999878', '2.999976', '0.00160'], [6, '1.999975', '3.999985', '2.999993', '0.000107'],
                   [7, '1.999998', '3.999998', '3.000000', '0.0000231']],
             note='7 iterations for $10^{-4}$ (Jacobi: 11) and 9 for $10^{-6}$ (Jacobi: 15). Row 1: $x = 7/4$; $y = (21 + 4(1.75) + 0)/8 = 3.5$; $z = (15 + 2(1.75) - 3.5)/5 = 3$.',
             notes="Put the Jacobi and Gauss–Seidel tables side by side. The Gauss–Seidel y in row 1 (3.5) is already much closer to 4 than Jacobi's (2.625), because it used the new x."),
        dict(type='widget', id='explore', title='Explore: Jacobi and Gauss–Seidel in pictures', w='iter2d',
             o=dict(mat='4 -1 3; -2 5 3', method='jacobi', step=3, height='380px', side=True, tableHeight='380px',
                    presets=[['diagonally dominant', '4 -1 3; -2 5 3', 'jacobi'], ['Gauss–Seidel', '4 -1 3; -2 5 3', 'gs'], ['rows swapped', '-2 5 3; 4 -1 3', 'jacobi'], ['weakly dominant', '1 0.9 1.9; 0.9 1 1.9', 'gs']]), lw=440,
             items=['Two equations, two lines; the solution is where they cross', '<b>Gauss–Seidel</b>: move horizontally to line 1, then vertically to line 2: a staircase', '<b>Jacobi</b>: both moves from the old point at once', 'Swap the rows: the same lines, but the iteration runs away'],
             notes="Start with Jacobi (3 steps), then switch the method to Gauss–Seidel: the staircase reaches the crossing in about half as many steps.\n\nThen the 'rows swapped' preset: the same two lines, but now each equation is solved for the 'wrong' unknown, ρ = 3.16 > 1, and the points shoot off. The order of the equations matters.\n\nThe 'weakly dominant' preset (nearly parallel lines, ρ_GS = 0.81) shows slow convergence."),
        dict(type='math', id='conv', title='When does it converge?',
             eqs=[dict(cap='Strict diagonal dominance in every row ⇒ Jacobi and Gauss–Seidel converge from any start', eq='|a_{ii}| > \\sum_{j \\ne i} |a_{ij}|, \\qquad i = 1, \\dots, n'),
                  dict(cap='The real reason: the error is multiplied by T at every step', eq='\\mathbf{e}^{(k+1)} = T\\,\\mathbf{e}^{(k)} \\;\\Rightarrow\\; \\mathbf{e}^{(k)} = T^k\\mathbf{e}^{(0)} \\to \\mathbf{0} \\iff \\rho(T) < 1', frag=True)],
             items=['$\\rho(T) = \\max|\\lambda_i(T)|$, the <b>spectral radius</b>: the matrix version of $|g\'(r)|$ in Lecture 8', 'Each iteration multiplies the error by about $\\rho$: about $d/(-\\log_{10}\\rho)$ iterations for $d$ digits',
                    'Diagonal dominance is <b>sufficient</b>, not necessary', 'For many matrices (including the plate): $\\rho(T_{GS}) = \\rho(T_J)^2$, so Gauss–Seidel needs half as many iterations'],
             ifrag=True,
             notes="Why dominance works: ‖T_J‖∞ = max over rows of Σ_{j≠i}|a_ij|/|a_ii| < 1 exactly when A is strictly diagonally dominant, and ρ(T) ≤ ‖T‖.\n\nThe last bullet holds for 'consistently ordered' matrices, which include tridiagonal matrices and the 5-point plate matrix."),
        dict(type='math', id='eig', title='Recap: eigenvalues and the spectral radius',
             eqs=[dict(cap='Eigenvalue λ and eigenvector v', eq='T\\mathbf{v} = \\lambda\\mathbf{v}, \\;\\mathbf{v} \\ne \\mathbf{0} \\quad\\Longleftrightarrow\\quad \\det(T - \\lambda I) = 0'),
                  dict(cap='2×2: the characteristic equation', eq='\\lambda^2 - (\\operatorname{tr} T)\\,\\lambda + \\det T = 0, \\qquad \\rho(T) = \\max(|\\lambda_1|, |\\lambda_2|)', frag=True)],
             items=['Along an eigenvector, $T^k\\mathbf{v} = \\lambda^k\\mathbf{v}$: it shrinks if $|\\lambda| < 1$, grows if $|\\lambda| > 1$', 'Any error is a mix of eigenvectors, so the largest $|\\lambda|$ wins in the end', '$\\rho < 1$: the iteration is a contraction, like $|g\'| < 1$',
                    'Eigenvalues return in ODE stability (Lecture 22) and in optimisation (Lecture 25)'],
             ifrag=True,
             notes="Keep it concrete: one 2×2 example on the next slide. Students who have forgotten eigenvalues only need the characteristic equation for 2×2."),
        dict(type='worked', id='p3', title='Problem 3: predict the speed from ρ',
             q='For $4x - y = 3$, $\\;-2x + 5y = 3$ (solution $(1, 1)$), find $\\rho(T_J)$ and $\\rho(T_{GS})$.',
             steps=['$T_J = -D^{-1}(L + U) = \\begin{pmatrix} 0 & 1/4 \\\\ 2/5 & 0\\end{pmatrix}$: $\\;\\lambda^2 - 0\\cdot\\lambda - \\tfrac{1}{10} = 0$, so $\\lambda = \\pm 0.3162$ and $\\rho(T_J) = 0.3162$',
                    'Gauss–Seidel: $x_{new} = (3 + y)/4$, then $y_{new} = (3 + 2x_{new})/5 = \\ldots + \\tfrac{1}{10}y$, so $T_{GS} = \\begin{pmatrix} 0 & 1/4 \\\\ 0 & 1/10\\end{pmatrix}$ with eigenvalues $0$ and $0.1$',
                    '$\\rho(T_{GS}) = 0.1 = \\rho(T_J)^2$: each Gauss–Seidel step gains one digit; each Jacobi step half a digit',
                    'Prediction for 6 digits: Jacobi about 12 steps, Gauss–Seidel about 6. Observed (change $< 10^{-6}$): 13 and 8'],
             answer='Both converge (ρ < 1). Gauss–Seidel is twice as fast, as the spectral radii predict.',
             right=dict(w='iter2d', o=dict(mat='4 -1 3; -2 5 3', method='gs', step=4, height='300px', side=True, tableHeight='300px')), rw=900,
             notes="The observed counts are slightly larger than the predictions because the stopping test measures the change between iterates, not the true error, and because the first steps include a transient.\n\nThe widget prints ρ for the selected method: switch between Jacobi and Gauss–Seidel to compare."),
        dict(type='math', id='sor', title='Over-relaxation (SOR): push past the Gauss–Seidel value',
             eqs=[dict(cap='SOR with relaxation factor ω; x̃ᵢ is the Gauss–Seidel value', eq='x_i^{(k+1)} = (1 - \\omega)\\,x_i^{(k)} + \\omega\\,\\tilde{x}_i'),
                  dict(cap='Best ω for the N × N plate', eq='\\omega_{opt} = \\frac{2}{1 + \\sin\\big(\\pi/(N+1)\\big)}, \\qquad \\rho(T_{\\omega_{opt}}) = \\omega_{opt} - 1', frag=True)],
             items=['$\\omega = 1$: Gauss–Seidel. $1 < \\omega < 2$: over-relaxation (go further in the same direction)', 'Converges only for $0 < \\omega < 2$ (for SPD matrices: for all of them)',
                    'Same cost per sweep as Gauss–Seidel: one extra multiply per unknown', 'Plate, 10 × 10 grid: Gauss–Seidel 132 sweeps, SOR with $\\omega = 1.56$: <b>31 sweeps</b>'],
             ifrag=True,
             notes="Algorithm: exactly the Gauss–Seidel pseudocode with the overwrite line replaced by x[i] ← x[i] + ω·(new − x[i]).\n\nSweep counts from the plate widget (edges 100, 50, 0, 0; stop when the largest change is below 10⁻⁴): N = 10: Jacobi 245, Gauss–Seidel 132, SOR(1.56) 31. N = 20: 786, 424, and 56 with ω = 1.74."),
        dict(type='widget', id='plate', title='Explore: the heat plate by Jacobi, Gauss–Seidel and SOR', w='plate', o=dict(N=10, omega=1.56, height='300px'), lw=520,
             items=['Each curve: largest change per sweep (log scale)', 'Gauss–Seidel ≈ twice as fast as Jacobi; SOR with a good ω is much faster again', 'Increase N: Jacobi and Gauss–Seidel slow down sharply ($\\rho \\to 1$)', 'Press <b>use best ω</b> and compare'],
             frag=True,
             notes="Try N = 2 first: that is the opening 4-unknown plate (Jacobi 19, Gauss–Seidel 11). Then N = 10 and N = 20 with the best ω. Then set ω = 1.95: too much over-relaxation slows SOR down again.\n\nThe heat map shows the SOR solution: hot near the top edge, warm on the right."),
        dict(type='compare', id='classic', title='Same plate, two approaches', kick='Classical vs numerical', mid='vs',
             left=dict(h='Direct (Gaussian elimination)', tag='Exact after fixed steps', cls='blue', items=['4 unknowns: 62 operations, exact', '$T = (43.75, 56.25, 18.75, 31.25)$', 'Stores and fills the whole matrix']),
             right=dict(h='Iterative (Gauss–Seidel)', tag='Improves a guess', cls='key', items=['4 unknowns: 11 sweeps to a change below $10^{-4}$', '$T = (43.75, 56.25, 18.75, 31.25)$ to 4 decimals', 'Stores only the grid of temperatures']),
             frag=True, below=dict(html='<div class="card bad frag fade"><span class="tag">When the direct approach cannot work</span><h3>A 1000 × 1000 grid: $10^6$ unknowns</h3><p>Dense elimination: 8 TB of memory and $6.7\\times10^{17}$ operations (21 years at $10^9$ per second). SOR with the best ω: about 2200 sweeps of $5\\times10^6$ operations, <b>about 11 seconds</b> and 8 MB. Jacobi would need about 2.8 million sweeps (4 hours): the method and ω matter.</p></div>'),
             notes="Estimates: ρ_J = cos(π/1001) = 0.999995 (2.8×10⁶ sweeps for 10⁻⁶); ρ_GS = ρ_J² (1.4×10⁶); ρ_SOR = 0.99374 (2.2×10³). Each sweep ≈ 5 operations per unknown.\n\nModern solvers (conjugate gradient, multigrid) do even better; SOR is the classical stepping stone."),
        dict(type='code', id='code', title='Jacobi and Gauss–Seidel in Python and C', code='jacobigs', lw=560,
             items=['Same system as Problems 1 and 2', 'Jacobi keeps an old and a new vector', 'Gauss–Seidel overwrites in place', 'Both stop when the largest change is below $10^{-6}$'],
             notes="Run both tabs: Jacobi 15 iterations, Gauss–Seidel 9. Lab task: swap the first two equations and watch both diverge."),
        dict(type='widget', id='fail', title='Limitations shown failing', kick='When iteration does not work', w='iter2d',
             o=dict(mat='-2 5 3; 4 -1 3', method='jacobi', step=4, height='330px', side=True, tableHeight='330px', presets=[['rows swapped', '-2 5 3; 4 -1 3', 'jacobi'], ['fixed by reordering', '4 -1 3; -2 5 3', 'jacobi'], ['slow: nearly parallel', '1 0.9 1.9; 0.9 1 1.9', 'gs'], ['ω too large', '4 -1 3; -2 5 3', 'sor']]), lw=560,
             items=['<b>Not diagonally dominant</b>: the same system with rows swapped has $\\rho = 3.16$; the iterates explode', 'Fix: <b>reorder the equations</b> so the largest coefficient of each row is on the diagonal',
                    '<b>Slow</b> when $\\rho$ is close to 1: nearly parallel lines, fine grids (Jacobi needs millions of sweeps)', '<b>Accuracy</b> only to the tolerance, and a small change is not always a small error when $\\rho \\approx 1$'],
             frag=True,
             notes="For the 'ω too large' preset, set ω to 1.9 with the slider: the iterates overshoot back and forth. Above 2 SOR always diverges.\n\nLast bullet: if ρ = 0.999, a change of 10⁻⁶ per step can still mean an error near 10⁻³ (error ≈ change × ρ/(1 − ρ))."),
        dict(type='exam', id='practice', src='Problem 4',
             q='"Solve by the Gauss–Seidel method, correct to three decimal places: $x + y + 54z = 110$, $\\;27x + 6y - z = 85$, $\\;6x + 15y + 2z = 72$."',
             tips=['As written the system is not diagonally dominant: <b>reorder</b> to $27x + 6y - z = 85$, $6x + 15y + 2z = 72$, $x + y + 54z = 110$ and say why', 'Write the three update formulas: $x = (85 - 6y + z)/27$, $y = (72 - 6x - 2z)/15$, $z = (110 - x - y)/54$',
                   'Table from $(0, 0, 0)$: $(3.1481, 3.5407, 1.9132)$, $(2.4322, 3.5720, 1.9258)$, $(2.4257, 3.5729, 1.9260)$, $(2.4255, 3.5730, 1.9260)$', 'Stop when two iterations agree to 3 decimals: $x = 2.426$, $y = 3.573$, $z = 1.926$'],
             notes=""),
        dict(type='profile', id='profile', title='Jacobi, Gauss–Seidel and SOR: method profile',
             best=['Huge sparse systems from grids: memory and work proportional to the number of nonzeros', 'Diagonally dominant or SPD matrices: guaranteed convergence', 'A good starting guess (the previous time step): few sweeps needed'],
             worst=['Not diagonally dominant and $\\rho(T) \\ge 1$: divergence', '$\\rho$ close to 1 (fine grids): Jacobi and Gauss–Seidel crawl', 'Small dense systems: elimination is faster and exact'],
             suited=['Heat, flow and electrostatics on grids (Laplace and Poisson equations)', 'Jacobi: parallel hardware (GPUs); Gauss–Seidel: sequential code, less memory', 'Smoothers inside multigrid; PageRank-type ranking iterations'],
             avoid=['Dense matrices with $n$ in the thousands (use LU)', 'Problems needing many digits from a slowly converging iteration', 'Indefinite or non-dominant matrices (use Krylov methods such as GMRES)'],
             verdict='Rule of thumb: <b>sparse and huge → iterate (SOR or better); dense or small → factor</b>. Always check dominance or $\\rho < 1$ first.',
             notes="Conjugate gradient (for SPD) and multigrid are the modern successors; mention them so students know the names."),
        dict(type='table', id='compare', title='Comparative analysis: iterative and direct solvers', cls='tb sm',
             head=['Method', 'Cost per sweep', 'Converges when', 'Plate $10\\times10$', 'Plate $1000\\times1000$', 'Parallel?'], tx=(0, 2), frag=True,
             rows=[['Jacobi', '≈ 2·nonzeros', 'diag. dominant, $\\rho(T_J) < 1$', '245 sweeps', '≈ 4 hours', '<span class="gr">yes</span>'], ['Gauss–Seidel', '≈ 2·nonzeros', 'diag. dominant or SPD', '132 sweeps', '≈ 2 hours', 'partly (red–black)'],
                   ['SOR, best ω', '≈ 2·nonzeros + n', 'SPD and $0 < \\omega < 2$', '31 sweeps', '≈ 11 s', 'partly'], ['Gaussian elimination (dense)', '$\\tfrac23 n^3$ once', 'nonsingular', '0.7 ms', '21 years, 8 TB', 'yes (blocks)'],
                   ['Banded LU (bandwidth $N$)', '≈ $2nN^2$ once', 'nonsingular', '0.02 ms', '≈ 33 min, 8 GB', 'partly']],
             note='Times at $10^9$ operations per second; sweep counts from the plate tool (edges 100, 50, 0, 0; change below $10^{-4}$); the $1000\\times1000$ estimates use $\\rho$ and a $10^{-6}$ error reduction.', notefrag=True,
             notes="Banded LU: the plate matrix has bandwidth N; elimination fills the band, about 2nN² = 2×10⁶×10⁶ = 2×10¹² operations for N = 1000 (about 33 minutes) and n·N doubles = 8 GB. For N = 10: 2×100×100 = 2×10⁴ operations."),
        dict(type='bridge', id='bridge', title='End of Module 3: where linear systems appear next', lead='We can now solve linear systems of any size and shape. They return all through the course:',
             keep=['Cramer and the inverse for 2×2 and 3×3 by hand', 'Elimination with pivoting, LU, Cholesky, Thomas', 'Jacobi, Gauss–Seidel, SOR for huge sparse systems', 'Norms, condition number, spectral radius'],
             rows=[['Splines need a tridiagonal solve', 'Thomas algorithm', 18],
                   ['Implicit ODE methods solve a system each step; stability is about eigenvalues', 'LU reuse; $\\rho$ and $|\\lambda h|$', 22],
                   ['Fitting a model to data: more equations than unknowns', 'Least squares: normal equations (Cholesky)', 23],
                   ['Training ML models: minimise a loss', 'Gradient descent: an iterative method like these', 25]],
             notes="This closes the module. Next module (Lectures 15–18): interpolation, starting with finite difference operators."),
        dict(type='apps', id='apps', n=2, lead='Click a card to see an iterative linear solver inside a real system.',
             items=[
                 dict(ic='🔎', h='Google PageRank', t='Ranking web pages by iterating a huge sparse system',
                      detail=dict(where='web search. The rank of a page is a weighted vote of the pages that link to it; for billions of pages this linear system is solved by iteration, never by elimination.',
                                  eq='\\mathbf{r}^{(k+1)} = 0.85\\,P\\,\\mathbf{r}^{(k)} + \\frac{0.15}{n}\\mathbf{1}, \\qquad P_{ij} = \\frac{1}{\\text{outlinks}(j)} \\text{ if } j \\to i',
                                  table=[['iteration', 'page 1', 'page 2', 'page 3', 'page 4'], [['0', '0.25', '0.25', '0.25', '0.25'], ['1', '0.2500', '0.1438', '0.5688', '0.0375'], ['2', '0.5209', '0.1438', '0.2978', '0.0375'], ['3', '0.2906', '0.2589', '0.4130', '0.0375'], ['28', '0.3725', '0.1958', '0.3941', '0.0375']]],
                                  note='Links: 1 → 2, 1 → 3, 2 → 3, 3 → 1, 4 → 3. Page 3 (three incoming links) and page 1 (linked from the popular page 3) rank highest; page 4 has no incoming links. Converged after 28 iterations: the matrix 0.85P has spectral radius 0.85.')),
                 dict(ic='⚡', h='Power systems: Gauss–Seidel load flow', t='Voltages at every bus of an electricity grid',
                      detail=dict(where='power-system analysis (a standard EEE course method). Each bus gives one complex equation linking its voltage to its neighbours through the admittance matrix $Y$, which is sparse.',
                                  eq='V_i^{(k+1)} = \\frac{1}{Y_{ii}}\\left(\\frac{P_i - jQ_i}{\\big(V_i^{(k)}\\big)^*} - \\sum_{m < i} Y_{im}V_m^{(k+1)} - \\sum_{m > i} Y_{im}V_m^{(k)}\\right)',
                                  steps=['Start every bus at 1.0 per unit (flat start)', 'Sweep the buses in order, using the newest voltages (Gauss–Seidel)', 'Often accelerated with a factor of about 1.6 (that is SOR)', 'Stop when no voltage changes by more than about $10^{-4}$ per unit'],
                                  note='Large grids today use Newton\'s method (Lecture 10) with sparse LU, but Gauss–Seidel load flow is still taught and used for its simplicity.')),
                 dict(ic='🖼️', h='Filling a hole in an image', t='Inpainting by repeated averaging',
                      detail=dict(where='image editing ("remove object" or repairing scratches). Missing pixels are filled so that each one is the average of its neighbours, with the surrounding pixels as fixed boundary values: the plate equation again.',
                                  w='plate', o=dict(N=12, bc=[200, 120, 40, 90], omega=1.6, height='200px'),
                                  note='Edges = known pixel brightness around the hole; the map shows the filled values. Real tools use the same idea with colour and with smarter weights.')),
                 dict(ic='🧠', h='Gradient descent is an iterative linear solver', t='The ML training loop, seen as Lecture 14',
                      detail=dict(where='machine learning. Fitting a linear model by minimising the squared error $\\tfrac12\\|X\\mathbf{w} - \\mathbf{y}\\|^2$ with gradient descent is the iteration below: a fixed-point iteration for the linear system $X^TX\\mathbf{w} = X^T\\mathbf{y}$.',
                                  eq='\\mathbf{w}^{(k+1)} = \\mathbf{w}^{(k)} - \\eta\\,X^T\\big(X\\mathbf{w}^{(k)} - \\mathbf{y}\\big) = \\underbrace{(I - \\eta X^TX)}_{T}\\,\\mathbf{w}^{(k)} + \\eta X^T\\mathbf{y}',
                                  steps=['Iteration matrix $T = I - \\eta X^TX$', 'Converges iff $\\rho(T) < 1$, i.e. learning rate $0 < \\eta < 2/\\lambda_{max}(X^TX)$', 'Speed set by $\\kappa(X^TX)$: elongated loss valleys mean $\\rho$ close to 1 and slow training', 'Momentum and Adam play the role that SOR plays here: they shrink the effective $\\rho$'],
                                  note='The spectral radius from today explains the learning-rate rule of Lecture 25.'))],
             notes="The PageRank numbers were computed with damping 0.85 from the uniform start, stopping when the largest change is below 10⁻⁶."),
        dict(type='check', id='check', q='One Gauss–Seidel step for $10x + y = 12$, $\\;x + 10y = 21$ from $(0, 0)$. What is $y^{(1)}$?',
             opts=['$2.1$', '$1.98$', '$1.2$', '$2.0$'], right=1,
             answer='B. $x^{(1)} = 12/10 = 1.2$; then $y^{(1)} = (21 - 1.2)/10 = 1.98$ (Gauss–Seidel uses the new $x$). Jacobi would give $y^{(1)} = 2.1$. The solution is $(1, 2)$.',
             notes="Option A is the Jacobi value: a good discussion point."),
        dict(type='summary', id='summary', items=[
            'Jacobi: solve row $i$ for $x_i$ using old values; Gauss–Seidel: use new values at once',
            'Both are fixed-point iterations $\\mathbf{x} = T\\mathbf{x} + \\mathbf{c}$; they converge iff $\\rho(T) < 1$ (diagonal dominance is enough)',
            'Gauss–Seidel is usually about twice as fast; SOR with a good $\\omega$ much faster',
            'Use iteration for huge sparse systems; factorisation for small or dense ones'],
            hw=['Solve $10x + y + z = 12$, $\\;x + 10y + z = 12$, $\\;x + y + 10z = 12$ by Jacobi and by Gauss–Seidel to 4 decimals. Compare the number of iterations.', 'Rearrange $x + 8y - 3z = 6$, $\\;9x + y + z = 11$, $\\;2x - y + 7z = 8$ to be diagonally dominant, then do three Gauss–Seidel iterations.',
                'Find $\\rho(T_J)$ and $\\rho(T_{GS})$ for $\\begin{pmatrix} 5 & 2 \\\\ 3 & 6\\end{pmatrix}$. Predict how many iterations each needs for 6 digits.', 'With the plate tool, find the best ω for $N = 20$ by experiment and compare it with the formula.'],
            solved='The 4-point plate: Jacobi reaches $(43.75, 56.25, 18.75, 31.25)$ in 19 sweeps, Gauss–Seidel in 11 (change below $10^{-4}$). The million-point plate: SOR with the best ω in about 2200 sweeps, roughly 11 seconds, where elimination would need 8 TB.',
            next='<b>Module 4: finite differences and interpolation.</b> The operators $\\Delta$, $\\nabla$, $\\delta$, $E$ and how they generate every interpolation formula.',
            notes="Homework answers: Q1: solution (1, 1, 1); diagonally dominant. Jacobi from 0: (1.2, 1.2, 1.2), (0.96, 0.96, 0.96), (1.008, …), converges in about 8 iterations to 4 decimals; Gauss–Seidel about 5. Q2: order 9x + y + z = 11, x + 8y − 3z = 6, 2x − y + 7z = 8; solution (1, 1, 1); GS from 0: (1.2222, 0.5972, 0.8790), (1.0582, 0.9473, 0.9758), (1.0085, 0.9899, 0.9961). Q3: T_J = [[0, −0.4], [−0.5, 0]], ρ_J = √0.2 = 0.4472; ρ_GS = 0.2; 6 digits: Jacobi about 6/0.349 ≈ 17, Gauss–Seidel about 6/0.699 ≈ 9. Q4: formula ω = 2/(1 + sin(π/21)) = 1.74."),
    ],
    code={
        'jacobigs': dict(file='jacobi_gauss_seidel', py='''# Jacobi and Gauss-Seidel for 4x - y + z = 7, 4x - 8y + z = -21, -2x + y + 5z = 15
A = [[4.0, -1.0, 1.0], [4.0, -8.0, 1.0], [-2.0, 1.0, 5.0]]
b = [7.0, -21.0, 15.0]
n, tol = 3, 1e-6

print("Jacobi")
x = [0.0] * n
for k in range(1, 101):
    new = [(b[i] - sum(A[i][j] * x[j] for j in range(n) if j != i)) / A[i][i] for i in range(n)]
    change = max(abs(new[i] - x[i]) for i in range(n))
    x = new
    print(f"{k:3d}  " + "  ".join(f"{v:.6f}" for v in x) + f"   {change:.2e}")
    if change < tol:
        break

print("Gauss-Seidel")
x = [0.0] * n
for k in range(1, 101):
    change = 0.0
    for i in range(n):
        new = (b[i] - sum(A[i][j] * x[j] for j in range(n) if j != i)) / A[i][i]
        change = max(change, abs(new - x[i]))
        x[i] = new                        # use it immediately
    print(f"{k:3d}  " + "  ".join(f"{v:.6f}" for v in x) + f"   {change:.2e}")
    if change < tol:
        break
''', c='''/* Jacobi and Gauss-Seidel for 4x - y + z = 7, 4x - 8y + z = -21, -2x + y + 5z = 15 */
#include <stdio.h>
#include <math.h>
#define N 3

double A[N][N] = {{4, -1, 1}, {4, -8, 1}, {-2, 1, 5}};
double b[N] = {7, -21, 15};

double row_value(int i, double x[N]) {          /* (b_i - sum_{j != i} a_ij x_j) / a_ii */
    double s = b[i];
    for (int j = 0; j < N; j++) if (j != i) s -= A[i][j] * x[j];
    return s / A[i][i];
}

int main(void) {
    double x[N], xn[N], tol = 1e-6;
    printf("Jacobi\\n");
    for (int i = 0; i < N; i++) x[i] = 0;
    for (int k = 1; k <= 100; k++) {
        double change = 0;
        for (int i = 0; i < N; i++) xn[i] = row_value(i, x);
        for (int i = 0; i < N; i++) { if (fabs(xn[i] - x[i]) > change) change = fabs(xn[i] - x[i]); x[i] = xn[i]; }
        printf("%3d  %.6f  %.6f  %.6f   %.2e\\n", k, x[0], x[1], x[2], change);
        if (change < tol) break;
    }
    printf("Gauss-Seidel\\n");
    for (int i = 0; i < N; i++) x[i] = 0;
    for (int k = 1; k <= 100; k++) {
        double change = 0;
        for (int i = 0; i < N; i++) {
            double nw = row_value(i, x);
            if (fabs(nw - x[i]) > change) change = fabs(nw - x[i]);
            x[i] = nw;                           /* use it immediately */
        }
        printf("%3d  %.6f  %.6f  %.6f   %.2e\\n", k, x[0], x[1], x[2], change);
        if (change < tol) break;
    }
    return 0;
}
'''),
        'sorplate': dict(file='sor_plate', py='''# SOR on the N x N heat plate: how does the number of sweeps depend on omega?
import math
N = 10
top, right, bottom, left = 100.0, 50.0, 0.0, 0.0

def sweeps(w, tol=1e-4):
    T = [[0.0] * (N + 2) for _ in range(N + 2)]
    for j in range(1, N + 1):
        T[0][j] = top
        T[N + 1][j] = bottom
    for i in range(1, N + 1):
        T[i][0] = left
        T[i][N + 1] = right
    for k in range(1, 20001):
        change = 0.0
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                gs = 0.25 * (T[i-1][j] + T[i+1][j] + T[i][j-1] + T[i][j+1])
                new = T[i][j] + w * (gs - T[i][j])
                change = max(change, abs(new - T[i][j]))
                T[i][j] = new
        if change < tol:
            return k, T
    return None, T

print(f"best omega by formula: {2 / (1 + math.sin(math.pi / (N + 1))):.4f}")
for w in [1.0, 1.25, 1.5, 1.56, 1.75, 1.9]:
    k, T = sweeps(w)
    print(f"omega = {w:4.2f}: {k:4d} sweeps, T[5][5] = {T[5][5]:.4f}")
''', c='''/* SOR on the N x N heat plate: how does the number of sweeps depend on omega? */
#include <stdio.h>
#include <math.h>
#define N 10

double T[N + 2][N + 2];

int sweeps(double w, double tol) {
    for (int i = 0; i < N + 2; i++) for (int j = 0; j < N + 2; j++) T[i][j] = 0;
    for (int j = 1; j <= N; j++) { T[0][j] = 100; T[N + 1][j] = 0; }       /* top, bottom */
    for (int i = 1; i <= N; i++) { T[i][0] = 0; T[i][N + 1] = 50; }        /* left, right */
    for (int k = 1; k <= 20000; k++) {
        double change = 0;
        for (int i = 1; i <= N; i++)
            for (int j = 1; j <= N; j++) {
                double gs = 0.25 * (T[i-1][j] + T[i+1][j] + T[i][j-1] + T[i][j+1]);
                double nw = T[i][j] + w * (gs - T[i][j]);
                if (fabs(nw - T[i][j]) > change) change = fabs(nw - T[i][j]);
                T[i][j] = nw;
            }
        if (change < tol) return k;
    }
    return -1;
}

int main(void) {
    double ws[6] = {1.0, 1.25, 1.5, 1.56, 1.75, 1.9};
    printf("best omega by formula: %.4f\\n", 2 / (1 + sin(M_PI / (N + 1))));
    for (int r = 0; r < 6; r++) {
        int k = sweeps(ws[r], 1e-4);
        printf("omega = %4.2f: %4d sweeps, T[5][5] = %.4f\\n", ws[r], k, T[5][5]);
    }
    return 0;
}
'''),
    },
    lab=dict(title='Iterative Methods Lab',
             intro='Watch Jacobi, Gauss–Seidel and SOR converge (or diverge), measure the spectral radius, and tune ω on the heat plate.',
             tabs=[
                 dict(name='Two equations', blocks=[
                     dict(p='Type a 2×2 system as "a₁₁ a₁₂ b₁; a₂₁ a₂₂ b₂". Choose the method and step through. The note under the table gives diagonal dominance and the spectral radius ρ.'),
                     dict(w='iter2d', o=dict(mat='4 -1 3; -2 5 3', method='gs', step=1, height='360px', side=True, tableHeight='360px',
                                             presets=[['dominant', '4 -1 3; -2 5 3', 'jacobi'], ['rows swapped', '-2 5 3; 4 -1 3', 'gs'], ['check question', '10 1 12; 1 10 21', 'gs'], ['homework 3', '5 2 7; 3 6 9', 'jacobi'], ['SOR', '1 0.9 1.9; 0.9 1 1.9', 'sor']]))]),
                 dict(name='Heat plate', blocks=[
                     dict(p='Jacobi, Gauss–Seidel and SOR on an N × N grid. Change N, the edge temperatures and ω. Which ω gives the fewest sweeps?'),
                     dict(w='plate', o=dict(N=10, omega=1.5, height='300px'))]),
                 dict(name='Code', blocks=[
                     dict(h='Jacobi and Gauss–Seidel'), dict(code='jacobigs', tasks=['Run it. How many iterations does each method need?', 'Swap the first two equations (and b). What happens, and why?', 'Change tol to 1e-10. How many more iterations?']),
                     dict(h='SOR on the plate'), dict(code='sorplate', tasks=['Run it. Which ω is best? Compare with the formula.', 'Set N = 20 (Python: N = 20; C: #define N 20). How do the counts change?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Distinguish the Jacobi and Gauss–Seidel methods.', 'Both solve equation $i$ for $x_i$. Jacobi uses only values from the previous iteration (two vectors, easy to parallelise); Gauss–Seidel uses each new value as soon as it is computed (one vector, usually about twice as fast).'),
                         ('State a sufficient condition for convergence of the Jacobi and Gauss–Seidel methods.', 'Strict diagonal dominance: $|a_{ii}| > \\sum_{j\\ne i}|a_{ij}|$ for every row. More generally, the iteration converges for every start iff the spectral radius of the iteration matrix is less than 1.'),
                         ('Solve $10x + y + z = 12$, $x + 10y + z = 12$, $x + y + 10z = 12$ by Gauss–Seidel.', 'From 0: $(1.2, 1.08, 0.972)$, $(0.9948, 1.0033, 1.0002)$, $(0.9996, 1.0000, 1.0000)$, then $(1.0000, 1.0000, 1.0000)$. Solution $(1, 1, 1)$.'),
                         ('Find the spectral radius of $T_J$ for $\\begin{pmatrix} 5 & 2 \\\\ 3 & 6\\end{pmatrix}$.', '$T_J = \\begin{pmatrix} 0 & -0.4 \\\\ -0.5 & 0\\end{pmatrix}$, $\\lambda^2 = 0.2$, $\\rho = 0.4472$. For Gauss–Seidel $\\rho = 0.2$.'),
                         ('What is SOR and what does ω do?', 'Successive over-relaxation: $x_i \\leftarrow (1 - \\omega)x_i + \\omega\\,\\tilde x_i$, where $\\tilde x_i$ is the Gauss–Seidel value. $\\omega = 1$ is Gauss–Seidel; $1 < \\omega < 2$ over-relaxes and, with a good choice (for the plate $2/(1 + \\sin(\\pi/(N+1)))$), reduces the number of sweeps dramatically. It diverges for $\\omega \\ge 2$.')])])]),
)
