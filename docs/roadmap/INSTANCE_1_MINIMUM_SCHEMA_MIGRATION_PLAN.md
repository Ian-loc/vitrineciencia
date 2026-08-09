# Plano de migração para o núcleo mínimo da Instância 1

**Status:** proposta executável após incorporação do PR de direção  
**Princípio:** migração sem perda, idempotente e reversível.

## 1. Objetivo

Migrar progressivamente a arquitetura incorporada no Marco 1 para um núcleo centrado em entradas de catálogo, sem apagar staging, evidências ou estruturas profundas antes de sua disposição formal.

## 2. Estrutura-alvo

Entidades semânticas do núcleo:

- `catalog.organizations`;
- `catalog.catalog_entries`;
- `catalog.entry_variables`;
- `catalog.entry_evidence`;
- `catalog.connector_profiles` opcional.

Relação estrutural necessária para preservar atribuição institucional sem perda:

- `catalog.entry_organizations` — ponte N:N entre entradas e organizações, com papel explícito.

`entry_organizations` não cria uma nova categoria conceitual do catálogo; é apenas a relação necessária para representar casos reais em que uma entrada possui mais de uma organização responsável e para sustentar filtros por organização sem reduzir a atribuição a um único responsável.

## 3. Estratégia

### Fase A — extensão aditiva

Criar novas tabelas por migration aditiva. Não remover ou renomear tabelas existentes.

### Fase B — crosswalk

Mapear registros existentes:

| Estrutura atual | Destino proposto |
|---|---|
| `organizations` | `organizations` preservada ou adaptada |
| relações explícitas fonte↔organização / responsáveis do staging | `entry_organizations`, preservando todas as organizações e papéis documentados; não inferir papel ausente |
| `sources` | `catalog_entries` com `entry_type = source/platform` |
| `covers_brazil` + classificação territorial P0–P3 | `catalog_entries.covers_brazil` + `catalog_entries.brazil_priority`, preservados como campos estruturados |
| `product_families` | entrada apenas quando útil; caso contrário, metadado ou relação histórica |
| `products` | `catalog_entries` quando forem unidades públicas materialmente distintas |
| `product_releases` | metadado adicional, subentrada excepcional ou extensão histórica |
| `variables` / `product_variables` | `entry_variables`, limitadas às variáveis principais |
| `metadata_assertions` | `entry_evidence`, agregada proporcionalmente |
| `distributions` | links essenciais da entrada ou candidato a conector |
| `data_assets` | não promovido ao núcleo; preservado como legado histórico |
| `access_capabilities` | resumo de acesso ou `connector_profiles` quando selecionado |
| métodos e perfis | campos simples/JSONB, salvo uso repetido comprovado |

## 4. Regras de transformação

1. nenhuma linha original é apagada;
2. cada entrada derivada preserva IDs de origem em `source_record_ids`;
3. a mesma carga não cria duplicatas;
4. alterações manuais posteriores não são sobrescritas silenciosamente;
5. conflitos são registrados para revisão;
6. relações profundas não são convertidas em novas entradas sem decisão de granularidade;
7. links são classificados por papel, sem inventário integral;
8. valores desconhecidos permanecem desconhecidos;
9. condições materiais de acesso — cadastro, solicitação, embargo, quotas ou restrições equivalentes — permanecem explícitas em `access_conditions_text` e não são reduzidas a `access_level` ou ao booleano de autenticação;
10. todas as organizações explicitamente responsáveis por uma entrada são preservadas em `entry_organizations`; um único responsável não pode substituir relações múltiplas existentes;
11. `covers_brazil` preserva a semântica estruturada atual (`sim`, `parcial`, `não`) e `brazil_priority` preserva `P0`–`P3`; nenhum dos dois é derivado novamente de texto livre de cobertura.

## 5. Tabela `catalog_entries`

Campos iniciais propostos:

