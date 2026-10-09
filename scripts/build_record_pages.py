#!/usr/bin/env python3
"""Gera a camada pública estática de registros da Vitrine Ciência.

A unidade pública é o registro DR. Produtos, distribuições, serviços, visualizadores
e documentos permanecem subordinados ao registro e não geram páginas próprias
nesta camada.
"""
from __future__ import annotations

import csv
import html
import json
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE_BASE = "https://ian-loc.github.io/vitrineciencia/"
DEFAULT_OUTPUT = ROOT / "_site"

RESOURCE_CSV = ROOT / "data" / "data_resources.csv"
PRODUCT_CSV = ROOT / "data" / "data_products.csv"
DISTRIBUTION_CSV = ROOT / "data" / "product_distributions.csv"
SEMANTIC = ROOT / "data" / "static_core_51_progress.json"
CORE_ACCESS = ROOT / "data" / "static_core_51_access_audit.json"
POST_ACCESS = ROOT / "data" / "post_core_access_audit.json"
BRAZIL_SCOPE = ROOT / "data" / "brazil_scope_priorities.json"
PUBLIC_DISCOVERY = ROOT / "schema" / "public-discovery-v0.1.json"
PUBLIC_RECORD_SCHEMA = ROOT / "schema" / "public-record-v1.json"

