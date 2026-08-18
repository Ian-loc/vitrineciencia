#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "data" / "data_products.csv"
DISTS = ROOT / "data" / "product_distributions.csv"
TODAY = "2026-08-18"

product_rows = [
    {
        "product_id": "DP000721",
        "resource_id": "DR0123",
        "product_name": "Brazil Data Cube Explorer",
        "product_acronym": "BDC Explorer",
        "product_family": "Serviços e aplicações Brazil Data Cube",
        "product_kind": "data_service",
        "product_description": "Portal web do Brazil Data Cube para descobrir, visualizar, comparar e baixar coleções de imagens, cubos de dados, classificações e mosaicos, com busca espaço-temporal e integração de gráficos de séries temporais e trajetórias LULC.",
        "research_areas": "Sensoriamento Remoto e Geoinformação | Infraestruturas e Ciência de Dados",
        "keywords": "Brazil Data Cube | BDC Explorer | visualização geoespacial | cubos de dados | sensoriamento remoto | download espaço-temporal",
        "geographic_coverage": "Coleções BDC com cobertura variável, incluindo o território brasileiro",
        "covers_brazil": "sim",
        "spatial_support": "Coleções, tiles, itens, assets e localizações consultadas no portal",
        "spatial_resolution": "Herdada de cada coleção ou asset; não definida pelo nível de zoom do visualizador",
        "temporal_coverage": "Herdada de cada coleção BDC disponibilizada no portal",
        "temporal_resolution": "Herdada da coleção, cubo, classificação ou mosaico consultado",
        "update_frequency": "Contínua conforme atualização das coleções e do catálogo BDC",
        "product_status": "ativo",
        "version_or_collection": "BDC Explorer 1.4.0 na página oficial auditada em 2026-08-18",
        "enumeration_scope": "external_index",
        "product_page_url": "https://data.inpe.br/bdc/en/data-cube-explorer-2/",
        "methodology_url": "https://brazil-data-cube.github.io/applications/dc_explorer.html",
        "primary_or_derived": "serviço",
        "limitations": "O Explorer não é um dataset observacional independente: exibe e distribui produtos subjacentes com sensores, resoluções, períodos, métodos e licenças próprios. A visualização não altera a resolução nativa. O sistema possui controle de acesso/autenticação e a disponibilidade de download depende do produto consultado.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000722",
        "resource_id": "DR0123",
        "product_name": "Brazil Data Cube STAC API",
        "product_acronym": "BDC STAC",
        "product_family": "Serviços e aplicações Brazil Data Cube",
        "product_kind": "data_service",
        "product_description": "Serviço SpatioTemporal Asset Catalog do INPE/Brazil Data Cube para descoberta padronizada de catálogos, coleções, itens e assets geoespaciais por API STAC.",
        "research_areas": "Sensoriamento Remoto e Geoinformação | Infraestruturas e Ciência de Dados",
        "keywords": "STAC | API | catálogo espaço-temporal | assets | coleções | interoperabilidade | Brazil Data Cube",
        "geographic_coverage": "Coleções publicadas no servidor STAC do INPE, incluindo coleções BDC para o Brasil e outros recortes",
        "covers_brazil": "sim",
        "spatial_support": "Catálogos, coleções, itens e geometrias dos assets registrados no STAC",
        "spatial_resolution": "Varia por coleção e asset; consultar metadados STAC da coleção/item",
        "temporal_coverage": "Varia por coleção; consultar extent temporal e itens STAC",
        "temporal_resolution": "Varia por coleção e produto",
        "update_frequency": "Contínua conforme publicação e atualização de coleções/itens no servidor",
        "product_status": "ativo",
        "version_or_collection": "STAC API do INPE/Brazil Data Cube auditada em 2026-08-18",
        "enumeration_scope": "external_index",
        "product_page_url": "https://data.inpe.br/bdc/en/stac-spatiotemporal-asset-catalog-2/",
        "methodology_url": "https://brazil-data-cube.github.io/applications.html",
        "primary_or_derived": "serviço",
        "limitations": "O STAC descreve e referencia datasets; não cria uma nova observação científica. Cobertura, resolução, processamento, qualidade e licença pertencem às coleções/assets subjacentes. Coleções indisponíveis ou restritas podem não ser acessíveis como as coleções públicas.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000723",
        "resource_id": "DR0123",
        "product_name": "Amostras de Uso e Cobertura da Terra — SAMPLE-DB / SAMPLE-WS",
        "product_acronym": "SAMPLE-DB",
        "product_family": "Amostras de uso e cobertura da terra",
        "product_kind": "federated_catalog",
        "product_description": "Banco compartilhado e infraestrutura de serviços para organizar, descobrir e acessar amostras de uso e cobertura da terra coletadas por diferentes projetos e indivíduos, com metadados que preservam diferenças de origem e método de coleta.",
        "research_areas": "Sensoriamento Remoto e Geoinformação | Agricultura, Florestas e Uso da Terra | Infraestruturas e Ciência de Dados",
        "keywords": "amostras LULC | SAMPLE-DB | SAMPLE-WS | treinamento | validação | uso e cobertura da terra | metadados",
        "geographic_coverage": "Variável por projeto/amostra; inclui amostras brasileiras usadas no ecossistema BDC",
        "covers_brazil": "sim",
        "spatial_support": "Amostras espaciais com geometrias e metadados definidos pelo projeto de origem",
        "spatial_resolution": "Não há resolução espacial única; depende da amostra, fonte e método de coleta/interpretação",
        "temporal_coverage": "Varia por conjunto de amostras e projeto de origem",
        "temporal_resolution": "Não uniforme; depende da data/período associado à amostra ou às imagens interpretadas",
        "update_frequency": "Contínua/por projeto conforme incorporação de amostras e metadados",
        "product_status": "ativo",
        "version_or_collection": "Infraestrutura SAMPLE-DB / SAMPLE-WS documentada pelo BDC; auditada em 2026-08-18",
        "enumeration_scope": "external_index",
        "product_page_url": "https://data.inpe.br/bdc/en/land-use-and-land-cover-samples/",
        "methodology_url": "https://data.inpe.br/bdc/en/land-use-and-land-cover-samples/",
        "primary_or_derived": "agregador",
        "limitations": "As amostras provêm de métodos heterogêneos, incluindo campo in situ e interpretação visual de imagens. Classe, data, geometria, qualidade e representatividade devem ser avaliadas por conjunto; o banco não constitui amostra probabilística nacional homogênea nem verdade de terreno automaticamente comparável entre projetos.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000724",
        "resource_id": "DR0123",
        "product_name": "TerraCollect",
        "product_acronym": "TerraCollect",
        "product_family": "Serviços e aplicações Brazil Data Cube",
        "product_kind": "software_output",
        "product_description": "Aplicação web multiusuário para criação de projetos, coleta e análise de amostras de uso e cobertura da terra, combinando visualização multitemporal de imagens, séries WTSS, trajetórias WLTS, Sample-DB e recursos cartográficos auxiliares.",
        "research_areas": "Sensoriamento Remoto e Geoinformação | Agricultura, Florestas e Uso da Terra | Infraestruturas e Ciência de Dados",
        "keywords": "TerraCollect | coleta de amostras | LULC | séries temporais | interpretação visual | treinamento | validação",
        "geographic_coverage": "Definida por cada projeto de coleta; suporta coleções e recursos com cobertura no Brasil",
        "covers_brazil": "sim",
        "spatial_support": "Projetos de amostragem e geometrias vetoriais criadas/avaliadas pelo usuário",
        "spatial_resolution": "Herdada das imagens e recursos utilizados na interpretação; não há resolução única do software",
        "temporal_coverage": "Herdada das coleções de imagens e séries selecionadas no projeto",
        "temporal_resolution": "Herdada dos dados de imagem e serviços integrados",
        "update_frequency": "Software/serviço atualizado pela equipe BDC; projetos e amostras atualizados pelos usuários",
        "product_status": "ativo",
        "version_or_collection": "TerraCollect 1.0.0 na página oficial auditada em 2026-08-18",
        "enumeration_scope": "complete",
        "product_page_url": "https://data.inpe.br/bdc/en/terracollect-2/",
        "methodology_url": "https://data.inpe.br/bdc/en/terracollect-2/",
        "primary_or_derived": "serviço",
        "limitations": "TerraCollect é ferramenta de coleta/análise, não dataset independente. A qualidade das amostras depende do desenho amostral, do intérprete, das imagens e das classes adotadas. O sistema requer autenticação e integrar mapas externos não torna suas legendas, resoluções ou métodos automaticamente equivalentes.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000725",
        "resource_id": "DR0123",
        "product_name": "Data Cube Builder",
        "product_acronym": "Cube Builder",
        "product_family": "Serviços e aplicações Brazil Data Cube",
        "product_kind": "software_output",
        "product_description": "Framework aberto do Brazil Data Cube para geração sob demanda de cubos de dados de observação da Terra em ambiente local ou AWS, executando mosaico espacial/reprojeção, reamostragem, composição temporal e bandas auxiliares de qualidade/proveniência.",
        "research_areas": "Sensoriamento Remoto e Geoinformação | Infraestruturas e Ciência de Dados",
        "keywords": "Cube Builder | data cube | ARD | composição temporal | LCF | AWS | processamento geoespacial",
        "geographic_coverage": "Definida pelas coleções de entrada e pela grade/configuração de processamento; aplicável ao Brasil e a outros recortes suportados",
        "covers_brazil": "sim",
        "spatial_support": "Tiles de grades e cenas/coleções de entrada processadas em cubos",
        "spatial_resolution": "Configurável; depende da coleção de entrada, grade e parâmetros de reamostragem",
        "temporal_coverage": "Definida pelas imagens de entrada selecionadas",
        "temporal_resolution": "Configurável por função e intervalo de composição temporal",
        "update_frequency": "Software versionado; cubos são gerados sob demanda",
        "product_status": "ativo",
        "version_or_collection": "Framework Cube Builder documentado pelo BDC; versão deve ser registrada pelo release/repositório usado",
        "enumeration_scope": "complete",
        "product_page_url": "https://data.inpe.br/bdc/en/data-cube-builder/",
        "methodology_url": "https://brazil-data-cube.github.io/specifications/processing-flow.html",
        "primary_or_derived": "serviço",
        "limitations": "O software não é uma coleção de dados. O cubo resultante depende dos dados de entrada, CRS, resolução, reamostragem, máscara de qualidade e função de composição. Reamostragem e composição temporal alteram a representação dos dados e devem ser documentadas na versão do cubo produzido.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000726",
        "resource_id": "DR0123",
        "product_name": "Web Crop Phenology Metrics Service",
        "product_acronym": "WCPMS",
        "product_family": "Serviços analíticos de séries temporais BDC",
        "product_kind": "data_service",
        "product_description": "Serviço web aberto para calcular métricas fenológicas a partir de séries temporais de cubos de observação da Terra, incluindo métricas associadas ao início, senescência e duração da estação de crescimento para localizações ou regiões consultadas.",
        "research_areas": "Sensoriamento Remoto e Geoinformação | Agricultura, Florestas e Uso da Terra | Infraestruturas e Ciência de Dados",
        "keywords": "WCPMS | fenologia | séries temporais | culturas agrícolas | data cubes | sensoriamento remoto | métricas fenológicas",
        "geographic_coverage": "Dependente dos cubos BDC utilizados; inclui cobertura de áreas agrícolas no Brasil",
        "covers_brazil": "sim",
        "spatial_support": "Localizações ou regiões informadas ao serviço, condicionadas ao suporte espacial do cubo de entrada",
        "spatial_resolution": "Herdada do cubo de observação da Terra utilizado",
        "temporal_coverage": "Herdada do cubo e intervalo temporal consultados",
        "temporal_resolution": "Herdada do cubo/série temporal e do método de extração de métricas",
        "update_frequency": "Sob demanda a partir dos cubos disponíveis; software/serviço versionado",
        "product_status": "ativo",
        "version_or_collection": "WCPMS documentado em publicação BDC 2026; cliente Python atualizado em 2026",
        "enumeration_scope": "complete",
        "product_page_url": "https://data.inpe.br/bdc/en/a-tool-for-crop-phenology-metrics-analysis-from-big-earth-observation-data-2/",
        "methodology_url": "https://doi.org/10.1080/20964471.2026.2641272",
        "primary_or_derived": "derivado",
        "limitations": "Métricas fenológicas são estimativas derivadas da série temporal e do algoritmo, não observações fenológicas de campo. Resultados dependem do sensor/cubo, resolução temporal, ruído/nuvens, pré-processamento e parametrização; datas de semeadura ou estágios agrícolas exigem validação independente para o contexto de uso.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000727",
        "resource_id": "DR0123",
        "product_name": "SITS — Satellite Image Time Series Analysis",
        "product_acronym": "sits",
        "product_family": "Serviços e aplicações Brazil Data Cube",
        "product_kind": "software_output",
        "product_description": "Software aberto para análise, visualização e classificação de séries temporais de imagens de satélite e cubos de dados, cobrindo seleção/avaliação de amostras, treinamento e validação de modelos de aprendizado de máquina, classificação e pós-processamento.",
        "research_areas": "Sensoriamento Remoto e Geoinformação | Infraestruturas e Ciência de Dados | Agricultura, Florestas e Uso da Terra",
        "keywords": "sits | séries temporais | machine learning | classificação LULC | data cubes | acurácia | amostras",
        "geographic_coverage": "Definida pelos cubos e regiões de interesse analisados; inclui coleções BDC e aplicações no Brasil",
        "covers_brazil": "sim",
        "spatial_support": "Cubos, tiles, regiões de interesse, amostras e séries temporais processadas pelo usuário",
        "spatial_resolution": "Herdada dos dados de entrada e operações de regularização/processamento",
        "temporal_coverage": "Herdada dos dados de entrada",
        "temporal_resolution": "Herdada/regularizada conforme cubo e fluxo analítico",
        "update_frequency": "Software versionado e atualizado pelo projeto/comunidade",
        "product_status": "ativo",
        "version_or_collection": "sits — software ativo; consultar versão do pacote usada na análise",
        "enumeration_scope": "complete",
        "product_page_url": "https://data.inpe.br/bdc/en/sits-satellite-image-time-series-2/",
        "methodology_url": "https://data.inpe.br/bdc/en/satellite-image-time-series-analysis-for-big-earth-observation-data-2/",
        "primary_or_derived": "serviço",
        "limitations": "SITS é software analítico, não dataset. Resultados dependem das coleções de entrada, amostras, desenho de validação, algoritmo, hiperparâmetros, pós-processamento e versão do pacote. Classificações geradas devem manter proveniência e métricas de acurácia próprias.",
        "last_verified": TODAY,
    },
]

