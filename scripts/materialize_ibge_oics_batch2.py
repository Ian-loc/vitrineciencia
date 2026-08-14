#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-08-14"

source_rows = [
    {
        "resource_id": "DR0052",
        "resource_name": "Macrocaracterização dos Recursos Naturais do Brasil",
        "acronym": "Macrocaracterização",
        "official_identity": "Coleção de estudos ambientais e mapeamentos integrados do IBGE",
        "description": "Coleção do IBGE que apresenta visão espacialmente integrada do meio natural do Brasil, articulando geologia, geomorfologia, pedologia e vegetação em estudos, mapas, bases e estatísticas.",
        "homepage_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html",
        "data_access_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html?edicao=26063&t=acesso-ao-produto",
        "research_areas": "Ciências Ambientais e Ecologia | Geociências, Solos e Geografia Física | Sensoriamento Remoto e Geoinformação",
        "keywords": "recursos naturais | geologia | geomorfologia | pedologia | vegetação | suscetibilidade | agricultura",
        "data_product_types": "mapas | bases geoespaciais | estudos | publicações | estatísticas",
        "data_formats": "Shapefile | TIF | PDF | formatos variados conforme edição",
        "visualization_types": "mapas | aplicações web | publicações",
        "geographic_coverage": "nacional — Brasil",
        "covers_brazil": "sim",
        "spatial_resolution": "varia conforme a edição; inclui 1:1.000.000 e 1:250.000",
        "temporal_coverage": "coleção iniciada em 2019; edições posteriores conforme tema",
        "temporal_resolution": "não se aplica",
        "data_sources": "bases ambientais do IBGE | literatura e fontes externas conforme estudo",
        "free_download": "sim",
        "access_conditions": "consulta e downloads públicos conforme edição e formato",
        "programmatic_access": "não",
        "access_protocols": "HTTP download | aplicações web",
        "authentication_required": "não",
        "access_documentation_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html",
        "license": "não localizada nesta rodada; observar termos de uso do IBGE e do produto",
        "institutional_status": "público",
        "owner_or_manager": "IBGE",
        "academic_uses": "Apoiar sínteses e análises territoriais integradas de recursos naturais, solos, relevo, geologia, vegetação, suscetibilidade e potencialidade agrícola.",
        "limitations": "Escala, método, formato e finalidade variam entre edições; produtos de macroescala não devem ser usados como substitutos de levantamentos locais quando a documentação assim restringir.",
        "academic_evidence_type": "documentação técnica oficial",
        "academic_evidence_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html",
        "academic_evidence_note": "A documentação oficial descreve a coleção, suas edições, produtos, aplicações web, mapas, bases e notas metodológicas.",
        "verification_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html",
        "last_verified": TODAY,
    },
    {
        "resource_id": "DR0053",
        "resource_name": "API de Pesquisas do IBGE",
        "acronym": "API de Pesquisas",
        "official_identity": "Serviço de Dados do IBGE — API de Pesquisas",
        "description": "API REST do IBGE para descoberta e consulta de pesquisas, períodos, indicadores, rankings e resultados por localidades.",
        "homepage_url": "https://servicodados.ibge.gov.br/api/docs/pesquisas",
        "data_access_url": "https://servicodados.ibge.gov.br/api/v1/pesquisas",
        "research_areas": "Infraestruturas e Ciência de Dados | Planejamento Territorial e Políticas Públicas",
        "keywords": "IBGE | pesquisas | indicadores | localidades | estatísticas | API",
        "data_product_types": "pesquisas | indicadores | resultados | rankings | metadados",
        "data_formats": "JSON",
        "visualization_types": "documentação web | resposta estruturada",
        "geographic_coverage": "nacional — Brasil; recortes variam conforme pesquisa e localidade",
        "covers_brazil": "sim",
        "spatial_resolution": "varia conforme pesquisa, indicador e localidade",
        "temporal_coverage": "varia conforme pesquisa e período disponível",
        "temporal_resolution": "varia conforme pesquisa",
        "data_sources": "pesquisas do IBGE | subconjunto da API de Agregados | outras fontes do Serviço de Dados",
        "free_download": "sim",
        "access_conditions": "consulta pública por endpoints documentados",
        "programmatic_access": "sim",
        "access_protocols": "REST API | HTTPS",
        "authentication_required": "não",
        "access_documentation_url": "https://servicodados.ibge.gov.br/api/docs/pesquisas",
        "license": "não localizada nesta rodada; observar termos de uso dos dados do IBGE",
        "institutional_status": "público",
        "owner_or_manager": "IBGE",
        "academic_uses": "Automatizar descoberta e extração de indicadores e resultados de pesquisas do IBGE por período e localidade.",
        "limitations": "Conteúdo e granularidade dependem da pesquisa; a documentação informa que o serviço combina subconjunto da API de Agregados com outras fontes continuamente enriquecidas e validadas.",
        "academic_evidence_type": "documentação técnica oficial",
        "academic_evidence_url": "https://servicodados.ibge.gov.br/api/docs/pesquisas",
        "academic_evidence_note": "Documentação oficial da API de Pesquisas versão 1.0.0 e de seus endpoints.",
        "verification_url": "https://servicodados.ibge.gov.br/api/docs/pesquisas",
        "last_verified": TODAY,
    },
    {
        "resource_id": "DR0054",
        "resource_name": "Catálogo de Metadados Geográficos do IBGE",
        "acronym": "Metadados Geo IBGE",
        "official_identity": "Catálogo GeoNetwork de metadados geográficos do IBGE",
        "description": "Catálogo institucional para descoberta e compartilhamento de metadados e informações georreferenciadas do IBGE.",
        "homepage_url": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/catalog.search#/home",
        "data_access_url": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/catalog.search#/home",
        "research_areas": "Sensoriamento Remoto e Geoinformação | Infraestruturas e Ciência de Dados | Geociências, Solos e Geografia Física",
        "keywords": "metadados | geoinformação | georreferenciamento | catálogo | IBGE | GeoNetwork",
        "data_product_types": "metadados geográficos | registros de catálogo | links para recursos",
        "data_formats": "metadados e páginas web; formatos de exportação não confirmados nesta rodada",
        "visualization_types": "busca de catálogo | páginas de metadados",
        "geographic_coverage": "Brasil e demais coberturas conforme registro",
        "covers_brazil": "sim",
        "spatial_resolution": "varia conforme o recurso descrito",
        "temporal_coverage": "varia conforme o recurso descrito",
        "temporal_resolution": "varia conforme o recurso descrito",
        "data_sources": "produtos e bases geográficas do IBGE",
        "free_download": "não se aplica",
        "access_conditions": "consulta pública ao catálogo",
        "programmatic_access": "desconhecido",
        "access_protocols": "consulta web; serviços programáticos não confirmados nesta rodada",
        "authentication_required": "não",
        "access_documentation_url": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/catalog.search#/home",
        "license": "varia conforme o recurso descrito; licença específica do catálogo não localizada nesta rodada",
        "institutional_status": "público",
        "owner_or_manager": "IBGE",
        "academic_uses": "Descobrir metadados, proveniência, cobertura e referências de produtos geográficos do IBGE antes do uso analítico.",
        "limitations": "O catálogo descreve recursos heterogêneos; propriedades científicas, formato, licença e acesso devem ser verificados no registro e produto correspondentes.",
        "academic_evidence_type": "documentação oficial",
        "academic_evidence_url": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/catalog.search#/home",
        "academic_evidence_note": "A interface oficial identifica o serviço como catálogo GeoNetwork voltado ao compartilhamento e uso integrado de informação georreferenciada.",
        "verification_url": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/catalog.search#/home",
        "last_verified": TODAY,
    },
    {
        "resource_id": "DR0055",
        "resource_name": "Observatório de Inovação para Cidades Sustentáveis",
        "acronym": "OICS",
        "official_identity": "Observatório de Inovação para Cidades Sustentáveis",
        "description": "Plataforma do CGEE para apoiar inovação e tomada de decisão baseada em evidências em cidades, reunindo soluções, estudos de caso e tipologias territoriais de sustentabilidade urbana.",
        "homepage_url": "https://oics.cgee.org.br/",
        "data_access_url": "https://oics.cgee.org.br/solucoes-e-casos/solucoes",
        "research_areas": "Ciências Ambientais e Ecologia | Planejamento Territorial e Políticas Públicas | Infraestruturas e Ciência de Dados",
        "keywords": "cidades sustentáveis | inovação | soluções baseadas na natureza | sustentabilidade urbana | estudos de caso | tipologias",
        "data_product_types": "soluções | estudos de caso | tipologias | indicadores | mapa interativo",
        "data_formats": "conteúdo web | mapas e indicadores; exportações não confirmadas nesta rodada",
        "visualization_types": "busca facetada | mapa interativo | páginas de solução | páginas de estudo de caso",
        "geographic_coverage": "Brasil e casos internacionais; foco de aplicação em cidades brasileiras",
        "covers_brazil": "sim",
        "spatial_resolution": "municípios, cidades-regiões e localizações de casos; varia conforme conteúdo",
        "temporal_coverage": "varia conforme solução, caso e indicador",
        "temporal_resolution": "varia conforme conteúdo",
        "data_sources": "indicadores e dados geográficos | literatura | documentação de soluções e estudos de caso",
        "free_download": "não",
        "access_conditions": "consulta pública pela plataforma",
        "programmatic_access": "não",
        "access_protocols": "HTTP web",
        "authentication_required": "não",
        "access_documentation_url": "https://oics.cgee.org.br/mapa-interativo",
        "license": "não localizada nesta rodada",
        "institutional_status": "público-acadêmico",
        "owner_or_manager": "CGEE — Centro de Gestão e Estudos Estratégicos",
        "academic_uses": "Descobrir e comparar soluções de sustentabilidade urbana, aplicações concretas, critérios de replicabilidade e tipologias territoriais para pesquisa, ensino e planejamento.",
        "limitations": "Soluções e estudos de caso são produtos de conhecimento aplicado, não datasets observacionais equivalentes; indicadores e escalas devem ser verificados no módulo correspondente.",
        "academic_evidence_type": "documentação oficial",
        "academic_evidence_url": "https://oics.cgee.org.br/",
        "academic_evidence_note": "A plataforma oficial distingue soluções replicáveis, estudos de caso como aplicações práticas e mapa interativo com tipologias baseadas em indicadores, dados geográficos e índices.",
        "verification_url": "https://oics.cgee.org.br/",
        "last_verified": TODAY,
    },
]

