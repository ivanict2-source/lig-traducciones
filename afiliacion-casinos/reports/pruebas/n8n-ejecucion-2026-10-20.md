# Prueba real de los flujos n8n — 2026-10-20

Entorno: n8n 2.42.2 (npm) sobre Node.js 24.21.0, base SQLite temporal, `NODES_EXCLUDE=["n8n-nodes-base.localFileTrigger"]`,
`PROJECT_DIR` apuntando al proyecto. Sin credenciales SMTP (deliberado).

## Importación (`n8n import:workflow`)

| Flujo | Resultado |
|---|---|
| borrador-bajo-demanda | APROBADA (tras corregir: faltaba `id` de flujo — error SQLITE NOT NULL) |
| copia-seguridad-diaria | APROBADA |
| informe-mensual | APROBADA |
| mantenimiento-semanal | APROBADA |

Exportación posterior: 4 flujos; tipos de nodo: emailSend, executeCommand, if, manualTrigger, scheduleTrigger, set, stickyNote.

## Ejecución (`n8n execute --id=...`)

| Flujo | Nodo de comando | Resultado global |
|---|---|---|
| borrador-bajo-demanda | exitCode 0 (pipeline --dry-run brief) | APROBADA (rama sin error, sin correo) |
| copia-seguridad-diaria | exitCode 0 (backup creado y verificado) | APROBADA |
| mantenimiento-semanal | exitCode 0 (validación, build, comprobaciones, panel) | BLOQUEADA en el nodo de correo: "Node does not have any credentials set" (falta SMTP, esperado) |
| informe-mensual | exitCode 0 (panel e informe generados) | BLOQUEADA en el nodo de correo por falta de SMTP (esperado) |

## Defectos encontrados y corregidos gracias a la prueba

1. Los JSON no tenían `id` de flujo: la CLI de n8n no los importaba.
2. n8n 2.x bloquea `$env` en expresiones (`N8N_BLOCK_ENV_ACCESS_IN_NODE`): se sustituyó por la variable de shell `$PROJECT_DIR` y destinatarios configurables tras importar.
3. Los flujos programados no se podían probar manualmente: se añadió un disparador «Probar ahora».

Nota: n8n 2.42.2 exige Node.js >= 24 si se instala con npm; con Docker no aplica.