dist_rows = [
    {
        "distribution_id": "DD000751", "product_id": "DP000721", "distribution_name": "BDC Explorer — aplicação web", "access_url": "https://data.inpe.br/bdc/explorer", "format": "Aplicação web; downloads nos formatos dos assets das coleções subjacentes", "access_protocol": "HTTPS", "access_tool": "Navegador web / BDC Explorer", "free_download": "parcial", "authentication_required": "sim", "access_conditions": "A visualização é web; o sistema implementa autenticação e a disponibilidade de download depende da coleção/asset consultado.", "license": "Varia por coleção/asset; consultar a licença no nível do produto baixado", "provider_attribution_required": "desconhecido", "subset_support": "sim — busca por coleção, espaço, tempo e seleção de itens/assets conforme o portal", "notes": "Distribuição do serviço de descoberta/visualização; não atribuir ao Explorer propriedades científicas dos datasets subjacentes.", "last_verified": TODAY,
    },
    {
        "distribution_id": "DD000752", "product_id": "DP000722", "distribution_name": "INPE/Brazil Data Cube STAC API v1", "access_url": "https://data.inpe.br/bdc/stac/v1/", "format": "STAC JSON; GeoJSON; metadados e links para assets", "access_protocol": "HTTPS | REST | STAC API", "access_tool": "STAC API; clientes STAC compatíveis", "free_download": "sim", "authentication_required": "não", "access_conditions": "Acesso público ao catálogo/coleções públicas; assets ou coleções restritas podem possuir condições próprias.", "license": "Varia por coleção/asset; consultar os metadados da coleção e do recurso", "provider_attribution_required": "desconhecido", "subset_support": "sim — coleção, bbox/intersects, datetime e filtros suportados pelo servidor STAC", "notes": "O endpoint fornece descoberta padronizada e links; conteúdo científico e licença pertencem às coleções/assets referenciados.", "last_verified": TODAY,
    },
    {
        "distribution_id": "DD000753", "product_id": "DP000723", "distribution_name": "BDC Land Use and Land Cover Samples — SAMPLE-DB/SAMPLE-WS", "access_url": "https://data.inpe.br/bdc/en/land-use-and-land-cover-samples/", "format": "Banco de amostras; metadados; serviço web; formatos variam por projeto/conjunto", "access_protocol": "HTTPS | serviço web", "access_tool": "SAMPLE-DB / SAMPLE-WS / ferramentas BDC", "free_download": "parcial", "authentication_required": "desconhecido", "access_conditions": "A descoberta e o acesso dependem do conjunto de amostras e das ferramentas/serviços BDC disponíveis; verificar condições do projeto de origem.", "license": "Varia por conjunto de amostras e projeto de origem; verificar metadados específicos", "provider_attribution_required": "desconhecido", "subset_support": "sim — descoberta/consulta por metadados e projeto conforme os serviços disponíveis", "notes": "Não homogeneizar amostras de origens e métodos distintos; preservar proveniência, classe, data e método de coleta.", "last_verified": TODAY,
    },
    {
        "distribution_id": "DD000754", "product_id": "DP000724", "distribution_name": "TerraCollect — aplicação web", "access_url": "https://data.inpe.br/bdc/terracollect", "format": "Aplicação web; projetos e amostras armazenados no serviço", "access_protocol": "HTTPS", "access_tool": "Navegador web / TerraCollect", "free_download": "parcial", "authentication_required": "sim", "access_conditions": "Requer controle de acesso/autenticação para criação e gestão de projetos; publicação/compartilhamento de amostras depende das funções e permissões do projeto.", "license": "Software descrito pelo BDC como livre e de código aberto; termos dos dados integrados variam por fonte", "provider_attribution_required": "desconhecido", "subset_support": "sim — por projeto, coleção, amostra e classes definidas no fluxo de coleta", "notes": "Ferramenta para produzir/gerenciar amostras; dados externos integrados mantêm suas próprias licenças e semânticas.", "last_verified": TODAY,
    },
    {
        "distribution_id": "DD000755", "product_id": "DP000725", "distribution_name": "Cube Builder — código-fonte e implementação", "access_url": "https://github.com/brazil-data-cube/cube-builder", "format": "Código-fonte; serviço/API; configuração de processamento", "access_protocol": "HTTPS | Git", "access_tool": "GitHub; Python/serviço Cube Builder; infraestrutura local ou AWS", "free_download": "sim", "authentication_required": "não", "access_conditions": "Código-fonte público; execução exige ambiente e dependências computacionais apropriadas. Serviços implantados podem ter políticas próprias.", "license": "Consultar LICENSE do release/repositório utilizado", "provider_attribution_required": "desconhecido", "subset_support": "não se aplica", "notes": "Distribuição de software; os cubos gerados devem registrar separadamente entrada, parâmetros, versão e licença dos dados de origem.", "last_verified": TODAY,
    },
    {
        "distribution_id": "DD000756", "product_id": "DP000726", "distribution_name": "WCPMS — cliente Python e acesso ao serviço", "access_url": "https://github.com/brazil-data-cube/wcpms.py", "format": "Código-fonte Python; cliente de serviço web; respostas de métricas fenológicas", "access_protocol": "HTTPS | REST via cliente", "access_tool": "wcpms.py / Python", "free_download": "sim", "authentication_required": "desconhecido", "access_conditions": "Cliente aberto; acesso efetivo ao serviço depende do endpoint/configuração do WCPMS e dos cubos disponíveis.", "license": "GPL-3.0 no repositório do cliente auditado; dados/cubos subjacentes mantêm licenças próprias", "provider_attribution_required": "sim", "subset_support": "sim — localização ou região, cubo/série e parâmetros suportados pelo serviço", "notes": "Métricas são resultados derivados do algoritmo e da série temporal; preservar versão do cliente/serviço e parâmetros da análise.", "last_verified": TODAY,
    },
    {
        "distribution_id": "DD000757", "product_id": "DP000727", "distribution_name": "sits — software para séries temporais de imagens", "access_url": "https://github.com/e-sensing/sits", "format": "Pacote R; código-fonte; documentação", "access_protocol": "HTTPS | Git | repositório de pacote", "access_tool": "R / pacote sits", "free_download": "sim", "authentication_required": "não", "access_conditions": "Software aberto; execução e acesso aos provedores de dados dependem do ambiente e das credenciais/termos de cada serviço externo quando aplicável.", "license": "GPL-2.0 conforme metadados codemeta do projeto auditado", "provider_attribution_required": "sim", "subset_support": "não se aplica", "notes": "Distribuição de software analítico; outputs gerados não devem ser confundidos com dados primários das coleções de entrada.", "last_verified": TODAY,
    },
]


