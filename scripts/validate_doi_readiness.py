#!/usr/bin/env python3
"""Valida o estado factual de release/DOI da Vitrine Ciência após a publicação v1.0.0."""
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
EXPECTED_DOI = "10.5281/zenodo.22130831"
EXPECTED_ZENODO_RECORD = "https://zenodo.org/records/22130831"
EXPECTED_RELEASE = "https://github.com/Ian-loc/vitrineciencia/releases/tag/v1.0.0"
EXPECTED_SOURCE_COMMIT = "27c545554f406b940662777e3f053e939ef3588c"
EXPECTED_ARCHIVE_SHA256 = "b2e7a996b075d45ef4caca853bf57618b54998724fc9b4bdea3afe3b6159d6f0"
LEGACY_TOKENS = (
    "catalog_current_version",
    '"0.7.0"',
    "38 campos",
    "BR1",
    "BR5",
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

if readiness.get("contract_version") != "2.1":
    fail("contract_version de prontidão DOI pós-release deve ser 2.1")
if readiness.get("catalog_state") != "released":
    fail("catalog_state deve ser released após publicação formal")
if readiness.get("target_stable_release") != "1.0.0":
    fail("target_stable_release deve ser 1.0.0")
if readiness.get("candidate_ref") != "release/v1.0.0":
    fail("candidate_ref deve permanecer release/v1.0.0 por proveniência")
if readiness.get("release_tag") != "v1.0.0":
    fail("release_tag deve ser v1.0.0")
if readiness.get("source_commit") != EXPECTED_SOURCE_COMMIT:
    fail("source_commit não corresponde ao snapshot científico congelado")
if readiness.get("archive_type") != "Dataset":
    fail("depósito deve ser classificado como Dataset")
if readiness.get("doi_allowed") is not True:
    fail("doi_allowed deve ser true após emissão do DOI")
if readiness.get("doi") != EXPECTED_DOI:
    fail(f"DOI esperado: {EXPECTED_DOI}")
if readiness.get("zenodo_record") != EXPECTED_ZENODO_RECORD:
    fail("registro Zenodo não corresponde ao depósito v1.0.0")
if readiness.get("github_release") != EXPECTED_RELEASE:
    fail("GitHub Release não corresponde à v1.0.0")
if readiness.get("archive_sha256") != EXPECTED_ARCHIVE_SHA256:
    fail("SHA-256 do arquivo científico não corresponde ao artefato validado")

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

for required in (
    'version: "1.0.0"',
    f'doi: "{EXPECTED_DOI}"',
    "Vitrine Ciência",
    "https://ian-loc.github.io/vitrineciencia/",
    "https://github.com/Ian-loc/vitrineciencia",
    "https://orcid.org/0000-0003-1164-9318",
):
    if required not in citation:
        fail(f"CITATION.cff sem metadado obrigatório pós-release: {required}")

if "fase ativa de QA/QC e manutenção" not in project_state:
    fail("PROJECT_STATE.md não preserva a fase corrente de QA/QC")
for required in ("release científica `v1.0.0` publicada", EXPECTED_DOI):
    if required not in project_state:
        fail(f"PROJECT_STATE.md sem estado pós-release obrigatório: {required}")

for gate_id in EXPECTED_GATES:
    if f"{gate_id} —" not in objectives:
        fail(f"FINAL_OBJECTIVES_AND_DOI_GATES.md não menciona {gate_id}")
for retired in ("G10 —", "G11 —", "G12 —"):
    if retired in objectives:
        fail(f"FINAL_OBJECTIVES_AND_DOI_GATES.md ainda expõe gate legado {retired.split()[0]}")

if "DOI da v1.0.0 foi emitido" not in readiness.get("decision_rule", ""):
    fail("regra de decisão DOI deve registrar explicitamente a emissão da v1.0.0")

gates = readiness.get("gates")
if not isinstance(gates, list) or [gate.get("id") for gate in gates] != EXPECTED_GATES:
    fail("release/doi_readiness.json deve conter G1–G9 em ordem")
for gate in gates:
    if gate.get("status") not in ALLOWED_GATE_STATUS:
        fail(f"{gate.get('id')}: status inválido")
    if not str(gate.get("evidence", "")).strip():
        fail(f"{gate.get('id')}: evidência vazia")

by_id = {gate["id"]: gate for gate in gates}
for completed_id in ("G2", "G3", "G4", "G5", "G7", "G8"):
    if by_id[completed_id]["status"] != "concluído":
        fail(f"{completed_id} deve estar concluído no estado pós-release")
if by_id["G9"]["status"] not in {"parcial", "concluído"}:
    fail("G9 deve estar parcial ou concluído após propagação do DOI no repositório")

print(
    "OK: estado DOI pós-release validado — "
    f"{snapshot['resources']} fontes, {snapshot['products']} produtos, "
    f"{snapshot['distributions']} distribuições; DOI={EXPECTED_DOI}; G1–G9 coerentes"
)
