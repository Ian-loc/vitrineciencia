# Workflow de implementação — Vitrine Ciência

**Estado operacional:** QA/QC e manutenção. A expansão de novas fontes, produtos e distribuições está **pausada** e só pode ser retomada por instrução humana explícita.

## Objetivo

Executar mudanças de dados, interface, documentação e release em pacotes pequenos, verificáveis e encerráveis, preservando o contrato fonte → produto → distribuição e a publicação estática.

## Princípios

1. as três tabelas CSV são canônicas;
2. JSONs e `_site` são derivados;
3. o Drive é espelho/histórico derivado;
4. CI verde valida estrutura e regressão, não fatos externos;
5. valores factuais exigem evidência proporcional;
6. IDs existentes são estáveis;
7. crescimento não exige migração de schema;
8. desconhecido pode permanecer desconhecido;
9. release/DOI congela um snapshot, não encerra a curadoria;
10. Simbiotrama e arquitetura relacional são fora do escopo operacional da Vitrine.

## Classes de pacote

### DATA
Correção factual ou semântica de registros existentes. Criação de nova fonte/produto/distribuição somente após retomada explícita da expansão por decisão humana.

### FIX
Correção de interface, build, navegação, acessibilidade ou publicação.

### DOC
Alinhamento de documentação/estado sem mudança conceitual.

### RELEASE
Tag, release notes, snapshot, citação e eventual depósito.

### INFRA
Mudança estrutural de schema/runtime; excepcional e HUMAN-DECISION.

## Fluxo padrão

1. partir do `main` atual;
2. declarar escopo e critério de conclusão;
3. reunir evidência necessária;
4. criar branch dedicada;
5. alterar somente o delta pertinente;
6. rodar validadores proporcionais;
7. revisar o diff;
8. executar QA renderizado/público quando necessário;
9. integrar conforme classe de risco;
10. verificar `main` e deploy;
11. registrar conclusão/changelog quando material.

## DATA

Enquanto a expansão estiver pausada:

- corrigir somente defeitos factuais, semânticos ou relacionais sustentados;
- preservar IDs canônicos e não reutilizar IDs removidos;
- remover duplicatas apenas quando a equivalência estiver comprovada, preservando o ID canônico mais antigo;
- não criar nova fonte, produto ou distribuição para preencher lacunas de QA;
- manter desconhecido/variável quando a evidência não justificar maior precisão.

Se a expansão for retomada por instrução humana explícita, voltam a valer os critérios de seleção, deduplicação, evidência, cobertura Brasil, licenças e granularidade material definidos nas políticas vigentes.

## FIX/frontend

Quando o delta afetar a interface, verificar conforme aplicável:

- carregamento;
- busca e filtros;
- comparação;
- análise descritiva;
- links e downloads;
- desktop/mobile;
- teclado/foco/acessibilidade;
- artefato `_site`;
- smoke após deploy.

## DOC

Documentação ativa deve refletir:

- identidade Vitrine Ciência;
- autoridade da `main` e dos três CSVs;
- estado vivo apenas nos documentos designados para isso;
- estado `unreleased` até release explícita;
- Drive como derivado;
- Simbiotrama como projeto separado;
- fase corrente de QA/QC e pausa de expansão.

Documentos históricos não devem ser reescritos como se fossem fatos atuais; devem ser classificados como histórico/proveniência.

## RELEASE

Antes de release estável:

- validar dados/relações e interface;
- alinhar README, metodologia, codebook, changelog e `CITATION.cff`;
- congelar tag/commit;
- construir snapshot reproduzível;
- inspecionar artefato;
- publicar GitHub Release;
- depositar no Zenodo somente após decisão humana e conferir metadados/arquivos antes de publicar o DOI.

## Validadores principais

```bash
python3 scripts/validate_brazil_scope.py
python3 scripts/validate_product_catalog.py
python3 scripts/validate_schema_identity.py
python3 scripts/validate_active_documentation.py
python3 scripts/build_catalog.py
python3 scripts/audit_link_roles.py --write
python3 scripts/validate_vitrine.py
python3 scripts/build_site_artifact.py
node --check assets/app.js
node --check assets/products.js
node --check assets/analytics.js
```

Outros testes são adicionados conforme o delta.

## Estado corrente

A autoridade do estado vivo é `docs/PROJECT_STATE.md`, `WORKFLOW_STATUS.md` e as três tabelas CSV canônicas. Este documento não replica contagens voláteis.

A fase operacional corrente é **QA/QC e manutenção**, com expansão de novas fontes, produtos e distribuições **pausada até nova instrução humana explícita**. As prioridades são disponibilidade/publicação, integridade canônica, QA semântico, documentação/release, robustez do CI e correções funcionais de UX.