product_rows = [
    {
        "product_id": "DP000017", "resource_id": "DR0052",
        "product_name": "Suscetibilidade a Deslizamentos do Brasil — primeira aproximação",
        "product_acronym": "Suscetibilidade a Deslizamentos",
        "product_family": "Macrocaracterização dos Recursos Naturais do Brasil",
        "product_kind": "map_layer_collection",
        "product_description": "Primeira aproximação nacional do IBGE para reconhecimento de áreas com diferentes níveis de suscetibilidade a deslizamentos, construída com bases de geologia, geomorfologia, pedologia, vegetação, uso e cobertura da terra e fontes externas.",
        "research_areas": "Geosciences | Geomorphology | Environmental risk | Territorial planning",
        "keywords": "deslizamentos | suscetibilidade | geomorfologia | risco | Brasil",
        "geographic_coverage": "Brasil", "covers_brazil": "sim",
        "spatial_support": "célula raster | polígonos derivados | mapa nacional",
        "spatial_resolution": "compatível com escala 1:1.000.000",
        "temporal_coverage": "2019 (publicação)", "temporal_resolution": "não se aplica",
        "update_frequency": "por edição", "product_status": "ativo",
        "version_or_collection": "Primeira aproximação | 2019", "enumeration_scope": "complete",
        "product_page_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/geomorfologia/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html?edicao=26063",
        "methodology_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/geomorfologia/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html?edicao=26063",
        "primary_or_derived": "derivado",
        "limitations": "Produto de macroescala e caráter informativo; o IBGE explicita que não deve ser usado para planejamento ou gestão local, obras de engenharia ou como substituto de mapeamentos detalhados.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000018", "resource_id": "DR0052",
        "product_name": "Potencialidade Agrícola Natural das Terras",
        "product_acronym": "Potencialidade Agrícola",
        "product_family": "Macrocaracterização dos Recursos Naturais do Brasil",
        "product_kind": "map_layer_collection",
        "product_description": "Mapeamento nacional que integra classes de solos e relevo para classificar as terras em cinco categorias de potencialidade e limitação ao uso agrícola, com distribuições e estatísticas nacionais e regionais.",
        "research_areas": "Soil science | Agriculture | Environmental planning | Geospatial analysis",
        "keywords": "potencialidade agrícola | solos | relevo | uso agrícola | Brasil",
        "geographic_coverage": "Brasil", "covers_brazil": "sim",
        "spatial_support": "polígonos | mapa nacional | estatísticas territoriais",
        "spatial_resolution": "maior escala de análise que o mapa de 2010; consultar metodologia da edição",
        "temporal_coverage": "2022 (publicação)", "temporal_resolution": "não se aplica",
        "update_frequency": "por edição", "product_status": "ativo",
        "version_or_collection": "Macrocaracterização — Potencialidade Agrícola | 2022", "enumeration_scope": "complete",
        "product_page_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html",
        "methodology_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html",
        "primary_or_derived": "derivado",
        "limitations": "A interpretação depende da metodologia, das classes de solos e relevo e da escala de análise; não extrapolar para aptidão agrícola operacional sem considerar fatores não representados no produto.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000019", "resource_id": "DR0052",
        "product_name": "Subprovíncias Estruturais do Brasil",
        "product_acronym": "Subprovíncias Estruturais",
        "product_family": "Macrocaracterização dos Recursos Naturais do Brasil",
        "product_kind": "map_layer_collection",
        "product_description": "Compartimentação geotectônica do Brasil em 97 subprovíncias estruturais, detalhando as províncias estruturais e representando espacialmente eventos da evolução geológica nacional.",
        "research_areas": "Geology | Tectonics | Geospatial analysis | Environmental planning",
        "keywords": "subprovíncias estruturais | geologia | tectônica | regionalização | Brasil",
        "geographic_coverage": "Brasil", "covers_brazil": "sim",
        "spatial_support": "polígonos | mapa nacional",
        "spatial_resolution": "escala 1:250.000",
        "temporal_coverage": "2020 (publicação)", "temporal_resolution": "não se aplica",
        "update_frequency": "por edição", "product_status": "ativo",
        "version_or_collection": "Macrocaracterização — Subprovíncias Estruturais | 2020", "enumeration_scope": "complete",
        "product_page_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html?edicao=28282&t=acesso-ao-produto",
        "methodology_url": "https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html?edicao=28282",
        "primary_or_derived": "derivado",
        "limitations": "A regionalização sintetiza modelos geotectônicos disponíveis e reflete heterogeneidade do conhecimento geológico; o próprio estudo reconhece questões ainda não esclarecidas em partes do território, especialmente na Amazônia.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000020", "resource_id": "DR0053",
        "product_name": "API de Pesquisas — consultas de pesquisas, indicadores e resultados",
        "product_acronym": "API de Pesquisas v1",
        "product_family": "Serviço de Dados do IBGE",
        "product_kind": "data_service",
        "product_description": "Serviço REST para listar pesquisas, períodos e indicadores e consultar resultados e rankings por localidades e parâmetros documentados.",
        "research_areas": "Data science | Official statistics | Public policy",
        "keywords": "API | pesquisas | indicadores | resultados | localidades | IBGE",
        "geographic_coverage": "Brasil; varia conforme pesquisa e localidade", "covers_brazil": "sim",
        "spatial_support": "unidades territoriais e localidades definidas por pesquisa",
        "spatial_resolution": "varia conforme pesquisa e localidade",
        "temporal_coverage": "varia conforme pesquisa", "temporal_resolution": "varia conforme pesquisa",
        "update_frequency": "serviço continuamente enriquecido e validado conforme documentação",
        "product_status": "ativo", "version_or_collection": "API de Pesquisas 1.0.0", "enumeration_scope": "complete",
        "product_page_url": "https://servicodados.ibge.gov.br/api/docs/pesquisas",
        "methodology_url": "https://servicodados.ibge.gov.br/api/docs/pesquisas",
        "primary_or_derived": "serviço",
        "limitations": "Não representa uma única pesquisa nem um conjunto homogêneo; cobertura, periodicidade, conceito e unidade territorial devem ser herdados da pesquisa e do indicador consultados.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000021", "resource_id": "DR0054",
        "product_name": "Catálogo de Metadados Geográficos do IBGE",
        "product_acronym": "GeoNetwork IBGE",
        "product_family": "Metadados geográficos do IBGE",
        "product_kind": "catalog",
        "product_description": "Índice institucional de descoberta de registros de metadados e informação georreferenciada do IBGE em interface GeoNetwork.",
        "research_areas": "Geospatial information science | Data infrastructure | Geosciences",
        "keywords": "metadados | catálogo | geoinformação | GeoNetwork | IBGE",
        "geographic_coverage": "varia conforme registro; inclui Brasil", "covers_brazil": "sim",
        "spatial_support": "metadados de recursos georreferenciados",
        "spatial_resolution": "herdada do recurso descrito",
        "temporal_coverage": "herdada do recurso descrito", "temporal_resolution": "herdada do recurso descrito",
        "update_frequency": "varia conforme publicação de registros", "product_status": "ativo",
        "version_or_collection": "catálogo corrente", "enumeration_scope": "external_index",
        "product_page_url": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/catalog.search#/home",
        "methodology_url": "",
        "primary_or_derived": "agregador",
        "limitations": "O catálogo é índice de descoberta; não generalizar licença, formato, escala, atualização ou acesso de um registro para os demais. Endpoints programáticos não foram afirmados sem documentação oficial nesta rodada.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000022", "resource_id": "DR0055",
        "product_name": "Catálogo de Soluções OICS",
        "product_acronym": "Soluções OICS",
        "product_family": "Soluções urbanas sustentáveis",
        "product_kind": "catalog",
        "product_description": "Catálogo pesquisável de modelos replicáveis de alternativas sustentáveis para desafios urbanos, organizado por temas, desafios, maturidade, tipo de inovação e Objetivos de Desenvolvimento Sustentável.",
        "research_areas": "Urban sustainability | Nature-based solutions | Public policy | Innovation",
        "keywords": "soluções urbanas | inovação | sustentabilidade | SbN | ODS | replicabilidade",
        "geographic_coverage": "aplicabilidade territorial variável; foco em cidades brasileiras", "covers_brazil": "sim",
        "spatial_support": "região de aplicabilidade e contexto urbano",
        "spatial_resolution": "varia conforme solução",
        "temporal_coverage": "varia conforme registro", "temporal_resolution": "não se aplica",
        "update_frequency": "irregular", "product_status": "ativo",
        "version_or_collection": "catálogo corrente", "enumeration_scope": "external_index",
        "product_page_url": "https://oics.cgee.org.br/solucoes-e-casos/solucoes",
        "methodology_url": "https://oics.cgee.org.br/",
        "primary_or_derived": "agregador",
        "limitations": "As soluções são produtos de conhecimento aplicado e não medições ambientais intercambiáveis; desempenho, maturidade, aplicabilidade e evidência devem ser avaliados no registro específico.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000023", "resource_id": "DR0055",
        "product_name": "Estudos de Caso OICS",
        "product_acronym": "Casos OICS",
        "product_family": "Aplicações de soluções urbanas sustentáveis",
        "product_kind": "catalog",
        "product_description": "Catálogo pesquisável de aplicações práticas de soluções, com contexto territorial, resultados esperados ou observados, orientações de replicação, referências e anexos conforme o caso.",
        "research_areas": "Urban sustainability | Applied environmental science | Public policy | Nature-based solutions",
        "keywords": "estudos de caso | cidades | soluções | replicabilidade | sustentabilidade | SbN",
        "geographic_coverage": "Brasil e casos internacionais", "covers_brazil": "sim",
        "spatial_support": "cidade | estado/província | país | local de aplicação",
        "spatial_resolution": "caso a caso",
        "temporal_coverage": "varia conforme caso", "temporal_resolution": "não se aplica",
        "update_frequency": "irregular", "product_status": "ativo",
        "version_or_collection": "catálogo corrente", "enumeration_scope": "external_index",
        "product_page_url": "https://oics.cgee.org.br/solucoes-e-casos/casos",
        "methodology_url": "https://oics.cgee.org.br/",
        "primary_or_derived": "agregador",
        "limitations": "Casos variam em contexto, profundidade documental e tipo de evidência; não generalizar resultados ou causalidade entre contextos sem avaliação do caso e das referências citadas.",
        "last_verified": TODAY,
    },
    {
        "product_id": "DP000024", "resource_id": "DR0055",
        "product_name": "Tipologias territoriais e Mapa Interativo OICS",
        "product_acronym": "Mapa OICS",
        "product_family": "Tipologias territoriais para cidades sustentáveis",
        "product_kind": "indicator_family",
        "product_description": "Módulo geográfico que caracteriza cidades-regiões por tipologias construídas a partir de conjuntos de indicadores, dados geográficos e índices e as relaciona a temas e soluções de sustentabilidade urbana.",
        "research_areas": "Urban sustainability | Territorial analysis | Geospatial information science | Public policy",
        "keywords": "tipologias | indicadores | cidades-regiões | mapa interativo | sustentabilidade urbana",
        "geographic_coverage": "cidades e regiões brasileiras conforme cobertura do módulo", "covers_brazil": "sim",
        "spatial_support": "município | cidade-região | unidade territorial do indicador",
        "spatial_resolution": "varia conforme indicador e tipologia",
        "temporal_coverage": "varia conforme indicador", "temporal_resolution": "varia conforme indicador",
        "update_frequency": "não documentada nesta rodada", "product_status": "ativo",
        "version_or_collection": "módulo corrente", "enumeration_scope": "family_level",
        "product_page_url": "https://oics.cgee.org.br/mapa-interativo",
        "methodology_url": "https://oics.cgee.org.br/mapa-interativo",
        "primary_or_derived": "derivado",
        "limitations": "Tipologias agregam indicadores e índices heterogêneos; interpretar sempre segundo definição, data, unidade territorial e método de cada componente e não como medição ambiental única.",
        "last_verified": TODAY,
    },
]

