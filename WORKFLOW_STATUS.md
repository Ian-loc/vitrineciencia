# Estado do workflow — Vitrine Ciência

Atualização operacional: 2026-08-10, `America/Sao_Paulo`

## Direção ativa

**Vitrine Ciência is a bounded scientific-data discovery catalog. Its conceptual product model is stable. Future development prioritizes data-volume growth, metadata correction, usability, maintenance and release management.**

O modelo operacional completo está em `docs/VITRINE_OPERATING_MODEL.md`.

A Vitrine deve crescer principalmente em **conteúdo científico e qualidade**, não em profundidade arquitetural.

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

Uma atividade passa por:

`PLANNED → EXECUTED → MATERIALIZED → VERIFIED → CONSOLIDATED`.

Um pacote só é `CONSOLIDATED` depois de:

1. implementação materializada em branch/PR;
2. validação apropriada ao delta;
3. auditoria do diff;
4. gate humano quando aplicável;
5. merge em `main`;
6. deploy quando houver efeito público;
7. verificação pós-merge/pós-deploy.

CI verde comprova estrutura e testes, **não** verdade factual externa.

## Estado técnico consolidado

### Interface pública

PRs #72–#75 e #77 consolidaram smoke externo, limpeza da linguagem pública, refinamento visual, correção mobile, QA em Chromium real e divulgação progressiva das fontes/produtos.

O estado publicado pós-PR #77 foi verificado em navegador real.

### Modelo operacional

PR #78 consolidou a Vitrine como catálogo delimitado, com quatro classes de mudança (`DATA`, `FIX`, `RELEASE`, `INFRA`) e pipeline obrigatório por pacote.

### Catálogo

O ciclo recente preservou os três conjuntos canônicos, mas **não equivale a uma nova auditoria factual 51/51**.

Portanto:

- estrutura atual: validada;
- interface atual: validada;
- modelo operacional: consolidado;
- conteúdo científico: requer reauditoria 51/51 antes de 1.0.0.

## G0 — saneamento e autoridade

### G0.1 — baseline operacional

**CONSOLIDATED.**

- PR #78 mesclado;
- `main@ba80cc44d2d2d42d7bda54bff9d84ddff97a5c18`;
- nenhum dado científico/frontend/analytics alterado.

### G0.2 — reconciliação dos PRs #57–#69

**MATERIALIZED / WAITING VALIDATION + MERGE GATE.**

Artefatos desta etapa:

- `docs/legacy/VITRINE_LEGACY_RECONCILIATION_2026-08-10.md`;
- `docs/legacy/VITRINE_LEGACY_SALVAGE_MANIFEST.csv`.

Classificação operacional:

- #57: `SALVAGE + HISTORICAL` — evidência de DETER Cerrado; nunca mesclar a arquitetura/guards;
- #58: `HISTORICAL + SUPERSEDED` — princípios úteis já absorvidos; nunca mesclar;
- #59: `SUPERSEDED + REMOVE` — PostgreSQL/runtime antigo; nunca mesclar;
- #60–#69: `SALVAGE` apenas dos onze arquivos `instance1_entry_enrichment_batch01–11.json`; infraestrutura antiga nunca deve ser mesclada.

Os lotes 01–11 cobrem `DR0001`–`DR0051`, mas **cobertura legada não significa verdade factual atual**.

### G0.3 — salvamento científico

**PLANNED / NEXT.**

Fluxo obrigatório para cada registro:

`registro canônico atual → payload legado → fonte oficial atual → decisão de campo → validação → próximo registro`.

Nenhum valor legado será importado automaticamente.

Campos sem equivalente seguro (`metadata_url`, `methodology_url`, `citation_text`, `citation_url`, `update_frequency_text`) permanecem como evidência de auditoria até decisão explícita do contrato canônico. `update_frequency_text` nunca será convertido em `temporal_resolution`.

### G0.4 — fechamento/limpeza do legado

Bloqueado pela preservação adequada.

Após integração de G0.2:

- #58 e #59 podem ser fechados como `superseded`;
- #57 permanece aberto até DETER Cerrado ser revalidado e sua evidência útil preservada;
- #60–#69 permanecem acessíveis até os respectivos lotes terem sido percorridos na auditoria 51/51;
- arquivos/branches obsoletos só serão removidos/arquivados depois de prova de preservação.

