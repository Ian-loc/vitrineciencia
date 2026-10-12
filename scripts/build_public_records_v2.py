#!/usr/bin/env python3
"""Constrói o read model público v2 a partir do public-record-v1.

A transformação é deliberadamente determinística:
- não recataloga os 58 registros;
- não altera URLs públicas;
- não cria novos produtos;
- não transforma inferências em fatos novos.

O objetivo é separar Registro da Vitrine e Recurso catalogado e fornecer
o read model usado tanto pelos JSONs públicos quanto pelo renderer HTML v2.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from build_record_pages import build_public_records as build_v1_records

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "_site"
SCHEMA_PATH = ROOT / "schema" / "public-record-v2.json"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def derived_resource_id(record_id: str) -> str:
    return f"{record_id}::resource"


def resource_route(route: dict, record_id: str) -> dict:
    return {
        "route_id": route["route_id"],
        "target_type": "resource",
        "target_id": derived_resource_id(record_id),
        "route_type": "resource_access",
        "roles": list(route.get("roles") or []),
        "label": route.get("label") or "",
        "url": route.get("url"),
        "primary": bool(route.get("primary")),
        "access_assessment": route.get("access_class"),
        "protocol": None,
        "format": None,
        "tool": None,
        "free_download": None,
        "authentication_required": None,
        "access_conditions": None,
        "license": None,
        "attribution_required": None,
        "subset_support": None,
        "notes": route.get("note"),
        "verified_at": route.get("verified_at"),
        "source": "public-record-v1-derived",
    }


def distribution_route(distribution: dict, offering_id: str) -> dict:
    return {
        "route_id": distribution["distribution_id"],
        "target_type": "offering",
        "target_id": offering_id,
        "route_type": "distribution",
        "roles": ["distribution"],
        "label": distribution.get("name") or "Forma de acesso",
        "url": distribution.get("url") or None,
        "primary": False,
        "access_assessment": None,
        "protocol": distribution.get("protocol") or None,
        "format": distribution.get("format") or None,
        "tool": distribution.get("tool") or None,
        "free_download": distribution.get("free_download") or None,
        "authentication_required": distribution.get("authentication_required") or None,
        "access_conditions": distribution.get("access_conditions") or None,
        "license": distribution.get("license") or None,
        "attribution_required": distribution.get("attribution_required") or None,
        "subset_support": distribution.get("subset_support") or None,
        "notes": distribution.get("notes") or None,
        "verified_at": distribution.get("last_verified") or None,
        "source": "legacy-distribution",
    }


def offering_from_product(product: dict) -> tuple[dict, list[dict], list[dict]]:
    offering_id = product["product_id"]
    access_routes = [
        distribution_route(item, offering_id)
        for item in product.get("distributions") or []
    ]
    distribution_ids = [item["route_id"] for item in access_routes]

    versions: list[dict] = []
    version_summary = str(product.get("version_or_collection") or "").strip()
    if version_summary:
        versions.append(
            {
                "version_id": f"{offering_id}::legacy-version",
                "offering_id": offering_id,
                "identifier_status": "derived_migration_key",
                "label": version_summary,
                "issued": None,
                "relation": None,
                "status": "legacy_summary",
                "source_field": "version_or_collection",
            }
        )

    offering = {
        "offering_id": offering_id,
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
        "version_ids": [item["version_id"] for item in versions],
        "access_route_ids": distribution_ids,
        "source": "legacy-product",
    }
    return offering, versions, access_routes


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


def transform_record(record: dict, schema: dict) -> dict:
    rid = record["resource_id"]
    resource_local_id = derived_resource_id(rid)

    offerings: list[dict] = []
    versions: list[dict] = []
    access_routes = [
        resource_route(route, rid)
        for route in (record.get("access") or {}).get("routes") or []
    ]

    for product in record.get("products") or []:
        offering, product_versions, product_routes = offering_from_product(product)
        offerings.append(offering)
        versions.extend(product_versions)
        access_routes.extend(product_routes)

    owner = (record.get("provenance") or {}).get("owner_or_manager") or ""
    agents = []
    if str(owner).strip():
        agents.append(
            {
                "agent_id": f"{rid}-A01",
                "name": owner,
                "roles": ["responsible_or_maintainer"],
                "institutional_status": (record.get("provenance") or {}).get("institutional_status") or "",
                "source": "legacy-owner_or_manager",
            }
        )

    return {
        "schema_version": schema["schema_version"],
        "record": {
            "id": rid,
            "status": "published",
            "catalog": "Vitrine Ciência",
            "public_url": record["url"],
            "resource_ref": resource_local_id,
            "verified_at": (record.get("curation") or {}).get("last_verified"),
            "access_verified_at": (record.get("curation") or {}).get("access_last_verified"),
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
                "primary_class": (record.get("access") or {}).get("primary_class"),
                "primary_status": (record.get("access") or {}).get("primary_status"),
                "free_download": (record.get("access") or {}).get("free_download"),
                "programmatic_access": (record.get("access") or {}).get("programmatic_access"),
                "authentication_required": (record.get("access") or {}).get("authentication_required"),
                "conditions": (record.get("access") or {}).get("conditions"),
                "protocols": list((record.get("access") or {}).get("protocols") or []),
            },
            "use_and_limits": dict(record.get("use_and_limits") or {}),
            "institutional_status": (record.get("provenance") or {}).get("institutional_status") or "",
            "data_sources": list((record.get("content") or {}).get("data_sources") or []),
        },
        "offerings": offerings,
        "versions": versions,
        "access_routes": access_routes,
        "agents": agents,
        "references": references_from_v1(record),
        "curation": {
            "last_verified": (record.get("curation") or {}).get("last_verified"),
            "access_last_verified": (record.get("curation") or {}).get("access_last_verified"),
            "access_reason": (record.get("curation") or {}).get("access_reason"),
            "migration_source_schema": record.get("schema_version"),
            "migration_mode": "deterministic_read_model_transform",
        },
    }


def build_public_records_v2() -> list[dict]:
    schema = read_json(SCHEMA_PATH)
    return [transform_record(record, schema) for record in build_v1_records()]


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
        f"{target.relative_to(output)}"
    )
    return records


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT
    build(target)
