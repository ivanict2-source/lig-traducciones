# Instrucciones para Claude Code — proyecto «Juego Verificado»

Sitio de afiliación de casinos online AUTORIZADOS (Colombia/Coljuegos, Perú/MINCETUR). Lee `ESTADO.md` al empezar.

## Reglas no negociables
- No inventes datos: licencias, contratos, dominios, comisiones, bonos, cifras, testimonios ni experiencias. Sin fuente → `[PENDIENTE: ...]` o `null`.
- Toda fuente nueva va a `data/sources.yaml` (id, url, fecha, `access: full|snippet`, claims).
- Nunca pongas `status: approved/published` ni `verification.status: verificado-humano`. Nunca ejecutes `scripts/approve.py`, `make deploy`, `wrangler deploy` ni `git push` (están denegados en `.claude/settings.json`).
- No gastes dinero, no contrates servicios, no publiques, no envíes comunicaciones a terceros, no expongas servicios locales a Internet.
- Nada de bonos, promesas de ganancia, «gratis», ni contenido dirigido a menores o a mercados sin licencia (Chile, República Dominicana excluidos).
- Contenido regulatorio: nunca traducir literalmente entre mercados.
- Respeta `config/budget.yaml` (topes de IA); usa `--dry-run` antes de lotes.

## Comandos
- `make validate` · `make build` · `make check` · `make test` · `make report` · `make pdf`
- Pipeline API: `.venv/bin/python scripts/pipeline.py --dry-run <brief|draft|translate|metadata|review> ...`

## Flujo editorial
planned → research → draft → review (máximo que puede poner un agente) → approved/published (solo persona).
Agentes: `.claude/agents/` (supervisor coordina). Skills: `.claude/skills/`.

## Al terminar una tarea
`make test` debe pasar; actualiza `ESTADO.md` si cambió algo relevante.
