// Auditoría de accesibilidad con axe-core sobre la web compilada.
// Uso: node tests/a11y.mjs dist-preview
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { chromium } from 'playwright-core';

const require = createRequire(import.meta.url);
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const dist = path.resolve(process.argv[2] || 'dist-preview');
const exe = process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

function pages(dir, base = '') {
  return fs.readdirSync(path.join(dir, base), { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? pages(dir, path.join(base, e.name)) : e.name === 'index.html' ? ['/' + (base ? base + '/' : '')] : [],
  );
}

const server = http.createServer((req, res) => {
  let p = path.join(dist, decodeURIComponent(req.url.split('?')[0]));
  if (p.endsWith('/')) p = path.join(p, 'index.html');
  fs.readFile(p, (err, buf) => {
    if (err) { res.writeHead(404); return res.end('404'); }
    const type = p.endsWith('.css') ? 'text/css' : p.endsWith('.svg') ? 'image/svg+xml' : 'text/html; charset=utf-8';
    res.writeHead(200, { 'Content-Type': type });
    res.end(buf);
  });
});
await new Promise((r) => server.listen(0, r));
const port = server.address().port;
const browser = await chromium.launch({ executablePath: exe });
let serious = 0;
const report = [];
for (const scheme of ['light', 'dark']) {
  const page = await browser.newPage({ colorScheme: scheme });
  for (const url of pages(dist)) {
    await page.goto(`http://127.0.0.1:${port}${url}`);
    await page.addScriptTag({ content: axeSource });
    const res = await page.evaluate(async () => await window.axe.run(document, { resultTypes: ['violations'] }));
    for (const v of res.violations) {
      const bad = ['serious', 'critical'].includes(v.impact);
      if (bad) serious++;
      report.push(`${bad ? 'ERROR' : 'AVISO'} [${scheme}] ${url}: ${v.id} (${v.impact}) x${v.nodes.length} — ${v.help}`);
    }
  }
  await page.close();
}
await browser.close();
server.close();
console.log(report.join('\n') || 'Sin incidencias de accesibilidad.');
console.log(`Páginas auditadas: ${pages(dist).length} x 2 esquemas · incidencias graves: ${serious}`);
process.exit(serious ? 1 : 0);
