#!/usr/bin/env python3
"""Valida autoridades canônicas de versões/coleções e proveniência."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "data" / "data_products.csv"
RESOURCES = ROOT / "data" / "data_resources.csv"
VERSIONS = ROOT / "data" / "product_versions.json"
PROVENANCE = ROOT / "data" / "provenance_assertions.json"
VERSION_SCHEMA = ROOT / "schema" / "product-versions-v1.json"
PROVENANCE_SCHEMA = ROOT / "schema" / "provenance-assertions-v1.json"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_json(path: Path):
    if not path.exists() or path.stat().st_size == 0:
        fail(f"arquivo ausente/vazio: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def expected_version_class(label: str) -> tuple[str, str]:
    value = label.strip().lower()
    if value.startswith("v") and value[1:2].isdigit():
        return "named_version", "explicit_version_label"
    if len(value) == 4 and value.isdigit():
        return "edition_or_year", "edition_label"
    if value.startswith("atualização publicada em "):
        return "provider_update", "descriptive_state"
    if value in {"coleção corrente", "coleções correntes"}:
        return "current_collection_state", "descriptive_state"
    if value == "coleções por bioma":
        return "collection_group", "descriptive_state"
    if value == "serviços correntes":
        return "service_state", "descriptive_state"
    if value in {"catálogo corrente", "catálogos correntes"}:
        return "catalog_state", "descriptive_state"
    if value.startswith("acesso via projetos "):
        return "access_configuration", "descriptive_state"
    if value.startswith("produto experimental desde "):
        return "experimental_state", "descriptive_state"
    return "descriptive_state", "descriptive_state"


products = read_csv(PRODUCTS)
resources = read_csv(RESOURCES)
versions_payload = read_json(VERSIONS)
provenance_payload = read_json(PROVENANCE)
version_schema = read_json(VERSION_SCHEMA)
provenance_schema = read_json(PROVENANCE_SCHEMA)

if versions_payload.get("schema_version") != "product-versions-v1" or versions_payload.get("status") != "canonical":
    fail("data/product_versions.json não é autoridade product-versions-v1")
if provenance_payload.get("schema_version") != "provenance-assertions-v1" or provenance_payload.get("status") != "canonical":
    fail("data/provenance_assertions.json não é autoridade provenance-assertions-v1")
if version_schema.get("authority") != "data/product_versions.json":
    fail("schema de versões não declara autoridade correta")
if provenance_schema.get("authority") != "data/provenance_assertions.json":
    fail("schema de proveniência não declara autoridade correta")

versions = versions_payload.get("versions") or []
assertions = provenance_payload.get("assertions") or []
if versions_payload.get("count") != len(versions):
    fail("product_versions.json: count divergente")
if provenance_payload.get("count") != len(assertions):
    fail("provenance_assertions.json: count divergente")

version_ids = [item.get("version_id") for item in versions]
provenance_ids = [item.get("provenance_id") for item in assertions]
if len(version_ids) != len(set(version_ids)):
    fail("version_id duplicado")
if len(provenance_ids) != len(set(provenance_ids)):
    fail("provenance_id duplicado")

product_by_id = {row["product_id"]: row for row in products}
resource_by_id = {row["resource_id"]: row for row in resources}

allowed_kinds = set(version_schema.get("kinds") or {})
allowed_identity = set(version_schema.get("identity_status_values") or [])
allowed_roles = set(provenance_schema.get("roles") or {})
allowed_agent_status = set(provenance_schema.get("agent_identity_status_values") or [])
allowed_assertion_status = set(provenance_schema.get("assertion_status_values") or [])

baseline_versions: dict[str, list[dict]] = {}
for item in versions:
    pid = str(item.get("offering_id") or "")
    rid = str(item.get("record_id") or "")
    if pid not in product_by_id:
        fail(f"{item.get('version_id')}: offering_id inexistente: {pid}")
    if product_by_id[pid]["resource_id"] != rid:
        fail(f"{item.get('version_id')}: record_id não corresponde ao produto")
    if item.get("kind") not in allowed_kinds:
        fail(f"{item.get('version_id')}: kind inválido")
    if item.get("identity_status") not in allowed_identity:
        fail(f"{item.get('version_id')}: identity_status inválido")
    if not str(item.get("label") or "").strip():
        fail(f"{item.get('version_id')}: label vazio")
    if item.get("source_field") == "version_or_collection":
        baseline_versions.setdefault(pid, []).append(item)

for product in products:
    pid = product["product_id"]
    label = product.get("version_or_collection", "").strip()
    baseline = baseline_versions.get(pid, [])
    if label:
        if len(baseline) != 1:
            fail(f"{pid}: deve haver exatamente uma versão baseline para version_or_collection")
        item = baseline[0]
        if item.get("label") != label:
            fail(f"{pid}: label canônico de versão diverge do CSV")
        expected_kind, expected_identity = expected_version_class(label)
        if item.get("kind") != expected_kind or item.get("identity_status") != expected_identity:
            fail(f"{pid}: semântica de versão baseline divergente")
        if item.get("verified_at") != (product.get("last_verified") or None):
            fail(f"{pid}: verified_at de versão diverge do produto")
    elif baseline:
        fail(f"{pid}: versão baseline existe sem version_or_collection no produto")

baseline_provenance: dict[str, list[dict]] = {}
for item in assertions:
    rid = str(item.get("record_id") or "")
    if rid not in resource_by_id:
        fail(f"{item.get('provenance_id')}: record_id inexistente: {rid}")
    if item.get("target_type") != "resource":
        fail(f"{item.get('provenance_id')}: target_type deve ser resource no baseline")
    if item.get("target_id") != f"{rid}::resource":
        fail(f"{item.get('provenance_id')}: target_id divergente")
    roles = item.get("roles") or []
    if not roles or any(role not in allowed_roles for role in roles):
        fail(f"{item.get('provenance_id')}: role inválido")
    if item.get("agent_identity_status") not in allowed_agent_status:
        fail(f"{item.get('provenance_id')}: agent_identity_status inválido")
    if item.get("assertion_status") not in allowed_assertion_status:
        fail(f"{item.get('provenance_id')}: assertion_status inválido")
    if item.get("source_field") == "owner_or_manager":
        baseline_provenance.setdefault(rid, []).append(item)

for resource in resources:
    rid = resource["resource_id"]
    owner = resource.get("owner_or_manager", "").strip()
    baseline = baseline_provenance.get(rid, [])
    if owner:
        if len(baseline) != 1:
            fail(f"{rid}: deve haver exatamente uma afirmação baseline de owner_or_manager")
        item = baseline[0]
        if item.get("agent_label") != owner:
            fail(f"{rid}: agent_label não preserva owner_or_manager")
        if item.get("roles") != ["responsible_or_maintainer"]:
            fail(f"{rid}: baseline legado deve preservar papel conservador")
        if item.get("assertion_status") != "legacy_grouped_statement":
            fail(f"{rid}: baseline legado deve permanecer legacy_grouped_statement")
        if item.get("institutional_status") != (resource.get("institutional_status") or None):
            fail(f"{rid}: institutional_status divergente")
        if item.get("verified_at") != (resource.get("last_verified") or None):
            fail(f"{rid}: verified_at de proveniência divergente")
    elif baseline:
        fail(f"{rid}: proveniência baseline existe sem owner_or_manager")

print(
    "OK versões/proveniência: "
    f"{len(versions)} objetos de versão ({len(baseline_versions)} ofertas baseline); "
    f"{len(assertions)} afirmações de proveniência ({len(baseline_provenance)} registros baseline)"
)
