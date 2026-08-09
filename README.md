# Vitrine Ciência

**Catálogo público e estático de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão.**

A Vitrine Ciência organiza e apresenta fontes e produtos de dados com busca, filtros, informações de acesso, cobertura, formatos, usos, limitações, evidências e links para as fontes originais.

## Produto público

- site: https://ian-loc.github.io/vitrineciencia/
- repositório: https://github.com/Ian-loc/vitrineciencia
- fontes: `data/data_resources.csv`
- produtos detalhados: `data/data_products.csv`
- distribuições de produtos: `data/product_distributions.csv`
- código: MIT
- metadados e curadoria original: CC BY 4.0

## Estado estrutural

Em 9 de agosto de 2026, a Vitrine e o Simbiotrama foram formalmente separados em repositórios e fluxos de trabalho independentes. O marco foi incorporado à `main` pelo PR #70, no commit `36211e96edc86fa0e2bb31c703141cd7c5df5480`.

A Vitrine é o produto público estático. O **Simbiotrama** é uma frente de trabalho diferente e possui repositório próprio: https://github.com/Ian-loc/simbiotrama

A Vitrine não depende de PostgreSQL/PostGIS, schemas, pipelines curatoriais ou CI do Simbiotrama para permanecer online. Falhas de desenvolvimento do Simbiotrama não devem bloquear o deploy da Vitrine, e alterações da Vitrine não devem alterar o estado do Simbiotrama.

Durante a migração protegida, materiais históricos do Simbiotrama podem continuar presentes em branches e no histórico Git deste repositório. Eles são evidência de preservação e não fazem parte do artefato publicado nem da autoridade ativa da Vitrine.

Documentos de governança:

- `docs/VITRINE_BOUNDARY.md` — fronteira operacional e contrato de disponibilidade;
- `docs/STRUCTURAL_SEPARATION_MILESTONE_2026-08-09.md` — registro do marco estrutural e de governança.

## Uso

A Vitrine apoia descoberta e triagem inicial. Antes de usar um dataset, confirme no produtor original a versão, licença, metodologia, resolução, cobertura, incerteza e condições de acesso.

## Manutenção

Mudanças em `main` devem preservar:

1. geração determinística dos dados públicos;
2. integridade de HTML/CSS/JavaScript;
3. funcionamento de busca, filtros, comparação e análise;
4. isolamento do artefato `_site`;
5. independência total do runtime/CI do Simbiotrama.

A disponibilidade externa do GitHub Pages é verificada após deployments; o CI protege a integridade do artefato, mas não substitui a verificação do estado externo de hospedagem.

## Citação

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. GitHub, 2026. https://ian-loc.github.io/vitrineciencia/

ORCID: https://orcid.org/0000-0003-1164-9318

A citação da Vitrine não substitui a citação da fonte, do produto e da versão originais.
