#!/usr/bin/env python3
"""Constrói o read model público v2 da Vitrine Ciência.

Autoridades usadas pelo v2:
- conteúdo científico ainda compatível com o public-record-v1;
- rotas: data/access_routes.json;
- versões promovidas: data/offering_versions.json;
- declarações de proveniência: data/provenance_statements.json.

Resumos legados continuam preservados quando sua semântica ainda não justifica
criar uma entidade estruturada.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

from build_record_pages import build_public_records as build_v1_records

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "_site"
SCHEMA_PATH = ROOT / "schema" / "public-record-v2.json"
ACCESS_ROUTES_PATH = ROOT / "data" / "access_routes.json"
VERSIONS_PATH = ROOT / "data" / "offering_versions.json"
PROVENANCE_PATH = ROOT / "data" / "provenance_statements.json"

ACCESS_STATUS_LABELS = {
    "A": "Dados disponíveis diretamente",
    "B": "Página específica para obtenção de dados",
    "C": "Serviço de dados como acesso principal",
    "D": "Visualização ou página de consulta",
    "E": "Acesso ainda não confirmado",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def derived_resource_id(record_id: str) -> str:
    return f"{record_id}::resource"


def offering_from_product(
    product: dict,
    route_ids: list[str],
    version_ids: list[str],
) -> dict:
    version_summary = str(product.get("version_or_collection") or "").strip()
    return {
        "offering_id": product["product_id"],
        "name": product["name"],
        "acronym": product.get("acronym"),
        "family": product.get("family"),
        "type": {
            "id": product.get("kind"),
            "label": product.get("kind_label"),
        },
        "description": product.get("description") or "",
        "themes": {
            "research_areas": list(product.get("research_areas") or []),
            "keywords": list(product.get("keywords") or []),
        },
        "coverage": {
            "geographic": product.get("geographic_coverage") or "",
            "covers_brazil": product.get("covers_brazil") or "",
            "spatial_support": product.get("spatial_support") or "",
            "spatial_resolution": product.get("spatial_resolution") or "",
            "temporal_coverage": product.get("temporal_coverage") or "",
            "temporal_resolution": product.get("temporal_resolution") or "",
            "update_frequency": product.get("update_frequency") or "",
        },
        "status": product.get("status") or "",
        "enumeration_scope": product.get("enumeration_scope") or "",
        "primary_or_derived": product.get("primary_or_derived") or "",
        "version_or_collection_summary": version_summary or None,
        "links": {
            "product_page": product.get("product_page_url"),
            "methodology": product.get("methodology_url"),
        },
        "limitations": product.get("limitations") or "",
        "verified_at": product.get("last_verified") or None,
        "version_ids": list(version_ids),
        "access_route_ids": list(route_ids),
        "source": "legacy-product",
    }


def references_from_v1(record: dict) -> list[dict]:
    evidence = record.get("evidence") or {}
    by_url: dict[str, dict] = {}

    def add(url: str | None, role: str, ref_type: str | None = None, note: str | None = None) -> None:
        value = str(url or "").strip()
        if not value.startswith("https://"):
            return
        item = by_url.setdefault(
            value,
            {
                "url": value,
                "roles": [],
                "type": ref_type or "documentation",
                "note": note or None,
            },
        )
        if role not in item["roles"]:
            item["roles"].append(role)
        if ref_type and item.get("type") == "documentation":
            item["type"] = ref_type
        if note and not item.get("note"):
            item["note"] = note

    add(
        evidence.get("url"),
        "scientific_or_technical_evidence",
        evidence.get("type") or "scientific_or_technical_evidence",
        evidence.get("note"),
    )
    add(
        evidence.get("verification_url"),
        "verification_source",
        "verification_source",
        None,
    )

    refs = list(by_url.values())
    refs.sort(key=lambda item: item["url"])
    for index, item in enumerate(refs, start=1):
        item["reference_id"] = f"{record['resource_id']}-REF{index:02d}"
    return refs


def canonical_routes_by_record() -> dict[str, list[dict]]:
    payload = read_json(ACCESS_ROUTES_PATH)
    if payload.get("schema_version") != "access-routes-v1" or payload.get("status") != "canonical":
        raise SystemExit("ERRO: data/access_routes.json não é uma autoridade access-routes-v1 válida")
    grouped: dict[str, list[dict]] = defaultdict(list)
    for route in payload.get("routes") or []:
        grouped[route["record_id"]].append(dict(route))
    return grouped


def canonical_versions_by_offering() -> dict[str, list[dict]]:
    payload = read_json(VERSIONS_PATH)
    if payload.get("schema_version") != "offering-versions-v1" or payload.get("status") != "canonical":
        raise SystemExit("ERRO: data/offering_versions.json não é uma autoridade de versões válida")
    grouped: dict[str, list[dict]] = defaultdict(list)
    for version in payload.get("versions") or []:
        grouped[version["offering_id"]].append(dict(version))
    return grouped


def canonical_provenance_by_record() -> dict[str, dict]:
    payload = read_json(PROVENANCE_PATH)
    if payload.get("schema_version") != "provenance-v1" or payload.get("status") != "canonical_statement_layer":
        raise SystemExit("ERRO: data/provenance_statements.json não é uma camada de proveniência válida")
    return {item["record_id"]: dict(item) for item in payload.get("statements") or []}


def transform_record(
    record: dict,
    schema: dict,
    routes: list[dict],
    versions_by_offering: dict[str, list[dict]],
    provenance_statement: dict,
) -> dict:
    rid = record["resource_id"]
    resource_local_id = derived_resource_id(rid)

    resource_routes = [item for item in routes if item.get("target_type") == "resource"]
    primary_routes = [item for item in resource_routes if item.get("primary")]
    if len(primary_routes) != 1:
        raise SystemExit(f"ERRO: {rid}: access_routes canônico deve ter uma rota principal")
    primary = primary_routes[0]
    access_class = primary.get("access_assessment") or "E"

    offering_route_ids: dict[str, list[str]] = defaultdict(list)
    for route in routes:
        if route.get("target_type") == "offering":
            offering_route_ids[route["target_id"]].append(route["route_id"])

    offerings: list[dict] = []
    versions: list[dict] = []
    for product in record.get("products") or []:
        pid = product["product_id"]
        product_versions = versions_by_offering.get(pid, [])
        offerings.append(
            offering_from_product(
                product,
                offering_route_ids.get(pid, []),
                [item["version_id"] for item in product_versions],
            )
        )
        versions.extend(dict(item) for item in product_versions)

    legacy_access = record.get("access") or {}
    provenance = {
        "provenance_id": provenance_statement["provenance_id"],
        "responsibility_statement": provenance_statement["responsibility_statement"],
        "institutional_status_summary": provenance_statement["institutional_status_summary"],
        "agent_resolution_status": provenance_statement["agent_resolution_status"],
        "role_resolution_status": provenance_statement["role_resolution_status"],
        "verified_at": provenance_statement.get("verified_at"),
        "authority": "data/provenance_statements.json",
    }

    return {
        "schema_version": schema["schema_version"],
        "record": {
            "id": rid,
            "status": "published",
            "catalog": "Vitrine Ciência",
            "public_url": record["url"],
            "resource_ref": resource_local_id,
            "verified_at": (record.get("curation") or {}).get("last_verified"),
            "access_verified_at": primary.get("verified_at"),
        },
        "resource": {
            "local_id": resource_local_id,
            "identifier_status": "derived_read_model_key",
            "name": record["title"],
            "acronym": record.get("acronym"),
            "type": dict(record["public_record_type"]),
            "official_identity": record.get("official_identity") or "",
            "description": record.get("description") or "",
            "themes": {
                "broad_research_areas": list(record.get("research_areas") or []),
                "detailed_research_areas": list(record.get("research_areas_detail") or []),
                "keywords": list(record.get("keywords") or []),
            },
            "scope": dict(record.get("scope") or {}),
            "content_summary": dict(record.get("content") or {}),
            "coverage": dict(record.get("coverage") or {}),
            "access_summary": {
                "primary_class": access_class,
                "primary_status": ACCESS_STATUS_LABELS.get(access_class, "Acesso em revisão"),
                "free_download": primary.get("free_download"),
                "programmatic_access": legacy_access.get("programmatic_access"),
                "authentication_required": primary.get("authentication_required"),
                "conditions": primary.get("access_conditions"),
                "protocols": list(legacy_access.get("protocols") or []),
            },
            "use_and_limits": dict(record.get("use_and_limits") or {}),
            "institutional_status": provenance_statement["institutional_status_summary"],
            "data_sources": list((record.get("content") or {}).get("data_sources") or []),
        },
        "offerings": offerings,
        "versions": versions,
        "access_routes": [dict(item) for item in routes],
        "provenance": provenance,
        "agents": [],
        "references": references_from_v1(record),
        "curation": {
            "last_verified": (record.get("curation") or {}).get("last_verified"),
            "access_last_verified": primary.get("verified_at"),
            "access_reason": (record.get("curation") or {}).get("access_reason"),
            "migration_source_schema": record.get("schema_version"),
            "access_route_authority": "data/access_routes.json",
            "version_authority": "data/offering_versions.json",
            "provenance_authority": "data/provenance_statements.json",
            "migration_mode": "v2_content_transform_with_canonical_relations",
        },
    }


def build_public_records_v2() -> list[dict]:
    schema = read_json(SCHEMA_PATH)
    routes_by_record = canonical_routes_by_record()
    versions_by_offering = canonical_versions_by_offering()
    provenance_by_record = canonical_provenance_by_record()

    records = []
    for record in build_v1_records():
        rid = record["resource_id"]
        if rid not in routes_by_record:
            raise SystemExit(f"ERRO: {rid}: sem rotas canônicas")
        if rid not in provenance_by_record:
            raise SystemExit(f"ERRO: {rid}: sem declaração de proveniência")
        records.append(
            transform_record(
                record,
                schema,
                routes_by_record[rid],
                versions_by_offering,
                provenance_by_record[rid],
            )
        )
    return records


def build(output: Path = DEFAULT_OUTPUT) -> list[dict]:
    records = build_public_records_v2()
    target = output / "data" / "v2"
    individual = target / "registros"
    individual.mkdir(parents=True, exist_ok=True)

    (target / "public_records.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for record in records:
        rid = record["record"]["id"].lower()
        (individual / f"{rid}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(
        f"OK: {len(records)} registros public-record-v2 gerados em "
        f"{target.relative_to(output)} com relações canônicas"
    )
    return records


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT
    build(target)
