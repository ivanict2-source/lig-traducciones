---
name: investigacion-seo
description: Prioriza temas y crea briefs SEO (intención de búsqueda, consultas objetivo, estructura, enlaces internos, riesgos) para el sitio de casinos autorizados. Úsala antes de redactar cualquier contenido nuevo o al planificar el calendario editorial.
allowed-tools: WebSearch, Read, Grep, Glob, Write
---

# Investigación SEO y briefs

## Entradas
- Tema candidato y mercado (`CO`, `PE` o `GLOBAL`).
- Datos de Search Console si existen (`data/metrics/gsc/*.csv`).

## Procedimiento
1. Comprueba que no exista ya un contenido con la misma intención (`grep -ri` en `content/`). Si existe, propone actualizarlo en vez de crear otro (evita canibalización y duplicados).
2. Analiza la SERP con WebSearch: tipos de página que aparecen, ángulos cubiertos, huecos (p. ej. falta de fuente oficial, información desactualizada). No copies texto de competidores.
3. NO inventes volúmenes de búsqueda ni dificultad. Si no hay datos de una herramienta, escribe «volumen: sin datos».
4. Prioriza con esta puntuación cualitativa: utilidad para el lector + capacidad de aportar verificación oficial + relación con páginas comerciales legítimas − riesgo regulatorio.
5. Escribe el brief en `content/briefs/<slug>.md` siguiendo `prompts/brief.md` (secciones fijas).

## Salida
- Brief con: intención, consultas objetivo, ángulo diferencial, estructura H2/H3, afirmaciones que requieren fuente, enlaces internos, riesgos de cumplimiento.

## Control de calidad
- Cada afirmación prevista tiene una fuente de `data/sources.yaml` o queda como PENDIENTE.
- El tema aporta valor propio (no es una página «delgada» de afiliación; ver política de Google en sources: google-spam-policies).
