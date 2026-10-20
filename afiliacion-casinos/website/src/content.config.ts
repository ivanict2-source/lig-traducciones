import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// El contenido vive fuera de la web (../content) para que el pipeline editorial,
// los scripts y Git trabajen sobre Markdown plano. El esquema refleja el flujo:
// planned -> research -> draft -> review -> approved -> published.
const editorial = z.object({
  title: z.string().min(10).max(70),
  description: z.string().min(50).max(160),
  permalink: z.string().regex(/^\/([a-z0-9-]+\/)*$/),
  type: z.enum(['guia', 'comparativa', 'resena', 'noticia', 'legal', 'editorial']),
  market: z.enum(['CO', 'PE', 'GLOBAL']),
  lang: z.enum(['es-CO', 'es-PE', 'es', 'en']),
  translation_key: z.string().optional(),
  status: z.enum(['planned', 'research', 'draft', 'review', 'approved', 'published']),
  sensitive: z.boolean(),
  approved_by: z.string().nullable().default(null),
  approved_date: z.coerce.date().nullable().default(null),
  last_verified: z.coerce.date(),
  sources: z.array(z.string()).default([]),
  author: z.string(),
  cost_usd: z.number().min(0).default(0),
  updated: z.coerce.date(),
});

export const collections = {
  guias: defineCollection({
    loader: glob({ pattern: '**/*.md', base: '../content/guias' }),
    schema: editorial,
  }),
  legal: defineCollection({
    loader: glob({ pattern: '**/*.md', base: '../content/legal' }),
    schema: editorial,
  }),
};
