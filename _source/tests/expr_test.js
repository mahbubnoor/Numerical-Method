require('../src/assets/expr.js');
const cases=[['x^3 - x - 2',1.5],['2x^3-2x-5',1.3],['e^x - 3x',0.6],['3x + sin x - e^x',0.4],['x^2-4x-10',5.5],['ln(x)',2],['x e^x - 1',0.5],['cos x - x e^x',0.5],['sqrt(1+x^2)',1],['1/(1+x)',0.5],['x^x',1.5],['sin^2(x)',0.7],['(x+1)(x-2)',3],['xsin(x)',1]];
for(const [s,x] of cases){ const f=Expr.make(s), d=f.deriv(); const h=1e-6, num=(f(x+h)-f(x-h))/(2*h);
 console.log(s.padEnd(18),'| text:',f.text.padEnd(22),"| f'=",d.text.padEnd(34),'| err',Math.abs(d(x)-num).toExponential(1),'| tex',d.tex); }
