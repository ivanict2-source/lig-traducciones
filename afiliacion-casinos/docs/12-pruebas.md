# 25. Pruebas realizadas

Estados: **APROBADA**, **FALLIDA**, **NO EJECUTADA**, **BLOQUEADA**, **PENDIENTE DE REVISIÓN HUMANA**. Fecha de ejecución: 2026-10-20. Registro completo de `make test` en `reports/pruebas-make-test.log`.

| # | Prueba | Herramienta | Resultado | Estado |
|---|---|---|---|---|
| 1 | Compilación de producción | `astro build` | 6 páginas; solo contenido aprobado y mercados publicables | APROBADA |
| 2 | Compilación de vista previa | `astro build` (preview) | 39 páginas con banner y `noindex` | APROBADA |
| 3 | Validación del esquema de contenido | zod en `content.config.ts` | Detectó y bloqueó una descripción de 167 caracteres y un título de 8 (corregidos) | APROBADA |
| 4 | Reglas editoriales y de cumplimiento | `validate_content.py` | 0 errores, 3 advertencias (despliegue bloqueado por páginas legales sin aprobar; Perú no publicable; una guía con 295 palabras) | APROBADA |
| 5 | Enlaces internos, SEO, metadatos, hreflang (preview) | `check_site.py` | 39 páginas, 0 errores, 0 advertencias | APROBADA |
| 6 | Enlaces internos de producción | `check_site.py --production` | 73 enlaces a 9 páginas legales sin aprobar | PENDIENTE DE REVISIÓN HUMANA (bloqueo deliberado) |
| 7 | Enlaces externos (47) | `check_site.py --external` | Red del entorno bloqueada | BLOQUEADA |
| 8 | Producción sin borradores, sin PENDIENTE y sin banner | pytest | Detectó un fallo real (aviso de Perú con PENDIENTE en producción); corregido | APROBADA |
| 9 | Solo operadores verificados por humanos en producción | pytest | 0 fichas en producción; 17 en preview | APROBADA |
| 10 | robots.txt y sitemap por entorno | pytest | Preview `Disallow: /`; producción bloquea `/go/` y publica el sitemap | APROBADA |
| 11 | Control de duplicados, frases prohibidas, fuentes desconocidas, permalinks reservados, publicación sin aprobación | pytest (6 casos) | Todos detectados | APROBADA |
| 12 | Coste, registro, caché, topes mensual y por tarea, rechazo, fallback y escalado de modelo | pytest con cliente simulado | 6 casos | APROBADA |
| 13 | Pipeline de IA en modo simulación | `pipeline.py --dry-run` | Prompt y coste máximo estimado (brief ≈ 0,045 USD) | APROBADA |
| 14 | Pipeline de IA con llamadas reales | API de Claude | Sin credenciales en el entorno | BLOQUEADA |
| 15 | Aprobación humana (rechaza agentes y PENDIENTE; publicar exige aprobación) | pytest | 2 casos | APROBADA |
| 16 | Analítica (clics frente a conversiones confirmadas; sin datos no inventa) | pytest con datos de prueba | 2 casos | APROBADA |
| 17 | Copias de seguridad (crear, verificar SHA-256, restaurar, excluir .env) | pytest | 1 caso de ida y vuelta | APROBADA |
| 18 | Redirección de afiliados (país permitido, bloqueos CL/DO/otros, sub-ID saneado, 404) | `node --test` | 4 casos | APROBADA |
| 19 | Accesibilidad | axe-core 4.13 + Chromium (38 páginas × claro/oscuro) | 0 incidencias (se corrigieron avisos de landmarks) | APROBADA |
| 20 | Visual en escritorio y móvil (390 px) | Capturas con Chromium | Se corrigió un desbordamiento horizontal de una URL larga | APROBADA |
| 21 | Validez de YAML/JSON y ausencia de credenciales en flujos n8n | pytest | OK | APROBADA |
| 22 | Formato de skills y subagentes | pytest (frontmatter) | 9 skills y 8 agentes válidos | APROBADA |
| 23 | Ausencia de secretos en archivos versionados | pytest (patrones de claves) | Ninguno | APROBADA |
| 24 | Importación de flujos n8n | n8n 2.42.2 CLI | 4/4 tras corregir 1 defecto | APROBADA |
| 25 | Ejecución de flujos n8n | `n8n execute` | Comandos con exitCode 0 en los 4; nodos de correo sin SMTP | APROBADA (comandos) / BLOQUEADA (correo) |
| 26 | Panel editorial y caducidad | `editorial_status.py` | Informe generado | APROBADA |
| 27 | Generación y apertura del PDF | ReportLab + `pdfinfo`/`pdftotext` | Ver capítulo 31 y la salida de `make pdf` | APROBADA |
| 28 | Instalación limpia desde un clon nuevo | `make setup && make test` | Ver nota inferior | APROBADA |
| 29 | Comprobación de tipos de Astro | `astro check` | Requiere instalar dependencias adicionales | NO EJECUTADA |
| 30 | Rendimiento | Tamaño de las páginas | HTML estático sin JavaScript propio; CSS único de unos 3 KB | APROBADA (medición básica) |
| 31 | Seguridad de dependencias | `npm audit` / `pip-audit` | No ejecutado (requiere red al servicio de avisos) | NO EJECUTADA |
| 32 | Prueba de `/go/` en el borde de Cloudflare | Despliegue real | Requiere despliegue autorizado | NO EJECUTADA |

**Instalación limpia:** se clonó el repositorio en un directorio temporal, se ejecutó `make setup` (creación de `.venv`, `pip install -r requirements.txt`, `npm ci`) y después `make test`; el resultado se registra en `reports/pruebas/instalacion-limpia.log`.

**Errores encontrados y corregidos durante las pruebas:** descripciones fuera de rango; landmarks de accesibilidad; desbordamiento en móvil; aviso de Perú con PENDIENTE en producción; flujos n8n sin `id`; uso de `$env` bloqueado en n8n 2.x; flujos programados sin disparador manual; una afirmación sin fuente en una guía («monopolio rentístico»), que se reformuló.
