"""Genera el informe PDF del proyecto a partir de docs/*.md y de los datos YAML.

Uso:  python scripts/build_pdf.py [--out reports/informe-proyecto.pdf] [--md reports/informe-proyecto.md]

- Cada documento de docs/ contiene capítulos con encabezado «# N. Título». Se
  ordenan por N; el capítulo 1 (portada) y el 32 (bibliografía) se generan aquí.
- Marcadores sustituidos con datos vivos: {{tabla_mercados}}, {{tabla_programas}},
  {{tabla_operadores}}, {{arbol}}, {{skills}}, {{agentes}}, {{bibliografia}}.
- Además del PDF escribe una versión Markdown editable unificada.
- Conversor Markdown mínimo: encabezados, párrafos, listas, tablas, código,
  citas, negrita, cursiva, código en línea y enlaces.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table,
                                TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DATA, ROOT, load_yaml  # noqa: E402

DOCS = ROOT / "docs"
ACCENT = colors.HexColor("#0b5cad")


# --- fuentes tipográficas -----------------------------------------------------
def register_fonts() -> tuple[str, str, str, str]:
    base = Path("/usr/share/fonts/truetype/dejavu")
    files = {"DV": "DejaVuSans.ttf", "DV-B": "DejaVuSans-Bold.ttf", "DV-I": "DejaVuSans-Oblique.ttf",
             "DVM": "DejaVuSansMono.ttf"}
    if all((base / f).exists() for f in files.values()):
        for name, f in files.items():
            pdfmetrics.registerFont(TTFont(name, str(base / f)))
        pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-B")
        return "DV", "DV-B", "DV-I", "DVM"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Courier"


FONT, BOLD, ITALIC, MONO = register_fonts()
ss = getSampleStyleSheet()
S = {
    "body": ParagraphStyle("body", parent=ss["BodyText"], fontName=FONT, fontSize=9.5, leading=13.5, spaceAfter=5),
    "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontName=BOLD, fontSize=17, leading=21, textColor=ACCENT,
                         spaceBefore=6, spaceAfter=10),
    "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontName=BOLD, fontSize=12.5, leading=16, spaceBefore=10,
                         spaceAfter=5),
    "h3": ParagraphStyle("h3", parent=ss["Heading3"], fontName=BOLD, fontSize=10.5, leading=14, spaceBefore=8,
                         spaceAfter=4),
    "cell": ParagraphStyle("cell", fontName=FONT, fontSize=7.4, leading=9.4),
    "cellh": ParagraphStyle("cellh", fontName=BOLD, fontSize=7.4, leading=9.4, textColor=colors.white),
    "code": ParagraphStyle("code", fontName=MONO, fontSize=7.4, leading=9.6, backColor=colors.HexColor("#f3f5f8"),
                           borderPadding=5, spaceBefore=4, spaceAfter=8),
    "quote": ParagraphStyle("quote", fontName=ITALIC, fontSize=9, leading=12.5, leftIndent=12,
                            textColor=colors.HexColor("#5b6370"), spaceAfter=6),
    "bullet": ParagraphStyle("bullet", fontName=FONT, fontSize=9.5, leading=13, leftIndent=14, bulletIndent=4,
                             spaceAfter=2),
    "title": ParagraphStyle("title", fontName=BOLD, fontSize=26, leading=32, alignment=TA_CENTER, textColor=ACCENT),
    "subtitle": ParagraphStyle("subtitle", fontName=FONT, fontSize=13, leading=18, alignment=TA_CENTER),
    "center": ParagraphStyle("center", fontName=FONT, fontSize=10, leading=14, alignment=TA_CENTER),
    "toc1": ParagraphStyle("toc1", fontName=FONT, fontSize=9.5, leading=13, leftIndent=10),
}


# --- Markdown -> flowables ------------------------------------------------------
def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", lambda m: f'<font face="{MONO}" size="8">{m.group(1)}</font>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<link href="\2" color="#0b5cad">\1</link>', text)
    text = re.sub(r"\[([^\]]+)\]\((/[^)]*)\)", r"\1 (\2)", text)
    return text


def table_flowable(rows: list[list[str]], width: float) -> Table:
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    lens = [max(min(len(r[i]), 60) for r in rows) + 4 for i in range(ncol)]
    floor = sum(lens) * 0.6 / ncol  # anchura mínima para que las columnas cortas no se partan letra a letra
    lens = [max(l, min(floor, 14)) for l in lens]
    total = sum(lens)
    widths = [width * l / total for l in lens]
    data = [[Paragraph(inline(c), S["cellh"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9ced6")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fb")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def md_to_flowables(md: str, width: float) -> list:
    out: list = []
    lines = md.split("\n")
    i = 0
    para: list[str] = []

    def flush():
        if para:
            out.append(Paragraph(inline(" ".join(para)), S["body"]))
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            flush()
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            out.append(Preformatted("\n".join(code), S["code"]))
        elif s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            out.append(table_flowable(rows, width))
            out.append(Spacer(1, 6))
            continue
        elif s.startswith("### "):
            flush(); out.append(Paragraph(inline(s[4:]), S["h3"]))
        elif s.startswith("## "):
            flush(); out.append(Paragraph(inline(s[3:]), S["h2"]))
        elif s.startswith("> "):
            flush(); out.append(Paragraph(inline(s[2:]), S["quote"]))
        elif re.match(r"^(\s*)[-*] ", line):
            flush()
            depth = len(re.match(r"^(\s*)", line).group(1)) // 2
            st = ParagraphStyle("b", parent=S["bullet"], leftIndent=14 + 12 * depth, bulletIndent=4 + 12 * depth)
            out.append(Paragraph(inline(re.sub(r"^\s*[-*] ", "", line)), st, bulletText="•"))
        elif re.match(r"^\s*\d+\. ", line):
            flush()
            num = re.match(r"^\s*(\d+)\.", line).group(1)
            out.append(Paragraph(inline(re.sub(r"^\s*\d+\. ", "", line)), S["bullet"], bulletText=f"{num}."))
        elif not s:
            flush()
        else:
            para.append(s)
        i += 1
    flush()
    return out


# --- contenido generado -----------------------------------------------------------
def md_table(header: list[str], rows: list[list]) -> str:
    esc = lambda v: str(v if v is not None else "—").replace("|", "/").replace("\n", " ")
    return "\n".join(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
                     + ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows])


def frontmatter(path: Path) -> dict:
    return load_yaml_text(path.read_text(encoding="utf-8").split("---")[1])


def load_yaml_text(text: str) -> dict:
    import yaml
    return yaml.safe_load(text)


def generated() -> dict[str, str]:
    markets = load_yaml(DATA / "markets.yaml")["markets"]
    programs = load_yaml(DATA / "programs.yaml")["programs"]
    ops = load_yaml(DATA / "operators.yaml")["operators"]
    sources = load_yaml(DATA / "sources.yaml")
    g = {}
    g["tabla_mercados"] = md_table(
        ["País", "Situación regulatoria", "Operadores autorizados", "Prioridad"],
        [[m["country"], m["regulatory_status"], m["authorized_operators"], m["priority"]] for m in markets]
    ) + "\n\n" + md_table(
        ["País", "Idioma", "Competencia", "Oportunidad SEO", "Dificultad", "Riesgo legal", "Monetización",
         "Fuentes oficiales/principales"],
        [[m["country"], m["language"], m["competition"], m["seo_opportunity"], m["entry_difficulty"],
          m["legal_risk"], m["monetization"], ", ".join(m["official_sources"])] for m in markets])
    g["tabla_programas"] = md_table(
        ["Programa", "Marcas / mercados", "Comisión (evidencia)", "Pago (evidencia)", "Arrastre negativo",
         "Afiliados RD", "Solicitud", "Fuentes"],
        [[p["name"], p["brands_markets"], f"{', '.join(p['commission']['models'])}: {p['commission']['rates']} ({p['commission']['evidence']})",
          f"mín. {p['payment']['min']}, {p['payment']['frequency']} ({p['payment']['evidence']})",
          f"{p['negative_carryover']['value']} ({p['negative_carryover']['evidence']})",
          p["dominican_affiliates"]["value"], p["apply_url"] or "no verificada", ", ".join(p["source_ids"])]
         for p in programs])
    g["tabla_operadores"] = md_table(
        ["Operador", "Mercado", "Licencia / contrato", "Titular", "Dominio", "Programa", "Verificación"],
        [[o["name"], o["market"], o["license_ref"], o["legal_entity"], o["official_url"], o["affiliate"]["program_id"],
          f"{o['verification']['status']} ({o['verification']['checked']})"] for o in ops])
    skills = sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md"))
    g["skills"] = md_table(["Skill", "Cuándo se usa", "Herramientas permitidas"],
                           [[f"`{frontmatter(s)['name']}`", frontmatter(s)["description"],
                             frontmatter(s).get("allowed-tools", "")] for s in skills])
    agents = sorted((ROOT / ".claude" / "agents").glob("*.md"))
    g["agentes"] = md_table(["Agente", "Modelo", "Herramientas", "Skills", "Descripción"],
                            [[f"`{frontmatter(a)['name']}`", frontmatter(a).get("model"), frontmatter(a).get("tools"),
                              ", ".join(frontmatter(a).get("skills") or []), frontmatter(a)["description"]]
                             for a in agents])
    g["arbol"] = "```\n" + tree() + "\n```"
    g["bibliografia"] = "\n".join(
        f"{i}. **{s['title']}** — {s['url']} — tipo: {s['type']}, fiabilidad: {s['reliability']}, consultada: "
        f"{s['accessed']} ({'fragmento de búsqueda' if s['access'] == 'snippet' else s['access']}). Id: `{s['id']}`"
        for i, s in enumerate(sources, 1))
    return g


def tree() -> str:
    lines = ["afiliacion-casinos/"]
    desc = {
        ".claude": "skills, subagentes y permisos de Claude Code", "automation": "flujos n8n y cron",
        "config": "marca, mercados, presupuesto y topes", "content": "contenidos Markdown (guías, legales, briefs)",
        "data": "operadores, programas, mercados, fuentes", "docs": "documentación (fuente de este PDF)",
        "prompts": "prompts del pipeline por API", "reports": "panel, pruebas, costes, PDF",
        "scripts": "validación, pipeline IA, informes, copias, PDF", "tests": "pruebas pytest",
        "website": "web Astro + Pages Function /go/ + pruebas Node",
    }
    for name in sorted(desc):
        lines.append(f"├── {name + '/':<14} {desc[name]}")
    for f in ["CLAUDE.md", "ESTADO.md", "INVENTARIO.md", "README.md", "Makefile", "requirements.txt",
              ".env.example", ".mcp.json.example"]:
        lines.append(f"├── {f}")
    return "\n".join(lines)


def chapters() -> dict[int, tuple[str, str]]:
    chs: dict[int, tuple[str, str]] = {}
    for f in sorted(DOCS.glob("*.md")):
        parts = re.split(r"^# (\d+)\. (.+)$", f.read_text(encoding="utf-8"), flags=re.M)
        for k in range(1, len(parts), 3):
            num = int(parts[k])
            if num in chs:
                raise SystemExit(f"Capítulo {num} duplicado en {f}")
            chs[num] = (parts[k + 1].strip(), parts[k + 2])
    chs[32] = ("Bibliografía con URLs y fechas de consulta", "{{bibliografia}}")
    return chs


def fill(text: str, g: dict[str, str]) -> str:
    return re.sub(r"\{\{(\w+)\}\}", lambda m: g[m.group(1)], text)


# --- documento -------------------------------------------------------------------
class Doc(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "h1":
            text = flowable.getPlainText()
            key = "c" + str(abs(hash(text)))
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=0)
            self.notify("TOCEntry", (0, text, self.page, key))


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 7.5)
    canvas.setFillColor(colors.HexColor("#5b6370"))
    canvas.drawString(2 * cm, 1.2 * cm, "Juego Verificado — Informe de investigación, diseño y construcción")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


def build(out: Path, md_out: Path) -> int:
    g = generated()
    chs = chapters()
    missing = [n for n in range(2, 33) if n not in chs]
    if missing:
        raise SystemExit(f"Faltan capítulos: {missing}")
    width = A4[0] - 4 * cm
    story: list = []
    today = dt.date.today().isoformat()
    # Portada (capítulo 1)
    story += [Spacer(1, 5 * cm), Paragraph("Juego Verificado", S["title"]), Spacer(1, 0.6 * cm),
              Paragraph("Negocio de afiliación de casinos online autorizados, operado con IA", S["subtitle"]),
              Spacer(1, 0.3 * cm),
              Paragraph("Investigación, estrategia, arquitectura, construcción, pruebas y plan de despliegue",
                        S["subtitle"]),
              Spacer(1, 2 * cm), Paragraph(f"Fecha: {today} · Mercados MVP: Colombia y Perú · Idioma: español",
                                           S["center"]),
              Spacer(1, 0.3 * cm),
              Paragraph("Documento interno para el propietario (residente en República Dominicana). "
                        "No constituye asesoramiento legal, fiscal ni financiero.", S["center"]),
              Spacer(1, 2.5 * cm)]
    legend = [["Etiqueta", "Significado"],
              ["Investigado", "Información obtenida con fuentes registradas (ver bibliografía)"],
              ["Construido", "Existe en el repositorio"], ["Probado", "Prueba ejecutada con resultado registrado"],
              ["Preparado sin desplegar", "Configurado pero no publicado"],
              ["Requiere credenciales", "Necesita cuentas o claves del propietario"],
              ["Requiere aprobación humana", "Bloqueado hasta revisión/autorización"],
              ["No verificado", "No se pudo confirmar en fuente primaria"]]
    story += [table_flowable(legend, width), PageBreak()]
    toc = TableOfContents()
    toc.levelStyles = [S["toc1"]]
    story += [Paragraph("Índice", S["h2"]), Paragraph("1. Portada", S["toc1"]), toc, PageBreak()]
    md_parts = [f"# Juego Verificado — Informe del proyecto\n\nFecha: {today}\n"]
    for num in sorted(chs):
        title, body = chs[num]
        body = fill(body, g)
        md_parts.append(f"# {num}. {title}\n{body}")
        story.append(Paragraph(f"{num}. {inline(title)}", S["h1"]))
        story += md_to_flowables(body, width)
        story.append(PageBreak() if num in (2, 3, 8, 10, 12, 18, 23, 25, 31) else Spacer(1, 12))
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = Doc(str(out), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
              bottomMargin=1.8 * cm, title="Juego Verificado - Informe del proyecto", author="Equipo del proyecto",
              subject="Afiliación de casinos online autorizados con IA")
    doc.multiBuild(story, onFirstPage=on_page, onLaterPages=on_page)
    md_out.write_text("\n\n".join(md_parts), encoding="utf-8")
    return doc.page


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "reports" / "informe-proyecto.pdf")
    ap.add_argument("--md", type=Path, default=ROOT / "reports" / "informe-proyecto.md")
    a = ap.parse_args()
    pages = build(a.out, a.md)
    data = a.out.read_bytes()
    ok = data.startswith(b"%PDF") and b"%%EOF" in data[-1024:]
    print(f"PDF: {a.out} · {pages} páginas · {len(data) // 1024} KB · estructura {'válida' if ok else 'NO VÁLIDA'}")
    print(f"Markdown editable: {a.md}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
