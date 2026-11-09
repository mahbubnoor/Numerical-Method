LECTURE = dict(
    title='Taylor Series and Order of Accuracy',
    short='Taylor Series and Order of Accuracy',
    sub='Almost every formula in this course comes from a Taylor series cut off after a few terms. The first neglected term tells us the error, and "O(h²)" tells us how fast it shrinks.',
    slides=[
        dict(type='cover', id='cover', notes="Opening: \"How does your calculator compute sin(0.3)? It has no triangle inside.\" It uses a polynomial, essentially a Taylor series (in practice a refined version), because polynomials need only + and ×.\n\nToday's tool, the Taylor series, is the engine behind finite differences, Newton's method, Euler and Runge–Kutta, and gradient descent. If students master one formula this term, it should be this one."),
        dict(type='goals', id='goals', items=[
            'Write the <b>Taylor series</b> of a function and its <b>remainder</b> term',
            'Approximate values and <b>bound the truncation error</b> using the remainder',
            'Explain <b>big-O</b> notation and the <b>order of accuracy</b> of a method',
            'Derive the forward and central difference formulas and their $O(h)$, $O(h^2)$ errors',
            'See the Taylor series as the <b>engine</b> of later methods: Newton (L9), difference operators (L15), ODE solvers (L21)'],
            prev='Round-off: doubles keep about 16 significant digits ($\\varepsilon \\approx 2.2\\times10^{-16}$).',
            today='The <b>other</b> source of error, truncation. The Taylor series lets us predict it before computing anything, and compare methods by their order.',
            notes="Recall the pipeline slide of Lecture 1: truncation error is the price of stopping an infinite process early, and round-off (Lecture 2) is the price of finite digits. Today's tool, the Taylor series, is the cleanest example of truncation: we will bound the error of a cut-off series without knowing the true answer.\n\nWhy this lecture comes so early: Lectures 4 (error propagation), 5 (condition numbers), 8 (fixed-point convergence), 9 (Newton) and 15 (difference operators) all use it. It is the one dependency of the whole course."),
        dict(type='math', id='series', title='The Taylor series',
             eqs=[dict(cap='About the point a', eq='\\begin{aligned} f(x) = {} & f(a) + f\'(a)(x-a) + \\frac{f\'\'(a)}{2!}(x-a)^2 \\\\ & + \\cdots + \\frac{f^{(n)}(a)}{n!}(x-a)^n + R_n(x) \\end{aligned}'),
                  dict(cap='Lagrange remainder (the error of stopping at degree n)', eq='R_n(x) = \\frac{f^{(n+1)}(\\xi)}{(n+1)!}(x-a)^{n+1}, \\qquad \\xi \\text{ between } a \\text{ and } x', frag=True)],
             items=['$a = 0$ gives the <b>Maclaurin</b> series', 'The polynomial matches $f$, $f\'$, $f\'\'$, … at $a$', 'We never know $\\xi$, but we can <b>bound</b> $|f^{(n+1)}|$ on the interval, which bounds the error', 'Close to $a$, $(x-a)^{n+1}$ is tiny: the approximation is excellent'],
             ifrag=True,
             notes="Write the series on the board and point at each part. The remainder is the key: it looks like the next term, except the derivative is evaluated at an unknown point ξ.\n\nIntuition: the degree-1 polynomial is the tangent line; degree 2 adds curvature; each extra term matches one more derivative.\n\nThe remainder is a mean value theorem in disguise: for n = 0 it says f(x) − f(a) = f'(ξ)(x − a)."),
        dict(type='cards', id='known', title='Series worth knowing by heart', n=3,
             cards=[dict(h='$e^{x}$', eq='1 + x + \\frac{x^2}{2!} + \\frac{x^3}{3!} + \\cdots', t='all $x$'),
                    dict(h='$\\sin x$', eq='x - \\frac{x^3}{3!} + \\frac{x^5}{5!} - \\cdots', t='all $x$ (radians)'),
                    dict(h='$\\cos x$', eq='1 - \\frac{x^2}{2!} + \\frac{x^4}{4!} - \\cdots', t='all $x$ (radians)'),
                    dict(h='$\\ln(1+x)$', eq='x - \\frac{x^2}{2} + \\frac{x^3}{3} - \\cdots', t='$-1 < x \\le 1$ only', cls='key'),
                    dict(h='$\\dfrac{1}{1-x}$', eq='1 + x + x^2 + x^3 + \\cdots', t='$|x| < 1$ only', cls='key'),
                    dict(h='$\\sqrt{1+x}$', eq='1 + \\frac{x}{2} - \\frac{x^2}{8} + \\cdots', t='$|x| \\le 1$')],
             notes="The two orange cards have a radius of convergence: outside it, adding more terms makes things worse. The widget on the next slide shows this vividly for ln(1 + x) beyond x = 1.\n\nUseful: sin x ≈ x and cos x ≈ 1 − x²/2 for small x, which explains the (1 − cos x)/x² → 1/2 limit used in Lecture 4."),
        dict(type='widget', id='taylorw', title='Explore: adding terms', w='taylor', o=dict(f='exp', n=2, height='420px'), lw=500,
             items=['Increase the degree: the polynomial hugs $f$ over a wider range', 'The error at a point is close to the <b>first neglected term</b>', 'Choose $\\ln(1+x)$ and go past $x = 1$: more terms make it <b>worse</b>', 'Choose $\\sin x$: odd degrees only add new terms'],
             notes="Live demo. With e^x and degree 2, the approximation is good near 0 and poor at x = 3. Raise to 6: good across the plot.\n\nFor ln(1 + x) the series diverges for x > 1: show degree 8 vs 12 at x = 2; the error grows. This is the radius of convergence in action.\n\nPoint out the 'first neglected term' line under the plot: it is always close to the actual error when x is near 0."),
        dict(type='worked', id='e05', title='Problem 1: $e^{0.5}$ with an error bound',
             src='Problem 1', q='Approximate $e^{0.5}$ using the first four terms of the Maclaurin series, and bound the error.',
             steps=['$e^{x} \\approx 1 + x + \\dfrac{x^2}{2} + \\dfrac{x^3}{6}$, so $e^{0.5} \\approx 1 + 0.5 + 0.125 + 0.0208333 = 1.6458333$',
                    'Remainder: $R_3 = \\dfrac{e^{\\xi}}{4!}(0.5)^4$ with $0 < \\xi < 0.5$',
                    'Bound: $e^{\\xi} < e^{0.5} < 2$, so $|R_3| < \\dfrac{2 \\times 0.0625}{24} = 0.0052$ (sharper: $e^{0.5}(0.5)^4/24 = 0.0043$)',
                    'Check: true $e^{0.5} = 1.6487213$, actual error $= 0.0028879$, inside the bound ✓'],
             answer='$e^{0.5} \\approx 1.6458$ with error less than $0.005$. The bound is honest (never too small) but a little pessimistic.',
             notes="The bound uses e^ξ < 2 because we may not use e^0.5 itself (we are computing it!). Using e^0.5 gives the sharper 0.0043, fine for checking."),
        dict(type='worked', id='nterms', title='How many terms do we need?',
             src='Problem 2', q='How many terms of $e^{x} = \\sum x^k/k!$ are needed to compute $e$ (that is, $x = 1$) with error less than $10^{-6}$?',
             steps=['Stopping after degree $n$: $|R_n| = \\dfrac{e^{\\xi}}{(n+1)!} < \\dfrac{3}{(n+1)!}$ since $e^{\\xi} < e < 3$',
                    'Need $\\dfrac{3}{(n+1)!} < 10^{-6}$, i.e. $(n+1)! > 3\\times10^{6}$',
                    '$9! = 362{,}880$ (too small), $10! = 3{,}628{,}800$ ✓, so $n + 1 = 10$, $n = 9$',
                    'Degree 9 means the terms $k = 0, 1, \\dots, 9$: <b>10 terms</b>. Check: $\\sum_{k=0}^{9} 1/k! = 2.7182815$, error $3.0\\times10^{-7}$ ✓'],
             answer='10 terms. This is how library designers decide the length of a polynomial: from the remainder bound, before writing any code.',
             notes="This is the reverse question: given an accuracy, find n. The factorial makes the remainder fall extremely fast, which is why e^x series are so effective for small x.\n\nLibraries reduce the argument first (e.g. e^x = 2^k e^r with |r| < 0.35) so that a short polynomial is enough everywhere."),
        dict(type='math', id='bigO', title='Step form and big-O notation',
             eqs=[dict(cap='Taylor series with step h', eq='f(x+h) = f(x) + h f\'(x) + \\frac{h^2}{2} f\'\'(x) + \\frac{h^3}{6} f\'\'\'(x) + \\cdots'),
                  dict(cap='Big-O', eq='E(h) = O(h^p) \\iff |E(h)| \\le C\\,h^p \\text{ for small } h', frag=True),
                  dict(cap='Order of accuracy', eq='E(h/2) \\approx E(h)/2^{p} \\qquad \\Rightarrow \\qquad p \\approx \\log_2 \\frac{E(h)}{E(h/2)}', frag=True)],
             items=['$O(h)$: halve $h$ → error halves (first order)', '$O(h^2)$: halve $h$ → error ÷ 4 (second order)', '$O(h^4)$: halve $h$ → error ÷ 16 (RK4, Simpson)', 'Higher order = far fewer steps for the same accuracy'],
             ifrag=True,
             notes="Write f(x+h) and stress: this is the same series with x − a replaced by h. Every numerical formula in Lectures 19–22 comes from this line.\n\nThe order test (third box) is how we verify a method experimentally: compute the error for h and h/2 and take log base 2 of the ratio. We do exactly that on the next slides."),
        dict(type='worked', id='derive', title='Deriving the difference formulas',
             src='Problem 3', q='From the Taylor series, derive the forward and central difference approximations of $f\'(x)$ and their truncation errors.',
             steps=['Forward: $f(x+h) = f(x) + hf\'(x) + \\tfrac{h^2}{2}f\'\'(\\xi)$ ⟹ $f\'(x) = \\dfrac{f(x+h) - f(x)}{h} - \\underbrace{\\tfrac{h}{2}f\'\'(\\xi)}_{O(h)}$',
                    'Write both $f(x \\pm h) = f(x) \\pm hf\'(x) + \\tfrac{h^2}{2}f\'\'(x) \\pm \\tfrac{h^3}{6}f\'\'\'(x) + \\cdots$',
                    'Subtract: $f(x+h) - f(x-h) = 2hf\'(x) + \\tfrac{h^3}{3}f\'\'\'(x) + \\cdots$ (the $f$ and $f\'\'$ terms cancel)',
                    'Divide by $2h$: $f\'(x) = \\dfrac{f(x+h) - f(x-h)}{2h} - \\underbrace{\\tfrac{h^2}{6}f\'\'\'(x)}_{O(h^2)} + \\cdots$'],
             answer='Forward difference: error $O(h)$. Central difference: error $O(h^2)$, for one extra function evaluation per point… and a much better answer.',
             notes="Why central is better: the even-order terms cancel by symmetry. For the same h the error is smaller by a factor of about h, and it falls 4 times per halving instead of 2."),
        dict(type='table', id='verify', title='Checking the order: $f(x) = \\ln x$ at $x = 1$ (exact $f\'(1) = 1$)',
             head=['$h$', 'forward', 'error', 'central', 'error', 'central error ratio'], frag=True,
             rows=[['0.1', '0.9531018', '−4.69e−2', '1.0033535', '3.35e−3', '—'], ['0.05', '0.9758033', '−2.42e−2', '1.0008346', '8.35e−4', '4.01'], ['0.025', '0.9877045', '−1.23e−2', '1.0002084', '2.08e−4', '4.00'], ['0.0125', '0.9938016', '−6.20e−3', '1.0000521', '5.21e−5', '4.00']],
             note='Forward errors halve when h halves (order 1). Central errors fall by 4 (order 2). Theory: central error ≈ $\\tfrac{h^2}{6}f\'\'\'(1) = \\tfrac{h^2}{6}\\cdot 2$ = 0.00333 for $h = 0.1$ ✓', notefrag=True,
             right=dict(code='order', ed='330px', out='170px'), rw=760,
             notes="Reveal one row at a time; ask the class to predict the next central error before it appears (divide by 4).\n\nf'''(x) = 2/x³ for ln x, so f'''(1) = 2 and the predicted central error at h = 0.1 is 0.01 × 2/6 = 0.00333. Measured: 0.00335. The O(h²) theory matches.\n\nRun the code box to reproduce the table, then change the function."),
        dict(type='exam', id='practice', src='Problem 4',
             q='"Starting from the Taylor series expansion of $f(x)$ about a point $x$, derive the central-difference approximation of $f\'(x)$ and show that its truncation error is $O(h^2)$. Using this formula with $h = 0.1$, estimate $f\'(1)$ for $f(x) = \\ln x$. Compare your result with the exact derivative and compute the actual error, commenting on whether it is consistent with the theoretical $O(h^2)$ order."',
             tips=['Derivation exactly as on slide 9: expand $f(x\\pm h)$, subtract, divide by $2h$, name the leading error term $-\\tfrac{h^2}{6}f\'\'\'(x)$',
                   'Numbers: $\\dfrac{\\ln 1.1 - \\ln 0.9}{0.2} = \\dfrac{0.0953102 + 0.1053605}{0.2} = 1.0033535$',
                   'Exact $f\'(1) = 1$; actual error $= 0.0033535$',
                   'Theory: $\\tfrac{h^2}{6}|f\'\'\'(1)| = \\tfrac{0.01}{6}\\times 2 = 0.0033333$: matches, so consistent with $O(h^2)$',
                   'Strong answers add: halving $h$ to 0.05 gives error $8.35\\times10^{-4}$, a factor 4 smaller'],
             notes=""),
        dict(type='ml', id='ml', items=[
            dict(ic='⬇️', h='Gradient descent is first-order Taylor', t='$L(w + \\Delta) \\approx L(w) + \\nabla L^{T}\\Delta$. The decrease is largest for $\\Delta = -\\eta\\nabla L$: that is the update rule (Lecture 25).'),
            dict(ic='🎯', h='Newton\'s method is second-order Taylor', t='Adding $\\tfrac12\\Delta^T H \\Delta$ (the Hessian) and minimising gives Newton\'s step: the basis of fast optimisers.'),
            dict(ic='🧮', h='Activation functions on chips', t='$\\tanh$, $e^x$ and GELU are computed with short polynomials whose length comes from remainder bounds.'),
            dict(ic='🔁', h='Backpropagation checks', t='Gradient checking compares backprop with $\\frac{L(w+h)-L(w-h)}{2h}$, the central difference, with $h \\approx 10^{-5}$: the best step size, explained in Lecture 4.')],
            notes="The gradient-checking card connects directly to today's step-size widget: PyTorch and course assignments use central differences with h around 1e-5; next lecture shows why that value is optimal (the step-size V-curve)."),
        dict(type='check', id='check', q='A method gives error $8\\times10^{-4}$ with step $h$ and $5\\times10^{-5}$ with step $h/2$. What is its order?',
             opts=['1', '2', '3', '4'], right=3,
             answer='D. The ratio is $8\\times10^{-4}/5\\times10^{-5} = 16 = 2^4$, so $p = \\log_2 16 = 4$.',
             notes="Follow-up: 'With h/4, what error do you expect?' 5e-5 / 16 ≈ 3.1e-6."),
        dict(type='summary', id='summary', items=[
            'Taylor: $f(x) = \\sum \\frac{f^{(k)}(a)}{k!}(x-a)^k + R_n$, with $R_n = \\frac{f^{(n+1)}(\\xi)}{(n+1)!}(x-a)^{n+1}$',
            'Bound $|f^{(n+1)}|$ to bound the truncation error; choose $n$ from the bound',
            '$O(h^p)$: halving $h$ divides the error by $2^p$; measure $p$ from two step sizes',
            'Forward difference $O(h)$; central difference $O(h^2)$',
            'Every method later in the course (Newton, difference formulas, Simpson, Runge–Kutta) is a truncated Taylor series'],
            hw=['Approximate $\\sin(\\pi/4)$ with three non-zero terms of the Maclaurin series and bound the error.', 'How many terms of the series for $\\cos x$ give $\\cos 1$ with error below $10^{-8}$?', 'Derive the backward difference $f\'(x) \\approx [f(x) - f(x-h)]/h$ and its error term.', 'Lab: run the order program for $f(x) = e^x$ at $x = 0$. Confirm the orders 1 and 2.'],
            next='<b>Errors and their propagation.</b> Measuring errors, how round-off and truncation errors combine and grow through arithmetic, catastrophic cancellation, and the best step size $h$.',
            notes="Homework answers: Q1: π/4 − (π/4)³/6 + (π/4)⁵/120 = 0.7071430, true 0.7071068, error 3.6e-5, bound (π/4)⁷/5040 = 3.66e-5 ✓. Q2: need 1/(2n+2)! < 1e-8; 12! = 4.8e8 works, so terms up to x^10: 6 terms. Q3: f(x−h) = f(x) − hf'(x) + h²/2 f''(ξ), so f'(x) = [f(x) − f(x−h)]/h + (h/2) f''(ξ), error O(h)."),
    ],
    code={
        'order': dict(file='difference_order', py='''import math

f = math.log          # try math.exp, math.sin ...
x = 1.0
exact = 1.0           # f'(1) for ln x

prev = None
for h in [0.1, 0.05, 0.025, 0.0125]:
    fwd = (f(x + h) - f(x)) / h
    ctr = (f(x + h) - f(x - h)) / (2 * h)
    e = abs(ctr - exact)
    ratio = prev / e if prev else float('nan')
    print(f"h={h:<7} fwd={fwd:.7f}  ctr={ctr:.7f}  ctr err={e:.2e}  ratio={ratio:.2f}")
    prev = e
''', c='''#include <stdio.h>
#include <math.h>

double f(double x) { return log(x); }

int main(void) {
    double x = 1.0, exact = 1.0, prev = 0;
    double hs[4] = {0.1, 0.05, 0.025, 0.0125};
    for (int i = 0; i < 4; i++) {
        double h = hs[i];
        double fwd = (f(x + h) - f(x)) / h;
        double ctr = (f(x + h) - f(x - h)) / (2 * h);
        double e = fabs(ctr - exact);
        printf("h=%-7g fwd=%.7f  ctr=%.7f  ctr err=%.2e  ratio=%.2f\\n", h, fwd, ctr, e, i ? prev / e : NAN);
        prev = e;
    }
    return 0;
}
'''),
        'taylor_sin': dict(file='taylor_sin', py='''import math

x = math.pi / 4
term = x            # first term of the sine series
total = 0.0
for k in range(6):
    total += term
    n = 2 * k + 1                              # degree of the term just added
    bound = abs(x) ** (n + 2) / math.factorial(n + 2)
    print(f"degree {n:2d}: sum = {total:.10f}  error = {abs(total - math.sin(x)):.2e}  bound = {bound:.2e}")
    term = -term * x * x / ((n + 1) * (n + 2))  # next term from the previous one
''', c='''#include <stdio.h>
#include <math.h>

int main(void) {
    double x = M_PI / 4, term = x, total = 0.0, fact = 1;
    for (int k = 0; k < 6; k++) {
        total += term;
        int n = 2 * k + 1;
        fact = 1; for (int i = 2; i <= n + 2; i++) fact *= i;
        double bound = pow(fabs(x), n + 2) / fact;
        printf("degree %2d: sum = %.10f  error = %.2e  bound = %.2e\\n", n, total, fabs(total - sin(x)), bound);
        term = -term * x * x / ((n + 1) * (n + 2));
    }
    return 0;
}
'''),
        'expterms': dict(file='exp_terms', py='''import math

x = 1.0
total, term, n = 0.0, 1.0, 0
while True:
    total += term
    n += 1
    term = term * x / n
    if abs(term) < 1e-6 / 3:          # remainder bound 3/(n)! below 1e-6
        break
print("terms used :", n)
print("sum        :", total)
print("true e     :", math.e)
print("error      :", abs(math.e - total))
'''),
    },
    lab=dict(title='Taylor Series Lab',
             intro='See polynomials approach a function, bound truncation errors, and measure the order of a formula yourself.',
             tabs=[
                 dict(name='Taylor explorer', blocks=[
                     dict(p='Pick a function and a degree. The orange dashed curve is the Taylor polynomial about 0. Move the evaluation point and compare the actual error with the first neglected term.'),
                     dict(w='taylor', o=dict(f='sin', n=3, height='340px'))]),
                 dict(name='Code', blocks=[
                     dict(h='Order of a difference formula'), dict(code='order', tasks=['Run it. Do the central-difference ratios approach 4?', 'Change f to math.exp and exact to math.exp(1.0). Same ratios?', 'Add h = 1e-6 and 1e-9 to the list. What happens to the central error, and why?']),
                     dict(h='Sine series with error bound'), dict(code='taylor_sin', tasks=['Run it. Is the error always below the bound?', 'Change x to 3. How many terms until the error is below 1e-6?']),
                     dict(h='How many terms for e?'), dict(code='expterms', tasks=['Run it. Compare with the 10 terms predicted on slide 7.', 'Change the tolerance to 1e-12. How many terms?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Write the Taylor series of $\\ln x$ about $x = 1$ up to the $(x-1)^3$ term.', '$\\ln x = (x-1) - \\tfrac{(x-1)^2}{2} + \\tfrac{(x-1)^3}{3} - \\cdots$'),
                         ('Approximate $\\cos(0.2)$ with the first three non-zero terms and bound the error.', '$1 - 0.02 + 0.0000667 = 0.9800667$. Next term $x^6/720 = 8.9\\times10^{-8}$ bounds the error. True value $0.9800666$.'),
                         ('Derive the central difference formula for $f\'(x)$ and state its order.', 'Expand $f(x\\pm h)$, subtract: $f(x+h)-f(x-h) = 2hf\'(x) + \\tfrac{h^3}{3}f\'\'\'(x)+\\cdots$. So $f\'(x) = \\tfrac{f(x+h)-f(x-h)}{2h} - \\tfrac{h^2}{6}f\'\'\'(x)$: order 2.'),
                         ('Errors of a method are $2.0\\times10^{-3}$ for $h = 0.2$ and $5.1\\times10^{-4}$ for $h = 0.1$. Estimate its order.', 'Ratio $\\approx 3.92 \\approx 4 = 2^2$, so order $p \\approx 2$ ($\\log_2 3.92 = 1.97$).'),
                         ('Why does the error of $(f(x+h) - f(x))/h$ increase again when $h$ is very small?', 'Round-off: $f(x+h)$ and $f(x)$ each have an error of about $\\varepsilon|f|$; their difference is divided by $h$, giving an error of about $\\varepsilon|f|/h$ that grows as $h \\to 0$. The total error is minimised near $h \\approx \\sqrt{\\varepsilon}$.')])])]),
)
