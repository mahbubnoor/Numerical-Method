LECTURE = dict(
    title='Errors and Their Propagation',
    short='Errors and Their Propagation',
    sub='Every numerical answer is wrong by some amount. We learn to measure that amount, predict how it grows, and avoid the one operation that destroys accuracy: subtracting nearly equal numbers.',
    slides=[
        dict(type='cover', id='cover', notes="Opening question: \"A shop scale is wrong by 10 grams. Is that a big error?\" Students will say: it depends. For a 50 kg rice sack it is nothing; for 20 grams of saffron it is a disaster.\n\nThat is the whole idea of relative error, and it is today's first topic."),
        dict(type='goals', id='goals', items=[
            'Compute <b>absolute</b>, <b>relative</b> and <b>percentage</b> errors and count correct significant digits',
            'Distinguish <b>round-off</b> error from <b>truncation</b> error, with examples of each',
            'Use the <b>error propagation</b> rules for $+,-,\\times,\\div$ and the general formula',
            'Recognise <b>catastrophic cancellation</b> and rewrite formulas to avoid it',
            'Find the <b>best step size</b> when truncation and round-off errors compete'],
            prev='Round-off: relative error up to $10^{-16}$ per number (L2). Truncation: the first neglected Taylor term, $O(h^p)$ (L3).',
            today='How do those tiny errors, plus the errors of stopping a method early, combine and grow through a calculation?',
            notes="Bridge: in Lecture 2 every number got a small relative error δ with |δ| ≤ 1.1e-16, and in Lecture 3 we met truncation error, the first neglected Taylor term. Today we follow those errors through arithmetic. Most operations keep them small. One operation, subtraction of nearly equal numbers, can multiply them by a billion."),
        dict(type='math', id='defs', title='Measuring error',
             lead='True value $x$, approximation $x^{*}$.',
             eqs=[dict(cap='Absolute error', eq='E_a = |x - x^{*}|'), dict(cap='Relative error', eq='E_r = \\dfrac{|x - x^{*}|}{|x|}'), dict(cap='Percentage error', eq='E_p = 100 \\times E_r \\,\\%')],
             right=dict(table=[['Approximation of $\\pi$', '$E_a$', '$E_r$'], [['3.14', '0.0015927', '$5.07\\times10^{-4}$'], ['22/7 = 3.142857', '0.0012645', '$4.02\\times10^{-4}$'], ['3.1416', '0.0000073', '$2.34\\times10^{-6}$']]], cls='tb sm'), rw=720,
             below=dict(html='<p class="frag fade">Relative error is scale-free: an error of 1 cm in 1 km ($10^{-5}$) is far better than 1 cm in 10 cm ($10^{-1}$). <b>Numerical analysts almost always report relative error.</b></p>'),
             notes="Compute the π table with the class. 3.14 has E_r ≈ 0.05%; 22/7 is slightly better than 3.14; 3.1416 is about 200 times better.\n\nWhen the true value is unknown (always, in practice) we use the best available estimate of x in the denominator, or an error bound."),
        dict(type='math', id='sigfig', title='How many significant digits are correct?',
             eqs=[dict(cap='Rule', eq='x^{*} \\text{ is correct to } n \\text{ significant digits if } \\; E_r \\le \\tfrac{1}{2}\\times 10^{1-n}'),
                  dict(cap='Decimal places', eq='x^{*} \\text{ is correct to } d \\text{ decimal places if } \\; E_a \\le \\tfrac{1}{2}\\times10^{-d}')],
             items=['$3.14$: $E_r = 5.07\\times10^{-4} \\le 0.5\\times10^{-2}$ ✓ but $> 0.5\\times10^{-3}$ ✗: <b>3 significant digits</b>',
                    '$3.1416$: $E_a = 7.3\\times10^{-6} \\le 0.5\\times10^{-4}$: correct to <b>4 decimal places</b>',
                    'Double precision: $E_r \\le 1.1\\times10^{-16}$ gives about <b>16</b>',
                    'Iterations: stop when $|x_{k+1}-x_k| < \\tfrac12\\times10^{-d}$ for $d$ decimal places (Lecture 1)'],
             ifrag=True,
             notes="The rule says: n correct significant digits means the relative error is at most half a unit in the n-th significant place.\n\nWork the 3.14 case slowly: n = 3 gives the bound 0.5 × 10^-2 = 5e-3, and 5.07e-4 is below it; n = 4 gives 5e-4, and 5.07e-4 is just above it. So 3 significant digits.\n\nCaution: the relative-error rule is a convention, and for numbers like 3.1416 it can credit one more digit than is written (the lab program reports 6). Never claim more digits than you actually write; for 3.1416 the honest statement is 'correct to 4 decimal places'."),
        dict(type='compare', id='kinds', title='Two sources of error in every computation', mid='+',
             left=dict(h='Round-off error', cls='blue', tag='Lecture 2', items=['From storing numbers with finitely many digits', 'Example: $\\tfrac{2}{3} \\to 0.6667$, $\\;0.1 \\to 0.1000000000000000055\\ldots$', 'Grows slowly with the number of operations', 'Reduced by higher precision (double, not float)']),
             right=dict(h='Truncation error', cls='key', tag='this course', items=['From replacing an infinite or exact process by a finite one', 'Example: $e = 1 + 1 + \\tfrac{1}{2!} + \\tfrac{1}{3!} + \\tfrac{1}{4!} = 2.708333$, error $0.009948$', 'Stopping an iteration, a finite step $h$, a cut series', 'Reduced by more terms, smaller $h$, more iterations']),
             below=dict(html='<p class="lead frag fade">Total error = round-off + truncation. Making $h$ smaller cuts truncation error but adds round-off error: a balance we measure later in this lecture and meet again in Lecture 19 (numerical differentiation).</p>'),
             notes="Most students confuse truncation (a property of the method) with chopping (a way of rounding). Make the distinction explicit: chopping is a kind of round-off; truncation error comes from truncating a mathematical process.\n\nThe e example: 5 terms of the series give 2.708333 against 2.718282; the error 0.009948 is truncation error, and it would be there even with infinitely many digits."),
        dict(type='math', id='prop', title='How errors propagate through arithmetic',
             lead='Inputs $x \\pm \\Delta x$ and $y \\pm \\Delta y$. Worst-case (maximum) error of the result:',
             eqs=[dict(cap='Sum and difference: absolute errors add', eq='\\Delta(x \\pm y) \\le \\Delta x + \\Delta y', frag=True),
                  dict(cap='Product and quotient: relative errors add', eq='\\frac{\\Delta(xy)}{|xy|} \\approx \\frac{\\Delta x}{|x|} + \\frac{\\Delta y}{|y|}, \\qquad \\frac{\\Delta(x/y)}{|x/y|} \\approx \\frac{\\Delta x}{|x|} + \\frac{\\Delta y}{|y|}', frag=True),
                  dict(cap='General function', eq='\\Delta f \\approx \\left|\\frac{\\partial f}{\\partial x}\\right|\\Delta x + \\left|\\frac{\\partial f}{\\partial y}\\right|\\Delta y + \\cdots', frag=True)],
             items=['Powers: $\\dfrac{\\Delta(x^n)}{|x^n|} \\approx |n|\\,\\dfrac{\\Delta x}{|x|}$', 'The general formula comes from the first-order Taylor expansion (Lecture 3)', 'Danger: in $x - y$ the absolute error stays, but if $x - y$ is tiny the <b>relative</b> error explodes'],
             ifrag=True,
             notes="Derive the product rule on the board: (x + Δx)(y + Δy) = xy + yΔx + xΔy + ΔxΔy. Drop ΔxΔy (second order) and divide by xy.\n\nThe last bullet is the bridge to cancellation: the subtraction rule says the absolute error does not grow, but dividing by a tiny result makes the relative error huge."),
        dict(type='worked', id='propex', title='Problem 1: relative error of a formula',
             src='Problem 1', q='If $u = \\dfrac{4x^2y^3}{z^4}$ and the errors in $x, y, z$ are each $0.001$, find the maximum relative error in $u$ at $x = y = z = 1$.',
             steps=['Take logarithms: $\\ln u = \\ln 4 + 2\\ln x + 3\\ln y - 4\\ln z$',
                    'Differentiate: $\\dfrac{\\Delta u}{u} = 2\\dfrac{\\Delta x}{x} + 3\\dfrac{\\Delta y}{y} - 4\\dfrac{\\Delta z}{z}$',
                    'Worst case: all terms add: $\\left|\\dfrac{\\Delta u}{u}\\right|_{\\max} = 2\\dfrac{0.001}{1} + 3\\dfrac{0.001}{1} + 4\\dfrac{0.001}{1}$',
                    '$= (2 + 3 + 4)\\times 0.001 = 0.009$'],
             answer='Maximum relative error $= 0.009$ (0.9%). The powers multiply the relative errors: $z^4$ contributes the most.',
             right=dict(card=dict(tag='Second example', h='Rectangle area', t='$l = 10.0 \\pm 0.05$ cm, $w = 5.0 \\pm 0.05$ cm.<br>$A = 50$ cm²; $\\Delta A \\approx w\\,\\Delta l + l\\,\\Delta w = 0.25 + 0.5 = 0.75$ cm².<br>Relative: $0.5\\% + 1\\% = 1.5\\%$.', cls='blue')), rw=600,
             notes="The log-differentiation trick turns products and powers into sums.\n\nWhy add absolute values: we want the maximum possible error, so we assume the worst signs. The −4 becomes +4.\n\nThe rectangle shows the same rule without logs: relative errors 0.5% and 1% add to 1.5%."),
        dict(type='bullets', id='cancel', title='Catastrophic cancellation', rw=820,
             lead='Subtracting two nearly equal numbers cancels their leading digits; only the noisy trailing digits survive.',
             items=['4-digit arithmetic: $\\sqrt{1001} - \\sqrt{1000} = 31.64 - 31.62 = 0.02$', 'True value $0.0158074$: relative error <b>26.5%</b>, from inputs accurate to 0.02%!',
                    'Rewrite (multiply by the conjugate): $\\dfrac{1}{\\sqrt{1001}+\\sqrt{1000}} = \\dfrac{1}{63.26} = 0.01581$ (error 0.01%)',
                    'The subtraction itself is exact; it <b>exposes</b> the earlier rounding errors'],
             frag=True,
             right=dict(html='<div class="card"><span class="tag">Digit view</span><p class="mono" style="font-size:30px;line-height:1.6">  31.6385…<br>− 31.6228…<br>= <span class="rd">00.0157</span>…</p><p>In 4 digits: 31.64 − 31.62: the two shared digits "31.6" cancel, leaving one digit of noise.</p></div>'),
             notes="Do the 4-digit calculation on the board. Students are shocked that an exact subtraction can produce a 26% error.\n\nThe key insight: the subtraction is not the culprit; the inputs already had small absolute errors (0.005 each). After subtraction the absolute error is the same, but the result is 160 times smaller, so the relative error is 160 times bigger.\n\nThe cure is algebra: rewrite to avoid the subtraction."),
        dict(type='widget', id='cancelw', title='Explore: naive vs rewritten formulas', w='cancel', o=dict(mode='cos', height='330px'), lw=520,
             items=['$\\dfrac{1-\\cos x}{x^2}$ should be ≈ 0.5 for small $x$', 'Move $x$ towards $10^{-8}$: the naive formula returns <b>0</b> (100% error)', 'Rewritten $\\dfrac{2\\sin^2(x/2)}{x^2}$ stays accurate', 'Try the other two expressions in the menu'],
             notes="Drag the slider to the left. Below about x = 1e-8, cos(x) rounds to exactly 1.0, so 1 − cos x = 0 and the naive formula returns 0.\n\nThe identity 1 − cos x = 2 sin²(x/2) involves no subtraction, so it stays accurate.\n\nThe quadratic formula option: for x² + bx + 1 = 0 with large |b|, the small root −b + √(b²−4) cancels. The fix 2/(−b − √(b²−4)) (from the product of roots = c/a) is how professional solvers compute roots."),
        dict(type='worked', id='quad', title='Fixing the quadratic formula',
             src='Problem 2', q='Solve $x^2 + 10^{8}x + 1 = 0$. The roots are about $-10^{8}$ and $-10^{-8}$.',
             steps=['Naive small root: $x_1 = \\dfrac{-10^8 + \\sqrt{10^{16} - 4}}{2}$: two numbers that agree in about 16 digits are subtracted',
                    'Double precision gives $x_1 = -7.4506\\times10^{-9}$: <b>25% wrong</b>',
                    'Use $x_1 x_2 = c/a = 1$: compute the large root safely, $x_2 = \\dfrac{-10^8 - \\sqrt{10^{16}-4}}{2}$ (no cancellation)',
                    'Then $x_1 = \\dfrac{c}{a\\,x_2} = \\dfrac{2c}{-b - \\sqrt{b^2-4ac}} = -1.0000\\times10^{-8}$ ✓'],
             answer='Rule: compute the root where $-b$ and $\\pm\\sqrt{b^2-4ac}$ have the <b>same sign</b>, then the other from $x_1x_2 = c/a$.',
             right=dict(code='quadcancel', ed='300px', out='120px'), rw=760,
             notes="Run the code box on the right: it shows −7.450580596923828e-09 for the naive formula and −1e-08 for the stable one.\n\nThis is not a toy: library root finders (numpy.roots uses eigenvalues; but hand-written quadratic solvers in graphics code) must use the stable form, or ray–sphere intersections flicker."),
        dict(type='code', id='series', title='Truncation and round-off together: $e^{-20}$ by Taylor series', code='expseries', lw=600,
             items=['$e^{x} = \\sum x^n/n!$ converges for every $x$ (no truncation problem with enough terms)', 'For $x = -20$ the terms reach $4.3\\times10^{7}$ with alternating signs: huge cancellation', 'The sum comes out wrong in every digit, even negative!', 'Cure: compute $1/e^{20}$ (all terms positive)'],
             notes="Run it. The naive alternating sum gives a value around 5.6e-09 instead of 2.06e-09: completely wrong despite using 100 terms, more than enough for truncation.\n\nThe largest term is 20^20/20! ≈ 4.3e7; its rounding error is about 4.3e7 × 1.1e-16 ≈ 5e-9, larger than the answer 2e-9 itself.\n\nThis is the clearest example of a mathematically correct formula that is numerically useless."),
        dict(type='widget', id='stepw', title='Truncation meets round-off: the best step size', w='stepsize', o=dict(f='sin(x)', x=1, height='380px'), lw=520,
             items=['$f\'(x) \\approx \\dfrac{f(x+h) - f(x)}{h}$ (Lecture 3): truncation error ∝ $h$ (right side of the V)', 'But $f(x+h) - f(x)$ <b>cancels</b>: round-off error ≈ $\\varepsilon / h$ grows as $h$ shrinks (left side)', 'Best forward $h \\approx \\sqrt{\\varepsilon} \\approx 10^{-8}$; best central $h \\approx \\varepsilon^{1/3} \\approx 10^{-5}$', 'Smallest possible error: about $10^{-8}$ (forward), $10^{-11}$ (central)'],
             notes="The V shape is one of the most important pictures in numerical analysis. Total error ≈ C·h^p + ε/h. Minimising gives the optimal h.\n\nWhy ε/h: f(x+h) and f(x) each carry a rounding error of about ε|f|; their difference is divided by h.\n\nThis is why 'just make h tiny' is wrong, a common belief among students."),
        dict(type='ml', id='ml', items=[
            dict(ic='📊', h='Variance in one pass', t='$\\sigma^2 = \\overline{x^2} - \\bar{x}^2$ cancels badly when the mean is large: data near $10^8$ give 22.0 instead of 22.5, and near $10^9$ the result is pure noise (it can even be negative). Libraries subtract the mean first (two passes) or use Welford\'s method.'),
            dict(ic='🧠', h='Log-sum-exp and softmax', t='$\\log\\sum e^{z_i}$ is computed as $m + \\log\\sum e^{z_i - m}$ with $m = \\max z_i$: no overflow, no loss of digits.'),
            dict(ic='🔊', h='Audio in decibels', t='Speech energy in dB uses $10\\log_{10}(E + \\epsilon)$; the small $\\epsilon$ stops $\\log 0$ on silent frames.'),
            dict(ic='💰', h='Money', t='Banks never store taka as binary floats: 0.1 is inexact. They use integers (paisa) or decimal arithmetic.')],
            notes="The variance example is a real bug that appears in student ML code. The lab has the program: data [1e8+4, 1e8+7, 1e8+13, 1e8+16] give 22.0 with the one-pass formula and the right 22.5 with two passes; with 1e9 the one-pass value is garbage."),
        dict(type='exam', id='practice', src='Problem 3',
             q='(a) Define absolute, relative and percentage errors. (b) If $\\pi$ is approximated by $3.14$, find the three errors. (c) Explain, with an example, why the subtraction of two nearly equal numbers causes loss of significant digits and how it can be avoided.',
             tips=['Write each definition as a formula with a one-line meaning', 'Show substitution: $E_a = |3.1415927 - 3.14| = 0.0015927$, $E_r = 0.0015927/3.1415927 = 5.07\\times10^{-4}$, $E_p = 0.0507\\%$',
                   'Cancellation: use the 4-digit $\\sqrt{1001} - \\sqrt{1000}$ example; give both the wrong and the rewritten result',
                   'State the cure in general: rewrite with conjugates, trig identities, or series for small arguments'],
             notes=""),
        dict(type='check', id='check', q='Which expression is computed <b>accurately</b> in double precision for $x = 10^{-10}$?',
             opts=['$\\sqrt{1+x} - 1$', '$\\dfrac{x}{\\sqrt{1+x} + 1}$', '$(1+x) - 1$', '$\\dfrac{e^{x} - 1}{x}$'], right=1,
             answer='B. It equals A exactly (multiply by the conjugate) but has no subtraction of nearly equal numbers. A, C and D all subtract 1 from a number very close to 1.',
             notes="Discuss D: e^x − 1 for small x is so common that C and Python provide expm1(x), which computes it accurately. Likewise log1p(x) = log(1 + x)."),
        dict(type='summary', id='summary', items=[
            '$E_a = |x - x^*|$, $E_r = E_a/|x|$, $E_p = 100E_r$; correct to $n$ significant digits if $E_r \\le \\tfrac12 10^{1-n}$',
            'Round-off: finite digits. Truncation: finite process. Total error is both',
            'Absolute errors add in $\\pm$; relative errors add in $\\times, \\div$; powers multiply them',
            'Subtracting nearly equal numbers destroys relative accuracy: <b>rewrite the formula</b>',
            'Total error = truncation + round-off: a V shape in $h$; best $h \\approx \\sqrt{\\varepsilon}$ (forward) or $\\varepsilon^{1/3}$ (central)'],
            hw=['Find $E_a$, $E_r$ and $E_p$ when $\\sqrt{2}$ is approximated by 1.414. How many significant digits are correct?', 'If $V = \\pi r^2 h$ with $r = 2.0 \\pm 0.01$ and $h = 5.0 \\pm 0.02$, find the maximum relative error in $V$.', 'Rewrite $\\ln(x+1) - \\ln x$ for large $x$ to avoid cancellation. Test both forms in Python for $x = 10^{12}$.', 'Lab: run the variance program and explain why the one-pass formula fails.'],
            next='<b>Conditioning and stability.</b> Why some problems amplify every small error (and no algorithm can help), while some algorithms ruin perfectly good problems.',
            notes="Homework answers: Q1: Ea = 0.000213562, Er = 1.51e-4, Ep = 0.0151%, 4 significant digits. Q2: ΔV/V = 2(0.01/2) + 0.02/5 = 0.01 + 0.004 = 0.014 (1.4%). Q3: ln((x+1)/x) = log1p(1/x); for x = 1e12 the naive form gives 1.0018652574217413e-12 (0.19% relative error), log1p gives 9.999999999995e-13."),
    ],
    code={
        'quadcancel': dict(file='quadratic_cancel', py='''import math
a, b, c = 1.0, 1e8, 1.0
d = math.sqrt(b*b - 4*a*c)
naive  = (-b + d) / (2*a)          # cancellation!
x2     = (-b - d) / (2*a)          # safe: same signs
stable = c / (a * x2)              # from x1 * x2 = c/a
print("naive  :", naive)
print("stable :", stable)
''', c='''#include <stdio.h>
#include <math.h>
int main(void) {
    double a = 1.0, b = 1e8, c = 1.0;
    double d = sqrt(b*b - 4*a*c);
    double naive  = (-b + d) / (2*a);     /* cancellation! */
    double x2     = (-b - d) / (2*a);     /* safe: same signs */
    double stable = c / (a * x2);         /* from x1 * x2 = c/a */
    printf("naive  : %.16g\\n", naive);
    printf("stable : %.16g\\n", stable);
    return 0;
}
'''),
        'expseries': dict(file='exp_series_cancel', py='''import math

def exp_series(x, terms=100):
    total, term = 0.0, 1.0
    for n in range(terms):
        total += term
        term = term * x / (n + 1)
    return total

x = -20.0
naive = exp_series(x)              # alternating huge terms
safe  = 1.0 / exp_series(-x)       # all terms positive
print(f"series e^-20    : {naive:.10e}")
print(f"1 / series e^20 : {safe:.10e}")
print(f"math.exp(-20)   : {math.exp(-20):.10e}")
print(f"largest term    : {20**20 / math.factorial(20):.3e}")
''', c='''#include <stdio.h>
#include <math.h>

double exp_series(double x, int terms) {
    double total = 0.0, term = 1.0;
    for (int n = 0; n < terms; n++) {
        total += term;
        term = term * x / (n + 1);
    }
    return total;
}

int main(void) {
    double naive = exp_series(-20.0, 100);       /* alternating huge terms */
    double safe  = 1.0 / exp_series(20.0, 100);  /* all terms positive */
    printf("series e^-20    : %.10e\\n", naive);
    printf("1 / series e^20 : %.10e\\n", safe);
    printf("exp(-20)        : %.10e\\n", exp(-20.0));
    return 0;
}
'''),
        'variance': dict(file='variance_cancel', py='''# One-pass vs two-pass variance (population variance)
data = [1e8 + 4, 1e8 + 7, 1e8 + 13, 1e8 + 16]
n = len(data)

mean = sum(data) / n
one_pass = sum(x*x for x in data) / n - mean**2      # E[x^2] - E[x]^2
two_pass = sum((x - mean)**2 for x in data) / n       # subtract mean first

print("one-pass variance:", one_pass)
print("two-pass variance:", two_pass)
print("true variance    : 22.5")
''', c='''/* One-pass vs two-pass variance (population variance) */
#include <stdio.h>
int main(void) {
    double data[4] = {1e8 + 4, 1e8 + 7, 1e8 + 13, 1e8 + 16};
    int n = 4;
    double s = 0, s2 = 0;
    for (int i = 0; i < n; i++) { s += data[i]; s2 += data[i] * data[i]; }
    double mean = s / n;
    double one_pass = s2 / n - mean * mean;      /* E[x^2] - E[x]^2 */
    double t = 0;
    for (int i = 0; i < n; i++) t += (data[i] - mean) * (data[i] - mean);
    double two_pass = t / n;
    printf("one-pass variance: %.17g\\n", one_pass);
    printf("two-pass variance: %.17g\\n", two_pass);
    printf("true variance    : 22.5\\n");
    return 0;
}
'''),
        'errcalc': dict(file='error_measures', py='''import math

x_true = math.pi
for x_approx in [3.14, 22/7, 3.1416, 355/113]:
    Ea = abs(x_true - x_approx)
    Er = Ea / abs(x_true)
    # largest n with Er <= 0.5 * 10**(1 - n)
    n = 0
    while Er <= 0.5 * 10**(1 - (n + 1)):
        n += 1
    print(f"{x_approx:<12.9g} Ea = {Ea:.3e}  Er = {Er:.3e}  Ep = {100*Er:.5f} %  sig. digits ~ {n}")
''', c='''#include <stdio.h>
#include <math.h>
int main(void) {
    double x_true = M_PI;
    double approx[4] = {3.14, 22.0 / 7, 3.1416, 355.0 / 113};
    for (int i = 0; i < 4; i++) {
        double Ea = fabs(x_true - approx[i]);
        double Er = Ea / fabs(x_true);
        int n = 0;
        while (Er <= 0.5 * pow(10, 1 - (n + 1))) n++;
        printf("%-12.9g Ea = %.3e  Er = %.3e  Ep = %.5f %%  sig. digits ~ %d\\n", approx[i], Ea, Er, 100 * Er, n);
    }
    return 0;
}
'''),
    },
    lab=dict(title='Error Lab',
             intro='Measure errors, watch cancellation destroy digits, and fix formulas by rewriting them.',
             tabs=[
                 dict(name='Cancellation explorer', blocks=[
                     dict(p='Choose an expression and move x. The red curve is the naive formula, the green curve the rewritten one. The vertical axis is the relative error on a log scale: 1e−16 is perfect, 1e0 means every digit is wrong.'),
                     dict(w='cancel', o=dict(mode='cos', height='300px'))]),
                 dict(name='Step size', blocks=[
                     dict(p='Error of the forward and central difference approximations of f′(x) as the step h changes (log scales). Type your own f(x).'),
                     dict(w='stepsize', o=dict(f='e^x', x=0, height='330px'))]),
                 dict(name='Code: error measures', blocks=[
                     dict(code='errcalc', tasks=['Run it. Which approximation of π is best?', 'Add 3.14159265 to the list. How many digits does the program report?', 'Change x_true to math.sqrt(2) and the list to [1.4, 1.41, 1.414, 1.4142].'])]),
                 dict(name='Code: cancellation', blocks=[
                     dict(h='e⁻²⁰ by series'), dict(code='expseries', tasks=['Run it. How wrong is the naive series?', 'Try x = -5 and x = -10. When does the naive sum become useless?', 'Print the largest term for x = -30. Compare its rounding error (× 1.1e-16) with e^-30.']),
                     dict(h='Variance'), dict(code='variance', tasks=['Run it. Which variance is right?', 'Change 1e8 to 1e9. What happens to the one-pass result?', 'Change 1e8 to 0. Do both methods now agree?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Find the absolute, relative and percentage errors if $2/3$ is approximated by $0.6667$.', '$E_a = |0.666667 - 0.6667| = 3.33\\times10^{-5}$; $E_r = 3.33\\times10^{-5}/0.666667 = 5.0\\times10^{-5}$; $E_p = 0.005\\%$.'),
                         ('If $u = \\dfrac{5xy^2}{z^3}$ and $\\Delta x = \\Delta y = \\Delta z = 0.001$ at $x = y = z = 1$, find the maximum relative error in $u$.', '$\\Delta u/u = \\Delta x/x + 2\\Delta y/y + 3\\Delta z/z = (1+2+3)(0.001) = 0.006$.'),
                         ('The sides of a rectangle are $l = 12.0 \\pm 0.1$ cm and $w = 8.0 \\pm 0.1$ cm. Find the area and its maximum error.', '$A = 96$ cm². $\\Delta A \\approx w\\Delta l + l\\Delta w = 0.8 + 1.2 = 2.0$ cm² (relative 2.08%).'),
                         ('Distinguish round-off error and truncation error with one example each.', 'Round-off: from finite digits, e.g. $1/3 \\to 0.3333$. Truncation: from stopping an infinite process, e.g. $e^x \\approx 1 + x + x^2/2$; the neglected terms are the truncation error.'),
                         ('Evaluate $\\sqrt{9.01} - 3$ in 4-significant-digit arithmetic, then by a rewritten formula. Compare with the true value $0.0016662$.', 'Naive: $\\sqrt{9.01} = 3.002$, so $3.002 - 3 = 0.002$ (20% error). Rewritten: $0.01/(\\sqrt{9.01} + 3) = 0.01/6.002 = 0.001666$ (0.01% error).'),
                         ('Why does $1 - \\cos x$ give 0 in double precision for $x = 10^{-9}$? Give an accurate formula.', '$\\cos(10^{-9}) = 1 - 5\\times10^{-19}$, which rounds to exactly 1.0 (the gap below 1 is $1.1\\times10^{-16}$). Use $2\\sin^2(x/2)$, which gives $5\\times10^{-19}$.')])])]),
)
