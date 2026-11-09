LECTURE = dict(
    title='Floating-Point Numbers',
    sub='A computer keeps about 7 or 16 significant digits, in binary. That one fact explains why 0.1 + 0.2 ≠ 0.3, and sets the accuracy limit of every method in this course.',
    slides=[
        dict(type='cover', id='cover', notes="Start with a live demo before any theory. Type into Python on the projector: 0.1 + 0.2 == 0.3. It prints False. Ask: \"Is Python broken?\" Collect answers.\n\nIt is not broken; it is doing exactly what the IEEE 754 standard says. By the end of today students can explain the exact number that is stored for 0.1, and why the comparison fails."),
        dict(type='goals', id='goals', items=[
            'Convert decimal fractions to <b>binary</b> and see why 0.1 never ends',
            'Write numbers in <b>normalised floating-point form</b> and count <b>significant digits</b>',
            'Read the three fields of an <b>IEEE 754</b> single and double number',
            'Define and compute <b>machine epsilon</b>; explain rounding vs chopping',
            'Recognise overflow, underflow and safe ways to <b>compare</b> floating-point numbers'],
            prev='Numerical methods compute approximate answers by iteration; we stop when the change is small enough.',
            today='How small can "small enough" be? The answer is set by how numbers are stored: about 16 significant decimal digits in double precision.',
            notes="Link to Lecture 1: the tol = 1e-20 experiment never stopped early. Today explains why: the gap between neighbouring doubles near 1.4 is about 2.2e-16, so two successive iterates can never differ by 1e-20 unless they are equal."),
        dict(type='worked', id='binary', title='Decimal fractions in binary: multiply by 2',
             src='Problem 1', q='Convert $0.625_{10}$ and $0.1_{10}$ to binary. Rule: multiply the fraction by 2; the integer part is the next bit.',
             steps=['$0.625 \\times 2 = 1.25 \\Rightarrow$ bit <b>1</b>, keep 0.25', '$0.25 \\times 2 = 0.5 \\Rightarrow$ bit <b>0</b>; $\\;0.5 \\times 2 = 1.0 \\Rightarrow$ bit <b>1</b>, remainder 0: stop. So $0.625_{10} = 0.101_2$ (exact)',
                    '$0.1 \\times 2 = 0.2 \\to 0,\\; 0.4 \\to 0,\\; 0.8 \\to 0,\\; 1.6 \\to 1,\\; 1.2 \\to 1,\\; 0.4 \\to 0, \\dots$',
                    'The remainder 0.4 has appeared before, so the pattern <b>repeats forever</b>: $0.1_{10} = 0.0\\overline{0011}_2$'],
             answer='A fraction is exact in binary only if its denominator is a power of 2 (½, ¼, ⅝ …). $0.1 = \\tfrac{1}{10}$ is not, so the computer must <b>cut it off</b>: a round-off error before any arithmetic happens.',
             right=dict(table=[['step', 'fraction × 2', 'bit'], [[1, '0.2', '0'], [2, '0.4', '0'], [3, '0.8', '0'], [4, '1.6', '1'], [5, '1.2', '1'], [6, '0.4', '0'], [7, '0.8', '0'], [8, '1.6', '1'], ['…', '…', '…']]]), rw=520,
             notes="Do 0.625 on the board first: students get a finite answer and feel confident. Then do 0.1 and let them discover the repetition themselves (0.4 comes back at step 6).\n\nAnalogy: 1/3 = 0.3333... never ends in decimal because 3 does not divide a power of 10. Likewise 1/10 never ends in binary because 10 = 2 × 5 and 5 does not divide a power of 2.\n\nCHECKPOINT (oral): 'Is 0.75 exact in binary?' Yes: 0.11. 'Is 0.2?' No."),
        dict(type='bullets', id='flform', title='Floating-point form and significant digits', rw=780,
             items=['<b>Normalised floating-point form</b> (decimal): $x = \\pm\\, 0.d_1 d_2 \\dots d_t \\times 10^{e}$ with $d_1 \\ne 0$',
                    'The digits $d_1 \\dots d_t$ are the <b>mantissa</b>; $e$ is the <b>exponent</b>; $t$ is the precision',
                    'Example: $-347.62 = -0.34762 \\times 10^{3}$, $\\;0.000123 = 0.123 \\times 10^{-3}$',
                    '<b>Significant digits</b>: all digits from the first non-zero digit onward. $0.000123$ has 3; $2.500$ has 4; $3070$ has 3 or 4 (ambiguous: write $0.3070\\times10^4$)',
                    'A computer stores only $t$ digits, so most real numbers are replaced by a nearby representable one'],
             right=dict(cards=[dict(tag='Chopping', h='Cut off extra digits', t='$\\tfrac{2}{3} = 0.666666\\dots \\to 0.6666$ (4 digits). Error up to one unit in the last place.'),
                               dict(tag='Rounding', h='Round to nearest', t='$\\tfrac{2}{3} \\to 0.6667$. Error at most <b>half</b> a unit in the last place. IEEE uses round-to-nearest, ties to even.', cls='key')], n=1),
             notes="The '3070' example: trailing zeros in an integer are ambiguous; scientific notation removes the ambiguity. Leading zeros are never significant.\n\nRounding error bound: with t-digit rounding in base 10, relative error ≤ 0.5 × 10^(1−t). Chopping: ≤ 10^(1−t)."),
        dict(type='html', id='ieee', title='IEEE 754: the format inside every CPU',
             lead='The same idea as scientific notation, but in base 2: $x = (-1)^{s} \\times 1.f \\times 2^{\\,E - \\text{bias}}$',
             html='<div class="grid g2"><div class="card blue"><h3>single (C <code>float</code>), 32 bits</h3><div style="display:flex;gap:4px;font:600 26px var(--mono);margin:8px 0"><div style="background:#c0392b;color:#fff;padding:8px 14px;border-radius:8px">1</div><div style="background:#2e7d4f;color:#fff;padding:8px 14px;border-radius:8px;flex:8">8 exponent</div><div style="background:#2f6db5;color:#fff;padding:8px 14px;border-radius:8px;flex:23">23 fraction</div></div><p>bias 127 · about <b>7</b> decimal digits · range ≈ $10^{\\pm 38}$</p></div>'
                  '<div class="card key"><h3>double (C <code>double</code>, Python <code>float</code>), 64 bits</h3><div style="display:flex;gap:4px;font:600 26px var(--mono);margin:8px 0"><div style="background:#c0392b;color:#fff;padding:8px 14px;border-radius:8px">1</div><div style="background:#2e7d4f;color:#fff;padding:8px 14px;border-radius:8px;flex:11">11 exponent</div><div style="background:#2f6db5;color:#fff;padding:8px 14px;border-radius:8px;flex:52">52 fraction</div></div><p>bias 1023 · about <b>16</b> decimal digits · range ≈ $10^{\\pm 308}$</p></div></div>'
                  '<div class="steps" style="margin-top:8px"><div class="frag fade"><span class="n">1</span><div>Example: $-6.25 = -110.01_2 = -1.1001_2 \\times 2^{2}$</div></div><div class="frag fade"><span class="n">2</span><div>sign $s = 1$; exponent field $E = 2 + 127 = 129 = 10000001_2$; fraction $f = 1001000\\dots0$ (the leading 1 is not stored)</div></div><div class="frag fade"><span class="n">3</span><div>Bits: <span class="mono"><span class="rd">1</span> <span class="gr">10000001</span> <span class="bl">10010000000000000000000</span></span> = <span class="mono">0xC0C80000</span></div></div></div>',
             notes="Walk through the two layouts, then the worked example step by step.\n\nThe 'hidden bit': in normalised binary the first digit is always 1, so IEEE does not store it. That gives one free bit of precision: 24 significant bits in single, 53 in double.\n\nWhy a bias instead of a signed exponent: it lets hardware compare positive floats as if they were integers.\n\nPython's float is a C double. C's float is single precision: use double in numerical code unless memory is very tight (GPUs and ML sometimes use float or even 16-bit formats)."),
        dict(type='widget', id='bits', title='Explore: what is really stored?', w='fpbits', o=dict(value='0.1', prec='single'), lw=560,
             items=['Type <b>0.1</b>: the stored value is not 0.1', 'Switch to <b>double</b>: closer, still not exact', 'Try <b>0.5</b> or <b>−6.25</b>: exact, because they are sums of powers of 2', 'Try <b>16777217</b> in single: the integer itself cannot be stored ($2^{24}+1$)'],
             notes="Use the widget live. For 0.1 in single precision, the stored value is 0.100000001490116119384765625. In double: 0.1000000000000000055511151231257827...\n\nThe 16777217 example surprises students: single precision cannot even store every integer above 2^24 = 16,777,216. Doubles lose integers above 2^53 ≈ 9 × 10^15.\n\nLet students suggest numbers."),
        dict(type='math', id='eps', title='Machine epsilon: the precision of the machine',
             eqs=[dict(cap='Definition: the gap between 1 and the next larger float', eq='\\varepsilon_{\\text{mach}} = (\\text{next float after } 1) - 1'),
                  dict(cap='Values', eq='\\begin{aligned} \\varepsilon_{\\text{single}} &= 2^{-23} \\approx 1.19\\times10^{-7} \\\\ \\varepsilon_{\\text{double}} &= 2^{-52} \\approx 2.22\\times10^{-16} \\end{aligned}'),
                  dict(cap='Rounding error bound', eq='\\text{fl}(x) = x(1 + \\delta), \\qquad |\\delta| \\le \\tfrac{1}{2}\\,\\varepsilon_{\\text{mach}}', frag=True)],
             items=['Relative spacing of floats is about $\\varepsilon$ everywhere: the gap near $10^{6}$ is about $2.2\\times10^{-10}$', 'So a double holds about $\\log_{10}(1/\\varepsilon) \\approx 16$ significant decimal digits', 'No tolerance smaller than about $\\varepsilon\\,|x|$ can ever be met', '$1 + \\varepsilon/2$ rounds back to exactly 1'],
             ifrag=True,
             notes="Machine epsilon is the single most useful number in this course. It tells you the best relative accuracy you can hope for.\n\nThe third box is the model of floating-point arithmetic: every stored number, and every result of +, −, ×, ÷, is the true value times (1 + δ) with |δ| at most half of epsilon (the unit round-off u ≈ 1.1e-16).\n\nSome books define machine epsilon as u = ε/2. Be clear which one you use; the code on the next slide finds 2^-52."),
        dict(type='code', id='code_eps', title='Find machine epsilon by experiment', code='eps', lw=600,
             items=['Halve $\\varepsilon$ until $1 + \\varepsilon/2$ is no longer different from 1', 'The C version also does it in <b>float</b>: about $10^{-7}$', 'Python has <code>sys.float_info.epsilon</code>; C has <code>DBL_EPSILON</code> in &lt;float.h&gt;'],
             notes="Run both. In C the float loop must store the result in a float variable each time; otherwise the compiler may keep extra precision (on x86-64 with SSE it does not, so the answer is 2^-23 = 1.19e-07).\n\nAsk: why do we test 1 + eps/2 != 1 and not eps/2 != 0? Because eps/2 is not zero for a very long time (down to 5e-324). We want the precision relative to 1, not the smallest number."),
        dict(type='code', id='code_01', title='0.1 + 0.2, and how to compare floats', code='point1', lw=620,
             items=['Neither 0.1, 0.2 nor 0.3 is exact; the rounding errors do not cancel', 'Never test floats with <code>==</code>; test <code>abs(a - b) &lt; tol</code>', 'Use a <b>relative</b> tolerance for large numbers: <code>math.isclose(a, b)</code>', 'Adding 0.1 ten times also misses 1.0: errors <b>accumulate</b>'],
             notes="Key practical rule for programmers: never compare floating-point results with ==. Loops like 'while x != 1.0: x += 0.1' never stop.\n\nThe printed 0.30000000000000004 is the shortest decimal that identifies the stored double uniquely; Python prints it so that float(repr(x)) == x.\n\nSwitch to the C tab: printf with %.17g shows the same 0.30000000000000004."),
        dict(type='code', id='code_float', title='float vs double: accumulation in C', code='floatsum', lang='c', lw=620,
             items=['Add 0.1 one million times. The true answer is 100000', '<code>float</code> drifts by about 1000: wrong in the 3rd significant digit', '<code>double</code> is wrong only after about 10 digits', 'Lesson: use <b>double</b> for numerical work; keep sums in double even if data are float'],
             notes="This is a C-only demo, because Python has no single-precision float without NumPy.\n\nWhy so bad for float: once the running sum is near 100000, the gap between floats is about 0.0078, so every '+ 0.1' is rounded to a multiple of 0.0078: each addition makes an error of up to 0.004, and a million additions add up.\n\nThe same effect makes deep-learning frameworks accumulate gradients in higher precision even when weights are stored in 16-bit."),
        dict(type='widget', id='line', title='Floats are not evenly spaced', w='fpline', o=dict(t=3, height='300px'), lw=560,
             items=['A toy system: base 2, 3 fraction bits, exponents −2 to 2', 'Each colour is one exponent: inside it, numbers are equally spaced', 'The gap <b>doubles</b> at each power of 2', 'But the <b>relative</b> gap stays about the same: that is machine epsilon'],
             notes="Drag the x slider and watch the nearest representable number (red dot). Near 0.25 the gaps are tiny; near 6 they are large.\n\nThis picture explains the relative error bound: absolute errors grow with the size of the number, relative errors do not.\n\nIncrease the bits slider: more numbers, smaller gaps, smaller epsilon. Real doubles have 52 fraction bits."),
        dict(type='cards', id='limits', title='At the edges: overflow, underflow, special values', n=3, frag=True,
             cards=[dict(tag='Overflow', h='Too big', t='$10^{308} \\times 10 = \\infty$ (inf). In Python, <code>2.0**1024</code> raises <i>OverflowError</i>; <code>math.exp(1000)</code> too.', cls='bad'),
                    dict(tag='Underflow', h='Too small', t='$10^{-320}$ is stored as a <b>subnormal</b> with fewer digits; below $5\\times10^{-324}$ it becomes 0.', cls='blue'),
                    dict(tag='NaN', h='Not a Number', t='$0/0$, $\\infty - \\infty$, $\\sqrt{-1}$ in C give NaN. NaN ≠ NaN: even <code>x == x</code> is false.', cls='key')],
             below=dict(html='<div class="ml frag fade"><span class="ic">🧠</span><div><h3>When training "blows up"</h3><p>A loss that becomes <b>NaN</b> or <b>inf</b> is usually overflow in <code>exp</code> (softmax) or a division by a tiny number. Libraries compute softmax as $e^{x_i - \\max x}$ to avoid overflow: a numerical-methods trick.</p></div></div>'),
             notes="Reveal the three cards, then the ML example.\n\nSoftmax trick: e^(x_i) overflows for x_i > 709. Subtracting the maximum first gives the same mathematical result (it cancels in the ratio) but every exponent is ≤ 0, so no overflow. Show on the board: e^(1000)/(e^(1000)+e^(999)) = 1/(1+e^(−1)).\n\nNaN propagates silently through every later operation; that is why a single bad value ruins a whole training run."),
        dict(type='check', id='check', q='In double precision, which of these is stored <b>exactly</b>?',
             opts=['0.1', '0.375', '1/3', '0.2 + 0.1'], right=1,
             answer='B: $0.375 = \\tfrac{3}{8} = 0.011_2$. The others have denominators that are not powers of 2, so their binary expansions never end.',
             notes="30 seconds, show of hands. Most students will get B now.\n\nFollow-up: 'Which is stored exactly: 1e22 or 1e23?' 1e22 is exact (10^22 = 2^22 × 5^22 and 5^22 < 2^53); 1e23 is not. A nice surprise for strong students."),
        dict(type='exam', id='practice', src='Problem 2',
             q='"Discuss the importance of numerical methods in computing science. Define the floating-point form of numbers, significant digit of a number and round-off error."',
             tips=['Floating-point form: $\\pm 0.d_1d_2\\dots d_t \\times \\beta^{e}$, $d_1 \\ne 0$; name mantissa, base, exponent; give one example',
                   'Significant digits: digits from the first non-zero digit; example $0.004560$ has 4 significant digits',
                   'Round-off error: true value − stored value, caused by keeping only $t$ digits; example $2/3 \\to 0.6667$, error $3.3\\times10^{-5}$',
                   'Mention chopping vs rounding and the bound $\\tfrac{1}{2}\\times10^{1-t}$ (relative) for rounding',
                   'One sentence of importance (Lecture 1) to open the answer'],
             notes="Insist on an example for each definition."),
        dict(type='summary', id='summary', items=[
            'Only fractions with power-of-2 denominators are exact in binary; 0.1 is not',
            'Floating point = sign × mantissa × base<sup>exponent</sup>, normalised; IEEE double has 53 significant bits',
            '$\\varepsilon_{\\text{mach}} = 2^{-52} \\approx 2.2\\times10^{-16}$: about 16 significant digits; rounding error ≤ ε/2 relative',
            'Never compare floats with ==; use a tolerance, preferably relative',
            'Use double; beware accumulation, overflow (inf), underflow and NaN'],
            hw=['Convert 13.375 and 0.3 to binary. Which one is exact?', 'Write 0.000452 and 45200 in normalised floating-point form and state the number of significant digits of each.', 'In the lab: find the stored double for 0.7 with the bit explorer. Is it above or below 0.7?', 'Run the float-vs-double C program with 10 million additions. Describe what happens to the float sum.'],
            next='<b>Taylor series and order of accuracy.</b> Round-off is one source of error; the other is truncation. The Taylor series predicts it, and every method in this course is built on it.',
            notes="Homework answers: 13.375 = 1101.011 (exact); 0.3 = 0.0100110011... (repeats, not exact). 0.000452 = 0.452 × 10^-3 (3 significant digits); 45200 = 0.452 × 10^5 (3 significant, or 5 if the zeros are measured). 0.7 is stored as 0.6999999999999999555910790149937 (below). With 10^7 additions the float sum is 1087937 instead of 1000000 (8.8% too high): above 2^19 = 524288 the gap between floats is 0.0625, so every + 0.1 is rounded to + 0.125."),
    ],
    code={
        'eps': dict(file='machine_epsilon', py='''# Machine epsilon: halve eps until 1 + eps/2 == 1
import sys
import math

eps = 1.0
count = 0
while 1.0 + eps / 2 != 1.0:
    eps = eps / 2
    count += 1

print("halvings      :", count)
print("machine eps   :", eps)
print("equals 2**-52 :", eps == 2**-52)
print("sys.float_info:", sys.float_info.epsilon)
print("digits ~      :", round(-math.log10(eps), 1))
''', c='''/* Machine epsilon in double and in float */
#include <stdio.h>
#include <float.h>

int main(void) {
    double eps = 1.0;
    int count = 0;
    while (1.0 + eps / 2 != 1.0) {
        eps = eps / 2;
        count++;
    }
    printf("double: halvings %d, eps = %g (DBL_EPSILON = %g)\\n", count, eps, DBL_EPSILON);

    float feps = 1.0f, one = 1.0f, test = 2.0f;
    count = 0;
    while (test != one) {
        feps = feps / 2;
        test = one + feps / 2;    /* stored back into a float */
        count++;
    }
    printf("float : halvings %d, eps = %g (FLT_EPSILON = %g)\\n", count, feps, FLT_EPSILON);
    return 0;
}
'''),
        'point1': dict(file='point_one', py='''import math

a = 0.1 + 0.2
print(a)
print(a == 0.3)                     # never compare floats with ==
print(abs(a - 0.3) < 1e-12)         # absolute tolerance
print(math.isclose(a, 0.3))         # relative tolerance (1e-9)
print(f"{0.1:.20f}")                # what is really stored

total = 0.0
for i in range(10):
    total += 0.1
print("0.1 added ten times:", total, " equal to 1.0?", total == 1.0)
''', c='''#include <stdio.h>
#include <math.h>

int main(void) {
    double a = 0.1 + 0.2;
    printf("%.17g\\n", a);
    printf("a == 0.3 ? %d\\n", a == 0.3);              /* 0 means false */
    printf("|a - 0.3| < 1e-12 ? %d\\n", fabs(a - 0.3) < 1e-12);
    printf("%.20f\\n", 0.1);

    double total = 0.0;
    for (int i = 0; i < 10; i++)
        total += 0.1;
    printf("0.1 added ten times: %.17g  equal to 1.0? %d\\n", total, total == 1.0);
    return 0;
}
'''),
        'floatsum': dict(file='float_vs_double', c='''/* Add 0.1 one million times in float and in double */
#include <stdio.h>

int main(void) {
    float  fs = 0.0f;
    double ds = 0.0;
    int n = 1000000;
    for (int i = 0; i < n; i++) {
        fs += 0.1f;
        ds += 0.1;
    }
    printf("true sum  : %d\\n", n / 10);
    printf("float sum : %.6f   error %.6f\\n", fs, fs - 100000.0);
    printf("double sum: %.6f   error %.3e\\n", ds, ds - 100000.0);
    return 0;
}
'''),
        'binconv': dict(file='decimal_to_binary', py='''# Convert a decimal fraction to binary by repeated multiplication by 2
x = 0.1
bits = ""
seen = {}
for step in range(1, 25):
    x = x * 2
    bit = int(x)
    bits += str(bit)
    x = x - bit
    print(f"step {step:2d}: bit {bit}, remainder {x:.6f}")
    if x == 0:
        break
print("0." + bits)
''', c='''/* Convert a decimal fraction to binary by repeated multiplication by 2 */
#include <stdio.h>

int main(void) {
    double x = 0.1;
    char bits[64];
    int n = 0;
    for (int step = 1; step <= 24; step++) {
        x = x * 2;
        int bit = (int)x;
        bits[n++] = '0' + bit;
        x = x - bit;
        printf("step %2d: bit %d, remainder %.6f\\n", step, bit, x);
        if (x == 0) break;
    }
    bits[n] = 0;
    printf("0.%s\\n", bits);
    return 0;
}
'''),
    },
    lab=dict(title='Floating-Point Lab',
             intro='See the bits inside a number, measure machine epsilon, and watch errors accumulate.',
             tabs=[
                 dict(name='Bit explorer', blocks=[
                     dict(p='Type any number (you can also type fractions such as 1/3). The sign, exponent and fraction bits update instantly, with the exact decimal value that is stored.'),
                     dict(w='fpbits', o=dict(value='0.1', prec='double')),
                     dict(p='<b>Try this:</b> 0.7 (is the stored value above or below?), 1e22 and 1e23 (one is exact), 1/3 in single vs double, 2^53 + 1 = 9007199254740993.')]),
                 dict(name='Number line', blocks=[
                     dict(p='A toy floating-point system with only a few bits. Move x and see which number it is stored as. Change the number of fraction bits.'),
                     dict(w='fpline', o=dict(t=3, height='260px'))]),
                 dict(name='Code', blocks=[
                     dict(h='Decimal to binary'), dict(code='binconv', tasks=['Run it for 0.1. At which step does the pattern start to repeat?', 'Change x to 0.625. Why does it stop after 3 steps?', 'Try 0.3 and 0.2. Which bits repeat?']),
                     dict(h='Machine epsilon'), dict(code='eps', tasks=['Run in Python and in C. Same double epsilon?', 'In C, what is the float epsilon?', 'Change the test to 1.0 + eps != 1.0 (no /2). What do you get and why is it ε/2?']),
                     dict(h='float vs double'), dict(code='floatsum', lang='c', tasks=['Run it. How big is the float error?', 'Change n to 10000000. The true sum is 1000000; why is the float sum about 1087937? (Hint: the gap between floats above 524288 is 0.0625)', 'Keep fs as float but add 0.1 (a double). Does it help?'])]),
                 dict(name='Practice', blocks=[
                     dict(qa=[
                         ('Convert $0.6875_{10}$ to binary.', '$0.6875\\times2=1.375\\to1$, $0.375\\times2=0.75\\to0$, $0.75\\times2=1.5\\to1$, $0.5\\times2=1.0\\to1$. So $0.1011_2$ (exact).'),
                         ('Write $-0.0003470$ in normalised decimal floating-point form. How many significant digits?', '$-0.3470\\times10^{-3}$; 4 significant digits (the trailing zero after 7 is significant, the leading zeros are not).'),
                         ('Represent $2/3$ with 4-digit chopping and 4-digit rounding. Give the absolute and relative error of each.', 'Chopping: $0.6666$, error $6.67\\times10^{-5}$, relative $1.0\\times10^{-4}$. Rounding: $0.6667$, error $3.33\\times10^{-5}$, relative $5.0\\times10^{-5}$.'),
                         ('Give the IEEE 754 single-precision bit pattern of $5.75$.', '$5.75 = 101.11_2 = 1.0111_2\\times2^{2}$. Sign 0, exponent $2+127 = 129 = 10000001$, fraction $0111000\\dots$. Bits: 0 10000001 01110000000000000000000 = 0x40B80000.'),
                         ('What is machine epsilon, and why can an iteration never meet the tolerance $10^{-20}$ in double precision?', '$\\varepsilon = 2^{-52} \\approx 2.2\\times10^{-16}$ is the gap between 1 and the next double. Neighbouring doubles near $x$ differ by about $\\varepsilon|x|$, so two different iterates near 1 always differ by at least $2.2\\times10^{-16} > 10^{-20}$.'),
                         ('Why is <code>if (x == 0.3)</code> dangerous after computing <code>x = 0.1 + 0.2</code>? What should be written?', 'Both sides carry different rounding errors (0.30000000000000004 vs 0.29999999999999998890), so the test is false. Write <code>fabs(x - 0.3) &lt; 1e-12</code>, or a relative test <code>fabs(x - y) &lt;= 1e-12 * fabs(y)</code>.')])])]),
)
