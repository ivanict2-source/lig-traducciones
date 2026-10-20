---
name: verificacion-fuentes
description: Verifica afirmaciones, fuentes, fechas y enlaces de un contenido o de los datos de operadores; ejecuta la validación de enlaces de la web compilada y marca lo caducado. Úsala antes de enviar un contenido a revisión humana y en el mantenimiento periódico.
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch, Bash(python scripts/*), Bash(npm run build*), Bash(make *)
---

# Verificación de fuentes y enlaces

## Procedimiento para un contenido
1. Extrae todas las afirmaciones sobre licencias, normas, fechas, cifras, pagos e impuestos.
2. Para cada una, comprueba que la fuente citada la respalda (`claims` en `data/sources.yaml`). Si `access: snippet`, intenta abrir la URL (WebFetch); si no es posible, déjalo indicado.
3. Comprueba que las fechas (`last_verified`) son de hoy si se ha revalidado.
4. Escribe el informe en `reports/revisiones/<archivo>-<fecha>.md` con la tabla: afirmación | fuente | respalda (sí/no/parcial) | acción.

## Procedimiento de enlaces (web)
```bash
make build            # compila producción y preview
python scripts/check_site.py website/dist-preview --json reports/pruebas/check_site_preview.json
python scripts/check_site.py website/dist-preview --external   # requiere red; si falla por red, estado BLOQUEADA
```

## Mantenimiento periódico
- `python scripts/editorial_status.py` lista contenido y operadores con verificación > 30 días.
- Un operador caducado debe revalidarse en el registro oficial antes de seguir mostrándose como verificado.

## Límites
- No cambies `verification.status` a `verificado-humano` ni `status` a `approved`: eso lo hace una persona con `scripts/approve.py`.
