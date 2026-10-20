# Juego Verificado — Informe del proyecto

Fecha: 2026-10-20


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



# 4. Investigación de mercado


## 4.1 Método y limitaciones

- La investigación se realizó el **20-10-2026** con la herramienta de búsqueda web de la sesión. La descarga directa de páginas (WebFetch y `curl`) estaba **bloqueada** por la política de red del entorno (errores DNS y 403), salvo los registros de paquetes npm y PyPI.
- Por tanto, las afirmaciones proceden de los **fragmentos y resúmenes** que devolvía el buscador sobre páginas identificadas. Cada fuente lleva `access: snippet` en `data/sources.yaml` y debe abrirse y confirmarse antes de publicar.
- No hubo acceso a herramientas de volumen de búsqueda ni de tráfico (los conectores de Ahrefs y Similarweb no conectaron en la sesión). Las valoraciones de competencia y oportunidad SEO son **cualitativas**.
- No se ha inventado ningún dato. Donde falta, figura «desconocido», `null` o `[PENDIENTE]`.

## 4.2 Matriz de mercados

| País | Situación regulatoria | Operadores autorizados | Prioridad |
|---|---|---|---|
| Colombia | Regulado desde 2016. Operadores online con contrato de concesión de Coljuegos. Régimen publicitario (Res. 20231000019054 de 2023) parcialmente suspendido por el Consejo de Estado en junio de 2026. | 15 según Coljuegos (mayo de 2026) | 1 |
| Perú | Regulado por la Ley 31557 y el DS 005-2023-MINCETUR desde el 10-02-2024. Bloqueo activo de plataformas no autorizadas en 2026. | No verificado (cifras contradictorias en prensa: >90 licencias vs 54 casinos). | 1 |
| México | Permisos de SEGOB vinculados a permisionarios; nueva ley en preparación (sep. 2026); IEPS al 50 % desde 2026 según prensa. | Sin registro público consolidado verificado. | 2 |
| España | Regulado (Ley 13/2011, DGOJ). RD 958/2020 alcanza expresamente a afiliados; el TS anuló varios artículos en 2024. | Lista oficial DGOJ (no descargada). | 3 |
| Argentina | Mosaico provincial (~20 de 24 jurisdicciones regulan); proyecto nacional en el Senado (mayo 2026). | Por provincia. | 3 |
| Brasil | Régimen de licencias federal (Lei 14.790/2023); Portaria SPA/MF 1.231/2024 regula publicidad y afiliados. | Lista oficial SPA (no consultada). | 3 |
| Canadá (Ontario) | Regulado (AGCO / iGaming Ontario). | Registro AGCO. | 3 |
| Reino Unido | Regulado (Gambling Act 2005, UKGC). Afiliados obligados contractualmente por la LCCP y sujetos a CAP/BCAP. | Registro público UKGC. | 3 |
| Estados Unidos (estados regulados) | Estado por estado; afiliados sujetos a registro de proveedor o licencia auxiliar según modelo de comisión (p. ej. Nueva Jersey). | Por estado. | 3 |
| Chile | No regulado para juego online: proyecto de ley (Boletín 14.838-03) en tramitación; la SCJ considera no autorizada la explotación. | Ninguno online bajo licencia chilena. | X |
| República Dominicana | Nueva Ley 86-26 (oct. 2026) crea la Dirección General de Juegos de Azar e incluye juego por internet; reglamentación pendiente. | Por determinar con la nueva ley. | X |

| País | Idioma | Competencia | Oportunidad SEO | Dificultad | Riesgo legal | Monetización | Fuentes oficiales/principales |
|---|---|---|---|---|---|---|---|
| Colombia | es-CO | alta | media | media | media | Probable: varios operadores con programas de afiliados conocidos (Betsson, Codere, RushBet, Betano, bwin). Condiciones por confirmar. | coljuegos-operadores-online, coljuegos-15-operadores, coljuegos-como-ser-operador |
| Perú | es-PE | media | media-alta | media | media | Probable (RushBet, Stake y otros autorizados según prensa). Programas por confirmar. | mincetur-faq-ley-31557, mincetur-inicio-registro, ds-005-2023-mincetur, elperuano-bloqueo-2026 |
| México | es-MX | alta | media | alta | media-alta | Alta potencialmente, pero la verificación de permisos es más difícil. | mx-reforma-2026, sigma-mx-reforma |
| España | es-ES | alta | baja | alta | media | Madura y muy competida. | boe-rd-958-2020, dgoj-faq-afiliados, ts-rd958-2024 |
| Argentina | es-AR | media | media | alta | alta | Fragmentada por provincia. | canal26-argentina |
| Brasil | pt-BR | alta | media | alta | alta | Mercado grande, pero exige contrato escrito en portugués y responsabilidad compartida. | spa-portaria-1231 |
| Canadá (Ontario) | en-CA | alta | baja | alta | media | Limitada: prohibida la publicidad pública de bonos e incentivos, también por afiliados. | agco-advertising |
| Reino Unido | en-GB | alta | baja | alta | media | Madura y saturada. | harrishagan-affiliates-uk |
| Estados Unidos (estados regulados) | en-US | alta | baja | alta | alta | Alta, pero con coste de licencias por estado y competencia muy fuerte. | ifrah-nj-affiliates |
| Chile | es-CL | media | n/a | n/a | alta | No procede. | chile-proyecto-2026 |
| República Dominicana | es-DO | baja | n/a | n/a | alta | No procede hasta conocer el reglamento. | rd-ley-86-26 |

Prioridad 1 = MVP; 2 = siguiente; 3 = condicionada a datos y asesoría; X = excluido.

## 4.3 Viabilidad para un propietario residente en República Dominicana

| Aspecto | Hallazgo | Estado |
|---|---|---|
| Admisión en programas | Ningún programa publica (en lo consultado) si acepta afiliados residentes en RD. | No verificado: preguntar por escrito |
| Cobro | Los agregadores citan transferencia, Skrill, Neteller y PayPal en algunos programas. Wise anuncia envíos a cuentas bancarias dominicanas. | Parcial: confirmar métodos por programa |
| Fiscalidad | El ISR dominicano grava rentas de fuente dominicana y ciertas rentas extranjeras de inversión ([dgii-aviso-22-25]). La DGII ha considerado de fuente dominicana servicios prestados desde RD a una empresa extranjera, con criterio no uniforme ([dgii-consulta-40]). | Requiere contador: probable tributación de las comisiones |
| Regulación local | La Ley 86-26 (Gaceta Oficial 11263, 2-10-2026, según fuente secundaria) crea la Dirección General de Juegos de Azar e incluye el juego por internet ([rd-ley-86-26]). | Requiere abogado: efecto sobre promotores desconocido |
| Forma jurídica | Persona física frente a sociedad (SRL): afecta a la tributación, al KYC de los programas y a la responsabilidad. | Decisión del propietario con asesoría |

**Conclusión:** viable en principio, condicionado a (1) aceptación por los programas, (2) confirmación fiscal y (3) que la Ley 86-26 no imponga obligaciones a quien promociona operadores extranjeros desde RD sin dirigirse al mercado dominicano.

## 4.4 Análisis competitivo (cualitativo)

Observaciones a partir de las búsquedas realizadas (una por mercado; no es un estudio exhaustivo):

