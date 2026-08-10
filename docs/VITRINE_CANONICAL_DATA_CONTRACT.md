# Vitrine Ciência — contrato canônico de dados

Status: **STABLE / ACTIVE**

Este documento descreve o contrato **existente** da Vitrine Ciência. Ele não cria uma nova arquitetura. O objetivo é permitir auditoria científica e crescimento de volume sem regressão para o antigo modo piloto ou para reconstrução profunda de catálogos externos.

## 1. Entidades canônicas

A Vitrine usa três tabelas públicas principais:

1. `data/data_resources.csv` — fontes e infraestruturas de dados;
2. `data/data_products.csv` — produtos materialmente distintos cuja identidade própria melhora descoberta, compreensão ou acesso;
3. `data/product_distributions.csv` — formas concretas de acesso a um produto.

Relações:

- uma fonte pode ter zero ou muitos produtos;
- todo produto referencia exatamente uma fonte por `resource_id`;
- todo produto catalogado deve possuir ao menos uma distribuição;
- toda distribuição referencia exatamente um produto por `product_id`.

Arquivos, tiles, bandas, endpoints ou formatos não se tornam produtos apenas por existirem.

## 2. Identificadores

- fontes: `DR####`;
- produtos: `DP######`;
- distribuições: `DD######`.

IDs são estáveis, únicos e não devem ser reciclados para outra entidade.

## 3. Contrato de fonte

O cabeçalho canônico de `data_resources.csv` permanece com 34 campos. Crescimento de linhas é esperado e não constitui mudança de schema.

### Identidade e descoberta — necessários para uma entrada útil

- `resource_id`
- `resource_name`
- `official_identity`
- `description`
- `homepage_url`
- `data_access_url`
- `research_areas`
- `keywords`
- `data_product_types`
- `geographic_coverage`
- `covers_brazil`
- `institutional_status`
- `owner_or_manager`
- `verification_url`
- `last_verified`

### Descrição científica e operacional — recomendados quando sustentados

- `acronym`
- `data_formats`
- `visualization_types`
- `spatial_resolution`
- `temporal_coverage`
- `temporal_resolution`
- `data_sources`
- `free_download`
- `access_conditions`
- `programmatic_access`
- `access_protocols`
- `authentication_required`
- `access_documentation_url`
- `license`
- `academic_uses`
- `limitations`
- `academic_evidence_type`
- `academic_evidence_url`
- `academic_evidence_note`

### Nullable-by-design

Um campo pode permanecer vazio, `desconhecido`, `não localizado`, `não documentado`, `não se aplica` ou equivalente permitido quando uma propriedade única não existe ou não foi sustentada proporcionalmente. Não preencher por inferência propriedades da plataforma a partir de um produto específico.

## 4. Contrato de produto

Um produto recebe linha própria somente quando possui identidade material independente para o usuário — por exemplo diferença relevante em finalidade científica, método, cobertura, resolução/suporte, coleção/versão científica ou caminho/condição de acesso.

### Obrigatórios

- `product_id`
- `resource_id`
- `product_name`
- `product_family`
- `product_kind`
- `product_description`
- `research_areas`
- `keywords`
- `geographic_coverage`
- `covers_brazil`
- `spatial_support`
- `spatial_resolution`
- `temporal_coverage`
- `temporal_resolution`
- `update_frequency`
- `product_status`
- `version_or_collection`
- `enumeration_scope`
- `product_page_url`
- `primary_or_derived`
- `limitations`
- `last_verified`

### Recomendados / nullable-by-design

- `product_acronym`
- `methodology_url`

`methodology_url` **não é obrigatório universalmente**. Para catálogos, serviços ou infraestruturas agregadoras, a metodologia científica pode pertencer aos produtos/datasets subjacentes. Nesses casos, deixar o campo vazio é preferível a inventar uma metodologia única.

## 5. Contrato de distribuição

Distribuição descreve como um produto é acessado. Não é uma nova identidade científica do produto.

Campos operacionais obrigatórios:

- `distribution_id`
- `product_id`
- `distribution_name`
- `access_url`
- `format`
- `access_protocol`
- `access_tool`
- `free_download`
- `authentication_required`
- `access_conditions`
- `license`
- `provider_attribution_required`
- `subset_support`
- `notes`
- `last_verified`

Quando licença, autenticação ou condição variam por coleção/recurso, registrar a limitação em vez de generalizar uma propriedade universal.

## 6. Regras semânticas obrigatórias

- `temporal_resolution` descreve o grão temporal do dado; não é frequência de atualização;
- `update_frequency` descreve cadência de publicação/atualização;
- `spatial_resolution` não deve ser inferida do zoom de um visualizador;
- a licença deve ser registrada no nível mais baixo em que foi efetivamente verificada;
- agregadores devem preservar o produtor/provedor primário dos dados;
- catálogos externos amplos usam `enumeration_scope=external_index`;
- produto não é formato de arquivo;
- distribuição não é produto;
- lacunas são preservadas sem inferência;
- legado serve como pista de auditoria, nunca como autoridade automática.

## 7. Política de crescimento

O baseline atual é 51 fontes, 11 produtos e 19 distribuições. Essas contagens são **ponto de partida**, não limites máximos.

O CI deve impedir perda acidental do baseline e violações do contrato, mas deve permitir crescimento legítimo de linhas dentro do mesmo schema.

Novas entradas devem passar por:

`scope → official evidence → curation → validation → diff audit → risk classification → integration → post-merge verification`.

## 8. Mudança de contrato

Adicionar novas linhas dentro destes campos não é mudança de contrato.

Alterar chaves, relações, significado dos campos, valores controlados de forma incompatível ou cardinalidades constitui mudança conceitual/schema e requer **HUMAN-DECISION** conforme `docs/VITRINE_OPERATING_MODEL.md`.
