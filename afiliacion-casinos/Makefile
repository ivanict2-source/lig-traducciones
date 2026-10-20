# Juego Verificado - tareas habituales. Requiere: Python 3.11+, Node 22+, make.
PY      ?= .venv/bin/python
WEB     := website
SHELL   := /bin/bash

.PHONY: help setup build validate check test a11y maintenance backup report pdf preview deploy clean

help:
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-12s %s\n",$$1,$$2}'

setup: ## Instala dependencias (venv Python + npm)
	python3 -m venv .venv && $(PY) -m pip install -q -r requirements.txt
	cd $(WEB) && npm ci --no-audit --no-fund

validate: ## Valida contenido, datos y reglas editoriales
	$(PY) scripts/validate_content.py

build: ## Compila producción (dist) y vista previa interna (dist-preview)
	cd $(WEB) && npm run build && npm run build:preview

check: build ## Enlaces internos, SEO y metadatos de la web compilada
	mkdir -p reports/pruebas
	$(PY) scripts/check_site.py $(WEB)/dist-preview --json reports/pruebas/check_site_preview.json
	-$(PY) scripts/check_site.py $(WEB)/dist --production --json reports/pruebas/check_site_production.json

a11y: ## Auditoría de accesibilidad (axe-core + Chromium)
	cd $(WEB) && npm run test:a11y

test: validate check ## Todas las pruebas automatizadas
	$(PY) -m pytest -q tests
	cd $(WEB) && npm test
	cd $(WEB) && npm run test:a11y

maintenance: validate check ## Mantenimiento periódico (para cron/n8n)
	$(PY) scripts/editorial_status.py --days 30 > /dev/null
	@echo "Panel actualizado en reports/estado-editorial.md"

backup: ## Copia de seguridad con rotación
	$(PY) scripts/backup.py create --keep 14

report: ## Panel editorial + rendimiento y costes
	$(PY) scripts/editorial_status.py > /dev/null
	$(PY) scripts/analytics_report.py > /dev/null
	@echo "Informes en reports/"

pdf: ## Genera el informe PDF del proyecto
	$(PY) scripts/build_pdf.py

preview: build ## Sirve la vista previa en http://localhost:4321 (solo local)
	cd $(WEB) && npx astro preview --outDir dist-preview --host 127.0.0.1

deploy: ## DESPLIEGUE A PRODUCCIÓN - solo con autorización del propietario
	@$(PY) scripts/validate_content.py --strict || (echo "Validación estricta fallida: despliegue cancelado"; exit 1)
	@read -p "Vas a publicar en producción. Escribe PUBLICAR para continuar: " ans && [ "$$ans" = "PUBLICAR" ]
	cd $(WEB) && npm run build && npx wrangler@4.147.0 pages deploy dist --project-name $${CF_PAGES_PROJECT:?define CF_PAGES_PROJECT}

clean:
	rm -rf $(WEB)/dist $(WEB)/dist-preview .cache
