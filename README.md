# Vitrine Ciência

**Catálogo público, estático, versionado e citável de fontes e produtos de dados científicos relevantes ao Brasil para pesquisa, ensino e extensão.**

A Vitrine Ciência organiza fontes, produtos e formas de acesso com busca, filtros, cobertura, formatos, temporalidade, limitações, evidências e links para os provedores originais. Ela é uma infraestrutura de **descoberta e triagem**: não substitui os datasets originais, sua documentação ou sua citação.

## Produto público e autoridade

- site: https://ian-loc.github.io/vitrineciencia/
- repositório canônico: https://github.com/Ian-loc/vitrineciencia
- branch canônica de desenvolvimento: `main`
- primeira release científica estável: `v1.0.0`
- fontes: `data/data_resources.csv`
- produtos: `data/data_products.csv`
- distribuições/acessos: `data/product_distributions.csv`
- classificação territorial: `data/brazil_scope_priorities.json`
- código: MIT
- metadados e curadoria original: CC BY 4.0

### Snapshot v1.0.0 — 19 de agosto de 2026

- **135 fontes**;
- **843 produtos**;
- **876 distribuições**;
- os identificadores correntes chegam a `DR0135`, `DP000861` e `DD000894`, pois IDs removidos/consolidados não são reciclados;
- verificações de fontes registradas até **2026-08-19**.

Essas contagens descrevem o snapshot da release e não são limites arquiteturais. O desenvolvimento pode continuar na `main`; análises reproduzíveis devem registrar a release/tag ou o commit efetivamente utilizado.

## Modelo vigente

```text
Fonte (DR####)
  └── Produto (DP######)
        └── Distribuição (DD######)
```

A tabela de fontes possui 34 campos; a de produtos, 24; e a de distribuições, 15. O contrato é deliberadamente simples e estável. Novas entidades só devem ser introduzidas se uma diferença cientificamente material não puder ser representada no modelo atual.

## Fronteira com o Simbiotrama

Desde 9 de agosto de 2026, **Vitrine Ciência** e **Simbiotrama** são projetos independentes. O Simbiotrama possui repositório próprio e pode desenvolver arquitetura relacional, PostgreSQL/PostGIS e outras instâncias sem criar dependência de runtime, publicação ou governança para a Vitrine.

Documentos relacionais antigos ainda presentes neste histórico pertencem à fase pré-separação ou ao Simbiotrama e são tratados como **evidência histórica**, não como direção ativa da Vitrine.

## Uso científico

Antes de utilizar um produto catalogado, confirme no provedor original:

- versão/coleção efetivamente usada;
- método e significado da variável;
- suporte/resolução espacial e temporal;
- licença, atribuição e condições de acesso;
- incertezas, limitações e atualizações posteriores.

A presença na Vitrine não certifica qualidade universal, comparabilidade ou adequação a uma análise específica.

## Manutenção

O fluxo normal é:

**discover → verify → curate → validate → publish → monitor → periodically release**.

Mudanças em `main` devem preservar integridade dos IDs e relações, geração determinística dos artefatos públicos, isolamento de `_site`, funcionamento da interface e independência do Simbiotrama. O Drive é espelho/histórico derivado e não autoridade concorrente.

Documentação ativa:

- `docs/PROJECT_STATE.md` — estado canônico do projeto;
- `docs/PROJECT_SCIENTIFIC_DIRECTION.md` — direção científica;
- `docs/VITRINE_CANONICAL_DATA_CONTRACT.md` — contrato de dados;
- `docs/VITRINE_OPERATING_MODEL.md` — operação e gates;
- `WORKFLOW_STATUS.md` — estado corrente e prioridades;
- `FINAL_OBJECTIVES_AND_DOI_GATES.md` — release citável e DOI;
- `RELEASE_NOTES_v1.0.0.md` — notas da primeira release científica estável.

## Release e citação

A `v1.0.0` é o primeiro snapshot científico estável deliberadamente congelado da Vitrine Ciência. Para análises reproduzíveis, cite a release/tag ou commit efetivamente utilizado e também a fonte/dataset original.

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. Version 1.0.0. 2026.

ORCID: https://orcid.org/0000-0003-1164-9318

Após a emissão do DOI, o identificador persistente deve ser incorporado ao README, `CITATION.cff`, release do GitHub e perfis acadêmicos sem alterar retroativamente o conteúdo científico do snapshot.
