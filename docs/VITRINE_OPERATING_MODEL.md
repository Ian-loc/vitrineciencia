# Vitrine Ciência — modelo operacional

**Status:** TRANSIÇÃO CONTROLADA  
**Atualização:** 2026-09-01

## Produto

A Vitrine é um catálogo de descoberta e acesso a dados científicos relevantes ao Brasil. O objetivo corrente é consolidar uma arquitetura simples, verificável e semanticamente correta antes de voltar a expandir o corpus.

A expansão de novas fontes, produtos e distribuições está **pausada**. Os termos são mantidos aqui apenas para compatibilidade com o schema legado.

## Estado operacional

- `main` continua no catálogo expandido 135/843/876;
- `v1.0.0` está publicada e permanece imutável;
- PR draft #267 contém o candidato 51 DR / 11 produtos / 19 distribuições e a quarentena da expansão;
- os 51 DR estão sob auditoria ontológica;
- nenhum conector federado faz parte do estado consolidado atual.

## Pipeline de trabalho atual

`inventário → evidência oficial → classificação ontológica → crosswalk → validação do modelo → registro de integração → pilotos → pipeline federado → publicação controlada → QA/reprodução`

A maior unidade coerente e segura deve ser processada por rodada. Casos bloqueados externamente não impedem avanço de casos independentes.

## Gates

### Fase 1 — ontologia

G0 inventário reconciliado → G1 51/51 classificados → G2 conflitos resolvidos/explicitados → G3 crosswalk consolidado → G4 modelo mínimo validado.

### Fase 2 — integração

Registrar para 51/51: método de acesso, endpoint/documentação quando aplicável, autenticação, status e prioridade. Classificar como automatizável agora/depois, manual-curated ou não prioritário.

### Fase 3 — federação

Primeiro piloto: MapBiomas Alerta GraphQL V2. Depois pelo menos três casos tecnologicamente distintos. Todo recurso passa por `raw → normalize → validate → deduplicate → classify → verify_access → quarantine/accept → publish`.

## Regras de qualidade

- evidência oficial antes de inferência;
- sem publicação direta de raw;
- falha de gate impede promoção;
- HTTP 200 não prova acesso a dados;
- ausência ou ambiguidade gera flag/quarentena, não preenchimento especulativo;
- read-back após escrita material;
- release histórica não é reescrita.

## Classes de mudança

- **DOC/QA:** pode avançar quando corrige estado, precisão ou verificabilidade sem alterar escopo.
- **CURATION:** exige evidência e validação proporcional.
- **SCHEMA/ONTOLOGY:** somente após G0–G4.
- **FEDERATION:** somente após Integration Registry.
- **RELEASE:** somente após o marco global e decisão humana específica.

## Limite da execução

O trabalho termina apenas no marco `VITRINE_FEDERATED_CORE_V1_CONSOLIDATED`, definido em `WORKFLOW_STATUS.md`, com artefatos materializados, QA global, reprodução limpa e smoke test público PASS.

Depois desse marco, expansão adicional constitui novo milestone.
