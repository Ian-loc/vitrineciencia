# Estado do workflow — Vitrine Ciência

Última redefinição operacional: 2026-08-10, America/Sao_Paulo

## Direção ativa

**Vitrine Ciência is a bounded scientific-data discovery catalog. Its conceptual product model is stable. Future development prioritizes data-volume growth, metadata correction, usability, maintenance and release management.**

O modelo operacional completo está em `docs/VITRINE_OPERATING_MODEL.md`.

A Vitrine deve crescer principalmente em **conteúdo científico e qualidade**, não em profundidade arquitetural.

## Autoridade atual

- repositório: `Ian-loc/vitrineciencia`;
- branch canônica: `main`;
- baseline consolidado antes deste pacote: `1645df4987cd45c64c40a88cf733e9ba5c1f4a40`;
- site: `https://ian-loc.github.io/vitrineciencia/`;
- fontes canônicas: `data/data_resources.csv`;
- produtos: `data/data_products.csv`;
- distribuições/acessos: `data/product_distributions.csv`;
- baseline de dados: **51 fontes, 11 produtos, 19 distribuições**.

A separação Vitrine–Simbiotrama é consolidada. PostgreSQL/PostGIS, runtime, schemas relacionais e pipelines do Simbiotrama não são dependências da Vitrine.

## Regra de materialização

Uma atividade passa pelos estados:

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

PRs #72–#75 e #77 consolidaram:

- smoke externo pós-deploy;
- remoção de linguagem interna de QA/governança da interface pública;
- refinamento visual;
- correção de navegação mobile;
- QA em Chromium real;
- divulgação progressiva das fontes e produtos;
- redução da rolagem excessiva;
- proteção contra overflow horizontal.

O estado publicado pós-PR #77 foi verificado em navegador real.

### Catálogo

O ciclo recente de interface preservou os três conjuntos canônicos; não realizou uma nova auditoria científica integral dos 51 registros.

Portanto:

- estrutura atual: validada;
- interface atual: validada;
- conteúdo científico: **requer auditoria 51/51 como próxima etapa substantiva antes de 1.0.0**.

## Pendências críticas atuais

### G0 — autoridade e saneamento

- [ ] integrar este modelo operacional no `main`;
- [ ] auditar PRs legados #57–#69;
- [ ] classificar cada legado como `SALVAGE`, `HISTORICAL`, `SUPERSEDED` ou `REMOVE`;
- [ ] recuperar seletivamente metadados científicos úteis sem importar arquitetura antiga;
- [ ] fechar PRs legados depois de preservar evidência útil;
- [ ] auditar arquivos ativos obsoletos no repositório;
- [ ] limpar/arquivar somente após prova de preservação;
- [ ] reconstruir o roadmap de analytics sobre `main` atual antes de qualquer merge.

### G1 — contrato canônico

- [ ] congelar campos obrigatórios, recomendados e nullable-by-design para fontes;
- [ ] congelar critério de produto materialmente distinto;
- [ ] congelar relações e regras de distribuição/acesso;
- [ ] adicionar testes contra duplicação semântica/IDs inválidos/orfandade.

### G2 — baseline científico

- [ ] auditar 51/51 fontes com evidência oficial atual;
- [ ] auditar 11/11 produtos;
- [ ] auditar 19/19 distribuições;
- [ ] corrigir links/metadados somente com evidência rastreável;
- [ ] registrar lacunas sem inferência;
- [ ] registrar `last_verified`/equivalente de forma consistente.

### G3 — expansão de volume

Bloqueado até G1 e baseline inicial de G2 estarem suficientemente estáveis.

Depois:

- batches de 5–10 entradas coerentes;
- foco Brasil;
- nova fonte/produto somente quando materialmente útil;
- sem enumeração automática de assets, tiles, bandas ou endpoints.

### G4 — qualidade operacional

- [ ] QA automático de URLs/IDs/relações;
- [ ] acessibilidade: teclado, foco, nomes acessíveis, contraste e axe;
- [ ] política de CI proporcional a DATA/FIX/RELEASE;
- [ ] cobertura adicional de browser quando justificar custo;
- [ ] manter smoke externo.

### G5 — release 1.0.0 e Zenodo

Bloqueado até saneamento, contrato, baseline científico e documentação ativa estarem consistentes.

Critérios mínimos:

- repositório saneado;
- 51 fontes auditadas;
- 11 produtos e 19 distribuições auditados;
- QA integral verde;
- versão/citação/licenças consistentes;
- snapshot reproduzível;
- deploy verificado.

Depois: tag → GitHub Release → snapshot → Zenodo → inspeção do DOI/metadata.

### G6 — analytics privacy-first

**NOT IMPLEMENTED.**

O PR #76 contém planejamento útil, mas sua branch foi criada antes do `main` atual e não deve ser mesclada no SHA atual.

Sequência futura:

- A0: política de coleta e seleção do provedor;
- A1: instrumentação mínima/reversível;
- A2: histórico durável apenas de agregados;
- A3: visão interna;
- A4: pequeno painel público agregado.

Nenhum tracker/cookie/beacon/fingerprint está autorizado por este status.

## Legado aberto a resolver

A cadeia #57–#69 pertence ao período anterior à separação/estabilização atual.

Regra:

**não mesclar a cadeia como arquitetura da Vitrine.**

Ela deve ser tratada como fonte potencial de:

- evidência científica reutilizável;
- decisões históricas;
- material obsoleto/superseded.

A recuperação correta é seletiva: `legacy evidence → current official verification → existing canonical field`.

## Política de concorrência

- preferir um pacote de implementação ativo por vez;
- PRs históricos congelados não contam como trabalho ativo;
- DATA batches independentes podem coexistir somente quando não disputam as mesmas linhas/contratos;
- evitar cadeias longas de PRs empilhados;
- novos pacotes devem nascer do `main` atual;
- qualquer mudança do head invalida autorização anterior.

## Pipeline por pacote

`scope → evidence → implementation → automated validation → diff audit → rendered/public validation when relevant → frozen SHA → human gate → merge/deploy → post-merge verification → consolidation`

## Próxima ordem de execução

1. **G0.1** integrar baseline operacional atual;
2. **G0.2** triagem completa de #57–#69, sem merge;
3. **G0.3** mapear e recuperar metadados científicos aproveitáveis do legado;
4. **G0.4** saneamento de arquivos/branches históricos após preservação;
5. **G0.5** reconstruir analytics roadmap sobre `main` atual e deixar apenas planejamento;
6. **G1** contrato canônico;
7. **G2** auditoria científica 51 + 11 + 19;
8. **G3** crescimento contínuo do catálogo;
9. **G4** reforços de QA e eficiência de CI;
10. **G5** Vitrine Ciência 1.0.0 + Zenodo;
11. **G6** analytics A0→A4, sem interferir na missão principal.

## Critério de longo prazo

O fluxo normal deve ser:

**discover → verify → curate → validate → publish → monitor → periodically release**.

A expansão conceitual deixou de ser o modo normal de desenvolvimento.