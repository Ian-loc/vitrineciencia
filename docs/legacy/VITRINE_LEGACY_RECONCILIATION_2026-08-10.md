# Vitrine Ciência — reconciliação dos PRs legados #57–#69

Data operacional: 2026-08-10 (`America/Sao_Paulo`)  
Autoridade de partida: `main@ba80cc44d2d2d42d7bda54bff9d84ddff97a5c18`

## Objetivo

Remover ambiguidade entre a Vitrine Ciência atual e a cadeia histórica de desenvolvimento #57–#69, preservando evidência científica útil sem reintroduzir a arquitetura antiga de Instância 1/PostgreSQL.

A regra é conservadora:

> **preservar evidência primeiro; corrigir o catálogo depois; nunca importar automaticamente valores legados.**

Os PRs antigos permanecem parte do histórico do GitHub. A reconciliação decide apenas o que deve continuar como insumo científico, o que é histórico e o que não deve voltar ao produto atual.

## Autoridade atual

A Vitrine é um catálogo delimitado de descoberta de dados científicos. Seu modelo conceitual é estável. O crescimento deve ocorrer principalmente por aumento do volume de fontes/produtos, correção de metadados, usabilidade, manutenção e releases.

Não são dependências da Vitrine:

- PostgreSQL/PostGIS;
- `catalog_entries`, `entry_variables`, `entry_evidence` ou outros schemas da antiga Instância 1;
- runtime de ingestão do Simbiotrama;
- genealogia obrigatória produto → release → distribuição → ativo;
- guards específicos por plataforma como requisito geral do catálogo.

## Classificações

- **SALVAGE** — contém evidência/curadoria que deve ser reavaliada contra a fonte oficial atual e, quando sustentada, usada para corrigir ou enriquecer a Vitrine atual.
- **HISTORICAL** — útil como proveniência, aprendizado ou registro de decisão, mas não é autoridade operacional.
- **SUPERSEDED** — arquitetura, processo ou decisão substituída pelo modelo atual; não deve ser integrada.
- **REMOVE** — não precisa ser preservado como arquivo ativo porque Git history já mantém sua proveniência. A classificação `REMOVE` nunca autoriza apagar evidência científica antes do salvamento.

## Matriz dos PRs

### PR #57 — Marco 2A DETER Cerrado

**Head histórico:** `7f12d64fe3a0c5ea5f735a77f25b7756d0773ad9`  
**Classificação:** `SALVAGE + HISTORICAL`  
**Política:** **NUNCA MESCLAR** no modelo atual.

O PR contém oito `database/mappings/deter_cerrado_*_guard_2026.json`, oito validadores correspondentes e relatórios de auditoria específicos de DETER Cerrado.

Valor reutilizável potencial:

- identidade e fronteira científica de DETER Cerrado;
- acesso, licença e citação;
- metadados e identificadores;
- método;
- legenda/classes;
- latência/operacionalização;
- qualidade e validação;
- endpoints oficiais quando ainda pertinentes.

Tratamento: extrair somente afirmações úteis ao modelo atual, revalidar nas fontes oficiais vigentes e comparar com `data/data_resources.csv`, `data/data_products.csv` e `data/product_distributions.csv`. Os guards e validadores específicos não entram no produto atual.

### PR #58 — simplificação da antiga Instância 1

**Head histórico:** `4af0d76233c17d40349483f5ad69c205a9989af2`  
**Classificação:** `HISTORICAL + SUPERSEDED`  
**Política:** **NUNCA MESCLAR**.

Conteúdo predominante: contratos, governança, schemas conceituais, roadmap, validators e documentação da antiga Instância 1.

Princípios ainda válidos — granularidade mínima suficiente, não inventar valores ausentes, distinguir plataforma de produto — já foram absorvidos pelo modelo operacional atual. Não há necessidade de portar o runtime/contrato antigo.

### PR #59 — implementação PostgreSQL do núcleo mínimo

**Head histórico:** `1fc7f9be704878261042a5a315f8827f81f0f3da`  
**Classificação:** `SUPERSEDED + REMOVE`  
**Política:** **NUNCA MESCLAR**.

