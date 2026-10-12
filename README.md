# Vitrine Ciência

**Catálogo científico curado para descobrir, compreender e acessar dados relevantes aos socioecossistemas brasileiros.**

Site público: https://ian-loc.github.io/vitrineciencia/  
Repositório canônico: https://github.com/Ian-loc/vitrineciencia

## Estado público atual — 12 de outubro de 2026

A autoridade canônica é o repositório `Ian-loc/vitrineciencia`; a branch `main` representa o estado público corrente. Planilhas, Drive, worktrees, documentos externos e conversas são auxiliares ou espelhos e não substituem o estado materializado no GitHub.

O estado público corrente é o `HEAD` validado de `main`. Checkpoints históricos preservam SHAs específicos; o README não fixa o head móvel do projeto.

Esse estado contém:

- **58 registros públicos `DR####`**;
- **11 produtos detalhados `DP######`**;
- **19 distribuições `DD######`**;
- **58 páginas individuais** em `/registros/dr####/`;
- read model v2 em `/data/v2/public_records.json` e JSON individual por registro;
- read model v1 mantido temporariamente em `/data/public_records.json` para compatibilidade;
- descoberta pública por fenômeno/processo, território, tipo de informação e forma de acesso;
- build estático, QA visual e smoke pós-deploy automatizados.

Mudanças públicas são aceitas somente após build/validação, QA visual quando aplicável e smoke pós-deploy. O checkpoint anterior ao modelo v2 está em `docs/CHECKPOINT_PUBLIC_58_2026-10-09.md`.

O núcleo histórico `DR0001–DR0051` permanece preservado e semanticamente auditado. As sete entradas pós-core atuais são `DR0136–DR0142`. A expansão histórica **135/843/876** continua preservada em `data/quarantine/v1.0.0-expanded/` e não retorna automaticamente à superfície pública.

## O que a Vitrine é hoje

A Vitrine é uma **camada de descoberta, curadoria e encaminhamento**. Ela não pretende copiar integralmente os catálogos externos nem hospedar todos os arquivos científicos.

A experiência pública segue, em termos funcionais:

**pergunta científica → fenômeno/processo/território/tipo de informação → registro da Vitrine → dados/produtos descritos quando existentes → forma de acesso → provedor/proveniência → documentação**

A unidade pública persistente é o **Registro da Vitrine** (`DR####`). Cada registro agrega as informações que a Vitrine conhece sobre um recurso externo, seus produtos, coleções, versões, distribuições, serviços, visualizadores e documentos, sem criar automaticamente uma nova página para cada item técnico.

O contrato público corrente é `schema/public-record-v2.json`. Ele separa explicitamente o **Registro da Vitrine** do **Recurso catalogado** descrito por esse registro. O v1 permanece temporariamente publicado como camada de compatibilidade e regressão.

## Dados e autoridades materiais

O schema físico legado permanece:

```
DR####  →  DP######  →  DD######
registro    produto      distribuição
```

Esse arranjo existe para compatibilidade, rastreabilidade e reprodução; não é a ontologia final do projeto.

As principais autoridades materiais são:

- `data/data_resources.csv`;
- `data/data_products.csv`;
- `data/product_distributions.csv`;
- `data/static_core_51_progress.json` — tipagem semântica do núcleo 51;
- `data/static_core_51_access_audit.json` — acesso A–E do núcleo;
- `data/post_core_access_audit.json` — acesso A–E das sete entradas pós-core;
- `data/brazil_scope_priorities.json` — papel territorial;
- `data/applied_priority_gate.json` — casos aplicados P1–P6;
- scripts de build e validação.

No conjunto vivo de 58 registros, a classificação da rota principal é atualmente **A=2, B=39, C=0, D=14, E=3**. Isso não mede qualidade científica; descreve o tipo de acesso principal verificado. Serviços programáticos secundários podem existir mesmo quando a rota principal é B ou D.

A prioridade territorial corrente é **P0=18, P1=24, P2=14, P3=2**.

## Cliente web atual

O cliente público é deliberadamente simples:

- HTML, CSS e JavaScript estáticos;
- geração e validação em Python;
- publicação por GitHub Pages;
- GitHub Actions para build, QA visual e smoke;
- sem framework frontend obrigatório;
- sem backend necessário para leitura;
- conteúdo essencial das páginas de registro disponível sem depender de APIs externas.

As superfícies principais são:

- `index.html` — entrada e orientação temática;
- `sources.html` — descoberta dos 58 registros;
- `products.html` — subconjunto de 11 itens detalhados e 19 distribuições;
- `/registros/dr####/` — página persistente de cada registro;
- `analytics.html` e páginas auxiliares — composição e método do acervo.

A existência das páginas individuais torna desnecessário manter toda a ficha técnica dentro dos cards de resultados. A simplificação desses cards é parte do próximo ciclo de interface.

## Evolução planejada: modelo público v2 e API

O modelo público v2 e o renderer das páginas individuais já estão implementados. A estrutura lógica corrente é:

**Registro da Vitrine → Recurso catalogado → oferta científica → versão/coleção → forma de acesso**

com proveniência, evidência e curadoria como dimensões transversais.

A próxima etapa da WEB é simplificar os cards de descoberta e, depois, tornar as rotas de acesso canônicas. A federação seguirá o princípio:

**federado na origem; indexado localmente na descoberta; descentralizado no acesso aos dados**.

O comportamento planejado é **static-first / stale-while-revalidate**:

1. HTML e JSON estáticos respondem imediatamente;
2. uma camada futura avalia a atualidade do registro;
3. se necessário, agenda atualização assíncrona no provedor;
4. respostas externas entram em staging e normalização;
5. validação, comparação e curadoria antecedem qualquer promoção;
6. falha externa nunca impede a leitura do snapshot público.

Um endpoint futuro conceitual é `GET /api/v1/records/{resource_id}`. Ele **não está implementado em produção**.

Também não estão implementados em `main`: Integration Registry executável, harvesting automático, conectores STAC/CKAN/OGC/REST/GraphQL, fila de refresh, `HarvestRun`, `AccessCheck`, `CurationDecision`, backend serverless ou PostgreSQL.

O planejamento corrente está consolidado em `docs/WEB_API_EVOLUTION_PLAN.md`.

## Release científica v1.0.0

A release histórica permanece imutável e reproduzível:

- GitHub Release: https://github.com/Ian-loc/vitrineciencia/releases/tag/v1.0.0
- Zenodo: https://zenodo.org/records/22130831
- DOI: https://doi.org/10.5281/zenodo.22130831
- commit congelado: `27c545554f406b940662777e3f053e939ef3588c`

A release histórica não representa automaticamente o catálogo vivo atual.

## Documentação canônica

- estado material: `docs/PROJECT_STATE.md`;
- execução e próximos gates: `WORKFLOW_STATUS.md`;
- modelo operacional: `docs/VITRINE_OPERATING_MODEL.md`;
- direção científica: `docs/PROJECT_SCIENTIFIC_DIRECTION.md`;
- política de seleção: `SELECTION_AND_COVERAGE_POLICY.md`;
- páginas públicas v1: `docs/PUBLIC_RECORD_PAGES_V1.md`;
- evolução WEB/API: `docs/WEB_API_EVOLUTION_PLAN.md`;
- checkpoint público atual: `docs/CHECKPOINT_PUBLIC_58_2026-10-09.md`;
- dicionário de dados: `CODEBOOK.md`.

Código: MIT. Metadados e curadoria original: CC BY 4.0.

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. Version 1.0.0. Zenodo, 2026. https://doi.org/10.5281/zenodo.22130831
