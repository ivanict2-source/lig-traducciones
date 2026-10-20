import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';

// Los datos estructurados (operadores, fuentes, mercados, configuración) viven en
// ../data y ../config. Se leen en tiempo de build: la web publicada es 100 % estática.
const root = path.resolve(process.cwd(), '..');

function load<T>(rel: string): T {
  return yaml.load(fs.readFileSync(path.join(root, rel), 'utf8')) as T;
}

export type MarketCode = 'CO' | 'PE';

export interface Verification {
  status: 'verificado-humano' | 'fuente-oficial-indirecta' | 'prensa';
  source_ids: string[];
  checked: string | Date;
  checked_by: string;
}

export interface Operator {
  id: string;
  name: string;
  market: MarketCode;
  regulator: string;
  license_ref: string | null;
  legal_entity: string | null;
  official_url: string | null;
  affiliate: { program_id: string | null; url: string | null; status: string };
  verification: Verification;
  notes?: string;
}

export interface Source {
  id: string;
  title: string;
  url: string;
  type: string;
  reliability: string;
  market: string;
  accessed: string | Date;
  access: string;
  claims: string[];
}

export interface Market {
  code: string;
  country: string;
  language: string;
  regulatory_status: string;
  official_sources: string[];
  regulator_registry: string | null;
  competition: string;
  seo_opportunity: string;
  entry_difficulty: string;
  authorized_operators: string;
  monetization: string;
  legal_risk: string;
  affiliate_obligations: string;
  priority: number | string;
  notes?: string;
}

export interface SiteConfig {
  brand: string;
  tagline: string;
  contact_email: string;
  min_age: number;
  active_markets: MarketCode[];
  blocked_affiliate_countries: string[];
  locales: Record<MarketCode, string>;
  market_notices: Record<MarketCode, string>;
}

export const isPreview = import.meta.env.PUBLIC_BUILD_MODE === 'preview';

export const site = load<SiteConfig>('config/site.yaml');
export const sources = load<Source[]>('data/sources.yaml');
export const markets = load<{ markets: Market[] }>('data/markets.yaml').markets;
const allOperators = load<{ operators: Operator[] }>('data/operators.yaml').operators;

/**
 * Mercados publicables: en producción se excluye cualquier mercado cuyo aviso
 * legal obligatorio siga incompleto (contiene PENDIENTE).
 */
export const publicMarkets: MarketCode[] = site.active_markets.filter(
  (m) => isPreview || !site.market_notices[m].includes('PENDIENTE'),
);

export const sourceById = new Map(sources.map((s) => [s.id, s]));

/** En producción solo se muestran operadores verificados por una persona. */
export function operatorsFor(market: MarketCode): Operator[] {
  return allOperators
    .filter((o) => o.market === market)
    .filter((o) => isPreview || o.verification.status === 'verificado-humano')
    .sort((a, b) => a.name.localeCompare(b.name, 'es'));
}

export const marketNames: Record<MarketCode, string> = { CO: 'Colombia', PE: 'Perú' };

export function fmtDate(d: string | Date | null | undefined): string {
  if (!d) return '—';
  const date = typeof d === 'string' ? new Date(d) : d;
  return date.toISOString().slice(0, 10);
}
