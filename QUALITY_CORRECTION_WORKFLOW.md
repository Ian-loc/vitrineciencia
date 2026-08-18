# Workflow de correções de qualidade — Vitrine Ciência

## Objetivo

Corrigir erros e incertezas que afetam descoberta, acesso ou interpretação sem transformar controle de qualidade em redesenho permanente do projeto.

## Regra central

**Qualidade é proporcional ao risco.** O objetivo é um catálogo tecnicamente defensável e útil, não eliminar toda lacuna documental existente nos provedores externos.

## Fontes de diagnóstico

- `data/data_quality_report.json` — preenchimento e campos desconhecidos/variáveis;
- `data/link_role_audit.json` — papéis e sobreposição de URLs;
- `scripts/validate_product_catalog.py` — integridade fonte/produto/distribuição;
- `scripts/validate_brazil_scope.py` — cobertura da classificação P0–P3;
- auditorias específicas em `audit/` e `docs/audits/`;
- falhas reais observadas na interface ou no acesso externo.

## Snapshot de qualidade — 18/08/2026

O catálogo possui 125 fontes; `data/data_quality_report.json` registra, entre os sinais explicitamente consolidados:

- 49 fontes com licença desconhecida/variável;
- 72 com alguma incerteza de acesso;
- data máxima de verificação `2026-08-18`.

Esses números orientam prioridade, mas não significam que os datasets externos sejam deficientes. Outros campos podem ser avaliados diretamente no catálogo quando necessário, sem transformar estimativas ad hoc em métricas oficiais.

## Priorização

### P0 — erro material

Corrigir primeiro:

- ID/relação quebrada;
- identidade errada ou duplicação material;
- URL que aponta para objeto incorreto;
- licença afirmada incorretamente;
- cobertura Brasil falsa;
- confusão entre observação, previsão, classificação, modelo ou registro administrativo;
- resolução/temporalidade inventada.

### P1 — acesso e interpretação

- autenticação, gratuidade, protocolo e formato;
- página de acesso desatualizada;
- limitações ausentes que podem induzir uso incorreto;
- granularidade de produto inadequada.

### P2 — completude útil

- metodologia/documentação adicional;
- detalhamento de versões;
- refinamento de usos e palavras-chave;
- melhoria de evidências representativas.

P2 não deve bloquear publicação de um snapshot defensável.

## Processo de correção

1. identificar achado material;
2. localizar evidência oficial/primária atual;
3. determinar nível correto: fonte, produto ou distribuição;
4. propor alteração mínima;
5. preservar `desconhecido` quando não há base suficiente;
6. validar IDs, relações, enums e URLs;
7. auditar o diff;
8. publicar/verificar quando aplicável;
9. encerrar o achado quando o risco relevante estiver tratado.

## Regras anti-inferência

- homepage não comprova licença de dataset;
- visualizador não comprova resolução nativa;
- endpoint existente não implica acesso gratuito;
- ausência de documentação não implica ausência do atributo;
- licença do portal não deve ser transferida automaticamente às distribuições;
- produto derivado não deve ser apresentado como observação primária.

## Duplicidades

Duplicidades de nome ou identidade devem ser revisadas semanticamente. IDs estáveis não são apagados ou reciclados silenciosamente. Quando necessário, uma consolidação deve preservar rastreabilidade e definir alias/tombstone ou outra estratégia explícita.

## Drive

O workbook do Drive não deve receber uma “correção” isolada. Primeiro corrige-se `main`; depois o espelho pode ser regenerado integralmente. Divergência do espelho é problema de sincronização, não evidência contra os CSVs canônicos.

## Critério de suficiência

Uma rodada de QA termina quando:

- não há erro material conhecido no escopo revisado;
- os validadores aplicáveis passam;
- limitações remanescentes estão explícitas;
- o retorno marginal de nova revisão é baixo em relação a outras prioridades do catálogo.

Novos achados futuros reabrem o registro específico; não tornam todo o catálogo perpetuamente provisório.
