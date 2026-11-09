require('../src/assets/numfmt.js'); require('../src/assets/minipy.js'); require('../src/assets/minic.js');
let buf = ''; process.stdin.on('data', d => buf += d).on('end', () => {
  const out = {};
  for (const j of JSON.parse(buf)) { const r = j.lang === 'py' ? MiniPy.run(j.src, { stdin: j.stdin }) : MiniC.run(j.src, { stdin: j.stdin }); out[j.k] = { out: r.out, error: r.error, warnings: r.warnings || [] }; }
  process.stdout.write(JSON.stringify(out));
});
