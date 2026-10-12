# Estado do workflow — Vitrine Ciência

**Atualização:** 12 de outubro de 2026 (`America/Sao_Paulo`)

## Autoridade operacional

`main` no GitHub é a autoridade canônica do estado público.

Runtime corrente: `HEAD` validado de `main`. O checkpoint público 58 anterior ao v2 está preservado em `docs/CHECKPOINT_PUBLIC_58_2026-10-09.md`.

## Estado publicado

- 58 registros `DR`;
- 11 produtos detalhados `DP`;
- 19 distribuições `DD`;
- na terminologia física dos validadores: **58 fontes, 11 produtos e 19 distribuições**;
- 58 páginas individuais;
- read model público agregado e JSON individual por registro;
- descoberta temática/facetada;
- expansão histórica 135/843/876 preservada em quarentena.

O marco histórico `VITRINE_STATIC_51_STABLE` continua válido como checkpoint do núcleo 51, mas **não é mais a descrição suficiente do runtime público atual**. O estado público vigente é o catálogo 58 com páginas individuais.

A fase ativa é de **QA/QC e manutenção do catálogo publicado**, combinada ao desenho do modelo v2. A expansão automática/em lote permanece **pausada**; inclusões pontuais exigem instrução humana explícita e gate curatorial.

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

Concluído no ciclo WEB v2:

- cards de `sources.html` simplificados na origem;
- redundância entre card e página individual reduzida;
- página do registro organizada em cinco blocos;
- informação científica do recurso separada visualmente da curadoria;
- renderer migrado para o modelo público v2 sem alterar URLs.

Próxima correção WEB/contrato: rotas de acesso canônicas.

### B. Modelo público v2 — MILESTONE ATIVO

Status: **read model v2 e renderer HTML v2 implementados; v1 preservado como compatibilidade temporária**.

Concluído nesta primeira etapa:

- `schema/public-record-v2.json`;
- transformação determinística v1→v2;
- `record` e `resource` separados;
- 11 produtos migrados para `offerings`;
- 19 distribuições preservadas como `access_routes`;
- versões legadas explicitamente marcadas como derivadas;
- agente legado migrado conservadoramente;
- validador de compatibilidade v1/v2;
- publicação paralela dos JSONs v2;
- renderer HTML baseado no v2;
- cinco blocos públicos nas 58 páginas;
- tipo público atribuído explicitamente ao recurso, não ao DR.

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

1. documentação e estado canônico — **concluído**;
2. read model `public-record-v2` paralelo — **concluído**;
3. renderer v2 e estrutura de cinco blocos — **concluído**;
4. simplificar cards e eliminar redundância/guardrails desnecessários — **concluído**;
5. rotas de acesso canônicas — **próxima ação**;
6. versões e proveniência estruturadas;
7. Integration Registry;
8. pilotos de conectores;
9. pipeline de harvesting;
10. API de leitura;
11. revalidação assíncrona e observabilidade.

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
