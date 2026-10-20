# 19. Automatizaciones

## 19.1 Qué se automatiza y cómo

| # | Proceso | Implementación | Estado |
|---|---|---|---|
| 1 | Descubrimiento de temas | Skill `investigacion-seo` + exportaciones de Search Console | Preparado (manual asistido) |
| 2 | Investigación de fuentes | Skill/agente `investigador` → `data/sources.yaml` | Construido |
| 3 | Briefs | `scripts/pipeline.py brief` o skill `investigacion-seo` | Construido (API no probada en real) |
| 4 | Borradores | `pipeline.py draft` (valida, reintenta, escala de modelo) o skill `redaccion-editorial` | Construido (API no probada en real) |
| 5 | Traducción/adaptación | `pipeline.py translate` o skill `traduccion-adaptacion` | Construido (API no probada en real) |
| 6 | Validación técnica | `scripts/validate_content.py`, `astro build` (esquema zod) | Construido y probado |
| 7 | Comprobación de enlaces | `scripts/check_site.py` (internos; externos con `--external`) | Internos probados; externos bloqueados por la red |
| 8 | Contenido caducado | `scripts/editorial_status.py --days 30` | Construido y probado |
| 9 | Informes | `editorial_status.py`, `analytics_report.py` | Construido y probado |
| 10 | Preparación de publicaciones | Skill `publicacion` + `make test` | Construido |
| 11 | Copias de seguridad | `scripts/backup.py` (rotación + SHA-256 + restauración) | Construido y probado |
| 12 | Notificación de errores | n8n (correo SMTP) o salida de cron | Preparado; requiere SMTP |
| 13 | Análisis de costes | `scripts/llm.py` (ledger) + skill `control-costes` | Construido y probado |
| 14 | Conversiones | `analytics_report.py` con CSV de los programas | Construido y probado con datos de prueba |

## 19.2 Programación recomendada: cron

`automation/cron/crontab.example`: copia diaria 02:30, mantenimiento los lunes 07:00 e informe el día 1 a las 08:00. En Windows, el Programador de tareas (preferiblemente con WSL).

## 19.3 Opción n8n (community, autoalojado)

Flujos exportados en `automation/n8n/`:

| Flujo | Nodos | Función |
|---|---|---|
| `mantenimiento-semanal.json` | Schedule → Execute Command (`make maintenance`) → IF exitCode≠0 → Email (error) / Email (resumen) | Validación, build, enlaces/SEO, caducidad |
| `copia-seguridad-diaria.json` | Schedule → Execute Command (`make backup`) → IF → Email | Copia con aviso solo si falla |
| `informe-mensual.json` | Schedule → Execute Command (`make report`) → Email | Panel editorial + rendimiento |
| `borrador-bajo-demanda.json` | Manual → Set (tema, mercado, dry_run) → Execute Command (`pipeline.py`) → IF → Email | Brief por API; *dry-run* por defecto |

**Importación:** n8n → *Workflows* → *Import from file* (o `n8n import:workflow --input=<archivo>`). Tras importar: asignar la credencial SMTP a los nodos de correo, cambiar el destinatario `CONFIGURAR-DESTINATARIO@example.com`, definir la variable de entorno `PROJECT_DIR` en el proceso de n8n, probar con el disparador «Probar ahora» y activar el flujo.

**Prueba real realizada:** los 4 flujos se importaron y ejecutaron en n8n 2.42.2 (ver `reports/pruebas/n8n-ejecucion-2026-10-20.md`). La prueba destapó y permitió corregir tres defectos: faltaba el `id` de flujo, n8n 2.x bloquea `$env` en expresiones (se usa la variable de shell `$PROJECT_DIR`) y los flujos programados no tenían disparador manual.

**Requisitos y seguridad:**
- `automation/n8n/docker-compose.yml` publica n8n **solo en 127.0.0.1**. No se expone a Internet; si algún día se necesitara acceso remoto, hacerlo mediante un túnel autenticado y con aprobación expresa.
- n8n 2.x **desactiva por defecto** los nodos Execute Command y Local File Trigger por motivos de seguridad. El compose habilita únicamente Execute Command (`NODES_EXCLUDE=["n8n-nodes-base.localFileTrigger"]`). Esto permite a n8n ejecutar comandos del sistema: por eso n8n debe quedarse en localhost y con usuario propietario protegido por contraseña.
- La imagen oficial de n8n no incluye Python ni `make`; para ejecutar los scripts dentro del contenedor hay que crear una imagen derivada o ejecutar n8n directamente en el host (`npx n8n@2.42.2`, que exige Node.js 24 o superior). Por eso cron es la opción recomendada.
- n8n 2.x bloquea por defecto el acceso a `$env` desde las expresiones; los flujos no lo usan.
- No hay credenciales en los JSON exportados (comprobado por prueba automatizada).
