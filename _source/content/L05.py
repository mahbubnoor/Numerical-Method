LECTURE = dict(
    title='Conditioning and Stability',
    sub='Some problems magnify every tiny error, and no algorithm can save them. Some algorithms ruin perfectly good problems. Telling the two apart is the most important diagnostic skill in numerical computing.',
    slides=[
        dict(type='cover', id='cover', notes="Opening story: two students solve the same 2×2 system on their phones. One types 2.0001, the other 2.0002 for one number (a rounding difference in their data). One gets x = 1, y = 1; the other x = 0, y = 2. Whose calculator is broken?\n\nNeither. The problem itself is ill-conditioned. Today we learn to measure that, and to separate it from a badly designed algorithm."),
        dict(type='goals', id='goals', items=[
            'Define <b>conditioning</b> (a property of the problem) and <b>stability</b> (a property of the algorithm)',
            'Compute the <b>condition number</b> of a function and of a matrix',
            'Predict how many digits are lost: about $\\log_{10}\\kappa$',
            'Recognise <b>unstable algorithms</b> and replace them with stable ones',
            'Explain <b>forward</b> and <b>backward</b> error'],
            prev='Errors propagate through arithmetic; cancellation can destroy relative accuracy.',
            today='Two questions behind every inaccurate answer: <b>Is the problem sensitive?</b> <b>Is my method careless?</b>',
            notes="Tell students now that we will build that answer together."),
        dict(type='compare', id='two', title='Problem vs algorithm', mid='≠',
             left=dict(h='Conditioning (the problem)', cls='blue', items=['How much does the <b>exact</b> answer change when the input changes a little?', 'Measured by the <b>condition number</b> $\\kappa$', 'Well-conditioned: $\\kappa$ small (≈ 1–100)', 'Ill-conditioned: $\\kappa$ huge; data errors are amplified', 'No algorithm can fix it; only better data, more precision or a reformulated problem']),
             right=dict(h='Stability (the algorithm)', cls='key', items=['Does the algorithm keep its <b>own</b> rounding errors small?', 'Stable: the answer is as good as the conditioning allows', 'Unstable: errors grow inside the algorithm (e.g. by $n!$ or by $10^{8}$)', 'Fixable: choose a different algorithm for the same problem', 'Examples: pivoting, rewriting formulas, backward recurrence']),
             below=dict(html='<p class="lead frag fade">Accurate result ⇐ <b>well-conditioned problem</b> + <b>stable algorithm</b>. You need both.</p>'),
             notes="Analogy: conditioning is the road (a mountain road is sensitive to small steering errors); stability is the driver (a careless driver crashes even on a straight road). A good driver on a terrible road still struggles; a careless driver crashes on a good road.\n\nKeep returning to these two columns throughout the lecture."),
        dict(type='math', id='kappaf', title='Condition number of evaluating $f(x)$',
             eqs=[dict(cap='Relative change out ÷ relative change in', eq='\\kappa_f(x) = \\left|\\frac{\\Delta f / f}{\\Delta x / x}\\right| \\approx \\left|\\frac{x\\,f\'(x)}{f(x)}\\right|')],
             right=dict(table=[['$f(x)$', '$\\kappa_f(x)$', 'verdict'], [['$\\sqrt{x}$', '$\\tfrac12$', 'always well'], ['$e^{x}$', '$|x|$', 'well unless $x$ huge'], ['$x - 1$ at $x = 1.001$', '$\\left|\\tfrac{x}{x-1}\\right| = 1001$', 'ill (cancellation)'], ['$\\tan x$ at $x = 1.57$', '≈ 1972', 'ill (near $\\pi/2$)'], ['$\\ln x$ near $x = 1$', '$\\left|\\tfrac{1}{\\ln x}\\right|$ → ∞', 'ill']]], cls='tb sm', frag=True), rw=820,
             below=dict(items=['Derivation: $\\Delta f \\approx f\'(x)\\,\\Delta x$, so $\\dfrac{\\Delta f}{f} \\approx \\dfrac{x f\'(x)}{f(x)}\\cdot\\dfrac{\\Delta x}{x}$', 'A relative input error $\\delta$ becomes about $\\kappa\\,\\delta$ in the output', 'Since every stored input has $\\delta \\approx 10^{-16}$, expect to lose about $\\log_{10}\\kappa$ digits'], frag=True),
             notes="Derive κ from the first-order Taylor expansion (Lecture 3): f(x + Δx) ≈ f(x) + f'(x)Δx.\n\nWork two rows: √x gives κ = x · (1/(2√x)) / √x = 1/2: square roots halve relative errors. x − 1 near 1: κ = x/(x − 1) = 1001: the problem of subtracting nearly equal numbers is itself ill-conditioned. Cancellation (Lecture 4) is an ill-conditioned operation.\n\ntan at 1.57: κ ≈ 2x/sin(2x) ≈ 1972, so three digits are lost even with a perfect algorithm."),
        dict(type='widget', id='lines', title='Explore: nearly parallel lines', w='illcond', o=dict(preset='ill', height='420px'), lw=520,
             items=['Two lines cross at the solution of a 2×2 system', 'When the lines are <b>nearly parallel</b>, a tiny shift moves the crossing a long way', 'Move the slider: $b_2$ changes in the 5th decimal', 'Switch to the well-conditioned system: the crossing barely moves'],
             notes="Live demo. In the ill-conditioned system, moving b2 by 0.0001 moves the solution from (1, 1) to (0, 2). The amplification factor shown is the condition number at work.\n\nGeometric picture of ill-conditioning: the rows of the matrix are nearly parallel vectors (nearly linearly dependent), so det(A) is tiny relative to the entries."),
        dict(type='worked', id='sys', title='Problem 1: an ill-conditioned system',
             src='Problem 1', q='Solve $x + y = 2$, $\\;x + 1.0001y = 2.0001$. Then change the second right-hand side to $2.0002$.',
             steps=['Subtract the equations: $0.0001\\,y = 0.0001 \\Rightarrow y = 1,\\; x = 1$',
                    'With $2.0002$: $0.0001\\,y = 0.0002 \\Rightarrow y = 2,\\; x = 0$',
                    'Input changed by $0.0001/2.0001 = 0.005\\%$; output changed by $100\\%$: amplification about $20{,}000$',
                    '$A^{-1} = \\dfrac{1}{0.0001}\\begin{pmatrix}1.0001 & -1\\\\ -1 & 1\\end{pmatrix}$, $\\;\\|A\\|_\\infty = 2.0001$, $\\;\\|A^{-1}\\|_\\infty = 20001$, $\\;\\kappa_\\infty(A) \\approx 40{,}004$'],
             answer='$\\kappa \\approx 4\\times10^{4}$: expect to lose about 4–5 significant digits, whatever method we use.',
             notes="Every method, exact arithmetic included, gives these answers: the sensitivity belongs to the problem.\n\nPractical meaning: if the coefficients come from measurements accurate to 4 digits, this system's solution has no correct digits at all. The right response is to question the model, not to buy a better computer."),
        dict(type='math', id='kappaA', title='Condition number of a matrix',
             eqs=[dict(cap='Definition', eq='\\kappa(A) = \\|A\\|\\,\\|A^{-1}\\| \\;\\ge 1'),
                  dict(cap='What it guarantees', eq='\\frac{\\|\\Delta \\mathbf{x}\\|}{\\|\\mathbf{x}\\|} \\le \\kappa(A)\\,\\frac{\\|\\Delta \\mathbf{b}\\|}{\\|\\mathbf{b}\\|}', frag=True)],
             items=['$\\|A\\|_\\infty$ = largest absolute <b>row sum</b> (easy by hand)', '$\\kappa = 1$: perfect (e.g. identity, rotations)', 'Rule of thumb: digits lost ≈ $\\log_{10}\\kappa(A)$', 'Singular matrix: $\\kappa = \\infty$. A small determinant alone does <b>not</b> mean ill-conditioned: $10^{-10}I$ has $\\kappa = 1$', 'Full treatment of norms: Lecture 11'],
             ifrag=True,
             notes="Condition number, not determinant, measures sensitivity.\n\nIn practice: numpy.linalg.cond(A). MATLAB warns 'Matrix is close to singular or badly scaled' when κ > 10^16-ish."),
        dict(type='code', id='hilbert', title='The famous Hilbert matrix', code='hilbert', lw=600,
             items=['$H_{ij} = \\dfrac{1}{i + j - 1}$; we solve $H\\mathbf{x} = \\mathbf{b}$ where the true $\\mathbf{x}$ is all ones', 'The algorithm (Gaussian elimination with pivoting, Lecture 12) is stable', 'Yet the error grows from $10^{-14}$ to $10^{-3}$ as $n$ goes 3 → 12', 'Because $\\kappa(H_{12}) \\approx 10^{16}$: all 16 digits are lost'],
             notes="Run it. Errors: n = 3: 1e-14, n = 5: 6e-13, n = 8: 1e-7, n = 10: 7e-4, n = 12: 6e-3. The condition numbers are about 5e2, 5e5, 1.5e10, 1.6e13 and 1.7e16.\n\nThe errors track κ × 1e-16 closely: the algorithm is doing as well as possible. This is the textbook example of an ill-conditioned problem with a stable algorithm.\n\nHilbert matrices are not exotic: they appear in least-squares polynomial fitting with the basis 1, x, x², … on [0, 1] (Lecture 24). That is why high-degree polynomial fits misbehave."),
        dict(type='widget', id='unst', title='An unstable algorithm for a well-conditioned problem', w='unstable', o=dict(n=20), lw=560,
             items=['$I_n = \\int_0^1 x^n e^{x-1}\\,dx$; integration by parts gives $I_n = 1 - n\\,I_{n-1}$', 'Start from $I_0 = 1 - e^{-1}$ (rounded) and go forward: the error is multiplied by $n$ each step', 'By $n = 20$ it is multiplied by $20! \\approx 2.4\\times10^{18}$: $I_{20} = -30.19$, impossible', 'Run the <b>same formula backwards</b> from a rough guess: errors are <b>divided</b> by $n$: stable'],
             notes="Use the slider. The forward column first goes negative at n = 18 and then explodes; every value must lie between 0 and 1/(n+1).\n\nThe problem is well-conditioned (the integral is a smooth, insensitive function of n); the algorithm is unstable. Rearranging the recurrence (I_{n−1} = (1 − I_n)/n) makes it stable: starting even from the crude guess I_40 = 0, the error at n = 20 is about 1/(40!/20!) ≈ 1e-30."),
        dict(type='cards', id='pairs', title='Unstable algorithms and their stable replacements', n=2, frag=True,
             cards=[dict(h='Gaussian elimination without pivoting', t='A tiny pivot like 0.001 creates huge multipliers (Lecture 12). <b>Fix:</b> partial pivoting.', cls='bad'),
                    dict(h='$(1-\\cos x)/x^2$ for small $x$', t='Cancellation inside the algorithm. <b>Fix:</b> $2\\sin^2(x/2)/x^2$.', cls='bad'),
                    dict(h='One-pass variance $\\overline{x^2} - \\bar{x}^2$', t='Cancellation for large means. <b>Fix:</b> subtract the mean first (two passes).', cls='bad'),
                    dict(h='Forward recurrence $I_n = 1 - nI_{n-1}$', t='Error × $n$ per step. <b>Fix:</b> run it backwards.', cls='bad')],
             notes="In each case the problem is fine and only the algorithm is to blame. The fix never needs more precision, only a smarter sequence of operations.\n\nAsk the class to state, for each card, whether the problem is ill-conditioned. (No, in all four.)"),
        dict(type='math', id='fwdbwd', title='Forward error and backward error',
             eqs=[dict(cap='Forward error: how wrong is the answer?', eq='|\\tilde{x} - x|'), dict(cap='Backward error: for which nearby problem is the answer exact?', eq='\\min\\{\\,|\\Delta| : \\tilde{x} \\text{ solves the problem with data } d + \\Delta\\,\\}'),
                  dict(cap='Link', eq='\\text{forward error} \\;\\lesssim\\; \\kappa \\times \\text{backward error}', frag=True)],
             items=['Example: root of $x^2 - 2 = 0$ computed as $\\tilde{x} = 1.4142$', 'Forward error: $|1.4142 - \\sqrt2| = 1.36\\times10^{-5}$', 'Backward: $1.4142^2 = 1.99996164$, so $\\tilde{x}$ is the <b>exact</b> root of $x^2 - 1.99996164 = 0$: data changed by $3.8\\times10^{-5}$', 'A <b>backward stable</b> algorithm always gives the exact answer to a slightly perturbed problem'],
             ifrag=True,
             notes="Backward error is the modern way to judge algorithms (Wilkinson): if the computed answer is the exact answer for data within rounding error of ours, the algorithm has done its job; any remaining error is the problem's fault (conditioning).\n\nThe link formula ties the lecture together: forward error ≈ condition number × backward error. Stable algorithm → small backward error; well-conditioned problem → small κ."),
        dict(type='html', id='grid', title='Diagnosing an inaccurate answer',
             html='<div class="grid g2" style="gap:20px"><div class="card ok"><span class="tag">well-conditioned + stable</span><h3>Accurate ✓</h3><p>$\\sqrt{x}$, Gaussian elimination with pivoting on a good matrix, $2\\sin^2(x/2)$.</p></div>'
                  '<div class="card key frag fade"><span class="tag">well-conditioned + unstable</span><h3>Inaccurate, but fixable</h3><p>Change the <b>algorithm</b>: pivot, rewrite, reverse the recurrence.</p></div>'
                  '<div class="card blue frag fade"><span class="tag">ill-conditioned + stable</span><h3>Inaccurate, algorithm is innocent</h3><p>Change the <b>problem</b>: better data, more precision, rescale, regularise. Hilbert matrix, nearly parallel lines.</p></div>'
                  '<div class="card bad frag fade"><span class="tag">ill-conditioned + unstable</span><h3>Hopeless</h3><p>Fix the algorithm first, then deal with the conditioning.</p></div></div>',
             notes="Use this grid as a checklist whenever a numerical result looks wrong. Step 1: estimate κ. If κ × 1e-16 is far smaller than the observed error, the algorithm is unstable. If they match, the problem is ill-conditioned."),
        dict(type='exam', id='practice', src='Problem 2',
             q='"Distinguish between an ill-conditioned problem and an unstable algorithm. A well-conditioned problem can still yield an inaccurate computed result. Using one example each, illustrate (i) a well-conditioned problem ruined by an unstable algorithm, and (ii) an ill-conditioned problem for which no algorithm, however stable, can guarantee an accurate result."',
             tips=['Definitions: conditioning = sensitivity of the exact solution to input changes ($\\kappa$); stability = whether the algorithm keeps its own rounding errors from growing',
                   '(i) $I_n = 1 - nI_{n-1}$ forward: well-conditioned integral, error × $n!$ ⇒ $I_{20} = -30$; or GE without pivoting on $0.001x + y = 1, x + y = 2$',
                   '(ii) $x + y = 2$, $x + 1.0001y = 2.0001$: changing 2.0001 → 2.0002 moves $(1,1)$ to $(0,2)$; $\\kappa \\approx 4\\times10^4$, true for any algorithm',
                   'Close with: accuracy needs both, forward error ≲ κ × backward error'],
             notes="Numbers in the examples make the answer convincing."),
        dict(type='ml', id='ml', items=[
            dict(ic='📐', h='Feature scaling', t='Features in metres and in millimetres make the normal-equations matrix ill-conditioned. Standardising features (mean 0, std 1) reduces $\\kappa$ and speeds up training.'),
            dict(ic='🛡️', h='Ridge regularisation', t='Solving $(X^TX + \\lambda I)\\mathbf{w} = X^T\\mathbf{y}$ instead of $X^TX\\mathbf{w} = X^T\\mathbf{y}$ caps the condition number: a cure for ill-conditioning (Lecture 23).'),
            dict(ic='⛰️', h='Ill-conditioned loss surfaces', t='When the Hessian\'s eigenvalues differ a lot (ratio = $\\kappa$), gradient descent zig-zags: exactly the situation studied in Lecture 25.'),
            dict(ic='🔢', h='Adam\'s epsilon', t='Optimisers divide by $\\sqrt{v} + \\epsilon$ with $\\epsilon = 10^{-8}$ so that a tiny denominator cannot amplify noise: a stability safeguard.')],
            notes="Conditioning is everywhere in ML, under different names: 'badly scaled features', 'exploding gradients', 'regularisation'. Students who understand κ understand why these tricks work."),
        dict(type='check', id='check', q='A linear system has $\\kappa(A) = 10^{10}$ and is solved in double precision with a <b>stable</b> algorithm. About how many correct significant digits can we expect?',
             opts=['16', '10', '6', '0'], right=2,
             answer='C. Double gives about 16 digits; $\\log_{10}\\kappa = 10$ digits are lost: about $16 - 10 = 6$ remain.',
             notes="Follow-up: in single precision (7 digits) the same system would give no correct digits at all."),
        dict(type='summary', id='summary', items=[
            '<b>Conditioning</b> belongs to the problem; <b>stability</b> to the algorithm',
            '$\\kappa_f = |xf\'(x)/f(x)|$; $\\kappa(A) = \\|A\\|\\|A^{-1}\\|$; digits lost ≈ $\\log_{10}\\kappa$',
            'Ill-conditioned: change the data or the problem. Unstable: change the algorithm',
            'Forward error ≲ κ × backward error; a backward-stable algorithm solves a nearby problem exactly'],
            hw=['Find $\\kappa_f(x)$ for $f(x) = x^{10}$ and for $f(x) = \\ln x$. Where is each ill-conditioned?', 'For $A = \\begin{pmatrix} 1 & 2 \\\\ 2 & 4.001\\end{pmatrix}$ compute $\\kappa_\\infty(A)$. How many digits would you lose?', 'Run the recurrence widget to $n = 25$. At which $n$ does the forward value first leave $[0, 1]$?', 'Write a model answer to Problem 2 in your own words (half a page).'],
            next='<b>Root finding and the bisection method.</b> The safest way to solve $f(x) = 0$: trap the root in an interval and halve it, with a guaranteed error bound.',
            notes="Homework answers: Q1: x^10: κ = 10 (moderate everywhere); ln x: κ = 1/|ln x|, infinite at x = 1. Q2: det = 0.001, A^-1 = (1/0.001)[[4.001, −2], [−2, 1]], ‖A‖∞ = 6.001, ‖A^-1‖∞ = 6001, κ ≈ 36,012: about 4.6 digits lost. Q3: the forward value first leaves [0, 1] at n = 18 (it becomes −0.0295)."),
    ],
    code={
        'hilbert': dict(file='hilbert_conditioning', py='''# Solve H x = b where H is the Hilbert matrix and the true x is all ones

def solve(A, b):                      # Gaussian elimination with partial pivoting
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(M[i][k]))
        M[k], M[p] = M[p], M[k]
        for i in range(k + 1, n):
            m = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] -= m * M[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / M[i][i]
    return x

for n in [3, 5, 8, 10, 12]:
    H = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
    b = [sum(row) for row in H]       # so that x = (1, 1, ..., 1)
    x = solve(H, b)
    err = max(abs(v - 1.0) for v in x)
    print(f"n = {n:2d}   max error = {err:.2e}")
''', c='''/* Solve H x = b where H is the Hilbert matrix and the true x is all ones */
#include <stdio.h>
#include <math.h>
#define MAXN 12

void solve(double A[][MAXN + 1], double x[], int n) {   /* A is n x (n+1), augmented */
    for (int k = 0; k < n; k++) {
        int p = k;
        for (int i = k + 1; i < n; i++) if (fabs(A[i][k]) > fabs(A[p][k])) p = i;
        for (int j = 0; j <= n; j++) { double t = A[k][j]; A[k][j] = A[p][j]; A[p][j] = t; }
        for (int i = k + 1; i < n; i++) {
            double m = A[i][k] / A[k][k];
            for (int j = k; j <= n; j++) A[i][j] -= m * A[k][j];
        }
    }
    for (int i = n - 1; i >= 0; i--) {
        double s = A[i][n];
        for (int j = i + 1; j < n; j++) s -= A[i][j] * x[j];
        x[i] = s / A[i][i];
    }
}

int main(void) {
    int sizes[5] = {3, 5, 8, 10, 12};
    double A[MAXN][MAXN + 1], x[MAXN];
    for (int t = 0; t < 5; t++) {
        int n = sizes[t];
        for (int i = 0; i < n; i++) {
            double s = 0;
            for (int j = 0; j < n; j++) { A[i][j] = 1.0 / (i + j + 1); s += A[i][j]; }
            A[i][n] = s;                     /* so that x = (1, 1, ..., 1) */
        }
        solve(A, x, n);
        double err = 0;
        for (int i = 0; i < n; i++) if (fabs(x[i] - 1.0) > err) err = fabs(x[i] - 1.0);
        printf("n = %2d   max error = %.2e\\n", n, err);
    }
    return 0;
}
'''),
        'recur': dict(file='unstable_recurrence', py='''import math

# forward: I_n = 1 - n * I_(n-1), starting from I_0 = 1 - 1/e
I = 1 - 1 / math.e
forward = [I]
for n in range(1, 21):
    I = 1 - n * I
    forward.append(I)

# backward: I_(n-1) = (1 - I_n) / n, starting from a crude guess I_40 = 0
J = 0.0
for n in range(40, 20, -1):
    J = (1 - J) / n
backward = [0.0] * 21
backward[20] = J
for n in range(20, 0, -1):
    backward[n - 1] = (1 - backward[n]) / n

for n in [0, 5, 10, 15, 17, 18, 20]:
    print(f"n = {n:2d}   forward = {forward[n]: .10f}   backward = {backward[n]:.10f}")
''', c='''#include <stdio.h>
#include <math.h>
int main(void) {
    double fw[21], bw[21];
    fw[0] = 1 - 1 / exp(1.0);
    for (int n = 1; n <= 20; n++) fw[n] = 1 - n * fw[n - 1];
    double J = 0.0;
    for (int n = 40; n > 20; n--) J = (1 - J) / n;
    bw[20] = J;
    for (int n = 20; n > 0; n--) bw[n - 1] = (1 - bw[n]) / n;
    int show[7] = {0, 5, 10, 15, 17, 18, 20};
    for (int k = 0; k < 7; k++)
        printf("n = %2d   forward = % .10f   backward = %.10f\\n", show[k], fw[show[k]], bw[show[k]]);
    return 0;
}
'''),
        'condnum': dict(file='condition_2x2', py='''# Condition number (infinity norm) of a 2x2 matrix, and the effect of a tiny change
a, b, c, d = 1.0, 1.0, 1.0, 1.0001
det = a*d - b*c
inv = [[d/det, -b/det], [-c/det, a/det]]
normA = max(abs(a) + abs(b), abs(c) + abs(d))
normI = max(abs(inv[0][0]) + abs(inv[0][1]), abs(inv[1][0]) + abs(inv[1][1]))
print(f"det = {det:.6g},  kappa = {normA * normI:.6g}")

for b2 in [2.0001, 2.0002, 2.0000]:
    e, f = 2.0, b2
    x = (e*d - b*f) / det
    y = (a*f - e*c) / det
    print(f"b2 = {b2}:  x = {x:.6f}, y = {y:.6f}")
'''),
    },
    lab=dict(title='Conditioning Lab',
             intro='Measure how sensitive a problem is, and see the difference between a sensitive problem and a careless algorithm.',
             tabs=[
                 dict(name='Nearly parallel lines', blocks=[
                     dict(p='Move the slider to change one number of the system slightly. Watch the crossing point and the amplification factor.'),
                     dict(w='illcond', o=dict(preset='ill', height='330px'))]),
                 dict(name='Unstable recurrence', blocks=[
                     dict(p='The same exact formula, run forward (unstable) and backward (stable). Every correct value lies between 0 and 1/(n+1).'),
                     dict(w='unstable', o=dict(n=20))]),
                 dict(name='Code', blocks=[
                     dict(h='Condition number of a 2×2 system'), dict(code='condnum', tasks=['Run it. How much does the solution move?', 'Change d to 2.0 (a well-conditioned matrix with a = c = 1). Repeat.', 'Change d to 1.00000001. What happens to kappa?']),
                     dict(h='Hilbert matrix'), dict(code='hilbert', tasks=['Run it. At which n is the error above 1e-6?', 'Add n = 13 and 14. What happens?', 'Explain: is the algorithm or the problem to blame?']),
                     dict(h='Forward vs backward recurrence'), dict(code='recur', tasks=['Run it. Where does forward go wrong?', 'Start the backward loop from n = 30 instead of 40. Is it still accurate at n = 20?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Define the condition number of a function and compute it for $f(x) = \\sqrt{x}$ and $f(x) = x - 1$.', '$\\kappa_f = |xf\'(x)/f(x)|$. $\\sqrt{x}$: $\\kappa = \\tfrac12$ (well-conditioned for all $x > 0$). $x - 1$: $\\kappa = |x/(x-1)|$, which is huge near $x = 1$.'),
                         ('Compute $\\kappa_\\infty(A)$ for $A = \\begin{pmatrix} 4 & 1 \\\\ 2 & 3 \\end{pmatrix}$.', '$\\det = 10$, $A^{-1} = \\tfrac{1}{10}\\begin{pmatrix} 3 & -1 \\\\ -2 & 4\\end{pmatrix}$. $\\|A\\|_\\infty = 5$, $\\|A^{-1}\\|_\\infty = 0.6$, so $\\kappa = 3$: well-conditioned.'),
                         ('Distinguish an ill-conditioned problem and an unstable algorithm, with one example each.', 'Ill-conditioned: exact answer very sensitive to data; e.g. $x + y = 2$, $x + 1.0001y = 2.0001$ ($\\kappa\\approx4\\times10^4$). Unstable: the algorithm amplifies its own rounding errors; e.g. $I_n = 1 - nI_{n-1}$ forward, which gives $I_{20} = -30.19$ although $0 < I_{20} < 1/21$.'),
                         ('A matrix has $\\kappa = 10^{12}$. How many correct digits do you expect in single and double precision?', 'Double: about $16 - 12 = 4$. Single: about $7 - 12 < 0$, so none.'),
                         ('Explain forward and backward error using the computed root $\\tilde{x} = 1.4142$ of $x^2 = 2$.', 'Forward error $|\\tilde{x} - \\sqrt2| = 1.36\\times10^{-5}$. Backward error: $\\tilde{x}^2 = 1.99996164$, so $\\tilde{x}$ solves $x^2 = 1.99996164$ exactly; the data changed by $3.8\\times10^{-5}$.'),
                         ('Is a matrix with a very small determinant always ill-conditioned? Explain.', 'No. $10^{-10}I$ has determinant $10^{-30}$ (3×3) but $\\kappa = 1$. Conditioning depends on $\\|A\\|\\|A^{-1}\\|$, not on the size of the determinant.')])])]),
)
