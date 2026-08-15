#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TODAY = "2026-08-15"


def append_csv(path, key, rows):
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        existing = {r[key] for r in reader}
    missing = [r for r in rows if r[key] not in existing]
    if not missing:
        return 0
    for row in missing:
        unknown = set(row) - set(fieldnames)
        if unknown:
            raise SystemExit(f"{path}: unknown fields: {sorted(unknown)}")
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        for row in missing:
            writer.writerow({k: row.get(k, "") for k in fieldnames})
    return len(missing)


resources = [
    {
        "resource_id": "DR0072",
        "resource_name": "Estatísticas e Indicadores Ambientais — IBGE",
        "acronym": "EIA IBGE",
        "official_identity": "Tema institucional de Estatísticas e Indicadores Ambientais do IBGE",
        "description": "Tema institucional que reúne estatísticas e indicadores ambientais do IBGE, incluindo desenvolvimento sustentável, mudanças climáticas, contas ambientais e sínteses territoriais.",
        "homepage_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estatisticas-e-indicadores-ambientais.html",
        "data_access_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estatisticas-e-indicadores-ambientais.html",
        "research_areas": "Ciências Ambientais e Ecologia | Clima e Ciências Atmosféricas | Planejamento Territorial e Políticas Públicas",
        "keywords": "estatísticas ambientais | indicadores | desenvolvimento sustentável | mudanças climáticas | contas ambientais | IBGE",
        "data_product_types": "indicadores | estatísticas | inventários de informação | publicações | tabelas",
        "data_formats": "PDF | SIDRA | XLSX | ODS | formatos variados conforme produto",
        "visualization_types": "tabelas | gráficos | mapas | publicações",
        "geographic_coverage": "Brasil; recortes variam conforme produto",
        "covers_brazil": "sim",
        "spatial_resolution": "varia conforme indicador e produto",
        "temporal_coverage": "varia conforme produto e edição",
        "temporal_resolution": "varia conforme indicador e série",
        "data_sources": "pesquisas do IBGE | bases oficiais de outras instituições | contas e estatísticas ambientais",
        "free_download": "parcial",
        "access_conditions": "consulta pública; downloads e SIDRA conforme produto",
        "programmatic_access": "parcial",
        "access_protocols": "HTTP download | SIDRA; varia conforme produto",
        "authentication_required": "não",
        "access_documentation_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estatisticas-e-indicadores-ambientais.html",
        "license": "licença específica deve ser verificada no produto ou distribuição; não inferida da página temática",
        "institutional_status": "público",
        "owner_or_manager": "IBGE",
        "academic_uses": "Analisar sustentabilidade, condições ambientais, mudanças climáticas e relações entre ambiente, sociedade e economia com estatísticas oficiais brasileiras.",
        "limitations": "O tema agrega produtos com métodos, anos, escalas e finalidades diferentes; não tratar o conjunto como uma série homogênea nem como dataset único.",
        "academic_evidence_type": "documentação técnica oficial",
        "academic_evidence_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estatisticas-e-indicadores-ambientais.html",
        "academic_evidence_note": "A página temática oficial lista produtos distintos de estatísticas e indicadores ambientais e deve ser usada como porta de descoberta, não como substituto de metadados de cada produto.",
        "verification_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estatisticas-e-indicadores-ambientais.html",
        "last_verified": TODAY,
    },
    {
        "resource_id": "DR0073",
        "resource_name": "Estudos Ambientais — IBGE",
        "acronym": "Estudos Ambientais IBGE",
        "official_identity": "Tema institucional de Estudos Ambientais do IBGE",
        "description": "Tema institucional que reúne estudos ambientais integrados do IBGE, incluindo zoneamento ecológico-econômico, geoestatísticas de recursos naturais, bacias, risco e outras sínteses geográficas e ambientais.",
        "homepage_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais.html",
        "data_access_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais.html",
        "research_areas": "Ciências Ambientais e Ecologia | Geociências, Solos e Geografia Física | Planejamento Territorial e Políticas Públicas",
        "keywords": "estudos ambientais | recursos naturais | zoneamento | geoestatística | risco | território | IBGE",
        "data_product_types": "estudos integrados | mapas | indicadores derivados | publicações | bases associadas",
        "data_formats": "PDF | mapas | tabelas | formatos variados conforme produto",
        "visualization_types": "mapas | tabelas | gráficos | publicações",
        "geographic_coverage": "Brasil e recortes regionais conforme estudo",
        "covers_brazil": "sim",
        "spatial_resolution": "varia conforme estudo e insumos",
        "temporal_coverage": "varia conforme estudo",
        "temporal_resolution": "por edição ou estudo",
        "data_sources": "levantamentos e bases do IBGE | fontes governamentais complementares | análises espaciais",
        "free_download": "parcial",
        "access_conditions": "consulta pública; downloads conforme estudo",
        "programmatic_access": "desconhecido",
        "access_protocols": "HTTP download | páginas de produto",
        "authentication_required": "não",
        "access_documentation_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais.html",
        "license": "licença específica deve ser verificada no produto ou arquivo; não inferida da página temática",
        "institutional_status": "público",
        "owner_or_manager": "IBGE",
        "academic_uses": "Apoiar análises integradas de recursos naturais, planejamento territorial, zoneamento e avaliação socioambiental em diferentes escalas.",
        "limitations": "Os estudos são heterogêneos em recorte, data, método e granularidade; páginas históricas podem permanecer acessíveis sem representar a versão mais recente de um fenômeno.",
        "academic_evidence_type": "documentação técnica oficial",
        "academic_evidence_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais.html",
        "academic_evidence_note": "A página oficial distingue vários produtos e famílias de estudos ambientais; cada produto deve preservar sua própria referência temporal e metodológica.",
        "verification_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais.html",
        "last_verified": TODAY,
    },
]

