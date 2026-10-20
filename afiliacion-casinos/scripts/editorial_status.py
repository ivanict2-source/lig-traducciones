"""Panel editorial en Markdown (sustituye a un CMS en la primera versión).

Uso:  python scripts/editorial_status.py [--days 30] [--out reports/estado-editorial.md]

Genera un informe con:
  - contenidos por estado (planned ... published);
  - pendientes de revisión humana y contenido sensible;
  - contenido y operadores con verificación caducada (> N días);
  - marcadores PENDIENTE abiertos;
  - coste acumulado de IA (ledger) y por contenido;
  - resultado de la última comprobación de la web, si existe.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import REPORTS, ROOT, STATUSES, all_docs, as_date, load_yaml, operators, today  # noqa: E402


def stale_items(days: int) -> tuple[list[str], list[str]]:
    t = today()
    docs = [f"{d.rel} (verificado {as_date(d.meta['last_verified'])})" for d in all_docs()
            if d.meta.get("market") != "GLOBAL" or d.meta.get("sensitive")
            if (t - as_date(d.meta["last_verified"])).days > days]
    ops = [f"{o['id']} (comprobado {as_date(o['verification']['checked'])})" for o in operators()
           if (t - as_date(o["verification"]["checked"])).days > days]
    return docs, ops


def ledger_totals() -> tuple[float, Counter]:
    cfg = load_yaml(ROOT / "config" / "budget.yaml")
    path = ROOT / cfg["ledger"]
    per_doc: Counter = Counter()
    total = 0.0
    if path.exists():
        with open(path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cost = float(row["cost_usd"])
                total += cost
                per_doc[row.get("target", "")] += cost
    return total, per_doc


def build(days: int) -> str:
    docs = all_docs()
    by_status = Counter(d.meta.get("status") for d in docs)
    stale_docs, stale_ops = stale_items(days)
    total, per_doc = ledger_totals()
    lines = [f"# Estado editorial — {today().isoformat()}", ""]
    lines += ["## Contenidos por estado", "", "| Estado | Nº |", "|---|---|"]
    lines += [f"| {s} | {by_status.get(s, 0)} |" for s in STATUSES]
    lines += ["", "## Pendientes de revisión humana", ""]
    pend = [d for d in docs if d.meta.get("status") in ("draft", "review")]
    lines += [f"- [{d.meta['status']}] {'**SENSIBLE** ' if d.meta.get('sensitive') else ''}"
              f"`{d.rel}` → {d.meta['permalink']}" for d in pend] or ["- Ninguno"]
    lines += ["", f"## Verificación caducada (> {days} días)", ""]
    lines += [f"- Contenido: {x}" for x in stale_docs] + [f"- Operador: {x}" for x in stale_ops] or ["- Nada caducado"]
    lines += ["", "## Marcadores PENDIENTE abiertos", ""]
    for d in docs:
        n = len(re.findall(r"PENDIENTE", d.body))
        if n:
            lines.append(f"- `{d.rel}`: {n}")
    ops = operators()
    vs = Counter(o["verification"]["status"] for o in ops)
    lines += ["", "## Operadores", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(vs.items())]
    lines += [f"- Con enlace de afiliado activo: {sum(1 for o in ops if (o.get('affiliate') or {}).get('url'))}"]
    lines += ["", "## Coste de IA (ledger)", "", f"- Total acumulado: {total:.4f} USD"]
    lines += [f"- {k or '(sin destino)'}: {v:.4f} USD" for k, v in per_doc.most_common(10)]
    site_json = REPORTS / "pruebas" / "check_site_preview.json"
    if site_json.exists():
        r = json.loads(site_json.read_text(encoding="utf-8"))
        lines += ["", "## Última comprobación de la web (preview)", "",
                  f"- Páginas: {r['pages']} · errores: {len(r['errors'])} · advertencias: {len(r['warnings'])}"]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--out", type=Path, default=REPORTS / "estado-editorial.md")
    args = ap.parse_args()
    md = build(args.days)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(md, encoding="utf-8")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
