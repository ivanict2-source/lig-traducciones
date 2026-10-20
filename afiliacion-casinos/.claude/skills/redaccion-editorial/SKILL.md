---
name: redaccion-editorial
description: Redacta borradores originales en español (es-CO / es-PE) a partir de un brief, siguiendo el manual de estilo y las reglas de cumplimiento, y los guarda en content/ con estado draft. Úsala cuando haya un brief aprobado para redactar.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(python scripts/validate_content.py*)
---

# Redacción editorial

## Entradas
- `content/briefs/<slug>.md`
- Manual: `prompts/sistema-editorial.md` (léelo completo antes de escribir).

## Procedimiento
1. Lee el brief y las fuentes citadas en `data/sources.yaml` (solo puedes afirmar lo que dicen sus `claims`).
2. Redacta el cuerpo en Markdown, sin H1, con subtítulos `##`, pasos concretos y citas `[id-fuente]` en las afirmaciones sensibles cuando sea un borrador interno. En la versión final las fuentes se muestran automáticamente al pie: elimina los corchetes si molestan a la lectura.
3. Lo que no esté respaldado → `[PENDIENTE: qué falta y dónde verificarlo]`.
4. Crea el archivo `content/guias/<mercado>-<slug>.md` con el frontmatter completo (ver un archivo existente como plantilla): `status: draft`, `sensitive: true` si trata licencias, legalidad, pagos o impuestos, `approved_by: null`.
5. Ejecuta `python scripts/validate_content.py` y corrige errores.

## Prohibido
- Testimonios, experiencias de juego, bonos, cifras de pago, «mejor casino» sin metodología, promesas de ganancia.
- Cambiar `status` a `approved` o `published`.

## Control de calidad
- Separación de hechos verificados / información del operador / valoración editorial.
- Mención a juego responsable y +18 cuando el texto conduzca a operadores.
- Longitud mínima orientativa: 300 palabras (guías), sin relleno.
