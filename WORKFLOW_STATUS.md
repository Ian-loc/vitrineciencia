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
- baseline de dados: **51 fontes, 11 produtos, 19 distribuições**.

A separação Vitrine–Simbiotrama é consolidada. PostgreSQL/PostGIS, runtime, schemas relacionais e pipelines do Simbiotrama não são dependências da Vitrine.

## Regra de materialização

`PLANNED → EXECUTED → MATERIALIZED → VERIFIED → CONSOLIDATED`

Um pacote só é `CONSOLIDATED` depois de implementação materializada, validação proporcional, diff audit, integração governada, deploy quando aplicável e verificação pós-merge/pós-deploy.

CI verde comprova estrutura/testes, **não verdade factual externa**.

## Gates proporcionais ao risco

### AUTO-SAFE
Documentação/status, saneamento reversível com proveniência preservada, QA/CI, correções factuais sem ambiguidade com evidência oficial e pequenas inclusões DATA dentro do contrato canônico podem ser integradas sem interrupção humana após todos os controles objetivos passarem.

### REVIEW
Grandes lotes, mudanças públicas relevantes ou correções factuais materialmente ambíguas exigem uma autorização humana para o pacote completo.

### HUMAN-DECISION
Escopo/modelo conceitual, schema incompatível, mudanças destrutivas/em massa, nova infraestrutura estrutural, analytics/privacy, licença/autoria/citação oficial, release `1.0.0` e Zenodo/DOI exigem decisão humana explícita.

## Estado técnico consolidado

### Interface pública
PRs #72–#75 e #77 consolidaram smoke externo, limpeza da linguagem pública, refinamento visual, correção mobile, QA em Chromium real e divulgação progressiva das fontes/produtos. O estado publicado pós-#77 foi verificado em navegador real.

### Modelo operacional
PR #78 consolidou a Vitrine como catálogo delimitado. A regra de gates proporcionais está sendo incorporada no pacote de reconciliação legado para remover o gargalo de autorização universal.

### Catálogo
O ciclo recente preservou os três conjuntos canônicos, mas **não equivale a nova auditoria factual 51/51**.

- estrutura: validada;
- interface: validada;
- modelo operacional: consolidado;
- conteúdo científico: requer reauditoria 51/51 antes de 1.0.0.

## G0 — saneamento e autoridade

### G0.1 — baseline operacional
**CONSOLIDATED.** PR #78 mesclado em `main@ba80cc44d2d2d42d7bda54bff9d84ddff97a5c18`.

### G0.2 — reconciliação dos PRs #57–#69
**MATERIALIZED / VALIDATING.**

Artefatos:
- `docs/legacy/VITRINE_LEGACY_RECONCILIATION_2026-08-10.md`;
- `docs/legacy/VITRINE_LEGACY_SALVAGE_MANIFEST.csv`.

Classificação:
- #57: `SALVAGE + HISTORICAL` — evidência DETER Cerrado; não mesclar guards/arquitetura;
- #58: `HISTORICAL + SUPERSEDED`;
- #59: `SUPERSEDED + REMOVE` — PostgreSQL/runtime antigo;
- #60–#69: `SALVAGE` somente dos onze `instance1_entry_enrichment_batch01–11.json`.

Os lotes cobrem `DR0001`–`DR0051`, mas cobertura legada **não significa verdade factual atual**.

Risco do pacote G0.2: **AUTO-SAFE** — governança/proveniência, sem alteração dos dados canônicos, frontend ou Pages.

### G0.3 — salvamento científico
**NEXT.**

Fluxo:
`registro canônico atual → payload legado → fonte oficial atual → decisão de campo → validação → próximo registro`.

Nenhum valor legado será importado automaticamente. Campos sem equivalente seguro permanecem evidência de auditoria até decisão do contrato canônico. `update_frequency_text` nunca vira `temporal_resolution` por aproximação.