products = [
    {
        "product_id": "DP000104",
        "resource_id": "DR0072",
        "product_name": "Indicadores de Desenvolvimento Sustentável — Brasil 2015",
        "product_acronym": "IDS Brasil 2015",
        "product_family": "Indicadores de Desenvolvimento Sustentável",
        "product_kind": "indicator_family",
        "product_description": "Conjunto de indicadores do IBGE para acompanhar o desenvolvimento sustentável brasileiro nas dimensões ambiental, social, econômica e institucional, com séries e fontes documentadas por indicador.",
        "research_areas": "Sustainability science | Environmental indicators | Socioecological systems | Public policy",
        "keywords": "desenvolvimento sustentável | indicadores | ambiente | sociedade | economia | instituições | SIDRA | IBGE",
        "geographic_coverage": "Brasil; País e Unidades da Federação quando disponível por indicador",
        "covers_brazil": "sim",
        "spatial_support": "Brasil | Unidade da Federação | outros recortes conforme indicador",
        "spatial_resolution": "varia conforme indicador e fonte",
        "temporal_coverage": "séries históricas variáveis; edição de referência 2015, com atualização SIDRA verificada em 2016",
        "temporal_resolution": "varia conforme indicador",
        "update_frequency": "histórica; continuidade posterior não inferida nesta auditoria",
        "product_status": "desconhecido",
        "version_or_collection": "Brasil 2015; série iniciada em 2002",
        "enumeration_scope": "complete",
        "product_page_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estatisticas-e-indicadores-ambientais/15838-indicadores-de-desenvolvimento-sustentavel.html",
        "methodology_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estatisticas-e-indicadores-ambientais/15838-indicadores-de-desenvolvimento-sustentavel.html",
        "primary_or_derived": "derivado",
        "limitations": "Os indicadores combinam fontes, recortes e periodicidades diferentes. A edição 2015 não deve ser apresentada como retrato atual; verificar a data de cada série/tabela antes de análise contemporânea.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000105",
        "resource_id": "DR0072",
        "product_name": "Estatísticas do Meio Ambiente e de Mudanças Climáticas — recomendações e iniciativas 2024",
        "product_acronym": "EMAMC 2024",
        "product_family": "Estatísticas do Meio Ambiente e de Mudanças Climáticas",
        "product_kind": "catalog",
        "product_description": "Inventário e diagnóstico preliminar do IBGE sobre a cobertura de estatísticas ambientais e de mudanças climáticas no Brasil, estruturado a partir do FDES 2013 e do Conjunto Global de Estatísticas e Indicadores sobre Mudanças Climáticas 2022 da ONU.",
        "research_areas": "Environmental statistics | Climate change | Data governance | Public policy",
        "keywords": "estatísticas ambientais | mudanças climáticas | FDES | indicadores climáticos | governança de dados | IBGE",
        "geographic_coverage": "Brasil; cobertura institucional e temática nacional",
        "covers_brazil": "sim",
        "spatial_support": "inventário temático/institucional; não se aplica como geometria única",
        "spatial_resolution": "não se aplica; varia conforme a estatística inventariada",
        "temporal_coverage": "publicação 2024; referências internacionais FDES 2013 e conjunto climático global 2022",
        "temporal_resolution": "não se aplica ao inventário; varia conforme estatística referenciada",
        "update_frequency": "por edição; frequência futura não documentada",
        "product_status": "ativo",
        "version_or_collection": "publicação 2024",
        "enumeration_scope": "external_index",
        "product_page_url": "https://www.ibge.gov.br/estatisticas/multidominio/meio-ambiente/41681-estatisticas-do-meio-ambiente-e-de-mudancas-climaticas.html",
        "methodology_url": "https://www.ibge.gov.br/estatisticas/multidominio/meio-ambiente/41681-estatisticas-do-meio-ambiente-e-de-mudancas-climaticas.html",
        "primary_or_derived": "agregador",
        "limitations": "É diagnóstico/inventário e proposta de agenda integradora, não uma base harmonizada de observações climáticas. Cada estatística referenciada preserva produtor, método, período e unidade próprios.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000106",
        "resource_id": "DR0073",
        "product_name": "Geoestatísticas de Recursos Naturais da Amazônia Legal — referência 2003",
        "product_acronym": "Geoestatísticas Amazônia Legal 2003",
        "product_family": "Geoestatística de Recursos Naturais da Amazônia Legal",
        "product_kind": "indicator_family",
        "product_description": "Síntese geoestatística do IBGE sobre organização e distribuição de recursos naturais e cobertura da terra na Amazônia Legal, baseada em dados do BDiA e análises espaciais de vegetação, relevo, solos, rochas e recursos minerais.",
        "research_areas": "Natural resources | Amazon studies | Geostatistics | Physical geography",
        "keywords": "Amazônia Legal | recursos naturais | vegetação | relevo | solos | geologia | cobertura da terra | BDiA",
        "geographic_coverage": "Amazônia Legal e Unidades da Federação que a compõem",
        "covers_brazil": "parcial",
        "spatial_support": "Amazônia Legal | Unidade da Federação | unidades temáticas derivadas",
        "spatial_resolution": "agregações e mapas derivados de bases ambientais; consultar a publicação por tema",
        "temporal_coverage": "dados de referência 2003; publicação 2011",
        "temporal_resolution": "snapshot temático",
        "update_frequency": "por edição; nenhuma atualização posterior inferida",
        "product_status": "ativo",
        "version_or_collection": "referência 2003; publicação 2011",
        "enumeration_scope": "complete",
        "product_page_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/15839-geoestatistica-de-recursos-naturais-da-amazonia-legal.html",
        "methodology_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/15839-geoestatistica-de-recursos-naturais-da-amazonia-legal.html",
        "primary_or_derived": "derivado",
        "limitations": "É síntese histórica baseada em dados de referência 2003 e publicada em 2011; não representa condição atual da Amazônia Legal. Escalas e métodos variam entre os quatro temas analisados.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000107",
        "resource_id": "DR0073",
        "product_name": "Zoneamento Ecológico-Econômico — estudos e publicações do IBGE",
        "product_acronym": "ZEE IBGE",
        "product_family": "Zoneamento Ecológico-Econômico",
        "product_kind": "catalog",
        "product_description": "Família de estudos e publicações do IBGE desenvolvidos no âmbito do Zoneamento Ecológico-Econômico, incluindo análises socioeconômicas e ambientais para recortes territoriais específicos em colaboração com o governo federal.",
        "research_areas": "Environmental planning | Territorial analysis | Socioecological systems | Public policy",
        "keywords": "ZEE | zoneamento ecológico-econômico | planejamento territorial | desenvolvimento sustentável | São Francisco | IBGE",
        "geographic_coverage": "recortes regionais do Brasil conforme projeto; não constitui cobertura nacional homogênea",
        "covers_brazil": "parcial",
        "spatial_support": "bacias, regiões e outros recortes definidos por projeto",
        "spatial_resolution": "varia conforme estudo e produto cartográfico",
        "temporal_coverage": "varia conforme projeto; MacroZEE São Francisco inclui referência 2009",
        "temporal_resolution": "por estudo/projeto",
        "update_frequency": "sem frequência única; por projeto",
        "product_status": "ativo",
        "version_or_collection": "coleção de estudos; edições variáveis",
        "enumeration_scope": "family_level",
        "product_page_url": "https://www.ibge.gov.br/geociencias/cartas-e-mapas/mapas-regionais/31681-zoneamento-ecologico-economico.html",
        "methodology_url": "https://www.ibge.gov.br/geociencias/cartas-e-mapas/mapas-regionais/31681-zoneamento-ecologico-economico.html",
        "primary_or_derived": "agregador",
        "limitations": "Não é um único zoneamento nacional nem uma camada uniforme. Cada estudo tem recorte, escala, data, método e finalidade próprios e deve ser citado individualmente no uso analítico.",
        "last_verified": TODAY,
    },
]

