# Vitrine Ciência — fronteira operacional

Decisão de separação: **2026-08-09**  
Revisão da fronteira: **2026-08-18**

## Status

`Ian-loc/vitrineciencia` é a autoridade da **Vitrine Ciência**, catálogo público estático e continuamente publicável. O **Simbiotrama** é um projeto independente em `Ian-loc/simbiotrama` e não pode ser dependência de runtime, CI ou publicação da Vitrine.

## Contrato do artefato público

O GitHub Pages publica somente a superfície necessária ao produto:

- `index.html`;
- `products.html`;
- `analytics.html`;
- `about.html`;
- CSS/JavaScript necessários;
- três tabelas canônicas e JSONs/metadata estritamente necessários à interface;
- classificação territorial Brasil;
- licenças e metadados opcionais de site.

O builder executável é `scripts/build_site_artifact.py`.

## Material proibido no artefato público

- documentação operacional/auditorias internas;
- scripts, workflows e configurações de desenvolvimento;
- schemas ou material de banco relacional;
- migrações/filas curatoriais internas;
- páginas/artefatos do Simbiotrama ou Simbioscópio;
- `data/federated_layers.json` e outros legados não requeridos pela Vitrine;
- segredos, logs ou credenciais.

## CI e disponibilidade

A CI da Vitrine deve validar:

1. contrato e integridade dos dados;
2. classificação Brasil;
3. geração determinística dos artefatos;
4. integridade HTML/CSS/JavaScript;
5. contratos de busca/filtros/comparação quando aplicáveis;
6. construção isolada de `_site`;
7. deploy do GitHub Pages;
8. smoke externo pós-deploy.

PostgreSQL/PostGIS e jobs do Simbiotrama são dependências proibidas do grafo de deploy.

## Autoridade de dados

No snapshot de 18/08/2026 a Vitrine contém **125 fontes, 752 produtos e 783 distribuições**. IDs correntes chegam a `DR0125`, `DP000756` e `DD000787`; lacunas históricas não são recicladas. As contagens podem crescer; o contrato público é a coerência das três tabelas, não uma contagem fixa.

## Material histórico

Arquivos relacionais/Simbiotrama anteriores à separação podem permanecer na árvore Git como evidência histórica. `docs/PROJECT_STATE.md` os classifica como `HISTORICAL_EVIDENCE`. Eles não devem ser apresentados como direção ativa nem copiados para `_site`.

## Teste de regressão da separação

A fronteira permanece válida enquanto:

1. Vitrine CI passa sem jobs do Simbiotrama;
2. Pages contém somente o artefato da Vitrine;
3. site, pesquisa, filtros, produtos, análise e downloads permanecem funcionais;
4. URL canônica é `https://ian-loc.github.io/vitrineciencia/`;
5. falha no Simbiotrama não bloqueia/remove a Vitrine;
6. falha na Vitrine não altera o Simbiotrama;
7. nenhuma página pública apresenta Simbiotrama como identidade ativa da Vitrine.

O marco original permanece registrado em `docs/STRUCTURAL_SEPARATION_MILESTONE_2026-08-09.md`.