STATUS_LABELS = {
    "sim": "Sim",
    "não": "Não",
    "parcial": "Parcial",
    "desconhecido": "Não confirmado",
    "não se aplica": "Não se aplica",
}
ACCESS_STATUS_LABELS = {
    "A": "Dados disponíveis diretamente",
    "B": "Página específica para obtenção de dados",
    "C": "Serviço de dados como acesso principal",
    "D": "Visualização ou página de consulta",
    "E": "Acesso ainda não confirmado",
}
PRODUCT_KIND_LABELS = {
    "dataset": "Conjunto de dados",
    "dataset_series": "Série de conjuntos de dados",
    "catalog": "Catálogo",
    "federated_catalog": "Catálogo federado",
    "data_service": "Serviço de dados",
    "indicator_family": "Família de indicadores",
    "map_layer_collection": "Coleção de camadas",
    "software_output": "Saída de software",
}
PRIMARY_OR_DERIVED_LABELS = {
    "primário": "Dado primário",
    "derivado": "Dado derivado",
    "agregador": "Agregador",
    "serviço": "Serviço",
    "misto": "Misto",
    "desconhecido": "Não confirmado",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def split_pipe(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split("|") if item.strip()]


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def display_status(value: str) -> str:
    return STATUS_LABELS.get(str(value or "").strip().lower(), str(value or "Não informado"))


def route_path(resource_id: str) -> str:
    return f"registros/{resource_id.lower()}/"


def absolute_record_url(resource_id: str) -> str:
    return SITE_BASE + route_path(resource_id)


def broad_areas(value: str, discovery_schema: dict) -> list[str]:
    mapping = discovery_schema["source_area_groups"]
    result: list[str] = []
    for item in split_pipe(value):
        public = mapping.get(item, item)
        if public not in result:
            result.append(public)
    return result


def type_for(resource_id: str, semantic_by_id: dict[str, dict], schema: dict) -> tuple[str, str]:
    overrides = schema.get("curated_overrides", {})
    type_id = overrides.get(resource_id)
    if not type_id:
        semantic = semantic_by_id.get(resource_id)
        if not semantic:
            fail(f"{resource_id}: tipagem pública ausente")
        internal = semantic.get("entity_type")
        type_id = schema.get("entity_type_mapping", {}).get(internal)
        if not type_id:
            fail(f"{resource_id}: entity_type sem mapeamento público: {internal}")
    info = schema["public_record_types"].get(type_id)
    if not info:
        fail(f"{resource_id}: tipo público desconhecido: {type_id}")
    return type_id, info["label"]


def scope_index(payload: dict) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for tier in payload.get("tiers", []):
        for rid in tier.get("resource_ids", []):
            result[rid] = {
                "priority_tier": tier.get("priority_tier"),
                "label": tier.get("display_label"),
                "scope_class": tier.get("brazil_scope_class"),
                "source_origin": tier.get("source_origin"),
                "inclusion_role": tier.get("inclusion_role"),
            }
    return result


def merge_route(
    routes_by_url: dict[str, dict],
    *,
    url: str,
    role: str,
    label: str,
    primary: bool = False,
    access_class: str | None = None,
    verified_at: str = "",
) -> None:
    url = str(url or "").strip()
    if not url.startswith("https://"):
        return
    route = routes_by_url.setdefault(
        url,
        {
            "url": url,
            "roles": [],
            "labels": [],
            "label": label,
            "primary": False,
            "access_class": None,
            "verified_at": verified_at or None,
        },
    )
    if role not in route["roles"]:
        route["roles"].append(role)
    if label not in route["labels"]:
        route["labels"].append(label)
    if primary:
        route["primary"] = True
        route["label"] = label
        route["access_class"] = access_class
    elif not route["primary"] and role == "official_site":
        route["label"] = label
    if verified_at and not route.get("verified_at"):
        route["verified_at"] = verified_at


def build_routes(resource: dict[str, str], audit: dict, schema: dict) -> list[dict]:
    access_class = str(audit.get("access_role") or "E")
    role_by_class = {"A": "direct_data", "B": "data_page", "C": "data_service", "D": "viewer", "E": "unconfirmed_access"}
    primary_role = role_by_class.get(access_class, "unconfirmed_access")
    route_types = schema["access_route_types"]
    verified = str(audit.get("source_last_verified") or resource.get("last_verified") or "")
    routes_by_url: dict[str, dict] = {}

    merge_route(
        routes_by_url,
        url=resource.get("data_access_url", ""),
        role=primary_role,
        label=route_types[primary_role]["label"],
        primary=True,
        access_class=access_class,
        verified_at=verified,
    )
    merge_route(
        routes_by_url,
        url=resource.get("homepage_url", ""),
        role="official_site",
        label=route_types["official_site"]["label"],
        verified_at=verified,
    )
    merge_route(
        routes_by_url,
        url=resource.get("access_documentation_url", ""),
        role="access_documentation",
        label=route_types["access_documentation"]["label"],
        verified_at=verified,
    )
    merge_route(
        routes_by_url,
        url=resource.get("academic_evidence_url", ""),
        role="scientific_reference",
        label=route_types["scientific_reference"]["label"],
        verified_at=verified,
    )
    merge_route(
        routes_by_url,
        url=resource.get("verification_url", ""),
        role="verification_source",
        label=route_types["verification_source"]["label"],
        verified_at=verified,
    )

    routes = list(routes_by_url.values())
    routes.sort(key=lambda item: (not item["primary"], "official_site" not in item["roles"], item["url"]))
    for index, route in enumerate(routes, start=1):
        route["route_id"] = f"{resource['resource_id']}-R{index:02d}"
    return routes


def distributions_by_product() -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for item in read_csv(DISTRIBUTION_CSV):
        grouped[item["product_id"]].append(item)
    return grouped


def products_by_resource() -> dict[str, list[dict]]:
    distributions = distributions_by_product()
    grouped: dict[str, list[dict]] = defaultdict(list)
    for product in read_csv(PRODUCT_CSV):
        enriched = dict(product)
        enriched["distributions"] = distributions.get(product["product_id"], [])
        grouped[product["resource_id"]].append(enriched)
    return grouped


def public_product(product: dict) -> dict:
    return {
        "product_id": product["product_id"],
        "name": product["product_name"],
        "acronym": product.get("product_acronym") or None,
        "family": product.get("product_family") or None,
        "kind": product.get("product_kind") or None,
        "kind_label": PRODUCT_KIND_LABELS.get(product.get("product_kind", ""), product.get("product_kind") or "Item de dados"),
        "description": product.get("product_description") or "",
        "research_areas": split_pipe(product.get("research_areas", "")),
        "keywords": split_pipe(product.get("keywords", "")),
        "geographic_coverage": product.get("geographic_coverage") or "",
        "covers_brazil": product.get("covers_brazil") or "",
        "spatial_support": product.get("spatial_support") or "",
        "spatial_resolution": product.get("spatial_resolution") or "",
        "temporal_coverage": product.get("temporal_coverage") or "",
        "temporal_resolution": product.get("temporal_resolution") or "",
        "update_frequency": product.get("update_frequency") or "",
        "status": product.get("product_status") or "",
        "version_or_collection": product.get("version_or_collection") or "",
        "enumeration_scope": product.get("enumeration_scope") or "",
        "product_page_url": product.get("product_page_url") or None,
        "methodology_url": product.get("methodology_url") or None,
        "primary_or_derived": product.get("primary_or_derived") or "",
        "limitations": product.get("limitations") or "",
        "last_verified": product.get("last_verified") or "",
        "distributions": [
            {
                "distribution_id": item["distribution_id"],
                "name": item.get("distribution_name") or "",
                "url": item.get("access_url") or "",
                "format": item.get("format") or "",
                "protocol": item.get("access_protocol") or "",
                "tool": item.get("access_tool") or "",
                "free_download": item.get("free_download") or "",
                "authentication_required": item.get("authentication_required") or "",
                "access_conditions": item.get("access_conditions") or "",
                "license": item.get("license") or "",
                "attribution_required": item.get("provider_attribution_required") or "",
                "subset_support": item.get("subset_support") or "",
                "notes": item.get("notes") or "",
                "last_verified": item.get("last_verified") or "",
            }
            for item in product.get("distributions", [])
        ],
    }


def build_public_records() -> list[dict]:
    resources = read_csv(RESOURCE_CSV)
    semantic_by_id = {item["resource_id"]: item for item in read_json(SEMANTIC).get("records", [])}
    schema = read_json(PUBLIC_RECORD_SCHEMA)
    discovery = read_json(PUBLIC_DISCOVERY)
    scope_by_id = scope_index(read_json(BRAZIL_SCOPE))
    audit_by_id: dict[str, dict] = {}
    for path in (CORE_ACCESS, POST_ACCESS):
        for item in read_json(path).get("records", []):
            audit_by_id[item["resource_id"]] = item
    product_groups = products_by_resource()

    records: list[dict] = []
    for resource in resources:
        rid = resource["resource_id"]
        if rid not in audit_by_id:
            fail(f"{rid}: classificação de acesso ausente")
        if rid not in scope_by_id:
            fail(f"{rid}: classificação territorial ausente")
        type_id, type_label = type_for(rid, semantic_by_id, schema)
        audit = audit_by_id[rid]
        detailed_products = [public_product(item) for item in product_groups.get(rid, [])]
        records.append(
            {
                "schema_version": schema["schema_version"],
                "resource_id": rid,
                "url": absolute_record_url(rid),
                "title": resource["resource_name"],
                "acronym": resource.get("acronym") or None,
                "public_record_type": {"id": type_id, "label": type_label},
                "official_identity": resource["official_identity"],
                "description": resource["description"],
                "research_areas": broad_areas(resource["research_areas"], discovery),
                "research_areas_detail": split_pipe(resource["research_areas"]),
                "keywords": split_pipe(resource["keywords"]),
                "scope": scope_by_id[rid],
                "content": {
                    "product_types": split_pipe(resource["data_product_types"]),
                    "formats": split_pipe(resource["data_formats"]),
                    "visualizations": split_pipe(resource["visualization_types"]),
                    "data_sources": split_pipe(resource["data_sources"]),
                },
                "coverage": {
                    "geographic": resource["geographic_coverage"],
                    "covers_brazil": resource["covers_brazil"],
                    "spatial_resolution": resource["spatial_resolution"],
                    "temporal_coverage": resource["temporal_coverage"],
                    "temporal_resolution": resource["temporal_resolution"],
                },
                "access": {
                    "primary_class": audit["access_role"],
                    "primary_status": ACCESS_STATUS_LABELS[audit["access_role"]],
                    "free_download": resource["free_download"],
                    "programmatic_access": resource["programmatic_access"],
                    "authentication_required": resource["authentication_required"],
                    "conditions": resource["access_conditions"],
                    "protocols": split_pipe(resource["access_protocols"]),
                    "routes": build_routes(resource, audit, schema),
                },
                "products": detailed_products,
                "provenance": {
                    "institutional_status": resource["institutional_status"],
                    "owner_or_manager": resource["owner_or_manager"],
                },
                "use_and_limits": {
                    "academic_uses": resource["academic_uses"],
                    "limitations": resource["limitations"],
                    "license": resource["license"],
                },
                "evidence": {
                    "type": resource["academic_evidence_type"],
                    "url": resource["academic_evidence_url"],
                    "note": resource["academic_evidence_note"],
                    "verification_url": resource["verification_url"],
                },
                "curation": {
                    "last_verified": resource["last_verified"],
                    "access_last_verified": audit.get("source_last_verified") or None,
                    "access_reason": audit.get("reason") or None,
                },
            }
        )
    if len(records) != len(resources):
        fail("contagem de registros públicos divergente")
    return records


def tags(items: list[str]) -> str:
    if not items:
        return ""
    return '<ul class="tag-list">' + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def fact(label: str, value: object) -> str:
    if value is None or str(value).strip() == "":
        value = "Não informado"
    return f'<dl class="record-fact"><dt>{esc(label)}</dt><dd>{esc(value)}</dd></dl>'


def external_link(label: str, url: str, class_name: str = "") -> str:
    if not str(url or "").startswith("https://"):
        return ""
    klass = f' class="{esc(class_name)}"' if class_name else ""
    return f'<a{klass} href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)} <span aria-hidden="true">↗</span><span class="sr-only"> (abre em nova aba)</span></a>'


def route_cards(record: dict) -> str:
    access = record["access"]
    blocks: list[str] = []
    for route in access["routes"]:
        if not any(role in route["roles"] for role in ("direct_data", "data_page", "data_service", "viewer", "unconfirmed_access", "official_site", "access_documentation")):
            continue
        classes = "route-card primary-route" if route["primary"] else "route-card"
        role_labels = [label for role, label in (
            ("official_site", "Site oficial"),
            ("access_documentation", "Documentação de acesso"),
            ("direct_data", "Dados"),
            ("data_page", "Página de dados"),
            ("data_service", "Serviço de dados"),
            ("viewer", "Visualização"),
            ("unconfirmed_access", "Acesso em revisão"),
        ) if role in route["roles"]]
        blocks.append(
            f'<article class="{classes}">'
            f'<strong>{esc(route["label"])}</strong>'
            f'<div class="route-meta">{"".join(f"<span>{esc(item)}</span>" for item in role_labels)}</div>'
            f'<div class="route-actions">{external_link(route["label"], route["url"])}</div>'
            f'</article>'
        )
    return '<div class="route-list">' + "".join(blocks) + "</div>"


def distribution_html(item: dict) -> str:
    facts = []
    if item.get("format"):
        facts.append(f"<span>Formato: {esc(item['format'])}</span>")
    if item.get("protocol"):
        facts.append(f"<span>Acesso: {esc(item['protocol'])}</span>")
    if item.get("free_download"):
        facts.append(f"<span>Download gratuito: {esc(display_status(item['free_download']))}</span>")
    if item.get("authentication_required"):
        facts.append(f"<span>Credencial: {esc(display_status(item['authentication_required']))}</span>")
    link = external_link("Acessar esta distribuição", item.get("url") or "")
    notes = "".join(
        f"<p><strong>{esc(label)}:</strong> {esc(value)}</p>"
        for label, value in (
            ("Condições", item.get("access_conditions")),
            ("Licença", item.get("license")),
            ("Observações", item.get("notes")),
        )
        if value
    )
    return (
        '<div class="distribution">'
        f'<strong>{esc(item.get("name") or "Forma de acesso")}</strong>'
        f'<div class="route-meta">{"".join(facts)}</div>'
        f'{notes}'
        f'<div class="route-actions">{link}</div>'
        '</div>'
    )


def product_html(product: dict) -> str:
    meta = [
        f"<span>{esc(product['kind_label'])}</span>",
        f"<span>{esc(PRIMARY_OR_DERIVED_LABELS.get(product.get('primary_or_derived', ''), product.get('primary_or_derived') or 'Natureza não confirmada'))}</span>",
    ]
    if product.get("version_or_collection"):
        meta.append(f"<span>Versão/coleção: {esc(product['version_or_collection'])}</span>")
    facts = "".join(
        [
            fact("Cobertura geográfica", product.get("geographic_coverage")),
            fact("Suporte espacial", product.get("spatial_support")),
            fact("Resolução espacial", product.get("spatial_resolution")),
            fact("Período coberto", product.get("temporal_coverage")),
            fact("Resolução temporal", product.get("temporal_resolution")),
            fact("Atualização", product.get("update_frequency")),
        ]
    )
    links = " ".join(
        item
        for item in (
            external_link("Abrir página do produto", product.get("product_page_url") or ""),
            external_link("Ver metodologia", product.get("methodology_url") or ""),
        )
        if item
    )
    distributions = "".join(distribution_html(item) for item in product.get("distributions", []))
    return (
        '<article class="record-product">'
        f'<h3>{esc(product["name"])}</h3>'
        f'<div class="route-meta">{"".join(meta)}</div>'
        f'<p>{esc(product.get("description") or "")}</p>'
        f'<div class="record-grid">{facts}</div>'
        + (f'<p><strong>Cuidados específicos:</strong> {esc(product["limitations"])}</p>' if product.get("limitations") else "")
        + (f'<div class="record-footer-actions">{links}</div>' if links else "")
        + (f'<div class="distribution-list"><h4>Formas de acesso registradas</h4>{distributions}</div>' if distributions else "")
        + '</article>'
    )


def nav_link(anchor: str, label: str) -> str:
    return f'<a href="#{esc(anchor)}">{esc(label)}</a>'


def render_record_page(record: dict) -> str:
    rid = record["resource_id"]
    canonical = record["url"]
    title = record["title"]
    description = record["description"]
    json_ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": f"{title} · Vitrine Ciência",
            "url": canonical,
            "inLanguage": "pt-BR",
            "about": {"@type": "Thing", "name": title, "identifier": rid},
            "isPartOf": {"@type": "DataCatalog", "name": "Vitrine Ciência", "url": SITE_BASE},
        },
        ensure_ascii=False,
    )
    products = record["products"]
    product_section = (
        '<div class="product-list">' + "".join(product_html(item) for item in products) + "</div>"
        if products
        else (
            '<p class="notice">A Vitrine ainda não enumera produtos, coleções ou releases deste registro como itens detalhados. '
            'O resumo abaixo descreve o que foi verificado no nível do registro; novas entidades poderão ser vinculadas aqui sem criar outra página pública.</p>'
        )
    )
    product_compare = (
        f'<p><a href="../../products.html?source={quote(title)}">Comparar estes produtos na visão detalhada da Vitrine →</a></p>'
        if products
        else ""
    )

    reference_links = []
    for route in record["access"]["routes"]:
        if "scientific_reference" in route["roles"]:
            reference_links.append(external_link("Ver referência científica ou técnica", route["url"]))
        if "verification_source" in route["roles"] and "scientific_reference" not in route["roles"]:
            reference_links.append(external_link("Ver fonte usada na verificação", route["url"]))
    reference_links = list(dict.fromkeys(reference_links))

    nav = "".join(
        [
            nav_link("sobre", "Sobre"),
            nav_link("acesso", "Como acessar"),
            nav_link("conteudos", "Conteúdos"),
            nav_link("cobertura", "Cobertura"),
            nav_link("produtos", "Produtos e releases"),
            nav_link("uso-em-pesquisa", "Uso em pesquisa"),
            nav_link("limitacoes", "Cuidados e limitações"),
            nav_link("proveniencia", "Proveniência"),
            nav_link("condicoes-de-uso", "Condições de uso"),
            nav_link("referencias", "Referências"),
            nav_link("curadoria", "Curadoria"),
        ]
    )

    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Vitrine Ciência">
