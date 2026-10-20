---
name: publicacion
description: Prepara una publicación - valida, compila, ejecuta todas las pruebas y deja el cambio listo en una rama para que una persona apruebe y despliegue. Úsala cuando un contenido esté aprobado por una persona o cuando haya que preparar un despliegue.
allowed-tools: Read, Grep, Glob, Bash(make *), Bash(python scripts/validate_content.py*), Bash(python scripts/check_site.py*), Bash(python scripts/editorial_status.py*), Bash(git status*), Bash(git diff*), Bash(git add*), Bash(git commit*)
---

# Preparación de la publicación

## Precondiciones (comprobar, no forzar)
- El contenido tiene `status: approved` o `published`, con `approved_by` de una persona. Si no, DETENTE.
- `python scripts/validate_content.py` sin errores.

## Pasos
1. `make test` (validación + build + pruebas Python/Node + accesibilidad + comprobación de enlaces).
2. Revisa que `website/dist` contiene la página y que no aparece ningún «PENDIENTE» ni el banner de vista previa.
3. `python scripts/editorial_status.py` y adjunta el resumen.
4. Crea un commit descriptivo en la rama de trabajo.
5. Informa a la persona: qué se publicará, resultado de las pruebas y el comando de despliegue (`make deploy`), que SOLO ejecuta ella.

## Prohibido
- Ejecutar `make deploy`, `wrangler pages deploy` o hacer push a la rama de producción sin autorización expresa.
- Ejecutar `scripts/approve.py`.
