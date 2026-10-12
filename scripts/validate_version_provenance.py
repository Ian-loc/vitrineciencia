#!/usr/bin/env python3
"""Valida versões/coleções e declarações de proveniência canônicas."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "data" / "data_products.csv"
RESOURCES = ROOT / "data" / "data_resources.csv"
VERSIONS = ROOT / "data" / "offering_versions.json"
PROVENANCE = ROOT / "data" / "provenance_statements.json"

ALLOWED_VERSION_KINDS = {"version", "collection", "edition", "release"}
ALLOWED_RESOLUTION_STATUS = {"unresolved_legacy_statement", "partially_resolved", "resolved"}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path):
    if not path.exists() or path.stat().st_size == 0:
        fail(f"arquivo ausente ou vazio: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


products = rows(PRODUCTS)
resources = rows(RESOURCES)
product_by_id = {row["product_id"]: row for row in products}
resource_by_id = {row["resource_id"]: row for row in resources}

version_payload = read_json(VERSIONS)
if version_payload.get("schema_version") != "offering-versions-v1":
    fail("offering_versions.json: schema_version inválida")
if version_payload.get("status") != "canonical":
    fail("offering_versions.json: status deve ser canonical")
if version_payload.get("authority") != "data/offering_versions.json":
    fail("offering_versions.json não se declara autoridade")

versions = version_payload.get("versions")
unresolved = version_payload.get("unresolved_legacy_summaries")
if not isinstance(versions, list) or not isinstance(unresolved, list):
    fail("offering_versions.json: versions e unresolved_legacy_summaries devem ser listas")

version_ids = [item.get("version_id") for item in versions]
if any(not item for item in version_ids) or len(version_ids) != len(set(version_ids)):
    fail("version_id ausente ou duplicado")

resolved_offerings: set[str] = set()
for item in versions:
    oid = item.get("offering_id")
    product = product_by_id.get(oid)
    if not product:
        fail(f"{item.get('version_id')}: offering_id inexistente: {oid}")
    if item.get("version_kind") not in ALLOWED_VERSION_KINDS:
        fail(f"{item.get('version_id')}: version_kind inválido")
    if not str(item.get("version_label") or "").strip():
        fail(f"{item.get('version_id')}: version_label vazio")
    if item.get("source_summary") != (product.get("version_or_collection") or ""):
        fail(f"{item.get('version_id')}: source_summary diverge do campo legado")
    if item.get("verified_at") != (product.get("last_verified") or None):
        fail(f"{item.get('version_id')}: verified_at diverge do produto")
    resolved_offerings.add(oid)

unresolved_by_offering: dict[str, dict] = {}
for item in unresolved:
    oid = item.get("offering_id")
    product = product_by_id.get(oid)
    if not product:
        fail(f"resumo não resolvido aponta para offering inexistente: {oid}")
    if oid in unresolved_by_offering:
        fail(f"resumo não resolvido duplicado para {oid}")
    if oid in resolved_offerings:
        fail(f"{oid}: offering aparece simultaneamente como versão resolvida e resumo não resolvido")
    if item.get("resolution_status") != "not_promoted_to_version_entity":
        fail(f"{oid}: resolution_status inesperado")
    if item.get("summary") != (product.get("version_or_collection") or ""):
        fail(f"{oid}: resumo não resolvido diverge do campo legado")
    if item.get("verified_at") != (product.get("last_verified") or None):
        fail(f"{oid}: verified_at do resumo diverge do produto")
    unresolved_by_offering[oid] = item

legacy_with_summary = {
    row["product_id"]
    for row in products
    if str(row.get("version_or_collection") or "").strip()
}
covered = resolved_offerings | set(unresolved_by_offering)
if covered != legacy_with_summary:
    fail(
        "cobertura dos resumos legados de versão divergente; "
        f"ausentes={sorted(legacy_with_summary - covered)}, extras={sorted(covered - legacy_with_summary)}"
    )

provenance_payload = read_json(PROVENANCE)
if provenance_payload.get("schema_version") != "provenance-v1":
    fail("provenance_statements.json: schema_version inválida")
if provenance_payload.get("status") != "canonical_statement_layer":
    fail("provenance_statements.json: status inesperado")
if provenance_payload.get("authority") != "data/provenance_statements.json":
    fail("provenance_statements.json não se declara autoridade")

statements = provenance_payload.get("statements")
if not isinstance(statements, list):
    fail("provenance_statements.json: statements deve ser lista")

by_record: dict[str, dict] = {}
prov_ids: set[str] = set()
for item in statements:
    pid = item.get("provenance_id")
    rid = item.get("record_id")
    if not pid or pid in prov_ids:
        fail("provenance_id ausente ou duplicado")
    prov_ids.add(pid)
    if rid not in resource_by_id:
        fail(f"{pid}: record_id inexistente: {rid}")
    if rid in by_record:
        fail(f"{rid}: mais de uma declaração de proveniência inicial")
    if item.get("agent_resolution_status") not in ALLOWED_RESOLUTION_STATUS:
        fail(f"{rid}: agent_resolution_status inválido")
    if item.get("role_resolution_status") not in ALLOWED_RESOLUTION_STATUS:
        fail(f"{rid}: role_resolution_status inválido")
    if item.get("source_field") != "owner_or_manager":
        fail(f"{rid}: source_field deve preservar a migração de owner_or_manager")

    source = resource_by_id[rid]
    if item.get("responsibility_statement") != source.get("owner_or_manager"):
        fail(f"{rid}: responsibility_statement diverge de owner_or_manager")
    if item.get("institutional_status_summary") != source.get("institutional_status"):
        fail(f"{rid}: institutional_status_summary diverge do recurso")
    if item.get("verified_at") != (source.get("last_verified") or None):
        fail(f"{rid}: verified_at da proveniência diverge do recurso")
    by_record[rid] = item

if set(by_record) != set(resource_by_id):
    fail("provenance_statements não cobre exatamente os 58 recursos vivos")

print(
    "OK version/provenance: "
    f"{len(versions)} versão(ões) promovida(s); "
    f"{len(unresolved_by_offering)} resumos legados não promovidos; "
    f"{len(statements)} declarações de proveniência preservadas sem parsing automático"
)
