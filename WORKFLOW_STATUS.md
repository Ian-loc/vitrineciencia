# Estado do workflow — Vitrine Ciência

Atualização operacional: 2026-08-10, `America/Sao_Paulo`

## Direção ativa

**Vitrine Ciência is a bounded scientific-data discovery catalog. Its conceptual product model is stable. Future development prioritizes data-volume growth, metadata correction, usability, maintenance and release management.**

O modelo operacional completo está em `docs/VITRINE_OPERATING_MODEL.md`.

A Vitrine cresce principalmente em **conteúdo científico e qualidade**, não em profundidade arquitetural.

## Autoridade atual

- repositório: `Ian-loc/vitrineciencia`;
- branch canônica: `main`;
- baseline operacional consolidado: `ba80cc44d2d2d42d7bda54bff9d84ddff97a5c18` (PR #78);
- site: `https://ian-loc.github.io/vitrineciencia/`;
- fontes canônicas: `data/data_resources.csv`;
- produtos: `data/data_products.csv`;
- distribuições/acessos: `data/product_distributions.csv`;
- baseline: **51 fontes, 11 produtos, 19 distribuições**.

A separação Vitrine–Simbiotrama é consolidada. PostgreSQL/PostGIS e runtime/schemas do Simbiotrama não são dependências da Vitrine.

## Regra de materialização

`PLANNED → EXECUTED → MATERIALIZED → VERIFIED → CONSOLIDATED`

Consolidação exige implementação, validação proporcional, diff audit, integração governada, deploy quando aplicável e verificação pós-merge/pós-deploy. CI verde comprova estrutura/testes, **não verdade factual externa**.

## Gates proporcionais

- **AUTO-SAFE:** documentação/status, saneamento reversível com proveniência preservada, QA/CI, pequenas correções factuais inequívocas com evidência oficial e pequenas inclusões DATA dentro do contrato. Pode integrar sem interrupção humana depois dos controles objetivos.
- **REVIEW:** lotes grandes, mudança pública relevante ou correção materialmente ambígua. Uma autorização humana para o pacote completo.
- **HUMAN-DECISION:** escopo/modelo conceitual, schema incompatível, destruição/em massa, nova infraestrutura, analytics/privacy, licença/autoria/citação oficial, `1.0.0` e Zenodo/DOI.

## Estado consolidado

### Interface
PRs #72–#75 e #77: smoke externo, linguagem pública, visual, mobile, Chromium real e progressive disclosure consolidados.

### Modelo operacional
PR #78: catálogo delimitado e pipeline consolidado. O PR #79 atualiza a política de gates para o modelo proporcional ao risco.

### Catálogo
Estrutura e interface validadas. O ciclo recente **não equivale a auditoria factual 51/51**; reauditoria científica permanece necessária antes de 1.0.0.

## G0 — saneamento e autoridade

### G0.1 baseline operacional
**CONSOLIDATED.** `main@ba80cc44d2d2d42d7bda54bff9d84ddff97a5c18`.

### G0.2 reconciliação #57–#69
**MATERIALIZED / VALIDATING — AUTO-SAFE.**

Artefatos:
- `docs/legacy/VITRINE_LEGACY_RECONCILIATION_2026-08-10.md`;
- `docs/legacy/VITRINE_LEGACY_SALVAGE_MANIFEST.csv`.

Classificação:
- #57 `SALVAGE + HISTORICAL`;
- #58 `HISTORICAL + SUPERSEDED`;
- #59 `SUPERSEDED + REMOVE`;
- #60–#69 `SALVAGE` somente dos onze `instance1_entry_enrichment_batch01–11.json`.

Nenhum valor legado é autoridade atual ou pode ser importado automaticamente.

### G0.3 salvamento científico
**NEXT.**

`registro canônico atual → payload legado → fonte oficial atual → decisão de campo → validação → próximo registro`

Campos legados sem equivalente seguro ficam como evidência. `update_frequency_text` nunca vira `temporal_resolution` por aproximação.

### G0.4 fechamento/limpeza
Depois de G0.2 em `main`:
- fechar #58/#59 como `superseded` é AUTO-SAFE e reversível;
- manter #57 até DETER Cerrado ser revalidado;
- manter #60–#69 até os lotes serem percorridos;
- remoção destrutiva/em massa é HUMAN-DECISION.

### G0.5 analytics roadmap
PR #76 diverge do `main`; não mesclar o SHA atual. Recriar em branch nova. Planejamento é AUTO-SAFE; ativação de analytics é HUMAN-DECISION.

## G1 contrato canônico
Congelar o contrato existente, critérios de produto e relações; adicionar testes de IDs/duplicação/orfandade. Documentar o contrato existente pode ser AUTO-SAFE; mudança incompatível é HUMAN-DECISION.

## G2 baseline científico
Auditar 51 fontes + 11 produtos + 19 distribuições com evidência oficial atual. Pequenas correções inequívocas são AUTO-SAFE; ambiguidades relevantes sobem para REVIEW.

## G3 expansão
Após G1/G2 inicial: batches pequenos (normalmente 5–10), foco Brasil, granularidade material, sem enumerar assets/bandas/endpoints.

## G4 qualidade
QA de URLs/IDs/relações, acessibilidade, CI proporcional, browsers quando justificado e smoke externo.

## G5 1.0.0 + Zenodo
**HUMAN-DECISION.** Requer saneamento, baseline 51+11+19, QA, versão/citação/licenças consistentes, snapshot reproduzível e deploy verificado.

## G6 analytics
**NOT IMPLEMENTED. HUMAN-DECISION PARA ATIVAÇÃO.**

A0 política/provedor → A1 instrumentação → A2 agregados históricos → A3 visão interna → A4 painel público agregado.

## Política de concorrência

- um pacote de implementação ativo por vez;
- evitar PRs empilhados;
- branches novas partem do `main` atual;
- AUTO-SAFE conclui sem gate humano artificial;
- REVIEW/HUMAN-DECISION param apenas quando julgamento humano agrega proteção real;
- recorrências podem continuar preparação/evidência segura quando houver gate real.

## Pipeline

`scope → evidence → implementation → validation → diff audit → public validation when relevant → risk classification → AUTO-SAFE merge ou REVIEW/HUMAN-DECISION gate → post-merge verification → consolidation`

## Próxima ordem

1. concluir G0.2;
2. fechar #58/#59;
3. iniciar G0.3 em `DR0001 → DR0051`;
4. limpar legado gradualmente;
5. reconstruir roadmap analytics sem implementação;
6. G1 contrato;
7. G2 51 + 11 + 19;
8. G3 crescimento;
9. G4 QA/eficiência;
10. G5 1.0.0 + Zenodo;
11. G6 analytics quando apropriado.

## Fluxo normal

**discover → verify → curate → validate → publish → monitor → periodically release**.