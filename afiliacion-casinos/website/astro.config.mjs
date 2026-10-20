// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const site = process.env.SITE_URL || 'https://juegoverificado.example';
const preview = process.env.PUBLIC_BUILD_MODE === 'preview';

export default defineConfig({
  site,
  trailingSlash: 'always',
  build: { format: 'directory' },
  // En modo preview no se genera sitemap: el sitio de revisión no debe indexarse.
  integrations: preview
    ? []
    : [sitemap({ filter: (page) => !page.includes('/go/') })],
});
