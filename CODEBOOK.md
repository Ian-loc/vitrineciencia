# Dicionário de dados — Vitrine Ciência

**Status atual:** schema físico legado/compatibilidade. `DR####`, `DP######` e `DD######` continuam válidos para reprodução e rastreabilidade; `fonte` não é assumida como classe ontológica final. Estado corrente: `docs/PROJECT_STATE.md`; contrato transitório: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`.

## 1. Autoridade e snapshot

A Vitrine usa três tabelas CSV canônicas no schema físico vigente:

- `data/data_resources.csv` — fontes (rótulo legado para registros `DR####`);
- `data/data_products.csv` — produtos;
- `data/product_distributions.csv` — distribuições.

O snapshot histórico `v1.0.0` contém **135 fontes, 843 produtos e 876 distribuições**. Os identificadores chegam a `DR0135`, `DP000861` e `DD000894`. No PR draft #267, o branch candidato usa 51 DR / 11 produtos / 19 distribuições e preserva a expansão em quarentena. Os JSONs e o site são derivados. O Drive é espelho/histórico derivado.

## 2. Fontes — 34 campos

| Campo | Definição |
|---|---|
| `resource_id` | Identificador estável `DR####`; nesta fase é identificador legado, não prova de tipo ontológico. |
| `resource_name` | Nome público/oficial registrado. |
| `acronym` | Sigla ou nome curto, quando aplicável. |
| `official_identity` | Natureza/função sustentada pela fonte oficial; deve ser confrontada na auditoria ontológica. |
| `description` | Síntese objetiva do propósito e conteúdo. |
| `homepage_url` | Página institucional/oficial da fonte. |
| `data_access_url` | Melhor rota cadastrada para descobrir, consultar ou baixar dados. |
| `research_areas` | Áreas temáticas usadas na descoberta. |
| `keywords` | Termos pesquisáveis. |
| `data_product_types` | Resumo dos tipos de conteúdo/produto. |
| `data_formats` | Formatos de dados; pode variar por produto. |
| `visualization_types` | Formas gerais de visualização. |
| `geographic_coverage` | Abrangência espacial geral. |
| `covers_brazil` | Se a fonte oferece conteúdo aplicável ao Brasil. |
| `spatial_resolution` | Resumo de suporte/resolução; pode declarar variabilidade. |
| `temporal_coverage` | Período geral coberto. |
| `temporal_resolution` | Granularidade temporal geral. |
| `data_sources` | Origem empírica/institucional dos dados. |
| `free_download` | Condição geral de download gratuito. |
| `access_conditions` | Cadastro, solicitação, quota, embargo ou restrição. |
| `programmatic_access` | Existência de acesso automatizado. |
| `access_protocols` | HTTP, API, OGC, STAC e protocolos equivalentes. |
| `authentication_required` | Necessidade de credencial. |
| `access_documentation_url` | Documentação técnica do acesso. |
| `license` | Licença/condição geral sustentada no nível da fonte. |
| `institutional_status` | Natureza institucional. |
| `owner_or_manager` | Responsável. |
| `academic_uses` | Usos plausíveis para pesquisa/ensino/extensão. |
| `limitations` | Limitações gerais e cautelas de interpretação. |
| `academic_evidence_type` | Tipo da evidência acadêmica/técnica representativa. |
| `academic_evidence_url` | Evidência representativa. |
| `academic_evidence_note` | O que a evidência sustenta. |
| `verification_url` | Evidência oficial principal da revisão. |
| `last_verified` | Data da revisão efetiva da linha. |

## 3. Produtos — 24 campos

- `product_id` — ID estável `DP######`;
- `resource_id` — referência física legada ao DR pai;
- `product_name`, `product_acronym`, `product_family`;
- `product_kind` — classe controlada do produto;
- `product_description`;
- `research_areas`, `keywords`;
- `geographic_coverage`, `covers_brazil`;
- `spatial_support`, `spatial_resolution`;
- `temporal_coverage`, `temporal_resolution`, `update_frequency`;
- `product_status`;
- `version_or_collection`;
- `enumeration_scope`;
- `product_page_url`, `methodology_url`;
- `primary_or_derived`;
- `limitations`;
- `last_verified`.

### `product_kind`

Valores atuais: `dataset`, `dataset_series`, `catalog`, `federated_catalog`, `data_service`, `indicator_family`, `map_layer_collection`, `software_output`.

### `enumeration_scope`

