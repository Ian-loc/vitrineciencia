# Auditoria de consistência documental

## Revisão corrente — 18 de agosto de 2026

### Escopo

Foram confrontados os documentos operacionais e normativos da Vitrine com:

- `main` de `Ian-loc/vitrineciencia`;
- três tabelas canônicas;
- `data/data_quality_report.json`;
- contrato `schema/product-catalog-v0.1.json`;
- build público e fronteira do GitHub Pages;
- documentação do Drive do projeto.

### Estado factual usado como referência

Em 18/08/2026:

- 125 fontes (`DR0001`–`DR0125`);
- 756 produtos (`DP000001`–`DP000756`);
- 787 distribuições (`DD000001`–`DD000787`);
- verificação das fontes registrada até 18/08/2026;
- modelo canônico: fonte → produto → distribuição;
- `CITATION.cff`: `unreleased`;
- site público: GitHub Pages independente;
- Drive: derivado/histórico; workbook legado não sincronizado com o snapshot corrente.

## Problemas encontrados nesta revisão

1. `WORKFLOW_STATUS.md`, `IMPLEMENTATION_WORKFLOW.md` e `QUALITY_CORRECTION_WORKFLOW.md` ainda descreviam o baseline de 51 fontes e ciclos DATA1/38 campos já superados.
2. `METHODOLOGY.md`, `CODEBOOK.md`, `PRODUCT_CATALOG_MODEL.md`, `docs/PROJECT_STATE.md`, `docs/PROJECT_SCIENTIFIC_DIRECTION.md` e `docs/GOVERNANCE.md` ainda apresentavam Instância 1/PostgreSQL/PostGIS como destino ativo da Vitrine.
3. `docs/VITRINE_OPERATING_MODEL.md` e `docs/VITRINE_CANONICAL_DATA_CONTRACT.md` ainda congelavam metas de 51 fontes/11 produtos/19 distribuições.
4. `SELECTION_AND_COVERAGE_POLICY.md` ainda bloqueava expansão até conclusão do antigo baseline, embora a `main` já possuísse 125 fontes.
5. `FINAL_OBJECTIVES_AND_DOI_GATES.md` estava conceitualmente atualizado, mas o snapshot 125/752/783 já estava quatro produtos/distribuições atrás do estado real.
6. Documentos do Drive ainda descreviam a recuperação do site em 9–10 de agosto, PR #72 e erro 404 como estado corrente.
7. O workbook do Drive permanecia legado e não deveria ser confundido com a base atual.

## Decisão documental

A documentação passa a seguir esta hierarquia:

1. `docs/PROJECT_STATE.md` — estado canônico e ciclo de vida dos artefatos;
2. `docs/PROJECT_SCIENTIFIC_DIRECTION.md` — missão e princípios;
3. `docs/VITRINE_CANONICAL_DATA_CONTRACT.md` — unidades/campos/relações;
4. `docs/VITRINE_OPERATING_MODEL.md` e `docs/GOVERNANCE.md` — operação e gates;
5. `WORKFLOW_STATUS.md` — estado temporal e prioridades;
6. `METHODOLOGY.md`, `CODEBOOK.md`, `PRODUCT_CATALOG_MODEL.md` e política de seleção — interpretação do catálogo;
7. release/DOI e changelog — preservação/citação;
8. documentos datados, roadmaps relacionais antigos e materiais Simbiotrama — `HISTORICAL_EVIDENCE`.

## Ajustes materializados neste pacote

- identidade Vitrine Ciência restabelecida em toda documentação ativa;
- snapshot atualizado para 125/756/787 onde contagens atuais são úteis;
- remoção de metas operacionais obsoletas 51/11/19 e 38 campos;
- PostgreSQL/PostGIS e Instâncias 1–3 retirados do caminho ativo da Vitrine;
- expansão contínua por lotes auditados reconhecida como estado real;
- QA reescrito com critério de suficiência e prioridade por risco;
- Drive explicitamente classificado como derivado e atualmente não sincronizado;
- release mantida como `unreleased`; DOI continua dependente de snapshot/tag/depósito e decisão humana;
- histórico pré-separação preservado sem autoridade normativa.

## Regra de manutenção documental

Documentação ativa deve ser atualizada quando houver mudança material de:

- identidade/escopo;
- modelo/schema;
- autoridade;
- estado de publicação/release;
- estratégia de Drive/DOI;
- contagens quando um documento optar por registrar um snapshot.

Documentos históricos datados **não devem ser reescritos para parecer atuais**. Devem ser preservados como evidência e claramente subordinados ao estado canônico.

## Histórico anterior

### 20–21 de julho de 2026

A auditoria documental original tratou o baseline de 51 fontes, sincronização de planilha 51×34 versus `.xlsx` 51×22, planos DATA1/0.8 e filas de revisão. Essas decisões foram válidas no estágio correspondente, mas foram superadas pelo crescimento do catálogo e pela separação estrutural entre Vitrine Ciência e Simbiotrama em agosto de 2026.

Os PRs, commits, matrizes e relatórios daquele período permanecem no histórico Git para rastreabilidade; não são requisitos do estado corrente.
