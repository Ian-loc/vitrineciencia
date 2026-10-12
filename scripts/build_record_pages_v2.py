#!/usr/bin/env python3
"""Renderiza as páginas públicas de registro a partir do read model public-record-v2.

O v1 permanece publicado como JSON de compatibilidade. Este renderer altera apenas
a representação HTML e o sitemap, preservando as 58 URLs públicas.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "_site"
SITE_BASE = "https://ian-loc.github.io/vitrineciencia/"

STATUS_LABELS = {
    "sim": "Sim",
    "não": "Não",
    "parcial": "Parcial",
    "desconhecido": "Não confirmado",
    "não se aplica": "Não se aplica",
}

PRIMARY_OR_DERIVED_LABELS = {
    "primário": "Dado primário",
    "derivado": "Dado derivado",
    "agregador": "Agregador",
    "serviço": "Serviço",
    "misto": "Misto",
    "desconhecido": "Não confirmado",
}

ROUTE_ROLE_LABELS = {
    "direct_data": "Dados",
    "data_page": "Página de dados",
    "data_service": "Serviço de dados",
    "viewer": "Visualização",
    "unconfirmed_access": "Acesso em revisão",
    "official_site": "Site oficial",
    "access_documentation": "Documentação de acesso",
    "distribution": "Distribuição",
}

ACCESS_ROLES = {
    "direct_data",
    "data_page",
    "data_service",
    "viewer",
    "unconfirmed_access",
    "official_site",
    "access_documentation",
    "distribution",
}

VERSION_KIND_LABELS = {
    "named_version": "Versão",
    "edition_or_year": "Edição",
    "provider_update": "Atualização",
    "current_collection_state": "Coleção",
    "collection_group": "Coleções",
    "service_state": "Estado do serviço",
    "catalog_state": "Estado do catálogo",
    "access_configuration": "Configuração de acesso",
    "experimental_state": "Estado",
    "descriptive_state": "Estado informado",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def display_status(value: object) -> str:
    raw = str(value or "").strip()
    if not raw:
        return "Não informado"
    return STATUS_LABELS.get(raw.lower(), raw)


def fact(label: str, value: object) -> str:
    text = str(value or "").strip() or "Não informado"
    return f'<dl class="record-fact"><dt>{esc(label)}</dt><dd>{esc(text)}</dd></dl>'


def tags(items: list[str] | None) -> str:
    values = [str(item).strip() for item in (items or []) if str(item).strip()]
    if not values:
        return '<p class="record-meta-note">Não informado.</p>'
    return '<ul class="tag-list">' + "".join(f"<li>{esc(item)}</li>" for item in values) + "</ul>"


def external_link(label: str, url: str | None, class_name: str = "") -> str:
    value = str(url or "").strip()
    if not value.startswith("https://"):
        return ""
    klass = f' class="{esc(class_name)}"' if class_name else ""
    return (
        f'<a{klass} href="{esc(value)}" target="_blank" rel="noopener noreferrer">'
        f'{esc(label)} <span aria-hidden="true">↗</span>'
        '<span class="sr-only"> (abre em nova aba)</span></a>'
    )


def nav_link(anchor: str, label: str) -> str:
    return f'<a href="#{esc(anchor)}">{esc(label)}</a>'


def resource_routes(record: dict) -> list[dict]:
    return [
        route for route in (record.get("access_routes") or [])
        if route.get("target_type") == "resource"
    ]


def offering_routes(record: dict, offering_id: str) -> list[dict]:
    return [
        route for route in (record.get("access_routes") or [])
        if route.get("target_type") == "offering"
        and route.get("target_id") == offering_id
    ]


def offering_versions(record: dict, offering_id: str) -> list[dict]:
    return [
        version for version in (record.get("versions") or [])
        if version.get("offering_id") == offering_id
    ]


def access_routes_html(record: dict) -> str:
    routes = [
        route for route in resource_routes(record)
        if any(role in ACCESS_ROLES for role in (route.get("roles") or []))
    ]
    if not routes:
        return '<p class="notice">A Vitrine ainda não possui uma rota externa confirmada para este recurso.</p>'

    primary = next((route for route in routes if route.get("primary")), routes[0])
    secondary = [route for route in routes if route is not primary]

    primary_roles = [
        ROUTE_ROLE_LABELS[role]
        for role in (primary.get("roles") or [])
        if role in ROUTE_ROLE_LABELS
    ]
    primary_action = external_link(
        primary.get("label") or "Abrir recurso",
        primary.get("url"),
        "access-primary-action",
    )
    if not primary_action:
        primary_action = (
            f'<p class="record-meta-note">{esc(primary.get("notes") or "A rota principal está registrada, mas não possui um link externo confirmado.")}</p>'
        )

    secondary_links: list[str] = []
    for route in secondary:
        action = external_link(route.get("label") or "Abrir recurso", route.get("url"))
        if action:
            secondary_links.append(f"<li>{action}</li>")
        elif route.get("notes"):
            secondary_links.append(
                f'<li><span>{esc(route.get("label") or "Forma de acesso")}: {esc(route["notes"])}</span></li>'
            )

    secondary_html = ""
    if secondary_links:
        secondary_html = (
            '<div class="access-secondary">'
            '<strong>Outras formas de acesso</strong>'
            f'<ul>{"".join(secondary_links)}</ul>'
            '</div>'
        )

    return (
        '<div class="access-panel">'
        '<div class="access-primary">'
        '<span class="access-eyebrow">Acesso principal</span>'
        f'<strong>{esc(primary.get("label") or "Forma de acesso")}</strong>'
        f'<div class="route-meta">{"".join(f"<span>{esc(item)}</span>" for item in primary_roles)}</div>'
        f'<div class="route-actions">{primary_action}</div>'
        '</div>'
        f'{secondary_html}'
        '</div>'
    )


def access_facts_html(access: dict) -> str:
    items = [
        ("Download", display_status(access.get("free_download"))),
        ("Acesso automatizado", display_status(access.get("programmatic_access"))),
        ("Credencial", display_status(access.get("authentication_required"))),
        ("Formas técnicas", " · ".join(access.get("protocols") or []) or "Não documentado"),
    ]
    return (
        '<dl class="access-facts">'
        + "".join(
            f'<div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>'
            for label, value in items
        )
        + "</dl>"
    )


def distribution_html(route: dict) -> str:
    facts: list[str] = []
    if route.get("format"):
        facts.append(f"<span>Formato: {esc(route['format'])}</span>")
    if route.get("protocol"):
        facts.append(f"<span>Acesso: {esc(route['protocol'])}</span>")
    if route.get("free_download"):
        facts.append(f"<span>Download gratuito: {esc(display_status(route['free_download']))}</span>")
    if route.get("authentication_required"):
        facts.append(f"<span>Credencial: {esc(display_status(route['authentication_required']))}</span>")

    notes = "".join(
        f"<p><strong>{esc(label)}:</strong> {esc(value)}</p>"
        for label, value in (
            ("Condições", route.get("access_conditions")),
            ("Licença", route.get("license")),
            ("Observações", route.get("notes")),
        )
        if value
    )
    return (
        '<div class="distribution">'
        f'<strong>{esc(route.get("label") or "Forma de acesso")}</strong>'
        f'<div class="route-meta">{"".join(facts)}</div>'
        f'{notes}'
        f'<div class="route-actions">{external_link("Acessar esta distribuição", route.get("url"))}</div>'
        '</div>'
    )


def offering_html(record: dict, offering: dict) -> str:
    type_info = offering.get("type") or {}
    meta = []
    if type_info.get("label"):
        meta.append(f"<span>{esc(type_info['label'])}</span>")
    nature = PRIMARY_OR_DERIVED_LABELS.get(
        offering.get("primary_or_derived", ""),
        offering.get("primary_or_derived") or "",
    )
    if nature:
        meta.append(f"<span>{esc(nature)}</span>")
    versions = offering_versions(record, offering["offering_id"])
    if versions:
        for version in versions:
            label = "Coleção" if version.get("version_kind") == "collection" else "Versão"
            meta.append(f"<span>{esc(label)}: {esc(version.get('version_label') or '')}</span>")
    if offering.get("version_or_collection_summary"):
        meta.append(f"<span>Versão/coleção informada: {esc(offering['version_or_collection_summary'])}</span>")

    coverage = offering.get("coverage") or {}
    facts = "".join(
        [
            fact("Cobertura geográfica", coverage.get("geographic")),
            fact("Suporte espacial", coverage.get("spatial_support")),
            fact("Resolução espacial", coverage.get("spatial_resolution")),
            fact("Período coberto", coverage.get("temporal_coverage")),
            fact("Resolução temporal", coverage.get("temporal_resolution")),
            fact("Atualização", coverage.get("update_frequency")),
        ]
    )

    links = offering.get("links") or {}
    action_links = " ".join(
        item
        for item in (
            external_link("Abrir página do produto", links.get("product_page")),
            external_link("Ver metodologia", links.get("methodology")),
        )
        if item
    )

    routes = offering_routes(record, offering["offering_id"])
    distributions = "".join(distribution_html(route) for route in routes)

    return (
        '<article class="record-product record-offering">'
        f'<h3>{esc(offering["name"])}</h3>'
        f'<div class="route-meta">{"".join(meta)}</div>'
        f'<p>{esc(offering.get("description") or "")}</p>'
        f'<div class="record-grid">{facts}</div>'
        + (
            f'<p><strong>Cuidados específicos:</strong> {esc(offering["limitations"])}</p>'
            if offering.get("limitations") else ""
        )
        + (f'<div class="record-footer-actions">{action_links}</div>' if action_links else "")
        + (
            f'<div class="distribution-list"><h4>Formas de acesso registradas</h4>{distributions}</div>'
            if distributions else ""
        )
        + '</article>'
    )


def references_html(record: dict) -> str:
    blocks: list[str] = []
    for ref in record.get("references") or []:
        roles = set(ref.get("roles") or [])
        if {"scientific_or_technical_evidence", "verification_source"}.issubset(roles):
            label = "Referência científica/técnica e fonte de verificação"
        elif "scientific_or_technical_evidence" in roles:
            label = "Referência científica ou técnica"
        elif "verification_source" in roles:
            label = "Fonte usada na verificação"
        else:
            label = "Referência"

        note = f'<p>{esc(ref["note"])}</p>' if ref.get("note") else ""
        blocks.append(
            '<article class="record-reference">'
            f'<strong>{esc(label)}</strong>'
            f'{note}'
            f'<div class="record-footer-actions">{external_link("Abrir referência", ref.get("url"))}</div>'
            '</article>'
        )
    if not blocks:
        return '<p class="record-meta-note">Nenhuma referência externa adicional foi registrada.</p>'
    return '<div class="record-reference-list">' + "".join(blocks) + "</div>"


def render_record_page(record: dict) -> str:
    catalog_record = record["record"]
    resource = record["resource"]
    rid = catalog_record["id"]
    canonical = catalog_record["public_url"]
    title = resource["name"]
    description = resource["description"]
    type_info = resource.get("type") or {}
    scope = resource.get("scope") or {}
    themes = resource.get("themes") or {}
    content = resource.get("content_summary") or {}
    coverage = resource.get("coverage") or {}
    access = resource.get("access_summary") or {}
    use_and_limits = resource.get("use_and_limits") or {}

    json_ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "identifier": rid,
            "name": f"{title} · Vitrine Ciência",
            "url": canonical,
            "inLanguage": "pt-BR",
            "about": {"@type": "Thing", "name": title},
            "isPartOf": {
                "@type": "DataCatalog",
                "name": "Vitrine Ciência",
                "url": SITE_BASE,
            },
        },
        ensure_ascii=False,
    )

    offerings = record.get("offerings") or []
    offering_section = (
        '<div class="product-list">' + "".join(offering_html(record, item) for item in offerings) + "</div>"
        if offerings
        else (
            '<p class="notice">A Vitrine ainda não detalhou conjuntos, produtos, séries ou coleções deste recurso como itens separados. '
            'O resumo desta página permanece no nível do recurso catalogado, sem inventar produtos que não foram curados.</p>'
        )
    )
    compare_link = (
        f'<p><a href="../../products.html?source={quote(title)}">Comparar estes itens na visão detalhada da Vitrine →</a></p>'
        if offerings else ""
    )

    provenance = record.get("provenance") or {}
    agents = record.get("agents") or []
    responsible = str(provenance.get("responsibility_statement") or "").strip() or " · ".join(
        str(agent.get("name") or "").strip()
        for agent in agents
        if str(agent.get("name") or "").strip()
    ) or "Não informado"
    unresolved_provenance = provenance.get("role_resolution_status") == "unresolved_legacy_statement" or any(
        agent.get("identity_status") == "unresolved_label"
        for agent in agents
    )
    provenance_note = (
        '<p class="provenance-status">Papéis institucionais ainda não discriminados pela Vitrine.</p>'
        '<details class="provenance-details"><summary>Entender esta proveniência</summary>'
        '<p>A Vitrine preserva o rótulo curado do catálogo e só separa produção, manutenção, publicação, hospedagem ou distribuição quando há evidência suficiente para distinguir esses papéis.</p>'
        '</details>'
        if unresolved_provenance else ""
    )

    nav = "".join(
        [
            nav_link("visao-geral", "Visão geral"),
            nav_link("dados-produtos", "Dados e produtos"),
            nav_link("acesso", "Como acessar"),
            nav_link("interpretacao", "Como interpretar"),
            nav_link("proveniencia-referencias", "Proveniência e referências"),
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
<link rel="stylesheet" href="../../assets/print.css" media="print">
<script type="application/ld+json">{json_ld}</script>
</head>
<body class="record-page" data-public-record-schema="public-record-v2">
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<nav class="site-nav" aria-label="Navegação principal"><div class="wrap nav-inner">
<a class="brand" href="../../index.html" aria-label="Vitrine Ciência — página inicial"><span>Vitrine Ciência</span><small>dados científicos sobre o Brasil</small></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav-links"><span aria-hidden="true">☰</span><span>Menu</span></button>
<div class="nav-links" id="site-nav-links"><a href="../../sources.html">Explorar dados</a><a href="../../products.html">Dados detalhados</a><span class="nav-about"><a href="../../about.html">Sobre a Vitrine</a><a class="nav-sub" href="../../analytics.html">Sobre o acervo</a></span></div>
</div></nav>
<header class="record-hero"><div class="wrap">
<p class="record-breadcrumbs"><a href="../../index.html">Vitrine Ciência</a> › <a href="../../sources.html">Explorar dados</a> › {esc(rid)}</p>
<div class="record-kicker"><span class="record-id">{esc(rid)}</span><span class="record-type">{esc(type_info.get("label") or "Recurso catalogado")}</span><span class="record-scope">{esc(scope.get("label") or "Escopo não informado")}</span></div>
<h1>{esc(title)}</h1>
<p class="record-identity">{esc(resource.get("official_identity") or "")}</p>
<p class="record-lead">{esc(description)}</p>
</div></header>

<main id="conteudo" class="wrap record-layout">
<div class="record-content">

<section class="record-section" id="visao-geral">
<h2>Visão geral</h2>
<div class="record-grid">
{fact("Tipo do recurso", type_info.get("label"))}
{fact("Abrangência na Vitrine", scope.get("label"))}
{fact("Cobertura geográfica", coverage.get("geographic"))}
{fact("Dados sobre o Brasil", display_status(coverage.get("covers_brazil")))}
{fact("Resolução ou escala espacial", coverage.get("spatial_resolution"))}
{fact("Período coberto", coverage.get("temporal_coverage"))}
{fact("Resolução temporal", coverage.get("temporal_resolution"))}
</div>
<h3>Áreas de pesquisa</h3>{tags(themes.get("broad_research_areas"))}
<h3>Termos relacionados</h3>{tags(themes.get("keywords"))}
</section>

<section class="record-section" id="dados-produtos">
<h2>Dados e produtos disponíveis</h2>
<div class="record-summary-block">
<h3>Resumo do conteúdo</h3>
<p><strong>Tipos de conteúdo:</strong></p>{tags(content.get("product_types"))}
<p><strong>Formatos descritos:</strong></p>{tags(content.get("formats"))}
<p><strong>Formas de visualização:</strong></p>{tags(content.get("visualizations"))}
</div>
{offering_section}{compare_link}
</section>

<section class="record-section" id="acesso">
<h2>Como acessar</h2>
<p class="access-status"><strong>Situação:</strong> {esc(access.get("primary_status") or "Não informado")}</p>
{access_routes_html(record)}
{access_facts_html(access)}
<p class="access-conditions"><strong>Condições:</strong> {esc(access.get("conditions") or "Não informado")}</p>
</section>

<section class="record-section" id="interpretacao">
<h2>Como interpretar</h2>
<h3>Possibilidades de uso em pesquisa</h3>
<p>{esc(use_and_limits.get("academic_uses") or "Não informado")}</p>
<h3>Cuidados e limitações</h3>
<p>{esc(use_and_limits.get("limitations") or "Não informado")}</p>
<p class="record-meta-note">Quando uma oferta detalhada possui cobertura, resolução, versão, licença ou limitação mais específica, a informação desse nível prevalece sobre o resumo geral do recurso.</p>
</section>

<section class="record-section" id="proveniencia-referencias">
<h2>Proveniência, condições e referências</h2>
<div class="record-grid">
{fact("Responsabilidade e proveniência", responsible)}
{fact("Natureza institucional", resource.get("institutional_status"))}
</div>
{provenance_note}
<h3>Principais fontes e insumos</h3>{tags(resource.get("data_sources"))}
<h3>Condições de uso e licença</h3>
<p>{esc(use_and_limits.get("license") or "Não informado")}</p>
<p class="record-meta-note">A licença acima é um resumo no nível do recurso. Ofertas e distribuições podem possuir condições próprias e, quando verificadas, essas condições específicas prevalecem.</p>
<h3>Referências e documentação</h3>
{references_html(record)}

<div class="record-curation" id="curadoria">
<h3>Sobre este registro na Vitrine</h3>
<p class="curation-summary"><strong>{esc(rid)}</strong> · revisado em {esc((record.get("curation") or {}).get("last_verified") or "data não informada")} · acesso verificado em {esc((record.get("curation") or {}).get("access_last_verified") or "data não informada")}</p>
<details class="curation-details">
<summary>Como a Vitrine verifica este registro</summary>
<p><strong>Tipo catalogado:</strong> {esc(type_info.get("label") or "Não informado")}</p>
<p>“Não confirmado” significa que a Vitrine não encontrou evidência suficiente na revisão registrada; não significa que o recurso inexista.</p>
<p>Esta página usa um snapshot estático curado. Atualizações futuras por API poderão ocorrer de forma assíncrona sem tornar a página dependente do provedor externo.</p>
</details>
</div>
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
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in base_urls:
        lines.append(f"  <url><loc>{html.escape(url)}</loc></url>")
    for item in records:
        record = item["record"]
        lastmod = (item.get("curation") or {}).get("last_verified")
        suffix = f"<lastmod>{esc(lastmod)}</lastmod>" if lastmod else ""
        lines.append(
            f"  <url><loc>{html.escape(record['public_url'])}</loc>{suffix}</url>"
        )
    lines.append("</urlset>")
    (output / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build(output: Path = DEFAULT_OUTPUT) -> list[dict]:
    source = output / "data" / "v2" / "public_records.json"
    if not source.exists():
        fail("read model public-record-v2 ausente; execute build_public_records_v2 antes")
    records = json.loads(source.read_text(encoding="utf-8"))
    page_root = output / "registros"
    page_root.mkdir(parents=True, exist_ok=True)

    for item in records:
        rid = item["record"]["id"].lower()
        page_dir = page_root / rid
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(render_record_page(item), encoding="utf-8")

    build_sitemap(output, records)
    print(f"OK: {len(records)} páginas públicas renderizadas a partir de public-record-v2")
    return records


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT
    build(target)
