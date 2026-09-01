# Workflow de implementação — Vitrine Ciência

**Estado operacional:** resgate e estabilização da GitHub Page estática atual.  
A expansão de novas fontes, produtos e distribuições permanece **pausada**. A arquitetura federada/Data Service também não é frente executora enquanto o marco estático não estiver concluído.

## Objetivo atual

Entregar a versão estática baseada nos 51 registros legados como um catálogo científico simples, correto e funcional para usuários atuais, sem depender da futura reestruturação arquitetural.

## Sequência obrigatória

1. **Restaurar núcleo** — 51 registros DR legados / 11 itens detalhados / 19 distribuições; preservar a expansão 135/843/876 em quarentena.
2. **Descoberta científica** — Home e catálogo por fenômeno/processo com termos controlados; busca textual livre fora da superfície principal.
3. **Separar papéis de acesso** — dados/download/portal, página do conjunto, API/serviço, viewer/documentação e página do provedor.
4. **Reduzir carga cognitiva** — metadados técnicos em refinamentos/detalhes; cards com identidade, descrição curta, cobertura, proveniência e ações úteis.
5. **Validar release estática** — CI, QA visual, diff e artefato isolado.
6. **Publicar o resgate** — incorporar o PR canônico e executar smoke test real da GitHub Pages.
7. **Recertificar 51/51** — revisar acessos em batches, registrar última verificação e classificar A/B/C/D/E.
8. **QA final** — confirmar coerência semântica, responsividade, teclado e percurso em 2–3 decisões.
9. **Concluir** — somente trabalho materializado e verificado conta como concluído.

## Regras de concorrência

- um único PR/branch executor para o mesmo escopo;
- antes de escrever, ler `main`, PR ativo, head SHA e arquivos modificados;
- se o head mudar, refazer a leitura antes de escrever;
- atualizar arquivo somente contra o blob SHA atual;
- conflito não é resolvido por sobrescrita forçada;
- PR superseded deve ser fechado ou claramente marcado.

## Regras de evidência e acesso

- evidência oficial/primária antes de inferência;
- HTTP 200 não prova que um destino fornece dados;
- não rotular PDF, viewer ou homepage genérica como download/API;
- desconhecido permanece desconhecido e recebe estado de revisão;
- preservar IDs, histórico e release `v1.0.0`;
- não publicar conteúdo de quarentena.

## Classes de trabalho até o marco estático

- **STATIC-UX:** descoberta temática, hierarquia visual e redução de carga cognitiva.
- **ACCESS-QA:** função do link, última verificação e classificação A/B/C/D/E.
- **DATA-CORE:** preservação 51/11/19 e quarentena histórica.
- **DOC/QA:** documentação de estado, testes, build e smoke test.

**Não executar ainda:** ONTOLOGY-2, FEDERATION, CONNECTORS, POSTGRESQL ou EXPANSION.

## Autoridade documental

- estado: `docs/PROJECT_STATE.md`;
- workflow/limite: `WORKFLOW_STATUS.md`;
- direção científica de longo prazo: `docs/PROJECT_SCIENTIFIC_DIRECTION.md`;
- contratos históricos/transitórios: demais documentos metodológicos.

Se houver conflito entre a direção futura e o estado de execução, **`docs/PROJECT_STATE.md` + `WORKFLOW_STATUS.md` governam o milestone ativo**.

## Marco de conclusão

Somente declarar `VITRINE_STATIC_51_STABLE` quando os critérios objetivos de `WORKFLOW_STATUS.md` estiverem materialmente satisfeitos. Depois, desabilitar a tarefa recorrente. Federação/Data Service passa a ser um novo milestone, não uma continuação automática.
