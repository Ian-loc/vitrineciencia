# Public Record v2 — migração e compatibilidade

**Status:** read model v2 e renderer HTML v2 implementados; v1 preservado como compatibilidade  
**Milestone:** `VITRINE_PUBLIC_MODEL_V2`  
**Data:** 12 de outubro de 2026

## 1. Objetivo

O `public-record-v2` introduz a separação semântica entre:

```
Registro da Vitrine
        │ descreve
        ▼
Recurso catalogado
```

A migração não recataloga os 58 registros e não altera a experiência HTML neste primeiro passo.

## 2. Estratégia de implantação

O v2 é publicado em paralelo:

- v1 agregado: `/data/public_records.json`;
- v1 individual: `/data/registros/dr####.json`;
- v2 agregado: `/data/v2/public_records.json`;
- v2 individual: `/data/v2/registros/dr####.json`.

As páginas `/registros/dr####/` são renderizadas pelo v2. O v1 continua publicado em JSON para comparação, regressão e compatibilidade durante a transição.

## 3. Crosswalk principal

| v1 | v2 | Regra |
|---|---|---|
| `resource_id` | `record.id` | preservado sem alteração |
| `url` | `record.public_url` | preservado |
| `title` | `resource.name` | preservado |
| `acronym` | `resource.acronym` | preservado |
| `public_record_type` | `resource.type` | tipo passa a pertencer ao recurso |
| `official_identity` | `resource.official_identity` | preservado |
| `description` | `resource.description` | preservado |
| áreas/palavras-chave | `resource.themes` | reorganização estrutural |
| `scope` | `resource.scope` | preservado |
| `coverage` | `resource.coverage` | preservado |
| `content` | `resource.content_summary` | preservado como resumo |
| resumo de acesso | `resource.access_summary` | preservado |
| `products[]` | `offerings[]` | 1:1 no primeiro crosswalk |
| `product.version_or_collection` | `versions[]` + resumo na offering | somente quando já preenchido |
| rotas do registro | `access_routes[]` alvo `resource` | preservadas |
| distribuições DD | `access_routes[]` alvo `offering` | ID DD preservado |
| `owner_or_manager` | `agents[]` | papel conservador `responsible_or_maintainer` |
| evidência/verificação | `references[]` | deduplicação por URL |
| metadados internos | `curation` | separados do recurso |

## 4. Identidade do recurso

O v2 não inventa um identificador científico externo para o recurso.

Cada recurso recebe uma chave técnica derivada:

`DR####::resource`

com:

`identifier_status = derived_read_model_key`.

Essa chave serve somente à relação interna do read model. Não deve ser citada como PID, DOI, ID oficial do provedor ou substituta do `DR####`.

## 5. Offerings

Os 11 produtos DP existentes são migrados 1:1 para `offerings`.

Isso não implica que todo produto futuro precise manter a semântica histórica de DP. O objetivo deste passo é provar compatibilidade sem perda antes de refinar a ontologia.

Nenhuma offering é inventada para os registros que atualmente não possuem produtos detalhados.

## 6. Versões

Quando um produto v1 já possui `version_or_collection`, o v2 cria um objeto de versão derivado.

Esses objetos recebem:

- `identifier_status = derived_migration_key`;
- `status = legacy_summary`;
- `source_field = version_or_collection`.

Eles são mecanismos de migração e não IDs científicos permanentes. O desenho definitivo de versões será tratado em milestone próprio.

## 7. Rotas de acesso

O read model v2 unifica a representação estrutural de rotas, mas ainda não cria a fonte canônica `access_routes`.

Existem dois grupos:

1. rotas do recurso, derivadas do v1;
2. distribuições existentes, preservadas com seus IDs DD e direcionadas à offering correspondente.

A futura canonicalização das rotas deverá migrar a autoridade dos campos legados para uma fonte explícita, sem quebrar este contrato de leitura.

## 8. Agentes e proveniência

O campo `owner_or_manager` mistura papéis. A migração não tenta decidir automaticamente se uma organização é produtora, mantenedora, publicadora ou host.

Por isso, o primeiro crosswalk usa apenas:

`responsible_or_maintainer`.

Papéis mais específicos dependem de curadoria posterior.

## 9. Referências

Referência científica/técnica e fonte de verificação são migradas para `references[]`.

Quando a mesma URL cumpre os dois papéis, ela aparece uma vez com múltiplos papéis. A migração não cria nova evidência.

## 10. Invariantes de compatibilidade

O validador v2 exige:

- exatamente os mesmos 58 registros;
- mesmo conjunto de DRs;
- URLs públicas inalteradas;
- registro e recurso estruturalmente distintos;
- nomes, descrições, áreas, escopo, cobertura e limitações preservados;
- 11 produtos preservados como offerings;
- 19 distribuições preservadas como access routes;
- nenhuma conversão de desconhecido em negativo;
- JSON individual idêntico ao objeto correspondente do índice agregado.

## 11. Estado após a migração do renderer

Já mudou:

- o HTML das 58 páginas agora consome o read model v2;
- a ficha pública foi reduzida a cinco blocos;
- “tipo” é apresentado como propriedade do recurso catalogado;
- produtos detalhados aparecem como ofertas científicas subordinadas;
- curadoria ficou secundária no último bloco.

Ainda não mudou:

- cards de `sources.html`;
- `public-interface-guardrails.js`;
- a fonte canônica das rotas de acesso;
- schema físico DR/DP/DD;
- Integration Registry;
- conectores;
- harvesting;
- backend;
- API pública.

## 12. Próxima etapa

Após o renderer v2:

1. concluir QA dos arquétipos MapBiomas, TerraBrasilis, GEE, GBIF, REDEMET, RESOLVE, Carbon Mapper e Planet Forest Carbon;
2. simplificar os cards de descoberta na origem;
3. reduzir a responsabilidade de `public-interface-guardrails.js`;
4. tornar rotas de acesso uma fonte canônica explícita;
5. depois estruturar versões e proveniência mais específicas.

Referências:

- `schema/public-record-v2.json`;
- `scripts/build_public_records_v2.py`;
- `scripts/validate_public_records_v2.py`;
- `docs/WEB_API_EVOLUTION_PLAN.md`.