- `complete` — portfólio relevante enumerado;
- `family_level` — aprofundamento por família;
- `external_index` — catálogo completo permanece externo;
- `representative_sample` — amostra explicitamente incompleta.

### `primary_or_derived`

Valores controlados: `primário`, `derivado`, `agregador`, `serviço`, `misto`, `desconhecido`.

## 4. Distribuições — 15 campos

- `distribution_id` — ID estável `DD######`;
- `product_id` — produto pai;
- `distribution_name`;
- `access_url`;
- `format`;
- `access_protocol`;
- `access_tool`;
- `free_download`;
- `authentication_required`;
- `access_conditions`;
- `license`;
- `provider_attribution_required`;
- `subset_support`;
- `notes`;
- `last_verified`.

Distribuição descreve **como acessar**, não o significado científico do produto.

## 5. Relações

```text
DR#### 1 ─── N DP###### 1 ─── N DD######
```

Essa cardinalidade é o contrato físico legado, não uma conclusão ontológica final.

- produto sem fonte é inválido no schema legado;
- distribuição sem produto é inválida;
- produto publicado sem distribuição é inválido;
- IDs não são reciclados;
- diferenças somente de URL, formato, tile ou banda não criam automaticamente novo produto.

## 6. Valores de incerteza

Quando a evidência não permite preenchimento específico, preservar estados como `desconhecido`, `parcial`, `não`, `não se aplica` ou descrição explícita de variabilidade, conforme o campo. Nunca converter desconhecido em negativo.

## 7. Papéis dos links

- **Site oficial** (`homepage_url`) — identidade institucional ou página oficial principal da fonte;
- **Acessar dados** (`data_access_url`) — página onde os dados podem ser pesquisados, visualizados, solicitados ou baixados;
- `access_documentation_url` — documentação técnica do acesso;
- `product_page_url` — página do produto;
- `methodology_url` — metodologia específica;
- `access_url` — distribuição concreta.

URLs podem coincidir quando uma página realmente cumpre mais de um papel, mas a igualdade não deve ser presumida como correta. HTTP 200 isolado não prova que a rota entrega dados utilizáveis.

## 8. Espaço e tempo

- resolução espacial ≠ escala ≠ precisão ≠ zoom;
- cobertura temporal ≠ resolução temporal ≠ frequência de atualização;
- suporte espacial deve refletir a unidade informacional do produto, não apenas a interface.

## 9. Autoridade e histórico

PostgreSQL/PostGIS, releases relacionais, variáveis normalizadas e entidades adicionais descritas em documentos antigos pertencem ao histórico do Simbiotrama. Não fazem parte do codebook ativo da Vitrine.

O contrato executável físico vigente é `schema/product-catalog-v0.1.json`; a especificação transitória é `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`. O novo schema canônico só será congelado após G0–G4 PASS.

## 10. Contrato dos campos descritivos e comparabilidade

A Vitrine distingue cinco classes de campo: **identificador**, **valor controlado**, **lista delimitada**, **texto estruturado** e **texto narrativo**. O objetivo é impedir que um único campo misture conceitos diferentes e tornar comparações lado a lado semanticamente válidas.

O contrato inicial está em `schema/descriptive-field-contract-v0.1.json`. Enquanto ele estiver em estado `experimental`, funciona como regra de curadoria e migração, sem invalidar automaticamente registros históricos ainda não normalizados.

Regras operacionais prioritárias:

1. **um campo = um conceito**: suporte espacial, resolução espacial, cobertura temporal, resolução temporal, frequência de atualização e versão não devem ser fundidos;
2. **valores controlados antes de prosa**: `sim`, `não`, `parcial`, `desconhecido`, classes de produto, origem e estado devem permanecer canônicos;
3. **listas usam ` | `**: áreas, palavras-chave, formatos e conjuntos equivalentes devem ser tratados como conjuntos de valores, não como parágrafos;
4. **descrição não substitui limitação**: descrições informam o que a fonte/produto é; limitações registram cautelas de interpretação;
5. **não inventar precisão**: quando a evidência não sustenta um valor comparável, usar `desconhecido`, `não se aplica` ou uma declaração explícita de variabilidade.

## 11. Camada pública de descoberta e comparação

A interface pública usa uma camada derivada definida em `schema/public-discovery-v0.1.json`. Ela **não substitui nem apaga** os valores detalhados dos CSVs canônicos.

As categorias e normalizações públicas permanecem compatíveis com o frontend corrente enquanto a ontologia é auditada. Nenhuma delas deve ser usada como evidência para reclassificar automaticamente um DR.
