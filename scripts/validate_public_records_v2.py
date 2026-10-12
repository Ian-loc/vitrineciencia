#!/usr/bin/env python3
"""Valida a migração determinística public-record-v1 -> public-record-v2."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
V1_PATH = SITE / "data" / "public_records.json"
V2_PATH = SITE / "data" / "v2" / "public_records.json"
V2_INDIVIDUAL = SITE / "data" / "v2" / "registros"
CANONICAL = ROOT / "data" / "data_resources.csv"
SCHEMA = ROOT / "schema" / "public-record-v2.json"
ACCESS_ROUTES = ROOT / "data" / "access_routes.json"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_json(path: Path):
    if not path.exists() or path.stat().st_size == 0:
        fail(f"arquivo ausente ou vazio: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_ids() -> list[str]:
    with CANONICAL.open(encoding="utf-8-sig", newline="") as handle:
        return [row["resource_id"] for row in csv.DictReader(handle)]


schema = read_json(SCHEMA)
canonical_routes_payload = read_json(ACCESS_ROUTES)
canonical_routes_by_record = {}
for route in canonical_routes_payload.get("routes") or []:
    canonical_routes_by_record.setdefault(route["record_id"], []).append(route)

v1_records = read_json(V1_PATH)
v2_records = read_json(V2_PATH)
ids = canonical_ids()

if len(v1_records) != len(ids) or len(v2_records) != len(ids):
    fail(f"contagem v1/v2 divergente do catálogo: v1={len(v1_records)}, v2={len(v2_records)}, catálogo={len(ids)}")

v1_by_id = {item["resource_id"]: item for item in v1_records}
v2_by_id = {item["record"]["id"]: item for item in v2_records}

if set(v1_by_id) != set(ids) or set(v2_by_id) != set(ids):
    fail("conjunto de IDs v1/v2 diverge do catálogo canônico")
if len(v2_by_id) != len(v2_records):
    fail("public-record-v2 contém IDs de registro duplicados")

allowed_types = set(schema["resource_types"])
forbidden_top_level = {"resource_id", "title", "public_record_type", "products", "access", "provenance", "evidence"}

total_offerings = 0
total_distribution_routes = 0
total_versions = 0

for rid in ids:
    v1 = v1_by_id[rid]
    v2 = v2_by_id[rid]
    record = v2.get("record") or {}
    resource = v2.get("resource") or {}

    if v2.get("schema_version") != schema["schema_version"]:
        fail(f"{rid}: schema_version v2 divergente")
    leaked = forbidden_top_level.intersection(v2)
    if leaked:
        fail(f"{rid}: campos v1 vazaram no topo do v2: {sorted(leaked)}")

    if record.get("id") != rid:
        fail(f"{rid}: record.id divergente")
    if record.get("public_url") != v1.get("url"):
        fail(f"{rid}: URL pública mudou durante a migração")
    if record.get("resource_ref") != resource.get("local_id"):
        fail(f"{rid}: record.resource_ref não aponta para resource.local_id")
    if resource.get("local_id") == rid:
        fail(f"{rid}: registro e recurso continuam usando a mesma identidade")
    if resource.get("identifier_status") != "derived_read_model_key":
        fail(f"{rid}: chave do recurso não está marcada como derivada")

    if resource.get("name") != v1.get("title"):
        fail(f"{rid}: nome do recurso não preservado")
    if resource.get("acronym") != v1.get("acronym"):
        fail(f"{rid}: sigla não preservada")
    if resource.get("description") != v1.get("description"):
        fail(f"{rid}: descrição não preservada")
    if resource.get("official_identity") != v1.get("official_identity"):
        fail(f"{rid}: identidade oficial não preservada")
    if resource.get("type") != v1.get("public_record_type"):
        fail(f"{rid}: tipo público não preservado")
    if (resource.get("type") or {}).get("id") not in allowed_types:
        fail(f"{rid}: tipo de recurso inválido")

    themes = resource.get("themes") or {}
    if themes.get("broad_research_areas") != v1.get("research_areas"):
        fail(f"{rid}: áreas públicas não preservadas")
    if themes.get("detailed_research_areas") != v1.get("research_areas_detail"):
        fail(f"{rid}: áreas detalhadas não preservadas")
    if themes.get("keywords") != v1.get("keywords"):
        fail(f"{rid}: palavras-chave não preservadas")
    if resource.get("scope") != v1.get("scope"):
        fail(f"{rid}: escopo territorial não preservado")
    if resource.get("coverage") != v1.get("coverage"):
        fail(f"{rid}: cobertura não preservada")
    if resource.get("use_and_limits") != v1.get("use_and_limits"):
        fail(f"{rid}: usos/licença/limitações não preservados")

    summary = resource.get("access_summary") or {}
    v1_access = v1.get("access") or {}
    for key in (
        "primary_class", "primary_status", "free_download",
        "programmatic_access", "authentication_required", "conditions", "protocols",
    ):
        if summary.get(key) != v1_access.get(key):
            fail(f"{rid}: resumo de acesso perdeu {key}")

    offerings = v2.get("offerings") or []
    offering_by_id = {item["offering_id"]: item for item in offerings}
    v1_products = v1.get("products") or []
    v1_product_by_id = {item["product_id"]: item for item in v1_products}
    if set(offering_by_id) != set(v1_product_by_id):
        fail(f"{rid}: offerings divergem dos produtos v1")
    total_offerings += len(offerings)

    routes = v2.get("access_routes") or []
    expected_routes = canonical_routes_by_record.get(rid) or []
    if routes != expected_routes:
        fail(f"{rid}: access_routes do read model divergem da autoridade data/access_routes.json")

    resource_routes = [item for item in routes if item.get("target_type") == "resource"]
    distribution_routes = [item for item in routes if item.get("route_type") == "distribution"]
    total_distribution_routes += len(distribution_routes)

    if sum(bool(item.get("primary")) for item in resource_routes) != 1:
        fail(f"{rid}: deve haver exatamente uma rota primária do recurso")
    for route in resource_routes:
        if route.get("target_id") != resource.get("local_id"):
            fail(f"{rid}: rota do recurso aponta para alvo incorreto")
    if (v2.get("curation") or {}).get("access_route_authority") != "data/access_routes.json":
        fail(f"{rid}: autoridade de access_routes não declarada no read model")

    for pid, product in v1_product_by_id.items():
        offering = offering_by_id[pid]
        for source_key, target_path in (
            ("name", "name"),
            ("description", "description"),
            ("status", "status"),
            ("enumeration_scope", "enumeration_scope"),
            ("primary_or_derived", "primary_or_derived"),
            ("limitations", "limitations"),
        ):
            if offering.get(target_path) != product.get(source_key):
                fail(f"{rid}/{pid}: campo de offering não preservado: {source_key}")
        if offering.get("version_or_collection_summary") != (product.get("version_or_collection") or None):
            fail(f"{rid}/{pid}: resumo de versão/coleção não preservado")

        expected_dd = {item["distribution_id"] for item in product.get("distributions") or []}
        actual_dd = {
            item["route_id"] for item in distribution_routes
            if item.get("target_id") == pid
        }
        if expected_dd != actual_dd:
            fail(f"{rid}/{pid}: distribuições não preservadas como access_routes")

    versions = v2.get("versions") or []
    expected_version_products = {
        item["product_id"]
        for item in v1_products
        if str(item.get("version_or_collection") or "").strip()
    }
    actual_version_products = {item.get("offering_id") for item in versions}
    if expected_version_products != actual_version_products:
        fail(f"{rid}: versões derivadas não correspondem aos campos legados")
    for item in versions:
        if item.get("status") != "legacy_summary" or item.get("identifier_status") != "derived_migration_key":
            fail(f"{rid}: versão derivada não está marcada como resumo legado")
    total_versions += len(versions)

    owner = (v1.get("provenance") or {}).get("owner_or_manager") or ""
    agents = v2.get("agents") or []
    if bool(str(owner).strip()) != bool(agents):
        fail(f"{rid}: migração de responsável/mantenedor inconsistente")
    if agents and agents[0].get("name") != owner:
        fail(f"{rid}: nome do responsável/mantenedor não preservado")

    individual = V2_INDIVIDUAL / f"{rid.lower()}.json"
    payload = read_json(individual)
    if payload != v2:
        fail(f"{rid}: JSON individual v2 diverge do agregado")

if total_offerings != sum(len(item.get("products") or []) for item in v1_records):
    fail("contagem total de offerings diverge do v1")
if total_distribution_routes != sum(
    len(product.get("distributions") or [])
    for record in v1_records
    for product in record.get("products") or []
):
    fail("contagem total de rotas de distribuição diverge do v1")

print(
    "OK public-record-v2: "
    f"{len(v2_records)} registros; {total_offerings} offerings; "
    f"{total_versions} resumos de versão; {total_distribution_routes} distribuições preservadas; "
    "URLs/conteúdo compatíveis com v1 e access_routes idênticas à autoridade canônica"
)