- `entry_id`;
- `stable_id`;
- `parent_entry_id` opcional;
- `entry_type`;
- `official_name`;
- `acronym`;
- `summary`;
- `scientific_scope`;
- `data_modalities`;
- `geographic_coverage_text`;
- `covers_brazil`;
- `brazil_priority`;
- `temporal_coverage_text`;
- `spatial_resolution_text`;
- `temporal_resolution_text`;
- `update_frequency_text`;
- `access_level`;
- `access_conditions_text`;
- `authentication_required`;
- `official_page_url`;
- `metadata_url`;
- `primary_access_url`;
- `methodology_url`;
- `license_text`;
- `license_url`;
- `citation_text`;
- `citation_url`;
- `curation_status`;
- `last_verified_at`;
- `additional_metadata` JSONB;
- `source_record_ids` JSONB;
- timestamps.

`access_conditions_text` preserva a condição declarada pela fonte em granularidade suficiente para a ficha pública. O campo não deve ser usado para inventariar todos os mecanismos técnicos de acesso; sua função é impedir perda semântica quando `access_level` e `authentication_required` não explicam, por si sós, requisitos como cadastro, solicitação, embargo ou quotas.

`covers_brazil` é um campo estruturado de cobertura territorial e não substitui `geographic_coverage_text`. `brazil_priority` materializa a classe curatorial P0–P3 definida na política de seleção. Ambos existem para permitir filtro determinístico e auditoria da política Brasil-primeiro.

### 5.1 Relação `entry_organizations`

Campos mínimos:

- `entry_id` FK → `catalog_entries`;
- `organization_id` FK → `organizations`;
- `organization_role` — papel declarado ou curatorialmente sustentado, como produtor, mantenedor, gestor ou parceiro; usar `unspecified` quando a relação é explícita mas o papel não é;
- `is_primary` booleano apenas para apresentação quando houver fonte para essa distinção;
- timestamps.

Regras:

- uma entrada pode ter uma ou várias organizações;
- nenhuma organização explicitamente associada é descartada para caber em um campo singular;
- o filtro por organização consulta esta relação;
- `is_primary` não autoriza apagar ou ocultar organizações secundárias;
- a migração não inventa papéis institucionais.

## 6. Variáveis

`entry_variables` deve armazenar somente conteúdos úteis para busca:

- `source_label`;
- `source_definition`;
- `search_label` opcional;
- `variable_group`;
- `unit_text` opcional;
- `evidence_id` opcional;
- estado curatorial.

Não importar automaticamente cada banda, classe ou coluna do modelo profundo.

## 7. Evidências

`entry_evidence` pode sustentar um campo ou grupo de campos:

- URL;
- papel da evidência;
- nota de suporte;
- data de recuperação;
- estado de verificação.

Não migrar afirmações atômicas sem avaliar sua utilidade no perfil público.

## 8. Conectores

`connector_profiles` só recebe candidatos selecionados. Distribuições e ativos existentes não são convertidos automaticamente em conectores.

## 9. Compatibilidade transitória

Durante a migração:

- CSV/JSON públicos permanecem inalterados;
- views podem expor o novo núcleo sem substituir o site;
- scripts antigos continuam disponíveis para regressão;
- o novo exportador deve ser testado lado a lado;
- nenhuma promoção a produção ocorre sem autorização.

## 10. Testes obrigatórios

- migration aplicada em banco vazio;
- migration aplicada após Marco 1;
- idempotência da carga;
- integridade de FKs;
- ausência de duplicação de entradas;
- preservação de IDs de origem;
- preservação N:N de organizações e seus papéis;
- preservação exata de `covers_brazil` e P0–P3;
- preservação de `access_conditions_text`;
- rollback ou restauração documentada;
- exportação determinística;
- casos GEDI, DETER Cerrado, IBGE e ANA/SNIRH;
- teste adversarial contra criação de entrada por arquivo/layer.

## 11. Critério de saída

O pacote executável será aceito quando:

- o núcleo mínimo estiver materializado;
- nenhum dado legado tiver sido removido;
- atribuições institucionais múltiplas e classificação territorial estiverem preservadas sem perda;
- os quatro casos forem representáveis;
- o exportador produzir fichas úteis;
- o CI estiver verde;
- revisão não identificar expansão indevida;
- houver autorização humana para merge.