Arquivos: workflow específico, schema SQL, script de promoção e testes transacionais. Não há payload curatorial independente a recuperar neste PR.

### PR #60 — lote curatorial 01

**Head histórico:** `c40e814abee05fb4592b1e94554abbe2ad9496ac`  
**Classificação:** `SALVAGE` para `data/instance1_entry_enrichment_batch01.json`; infraestrutura do PR é `SUPERSEDED`.

Cobertura: `DR0002`, `DR0003`, `DR0004`.

### PR #61 — lote curatorial 02

**Head histórico:** `94e5568edb4cce4138f829b9c34234bd168b1d88`  
**Classificação:** `SALVAGE` para `data/instance1_entry_enrichment_batch02.json`; workflow antigo é `SUPERSEDED`.

Cobertura: `DR0005`–`DR0007`.

### PR #62 — lote curatorial 03

**Head histórico:** `50b9e3a988fd3ed50ff351e6b0f975ee2feb00ea`  
**Classificação:** `SALVAGE` para `data/instance1_entry_enrichment_batch03.json`; workflow antigo é `SUPERSEDED`.

Cobertura: `DR0008`–`DR0010`.

### PR #63 — lotes curatoriais 04 e 05

**Head histórico:** `27761312c6c7bca26377d465f68ad1b1ee4df36f`  
**Classificação:** `SALVAGE`.

Payloads:

- `data/instance1_entry_enrichment_batch04.json`;
- `data/instance1_entry_enrichment_batch05.json`.

Cobertura conjunta: `DR0011`–`DR0016`.

### PR #64 — lote curatorial 06

**Head histórico:** `7467c15fae0424643333fc111dba2d8734d5b69c`  
**Classificação:** `SALVAGE`.

Payload: `data/instance1_entry_enrichment_batch06.json`.

Cobertura: `DR0001`, `DR0017`–`DR0021`.

### PR #65 — lote curatorial 07

**Head histórico:** `f6af113a3c8bbd80d80ce0c4fc45f7742f9c4634`  
**Classificação:** `SALVAGE`.

Payload: `data/instance1_entry_enrichment_batch07.json`.

Cobertura: `DR0022`–`DR0027`.

### PR #66 — lote curatorial 08

**Head histórico:** `15ab97f15574aa7086fa4402627ff32c74f2159b`  
**Classificação:** `SALVAGE`.

Payload: `data/instance1_entry_enrichment_batch08.json`.

Cobertura: `DR0028`–`DR0033`.

### PR #67 — lote curatorial 09

**Head histórico:** `04044cef01fe4dc046d4cf8509215d915f446eb9`  
**Classificação:** `SALVAGE`.

Payload: `data/instance1_entry_enrichment_batch09.json`.

Cobertura: `DR0034`–`DR0039`.

### PR #68 — lote curatorial 10

**Head histórico:** `6d22b82e61df419b1e3be2cd1971d9b8fdb9573a`  
**Classificação:** `SALVAGE`.

Payload: `data/instance1_entry_enrichment_batch10.json`.

Cobertura: `DR0040`–`DR0045`.

### PR #69 — lote curatorial 11

**Head histórico:** `cfde00033b8bf542c1d0147685acc31278cef8f3`  
**Classificação:** `SALVAGE`.

Payload: `data/instance1_entry_enrichment_batch11.json`.

Cobertura: `DR0046`–`DR0051`.

## Cobertura dos lotes salváveis

A união dos lotes 01–11 cobre as 51 fontes atuais:

- lote 06: `DR0001`;
- lote 01: `DR0002`–`DR0004`;
- lote 02: `DR0005`–`DR0007`;
- lote 03: `DR0008`–`DR0010`;
- lotes 04–05: `DR0011`–`DR0016`;
- lote 06: `DR0017`–`DR0021`;
- lote 07: `DR0022`–`DR0027`;
- lote 08: `DR0028`–`DR0033`;
- lote 09: `DR0034`–`DR0039`;
- lote 10: `DR0040`–`DR0045`;
- lote 11: `DR0046`–`DR0051`.

