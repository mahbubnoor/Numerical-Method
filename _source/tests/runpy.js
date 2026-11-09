require('../src/assets/numfmt.js'); require('../src/assets/minipy.js');
const fs=require('fs'); const r=MiniPy.run(fs.readFileSync(process.argv[2],'utf8'), {stdin: process.argv[3]? fs.readFileSync(process.argv[3],'utf8'):''});
process.stdout.write(r.out); if(r.error){ process.stdout.write('\n<<ERR>> '+r.error+'\n'); }
