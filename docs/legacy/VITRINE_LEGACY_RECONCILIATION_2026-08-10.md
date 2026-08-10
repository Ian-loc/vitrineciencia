# Vitrine Ciência — reconciliação dos PRs legados #57–#69

Data operacional: 2026-08-10 (`America/Sao_Paulo`)  
Autoridade de partida: `main@ba80cc44d2d2d42d7bda54bff9d84ddff97a5c18`

## Objetivo

Remover ambiguidade entre a Vitrine Ciência atual e a cadeia histórica de desenvolvimento #57–#69, preservando evidência científica útil sem reintroduzir a arquitetura antiga de Instância 1/PostgreSQL.

Regra conservadora:

> **preservar evidência primeiro; corrigir o catálogo depois; nunca importar automaticamente valores legados.**

Os PRs antigos permanecem parte do histórico do GitHub. A reconciliação decide o que continua como insumo científico, o que é histórico e o que não deve voltar ao produto atual.

## Autoridade atual

A Vitrine é um catálogo delimitado de descoberta de dados científicos. Seu modelo conceitual é estável. O crescimento deve ocorrer principalmente por aumento do volume de fontes/produtos, correção de metadados, usabilidade, manutenção e releases.

Não são dependências da Vitrine: PostgreSQL/PostGIS; schemas/runtime da antiga Instância 1; runtime do Simbiotrama; genealogia obrigatória produto → release → distribuição → ativo; guards específicos por plataforma como requisito geral.

## Classificações

- **SALVAGE** — evidência/curadoria a reavaliar contra a fonte oficial atual antes de qualquer uso.
- **HISTORICAL** — proveniência/aprendizado, não autoridade operacional.
- **SUPERSEDED** — arquitetura/processo substituído; não integrar.
- **REMOVE** — não precisa permanecer como arquivo operacional ativo porque Git history preserva a proveniência. Nunca autoriza apagar evidência científica antes do salvamento.

## Matriz dos PRs

### #57 — SALVAGE + HISTORICAL
Head histórico: `7f12d64fe3a0c5ea5f735a77f25b7756d0773ad9`.

Contém guards, validadores e relatórios específicos de DETER Cerrado. Valor potencial: identidade, método, classes, acesso, licença, metadados, latência, qualidade, limitações e endpoints oficiais ainda pertinentes. Esses fatos devem ser extraídos somente durante a nova auditoria e revalidados na fonte oficial. Guards/arquitetura não entram no produto atual.

### #58 — HISTORICAL + SUPERSEDED
Head histórico: `4af0d76233c17d40349483f5ad69c205a9989af2`.

Política/arquitetura da antiga Instância 1. Princípios ainda válidos — granularidade mínima suficiente, não inventar valores, distinguir plataforma de produto — já estão absorvidos no modelo operacional atual. Não portar runtime/contrato antigo.

### #59 — SUPERSEDED + REMOVE
Head histórico: `1fc7f9be704878261042a5a315f8827f81f0f3da`.

Workflow, schema SQL, promoção e testes PostgreSQL. Não há payload curatorial independente a recuperar.

### #60 — SALVAGE lote 01
Head: `c40e814abee05fb4592b1e94554abbe2ad9496ac`. Payload: `data/instance1_entry_enrichment_batch01.json`. Cobertura: `DR0002`–`DR0004`.

### #61 — SALVAGE lote 02
Head: `94e5568edb4cce4138f829b9c34234bd168b1d88`. Payload: `data/instance1_entry_enrichment_batch02.json`. Cobertura: `DR0005`–`DR0007`.

### #62 — SALVAGE lote 03
Head: `50b9e3a988fd3ed50ff351e6b0f975ee2feb00ea`. Payload: `data/instance1_entry_enrichment_batch03.json`. Cobertura: `DR0008`–`DR0010`.

### #63 — SALVAGE lotes 04–05
Head: `27761312c6c7bca26377d465f68ad1b1ee4df36f`. Payloads: `batch04.json`, `batch05.json`. Cobertura: `DR0011`–`DR0016`.

