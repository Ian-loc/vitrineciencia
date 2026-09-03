# Estado canônico — Vitrine Ciência

**Data de referência:** 1º de setembro de 2026  
**Fuso:** `America/Sao_Paulo`

## Estado global

A **fase ativa de QA/QC e manutenção** é o **resgate e a estabilização da Vitrine Ciência estática atual**, antes da mudança conceitual para Data Service/federação.

A aplicação precisa permanecer utilizável enquanto outras pessoas já a usam. Por isso, o trabalho ativo está concentrado em restaurar o núcleo legado de 51 registros, reduzir carga cognitiva, orientar a descoberta por tema científico e corrigir a semântica dos links de acesso.

A expansão de novas fontes, produtos e distribuições continua **pausada**.

## Estado material

- `main` ainda corresponde ao estado público expandido de 135/843/876 até a incorporação do PR de resgate.
- A **release científica `v1.0.0` publicada** permanece imutável, incluindo seu snapshot histórico, tag e DOI `10.5281/zenodo.22130831`.
- O PR `#267` (`curation/core-51-socioecological-discovery-20260901`) é o único PR executor ativo para o resgate estático.
- Na terminologia física do schema legado, o branch candidato contém **51 fontes, 11 produtos, 19 distribuições**. Esses rótulos preservam compatibilidade estrutural e não afirmam que todos os 51 registros são datasets ou pertencem à mesma classe ontológica.
- A expansão histórica permanece preservada em `data/quarantine/v1.0.0-expanded/`.
- Os 51 DR podem representar instituição, plataforma, programa, catálogo, infraestrutura ou outra forma de origem/acesso; a interface pública deve descrevê-los com linguagem honesta e proporcional à evidência disponível.

## Objetivo público atual

A navegação da versão estática deve seguir:

**fenômeno/processo → registros relevantes do núcleo 51 → dado/item detalhado quando existente → rota real de acesso → API/serviço quando existente → proveniência/provedor**.

A interface deve distinguir publicamente:

- dado/download/portal de dados;
- página específica do conjunto;
- API/serviço;
- visualizador ou documentação;
- página do provedor/proveniência.

Somente destinos cujo papel está suficientemente demonstrado podem ser rotulados como acesso confirmado a dados.

## Gates ativos

**S0 — release estática de resgate**

- preservar 51/11/19 e a quarentena histórica;
- Home e catálogo orientados por tema científico controlado;
- 51 registros como superfície ampla de descoberta;
- 11 itens/19 distribuições explicitamente como subconjunto detalhado;
- semântica conservadora dos botões de acesso;
- CI + QA visual + smoke test público.

**S1 — recertificação de acesso 51/51**

Cada DR deve receber nova verificação factual e classificação de acesso:

- `A DIRECT_DATA`;
- `B DATASET_PAGE`;
- `C API_SERVICE`;
- `D VIEWER_DOC`;
- `E BROKEN_UNCERTAIN`.

**S2 — QA final estático**

Confirmar filtros, responsividade, navegação em 2–3 decisões, ausência de quarentena na superfície e coerência entre rótulo e destino.

## Fora do marco atual

Até o token `VITRINE_STATIC_51_STABLE`, não iniciar como frente executora:

- ontologia 2.0 exaustiva;
- Integration Registry federado;
- conectores STAC/CKAN/OGC/REST/GraphQL;
- harvesting;
- PostgreSQL/backend próprio;
- reentrada da expansão.

Esses elementos permanecem como direção futura, mas não são pré-condição para corrigir a GitHub Page que está em uso hoje.

## Regra de conclusão

O marco estático só é concluído quando o site público estiver funcional, os 51 acessos estiverem recertificados ou explicitamente marcados como incertos, e CI/QA/smoke estiverem verdes.

Somente então declarar:

`VITRINE_STATIC_51_STABLE`

Depois desse token, a automação executora deve ser desativada. A migração para Data Service/federação será um novo milestone, dependente de autorização posterior.
