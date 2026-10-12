# Workflow de correções de qualidade — Vitrine Ciência

## Estado

A fase corrente é de **QA/QC e manutenção** do catálogo público 58, em paralelo ao desenho controlado do modelo público v2.

A expansão de novas fontes, produtos e distribuições está **pausada** como processo automático/em lote e requer **instrução humana explícita** para adições pontuais ou retomada mais ampla. Para o estado vivo, consultar `docs/PROJECT_STATE.md` e `WORKFLOW_STATUS.md`.

## Objetivo

Corrigir erros que afetem identidade, descoberta, acesso, interpretação, proveniência ou rastreabilidade sem transformar QA em expansão automática ou redesign não governado.

## Prioridade

### P0 — erro material

- identidade ou relação incorreta;
- duplicidade real;
- URL apontando para objeto errado;
- registro confundido com recurso;
- dataset confundido com plataforma, serviço, viewer ou documentação;
- acesso afirmado sem evidência;
- licença/cobertura/resolução/temporalidade inventada;
- proveniência incorreta;
- regressão que quebra uma das 58 URLs públicas.

### P1 — acesso e interpretação

- autenticação, gratuidade, protocolo ou formato incorretos;
- landing page inadequada;
- limitação necessária ausente;
- classificação científica ou territorial enganosa;
- versão/coleção apresentada como comparável sem evidência;
- papel de rota incorreto.

### P2 — completude útil

- documentação adicional;
- palavras-chave;
- detalhamento de versão;
- papéis de proveniência;
- refinamentos que não alteram identidade nem acesso.

P2 não bloqueia trabalho de maior risco.

## Processo

1. identificar o achado;
2. localizar a autoridade canônica afetada;
3. recuperar evidência oficial/primária;
4. determinar o tipo e papel real da entidade;
5. propor a menor correção defensável;
6. preservar desconhecido quando não houver evidência;
7. validar IDs, relações, vocabulários e URLs;
8. auditar diff;
9. fazer read-back;
10. executar CI/QA/smoke proporcional;
11. fechar somente quando o risco material estiver tratado.

## Regras anti-inferência

- homepage não comprova licença;
- visualizador não comprova resolução;
- endpoint não implica acesso gratuito;
- HTTP 200 não prova dados utilizáveis;
- ausência de documentação não significa ausência do atributo;
- licença do portal não é automaticamente licença do produto;
- recurso descoberto por API não é publicado automaticamente;
- resposta de harvesting não altera diretamente o snapshot público.

## QA do modelo v2

Mudanças v2 devem testar:

- preservação das 58 URLs;
- preservação dos IDs;
- separação `record → resource`;
- compatibilidade de rotas;
- desconhecido ≠ não;
- produtos somente quando materialmente existentes;
- renderização HTML/JSON coerente.

## Diagnóstico

Artefatos derivados e validadores orientam investigação, mas não substituem evidência externa. CI verde comprova conformidade do repositório, não verdade científica ou institucional.
