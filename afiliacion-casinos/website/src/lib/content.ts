import { getCollection, type CollectionEntry } from 'astro:content';
import { isPreview, publicMarkets, type MarketCode } from './data';

export type Entry = CollectionEntry<'guias'> | CollectionEntry<'legal'>;

/**
 * Regla de publicación:
 * - producción: solo `published` con `approved_by` y `approved_date` (aprobación humana).
 * - preview: todo lo que tenga borrador (draft, review, approved, published), con aviso visible.
 */
export function isPublishable(e: Entry): boolean {
  const d = e.data;
  if (isPreview) return ['draft', 'review', 'approved', 'published'].includes(d.status);
  const marketOk = d.market === 'GLOBAL' || publicMarkets.includes(d.market as MarketCode);
  return marketOk && d.status === 'published' && !!d.approved_by && !!d.approved_date;
}

export async function publishedEntries(): Promise<Entry[]> {
  const all = [...(await getCollection('guias')), ...(await getCollection('legal'))];
  return all.filter(isPublishable);
}

/** Equivalentes en otros mercados/idiomas (hreflang). */
export async function alternatesFor(e: Entry): Promise<{ lang: string; href: string }[]> {
  if (!e.data.translation_key) return [];
  const all = await publishedEntries();
  return all
    .filter((x) => x.data.translation_key === e.data.translation_key)
    .map((x) => ({ lang: x.data.lang, href: x.data.permalink }));
}
