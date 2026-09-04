# Estado do workflow — Vitrine Ciência

Atualização: **2026-09-04** (`America/Sao_Paulo`)

## Autoridade operacional

O GitHub é a autoridade canônica. `main` representa o estado público corrente; Drive, worktrees locais, handoffs e chats não substituem o que está materializado e validado no repositório.

Arquivos/matrizes que controlam o marco estático:

- `data/data_resources.csv`, `data/data_products.csv`, `data/product_distributions.csv`;
- `data/static_core_51_access_audit.json`;
- `data/static_core_51_progress.json`;
- `data/applied_priority_gate.json`;
- scripts de build e validação.

Artefatos públicos são derivados dessas autoridades.

## Fase ativa

A frente ativa é o **fechamento da Fase III — QA/QC e consolidação funcional da Vitrine estática DR0001–DR0051**.

A expansão geral permanece pausada. O estado público usa **51 registros DR, 11 itens detalhados e 19 distribuições**; os 11/19 são subconjunto detalhado. A expansão histórica 135/843/876 permanece em quarentena.

A recertificação semântica está concluída em **51/51**. A matriz corrente de acesso é **A=1, B=38, C=0, D=10, E=2**; `DR0014` e `DR0039` permanecem E de forma deliberada e documentada.

## Contrato operacional

`DR####` é identificador legado de entrada, não classe ontológica. A estrutura `Fonte → Produto → Distribuição` permanece apenas para compatibilidade e rastreabilidade.

A experiência pública deve seguir:

**pergunta científica → fenômeno/processo → território/tempo/escala → dataset/família de dados → produto científico quando necessário → distribuição/rota de acesso ou DataService → provedor/proveniência → documentação**.

Devem permanecer distintos quando aplicável: Provider/Institution, Program/Initiative, Platform/Catalog/Data Infrastructure, Dataset/Collection, Product, Distribution, DataService, Portal/Viewer e Documentation/Publication.

## Estado das fases

1. **Fase I — reconciliar e fixar o estado real: CONCLUÍDA**
   - 51/51 com tipagem semântica factual;
   - 51/51 com rota A–E e justificativa;
   - dois E preservados como limitações verificadas, não pendências ocultas.

2. **Fase II — reorganizar a representação estática: MATERIALIZADA**
   - Home orientada por pergunta/tema;
   - `sources.html` como descoberta ampla dos 51;
   - `products.html` como subconjunto detalhado 11/19;
   - Baixar dados / Página do conjunto / API-serviço / Viewer / Documentação / Provedor separados por função;
   - P1–P6 materializado na superfície pública.

3. **Fase III — consolidação funcional: EM FECHAMENTO**
   - QA estrutural, semântico, científico e de navegação;
   - filtros, URL params, teclado/acessibilidade básica, desktop/tablet/mobile;
   - zero CTA de dados/download/API apontando silenciosamente para viewer/PDF/documentação/homepage genérica;
   - CI principal, QA visual e smoke público no SHA final;
   - documentação e checkpoint sincronizados com `main`.

## Classificação de acesso

- **A DIRECT_DATA** — arquivo/download/endpoint que entrega dados.
- **B DATASET_PAGE** — página específica com mecanismo explícito de obtenção.
- **C API_SERVICE** — API/OGC/STAC/CKAN/GraphQL ou serviço de consulta/extração como rota principal.
- **D VIEWER_DOC** — viewer, mapa, dashboard, documentação ou PDF sem acesso de dados demonstrado na rota principal.
- **E BROKEN_UNCERTAIN** — rota genérica, inadequada como acesso agregado ou sem obtenção demonstrada.

Somente A–C podem ser apresentados como acesso confirmado a dados. HTTP 200 isolado não é prova de acesso.

## Eficiência de execução

- não reabrir caso fechado sem nova evidência, conflito ou regressão;
- mudança factual começa na autoridade canônica apropriada e é propagada pelo build;
- não corrigir classificação apenas no HTML/JavaScript;
- bloqueio externo local não interrompe casos independentes;
- candidate delta → validação → escrita → read-back → QA;
- uma única branch sequencial por fechamento; nenhum PR concorrente para o mesmo marco.

## Gate P1–P6

P1 AdaptaBrasil MCTI; P2 MapBiomas Municípios; P3 IEDE-MG/FJP; P4 BDMG com dado público verificável; P5 SICAR/CAR e SIGEF/INCRA separados; P6 IBGE Cidades e Estados. Todos devem permanecer sustentados por objeto informacional real, proveniência e acesso corretamente rotulado.

## Definition of Done — `VITRINE_STATIC_51_STABLE`

O marco exige simultaneamente:

- `main` pública no núcleo 51, com expansão histórica fora do catálogo vivo;
- 51/51 com tipo/papel factual;
- 51/51 com fenômeno/processo, território, tipo de informação, proveniência e A–E sustentados;
- dataset/família como objeto científico central quando identificável, sem invenção;
- zero microproduto criado apenas por formato/protocolo/interface;
- Distribution, DataService, Viewer, Documentation e Provider/Provenance semanticamente distintos;
- P1–P6 factuais;
- filtros controlados funcionando e busca livre não principal;
- 11/19 explicitamente subconjunto;
- zero botão dados/download/API levando silenciosamente a viewer/PDF/documentação/homepage genérica;
- percurso tema → entrada/dataset → rota útil em 2–3 decisões nos casos representativos;
- CI principal + QA visual + smoke público PASS no SHA final;
- README/PROJECT_STATE/WORKFLOW_STATUS sincronizados com o estado material;
- checkpoint final curto no repo com contagens, tipologia, P1–P6 e limitações.

Somente então declarar:

`VITRINE_STATIC_51_STABLE`

Depois desse token, a execução recorrente do marco estático deve ser desativada.

## Fora do escopo até esse marco

- ontologia 2.0 exaustiva;
- Integration Registry;
- conectores federados;
- harvesting;
- PostgreSQL/backend próprio;
- reentrada da expansão;
- nova release/DOI.
