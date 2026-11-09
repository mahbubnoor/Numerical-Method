"""25-lecture roadmap for CSE-3107 Numerical Methods (University of Barishal).
Ordered by dependency: every lecture uses only ideas taught before it. `needs` lists the lectures it builds on."""
ROADMAP = [
    # Module 1: foundations. Round-off, then truncation (Taylor), then how both propagate, then sensitivity.
    dict(n=1, needs=[], title='Why Numerical Methods?', topics='Modelling pipeline, analytical vs numerical solutions, iteration and stopping rules, CSE and ML case studies'),
    dict(n=2, needs=[1], title='Floating-Point Numbers', topics='Binary fractions, IEEE 754 single and double, machine epsilon, rounding vs chopping, significant digits'),
    dict(n=3, needs=[1], title='Taylor Series and Order of Accuracy', topics='Taylor expansion and remainder, truncation error bounds, big-O and order of accuracy, forward and central differences'),
    dict(n=4, needs=[2, 3], title='Errors and Their Propagation', topics='Absolute, relative and percentage error, error propagation, catastrophic cancellation, best step size (truncation vs round-off)'),
    dict(n=5, needs=[3, 4], title='Conditioning and Stability', topics='Well- and ill-conditioned problems, condition number, forward and backward error, stable vs unstable algorithms'),
    # Module 2: nonlinear equations. Bracketing first (safe), then open methods (fast), then systems.
    dict(n=6, needs=[1, 4], title='Root Finding and the Bisection Method', topics='Bracketing, intermediate value theorem, error bound, number of iterations, bisection code in Python and C'),
    dict(n=7, needs=[6], title='The False Position Method', topics='Regula Falsi as a chord method, worked examples, comparison with bisection, the one-sided stall and its fix'),
    dict(n=8, needs=[3, 6], title='Fixed-Point Iteration', topics='Method of iteration x = g(x), convergence condition |g′(x)| < 1, choosing g, cobweb diagrams, linear convergence'),
    dict(n=9, needs=[3, 8], title='The Newton–Raphson Method', topics='Tangent-line derivation, quadratic convergence, failure cases, square-root algorithm, Newton in Python and C'),
    dict(n=10, needs=[7, 9], title='Secant Method and Nonlinear Systems', topics='Secant method, order of convergence compared, choosing a method, Newton for systems and the Jacobian'),
    # Module 3: linear systems. Needed by splines (tridiagonal), least squares (normal equations), stability of ODEs (eigenvalues).
    dict(n=11, needs=[5], title="Linear Systems, Cramer's Rule and the Inverse", topics="Matrix form Ax = b, Cramer's rule, matrix inversion, cost of each, vector and matrix norms, condition number"),
    dict(n=12, needs=[5, 11], title='Gaussian and Gauss–Jordan Elimination', topics='Forward elimination and back substitution, Gauss–Jordan, operation count, partial pivoting, growth factor'),
    dict(n=13, needs=[12], title='LU, Cholesky and Tridiagonal Systems', topics='Doolittle and Crout LU, many right-hand sides, symmetric positive definite matrices, Cholesky, Thomas algorithm'),
    dict(n=14, needs=[8, 12], title='Iterative Methods: Jacobi, Gauss–Seidel, SOR', topics='Jacobi and Gauss–Seidel, diagonal dominance, eigenvalue recap and spectral radius, SOR, sparse matrices'),
    # Module 4: interpolation. Operators first: they generate every formula that follows.
    dict(n=15, needs=[3], title='Finite Differences and Operators', topics='Difference tables, Δ, ∇, δ, E, μ, D and their relations, E = e^(hD), differences of a polynomial, missing terms'),
    dict(n=16, needs=[15], title="Newton's Forward and Backward Interpolation", topics='Newton–Gregory formulas for equal intervals, choosing forward or backward, interpolation vs extrapolation, error'),
    dict(n=17, needs=[15, 16], title='Lagrange and Divided-Difference Interpolation', topics="Unequal intervals, Lagrange's formula, Newton's divided differences, inverse interpolation"),
    dict(n=18, needs=[13, 17], title='Spline Interpolation and the Runge Phenomenon', topics='Why high-degree polynomials oscillate, linear and cubic splines, smoothness conditions, natural splines'),
    # Module 5: calculus. Built directly on the interpolation formulas.
    dict(n=19, needs=[3, 4, 16], title='Numerical Differentiation', topics="Derivatives from Newton's formulas and from Taylor series, second derivatives, step size, Richardson extrapolation"),
    dict(n=20, needs=[16, 19], title='Numerical Integration', topics='General quadrature formula, trapezoidal, Simpson 1/3 and 3/8, composite rules and their errors, Romberg, Gauss (intro)'),
    # Module 6: ODEs. Heun uses the trapezoid rule, Milne uses Simpson, Adams uses backward differences.
    dict(n=21, needs=[3, 20], title='ODEs I: Taylor, Picard and Euler Methods', topics="Initial value problems, Picard's method, Taylor series method, Euler and modified Euler (Heun), local vs global error"),
    dict(n=22, needs=[16, 20, 21], title='ODEs II: Runge–Kutta and Predictor–Corrector', topics="RK2 and RK4, Milne's and Adams predictor–corrector methods, stability, stiff equations"),
    # Module 7: data fitting and optimization for machine learning.
    dict(n=23, needs=[5, 13], title='Least Squares and Linear Regression', topics='Overdetermined systems, normal equations, geometric meaning, goodness of fit, conditioning, link to machine learning'),
    dict(n=24, needs=[23], title='Polynomial, Exponential and Trigonometric Fitting', topics='Polynomial regression, linearising y = ae^(bx) and y = ax^b, trigonometric fits, overfitting'),
    dict(n=25, needs=[6, 9, 10, 14, 24], title='Numerical Optimization for Machine Learning', topics="Golden-section search, gradient descent, learning rate and curvature, Newton's method for optimisation, Gauss–Newton"),
]
MODULES = [
    ('Foundations of numerical computing', 'Lectures 1–5', range(1, 6)),
    ('Solving nonlinear equations', 'Lectures 6–10', range(6, 11)),
    ('Systems of linear equations', 'Lectures 11–14', range(11, 15)),
    ('Finite differences and interpolation', 'Lectures 15–18', range(15, 19)),
    ('Numerical differentiation and integration', 'Lectures 19–20', range(19, 21)),
    ('Ordinary differential equations', 'Lectures 21–22', range(21, 23)),
    ('Data fitting and optimization for machine learning', 'Lectures 23–25', range(23, 26)),
]
