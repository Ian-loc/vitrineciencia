# Workflow de implementação — Vitrine Ciência

**Estado operacional:** QA/QC do catálogo público 58, manutenção do cliente GitHub Pages e preparação do modelo público v2.  
A expansão de novas fontes, produtos e distribuições permanece **pausada** como processo automático/em lote e só pode avançar por **instrução humana explícita** e decisão curatorial documentada.

## Objetivo atual

Preservar o runtime público estável enquanto a arquitetura evolui de um catálogo estático v1 para um modelo público v2 compatível com futura API/federação.

O objetivo imediato **não** é implantar harvesting ou backend. É tornar o modelo público suficientemente preciso para que a automação futura tenha alvos semânticos estáveis.

## Baseline

A baseline de execução está em `docs/PROJECT_STATE.md` e `WORKFLOW_STATUS.md`.

O estado público corrente possui 58 registros, páginas individuais e read models JSON. O checkpoint histórico 51 continua como evidência do núcleo, não como descrição integral do runtime.

## Sequência obrigatória

1. **Preservar baseline** — nenhum trabalho começa sem ler `main`, PRs ativos e estado canônico.
2. **Corrigir documentação/QA** — discrepâncias de estado devem ser eliminadas antes de novas mudanças arquiteturais.
3. **Definir public-record-v2** — separar CatalogRecord e Recurso catalogado.
4. **Garantir compatibilidade** — 58 URLs, IDs e conteúdo essencial devem sobreviver à migração.
5. **Simplificar cards** — descoberta deixa de repetir a ficha detalhada.
6. **Reorganizar páginas individuais** — visão geral, dados/produtos, acesso, interpretação, proveniência.
7. **Canonicalizar access routes** — links deixam de depender de inferência no renderer.
8. **Estruturar versões/proveniência** — somente onde materialmente necessário.
9. **Criar Integration Registry** — antes de conectores.
10. **Executar pilotos de integração** — STAC + padrão adicional + caso proprietário.
11. **Construir pipeline** — raw/staging/normalize/diff/gate.
12. **Só então expor API** — leitura primeiro, revalidação assíncrona depois.

## Regras de concorrência

- um único PR executor por escopo;
- ler o head atual antes de escrever;
- atualizar arquivo contra blob SHA corrente;
- não sobrescrever conflito;
- fechar ou marcar PR superseded;
- executar read-back e CI proporcional.

## Regras de evidência e acesso

- evidência oficial/primária antes de inferência;
- HTTP 200 não prova acesso a dados;
- API/serviço não é automaticamente produto;
- viewer/PDF/homepage não são download;
- desconhecido permanece desconhecido;
- preservar IDs e release histórica;
- não publicar raw/staging;
- nenhuma API externa é requisito para a leitura pública.

## Classes de trabalho

- **WEB-MAINTENANCE** — regressões e QA do cliente atual;
- **PUBLIC-MODEL-V2** — schema/read model;
- **ACCESS-MODEL** — rotas, status e verificação;
- **PROVENANCE/VERSIONING** — agentes, papéis e versões;
- **INTEGRATION-REGISTRY** — perfis de integração;
- **CONNECTORS** — somente após o registry;
- **API/RUNTIME** — somente após modelo e pipeline.

## O que não executar automaticamente

- expansão em lote;
- reentrada da quarentena histórica;
- harvesting sem Integration Registry;
- publicação automática de itens descobertos;
- PostgreSQL/backend como pré-requisito;
- merge da branch experimental `agent/federated-explorer-mvp`;
- nova release/DOI sem decisão específica.

## Autoridade documental

- estado: `docs/PROJECT_STATE.md`;
- workflow: `WORKFLOW_STATUS.md`;
- direção científica: `docs/PROJECT_SCIENTIFIC_DIRECTION.md`;
- arquitetura WEB/API: `docs/WEB_API_EVOLUTION_PLAN.md`;
- contrato público atual: `docs/PUBLIC_RECORD_PAGES_V1.md`.

Se houver conflito, `docs/PROJECT_STATE.md` + `WORKFLOW_STATUS.md` governam o milestone ativo.

## Próximo marco

`VITRINE_PUBLIC_MODEL_V2`

Critério: modelo record/resource validado contra todos os 58 registros, sem regressão de URL/ID e com HTML/JSON derivados do mesmo objeto.
