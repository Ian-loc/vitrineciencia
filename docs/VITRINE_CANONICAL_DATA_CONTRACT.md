# Vitrine Ciência — contrato canônico de dados

Status: **ACTIVE / NO SCHEMA EXPANSION**  
Data: 2026-08-10 (`America/Sao_Paulo`)  
Base: `main@9e83ffa3fa5fa6e74865f8f2986c30c7966ec239`

## 1. Objetivo

Congelar a semântica do modelo atual para permitir auditoria e crescimento de dados sem voltar a expandir arquitetura.

Este contrato **não adiciona colunas, entidades ou relações**. Ele documenta as três tabelas já canônicas:

1. `data/data_resources.csv` — 51 fontes;
2. `data/data_products.csv` — 11 produtos;
3. `data/product_distributions.csv` — 19 distribuições/acessos.

## 2. Unidade semântica

### Fonte (`DR####`)

Representa uma organização, plataforma, infraestrutura, catálogo ou serviço cientificamente útil como ponto de descoberta. Uma fonte não deve ser fragmentada por arquivo, camada, banda, release ou endpoint.

### Produto (`DP######`)

Representa uma oferta científica materialmente distinta dentro de uma fonte. Produto próprio exige diferença relevante de finalidade, método, cobertura, resolução/suporte, coleção/versão científica ou acesso.

### Distribuição (`DD######`)

Representa uma forma concreta de acessar um produto — download, metadados, API, catálogo ou outra rota de acesso. Distribuições não criam novos produtos por si só.

## 3. Contrato da tabela de fontes

Cabeçalho canônico atual, com **34 campos**:

`resource_id, resource_name, acronym, official_identity, description, homepage_url, data_access_url, research_areas, keywords, data_product_types, data_formats, visualization_types, geographic_coverage, covers_brazil, spatial_resolution, temporal_coverage, temporal_resolution, data_sources, free_download, access_conditions, programmatic_access, access_protocols, authentication_required, access_documentation_url, license, institutional_status, owner_or_manager, academic_uses, limitations, academic_evidence_type, academic_evidence_url, academic_evidence_note, verification_url, last_verified`

### 3.1 Identidade — obrigatória

- `resource_id` — ID estável `DR####`, único e nunca reciclado;
- `resource_name` — nome público da entrada;
- `official_identity` — identidade/função sustentada pela fonte oficial;
- `description` — resumo factual curto;
- `homepage_url` — página oficial principal vigente;
- `owner_or_manager` — responsável institucional;
- `institutional_status` — natureza institucional no vocabulário vigente.

`acronym` é opcional quando não existe sigla oficial ou de uso estabelecido.

### 3.2 Descoberta científica — obrigatória ou explicitamente variável

- `research_areas`;
- `keywords`;
- `data_product_types`;
- `geographic_coverage`;
- `covers_brazil`.

`spatial_resolution`, `temporal_coverage`, `temporal_resolution` e `data_sources` podem declarar variação por produto/recurso quando uma propriedade única da fonte seria falsa.

### 3.3 Acesso — obrigatório com desconhecido explícito quando necessário

- `data_access_url` — melhor rota oficial de acesso/descoberta;
- `free_download` — condição de download, não sinônimo de gratuidade da plataforma;
- `access_conditions`;
- `programmatic_access`;
- `access_protocols`;
- `authentication_required`;
- `license`.

`access_documentation_url` é condicional: preencher somente quando houver documentação oficial apropriada. Não usar outro tipo de URL apenas para evitar vazio.

### 3.4 Formatos e visualização

- `data_formats` descreve **formatos de dados**, não protocolos;
- `visualization_types` descreve formas de visualização;
- WMS/WFS/WCS/CSW/STAC/API/HTTP pertencem a `access_protocols`, não a `data_formats`.

Quando formatos variam entre recursos, declarar essa variação em vez de enumerar exaustivamente o catálogo externo.

### 3.5 Uso, limitações e evidência acadêmica

- `academic_uses` descreve usos plausíveis diretamente sustentados pelo conteúdo/escopo da fonte;
- `limitations` registra restrições relevantes para interpretação e uso;
- `academic_evidence_type`, `academic_evidence_url`, `academic_evidence_note` registram evidência acadêmica selecionada quando existente.

Esses campos **não devem ser usados como depósito para metodologia, metadados ou citação institucional apenas porque não existe coluna dedicada**.

### 3.6 Verificação

- `verification_url` deve apontar para evidência oficial representativa da identidade/estado da fonte;
- `last_verified` só deve mudar quando a linha foi efetivamente revisada na rodada atual, não quando apenas um link isolado foi testado.