distribution_rows = [
    {"distribution_id":"DD000025","product_id":"DP000017","distribution_name":"Suscetibilidade a deslizamentos — base vetorial","access_url":"https://www.ibge.gov.br/geociencias/informacoes-ambientais/geomorfologia/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html?edicao=26063&t=acesso-ao-produto","format":"Shapefile","access_protocol":"HTTP download","access_tool":"navegador web | SIG","free_download":"sim","authentication_required":"não","access_conditions":"download público pela página oficial","license":"consultar termos do IBGE e do produto","provider_attribution_required":"sim","subset_support":"não documentado","notes":"Manter escala compatível com 1:1.000.000 e caráter informativo do produto.","last_verified":TODAY},
    {"distribution_id":"DD000026","product_id":"DP000018","distribution_name":"Potencialidade Agrícola — base e mapa","access_url":"https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html","format":"Shapefile | PDF | publicação","access_protocol":"HTTP download | aplicações web","access_tool":"navegador web | SIG | BDiA | PGI","free_download":"sim","authentication_required":"não","access_conditions":"acesso público conforme formato","license":"consultar termos do IBGE e do produto","provider_attribution_required":"sim","subset_support":"nacional e regional nas análises publicadas; recortes no BDiA/PGI conforme ferramenta","notes":"A página oficial também oferece livro, folder e nota metodológica.","last_verified":TODAY},
    {"distribution_id":"DD000027","product_id":"DP000019","distribution_name":"Subprovíncias Estruturais — mapa e dados","access_url":"https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/24252-macrocaracterizacao-dos-recursos-naturais-do-brasil.html?edicao=28282&t=acesso-ao-produto","format":"mapa | base geoespacial | publicação; consultar edição","access_protocol":"HTTP download | aplicações web","access_tool":"navegador web | SIG | PGI","free_download":"sim","authentication_required":"não","access_conditions":"acesso público pela página oficial","license":"consultar termos do IBGE e do produto","provider_attribution_required":"sim","subset_support":"Brasil; recortes dependem da aplicação","notes":"Representa 97 subprovíncias estruturais em escala 1:250.000; considerar errata cartográfica publicada em 2020.","last_verified":TODAY},
    {"distribution_id":"DD000028","product_id":"DP000020","distribution_name":"API de Pesquisas v1","access_url":"https://servicodados.ibge.gov.br/api/v1/pesquisas","format":"JSON","access_protocol":"REST API | HTTPS","access_tool":"script | navegador | cliente HTTP","free_download":"sim","authentication_required":"não","access_conditions":"consulta pública; parâmetros e rotas conforme documentação","license":"consultar termos de uso dos dados do IBGE","provider_attribution_required":"sim","subset_support":"pesquisa | período | indicador | localidade conforme endpoint","notes":"Documentação oficial identifica a versão 1.0.0 e descreve rotas para pesquisas, indicadores, rankings e resultados.","last_verified":TODAY},
    {"distribution_id":"DD000029","product_id":"DP000021","distribution_name":"GeoNetwork IBGE — catálogo web","access_url":"https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/catalog.search#/home","format":"metadados web","access_protocol":"HTTP web","access_tool":"navegador web","free_download":"não se aplica","authentication_required":"não","access_conditions":"consulta pública","license":"varia conforme recurso; licença do catálogo não localizada nesta rodada","provider_attribution_required":"desconhecido","subset_support":"busca e filtros do catálogo","notes":"Não foram registrados endpoints CSW/API sem documentação oficial suficiente nesta rodada.","last_verified":TODAY},
    {"distribution_id":"DD000030","product_id":"DP000022","distribution_name":"OICS — busca de Soluções","access_url":"https://oics.cgee.org.br/solucoes-e-casos/solucoes","format":"conteúdo web estruturado","access_protocol":"HTTP web","access_tool":"navegador web","free_download":"não","authentication_required":"não","access_conditions":"consulta pública com busca e filtros","license":"não localizada nesta rodada","provider_attribution_required":"desconhecido","subset_support":"tema | desafio | maturidade | tipo de inovação | ODS | região aplicável","notes":"Soluções são definidas pelo OICS como modelos replicáveis de alternativas sustentáveis para desafios urbanos.","last_verified":TODAY},
    {"distribution_id":"DD000031","product_id":"DP000023","distribution_name":"OICS — busca de Estudos de Caso","access_url":"https://oics.cgee.org.br/solucoes-e-casos/casos","format":"conteúdo web estruturado","access_protocol":"HTTP web","access_tool":"navegador web","free_download":"não","authentication_required":"não","access_conditions":"consulta pública com busca e filtros","license":"não localizada nesta rodada","provider_attribution_required":"desconhecido","subset_support":"tema | país | estado/província | cidade | ODS","notes":"Os estudos de caso são descritos pelo OICS como aplicações práticas de soluções, com contextos e implicações.","last_verified":TODAY},
    {"distribution_id":"DD000032","product_id":"DP000024","distribution_name":"OICS — Mapa Interativo","access_url":"https://oics.cgee.org.br/mapa-interativo","format":"Web GIS | visualização de indicadores","access_protocol":"HTTP web","access_tool":"navegador web","free_download":"não","authentication_required":"não","access_conditions":"consulta pública","license":"não localizada nesta rodada","provider_attribution_required":"desconhecido","subset_support":"território | tipologia | tema conforme interface","notes":"Módulo relaciona tipologias territoriais baseadas em indicadores, dados geográficos e índices às soluções de sustentabilidade urbana.","last_verified":TODAY},
]


