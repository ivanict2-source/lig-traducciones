# 9. Arquitectura técnica

## 9.1 Tres arquitecturas comparadas

| | A. Máxima economía (local + web estática) | B. Híbrida (A + n8n local) | C. Gestionada en la nube |
|---|---|---|---|
| Componentes | Astro + Markdown/Git, scripts Python, Claude Code + skills, Cloudflare Pages, cron | A + n8n community en Docker (127.0.0.1) para programar flujos y alertas | n8n Cloud o VPS, CMS headless alojado, base de datos gestionada, API de IA desatendida |
| Coste inicial | 0 USD (+ dominio) | 0 USD (+ dominio) | Configuración de servicios de pago |
| Coste mensual | 0 USD + IA opcional | 0 USD + IA opcional + electricidad del equipo | Suscripciones (n8n Cloud, VPS, CMS): no se cotizaron; todas de pago |
| Coste anual estimado | ~10,5 USD (dominio) + IA (0-360 USD con tope) | Igual que A | Varios cientos de USD adicionales (sin cotizar) |
| Tokens/créditos | Redacción en Claude Code (suscripción); API solo para automatizar, con tope mensual | Igual que A | Mayor: todo pasa por API |
| Alojamiento | Cloudflare Pages gratuito: 500 builds/mes, activos estáticos sin medición, Functions con cuota de Workers gratuita (100.000 solicitudes/día) [cf-pages-limits] | Igual | Según proveedor |
| Mantenimiento | Bajo: sin servidores | Medio: actualizar n8n y Docker | Medio-alto |
| Limitaciones | Requiere el equipo encendido para tareas programadas; sin panel web | Igual + el nodo Execute Command de n8n 2.x viene desactivado por seguridad y hay que habilitarlo | Coste y dependencia |
| Seguridad | Superficie mínima (web estática) | n8n solo en localhost; habilitar Execute Command amplía su capacidad | Más credenciales y superficie expuesta |
| Dependencias externas | Cloudflare, Google Search Console, Anthropic | + Docker, n8n | + proveedores cloud |
| Migración | Trivial: HTML estático + Git (portable a Netlify, Vercel, GitHub Pages u otro) | Fácil: flujos exportados en JSON | Más difícil |

**Opción de coste mínimo:** A. **Opción recomendada:** A para el MVP, B solo si el propietario prefiere una interfaz visual para las tareas programadas; C descartada mientras no haya ingresos que la justifiquen.

## 9.2 Diagrama lógico (arquitectura A/B)

```
 [Equipo local]                                         [Internet]
  Claude Code + skills/agentes ──┐
  scripts/pipeline.py (API) ─────┤→ content/*.md (Git) ─┐
  scripts/validate/check ────────┘                      │ git push / wrangler (con autorización)
  cron o n8n (127.0.0.1) → make maintenance/backup     ▼
                                              Cloudflare Pages
                                              ├─ HTML estático (Astro)
                                              ├─ /go/<id>/ Pages Function (control geográfico)
                                              └─ Web Analytics (sin cookies)
  data/metrics/*.csv  ← exportaciones de Search Console y programas de afiliación
```

## 9.3 Decisiones clave

1. **Sin base de datos:** Markdown con frontmatter + YAML en Git cubren el volumen previsto; Git aporta historial, revisión y copia remota.
2. **Sin servidor permanente:** la única lógica en el borde es la redirección de afiliados (`website/functions/go/[id].js`), necesaria para no redirigir tráfico desde países sin licencia.
3. **Sin panel web:** el «panel» es `reports/estado-editorial.md`, generado por script (estados, pendientes, caducidad, costes). Construir un CMS no aporta valor con un solo editor.
4. **Dos compilaciones:** producción (solo contenido aprobado por una persona) y vista previa interna (`noindex`, banner rojo) para revisar borradores.
5. **Entornos separados:** desarrollo local y vista previa no indexable frente a producción en Cloudflare Pages; variables de entorno por entorno; `.env` nunca en Git.
6. **Dependencias fijadas** a versiones publicadas hace al menos 14 días (Astro 7.3.5, @astrojs/sitemap 3.7.4, anthropic 1.11.0, n8n 2.42.2, wrangler 4.147.0) para reducir el riesgo de la cadena de suministro.

# 10. Comparativa de herramientas

| Necesidad | Elegida | Alternativas evaluadas | Motivo | Coste (estado) |
|---|---|---|---|---|
| Generador web | Astro 7 | Hugo, Eleventy, Next.js | HTML estático sin JS por defecto, colecciones de contenido con validación de esquema (zod) | 0 (open source) |
| Alojamiento | Cloudflare Pages | Netlify, Vercel, GitHub Pages | Plan gratuito amplio, Functions para `/go/`, analítica sin cookies integrable | 0 en plan gratuito (límites documentados; pueden cambiar) |
| Contenido | Markdown + Git | CMS headless, WordPress | Coste cero, versionado, revisable por IA y por personas | 0 |
| Automatización | cron + Makefile | n8n community, n8n Cloud | Menos piezas; n8n como opción visual | 0; n8n autoalojado bajo Sustainable Use License, uso interno permitido [n8n-license-faq] |
| IA interactiva | Claude Code + skills/subagentes | Uso exclusivo de API | Sin coste marginal por token dentro de la suscripción | Según plan contratado (no verificado en este informe) |
| IA desatendida | API de Claude (Haiku 5.5 / Sonnet 5.5 / Opus 5.5) | Otros proveedores | Enrutado por tarea y tope de gasto | 0,10/0,50 · 2/10 · 4/20 USD por millón de tokens de entrada/salida [anthropic-pricing-skill] |
| Analítica | Cloudflare Web Analytics | Plausible, Umami autoalojado, GA4 | Gratuita y sin cookies según el proveedor | 0 [cf-web-analytics] |
| SEO | Google Search Console (exportaciones CSV) | Ahrefs, Semrush | Gratuita y con datos reales del propio sitio | 0 |
| Monitorización | `make maintenance` + alertas por correo (n8n) | Servicios de uptime | Web estática: el riesgo principal es contenido caducado, no caídas | 0 |
| PDF | ReportLab | WeasyPrint, Pandoc | Disponible, sin dependencias del sistema | 0 |
| Accesibilidad | axe-core + Chromium | Lighthouse | Automatizable en pruebas | 0 |

Ningún servicio se ha dado por gratuito sin indicar su fuente; los planes gratuitos tienen límites y pueden cambiar sus condiciones.
