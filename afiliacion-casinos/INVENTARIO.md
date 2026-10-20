# Inventario de entregables

| Entregable | Ubicación | Estado |
|---|---|---|
| Sitio web funcional (código) | `website/` | Construido y probado; no desplegado |
| Redirección de afiliados con control geográfico | `website/functions/go/`, `website/edge/` | Construido y probado (unitario); sin probar en Cloudflare |
| Sistema de contenido | `content/`, `website/src/content.config.ts`, `scripts/validate_content.py` | Construido y probado |
| Contenidos iniciales (5 guías, 9 legales/editoriales) | `content/` | Redactados; PENDIENTE DE REVISIÓN HUMANA |
| Datos de operadores, programas, mercados y fuentes | `data/` | Construidos; verificación humana pendiente |
| Configuraciones de automatización | `automation/n8n/*.json`, `automation/cron/` | Construidas; importadas y ejecutadas en n8n 2.42.2; correo requiere SMTP |
| Skills de Claude Code (9) | `.claude/skills/` | Creadas; formato validado y detectadas por Claude Code |
| Prompts de agentes (8) | `.claude/agents/`, `prompts/` | Creados |
| Scripts auxiliares | `scripts/`, `website/scripts/`, `Makefile` | Construidos y probados |
| Pipeline de IA con control de costes | `scripts/llm.py`, `scripts/pipeline.py`, `config/budget.yaml` | Probado con cliente simulado y dry-run; llamadas reales BLOQUEADAS (sin credenciales) |
| Pruebas automatizadas | `tests/`, `website/tests/` | 29 pytest + 4 Node + accesibilidad: APROBADAS |
| Variables de entorno de ejemplo | `.env.example` | Hecho (sin secretos) |
| Documentación de instalación | `README.md`, `docs/11-*.md` | Hecho; instalación limpia verificada |
| Documentación de seguridad | `docs/08-seguridad-privacidad.md`, `.claude/settings.json`, `website/public/_headers` | Hecho |
| Presupuesto desglosado | `docs/09-presupuesto.md`, `config/budget.yaml` | Hecho (precios confirmados vs. estimados) |
| Informe de investigación | `docs/00-03`, `data/sources.yaml` | Hecho; fuentes leídas como fragmentos de búsqueda |
| PDF final | `reports/informe-proyecto.pdf` (+ `reports/informe-proyecto.md`) | Generado y verificado (`scripts/build_pdf.py`) |
| Panel editorial | `reports/estado-editorial.md` | Generado |
| Lista de tareas pendientes y bloqueos | `ESTADO.md`, `docs/13-pendientes-riesgos-checklist.md` | Hecho |
| Plantilla MCP | `.mcp.json.example` | Plantilla sin probar (ningún MCP instalado) |
