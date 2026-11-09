require('../src/assets/numfmt.js'); const F=globalThis.NumFmt; const d=require('./fmt.json');
let bad=0, n=0;
for(const [x,res,rep,r2] of d.rows){ d.specs.forEach((s,i)=>{n++; const g=F.pyFormat(x,s,'float',null); if(g!==res[i]){ if(bad<15) console.log('spec',s,x,'py',res[i],'js',g); bad++;}});
 n++; if(F.pyRepr(x)!==rep){bad++; if(bad<15)console.log('repr',x,rep,F.pyRepr(x));}
 if(r2!==null){n++; if(F.roundHalfEven(x,2)!==r2){bad++; if(bad<25)console.log('round',x,r2,F.roundHalfEven(x,2));}}}
console.log('python checks',n,'bad',bad);
