# Dicionário de dados — Vitrine Ciência

## 1. Autoridade e snapshot

A Vitrine usa três tabelas CSV canônicas na `main`:

- `data/data_resources.csv` — fontes;
- `data/data_products.csv` — produtos;
- `data/product_distributions.csv` — distribuições.

Snapshot candidato `v1.0.0` de 19/08/2026: **135 fontes, 833 produtos e 866 distribuições**. Os identificadores correntes chegam a `DR0135`, `DP000861` e `DD000894`. Os JSONs e o site são derivados. O Drive é espelho/histórico derivado.

## 2. Fontes — 34 campos

| Campo | Definição |
|---|---|
| `resource_id` | Identificador estável `DR####`. |
| `resource_name` | Nome público/oficial da fonte. |
| `acronym` | Sigla ou nome curto, quando aplicável. |
| `official_identity` | Natureza/função sustentada pela fonte oficial. |
| `description` | Síntese objetiva do propósito e conteúdo. |
| `homepage_url` | Página institucional/oficial da fonte. |
| `data_access_url` | Melhor rota para descobrir, consultar ou baixar dados. |
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
- `resource_id` — fonte pai;
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

- produto sem fonte é inválido;
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

URLs podem coincidir quando uma página realmente cumpre mais de um papel, mas a igualdade não deve ser presumida como correta.

## 8. Espaço e tempo

- resolução espacial ≠ escala ≠ precisão ≠ zoom;
- cobertura temporal ≠ resolução temporal ≠ frequência de atualização;
- suporte espacial deve refletir a unidade informacional do produto, não apenas a interface.

## 9. Autoridade e histórico

PostgreSQL/PostGIS, releases relacionais, variáveis normalizadas e entidades adicionais descritas em documentos antigos pertencem ao histórico do Simbiotrama. Não fazem parte do codebook ativo da Vitrine.

O contrato executável vigente é `schema/product-catalog-v0.1.json` e a especificação normativa é `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`.

## 10. Contrato dos campos descritivos e comparabilidade

A Vitrine passa a distinguir cinco classes de campo: **identificador**, **valor controlado**, **lista delimitada**, **texto estruturado** e **texto narrativo**. O objetivo é impedir que um único campo misture conceitos diferentes e tornar comparações lado a lado semanticamente válidas.

O contrato inicial está em `schema/descriptive-field-contract-v0.1.json`. Enquanto ele estiver em estado `experimental`, funciona como regra de curadoria e migração, sem invalidar automaticamente registros históricos ainda não normalizados.

Regras operacionais prioritárias:

1. **um campo = um conceito**: suporte espacial, resolução espacial, cobertura temporal, resolução temporal, frequência de atualização e versão não devem ser fundidos;
2. **valores controlados antes de prosa**: `sim`, `não`, `parcial`, `desconhecido`, classes de produto, origem e estado devem permanecer canônicos;
3. **listas usam ` | `**: áreas, palavras-chave, formatos e conjuntos equivalentes devem ser tratados como conjuntos de valores, não como parágrafos;
4. **descrição não substitui limitação**: descrições informam o que a fonte/produto é; limitações registram cautelas de interpretação;
5. **fonte resume, produto especifica**: quando resolução, período, versão ou licença variam entre produtos, o nível fonte deve declarar a variabilidade e o detalhe deve ficar no produto/distribuição;
6. **não inventar precisão**: quando a evidência não sustenta um valor comparável, usar `desconhecido`, `não se aplica` ou uma declaração explícita de variabilidade.

### Prioridades de migração

- separar `access_conditions` em classe + nota quando o schema de fontes for revisado;
- separar `update_frequency` em classe controlada + nota específica;
- revisar `geographic_coverage` para distinguir tipo de abrangência, local e observações;
- auditar primeiro os produtos que aparecem em comparações públicas e, depois, propagar a normalização ao restante do catálogo;
- manter campos narrativos (`description`, `academic_uses`, `limitations`) curtos, factuais e com papéis não sobrepostos.

## 11. Camada pública de descoberta e comparação

A interface pública usa uma camada derivada definida em `schema/public-discovery-v0.1.json`. Ela **não substitui nem apaga** os valores detalhados dos CSVs canônicos.

### Áreas de pesquisa públicas

As classificações detalhadas são agrupadas em seis áreas amplas:

1. **Ecologia, Biodiversidade e Meio Ambiente**;
2. **Clima, Água e Atmosfera**;
3. **Geociências e Solos**;
4. **Agricultura, Florestas e Uso da Terra**;
5. **Território, Sociedade e Políticas Públicas**;
6. **Geoinformação, Sensoriamento e Ciência de Dados**.

Nos JSONs públicos, `research_areas` recebe essas categorias amplas e `research_areas_detail` preserva a classificação detalhada anterior. Assim, filtros, cartões e gráficos usam uma taxonomia simples, enquanto a informação temática fina continua disponível para rastreabilidade e evolução futura.

### Suporte espacial e frequência de atualização

A camada pública também separa o valor comparável da descrição histórica:

- `spatial_support` passa a expor uma ou mais **classes controladas de suporte**; `spatial_support_detail` preserva o texto original;
- `update_frequency` passa a expor uma **classe controlada de frequência**; `update_frequency_detail` preserva o texto original.

A normalização é determinística e conservadora: termos de apresentação como “mapa”, “gráfico” ou “análise” não são tratados como suporte espacial; quando não há evidência suficiente, a classe permanece `desconhecido`/`desconhecida` em vez de ser inferida.
