"""Copia de seguridad local de todo lo que no es reproducible.

Uso:
  python scripts/backup.py create [--dest backups] [--keep 14]
  python scripts/backup.py verify backups/backup-AAAAMMDD-HHMMSS.tar.gz
  python scripts/backup.py restore backups/backup-....tar.gz --to /ruta/destino

Incluye: content/, data/, config/, prompts/, reports/ (sin PDFs regenerables
opcionalmente), .claude/ y automation/. Excluye secretos (.env), dependencias
y builds. La copia principal es Git + remoto; este archivo cubre el caso de
pérdida del remoto o de cambios no confirmados. Guarda una copia fuera del equipo
(disco externo o almacenamiento en la nube) manualmente o con n8n.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ["content", "data", "config", "prompts", "reports", ".claude", "automation", "docs"]
EXCLUDE_NAMES = {".env", "node_modules", "dist", "dist-preview", ".venv", "__pycache__", ".cache"}


def _filter(ti: tarfile.TarInfo):
    parts = set(Path(ti.name).parts)
    if parts & EXCLUDE_NAMES or ti.name.endswith(".env"):
        return None
    return ti


def create(dest: Path, keep: int) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / f"backup-{dt.datetime.now():%Y%m%d-%H%M%S}.tar.gz"
    with tarfile.open(out, "w:gz") as tar:
        for name in INCLUDE:
            p = ROOT / name
            if p.exists():
                tar.add(p, arcname=name, filter=_filter)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    out.with_suffix(".gz.sha256").write_text(f"{digest}  {out.name}\n")
    backups = sorted(dest.glob("backup-*.tar.gz"))
    for old in backups[:-keep]:
        old.unlink()
        sha = old.with_suffix(".gz.sha256")
        if sha.exists():
            sha.unlink()
    return out


def verify(path: Path) -> bool:
    sha = path.with_suffix(".gz.sha256")
    if sha.exists() and sha.read_text().split()[0] != hashlib.sha256(path.read_bytes()).hexdigest():
        return False
    with tarfile.open(path) as tar:
        names = tar.getnames()
    return any(n.startswith("content") for n in names) and any(n.startswith("data") for n in names)


def restore(path: Path, to: Path) -> None:
    to.mkdir(parents=True, exist_ok=True)
    with tarfile.open(path) as tar:
        tar.extractall(to, filter="data")


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create"); c.add_argument("--dest", type=Path, default=ROOT / "backups"); c.add_argument("--keep", type=int, default=14)
    v = sub.add_parser("verify"); v.add_argument("path", type=Path)
    r = sub.add_parser("restore"); r.add_argument("path", type=Path); r.add_argument("--to", type=Path, required=True)
    a = ap.parse_args()
    if a.cmd == "create":
        out = create(a.dest, a.keep)
        print(f"Copia creada: {out} ({out.stat().st_size // 1024} KB)")
        return 0
    if a.cmd == "verify":
        ok = verify(a.path)
        print("Copia válida" if ok else "COPIA NO VÁLIDA")
        return 0 if ok else 1
    restore(a.path, a.to)
    print(f"Restaurado en {a.to}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
