# Versões, coleções e proveniência — contrato v1

**Status:** autoridade canônica inicial  
**Atualização:** 12 de outubro de 2026  
**Escopo:** `data/product_versions.json` e `data/provenance_assertions.json`

## 1. Objetivo

Esta camada resolve duas ambiguidades remanescentes do `public-record-v2`:

1. `version_or_collection` não pode ser tratado automaticamente como uma versão citável;
2. `owner_or_manager` não pode ser tratado automaticamente como um agente único com papel ontológico preciso.

O objetivo é estruturar o que já está sustentado sem inventar precisão.

## 2. Versões e coleções

A autoridade é:

`data/product_versions.json`

sob:

`schema/product-versions-v1.json`.

Cada objeto possui identidade própria no contrato, mas seu `identity_status` explicita se o rótulo representa:

- versão explicitamente nomeada;
- edição/ano;
- ou somente um estado descritivo.

### Classes atuais

- `named_version` — versão explicitamente nomeada;
- `edition_or_year` — edição ou ano;
- `provider_update` — atualização publicada;
- `current_collection_state` — coleção corrente sem ID mais específico;
- `collection_group` — grupo de coleções;
- `service_state` — estado de serviço;
- `catalog_state` — estado de catálogo;
- `access_configuration` — configuração de acesso;
- `experimental_state` — condição experimental;
- `descriptive_state` — estado não classificado.

Somente a existência de um objeto em `versions[]` não significa que exista um PID ou uma versão científica citável.

## 3. Compatibilidade com o schema físico

O campo `data_products.csv:version_or_collection` permanece temporariamente sincronizado.

Para cada produto com esse campo preenchido existe uma afirmação baseline na autoridade de versões.

A evolução futura pode acrescentar versões curadas adicionais sem exigir alteração imediata do CSV legado.

## 4. Apresentação pública

O renderer usa a semântica da versão para escolher o rótulo adequado.

Exemplos:

- `named_version` → “Versão”;
- `edition_or_year` → “Edição”;
- `provider_update` → “Atualização”;
- `service_state` → “Estado do serviço”;
- `access_configuration` → “Configuração de acesso”.

Assim, “acesso via projetos Google Cloud” deixa de ser apresentado genericamente como “Versão/coleção”.

## 5. Proveniência

A autoridade é:

`data/provenance_assertions.json`

sob:

`schema/provenance-assertions-v1.json`.

A unidade não é simplesmente “organização”, mas uma **afirmação de proveniência/responsabilidade** direcionada a um recurso.

Campos centrais:

- `provenance_id`;
- `record_id`;
- `target_id`;
- `agent_id`;
- `agent_label`;
- `roles`;
- `agent_identity_status`;
- `assertion_status`;
- `verified_at`.

## 6. Baseline conservador

O campo legado `owner_or_manager` frequentemente contém:

- mais de uma organização;
- redes e participantes;
- produtores e distribuidores misturados;
- provedores de insumo;
- operadores e instituições-mãe.

Por isso, o baseline preserva literalmente cada rótulo em uma afirmação:

`responsible_or_maintainer`

com:

`agent_identity_status = unresolved_label`

e:

`assertion_status = legacy_grouped_statement`.

Nenhum separador `/`, `;` ou “e” é usado automaticamente para criar agentes novos.

## 7. Papéis disponíveis para curadoria futura

O contrato admite:

- `responsible_or_maintainer`;
- `producer`;
- `maintainer`;
- `publisher`;
- `host`;
- `distributor`;
- `methodological_responsibility`.

Papéis específicos só devem ser promovidos quando houver evidência suficiente.

## 8. Relação com o public-record-v2

O read model agora declara:

- `curation.version_authority = data/product_versions.json`;
- `curation.provenance_authority = data/provenance_assertions.json`.

As `offerings[]` apontam para `version_ids`.

Os `agents[]` públicos são derivados das afirmações de proveniência, não mais diretamente de `owner_or_manager`.

## 9. Invariantes

- não dividir rótulos institucionais automaticamente;
- não transformar estado corrente em versão citável;
- não inventar data de emissão;
- não inferir produtor a partir de host;
- não inferir distribuidor a partir de publicador;
- preservar o texto legado até que haja curadoria mais específica;
- manter rastreabilidade até o campo fonte.

## 10. Próxima curadoria

A próxima fase de proveniência deve ser seletiva.

Prioridade recomendada:

- MapBiomas;
- TerraBrasilis;
- Google Earth Engine;
- GBIF;
- Carbon Mapper;
- RESOLVE;
- Global Safety Net;
- Global Human Modification;
- Planet Forest Carbon.

Nesses casos, a separação de produtor, mantenedor, publicador, host e distribuidor pode melhorar materialmente interpretação e futuras integrações.

Integration Registry continua posterior à estabilização desses papéis.
