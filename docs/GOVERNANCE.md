# Governança — Vitrine Ciência

## 1. Finalidade

A governança da Vitrine protege um produto simples: catálogo público, estático, reproduzível e cientificamente defensável de fontes, produtos e formas de acesso relevantes ao Brasil.

## 2. Autoridade

Ordem vigente:

1. `main` de `Ian-loc/vitrineciencia`;
2. três CSVs canônicos;
3. contratos e validadores executáveis;
4. documentação ativa indicada em `docs/PROJECT_STATE.md`;
5. auditorias e evidências;
6. artefatos derivados e espelhos do Drive.

O Simbiotrama é independente e não participa da autoridade, runtime ou publicação da Vitrine.

## 3. Regime de mudança

Mudanças devem seguir um pacote coerente:

`scope → evidence → implementation → validation → diff audit → public validation when relevant → integration → post-merge verification → consolidation`

Branch nova parte de `main`. Alterações não relacionadas devem permanecer separadas. O critério de conclusão deve ser explícito e proporcional ao risco.

## 4. Classes de risco

### AUTO-SAFE

Pode avançar quando controles objetivos passam:

- documentação e status;
- correções de QA/CI que não relaxem gates;
- pequenas correções factuais inequívocas com evidência oficial;
- pequenos lotes de fontes/produtos dentro do contrato vigente;
- saneamento reversível e sem efeito destrutivo.

### REVIEW

Requer revisão humana do pacote:

- lote grande;
- mudança pública significativa de interface/comportamento;
- evidência factual conflitante;
- alteração operacional de impacto difícil de avaliar somente por testes.

### HUMAN-DECISION

Requer decisão explícita antes da mudança material:

- alteração de escopo ou schema incompatível;
- remoção destrutiva/em massa;
- nova infraestrutura estrutural;
- tracking/analytics de usuários ou decisão de privacidade;
- licença, autoria ou política oficial de citação;
- release `1.0.0`;
- publicação de DOI/Zenodo.

## 5. Curadoria

Uma alteração de dados deve:

- preservar IDs existentes;
- manter integridade fonte → produto → distribuição;
- sustentar valores factuais com evidência adequada;
- registrar desconhecido/variável quando a evidência não permite precisão maior;
- evitar promoção de propriedades específicas para níveis mais gerais;
- registrar `last_verified` somente após revisão efetiva;
- atualizar classificação Brasil e artefatos derivados quando aplicável.

## 6. Papéis

### Responsável científico e mantenedor

Define missão, prioridades, escopo, autoria, licença, releases e decisões HUMAN-DECISION.

### Curadoria/contribuição

Propõe e verifica registros, preserva proveniência, identifica limitações e executa o contrato sem inventar metadados.

### Automação

Valida estrutura, relações, contratos e regressões; constrói artefatos derivados; não substitui julgamento factual externo nem decide mudanças de escopo.

## 7. Publicação

O workflow de Pages deve construir apenas o artefato público definido em `docs/VITRINE_BOUNDARY.md`. Materiais internos, schemas históricos, auditorias e conteúdo do Simbiotrama não podem vazar para `_site`.

Publicação é considerada consolidada somente depois de build/CI e verificação pós-deploy aplicáveis.

## 8. Drive

Arquivos do Drive são documentação, histórico ou espelhos derivados. Não devem receber correções canônicas isoladas. Um espelho só pode ser chamado de sincronizado se declarar commit-fonte e tiver sido comparado contra o snapshot correspondente.

## 9. Releases e DOI

A Vitrine viva pode continuar evoluindo entre releases. Uma release citável exige tag/commit imutável, dados e documentação coerentes, artefato reproduzível e inspeção do pacote. DOI é uma decisão humana e deve representar um snapshot arquivado, não apenas a página dinâmica.

## 10. Evidência histórica

Documentos relacionais/Simbiotrama anteriores a 09/08/2026, auditorias antigas, PRs e decisões superadas devem ser preservados como histórico, mas não podem competir com a documentação ativa. `docs/PROJECT_STATE.md` define essa classificação.