- **Colombia («mejores casinos online legales Colombia»):** abundan rankings de afiliados alojados en **secciones comerciales de medios** (p. ej. «Información Comercial» de un diario regional) o en **subcarpetas de dominios ajenos** sin relación temática (un dominio brasileño de oposiciones con rankings de casinos colombianos). Es el patrón que Google denomina *site reputation abuse*: ventaja temporal para ellos, pero volátil. Al menos un listado incluía un operador con licencia de Curazao entre los «legales». Los rankings mezclan bonos y requisitos de apuesta (p. ej. rollover de 35x en 7 días).
- **Perú:** los resultados están dominados por **noticias regulatorias** (Ley 31557, bloqueos del MINCETUR, nuevas licencias) y comunicados de operadores; hay poco contenido práctico y actualizado sobre cómo verificar una autorización.
- **Señales de confianza ausentes en la competencia:** fecha de verificación, número de contrato o resolución, enlace al registro oficial, separación de hechos y opinión, registro de correcciones.
- **Riesgo de competir:** los portales consolidados y los medios tienen autoridad de dominio muy superior para consultas comerciales («mejores casinos»). La estrategia evita competir de frente en esas consultas al inicio y se centra en consultas informativas de verificación, más defendibles con contenido original.
- **No se copió** contenido, marca ni datos privados de terceros.

## 4.5 Tiempos razonables

No hay datos propios ni fuentes verificables sobre plazos de indexación y conversión en este nicho; cualquier cifra sería especulativa. El plan (capítulo 12) fija **puntos de control** a 30, 90 y 180 días desde la publicación con métricas observadas, en lugar de prometer plazos.



# 5. Fuentes y referencias


El registro completo está en `data/sources.yaml` y se reproduce en la bibliografía (capítulo 32). Reglas aplicadas:

1. Prioridad: legislación y reguladores → documentación de programas → documentación de proveedores → estudios identificables → herramientas → prensa especializada.
2. Cada fuente registra título, URL, tipo, fiabilidad, mercado, fecha de consulta, modo de acceso y afirmaciones que respalda.
3. Contradicciones registradas: fecha de la sentencia del Supremo español sobre el RD 958/2020 (2 o 4 de abril de 2024); número de operadores en Colombia (tabla de 14 filas frente a boletín de 15); número de licencias en Perú (>90 frente a 54); términos de Betsson (arrastre negativo) y Betano (CPA). Se prioriza la fuente oficial y, si no la hay, se marca como pendiente.
4. La web publica las fuentes de cada página y una página pública de fuentes.



# 6. Análisis regulatorio por jurisdicción


Resumen (detalle y fuentes en la matriz y en la bibliografía). **No es asesoramiento legal.**

**Colombia.** Juegos online mediante contrato de concesión con Coljuegos (Res. 20161200025334 de 2016). Coljuegos publica la lista de operadores autorizados con número de contrato: 15 en mayo de 2026. La publicidad se rige por la Res. 20231000019054 de 2023 (alcanza a terceros que publicitan por cuenta del operador): leyenda «Autorizado por COLJUEGOS», prohibido sugerir gratuidad o prometer ganancias. En junio de 2026 el Consejo de Estado suspendió provisionalmente varias disposiciones (entre ellas, el tope del 20 % de inversión publicitaria). Implicación para el afiliado: promocionar solo concesionarios vigentes, con la leyenda y sin promesas.

**Perú.** Ley 31557 y DS 005-2023-MINCETUR (vigentes desde el 10-02-2024). El MINCETUR autoriza y registra explotadores y plataformas (vigencia de 6 años). Publicidad: solo de plataformas autorizadas, sin dirigirse a menores y con advertencia sobre la ludopatía. Bloqueo de 50 plataformas ilegales en octubre de 2026. Implicación: lista de operadores solo tras verificación en el registro y texto literal de la advertencia en cada página del mercado.

**México.** Permisos de SEGOB vinculados a permisionarios; nueva Ley de Juegos y Sorteos en preparación; IEPS del 50 % desde 2026 según prensa. Sin registro público consolidado verificado. Prioridad 2.

**España.** Ley 13/2011; DGOJ. El RD 958/2020 incluye expresamente a los afiliados; los operadores responden por la publicidad de sus afiliados y estos deben comprobar el título habilitante del anunciante. El Supremo anuló varios artículos en 2024. Mercado saturado. Prioridad 3.

**Argentina.** Regulación provincial (unas 20 de 24 jurisdicciones) y proyecto nacional. Requiere segmentación provincial. Prioridad 3.

**Brasil.** Lei 14.790/2023 y Portaria SPA/MF 1.231/2024: la actividad de los afiliados forma parte del marketing del operador; contratos escritos en portugués; sanciones a operadores y afiliados. Prioridad 3 (idioma y riesgo).

**Ontario (Canadá).** AGCO: prohibida la publicidad pública de incentivos, también por afiliados; los afiliados no pueden promocionar sitios no registrados. Prioridad 3.

**Reino Unido.** Gambling Act 2005; LCCP (SR Code 1.1.2) obliga contractualmente a los afiliados; CAP/BCAP. Saturado. Prioridad 3.

**Estados Unidos.** Estado por estado; en Nueva Jersey, registro de proveedor o licencia auxiliar del afiliado según el modelo de comisión. Prioridad 3.

**Chile.** Sin régimen de licencias online (Boletín 14.838-03 en tramitación). **Excluido**; la redirección de afiliados bloquea el tráfico chileno.

**República Dominicana.** Ley 86-26 (2026) con nuevo regulador; reglamento pendiente. **Excluido** como mercado objetivo hasta conocer el reglamento; el tráfico dominicano también se bloquea en `/go/`.


# 7. Programas de afiliación identificados


## 7.1 Estado de la verificación

Se identificaron programas reales asociados a operadores autorizados en Colombia o Perú. **Ninguna condición contractual está verificada en una fuente primaria**: los T&C oficiales no pudieron abrirse desde el entorno y las cifras proceden de agregadores de terceros (fiabilidad baja) que a menudo se contradicen. Tampoco se encontraron enlaces oficiales de solicitud verificables, por lo que `apply_url` queda en `null` en lugar de suponer una URL.

Clasificación de evidencia usada en `data/programs.yaml`: **verificado** (fuente primaria leída), **comunicado-comercial** (afirmación del propio programa), **agregador** (tercero) y **desconocido**.

