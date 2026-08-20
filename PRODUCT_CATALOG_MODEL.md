# Modelo do catálogo de produtos — Vitrine Ciência

## 1. Decisão vigente

A Vitrine usa um modelo deliberadamente simples e estável:

```text
Fonte (DR####)
  1 ─── N Produto (DP######)
              1 ─── N Distribuição (DD######)
```

Esse modelo é a arquitetura **canônica da Vitrine atual**. Não existe obrigação de promover a Vitrine para PostgreSQL/PostGIS ou para a antiga hierarquia relacional do Simbiotrama.

## 2. Fonte

Responde principalmente:

- quem mantém ou organiza o acesso;
- qual é a infraestrutura/plataforma;
- qual sua função institucional;
- quais tipos gerais de conteúdo oferece;
- qual a cobertura geral;
- como localizar os dados.

Uma fonte não deve ser duplicada apenas porque possui várias coleções, páginas ou endpoints.

## 3. Produto

Responde:

- qual oferta informacional materialmente distinta existe;
- o que ela representa ou permite descobrir;
- qual cobertura e suporte são relevantes;
- qual coleção/versão está sendo descrita quando necessário;
- qual sua natureza (`product_kind` e `primary_or_derived`);
- quais limitações condicionam interpretação;
- como chegar às distribuições.

Um produto pode ser dataset, série, catálogo, serviço, família de indicadores, coleção de camadas ou saída de software quando essa unidade melhora materialmente a descoberta.

## 4. Distribuição

Descreve uma rota concreta de acesso ao produto:

- download;
- API;
- serviço OGC/STAC;
- catálogo;
- aplicação web;
- outro mecanismo verificável.

Pertencem à distribuição: URL, formato, protocolo, ferramenta, gratuidade, autenticação, condições, licença/atribuição, suporte a recorte e notas operacionais.

## 5. Granularidade

Criar produto separado apenas quando houver diferença relevante de:

- finalidade/conteúdo;
- método ou natureza de produção;
- cobertura espacial/temporal;
- suporte/resolução;
- coleção/versão cientificamente significativa;
- condição ou caminho de acesso que mude materialmente o objeto descoberto.

Não criar produto apenas por existir:

- outro arquivo;
- banda;
- tile;
- formato;
- endpoint técnico equivalente;
- página de download alternativa.

## 6. Catálogos e serviços

A Vitrine pode registrar catálogos e serviços como produtos quando são ofertas materialmente distintas e classificadas honestamente. Isso **não significa** que um catálogo ou API seja observação científica. `product_kind`, descrição e limitações devem explicitar sua natureza.

Catálogos amplos usam `enumeration_scope=external_index`; a Vitrine não deve copiar integralmente megacatálogos.

## 7. Espaço e tempo

Produto deve separar, tanto quanto o contrato permite:

- cobertura geográfica;
- suporte espacial;
- resolução espacial;
- cobertura temporal;
- resolução temporal;
- frequência de atualização.

Zoom da interface não define resolução; data de atualização da página não define necessariamente a temporalidade do dado.

## 8. Origem e derivação

`primary_or_derived` distingue `primário`, `derivado`, `agregador`, `serviço`, `misto` e `desconhecido`. Essa classificação é semântica e não um julgamento de qualidade.

## 9. Versão

O modelo corrente não possui entidade `release` independente. Versão/coleção pertinente é registrada em `version_or_collection`. Quando uma plataforma tem histórico complexo, a Vitrine pode registrar o produto em nível de família/coleção e direcionar o usuário ao índice externo em vez de normalizar cada release.

## 10. Variáveis

Variáveis normalizadas permanecem **deferred** no contrato `product-catalog-v0.1`. A necessidade de uma tabela de variáveis deve ser demonstrada por ganho real de descoberta e não pela mera existência de bandas/colunas nos datasets externos.

## 11. Relação com a arquitetura histórica

Documentos antigos deste repositório descrevem organização → fonte → família → produto → release → distribuição → ativo e banco PostgreSQL/PostGIS. Essa arquitetura pertence à fase pré-separação/Simbiotrama e é preservada por proveniência. Não é modelo ativo da Vitrine.

## 12. Estado corrente

Este documento define o **modelo**, não replica contagens voláteis do catálogo. O estado quantitativo corrente deve ser lido em `docs/PROJECT_STATE.md` e `data/data_quality_report.json`, ambos validados contra as tabelas canônicas. Lacunas históricas de IDs são preservadas e IDs não são reciclados.