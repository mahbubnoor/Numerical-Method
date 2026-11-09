require('../src/assets/numfmt.js'); const F=globalThis.NumFmt; const fs=require('fs');
const vals=fs.readFileSync('vals.txt','utf8').trim().split('\n').map(Number); const exp=fs.readFileSync('c_out.txt','utf8').split('\n');
const f=["%f","%.3f","%.0f","%e","%.2e","%g","%.3g","%.10g","%10.4f","%-12.3f|","%+.2f","%012.4f","%G","%#.3g"];
let k=0,bad=0; for(const x of vals){ for(const s of f){ const g=F.cFormat(s,[{v:x,t:'double'}]); if(g!==exp[k]){bad++; if(bad<10)console.log(s,x,exp[k],g);} k++; } }
console.log('C checks',k,'bad',bad);
