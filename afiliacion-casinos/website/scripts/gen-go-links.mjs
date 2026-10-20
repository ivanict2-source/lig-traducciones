// Genera edge/go-links.generated.js a partir de ../data/operators.yaml y ../config/site.yaml.
// Solo entran operadores con enlace de afiliado firmado Y verificación humana.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import yaml from 'js-yaml';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..', '..');
const ops = yaml.load(fs.readFileSync(path.join(root, 'data/operators.yaml'), 'utf8')).operators;
const site = yaml.load(fs.readFileSync(path.join(root, 'config/site.yaml'), 'utf8'));

const links = {};
for (const op of ops) {
  if (!op.affiliate?.url || op.verification?.status !== 'verificado-humano') continue;
  if (!/^https:\/\//.test(op.affiliate.url)) throw new Error(`URL de afiliado no HTTPS: ${op.id}`);
  links[op.id] = { url: op.affiliate.url, allowed_countries: [op.market] };
}
const data = { blocked_countries: site.blocked_affiliate_countries, links };
const out = path.join(here, '..', 'edge', 'go-links.generated.js');
fs.writeFileSync(out, `// Generado por scripts/gen-go-links.mjs. No editar.\nexport default ${JSON.stringify(data, null, 2)};\n`);
console.log(`go-links: ${Object.keys(links).length} enlaces activos`);