def append_rows(path, rows, expected_last_id, id_field):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing = list(reader)
        fields = reader.fieldnames
    assert fields, path
    ids = [r[id_field] for r in existing]
    assert ids[-1] == expected_last_id, (path, ids[-1], expected_last_id)
    if rows[0][id_field] in ids:
        return False
    for row in rows:
        missing = set(fields) - set(row)
        extra = set(row) - set(fields)
        assert not missing and not extra, (path, missing, extra)
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writerows(rows)
    return True

sources = ROOT / "data/data_resources.csv"
products = ROOT / "data/data_products.csv"
dists = ROOT / "data/product_distributions.csv"

append_rows(sources, source_rows, "DR0051", "resource_id")
append_rows(products, product_rows, "DP000016", "product_id")
append_rows(dists, distribution_rows, "DD000024", "distribution_id")

# Deterministic relational validation after materialization.
with sources.open(newline="", encoding="utf-8") as f:
    sr = list(csv.DictReader(f))
with products.open(newline="", encoding="utf-8") as f:
    pr = list(csv.DictReader(f))
with dists.open(newline="", encoding="utf-8") as f:
    dr = list(csv.DictReader(f))

assert len(sr) == 55, len(sr)
assert len(pr) == 24, len(pr)
assert len(dr) == 32, len(dr)
assert len({r['resource_id'] for r in sr}) == len(sr)
assert len({r['product_id'] for r in pr}) == len(pr)
assert len({r['distribution_id'] for r in dr}) == len(dr)
source_ids = {r['resource_id'] for r in sr}
product_ids = {r['product_id'] for r in pr}
assert all(r['resource_id'] in source_ids for r in pr)
assert all(r['product_id'] in product_ids for r in dr)

