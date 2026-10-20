"""Utilidades compartidas por los scripts del proyecto."""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DATA = ROOT / "data"
CONFIG = ROOT / "config"
REPORTS = ROOT / "reports"
WEBSITE = ROOT / "website"

STATUSES = ["planned", "research", "draft", "review", "approved", "published"]
# Rutas generadas por la web que el contenido Markdown no puede ocupar.
RESERVED_PREFIXES = ["/co/operadores/", "/pe/operadores/", "/go/"]
RESERVED_EXACT = {"/", "/co/", "/pe/", "/mercados/", "/fuentes/", "/404/"}


def load_yaml(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def today() -> dt.date:
    return dt.date.today()


def as_date(value) -> dt.date | None:
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value))


@dataclass
class Doc:
    path: Path
    meta: dict
    body: str

    @property
    def rel(self) -> str:
        try:
            return str(self.path.relative_to(ROOT))
        except ValueError:  # documentos fuera del proyecto (p. ej. pruebas)
            return str(self.path)


FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)


def parse_doc(path: Path) -> Doc:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER.match(text)
    if not m:
        raise ValueError(f"{path}: falta frontmatter YAML")
    return Doc(path, yaml.safe_load(m.group(1)) or {}, m.group(2))


def write_doc(doc: Doc) -> None:
    head = yaml.safe_dump(doc.meta, allow_unicode=True, sort_keys=False).strip()
    doc.path.write_text(f"---\n{head}\n---\n{doc.body}", encoding="utf-8")


def all_docs(content_dir: Path = CONTENT) -> list[Doc]:
    return [parse_doc(p) for p in sorted(content_dir.rglob("*.md"))]


def sources_index() -> dict:
    return {s["id"]: s for s in load_yaml(DATA / "sources.yaml")}


def operators() -> list[dict]:
    return load_yaml(DATA / "operators.yaml")["operators"]


def word_count(markdown: str) -> int:
    return len(re.findall(r"\w+", markdown, re.U))
