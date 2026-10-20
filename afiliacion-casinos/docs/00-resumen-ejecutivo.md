# 2. Resumen ejecutivo

**Fecha del informe:** 20 de octubre de 2026. **Propietario:** residente en República Dominicana. **Techo de inversión:** 5.000 USD (no es un objetivo de gasto).

## Qué se propone

Un único sitio editorial en español, **«Juego Verificado»** (nombre provisional), que informa qué operadores de casino y apuestas online están **autorizados** en cada país, comprobado en el registro oficial del regulador, con fuente y fecha de verificación. Se monetiza con comisiones de afiliación de operadores autorizados. El MVP cubre **Colombia** (Coljuegos) y **Perú** (MINCETUR, Ley 31557): los dos mercados latinoamericanos investigados que combinan régimen de licencias online vigente, registro público consultable y programas de afiliación conocidos.

## Por qué no la idea inicial tal cual

Un portal internacional multilingüe de casinos compite con sitios consolidados, multiplica el riesgo regulatorio (cada país tiene reglas propias para afiliados) y diluye un presupuesto pequeño. Además, Google penaliza explícitamente el contenido generado a escala sin valor añadido y las páginas de afiliación «delgadas» ([google-spam-policies]). La ventaja defendible de un operador pequeño con IA no es producir más páginas, sino **verificar mejor**: registros oficiales, fechas, fuentes y avisos regulatorios automatizados con control humano.

## Qué está construido y probado (en este repositorio)

| Componente | Estado |
|---|---|
| Web estática Astro 7 (portada, mercados, comparativas de licencias, fichas, guías, legales, fuentes) | Construida y probada (build producción + preview) |
| Sistema de contenidos Markdown con flujo planned → published y aprobación humana obligatoria | Construido y probado |
| Datos estructurados: 17 operadores, 7 programas, 11 mercados, 46 fuentes | Construido; datos pendientes de verificación humana |
| Redirección de afiliados con bloqueo geográfico (Cloudflare Pages Function) | Construida y probada con pruebas unitarias; sin desplegar |
| Pipeline de IA con topes de coste, caché y registro (API de Claude) | Construido y probado con cliente simulado; sin llamadas reales (no hay credenciales) |
| 9 skills y 8 subagentes de Claude Code | Creados; validado su formato |
| 4 flujos n8n + programación cron | Creados; ver estado de la prueba de importación en el capítulo de pruebas |
| Pruebas: 29 Python, 4 Node, accesibilidad axe (38 páginas × 2 temas), enlaces y SEO | Ejecutadas y aprobadas |
| Copias de seguridad, panel editorial, informe de rendimiento | Construidos y probados |
| Este PDF y su fuente Markdown | Generados |

## Qué falta y requiere a una persona

1. **Verificar manualmente** cada operador en el registro oficial (el entorno no permitía abrir páginas web: las fuentes se leyeron como resultados de búsqueda).
2. **Revisar y aprobar** las 14 páginas en estado *review* (legales y guías). Hasta entonces, la compilación de producción no contiene esas páginas y el despliegue está **bloqueado por diseño**.
3. Completar la **advertencia literal sobre ludopatía** de Perú (DS 005-2023-MINCETUR); sin ella, Perú no se publica.
4. **Asesoría** legal y fiscal en República Dominicana (Ley 86-26 de 2026; tributación de comisiones según la DGII) y validación de obligaciones de afiliados en Colombia y Perú.
5. Contactar a los programas de afiliación y confirmar por escrito que aceptan a un afiliado residente en RD, con sus condiciones (no se pudo verificar).
6. Comprar el dominio, crear la cuenta de Cloudflare y autorizar el despliegue.

## Coste

- **Mínimo viable:** ~10,5 USD/año (dominio, estimado) + 0 USD de alojamiento y analítica en planes gratuitos, usando Claude Code con la suscripción existente para redactar.
- **Recomendado:** ~370 USD/año (dominio + tope de API de 30 USD/mes para automatizar) más una **asignación** de hasta 1.500 USD para asesoría legal y fiscal (pendiente de cotización).
- Coste de IA por artículo con el pipeline: **≈0,15–0,60 USD** (estimación con precios oficiales; tokens estimados).

## Advertencia

No hay proyección de ingresos: no se dispone de datos verificables de tráfico, conversión ni comisiones para este sitio, y presentarlos sería especulativo. El plan de validación (capítulo 12) define cuándo y con qué datos ampliar la inversión.