# Regenerate the derived homepage/access-role audit from the canonical source CSV.
records = []
separate = same = na = 0
for r in sr:
    h = (r.get('homepage_url') or '').strip()
    d = (r.get('data_access_url') or '').strip()
    if d == 'não se aplica':
        na += 1
    elif h and d and h != d:
        separate += 1
    else:
        same += 1
        records.append({
            'resource_id': r['resource_id'],
            'resource_name': r['resource_name'],
            'status': 'same_destination_pending_review',
            'homepage_url': h,
            'data_access_url': d,
        })
role_audit = {
    'records': len(sr),
    'standard': {
        'homepage_url': 'Página institucional principal ou página oficial sobre a fonte.',
        'data_access_url': 'Página onde os dados podem ser pesquisados, visualizados, solicitados ou baixados.',
        'same_destination': 'Pendência de revisão; somente pode ser mantida como exceção documentada após inspeção oficial.',
        'not_applicable': 'Usado quando o recurso não oferece dados para consulta ou download, como software de publicação.',
    },
    'counts': {
        'separate_destinations': separate,
        'same_destination_pending_review': same,
        'data_access_not_applicable': na,
    },
    'records_requiring_review': records,
    'interpretation': 'A igualdade entre os dois links não prova erro, mas indica que os papéis institucional e de acesso ainda não foram demonstrados separadamente.',
}
(ROOT / 'data/link_role_audit.json').write_text(json.dumps(role_audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print(json.dumps({
    'sources': len(sr), 'products': len(pr), 'distributions': len(dr),
    'new_sources': [r['resource_id'] for r in source_rows],
    'new_products': [r['product_id'] for r in product_rows],
    'new_distributions': [r['distribution_id'] for r in distribution_rows],
    'link_role_counts': role_audit['counts'],
}, ensure_ascii=False, indent=2))
