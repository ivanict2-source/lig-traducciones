---
name: control-costes
description: Estima, limita y registra el coste de IA y de infraestructura del proyecto; revisa el ledger, propone el modelo más económico por tarea y detiene tareas que superan el presupuesto. Úsala antes de lanzar tareas de generación en lote y en el informe mensual.
allowed-tools: Read, Grep, Bash(python scripts/pipeline.py --dry-run*), Bash(python scripts/editorial_status.py*), Bash(python scripts/analytics_report.py*), Edit
---

# Control de costes

## Fuentes de verdad
- Precios y topes: `config/budget.yaml` (routing por tarea, `limits.monthly_usd`, `limits.per_task_usd`, `max_iterations`).
- Consumo real: `reports/costes/ledger.csv` (lo escribe `scripts/llm.py` con los tokens reportados por la API).

## Procedimiento
1. Antes de un lote: `python scripts/pipeline.py --dry-run <subcomando> ...` para cada tarea y suma los costes máximos.
2. Si el total supera el saldo mensual restante, reduce el lote o pide autorización.
3. Preferencias: (a) hacer el trabajo en Claude Code con skills (sin coste marginal de API), (b) Haiku para metadatos/clasificación, (c) Sonnet para borradores y traducciones, (d) Opus solo para verificación/cumplimiento o tras dos fallos de validación.
4. Reutiliza: la caché `.cache/llm` evita repetir peticiones idénticas; no regeneres contenido que no ha cambiado.
5. Informe mensual: total por modelo y tarea, coste por contenido publicado (`scripts/analytics_report.py`).

## Prohibido
- Subir `limits.monthly_usd` sin autorización del propietario.
- Activar planes de pago de cualquier servicio.