Essa cobertura **não equivale a 51/51 campos corretos hoje**. Ela significa apenas que existe material legado a ser usado como ponto de partida para uma nova auditoria.

## Crosswalk seguro: legado → Vitrine atual

Os lotes antigos usam campos que não correspondem um-a-um ao CSV atual. A regra é não converter semanticamente por aproximação.

| Campo legado | Campo atual possível | Regra |
|---|---|---|
| `stable_id` | `resource_id` | correspondência direta, mas confirmar identidade antes de qualquer edição |
| `free_access` | `free_download` e/ou `access_conditions` | **não importar diretamente**; acesso gratuito à plataforma não implica download gratuito de todo recurso |
| `authentication_required` | `authentication_required` | mesmo conceito geral, mas converter vocabulário somente após revalidação (`yes/no/partial` ≠ `sim/não/...` automaticamente) |
| `metadata_url` | nenhum campo dedicado | usar como evidência/rota de verificação; não forçar em `access_documentation_url` |
| `methodology_url` | nenhum campo dedicado | usar como evidência para descrição/limitações/metodologia do produto quando aplicável; não forçar em campo inadequado |
| `citation_text` | nenhum campo dedicado | preservar como evidência; não inserir em `academic_evidence_note` sem justificativa |
| `citation_url` | nenhum campo dedicado | preservar como evidência; pode apoiar instrução futura de citação/release |
| `update_frequency_text` | nenhum equivalente direto | **não converter em `temporal_resolution`**; são conceitos distintos |

## Estados de evidência

Os lotes antigos usam, entre outros:

- `verified`;
- `partially_verified`;
- `not_found`;
- `not_applicable`.

Esses estados qualificam **a afirmação no momento daquela curadoria**, não o registro atual inteiro. Eles não devem ser transformados em confiança global da fonte.

Na nova auditoria:

1. abrir a evidência oficial registrada;
2. confirmar se ainda é atual e se sustenta exatamente a afirmação;
3. registrar mudança de URL/versão quando houver;
4. comparar com o valor atual no CSV;
5. modificar o CSV apenas quando a evidência atual sustentar a correção;
6. manter ausência explícita quando a propriedade não existe no nível da fonte.

## Ordem de salvamento

A auditoria científica 51/51 deve reutilizar os lotes como fila, na ordem dos IDs canônicos, e não na ordem histórica dos PRs.

Para cada `DR####`:

`registro atual → payload legado → fonte oficial atual → decisão de campo → validação → próximo registro`.

O objetivo é terminar com uma única tabela canônica atual, não manter dois sistemas de verdade.

## Política de fechamento dos PRs antigos

- #58 e #59 podem ser fechados como `superseded` após esta reconciliação estar integrada no `main`.
- #57 deve permanecer acessível como evidência histórica até a revalidação específica de DETER Cerrado; depois pode ser fechado como `superseded / evidence preserved`.
- #60–#69 devem permanecer acessíveis até que os respectivos lotes tenham sido percorridos na auditoria 51/51 e os valores úteis tenham sido incorporados ou explicitamente rejeitados.
- fechar um PR não autoriza apagar seu commit ou sua proveniência.

## Critério de conclusão da reconciliação legada

Este trabalho será concluído apenas quando:

1. todos os PRs #57–#69 estiverem classificados;
2. os 11 lotes estiverem registrados por SHA e caminho;
3. a auditoria 51/51 tiver decidido cada candidato reutilizável;
4. nenhum valor legado estiver sendo tratado como verdadeiro sem verificação atual;
5. os PRs obsoletos tiverem sido fechados com disposição clara;
6. a fila normal de desenvolvimento deixar de depender da arquitetura antiga.

## Próxima ação após este pacote

Iniciar a auditoria científica de `DR0001` e seguir sequencialmente até `DR0051`, usando o manifesto legado como apoio e as fontes oficiais atuais como autoridade factual.