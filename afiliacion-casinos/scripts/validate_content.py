"""Validación editorial, de cumplimiento y de datos.

Uso:  python scripts/validate_content.py [--strict]

Comprueba (sin red ni IA):
  - frontmatter completo y estados válidos;
  - flujo de aprobación (published/approved requieren aprobación humana);
  - contenido publicado sin marcadores PENDIENTE;
  - fuentes citadas existentes en data/sources.yaml;
  - permalinks únicos y no reservados;
  - frases comerciales prohibidas (promesas de ganancia, "gratis", etc.);
  - contenido casi duplicado (similitud de shingles);
  - datos de operadores y programas coherentes con las reglas de publicación;
  - páginas legales obligatorias aprobadas antes de un despliegue a producción.

Código de salida 0 si no hay errores. Las advertencias no bloquean salvo --strict.
"""
from __future__ import annotations

import argparse
import itertools
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    DATA, ROOT, RESERVED_EXACT, RESERVED_PREFIXES, STATUSES, all_docs, as_date, load_yaml,
    operators, sources_index, word_count,
)

REQUIRED = ["title", "description", "permalink", "type", "market", "lang", "status",
            "sensitive", "last_verified", "author", "updated"]
REQUIRED_LEGAL = ["/aviso-de-afiliacion/", "/privacidad/", "/cookies/", "/condiciones-de-uso/",
                  "/juego-responsable/", "/metodologia/", "/contacto/"]
# Expresiones que no pueden aparecer en contenido publicado (salvo en negación
# explícita revisada por una persona: se marca con <!-- permitido: ... -->).
BANNED = [
    r"ganancias? segura", r"dinero f[aá]cil", r"sin riesgo", r"garantizad[oa]s? (de )?gan",
    r"\bgratis\b", r"hazte rico", r"siempre ganas", r"bono (exclusivo|sin dep[oó]sito)",
]
MIN_WORDS = {"guia": 300, "noticia": 200, "comparativa": 200, "resena": 600, "legal": 80, "editorial": 40}
SIMILARITY_THRESHOLD = 0.5


