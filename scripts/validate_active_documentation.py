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
    ROOT / "PRODUCT_CATALOG_MODEL.md",
    ROOT / "SELECTION_AND_COVERAGE_POLICY.md",
    ROOT / "docs" / "VITRINE_BOUNDARY.md",
    ROOT / "docs" / "VITRINE_CANONICAL_DATA_CONTRACT.md",
    ROOT / "docs" / "VITRINE_OPERATING_MODEL.md",
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


def main() -> None:
    counts = {name: count_csv(path) for name, path in CANONICAL.items()}
    expected_fragment = (
        f"{counts['fontes']} fontes" ,
        f"{counts['produtos']} produtos",
        f"{counts['distribuições']} distribuições",
    )

    for path in STATE_DOCS:
        text = read(path)
        missing = [fragment for fragment in expected_fragment if fragment not in text]
        if missing:
            fail(
                f"{path.relative_to(ROOT)} não reflete as contagens canônicas; "
                f"faltam: {', '.join(missing)}"
            )
        normalized = text.lower()
        if "qa/qc" not in normalized:
            fail(f"{path.relative_to(ROOT)} não declara a fase ativa de QA/QC")
        if "expans" not in normalized or "paus" not in normalized:
            fail(
                f"{path.relative_to(ROOT)} não declara explicitamente a pausa de expansão"
            )

    for path in NO_VOLATILE_SNAPSHOT_DOCS:
        text = read(path)
        match = COUNT_PATTERN.search(text)
        if match:
            snippet = " ".join(match.group(0).split())
            fail(
                f"{path.relative_to(ROOT)} replica snapshot quantitativo volátil: {snippet}"
            )

    selection = read(ROOT / "SELECTION_AND_COVERAGE_POLICY.md").lower()
    if "pausada" not in selection or "instrução humana explícita" not in selection:
        fail("SELECTION_AND_COVERAGE_POLICY.md não preserva a pausa de expansão")

    operating = read(ROOT / "docs" / "VITRINE_OPERATING_MODEL.md").lower()
    if "expansão de novas fontes, produtos e distribuições está **pausada**" not in operating:
        fail("VITRINE_OPERATING_MODEL.md não preserva a pausa de expansão")

    print(
        "OK active documentation state: "
        f"{counts['fontes']} fontes, {counts['produtos']} produtos, "
        f"{counts['distribuições']} distribuições; snapshots voláteis centralizados"
    )


if __name__ == "__main__":
    main()
