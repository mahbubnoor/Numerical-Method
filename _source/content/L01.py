LECTURE = dict(
    title='Why Numerical Methods?',
    short='Why Numerical Methods?',
    sub='When no formula exists, we compute the answer step by step: guess, improve, repeat, and stop when it is good enough.',
    slides=[
        dict(type='cover', id='cover', notes="Welcome to CSE-3107. Open with a question to the class: \"Your calculator says the square root of 2 is 1.41421356. How did it get that number? There is no 'square root circuit'.\" Take two or three answers.\n\nThe honest answer: it runs a short loop, an iteration, that improves a guess until it stops changing. That loop is a numerical method, and today we will run it ourselves, by hand and in code.\n\nThe orange dots on this slide get closer and closer to one point: that is the picture of this whole course."),
        dict(type='goals', id='goals', items=[
            'Explain why many real problems have <b>no exact formula</b> and need numerical methods',
            'Describe the <b>modelling pipeline</b>: problem → model → algorithm → program → answer',
            'Distinguish an <b>analytical</b> (exact) solution from a <b>numerical</b> (approximate) one',
            'Run an <b>iteration</b> by hand and in code, and choose a sensible <b>stopping rule</b>',
            'Compare <b>bracketing</b> and <b>open</b> iteration methods and their limitations'],
            today='A numerical method replaces "find the exact formula" with "compute a number that is as close as we need". Today: why, and the basic loop behind almost every method in this course.',
            reading='Lab PCs: open the course folder and index.html. Everything works offline.',
            notes="Read the goals aloud.\n\nCHECKPOINT (oral): \"Can anyone name a calculation you did in school that had an exact formula?\" (Quadratic formula, area of a circle.) \"Today we see what happens when there is none.\""),
        dict(type='cards', id='nofmla', title='Many problems have no formula to plug into', n=3, frag=True,
             lead='Each of these is easy to state and has an answer, yet no finite formula gives it exactly.',
             cards=[
                 dict(tag='Equation', h='Solve $x = \\cos x$', t='No algebra isolates $x$. The answer is $x \\approx 0.739085$, found only by computing.'),
                 dict(tag='Polynomial', h='Solve $x^5 - x - 1 = 0$', t='Abel (1824): there is <b>no general formula</b> for polynomials of degree 5 or more.'),
                 dict(tag='Integral', h='$\\int_0^1 e^{-x^2}\\,dx$', t='$e^{-x^2}$ has no elementary antiderivative, yet the area is a definite number ≈ 0.746824.'),
                 dict(tag='Differential equation', h="Pendulum $\\theta'' = -\\frac{g}{L}\\sin\\theta$", t='No formula for $\\theta(t)$ in elementary functions; games and simulators step it forward numerically.'),
                 dict(tag='Large system', h='$A\\mathbf{x} = \\mathbf{b}$ with $10^6$ unknowns', t="Cramer's rule would need about $10^{6}!$ operations. Elimination or iteration is the only way."),
                 dict(tag='Data', h='Fit a line to 10,000 points', t='The data have noise; no line passes through all points. We compute the <b>best</b> line (least squares).')],
             notes="Go through the six cards one at a time (each press reveals one).\n\nKey message: \"has no formula\" does not mean \"has no answer\". x = cos x clearly has a solution: draw y = x and y = cos x on the board and point at the crossing. We just cannot write it with +, −, ×, ÷, roots and the usual functions.\n\nAbel–Ruffini: worth one sentence. Students often think there is a 'quintic formula'. There is not, and that is a theorem, not a lack of effort.\n\nEach card points ahead: equations (Lectures 6–10), linear systems (11–14), integrals (20), ODEs (21–22), data fitting (23–24)."),
        dict(type='compare', id='anvsnum', title='Analytical vs numerical solution', mid='vs',
             left=dict(h='Analytical (exact)', cls='blue', items=['A <b>formula</b> or symbolic expression', 'Exact: $x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$', 'Works for every input of that form at once', 'Often impossible for real problems', 'Example: $\\int_0^1 x^2\\,dx = \\tfrac{1}{3}$']),
             right=dict(h='Numerical (approximate)', cls='key', items=['An <b>algorithm</b>: a finite list of arithmetic steps', 'A <b>number</b>: $x \\approx 0.739085$', 'Must be re-run for each new input', 'Works on almost any problem a computer can evaluate', 'Comes with an <b>error</b> we must estimate and control']),
             below=dict(html='<p class="lead frag fade">An algorithm, an error estimate and a stopping rule: those three things together make a <span class="hl">numerical method</span>.</p>'),
             notes="Contrast the two columns row by row.\n\nPoint out the hidden cost of numerical answers: every one comes with an error. A numerical answer without an error estimate is not finished. We will spend Lectures 2–5 on errors before learning methods, because every later method is judged by how fast its error shrinks.\n\nAsk: \"Is 1/3 = 0.333333 analytical or numerical?\" (The fraction is exact; the decimal is a numerical approximation with error 3.3e-7.)"),
        dict(type='html', id='pipeline', title='The modelling pipeline',
             lead='Numerical methods sit in the middle of every computational project. Errors can enter at every arrow.',
             html='<div class="flow"><div><b>Real problem</b>How hot will this CPU get?</div><i>→</i><div class="frag fade"><b>Mathematical model</b>Heat equation, material constants</div><i class="frag fade">→</i><div class="frag fade"><b>Numerical method</b>Finite differences, an iteration</div><i class="frag fade">→</i><div class="frag fade"><b>Program</b>Python, C, NumPy</div><i class="frag fade">→</i><div class="frag fade"><b>Result + check</b>87 °C ± 2 °C. Does it match a measurement?</div></div>'
                  '<div class="grid g3 frag fade" style="margin-top:20px"><div class="card bad"><h3>Modelling error</h3><p>The model ignores something real (air flow, friction).</p></div><div class="card key"><h3>Truncation error</h3><p>The method stops early: finite steps instead of an infinite process. <b>This course.</b></p></div><div class="card blue"><h3>Round-off error</h3><p>The computer keeps only about 16 digits. <b>Lecture 2.</b></p></div></div>',
             notes="Walk through the pipeline left to right with the CPU example. Then reveal the three error types.\n\nThis course lives in the third and fourth boxes. We do not choose the model (physics, economics or ML does that), but we must choose a method whose error is small enough and whose cost is affordable.\n\nThe last box matters: always check a numerical answer, by a second method, a known special case, or a measurement. We will check every worked example in this course by running code."),
        dict(type='cards', id='cases', title='Where numerical methods run every day in CSE', n=3,
             cards=[
                 dict(tag='Machine learning', h='Training = optimisation', t='Gradient descent takes thousands of small steps downhill on a loss function. That is Lecture 25.', frag=True),
                 dict(tag='Graphics and games', h='Ray tracing and physics', t='Where does a light ray hit a curved surface? A root-finding problem (Lecture 9). Game physics steps ODEs with Euler-type methods (Lecture 21).', frag=True),
                 dict(tag='Speech and signals', h='Filters and the FFT', t='Speech enhancement fits filters by least squares (Lecture 23); spectra come from numerical integration and the FFT.', frag=True),
                 dict(tag='Web search', h='PageRank', t="Google's original ranking solves a linear system with billions of unknowns by repeated iteration (Lecture 14).", frag=True),
                 dict(tag='Navigation', h='GPS position', t='Your phone solves a nonlinear system of 4 equations (distance to satellites) with Newton\'s method (Lecture 10).', frag=True),
                 dict(tag='Data science', h='Regression and interpolation', t='Trend lines, filling missing sensor values, smooth curves through points (Lectures 15–18 and 23–24).', frag=True)],
             notes="Reveal one card at a time and ask the class to guess the method before you reveal the lecture number.\n\nThe ML card is the one to dwell on: many students take machine learning next year. Every 'model.fit()' call is a numerical optimisation loop, and when training 'diverges' (loss becomes NaN), that is a numerical-methods failure: too large a step, or floating-point overflow. They will understand both by the end of this course."),
        dict(type='bullets', id='iterate', title='The core idea: iteration', rw=900,
             lead='Start with a guess, apply a rule that improves it, repeat.',
             items=['To find $\\sqrt{N}$: if $x$ is too big, then $N/x$ is too small, so <b>average them</b>',
                    'Rule: $x_{k+1} = \\tfrac{1}{2}\\left(x_k + \\dfrac{N}{x_k}\\right)$ (Babylonian / Heron\'s method, about 1800 BC)',
                    'Every step uses only $+$, $\\div$ and $\\times\\tfrac12$: things a computer does well',
                    'Press <b>Next step</b>: the number of correct digits roughly <b>doubles</b> each time'],
             right=dict(w='babylon', o=dict(N=2, x0=1)),
             notes="This is a 4,000-year-old algorithm, and it is still essentially how computers compute square roots (Newton's method, Lecture 9, gives exactly this formula).\n\nUse the widget live: N = 2, x0 = 1. Press Next step and read the 'correct digits' column: 0, 1, 2, 5, 11, 16. Doubling digits is called quadratic convergence; we will prove it in Lecture 9.\n\nTry x0 = 100: it still works, just a few steps slower. Try N = 10. Ask a student to pick N."),
        dict(type='worked', id='byhand', title='By hand: $\\sqrt{2}$ starting from $x_0 = 1$',
             src='Problem 1', q='Use $x_{k+1} = \\tfrac{1}{2}(x_k + 2/x_k)$ with $x_0 = 1$. Stop when two successive values agree to 4 decimal places.',
             steps=['$x_1 = \\tfrac12\\left(1 + \\tfrac{2}{1}\\right) = \\tfrac12(3) = 1.5$',
                    '$x_2 = \\tfrac12\\left(1.5 + \\tfrac{2}{1.5}\\right) = \\tfrac12(1.5 + 1.333333) = 1.416667$',
                    '$x_3 = \\tfrac12\\left(1.416667 + \\tfrac{2}{1.416667}\\right) = \\tfrac12(1.416667 + 1.411765) = 1.414216$',
                    '$x_4 = \\tfrac12\\left(1.414216 + \\tfrac{2}{1.414216}\\right) = 1.414214$; $\\;|x_4 - x_3| = 0.000002 < 0.00005$, so stop'],
             answer='$\\sqrt{2} \\approx 1.4142$ (true value 1.41421356…). Four steps, using only arithmetic.',
             right=dict(table=[['k', '$x_k$', '$|x_k - x_{k-1}|$'], [[0, '1.000000', '—'], [1, '1.500000', '0.500000'], [2, '1.416667', '0.083333'], [3, '1.414216', '0.002451'], [4, '1.414214', '0.000002']]], frag=False), rw=640,
             notes="Do this on the board with the class, one line per press. Make students compute x2 on their calculators before you reveal it.\n\nStopping test 'agree to 4 decimal places' means |x_k − x_{k−1}| < 0.5 × 10^−4 = 0.00005."),
        dict(type='code', id='code1', title='The same loop in Python and C', code='sqrt_iter', lw=600,
             items=['Press <b>▶ Run</b>, then switch the tab to <b>C</b> and run again: same numbers', 'Change <code>N</code> to 10 and run', 'Change <code>x</code> (the first guess) to 1000: how many more steps?', 'Make <code>tol</code> 1e-20. What happens, and why? (Lecture 2)'],
             notes="Run the Python version first. Then the C version: identical output, because both use IEEE double precision.\n\nTry the suggestions live. The last one is a teaser: with tol = 1e-20 the loop never stops early, because x_new and x eventually differ by 0 or by one unit in the 16th digit; there are only about 16 digits. The 'for k in range(1, 50)' cap saves us. This is why every iteration needs a maximum-iteration guard.\n\nThese code boxes run in the browser, offline. Students can download (⤓) and run the same file in Jupyter or with gcc."),
        dict(type='math', id='stop', title='When do we stop iterating?',
             lead='An iteration never reaches the exact answer, so we must decide when it is close enough.',
             eqs=[dict(cap='Absolute change', eq='|x_{k+1} - x_k| < \\varepsilon'), dict(cap='Relative change (scale-free)', eq='\\dfrac{|x_{k+1} - x_k|}{|x_{k+1}|} < \\varepsilon'), dict(cap='Residual (for f(x) = 0)', eq='|f(x_{k+1})| < \\varepsilon')],
             items=['Use <b>relative</b> change when $x$ may be very large or very small', 'A small change does not <i>guarantee</i> a small error, but for converging methods it is a good estimate', 'Always add a <b>maximum number of iterations</b>: if the method diverges, the loop must still end', '"Correct to $d$ decimal places" means $|x_{k+1} - x_k| < 0.5 \\times 10^{-d}$'],
             ifrag=True,
             notes="The three tests in the boxes are what professional libraries use, usually two of them together.\n\nWhy relative change: if x ≈ 10^8, an absolute tolerance of 1e-6 may be impossible to reach (the spacing of doubles near 10^8 is about 1.5e-8, fine here, but near 10^12 it is 1.2e-4). If x ≈ 10^-9, a tolerance of 1e-6 accepts garbage."),
        dict(type='cards', id='good', title='What makes a numerical method good?', n=4,
             cards=[dict(h='Accurate', t='The error can be made as small as we need, and we can <b>estimate</b> it.', cls='ok'),
                    dict(h='Efficient', t='Few operations per step and few steps. Cost matters when $n = 10^6$.', cls='blue'),
                    dict(h='Stable', t='Small round-off errors stay small instead of growing (Lecture 5).', cls='key'),
                    dict(h='Robust', t='Works for many inputs; fails loudly, not silently.', cls='bad')],
             below=dict(html='<p class="lead frag fade">No method wins on all four. Bisection is robust but slow; Newton is fast but can fail. Choosing the method for the problem is the skill this course builds.</p>'),
             notes="These four words return in every lecture. When we meet a new method, we will always ask: how accurate, how fast, how stable, how robust?"),
        dict(type='table', id='types', title='Types of iteration methods and their limitations', kick='Key summary',
             head=['Family', 'Methods', 'Needs', 'Strength', 'Limitation'], tx=(0, 1, 2, 3, 4), frag=True, cls='tb sm',
             rows=[['<b>Bracketing</b>', 'Bisection, False Position', 'An interval $[a,b]$ with $f(a)f(b)<0$', 'Always converges', 'Slow; needs a sign change; misses double roots like $(x-1)^2$'],
                   ['<b>Open: fixed point</b>', 'Iteration method $x = g(x)$', 'A rewrite $x = g(x)$ and $x_0$', 'Very simple', 'Converges only if $|g\'(x)| < 1$ near the root'],
                   ['<b>Open: Newton–Raphson</b>', 'Tangent line', '$f\'(x)$ and $x_0$', 'Very fast (digits double)', "Fails if $f'(x) \\approx 0$; may diverge from a poor $x_0$"],
                   ['<b>Open: Secant</b>', 'Chord through last two points', '$x_0$, $x_1$ (no derivative)', 'Fast, no derivative', 'May diverge; division by $f(x_1)-f(x_0) \\approx 0$'],
                   ['<b>Linear systems</b>', 'Jacobi, Gauss–Seidel', '$A\\mathbf{x}=\\mathbf{b}$, a starting vector', 'Cheap for huge sparse systems', 'Converges only for e.g. diagonally dominant $A$']],
             note='Lectures 6–10 study each root-finding method in detail; Lecture 14 covers iterative methods for linear systems.',
             notes="Reveal one row at a time.\n\nThe distinction to emphasise: bracketing methods trap the root between two points and cannot lose it; open methods use one or two points and can wander away, but are much faster when they work."),
        dict(type='ml', id='ml', items=[
            dict(ic='🧠', h='Training a neural network', t='Each epoch is one iteration $w_{k+1} = w_k - \\eta \\nabla L(w_k)$. The stopping rule is a tolerance on the loss or a maximum number of epochs: exactly today\'s two tests.'),
            dict(ic='🎮', h='Game physics at 60 frames per second', t='Every frame advances positions with a numerical ODE step. Too large a step and objects fly through walls: a stability failure.'),
            dict(ic='📈', h='Recommendation and ranking', t='PageRank and many recommender systems repeat $x_{k+1} = Mx_k$ until the vector stops changing.'),
            dict(ic='🔊', h='Speech processing', t='Pitch tracking finds roots of a correlation function; enhancement solves least-squares problems frame by frame.')],
            notes="Spend two minutes here, not more. The point: the loop structure on the Babylonian slide (guess, improve, check, repeat) is the same loop inside ML training, game engines and search engines.\n\nIf students ask about libraries: NumPy, SciPy and PyTorch implement these methods in optimised C and Fortran. Knowing what is inside lets you choose settings (tolerances, step sizes) and diagnose failures."),
        dict(type='exam', id='practice', src='Problem 2',
             q='"Why do we need to study numerical methods in CSE? Briefly describe different types of iteration methods and the limitations of each one of these."<br><span class="small">Another wording: "Why are numerical methods considered indispensable in computer science, and how do they address challenges posed by mathematical functions that lack analytical solutions?"</span>',
             tips=['Open with a definition: an algorithm of finite arithmetic steps that computes an approximate answer with a controlled error',
                   'Give <b>two or three concrete reasons</b> with examples: no closed form ($x=\\cos x$, quintics), huge systems, data with noise, ODEs',
                   'Name the families: <b>bracketing</b> (bisection, false position) and <b>open</b> (fixed point, Newton, secant)',
                   'One limitation each, in a small table',
                   'Finish with one CSE example (ML training, graphics, GPS)'],
             notes="Model the answer structure."),
        dict(type='check', id='check', q='Which one of these problems <b>needs</b> a numerical method?',
             opts=['Solve $2x + 3 = 7$', 'Solve $x = \\cos x$', 'Area of a circle of radius 3', 'Derivative of $x^2$'], right=1,
             answer='B. The others have exact formulas ($x=2$, $9\\pi$, $2x$). For $x=\\cos x$ we iterate: try $x_{k+1} = \\cos x_k$ from $x_0 = 1$ in the lab and watch it settle at 0.739085.',
             notes="Give 30 seconds, then a show of hands for A/B/C/D. Reveal.\n\nFollow-up for fast students: x = cos x can be solved by simply repeating x = cos(x) on a calculator (press cos over and over in radian mode). Try it: 1, 0.5403, 0.8576, 0.6543, ... slowly settling. That is fixed-point iteration, Lecture 8."),
        dict(type='summary', id='summary', items=[
            'Many problems (equations, integrals, ODEs, big systems, noisy data) have <b>no exact formula</b>',
            'A numerical method = <b>algorithm</b> + <b>error estimate</b> + <b>stopping rule</b>',
            'Iteration: guess → improve → check → repeat; Babylonian $\\sqrt{N}$ doubles the correct digits each step',
            'Stop on absolute or relative change, or residual, and always cap the iterations',
            'Bracketing methods are safe but slow; open methods are fast but can diverge'],
            hw=['By hand, find $\\sqrt{5}$ with $x_0 = 2$ until 4 decimal places agree. Show the table.',
                'In the lab, run $x_{k+1} = \\cos x_k$ from $x_0 = 1$. How many iterations until 6 decimals agree? Compare with Babylonian $\\sqrt{2}$.',
                'Write a half-page answer to Problem 2 with your own CSE example.'],
            next='<b>Floating-point numbers.</b> Why does $0.1 + 0.2 \\ne 0.3$ in Python and C? How many digits does a computer really keep, and what is machine epsilon?',
            notes="Recap in one minute using the five bullets.\n\nHomework answers (for you): Q1: x1 = 2.25, x2 = 2.236111, x3 = 2.236068, x4 = 2.236068, so √5 ≈ 2.2361. Q2: cos iteration needs 36 iterations for 6-decimal agreement (it converges linearly, rate |sin(0.739)| ≈ 0.67), versus 4–5 for Babylonian. This contrast previews linear vs quadratic convergence.\n\nTell them the lab for this lecture has the Babylonian explorer and two code tasks."),
    ],
    code={
        'sqrt_iter': dict(file='sqrt_babylonian', py='''# Babylonian (Heron's) method for the square root of N
N = 2.0
x = 1.0          # first guess
tol = 1e-12      # stop when two guesses agree this closely

for k in range(1, 50):
    x_new = 0.5 * (x + N / x)
    print(f"k = {k}:  x = {x_new:.15f}   change = {abs(x_new - x):.2e}")
    if abs(x_new - x) < tol:
        break
    x = x_new

print("sqrt(N) by iteration :", x_new)
print("N ** 0.5 for compare :", N ** 0.5)
''', c='''/* Babylonian (Heron's) method for the square root of N */
#include <stdio.h>
#include <math.h>

int main(void) {
    double N = 2.0;
    double x = 1.0;       /* first guess */
    double tol = 1e-12;   /* stop when two guesses agree this closely */
    double x_new = x;

    for (int k = 1; k < 50; k++) {
        x_new = 0.5 * (x + N / x);
        printf("k = %d:  x = %.15f   change = %.2e\\n", k, x_new, fabs(x_new - x));
        if (fabs(x_new - x) < tol)
            break;
        x = x_new;
    }
    printf("sqrt(N) by iteration : %.16g\\n", x_new);
    printf("sqrt(N) from math.h  : %.16g\\n", sqrt(N));
    return 0;
}
'''),
        'cos_iter': dict(file='cos_fixed_point', py='''# Solve x = cos(x) by repeating x <- cos(x)
import math

x = 1.0
for k in range(1, 101):
    x_new = math.cos(x)
    if abs(x_new - x) < 0.5e-6:      # 6 decimal places agree
        print(f"converged after {k} iterations: x = {x_new:.6f}")
        break
    x = x_new
else:
    print("did not converge in 100 iterations")
''', c='''/* Solve x = cos(x) by repeating x <- cos(x) */
#include <stdio.h>
#include <math.h>

int main(void) {
    double x = 1.0, x_new;
    int k, done = 0;
    for (k = 1; k <= 100; k++) {
        x_new = cos(x);
        if (fabs(x_new - x) < 0.5e-6) {   /* 6 decimal places agree */
            printf("converged after %d iterations: x = %.6f\\n", k, x_new);
            done = 1;
            break;
        }
        x = x_new;
    }
    if (!done) printf("did not converge in 100 iterations\\n");
    return 0;
}
'''),
    },
    lab=dict(title='Iteration Lab',
             intro='Run your first numerical methods: watch digits appear, then write and change the loops yourself.',
             tabs=[
                 dict(name='Explore', blocks=[
                     dict(p='Pick any positive N and a starting guess. Each step averages x and N/x. Watch the <b>correct digits</b> column: it roughly doubles every step.'),
                     dict(w='babylon', o=dict(N=2, x0=1)),
                     dict(p='<b>Try this:</b> N = 10 with x₀ = 1; N = 2 with x₀ = 1000 (a terrible guess: how many extra steps?); N = 0.0001.')]),
                 dict(name='Code: square root', blocks=[
                     dict(code='sqrt_iter', tasks=['Run it in Python, then switch to C and run again. Are the numbers identical?', 'Change N to 10. Which iteration first shows 1e-12 or smaller?', 'Change the first guess to 1000. Count the extra iterations.', 'Set tol = 1e-20. Why does the loop now run until k = 49? (Hint: about 16 digits)', 'Add a counter and print "iterations used" at the end.'])]),
                 dict(name='Code: x = cos x', blocks=[
                     dict(code='cos_iter', tasks=['Run it. How many iterations for 6 decimals?', 'Compare with the square-root loop (about 5). Which converges faster?', 'Change the start to x = 100. Does it still converge?', 'Try x = 2cos(x) instead (change the line). What happens?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Find $\\sqrt{5}$ by the Babylonian method with $x_0 = 2$, correct to 4 decimal places.', '$x_1 = \\tfrac12(2 + 5/2) = 2.25$, $x_2 = \\tfrac12(2.25 + 5/2.25) = 2.236111$, $x_3 = 2.236068$, $x_4 = 2.236068$. Since $|x_4 - x_3| < 0.00005$, $\\sqrt5 \\approx 2.2361$.'),
                         ('State three different stopping criteria for an iteration and say when each is preferred.', 'Absolute change $|x_{k+1}-x_k| < \\varepsilon$ (values of moderate size); relative change $|x_{k+1}-x_k|/|x_{k+1}| < \\varepsilon$ (very large or very small values); residual $|f(x_k)| < \\varepsilon$ (root finding, when $f$ is well scaled). Always add a maximum iteration count.'),
                         ('Distinguish analytical and numerical solutions with one example of each.', 'Analytical: exact formula, e.g. $x = (-b\\pm\\sqrt{b^2-4ac})/2a$. Numerical: approximate number from an algorithm with an error estimate, e.g. $x = \\cos x \\Rightarrow x \\approx 0.739085$ by iteration.'),
                         ('Why is a maximum number of iterations needed even when we have a tolerance?', 'If the method diverges or oscillates, or if the tolerance is smaller than the precision of the computer allows (about $10^{-16}$ relative), the tolerance is never met and the loop would run forever.'),
                         ('Name the two families of root-finding iteration methods and give one limitation of each.', 'Bracketing (bisection, false position): slow, needs $f(a)f(b) < 0$. Open (fixed point, Newton, secant): may diverge; Newton needs $f\'(x)$ and fails when $f\'(x) \\approx 0$.')])])]),
)
