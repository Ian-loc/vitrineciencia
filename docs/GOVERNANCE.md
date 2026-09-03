# Governança — Vitrine Ciência

**Atualização:** 2026-09-01  
**Fase:** QA/QC, re-curadoria e auditoria ontológica.

## Finalidade

A governança protege um produto simples, reproduzível e cientificamente defensável de descoberta e acesso a dados relevantes ao Brasil.

A expansão de novas fontes, produtos e distribuições está **pausada**. Esses termos pertencem ao schema legado; os 51 registros `DR0001–DR0051` estão sob auditoria ontológica.

## Autoridade

1. `main` para o estado público incorporado;
2. tag/release `v1.0.0` para o snapshot histórico imutável;
3. branch/PR em revisão para mudanças ainda não incorporadas;
4. dados, contratos e validadores do respectivo estado Git;
5. `docs/PROJECT_STATE.md` e `WORKFLOW_STATUS.md` para estado e execução;
6. evidências/auditorias;
7. artefatos derivados e espelhos.

PR draft não é `main`. CI verde não transforma branch candidata em estado público.

## Regime de mudança

`scope → evidence → implementation → validation → diff audit → public validation quando aplicável → integration → post-merge verification → consolidation`

### DOC/QA

Pode corrigir documentação, testes e estado sem ampliar escopo nem relaxar gates.

### CURATION / REVIEW

Classificações factuais e semânticas exigem evidência proporcional. Ambiguidade material permanece explícita.

### HUMAN-DECISION

Exige decisão humana explícita:

- retomada de expansão;
- merge final de pacote estrutural relevante;
- schema/ontologia incompatível;
- remoção destrutiva/em massa;
- nova infraestrutura estrutural;
- licença/autoria/citação oficial;
- release, tag ou DOI.

## Curadoria atual

Para `DR0001–DR0051`:

- preservar IDs legados;
- não assumir que todos são `fonte` do mesmo tipo;
- determinar identidade e tipo real com evidência oficial;
- separar provider, program, platform, catalog, infrastructure, dataset, service e viewer quando aplicável;
- construir crosswalk antes de congelar o novo schema;
- não implementar federação antes de G0–G4 PASS.

A relação física legada `DR → DP → DD` permanece válida para compatibilidade e reprodução; não é ontologia final.

## Automação

Automação pode coletar evidência, validar, comparar, detectar regressões e materializar artefatos. Não deve:

- inventar metadados;
- decidir sozinha ambiguidade científica relevante;
- publicar automaticamente tudo que uma API encontra;
- promover branch sem os gates previstos.

## Publicação

O Pages publica somente a superfície definida em `docs/VITRINE_BOUNDARY.md`. Quarentena, auditorias, segredos e material operacional não podem vazar para `_site`.

Publicação só é consolidada depois de build/CI e verificação pós-deploy aplicáveis.

## Releases

`v1.0.0` permanece imutável. Novo marco citável exige snapshot reproduzível, QA, tag/commit e decisão humana específica.

O limite da consolidação atual é `VITRINE_FEDERATED_CORE_V1_CONSOLIDATED`, definido em `WORKFLOW_STATUS.md`.
