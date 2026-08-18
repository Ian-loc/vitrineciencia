# Vitrine Ciência — contrato canônico de dados

Status: **ACTIVE / STABLE**  
Atualização: **2026-08-18**

## 1. Objetivo

Definir a semântica estável do catálogo para permitir crescimento e correção sem redesenhar a arquitetura a cada nova fonte.

As três tabelas canônicas são:

1. `data/data_resources.csv` — fontes;
2. `data/data_products.csv` — produtos;
3. `data/product_distributions.csv` — distribuições/acessos.

Snapshot de 18/08/2026: **125 fontes, 752 produtos e 783 distribuições**. Os identificadores correntes chegam a `DR0125`, `DP000756` e `DD000787`, porque lacunas históricas não são recicladas. As contagens são estado, não contrato.

## 2. Unidades semânticas

### Fonte (`DR####`)

Plataforma, portal, repositório, catálogo, programa, rede, observatório ou infraestrutura cientificamente útil como ponto de descoberta/acesso. Uma fonte não é fragmentada por arquivo, banda, tile, versão ou endpoint.

### Produto (`DP######`)

Oferta materialmente distinta dentro de uma fonte. A distinção deve melhorar descoberta, compreensão ou acesso por diferença relevante de finalidade, conteúdo, método, cobertura, suporte/resolução, coleção/versão ou condição de acesso.

### Distribuição (`DD######`)

Forma concreta de acessar um produto: download, API, serviço geoespacial, catálogo, aplicação ou outra rota de acesso. Uma distribuição não cria um novo produto por si só.

## 3. Tabela de fontes — 34 campos

`resource_id, resource_name, acronym, official_identity, description, homepage_url, data_access_url, research_areas, keywords, data_product_types, data_formats, visualization_types, geographic_coverage, covers_brazil, spatial_resolution, temporal_coverage, temporal_resolution, data_sources, free_download, access_conditions, programmatic_access, access_protocols, authentication_required, access_documentation_url, license, institutional_status, owner_or_manager, academic_uses, limitations, academic_evidence_type, academic_evidence_url, academic_evidence_note, verification_url, last_verified`

Regras centrais:

- `resource_id` é estável, único e nunca reciclado;
- identidade, descrição, responsável e URLs devem ser sustentados;
- `data_formats` descreve formatos, não protocolos;
- `access_protocols` descreve HTTP/API/OGC/STAC e equivalentes;
- resolução/temporalidade podem declarar variação quando um valor único seria falso;
- `last_verified` muda somente após revisão efetiva do registro;
- propriedades de um produto específico não devem ser promovidas para toda a fonte.

## 4. Tabela de produtos — 24 campos

`product_id, resource_id, product_name, product_acronym, product_family, product_kind, product_description, research_areas, keywords, geographic_coverage, covers_brazil, spatial_support, spatial_resolution, temporal_coverage, temporal_resolution, update_frequency, product_status, version_or_collection, enumeration_scope, product_page_url, methodology_url, primary_or_derived, limitations, last_verified`

Valores controlados de `product_kind` no contrato atual incluem:

- `dataset`;
- `dataset_series`;
- `catalog`;
- `federated_catalog`;
- `data_service`;
- `indicator_family`;
- `map_layer_collection`;
- `software_output`.

`enumeration_scope`: `complete`, `family_level`, `external_index` ou `representative_sample`.

Regras:

- todo produto referencia uma fonte existente;
- catálogos amplos usam `external_index`;
- não inventar versão, método, resolução ou frequência comuns quando variam;
- `methodology_url` pode permanecer vazio quando não existe metodologia específica apropriada;
- produto não é sinônimo de arquivo ou endpoint.

## 5. Tabela de distribuições — 15 campos

`distribution_id, product_id, distribution_name, access_url, format, access_protocol, access_tool, free_download, authentication_required, access_conditions, license, provider_attribution_required, subset_support, notes, last_verified`

Regras:

- toda distribuição referencia produto existente;
- todo produto deve possuir pelo menos uma distribuição no contrato publicado;
- formato, protocolo e ferramenta são propriedades distintas;
- licença é registrada no nível mais específico verificável;
- gratuidade e autenticação devem refletir a rota de acesso descrita, não uma generalização da plataforma.

## 6. Integridade relacional

1. IDs são únicos e obedecem aos padrões `DR####`, `DP######`, `DD######`.
2. Produto sem fonte é inválido.
3. Distribuição sem produto é inválida.
4. Produto sem distribuição é inválido no catálogo publicado.
5. Novas linhas não duplicam semanticamente entidades existentes apenas por diferenças técnicas menores.
6. IDs existentes não são reutilizados para outro objeto.

## 7. Ausência e incerteza

Nunca preencher por inferência. Conforme o campo/vocabulário, usar estados como:

- desconhecido;
- não localizado/não documentado;
- parcial;
- não aplicável;
- varia por produto/recurso.

Desconhecido não significa “não”.

## 8. Cobertura Brasil

`data/brazil_scope_priorities.json` é camada curatorial vinculada às fontes:

- P0 — fonte brasileira;
- P1 — cobertura Brasil sistemática;
- P2 — cobertura Brasil parcial/dependente do produto;
- P3 — referência comparativa excepcional sem cobertura direta.

A prioridade territorial organiza curadoria e descoberta; não certifica qualidade científica.

## 9. Variáveis e entidades adicionais

O schema `product-catalog-v0.1` registra `variable` como **deferred**. A Vitrine não possui hoje obrigação de migrar para um banco relacional ou criar entidades de release, variável, ativo, método ou perfil. Uma entidade adicional só deve ser proposta quando houver necessidade material recorrente que o contrato atual não represente de forma honesta.

## 10. Gate de entrada

### Nova fonte

Deve ser útil à descoberta científica relacionada ao Brasil, ter identidade rastreável, não duplicar uma fonte existente sem diferença útil e possuir evidência suficiente para os campos essenciais.

### Novo produto

Linha própria somente quando a distinção melhora materialmente a descoberta/compreensão/acesso.

### Nova distribuição

Deve representar uma rota de acesso real e verificável para produto existente.

## 11. Gate de auditoria

`registro atual → evidência oficial/primária → decisão campo a campo → correção inequívoca → validação → diff audit → integração conforme risco`

CI comprova conformidade estrutural, não verdade factual externa.

## 12. Estabilidade

O contrato é estável e permite crescimento de linhas. Nenhuma contagem histórica — 51/11/19, 125/752/783 ou outra — é requisito para manutenção ou release. Mudança incompatível do schema exige decisão separada e documentação coordenada.
