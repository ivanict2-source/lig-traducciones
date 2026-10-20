# 13. Instrucciones de instalación paso a paso

Requisitos: Git, Python 3.11 o superior, Node.js 22 o superior, `make` (Linux/macOS o WSL en Windows). Opcional: Docker (n8n), Chromium (auditoría de accesibilidad; se usa el de Playwright si existe, o la ruta en `CHROMIUM_PATH`).

```bash
git clone <URL-del-repositorio> && cd lig-traducciones/afiliacion-casinos
make setup            # crea .venv e instala dependencias fijadas (pip + npm ci)
cp .env.example .env  # rellenar solo lo necesario; nunca subir .env
make test             # validación, builds, enlaces/SEO, pytest, Node y accesibilidad
make preview          # vista previa interna en http://127.0.0.1:4321 (noindex)
```

Uso con Claude Code: abrir Claude Code en `afiliacion-casinos/`. Se cargan `CLAUDE.md`, las skills (`.claude/skills/`), los subagentes (`.claude/agents/`) y los permisos (`.claude/settings.json`). Ejemplo: «Usa el agente supervisor para crear un artículo sobre cómo comprobar el número de contrato en Coljuegos».

Pipeline por API (opcional): definir `ANTHROPIC_API_KEY` en `.env` (o `ant auth login`) y probar primero con `--dry-run`:

```bash
.venv/bin/python scripts/pipeline.py --dry-run brief --topic "..." --market CO
```

**Instalación limpia verificada:** el procedimiento se ejecutó desde cero en un clon nuevo (ver capítulo 25).

# 14. Estructura de carpetas

{{arbol}}

# 15. Código y configuración relevantes

| Archivo | Función |
|---|---|
| `website/src/content.config.ts` | Esquema zod de los contenidos (bloquea el build si falta un campo) |
| `website/src/lib/content.ts` | Regla de publicación (producción solo `published` + aprobación + mercado publicable) |
| `website/src/lib/data.ts` | Carga de YAML; operadores visibles solo si `verificado-humano`; mercados publicables |
| `website/src/layouts/Base.astro` | SEO (canonical, hreflang, robots), avisos +18, afiliación, leyenda del mercado |
| `website/edge/go.js` + `functions/go/[id].js` | Redirección de afiliados con control geográfico |
| `website/scripts/gen-go-links.mjs` | Genera los enlaces activos desde `operators.yaml` |
| `website/public/_headers` | Cabeceras de seguridad |
| `scripts/validate_content.py` | Reglas editoriales, de cumplimiento, duplicados y datos |
| `scripts/check_site.py` | Enlaces internos/externos, SEO, hreflang, a11y básica |
| `scripts/llm.py` / `scripts/pipeline.py` | IA con presupuesto, caché y registro / fases del pipeline |
| `scripts/approve.py` | Aprobación y publicación humanas; verificación de operadores |
| `scripts/editorial_status.py` | Panel editorial y caducidad |
| `scripts/analytics_report.py` | Rendimiento SEO, afiliación y costes |
| `scripts/backup.py` | Copias de seguridad |
| `scripts/build_pdf.py` | Este informe |
| `config/site.yaml`, `config/budget.yaml` | Marca, mercados, leyendas / precios, topes y enrutado de modelos |

# 27. Procedimiento de despliegue

**Requiere autorización expresa del propietario.** Nada se ha desplegado.

1. Comprar el dominio (p. ej. en Cloudflare Registrar) y crear la cuenta de Cloudflare con autenticación en dos pasos.
2. Crear un proyecto de Cloudflare Pages conectado al repositorio de Git o para subida directa:
   - Directorio raíz: `afiliacion-casinos/website`
   - Comando de build: `npm ci && npm run build`
   - Directorio de salida: `dist`
   - Variables: `SITE_URL=https://<dominio>`, `PUBLIC_CF_BEACON_TOKEN=<token>` (opcional), `NODE_VERSION=22`
   - La carpeta `functions/` se despliega automáticamente como Pages Functions (`/go/`).
3. Producción solo desde la rama principal. En Cloudflare Pages, definir la variable `PUBLIC_BUILD_MODE=preview` **solo en el entorno de vista previa** (ramas de trabajo): el mismo comando de build genera entonces una web `noindex`, con banner de borrador y sin sitemap.
4. Alternativa por línea de comandos: `make deploy` (exige validación estricta sin advertencias, confirmación escrita y `CF_PAGES_PROJECT`).
5. Tras el primer despliegue: verificar el dominio en Google Search Console, enviar `sitemap-index.xml`, activar Web Analytics y comprobar `/go/` desde el país del mercado (o con un VPN de ese país solo para pruebas internas).
6. **Reversión:** en Cloudflare Pages, promover el despliegue anterior; o `git revert` y nuevo build.

# 28. Mantenimiento y copias de seguridad

| Frecuencia | Tarea | Comando |
|---|---|---|
| Diaria | Copia de seguridad (rotación de 14, SHA-256) | `make backup` |
| Semanal | Validación, build, enlaces/SEO, caducidad, panel | `make maintenance` |
| Semanal | Revisar `reports/estado-editorial.md` y la cola de revisión | — |
| Mensual | Informe de rendimiento y costes; descargar CSV de Search Console y programas a `data/metrics/` | `make report` |
| Mensual | Revalidar operadores en los registros oficiales (o ante cualquier noticia regulatoria) | skill `verificacion-fuentes` + `approve.py verify-operator` |
| Trimestral | Actualizar dependencias (solo versiones con ≥ 14 días), revisar límites de los planes gratuitos | `npm outdated`, `pip list --outdated` |
| Trimestral | Probar restauración | `scripts/backup.py restore <archivo> --to /tmp/prueba` |

**Recuperación:** (1) clonar el repositorio; (2) si falta algo no confirmado, restaurar la última copia con `backup.py restore`; (3) `make setup && make test`; (4) redeploy. Guardar periódicamente una copia fuera del equipo (disco externo o almacenamiento propio).
