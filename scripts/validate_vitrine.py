#!/usr/bin/env python3
"""Validate the independent, user-facing Vitrine surface."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://ian-loc.github.io/vitrineciencia/"
REPO_URL = "https://github.com/Ian-loc/vitrineciencia"
PUBLIC_PAGES = ("index.html", "products.html", "sources.html", "analytics.html", "about.html")
INTERACTIVE_PAGES = {"products.html", "sources.html", "analytics.html"}
PUBLIC_RENDER_FILES = (
    *PUBLIC_PAGES,
    "assets/app.js",
    "assets/products.js",
    "assets/product-ux-v2.js",
    "assets/home.js",
    "assets/navigation.js",
)
IDENTITY_FILES = (*PUBLIC_PAGES, "README.md", "CITATION.cff")
CANONICAL_URLS = {
    "index.html": SITE_URL,
    "products.html": SITE_URL + "products.html",
    "sources.html": SITE_URL + "sources.html",
    "analytics.html": SITE_URL + "analytics.html",
    "about.html": SITE_URL + "about.html",
}
FORBIDDEN_PAGE_TOKENS = (
    "Simbiotrama",
    "Simbioscópio",
    "Simbioscopio",
    "explorer.html",
    "abordagens.html",
    "Ian-loc/ScienceDataSourcesCatalog",
    "github.io/ScienceDataSourcesCatalog",
)
FORBIDDEN_PUBLIC_COPY = (
    "Transparência de qualidade",
    "Cobertura e estado dos metadados",
    "no piloto",
    "Escopo de enumeração",
    "Identificador interno",
    "Avaliação e governança",
    "data-build-meta",
    "Build:",
    "P0 —",
    "P1 —",
    "P2 —",
    "P3 —",
)
REQUIRED_IDS = {
    "index.html": {"conteudo", "home-q", "home-products", "home-sources", "home-access"},
    "products.html": {
        "produtos", "product-search", "product-q", "product-filters", "product-area",
        "product-coverage", "product-year-start", "product-year-end", "product-temporal",
        "product-spatial-support", "product-spatial-resolution", "product-access", "product-format",
        "product-free", "product-source", "product-brazil", "product-kind", "product-license",
        "product-protocol", "product-auth", "product-status", "product-origin", "product-sort",
        "product-clear", "product-list", "product-count", "product-results-more", "product-show-more",
        "product-shown-count", "compare-bar", "compare-dialog", "query-interpretation"
    },
    "sources.html": {
        "conteudo", "catalogo", "hero-search", "q", "filters", "scope", "area", "brazil",
        "download", "programmatic", "coverage", "format", "evidence", "sort", "clear", "list",
        "count", "results-more", "show-more", "shown-count"
    },
    "analytics.html": {"analise", "summary", "chart-areas", "chart-download", "chart-programmatic", "chart-brazil", "chart-evidence", "chart-formats", "chart-visualizations"},
    "about.html": {"sobre", "o-que-e", "como-organizamos", "verificacao", "antes-de-usar", "citacao"},
}


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.tags: list[str] = []
        self.local_refs: list[str] = []
        self.external_assets: list[str] = []
        self.canonical_urls: list[str] = []
        self.og_urls: list[str] = []
        self.lang = ""
        self.viewport = False
        self.skip = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.tags.append(tag)
        rel_tokens = (values.get("rel") or "").split()
        if tag == "html":
            self.lang = values.get("lang") or ""
        if tag == "meta" and values.get("name") == "viewport":
            self.viewport = True
        if tag == "meta" and values.get("property") == "og:url" and values.get("content"):
            self.og_urls.append(values["content"] or "")
        if tag == "link" and "canonical" in rel_tokens and values.get("href"):
            self.canonical_urls.append(values["href"] or "")
        if tag == "a" and "skip" in (values.get("class") or "").split() and (values.get("href") or "").startswith("#"):
            self.skip = True
        if values.get("id"):
            self.ids.append(values["id"] or "")
        ref = values.get("src") if tag == "script" else values.get("href") if tag in {"a", "link"} else None
        if not ref or ref.startswith(("#", "mailto:", "tel:")):
            return
        parsed = urlparse(ref)
        if parsed.scheme or parsed.netloc:
            if tag == "script" or (tag == "link" and "stylesheet" in rel_tokens):
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
    if filename in INTERACTIVE_PAGES and "noscript" not in parser.tags:
        fail(f"{filename}: fallback noscript ausente para página interativa")
    if parser.external_assets:
        fail(f"{filename}: dependência externa não permitida: {', '.join(parser.external_assets)}")
    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        fail(f"{filename}: IDs duplicados: {', '.join(duplicates)}")
    missing = sorted(REQUIRED_IDS[filename].difference(parser.ids))
    if missing:
        fail(f"{filename}: IDs obrigatórios ausentes: {', '.join(missing)}")
    if "assets/visual-refinement.css" not in content or "assets/ux-v2.css" not in content:
        fail(f"{filename}: camadas visuais públicas obrigatórias ausentes")
    expected_url = CANONICAL_URLS[filename]
    if parser.canonical_urls != [expected_url]:
        fail(f"{filename}: canonical deve ser único e igual a {expected_url}")
    if parser.og_urls != [expected_url]:
        fail(f"{filename}: og:url deve ser único e igual ao canonical")
    if '<meta name="twitter:card" content="summary">' not in content:
        fail(f"{filename}: twitter:card ausente")
    if filename == "index.html":
        if '"@type":"DataCatalog"' not in content or '"@context":"https://schema.org"' not in content:
            fail("index.html: metadados estruturados DataCatalog ausentes")
        if 'https://orcid.org/0000-0003-1164-9318' not in content:
            fail("index.html: ORCID do criador ausente dos metadados estruturados")
        if 'action="products.html"' not in content:
            fail("index.html: busca principal deve encaminhar à descoberta de produtos")
    for ref in parser.local_refs:
        target = (path.parent / ref).resolve()
        if ROOT not in target.parents and target != ROOT:
            fail(f"{filename}: referência fora do repositório: {ref}")
        if not target.exists():
            fail(f"{filename}: referência local ausente: {ref}")


def validate_identity() -> None:
    for filename in IDENTITY_FILES:
        content = (ROOT / filename).read_text(encoding="utf-8")
        if "Vitrine Ciência" not in content:
            fail(f"{filename}: identidade Vitrine Ciência ausente")
    for filename in PUBLIC_PAGES:
        content = (ROOT / filename).read_text(encoding="utf-8")
        found = [token for token in FORBIDDEN_PAGE_TOKENS if token in content]
        if found:
            fail(f"{filename}: referência fora da fronteira pública: {', '.join(found)}")
    for filename in ("README.md", "about.html", "CITATION.cff"):
        content = (ROOT / filename).read_text(encoding="utf-8")
        if SITE_URL not in content:
            fail(f"{filename}: URL canônica da Vitrine ausente")
        if REPO_URL not in content:
            fail(f"{filename}: URL canônica do repositório ausente")


def validate_public_copy() -> None:
    leaks: list[str] = []
    for filename in PUBLIC_RENDER_FILES:
        content = (ROOT / filename).read_text(encoding="utf-8")
        for token in FORBIDDEN_PUBLIC_COPY:
            if token in content:
                leaks.append(f"{filename}: {token}")
    if leaks:
        fail("linguagem interna/de desenvolvimento exposta na superfície pública: " + "; ".join(leaks))

    app = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
    products_js = (ROOT / "assets" / "products.js").read_text(encoding="utf-8")
    if "academic_evidence_note" in app:
        fail("assets/app.js não deve renderizar nem indexar academic_evidence_note")
    if "distribution.notes" in products_js:
        fail("assets/products.js não deve renderizar nem indexar distribution.notes")

    forbidden_assets = ("assets/quality-summary.js", "assets/build-meta.js")
    for filename in PUBLIC_PAGES:
        content = (ROOT / filename).read_text(encoding="utf-8")
        found = [asset for asset in forbidden_assets if asset in content]
        if found:
            fail(f"{filename}: asset interno não deve ser carregado publicamente: {', '.join(found)}")


def validate_visual_contract() -> None:
    visual = (ROOT / "assets" / "visual-refinement.css").read_text(encoding="utf-8")
    ux = (ROOT / "assets" / "ux-v2.css").read_text(encoding="utf-8")
    required_visual = (
        ".results-more[hidden]{display:none}",
        "scroll-snap-type:x proximity",
    )
    missing = [rule for rule in required_visual if rule not in visual]
    if missing:
        fail("contrato visual base incompleto")
    required_ux = (
        ".nav-toggle",
        ".scientific-filter-grid",
        ".product-triage",
        ".compare-remove",
        "@media(max-width:820px)",
    )
    missing_ux = [rule for rule in required_ux if rule not in ux]
    if missing_ux:
        fail("contrato UX product-first incompleto: " + ", ".join(missing_ux))

    progressive_contracts = {
        "assets/app.js": ("const PAGE_SIZE = 12;", "filtered.slice(0, visibleCount)", "visibleCount + PAGE_SIZE"),
        "assets/products.js": ("const PAGE_SIZE = 6;", "filtered.slice(0, visibleCount)", "visibleCount + PAGE_SIZE"),
    }
    for filename, rules in progressive_contracts.items():
        content = (ROOT / filename).read_text(encoding="utf-8")
        missing_progressive = [rule for rule in rules if rule not in content]
        if missing_progressive:
            fail(f"divulgação progressiva incompleta em {filename}")

    product_ux = (ROOT / "assets" / "product-ux-v2.js").read_text(encoding="utf-8")
    required_product_ux = (
        "uxRelevanceScore(b,query) - uxRelevanceScore(a,query)",
        "uxBrazilScore(b) - uxBrazilScore(a)",
        "uxCompletenessScore(b) - uxCompletenessScore(a)",
        "uxSourceOriginScore(b) - uxSourceOriginScore(a)",
        "data-remove-compare",
        'els.compareDialog.addEventListener("close", uxResetSelection);',
        "uxCoverageContainsPeriod",
        "uxProductMatchesQuery",
    )
    missing_product_ux = [rule for rule in required_product_ux if rule not in product_ux]
    if missing_product_ux:
        fail("contrato funcional product-first incompleto: " + ", ".join(missing_product_ux))


def validate_required_assets() -> None:
    required = (
        "assets/style.css", "assets/accessibility.css", "assets/brazil-scope.css", "assets/products.css",
        "assets/visual-refinement.css", "assets/ux-v2.css", "assets/app.js", "assets/products.js",
        "assets/product-ux-v2.js", "assets/home.js", "assets/navigation.js", "assets/analytics.js",
        "assets/quality-summary.js", "assets/build-meta.js",
        "data/data_resources.csv", "data/data_resources.json", "data/data_products.csv", "data/data_products.json",
        "data/product_distributions.csv", "data/brazil_scope_priorities.json", "data/build-meta.json",
    )
    missing = [name for name in required if not (ROOT / name).exists() or (ROOT / name).stat().st_size == 0]
    if missing:
        fail("artefatos obrigatórios ausentes: " + ", ".join(missing))


for page in PUBLIC_PAGES:
    validate_page(page)
validate_identity()
validate_public_copy()
validate_visual_contract()
validate_required_assets()
print("OK: Vitrine product-first, navegável e com superfície pública limpa")
