# UX6 — descoberta e comparação de produtos

## Status

**Implementado e em manutenção.** Este documento descreve a camada pública de produtos como um subconjunto detalhado do catálogo.

As contagens correntes não são replicadas aqui; consultar `docs/PROJECT_STATE.md`, `WORKFLOW_STATUS.md` e as tabelas canônicas.

A fase corrente é de **QA/QC e manutenção**. A expansão de novas fontes, produtos e distribuições está **pausada** como processo automático/em lote até nova **instrução humana explícita**.

## Papel atual

`products.html` não é a página principal de descoberta nem pretende enumerar todo o conteúdo científico dos 58 registros.

Seu papel é:

- oferecer uma visão comparável dos itens já detalhados;
- expor propriedades que pertencem ao produto, não ao registro agregador;
- preservar distribuições e acessos específicos;
- servir de laboratório para o modelo mais rico que deverá migrar para `public-record-v2`.

## Relação com as páginas individuais

Após o PR #277, cada DR possui página própria.

A navegação desejada é:

`descoberta → registro → produto detalhado quando existente → distribuição/acesso`

Produtos não recebem página pública independente por padrão.

## Regras vigentes

- registro, recurso, produto e distribuição não são sinônimos;
- formatos diferentes não criam produto por si só;
- API/serviço não é automaticamente produto;
- resolução não é inferida pelo viewer;
- licença/proveniência são registradas no nível mais específico sustentado;
- megacatálogos usam enumeração seletiva ou índice externo;
- a interface não certifica comparabilidade universal;
- versão/coleção deve ser preservada quando necessária à interpretação.

## Limitação conhecida

O contrato físico atual ainda usa `resource_id → product_id → distribution_id`.

O modelo v2 deverá permitir representar com mais clareza:

- oferta científica;
- série/família;
- versão/coleção;
- distribuição;
- DataService;
- rota de acesso;
- proveniência.

## Validação

O pipeline deve exigir, conforme o delta:

1. validação territorial;
2. validação do catálogo de produtos;
3. build de derivados;
4. auditoria de papéis dos links;
5. validação geral;
6. build de `_site`;
7. sintaxe JavaScript;
8. QA visual quando houver mudança de interface;
9. smoke pós-deploy.

## Evolução

O próximo passo não é aumentar indiscriminadamente o número de produtos.

É usar casos representativos para validar o modelo v2 e, depois, enriquecer registros em que a decomposição por produtos/versões melhora materialmente a descoberta.

## GitHub Pages

A publicação oficial continua via GitHub Actions. A fronteira pública é definida em `docs/VITRINE_BOUNDARY.md` e `scripts/build_site_artifact.py`.
