# Estado canônico — Vitrine Ciência

**Data de referência:** 1º de setembro de 2026  
**Fuso:** `America/Sao_Paulo`

## Estado global

A Vitrine está em **re-curadoria estrutural e ontológica**. A prioridade atual não é ampliar catálogo nem implementar federação: é determinar corretamente o que representam os 51 registros legados `DR0001–DR0051`.

### Estado material

- `main` permanece no commit público corrente `f991c9e506bc5c33220e530f7031179afe8e3cec`, com o catálogo expandido de 135/843/876.
- A release `v1.0.0` permanece imutável no commit `27c545554f406b940662777e3f053e939ef3588c`, GitHub Release e Zenodo DOI `10.5281/zenodo.22130831`.
- O PR draft `#267` (`curation/core-51-socioecological-discovery-20260901`) contém um **candidato** de restauração operacional para 51 registros DR / 11 produtos / 19 distribuições, com a expansão preservada em quarentena.
- O PR #267 **não está incorporado à `main`** e não deve ser descrito como estado público consolidado.

## Problema conceitual ativo

O termo histórico **fonte** mistura tipos de entidade diferentes. Os 51 registros podem representar, entre outros, instituição/provedor, programa, plataforma, catálogo, infraestrutura, dataset/coleção, serviço ou portal.

Portanto:

- `DR####` é, nesta fase, um **identificador legado de registro**, não prova de tipo ontológico;
- `Fonte → Produto → Distribuição` permanece como estrutura histórica/operacional, não como ontologia final congelada;
- nenhuma entidade deve ser reclassificada por aparência do nome ou conveniência de schema.

## Objetivo ativo e gates

**G0** — inventário DR0001–DR0051 e autoridades reconciliados.  
**G1** — 51/51 classificados com evidência e confiança.  
**G2** — conflitos, duplicatas e misturas resolvidos ou explicitamente não resolvidos.  
**G3** — crosswalk legado → entidades canônicas → relações → ação de migração.  
**G4** — ontologia mínima validada contra todos os 51 casos.

Somente após G0–G4 PASS começa o registro de integração por API/serviço/download. Conectores não pertencem à fase atual.

## Direção científica pública

A descoberta deve seguir:

**fenômeno/processo → território → tempo/escala → dado utilizável → acesso → provedor/proveniência**.

Catálogo, API, serviço, visualizador e documentação são papéis distintos e não devem ser apresentados como datasets equivalentes.

## Regras vigentes

- evidência oficial/primária antes de inferência;
- desconhecido permanece desconhecido;
- preservar IDs e histórico;
- não publicar automaticamente recurso descoberto por API;
- não alterar retroativamente `v1.0.0`;
- manter expansão em quarentena até revisão explícita;
- mudanças públicas exigem validação, diff audit, CI e smoke test quando aplicável.

## Próxima fase já delimitada

Após G0–G4: Integration Registry 51/51 → MapBiomas Alerta como primeiro piloto GraphQL → pelo menos três pilotos tecnológicos heterogêneos → pipeline reutilizável → catálogo público gerado e testado.

O limite global de conclusão está definido em `WORKFLOW_STATUS.md` pelo token `VITRINE_FEDERATED_CORE_V1_CONSOLIDATED`.
