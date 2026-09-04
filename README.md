# Vitrine Ciência

**Catálogo público e citável para descobrir e acessar dados científicos relevantes ao Brasil.**

## Estado atual — 4 de setembro de 2026

- **Autoridade canônica:** o repositório `Ian-loc/vitrineciencia`; `main` é o estado público corrente. Worktrees locais, Drive, handoffs e chats são auxiliares e não substituem o que está materializado no GitHub.
- O marco estático do núcleo **DR0001–DR0051 está consolidado**: `VITRINE_STATIC_51_STABLE`.
- O runtime público validado é o commit **`495bfe6a968176670461662869d1a3773797baf3`**.
- Nesse runtime, os três gates finais passaram: build/deploy (`33906109623`), QA visual/responsivo (`33906109551`) e smoke pós-deploy (`33906157842`).
- O catálogo vivo usa **51 registros DR, 11 itens detalhados e 19 distribuições**. Os 11/19 são um subconjunto detalhado, não toda a cobertura científica dos 51.
- A expansão histórica **135/843/876** permanece preservada em `data/quarantine/v1.0.0-expanded/` e fora do catálogo vivo.
- A recertificação semântica está concluída em **51/51**; `DR####` é identificador legado de entrada, não classe ontológica.
- A matriz canônica de acesso registra **A=1, B=38, C=0, D=10, E=2**. Os dois E (`DR0014` e `DR0039`) são limitações deliberadamente documentadas, não pendências silenciosas.
- O gate aplicado P1–P6 está materializado para AdaptaBrasil, MapBiomas Municípios, IEDE-MG/FJP, BDMG, SICAR/CAR + SIGEF/INCRA e IBGE Cidades e Estados.
- O artefato público fecha suas dependências locais e separa explicitamente a autoridade de tipagem semântica da autoridade A–E de acesso.

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

## Estado operacional

As três fases do marco estático estão concluídas:

1. **Fase I — reconciliação e recertificação:** 51/51 semanticamente tipados e com A–E justificado.
2. **Fase II — representação estática:** Home tema-first, `sources.html` para os 51, `products.html` para o subconjunto 11/19 e P1–P6 integrado.
3. **Fase III — consolidação funcional:** filtros controlados, runtime dos cards, papéis semânticos, fechamento de dependências, responsividade, deploy e smoke público validados.

A **fase ativa de QA/QC e manutenção** passa a ser manutenção do marco estável e correção de regressões; não significa recertificação pendente.

## Próximo milestone

Federação por APIs/Data Services é um **novo milestone**, separado do marco estático e ainda não ativado automaticamente. Integration Registry, conectores STAC/CKAN/OGC/REST/GraphQL, harvesting, PostgreSQL/backend próprio ou reentrada da expansão exigem autorização e escopo próprios. Nenhum recurso descoberto por API entra automaticamente na superfície pública.

## Release científica v1.0.0

A release histórica permanece imutável e reproduzível:

- GitHub Release: https://github.com/Ian-loc/vitrineciencia/releases/tag/v1.0.0
- Zenodo: https://zenodo.org/records/22130831
- DOI: https://doi.org/10.5281/zenodo.22130831
- commit congelado: `27c545554f406b940662777e3f053e939ef3588c`

## Autoridade operacional

- estado corrente: `docs/PROJECT_STATE.md`;
- execução e gates: `WORKFLOW_STATUS.md`;
- checkpoint do marco: `docs/CHECKPOINT_STATIC_51_2026-09-04.md`;
- direção científica: `docs/PROJECT_SCIENTIFIC_DIRECTION.md`;
- contrato legado/transitório: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`;
- matriz de acesso: `data/static_core_51_access_audit.json`;
- recertificação semântica: `data/static_core_51_progress.json`;
- gate aplicado: `data/applied_priority_gate.json`;
- repositório: https://github.com/Ian-loc/vitrineciencia;
- site: https://ian-loc.github.io/vitrineciencia/.

Código: MIT. Metadados e curadoria original: CC BY 4.0.

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. Version 1.0.0. Zenodo, 2026. https://doi.org/10.5281/zenodo.22130831
