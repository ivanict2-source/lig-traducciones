// Cloudflare Pages Function: /go/<id>/
import { resolveGo } from '../../edge/go.js';
import data from '../../edge/go-links.generated.js';

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const result = resolveGo(
    {
      id: context.params.id,
      country: context.request.cf && context.request.cf.country,
      src: url.searchParams.get('src'),
    },
    data,
  );
  return new Response(result.body || null, { status: result.status, headers: result.headers });
}
