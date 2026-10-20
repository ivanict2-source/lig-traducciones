"""Informe de rendimiento: Search Console + informes de los programas de afiliación + costes.

No se conecta a ninguna API: trabaja con exportaciones CSV que la persona
descarga (o que un flujo n8n autorizado deposita) en data/metrics/:

  data/metrics/gsc/*.csv          Exportación "Páginas" de Search Console
                                   columnas: page, clicks, impressions, ctr, position
  data/metrics/affiliate/*.csv    Informe normalizado por programa
                                   columnas: date, program, subid, clicks, registrations,
                                             ftd, commission_usd, status (confirmed|pending)

Reglas: los clics de afiliado NO son conversiones; solo se suman como ingresos
las comisiones con status=confirmed reportadas por el programa.

Uso: python scripts/analytics_report.py [--metrics data/metrics] [--out reports/rendimiento.md]
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, all_docs, load_yaml  # noqa: E402


def read_csvs(folder: Path) -> list[dict]:
    rows: list[dict] = []
    for f in sorted(folder.glob("*.csv")) if folder.exists() else []:
        with open(f, encoding="utf-8") as fh:
            rows.extend(csv.DictReader(fh))
    return rows


def market_of_path(path: str) -> str:
    seg = path.strip("/").split("/")[0] if path.strip("/") else ""
    return seg.upper() if seg in ("co", "pe") else "GLOBAL"


def build(metrics: Path) -> str:
    gsc = read_csvs(metrics / "gsc")
    aff = read_csvs(metrics / "affiliate")
    lines = ["# Informe de rendimiento", ""]
    if not gsc and not aff:
        lines.append("Sin datos: no hay exportaciones en data/metrics/. Nada que informar (no se estiman cifras).")
        return "\n".join(lines) + "\n"

    page_stats = defaultdict(lambda: {"clicks": 0, "impressions": 0, "pos_w": 0.0})
    for r in gsc:
        path = "/" + r["page"].split("://", 1)[-1].split("/", 1)[-1] if "://" in r["page"] else r["page"]
        s = page_stats[path]
        clicks, imp = int(r["clicks"]), int(r["impressions"])
        s["clicks"] += clicks
        s["impressions"] += imp
        s["pos_w"] += float(r["position"]) * imp
    tot_c = sum(s["clicks"] for s in page_stats.values())
    tot_i = sum(s["impressions"] for s in page_stats.values())
    lines += ["## Búsqueda orgánica (Search Console)", "",
              f"- Clics: {tot_c} · Impresiones: {tot_i} · CTR: {(tot_c / tot_i * 100 if tot_i else 0):.2f} %", "",
              "| Página | Clics | Impresiones | CTR | Posición media |", "|---|---|---|---|---|"]
    for path, s in sorted(page_stats.items(), key=lambda x: -x[1]["clicks"])[:25]:
        ctr = s["clicks"] / s["impressions"] * 100 if s["impressions"] else 0
        pos = s["pos_w"] / s["impressions"] if s["impressions"] else 0
        lines.append(f"| {path} | {s['clicks']} | {s['impressions']} | {ctr:.2f} % | {pos:.1f} |")

    by_sub = defaultdict(lambda: defaultdict(float))
    for r in aff:
        k = by_sub[r["subid"]]
        k["clicks"] += float(r["clicks"] or 0)
        k["registrations"] += float(r["registrations"] or 0)
        k["ftd"] += float(r["ftd"] or 0)
        if r["status"] == "confirmed":
            k["confirmed_usd"] += float(r["commission_usd"] or 0)
        else:
            k["pending_usd"] += float(r["commission_usd"] or 0)
    lines += ["", "## Afiliación (datos reportados por los programas)", "",
              "| sub-ID (mercado-operador) | Clics | Registros | Primeros depósitos | Comisión confirmada USD | Pendiente USD |",
              "|---|---|---|---|---|---|"]
    by_market = defaultdict(float)
    for sub, k in sorted(by_sub.items()):
        lines.append(f"| {sub} | {k['clicks']:.0f} | {k['registrations']:.0f} | {k['ftd']:.0f} | "
                     f"{k['confirmed_usd']:.2f} | {k['pending_usd']:.2f} |")
        by_market[sub.split("-")[0].upper()] += k["confirmed_usd"]
    lines += ["", "### Ingresos confirmados por mercado", ""]
    lines += [f"- {m}: {v:.2f} USD" for m, v in sorted(by_market.items())] or ["- Ninguno"]

    cfg = load_yaml(ROOT / "config" / "budget.yaml")
    ledger = ROOT / cfg["ledger"]
    ai_cost = 0.0
    if ledger.exists():
        with open(ledger, encoding="utf-8") as f:
            ai_cost = sum(float(r["cost_usd"]) for r in csv.DictReader(f))
    fixed_year = sum(c["usd_year"] for c in cfg["fixed_costs"])
    revenue = sum(by_market.values())
    published = sum(1 for d in all_docs() if d.meta.get("status") == "published")
    lines += ["", "## Costes", "", f"- IA acumulada: {ai_cost:.2f} USD",
              f"- Fijos anuales estimados: {fixed_year:.2f} USD",
              f"- Ingresos confirmados: {revenue:.2f} USD",
              f"- Coste de IA por contenido publicado: {(ai_cost / published if published else 0):.2f} USD"]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", type=Path, default=ROOT / "data" / "metrics")
    ap.add_argument("--out", type=Path, default=ROOT / "reports" / "rendimiento.md")
    a = ap.parse_args()
    md = build(a.metrics)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(md, encoding="utf-8")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
