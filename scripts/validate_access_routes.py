#!/usr/bin/env python3
"""Valida a autoridade canônica de rotas de acesso da Vitrine Ciência."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
ROUTES_PATH = ROOT / "data" / "access_routes.json"
RESOURCES_PATH = ROOT / "data" / "data_resources.csv"
PRODUCTS_PATH = ROOT / "data" / "data_products.csv"
DISTRIBUTIONS_PATH = ROOT / "data" / "product_distributions.csv"
CORE_ACCESS = ROOT / "data" / "static_core_51_access_audit.json"
POST_ACCESS = ROOT / "data" / "post_core_access_audit.json"

ROLE_BY_CLASS = {
    "A": "direct_data",
    "B": "data_page",
    "C": "data_service",
    "D": "viewer",
    "E": "unconfirmed_access",
}
ALLOWED_ROUTE_TYPES = {
    "direct_data",
    "data_page",
    "data_service",
    "viewer",
    "unconfirmed_access",
    "official_site",
    "access_documentation",
    "distribution",
}
ALLOWED_ROLES = set(ALLOWED_ROUTE_TYPES)
DISTRIBUTION_FIELD_MAP = {
    "label": "distribution_name",
    "url": "access_url",
    "format": "format",
    "protocol": "access_protocol",
    "tool": "access_tool",
    "free_download": "free_download",
    "authentication_required": "authentication_required",
    "access_conditions": "access_conditions",
    "license": "license",
    "attribution_required": "provider_attribution_required",
    "subset_support": "subset_support",
    "notes": "notes",
    "verified_at": "last_verified",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path):
    if not path.exists() or path.stat().st_size == 0:
        fail(f"arquivo ausente ou vazio: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def https(value: object) -> bool:
    return str(value or "").startswith("https://")


def normalize_url(value: object) -> str:
    parsed = urlsplit(str(value or "").strip())
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


payload = read_json(ROUTES_PATH)
if payload.get("schema_version") != "access-routes-v1":
    fail("data/access_routes.json deve declarar schema_version=access-routes-v1")
if payload.get("status") != "canonical":
    fail("data/access_routes.json deve declarar status=canonical")
if payload.get("authority") != "data/access_routes.json":
    fail("data/access_routes.json não se declara como autoridade")

routes = payload.get("routes")
if not isinstance(routes, list) or not routes:
    fail("data/access_routes.json: routes deve ser lista não vazia")

resources = rows(RESOURCES_PATH)
products = rows(PRODUCTS_PATH)
distributions = rows(DISTRIBUTIONS_PATH)
resource_by_id = {row["resource_id"]: row for row in resources}
product_by_id = {row["product_id"]: row for row in products}
distribution_by_id = {row["distribution_id"]: row for row in distributions}

audit_records = []
for path in (CORE_ACCESS, POST_ACCESS):
    audit_records.extend(read_json(path).get("records") or [])
audit_by_id = {item["resource_id"]: item for item in audit_records}

if set(audit_by_id) != set(resource_by_id):
    fail("auditorias A–E não cobrem exatamente os recursos canônicos")

route_ids = [route.get("route_id") for route in routes]
if any(not item for item in route_ids):
    fail("rota sem route_id")
if len(route_ids) != len(set(route_ids)):
    fail("route_id duplicado em data/access_routes.json")

resource_routes_by_id: dict[str, list[dict]] = {rid: [] for rid in resource_by_id}
distribution_routes: dict[str, dict] = {}

for route in routes:
    route_id = route["route_id"]
    rid = route.get("record_id")
    if rid not in resource_by_id:
        fail(f"{route_id}: record_id inválido: {rid}")

    route_type = route.get("route_type")
    if route_type not in ALLOWED_ROUTE_TYPES:
        fail(f"{route_id}: route_type inválido: {route_type}")

    roles = route.get("roles")
    if not isinstance(roles, list) or not roles:
        fail(f"{route_id}: roles deve ser lista não vazia")
    unknown_roles = set(roles) - ALLOWED_ROLES
    if unknown_roles:
        fail(f"{route_id}: roles inválidos: {sorted(unknown_roles)}")
    if len(roles) != len(set(roles)):
        fail(f"{route_id}: roles duplicados")

    url = route.get("url")
    if url is not None and not https(url):
        fail(f"{route_id}: URL deve ser HTTPS ou null")

    if route.get("target_type") == "resource":
        if route.get("target_id") != f"{rid}::resource":
            fail(f"{route_id}: alvo de recurso inválido")
        if route_type == "distribution" or "distribution" in roles:
            fail(f"{route_id}: rota de recurso não pode ser distribuição")
        resource_routes_by_id[rid].append(route)
    elif route.get("target_type") == "offering":
        pid = route.get("target_id")
        product = product_by_id.get(pid)
        if not product:
            fail(f"{route_id}: offering alvo inexistente: {pid}")
        if product["resource_id"] != rid:
            fail(f"{route_id}: offering pertence a outro registro")
        if route_type != "distribution" or roles != ["distribution"]:
            fail(f"{route_id}: rota de offering deve ser distribuição")
        if route.get("primary"):
            fail(f"{route_id}: distribuição não pode ser rota principal do recurso")
        distribution_routes[route_id] = route
    else:
        fail(f"{route_id}: target_type deve ser resource ou offering")

for rid, resource in resource_by_id.items():
    current = resource_routes_by_id[rid]
    primary = [route for route in current if route.get("primary")]
    if len(primary) != 1:
        fail(f"{rid}: deve existir exatamente uma rota principal; encontrado {len(primary)}")
    primary = primary[0]

    audit = audit_by_id[rid]
    expected_class = audit["access_role"]
    if primary.get("access_assessment") != expected_class:
        fail(f"{rid}: access_assessment da rota principal diverge da auditoria")
    if primary.get("route_type") != ROLE_BY_CLASS[expected_class]:
        fail(f"{rid}: route_type da rota principal diverge da classe {expected_class}")
    if ROLE_BY_CLASS[expected_class] not in primary.get("roles", []):
        fail(f"{rid}: papel da rota principal não contém a classe funcional esperada")

    legacy_data_url = resource["data_access_url"].strip()
    if https(legacy_data_url):
        if normalize_url(primary.get("url")) != normalize_url(legacy_data_url):
            fail(f"{rid}: rota principal diverge de data_access_url durante a transição")
        if primary.get("status") != "active":
            fail(f"{rid}: rota principal HTTPS deve estar active")
    else:
        if primary.get("url") is not None:
            fail(f"{rid}: data_access_url não é HTTPS mas rota principal possui URL")
        if expected_class != "E":
            fail(f"{rid}: somente classe E pode ter rota principal sem URL")
        expected_status = "not_applicable" if legacy_data_url.lower() == "não se aplica" else "unconfirmed"
        if primary.get("status") != expected_status:
            fail(f"{rid}: status da rota sem URL deveria ser {expected_status}")

    homepage = resource["homepage_url"].strip()
    if https(homepage):
        matches = [
            route for route in current
            if "official_site" in route.get("roles", [])
            and normalize_url(route.get("url")) == normalize_url(homepage)
        ]
        if len(matches) != 1:
            fail(f"{rid}: homepage_url deve existir exatamente uma vez com papel official_site")

    access_doc = resource.get("access_documentation_url", "").strip()
    if https(access_doc):
        matches = [
            route for route in current
            if "access_documentation" in route.get("roles", [])
            and normalize_url(route.get("url")) == normalize_url(access_doc)
        ]
        if len(matches) != 1:
            fail(f"{rid}: access_documentation_url deve existir exatamente uma vez")

    seen_urls: set[str] = set()
    for route in current:
        if route.get("url"):
            key = normalize_url(route["url"])
            if key in seen_urls:
                fail(f"{rid}: mesma URL aparece em mais de uma rota de recurso")
            seen_urls.add(key)
        if {"scientific_reference", "verification_source"} & set(route.get("roles", [])):
            fail(f"{rid}: referência/evidência vazou para access_routes")

if set(distribution_routes) != set(distribution_by_id):
    missing = sorted(set(distribution_by_id) - set(distribution_routes))
    extra = sorted(set(distribution_routes) - set(distribution_by_id))
    fail(f"rotas de distribuição divergem dos DD canônicos; ausentes={missing}, extras={extra}")

for ddid, source in distribution_by_id.items():
    route = distribution_routes[ddid]
    product = product_by_id[source["product_id"]]
    if route.get("record_id") != product["resource_id"]:
        fail(f"{ddid}: record_id incompatível com o produto")
    if route.get("target_id") != source["product_id"]:
        fail(f"{ddid}: target_id incompatível com product_id")
    for route_field, source_field in DISTRIBUTION_FIELD_MAP.items():
        expected = source[source_field].strip() or None
        actual = route.get(route_field)
        if actual != expected:
            fail(
                f"{ddid}: {route_field} diverge de {source_field}; "
                f"rota={actual!r}, canônico={expected!r}"
            )
    if route.get("status") != ("active" if https(source["access_url"]) else "unconfirmed"):
        fail(f"{ddid}: status incompatível com access_url")

baseline = payload.get("migration_baseline") or {}
expected_counts = {
    "resources": len(resources),
    "offerings": len(products),
    "distributions": len(distributions),
    "resource_routes": sum(len(items) for items in resource_routes_by_id.values()),
    "total_routes": len(routes),
}
for key, expected in expected_counts.items():
    if baseline.get(key) != expected:
        fail(f"migration_baseline.{key}={baseline.get(key)!r}; esperado {expected}")

primary_counts = {
    cls: sum(
        1
        for current in resource_routes_by_id.values()
        for route in current
        if route.get("primary") and route.get("access_assessment") == cls
    )
    for cls in ROLE_BY_CLASS
}
if primary_counts != {"A": 2, "B": 39, "C": 0, "D": 14, "E": 3}:
    fail(f"contagens A–E inesperadas: {primary_counts}")

print(
    "OK access-routes-v1: "
    f"{len(routes)} rotas canônicas; "
    f"{expected_counts['resource_routes']} no nível do recurso; "
    f"{len(distribution_routes)} distribuições; "
    f"A–E={primary_counts}"
)
