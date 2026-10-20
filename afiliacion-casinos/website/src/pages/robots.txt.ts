import type { APIRoute } from 'astro';

export const GET: APIRoute = ({ site }) => {
  const preview = import.meta.env.PUBLIC_BUILD_MODE === 'preview';
  const body = preview
    ? 'User-agent: *\nDisallow: /\n'
    : `User-agent: *\nDisallow: /go/\nAllow: /\n\nSitemap: ${new URL('sitemap-index.xml', site).href}\n`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