<meta property="og:title" content="{esc(title)} · Vitrine Ciência">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(title)} · Vitrine Ciência">
<meta name="twitter:description" content="{esc(description)}">
<meta name="theme-color" content="#173f32">
<meta name="color-scheme" content="light">
<title>{esc(title)} · Vitrine Ciência</title>
<link rel="stylesheet" href="../../assets/style.css">
<link rel="stylesheet" href="../../assets/accessibility.css">
<link rel="stylesheet" href="../../assets/visual-refinement.css">
<link rel="stylesheet" href="../../assets/ux-v2.css">
<link rel="stylesheet" href="../../assets/ux-simple.css">
<link rel="stylesheet" href="../../assets/record-page.css">
<script type="application/ld+json">{json_ld}</script>
</head>
<body class="record-page">
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<nav class="site-nav" aria-label="Navegação principal"><div class="wrap nav-inner">
<a class="brand" href="../../index.html" aria-label="Vitrine Ciência — página inicial"><span>Vitrine Ciência</span><small>dados científicos sobre o Brasil</small></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav-links"><span aria-hidden="true">☰</span><span>Menu</span></button>
<div class="nav-links" id="site-nav-links"><a href="../../sources.html">Explorar dados</a><a href="../../products.html">Dados detalhados</a><span class="nav-about"><a href="../../about.html">Sobre a Vitrine</a><a class="nav-sub" href="../../analytics.html">Sobre o acervo</a></span></div>
</div></nav>
<header class="record-hero"><div class="wrap">
<p class="record-breadcrumbs"><a href="../../index.html">Vitrine Ciência</a> › <a href="../../sources.html">Explorar dados</a> › {esc(rid)}</p>
<div class="record-kicker"><span class="record-id">{esc(rid)}</span><span class="record-type">{esc(record["public_record_type"]["label"])}</span><span class="record-scope">{esc(record["scope"]["label"])}</span></div>
<h1>{esc(title)}</h1>
<p class="record-identity">{esc(record["official_identity"])}</p>
<p class="record-lead">{esc(description)}</p>
</div></header>
<main id="conteudo" class="wrap record-layout">
<div class="record-content">
<section class="record-section" id="sobre"><h2>Sobre este registro</h2>
<p>Esta página reúne as informações que a Vitrine Ciência mantém para este registro. Produtos, coleções, releases, distribuições, serviços e documentos vinculados aparecem subordinados aqui; eles não criam páginas públicas independentes por padrão.</p>
<h3>Áreas de pesquisa</h3>{tags(record["research_areas"])}
<h3>Termos relacionados</h3>{tags(record["keywords"])}
</section>

