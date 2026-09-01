# Vitrine Ciência

**Catálogo público e citável para descobrir dados científicos relevantes ao Brasil.**

A Vitrine Ciência está sendo re-curada para responder melhor a perguntas de pesquisa. A navegação prioriza **fenômenos e processos socioecológicos, território, tempo/escala e acesso aos dados**. Instituição provedora, nome técnico do produto, formato e plataforma aparecem como contexto de proveniência e uso.

## Estado vivo

A `main` apresenta o núcleo auditado anterior à expansão:

- **51 fontes**;
- **11 produtos**;
- **19 distribuições/acessos**.

A expansão de 135 fontes, 843 produtos e 876 distribuições da release `v1.0.0` foi preservada integralmente em `data/quarantine/v1.0.0-expanded/` e está fora da superfície viva enquanto passa por revisão de utilidade, granularidade, classificação e links.

A expansão de novas fontes, produtos e distribuições está pausada até instrução humana explícita.

## Release científica v1.0.0

A release histórica continua imutável e reproduzível:

- GitHub Release: https://github.com/Ian-loc/vitrineciencia/releases/tag/v1.0.0
- Zenodo: https://zenodo.org/records/22130831
- DOI: https://doi.org/10.5281/zenodo.22130831
- commit congelado: `27c545554f406b940662777e3f053e939ef3588c`
- snapshot: 135 fontes / 843 produtos / 876 distribuições.

Quarentena na `main` não altera a tag, o DOI ou o arquivo depositado.

## Como a Vitrine deve responder

A experiência pública segue a hierarquia:

**pergunta científica → fenômeno/processo → território → tempo/escala → conjunto de dados → forma de acesso → provedor/proveniência**.

Busca livre não é o mecanismo primário. A interface privilegia termos controlados e filtros determinísticos. Catálogos, APIs, serviços e visualizadores podem ser úteis, mas devem ser identificados como tal e não apresentados como se fossem datasets equivalentes.

## Modelo de dados

```text
Fonte (DR####)
  └── Produto (DP######)
        └── Distribuição (DD######)
```

- **Fonte**: quem mantém/produz ou oferece os dados.
- **Produto**: dataset, série, catálogo, serviço ou oferta cientificamente distinta.
- **Distribuição**: rota concreta de acesso, como download, API, WFS/WCS ou portal.

O modelo permanece estável; o que muda é a hierarquia de apresentação ao usuário.

## Qualidade de acesso

A curadoria distingue download direto, landing page com download, portal/API de extração, visualização/documentação e acesso incerto/restrito. Casos duvidosos são marcados para revisão em vez de convertidos em disponibilidade confirmada.

Antes de usar um conjunto de dados, confirme no provedor original versão, método, resolução, cobertura, licença e limitações.

## Autoridade

- site: https://ian-loc.github.io/vitrineciencia/
- repositório: https://github.com/Ian-loc/vitrineciencia
- dados vivos: `data/data_resources.csv`, `data/data_products.csv`, `data/product_distributions.csv`
- estado canônico: `docs/PROJECT_STATE.md`
- workflow corrente: `WORKFLOW_STATUS.md`
- código: MIT
- metadados e curadoria original: CC BY 4.0

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. Version 1.0.0. Zenodo, 2026. https://doi.org/10.5281/zenodo.22130831

ORCID: https://orcid.org/0000-0003-1164-9318
