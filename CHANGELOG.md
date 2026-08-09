# Histórico de mudanças

Este projeto segue versionamento semântico. Alterações ainda não publicadas são agrupadas em uma única seção; detalhes operacionais permanecem rastreáveis no histórico de commits, pull requests e auditorias arquivadas.

## Não lançado

### Separação estrutural — Vitrine Ciência × Simbiotrama — 2026-08-09

- o repositório foi renomeado e consolidado como **Vitrine Ciência** (`Ian-loc/vitrineciencia`);
- a Vitrine passou a ser tratada como produto público estático independente;
- o **Simbiotrama** passou a possuir repositório próprio em `Ian-loc/simbiotrama`;
- PR #70 incorporado à `main` no commit `36211e96edc86fa0e2bb31c703141cd7c5df5480`;
- URL canônica da Vitrine atualizada para `https://ian-loc.github.io/vitrineciencia/`;
- workflow de Pages desacoplado de PostgreSQL/PostGIS e de todos os jobs da Instância 1 do Simbiotrama;
- artefato público reduzido à superfície da Vitrine: fontes, produtos, análise, método/citação, assets e dados estáticos necessários;
- `explorer.html`, `abordagens.html`, `data/federated_layers.json` e superfícies Simbiotrama/Simbioscópio excluídos do artefato publicado;
- criado validador de fronteira que impede regressão da identidade pública ou reintrodução de dependência do Simbiotrama;
- conteúdo científico das 51 fontes canônicas preservado durante a separação;
- branches e PRs históricos/migratórios do Simbiotrama preservados temporariamente como evidência, sem autorização para merge na Vitrine;
- documentação oficial atualizada com contrato operacional, governança e marco estrutural.

### Histórico pré-separação preservado

Os itens abaixo registram a evolução ocorrida antes da cisão dos repositórios. Referências a Simbiotrama/Simbioscópio nessa seção são históricas e **não** representam o escopo ativo da Vitrine.

#### Sanity pós-Marco 1

- nome canônico então padronizado como **Simbiotrama**;
- criado `docs/PROJECT_STATE.md` para classificar `ACTIVE`, `BACKLOG`, `LEGACY_OPERATIONAL`, `RETIRED` e `HISTORICAL_EVIDENCE`;
- criado roadmap canônico `docs/roadmap/SIMBIOTRAMA_IMPLEMENTATION_ROADMAP.md`;
- caminho antigo do roadmap do Simbioscópio convertido em alias aposentado para preservar links históricos;
- governança, direção científica, decisão arquitetural e README alinhados ao estado pós-Marco 1;
- PR #53 fechado como `superseded`, sem incorporação de registros paralelos ou classes universais de compatibilidade;
- documentação de marcos reduzida ao registro consolidado, política de pacotes, índice e estado legível por máquina;
- explorador visual N0 e `data/federated_layers.json` classificados como legado operacional sem desenvolvimento analítico ativo;
- validador científico ampliado para testar autoridade, ciclo de vida, roadmap, nomenclatura e preservação do legado N0.

#### Adicionado — Instância 1

- decisão estratégica que estabeleceu a **Instância 1 — Catálogo relacional científico-operacional** como foco ativo daquela frente;
- documentação canônica da Instância 1;
- modelo PostgreSQL/PostGIS para organizações, fontes, famílias, produtos, releases, variáveis, métodos, perfis espaciais e temporais, qualidade, distribuições, ativos, capacidades, taxonomias, citações, evidências e revisões;
- schema de staging para migração sem perda dos CSVs;
- registro de problemas e bloqueios de migração;
- workflow contínuo de curadoria produto por produto;
- portões de migração, aprofundamento, interface e promoção do banco;
- definição de `information_message` e `non_representations`;
- evidência de metadados por entidade e campo.

#### Alterado — direção do projeto naquela fase

- projeto então recentrado no aprofundamento do catálogo antes de novas capacidades analíticas;
- PostgreSQL/PostGIS definido como arquitetura de destino do Simbiotrama;
- CSVs mantidos como autoridade pública transitória;
- separação normativa reforçada entre organização, fonte, família, produto, release, distribuição, ativo e variável;
- Instâncias 2 e 3 registradas como backlog do Simbiotrama;
- política de comparabilidade e inferência mantida como guardrail futuro.

#### Preservado do desenvolvimento anterior

- camada pública de fontes, produtos e distribuições que originou a atual Vitrine;
- classificação territorial Brasil-primeiro;
- Dynamic World V1 como produto piloto selecionado;
- validações, governança, contribuição, citação, licença e proveniência.

## 0.7.0 — 2026-07-18

- consolidado `data/data_resources.csv` como fonte canônica;
- ampliado o esquema para 34 campos;
- revisadas 51 fontes de dados;
- incorporadas evidências acadêmicas, técnicas e oficiais representativas;
- condensados temas em nove áreas de pesquisa;
- separados download, acesso programático, protocolos e autenticação;
- adicionadas páginas de catálogo, análise, método e citação;
- adicionados metodologia, codebook, licenças separadas e `CITATION.cff`.

## 0.6.0 — 2026-07-18

- definida a autoridade do CSV no GitHub;
- ampliado o esquema de 22 para 26 campos;
- revisadas identidade, utilidade, limitações, links e condições de acesso;
- adicionadas validação automática e geração do JSON público.
