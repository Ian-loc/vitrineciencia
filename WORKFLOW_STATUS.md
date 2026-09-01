# Estado do workflow — Vitrine Ciência

Atualização: **2026-09-01** (`America/Sao_Paulo`)

## Fase ativa

**QA/QC e auditoria ontológica dos 51 registros legados DR0001–DR0051.**

A expansão de novas fontes, produtos e distribuições está **pausada**. `Fonte` é um rótulo do schema legado, não uma classe ontológica já confirmada.

Não implementar conectores, novo schema definitivo ou expansão antes do fechamento G0–G4.

## Sequência de execução

1. **G0** — reconciliar inventário e autoridades dos 51 registros.
2. **G1** — classificar 51/51 com evidência oficial e confiança.
3. **G2** — resolver duplicatas, misturas e conflitos; marcar ambiguidades reais.
4. **G3** — produzir crosswalk legado → entidade canônica → relações → migração.
5. **G4** — validar a ontologia mínima contra todos os 51 casos.
6. **Fase 2** — Integration Registry 51/51: GraphQL/REST/STAC/CKAN/OGC/download/manual, autenticação e prioridade científica.
7. **Fase 3** — pipeline federado; primeiro piloto obrigatório: **MapBiomas Alerta**; depois pelo menos três pilotos heterogêneos.
8. **Consolidação** — catálogo público gerado, QA global, reprodução limpa e smoke test.

## Critério de evidência

Ordem: documentação oficial da entidade/provedor → documentação técnica/API oficial → auditorias verificadas do repositório → literatura/secundárias apenas como apoio.

Não inferir tipo, API, disponibilidade ou qualidade.

## Estado material do repositório

- `main`: ainda 135/843/876 no estado público corrente.
- `v1.0.0`: release histórica imutável.
- PR draft `#267`: branch candidato com **51 fontes** (rótulo legado), **11 produtos** e **19 distribuições**, mais a expansão preservada em quarentena.
- os 51 DR ainda estão **sob classificação ontológica**.

## Artefatos obrigatórios de consolidação

O produto final deve materializar, em caminhos canônicos ou equivalentes registrados no manifesto:

1. auditoria ontológica 51/51;
2. crosswalk legado → entidades canônicas;
3. schema Vitrine Core v1;
4. vocabulários controlados;
5. Integration Registry 51/51;
6. pipeline e conectores executáveis;
7. fixtures e testes automatizados;
8. catálogo público contendo somente `ACCEPTED/PUBLISHED`;
9. catálogo de quarentena;
10. QA global machine-readable;
11. manifesto final;
12. relatório curto de conclusão;
13. tag `vitrine-federated-core-v1`;
14. site publicado com smoke test PASS.

## Definition of Done

A tarefa termina somente quando:

- 51/51 possuem disposition ontológica;
- o modelo canônico acomoda os 51 casos sem `source/fonte` genérico;
- Integration Registry cobre 51/51;
- pipeline executável bloqueia promoção quando QA falha;
- MapBiomas Alerta passa ponta a ponta com execução real e fixture;
- pelo menos três outros pilotos distintos passam pelo mesmo pipeline;
- catálogo público exclui quarentena/não confirmados;
- QA global não contém falha crítica;
- uma execução limpa reconstrói os artefatos públicos;
- site publicado passa smoke test;
- read-back final confirma manifesto, contagens e estado público.

Somente então declarar:

`VITRINE_FEDERATED_CORE_V1_CONSOLIDATED`

Após esse token, a execução recorrente deve ser desativada. Expansão posterior é novo milestone e exige autorização explícita.

## Fora do escopo atual

- reentrada em massa da expansão;
- redesign adicional de interface;
- criação indiscriminada de datasets a partir de recursos de API;
- alteração retroativa da release `v1.0.0`;
- nova release/DOI antes do marco final e de decisão humana específica.
