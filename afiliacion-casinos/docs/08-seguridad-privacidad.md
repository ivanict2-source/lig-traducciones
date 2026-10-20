# 24. Seguridad y privacidad

## 24.1 Medidas implementadas

| Riesgo | Medida | Verificación |
|---|---|---|
| Secretos en el repositorio | `.env` en `.gitignore`; `.env.example` sin valores; Claude Code tiene denegada la lectura de `.env` | Prueba `test_no_secrets_in_tracked_files` (patrones de claves de Anthropic, AWS, GitHub, Slack y claves privadas) |
| Publicación accidental de borradores | Compilación de producción solo con contenido `published` + aprobación humana; mercados con aviso incompleto excluidos | Pruebas `test_production_contains_only_approved_content` y `..._only_lists_human_verified_operators` |
| Acciones irreversibles por agentes | Permisos denegados: `approve.py`, `make deploy`, `wrangler deploy`, `git push`; `make deploy` exige validación estricta y escribir PUBLICAR | Revisión de `.claude/settings.json` |
| Tráfico de afiliación a mercados no autorizados | `/go/` solo redirige si el país (cabecera de Cloudflare) coincide con el de la licencia; CL y DO bloqueados | `website/tests/go.test.mjs` |
| Inyección en la redirección | Sub-ID saneado (solo `a-z0-9-`, 60 caracteres), destinos solo desde datos generados y HTTPS obligatorio | Pruebas unitarias + `gen-go-links.mjs` |
| Ataques en el navegador | CSP estricta sin scripts de terceros (salvo el beacon de Cloudflare), `frame-ancestors 'none'`, HSTS, `nosniff` | `public/_headers` |
| Exposición de n8n | Publicado solo en 127.0.0.1; Execute Command habilitado de forma explícita y documentada | `docker-compose.yml` |
| Cadena de suministro | Versiones fijadas con ≥ 14 días de antigüedad; dependencias mínimas (3 de ejecución en la web) | `package.json`, `requirements.txt` |
| Gasto descontrolado de IA | Topes mensual y por tarea, iteraciones máximas, caché y registro | `tests/test_llm.py` |
| Pérdida de datos | Git + copias comprimidas con suma SHA-256, rotación y restauración probada | `tests/test_scripts.py` |

## 24.2 Privacidad

- No hay cuentas de usuario, formularios, cookies propias ni píxeles publicitarios.
- Analítica sin cookies (según Cloudflare). Los datos técnicos de conexión los trata Cloudflare como encargado.
- Las métricas de afiliación son agregadas por sub-ID, sin datos personales de jugadores.
- La política de privacidad (borrador) cita como referencia la Ley 172-13 (RD), la Ley 1581 de 2012 (Colombia) y la Ley 29733 (Perú): **requiere revisión profesional**.

## 24.3 Pendiente

- Activar la autenticación en dos pasos en Cloudflare, el registrador, GitHub y los programas de afiliación.
- Usar un token de API de Cloudflare con permisos mínimos (solo Pages) si se despliega desde la línea de comandos.
- Gestor de contraseñas para las credenciales de los programas.
