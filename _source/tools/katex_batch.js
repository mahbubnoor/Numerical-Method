const katex = require('katex'); let buf = '';
process.stdin.on('data', d => buf += d).on('end', () => {
  const items = JSON.parse(buf);
  const out = items.map(([tex, disp]) => { try { return katex.renderToString(tex, { displayMode: disp, throwOnError: true, strict: 'ignore' }); } catch (e) { return '<span class="katex-error">' + e.message + '</span>'; } });
  process.stdout.write(JSON.stringify(out));
});
