# Vitrine Ciência

**Catálogo público e citável para descobrir e acessar dados científicos relevantes ao Brasil.**

## Estado atual — 1º de setembro de 2026

- `main` continua sendo o estado público corrente do repositório e ainda contém o catálogo expandido derivado da release `v1.0.0` (**135 registros historicamente chamados de fontes, 843 produtos e 876 distribuições**).
- O PR draft **#267** é um pacote candidato de re-curadoria. Nele, a expansão foi preservada em `data/quarantine/v1.0.0-expanded/` e a superfície candidata foi reduzida para **51 registros legados DR, 11 produtos e 19 distribuições**.
- Esses 51 registros **não são assumidos como 51 entidades do mesmo tipo**. O rótulo histórico `fonte` está em auditoria ontológica.
- Nenhum merge, novo schema, conector federado ou nova release está autorizado por este estado.

## Objetivo ativo

Antes de consolidar a arquitetura Vitrine 2.0, cada registro `DR0001–DR0051` deve ser classificado pelo que realmente representa: instituição/provedor, programa/iniciativa, plataforma, catálogo/repositório, infraestrutura de dados, dataset/coleção, serviço de dados, portal/visualizador ou combinação explicitamente decomposta.

A direção pública permanece:

**fenômeno/processo → território → tempo/escala → dado utilizável → acesso → provedor/proveniência**.

Busca livre não é o mecanismo principal. A interface deve privilegiar filtros controlados e encaminhar o usuário a dados efetivamente acessíveis.

## Modelo: estado transitório

A estrutura histórica `Fonte (DR) → Produto (DP) → Distribuição (DD)` continua existindo como **estrutura legada de armazenamento e rastreabilidade**. Ela não é mais tratada como ontologia final.

O modelo canônico só será congelado após a auditoria 51/51 e deverá distinguir, no mínimo quando aplicável:

- Provider/Institution;
- Program/Initiative;
- Platform/Catalog/Data Infrastructure;
- Dataset/Collection;
- Distribution;
- DataService.

## Federação por APIs

A federação é uma fase posterior. Primeiro: auditoria ontológica 51/51. Depois: registro de integração 51/51. Só então: pipeline e pilotos, com **MapBiomas Alerta como primeiro caso obrigatório**.

Nenhum recurso descoberto por API entra automaticamente na superfície pública.

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
- repositório: https://github.com/Ian-loc/vitrineciencia;
- site: https://ian-loc.github.io/vitrineciencia/.

Código: MIT. Metadados e curadoria original: CC BY 4.0.

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. Version 1.0.0. Zenodo, 2026. https://doi.org/10.5281/zenodo.22130831
