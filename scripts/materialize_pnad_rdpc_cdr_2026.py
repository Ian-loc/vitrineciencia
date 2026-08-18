#!/usr/bin/env python3
import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "data/data_products.csv"
DISTS = ROOT / "data/product_distributions.csv"
TODAY = "2026-08-18"

new_products = [
    {
        "product_id": "DP000757",
        "resource_id": "DR0093",
        "product_name": "PNAD Contínua — Rendimento domiciliar per capita 2025",
        "product_acronym": "PNADC RDPC 2025",
        "product_family": "PNAD Contínua — divulgação anual",
        "product_kind": "indicator_family",
        "product_description": "Valores anuais do rendimento nominal mensal domiciliar per capita da população residente, calculados pelo IBGE a partir da PNAD Contínua 2025 para o Brasil e as Unidades da Federação.",
        "research_areas": "Demography | Social statistics | Public policy",
        "keywords": "PNAD Contínua | rendimento domiciliar per capita | renda | FPE | Brasil | Unidades da Federação | 2025 | IBGE",
        "geographic_coverage": "Brasil e Unidades da Federação",
        "covers_brazil": "sim",
        "spatial_support": "estimativas agregadas da pesquisa domiciliar amostral",
        "spatial_resolution": "Brasil e Unidade da Federação",
        "temporal_coverage": "2025",
        "temporal_resolution": "anual",
        "update_frequency": "anual",
        "product_status": "ativo",
        "version_or_collection": "2025; divulgado em 27/02/2026; release atualizado em 27/03/2026",
        "enumeration_scope": "complete",
        "product_page_url": "https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45942-ibge-divulga-rendimento-domiciliar-per-capita-2025-para-brasil-e-unidades-da-federacao",
        "methodology_url": "https://metadados.ibge.gov.br/consulta/estatisticos/operacoes-estatisticas/B5",
        "primary_or_derived": "derivado",
        "limitations": "Indicador derivado de pesquisa amostral, não registro administrativo individual. O RDPC é a razão entre o total dos rendimentos domiciliares nominais e o total de moradores, usando rendimentos de trabalho e outras fontes e as primeiras visitas acumuladas dos quatro trimestres de 2025. Comparações exigem preservar desenho amostral, pesos, conceitos e revisões; valores nominais não equivalem a renda real sem deflação. Para Roraima, a divulgação registra valor específico em cumprimento a decisão judicial.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000758",
        "resource_id": "DR0093",
        "product_name": "PNAD Contínua — Coeficiente de Desequilíbrio Regional 2025",
        "product_acronym": "PNADC CDR 2025",
        "product_family": "PNAD Contínua — indicador regional",
        "product_kind": "indicator_family",
        "product_description": "Coeficientes de Desequilíbrio Regional de 2025 calculados pelo IBGE com base na PNAD Contínua para as Regiões Norte, Nordeste e Centro-Oeste, em comparação com o rendimento domiciliar per capita nacional.",
        "research_areas": "Demography | Social statistics | Public policy | Regional development",
        "keywords": "PNAD Contínua | coeficiente de desequilíbrio regional | CDR | renda | desenvolvimento regional | Norte | Nordeste | Centro-Oeste | 2025 | IBGE",
        "geographic_coverage": "Brasil como referência; Regiões Norte, Nordeste e Centro-Oeste para o CDR",
        "covers_brazil": "sim",
        "spatial_support": "estimativas regionais derivadas de pesquisa domiciliar amostral",
        "spatial_resolution": "Grande Região para Norte, Nordeste e Centro-Oeste; Brasil como referência",
        "temporal_coverage": "2025",
        "temporal_resolution": "anual",
        "update_frequency": "anual",
        "product_status": "ativo",
        "version_or_collection": "2025; divulgação oficial em maio de 2026",
        "enumeration_scope": "complete",
        "product_page_url": "https://www.ibge.gov.br/estatisticas/sociais/populacao/17270-pnad-continua.html?edicao=47159",
        "methodology_url": "https://metadados.ibge.gov.br/consulta/estatisticos/operacoes-estatisticas/B5",
        "primary_or_derived": "derivado",
        "limitations": "Indicador derivado da PNAD Contínua e voltado à comparação regional segundo a sistemática normativa aplicável; não mede desigualdade intrarregional, pobreza, custo de vida ou desenvolvimento multidimensional. O CDR deve ser interpretado com o RDPC e a metodologia oficial e não como observação econômica direta de indivíduos ou municípios.",
        "last_verified": TODAY,
    },
]

