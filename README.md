# Vitrine Ciência

**Catálogo público e citável para descobrir e acessar dados científicos relevantes ao Brasil.**

## Estado atual — 4 de setembro de 2026

- **Autoridade canônica:** o repositório `Ian-loc/vitrineciencia`; `main` é o estado público corrente. Worktrees locais, Drive, handoffs e chats são auxiliares e não substituem o que está materializado no GitHub.
- O catálogo vivo usa o núcleo estático de **51 registros legados DR0001–DR0051**.
- Na estrutura física legada, o estado público contém **51 registros DR, 11 itens detalhados e 19 distribuições**. Os 11/19 são um subconjunto detalhado, não toda a cobertura científica dos 51.
- A expansão histórica **135/843/876** permanece preservada em `data/quarantine/v1.0.0-expanded/` e fora do catálogo vivo.
- A recertificação semântica está concluída em **51/51**; `DR####` é identificador legado de entrada, não classe ontológica.
- A matriz canônica de acesso registra **A=1, B=38, C=0, D=10, E=2**. Os dois E (`DR0014` e `DR0039`) são limitações deliberadamente documentadas, não pendências silenciosas.
- O gate aplicado P1–P6 está materializado para AdaptaBrasil, MapBiomas Municípios, IEDE-MG/FJP, BDMG, SICAR/CAR + SIGEF/INCRA e IBGE Cidades e Estados.
- O fechamento corrente é **QA funcional e sincronização documental** antes de declarar `VITRINE_STATIC_51_STABLE`.

## Direção pública

A experiência deve seguir:

**pergunta científica → fenômeno/processo → território/tempo/escala → dataset/família de dados → produto científico quando necessário → distribuição/rota de acesso ou DataService → provedor/proveniência → documentação**.

Busca livre não é o mecanismo principal. A interface privilegia filtros controlados e encaminhamento a rotas cuja função foi classificada explicitamente.

## Modelo e autoridade dos dados

A estrutura histórica `Fonte (DR) → Produto (DP) → Distribuição (DD)` permanece para **compatibilidade, IDs e rastreabilidade**; ela não é tratada como ontologia final.

As autoridades materiais do estado estático são:

- `data/data_resources.csv`, `data/data_products.csv`, `data/product_distributions.csv` — estrutura física canônica legada;
- `data/static_core_51_access_audit.json` — classificação factual da rota principal A–E;
- `data/static_core_51_progress.json` — recertificação semântica/tipagem 51/51;
- `data/applied_priority_gate.json` — gate aplicado P1–P6;
- scripts de build/validação — regras de materialização e QA;
- JSONs públicos, HTML e artefato `_site` — **derivados**, não fontes independentes de verdade.

Quando aplicável, devem permanecer distintos: Provider/Institution, Program/Initiative, Platform/Catalog/Data Infrastructure, Dataset/Collection, Product, Distribution, DataService, Portal/Viewer e Documentation/Publication. Formato, arquivo, API, viewer ou documentação não criam produto científico por conveniência. Proveniência é transversal ao objeto de dados.

## Classificação de acesso

- **A DIRECT_DATA** — arquivo, diretório ou endpoint que entrega dados;
- **B DATASET_PAGE** — página específica com mecanismo explícito de obtenção;
- **C API_SERVICE** — API/OGC/STAC/CKAN/GraphQL ou serviço de consulta/extração como rota principal;
- **D VIEWER_DOC** — viewer, mapa, dashboard ou documentação sem acesso de dados demonstrado na rota principal;
- **E BROKEN_UNCERTAIN** — rota genérica, inadequada como acesso agregado ou não demonstrada para obtenção de dados.

Somente A–C podem ser apresentados como acesso confirmado a dados. HTTP 200 isolado não comprova acesso científico.

## Fase operacional

A Fase I de reconciliação e a recertificação semântica 51/51 estão concluídas. A Fase II de reorganização estática está materializada. A frente ativa é o **fechamento da Fase III**:

1. manter Home, `sources.html` e `products.html` coerentes com a tipologia e a classificação A–E;
2. confirmar filtros controlados, parâmetros de URL, teclado/acessibilidade e responsividade;
3. garantir zero botão de dados/download/API apontando silenciosamente para viewer/PDF/documentação/homepage genérica;
4. obter CI principal, QA visual e smoke público verdes no SHA final;
5. sincronizar README, `docs/PROJECT_STATE.md`, `WORKFLOW_STATUS.md` e checkpoint final.

Somente então declarar `VITRINE_STATIC_51_STABLE`.

## Federação por APIs

Federação permanece **fora deste marco**. Até `VITRINE_STATIC_51_STABLE`, não iniciar Integration Registry, conectores STAC/CKAN/OGC/REST/GraphQL, harvesting, PostgreSQL/backend próprio ou reentrada da expansão. Nenhum recurso descoberto por API entra automaticamente na superfície pública.

## Release científica v1.0.0

A release histórica permanece imutável e reproduzível:

- GitHub Release: https://github.com/Ian-loc/vitrineciencia/releases/tag/v1.0.0
- Zenodo: https://zenodo.org/records/22130831
- DOI: https://doi.org/10.5281/zenodo.22130831
- commit congelado: `27c545554f406b940662777e3f053e939ef3588c`

## Autoridade operacional

- estado corrente: `docs/PROJECT_STATE.md`;
- execução e gates: `WORKFLOW_STATUS.md`;
- direção científica: `docs/PROJECT_SCIENTIFIC_DIRECTION.md`;
- contrato legado/transitório: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`;
- matriz de acesso: `data/static_core_51_access_audit.json`;
- recertificação semântica: `data/static_core_51_progress.json`;
- gate aplicado: `data/applied_priority_gate.json`;
- repositório: https://github.com/Ian-loc/vitrineciencia;
- site: https://ian-loc.github.io/vitrineciencia/.

Código: MIT. Metadados e curadoria original: CC BY 4.0.

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. Version 1.0.0. Zenodo, 2026. https://doi.org/10.5281/zenodo.22130831
