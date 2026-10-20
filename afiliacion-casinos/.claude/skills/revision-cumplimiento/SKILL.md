---
name: revision-cumplimiento
description: Revisa contenidos y configuraciones comerciales frente a las reglas publicitarias y de afiliación de cada mercado (Coljuegos, MINCETUR) y escala a revisión humana todo lo regulatorio. Úsala antes de que un contenido pase a revisión humana y siempre que se añada un enlace de afiliado o un mercado.
allowed-tools: Read, Grep, Glob, Write
---

# Revisión de cumplimiento y riesgos

## Lista de control por contenido
- [ ] Solo menciona operadores autorizados en el mercado del contenido.
- [ ] No promete ganancias, no presenta el juego como gratuito ni como solución económica.
- [ ] No menciona bonos o promociones (decisión editorial del MVP).
- [ ] No se dirige a menores; incluye +18 y juego responsable cuando enlaza a operadores.
- [ ] La leyenda del mercado (`config/site.yaml` → `market_notices`) es correcta y el texto peruano es el literal del reglamento.
- [ ] Enlaces comerciales con `rel="sponsored nofollow"` y a través de `/go/`.
- [ ] No hay instrucciones para eludir bloqueos, VPN o verificación de edad.

## Lista de control para enlaces de afiliado
- [ ] Contrato firmado y T&C leídos por una persona.
- [ ] Operador `verificado-humano` en el registro oficial.
- [ ] `allowed_countries` = solo el mercado de la licencia (lo genera `website/scripts/gen-go-links.mjs`).
- [ ] Países bloqueados en `config/site.yaml` (`blocked_affiliate_countries`).

## Escalamiento obligatorio a humano (y asesoría legal cuando se indique)
- Cualquier afirmación de legalidad, licencias, impuestos o condiciones contractuales.
- Entrada en un mercado nuevo (requiere asesoría local).
- Dudas sobre obligaciones del afiliado residente en República Dominicana (Ley 86-26, tributación DGII).

## Salida
`reports/revisiones/<archivo>-cumplimiento-<fecha>.md` con veredicto «APTO PARA REVISIÓN HUMANA» o «NECESITA CAMBIOS». Nunca «aprobado».
