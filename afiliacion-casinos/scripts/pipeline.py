"""Pipeline editorial asistido por la API de Claude (opcional).

Alternativa sin coste marginal de API: ejecutar las mismas fases desde Claude
Code con las skills de .claude/skills (usa la suscripción de Claude Code).
Este script sirve para la automatización desatendida (cron / n8n).

Subcomandos:
  brief     --topic "..." --market CO --slug mi-tema
  draft     --brief content/briefs/mi-tema.md [--words 900]
  translate --src content/guias/x.md --market PE
  metadata  --src content/guias/x.md
  review    --src content/guias/x.md

Opciones comunes: --dry-run (muestra prompt y coste máximo estimado, sin llamar a la API).

Ningún subcomando aprueba ni publica: el estado máximo que escribe es "draft".
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONTENT, ROOT, Doc, parse_doc, sources_index, write_doc  # noqa: E402
from llm import LLM, BudgetExceeded, RefusalError, estimate_tokens, has_credentials  # noqa: E402

PROMPTS = ROOT / "prompts"
LOCALE = {"CO": "es-CO", "PE": "es-PE", "GLOBAL": "es"}


def prompt(name: str) -> str:
    return (PROMPTS / f"{name}.md").read_text(encoding="utf-8")


def sources_for(market: str) -> str:
    rows = []
    for s in sources_index().values():
        if s["market"] in (market, "GLOBAL"):
            rows.append(f"- {s['id']}: {s['title']} — " + " | ".join(s["claims"]))
    return "\n".join(rows)


def slugify(text: str) -> str:
    text = text.lower()
    for a, b in zip("áéíóúüñ", "aeiouun"):
        text = text.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:60]


def call(llm: LLM, task: str, user: str, target: str, dry: bool, **kw) -> str | None:
    system = prompt("sistema-editorial")
    model = llm.model_for(task)
    if dry:
        max_t = kw.get("max_tokens") or llm.limits["max_output_tokens"]
        est = llm.price(model, estimate_tokens(system + user), max_t)
        print(f"[dry-run] tarea={task} modelo={model} tokens_entrada~{estimate_tokens(system + user)} "
              f"max_salida={max_t} coste_máximo~{est:.4f} USD")
        print(user[:1500] + ("…" if len(user) > 1500 else ""))
        return None
    if not has_credentials():
        raise SystemExit("Sin credenciales de API (ANTHROPIC_API_KEY). Usa --dry-run o las skills de Claude Code.")
    return llm.run(task, system, user, target=target, **kw).text


def validate_draft_body(body: str) -> list[str]:
    problems = []
    if re.search(r"^# ", body, re.M):
        problems.append("contiene H1")
    if len(body.split()) < 150:
        problems.append("demasiado corto")
    if re.search(r"ganancias? segura|\bgratis\b|sin riesgo", body.lower()):
        problems.append("expresión comercial prohibida")
    return problems


def cmd_brief(a, llm):
    user = prompt("brief").format(topic=a.topic, market=a.market, sources=sources_for(a.market))
    text = call(llm, "brief", user, a.slug, a.dry_run, max_tokens=4000)
    if text is None:
        return
    out = CONTENT / "briefs" / f"{a.slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    meta = {"topic": a.topic, "market": a.market, "slug": a.slug, "status": "research",
            "created": dt.date.today().isoformat()}
    out.write_text("---\n" + json.dumps(meta, ensure_ascii=False) + "\n---\n" + text, encoding="utf-8")
    print(f"Brief guardado en {out}")


def cmd_draft(a, llm):
    brief_text = Path(a.brief).read_text(encoding="utf-8")
    meta = json.loads(brief_text.split("---\n")[1])
    user = prompt("borrador").format(brief=brief_text, words=a.words, sources=sources_for(meta["market"]))
    body = None
    for attempt in range(llm.limits["max_iterations"]):
        body = call(llm, "draft", user, meta["slug"], a.dry_run, escalate=attempt >= 2)
        if body is None:
            return
        problems = validate_draft_body(body)
        if not problems:
            break
        print(f"Intento {attempt + 1}: {problems}; reintentando")
        user += f"\n\nCorrige estos problemas del intento anterior: {problems}"
    else:
        raise SystemExit("El borrador no superó la validación tras el máximo de iteraciones")
    cited = sorted(set(re.findall(r"\[([a-z0-9-]+)\]", body)) & set(sources_index()))
    market = meta["market"]
    prefix = "" if market == "GLOBAL" else f"/{market.lower()}"
    doc = Doc(CONTENT / "guias" / f"{meta['slug']}.md", {
        "title": meta["topic"][:70],
        "description": f"[PENDIENTE: metadatos] {meta['topic']}"[:160].ljust(50, "."),
        "permalink": f"{prefix}/guias/{meta['slug']}/",
        "type": "guia", "market": market, "lang": LOCALE[market], "status": "draft",
        "sensitive": True, "approved_by": None, "approved_date": None,
        "last_verified": dt.date.today().isoformat(), "sources": cited,
        "author": "pipeline IA (borrador)", "cost_usd": 0, "updated": dt.date.today().isoformat(),
    }, "\n" + body.strip() + "\n")
    write_doc(doc)
    print(f"Borrador guardado en {doc.path} (estado: draft)")


def cmd_translate(a, llm):
    src = parse_doc(Path(a.src))
    user = prompt("traduccion").format(
        src_lang=src.meta["lang"], src_market=src.meta["market"], dst_lang=LOCALE[a.market],
        dst_market=a.market, sources=sources_for(a.market), body=src.body)
    body = call(llm, "translation", user, src.path.stem, a.dry_run)
    if body is None:
        return
    slug = src.path.stem.split("-", 1)[-1]
    meta = dict(src.meta, market=a.market, lang=LOCALE[a.market], status="draft", approved_by=None,
                approved_date=None, author="pipeline IA (traducción)", updated=dt.date.today().isoformat(),
                permalink=f"/{a.market.lower()}/guias/{slug}/",
                translation_key=src.meta.get("translation_key") or src.path.stem)
    out = CONTENT / "guias" / f"{a.market.lower()}-{slug}.md"
    if out.exists():
        raise SystemExit(f"{out} ya existe: no se sobrescribe")
    write_doc(Doc(out, meta, "\n" + body.strip() + "\n"))
    print(f"Adaptación guardada en {out} (estado: draft)")


def cmd_metadata(a, llm):
    src = parse_doc(Path(a.src))
    text = call(llm, "metadata", prompt("metadatos").format(body=src.body[:6000]), src.path.stem,
                a.dry_run, max_tokens=500, effort="low")
    if text is None:
        return
    data = json.loads(text[text.find("{"): text.rfind("}") + 1])
    ok = len(data["title"]) <= 60 and 120 <= len(data["description"]) <= 160
    print(json.dumps(data, ensure_ascii=False, indent=2))
    if ok and a.apply:
        src.meta.update(title=data["title"], description=data["description"])
        write_doc(src)
        print("Metadatos aplicados")


def cmd_review(a, llm):
    src = parse_doc(Path(a.src))
    user = prompt("revision").format(market=src.meta["market"], sources=sources_for(src.meta["market"]),
                                     body=src.body)
    text = call(llm, "compliance", user, src.path.stem, a.dry_run, effort="high")
    if text is None:
        return
    out = ROOT / "reports" / "revisiones" / f"{src.path.stem}-{dt.date.today().isoformat()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"Informe de revisión en {out}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("brief"); b.add_argument("--topic", required=True); b.add_argument("--market", required=True, choices=["CO", "PE", "GLOBAL"]); b.add_argument("--slug")
    d = sub.add_parser("draft"); d.add_argument("--brief", required=True); d.add_argument("--words", type=int, default=900)
    t = sub.add_parser("translate"); t.add_argument("--src", required=True); t.add_argument("--market", required=True, choices=["CO", "PE"])
    m = sub.add_parser("metadata"); m.add_argument("--src", required=True); m.add_argument("--apply", action="store_true")
    r = sub.add_parser("review"); r.add_argument("--src", required=True)
    a = ap.parse_args()
    if getattr(a, "slug", None) is None and a.cmd == "brief":
        a.slug = slugify(a.topic)
    llm = LLM()
    try:
        {"brief": cmd_brief, "draft": cmd_draft, "translate": cmd_translate,
         "metadata": cmd_metadata, "review": cmd_review}[a.cmd](a, llm)
    except BudgetExceeded as e:
        print(f"PRESUPUESTO: {e}")
        return 3
    except RefusalError as e:
        print(f"RECHAZO: {e}")
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
