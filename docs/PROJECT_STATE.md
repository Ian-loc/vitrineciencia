# Estado canônico — Vitrine Ciência

**Data de referência:** 3 de setembro de 2026  
**Fuso:** `America/Sao_Paulo`

## Estado global

A fase ativa é a **QA/QC, consolidação semântica e funcional da Vitrine Ciência estática com o núcleo DR0001–DR0051**, antes de qualquer mudança para Data Service/federação.

A expansão geral permanece pausada. O trabalho corrente recertifica os 51 registros, reduz carga cognitiva, orienta a descoberta por tema científico e corrige a semântica de dados, produtos, rotas e proveniência.

## Estado material

- `main` já contém e publica o núcleo estático de **51 registros DR / 11 itens detalhados / 19 distribuições**.
- Na terminologia física exigida pelo schema/validador legado, isso corresponde a **51 fontes, 11 produtos e 19 distribuições**; esses rótulos não definem a ontologia pública.
- O PR `#267` foi incorporado em `main` em 3 de setembro de 2026 e não é mais uma frente ativa.
- O workflow principal de publicação e o smoke test público pós-deploy passaram para o estado estático 51/11/19.
- A release científica `v1.0.0`, sua tag, DOI `10.5281/zenodo.22130831` e snapshot histórico permanecem imutáveis.
- A expansão histórica 135/843/876 permanece preservada em `data/quarantine/v1.0.0-expanded/` e fora do catálogo vivo.
- Os 51 DR podem representar tipos distintos de entidade. `DR####` é identificador legado e não implica que a entrada seja dataset, provedor ou plataforma.

## Modelo público corrente

A navegação deve seguir:

**pergunta científica → fenômeno/processo → território/tempo/escala → dataset/família de dados → produto científico quando necessário → distribuição/rota de acesso ou DataService → provedor/proveniência → documentação**.

A estrutura física histórica `DR → DP → DD` permanece apenas para compatibilidade e rastreabilidade.

A interface e a recertificação devem distinguir, quando aplicável:

- Provider/Institution;
- Program/Initiative;
- Platform/Catalog/Data Infrastructure;
- Dataset/Collection;
- Product, somente quando materialmente distinto;
- Distribution;
- DataService/API;
- Portal/Viewer;
- Documentation/Publication.

Proveniência é transversal: produzir, publicar, manter, hospedar/expor e documentar são relações diferentes. Formato, arquivo, API, viewer e documentação não criam produto científico por si sós.

## Classificação de acesso

Cada DR deve receber verificação factual da rota principal:

- `A DIRECT_DATA` — arquivo/download/endpoint que entrega dados;
- `B DATASET_PAGE` — página específica com mecanismo explícito de obtenção;
- `C API_SERVICE` — API/OGC/STAC/CKAN/GraphQL ou serviço de consulta/extração;
- `D VIEWER_DOC` — viewer/dashboard/mapa/documentação/PDF sem acesso de dados demonstrado;
- `E BROKEN_UNCERTAIN` — rota quebrada, restrita, genérica ou ainda incerta.

Somente A–C podem ser apresentados como acesso confirmado a dados. HTTP 200 isolado não comprova acesso.

## Fases ativas

**Fase I — reconciliar e fixar o estado real**

- sincronizar documentação com `main` publicado;
- recertificar os 51 por tipo/papel, fenômeno/processo, território, informação, proveniência, dataset/família quando sustentado, rota A–E e `last_verified`;
- não forçar Dataset quando a entrada é instituição, plataforma, catálogo ou outro tipo.

**Fase II — reorganizar a representação estática**

- Home orientada por pergunta/tema;
- `sources.html` como superfície ampla de descoberta dos 51;
- `products.html` como subconjunto detalhado 11/19, com tipologia honesta;
- funções de acesso explicitamente separadas: dados, página do conjunto, API/serviço, viewer, documentação e provedor.

**Fase III — consolidação funcional**

- QA semântico, estrutural, científico e de navegação;
- filtros, URL params, teclado, desktop/tablet/mobile;
- zero botão download/dados/API apontando silenciosamente para viewer/PDF/documentação/homepage genérica;
- CI, QA visual e smoke público no SHA final.

## Gate P1–P6

Devem permanecer representados por objeto informacional real, proveniência explícita e acesso corretamente rotulado:

- P1 AdaptaBrasil MCTI;
- P2 MapBiomas Municípios;
- P3 IEDE-MG/FJP, distinta de IDE-Sisema;
- P4 BDMG com dado público verificável;
- P5 SICAR/CAR e SIGEF/INCRA separados;
- P6 IBGE Cidades e Estados com indicador municipal real.

## Fora do marco atual

Até `VITRINE_STATIC_51_STABLE`, não iniciar como frente executora:

- ontologia 2.0 exaustiva;
- Integration Registry federado;
- conectores STAC/CKAN/OGC/REST/GraphQL;
- harvesting;
- PostgreSQL/backend próprio;
- reentrada da expansão;
- nova release/DOI.

## Regra de conclusão

O marco estático termina somente quando os 51 estiverem semanticamente recertificados ou explicitamente unresolved, os acessos A–E estiverem factualmente sustentados, a interface refletir a distinção dataset/produto/distribuição/serviço/proveniência e CI/QA/smoke estiverem verdes no estado final.

Somente então declarar:

`VITRINE_STATIC_51_STABLE`

Depois desse token, a execução recorrente deve ser desativada. Federação/Data Service pertence a novo milestone e exige autorização posterior.