| Programa | Marcas / mercados | Comisión (evidencia) | Pago (evidencia) | Arrastre negativo | Afiliados RD | Solicitud | Fuentes |
|---|---|---|---|---|---|---|---|
| Codere Partners | Codere (España, LatAm según el propio programa) | revshare, cpa, hibrido: a petición (agregador) | mín. 200 EUR, mensual (agregador) | no (agregador) | desconocido | no verificada | statsdrone-codere |
| Betsson Group Affiliates | Betsson y otras marcas del grupo (incluye Colombia según Coljuegos) | revshare, cpa, hibrido: 25-50 % RevShare (agregador) | mín. 50 EUR, mensual (agregador) | contradictorio (agregador) | desconocido | no verificada | statsdrone-betsson |
| Rush Affiliates (Rush Street Interactive) | RushBet Colombia / México (Perú no confirmado) | revshare: 25-35 % RevShare (agregador) | mín. desconocido, desconocido (desconocido) | desconocido (desconocido) | desconocido | no verificada | statsdrone-rush, rsi-rushbet-peru |
| Betano Affiliates (Kaizen Gaming) | Betano LatAm (Colombia, México, Argentina, Perú por confirmar) | revshare: 20 % RevShare (ficha LatAm); otra ficha cita 20-30 % y CPA (agregador) | mín. desconocido, mensual (agregador) | desconocido (desconocido) | desconocido | no verificada | statsdrone-betano-latam |
| Entain Partners | bwin y otras marcas de Entain | revshare: hasta 35 % RevShare (sin mercado especificado) (agregador) | mín. desconocido, desconocido (desconocido) | desconocido (desconocido) | desconocido | no verificada | affpaying-entain |
| Red Luckia | Luckia (España, Colombia) | revshare: 25-45 % RevShare (agregador) | mín. desconocido, mensual (agregador) | desconocido (desconocido) | desconocido | no verificada | statsdrone-luckia |
| bet365 Partners | bet365 (mercados aceptados contradictorios entre directorios; Colombia no confirmado) | revshare: 30 % RevShare plano (directorios) (agregador) | mín. 100-250 EUR según la fuente, mensual (agregador) | desconocido (desconocido) | desconocido | no verificada | statsdrone-bet365 |

## 7.2 Preguntas que hay que enviar por escrito a cada programa

1. ¿Aceptan afiliados (persona física o empresa) residentes en República Dominicana? ¿Qué KYC exigen?
2. ¿Qué marcas y mercados están disponibles (Colombia, Perú, México)?
3. Tipo y tasa de comisión, umbral de calificación del CPA y periodo de retención.
4. ¿Hay arrastre de saldo negativo? ¿Cuota administrativa?
5. Pago mínimo, frecuencia, métodos hacia RD y moneda.
6. Duración de la cookie o ventana de atribución y si admiten sub-ID por página.
7. Restricciones de marca (puja por marca, logotipos), creatividades aprobadas y requisitos regulatorios por país.
8. Cláusulas de terminación, inactividad y retención de comisiones.

## 7.3 Criterios de selección

1. El operador figura como autorizado en el registro oficial del mercado.
2. El programa acepta afiliados de RD y paga por un método disponible.
3. Revenue share o híbrido sin arrastre negativo, preferentemente.
4. Admite sub-ID (para atribuir conversiones por página sin cookies propias).
5. No exige prácticas contrarias a la política editorial (bonos destacados, rankings comprados).
6. Diversificación: ningún programa debería superar el 40 % de los ingresos confirmados una vez haya ingresos.

## 7.4 Operadores en la base de datos

| Operador | Mercado | Licencia / contrato | Titular | Dominio | Programa | Verificación |
|---|---|---|---|---|---|---|
| Wplay | CO | Contrato de concesión 2182 | Aquila Global Group | — | — | fuente-oficial-indirecta (2026-10-20) |
| BetPlay | CO | Contrato de concesión 1876 | Corredor Empresarial | — | — | fuente-oficial-indirecta (2026-10-20) |
| Betsson | CO | Contrato de concesión 1895 | — | — | betsson-group-affiliates | fuente-oficial-indirecta (2026-10-20) |
| Codere | CO | Contrato de concesión 2218 | — | — | codere-partners | fuente-oficial-indirecta (2026-10-20) |
| RushBet | CO | Contrato de concesión 1972 | — | — | rush-affiliates | fuente-oficial-indirecta (2026-10-20) |
| Bwin | CO | Contrato de concesión 2229 | — | — | entain-partners | fuente-oficial-indirecta (2026-10-20) |
| Stake | CO | Contrato de concesión 2226 | — | — | — | fuente-oficial-indirecta (2026-10-20) |
| Betano | CO | Contrato de concesión 2104 | — | — | betano-affiliates | fuente-oficial-indirecta (2026-10-20) |
| YaJuego | CO | Contrato de concesión 2240 | — | — | — | fuente-oficial-indirecta (2026-10-20) |
| MrYoker | CO | Contrato de concesión C2261 de 2026 (vigencia hasta 2031) | Global Vitxo S.A.S. | https://www.mryoker.co | — | fuente-oficial-indirecta (2026-10-20) |
| Luckia | CO | — | — | — | red-luckia | fuente-oficial-indirecta (2026-10-20) |
| Sportium | CO | — | — | — | — | fuente-oficial-indirecta (2026-10-20) |
| Rivalo | CO | — | — | — | — | fuente-oficial-indirecta (2026-10-20) |
| Zamba | CO | — | — | — | — | fuente-oficial-indirecta (2026-10-20) |
| Bingo Casino | CO | — | — | — | — | fuente-oficial-indirecta (2026-10-20) |
| RushBet | PE | — | — | — | rush-affiliates | prensa (2026-10-20) |
| Stake | PE | — | — | — | — | prensa (2026-10-20) |


# 8. Estrategia comercial seleccionada


**Modelo híbrido «verificación primero» en un único dominio en español, con subcarpetas por país** (`/co/`, `/pe/`), etiquetas `hreflang` es-CO / es-PE y expansión por subcarpetas cuando los datos lo justifiquen.

1. **Propuesta de valor:** «¿Está autorizado este casino en mi país?» respondido con el registro oficial, número de contrato o resolución, titular y fecha de verificación. Ningún competidor revisado en la búsqueda prioriza este enfoque: varias listas de «mejores casinos legales en Colombia» aparecen alojadas en secciones comerciales de medios o en subcarpetas de dominios ajenos, y al menos una mezcla operadores con licencia de Curazao (ver capítulo 4.4).
2. **Contenido:** guías de verificación por país, explicaciones de cambios normativos, señales de alerta, fichas factuales por operador y comparativas de licencias. Reseñas valorativas solo con metodología documentada y prueba real.
3. **Monetización:** enlaces de afiliado únicamente a operadores verificados manualmente, solo desde el país de la licencia (bloqueo geográfico en `/go/`), revenue share o híbrido preferente para construir ingresos recurrentes; CPA si el programa lo ofrece y se necesita caja.
4. **Diversificación:** al menos 3 programas por mercado antes de escalar contenido comercial.
5. **Lo que no se hace:** bonos, rankings pagados, páginas masivas por plantilla, mercados sin licencias, publicidad pagada (las plataformas restringen la publicidad de juego y exigen certificaciones; no se investigó en detalle y no es necesaria para validar).

**Por qué Colombia y Perú primero:** régimen online vigente con registro oficial (Coljuegos publica operador y número de contrato; el MINCETUR publica autorizaciones), operadores con programas de afiliados conocidos, idioma español, y en Perú un mercado regulado reciente (2024) con bloqueo activo de la oferta ilegal, lo que aumenta la demanda de información de verificación. México queda en prioridad 2 hasta que exista un registro público verificable o la nueva ley; España, Argentina, Brasil, Ontario, Reino Unido y EE. UU. en prioridad 3; Chile y República Dominicana excluidos por ahora.


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


