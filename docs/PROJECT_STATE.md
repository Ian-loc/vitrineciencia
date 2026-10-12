# Estado canônico — Vitrine Ciência

**Data de referência:** 12 de outubro de 2026  
**Fuso:** `America/Sao_Paulo`

## 1. Autoridade e estado material

O repositório `Ian-loc/vitrineciencia` é a autoridade canônica. A branch `main` representa o estado público corrente. Drive, planilhas, worktrees, handoffs e conversas são auxiliares ou espelhos e não substituem o que está materializado e validado no GitHub.

O runtime público corrente é sempre o `HEAD` validado da branch `main`. O checkpoint factual anterior ao modelo v2 permanece registrado em `docs/CHECKPOINT_PUBLIC_58_2026-10-09.md`; SHAs de checkpoints não devem ser confundidos com o head móvel do projeto.

Toda mudança de interface precisa passar por build/validação, QA visual quando aplicável e smoke pós-deploy.

Não há uma migração de backend em andamento no estado público. O site continua sendo um artefato estático publicado por GitHub Pages.

A **fase ativa de QA/QC e manutenção** continua vigente para o runtime 58, em paralelo ao desenho do modelo público v2. A expansão automática ou em lote permanece **pausada**; novas entradas só podem ser incorporadas por decisão curatorial e instrução humana explícita.

## 2. Catálogo vivo

O estado vivo contém:

- **58 registros `DR####`**;
- **11 produtos detalhados `DP######`**;
- **19 distribuições `DD######`**;

Na terminologia física usada pelos validadores, o catálogo corrente corresponde a **58 fontes, 11 produtos e 19 distribuições**; “fonte” é um rótulo legado do schema físico.
- 58 páginas individuais em `/registros/dr####/`;
- `data/public_records.json`;
- 58 JSONs individuais em `data/registros/dr####.json`.

O núcleo histórico `DR0001–DR0051` permanece preservado. As entradas pós-core são:

- `DR0136` — REDEMET;
- `DR0137` — RESOLVE Ecoregions 2017;
- `DR0138` — Global Safety Net GSN3.1;
- `DR0139` — Carbon Mapper;
- `DR0140` — Global Human Modification v3;
- `DR0141` — Planet Forest Carbon;
- `DR0142` — Climate Finance Tracker, mantido como referência comparativa sem cobertura brasileira.

Os IDs `DR0052–DR0135` permanecem associados ao snapshot histórico v1.0.0 em quarentena e não devem ser reciclados.

A expansão histórica **135/843/876** está em `data/quarantine/v1.0.0-expanded/` e não faz parte do catálogo vivo.

## 3. Auditorias e cobertura

A tipagem semântica detalhada do núcleo está em `data/static_core_51_progress.json` e cobre 51/51 registros históricos.

A classificação da rota principal do núcleo é:

- A=1;
- B=38;
- C=0;
- D=10;
- E=2.

A auditoria pós-core, em `data/post_core_access_audit.json`, registra:

- A=1;
- B=1;
- C=0;
- D=4;
- E=1.

No catálogo vivo completo de 58 registros, portanto:

**A=2, B=39, C=0, D=14, E=3.**

A classe descreve a rota principal verificada e não exclui serviços técnicos secundários. Carbon Mapper, por exemplo, pode ter visualizador como rota pública principal e REST/STAC como capacidades complementares.

A classificação territorial corrente em `data/brazil_scope_priorities.json` é:

- P0 — fonte brasileira: 18;
- P1 — cobertura sistemática do Brasil: 24;
- P2 — cobertura parcial/indireta: 14;
- P3 — referência comparativa: 2.

## 4. Modelo físico e modelo público

O modelo físico legado permanece:

```
DR#### 1 ─── N DP###### 1 ─── N DD######
```

Ele existe para compatibilidade, IDs e rastreabilidade; não é a ontologia final.

O HTML das páginas individuais é gerado pelo `public-record-v2`, mantendo `DR####` como unidade de navegação persistente.

O v2 é publicado como:

- `/data/v2/public_records.json`;
- `/data/v2/registros/dr####.json`;
- `/registros/dr####/` — representação HTML humana do mesmo modelo.

O v2 separa `record` e `resource`, preserva as URLs, migra os produtos atuais para `offerings` e preserva as distribuições como rotas direcionadas às ofertas. O v1 continua publicado em JSON como camada de compatibilidade e regressão durante a transição.

A página de um registro agrega, quando disponíveis:

