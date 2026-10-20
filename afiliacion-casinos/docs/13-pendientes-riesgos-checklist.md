# 26. Errores pendientes

| # | Elemento | Tipo | Estado | Acción |
|---|---|---|---|---|
| 1 | El build de producción tiene 73 enlaces internos rotos hacia las 9 páginas legales/editoriales aún no aprobadas | Bloqueo deliberado | PENDIENTE DE REVISIÓN HUMANA | Aprobar las páginas legales; `check_site.py --production` debe quedar en 0 |
| 2 | Perú no se publica en producción: falta el texto literal de la advertencia sobre ludopatía | Bloqueo deliberado | PENDIENTE DE REVISIÓN HUMANA | Copiar el texto del DS 005-2023-MINCETUR en `config/site.yaml` |
| 3 | Ningún operador está `verificado-humano`: las tablas de producción salen vacías | Bloqueo deliberado | PENDIENTE DE REVISIÓN HUMANA | Verificación manual en Coljuegos/MINCETUR |
| 4 | Enlaces externos sin comprobar (48 únicos) | Limitación del entorno | BLOQUEADA (red) | `python scripts/check_site.py website/dist-preview --external` en un equipo con Internet |
| 5 | Pipeline por API sin llamadas reales | Falta de credenciales | BLOQUEADA | Definir `ANTHROPIC_API_KEY` y ejecutar un brief real con tope bajo |
| 6 | Correo de alertas n8n | Falta de credenciales SMTP | BLOQUEADA | Configurar credencial SMTP en n8n |
| 7 | `senales-casino-no-autorizado.md` tiene 295 palabras (mínimo orientativo 300) | Advertencia editorial | Pendiente | Ampliar durante la revisión |
| 8 | Comprobación de tipos de Astro (`astro check`) | Herramienta no instalada | NO EJECUTADA | Opcional: instalar `@astrojs/check` y `typescript` |
| 9 | Prueba de `/go/` en el borde real de Cloudflare | Requiere despliegue | NO EJECUTADA | Probar tras el primer despliegue autorizado |

# 30. Riesgos y decisiones pendientes

## 30.1 Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Programas que no aceptan afiliados de RD | Desconocida | Alto | Preguntar antes de invertir en contenido comercial; diversificar |
| Cambio regulatorio (Colombia: proceso ante el Consejo de Estado; Perú: fiscalización; México: nueva ley; RD: Ley 86-26) | Media | Alto | Revisión mensual de fuentes; contenidos con fecha de verificación; asesoría |
| Obligaciones fiscales o regulatorias del afiliado en RD | Media | Alto | Asesoría antes de cobrar comisiones |
| Actualizaciones de algoritmo y políticas de spam de Google | Media | Alto | Pocas páginas útiles, sin contenido masivo, sin enlaces comprados |
| Competencia de portales y medios consolidados | Alta | Medio | Nicho de verificación; consultas informativas primero |
| Dependencia de pocos operadores | Media | Medio | ≥ 3 programas por mercado; ningún programa > 40 % de ingresos |
| Errores de datos (operador que pierde la licencia) | Media | Alto (reputación y cumplimiento) | Caducidad de 30 días; verificación humana; correcciones públicas |
| Cambios en los planes gratuitos (Cloudflare) | Baja | Medio | Web estática portable a otros proveedores |
| Coste de IA | Baja | Bajo | Topes mensual y por tarea |
| Errores de la IA (alucinaciones) | Media | Alto | Fuentes obligatorias, PENDIENTE, validador, aprobación humana |
| Uso de una marca registrada como nombre del sitio | Desconocida | Medio | Búsqueda de marcas antes de comprar el dominio |

## 30.2 Decisiones pendientes del propietario

1. Aprobar la estrategia (Colombia + Perú, verificación primero) o pedir otra.
2. Marca y dominio definitivos.
3. Persona física o sociedad; asesoría legal y fiscal (asignación de hasta 1.500 USD).
4. Si se usa la API para automatizar (tope de 30 USD/mes) o solo Claude Code.
5. cron o n8n.
6. Qué programas solicitar primero.
7. Autorizar el primer despliegue.

# 31. Lista de comprobación final

| Estado | Elemento |
|---|---|
| INVESTIGADO | Regulación de 11 mercados, programas, competencia, herramientas y precios (con limitaciones de acceso indicadas) |
| CONSTRUIDO | Web, contenidos, datos, pipeline de IA, validadores, panel, analítica, copias, skills, agentes, flujos n8n, cron, PDF |
| PROBADO | 29 pruebas Python, 4 Node, axe en 38 páginas × 2 temas, enlaces/SEO, importación y ejecución real en n8n, instalación limpia |
| PREPARADO, SIN DESPLEGAR | Cloudflare Pages, `/go/`, analítica, sitemap, `make deploy` |
| REQUIERE CREDENCIALES | API de Claude, Cloudflare, SMTP para n8n, cuentas de programas de afiliación, Search Console |
| REQUIERE APROBACIÓN HUMANA | 14 contenidos en revisión, verificación de 17 operadores, texto legal de Perú, despliegue, gastos |
| NO VERIFICADO | Condiciones de los programas, admisión de afiliados de RD, texto completo de las fuentes (leídas como fragmentos), efecto de la Ley 86-26, tratamiento fiscal |