distributions = [
    {
        "distribution_id": "DD000120",
        "product_id": "DP000104",
        "distribution_name": "IDS Brasil 2015 — publicação e tabelas oficiais",
        "access_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estatisticas-e-indicadores-ambientais/15838-indicadores-de-desenvolvimento-sustentavel.html",
        "format": "PDF | tabelas SIDRA; varia conforme indicador",
        "access_protocol": "HTTP web | SIDRA",
        "access_tool": "navegador web | SIDRA",
        "free_download": "sim",
        "authentication_required": "não",
        "access_conditions": "consulta pública; selecionar edição/tabela conforme indicador",
        "license": "não localizada especificamente nesta auditoria; observar termos de uso do IBGE e da tabela",
        "provider_attribution_required": "sim",
        "subset_support": "por indicador/tabela e recorte quando disponível no SIDRA",
        "notes": "A página oficial preserva a edição 2015 e a série histórica; registrar a data de referência efetiva de cada indicador.",
        "last_verified": TODAY,
    },
    {
        "distribution_id": "DD000121",
        "product_id": "DP000105",
        "distribution_name": "Estatísticas do Meio Ambiente e Mudanças Climáticas 2024 — publicação",
        "access_url": "https://www.ibge.gov.br/estatisticas/multidominio/meio-ambiente/41681-estatisticas-do-meio-ambiente-e-de-mudancas-climaticas.html",
        "format": "PDF | página HTML",
        "access_protocol": "HTTP download | web",
        "access_tool": "navegador web",
        "free_download": "sim",
        "authentication_required": "não",
        "access_conditions": "consulta pública",
        "license": "não localizada especificamente nesta auditoria; observar termos de uso do IBGE",
        "provider_attribution_required": "sim",
        "subset_support": "não; publicação/inventário",
        "notes": "Distribuição é uma publicação diagnóstica; não confundir com download de uma base climática harmonizada.",
        "last_verified": TODAY,
    },
    {
        "distribution_id": "DD000122",
        "product_id": "DP000106",
        "distribution_name": "Geoestatísticas de Recursos Naturais da Amazônia Legal — publicação",
        "access_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/15839-geoestatistica-de-recursos-naturais-da-amazonia-legal.html",
        "format": "PDF | página HTML",
        "access_protocol": "HTTP download | web",
        "access_tool": "navegador web",
        "free_download": "sim",
        "authentication_required": "não",
        "access_conditions": "consulta pública",
        "license": "não localizada especificamente nesta auditoria; observar termos de uso do IBGE",
        "provider_attribution_required": "sim",
        "subset_support": "por capítulo/tema na publicação; sem API específica confirmada",
        "notes": "Resultados derivam de dados ambientais de referência 2003; não usar como snapshot atual da Amazônia Legal.",
        "last_verified": TODAY,
    },
    {
        "distribution_id": "DD000123",
        "product_id": "DP000107",
        "distribution_name": "Zoneamento Ecológico-Econômico — página de estudos e downloads",
        "access_url": "https://www.ibge.gov.br/geociencias/cartas-e-mapas/mapas-regionais/31681-zoneamento-ecologico-economico.html",
        "format": "PDF e materiais variáveis conforme estudo",
        "access_protocol": "HTTP download | web",
        "access_tool": "navegador web",
        "free_download": "sim",
        "authentication_required": "não",
        "access_conditions": "consulta pública; selecionar publicação/projeto",
        "license": "não localizada de forma uniforme para toda a família; verificar em cada publicação/material",
        "provider_attribution_required": "sim",
        "subset_support": "por publicação/projeto",
        "notes": "A página reúne estudos distintos; a existência de uma publicação não implica uma camada geoespacial uniforme para todo o Brasil.",
        "last_verified": TODAY,
    },
]

nr = append_csv(DATA / "data_resources.csv", "resource_id", resources)
np = append_csv(DATA / "data_products.csv", "product_id", products)
nd = append_csv(DATA / "product_distributions.csv", "distribution_id", distributions)

priority_path = DATA / "brazil_scope_priorities.json"
priority = json.loads(priority_path.read_text(encoding="utf-8"))
priority["reviewed_at"] = TODAY
for tier in priority.get("tiers", []):
    if tier.get("priority_tier") == "P0":
        ids = tier.setdefault("resource_ids", [])
        for rid in ("DR0072", "DR0073"):
            if rid not in ids:
                ids.append(rid)
        break
else:
    raise SystemExit("P0 tier not found")
priority_path.write_text(json.dumps(priority, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"materialized resources={nr} products={np} distributions={nd}")
