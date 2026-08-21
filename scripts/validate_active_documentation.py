#!/usr/bin/env python3
"""Validate that active Vitrine documentation does not drift from canonical state."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANONICAL = {
    "fontes": ROOT / "data" / "data_resources.csv",
    "produtos": ROOT / "data" / "data_products.csv",
    "distribuições": ROOT / "data" / "product_distributions.csv",
}

STATE_DOCS = [
    ROOT / "docs" / "PROJECT_STATE.md",
    ROOT / "WORKFLOW_STATUS.md",
]

NO_VOLATILE_SNAPSHOT_DOCS = [
    ROOT / "AUDIT_REPORT.md",
    ROOT / "IMPLEMENTATION_WORKFLOW.md",
    ROOT / "PRODUCT_CATALOG_MODEL.md",
    ROOT / "QUALITY_CORRECTION_WORKFLOW.md",
    ROOT / "SELECTION_AND_COVERAGE_POLICY.md",
    ROOT / "docs" / "UX6_PRODUCT_DISCOVERY_IMPLEMENTATION.md",
    ROOT / "docs" / "VITRINE_BOUNDARY.md",
    ROOT / "docs" / "VITRINE_CANONICAL_DATA_CONTRACT.md",
    ROOT / "docs" / "VITRINE_OPERATING_MODEL.md",
]

HISTORICAL_SNAPSHOT_DOCS = [
    ROOT / "DOCUMENTATION_CONSISTENCY_AUDIT.md",
]

COUNT_PATTERN = re.compile(
    r"\b\d+\s+fontes\b.{0,160}\b\d+\s+produtos\b.{0,160}"
    r"\b\d+\s+distribui(?:ções|coes)\b",
    flags=re.IGNORECASE | re.DOTALL,
)


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def count_csv(path: Path) -> int:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def read(path: Path) -> str:
    if not path.exists():
        fail(f"documento ativo ausente: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def citation_version() -> str:
    text = read(ROOT / "CITATION.cff")
    match = re.search(r'^version:\s*["\']?([^"\'\s]+)["\']?\s*$', text, flags=re.MULTILINE)
    if not match:
        fail("CITATION.cff não declara version de forma reconhecível")
    return match.group(1)


def validate_release_state() -> None:
    """Prevent the live branch from presenting an unpublished candidate as released."""
    version = citation_version()
    changelog = read(ROOT / "CHANGELOG.md")

    if version == "unreleased":
        if re.search(r"^##\s+1\.0\.0\b", changelog, flags=re.MULTILINE):
            fail(
                "CHANGELOG.md apresenta 1.0.0 como release formal enquanto "
                "CITATION.cff permanece unreleased"
            )
        if "## Candidata v1.0.0" not in changelog:
            fail("CHANGELOG.md não identifica explicitamente v1.0.0 como candidata")

    license_public = read(ROOT / "LICENSE-DATA.md")
    license_package_source = read(ROOT / "DATA_LICENSE.md")
    if license_public != license_package_source:
        fail(
            "LICENSE-DATA.md e DATA_LICENSE.md divergem; a licença pública e a "
            "licença usada no pacote de release devem ser semanticamente idênticas"
        )


def validate_historical_snapshots() -> None:
    """Keep dated audits clearly historical so stale counts cannot masquerade as live state."""
    for path in HISTORICAL_SNAPSHOT_DOCS:
        text = read(path)
        normalized = text.lower()
        if "historical_evidence" not in normalized:
            fail(f"{path.relative_to(ROOT)} contém snapshot histórico sem marcador HISTORICAL_EVIDENCE")
        if "não representa o estado corrente" not in normalized:
            fail(f"{path.relative_to(ROOT)} não declara explicitamente que o snapshot não representa o estado corrente")
        if "docs/project_state.md" not in normalized or "workflow_status.md" not in normalized:
            fail(f"{path.relative_to(ROOT)} não aponta para as fontes do estado vivo")
        if re.search(r"^##\s+revisão corrente\b", text, flags=re.IGNORECASE | re.MULTILINE):
            fail(f"{path.relative_to(ROOT)} volta a apresentar snapshot histórico como revisão corrente")


def main() -> None:
    counts = {name: count_csv(path) for name, path in CANONICAL.items()}
    expected_fragment = (
        f"{counts['fontes']} fontes",
        f"{counts['produtos']} produtos",
        f"{counts['distribuições']} distribuições",
    )

    for path in STATE_DOCS:
        text = read(path)
        missing = [fragment for fragment in expected_fragment if fragment not in text]
        if missing:
            fail(f"{path.relative_to(ROOT)} não reflete as contagens canônicas; faltam: {', '.join(missing)}")
        normalized = text.lower()
        if "qa/qc" not in normalized:
            fail(f"{path.relative_to(ROOT)} não declara a fase ativa de QA/QC")
        if "expans" not in normalized or "paus" not in normalized:
            fail(f"{path.relative_to(ROOT)} não declara explicitamente a pausa de expansão")

    for path in NO_VOLATILE_SNAPSHOT_DOCS:
        text = read(path)
        match = COUNT_PATTERN.search(text)
        if match:
            snippet = " ".join(match.group(0).split())
            fail(f"{path.relative_to(ROOT)} replica snapshot quantitativo volátil: {snippet}")

    validate_historical_snapshots()

    selection = read(ROOT / "SELECTION_AND_COVERAGE_POLICY.md").lower()
    if "pausada" not in selection or "instrução humana explícita" not in selection:
        fail("SELECTION_AND_COVERAGE_POLICY.md não preserva a pausa de expansão")

    operating = read(ROOT / "docs" / "VITRINE_OPERATING_MODEL.md").lower()
    if "expansão de novas fontes, produtos e distribuições está **pausada**" not in operating:
        fail("VITRINE_OPERATING_MODEL.md não preserva a pausa de expansão")

    implementation = read(ROOT / "IMPLEMENTATION_WORKFLOW.md").lower()
    if "qa/qc" not in implementation:
        fail("IMPLEMENTATION_WORKFLOW.md não declara a fase corrente de QA/QC")
    if "expansão de novas fontes, produtos e distribuições" not in implementation or "pausada" not in implementation:
        fail("IMPLEMENTATION_WORKFLOW.md não preserva a pausa de expansão")
    if "instrução humana explícita" not in implementation:
        fail("IMPLEMENTATION_WORKFLOW.md não exige decisão humana para retomar expansão")

    quality = read(ROOT / "QUALITY_CORRECTION_WORKFLOW.md").lower()
    if "qa/qc" not in quality:
        fail("QUALITY_CORRECTION_WORKFLOW.md não declara a fase corrente de QA/QC")
    if "expansão de novas fontes, produtos e distribuições" not in quality or "pausada" not in quality:
        fail("QUALITY_CORRECTION_WORKFLOW.md não preserva a pausa de expansão")
    if "instrução humana explícita" not in quality:
        fail("QUALITY_CORRECTION_WORKFLOW.md não exige decisão humana para retomar expansão")
    if "docs/project_state.md" not in quality or "workflow_status.md" not in quality:
        fail("QUALITY_CORRECTION_WORKFLOW.md não aponta para as fontes do estado vivo")

    ux6 = read(ROOT / "docs" / "UX6_PRODUCT_DISCOVERY_IMPLEMENTATION.md").lower()
    if "qa/qc" not in ux6:
        fail("UX6_PRODUCT_DISCOVERY_IMPLEMENTATION.md não declara a fase corrente de QA/QC")
    if "expansão de novas fontes, produtos e distribuições" not in ux6 or "pausada" not in ux6:
        fail("UX6_PRODUCT_DISCOVERY_IMPLEMENTATION.md não preserva a pausa de expansão")
    if "instrução humana explícita" not in ux6:
        fail("UX6_PRODUCT_DISCOVERY_IMPLEMENTATION.md não exige decisão humana para retomar expansão")
    if "docs/project_state.md" not in ux6 or "workflow_status.md" not in ux6:
        fail("UX6_PRODUCT_DISCOVERY_IMPLEMENTATION.md não aponta para as fontes do estado vivo")

    validate_release_state()

    print(
        "OK active documentation state: "
        f"{counts['fontes']} fontes, {counts['produtos']} produtos, "
        f"{counts['distribuições']} distribuições; snapshots voláteis centralizados; "
        f"release={citation_version()}"
    )


if __name__ == "__main__":
    main()
