"""Comprobaciones sobre la web compilada (dist/ o dist-preview/).

Uso:
  python scripts/check_site.py website/dist-preview            # enlaces internos + SEO + a11y básica
  python scripts/check_site.py website/dist --production       # además: sin borradores, indexable
  python scripts/check_site.py website/dist-preview --external # lista y comprueba enlaces externos (requiere red)

Sin dependencias externas: usa html.parser de la biblioteca estándar.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict] = []
        self.meta: dict[str, str] = {}
        self.canonical: str | None = None
        self.hreflang: dict[str, str] = {}
        self.lang: str | None = None
        self.h1 = 0
        self.title = ""
        self._in_title = False
        self.imgs_without_alt = 0
        self.preview_banner = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "a" and "href" in a:
            self.links.append(a)
        elif tag == "meta" and "name" in a:
            self.meta[a["name"]] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "link" and a.get("rel") == "alternate" and "hreflang" in a:
            self.hreflang[a["hreflang"]] = a.get("href", "")
        elif tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "img" and not a.get("alt"):
            self.imgs_without_alt += 1
        elif tag == "div" and "preview-banner" in (a.get("class") or ""):
            self.preview_banner = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def page_url(dist: Path, file: Path) -> str:
    rel = file.relative_to(dist).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def resolve_internal(dist: Path, href: str) -> bool:
    path = urlparse(href).path
    if path.startswith("/go/"):
        return True  # gestionado por la Pages Function; se prueba en tests/test_go.mjs
    target = dist / path.lstrip("/")
    if path.endswith("/"):
        return (target / "index.html").exists()
    return target.exists() or (target.with_suffix(".html")).exists()


def check(dist: Path, production: bool, external: bool) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    external_links: dict[str, list[str]] = defaultdict(list)
    pages = sorted(dist.rglob("*.html"))
    parsed: dict[str, PageParser] = {}
    for f in pages:
        p = PageParser()
        p.feed(f.read_text(encoding="utf-8"))
        url = page_url(dist, f)
        parsed[url] = p
        is_404 = url == "/404.html"
        # SEO
        if not p.title.strip():
            errors.append(f"{url}: sin <title>")
        elif len(p.title) > 75:
            warnings.append(f"{url}: título largo ({len(p.title)} caracteres)")
        desc = p.meta.get("description", "")
        if not 50 <= len(desc) <= 170:
            errors.append(f"{url}: meta description fuera de rango ({len(desc)})")
        if not p.canonical and not is_404:
            errors.append(f"{url}: sin canonical")
        if p.h1 != 1:
            errors.append(f"{url}: {p.h1} etiquetas h1 (debe haber 1)")
        if not p.lang:
            errors.append(f"{url}: <html> sin atributo lang")
        if p.imgs_without_alt:
            errors.append(f"{url}: {p.imgs_without_alt} imágenes sin alt")
        robots = p.meta.get("robots", "")
        if production:
            if p.preview_banner:
                errors.append(f"{url}: banner de vista previa en build de producción")
            if "noindex" in robots and not is_404:
                errors.append(f"{url}: noindex en producción")
        elif "noindex" not in robots:
            errors.append(f"{url}: la vista previa debe ser noindex")
        # Enlaces
        for a in p.links:
            href = a["href"]
            if href.startswith(("mailto:", "#", "tel:")):
                continue
            if href.startswith("/"):
                if not resolve_internal(dist, href):
                    errors.append(f"{url}: enlace interno roto {href}")
                if href.startswith("/go/") and "sponsored" not in (a.get("rel") or ""):
                    errors.append(f"{url}: enlace de afiliado sin rel=sponsored {href}")
            elif href.startswith("http"):
                external_links[href].append(url)
                rel = a.get("rel") or ""
                if "noopener" not in rel and a.get("target") == "_blank":
                    warnings.append(f"{url}: enlace externo con target=_blank sin noopener {href}")
            else:
                warnings.append(f"{url}: enlace relativo no estándar {href}")
    # hreflang recíproco
    for url, p in parsed.items():
        for lang, href in p.hreflang.items():
            path = urlparse(href).path
            other = parsed.get(path)
            if other is None:
                errors.append(f"{url}: hreflang {lang} apunta a página inexistente {path}")
            elif not any(urlparse(h).path == url for h in other.hreflang.values()):
                errors.append(f"{url}: hreflang no recíproco con {path}")
    ext_result = {}
    if external:
        for href in sorted(external_links):
            try:
                req = urllib.request.Request(href, method="HEAD", headers={"User-Agent": "link-checker/1.0"})
                with urllib.request.urlopen(req, timeout=15) as r:
                    ext_result[href] = r.status
            except urllib.error.HTTPError as e:
                ext_result[href] = e.code
            except Exception as e:  # red bloqueada, DNS, timeout
                ext_result[href] = f"ERROR: {type(e).__name__}"
        for href, st in ext_result.items():
            if not (isinstance(st, int) and st < 400):
                warnings.append(f"externo {href}: {st}")
    return {
        "pages": len(pages),
        "errors": errors,
        "warnings": warnings,
        "external_links": sorted(external_links),
        "external_status": ext_result,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dist", type=Path)
    ap.add_argument("--production", action="store_true")
    ap.add_argument("--external", action="store_true")
    ap.add_argument("--json", type=Path, help="guardar el resultado en JSON")
    args = ap.parse_args()
    if not args.dist.exists():
        print(f"No existe {args.dist}: compila la web primero")
        return 2
    res = check(args.dist, args.production, args.external)
    for w in res["warnings"]:
        print(f"ADVERTENCIA: {w}")
    # Agrupa los enlaces rotos por destino para que el informe sea legible.
    broken: dict[str, set] = defaultdict(set)
    for e in res["errors"]:
        if "enlace interno roto" in e:
            page, target = e.split(": enlace interno roto ")
            broken[target].add(page)
        else:
            print(f"ERROR: {e}")
    for target, pages in sorted(broken.items()):
        print(f"ERROR: enlace interno roto {target} (en {len(pages)} páginas)")
    print(f"Páginas: {res['pages']} · enlaces externos únicos: {len(res['external_links'])} · "
          f"errores: {len(res['errors'])} · advertencias: {len(res['warnings'])}")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