```
afiliacion-casinos/
├── .claude/       skills, subagentes y permisos de Claude Code
├── automation/    flujos n8n y cron
├── config/        marca, mercados, presupuesto y topes
├── content/       contenidos Markdown (guías, legales, briefs)
├── data/          operadores, programas, mercados, fuentes
├── docs/          documentación (fuente de este PDF)
├── prompts/       prompts del pipeline por API
├── reports/       panel, pruebas, costes, PDF
├── scripts/       validación, pipeline IA, informes, copias, PDF
├── tests/         pruebas pytest
├── website/       web Astro + Pages Function /go/ + pruebas Node
├── CLAUDE.md
├── ESTADO.md
├── INVENTARIO.md
├── README.md
├── Makefile
├── requirements.txt
├── .env.example
├── .mcp.json.example
```



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



# 16. Prompts de los agentes


## 16.1 Diseño del sistema de agentes

Ocho subagentes de Claude Code en `.claude/agents/`, cada uno con responsabilidad, entradas, salidas, herramientas autorizadas, límites, criterios de calidad, condiciones de escalamiento, límite de coste y prueba de funcionamiento. El rol de **agente de automatización** propuesto inicialmente no se creó: el mantenimiento de scripts lo hace la sesión principal de Claude Code y un agente extra no aportaba nada distinto (se evitan agentes redundantes).

