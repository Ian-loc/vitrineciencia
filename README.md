# Vitrine Ciência

**Catálogo público e citável para descobrir e acessar dados científicos relevantes ao Brasil.**

## Estado atual — 3 de setembro de 2026

- `main` é o estado público corrente e usa o núcleo estático de **51 registros legados DR0001–DR0051**.
- O PR **#267** foi incorporado em `main` em 3 de setembro de 2026; não é mais uma frente ativa.
- Na estrutura física legada, o estado público contém **51 registros DR, 11 itens detalhados e 19 distribuições**. Os 11/19 são um subconjunto detalhado, não toda a cobertura científica dos 51.
- A expansão histórica **135/843/876** permanece preservada em `data/quarantine/v1.0.0-expanded/` e não integra o catálogo vivo.
- A publicação do núcleo 51 passou pelo workflow principal e pelo smoke test público pós-deploy.
- Os 51 DR **não são assumidos como entidades do mesmo tipo**. `DR####` é um identificador legado de entrada; a recertificação corrente distingue instituição/provedor, programa/iniciativa, plataforma/catálogo/infraestrutura, dataset/coleção, serviço e portal/viewer quando a evidência permite.

## Objetivo ativo

Concluir a recertificação semântica e de acesso dos 51 registros e estabilizar a interface estática antes de qualquer nova arquitetura federada.

A direção pública é:

**pergunta científica → fenômeno/processo → território/tempo/escala → dataset/família de dados → produto científico quando necessário → distribuição/rota de acesso ou DataService → provedor/proveniência → documentação**.

Busca livre não é o mecanismo principal. A interface privilegia filtros controlados e encaminhamento a rotas de dados efetivamente demonstradas.

## Modelo: estado transitório

A estrutura histórica `Fonte (DR) → Produto (DP) → Distribuição (DD)` continua existindo para **compatibilidade, IDs e rastreabilidade**. Ela não é tratada como ontologia final.

O modelo em consolidação distingue, quando aplicável:

- Provider/Institution;
- Program/Initiative;
- Platform/Catalog/Data Infrastructure;
- Dataset/Collection;
- Product, somente quando o objeto informacional é materialmente distinto;
- Distribution;
- DataService;
- Portal/Viewer;
- Documentation/Publication.

Formato, arquivo, API, viewer ou documentação não viram produto científico por conveniência. Proveniência é transversal ao objeto de dados.

## Fase operacional

A frente ativa é a consolidação estática 51/51:

1. recertificar tipo/papel, fenômeno/processo, território, informação, proveniência e acesso de cada DR;
2. classificar a rota principal como `A DIRECT_DATA`, `B DATASET_PAGE`, `C API_SERVICE`, `D VIEWER_DOC` ou `E BROKEN_UNCERTAIN`;
3. refletir essas relações nos cards e filtros sem aumentar carga cognitiva;
4. fechar QA estrutural, semântico, visual e smoke público.

Somente A–C são acesso confirmado a dados. Viewer, PDF, documentação e homepage genérica devem ser rotulados pelo papel real.

## Federação por APIs

Federação é fase posterior e não está sendo executada neste marco. Nenhum recurso descoberto por API entra automaticamente na superfície pública.

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
- matriz de recertificação de acesso: `data/static_core_51_access_audit.json`;
- repositório: https://github.com/Ian-loc/vitrineciencia;
- site: https://ian-loc.github.io/vitrineciencia/.

Código: MIT. Metadados e curadoria original: CC BY 4.0.

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. Version 1.0.0. Zenodo, 2026. https://doi.org/10.5281/zenodo.22130831
