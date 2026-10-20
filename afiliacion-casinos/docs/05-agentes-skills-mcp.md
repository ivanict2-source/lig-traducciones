# 16. Prompts de los agentes

## 16.1 Diseño del sistema de agentes

Ocho subagentes de Claude Code en `.claude/agents/`, cada uno con responsabilidad, entradas, salidas, herramientas autorizadas, límites, criterios de calidad, condiciones de escalamiento, límite de coste y prueba de funcionamiento. El rol de **agente de automatización** propuesto inicialmente no se creó: el mantenimiento de scripts lo hace la sesión principal de Claude Code y un agente extra no aportaba nada distinto (se evitan agentes redundantes).

{{agentes}}

**Flujo del supervisor:** estratega-seo (brief) → redactor (draft) → verificador + cumplimiento (informes) → si ambos son aptos, estado `review` → cola de revisión humana. Una sola iteración de corrección; si persiste el fallo, se detiene y escala. Un contenido defectuoso no bloquea a los demás.

## 16.2 Prompt de sistema del pipeline por API

El pipeline desatendido usa `prompts/sistema-editorial.md` como prompt de sistema estable (se cachea) y plantillas por tarea: `brief.md`, `borrador.md`, `traduccion.md`, `metadatos.md`, `revision.md`. Principios del prompt de sistema: veracidad (marcar PENDIENTE en lugar de inventar), citas de fuentes por id, separación hechos / operador / opinión, cumplimiento publicitario (sin promesas, gratuidad, menores ni bonos), solo mercado autorizado, estilo claro adaptado al país y utilidad real para el lector.

# 17. Skills creadas y cómo instalarlas

Formato oficial vigente consultado en la documentación de Claude Code ([claude-code-skills-docs]): `.claude/skills/<nombre>/SKILL.md` con frontmatter YAML (`name`, `description`, `allowed-tools`). Al abrir Claude Code en la carpeta `afiliacion-casinos/`, las skills del proyecto se cargan automáticamente; no requieren instalación adicional. Para usarlas en otros proyectos, copiar la carpeta a `~/.claude/skills/`.

{{skills}}

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
