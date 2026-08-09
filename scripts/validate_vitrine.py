#!/usr/bin/env python3
"""Validate the independent public Vitrine surface."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://ian-loc.github.io/vitrineciencia/"
REPO_URL = "https://github.com/Ian-loc/vitrineciencia"
PUBLIC_PAGES = ("index.html", "products.html", "analytics.html", "about.html")
PUBLIC_IDENTITY_FILES = (*PUBLIC_PAGES, "README.md", "CITATION.cff")
FORBIDDEN_TOKENS = (
    "Simbiotrama",
    "Simbioscópio",
    "Simbioscopio",
    "explorer.html",
    "abordagens.html",
    "Ian-loc/ScienceDataSourcesCatalog",
    "github.io/ScienceDataSourcesCatalog",
)
REQUIRED_IDS = {
    "index.html": {"conteudo", "catalogo", "hero-search", "q", "filters", "scope", "area", "brazil", "download", "programmatic", "coverage", "format", "evidence", "sort", "clear", "list", "count"},
    "products.html": {"produtos", "product-search", "product-q", "product-filters", "product-source", "product-area", "product-brazil", "product-kind", "product-format", "product-protocol", "product-auth", "product-status", "product-origin", "product-sort", "product-clear", "product-list", "product-count", "compare-bar", "compare-dialog"},
    "analytics.html": {"analise", "summary", "chart-areas", "chart-download", "chart-programmatic", "chart-brazil", "chart-evidence", "chart-formats", "chart-visualizations"},
    "about.html": {"sobre"},
}


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.tags: list[str] = []
        self.local_refs: list[str] = []
        self.external_assets: list[str] = []
        self.lang = ""
        self.viewport = False
        self.skip = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.tags.append(tag)
        if tag == "html":
            self.lang = values.get("lang") or ""
        if tag == "meta" and values.get("name") == "viewport":
            self.viewport = True
        if tag == "a" and "skip" in (values.get("class") or "").split() and (values.get("href") or "").startswith("#"):
            self.skip = True
        if values.get("id"):
            self.ids.append(values["id"] or "")
        ref = values.get("src") if tag == "script" else values.get("href") if tag in {"a", "link"} else None
        if not ref or ref.startswith(("#", "mailto:", "tel:")):
            return
        parsed = urlparse(ref)
        if parsed.scheme or parsed.netloc:
            if tag in {"script", "link"}:
                self.external_assets.append(ref)
            return
        if parsed.path and not parsed.path.endswith("/"):
            self.local_refs.append(parsed.path)


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def validate_page(filename: str) -> None:
    path = ROOT / filename
    if not path.exists():
        fail(f"página ausente: {filename}")
    content = path.read_text(encoding="utf-8")
    parser = Parser()
    parser.feed(content)
    if parser.lang != "pt-BR":
        fail(f"{filename}: lang deve ser pt-BR")
    if not parser.viewport or not parser.skip:
        fail(f"{filename}: viewport/skip-link ausente")
    if parser.tags.count("main") != 1 or parser.tags.count("h1") != 1:
        fail(f"{filename}: deve ter exatamente um main e um h1")
    if "noscript" not in parser.tags:
        fail(f"{filename}: fallback noscript ausente")
    if parser.external_assets:
        fail(f"{filename}: dependência externa não permitida: {', '.join(parser.external_assets)}")
    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        fail(f"{filename}: IDs duplicados: {', '.join(duplicates)}")
    missing = sorted(REQUIRED_IDS[filename].difference(parser.ids))
    if missing:
        fail(f"{filename}: IDs obrigatórios ausentes: {', '.join(missing)}")
    for ref in parser.local_refs:
        target = (path.parent / ref).resolve()
        if ROOT not in target.parents and target != ROOT:
            fail(f"{filename}: referência fora do repositório: {ref}")
        if not target.exists():
            fail(f"{filename}: referência local ausente: {ref}")


def validate_identity() -> None:
    for filename in PUBLIC_IDENTITY_FILES:
        content = (ROOT / filename).read_text(encoding="utf-8")
        if "Vitrine Ciência" not in content:
            fail(f"{filename}: identidade Vitrine Ciência ausente")
        found = [token for token in FORBIDDEN_TOKENS if token in content]
        if found:
            fail(f"{filename}: referência fora da fronteira pública: {', '.join(found)}")
    for filename in ("README.md", "about.html", "CITATION.cff"):
        content = (ROOT / filename).read_text(encoding="utf-8")
        if SITE_URL not in content:
            fail(f"{filename}: URL canônica da Vitrine ausente")
        if REPO_URL not in content:
            fail(f"{filename}: URL canônica do repositório ausente")


def validate_required_assets() -> None:
    required = (
        "assets/style.css", "assets/accessibility.css", "assets/brazil-scope.css", "assets/products.css",
        "assets/app.js", "assets/products.js", "assets/analytics.js", "assets/quality-summary.js", "assets/build-meta.js",
        "data/data_resources.csv", "data/data_resources.json", "data/data_products.csv", "data/data_products.json",
        "data/product_distributions.csv", "data/brazil_scope_priorities.json", "data/build-meta.json",
    )
    missing = [name for name in required if not (ROOT / name).exists() or (ROOT / name).stat().st_size == 0]
    if missing:
        fail("artefatos obrigatórios ausentes: " + ", ".join(missing))


for page in PUBLIC_PAGES:
    validate_page(page)
validate_identity()
validate_required_assets()
print("OK: Vitrine independente, navegável e sem dependências públicas do Simbiotrama")
