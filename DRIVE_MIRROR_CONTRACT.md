# Contrato histórico de espelhamento no Google Drive

## Status

Este documento registra a política histórica de espelhamento da base no Google Drive. **Ele não define mais o estado canônico corrente da Vitrine Ciência e não deve ser usado como gate de publicação, auditoria ou DOI.**

A autoridade ativa é o repositório `Ian-loc/vitrineciencia`, branch `main`, com as tabelas:

- `data/data_resources.csv`;
- `data/data_products.csv`;
- `data/product_distributions.csv`.

O site público e os JSONs são artefatos derivados dessas tabelas.

## Finalidade dos espelhos

Planilhas ou arquivos `.xlsx` mantidos no Drive podem continuar existindo para consulta, histórico, interoperabilidade ou trabalho manual, mas são **espelhos derivados**. Eles não substituem o GitHub, não recebem autoridade própria e não devem ser usados para corrigir a base canônica sem passar pelo fluxo normal de curadoria e validação.

Fluxo autorizado:

`main → tabelas canônicas → validação → artefatos públicos/release → espelhos opcionais`

Alterações originadas em um espelho somente alcançam a Vitrine após revisão e materialização no GitHub.

## Metadados mínimos de um espelho

Toda regeneração de planilha ou `.xlsx` deve registrar, quando aplicável:

- `catalog_version` ou tag da release;
- `source_repository`;
- `source_branch`;
- `source_commit`;
- arquivos canônicos de origem;
- `generated_at`;
- `generated_by`;
- número de fontes, produtos e distribuições incluídos;
- resultado da verificação;
- declaração explícita de que o arquivo é derivado e não canônico.

## Regras de conteúdo

1. IDs canônicos devem permanecer únicos e inalterados.
2. Valores textuais, URLs, listas multivaloradas, acentos e pontuação devem ser preservados quando o objetivo for um espelho fiel.
3. Nenhum valor deve ser enriquecido, abreviado ou corrigido somente no espelho.
4. Abas históricas, dicionários, auditorias e notas podem ser preservados, desde que claramente identificados como não canônicos.
5. Fórmulas, filtros e formatação não podem alterar silenciosamente os valores exportados.
6. Um espelho de release deve declarar exatamente qual commit/tag originou seus dados.

## Verificação de sincronização

Um espelho só pode ser chamado de sincronizado quando a comparação com o snapshot-fonte confirmar:

- cabeçalhos esperados;
- igualdade dos IDs incluídos;
- ausência de duplicações ou deslocamentos;
- preservação de URLs e valores textuais;
- contagens coerentes com o escopo declarado;
- commit-fonte e data de geração registrados.

As contagens históricas de 51 fontes e versões antigas como 0.7.0 pertencem ao estágio inicial do projeto e **não são requisitos da Vitrine atual**.

## Relação com releases e DOI

O Drive não é requisito para uma release citável nem para o DOI. Para arquivamento científico, a prioridade é produzir um snapshot reproduzível a partir de uma tag Git e depositá-lo no repositório de preservação adotado, mantendo o commit-fonte e as licenças explícitos.

Espelhos em Drive podem ser gerados depois da release quando trouxerem utilidade operacional, mas não devem bloquear o encerramento de uma versão tecnicamente válida.

## Registro histórico

Em julho de 2026, a política de espelhamento foi criada quando o catálogo possuía 51 fontes e a planilha nativa e o `.xlsx` tinham estados de sincronização diferentes. Essa informação permanece relevante apenas como histórico de migração. Desde a separação estrutural da **Vitrine Ciência** em agosto de 2026, o GitHub passou a ser a autoridade operacional independente do produto público.