### G0.4 — fechamento/limpeza do legado
Após G0.2 em `main`:
- #58/#59 podem ser fechados como `superseded` — ação reversível, AUTO-SAFE;
- #57 permanece até DETER Cerrado ser revalidado;
- #60–#69 permanecem acessíveis até os lotes correspondentes serem percorridos;
- remoções destrutivas/em massa sobem para HUMAN-DECISION.

### G0.5 — analytics roadmap
PR #76 contém planejamento útil, mas diverge do `main` atual. Não mesclar o SHA atual. Recriar depois em branch nova; continuará **PLANNED / NOT IMPLEMENTED**. Ativação de analytics é HUMAN-DECISION.

## G1 — contrato canônico
- congelar campos obrigatórios/recomendados/nullable-by-design;
- congelar critério de produto materialmente distinto;
- congelar relações fonte–produto–distribuição;
- decidir destino de metadados legados sem equivalente seguro;
- adicionar testes de IDs, duplicação e orfandade.

Mudança incompatível do contrato é HUMAN-DECISION; documentação/validação do contrato existente pode ser AUTO-SAFE.

## G2 — baseline científico
- auditar 51/51 fontes com evidência oficial atual;
- auditar 11/11 produtos;
- auditar 19/19 distribuições;
- corrigir somente com evidência rastreável;
- registrar lacunas sem inferência;
- atualizar `last_verified` somente após verificação real.

Correções pequenas e inequívocas são AUTO-SAFE; ambiguidades relevantes sobem para REVIEW.

## G3 — expansão de volume
Depois de G1 e baseline inicial de G2:
- batches normalmente de 5–10 entradas;
- foco Brasil;
- nova fonte/produto somente quando materialmente útil;
- sem enumeração automática de assets, tiles, bandas ou endpoints.

## G4 — qualidade operacional
- QA automático de URLs/IDs/relações;
- acessibilidade: teclado, foco, nomes acessíveis, contraste e axe;
- CI proporcional a `DATA/FIX/RELEASE`;
- browsers adicionais quando o risco justificar;
- manter smoke externo.

## G5 — Vitrine Ciência 1.0.0 + Zenodo
HUMAN-DECISION. Bloqueado até saneamento, contrato, baseline científico, documentação e QA estarem consistentes.

Critérios mínimos:
- repositório saneado;
- 51 fontes auditadas;
- 11 produtos e 19 distribuições auditados;
- QA integral verde;
- versão/citação/licenças consistentes;
- snapshot reproduzível;
- deploy verificado.

## G6 — analytics privacy-first
**NOT IMPLEMENTED / HUMAN-DECISION PARA ATIVAÇÃO.**

A0 política/provedor → A1 instrumentação mínima → A2 agregados históricos → A3 visão interna → A4 painel público agregado.

## Política de concorrência

- um pacote de implementação ativo por vez;
- evitar cadeias empilhadas;
- novos pacotes partem do `main` atual;
- AUTO-SAFE deve concluir sem gate humano artificial;
- REVIEW/HUMAN-DECISION aguardam apenas quando o julgamento humano agrega proteção real;
- recorrências podem continuar evidência/preparação segura quando houver gate real pendente.

## Pipeline por pacote

`scope → evidence → implementation → automated validation → diff audit → rendered/public validation when relevant → risk classification → AUTO-SAFE merge ou REVIEW/HUMAN-DECISION gate → post-merge verification → consolidation`

## Próxima ordem

1. concluir **G0.2**;
2. fechar #58/#59 como `superseded` após reconciliação em `main`;
3. iniciar **G0.3** em `DR0001 → DR0051`;
4. limpar legado gradualmente após preservação;
5. reconstruir roadmap analytics em branch atualizada, sem implementação;
6. G1 contrato canônico;
7. G2 51 + 11 + 19;
8. G3 crescimento contínuo;
9. G4 QA/eficiência;
10. G5 1.0.0 + Zenodo;
11. G6 analytics quando apropriado.

## Fluxo normal

**discover → verify → curate → validate → publish → monitor → periodically release**.

Expansão conceitual deixou de ser o modo normal de desenvolvimento.