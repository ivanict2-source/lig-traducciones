# Estado del proyecto (seguimiento para continuar sin perder contexto)

**Última actualización:** 2026-10-20 · **Rama:** `claude/casino-affiliate-ai-business-abdrjp`

## Decisiones tomadas
1. Un solo dominio en español, subcarpetas por país; MVP Colombia + Perú; estrategia «verificación primero» (docs/01).
2. Arquitectura A: Astro estático + Markdown/Git + Cloudflare Pages + scripts locales + cron; n8n opcional (docs/04).
3. Sin base de datos, sin CMS, sin servidor: panel = `reports/estado-editorial.md`.
4. Aprobación humana obligatoria para publicar y para marcar operadores como verificados (`scripts/approve.py`).
5. Afiliación solo vía `/go/` con control geográfico; CL y DO bloqueados.
6. IA: Claude Code + skills para trabajo interactivo; API con topes (30 USD/mes, 1,50 USD/tarea) para automatizar.
7. Dependencias fijadas a versiones con ≥ 14 días.

## Hecho
Investigación (46 fuentes), datos (17 operadores, 7 programas, 11 mercados), web, 14 contenidos en revisión, scripts, 9 skills, 8 agentes, 4 flujos n8n probados, cron, pruebas (`make test` verde), PDF de 34 páginas.

## Bloqueos (requieren al propietario)
- Verificación manual de operadores; aprobación de 14 contenidos; texto literal de la advertencia de Perú.
- Asesoría legal/fiscal (RD Ley 86-26, DGII); confirmación de los programas de afiliación.
- Dominio, cuenta de Cloudflare, Search Console, SMTP para n8n, `ANTHROPIC_API_KEY` (opcional).
- Red del entorno de construcción: no se pudieron abrir páginas web (solo resultados de búsqueda) ni comprobar enlaces externos.

## Sesión siguiente (pedido del propietario)
- **Traslado a repositorio independiente** (el propietario no quiere ningún vínculo con el otro repositorio):
  1. El propietario crea el repo privado `juego-verificado` y da acceso a la app de Claude.
  2. `git subtree split --prefix=afiliacion-casinos`, clonar, reiniciar historial con un único commit en `main`.
  3. Quitar referencias al repositorio anterior (README, docs/05, docs/11, cron, build_pdf tree, logs de pruebas), `make setup && make test`, `make pdf`, comprobar con `git grep` que no quedan menciones.
  4. Push a `juego-verificado` y, solo con confirmación expresa, borrar la rama del repositorio anterior.
- Responder en detalle: ¿es buena idea de negocio y vale la pena? (veredicto preliminar dado: experimento de bajo coste con criterios de abandono; ver conversación).
- Vista previa privada publicada: https://claude.ai/artifact/Cj4DKDweX7dppA5rsDJhuC
- Revisar `docs/anexo-estructura-georgia-estonia.md` (cuenta en Georgia + OÜ en Estonia). Conclusión preliminar: no constituir aún; validar con asesor en RD.
- Repetir `git push` cuando GitHub tenga acceso (2-3 commits locales pendientes).

## Próximos pasos sugeridos
1. Propietario: leer `reports/informe-proyecto.pdf` y decidir (capítulo 30.2).
2. Ejecutar `python scripts/check_site.py website/dist-preview --external` con Internet.
3. Abrir cada fuente `access: snippet` y confirmar; luego `approve.py verify-operator`.
4. Solicitar programas de afiliación con las preguntas de docs/03.
