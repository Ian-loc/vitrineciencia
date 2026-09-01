# Vitrine Ciência — contrato de dados

**Status:** TRANSITÓRIO / SOB AUDITORIA ONTOLÓGICA  
**Atualização:** 2026-09-01

## 1. Escopo deste documento

O contrato histórico `Fonte (DR) → Produto (DP) → Distribuição (DD)` continua necessário para reproduzir `v1.0.0`, preservar IDs e operar o pacote candidato do PR #267. Ele **não é mais tratado como ontologia final estável**.

As tabelas atuais permanecem:

- `data/data_resources.csv`;
- `data/data_products.csv`;
- `data/product_distributions.csv`.

Seus schemas físicos continuam válidos para compatibilidade e QA enquanto a auditoria 51/51 ocorre. Definições campo a campo permanecem documentadas no `CODEBOOK.md` e validadores existentes.

## 2. Regra central de transição

`DR####` deve ser interpretado como **identificador legado de registro**. Um DR pode representar tipos de entidade distintos e não deve ser automaticamente chamado de provedor, plataforma, dataset ou catálogo.

Nenhuma migração deve apagar ou reciclar IDs. A futura estrutura usa crosswalk explícito entre IDs legados e entidades canônicas.

## 3. Tipologia em avaliação

A auditoria deve testar, sem forçar classificação:

- `PROVIDER_INSTITUTION`;
- `PROGRAM_INITIATIVE`;
- `PLATFORM`;
- `CATALOG_REPOSITORY`;
- `DATA_INFRASTRUCTURE`;
- `DATASET_COLLECTION`;
- `DATA_SERVICE`;
- `PORTAL_VIEWER`;
- `MIXED_COMPOSITE`;
- `AMBIGUOUS_UNRESOLVED`.

A ontologia final só será congelada depois de validada contra os 51 registros.

## 4. Regras permanentes já confirmadas

- preservar identidade e proveniência;
- não promover propriedade de um dataset para uma instituição/plataforma inteira;
- formato, protocolo e ferramenta são propriedades distintas;
- API/serviço de dados não é novo dataset por padrão;
- viewer, PDF ou documentação não comprovam distribuição de dados;
- desconhecido não significa `não`;
- licença e acesso devem ser registrados no nível sustentado pela evidência;
- CI comprova conformidade estrutural, não verdade factual externa.

## 5. Relação com a release v1.0.0

O schema histórico permanece **congelado e válido para reprodução da release `v1.0.0`**. A revisão atual não altera retrospectivamente a release, tag, DOI ou depósito Zenodo.

## 6. Gate para o novo contrato

Um novo contrato canônico só pode substituir este estado transitório quando G0–G4 estiverem PASS e existir:

1. auditoria ontológica 51/51;
2. crosswalk legado → entidades canônicas;
3. vocabulários controlados;
4. schema que represente honestamente os 51 casos;
5. validadores positivos e negativos.

Até esse gate, não declarar o modelo novo como `STABLE`.
