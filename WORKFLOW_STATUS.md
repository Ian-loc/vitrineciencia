# Estado do workflow — Vitrine Ciência

Atualização: **2026-08-18** (`America/Sao_Paulo`)

## Direção ativa

A Vitrine Ciência é um **catálogo público, estático e delimitado para descoberta de dados científicos relevantes ao Brasil**. O modelo conceitual está estável em três unidades: fonte → produto → distribuição. O trabalho corrente prioriza crescimento de conteúdo, precisão factual, qualidade de metadados, usabilidade e preparação de releases reproduzíveis.

## Autoridade

- repositório: `Ian-loc/vitrineciencia`;
- branch: `main`;
- site: `https://ian-loc.github.io/vitrineciencia/`;
- fontes: `data/data_resources.csv`;
- produtos: `data/data_products.csv`;
- distribuições: `data/product_distributions.csv`;
- Drive: espelho/histórico derivado, não canônico;
- versão de citação: `unreleased` até release explícita.

## Snapshot corrente

Em 18/08/2026:

- **125 fontes**;
- **752 produtos**;
- **783 distribuições**;
- os maiores identificadores correntes são `DR0125`, `DP000756` e `DD000787`; lacunas de IDs são preservadas e não recicladas;
- `data_quality_report.json`: 125 registros de fonte; verificação máxima `2026-08-18`;
- incerteza de acesso registrada em 72 fontes e de licença em 49 fontes — sinais de curadoria pendente, não falhas estruturais.

As contagens são observacionais e podem crescer; não são gates de arquitetura.

## Estado consolidado

### Produto e publicação

**CONSOLIDADO.** A Vitrine opera como GitHub Pages independente, com build isolado em `_site`, validação pré-publicação e smoke pós-deploy. O artefato público não depende do Simbiotrama, PostgreSQL/PostGIS ou materiais internos de auditoria.

### Modelo de dados

**CONSOLIDADO / ESTÁVEL.** Contrato vigente:

- fonte: 34 campos, ID `DR####`;
- produto: 24 campos, ID `DP######`;
- distribuição: 15 campos, ID `DD######`;
- relações obrigatórias `produto → fonte` e `distribuição → produto`;
- classificação Brasil P0–P3 vinculada por `resource_id`.

### Curadoria

**ATIVA.** Novas fontes e produtos podem entrar em pequenos lotes quando possuem identidade rastreável, relevância para o Brasil, evidência oficial suficiente e representação honesta no contrato vigente. Valores desconhecidos ou variáveis permanecem explícitos.

### Documentação

**EM ALINHAMENTO NESTE PACOTE.** Documentos que ainda descreviam o antigo estágio de 51 fontes, a migração 0.8/38 campos ou o PostgreSQL/PostGIS como destino da Vitrine estão sendo substituídos por documentação compatível com o produto atual. Arquitetura relacional do Simbiotrama permanece apenas como histórico/proveniência neste repositório.

### Drive

**DERIVADO / NÃO SINCRONIZADO.** O workbook histórico do Drive não representa o estado completo de `main`. Ele não deve ser chamado de sincronizado até ser regenerado e comparado contra as três tabelas canônicas do snapshot-fonte.

### Release e DOI

**NÃO LANÇADO.** A Vitrine ainda não possui uma release científica congelada com DOI. O caminho previsto é GitHub tag/release + snapshot reproduzível + depósito Dataset no Zenodo, após os gates objetivos de `FINAL_OBJECTIVES_AND_DOI_GATES.md` e decisão humana de publicação.

## Gates proporcionais ao risco

- **AUTO-SAFE:** documentação, QA/CI, correção factual inequívoca, inclusão pequena dentro do contrato e saneamento reversível;
- **REVIEW:** lotes grandes, mudança pública relevante ou evidência factual materialmente ambígua;
- **HUMAN-DECISION:** mudança de escopo/schema, ação destrutiva, licença/autoria/citação oficial, tracking/privacidade, release `1.0.0` e DOI.

Pipeline:

`scope → evidence → implementation → validation → diff audit → public validation when relevant → integration → post-merge verification → consolidation`

## Prioridades atuais

1. manter a documentação ativa sincronizada com o catálogo real;
2. continuar expansão Brasil-primeiro em lotes auditados;
3. reduzir incertezas materiais de licença, acesso, resolução e cobertura sem inventar valores;
4. revisar duplicidades/identidades quando puderem alterar a descoberta;
5. preservar CI, smoke pós-deploy e QA visual proporcional ao risco;
6. preparar uma release estável e citável quando o snapshot estiver tecnicamente defensável;
7. regenerar o espelho do Drive quando isso trouxer utilidade operacional, sem bloquear a release.

## Fora do caminho ativo

- migração da Vitrine para PostgreSQL/PostGIS;
- Instâncias 1–3 do Simbiotrama;
- expansão obrigatória para 38 campos;
- qualquer requisito fixo de 51 fontes / 11 produtos / 19 distribuições.

Esses elementos aparecem apenas em documentação histórica anterior à separação dos projetos.
