# Workflow de correções de qualidade — Vitrine Ciência

## Estado

A fase corrente é de **QA/QC, re-curadoria e auditoria ontológica**. A expansão de novas fontes, produtos e distribuições está **pausada** até nova **instrução humana explícita**. Para o estado vivo, consultar `docs/PROJECT_STATE.md` e `WORKFLOW_STATUS.md`.

## Objetivo

Corrigir erros que afetem identidade, descoberta, acesso, interpretação ou rastreabilidade sem transformar QA em expansão ou redesign permanente.

## Prioridade

### P0 — erro material

- identidade ou relação incorreta;
- duplicidade real;
- URL apontando para objeto errado;
- dataset confundido com plataforma, catálogo, serviço, viewer ou documentação;
- acesso afirmado sem evidência;
- licença/cobertura/resolução/temporalidade inventada;
- proveniência incorreta.

### P1 — acesso e interpretação

- autenticação, gratuidade, protocolo ou formato incorretos;
- landing page inadequada;
- limitação necessária para uso não registrada;
- classificação científica ou territorial enganosa.

### P2 — completude útil

- documentação adicional;
- palavras-chave;
- detalhamento de versão;
- refinamentos que não alteram identidade nem acesso.

P2 não bloqueia trabalho de maior risco.

## Processo

1. identificar o achado;
2. localizar evidência oficial/primária;
3. determinar o **tipo e papel real da entidade**; não forçar o nível legado fonte/produto/distribuição;
4. propor a menor correção defensável;
5. preservar `desconhecido` quando não houver evidência;
6. validar IDs, relações, vocabulários e URLs aplicáveis;
7. auditar diff;
8. fazer read-back da escrita;
9. executar CI/teste público quando aplicável;
10. fechar somente quando o risco material estiver tratado.

## Regras anti-inferência

- homepage não comprova licença de dataset;
- visualizador não comprova resolução nativa;
- endpoint existente não implica acesso gratuito;
- HTTP 200 não prova que há dados utilizáveis;
- ausência de documentação não significa ausência do atributo;
- licença do portal não deve ser transferida automaticamente ao dataset/distribuição;
- recurso descoberto por API não é publicado automaticamente.

## Diagnóstico

Artefatos derivados e validadores existentes podem orientar investigação, mas não substituem evidência externa. CI verde comprova conformidade do repositório, não verdade científica ou institucional.
