# 20. Configuración del sitio

## 20.1 Páginas

| Tipo | Ruta | Origen | Producción |
|---|---|---|---|
| Portada | `/` | `src/pages/index.astro` | Sí |
| Mercado | `/co/`, `/pe/` | `[market]/index.astro` + `data/markets.yaml` | Solo mercados con aviso legal completo (hoy: Colombia) |
| Comparativa de licencias | `/co/operadores/` | `[market]/operadores/index.astro` | Sí (vacía hasta verificar operadores) |
| Ficha de operador | `/co/operadores/<id>/` | `[market]/operadores/[id].astro` + `data/operators.yaml` | Solo `verificado-humano` |
| Guías y noticias | `/co/guias/...`, `/pe/guias/...`, `/guias/...` | `content/guias/*.md` | Solo `published` con aprobación humana |
| Legales y editoriales | `/aviso-de-afiliacion/`, `/privacidad/`, `/cookies/`, `/condiciones-de-uso/`, `/juego-responsable/` (incluye edad mínima), `/metodologia/`, `/correcciones/`, `/sobre-nosotros/`, `/contacto/` | `content/legal/*.md` | Tras aprobación |
| Licencias y mercados | `/mercados/` | `data/markets.yaml` | Sí |
| Fuentes | `/fuentes/` | `data/sources.yaml` | Sí |
| Redirección de afiliados | `/go/<id>/` | `functions/go/[id].js` | Solo enlaces con contrato y verificación |

Elementos en todas las páginas: franja +18 y aviso de riesgo, aviso de afiliación en el pie, enlace a juego responsable, leyenda obligatoria del mercado (Colombia: «Autorizado por COLJUEGOS…»; Perú: advertencia de ludopatía, pendiente del texto literal), fecha de verificación y fuentes en cada guía y ficha.

## 20.2 Reglas de presentación de operadores

- Fichas con tres bloques separados: **hechos verificados** (regulador, contrato/resolución, titular, dominio), **información del operador** (vacía hasta recopilarla, identificada como tal) y **valoración editorial** (vacía: no hay reseñas sin revisión documentada).
- Orden alfabético; sin bonos; sin puntuaciones.
- Enlace comercial solo si hay contrato (`/go/`, `rel="sponsored nofollow"`); sin contrato, enlace al dominio oficial (`rel="nofollow"`); sin dominio verificado, sin enlace.

## 20.3 Configuración técnica

- `config/site.yaml`: marca, mercados activos, países bloqueados para afiliación (CL, DO), leyendas por mercado.
- `SITE_URL`, `PUBLIC_CF_BEACON_TOKEN`, `PUBLIC_BUILD_MODE` (preview) por variables de entorno.
- `public/_headers`: CSP estricta, HSTS, `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy`, `Permissions-Policy`.
- `robots.txt` dinámico: la vista previa bloquea todo; producción bloquea `/go/` y publica el sitemap.
- Sitemap con `@astrojs/sitemap` (excluye `/go/`); no se genera en la vista previa.

# 21. Proceso editorial

```
planned → research → draft → review → approved → published
           (IA)       (IA)    (IA →     (PERSONA)   (PERSONA)
                              cola humana)
```

1. **Planificación:** el estratega SEO crea el brief (intención, consultas, ángulo, estructura, afirmaciones que requieren fuente).
2. **Investigación:** el investigador añade fuentes a `data/sources.yaml`.
3. **Borrador:** el redactor escribe (`status: draft`); lo no respaldado queda como `[PENDIENTE]`.
4. **Verificación y cumplimiento:** informes en `reports/revisiones/`. Si son aptos, el supervisor pasa el contenido a `review`.
5. **Revisión humana:** la persona abre cada fuente, resuelve los PENDIENTE y ejecuta `scripts/approve.py approve <archivo> --by "Nombre"` (exige escribir APRUEBO; rechaza aprobadores con nombre de agente y textos con PENDIENTE).
6. **Publicación:** `scripts/approve.py publish <archivo>` y despliegue autorizado.
7. **Actualización:** `editorial_status.py` marca como caducado lo verificado hace más de 30 días; la revalidación actualiza `last_verified`.
8. **Correcciones:** registro público en `/correcciones/`.

Campos de control por contenido: `status`, `sensitive`, `approved_by`, `approved_date`, `last_verified`, `sources`, `author`, `cost_usd`, `updated`, `translation_key`.

**Traducción:** adaptación por mercado, nunca traslado literal de normas; `translation_key` común para generar `hreflang` recíproco (comprobado por `check_site.py`).

# 22. Estrategia SEO

1. **Arquitectura:** un dominio, subcarpetas por país, enlazado interno portada → mercado → comparativa → fichas, y guías ↔ comparativa.
2. **Intención:** empezar por consultas informativas de verificación («cómo saber si un casino es legal en Perú», «Coljuegos lista de operadores», «¿está autorizado X?»), donde el contenido original con fuente oficial compite mejor que las listas comerciales; después, consultas comerciales («casinos legales Colombia»), apoyadas en la comparativa de licencias.
3. **Señales de calidad (E-E-A-T):** metodología pública, fuentes visibles, fechas de verificación, correcciones, autoría y revisión humana registradas.
4. **Contenido programático con valor:** las fichas por operador se generan desde datos, pero cada una aporta datos verificados propios (contrato, titular, fecha); no se crean páginas por plantilla sin datos (p. ej. «casino X en ciudad Y»).
5. **Técnico:** HTML estático rápido, un H1, títulos ≤ 70 caracteres, descripciones de 50-160, canonical, `hreflang`, sitemap, `noindex` en la vista previa y en `/go/`. Todo comprobado por `check_site.py`.
6. **Medición:** Search Console (impresiones, clics, CTR, posición por página) exportado a `data/metrics/gsc/`.
7. **Riesgos:** cambios de algoritmo y políticas de spam; mitigación: pocas páginas de alta utilidad, sin compra de enlaces ni dominios caducados, y diversificación futura (boletín por correo cuando haya audiencia).

# 23. Medición de conversiones

| Métrica | Fuente | Dónde |
|---|---|---|
| Visitas | Cloudflare Web Analytics (sin cookies) | Panel de Cloudflare |
| Impresiones, clics, CTR, posición | Google Search Console | `data/metrics/gsc/*.csv` → `analytics_report.py` |
| Clics de afiliación | Informes de cada programa (por sub-ID) | `data/metrics/affiliate/*.csv` |
| Registros, primeros depósitos, comisiones | Informes de cada programa | Ídem; solo `status=confirmed` cuenta como ingreso |
| Coste de herramientas e IA | `config/budget.yaml`, `reports/costes/ledger.csv` | `analytics_report.py`, `editorial_status.py` |
| Ingresos por página, mercado e idioma | Sub-ID `<mercado>-<operador>` (`/go/<id>/?src=`) | `analytics_report.py` |

Principios: un clic **no** es una conversión; solo se atribuyen ingresos reportados por el programa; no se instalan cookies propias ni píxeles de seguimiento; los datos se agregan por sub-ID, no por persona. Formato normalizado de los CSV en `scripts/analytics_report.py`.
