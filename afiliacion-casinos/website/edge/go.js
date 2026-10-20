// Lógica pura de redirección de enlaces de afiliado (/go/<id>/).
// Se mantiene separada de la Pages Function para poder probarla con Node.
//
// Reglas:
//  1. Solo existen los enlaces generados desde data/operators.yaml con acuerdo
//     de afiliación y verificación humana (scripts/build_go_links.py).
//  2. Solo se redirige si el país del visitante (cabecera CF) está en
//     allowed_countries del enlace y no está en la lista de bloqueo global.
//  3. Nunca se cachea ni se indexa la redirección.

const BASE_HEADERS = {
  'Cache-Control': 'no-store',
  'X-Robots-Tag': 'noindex, nofollow',
};

function page(status, title, text) {
  const html = `<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>${title}</title></head><body style="font-family:system-ui;max-width:40rem;margin:2rem auto;padding:0 16px"><h1>${title}</h1><p>${text}</p><p><a href="/">Volver a la portada</a></p></body></html>`;
  return { status, headers: { ...BASE_HEADERS, 'Content-Type': 'text/html; charset=utf-8' }, body: html };
}

export function sanitizeSubid(value) {
  return String(value || '').toLowerCase().replace(/[^a-z0-9-]/g, '').slice(0, 60);
}

export function resolveGo({ id, country, src }, data) {
  const link = data.links[id];
  if (!link) return page(404, 'Enlace no disponible', 'Este enlace no existe o ha sido retirado.');
  const c = (country || 'XX').toUpperCase();
  if (data.blocked_countries.includes(c) || !link.allowed_countries.includes(c)) {
    return page(
      451,
      'No disponible en tu país',
      'Este operador solo está autorizado en otro mercado. No redirigimos tráfico a operadores fuera del país donde tienen licencia.',
    );
  }
  const target = link.url.replace('{subid}', encodeURIComponent(sanitizeSubid(src) || 'web'));
  return { status: 302, headers: { ...BASE_HEADERS, Location: target }, body: '' };
}
