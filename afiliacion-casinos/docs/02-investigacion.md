# 4. Investigación de mercado

## 4.1 Método y limitaciones

- La investigación se realizó el **20-10-2026** con la herramienta de búsqueda web de la sesión. La descarga directa de páginas (WebFetch y `curl`) estaba **bloqueada** por la política de red del entorno (errores DNS y 403), salvo los registros de paquetes npm y PyPI.
- Por tanto, las afirmaciones proceden de los **fragmentos y resúmenes** que devolvía el buscador sobre páginas identificadas. Cada fuente lleva `access: snippet` en `data/sources.yaml` y debe abrirse y confirmarse antes de publicar.
- No hubo acceso a herramientas de volumen de búsqueda ni de tráfico (los conectores de Ahrefs y Similarweb no conectaron en la sesión). Las valoraciones de competencia y oportunidad SEO son **cualitativas**.
- No se ha inventado ningún dato. Donde falta, figura «desconocido», `null` o `[PENDIENTE]`.

## 4.2 Matriz de mercados

{{tabla_mercados}}

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
