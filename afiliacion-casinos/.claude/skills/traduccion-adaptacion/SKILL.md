---
name: traduccion-adaptacion
description: Adapta un contenido existente a otro mercado o idioma (es-CO, es-PE, más adelante en) con terminología consistente y sin trasladar literalmente el contenido regulatorio. Úsala para crear la versión de un artículo para otro país.
allowed-tools: Read, Grep, Glob, Write, Bash(python scripts/validate_content.py*)
---

# Traducción y adaptación por mercado

## Reglas
1. Adaptación, no traducción literal: moneda, regulador, terminología local («apuestas deportivas», «casa de apuestas», «tragamonedas» / «tragaperras» según país).
2. El contenido regulatorio NUNCA se traslada: cada norma, autoridad, plazo o impuesto del mercado de origen se sustituye por el equivalente del destino con fuente oficial, o por `[PENDIENTE: ...]`.
3. Mantén el mismo `translation_key` que el original para que la web genere `hreflang` recíproco.
4. Nuevo archivo con `status: draft`, `permalink` del mercado destino y `lang` correcto.
5. Valida con `python scripts/validate_content.py` (detecta duplicados: si la similitud es alta, el texto no está suficientemente adaptado).

## Glosario mínimo
| Concepto | es-CO | es-PE |
|---|---|---|
| Regulador | Coljuegos | MINCETUR (DGJCMT) |
| Título habilitante | contrato de concesión | autorización / resolución |
| Moneda | COP | PEN (soles) |

## Salida
Archivo nuevo en `content/guias/` + lista de PENDIENTES regulatorios para el agente investigador.
