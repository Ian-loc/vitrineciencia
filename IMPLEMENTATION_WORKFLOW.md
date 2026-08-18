# Workflow de implementação — Vitrine Ciência

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
Nova fonte/produto/distribuição ou correção factual.

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

Para nova fonte:

- checar duplicidade;
- verificar identidade, cobertura Brasil, acesso, responsável e evidência;
- atribuir próximo `DR####`;
- atualizar P0–P3;
- adicionar produtos materialmente úteis;
- adicionar ao menos uma distribuição por produto;
- preservar licenças e limitações no nível adequado.

Para novos produtos:

- não enumerar arquivos/bandas/tiles sem ganho material;
- usar `external_index` para megacatálogos;
- registrar suporte/resolução/temporalidade somente quando sustentados.

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
- snapshot atual quando números forem necessários;
- estado `unreleased` até release explícita;
- Drive como derivado;
- Simbiotrama como projeto separado.

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

Em 18/08/2026: **125 fontes, 752 produtos e 783 distribuições**; IDs correntes chegam a `DR0125`, `DP000756` e `DD000787`. A prioridade operacional é continuar expansão/qualidade, manter documentação e publicação coerentes e preparar uma primeira release científica quando o snapshot escolhido estiver tecnicamente defensável.
