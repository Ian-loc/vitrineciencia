# Estado do workflow — Vitrine Ciência

Atualização: **2026-09-01** (`America/Sao_Paulo`)

## Fase ativa

A fase ativa de **QA/QC** é o **resgate e a estabilização da Vitrine Ciência estática com o núcleo legado de 51 registros DR0001–DR0051**.

A expansão permanece pausada. A futura arquitetura federada/Data Service também permanece pausada enquanto a versão estática usada hoje não estiver correta, navegável e operacionalmente confiável.

Há uma única frente executora recorrente para este projeto. Enquanto o PR `#267` estiver aberto, não abrir branch/PR concorrente com o mesmo escopo.

Na terminologia física do schema legado, o candidato contém **51 fontes, 11 produtos, 19 distribuições**. Esses nomes preservam compatibilidade do corpus e não congelam uma ontologia final.

## Sequência de execução

1. **S0 — release estática de resgate**
   - restaurar 51 registros / 11 itens detalhados / 19 distribuições;
   - preservar 135/843/876 somente em quarentena histórica;
   - Home orientada por fenômeno/processo;
   - 51 registros como superfície ampla de descoberta;
   - 11/19 explicitamente como subconjunto detalhado;
   - separar dados, API/serviço, página do conjunto, visualizador/documentação e página do provedor;
   - CI, QA visual e smoke test público.
2. **S1 — recertificação 51/51 de acessos**
   - revisar em batches de 8–15;
   - registrar `last_verified` e função factual do destino;
   - classificar cada acesso como A/B/C/D/E;
   - corrigir ou marcar como revisão qualquer PDF, viewer, homepage genérica, login, rota quebrada ou ambígua.
3. **S2 — QA final estático**
   - filtros, navegação, mobile/desktop, teclado e parâmetros de URL;
   - contagens e fronteira pública;
   - coerência rótulo → destino;
   - percurso tema → resultado → acesso em no máximo 2–3 decisões.

## Classificação de acesso

- **A DIRECT_DATA** — download, arquivo ou endpoint que entrega dados.
- **B DATASET_PAGE** — página específica do conjunto com mecanismo explícito de obtenção.
- **C API_SERVICE** — API/OGC/STAC/CKAN/GraphQL ou serviço que permite consulta/extração.
- **D VIEWER_DOC** — visualizador, mapa, dashboard, documentação, artigo ou PDF sem acesso de dados demonstrado.
- **E BROKEN_UNCERTAIN** — quebrado, restrito ou incerto.

Somente A–C podem ser apresentados como acesso confirmado a dados. D deve ser rotulado pelo que é; E permanece “acesso em revisão”.

## Estado material do repositório

- `main`: estado público expandido 135/843/876 até a incorporação do resgate.
- `v1.0.0`: release histórica imutável.
- PR `#267`: candidato estático 51/11/19, com expansão preservada em quarentena.
- PR `#265`: fechado sem merge por estar superseded.

## Definition of Done — `VITRINE_STATIC_51_STABLE`

O marco termina somente quando:

- `main` pública usa o núcleo 51 e a quarentena histórica continua preservada;
- Home e filtros controlados funcionam sem busca textual livre como mecanismo principal;
- 51/51 têm disposition de acesso A/B/C/D/E e verificação atual registrada, ou E explicitamente justificado;
- nenhuma ação rotulada como dados/download/API aponta silenciosamente para PDF, viewer, documentação ou homepage genérica;
- onde dados, API e homepage são distintos, a interface distingue essas funções;
- 11 itens/19 distribuições são apresentados como subconjunto detalhado;
- CI, QA visual e smoke test público passam no commit final;
- não há PR executor concorrente com o mesmo escopo;
- o estado final e limitações residuais estão documentados;
- o usuário consegue sair de um tema científico e chegar a uma opção relevante e a uma rota corretamente rotulada em 2–3 decisões.

Somente então declarar:

`VITRINE_STATIC_51_STABLE`

Após esse token, a execução recorrente deve ser desativada.

## Fora do escopo até esse marco

- ontologia 2.0 exaustiva como pré-condição de publicação;
- Integration Registry;
- conectores federados;
- MapBiomas Alerta como piloto GraphQL;
- PostgreSQL/backend próprio;
- reentrada da expansão;
- nova release/DOI.

Esses itens pertencem ao próximo milestone conceitual, não ao resgate da página estática atual.
