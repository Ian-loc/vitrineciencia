# Estado canônico e disposição dos artefatos — Vitrine Ciência

**Data de referência:** 20 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Estado global:** catálogo público operacional; contrato fonte → produto → distribuição estável; fase ativa de QA/QC e manutenção; candidata `v1.0.0` preparada, ainda sem tag Git imutável, GitHub Release ou DOI.

## 1. Autoridade

1. `main` de `Ian-loc/vitrineciencia` para desenvolvimento corrente;
2. tags/releases imutáveis para snapshots científicos quando formalmente publicados;
3. três tabelas canônicas: `data_resources.csv`, `data_products.csv`, `product_distributions.csv`;
4. contratos e validadores executáveis da Vitrine;
5. documentação ativa listada abaixo;
6. auditorias/evidências históricas;
7. espelhos do Drive e outros snapshots derivados.

JSONs, páginas públicas e relatórios de qualidade são artefatos derivados. O Google Drive não é autoridade concorrente.

## 2. Estado do catálogo

Snapshot candidato a `v1.0.0`, preparado em 19/08/2026:

- **135 fontes**;
- **843 produtos**;
- **876 distribuições**;
- identificadores correntes chegam a `DR0135`, `DP000861` e `DD000894`; lacunas históricas de IDs são preservadas;
- fontes verificadas até 19/08/2026;
- schema vigente: 34 campos de fonte, 24 de produto e 15 de distribuição.

Essas contagens caracterizam a candidata `v1.0.0`; não são gate, teto ou requisito arquitetural. A expansão de novas fontes, produtos e distribuições está pausada durante a fase atual de QA/QC e só deve ser retomada mediante instrução humana explícita.

## 3. Ciclo de vida dos artefatos

### `ACTIVE`

- interface pública da Vitrine;
- três CSVs canônicos e classificação Brasil P0–P3;
- scripts de build e validação da Vitrine;
- GitHub Pages e smoke pós-deploy;
- documentação pública/metodológica, citação, licenças e preparação de release;
- QA/QC, correções factuais/semânticas, robustez de CI/publicação e bugs reais de UX.

### `PAUSED`

- inclusão de novas fontes;
- inclusão de novos produtos;
- inclusão de novas distribuições.

A expansão permanece pausada até nova instrução humana explícita.

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
- `FINAL_OBJECTIVES_AND_DOI_GATES.md` e `docs/RELEASE_POLICY.md` — release/DOI;
- `RELEASE_NOTES_v1.0.0.md` — notas da candidata à primeira release estável.

## 6. Estado operacional

- site público: GitHub Pages configurado e validado pelo pipeline; confirmação externa deve ser feita quando o ambiente permitir;
- CI: valida dados, frontend, derivados versionados e artefato público;
- smoke externo: configurado para executar após deploy bem-sucedido;
- fase ativa: QA/QC e manutenção; expansão de conteúdo pausada;
- candidata científica: `v1.0.0` preparada na branch `release/v1.0.0`;
- tag imutável `v1.0.0`: **ainda não criada**;
- GitHub Release `v1.0.0`: **ainda não publicada**;
- DOI: **ainda não emitido**;
- Drive: contém documentação/histórico e um workbook legado; o workbook não está sincronizado com o catálogo corrente e não é gate da release.

Nenhuma nova tag/release ou depósito DOI deve ser criado sem instrução humana explícita.

## 7. Critério de sanidade contínua

Antes de cada pacote:

1. partir de um commit explicitamente identificado;
2. preservar IDs e relações;
3. usar evidência proporcional à afirmação;
4. não promover propriedades de um produto para a fonte inteira;
5. não transformar arquivo/banda/endpoint em produto sem diferença material;
6. registrar desconhecido em vez de inferir;
7. executar validação proporcional ao delta;
8. verificar publicação quando o artefato público puder mudar;
9. para release, registrar commit, tag, conteúdo do pacote e resultado dos gates;
10. encerrar o pacote quando o critério de suficiência estiver atendido.
