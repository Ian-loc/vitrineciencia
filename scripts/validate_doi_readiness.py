#!/usr/bin/env python3
"""Valida a prontidão factual da candidata DOI contra o modelo atual da Vitrine."""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS_PATH = ROOT / "release" / "doi_readiness.json"
OBJECTIVES_PATH = ROOT / "FINAL_OBJECTIVES_AND_DOI_GATES.md"
CITATION_PATH = ROOT / "CITATION.cff"
PROJECT_STATE_PATH = ROOT / "docs" / "PROJECT_STATE.md"

EXPECTED_GATES = [f"G{i}" for i in range(1, 10)]
ALLOWED_GATE_STATUS = {"concluído", "parcial", "bloqueado"}
EXPECTED_SNAPSHOT_KEYS = {
    "resources": ROOT / "data" / "data_resources.csv",
    "products": ROOT / "data" / "data_products.csv",
    "distributions": ROOT / "data" / "product_distributions.csv",
}
LEGACY_TOKENS = (
    "catalog_current_version",
    '"0.7.0"',
    "38 campos",
    "BR1",
    "BR5",
    "35 fontes",
    "16 registros",
    "Lara, Ian",
)


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def row_count(path: Path) -> int:
    if not path.exists():
        fail(f"arquivo ausente: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def require_text(path: Path) -> str:
    if not path.exists():
        fail(f"arquivo ausente: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


readiness_text = require_text(READINESS_PATH)
readiness = json.loads(readiness_text)
objectives = require_text(OBJECTIVES_PATH)
citation = require_text(CITATION_PATH)
project_state = require_text(PROJECT_STATE_PATH)

for token in LEGACY_TOKENS:
    if token in readiness_text:
        fail(f"release/doi_readiness.json ainda contém contrato legado: {token}")

if readiness.get("contract_version") != "2.0":
    fail("contract_version de prontidão DOI deve ser 2.0")
if readiness.get("catalog_state") != "unreleased":
    fail("catalog_state deve permanecer unreleased antes da tag/release formal")
if readiness.get("target_stable_release") != "1.0.0":
    fail("target_stable_release deve ser 1.0.0")
if readiness.get("candidate_ref") != "release/v1.0.0":
    fail("candidate_ref deve ser release/v1.0.0")
if readiness.get("archive_type") != "Dataset":
    fail("depósito planejado deve ser classificado como Dataset")
if readiness.get("doi_allowed") is not False:
    fail("DOI deve permanecer bloqueado até decisão humana explícita e gates finais")

reviewed = readiness.get("last_reviewed")
try:
    date.fromisoformat(str(reviewed))
except ValueError:
    fail("last_reviewed deve ser uma data ISO YYYY-MM-DD")

snapshot = readiness.get("snapshot")
if not isinstance(snapshot, dict):
    fail("snapshot de prontidão DOI ausente ou inválido")
for key, path in EXPECTED_SNAPSHOT_KEYS.items():
    actual = row_count(path)
    if snapshot.get(key) != actual:
        fail(f"snapshot.{key}={snapshot.get(key)!r}, mas tabela canônica contém {actual}")

if 'version: "unreleased"' not in citation:
    fail("CITATION.cff deve permanecer unreleased antes da publicação formal")
for required in (
    "Vitrine Ciência",
    "https://ian-loc.github.io/vitrineciencia/",
    "https://github.com/Ian-loc/vitrineciencia",
    "https://orcid.org/0000-0003-1164-9318",
):
    if required not in citation:
        fail(f"CITATION.cff sem identidade obrigatória: {required}")

if "fase ativa de QA/QC e manutenção" not in project_state:
    fail("PROJECT_STATE.md não preserva a fase corrente de QA/QC")
if "ainda sem tag Git imutável, GitHub Release ou DOI" not in project_state:
    fail("PROJECT_STATE.md não preserva o estado unreleased da candidata")

for gate_id in EXPECTED_GATES:
    if f"{gate_id} —" not in objectives:
        fail(f"FINAL_OBJECTIVES_AND_DOI_GATES.md não menciona {gate_id}")
for retired in ("G10 —", "G11 —", "G12 —"):
    if retired in objectives:
        fail(f"FINAL_OBJECTIVES_AND_DOI_GATES.md ainda expõe gate legado {retired.split()[0]}")

if "instrução humana explícita" not in readiness.get("decision_rule", ""):
    fail("regra de decisão DOI deve exigir instrução humana explícita")

gates = readiness.get("gates")
if not isinstance(gates, list) or [gate.get("id") for gate in gates] != EXPECTED_GATES:
    fail("release/doi_readiness.json deve conter G1–G9 em ordem")
for gate in gates:
    if gate.get("status") not in ALLOWED_GATE_STATUS:
        fail(f"{gate.get('id')}: status inválido")
    if not str(gate.get("evidence", "")).strip():
        fail(f"{gate.get('id')}: evidência vazia")

by_id = {gate["id"]: gate for gate in gates}
for blocked_id in ("G7", "G8", "G9"):
    if by_id[blocked_id]["status"] == "concluído":
        fail(f"{blocked_id} não pode estar concluído antes de tag/depósito/DOI")

print(
    "OK: prontidão DOI alinhada ao modelo atual — "
    f"{snapshot['resources']} fontes, {snapshot['products']} produtos, "
    f"{snapshot['distributions']} distribuições; G1–G9 coerentes; DOI bloqueado"
)
