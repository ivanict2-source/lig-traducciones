# 11. Presupuesto

Todos los importes en USD. **Confirmado** = precio público consultado en una fuente identificada (puede cambiar). **Estimado** = cálculo propio o fuente secundaria. **Asignación** = reserva presupuestaria a la espera de cotización; no es un precio.

## 11.1 Precios de referencia

| Concepto | Importe | Estado | Fuente |
|---|---|---|---|
| Dominio .com en Cloudflare Registrar | 10,11-10,46/año | Estimado (rastreadores de terceros) | [cf-registrar-com-price] |
| Cloudflare Pages (gratuito) | 0 | Confirmado con límites: 500 builds/mes; Functions con cuota gratuita de Workers | [cf-pages-limits] |
| Cloudflare Web Analytics | 0 | Confirmado por el proveedor | [cf-web-analytics] |
| Google Search Console | 0 | Conocimiento general (no consultado en esta sesión) | — |
| n8n community autoalojado | 0 | Licencia de uso interno | [n8n-license-faq] |
| Claude Haiku 5.5 | 0,10 entrada / 0,50 salida por millón de tokens | Confirmado | [anthropic-pricing-skill] |
| Claude Sonnet 5.5 | 2 / 10 por millón de tokens | Confirmado | [anthropic-pricing-skill] |
| Claude Opus 5.5 | 4 / 20 por millón de tokens | Confirmado | [anthropic-pricing-skill] |
| Batch API | −50 % | Confirmado | [anthropic-pricing-skill] |
| Suscripción de Claude Code | Según el plan del propietario | No verificado | — |

## 11.2 Coste de IA por artículo (pipeline por API)

| Tarea | Modelo | Tokens estimados (entrada / salida) | Coste |
|---|---|---|---|
| Brief | Sonnet 5.5 | 3.000 / 2.000 | 0,026 |
| Borrador | Sonnet 5.5 | 5.000 / 3.000 | 0,040 |
| Metadatos | Haiku 5.5 | 2.000 / 200 | 0,0003 |
| Verificación y cumplimiento | Opus 5.5 | 6.000 / 3.000 | 0,084 |
| **Total por artículo (1 iteración)** | | | **≈ 0,15** |
| Con reintentos y razonamiento adicional facturado como salida | | | **≈ 0,30-0,60** |

Los tokens son estimaciones; el coste real queda en `reports/costes/ledger.csv` con los tokens reportados por la API. El tope por tarea (1,50) y el mensual (30) detienen el pipeline. Con la suscripción de Claude Code y las skills, el coste marginal por artículo es 0.

## 11.3 Escenarios

| Partida | 1. Mínimo viable | 2. Recomendado | 3. Ampliación (solo con datos) |
|---|---|---|---|
| Desarrollo | 0 (hecho en este repositorio) | 0 | Según la mejora |
| Dominio | 10,5/año (estimado) | 10,5/año | +10,5/año por dominio adicional (no recomendado: subcarpetas) |
| Alojamiento | 0 | 0 | Cloudflare Workers de pago si se supera la cuota gratuita (no cotizado) |
| IA | 0 (Claude Code) | Tope de 30/mes de API = máx. 360/año | Aumentar el tope tras demostrar retorno |
| Automatización | 0 (cron) | 0 (cron o n8n local) | VPS para n8n (asignación ≤ 120/año) |
| Analítica | 0 | 0 | Herramienta SEO de pago (asignación ≤ 1.500/año, solo si los datos lo justifican) |
| Asesoría legal y fiscal | 0 (no recomendado) | **Asignación ≤ 1.500** (RD, Colombia, Perú) | Asesoría por mercado nuevo (asignación ≤ 750 por mercado) |
| Servicios auxiliares | 0 (reenvío de correo gratuito; verificar) | 0 | — |
| Mantenimiento | Tiempo del propietario | Tiempo del propietario | Revisor editorial externo (asignación por definir) |
| **Inicial** | **≈ 10,5** | **≈ 10,5 + asignación legal ≤ 1.500** | — |
| **Recurrente anual** | **≈ 10,5** | **≈ 370** | Según activación |

Con el escenario recomendado, el primer año queda por debajo de **1.900** del techo de 5.000, conservando más de 3.000 de liquidez.

## 11.4 Controles de consumo implementados

Presupuesto por tarea, tope mensual, máximo de iteraciones, `max_tokens` acotado, caché local por hash de la petición, prompt de sistema cacheado en la API, reutilización de investigación (`data/sources.yaml`), enrutado a modelos económicos para tareas sencillas, escalado a Opus solo en tareas sensibles o tras dos fallos y registro de cada llamada.
