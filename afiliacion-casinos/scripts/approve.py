"""Aprobación y publicación HUMANAS de contenidos.

Este es el único punto del sistema que puede pasar un contenido a `approved` o
`published`. Debe ejecutarlo una persona; los agentes de IA tienen prohibido
usarlo (ver CLAUDE.md y .claude/settings.json).

Uso:
  python scripts/approve.py approve content/guias/x.md --by "Nombre Apellido"
  python scripts/approve.py publish content/guias/x.md
  python scripts/approve.py verify-operator wplay-co --by "Nombre Apellido" [--url https://...] [--license "..."]

Requisitos para aprobar: sin marcadores PENDIENTE, validación sin errores y
confirmación interactiva (escribir "APRUEBO"), salvo --yes en entornos de prueba.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DATA, parse_doc, write_doc  # noqa: E402
from validate_content import validate  # noqa: E402


def confirm(prompt: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    return input(f"{prompt}\nEscribe APRUEBO para confirmar: ").strip() == "APRUEBO"


def approve(path: Path, by: str, assume_yes: bool) -> int:
    doc = parse_doc(path)
    if by.lower().startswith(("agente", "claude", "ia", "ai", "pipeline")):
        print("La aprobación debe registrarla una persona, no un agente.")
        return 1
    if re.search(r"PENDIENTE", doc.body) or "PENDIENTE" in str(doc.meta):
        print("No se puede aprobar: quedan marcadores PENDIENTE.")
        return 1
    if doc.meta.get("status") not in ("review", "approved"):
        print(f"Solo se aprueba contenido en 'review' (estado actual: {doc.meta.get('status')}).")
        return 1
    if not confirm(f"Vas a aprobar {path} ({doc.meta['title']}). ¿Has verificado cada fuente abriéndola?", assume_yes):
        print("Cancelado.")
        return 1
    doc.meta.update(status="approved", approved_by=by, approved_date=dt.date.today().isoformat())
    write_doc(doc)
    errors, _ = validate()
    if errors:
        print("Aprobado, pero la validación global tiene errores:\n" + "\n".join(errors))
    print(f"Aprobado por {by}.")
    return 0


def publish(path: Path) -> int:
    doc = parse_doc(path)
    if doc.meta.get("status") != "approved" or not doc.meta.get("approved_by"):
        print("Solo se publica contenido aprobado por una persona.")
        return 1
    doc.meta.update(status="published", updated=dt.date.today().isoformat())
    write_doc(doc)
    print(f"Marcado como publicado: {doc.meta['permalink']} (se desplegará en el próximo build)")
    return 0


def verify_operator(op_id: str, by: str, url: str | None, license_ref: str | None, assume_yes: bool) -> int:
    path = DATA / "operators.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    op = next((o for o in data["operators"] if o["id"] == op_id), None)
    if op is None:
        print(f"Operador {op_id} no encontrado")
        return 1
    if not confirm(f"¿Has abierto el registro oficial de {op['regulator']} y confirmado que {op['name']} figura como autorizado?", assume_yes):
        return 1
    if url:
        op["official_url"] = url
    if license_ref:
        op["license_ref"] = license_ref
    op["verification"].update(status="verificado-humano", checked=dt.date.today().isoformat(), checked_by=by)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"{op_id} verificado por {by}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("approve"); a.add_argument("path", type=Path); a.add_argument("--by", required=True); a.add_argument("--yes", action="store_true")
    p = sub.add_parser("publish"); p.add_argument("path", type=Path)
    v = sub.add_parser("verify-operator"); v.add_argument("id"); v.add_argument("--by", required=True)
    v.add_argument("--url"); v.add_argument("--license"); v.add_argument("--yes", action="store_true")
    args = ap.parse_args()
    if args.cmd == "approve":
        return approve(args.path, args.by, args.yes)
    if args.cmd == "publish":
        return publish(args.path)
    return verify_operator(args.id, args.by, args.url, args.license, args.yes)


if __name__ == "__main__":
    sys.exit(main())
