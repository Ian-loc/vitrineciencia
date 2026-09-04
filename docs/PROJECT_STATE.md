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

O marco de **consolidação semântica e funcional do núcleo estático DR0001–DR0051 está concluído**.

`VITRINE_STATIC_51_STABLE`

O runtime público que satisfez simultaneamente os gates finais é **`495bfe6a968176670461662869d1a3773797baf3`**:

- build/validação/deploy: workflow `33906109623` — PASS;
- QA visual e responsivo: workflow `33906109551` — PASS;
- smoke pós-deploy sobre o site publicado: workflow `33906157842` — PASS.

A expansão geral permanece pausada. A recertificação semântica 51/51 está concluída. A **fase ativa de QA/QC e manutenção** passa a significar preservação do marco estável e correção de regressões, não recertificação pendente.

## Estado material

- `main` publica o núcleo estático de **51 registros DR / 11 itens detalhados / 19 distribuições**.
- Na terminologia física exigida pelo schema/validador legado, isso corresponde a **51 fontes, 11 produtos e 19 distribuições**; esses rótulos não definem a ontologia pública.
- Os 11/19 são um subconjunto detalhado, não toda a cobertura científica dos 51.
- A expansão histórica 135/843/876 permanece preservada em `data/quarantine/v1.0.0-expanded/` e fora do catálogo vivo.
- `data/static_core_51_progress.json` registra **51/51 com tipagem semântica concluída**, sem pendências de tipagem.
- `data/static_core_51_access_audit.json` registra **A=1, B=38, C=0, D=10, E=2**.
- Os dois E são limitações deliberadas e documentadas: `DR0014` (SiBBr, rota canônica genérica) e `DR0039` (GBIF IPT, software de publicação e não rota agregada de obtenção).
- O gate P1–P6 está materializado em `data/applied_priority_gate.json`.
- O artefato público fecha as dependências locais necessárias à interface e valida referências HTML e `fetch()` literais durante o build.
- Tipagem semântica e classificação de acesso são autoridades distintas: `static_core_51_progress.json` não substitui `static_core_51_access_audit.json`.
- A **release científica `v1.0.0` publicada**, sua tag, DOI `10.5281/zenodo.22130831` e snapshot histórico permanecem imutáveis.

## Fontes materiais de verdade no marco estático

- `data/data_resources.csv`;
- `data/data_products.csv`;
- `data/product_distributions.csv`;
- `data/static_core_51_access_audit.json`;
- `data/static_core_51_progress.json`;
- `data/product_distribution_roles.json`;
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

**Fase I — reconciliar e fixar o estado real: CONCLUÍDA**

- 51/51 semanticamente tipados;
- 51/51 com classificação A–E e justificativa;
- dois E preservados explicitamente como limitações verificadas.

**Fase II — reorganizar a representação estática: CONCLUÍDA**

- Home orientada por pergunta/tema;
- `sources.html` como superfície ampla dos 51;
- `products.html` como subconjunto detalhado 11/19 com tipologia explícita;
- rotas de acesso separadas por função;
- P1–P6 integrado à superfície pública.

**Fase III — consolidação funcional: CONCLUÍDA**

- QA semântico, estrutural, científico e de navegação;
- filtros controlados, URL params, teclado, desktop/tablet/mobile;
- regressões de runtime nos observadores de Produtos e Fontes corrigidas sem relaxar o QA;
- fechamento das dependências do artefato público validado;
- CI principal, QA visual e smoke público verdes no runtime `495bfe6a968176670461662869d1a3773797baf3`;
- documentação e checkpoint sincronizados com o estado material.

## Gate P1–P6

Devem permanecer representados por objeto informacional real, proveniência explícita e acesso corretamente rotulado:

- P1 AdaptaBrasil MCTI;
- P2 MapBiomas Municípios;
- P3 IEDE-MG/FJP, distinta de IDE-Sisema;
- P4 BDMG com dado público verificável;
- P5 SICAR/CAR e SIGEF/INCRA separados;
- P6 IBGE Cidades e Estados com indicador municipal real.

## Manutenção após o marco

A partir de `VITRINE_STATIC_51_STABLE`:

- o núcleo 51 não deve ser reaberto sem nova evidência, conflito factual ou regressão;
- mudanças de conteúdo continuam começando na autoridade canônica adequada;
- regressões devem ser corrigidas e verificadas pelos mesmos gates proporcionais;
- a expansão histórica não retorna automaticamente ao catálogo vivo;
- uma nova frente de federação/Data Service deve ser tratada como milestone independente.

## Próximo milestone — não ativado automaticamente

Permanecem fora do marco estático concluído e exigem autorização/escopo próprios:

- ontologia 2.0 exaustiva;
- Integration Registry federado;
- conectores STAC/CKAN/OGC/REST/GraphQL;
- harvesting;
- PostgreSQL/backend próprio;
- reentrada da expansão;
- nova release/DOI.

## Checkpoint

O checkpoint factual do fechamento está em `docs/CHECKPOINT_STATIC_51_2026-09-04.md`.