- identidade e descrição;
- temas;
- cobertura;
- condições de acesso;
- rotas;
- produtos;
- distribuições;
- limitações;
- proveniência;
- licença;
- referências;
- dados de curadoria.

A decisão de não criar página para cada arquivo, endpoint, asset ou versão permanece vigente.

## 5. Separação registro–recurso

O v2 materializa:

```
Registro da Vitrine
        │ descreve
        ▼
Recurso catalogado
```

`DR####` identifica o registro mantido pela Vitrine. Tipos como iniciativa, plataforma, catálogo, base ou rede pertencem ao recurso catalogado. As 58 URLs foram preservadas.

## 6. Cliente web

O cliente público corrente usa HTML, CSS e JavaScript estáticos e é montado por scripts Python.

Características atuais:

- GitHub Pages como hosting;
- GitHub Actions para validação e publicação;
- conteúdo essencial das páginas de registro pré-renderizado;
- JavaScript usado para filtros, refinamentos e melhoria progressiva;
- `sources.html` como superfície principal de descoberta;
- `products.html` como subconjunto detalhado;
- uma página por registro;
- JSONs públicos derivados do mesmo read model.

Dívidas técnicas reconhecidas:

- cards de descoberta ainda contêm detalhes extensos que se tornaram redundantes após a criação das páginas individuais;
- `public-interface-guardrails.js` remove parte do conteúdo técnico após renderização; a solução futura deve simplificar o card na origem;
- as rotas públicas ainda são majoritariamente derivadas de campos de URL e auditorias, não uma entidade canônica própria;
- versões/coleções ainda estão embutidas no produto;
- proveniência ainda é simplificada em campos como `owner_or_manager`;
- datas de revisão da Vitrine e atualização informada pelo provedor ainda não estão plenamente separadas.

## 7. Estado da via API/federação

A federação é **planejada, mas não implementada em produção**.

Já está materializado:

- read model JSON por registro;
- contrato de persistência das URLs;
- princípio `static-first / stale-while-revalidate`;
- documentação de pipeline futuro;
- casos de estudo com REST/STAC, acesso contratado, visualizadores e downloads;
- planejamento no Linear, principalmente `MEI-18`.

Ainda não existe em `main`:

- API pública da Vitrine;
- Integration Registry executável;
- conectores ativos;
- harvesting automático;
- refresh acionado por visita;
- fila/worker;
- staging operacional;
- `HarvestRun`, `AccessCheck` ou `CurationDecision` executáveis;
- banco de dados próprio necessário ao runtime.

O endpoint `GET /api/v1/records/{resource_id}` é uma proposta de contrato, não um endpoint disponível.

## 8. Arquitetura alvo

A evolução deverá manter o site estático como superfície resiliente e introduzir automação por etapas:

```
provedores externos
        ↓
Integration Registry
        ↓
conectores / harvesting
        ↓
raw + staging
        ↓
normalização
        ↓
deduplicação + classificação
        ↓
validação / diff / curadoria
        ↓
snapshot público
        ↓
JSON + HTML estático
        ↓
usuário
```

Uma API futura pode servir o mesmo read model e solicitar revalidação assíncrona, mas a leitura pública nunca deve depender de uma chamada em tempo real ao provedor externo.

## 9. Branch experimental antiga

A branch `agent/federated-explorer-mvp` contém um protótipo cartográfico de composição visual WMS/WMTS com MapLibre.

Ela não representa a arquitetura atual:

- divergiu profundamente de `main`;
- usa estrutura e identidade antigas do projeto;
- implementa composição visual, não uma API federada;
- não deve ser incorporada por merge.

Ideias reutilizáveis, como manifesto de proveniência e registro explícito de falhas externas, podem ser reimplementadas futuramente sobre o estado atual.

## 10. Release histórica

A **release científica `v1.0.0` publicada**, sua tag, DOI `10.5281/zenodo.22130831` e snapshot permanecem imutáveis.

## 11. Próximo marco

O marco **`VITRINE_PUBLIC_MODEL_V2`** está em execução.

O read model v2 e o renderer das páginas individuais estão implementados. O próximo passo é simplificar os cards de descoberta e reduzir a redundância entre `sources.html` e as páginas completas, preservando os testes dos arquétipos.

A sequência semântica alvo permanece:

`Registro da Vitrine → Recurso catalogado → oferta científica → versão/coleção → forma de acesso`

com proveniência, evidência e curadoria transversais.

Integration Registry e conectores continuam posteriores à estabilização da interface e das rotas canônicas.

Plano: `docs/WEB_API_EVOLUTION_PLAN.md`.
