# Estado canônico — Vitrine Ciência

**Data de referência:** 4 de setembro de 2026  
**Fuso:** `America/Sao_Paulo`

## Autoridade

O repositório `Ian-loc/vitrineciencia` é a **autoridade canônica do projeto**. `main` representa o estado público corrente. Worktrees locais, Google Drive, handoffs e chats são auxiliares de trabalho ou espelhos documentais; não substituem o estado materializado no GitHub.

Dentro do repositório, a hierarquia corrente é:

1. arquivos de dados e matrizes de auditoria canônicas;
2. scripts de build e validação;
3. artefatos públicos derivados (JSON/HTML/`_site`);
4. documentação de estado, que deve descrever o material e nunca contradizê-lo.

## Estado global

A Vitrine está no fechamento da **consolidação semântica e funcional do núcleo estático DR0001–DR0051**, antes de qualquer mudança para Data Service/federação.

A expansão geral permanece pausada. A recertificação semântica 51/51 está concluída e a frente ativa é QA funcional, publicação e sincronização documental.

## Estado material

- `main` publica o núcleo estático de **51 registros DR / 11 itens detalhados / 19 distribuições**.
- Na terminologia física exigida pelo schema/validador legado, isso corresponde a **51 fontes, 11 produtos e 19 distribuições**; esses rótulos não definem a ontologia pública.
- Os 11/19 são um subconjunto detalhado, não toda a cobertura científica dos 51.
- A expansão histórica 135/843/876 permanece preservada em `data/quarantine/v1.0.0-expanded/` e fora do catálogo vivo.
- `data/static_core_51_progress.json` registra **51/51 com tipagem semântica concluída**, sem pendências de tipagem.
- `data/static_core_51_access_audit.json` registra **A=1, B=38, C=0, D=10, E=2**.
- Os dois E são limitações deliberadas e documentadas: `DR0014` (SiBBr, rota canônica genérica) e `DR0039` (GBIF IPT, software de publicação e não rota agregada de obtenção).
- O gate P1–P6 está materializado em `data/applied_priority_gate.json`.
- A **release científica `v1.0.0` publicada**, sua tag, DOI `10.5281/zenodo.22130831` e snapshot histórico permanecem imutáveis.

## Fontes materiais de verdade no marco estático

- `data/data_resources.csv`;
- `data/data_products.csv`;
- `data/product_distributions.csv`;
- `data/static_core_51_access_audit.json`;
- `data/static_core_51_progress.json`;
- `data/applied_priority_gate.json`.

JSONs públicos, páginas e `_site` são derivados. Mudanças de classificação ou significado devem começar nas fontes canônicas correspondentes e ser propagadas pelo build/validação; não devem ser corrigidas apenas na UI.

## Modelo público corrente

A navegação deve seguir:

**pergunta científica → fenômeno/processo → território/tempo/escala → dataset/família de dados → produto científico quando necessário → distribuição/rota de acesso ou DataService → provedor/proveniência → documentação**.

A estrutura física histórica `DR → DP → DD` permanece apenas para compatibilidade e rastreabilidade.

A interface e a recertificação distinguem, quando aplicável:

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

- `A DIRECT_DATA` — arquivo/download/endpoint que entrega dados;
- `B DATASET_PAGE` — página específica com mecanismo explícito de obtenção;
- `C API_SERVICE` — API/OGC/STAC/CKAN/GraphQL ou serviço de consulta/extração como rota principal;
- `D VIEWER_DOC` — viewer/dashboard/mapa/documentação/PDF sem acesso de dados demonstrado na rota principal;
- `E BROKEN_UNCERTAIN` — rota genérica, inadequada como acesso agregado ou sem obtenção demonstrada.

Somente A–C podem ser apresentados como acesso confirmado a dados. HTTP 200 isolado não comprova acesso.

## Estado das fases

**Fase I — reconciliar e fixar o estado real: CONCLUÍDA para o marco estático**

- 51/51 semanticamente tipados;
- 51/51 com classificação A–E e justificativa;
- dois E preservados explicitamente como limitações verificadas.

**Fase II — reorganizar a representação estática: MATERIALIZADA**

- Home orientada por pergunta/tema;
- `sources.html` como superfície ampla dos 51;
- `products.html` como subconjunto detalhado 11/19 com tipologia explícita;
- rotas de acesso separadas por função;
- P1–P6 integrado à superfície pública.

**Fase III — consolidação funcional: EM FECHAMENTO**

- QA semântico, estrutural, científico e de navegação;
- filtros, URL params, teclado, desktop/tablet/mobile;
- zero botão download/dados/API apontando silenciosamente para viewer/PDF/documentação/homepage genérica;
- CI principal, QA visual e smoke público no SHA final;
- sincronização de README/PROJECT_STATE/WORKFLOW_STATUS;
- checkpoint final no repositório.

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

O marco estático termina somente quando, no mesmo estado final:

- 51/51 permanecerem semanticamente recertificados;
- A–E permanecer factualmente sustentado;
- P1–P6 permanecer factual;
- a interface refletir as distinções semânticas sem regressão;
- CI principal, QA visual e smoke público estiverem verdes;
- README/PROJECT_STATE/WORKFLOW_STATUS e checkpoint estiverem sincronizados com `main`.

Somente então declarar:

`VITRINE_STATIC_51_STABLE`

Depois desse token, a execução recorrente do marco estático deve ser desativada. Federação/Data Service pertence a novo milestone e exige autorização posterior.
