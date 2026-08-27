# Histórico de mudanças

O projeto segue versionamento semântico. A `main` pode avançar entre releases; itens posteriores ao último snapshot congelado permanecem em **Não lançado**.

## Não lançado

- DOI da release `v1.0.0` propagado para `CITATION.cff`, README, notas de release e ledger de prontidão DOI após publicação no Zenodo;
- fase ativa alterada para **QA/QC e manutenção**, com expansão de novas fontes/produtos/distribuições pausada até nova decisão humana explícita;
- smoke-test público alinhado à fronteira real do GitHub Pages: CSVs canônicos internos deixaram de ser tratados como endpoints públicos esperados e passaram a ser verificados como não publicados;
- smoke-test pós-deploy passou a validar o `head_sha` exato do workflow publicado, evitando falso negativo quando a `main` avança antes do teste externo;
- workflow legado `validate-source-corrections.yml`, incompatível com a fronteira pública atual e preso ao antigo baseline de 51 fontes, removido;
- validador legado `scripts/validate_frontend.py`, ainda preso à identidade `Science Data Sources Catalog` e ao gate fixo de 51 fontes, removido; checklist de PR alinhado aos validadores atuais da Vitrine;
- workflow de Pages passou a usar **privilégio mínimo por job**: PRs/validação mantêm apenas `contents: read`, enquanto `pages: write` e `id-token: write` ficam restritos ao job de deploy;
- empacotamento Zenodo v1.0.0 deixou de rodar automaticamente em PRs durante a fase de QA/QC e passou a ser **somente manual (`workflow_dispatch`)**, evitando artefatos de release desnecessários;
- documentos duplicados de licença de dados foram sincronizados e o gate de documentação ativa passou a impedir nova divergência entre eles.

## v1.0.0 — snapshot de 19 de agosto de 2026; publicação formal em 27 de agosto de 2026

Primeira release científica estável da Vitrine Ciência, publicada como tag Git anotada e GitHub Release e preservada no Zenodo como Dataset.

- DOI: `10.5281/zenodo.22130831`;
- Zenodo: https://zenodo.org/records/22130831;
- GitHub Release: https://github.com/Ian-loc/vitrineciencia/releases/tag/v1.0.0;
- commit científico congelado: `27c545554f406b940662777e3f053e939ef3588c`;
- arquivo científico preservado: `vitrine-ciencia-v1.0.0.zip`;
- SHA-256 do arquivo científico: `b2e7a996b075d45ef4caca853bf57618b54998724fc9b4bdea3afe3b6159d6f0`;
- contrato público estabilizado em três tabelas: fonte → produto → distribuição;
- snapshot congelado com **135 fontes, 843 produtos e 876 distribuições**;
- identificadores correntes até `DR0135`, `DP000861` e `DD000894`, com lacunas históricas preservadas e IDs não reciclados;
- schema estável de **34 campos para fontes, 24 para produtos e 15 para distribuições**;
- expansão Brasil-primeiro com fontes institucionais e produtos de ambiente, biodiversidade, clima, água, geociências, agricultura, florestas, sensoriamento remoto, saúde, educação, território e políticas públicas;
- classificação territorial P0–P3 mantida como camada curatorial vinculada às fontes;
- camada pública derivada com seis áreas amplas e normalização conservadora de suporte espacial e frequência de atualização, preservando o texto detalhado original;
- fortalecimento da validação relacional, papéis de links, build isolado, QA visual e smoke pós-deploy;
- separação explícita entre licenciamento do código (MIT), curadoria/metadados originais (CC BY 4.0) e licenças dos datasets externos catalogados;
- documentação de release/DOI consolidada e depósito definido como **Dataset**;
- Drive reafirmado como espelho/histórico derivado, não como autoridade concorrente;
- Vitrine Ciência e Simbiotrama mantidos como projetos estruturalmente independentes.

A `main` e a interface pública permanecem vivas e podem avançar após a release. A reprodutibilidade de `v1.0.0` é definida pela tag, pelo commit congelado e pelo depósito Zenodo, e não pelo estado posterior da `main`.

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

> Nota: versões 0.6/0.7 e o baseline de 51 fontes são marcos históricos anteriores à primeira release científica estável `v1.0.0`.
