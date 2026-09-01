# Workflow de implementação — Vitrine Ciência

**Estado operacional:** QA/QC, re-curadoria e auditoria ontológica.  
A expansão de novas fontes, produtos e distribuições está **pausada** e só pode ser retomada por **instrução humana explícita**. Os termos são mantidos aqui para compatibilidade com o schema legado.

## Objetivo atual

Executar a consolidação em etapas verificáveis, sem antecipar schema ou federação antes de resolver a identidade dos 51 registros legados.

## Sequência obrigatória

1. **Inventário** — reconciliar DR0001–DR0051 e evidências existentes.
2. **Evidência** — usar documentação oficial/primária proporcional ao problema.
3. **Classificação ontológica** — determinar o que cada DR representa; não forçar `fonte`.
4. **Crosswalk** — legado → entidade(s) canônica(s) → relações → ação de migração.
5. **Validação G0–G4** — somente então congelar o novo modelo.
6. **Integration Registry** — mapear API/serviço/download/manual para 51/51.
7. **Pilotos** — MapBiomas Alerta primeiro; depois casos tecnologicamente distintos.
8. **Pipeline** — raw → normalize → validate → deduplicate → classify → verify_access → quarantine/accept → publish.
9. **QA e reprodução** — testes, read-back, build limpo e smoke público.
10. **Consolidação** — somente trabalho materializado e verificado conta como concluído.

## Regras

- preservar IDs e histórico;
- CI verde valida estrutura/regressão, não fatos externos;
- não inferir informação ausente;
- não publicar raw automaticamente;
- falha de gate impede promoção;
- a release `v1.0.0` não é reescrita;
- nenhum merge/release/DOI é autorizado por este documento.

## Classes de trabalho

- **DOC/QA:** alinhamento de estado, precisão, testes e documentação.
- **CURATION:** classificação factual/semântica sustentada por evidência.
- **ONTOLOGY/SCHEMA:** permitido somente após G0–G4.
- **FEDERATION:** permitido somente após Integration Registry.
- **RELEASE:** somente após o marco global e decisão humana específica.

## Autoridade documental

- estado: `docs/PROJECT_STATE.md`;
- direção: `docs/PROJECT_SCIENTIFIC_DIRECTION.md`;
- workflow/limite: `WORKFLOW_STATUS.md`;
- contrato transitório: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`.

A fase corrente de QA/QC deve permanecer explícita nesses documentos. A expansão de novas fontes, produtos e distribuições permanece pausada até instrução humana explícita.