new_dists = [
    {
        "distribution_id": "DD000788",
        "product_id": "DP000757",
        "distribution_name": "IBGE — tabela e release do Rendimento domiciliar per capita 2025",
        "access_url": "https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45942-ibge-divulga-rendimento-domiciliar-per-capita-2025-para-brasil-e-unidades-da-federacao",
        "format": "HTML | tabela web",
        "access_protocol": "HTTPS",
        "access_tool": "navegador web",
        "free_download": "sim",
        "authentication_required": "não",
        "access_conditions": "acesso público",
        "license": "consultar termos do IBGE; licença específica desta distribuição não inferida",
        "provider_attribution_required": "sim",
        "subset_support": "Brasil e Unidade da Federação na tabela publicada",
        "notes": "Release oficial com os valores de RDPC de 2025 e nota metodológica resumida. Para análises reproduzíveis, preservar a data/versão da divulgação e consultar a documentação da PNAD Contínua.",
        "last_verified": TODAY,
    },
    {
        "distribution_id": "DD000789",
        "product_id": "DP000758",
        "distribution_name": "IBGE — Coeficiente de Desequilíbrio Regional 2025",
        "access_url": "https://www.ibge.gov.br/estatisticas/sociais/populacao/17270-pnad-continua.html?edicao=47159",
        "format": "HTML | PDF conforme recurso oficial",
        "access_protocol": "HTTPS",
        "access_tool": "navegador web",
        "free_download": "sim",
        "authentication_required": "não",
        "access_conditions": "acesso público",
        "license": "consultar termos do IBGE; licença específica desta distribuição não inferida",
        "provider_attribution_required": "sim",
        "subset_support": "Regiões Norte, Nordeste e Centro-Oeste; Brasil como referência",
        "notes": "Página oficial da PNAD Contínua com a seção do CDR e recurso PDF. Interpretar o indicador apenas nas regiões e no período documentados.",
        "last_verified": TODAY,
    },
]


def read_rows(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def append_rows(path, rows):
    existing = read_rows(path)
    if not existing:
        raise RuntimeError(f"empty canonical file: {path}")
    fieldnames = list(existing[0].keys())
    ids = {r[fieldnames[0]] for r in existing}
    for row in rows:
        if set(row) != set(fieldnames):
            raise RuntimeError(f"schema mismatch for {row.get(fieldnames[0])}")
        if row[fieldnames[0]] in ids:
            old = next(r for r in existing if r[fieldnames[0]] == row[fieldnames[0]])
            if old != row:
                raise RuntimeError(f"ID collision with nonidentical row: {row[fieldnames[0]]}")
            continue
        if path == PRODUCTS and any(r.get("product_page_url") == row["product_page_url"] and r.get("product_name") == row["product_name"] for r in existing):
            raise RuntimeError(f"duplicate product URL/name: {row['product_name']}")
        with path.open("a", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n").writerow(row)
        existing.append(row)
        ids.add(row[fieldnames[0]])

append_rows(PRODUCTS, new_products)
append_rows(DISTS, new_dists)
products = read_rows(PRODUCTS)
dists = read_rows(DISTS)
pids = {r["product_id"] for r in products}
if len(pids) != len(products): raise RuntimeError("duplicate product_id")
if len({r["distribution_id"] for r in dists}) != len(dists): raise RuntimeError("duplicate distribution_id")
if any(r["product_id"] not in pids for r in dists): raise RuntimeError("distribution FK violation")
for pid in ("DP000757", "DP000758"):
    if sum(r["product_id"] == pid for r in products) != 1: raise RuntimeError(f"product read-back failed: {pid}")
    if sum(r["product_id"] == pid for r in dists) != 1: raise RuntimeError(f"distribution read-back failed: {pid}")
subprocess.run(["python3", "scripts/build_catalog.py"], cwd=ROOT, check=True)
print(f"OK materialized: products={len(products)} distributions={len(dists)}")