<section class="record-section" id="acesso"><h2>Como acessar</h2>
<p><strong>Situação da rota principal:</strong> {esc(record["access"]["primary_status"])}</p>
{route_cards(record)}
<div class="record-grid">
{fact("Download gratuito", display_status(record["access"]["free_download"]))}
{fact("Acesso automatizado", display_status(record["access"]["programmatic_access"]))}
{fact("Cadastro ou credencial", display_status(record["access"]["authentication_required"]))}
{fact("Formas técnicas de acesso", " · ".join(record["access"]["protocols"]) or "Não documentado")}
</div>
<p><strong>Condições de acesso:</strong> {esc(record["access"]["conditions"])}</p>
</section>

<section class="record-section" id="conteudos"><h2>O que você encontra aqui</h2>
<h3>Tipos de conteúdo</h3>{tags(record["content"]["product_types"])}
<h3>Formatos de dados</h3>{tags(record["content"]["formats"])}
<h3>Formas de visualização</h3>{tags(record["content"]["visualizations"])}
</section>

<section class="record-section" id="cobertura"><h2>Cobertura espacial e temporal</h2>
<div class="record-grid">
{fact("Cobertura geográfica", record["coverage"]["geographic"])}
{fact("Dados sobre o Brasil", display_status(record["coverage"]["covers_brazil"]))}
{fact("Resolução ou escala espacial", record["coverage"]["spatial_resolution"])}
{fact("Período coberto", record["coverage"]["temporal_coverage"])}
{fact("Resolução temporal", record["coverage"]["temporal_resolution"])}
</div>
<p class="record-meta-note">Quando um produto detalhado possui informação espacial ou temporal mais específica, ela prevalece sobre este resumo geral do registro.</p>
</section>