### #64 — SALVAGE lote 06
Head: `7467c15fae0424643333fc111dba2d8734d5b69c`. Payload: `batch06.json`. Cobertura: `DR0001`, `DR0017`–`DR0021`.

### #65 — SALVAGE lote 07
Head: `f6af113a3c8bbd80d80ce0c4fc45f7742f9c4634`. Cobertura: `DR0022`–`DR0027`.

### #66 — SALVAGE lote 08
Head: `15ab97f15574aa7086fa4402627ff32c74f2159b`. Cobertura: `DR0028`–`DR0033`.

### #67 — SALVAGE lote 09
Head: `04044cef01fe4dc046d4cf8509215d915f446eb9`. Cobertura: `DR0034`–`DR0039`.

### #68 — SALVAGE lote 10
Head: `6d22b82e61df419b1e3be2cd1971d9b8fdb9573a`. Cobertura: `DR0040`–`DR0045`.

### #69 — SALVAGE lote 11
Head: `cfde00033b8bf542c1d0147685acc31278cef8f3`. Cobertura: `DR0046`–`DR0051`.

## Cobertura dos lotes salváveis

A união dos lotes 01–11 cobre `DR0001`–`DR0051`. Isso **não equivale a 51 registros factualmente corretos hoje**; significa somente que existe material histórico para acelerar uma nova auditoria.

## Crosswalk seguro

| Campo legado | Campo atual potencial | Regra |
|---|---|---|
| `stable_id` | `resource_id` | confirmar identidade |
| `free_access` | `free_download` / `access_conditions` | não importar diretamente |
| `authentication_required` | `authentication_required` | converter só após revalidar semântica/vocabulário |
| `metadata_url` | sem campo direto | usar como evidência; não forçar em campo inadequado |
| `methodology_url` | sem campo direto | usar como evidência; não forçar em `academic_evidence_url` |
| `citation_text` / `citation_url` | sem campo direto | preservar para auditoria/contrato |
| `update_frequency_text` | sem equivalente | **nunca converter em `temporal_resolution`** |

Os estados `verified`, `partially_verified`, `not_found` e `not_applicable` qualificam afirmações na curadoria histórica; não são confiança global atual.

## Ordem de salvamento

A auditoria deve seguir IDs canônicos:

`registro atual → payload legado → fonte oficial atual → decisão de campo → validação → próximo registro`.

Para cada `DR####`:

1. ler a linha canônica;
2. ler somente o payload legado correspondente;
3. revalidar a fonte oficial atual;
4. decidir campos independentemente;
5. corrigir apenas valores inequívocos e sustentados;
6. registrar lacunas sem inferência;
7. atualizar `last_verified` somente após verificação real;
8. validar catálogo e diff;
9. registrar aceitação/rejeição/ausência de equivalente para evidência legada.

## Política de fechamento

- #58/#59 podem ser fechados como `superseded` depois desta reconciliação estar em `main`;
- #57 permanece acessível até DETER Cerrado ser revalidado;
- #60–#69 permanecem acessíveis até seus lotes serem percorridos;
- fechar PR não apaga commits/proveniência.

## Classificação de risco deste pacote

**AUTO-SAFE.**

Motivos:

- somente governança/status/proveniência;
- nenhum CSV/JSON canônico alterado;
- nenhum frontend, build ou Pages alterado;
- analytics não ativado;
- totalmente reversível pelo Git;
- CI, diff audit e zero achados continuam obrigatórios.

Pelo modelo operacional atual, este pacote pode ser integrado sem interrupção humana adicional depois que os controles objetivos passarem. Gates humanos permanecem para `REVIEW` e `HUMAN-DECISION`.

## Critério de conclusão da reconciliação legada

1. todos #57–#69 classificados;
2. 11 lotes registrados por SHA/caminho;
3. auditoria 51/51 decide cada candidato reutilizável;
4. nenhum valor legado tratado como atual sem verificação;
5. PRs obsoletos fechados com disposição clara;
6. fila normal deixa de depender da arquitetura antiga.

## Próxima ação

Iniciar auditoria científica em `DR0001` e seguir até `DR0051`, usando legado como apoio e fontes oficiais atuais como autoridade factual.