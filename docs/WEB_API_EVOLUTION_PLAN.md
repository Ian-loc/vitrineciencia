# Evolução do cliente WEB e da arquitetura API — Vitrine Ciência

**Status:** plano técnico vigente  
**Atualização:** 12 de outubro de 2026  
**Escopo:** evolução incremental do cliente GitHub Pages para um catálogo federado resiliente

## 1. Objetivo

Este documento descreve como o cliente web atual está construído, quais limitações são conhecidas e como a Vitrine deve evoluir para incorporar APIs e harvesting sem perder a estabilidade da superfície pública.

A diretriz central é:

> **o site estático continua sendo uma representação pública confiável; automação futura atualiza o estado curado, não substitui a experiência por consultas externas síncronas.**

## 2. Cliente web atual

A implementação corrente usa:

- HTML estático;
- CSS local;
- JavaScript sem framework obrigatório;
- scripts Python para geração e validação;
- GitHub Actions;
- GitHub Pages.

Fluxo atual:

```
CSV + auditorias + schemas
        ↓
build Python
        ↓
read models JSON
        ↓
HTML + assets
        ↓
_site
        ↓
GitHub Pages
```

Principais superfícies:

- Home: orientação temática;
- `sources.html`: descoberta dos 58 registros;
- `products.html`: visão do subconjunto detalhado;
- `/registros/dr####/`: representação completa de cada registro;
- páginas de análise/metodologia.

## 3. Read model já disponível

O PR #277 criou uma ponte importante para a futura API:

- `data/public_records.json`;
- `data/registros/dr####.json`;
- HTML gerado a partir do mesmo modelo.

Isso significa que a futura API não precisa inventar uma representação totalmente nova; ela pode evoluir o mesmo contrato.

## 4. Problemas ainda presentes no cliente

### 4.1 Registro e recurso parcialmente fundidos

`public-record-v1` ainda atribui tipos externos ao registro da Vitrine.

Correção: introduzir `record` e `resource` separados.

### 4.2 Cards excessivamente detalhados

`sources.html` ainda renderiza detalhes técnicos extensos.

Correção: cards devem orientar descoberta e enviar o usuário à página individual.

### 4.3 Guardrails pós-renderização

`public-interface-guardrails.js` remove informações e links técnicos depois que o card foi construído.

Correção: gerar diretamente a interface pública correta.

### 4.4 Rotas derivadas

Papéis de links ainda são inferidos de campos gerais e auditorias.

Correção: criar uma coleção canônica `access_routes`.

### 4.5 Versão não é entidade própria

`version_or_collection` está embutido no produto.

Correção: modelar versões/coleções quando necessárias à reprodutibilidade.

### 4.6 Proveniência simplificada

`owner_or_manager` comprime vários papéis.

Correção: agentes + papéis, como produtor, mantenedor, publicador, host e distribuidor.

### 4.7 Datas ambíguas

Separar:

- verificação de acesso pela Vitrine;
- atualização informada pelo provedor;
- alteração do registro da Vitrine;
- data/versão do produto.

## 5. Modelo público v2

Estrutura recomendada:

```
record
  id
  status
  created_at
  updated_at
  verified_at

resource
  name
  acronym
  type
  description
  themes
  scope

offerings[]
  id
  type
  name
  description
  spatial
  temporal
  methodology
  limitations

versions[]
  id
  offering_id
  label
  issued
  relation
  status

access_routes[]
  id
  target_type
  target_id
  type
  url
  protocol
  format
  auth
  access_conditions
  license
  verified_at

agents[]
  id
  name
  role

references[]
  type
  title
  url
  doi

curation
  evidence
  notes
  status
```

Esse é um modelo lógico; não implica imediatamente novas tabelas relacionais.

## 5.1 Estado material da migração

A implementação inicial gera, em paralelo:

- `/data/v2/public_records.json`;
- `/data/v2/registros/dr####.json`.

O HTML continua no v1 até que a equivalência funcional e os novos blocos públicos sejam validados.

O crosswalk e seus invariantes estão em `docs/PUBLIC_RECORD_V2_MIGRATION.md`.

## 6. Interface após o v2

### Cards

Devem mostrar apenas informação suficiente para decidir se o registro merece ser aberto.

### Página individual

Deve concentrar interpretação, produtos e acesso.

### Página do provedor

Continua sendo autoridade para documentação operacional completa e dados originais.

A Vitrine deve agregar valor por comparação, organização e curadoria, não por duplicação.

## 7. Integration Registry

O Integration Registry é a camada que conecta recurso curado a mecanismo de atualização.

Campos mínimos:

- integration_id;
- record/resource alvo;
- provider;
- connector_type;
- endpoint;
- docs_url;
- authentication_type;
- credentials_scope;
- license_scope;
- redistribution_policy;
- rate_limit;
- pagination;
- external_id strategy;
- version semantics;
- freshness_ttl;
- last_success;
- last_failure;
- enabled;
- curation mode.