<section class="record-section" id="produtos"><h2>Produtos, coleções e releases descritos em detalhe</h2>
{product_section}{product_compare}
</section>

<section class="record-section" id="uso-em-pesquisa"><h2>Possibilidades de uso em pesquisa</h2><p>{esc(record["use_and_limits"]["academic_uses"])}</p></section>

<section class="record-section" id="limitacoes"><h2>Cuidados e limitações</h2><p>{esc(record["use_and_limits"]["limitations"])}</p></section>

<section class="record-section" id="proveniencia"><h2>Proveniência</h2>
<div class="record-grid">
{fact("Responsável ou mantenedor", record["provenance"]["owner_or_manager"])}
{fact("Natureza institucional", record["provenance"]["institutional_status"])}
</div>
<h3>Principais fontes e insumos</h3>{tags(record["content"]["data_sources"])}
</section>

<section class="record-section" id="condicoes-de-uso"><h2>Condições de uso e licença</h2><p>{esc(record["use_and_limits"]["license"])}</p>
<p class="record-meta-note">A licença registrada aqui é um resumo no nível do registro. Produtos e distribuições podem possuir condições próprias e, quando verificadas, essas condições específicas prevalecem.</p>
</section>

<section class="record-section" id="referencias"><h2>Referências e documentação</h2>
<div class="record-reference">
<p><strong>Tipo de referência:</strong> {esc(record["evidence"]["type"])}</p>
<p>{esc(record["evidence"]["note"])}</p>
<div class="record-footer-actions">{" ".join(reference_links)}</div>
</div>
</section>

