#!/usr/bin/env python3
"""Build the isolated static artifact published as the Vitrine Ciência."""
from __future__ import annotations

import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"

REQUIRED_FILES = (
    "index.html", "products.html", "products-list.html", "sources.html", "analytics.html", "analytics-products.html", "about.html",
    "LICENSE", "LICENSE-DATA.md", "robots.txt", "sitemap.xml",
    "assets/style.css", "assets/accessibility.css", "assets/brazil-scope.css", "assets/products.css",
    "assets/visual-refinement.css", "assets/export-selective.css", "assets/ux-v2.css", "assets/ux-v3.css", "assets/ux-simple.css",
    "assets/product-card-refinement.css", "assets/product-index.css", "assets/discovery-guardrails.css",
    "assets/app.js", "assets/ptbr.js", "assets/products.js", "assets/product-filter-ux.js", "assets/product-index.js", "assets/product-ui-fixes.js",
    "assets/product-label-fix.js", "assets/product-distribution-roles.js", "assets/home.js", "assets/navigation.js",
    "assets/analytics.js", "assets/analytics-products.js", "assets/export-selective.js", "assets/source-comparison.js",
    "assets/discovery-guardrails.js", "assets/static-catalog-51.js", "assets/source-discovery-v2.js",
    "assets/semantic-roles.js", "assets/applied-priority.js",
    "data/data_resources.json", "data/data_products.json", "data/brazil_scope_priorities.json",
    "data/static_core_51_access_audit.json", "data/static_core_51_progress.json",
    "data/applied_priority_gate.json", "data/product_distribution_roles.json",
)

OPTIONAL_FILES = ("404.html", "CNAME", "favicon.ico", "favicon.svg")
FORBIDDEN_PUBLIC_PATHS = (
    "explorer.html", "abordagens.html", "data/data_resources.csv", "data/data_products.csv", "data/product_distributions.csv",
    "data/product_distributions.json", "data/federated_layers.json", "data/build-meta.json", "data/quarantine",
    "assets/product-ux-v2.js", "assets/product-ux-compat.js", "assets/explorer.js", "assets/explorer.css", "assets/approaches.css",
    "assets/quality-summary.js", "assets/build-meta.js", "WORKFLOW_STATUS.md", "IMPLEMENTATION_WORKFLOW.md", "DOCUMENTATION_CONSISTENCY_AUDIT.md",
    "migration", "scripts", ".github", "audit", "schema", "database", "docs", "config", "release",
)

HTML_REF_RE = re.compile(r"(?:src|href)=[\"']([^\"']+)[\"']", re.IGNORECASE)
FETCH_REF_RE = re.compile(r"fetch\(\s*[\"']([^\"']+)[\"']")


def copy_file(relative_path: str, *, required: bool) -> None:
    source = ROOT / relative_path
    if not source.exists():
        if required:
            raise SystemExit(f"ERRO: arquivo público obrigatório ausente: {relative_path}")
        return
    destination = OUTPUT / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def local_target(ref: str, *, document_relative: bool) -> Path | None:
    value = ref.strip()
    if not value or value.startswith(("#", "mailto:", "tel:", "data:")):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    path = parsed.path
    if not path or path.endswith("/"):
        return None
    if path.startswith("/"):
        path = path.lstrip("/")
    return OUTPUT / path if document_relative else OUTPUT / path


def validate_runtime_closure() -> None:
    missing: set[str] = set()

    for page in OUTPUT.glob("*.html"):
        content = page.read_text(encoding="utf-8")
        for ref in HTML_REF_RE.findall(content):
            target = local_target(ref, document_relative=True)
            if target is not None and not target.exists():
                missing.add(f"{page.name} -> {ref}")

    for script in (OUTPUT / "assets").glob("*.js"):
        content = script.read_text(encoding="utf-8")
        for ref in FETCH_REF_RE.findall(content):
            target = local_target(ref, document_relative=False)
            if target is not None and not target.exists():
                missing.add(f"{script.relative_to(OUTPUT)} fetch -> {ref}")

    if missing:
        raise SystemExit("ERRO: artefato público com dependências locais ausentes: " + "; ".join(sorted(missing)))


def main() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    for relative_path in REQUIRED_FILES:
        copy_file(relative_path, required=True)
    for relative_path in OPTIONAL_FILES:
        copy_file(relative_path, required=False)
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")

    leaked = [name for name in FORBIDDEN_PUBLIC_PATHS if (OUTPUT / name).exists()]
    if leaked:
        raise SystemExit("ERRO: artefato da Vitrine contém material fora da fronteira: " + ", ".join(leaked))

    validate_runtime_closure()
    files = sum(1 for path in OUTPUT.rglob("*") if path.is_file())
    print(f"OK: artefato público da Vitrine criado em {OUTPUT} com {files} arquivos; dependências locais fechadas")


if __name__ == "__main__":
    main()
