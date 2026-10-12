# Política de seleção e cobertura — Vitrine Ciência

**Status:** vigente  
**Atualização:** 12 de outubro de 2026

## 1. Escopo

A Vitrine prioriza dados ecológicos, ambientais e socioecológicos relevantes ao Brasil, além de informação territorial/contextual necessária à interpretação.

Origem brasileira ou internacional não é uma nota de qualidade.

## 2. Estado do catálogo

O catálogo vivo possui 58 registros.

O núcleo histórico `DR0001–DR0051` permanece preservado. As sete entradas `DR0136–DR0142` foram incorporadas por decisões curatoriais explícitas.

A expansão histórica 135/843/876 permanece em quarentena.

Isso significa que “sem nova ingestão” não deve ser lido como proibição absoluta de qualquer adição pontual. A regra vigente é:

> **A expansão de novas fontes, produtos e distribuições está pausada como processo automático ou em lote e só pode ser retomada por instrução humana explícita. Adições pontuais podem ser aprovadas por decisão curatorial documentada.**

Portanto, a expansão continua controlada e explícita, sem reabrir a ingestão indiscriminada.

## 3. Critério para nova entrada

Um novo registro de alto nível só deve ser criado quando existir um recurso catalogável materialmente distinto e útil para descoberta.

Antes de criar um DR, determinar:

- identidade real do recurso;
- tipo do recurso;
- provedor e papéis institucionais;
- relevância territorial;
- dados/produtos que oferece;
- acesso real disponível;
- licença/condições conhecidas;
- evidência oficial;
- risco de duplicação com registro existente.

Não criar novo DR apenas por:

- novo arquivo;
- novo formato;
- novo endpoint;
- nova página de documentação;
- camada do mesmo produto;
- asset STAC;
- cena;
- pluma;
- download alternativo.

## 4. Granularidade científica

Uma distinção justifica nova entidade subordinada quando muda de forma material:

- significado científico;
- variável/fenômeno;
- método;
- população/unidade observada;
- cobertura;
- versão citável;
- licença;
- interpretação;
- reprodutibilidade.

Diferenças apenas de entrega pertencem normalmente à distribuição ou rota de acesso.

## 5. Prioridade territorial

A classificação corrente usa:

- **P0** — fonte brasileira;
- **P1** — cobertura sistemática do Brasil;
- **P2** — cobertura parcial ou indireta;
- **P3** — referência comparativa.

Estado atual: P0=18, P1=24, P2=14, P3=2.

A classificação territorial orienta descoberta e prioridade de curadoria; não mede qualidade científica.

## 6. Acesso

Distinguir sempre:

- download direto;
- página específica de dados;
- serviço/API;
- catálogo;
- visualizador;
- documentação;
- acesso restrito;
- acesso não confirmado.

HTTP 200 não comprova acesso a dados.

Uma rota principal pode ser D mesmo quando existe API secundária.

## 7. Produtos e versões

Produtos não devem ser enumerados apenas para aumentar cobertura.

Priorizar produtos/famílias que ajudam a responder:

- o que o recurso oferece;
- que fenômeno representa;
- onde e quando se aplica;
- em que escala/resolução;
- qual versão deve ser citada;
- como acessar.

Versões devem ser estruturadas quando forem necessárias à comparação e reprodutibilidade, mas não recebem página pública automaticamente.

## 8. Quarentena

Resultados provenientes de:

- expansão histórica;
- harvesting;
- conectores;
- importações em lote;
- fontes com evidência incompleta;

não entram diretamente na superfície pública.

O caminho é:

`candidate/raw → evidence → normalization → classification → QA/curation → accept or quarantine`.

## 9. Federação e seleção

A futura federação não altera o critério científico de entrada.

Uma API pode descobrir centenas de objetos; somente os objetos relevantes e adequadamente classificados entram no catálogo público.

O Integration Registry registra capacidade técnica; ele não é uma lista automática de conteúdo publicado.

## 10. Revisão e remoção

Um registro pode ser corrigido, dividido, fundido, descontinuado ou mantido como histórico quando houver evidência para isso.

IDs não devem ser reciclados.

Mudanças devem preservar rastreabilidade e, quando possível, redirecionamento ou relação explícita entre estados.

Estado factual: `docs/PROJECT_STATE.md`.  
Execução: `WORKFLOW_STATUS.md`.  
Plano de evolução: `docs/WEB_API_EVOLUTION_PLAN.md`.
