# Estado do workflow — Vitrine Ciência

Atualização: **2026-08-19** (`America/Sao_Paulo`)

## Direção ativa

A Vitrine Ciência é um **catálogo público, estático, versionado e delimitado para descoberta de dados científicos relevantes ao Brasil**. O modelo conceitual está estável em três unidades: fonte → produto → distribuição. O trabalho corrente prioriza crescimento de conteúdo, precisão factual, qualidade de metadados, usabilidade e releases reproduzíveis.

## Autoridade

- repositório: `Ian-loc/vitrineciencia`;
- branch canônica de desenvolvimento: `main`;
- branch de preparação da primeira release estável: `release/v1.0.0`;
- site: `https://ian-loc.github.io/vitrineciencia/`;
- fontes: `data/data_resources.csv`;
- produtos: `data/data_products.csv`;
- distribuições: `data/product_distributions.csv`;
- Drive: espelho/histórico derivado, não canônico;
- versão de citação candidata: `1.0.0`.

## Snapshot candidato v1.0.0

Em 19/08/2026:

- **135 fontes**;
- **833 produtos**;
- **866 distribuições**;
- os maiores identificadores correntes são `DR0135`, `DP000861` e `DD000894`; lacunas de IDs são preservadas e não recicladas;
- `data_quality_report.json`: 135 registros de fonte; verificação máxima `2026-08-19`;
- incertezas de acesso/licença permanecem registradas explicitamente e são sinais de curadoria, não falhas estruturais.

As contagens caracterizam o snapshot candidato e não são gates de arquitetura.

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

**ATIVA.** Novas fontes e produtos podem entrar em pequenos lotes na `main` quando possuem identidade rastreável, relevância para o Brasil, evidência oficial suficiente e representação honesta no contrato vigente. Valores desconhecidos ou variáveis permanecem explícitos. Depois da tag `v1.0.0`, novas mudanças pertencem a releases posteriores e não alteram retroativamente o snapshot publicado.

### Documentação

**ALINHADA PARA v1.0.0.** README, citação, changelog, licença da curadoria, política de release, estado do projeto, release notes e gates de DOI foram atualizados para o snapshot candidato de 19/08/2026.

### Drive

**DERIVADO / NÃO SINCRONIZADO.** O workbook histórico do Drive não representa o estado completo da release. Ele não é gate de DOI e não deve ser chamado de sincronizado até ser regenerado e comparado contra as três tabelas canônicas.

### Release e DOI

**RELEASE v1.0.0 EM PREPARAÇÃO FORMAL.** A branch `release/v1.0.0` contém a documentação do primeiro snapshot científico estável. A publicação definitiva exige validação final, integração na `main`, tag Git imutável `v1.0.0`, GitHub Release, pacote de depósito inspecionado e Zenodo Dataset. O DOI ainda não foi emitido.

## Gates proporcionais ao risco

- **AUTO-SAFE:** documentação, QA/CI, correção factual inequívoca, inclusão pequena dentro do contrato e saneamento reversível;
- **REVIEW:** lotes grandes, mudança pública relevante ou evidência factual materialmente ambígua;
- **HUMAN-DECISION:** mudança de escopo/schema, ação destrutiva, licença/autoria/citação oficial, tracking/privacidade, release `1.0.0` e DOI.

A decisão humana de preparar `v1.0.0` foi registrada em 19/08/2026. A emissão do DOI continua condicionada aos gates objetivos.

Pipeline:

`scope → evidence → implementation → validation → diff audit → public validation when relevant → integration → post-merge verification → release/tag → deposit → DOI propagation`

## Prioridades atuais

1. concluir CI e auditoria do diff da PR de `v1.0.0`;
2. garantir que nenhum dado científico canônico tenha sido alterado inadvertidamente pela preparação da release;
3. materializar e inspecionar o pacote Zenodo do commit final;
4. criar tag/release GitHub `v1.0.0` após integração;
5. depositar como **Dataset** no Zenodo;
6. incorporar o DOI ao repositório e perfis após emissão;
7. retomar a expansão Brasil-primeiro na `main` em versões posteriores.

## Fora do caminho ativo

- migração da Vitrine para PostgreSQL/PostGIS;
- Instâncias 1–3 do Simbiotrama;
- expansão obrigatória para 38 campos;
- qualquer requisito fixo de 51 fontes / 11 produtos / 19 distribuições.

Esses elementos aparecem apenas em documentação histórica anterior à separação dos projetos.