def read_rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), list(r)

p_fields, existing_products = read_rows(PRODUCTS)
d_fields, existing_dists = read_rows(DISTS)
assert len(existing_products) == 716, f"baseline inesperado de produtos: {len(existing_products)}"
assert len(existing_dists) == 746, f"baseline inesperado de distribuições: {len(existing_dists)}"
assert existing_products[-1]["product_id"] == "DP000720", existing_products[-1]["product_id"]
assert existing_dists[-1]["distribution_id"] == "DD000750", existing_dists[-1]["distribution_id"]

existing_pids = {r["product_id"] for r in existing_products}
existing_dids = {r["distribution_id"] for r in existing_dists}
existing_urls = {r["product_page_url"].rstrip("/") for r in existing_products}
for row in product_rows:
    assert row["product_id"] not in existing_pids
    assert row["product_page_url"].rstrip("/") not in existing_urls, f"product_page_url já catalogada: {row['product_page_url']}"
for row in dist_rows:
    assert row["distribution_id"] not in existing_dids

with PRODUCTS.open("a", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=p_fields, lineterminator="\n")
    w.writerows(product_rows)
with DISTS.open("a", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=d_fields, lineterminator="\n")
    w.writerows(dist_rows)

_, final_products = read_rows(PRODUCTS)
_, final_dists = read_rows(DISTS)
assert len(final_products) == 723
assert len(final_dists) == 753
assert final_products[-7]["product_id"] == "DP000721" and final_products[-1]["product_id"] == "DP000727"
assert final_dists[-7]["distribution_id"] == "DD000751" and final_dists[-1]["distribution_id"] == "DD000757"
print("OK append BDC services: 7 products, 7 distributions; totals 723/753")
