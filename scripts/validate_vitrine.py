#!/usr/bin/env python3
"""Validate the user-facing static Vitrine Ciência rescue surface."""
from __future__ import annotations

import csv
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://ian-loc.github.io/vitrineciencia/"
REPO_URL = "https://github.com/Ian-loc/vitrineciencia"
PUBLIC_PAGES = ("index.html", "products.html", "sources.html", "analytics.html", "analytics-products.html", "about.html")
INTERACTIVE_PAGES = {"products.html", "sources.html", "analytics.html", "analytics-products.html"}
CANONICAL_URLS = {
    "index.html": SITE_URL,
    "products.html": SITE_URL + "products.html",
    "sources.html": SITE_URL + "sources.html",
    "analytics.html": SITE_URL + "analytics.html",
    "analytics-products.html": SITE_URL + "analytics-products.html",
    "about.html": SITE_URL + "about.html",
}
REQUIRED_IDS = {
    "index.html": {"conteudo", "home-theme", "home-products", "home-sources", "home-access", "home-product-areas", "home-all-sources"},
    "products.html": {
        "produtos", "product-search", "product-q", "product-filters", "product-theme", "product-coverage",
        "product-year-start", "product-year-end", "product-temporal", "product-support", "product-spatial",
        "product-access", "product-format", "product-free", "product-license", "product-area", "product-source",
        "product-kind", "product-auth", "product-status", "product-origin", "product-brazil", "product-sort",
        "product-clear", "product-list", "product-count", "product-results-more", "product-show-more",
        "product-shown-count", "product-result-insights", "interpreted-query", "compare-bar", "compare-dialog"
    },
    "sources.html": {
        "conteudo", "catalogo", "hero-search", "q", "source-theme-shortcut", "source-theme-status", "filters",
        "scope", "area", "brazil", "download", "programmatic", "coverage", "format", "evidence", "sort",
        "clear", "list", "count", "results-more", "show-more", "shown-count"
    },
    "analytics.html": {"analise", "summary", "chart-areas", "chart-download", "chart-programmatic", "chart-brazil", "chart-evidence", "chart-formats", "chart-visualizations"},
    "analytics-products.html": {"analise-produtos", "product-summary", "product-chart-areas", "product-chart-kinds", "product-chart-brazil", "product-chart-temporal", "product-chart-support", "product-chart-formats", "product-chart-access"},
    "about.html": {"sobre", "o-que-e", "como-usar", "verificacao", "limites", "citacao"},
}
FORBIDDEN_PAGE_TOKENS = (
    "Simbiotrama", "Simbioscópio", "Simbioscopio", "explorer.html", "abordagens.html",
    "Ian-loc/ScienceDataSourcesCatalog", "github.io/ScienceDataSourcesCatalog",
)
FORBIDDEN_PUBLIC_COPY = (
    "Transparência de qualidade", "Cobertura e estado dos metadados", "no piloto", "Escopo de enumeração",
    "Identificador interno", "Avaliação e governança", "data-build-meta", "Build:", "P0 —", "P1 —", "P2 —", "P3 —",
    "A arquitetura científica interna", "arquitetura científica interna", "arquitetura interna",
    "Decisão arquitetural", "Direção experimental", "snapshot candidato", "Snapshot candidato",
    "produto principal preservado", "MVP", "teto de inferência",
)


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.tags: list[str] = []
        self.local_refs: list[str] = []
        self.external_assets: list[str] = []
        self.canonical_urls: list[str] = []
        self.og_urls: list[str] = []
        self.inputs: list[dict[str, str | None]] = []
        self.forms: list[dict[str, str | None]] = []
        self.lang = ""
        self.viewport = False
        self.skip = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.tags.append(tag)
        rel_tokens = (values.get("rel") or "").split()
        if tag == "html": self.lang = values.get("lang") or ""
        if tag == "meta" and values.get("name") == "viewport": self.viewport = True
        if tag == "meta" and values.get("property") == "og:url" and values.get("content"): self.og_urls.append(values["content"] or "")
        if tag == "link" and "canonical" in rel_tokens and values.get("href"): self.canonical_urls.append(values["href"] or "")
        if tag == "a" and "skip" in (values.get("class") or "").split() and (values.get("href") or "").startswith("#"): self.skip = True
        if tag == "input": self.inputs.append(values)
        if tag == "form": self.forms.append(values)
        if values.get("id"): self.ids.append(values["id"] or "")
        ref = values.get("src") if tag == "script" else values.get("href") if tag in {"a", "link"} else None
        if not ref or ref.startswith(("#", "mailto:", "tel:")): return
        parsed = urlparse(ref)
        if parsed.scheme or parsed.netloc:
            if tag == "script" or (tag == "link" and "stylesheet" in rel_tokens): self.external_assets.append(ref)
            return
        if parsed.path and not parsed.path.endswith("/"): self.local_refs.append(parsed.path)


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def csv_rows(relative_path: str) -> int:
    path = ROOT / relative_path
    if not path.exists(): fail(f"CSV ausente: {relative_path}")
    with path.open(encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def validate_counts() -> None:
    live = {
        "data/data_resources.csv": 51,
        "data/data_products.csv": 11,
        "data/product_distributions.csv": 19,
    }
    for filename, expected in live.items():
        found = csv_rows(filename)
        if found != expected: fail(f"{filename}: esperado {expected}, encontrado {found}")

    quarantine = ROOT / "data/quarantine/v1.0.0-expanded"
    if not quarantine.exists(): fail("quarentena v1.0.0-expanded ausente")
    frozen = {
        "data_resources.csv": 135,
        "data_products.csv": 843,
        "product_distributions.csv": 876,
    }
    for filename, expected in frozen.items():
        found = csv_rows(f"data/quarantine/v1.0.0-expanded/{filename}")
        if found != expected: fail(f"quarentena/{filename}: esperado {expected}, encontrado {found}")


def validate_page(filename: str) -> None:
    path = ROOT / filename
    if not path.exists(): fail(f"página ausente: {filename}")
    content = path.read_text(encoding="utf-8")
    parser = Parser(); parser.feed(content)
    if parser.lang != "pt-BR": fail(f"{filename}: lang deve ser pt-BR")
    if not parser.viewport or not parser.skip: fail(f"{filename}: viewport/skip-link ausente")
    if parser.tags.count("main") != 1 or parser.tags.count("h1") != 1: fail(f"{filename}: deve ter exatamente um main e um h1")
    if filename in INTERACTIVE_PAGES and "noscript" not in parser.tags: fail(f"{filename}: fallback noscript ausente")
    if parser.external_assets: fail(f"{filename}: dependência externa não permitida: {', '.join(parser.external_assets)}")
    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates: fail(f"{filename}: IDs duplicados: {', '.join(duplicates)}")
    missing = sorted(REQUIRED_IDS[filename].difference(parser.ids))
    if missing: fail(f"{filename}: IDs obrigatórios ausentes: {', '.join(missing)}")
    if "assets/visual-refinement.css" not in content or "assets/ux-v2.css" not in content or "assets/ux-simple.css" not in content:
        fail(f"{filename}: camadas visuais públicas obrigatórias ausentes")
    expected_url = CANONICAL_URLS[filename]
    if parser.canonical_urls != [expected_url]: fail(f"{filename}: canonical deve ser único e igual a {expected_url}")
    if parser.og_urls != [expected_url]: fail(f"{filename}: og:url deve ser único e igual ao canonical")
    if '<meta name="twitter:card" content="summary">' not in content: fail(f"{filename}: twitter:card ausente")
    for token in FORBIDDEN_PAGE_TOKENS:
        if token in content: fail(f"{filename}: referência fora da fronteira pública: {token}")
    for token in FORBIDDEN_PUBLIC_COPY:
        if token in content: fail(f"{filename}: linguagem interna exposta: {token}")
    for ref in parser.local_refs:
        target = (path.parent / ref).resolve()
        if ROOT not in target.parents and target != ROOT: fail(f"{filename}: referência fora do repositório: {ref}")
        if not target.exists(): fail(f"{filename}: referência local ausente: {ref}")

    if filename == "index.html":
        if '"@type":"DataCatalog"' not in content or '"@context":"https://schema.org"' not in content: fail("index.html: metadados DataCatalog ausentes")
        if "https://orcid.org/0000-0003-1164-9318" not in content: fail("index.html: ORCID ausente")
        if not any(form.get("action") == "sources.html" for form in parser.forms): fail("index.html: descoberta principal deve abrir o núcleo de 51 registros")
        if 'id="home-theme"' not in content or 'name="q"' not in content: fail("index.html: seletor temático controlado ausente")
        if any((item.get("type") or "text").lower() in {"text", "search"} for item in parser.inputs): fail("index.html: busca textual livre não pode ser instrumento principal")
        if "51 registros para descoberta" not in content: fail("index.html: relação entre núcleo 51 e subconjunto detalhado não está explícita")
    elif filename == "sources.html":
        if "assets/static-catalog-51.js" not in content: fail("sources.html: controlador temático do núcleo 51 ausente")
        if "source-theme-shortcut" not in content: fail("sources.html: filtro temático controlado ausente")
        if any((item.get("type") or "text").lower() in {"text", "search"} and item.get("id") == "q" for item in parser.inputs): fail("sources.html: q deve permanecer oculto, não busca livre")
    elif filename == "products.html":
        if "assets/products.js" not in content: fail("products.html: controlador canônico ausente")
        if "subconjunto" not in content.lower() or "51 registros" not in content: fail("products.html: escopo 11/19 como subconjunto do núcleo 51 deve estar explícito")


def validate_identity() -> None:
    for filename in (*PUBLIC_PAGES, "README.md", "CITATION.cff"):
        content = (ROOT / filename).read_text(encoding="utf-8")
        if "Vitrine Ciência" not in content: fail(f"{filename}: identidade Vitrine Ciência ausente")
    for filename in ("README.md", "about.html", "CITATION.cff"):
        content = (ROOT / filename).read_text(encoding="utf-8")
        if SITE_URL not in content: fail(f"{filename}: URL canônica da Vitrine ausente")
        if REPO_URL not in content: fail(f"{filename}: URL canônica do repositório ausente")


def validate_functional_contracts() -> None:
    app = (ROOT / "assets/app.js").read_text(encoding="utf-8")
    products = (ROOT / "assets/products.js").read_text(encoding="utf-8")
    guardrails = (ROOT / "assets/discovery-guardrails.js").read_text(encoding="utf-8")
    theme = (ROOT / "assets/static-catalog-51.js").read_text(encoding="utf-8")
    if "const PAGE_SIZE = 12;" not in app or "filtered.slice(0, visibleCount)" not in app: fail("assets/app.js: divulgação progressiva ausente")
    for token in ("const PAGE_SIZE = 18;", "THEME_GROUPS", "productAccessCategories", "parseQuery"):
        if token not in products: fail(f"assets/products.js: contrato ausente: {token}")
    for token in ("Página do provedor", "API / documentação", "Dados / download", "access-review-note"):
        if token not in guardrails: fail(f"discovery-guardrails.js: semântica de acesso ausente: {token}")
    for token in ("source-theme-shortcut", "URLSearchParams", "sources.html"):
        if token not in theme: fail(f"static-catalog-51.js: contrato temático ausente: {token}")


def validate_required_assets() -> None:
    required = (
        "assets/style.css", "assets/accessibility.css", "assets/brazil-scope.css", "assets/products.css",
        "assets/visual-refinement.css", "assets/ux-v2.css", "assets/ux-simple.css", "assets/product-card-refinement.css",
        "assets/discovery-guardrails.css", "assets/app.js", "assets/ptbr.js", "assets/products.js", "assets/home.js",
        "assets/navigation.js", "assets/analytics.js", "assets/analytics-products.js", "assets/export-selective.js",
        "assets/source-comparison.js", "assets/discovery-guardrails.js", "assets/static-catalog-51.js",
        "data/data_resources.csv", "data/data_resources.json", "data/data_products.csv", "data/data_products.json",
        "data/product_distributions.csv", "data/brazil_scope_priorities.json",
    )
    missing = [name for name in required if not (ROOT / name).exists() or (ROOT / name).stat().st_size == 0]
    if missing: fail("artefatos obrigatórios ausentes: " + ", ".join(missing))


validate_counts()
for page in PUBLIC_PAGES: validate_page(page)
validate_identity()
validate_functional_contracts()
validate_required_assets()
print("OK: Vitrine estática 51/11/19 validada com descoberta temática e papéis de acesso separados")
