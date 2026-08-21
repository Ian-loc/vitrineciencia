# Contrato de espelhamento no Google Drive

## Status

O Google Drive é **repositório documental, histórico e de espelhos derivados** da Vitrine Ciência. Ele não define o estado canônico corrente, não é gate de publicação e não deve concorrer com o GitHub.

Autoridade ativa:

- `Ian-loc/vitrineciencia`, branch `main`;
- `data/data_resources.csv`;
- `data/data_products.csv`;
- `data/product_distributions.csv`.

## Estado vivo

As contagens e o estado operacional corrente não são replicados neste contrato. Para o estado vivo, consultar `docs/PROJECT_STATE.md`, `WORKFLOW_STATUS.md` e as três tabelas canônicas em `data/`.

O workbook legado existente no Drive foi criado em fase anterior e **não deve ser apresentado como cópia corrente da base sem comparação contra um commit explícito da `main`**. Uma divergência do espelho é um problema de sincronização do derivado e não altera a autoridade dos dados canônicos do GitHub.

## Finalidade dos espelhos

Planilhas/`.xlsx` podem existir para:

- consulta manual;
- ensino/apresentação;
- interoperabilidade;
- snapshot de release;
- histórico de migração.

Eles são derivados e nunca recebem autoridade própria.

Fluxo autorizado:

`main → tabelas canônicas → validação → artefatos/release → espelho opcional`

Uma correção originada em planilha só se torna canônica após revisão e materialização no GitHub.

## Conteúdo recomendado de um espelho corrente

Quando regenerado, o espelho deve representar as três unidades do catálogo, preferencialmente em abas separadas:

- `data_resources`;
- `data_products`;
- `product_distributions`;
- metadados do snapshot;
- opcionalmente dicionário/changelog claramente identificados como auxiliares.

Não é suficiente atualizar apenas a aba de fontes e chamar o workbook de sincronizado se produtos/distribuições permanecerem antigos.

## Metadados mínimos

Registrar:

- `source_repository`;
- `source_branch`;
- `source_commit`;
- arquivos canônicos de origem;
- `generated_at`;
- número de fontes, produtos e distribuições;
- resultado da comparação;
- declaração de que o arquivo é derivado e não canônico;
- versão/tag quando o espelho representar uma release.

## Regras

1. preservar IDs canônicos e valores textuais;
2. não enriquecer/corrigir somente no espelho;
3. não alterar silenciosamente valores por fórmula/formatação;
4. não remover acentos, URLs, listas ou pontuação relevantes;
5. separar histórico/notas de dados canônicos;
6. declarar explicitamente escopo parcial quando o espelho não contiver as três tabelas.

## Verificação de sincronização

Um espelho só é **sincronizado** quando a comparação contra o commit-fonte confirma:

- cabeçalhos esperados;
- igualdade dos IDs incluídos;
- contagens coerentes com o escopo declarado;
- ausência de duplicações/deslocamentos;
- preservação dos valores;
- commit/data de geração registrados.

## Relação com release e DOI

O Drive **não é requisito** para release ou DOI. Para preservação científica, a prioridade é um snapshot reproduzível a partir de uma tag Git e depósito no repositório de preservação adotado. Um espelho pode ser gerado antes ou depois quando trouxer utilidade, sem bloquear o encerramento de uma release correta.

## Histórico

O contrato surgiu quando a Vitrine possuía 51 fontes e existiam planilhas com estruturas divergentes. Contagens como 51 ou versões como 0.7.0 são marcos históricos, não requisitos atuais. Desde a separação da Vitrine e do Simbiotrama, o GitHub é a autoridade operacional independente da Vitrine.
