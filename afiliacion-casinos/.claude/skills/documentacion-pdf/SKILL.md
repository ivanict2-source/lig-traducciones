---
name: documentacion-pdf
description: Regenera la documentación del proyecto (docs/*.md) y el informe PDF profesional en reports/ con ReportLab, y verifica que el PDF existe y se abre. Úsala tras cambios relevantes en investigación, arquitectura, presupuesto o estado del proyecto.
allowed-tools: Read, Edit, Write, Glob, Bash(python scripts/build_pdf.py*), Bash(make pdf*)
---

# Documentación y PDF

1. Actualiza los Markdown de `docs/` (son la fuente del PDF; el orden lo fija `scripts/build_pdf.py`).
2. Actualiza `ESTADO.md` e `INVENTARIO.md` si cambió el estado de algún entregable.
3. `make pdf` → genera `reports/informe-proyecto.pdf` y comprueba número de páginas y que el archivo se puede leer.
4. No incluyas credenciales ni datos personales en el PDF.
5. Distingue siempre: investigado / construido / probado / preparado sin desplegar / requiere credenciales / requiere aprobación humana / no verificado.
