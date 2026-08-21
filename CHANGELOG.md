# Histórico de mudanças

O projeto segue versionamento semântico. A `main` pode avançar entre releases; itens posteriores ao último snapshot congelado permanecem em **Não lançado**.

## Não lançado

- fase ativa alterada para **QA/QC e manutenção**, com expansão de novas fontes/produtos/distribuições pausada até nova decisão humana explícita;
- smoke-test público alinhado à fronteira real do GitHub Pages: CSVs canônicos internos deixaram de ser tratados como endpoints públicos esperados e passaram a ser verificados como não publicados;
- smoke-test pós-deploy passou a validar o `head_sha` exato do workflow publicado, evitando falso negativo quando a `main` avança antes do teste externo;
- workflow legado `validate-source-corrections.yml`, incompatível com a fronteira pública atual e preso ao antigo baseline de 51 fontes, removido;
- validador legado `scripts/validate_frontend.py`, ainda preso à identidade `Science Data Sources Catalog` e ao gate fixo de 51 fontes, removido; checklist de PR alinhado aos validadores atuais da Vitrine;
- workflow de Pages passou a usar **privilégio mínimo por job**: PRs/validação mantêm apenas `contents: read`, enquanto `pages: write` e `id-token: write` ficam restritos ao job de deploy;
- empacotamento do candidato Zenodo v1.0.0 deixou de rodar automaticamente em PRs durante a fase de QA/QC e passou a ser **somente manual (`workflow_dispatch`)**, evitando artefatos de release desnecessários;
- documentos duplicados de licença de dados foram sincronizados e o gate de documentação ativa passou a impedir nova divergência entre eles;
- o changelog deixou de apresentar `v1.0.0` como release formal já publicada enquanto não existem tag Git imutável, GitHub Release e DOI.

## Candidata v1.0.0 — 19 de agosto de 2026

Snapshot candidato à primeira release científica estável e à preservação com DOI. Este estado **ainda não constitui uma release formal publicada**: a tag Git imutável, o GitHub Release e o depósito/DOI permanecem pendentes de decisão humana explícita.

- contrato público estabilizado em três tabelas: fonte → produto → distribuição;
- snapshot candidato congelado com **135 fontes, 843 produtos e 876 distribuições**;
- identificadores correntes até `DR0135`, `DP000861` e `DD000894`, com lacunas históricas preservadas e IDs não reciclados;
- schema estável de **34 campos para fontes, 24 produtos e 15 distribuições**;
- expansão Brasil-primeiro com fontes institucionais e produtos de ambiente, biodiversidade, clima, água, geociências, agricultura, florestas, sensoriamento remoto, saúde, educação, território e políticas públicas;
- classificação territorial P0–P3 mantida como camada curatorial vinculada às fontes;
- camada pública derivada com seis áreas amplas e normalização conservadora de suporte espacial e frequência de atualização, preservando o texto detalhado original;
- fortalecimento da validação relacional, papéis de links, build isolado, QA visual e smoke pós-deploy;
- separação explícita entre licenciamento do código (MIT), curadoria/metadados originais (CC BY 4.0) e licenças dos datasets externos catalogados;
- a branch candidata `release/v1.0.0` pode declarar versão `1.0.0`; a `main` permanece `unreleased` até a publicação formal;
- documentação de release/DOI consolidada e pacote de depósito definido como **Dataset**;
- Drive reafirmado como espelho/histórico derivado, não como autoridade concorrente;
- Vitrine Ciência e Simbiotrama mantidos como projetos estruturalmente independentes.

### Separação estrutural — Vitrine Ciência × Simbiotrama — 9 de agosto de 2026

- repositório consolidado como **Vitrine Ciência** (`Ian-loc/vitrineciencia`);
- Vitrine estabelecida como produto público estático independente;
- Simbiotrama passou a possuir repositório próprio `Ian-loc/simbiotrama`;
- PR #70 incorporado à `main` no commit `36211e96edc86fa0e2bb31c703141cd7c5df5480`;
- URL canônica: `https://ian-loc.github.io/vitrineciencia/`;
- workflow de Pages desacoplado de PostgreSQL/PostGIS e jobs do Simbiotrama;
- artefato público limitado à superfície da Vitrine;
- materiais históricos do Simbiotrama preservados sem autoridade operacional sobre a Vitrine.

### Histórico pré-separação

Antes de 09/08/2026, este repositório também abrigou desenvolvimento do Simbiotrama/Simbioscópio, incluindo propostas de PostgreSQL/PostGIS, Instâncias 1–3, roadmaps relacionais, migrações e contratos de comparabilidade. Esses registros permanecem no histórico por proveniência, mas não representam o escopo ativo da Vitrine.

## 0.7.0 — 18 de julho de 2026

- `data/data_resources.csv` consolidado como fonte canônica inicial;
- esquema de fontes ampliado para 34 campos;
- baseline inicial de 51 fontes revisado;
- incorporadas evidências acadêmicas, técnicas e oficiais representativas;
- separados download, acesso programático, protocolos e autenticação;
- adicionadas páginas de catálogo, análise, método e citação;
- adicionados metodologia, codebook, licenças e `CITATION.cff`.

## 0.6.0 — 18 de julho de 2026

- definida a autoridade inicial do CSV no GitHub;
- ampliado o esquema de fontes de 22 para 26 campos;
- revisadas identidade, utilidade, limitações, links e acesso;
- adicionadas validação automática e geração do JSON público.

> Nota: versões 0.6/0.7 e o baseline de 51 fontes são marcos históricos anteriores à candidata `v1.0.0`; a primeira release científica estável somente existirá após publicação formal de tag/release imutável.
