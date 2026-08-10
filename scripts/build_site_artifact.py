#!/usr/bin/env python3
"""Build the isolated static artifact published as the Vitrine Ciência.

Only files required by the public discovery interface are copied. Development,
QA, build metadata, database material and operational documentation remain in
the repository and are not shipped in the GitHub Pages artifact.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"

REQUIRED_FILES = (
    "index.html",
    "products.html",
    "analytics.html",
    "about.html",
    "LICENSE",
    "LICENSE-DATA.md",
    "assets/style.css",
    "assets/accessibility.css",
    "assets/brazil-scope.css",
    "assets/products.css",
    "assets/visual-refinement.css",
    "assets/app.js",
    "assets/products.js",
    "assets/analytics.js",
    "data/data_resources.csv",
    "data/data_resources.json",
    "data/data_products.csv",
    "data/data_products.json",
    "data/product_distributions.csv",
    "data/brazil_scope_priorities.json",
)

OPTIONAL_FILES = (
    "404.html",
    "CNAME",
    "favicon.ico",
    "favicon.svg",
    "robots.txt",
    "sitemap.xml",
    "data/product_distributions.json",
)

FORBIDDEN_PUBLIC_PATHS = (
    "explorer.html",
    "abordagens.html",
    "data/federated_layers.json",
    "data/build-meta.json",
    "assets/explorer.js",
    "assets/explorer.css",
    "assets/approaches.css",
    "assets/quality-summary.js",
    "assets/build-meta.js",
    "WORKFLOW_STATUS.md",
    "IMPLEMENTATION_WORKFLOW.md",
    "DOCUMENTATION_CONSISTENCY_AUDIT.md",
    "migration",
    "scripts",
    ".github",
    "audit",
    "schema",
    "database",
    "docs",
    "config",
    "release",
)


def copy_file(relative_path: str, *, required: bool) -> None:
    source = ROOT / relative_path
    if not source.exists():
        if required:
            raise SystemExit(f"ERRO: arquivo público obrigatório ausente: {relative_path}")
        return
    destination = OUTPUT / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


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

    files = sum(1 for path in OUTPUT.rglob("*") if path.is_file())
    print(f"OK: artefato público da Vitrine criado em {OUTPUT} com {files} arquivos")


if __name__ == "__main__":
    main()
