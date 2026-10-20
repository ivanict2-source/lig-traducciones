# 3. Evaluación crítica del modelo inicial

## 3.1 Cómo gana dinero un afiliado de casinos

El afiliado publica contenido que dirige usuarios a un operador mediante un enlace con identificador. El operador paga según el contrato:

- **CPA (coste por adquisición):** importe fijo por cada jugador que cumple un criterio (habitualmente registro + primer depósito por encima de un umbral). Ingreso inmediato y acotado.
- **Revenue share:** porcentaje de los ingresos netos de juego que el jugador genera durante la vida de la cuenta. Ingreso recurrente, pero variable y expuesto a deducciones (bonos, impuestos, comisiones de pago) y, según el contrato, al **arrastre de saldo negativo** (*negative carryover*).
- **Híbrido:** CPA reducido + revenue share.

Las condiciones concretas (tasas, umbrales, retenciones, duración de la atribución, cláusulas de exclusión e inactividad) **no se pudieron verificar en fuentes primarias**: los términos oficiales no eran accesibles desde el entorno. Los agregadores consultados citan, por ejemplo, revenue share del 25-50 % en Betsson o «tarifas a petición» en Codere, y se contradicen entre sí (ver capítulo 7). Deben confirmarse por escrito con cada programa.

## 3.2 Debilidades de la idea inicial («negocio internacional de casinos con IA»)

| Supuesto inicial | Problema detectado | Evidencia |
|---|---|---|
| Alcance internacional desde el inicio | Cada mercado impone reglas propias a los afiliados (Brasil: contratos en portugués y responsabilidad compartida; Ontario: prohibición de anunciar incentivos; Nueva Jersey: registro o licencia del afiliado; España: el RD 958/2020 alcanza a afiliados). Multiplica el coste legal. | [spa-portaria-1231], [agco-advertising], [ifrah-nj-affiliates], [boe-rd-958-2020] |
| La IA permite producir mucho contenido | Google trata como spam la producción masiva para manipular rankings, con IA o sin ella, y las páginas de afiliación sin valor añadido. | [google-spam-policies], [google-march-2024] |
| Si el casino acepta jugadores de un país, se puede promocionar allí | Falso: Chile no tiene régimen de licencias online y su superintendencia considera no autorizada la explotación; Perú bloquea plataformas no autorizadas. | [chile-proyecto-2026], [elperuano-bloqueo-2026] |
| El residente en RD no tiene restricciones | La nueva Ley 86-26 (octubre de 2026) incluye el juego por internet y crea un regulador; su reglamento y su efecto sobre promotores no se conocen aún. La DGII ha calificado como renta de fuente dominicana servicios prestados desde RD a empresas extranjeras (criterio no uniforme). | [rd-ley-86-26], [dgii-consulta-40], [dgii-aviso-22-25] |
| Depender de uno o dos operadores es suficiente | Concentra el riesgo: cambios contractuales, salida del mercado (Coljuegos ha retirado operadores entre 2024 y 2026) o cierre del programa. | [coljuegos-15-operadores] |

## 3.3 Alternativas comparadas

Escala 1 (peor) a 5 (mejor). Valoración cualitativa del equipo, basada en la investigación; sin datos de volumen de búsqueda (las herramientas SEO de pago no estaban disponibles).

| Alternativa | Coste | Esfuerzo | Competencia | Potencial | Dificultad técnica | Riesgo regulatorio | Dependencia | Total |
|---|---|---|---|---|---|---|---|---|
| 1. Portal multilingüe único internacional | 2 | 1 | 1 | 4 | 3 | 1 | 3 | 15 |
| 2. Varios sitios por idioma/mercado | 1 | 1 | 2 | 4 | 2 | 2 | 3 | 15 |
| 3. Portal en español con expansión posterior | 4 | 4 | 2 | 3 | 4 | 3 | 3 | 23 |
| 4. Web de comparativas comerciales | 4 | 3 | 1 | 3 | 4 | 2 | 2 | 19 |
| 5. Guías informativas y análisis originales | 4 | 3 | 3 | 2 | 4 | 4 | 4 | 24 |
| **6. Híbrido: verificación oficial + guías + comparativas de licencias** | **4** | **3** | **3** | **3** | **4** | **4** | **3** | **24** |
| 7. Otros: herramienta B2B de cumplimiento para afiliados/operadores | 3 | 2 | 4 | 2 | 2 | 4 | 4 | 21 |

La alternativa 5 empata en puntuación pero no monetiza por sí sola; la 6 la incluye y añade la capa comercial legítima. La alternativa 7 (vender a otros afiliados un monitor de licencias y avisos regulatorios) es interesante como segunda línea **si** el sitio demuestra que el sistema de verificación funciona: se reserva para la fase de expansión.

# 8. Estrategia comercial seleccionada

**Modelo híbrido «verificación primero» en un único dominio en español, con subcarpetas por país** (`/co/`, `/pe/`), etiquetas `hreflang` es-CO / es-PE y expansión por subcarpetas cuando los datos lo justifiquen.

1. **Propuesta de valor:** «¿Está autorizado este casino en mi país?» respondido con el registro oficial, número de contrato o resolución, titular y fecha de verificación. Ningún competidor revisado en la búsqueda prioriza este enfoque: varias listas de «mejores casinos legales en Colombia» aparecen alojadas en secciones comerciales de medios o en subcarpetas de dominios ajenos, y al menos una mezcla operadores con licencia de Curazao (ver capítulo 4.4).
2. **Contenido:** guías de verificación por país, explicaciones de cambios normativos, señales de alerta, fichas factuales por operador y comparativas de licencias. Reseñas valorativas solo con metodología documentada y prueba real.
3. **Monetización:** enlaces de afiliado únicamente a operadores verificados manualmente, solo desde el país de la licencia (bloqueo geográfico en `/go/`), revenue share o híbrido preferente para construir ingresos recurrentes; CPA si el programa lo ofrece y se necesita caja.
4. **Diversificación:** al menos 3 programas por mercado antes de escalar contenido comercial.
5. **Lo que no se hace:** bonos, rankings pagados, páginas masivas por plantilla, mercados sin licencias, publicidad pagada (las plataformas restringen la publicidad de juego y exigen certificaciones; no se investigó en detalle y no es necesaria para validar).

**Por qué Colombia y Perú primero:** régimen online vigente con registro oficial (Coljuegos publica operador y número de contrato; el MINCETUR publica autorizaciones), operadores con programas de afiliados conocidos, idioma español, y en Perú un mercado regulado reciente (2024) con bloqueo activo de la oferta ilegal, lo que aumenta la demanda de información de verificación. México queda en prioridad 2 hasta que exista un registro público verificable o la nueva ley; España, Argentina, Brasil, Ontario, Reino Unido y EE. UU. en prioridad 3; Chile y República Dominicana excluidos por ahora.