| Agente | Modelo | Herramientas | Skills | Descripción |
|---|---|---|---|---|
| `analista` | haiku | Read, Grep, Glob, Bash, Write | control-costes | Resume métricas de Search Console, programas de afiliación y costes; detecta problemas y propone experimentos. Úsalo para el informe semanal o mensual. |
| `cumplimiento` | opus | Read, Grep, Glob, Write | revision-cumplimiento | Detecta riesgos regulatorios y publicitarios y decide qué debe ir a revisión humana o legal. Úsalo antes de revisión humana y siempre que se añadan enlaces de afiliado o mercados. |
| `estratega-seo` | sonnet | WebSearch, Read, Grep, Glob, Write | investigacion-seo | Prioriza temas, define intención de búsqueda y arquitectura de contenidos, y crea briefs. Úsalo para planificar el calendario editorial o antes de redactar. |
| `investigador` | sonnet | WebSearch, WebFetch, Read, Grep, Glob, Edit, Write | investigacion-mercado | Investiga regulación, registros oficiales, operadores y programas de afiliación con fuentes verificables. Úsalo para mercados nuevos, cambios normativos o para actualizar data/*.yaml. |
| `redactor` | sonnet | Read, Grep, Glob, Write, Edit, Bash | redaccion-editorial | Redacta borradores originales a partir de briefs siguiendo el manual editorial. Úsalo cuando exista un brief listo. |
| `supervisor` | opus | Read, Grep, Glob, Bash, Agent | control-costes, publicacion | Coordina el flujo editorial completo entre agentes, aplica topes de coste e iteraciones y detiene tareas defectuosas. Úsalo para ejecutar un ciclo editorial de principio a fin. |
| `traductor` | sonnet | Read, Grep, Glob, Write, Bash | traduccion-adaptacion | Adapta contenidos a otro mercado o idioma con terminología consistente y sin trasladar contenido regulatorio. Úsalo para crear versiones por país. |
| `verificador` | opus | Read, Grep, Glob, WebSearch, WebFetch, Bash, Write | verificacion-fuentes | Comprueba afirmaciones, fuentes, fechas, enlaces y caducidad de datos. Úsalo antes de cualquier revisión humana y en el mantenimiento semanal. |

**Flujo del supervisor:** estratega-seo (brief) → redactor (draft) → verificador + cumplimiento (informes) → si ambos son aptos, estado `review` → cola de revisión humana. Una sola iteración de corrección; si persiste el fallo, se detiene y escala. Un contenido defectuoso no bloquea a los demás.

## 16.2 Prompt de sistema del pipeline por API

El pipeline desatendido usa `prompts/sistema-editorial.md` como prompt de sistema estable (se cachea) y plantillas por tarea: `brief.md`, `borrador.md`, `traduccion.md`, `metadatos.md`, `revision.md`. Principios del prompt de sistema: veracidad (marcar PENDIENTE en lugar de inventar), citas de fuentes por id, separación hechos / operador / opinión, cumplimiento publicitario (sin promesas, gratuidad, menores ni bonos), solo mercado autorizado, estilo claro adaptado al país y utilidad real para el lector.



# 17. Skills creadas y cómo instalarlas


Formato oficial vigente consultado en la documentación de Claude Code ([claude-code-skills-docs]): `.claude/skills/<nombre>/SKILL.md` con frontmatter YAML (`name`, `description`, `allowed-tools`). Al abrir Claude Code en la carpeta `afiliacion-casinos/`, las skills del proyecto se cargan automáticamente; no requieren instalación adicional. Para usarlas en otros proyectos, copiar la carpeta a `~/.claude/skills/`.

| Skill | Cuándo se usa | Herramientas permitidas |
|---|---|---|
| `control-costes` | Estima, limita y registra el coste de IA y de infraestructura del proyecto; revisa el ledger, propone el modelo más económico por tarea y detiene tareas que superan el presupuesto. Úsala antes de lanzar tareas de generación en lote y en el informe mensual. | Read, Grep, Bash(python scripts/pipeline.py --dry-run*), Bash(python scripts/editorial_status.py*), Bash(python scripts/analytics_report.py*), Edit |
| `documentacion-pdf` | Regenera la documentación del proyecto (docs/*.md) y el informe PDF profesional en reports/ con ReportLab, y verifica que el PDF existe y se abre. Úsala tras cambios relevantes en investigación, arquitectura, presupuesto o estado del proyecto. | Read, Edit, Write, Glob, Bash(python scripts/build_pdf.py*), Bash(make pdf*) |
| `investigacion-mercado` | Investiga la regulación, el registro oficial de operadores y los programas de afiliación de un mercado de juego online, y registra cada afirmación con su fuente en data/sources.yaml. Úsala al evaluar un país nuevo, al revisar cambios normativos o al actualizar operators.yaml / programs.yaml / markets.yaml. | WebSearch, WebFetch, Read, Grep, Glob, Edit, Write |
| `investigacion-seo` | Prioriza temas y crea briefs SEO (intención de búsqueda, consultas objetivo, estructura, enlaces internos, riesgos) para el sitio de casinos autorizados. Úsala antes de redactar cualquier contenido nuevo o al planificar el calendario editorial. | WebSearch, Read, Grep, Glob, Write |
| `publicacion` | Prepara una publicación - valida, compila, ejecuta todas las pruebas y deja el cambio listo en una rama para que una persona apruebe y despliegue. Úsala cuando un contenido esté aprobado por una persona o cuando haya que preparar un despliegue. | Read, Grep, Glob, Bash(make *), Bash(python scripts/validate_content.py*), Bash(python scripts/check_site.py*), Bash(python scripts/editorial_status.py*), Bash(git status*), Bash(git diff*), Bash(git add*), Bash(git commit*) |
| `redaccion-editorial` | Redacta borradores originales en español (es-CO / es-PE) a partir de un brief, siguiendo el manual de estilo y las reglas de cumplimiento, y los guarda en content/ con estado draft. Úsala cuando haya un brief aprobado para redactar. | Read, Grep, Glob, Write, Edit, Bash(python scripts/validate_content.py*) |
| `revision-cumplimiento` | Revisa contenidos y configuraciones comerciales frente a las reglas publicitarias y de afiliación de cada mercado (Coljuegos, MINCETUR) y escala a revisión humana todo lo regulatorio. Úsala antes de que un contenido pase a revisión humana y siempre que se añada un enlace de afiliado o un mercado. | Read, Grep, Glob, Write |
| `traduccion-adaptacion` | Adapta un contenido existente a otro mercado o idioma (es-CO, es-PE, más adelante en) con terminología consistente y sin trasladar literalmente el contenido regulatorio. Úsala para crear la versión de un artículo para otro país. | Read, Grep, Glob, Write, Bash(python scripts/validate_content.py*) |
| `verificacion-fuentes` | Verifica afirmaciones, fuentes, fechas y enlaces de un contenido o de los datos de operadores; ejecuta la validación de enlaces de la web compilada y marca lo caducado. Úsala antes de enviar un contenido a revisión humana y en el mantenimiento periódico. | Read, Grep, Glob, WebSearch, WebFetch, Bash(python scripts/*), Bash(npm run build*), Bash(make *) |

La validación de enlaces no tiene skill propia (sería redundante): forma parte de `verificacion-fuentes` y de `publicacion`, y la ejecutan los scripts.

**Permisos del proyecto** (`.claude/settings.json`): se permiten los scripts de validación, compilación y pruebas; se **deniegan** `scripts/approve.py`, `make deploy`, `wrangler deploy`, `git push` y la lectura de `.env`. Así, ningún agente puede aprobar, publicar ni desplegar.



# 18. MCP y conectores


## 18.1 Clasificación

| Tipo | En este proyecto |
|---|---|
| Skills (instrucciones) | 9 skills en `.claude/skills/` |
| Herramientas ejecutables | Scripts en `scripts/` y `website/scripts/`, `Makefile` |
| Servidores MCP | Ninguno instalado. Plantilla sin probar en `.mcp.json.example` |
| Conectores a servicios externos | Ninguno configurado en el proyecto |
| APIs con credenciales | API de Claude (opcional), API de Cloudflare (despliegue) |
| Integraciones con suscripción/autorización | Programas de afiliación (alta manual), Search Console (verificación del dominio) |

## 18.2 Evaluación

- **No se instaló ningún servidor MCP de terceros.** Las necesidades del MVP (leer y escribir archivos, ejecutar scripts, buscar en la web) las cubren las herramientas nativas de Claude Code. Un MCP añade superficie de ataque y credenciales sin ventaja clara.
- **Candidatos para más adelante** (evaluar procedencia, mantenimiento, permisos y licencia antes de instalar): un conector oficial de Google Search Console para automatizar la importación de métricas, y uno de Cloudflare para consultar despliegues y analítica.
- En la sesión de construcción, varios conectores de la cuenta (Ahrefs, Similarweb, Notion, Slack, entre otros) **fallaron al conectar** (error 403 del proxy). No se afirma que ningún conector funcione.
- Las credenciales siempre por variables de entorno (`.env`, no versionado); la plantilla `.env.example` no contiene secretos.


# 19. Automatizaciones


## 19.1 Qué se automatiza y cómo

| # | Proceso | Implementación | Estado |
|---|---|---|---|
| 1 | Descubrimiento de temas | Skill `investigacion-seo` + exportaciones de Search Console | Preparado (manual asistido) |
| 2 | Investigación de fuentes | Skill/agente `investigador` → `data/sources.yaml` | Construido |
| 3 | Briefs | `scripts/pipeline.py brief` o skill `investigacion-seo` | Construido (API no probada en real) |
| 4 | Borradores | `pipeline.py draft` (valida, reintenta, escala de modelo) o skill `redaccion-editorial` | Construido (API no probada en real) |
| 5 | Traducción/adaptación | `pipeline.py translate` o skill `traduccion-adaptacion` | Construido (API no probada en real) |
| 6 | Validación técnica | `scripts/validate_content.py`, `astro build` (esquema zod) | Construido y probado |
| 7 | Comprobación de enlaces | `scripts/check_site.py` (internos; externos con `--external`) | Internos probados; externos bloqueados por la red |
| 8 | Contenido caducado | `scripts/editorial_status.py --days 30` | Construido y probado |
| 9 | Informes | `editorial_status.py`, `analytics_report.py` | Construido y probado |
| 10 | Preparación de publicaciones | Skill `publicacion` + `make test` | Construido |
| 11 | Copias de seguridad | `scripts/backup.py` (rotación + SHA-256 + restauración) | Construido y probado |
| 12 | Notificación de errores | n8n (correo SMTP) o salida de cron | Preparado; requiere SMTP |
| 13 | Análisis de costes | `scripts/llm.py` (ledger) + skill `control-costes` | Construido y probado |
| 14 | Conversiones | `analytics_report.py` con CSV de los programas | Construido y probado con datos de prueba |

## 19.2 Programación recomendada: cron

`automation/cron/crontab.example`: copia diaria 02:30, mantenimiento los lunes 07:00 e informe el día 1 a las 08:00. En Windows, el Programador de tareas (preferiblemente con WSL).

## 19.3 Opción n8n (community, autoalojado)

Flujos exportados en `automation/n8n/`:

| Flujo | Nodos | Función |
|---|---|---|
| `mantenimiento-semanal.json` | Schedule → Execute Command (`make maintenance`) → IF exitCode≠0 → Email (error) / Email (resumen) | Validación, build, enlaces/SEO, caducidad |
| `copia-seguridad-diaria.json` | Schedule → Execute Command (`make backup`) → IF → Email | Copia con aviso solo si falla |
| `informe-mensual.json` | Schedule → Execute Command (`make report`) → Email | Panel editorial + rendimiento |
| `borrador-bajo-demanda.json` | Manual → Set (tema, mercado, dry_run) → Execute Command (`pipeline.py`) → IF → Email | Brief por API; *dry-run* por defecto |

**Importación:** n8n → *Workflows* → *Import from file* (o `n8n import:workflow --input=<archivo>`). Tras importar: asignar la credencial SMTP a los nodos de correo, cambiar el destinatario `CONFIGURAR-DESTINATARIO@example.com`, definir la variable de entorno `PROJECT_DIR` en el proceso de n8n, probar con el disparador «Probar ahora» y activar el flujo.

**Prueba real realizada:** los 4 flujos se importaron y ejecutaron en n8n 2.42.2 (ver `reports/pruebas/n8n-ejecucion-2026-10-20.md`). La prueba destapó y permitió corregir tres defectos: faltaba el `id` de flujo, n8n 2.x bloquea `$env` en expresiones (se usa la variable de shell `$PROJECT_DIR`) y los flujos programados no tenían disparador manual.

**Requisitos y seguridad:**
- `automation/n8n/docker-compose.yml` publica n8n **solo en 127.0.0.1**. No se expone a Internet; si algún día se necesitara acceso remoto, hacerlo mediante un túnel autenticado y con aprobación expresa.
- n8n 2.x **desactiva por defecto** los nodos Execute Command y Local File Trigger por motivos de seguridad. El compose habilita únicamente Execute Command (`NODES_EXCLUDE=["n8n-nodes-base.localFileTrigger"]`). Esto permite a n8n ejecutar comandos del sistema: por eso n8n debe quedarse en localhost y con usuario propietario protegido por contraseña.
- La imagen oficial de n8n no incluye Python ni `make`; para ejecutar los scripts dentro del contenedor hay que crear una imagen derivada o ejecutar n8n directamente en el host (`npx n8n@2.42.2`, que exige Node.js 24 o superior). Por eso cron es la opción recomendada.
- n8n 2.x bloquea por defecto el acceso a `$env` desde las expresiones; los flujos no lo usan.
- No hay credenciales en los JSON exportados (comprobado por prueba automatizada).


# 20. Configuración del sitio


## 20.1 Páginas

| Tipo | Ruta | Origen | Producción |
|---|---|---|---|
| Portada | `/` | `src/pages/index.astro` | Sí |
| Mercado | `/co/`, `/pe/` | `[market]/index.astro` + `data/markets.yaml` | Solo mercados con aviso legal completo (hoy: Colombia) |
| Comparativa de licencias | `/co/operadores/` | `[market]/operadores/index.astro` | Sí (vacía hasta verificar operadores) |
| Ficha de operador | `/co/operadores/<id>/` | `[market]/operadores/[id].astro` + `data/operators.yaml` | Solo `verificado-humano` |
| Guías y noticias | `/co/guias/...`, `/pe/guias/...`, `/guias/...` | `content/guias/*.md` | Solo `published` con aprobación humana |
| Legales y editoriales | `/aviso-de-afiliacion/`, `/privacidad/`, `/cookies/`, `/condiciones-de-uso/`, `/juego-responsable/` (incluye edad mínima), `/metodologia/`, `/correcciones/`, `/sobre-nosotros/`, `/contacto/` | `content/legal/*.md` | Tras aprobación |
| Licencias y mercados | `/mercados/` | `data/markets.yaml` | Sí |
| Fuentes | `/fuentes/` | `data/sources.yaml` | Sí |
| Redirección de afiliados | `/go/<id>/` | `functions/go/[id].js` | Solo enlaces con contrato y verificación |

Elementos en todas las páginas: franja +18 y aviso de riesgo, aviso de afiliación en el pie, enlace a juego responsable, leyenda obligatoria del mercado (Colombia: «Autorizado por COLJUEGOS…»; Perú: advertencia de ludopatía, pendiente del texto literal), fecha de verificación y fuentes en cada guía y ficha.

## 20.2 Reglas de presentación de operadores

- Fichas con tres bloques separados: **hechos verificados** (regulador, contrato/resolución, titular, dominio), **información del operador** (vacía hasta recopilarla, identificada como tal) y **valoración editorial** (vacía: no hay reseñas sin revisión documentada).
- Orden alfabético; sin bonos; sin puntuaciones.
- Enlace comercial solo si hay contrato (`/go/`, `rel="sponsored nofollow"`); sin contrato, enlace al dominio oficial (`rel="nofollow"`); sin dominio verificado, sin enlace.

## 20.3 Configuración técnica

- `config/site.yaml`: marca, mercados activos, países bloqueados para afiliación (CL, DO), leyendas por mercado.
- `SITE_URL`, `PUBLIC_CF_BEACON_TOKEN`, `PUBLIC_BUILD_MODE` (preview) por variables de entorno.
- `public/_headers`: CSP estricta, HSTS, `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy`, `Permissions-Policy`.
- `robots.txt` dinámico: la vista previa bloquea todo; producción bloquea `/go/` y publica el sitemap.
- Sitemap con `@astrojs/sitemap` (excluye `/go/`); no se genera en la vista previa.



# 21. Proceso editorial


```
planned → research → draft → review → approved → published
           (IA)       (IA)    (IA →     (PERSONA)   (PERSONA)
                              cola humana)
```

1. **Planificación:** el estratega SEO crea el brief (intención, consultas, ángulo, estructura, afirmaciones que requieren fuente).
2. **Investigación:** el investigador añade fuentes a `data/sources.yaml`.
3. **Borrador:** el redactor escribe (`status: draft`); lo no respaldado queda como `[PENDIENTE]`.
4. **Verificación y cumplimiento:** informes en `reports/revisiones/`. Si son aptos, el supervisor pasa el contenido a `review`.
5. **Revisión humana:** la persona abre cada fuente, resuelve los PENDIENTE y ejecuta `scripts/approve.py approve <archivo> --by "Nombre"` (exige escribir APRUEBO; rechaza aprobadores con nombre de agente y textos con PENDIENTE).
6. **Publicación:** `scripts/approve.py publish <archivo>` y despliegue autorizado.
7. **Actualización:** `editorial_status.py` marca como caducado lo verificado hace más de 30 días; la revalidación actualiza `last_verified`.
8. **Correcciones:** registro público en `/correcciones/`.

Campos de control por contenido: `status`, `sensitive`, `approved_by`, `approved_date`, `last_verified`, `sources`, `author`, `cost_usd`, `updated`, `translation_key`.

**Traducción:** adaptación por mercado, nunca traslado literal de normas; `translation_key` común para generar `hreflang` recíproco (comprobado por `check_site.py`).



# 22. Estrategia SEO


1. **Arquitectura:** un dominio, subcarpetas por país, enlazado interno portada → mercado → comparativa → fichas, y guías ↔ comparativa.
2. **Intención:** empezar por consultas informativas de verificación («cómo saber si un casino es legal en Perú», «Coljuegos lista de operadores», «¿está autorizado X?»), donde el contenido original con fuente oficial compite mejor que las listas comerciales; después, consultas comerciales («casinos legales Colombia»), apoyadas en la comparativa de licencias.
3. **Señales de calidad (E-E-A-T):** metodología pública, fuentes visibles, fechas de verificación, correcciones, autoría y revisión humana registradas.
4. **Contenido programático con valor:** las fichas por operador se generan desde datos, pero cada una aporta datos verificados propios (contrato, titular, fecha); no se crean páginas por plantilla sin datos (p. ej. «casino X en ciudad Y»).
5. **Técnico:** HTML estático rápido, un H1, títulos ≤ 70 caracteres, descripciones de 50-160, canonical, `hreflang`, sitemap, `noindex` en la vista previa y en `/go/`. Todo comprobado por `check_site.py`.
6. **Medición:** Search Console (impresiones, clics, CTR, posición por página) exportado a `data/metrics/gsc/`.
7. **Riesgos:** cambios de algoritmo y políticas de spam; mitigación: pocas páginas de alta utilidad, sin compra de enlaces ni dominios caducados, y diversificación futura (boletín por correo cuando haya audiencia).



# 23. Medición de conversiones


| Métrica | Fuente | Dónde |
|---|---|---|
| Visitas | Cloudflare Web Analytics (sin cookies) | Panel de Cloudflare |
| Impresiones, clics, CTR, posición | Google Search Console | `data/metrics/gsc/*.csv` → `analytics_report.py` |
| Clics de afiliación | Informes de cada programa (por sub-ID) | `data/metrics/affiliate/*.csv` |
| Registros, primeros depósitos, comisiones | Informes de cada programa | Ídem; solo `status=confirmed` cuenta como ingreso |
| Coste de herramientas e IA | `config/budget.yaml`, `reports/costes/ledger.csv` | `analytics_report.py`, `editorial_status.py` |
| Ingresos por página, mercado e idioma | Sub-ID `<mercado>-<operador>` (`/go/<id>/?src=`) | `analytics_report.py` |

Principios: un clic **no** es una conversión; solo se atribuyen ingresos reportados por el programa; no se instalan cookies propias ni píxeles de seguimiento; los datos se agregan por sub-ID, no por persona. Formato normalizado de los CSV en `scripts/analytics_report.py`.


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


# 26. Errores pendientes


| # | Elemento | Tipo | Estado | Acción |
|---|---|---|---|---|
| 1 | El build de producción tiene 73 enlaces internos rotos hacia las 9 páginas legales/editoriales aún no aprobadas | Bloqueo deliberado | PENDIENTE DE REVISIÓN HUMANA | Aprobar las páginas legales; `check_site.py --production` debe quedar en 0 |
| 2 | Perú no se publica en producción: falta el texto literal de la advertencia sobre ludopatía | Bloqueo deliberado | PENDIENTE DE REVISIÓN HUMANA | Copiar el texto del DS 005-2023-MINCETUR en `config/site.yaml` |
| 3 | Ningún operador está `verificado-humano`: las tablas de producción salen vacías | Bloqueo deliberado | PENDIENTE DE REVISIÓN HUMANA | Verificación manual en Coljuegos/MINCETUR |
| 4 | Enlaces externos sin comprobar (47 únicos) | Limitación del entorno | BLOQUEADA (red) | `python scripts/check_site.py website/dist-preview --external` en un equipo con Internet |
| 5 | Pipeline por API sin llamadas reales | Falta de credenciales | BLOQUEADA | Definir `ANTHROPIC_API_KEY` y ejecutar un brief real con tope bajo |
| 6 | Correo de alertas n8n | Falta de credenciales SMTP | BLOQUEADA | Configurar credencial SMTP en n8n |
| 7 | `senales-casino-no-autorizado.md` tiene 295 palabras (mínimo orientativo 300) | Advertencia editorial | Pendiente | Ampliar durante la revisión |
| 8 | Comprobación de tipos de Astro (`astro check`) | Herramienta no instalada | NO EJECUTADA | Opcional: instalar `@astrojs/check` y `typescript` |
| 9 | Prueba de `/go/` en el borde real de Cloudflare | Requiere despliegue | NO EJECUTADA | Probar tras el primer despliegue autorizado |



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


# 32. Bibliografía con URLs y fechas de consulta
1. **Real Decreto 958/2020, de comunicaciones comerciales de las actividades de juego (BOE-A-2020-13495)** — https://www.boe.es/buscar/act.php?id=BOE-A-2020-13495 — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `boe-rd-958-2020`
2. **DGOJ - Preguntas frecuentes / Publicidad en el juego** — https://www.ordenacionjuego.es/en/node/2151 — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `dgoj-faq-afiliados`
3. **El Tribunal Supremo anula varios artículos del Real Decreto 958/2020 (Poder Judicial)** — https://www.poderjudicial.es/cgpj/es/Poder-Judicial/Tribunal-Supremo/Noticias-Judiciales/El-Tribunal-Supremo-anula-varios-articulos-del-Real-Decreto-958-2020-de-comunicaciones-comerciales-de-las-actividades-de-juego — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `ts-rd958-2024`
4. **Operadores de Juegos Online Autorizados por Coljuegos** — https://www.coljuegos.gov.co/publicaciones/301841/juegosonline/ — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `coljuegos-operadores-online`
5. **¿Es usuario de apuestas en línea? Conozca los 15 operadores autorizados por Coljuegos** — https://www.coljuegos.gov.co/publicaciones/306824/es-usuario-de-apuestas-en-linea-conozca-los-15-operadores-autorizados-por-coljuegos/ — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `coljuegos-15-operadores`
6. **MrYoker, el nuevo operador en línea autorizado por Coljuegos** — https://www.coljuegos.gov.co/publicaciones/307328/mryoker-el-nuevo-operador-en-linea-autorizado-por-coljuegos/ — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `coljuegos-mryoker`
7. **Coljuegos - Cómo ser operador de juegos novedosos / Juegos operados por internet** — https://www.coljuegos.gov.co/publicaciones/juegos_operados_por_internet_pub — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `coljuegos-como-ser-operador`
8. **CMS - Lineamientos de publicidad en las apuestas deportivas (Colombia)** — https://cms.law/es/col/publication/lineamientos-de-publicidad-en-las-apuestas-deportivas — tipo: law-firm, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `cms-coljuegos-publicidad`
9. **El Consejo de Estado frenó límites y sanciones que impuso Coljuegos a la publicidad del juego online (Yogonet, 25-06-2026)** — https://www.yogonet.com/latinoamerica/noticias/2026/06/25/109515-el-consejo-de-estado-freno-limites-y-sanciones-que-impuso-coljuegos-a-la-publicidad-del-juego-online — tipo: trade-press, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `consejo-estado-coljuegos-2026`
10. **Colombia court suspends key advertising rules for online operators (iGaming Business)** — https://igamingbusiness.com/legal-compliance/colombia-court-suspend-key-advertising-rules-online-operators/ — tipo: trade-press, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `igb-colombia-suspension`
11. **MINCETUR - Preguntas frecuentes Ley N.º 31557** — https://apuestasdeportivas.mincetur.gob.pe/PDF/PREGUNTAS_FRECUENTES_v2.pdf — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `mincetur-faq-ley-31557`
12. **Mincetur inició el proceso de autorización y registro de solicitudes (gob.pe)** — https://www.gob.pe/institucion/mincetur/noticias/906358-mincetur-inicio-el-proceso-de-autorizacion-y-registro-de-solicitudes-vinculadas-a-la-actividad-de-juegos-y-apuestas-deportivas-a-distancia — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `mincetur-inicio-registro`
13. **Decreto Supremo N.º 005-2023-MINCETUR (texto en Congreso)** — https://www.congreso.gob.pe/Docs/DGP/DIDP/files/ds_005-2023-mincetur.pdf — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `ds-005-2023-mincetur`
14. **Garrigues - Perú aprueba el reglamento de explotación de juegos y apuestas deportivas a distancia** — https://www.garrigues.com/es_ES/noticia/peru-aprueba-reglamento-explotacion-juegos-apuestas-deportivas-distancia — tipo: law-firm, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `garrigues-peru-reglamento`
15. **Mincetur bloquea 50 plataformas de juegos a distancia que operaban sin autorización (El Peruano, 2026)** — https://elperuano.pe/noticia/305981-mincetur-bloquea-50-plataformas-de-juegos-a-distancia-y-apuestas-deportivas-que-operaban-sin-autorizacion — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `elperuano-bloqueo-2026`
16. **Cómo identificar las plataformas de juego en línea con licencia (Perú Retail)** — https://www.peru-retail.com/como-identificar-las-plataformas-de-juego-en-linea-con-licencia-para-operar-en-el-pais-el-caso-de-stake-peru/ — tipo: press, fiabilidad: baja, consultada: 2026-10-20 (fragmento de búsqueda). Id: `peru-retail-licencias`
17. **Rush Street Interactive expands Latin American footprint with launch of RushBet in Peru (MFN)** — https://mfn.se/one/a/rush-street-interactive/rush-street-interactive-expands-latin-american-footprint-with-launch-of-rushbet-in-peru-7f5df5ca — tipo: vendor, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `rsi-rushbet-peru`
18. **Stake aterriza en el mercado de Perú tras obtener la licencia (Yogonet, 2024)** — https://www.yogonet.com/latinoamerica/noticias/2024/08/20/100453-stake-aterriza-en-el-mercado-de-peru-tras-obtener-la-licencia-para-operar-casino-y-apuestas-deportivas-online — tipo: trade-press, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `yogonet-stake-peru`
19. **Así cambió la regulación de apuestas y casinos en México en 2026 (Vanguardia)** — https://www.vanguardia.com/deportes/2026/08/20/asi-cambio-la-regulacion-de-apuestas-y-casinos-en-mexico-en-2026/ — tipo: press, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `mx-reforma-2026`
20. **Reforma ley casinos México: riesgos de blanqueo (SIGMA)** — https://sigma.world/es/news/reforma-ley-casinos-mexico-riesgos-blanqueo/ — tipo: trade-press, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `sigma-mx-reforma`
21. **Portaria SPA/MF n.º 1.231/2024 (versión bilingüe, Montgomery)** — https://advennt.com/wp-content/uploads/2024/08/MONTGOMERY-Bilingual-dual-column-version-of-SPA-MF-Ordinance-No.-1231-of-31st-July-2024603317.1.pdf — tipo: law-firm, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `spa-portaria-1231`
22. **AGCO - Important Information for Advertising and Marketing in Ontario's New iGaming Market** — https://www.agco.ca/en/news/important-information-advertising-and-marketing-ontarios-new-igaming-market — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `agco-advertising`
23. **Harris Hagan - Keeping Affiliates in Line** — https://www.harrishagan.com/keeping-affiliates-in-line-no-fudging/ — tipo: law-firm, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `harrishagan-affiliates-uk`
24. **Ifrah Law - New Jersey DGE releases guidance for affiliate marketers** — https://www.ifrahlaw.com/ifrah-on-igaming/new-jersey-dge-releases-guidance-for-affiliate-marketers/ — tipo: law-firm, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `ifrah-nj-affiliates`
25. **Chile: quién podría operar apuestas online (Radio Agricultura, 13-10-2026)** — https://www.radioagricultura.cl/noticias/chile-quien-podria-operar-apuestas-online-las-condiciones-que-se-empiezan-a-discutir_20261013/ — tipo: press, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `chile-proyecto-2026`
26. **El mosaico roto: regular el juego online provincia a provincia (Canal26, 08-06-2026)** — https://www.canal26.com/general/2026/06/08/el-mosaico-roto-regular-el-juego-online-provincia-a-provincia-es-una-solucion-que-ya-nacio-vieja/ — tipo: press, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `canal26-argentina`
27. **Guía: lo que cambia para casinos, bancas y apuestas con la nueva Ley 86-26 (República Dominicana)** — https://inmobiliario.do/guia-lo-que-cambia-para-casinos-bancas-y-apuestas-con-la-nueva-ley-86-26/ — tipo: press, fiabilidad: baja, consultada: 2026-10-20 (fragmento de búsqueda). Id: `rd-ley-86-26`
28. **DGII - Aviso 22-25: criterio de territorialidad del ISR** — https://dgii.gov.do/publicacionesOficiales/avisosInformativos/Documents/2025/22-25.pdf — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `dgii-aviso-22-25`
29. **DGII - Consulta 40: renta de fuente dominicana de asalariado por una empresa extranjera** — https://dgii.gov.do/legislacion/consultas/Documents/Agosto/Consulta 40-Renta de fuente dominicana de asalariado por una empresa extranjera.pdf — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `dgii-consulta-40`
30. **Google Search Central - Spam policies for Google web search** — https://developers.google.com/search/docs/essentials/spam-policies — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `google-spam-policies`
31. **Google Search's guidance on using generative AI content on your website** — https://developers.google.com/search/docs/fundamentals/using-gen-ai-content — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `google-gen-ai-guidance`
32. **What web creators should know about our March 2024 core update and new spam policies** — https://developers.google.com/search/blog/2024/03/core-update-spam-policies — tipo: official, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `google-march-2024`
33. **Cloudflare Pages - Limits (documentación oficial, réplica en preview)** — https://developers.cloudflare.com/pages/platform/limits/ — tipo: vendor, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `cf-pages-limits`
34. **Cloudflare Web Analytics** — https://cloudflare.com/web-analytics — tipo: vendor, fiabilidad: media, consultada: 2026-10-20 (fragmento de búsqueda). Id: `cf-web-analytics`
35. **Cloudflare .COM domain pricing tracker (domainoffer.net)** — https://domainoffer.net/tld/com/cloudflare — tipo: aggregator, fiabilidad: baja, consultada: 2026-10-20 (fragmento de búsqueda). Id: `cf-registrar-com-price`
36. **n8n - Sustainable Use License FAQ** — https://docs.n8n.io/n8n-community-license/community-license/license-faq — tipo: vendor, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `n8n-license-faq`
37. **Claude Code Docs - Extend Claude with skills / Create custom subagents** — https://code.claude.com/docs/en/skills — tipo: vendor, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `claude-code-skills-docs`
38. **Anthropic Claude API - tabla de modelos y precios (referencia de la skill claude-api, caché 2026-10-06)** — https://platform.claude.com/docs/en/about-claude/pricing — tipo: vendor, fiabilidad: alta, consultada: 2026-10-20 (tool-reference). Id: `anthropic-pricing-skill`
39. **StatsDrone - Codere Partners** — https://statsdrone.com/affiliate-programs/codere-partners/ — tipo: aggregator, fiabilidad: baja, consultada: 2026-10-20 (fragmento de búsqueda). Id: `statsdrone-codere`
40. **StatsDrone / AffPapa - Betsson Group Affiliates** — https://affpapa.com/affiliate-program/betsson-group-affiliates/ — tipo: aggregator, fiabilidad: baja, consultada: 2026-10-20 (fragmento de búsqueda). Id: `statsdrone-betsson`
41. **StatsDrone - Rush Affiliates** — https://statsdrone.com/affiliate-programs/rush-affiliates — tipo: aggregator, fiabilidad: baja, consultada: 2026-10-20 (fragmento de búsqueda). Id: `statsdrone-rush`
42. **StatsDrone - Betano LatAm Affiliates** — https://statsdrone.com/affiliate-programs/betano-latam-affiliates/ — tipo: aggregator, fiabilidad: baja, consultada: 2026-10-20 (fragmento de búsqueda). Id: `statsdrone-betano-latam`
43. **StatsDrone - Red Luckia** — https://statsdrone.com/affiliate-programs/red-luckia — tipo: aggregator, fiabilidad: baja, consultada: 2026-10-20 (fragmento de búsqueda). Id: `statsdrone-luckia`
44. **StatsDrone - bet365 Partners** — https://statsdrone.com/affiliate-programs/bet365-partners — tipo: aggregator, fiabilidad: baja, consultada: 2026-10-20 (fragmento de búsqueda). Id: `statsdrone-bet365`
45. **AffPaying - Entain Partners** — https://www.affpaying.com/entainpartners — tipo: aggregator, fiabilidad: baja, consultada: 2026-10-20 (fragmento de búsqueda). Id: `affpaying-entain`
46. **n8n - 2.0 breaking changes** — https://docs.n8n.io/2-0-breaking-changes — tipo: vendor, fiabilidad: alta, consultada: 2026-10-20 (fragmento de búsqueda). Id: `n8n-2-breaking-changes`