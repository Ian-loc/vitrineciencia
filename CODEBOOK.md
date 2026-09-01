# Dicionário de dados — Vitrine Ciência

**Status:** SCHEMA FÍSICO LEGADO / COMPATIBILIDADE  
**Atualização:** 2026-09-01

Este documento descreve os campos das três tabelas históricas usadas por `v1.0.0` e pelo branch candidato do PR #267. Ele **não define a ontologia final da Vitrine 2.0**.

- `data/data_resources.csv` — registros `DR####`, historicamente chamados de fontes;
- `data/data_products.csv` — registros `DP######`;
- `data/product_distributions.csv` — registros `DD######`.

Na `main` pública corrente, o catálogo expandido permanece 135/843/876. No PR #267, o schema físico candidato contém 51 DR / 11 produtos / 19 distribuições e a expansão está preservada em quarentena.

`DR####` deve ser interpretado como identificador legado até que a auditoria 51/51 determine o tipo real da entidade. Os campos abaixo continuam válidos como contrato físico de leitura/reprodução, não como prova de que todos os DR representam o mesmo tipo ontológico.

## Registros DR — 34 campos

| Campo | Definição operacional |
|---|---|
| `resource_id` | Identificador legado estável `DR####`. |
| `resource_name` | Nome registrado; deve ser confrontado com a identidade oficial. |
| `acronym` | Sigla ou nome curto, quando aplicável. |
| `official_identity` | Natureza/função documentada; não substitui a classificação ontológica atual. |
| `description` | Síntese objetiva do propósito/conteúdo. |
| `homepage_url` | Página institucional/oficial. |
| `data_access_url` | Rota cadastrada para descobrir/consultar/baixar dados; deve ser verificada. |
| `research_areas` | Áreas temáticas legadas usadas na descoberta. |
| `keywords` | Termos pesquisáveis. |
| `data_product_types` | Resumo legado dos tipos de conteúdo. |
| `data_formats` | Formatos; podem variar por dataset/coleção. |
| `visualization_types` | Formas gerais de visualização. |
| `geographic_coverage` | Abrangência espacial geral documentada. |
| `covers_brazil` | Indicação legada de cobertura brasileira. |
| `spatial_resolution` | Resumo de suporte/resolução; pode variar. |
| `temporal_coverage` | Período geral coberto. |
| `temporal_resolution` | Granularidade temporal geral. |
| `data_sources` | Origem empírica/institucional dos dados. |
| `free_download` | Condição geral registrada de download gratuito. |
| `access_conditions` | Cadastro, solicitação, quota, embargo ou restrição. |
| `programmatic_access` | Existência registrada de acesso automatizado. |
| `access_protocols` | HTTP/API/OGC/STAC e equivalentes. |
| `authentication_required` | Necessidade de credencial. |
| `access_documentation_url` | Documentação técnica do acesso. |
| `license` | Licença/condição sustentada no nível descrito. |
| `institutional_status` | Natureza institucional registrada. |
| `owner_or_manager` | Responsável registrado. |
| `academic_uses` | Usos documentados/plausíveis para pesquisa/ensino/extensão. |
| `limitations` | Limitações gerais e cautelas. |
| `academic_evidence_type` | Tipo de evidência acadêmica/técnica representativa. |
| `academic_evidence_url` | Evidência representativa. |
| `academic_evidence_note` | O que a evidência sustenta. |
| `verification_url` | Evidência oficial principal da revisão. |
| `last_verified` | Data da revisão efetiva da linha. |

## Produtos — 24 campos

`product_id, resource_id, product_name, product_acronym, product_family, product_kind, product_description, research_areas, keywords, geographic_coverage, covers_brazil, spatial_support, spatial_resolution, temporal_coverage, temporal_resolution, update_frequency, product_status, version_or_collection, enumeration_scope, product_page_url, methodology_url, primary_or_derived, limitations, last_verified`

`resource_id` é apenas a relação física legada com DR; essa relação poderá ser reinterpretada pelo crosswalk ontológico.

## Distribuições — 15 campos

`distribution_id, product_id, distribution_name, access_url, format, access_protocol, access_tool, free_download, authentication_required, access_conditions, license, provider_attribution_required, subset_support, notes, last_verified`

Distribuição deve representar rota real de acesso quando publicada. API, WMS/WFS, arquivo e landing page são mecanismos diferentes; viewer/documentação devem ser qualificados explicitamente.

## Regra de transição

Preservar IDs e campos até a migração controlada. O novo schema canônico só substitui este codebook depois de G0–G4 PASS, crosswalk 51/51 e validadores aprovados.

Estado corrente: `docs/PROJECT_STATE.md`. Contrato transitório: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`.