Ele deve existir antes dos conectores entrarem em produção.

## 8. Conectores

Ordem proposta:

### STAC

Para coleções e itens espaço-temporais.

### CKAN

Para catálogos com datasets/resources estruturados.

### OGC

OGC API e, quando necessário, serviços legados WMS/WFS/WCS/CSW.

### ArcGIS REST

Para Feature Services e catálogos institucionais.

### REST/GraphQL específicos

Exemplo: Carbon Mapper e outros provedores com contratos próprios.

### Manual/static

Fontes sem API adequada continuam válidas e são curadas manualmente.

## 9. Pipeline de harvesting

```
fetch
  ↓
raw immutable
  ↓
staging
  ↓
normalize
  ↓
deduplicate
  ↓
classify
  ↓
verify access
  ↓
compare/diff
  ↓
curation decision
  ↓
accepted snapshot
  ↓
build/publication
```

Objetos operacionais futuros recomendados:

- `HarvestRun`;
- `AccessCheck`;
- `CurationDecision`.

Eles não fazem parte do runtime atual.

## 10. API Vitrine

Primeira função da API: servir o mesmo objeto público usado pelo site.

Endpoint conceitual:

`GET /api/v1/records/{resource_id}`

Possíveis endpoints posteriores:

- consulta de freshness;
- histórico de versões;
- status de integração;
- solicitação de refresh.

A API administrativa de refresh não deve ser confundida com o endpoint público de leitura.

## 11. Revalidação por acesso

Abrir uma página pode futuramente sinalizar interesse e iniciar revalidação apenas quando:

- TTL expirou;
- integração está habilitada;
- não existe job equivalente recente;
- rate limits permitem;
- política do provedor autoriza.

Nunca:

`1 page view = 1 request externo obrigatório`.

## 12. Resiliência

Em caso de falha externa:

- página permanece disponível;
- snapshot anterior permanece legível;
- falha é registrada;
- estado de acesso pode ser reavaliado;
- atualização é tentada posteriormente.

Esse comportamento é requisito, não otimização.

## 13. Backend

GitHub Pages continua suficiente para a leitura estática.

Para refresh/harvesting futuro será necessária uma camada computacional separada, possivelmente serverless ou serviço leve.

A tecnologia ainda **não está escolhida**.

PostgreSQL/PostGIS não é pré-requisito para o próximo passo.

## 14. Protótipo de explorador federado

A branch `agent/federated-explorer-mvp` implementou composição visual WMS/WMTS com MapLibre.

Estado:

- experimental;
- muito atrás de `main`;
- não integrado;
- não é API da Vitrine;
- não deve ser mergeado.

Ideias reaproveitáveis:

- manifesto de proveniência;
- estado compartilhável;
- aviso de compatibilidade;
- falha por camada;
- separação entre composição visual e harmonização analítica.

## 15. Ordem de implementação

### M0 — documentação e baseline — CONCLUÍDO

Documentação sincronizada ao runtime 58 e checkpoint factual registrado.

### M1 — `public-record-v2` — EM EXECUÇÃO

Primeira etapa concluída: read model v2 paralelo ao v1, com separação `record → resource`, crosswalk determinístico e validação de compatibilidade.

Próxima etapa M1: migrar o renderer HTML para consumir o v2, mantendo v1 temporariamente como referência de regressão.

### M2 — cards e página individual

Simplificar descoberta e reorganizar ficha.

### M3 — rotas canônicas

Transformar links em objetos explícitos.

### M4 — versões e proveniência

Estruturar versão/coleção e agentes/papéis.

### M5 — Integration Registry

Classificar integrações dos registros prioritários.

### M6 — conectores piloto

STAC + um segundo padrão + um caso proprietário.

### M7 — pipeline

Implementar raw/staging/normalize/diff/gates.

### M8 — API de leitura

Servir read model.

### M9 — revalidação assíncrona

Freshness, queue, retries e observabilidade.

## 16. Critérios para avançar para M5

Não iniciar federação operacional antes de:

- modelo v2 validado;
- rotas de acesso separadas;
- IDs e relações estáveis;
- política de versionamento suficiente;
- proveniência mínima estruturada;
- testes de compatibilidade v1→v2;
- zero regressão nas URLs públicas.

## 17. Não objetivos

A evolução não deve:

- transformar a Vitrine em data lake;
- consultar todos os provedores em tempo real a cada busca;
- publicar automaticamente tudo que uma API retorna;
- criar páginas por asset;
- tratar API como produto científico;
- exigir backend para que a página atual funcione;
- forçar todos os provedores ao mesmo protocolo.

## 18. Resultado esperado

A arquitetura final deve permitir que a mesma entidade curada seja:

- encontrada na interface;
- representada em HTML;
- serializada em JSON;
- servida por API;
- atualizada por conectores;
- reconstruída a partir de evidência e logs;

sem que a disponibilidade pública dependa das APIs externas.
