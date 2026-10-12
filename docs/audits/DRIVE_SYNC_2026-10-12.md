# Auditoria do Drive — 12/10/2026

Fonte canônica: `Ian-loc/vitrineciencia`, `main`, commit `bb7c21b13585c94dc57e37efdc3af45eeabf6178`.
Pasta: https://drive.google.com/drive/folders/1QTJTG1ErnxeHKgC86ZYGHb7vqgbNL7jq

## Resultado da inspeção

A pasta estava parcialmente desatualizada. A planilha de outubro já preservava as três tabelas atuais; o índice de setembro, a carta e o plano operacional de agosto ainda descreviam estados anteriores.

| Item | Constatação | Tratamento |
|---|---|---|
| Índice raiz | 51 registros e checkpoint de setembro tratados como correntes | Atualizado em lugar, preservando ID e URL, com referência 58/11/19 e baseline v2. |
| Planilha 08/10 | Todas as células das três tabelas coincidem com main | Snapshot preservado; comparação integral registrada e escopo parcial em relação ao v2. |
| Carta e plano de agosto | 135/843/876; caminhos canônicos antigos; release/DOI descritos como ausentes | Identificados como históricos; cópias atuais disponibilizadas de PROJECT_STATE e WORKFLOW_STATUS. |
| Dados e pacote expandido | Evidência histórica, não catálogo vivo | Preservados; três CSVs atuais disponibilizados separadamente. |
| Checkpoint Static 51 | Evidência histórica válida | Preservado; auditoria atual acrescentada. |
| GitHub | PR #284 integrado; build, QA visual e smoke passaram | Comparação e contrato de manutenção registrados neste repositório. |

## Comparação integral

Cabeçalhos, ordem, IDs e todos os valores foram comparados, normalizando somente células vazias finais omitidas pelo retorno de Sheets. Nenhum valor científico foi alterado.

- `data/data_resources.csv`: 58 linhas, 34 colunas; igualdade integral; SHA-256 `460237bb4d9d12cda556881fbc6f802765ba76d79b8900e3124758e9aa0d5ea1`.
- `data/data_products.csv`: 11 linhas, 24 colunas; igualdade integral; SHA-256 `77a62e351ea5d540393aa74bd30c16013453f428a45b0db036707763d42fb1b3`.
- `data/product_distributions.csv`: 19 linhas, 15 colunas; igualdade integral; SHA-256 `4f33e22aa650c92d79881fe9cda7e5dfa22ed75dcc4f882c4ad45edca6a3b6ea`.

O relatório JSON registra os hashes, commits, planilha e IDs dos três gates bem-sucedidos do commit-fonte. A planilha não contém as autoridades auxiliares de rotas, versões e proveniência v2; estas permanecem no GitHub.

## Continuidade

Manter QA/QC, curadoria seletiva e preservação das 58 URLs. Próxima frente: Integration Registry. API e harvesting permanecem planejados. A release v1.0.0 e DOI 10.5281/zenodo.22130831 não são alterados por esta sincronização.

## Verificação das alterações

Índice relido e arquivos confirmados nas pastas de destino. Build local, documentação ativa, rotas, versões/proveniência, páginas e compatibilidade v1/v2 passaram. O JSON registra IDs e URLs dos arquivos criados/atualizados. As alterações deste ciclo são documentais; nenhuma tabela científica canônica ou interface foi modificada.
