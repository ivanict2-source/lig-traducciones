---
name: investigacion-mercado
description: Investiga la regulación, el registro oficial de operadores y los programas de afiliación de un mercado de juego online, y registra cada afirmación con su fuente en data/sources.yaml. Úsala al evaluar un país nuevo, al revisar cambios normativos o al actualizar operators.yaml / programs.yaml / markets.yaml.
allowed-tools: WebSearch, WebFetch, Read, Grep, Glob, Edit, Write
---

# Investigación de mercado y regulación

## Entradas
- Código de mercado (p. ej. `CO`, `PE`, `MX`) y pregunta concreta (regulador, registro, publicidad, afiliados, impuestos).
- Estado actual: `data/markets.yaml`, `data/operators.yaml`, `data/programs.yaml`, `data/sources.yaml`.

## Procedimiento
1. Lee la fila del mercado en `data/markets.yaml` y las fuentes ya registradas para no repetir búsquedas (reutiliza investigación).
2. Busca primero fuentes oficiales: regulador, boletín/diario oficial, ministerio. Usa `allowed_domains` con el dominio del regulador cuando sea posible.
3. Después, despachos de abogados y prensa especializada solo para contexto; márcalas `reliability: media|baja`.
4. Para cada afirmación nueva añade (o amplía) una entrada en `data/sources.yaml` con `id`, `title`, `url`, `type`, `reliability`, `market`, `accessed` (fecha de hoy), `access` (`full` si leíste la página entera, `snippet` si solo viste el resultado del buscador) y `claims`.
5. Si dos fuentes se contradicen, registra ambas y anota la contradicción en `claims`; prioriza la oficial.
6. Actualiza `markets.yaml` / `operators.yaml` / `programs.yaml`. Los operadores nuevos entran SIEMPRE con `verification.status: fuente-oficial-indirecta` o `prensa`, nunca `verificado-humano`.
7. Ejecuta `python scripts/validate_content.py` y corrige errores.

## Prohibido
- Inventar URLs, números de licencia, comisiones, porcentajes o dominios. Si no está en una fuente: `null` y nota de pendiente.
- Suponer que un programa acepta afiliados residentes en República Dominicana.
- Recomendar dirigir tráfico a mercados sin régimen de licencias o eludir geobloqueos.

## Salida
- Diff en los YAML + resumen en el chat: hallazgos, contradicciones, qué falta y qué debe verificar una persona.

## Control de calidad
- Cada `claims` es una frase verificable, con fecha y fuente.
- Ninguna afirmación sensible depende solo de una fuente de fiabilidad baja.
