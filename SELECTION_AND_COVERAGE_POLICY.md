# Política de seleção, exclusão, duplicidade e cobertura — Vitrine Ciência

## 1. Objetivo

Explicitar por que uma fonte ou produto entra, como duplicidades são controladas e como o Brasil é priorizado. A Vitrine não é declarada completa ou representativa de todo o universo de dados científicos existente.

## 2. Prioridade territorial

O **Brasil é o escopo territorial central**. A curadoria prioriza:

1. fontes brasileiras com dados úteis sobre o Brasil;
2. fontes internacionais com cobertura brasileira sistemática e diretamente pesquisável;
3. fontes internacionais cuja cobertura brasileira depende de coleção, sítio, depósito ou produto;
4. excepcionalmente, referências sem cobertura brasileira direta com valor metodológico/comparativo claro.

Prioridade territorial não é nota de qualidade científica.

## 3. Classificação P0–P3

`data/brazil_scope_priorities.json` classifica as fontes:

| Prioridade | Classe | Papel |
|---|---|---|
| `P0` | `fonte_brasileira` | núcleo |
| `P1` | `cobertura_brasil_sistematica` | complemento internacional prioritário |
| `P2` | `cobertura_brasil_parcial` | contexto dependente do produto/coleção |
| `P3` | `referencia_sem_cobertura_brasil` | referência comparativa excepcional |

A classificação é curatorial e auditável; não deve ser inferida apenas por domínio, idioma ou nome institucional.

## 4. Critérios de inclusão de fonte

Uma fonte deve:

- oferecer dados, metadados ou infraestrutura útil de descoberta/acesso;
- possuir identidade e governança rastreáveis;
- ter utilidade para pesquisa, ensino ou extensão;
- permitir descrição honesta de cobertura, acesso, licença e limitações;
- demonstrar vínculo com o Brasil ou justificar sua função secundária;
- não duplicar semanticamente outra fonte sem benefício claro de descoberta.

## 5. Critérios de exclusão

Não criar fonte para:

- notícia, blog ou material somente editorial;
- artigo/relatório sem infraestrutura associada;
- dataset isolado pertencente a fonte já catalogada, quando deve ser produto;
- mirror sem governança própria;
- recurso descontinuado sem função independente;
- objeto cuja identidade não possa ser sustentada;
- fonte internacional redundante sem cobertura do Brasil ou função estratégica distinta.

## 6. Entrada de produto

Produto recebe ID próprio quando sua distinção melhora materialmente a descoberta por finalidade, conteúdo, método, cobertura, suporte/resolução, coleção/versão ou acesso. Arquivos, bandas, tiles, formatos e endpoints não criam produtos automaticamente.

O campo `enumeration_scope` evita falsa completude: `complete`, `family_level`, `external_index` ou `representative_sample`.

## 7. Duplicidade

### Mesmo recurso, nomes ou URLs diferentes

Manter uma entrada e preservar o nome/rota vigente quando representam a mesma identidade e governança.

### Portal e produto

Portal/fonte e produto podem coexistir porque ocupam níveis diferentes. Não duplicar produto apenas por outra página de acesso.

### Agregador e provedor

Podem coexistir quando oferecem funções distintas, mas a proveniência do provedor primário deve permanecer explícita.

### Sucessor

Preferir o sucessor ativo quando o anterior apenas redireciona; preservar histórico necessário sem duplicar a descoberta corrente.

## 8. Candidatos e inclusão

Novas fontes podem ser triadas em `candidates/source_candidates.csv`, mas a inclusão no CSV canônico é permitida após evidência suficiente, verificação de duplicidade/escopo, validação estrutural e revisão proporcional ao risco. Não existe mais bloqueio geral que impeça expansão até “finalizar 51 fontes”.

## 9. Fila de expansão

Priorizar:

1. fontes brasileiras que reduzam lacunas relevantes;
2. fontes internacionais com cobertura sistemática do Brasil;
3. aprofundamento de produtos de fontes já catalogadas quando isso melhora substancialmente a utilidade;
4. coberturas parciais e metacatálogos;
5. referências P3 somente com justificativa explícita.

Volume bruto não substitui relevância, qualidade documental ou diferença semântica.

## 10. Lacunas

A avaliação de lacunas pode considerar:

- área de pesquisa;
- bioma/região;
- escala e suporte;
- natureza institucional;
- tipo de produto;
- acesso programático;
- gratuidade/autenticação;
- presença e profundidade de dados brasileiros;
- representação de produtos e distribuições.

A matriz orienta busca; não cria cotas.

## 11. Revisão

- antes de cada lote: checar duplicidades e cobertura Brasil;
- a cada inclusão de fonte: atualizar P0–P3;
- periodicamente: revisar recursos descontinuados, renomeados ou incorporados;
- imediatamente: tratar mudanças relevantes de governança/licença/acesso;
- antes de uma release estável: resolver duplicidades materiais conhecidas ou documentar seu tratamento.

## 12. Estado atual

Em 18/08/2026 a Vitrine possui **125 fontes, 756 produtos e 787 distribuições** dentro do contrato de 34/24/15 campos. O catálogo está em expansão contínua e auditada. Não há requisito de migração para 38 campos ou de retornar ao baseline histórico de 51 fontes.