### G0.5 — analytics roadmap

O PR #76 contém planejamento útil, mas sua branch diverge do `main` atual. Não mesclar no SHA atual.

Após o saneamento legado imediato, recriar o roadmap em branch nova a partir do `main` vigente. Continuará **PLANNED / NOT IMPLEMENTED** e não autorizará tracker, cookie, beacon ou fingerprint.

## G1 — contrato canônico

Próximo gate estrutural antes da expansão em volume:

- congelar campos obrigatórios/recomendados/nullable-by-design para fontes;
- congelar critério de produto materialmente distinto;
- congelar relações e regras de distribuição/acesso;
- decidir explicitamente o destino dos metadados legados sem equivalente seguro;
- adicionar testes contra IDs inválidos, duplicação semântica e relações órfãs.

## G2 — baseline científico

Após G0/G1:

- auditar 51/51 fontes com evidência oficial atual;
- auditar 11/11 produtos;
- auditar 19/19 distribuições;
- corrigir links/metadados somente com evidência rastreável;
- registrar lacunas sem inferência;
- atualizar `last_verified` somente após verificação real.

## G3 — expansão de volume

Bloqueada até o contrato canônico e baseline inicial estarem estáveis.

Depois:

- batches de 5–10 entradas coerentes;
- foco Brasil;
- nova fonte/produto somente quando materialmente útil;
- sem enumeração automática de assets, tiles, bandas ou endpoints.

## G4 — qualidade operacional

- QA automático de URLs/IDs/relações;
- acessibilidade: teclado, foco, nomes acessíveis, contraste e axe;
- CI proporcional a `DATA/FIX/RELEASE`;
- browsers adicionais quando o risco justificar o custo;
- manter smoke externo.

## G5 — Vitrine Ciência 1.0.0 + Zenodo

Bloqueado até saneamento, contrato, baseline científico e documentação ativa estarem consistentes.

Critérios mínimos:

- repositório saneado;
- 51 fontes auditadas;
- 11 produtos e 19 distribuições auditados;
- QA integral verde;
- versão/citação/licenças consistentes;
- snapshot reproduzível;
- deploy verificado.

Sequência: `tag → GitHub Release → snapshot → Zenodo → inspeção DOI/metadata`.

## G6 — analytics privacy-first

**NOT IMPLEMENTED.**

Sequência futura:

- A0: política de coleta e seleção do provedor;
- A1: instrumentação mínima/reversível;
- A2: histórico durável apenas de agregados;
- A3: visão interna;
- A4: pequeno painel público agregado.

## Política de concorrência

- um pacote de implementação ativo por vez;
- PRs históricos congelados não contam como trabalho ativo;
- evitar cadeias longas de PRs empilhados;
- novos pacotes nascem do `main` atual;
- mudança do head invalida autorização anterior;
- enquanto um PR aguarda gate humano, recorrências podem apenas fazer leitura/inventário/preparação da etapa seguinte.

## Pipeline por pacote

`scope → evidence → implementation → automated validation → diff audit → rendered/public validation when relevant → frozen SHA → human gate → merge/deploy → post-merge verification → consolidation`

## Próxima ordem de execução

1. **G0.2** validar e integrar a reconciliação #57–#69;
2. fechar #58/#59 como `superseded` após a reconciliação estar em `main`;
3. **G0.3** iniciar auditoria científica sequencial `DR0001 → DR0051`, reutilizando os lotes apenas como pistas/evidências;
4. **G0.4** arquivar/limpar legado à medida que sua evidência for preservada;
5. **G0.5** reconstruir o roadmap de analytics sobre `main` atual, sem implementação;
6. **G1** consolidar contrato canônico;
7. **G2** concluir 51 + 11 + 19;
8. **G3** crescer continuamente o catálogo;
9. **G4** reforçar QA/eficiência;
10. **G5** lançar 1.0.0 e depositar no Zenodo;
11. **G6** analytics A0→A4 quando apropriado.

## Fluxo normal de longo prazo

**discover → verify → curate → validate → publish → monitor → periodically release**.

Expansão conceitual deixou de ser o modo normal de desenvolvimento.