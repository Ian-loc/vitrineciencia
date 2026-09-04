# Checkpoint — Vitrine estática 51

**Data:** 2026-09-04  
**Status:** `VITRINE_STATIC_51_STABLE`

## Autoridade

GitHub `Ian-loc/vitrineciencia`, branch `main`.

Runtime público validado: `495bfe6a968176670461662869d1a3773797baf3`.

## Estado material

- 51 registros DR no núcleo público;
- 11 itens detalhados;
- 19 distribuições/rotas no subconjunto detalhado;
- 51/51 com tipagem semântica concluída;
- acesso de fontes: A=1, B=38, C=0, D=10, E=2;
- `DR0014` e `DR0039` permanecem E como limitações verificadas;
- P1–P6 materializado sem alterar as contagens 51/11/19;
- expansão 135/843/876 preservada apenas em quarentena/histórico;
- release `v1.0.0` e DOI `10.5281/zenodo.22130831` permanecem imutáveis.

## Autoridades de classificação

- estrutura física: `data/data_resources.csv`, `data/data_products.csv`, `data/product_distributions.csv`;
- acesso A–E: `data/static_core_51_access_audit.json`;
- tipagem semântica: `data/static_core_51_progress.json`;
- papéis das 19 rotas: `data/product_distribution_roles.json`;
- gate territorial aplicado: `data/applied_priority_gate.json`.

A interface não deve inferir essas classificações por palavras-chave.

## Correções de fechamento

- `products.html` voltou a materializar os 11 cards e a expor a contagem das 19 rotas;
- território em Produtos usa controle fechado, não busca livre;
- o artefato `_site` fecha dependências locais utilizadas pelas páginas e valida referências HTML e `fetch()` literais;
- `source-discovery-v2.js` consome A–E da matriz canônica de acesso;
- `semantic-roles.js` combina tipagem semântica e acesso sem confundir suas autoridades;
- ciclos de `MutationObserver` em Produtos e Fontes foram removidos sem relaxar o QA;
- P1–P6 está incluído no artefato publicado.

## Evidência automatizada do runtime

- build/validação/deploy — run `33906109623`: PASS;
- QA visual/responsivo — run `33906109551`: PASS;
- smoke pós-deploy — run `33906157842`: PASS.

Os três runs referem-se ao runtime `495bfe6a968176670461662869d1a3773797baf3`.

## Regra após o checkpoint

A **fase ativa de QA/QC e manutenção** passa a tratar apenas manutenção e regressões do marco estável. Não reabrir a recertificação do núcleo sem nova evidência factual, conflito ou regressão.

Federação/Data Service, Integration Registry, harvesting, backend próprio, reentrada da expansão e nova release/DOI são trabalhos posteriores e não são iniciados por este checkpoint.