## 4. Contrato da tabela de produtos

Cabeçalho canônico atual, com **24 campos**:

`product_id, resource_id, product_name, product_acronym, product_family, product_kind, product_description, research_areas, keywords, geographic_coverage, covers_brazil, spatial_support, spatial_resolution, temporal_coverage, temporal_resolution, update_frequency, product_status, version_or_collection, enumeration_scope, product_page_url, methodology_url, primary_or_derived, limitations, last_verified`

### Obrigatórios

- `product_id` — ID `DP######`, único;
- `resource_id` — deve existir em `data_resources.csv`;
- `product_name`;
- `product_kind`;
- `product_description`;
- `research_areas`;
- `geographic_coverage`;
- `covers_brazil`;
- `product_status`;
- `enumeration_scope`;
- `product_page_url`;
- `primary_or_derived`;
- `last_verified` após auditoria real.

### Condicionais

`product_acronym`, `product_family`, `keywords`, `spatial_support`, `spatial_resolution`, `temporal_coverage`, `temporal_resolution`, `update_frequency`, `version_or_collection`, `methodology_url` e `limitations` são preenchidos quando aplicáveis e sustentados.

Nunca inventar resolução, versão, frequência ou método comuns a uma família quando variam entre coleções.

## 5. Contrato da tabela de distribuições

Cabeçalho canônico atual, com **15 campos**:

`distribution_id, product_id, distribution_name, access_url, format, access_protocol, access_tool, free_download, authentication_required, access_conditions, license, provider_attribution_required, subset_support, notes, last_verified`

### Obrigatórios

- `distribution_id` — ID `DD######`, único;
- `product_id` — deve existir em `data_products.csv`;
- `distribution_name`;
- `access_url`;
- `access_protocol`;
- `access_tool`;
- `free_download`;
- `authentication_required`;
- `access_conditions`;
- `license` ou declaração explícita de que deve ser verificada no produto/provedor;
- `last_verified` após auditoria real.

`format`, `provider_attribution_required`, `subset_support` e `notes` são condicionais.

## 6. Regras relacionais

1. `resource_id` é único na tabela de fontes.
2. `product_id` é único e deve referenciar uma fonte existente.
3. `distribution_id` é único e deve referenciar um produto existente.
4. Produto não pode existir sem fonte pai.
5. Distribuição não pode existir sem produto pai.
6. Novas linhas não devem duplicar semanticamente uma entidade existente apenas por diferença de URL, formato ou versão técnica sem significado científico.

## 7. Ausência e incerteza

Nunca inferir para completar tabela.

Quando o vocabulário atual permitir, distinguir:

- desconhecido / não documentado;
- não localizado;
- não aplicável;
- parcial;
- varia conforme produto/recurso.

O valor deve refletir a propriedade no nível da entidade representada. Propriedade de um dataset específico não deve ser promovida à plataforma inteira.

## 8. Evidência externa que não cabe no schema

A auditoria pode encontrar URLs oficiais úteis para:

- catálogos de metadados;
- metodologia;
- instruções de citação;
- frequência de atualização da plataforma.

Quando não houver campo semanticamente correto, a informação fica na **trilha de auditoria**, não é forçada em coluna inadequada.

Adicionar nova coluna é mudança de contrato e deve ser avaliada separadamente como `HUMAN-DECISION` se alterar o modelo conceitual. A mera existência de informação útil não justifica expansão do schema.

## 9. Gate de entrada de nova fonte

Uma fonte nova deve:

1. ser materialmente útil para descoberta científica relacionada ao Brasil;
2. possuir identidade institucional rastreável;
3. não duplicar entrada existente;
4. poder ser descrita no contrato atual sem inventar propriedades;
5. ter evidência oficial suficiente para os campos essenciais.

## 10. Gate de entrada de novo produto

Produto próprio somente quando a distinção melhora de forma material a descoberta/compreensão/acesso. Arquivo, tile, banda, formato, endpoint ou atualização técnica isolados não satisfazem esse critério.

## 11. Gate de auditoria

Para cada registro:

`registro atual → evidência legada útil → fonte oficial atual → decisão campo a campo → correção inequívoca → validação → diff audit → integração conforme risco`

Correções pequenas, factuais e inequívocas dentro deste contrato são `AUTO-SAFE`. Evidência conflitante ou alteração semântica relevante sobe para `REVIEW`. Mudança do contrato sobe para `HUMAN-DECISION`.

## 12. Critério de estabilidade

Este contrato permanece congelado durante a auditoria 51 + 11 + 19. Lacunas encontradas devem ser registradas; não se altera o schema no meio da auditoria apenas para acomodar uma fonte específica.