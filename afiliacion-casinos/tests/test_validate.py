import shutil
from pathlib import Path

import pytest

from common import ROOT
from validate_content import jaccard, shingles, validate

DOC = """---
title: "Guía de prueba sobre licencias de juego"
description: "Descripción de prueba con longitud suficiente para cumplir el mínimo de cincuenta caracteres."
permalink: "{permalink}"
type: guia
market: CO
lang: es-CO
status: {status}
sensitive: true
approved_by: {approved_by}
approved_date: {approved_date}
last_verified: 2026-10-20
sources: [{sources}]
author: "test"
cost_usd: 0
updated: 2026-10-20
---
{body}
"""


def write(tmp: Path, name: str, **kw):
    defaults = dict(permalink="/co/guias/prueba/", status="review", approved_by="null", approved_date="null",
                    sources="coljuegos-operadores-online", body="Texto de prueba. " * 80)
    defaults.update(kw)
    (tmp / name).write_text(DOC.format(**defaults), encoding="utf-8")


def test_repository_content_is_valid():
    errors, _ = validate()
    assert errors == []


def test_published_without_human_approval_fails(tmp_path):
    write(tmp_path, "a.md", status="published")
    errors, _ = validate(content_dir=tmp_path)
    assert any("sin aprobación humana" in e for e in errors)


def test_published_with_pending_marker_fails(tmp_path):
    write(tmp_path, "a.md", status="published", approved_by="Ana", approved_date="2026-10-20",
          body="Dato [PENDIENTE: verificar]. " + "texto " * 400)
    errors, _ = validate(content_dir=tmp_path)
    assert any("PENDIENTE" in e for e in errors)


def test_banned_phrase_blocks_publication(tmp_path):
    write(tmp_path, "a.md", status="published", approved_by="Ana", approved_date="2026-10-20",
          body="Consigue ganancias seguras hoy. " + "texto " * 400)
    errors, _ = validate(content_dir=tmp_path)
    assert any("prohibida" in e for e in errors)


def test_unknown_source_and_reserved_permalink(tmp_path):
    write(tmp_path, "a.md", sources="fuente-inventada", permalink="/co/operadores/x/")
    errors, _ = validate(content_dir=tmp_path)
    assert any("fuente desconocida" in e for e in errors)
    assert any("reservado" in e for e in errors)


def test_duplicate_detection(tmp_path):
    body = " ".join(f"palabra{i}" for i in range(400))
    write(tmp_path, "a.md", body=body)
    write(tmp_path, "b.md", body=body, permalink="/co/guias/otra/")
    errors, _ = validate(content_dir=tmp_path)
    assert any("casi duplicado" in e for e in errors)


def test_jaccard_basic():
    assert jaccard(shingles("a b c d e f g"), shingles("a b c d e f g")) == 1.0
    assert jaccard(set(), {"x"}) == 0.0


def test_production_blocked_until_legal_pages_published():
    _, warnings = validate()
    assert any("DESPLIEGUE A PRODUCCIÓN BLOQUEADO" in w for w in warnings)