def shingles(text: str, k: int = 5) -> set:
    words = re.findall(r"\w+", text.lower())
    return {" ".join(words[i:i + k]) for i in range(max(0, len(words) - k + 1))}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def validate(strict: bool = False, content_dir=None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    docs = all_docs(content_dir) if content_dir else all_docs()
    srcs = sources_index()
    seen: dict[str, str] = {}

    for d in docs:
        m = d.meta
        for key in REQUIRED:
            if key not in m or m[key] in ("", None) and key not in ("approved_by",):
                errors.append(f"{d.rel}: falta el campo '{key}'")
        status = m.get("status")
        if status not in STATUSES:
            errors.append(f"{d.rel}: estado no válido '{status}'")
        if status in ("approved", "published") and not (m.get("approved_by") and m.get("approved_date")):
            errors.append(f"{d.rel}: estado '{status}' sin aprobación humana (approved_by/approved_date)")
        pl = m.get("permalink", "")
        if not re.fullmatch(r"/([a-z0-9-]+/)*", pl or ""):
            errors.append(f"{d.rel}: permalink mal formado '{pl}'")
        if pl in RESERVED_EXACT or any(pl.startswith(p) for p in RESERVED_PREFIXES):
            errors.append(f"{d.rel}: permalink reservado por la web '{pl}'")
        if pl in seen:
            errors.append(f"{d.rel}: permalink duplicado con {seen[pl]}")
        seen[pl] = d.rel
        for sid in m.get("sources", []) or []:
            if sid not in srcs:
                errors.append(f"{d.rel}: fuente desconocida '{sid}'")
        if m.get("sensitive") and m.get("type") not in ("legal", "editorial") and not m.get("sources"):
            errors.append(f"{d.rel}: contenido sensible sin fuentes")
        if len(m.get("title", "")) > 70:
            errors.append(f"{d.rel}: título de más de 70 caracteres")
        if not 50 <= len(m.get("description", "")) <= 160:
            errors.append(f"{d.rel}: descripción fuera de 50-160 caracteres")
        if status == "published":
            if re.search(r"PENDIENTE", d.body):
                errors.append(f"{d.rel}: contenido publicado con marcadores PENDIENTE")
            if m.get("market") in ("CO", "PE") and as_date(m["last_verified"]) is None:
                errors.append(f"{d.rel}: falta last_verified")
        body_l = d.body.lower()
        for pat in BANNED:
            for hit in re.finditer(pat, body_l):
                line = body_l[max(0, hit.start() - 80):hit.end() + 80]
                if "permitido:" in line:
                    continue
                msg = f"{d.rel}: expresión comercial prohibida '{hit.group(0)}'"
                (errors if status == "published" else warnings).append(msg)
        wc = word_count(d.body)
        if wc < MIN_WORDS.get(m.get("type"), 0):
            warnings.append(f"{d.rel}: solo {wc} palabras (mínimo orientativo {MIN_WORDS[m['type']]})")

    # Duplicación
    sh = {d.rel: shingles(d.body) for d in docs}
    for a, b in itertools.combinations(sh, 2):
        s = jaccard(sh[a], sh[b])
        if s >= SIMILARITY_THRESHOLD:
            errors.append(f"contenido casi duplicado ({s:.2f}): {a} ~ {b}")

    # Páginas legales obligatorias (bloquean despliegue a producción, no el desarrollo)
    published = {d.meta.get("permalink") for d in docs if d.meta.get("status") == "published"}
    missing = [p for p in REQUIRED_LEGAL if p not in published]
    if missing:
        warnings.append("DESPLIEGUE A PRODUCCIÓN BLOQUEADO: páginas legales sin aprobar/publicar: " + ", ".join(missing))

    # Avisos obligatorios por mercado
    site = load_yaml(ROOT / "config" / "site.yaml")
    for mk in site["active_markets"]:
        if "PENDIENTE" in site["market_notices"].get(mk, "PENDIENTE"):
            warnings.append(f"MERCADO {mk} NO PUBLICABLE en producción: aviso legal obligatorio incompleto (config/site.yaml)")

    # Operadores
    seen_ops = set()
    for op in operators():
        oid = op.get("id")
        if oid in seen_ops:
            errors.append(f"operators.yaml: id duplicado {oid}")
        seen_ops.add(oid)
        v = op.get("verification", {})
        if v.get("status") not in ("verificado-humano", "fuente-oficial-indirecta", "prensa"):
            errors.append(f"operators.yaml: {oid} estado de verificación no válido")
        for sid in v.get("source_ids", []):
            if sid not in srcs:
                errors.append(f"operators.yaml: {oid} fuente desconocida {sid}")
        for key in ("official_url",):
            url = op.get(key)
            if url and not str(url).startswith("https://"):
                errors.append(f"operators.yaml: {oid} {key} debe ser https")
        aff = op.get("affiliate", {}) or {}
        if aff.get("url"):
            if v.get("status") != "verificado-humano":
                errors.append(f"operators.yaml: {oid} tiene enlace de afiliado sin verificación humana")
            if not str(aff["url"]).startswith("https://"):
                errors.append(f"operators.yaml: {oid} enlace de afiliado no https")
        if v.get("status") == "verificado-humano" and v.get("checked_by", "").startswith("agente"):
            errors.append(f"operators.yaml: {oid} marcado como verificado-humano por un agente")

    # Programas
    prog_ids = {p["id"] for p in load_yaml(DATA / "programs.yaml")["programs"]}
    for op in operators():
        pid = (op.get("affiliate") or {}).get("program_id")
        if pid and pid not in prog_ids:
            errors.append(f"operators.yaml: {op['id']} programa desconocido {pid}")

    if strict:
        errors.extend(warnings)
        warnings = []
    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="tratar advertencias como errores")
    args = ap.parse_args()
    errors, warnings = validate(args.strict)
    for w in warnings:
        print(f"ADVERTENCIA: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(f"Resultado: {len(errors)} errores, {len(warnings)} advertencias")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
