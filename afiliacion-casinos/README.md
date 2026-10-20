# Juego Verificado — afiliación de casinos online autorizados, operada con IA

Sitio editorial en español que informa qué operadores de juego online están **autorizados** en Colombia (Coljuegos) y Perú (MINCETUR), con fuente oficial y fecha de verificación, monetizado con afiliación solo a operadores verificados. Incluye el sistema de contenido, automatizaciones, skills y agentes de Claude Code, pruebas y el informe completo.

> Este proyecto vive en la subcarpeta `afiliacion-casinos/` del repositorio y no modifica el sitio existente de la raíz.

**Informe completo:** [`reports/informe-proyecto.pdf`](reports/informe-proyecto.pdf) (versión editable: `reports/informe-proyecto.md`; fuentes en `docs/`).

## Inicio rápido

```bash
cd afiliacion-casinos
make setup     # .venv + dependencias fijadas (pip, npm ci)
make test      # validación, builds, enlaces/SEO, pytest, Node, accesibilidad
make preview   # vista previa interna (noindex) en http://127.0.0.1:4321
make help      # todas las tareas
```

Requisitos: Python 3.11+, Node.js 22+, make. Opcional: Docker (n8n), Chromium (accesibilidad).

## Cómo se trabaja

1. Abrir **Claude Code** en esta carpeta: carga `CLAUDE.md`, 9 skills y 8 subagentes.
2. Pedir, por ejemplo: «Usa el agente supervisor para preparar una guía sobre X en Perú».
3. Los agentes dejan el contenido en `review`. **Una persona** revisa y aprueba con `scripts/approve.py` (los agentes lo tienen prohibido).
4. `make test` y, con autorización del propietario, `make deploy`.

## Estructura

| Carpeta | Contenido |
|---|---|
| `website/` | Web Astro, Pages Function `/go/` con control geográfico, pruebas Node y de accesibilidad |
| `content/` | Guías, páginas legales y briefs en Markdown con frontmatter |
| `data/` | Operadores, programas, mercados y registro de fuentes (YAML) |
| `config/` | Marca, mercados, avisos legales; presupuesto y topes de IA |
| `scripts/` | Validación, comprobación de la web, pipeline de IA, aprobación, panel, analítica, copias, PDF |
| `.claude/` | Skills, subagentes y permisos de Claude Code |
| `automation/` | Flujos n8n (probados en n8n 2.42.2) y cron |
| `docs/` | Documentación (fuente del PDF) |
| `reports/` | PDF, panel editorial, resultados de pruebas, costes |
| `tests/` | Pruebas pytest |

## Estado

Ver [`ESTADO.md`](ESTADO.md) (seguimiento para continuar el trabajo) e [`INVENTARIO.md`](INVENTARIO.md) (estado de cada entregable). **Nada está desplegado ni se ha gastado dinero.**
