# Direção científica — Vitrine Ciência

**Status:** vigente  
**Atualização:** 12 de outubro de 2026  
**Fase operacional:** QA/QC do catálogo público 58, manutenção do cliente estático e desenho do modelo público v2. Estado factual: `docs/PROJECT_STATE.md`; execução: `WORKFLOW_STATUS.md`.

## Missão

A Vitrine Ciência deve reduzir o caminho entre uma pergunta científica e um conjunto de dados adequado, compreensível e acessível para pesquisa sobre sistemas ambientais, ecológicos e socioecológicos relevantes ao Brasil.

A Vitrine não é, por padrão, um repositório integral nem uma réplica dos catálogos externos. Ela é uma camada de **descoberta, curadoria, interpretação e encaminhamento**.

A expansão de novas fontes, produtos e distribuições está **pausada** como processo automático/em lote. Novas entradas exigem **instrução humana explícita**, evidência e decisão curatorial; isso não impede correções nem adições pontuais formalmente autorizadas.

## Unidade de valor

O sucesso da Vitrine não deve ser medido principalmente pela quantidade de registros, produtos ou campos preenchidos.

Medidas mais relevantes são:

- proporção de registros com acesso real e corretamente rotulado;
- atualidade das verificações;
- número de decisões entre descoberta e acesso;
- cobertura dos fenômenos relevantes;
- clareza entre recurso, produto, versão, distribuição e serviço;
- qualidade da proveniência e das limitações;
- redução de microprodutos redundantes;
- reprodutibilidade do estado público.

## Ordem de descoberta

A experiência pública deve priorizar:

**fenômeno/processo → território/contexto → recurso relevante → dado/produto adequado → acesso → proveniência**

A organização técnica do provedor aparece quando necessária, não como pré-requisito para a descoberta.

## Registro e recurso

O `DR####` identifica um **Registro da Vitrine**.

O objeto real descrito por esse registro é um **Recurso catalogado**, que pode ser:

- iniciativa/programa;
- plataforma/sistema;
- catálogo/repositório;
- infraestrutura/serviço;
- base/coleção;
- rede/observatório;
- registro/guia/referência.

A versão pública v1 ainda não separa essas entidades estruturalmente; essa é a principal correção do modelo v2.

## Princípios científicos

1. **Utilidade antes de granularidade.**
2. **Registro não é necessariamente dataset.**
3. **Dado, serviço, visualização e documentação são objetos distintos.**
4. **Produto científico só existe quando há significado próprio além da forma de entrega.**
5. **Versão deve ser distinguida quando altera conteúdo, método ou reprodutibilidade.**
6. **Proveniência é uma relação transversal, não um único campo de “dono”.**
7. **Acesso precisa ser verificável e ter função explícita.**
8. **Desconhecido não é negativo.**
9. **Resumo no nível do registro não deve inventar precisão ausente nos produtos.**
10. **Produto mais específico prevalece sobre resumo geral quando há evidência melhor.**
11. **Brasil é prioridade territorial, não selo de qualidade.**
12. **Curadoria antecede automação.**

## Federação

A direção de longo prazo é um catálogo científico federado de metadados e acesso.

Os dados permanecem, em regra, nos provedores. A Vitrine mantém:

- identidade;
- relações;
- classificação científica;
- cobertura;
- versão;
- proveniência;
- licença;
- métodos de acesso;
- estado da verificação;
- metadados necessários à descoberta.

O harvesting serve para reduzir desatualização e trabalho repetitivo; não substitui decisão curatorial.

## Atualização por API

A futura atualização sob demanda deve preservar três propriedades:

- **resiliência:** o snapshot continua disponível;
- **auditabilidade:** mudanças externas passam por staging/diff;
- **controle científico:** novos objetos não entram automaticamente na superfície pública.

Portanto, o padrão alvo é `static-first / stale-while-revalidate`, não consulta distribuída síncrona.

## Escopo territorial

A descoberta deve distinguir:

- fonte brasileira;
- cobertura sistemática do Brasil;
- cobertura parcial/indireta;
- referência comparativa.

Um recurso internacional pode ser altamente relevante; um recurso brasileiro pode ser pouco adequado a determinada pergunta. Proveniência e cobertura são descrições, não notas de qualidade.

## Critério de sucesso

A Vitrine é satisfatória quando uma pessoa consegue:

1. começar por uma pergunta ou fenômeno;
2. localizar recursos adequados;
3. entender o que cada opção representa;
4. distinguir produto, versão e forma de acesso;
5. avaliar cobertura e limitações;
6. chegar ao dado no provedor;
7. saber quem produziu, publicou e mantém a informação.

E quando o mantenedor consegue reconstruir por que cada objeto está publicado, qual evidência o sustenta e como foi atualizado.
