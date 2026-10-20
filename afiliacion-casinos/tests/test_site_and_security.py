"""Pruebas sobre la web compilada, la configuración y la ausencia de secretos.

Requieren haber compilado antes ambas versiones (make build), si no, se omiten.
"""
import json
import re
import subprocess
from pathlib import Path

import pytest
import yaml

from check_site import check
from common import ROOT, all_docs

DIST = ROOT / "website" / "dist"
PREVIEW = ROOT / "website" / "dist-preview"
needs_build = pytest.mark.skipif(not (DIST.exists() and PREVIEW.exists()), reason="web no compilada")


@needs_build
def test_preview_has_no_seo_or_link_errors():
    res = check(PREVIEW, production=False, external=False)
    assert res["errors"] == []


@needs_build
def test_production_contains_only_approved_content():
    unpublished = [d.meta["permalink"] for d in all_docs() if d.meta["status"] != "published"]
    for permalink in unpublished:
        assert not (DIST / permalink.strip("/") / "index.html").exists(), permalink
    for html in DIST.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        assert "VISTA PREVIA INTERNA" not in text
        assert "PENDIENTE" not in text, html


@needs_build
def test_production_only_lists_human_verified_operators():
    ops = yaml.safe_load((ROOT / "data" / "operators.yaml").read_text(encoding="utf-8"))["operators"]
    for op in ops:
        page = DIST / op["market"].lower() / "operadores" / op["id"] / "index.html"
        assert page.exists() == (op["verification"]["status"] == "verificado-humano"), op["id"]


@needs_build
def test_production_errors_are_only_unapproved_legal_pages():
    res = check(DIST, production=True, external=False)
    legal = {d.meta["permalink"] for d in all_docs()}
    for e in res["errors"]:
        target = e.split("enlace interno roto ")[-1]
        assert target in legal, e


@needs_build
def test_preview_is_not_indexable_and_production_robots():
    assert "Disallow: /" in (PREVIEW / "robots.txt").read_text()
    prod = (DIST / "robots.txt").read_text()
    assert "Disallow: /go/" in prod and "Sitemap:" in prod
    assert not (PREVIEW / "sitemap-index.xml").exists()


def test_yaml_and_json_configs_parse():
    for p in list((ROOT / "config").glob("*.yaml")) + list((ROOT / "data").glob("*.yaml")):
        assert yaml.safe_load(p.read_text(encoding="utf-8")) is not None, p
    for p in (ROOT / "automation" / "n8n").glob("*.json"):
        wf = json.loads(p.read_text(encoding="utf-8"))
        assert wf["nodes"] and "connections" in wf, p
        # Los flujos exportados no deben incluir credenciales embebidas.
        assert '"credentials": {"' not in json.dumps(wf) or all(
            "id" not in str(n.get("credentials", "")) for n in wf["nodes"]), p


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---")[1])


def test_skills_and_agents_have_valid_frontmatter():
    skills = list((ROOT / ".claude" / "skills").glob("*/SKILL.md"))
    agents = list((ROOT / ".claude" / "agents").glob("*.md"))
    assert len(skills) >= 6 and len(agents) >= 6
    for s in skills:
        fm = frontmatter(s)
        assert fm["name"] == s.parent.name and len(fm["description"]) > 40, s
    for a in agents:
        fm = frontmatter(a)
        assert fm["name"] == a.stem and fm["description"], a


SECRET_PATTERNS = [r"sk-ant-[A-Za-z0-9_-]{10,}", r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
                   r"xox[baprs]-[A-Za-z0-9-]{10,}", r"ghp_[A-Za-z0-9]{30,}"]


def test_no_secrets_in_tracked_files():
    files = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout.split()
    for f in files:
        p = ROOT / f
        if p.suffix in (".png", ".pdf", ".gz") or not p.is_file():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for pat in SECRET_PATTERNS:
            assert not re.search(pat, text), f"posible secreto en {f}"
    assert ".env" not in files
