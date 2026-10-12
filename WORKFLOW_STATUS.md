# Estado do workflow — Vitrine Ciência

**Atualização:** 12 de outubro de 2026 (`America/Sao_Paulo`)

## Autoridade operacional

`main` no GitHub é a autoridade canônica do estado público.

Runtime corrente:

`378e3d43c71988f3c7966e33f3d4f5cb879b1443`

Gates do runtime:

- build/validação/deploy `37957241426` — PASS;
- QA visual `37957241480` — PASS;
- smoke pós-deploy `37957322300` — PASS.

## Estado publicado

- 58 registros `DR`;
- 11 produtos detalhados `DP`;
- 19 distribuições `DD`;
- 58 páginas individuais;
- read model público agregado e JSON individual por registro;
- descoberta temática/facetada;
- expansão histórica 135/843/876 preservada em quarentena.

O marco histórico `VITRINE_STATIC_51_STABLE` continua válido como checkpoint do núcleo 51, mas **não é mais a descrição suficiente do runtime público atual**. O estado público vigente é o catálogo 58 com páginas individuais.

## Estado das frentes

### A. WEB estática — OPERACIONAL

Objetivo: manter um catálogo público estável, compreensível e independente da disponibilidade de APIs externas.

Concluído:

- descoberta tema-first;
- filtros controlados;
- distinção de papéis de acesso;
- 58 páginas de registro;
- JSONs públicos;
- canonical/sitemap;
- QA estrutural e visual;
- smoke do deploy.

Próximas correções WEB:

1. simplificar os cards de `sources.html` na origem;
2. reduzir redundância entre card e página individual;
3. reorganizar a página do registro em blocos orientados ao usuário;
4. separar visualmente informação científica do recurso e curadoria da Vitrine;
5. migrar o renderer para o modelo público v2 sem alterar URLs.

### B. Modelo público v2 — PRÓXIMO MILESTONE

Status: planejado; não implementado.

Contrato alvo:

```
CatalogRecord
  └── resource
        ├── offerings
        ├── versions
        ├── access_routes
        ├── agents/provenance
        └── references
```

A página `/registros/dr####/` permanece persistente.

Critérios de aceite:

- registro e recurso separados semanticamente;
- tipo público atribuído ao recurso;
- rotas de acesso explicitamente tipadas;
- versões distinguíveis quando materialmente relevantes;
- proveniência com papéis;
- nenhuma regressão nas 58 URLs;
- geração HTML/JSON do mesmo objeto.

### C. Integration Registry — DEPOIS DO MODELO V2

Status: planejado; não iniciado em `main`.

Deverá registrar por integração:

- provedor/recurso;
- tecnologia;
- endpoint;
- autenticação;
- licença e restrições;
- forma de paginação;
- identificadores externos;
- frequência/TTL;
- estado operacional;
- prioridade de automação.

Casos piloto prioritários já estudados incluem Carbon Mapper REST/STAC, RESOLVE/Earth Engine, GSN e produtos com acesso contratado.

### D. Conectores e harvesting — FUTURO CONTROLADO

Status: não implementado.

Ordem recomendada de conectores:

1. STAC/STAC API;
2. CKAN;
3. OGC API e serviços OGC relevantes;
4. ArcGIS REST;
5. REST/GraphQL específicos;
6. fluxos manuais quando não houver API adequada.

Todo pipeline deverá seguir:

`fetch → raw/staging → normalize → deduplicate → classify → validate → diff → curation gate → publish`

Nenhum item descoberto por API entra automaticamente no catálogo público.

### E. API Vitrine — FUTURO

Status: contrato conceitual apenas.

Primeiro endpoint de leitura proposto:

`GET /api/v1/records/{resource_id}`

A API deve servir o mesmo modelo que alimenta o HTML/JSON estático.

Atualização sob demanda deverá ser assíncrona e limitada por freshness/TTL, cooldown e rate limits. Abrir uma página não deve equivaler a uma chamada obrigatória ao provedor.

## Ordem de execução recomendada

1. documentação e estado canônico — **esta atualização**;
2. `public-record-v2`;
3. simplificação dos cards e redesign das páginas;
4. rotas de acesso canônicas;
5. versões e proveniência estruturadas;
6. Integration Registry;
7. pilotos de conectores;
8. pipeline de harvesting;
9. API de leitura;
10. revalidação assíncrona e observabilidade.

## Regras que não mudam

- dados científicos permanecem, em regra, no provedor;
- a Vitrine não cria página por arquivo/asset;
- API, viewer e documentação não são automaticamente produtos científicos;
- HTTP 200 não comprova acesso a dados;
- ausência de evidência não vira “não”;
- release histórica não é reescrita;
- harvesting não publica automaticamente;
- falha externa não derruba a superfície pública.

## Documentos operacionais

- estado: `docs/PROJECT_STATE.md`;
- arquitetura WEB/API: `docs/WEB_API_EVOLUTION_PLAN.md`;
- páginas v1: `docs/PUBLIC_RECORD_PAGES_V1.md`;
- direção científica: `docs/PROJECT_SCIENTIFIC_DIRECTION.md`;
- seleção: `SELECTION_AND_COVERAGE_POLICY.md`;
- checkpoint atual: `docs/CHECKPOINT_PUBLIC_58_2026-10-09.md`.
