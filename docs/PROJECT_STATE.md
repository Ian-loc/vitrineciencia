# Estado canônico e disposição dos artefatos — Vitrine Ciência

**Data de referência:** 18 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Estado global:** catálogo público operacional; contrato fonte → produto → distribuição estável; expansão e revisão factual contínuas.

## 1. Autoridade

1. `main` de `Ian-loc/vitrineciencia`;
2. três tabelas canônicas: `data_resources.csv`, `data_products.csv`, `product_distributions.csv`;
3. contratos e validadores executáveis da Vitrine;
4. documentação ativa listada abaixo;
5. auditorias/evidências históricas;
6. espelhos do Drive e outros snapshots derivados.

JSONs, páginas públicas e relatórios de qualidade são artefatos derivados. O Google Drive não é autoridade concorrente.

## 2. Estado do catálogo

Snapshot observado em 18/08/2026:

- **125 fontes**;
- **752 produtos**;
- **783 distribuições**;
- identificadores correntes chegam a `DR0125`, `DP000756` e `DD000787`; lacunas históricas de IDs são preservadas;
- fontes verificadas até 18/08/2026.

As contagens podem crescer sem mudança de schema.

## 3. Ciclo de vida dos artefatos

### `ACTIVE`

- interface pública da Vitrine;
- três CSVs canônicos e classificação Brasil P0–P3;
- scripts de build e validação da Vitrine;
- GitHub Pages e smoke pós-deploy;
- documentação pública/metodológica, citação, licenças e release;
- curadoria e expansão de fontes/produtos dentro do contrato vigente.

### `DERIVED`

- JSONs construídos a partir dos CSVs;
- `_site`;
- relatórios automáticos de qualidade;
- planilhas/workbooks do Drive quando regenerados.

### `HISTORICAL_EVIDENCE`

Materiais da fase pré-separação que tratam Simbiotrama, Simbioscópio, Instância 1, PostgreSQL/PostGIS, migração 0.8/38 campos, antigas filas de 51 fontes ou roadmaps relacionais. Exemplos:

- `docs/INSTANCE_1_RELATIONAL_SCIENTIFIC_CATALOG.md`;
- `docs/roadmap/INSTANCE_1_CURATION_WORKFLOW.md`;
- `docs/roadmap/SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md`;
- `docs/roadmap/SIMBIOSCOPE_IMPLEMENTATION_ROADMAP.md`;
- decisões e schemas relacionais ligados ao antigo Simbiotrama;
- auditorias datadas e PRs encerrados da transição.

Esses arquivos são preservados por proveniência, mas **não orientam desenvolvimento novo da Vitrine**.

## 4. Fronteira com o Simbiotrama

A separação estrutural ocorreu em 09/08/2026. O Simbiotrama é um projeto independente em `Ian-loc/simbiotrama`. Arquitetura relacional, PostgreSQL/PostGIS, composição territorial e literatura curada pertencem ao Simbiotrama quando retomados; não são requisitos da Vitrine.

## 5. Documentação ativa

- `README.md` — entrada pública;
- `docs/PROJECT_STATE.md` — este estado canônico;
- `docs/PROJECT_SCIENTIFIC_DIRECTION.md` — direção científica;
- `docs/GOVERNANCE.md` — autoridade e gates;
- `docs/VITRINE_BOUNDARY.md` — fronteira de publicação;
- `docs/VITRINE_CANONICAL_DATA_CONTRACT.md` — schema vigente;
- `docs/VITRINE_OPERATING_MODEL.md` — operação e crescimento;
- `METHODOLOGY.md` — metodologia de curadoria;
- `CODEBOOK.md` — dicionário dos campos;
- `PRODUCT_CATALOG_MODEL.md` — modelo fonte/produto/distribuição;
- `SELECTION_AND_COVERAGE_POLICY.md` — seleção e prioridade Brasil;
- `WORKFLOW_STATUS.md` — estado corrente;
- `FINAL_OBJECTIVES_AND_DOI_GATES.md` e `docs/RELEASE_POLICY.md` — release/DOI.

## 6. Estado operacional

- site público: operacional e publicado por GitHub Pages;
- CI: valida dados, frontend e artefato público;
- smoke externo: executado após deploy;
- release científica: ainda `unreleased`;
- DOI: ainda não emitido;
- Drive: contém documentação/histórico e um workbook legado; o workbook não está sincronizado com o catálogo atual.

## 7. Critério de sanidade contínua

Antes de cada pacote:

1. partir do `main` atual;
2. preservar IDs e relações;
3. usar evidência proporcional à afirmação;
4. não promover propriedades de um produto para a fonte inteira;
5. não transformar arquivo/banda/endpoint em produto sem diferença material;
6. registrar desconhecido em vez de inferir;
7. executar validação proporcional ao delta;
8. verificar publicação quando o artefato público puder mudar;
9. encerrar o pacote quando o critério de suficiência estiver atendido.
