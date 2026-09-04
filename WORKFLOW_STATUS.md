# Estado do workflow — Vitrine Ciência

Atualização: **2026-09-03** (`America/Sao_Paulo`)

## Fase ativa

A fase ativa é a **QA/QC, consolidação semântica e funcional da Vitrine Ciência estática com o núcleo DR0001–DR0051**.

O resgate S0 já foi incorporado e publicado. O PR `#267` está encerrado por merge e não deve ser reaberto. Há uma única frente executora recorrente para a Vitrine.

O estado público usa **51 registros DR, 11 itens detalhados e 19 distribuições**. Na terminologia física exigida pelo schema/validador legado, isso corresponde a **51 fontes, 11 produtos e 19 distribuições**; esses rótulos não definem a ontologia pública. Os 11/19 são subconjunto detalhado. A expansão histórica 135/843/876 permanece em quarentena e a expansão geral está **pausada**.

## Contrato operacional

`DR####` é identificador legado de entrada, não classe ontológica. A estrutura `Fonte → Produto → Distribuição` permanece apenas para compatibilidade e rastreabilidade.

A experiência pública deve seguir:

**pergunta científica → fenômeno/processo → território/tempo/escala → dataset/família de dados → produto científico quando necessário → distribuição/rota de acesso ou DataService → provedor/proveniência → documentação**.

Devem permanecer distintos quando aplicável: Provider/Institution, Program/Initiative, Platform/Catalog/Data Infrastructure, Dataset/Collection, Product, Distribution, DataService, Portal/Viewer e Documentation/Publication.

## Sequência de execução

1. **Fase I — reconciliar e fixar o estado real**
   - sincronizar documentos de autoridade com `main` publicado;
   - recertificar 51/51 por `entity_type/role`, fenômeno/processo, território, tipo de informação, proveniência, dataset/família quando sustentado, rota A–E e `last_verified`;
   - priorizar E, ambiguidades semânticas e depois D;
   - não forçar Dataset onde não houver evidência.
2. **Fase II — reorganizar a representação estática**
   - Home orientada por pergunta/tema;
   - `sources.html` como descoberta ampla dos 51;
   - `products.html` como subconjunto detalhado, reclassificado semanticamente quando necessário;
   - separar Baixar dados / Página do conjunto / API-serviço / Viewer / Documentação / Provedor / Acesso em revisão;
   - proveniência como relações transversais, não como pai único do dado.
3. **Fase III — consolidação funcional**
   - QA estrutural, semântico, científico e de navegação;
   - filtros, URL params, teclado/acessibilidade básica, desktop/tablet/mobile;
   - CI principal, QA visual e smoke público no SHA final.

## Classificação de acesso

- **A DIRECT_DATA** — arquivo/download/endpoint que entrega dados.
- **B DATASET_PAGE** — página específica com mecanismo explícito de obtenção.
- **C API_SERVICE** — API/OGC/STAC/CKAN/GraphQL ou serviço de consulta/extração.
- **D VIEWER_DOC** — viewer, mapa, dashboard, documentação ou PDF sem acesso de dados demonstrado.
- **E BROKEN_UNCERTAIN** — rota quebrada, restrita, genérica ou incerta.

Somente A–C podem ser apresentados como acesso confirmado a dados. HTTP 200 isolado não é prova de acesso.

## Eficiência de execução

- usar `data/static_core_51_access_audit.json` como matriz persistente de recertificação;
- batch adaptativo: 12–20 simples, 8–12 moderados, 3–7 complexos;
- não reabrir caso fechado sem nova evidência, conflito ou regressão;
- bloqueio externo local não interrompe casos independentes;
- candidate delta → validação → escrita → read-back → QA incremental → avanço do cursor;
- QA global/visual/smoke somente em gate, regressão, mudança material de interface ou fechamento;
- uma única branch sequencial se branch for necessária; nenhum PR concorrente.

## Gate P1–P6

P1 AdaptaBrasil MCTI; P2 MapBiomas Municípios; P3 IEDE-MG/FJP; P4 BDMG com dado público verificável; P5 SICAR/CAR e SIGEF/INCRA separados; P6 IBGE Cidades e Estados. Todos devem permanecer sustentados por objeto informacional real, proveniência e acesso corretamente rotulado.

## Estado de acesso antes da recertificação corrente

A matriz estática herdada do resgate registrava **A=1, B=32, C=0, D=10, E=8**. Após recertificação oficial do TerraBrasilis em 3 de setembro de 2026, a matriz corrente registra **A=1, B=33, C=0, D=10, E=7**. Mudanças adicionais exigem evidência oficial atual e read-back.

## Definition of Done — `VITRINE_STATIC_51_STABLE`

O marco exige simultaneamente:

- `main` pública no núcleo 51, com expansão histórica fora do catálogo vivo;
- 51/51 com tipo/papel factual ou unresolved explícito;
- 51/51 com fenômeno/processo, território, tipo de informação, proveniência e A–E com verificação atual ou E justificado;
- dataset/família como objeto científico central quando identificável, sem invenção;
- zero microproduto criado apenas por formato/protocolo/interface;
- Distribution, DataService, Viewer, Documentation e Provider/Provenance semanticamente distintos;
- P1–P6 factuais;
- filtros controlados funcionando e busca livre não principal;
- 11/19 explicitamente subconjunto;
- zero botão dados/download/API levando silenciosamente a viewer/PDF/documentação/homepage genérica;
- percurso tema → entrada/dataset → rota útil em 2–3 decisões nos casos representativos;
- CI + QA visual + smoke público PASS no SHA final;
- README/PROJECT_STATE/WORKFLOW_STATUS sincronizados com o estado material;
- checkpoint final curto no repo com contagens, tipologia, P1–P6 e limitações.

Somente então declarar:

`VITRINE_STATIC_51_STABLE`

Depois desse token, a execução recorrente deve ser desativada.

## Fora do escopo até esse marco

- ontologia 2.0 exaustiva;
- Integration Registry;
- conectores federados;
- harvesting;
- PostgreSQL/backend próprio;
- reentrada da expansão;
- nova release/DOI.
