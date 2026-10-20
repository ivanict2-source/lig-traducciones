# 12. Plan de ejecución

Las duraciones son estimaciones de esfuerzo, no fechas. Dependen sobre todo de la disponibilidad del propietario para las tareas humanas.

| Etapa | Objetivo | Tareas | Archivos | Coste | Dependencias | Riesgos | Pruebas | Criterio de finalización | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1. Investigación y decisión | Viabilidad, mercados, estrategia | Investigación regulatoria, programas, competencia | `docs/01-03`, `data/*.yaml` | 0 | Acceso web | Fuentes solo como fragmentos de búsqueda | Validación de datos | Estrategia documentada con fuentes | **Hecha** (con verificación humana pendiente) |
| 2. Diseño | Arquitectura, agentes, presupuesto | Comparativas, diseño de flujos y agentes | `docs/04-09` | 0 | Etapa 1 | — | Revisión | Arquitectura y presupuesto aprobados por el propietario | **Hecha**; falta aprobación del propietario |
| 3. MVP | Web + contenidos + datos | Astro, contenidos, legales, fichas | `website/`, `content/`, `data/` | 0 | Etapa 2 | Datos sin verificar | Build, SEO, a11y | Builds sin errores; producción solo con aprobados | **Hecha** (código); contenido en revisión |
| 4. Automatización | Flujos repetibles y controles | Pipeline IA, validadores, n8n, cron, backups | `scripts/`, `automation/`, `.claude/` | 0 | Etapa 3 | API sin probar en real | Pytest, Node, n8n | Pruebas aprobadas | **Hecha**; API real pendiente de credenciales |
| 5. Pruebas | Calidad | Ejecutar y corregir | `tests/`, `reports/pruebas/` | 0 | Etapas 3-4 | Pruebas externas bloqueadas por red | Todas | `make test` sin errores | **Hecha** (ver cap. 25) |
| 6. Preparación del despliegue | Dejar todo listo | Dominio, Cloudflare, Search Console, aprobaciones | `docs/11-*`, `Makefile` | ~10,5 | **Propietario**: compra, cuentas, aprobaciones | Retrasos en verificación humana | Validación estricta, check de producción | `make deploy` sin bloqueos | **Preparada; requiere autorización y tareas humanas** |
| 7. Validación comercial | Medir tráfico, interés y conversiones | Publicar 10-15 páginas útiles, alta en 3+ programas, medir 90-180 días | `data/metrics/`, `reports/rendimiento.md` | IA ≤ 30/mes | Etapa 6, programas aceptados | Indexación lenta, rechazo de programas | Informes mensuales | Puntos de control (abajo) | Pendiente |
| 8. Expansión | Crecer con datos | Nuevos mercados/idiomas/herramientas según criterios | — | Según criterio | Etapa 7 | Regulatorio | — | Criterios cuantificables cumplidos | Pendiente |

## 12.1 Lista de tareas humanas para desbloquear el despliegue (orden recomendado)

1. Leer este informe y decidir marca y dominio (comprobar disponibilidad y marcas registradas).
2. Consulta legal y fiscal (RD; obligaciones del afiliado en Colombia y Perú).
3. Verificar cada operador de Colombia en el registro de Coljuegos y registrar la verificación con `scripts/approve.py verify-operator <id> --by "Nombre" [--url ...]`.
4. Completar los PENDIENTE de las páginas legales (titular, contacto, plazos) y aprobarlas.
5. Revisar, completar y aprobar las guías.
6. Copiar el texto literal de la advertencia de Perú en `config/site.yaml` (desbloquea `/pe/`).
7. Comprar el dominio, crear el proyecto de Cloudflare Pages y verificar el dominio en Search Console.
8. Solicitar el alta en los programas de afiliación con las preguntas del capítulo 7.2.
9. Autorizar `make deploy`.

## 12.2 Experimentos de validación (etapa 7)

| Experimento | Hipótesis | Métrica | Umbral de decisión |
|---|---|---|---|
| Guías de verificación vs. comparativa | Las consultas informativas indexan antes | Impresiones por página a 90 días | Priorizar el tipo de página con más impresiones medianas |
| Mejora de títulos (CTR) | Títulos con «registro oficial» mejoran el CTR | CTR por página (Search Console) | Mantener si el CTR mejora ≥ 20 % relativo con ≥ 500 impresiones |
| Posición del enlace comercial en la ficha | Más visible = más clics sin perjudicar la confianza | Clics de afiliación por sesión (informe del programa) | Mantener si los clics suben sin aumento de quejas |
| Perú vs. Colombia | Perú tiene menos competencia | Impresiones y clics por mercado | Asignar el 70 % del nuevo contenido al mercado ganador |

# 29. Plan de expansión

La expansión se activa solo con datos observados. Criterios propuestos (decisiones del propietario, no previsiones):

| Ampliación | Criterio cuantificable |
|---|---|
| Más contenido en CO/PE | ≥ 1.000 impresiones/semana en Search Console durante 4 semanas seguidas |
| Aumentar el tope de API | Ingresos confirmados de los últimos 3 meses ≥ 3 veces el gasto de IA del mismo periodo |
| México | Registro público de permisos verificable o nueva ley publicada + asesoría local + ≥ 1 programa con marcas mexicanas aceptado |
| Inglés | Evidencia en Search Console de demanda en inglés para mercados con licencia accesibles (p. ej. ≥ 500 impresiones/mes en consultas en inglés) y un mercado angloparlante con riesgo asumible |
| Herramienta SEO de pago | ≥ 50 páginas publicadas y necesidad de datos de competidores no cubierta por Search Console |
| n8n en VPS | Necesidad real de ejecución 24/7 que el equipo local no cubre |
| Producto B2B (monitor de licencias para afiliados/operadores) | ≥ 3 solicitudes de terceros o interés documentado; el sistema de verificación funcionando 6 meses sin errores graves |
| Brasil | Contrato en portugués revisado por un abogado brasileño y capacidad editorial en portugués |
