# Estado do workflow — Vitrine Ciência

Atualização: **2026-08-19** (`America/Sao_Paulo`)

## Direção ativa

A Vitrine Ciência é um **catálogo público, estático, versionado e delimitado para descoberta de dados científicos relevantes ao Brasil**. O modelo conceitual está estável em três unidades: fonte → produto → distribuição.

A fase corrente é de **QA/QC e manutenção**, com prioridade para disponibilidade pública, integridade canônica, correções factuais e semânticas, robustez de build/CI, documentação/citação, acessibilidade e bugs reais de UX. **A expansão de novas fontes, produtos ou distribuições está pausada** e só deve ser retomada mediante instrução humana explícita.

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
- **843 produtos**;
- **876 distribuições**;
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

### Curadoria e QA/QC

**ATIVOS, SEM EXPANSÃO DE ESCOPO.** O trabalho corrente corrige apenas o catálogo já existente: duplicatas comprovadas, metadados contraditórios, papéis de links, versões, cobertura, metodologia, licenças, citações, limitações, derivados e defeitos técnicos. Valores desconhecidos ou variáveis permanecem explícitos. Novas fontes, produtos ou distribuições não entram durante esta fase sem instrução humana explícita.

### Documentação

**ALINHADA PARA v1.0.0 E MANUTENÇÃO.** README, citação, changelog, licença da curadoria, política de release, estado do projeto, release notes e gates de DOI descrevem o snapshot científico; documentos operacionais devem refletir a fase atual de QA/QC.

### Drive

**DERIVADO / NÃO SINCRONIZADO.** O workbook histórico do Drive não representa o estado completo da release. Ele não é gate de DOI e não deve ser chamado de sincronizado até ser regenerado e comparado contra as três tabelas canônicas.

### Release e DOI

**v1.0.0 PREPARADA; DOI NÃO EMITIDO.** Qualquer criação de nova tag/release, depósito no Zenodo ou emissão/propagação de DOI requer instrução humana explícita e os gates de release aplicáveis. A manutenção corrente não deve criar nova release ou DOI automaticamente.

## Gates proporcionais ao risco

- **AUTO-SAFE:** documentação, QA/CI, correção factual inequívoca, saneamento reversível e correções de publicação/UX de baixo risco;
- **REVIEW:** mudanças públicas relevantes, lotes grandes de correções ou evidência factual materialmente ambígua;
- **HUMAN-DECISION:** mudança de escopo/schema, ação destrutiva, licença/autoria/citação oficial, tracking/privacidade, nova release/tag e DOI.

Pipeline de manutenção:

`estado vivo → defeito/risco material → evidência → correção mínima → validação → read-back → publicação quando aplicável → encerramento`

## Prioridades atuais

1. garantir disponibilidade da GitHub Pages e consistência entre commit publicado e smoke pós-deploy;
2. manter zero FKs inválidas, órfãos ou duplicatas semânticas comprovadas;
3. reduzir ambiguidades reais de metadados e papéis homepage/acesso sem fabricar diferenças;
4. eliminar referências legadas e manter identidade, citação, release e documentação coerentes;
5. fortalecer validadores e workflows, removendo gates legados, falsos positivos e flakiness;
6. corrigir bugs reais de busca, filtros, comparação, links, responsividade e acessibilidade;
7. **não expandir o catálogo** até nova decisão humana explícita.

## Fora do caminho ativo

- mapeamento de novas fontes, produtos ou distribuições;
- migração da Vitrine para PostgreSQL/PostGIS;
- Instâncias 1–3 do Simbiotrama;
- expansão obrigatória para 38 campos;
- qualquer requisito fixo de 51 fontes / 11 produtos / 19 distribuições.

Esses elementos aparecem apenas em documentação histórica anterior à separação dos projetos ou permanecem deliberadamente pausados.
