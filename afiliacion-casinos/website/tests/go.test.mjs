// Pruebas de la lógica de redirección de afiliados (node --test).
import test from 'node:test';
import assert from 'node:assert/strict';
import { resolveGo, sanitizeSubid } from '../edge/go.js';

const data = {
  blocked_countries: ['CL', 'DO'],
  links: { 'wplay-co': { url: 'https://aff.example/?sub={subid}', allowed_countries: ['CO'] } },
};

test('redirige desde el país autorizado y añade sub-ID saneado', () => {
  const r = resolveGo({ id: 'wplay-co', country: 'CO', src: 'co-Wplay<script>' }, data);
  assert.equal(r.status, 302);
  assert.equal(r.headers.Location, 'https://aff.example/?sub=co-wplayscript');
  assert.equal(r.headers['Cache-Control'], 'no-store');
  assert.match(r.headers['X-Robots-Tag'], /noindex/);
});

test('bloquea países fuera del mercado autorizado', () => {
  assert.equal(resolveGo({ id: 'wplay-co', country: 'PE' }, data).status, 451);
  assert.equal(resolveGo({ id: 'wplay-co', country: 'CL' }, data).status, 451);
  assert.equal(resolveGo({ id: 'wplay-co', country: undefined }, data).status, 451);
});

test('enlace desconocido devuelve 404 sin redirección', () => {
  const r = resolveGo({ id: 'nope', country: 'CO' }, data);
  assert.equal(r.status, 404);
  assert.equal(r.headers.Location, undefined);
});

test('sanitizeSubid', () => {
  assert.equal(sanitizeSubid('../../etc'), 'etc');
  assert.equal(sanitizeSubid(null), '');
});