<section class="record-section" id="curadoria"><h2>Curadoria da Vitrine</h2>
<div class="record-grid">
{fact("Identificador do registro", rid)}
{fact("Tipo público do registro", record["public_record_type"]["label"])}
{fact("Registro revisado em", record["curation"]["last_verified"])}
{fact("Acesso verificado em", record["curation"]["access_last_verified"] or "Não informado")}
</div>
<p class="record-meta-note">“Não confirmado” significa que a Vitrine não encontrou evidência suficiente na revisão registrada; não significa que o recurso inexista.</p>
<p class="record-meta-note">Esta página usa um snapshot estático curado. A futura integração por API poderá atualizar este registro de forma assíncrona, sem tornar a disponibilidade desta página dependente da API externa.</p>
</section>
</div>
<aside class="record-nav" aria-label="Nesta página"><strong>Nesta página</strong>{nav}</aside>
</main>
<footer class="wrap"><p><strong>Vitrine Ciência</strong> · <a href="../../sources.html">Explorar dados</a> · <a href="../../products.html">Dados detalhados</a> · <a href="../../about.html">Sobre</a></p><p>Brasil · Registro curado pela Vitrine Ciência</p></footer>
<script src="../../assets/navigation.js" defer></script>
</body></html>
'''


def build_sitemap(output: Path, records: list[dict]) -> None:
    base_urls = [
        SITE_BASE,
        SITE_BASE + "products.html",
        SITE_BASE + "products-list.html",
        SITE_BASE + "sources.html",
        SITE_BASE + "about.html",
        SITE_BASE + "analytics.html",
        SITE_BASE + "analytics-products.html",
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in base_urls:
        lines.append(f"  <url><loc>{html.escape(url)}</loc></url>")
    for record in records:
        lastmod = record["curation"].get("last_verified")
        suffix = f"<lastmod>{esc(lastmod)}</lastmod>" if lastmod else ""
        lines.append(f"  <url><loc>{html.escape(record['url'])}</loc>{suffix}</url>")
    lines.append("</urlset>")
    (output / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build(output: Path = DEFAULT_OUTPUT) -> list[dict]:
    records = build_public_records()
    data_dir = output / "data"
    record_data_dir = data_dir / "registros"
    record_data_dir.mkdir(parents=True, exist_ok=True)
    page_root = output / "registros"
    page_root.mkdir(parents=True, exist_ok=True)

    (data_dir / "public_records.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for record in records:
        rid_lower = record["resource_id"].lower()
        (record_data_dir / f"{rid_lower}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        page_dir = page_root / rid_lower
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(render_record_page(record), encoding="utf-8")

    build_sitemap(output, records)
    print(f"OK: {len(records)} páginas públicas de registro e JSONs estáticos gerados")
    return records


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT
    build(target)
