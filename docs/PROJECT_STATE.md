# Estado canônico e disposição dos artefatos — Vitrine Ciência

**Data de referência:** 27 de agosto de 2026  
**Fuso:** `America/Sao_Paulo`  
**Estado global:** catálogo público operacional; contrato **Fonte → Produto → Distribuição** estável; descoberta pública **product-first**; QA/QC e manutenção ativos; candidata `v1.0.0` ainda sem tag Git imutável, GitHub Release ou DOI.

## 1. Autoridade

1. `main` de `Ian-loc/vitrineciencia` para desenvolvimento corrente;
2. tags/releases imutáveis para snapshots científicos quando formalmente publicados;
3. três tabelas canônicas: `data_resources.csv`, `data_products.csv`, `product_distributions.csv`;
4. contratos e validadores executáveis da Vitrine;
5. documentação ativa;
6. auditorias/evidências históricas;
7. espelhos do Drive e outros snapshots derivados.

JSONs, páginas públicas e relatórios de qualidade são artefatos derivados. O Google Drive não é autoridade concorrente.

## 2. Estado do catálogo

Snapshot candidato a `v1.0.0`, preparado em 19/08/2026:

- **135 fontes**;
- **843 produtos**;
- **876 distribuições**;
- identificadores correntes chegam a `DR0135`, `DP000861` e `DD000894`;
- fontes verificadas até 19/08/2026;
- schema vigente: 34 campos de fonte, 24 de produto e 15 de distribuição.

**135 é a contagem de fontes.** A superfície pública de descoberta opera sobre os **843 produtos**. O pacote de UX de 27/08/2026 reorganiza descoberta, filtros, ranking, cards e comparação; não cria registros científicos novos.

## 3. Estado da experiência pública

### Unidade primária de descoberta

O usuário começa por **produtos/datasets**. Fontes são apresentadas como proveniência, responsabilidade institucional e contexto de documentação. A arquitetura interna continua:

```text
Fonte
  └── Produto
        └── Distribuição
```

### Busca e filtros

A busca reconhece deterministicamente temas/sinônimos científicos, biomas, Brasil, anos e resoluções espaciais. Os filtros principais são tema/variável, geografia, período, resolução temporal, suporte espacial, resolução espacial, forma de acesso, formato, licença e gratuidade. Fonte, tipo, autenticação, estado, origem e disponibilidade Brasil são complementares.

O ranking padrão é: **relevância → dados para o Brasil → completude/documentação → origem da fonte → nome**.

### Resultado canônico

O card canônico é o card de produto, com **Onde? · Quando? · Escala? · Acesso?** sempre visíveis. Metodologia, limitações, licença, versão, proveniência e distribuições ficam no detalhe expandido. A listagem mostra 18 produtos por lote em desktop/tablet responsivo, com 3/2/1 colunas conforme largura.

### Comparação

Um único controlador mantém a seleção de produtos. A exportação CSV lê a tabela efetivamente aberta e não possui estado próprio. Produtos podem ser removidos dentro da comparação; fechar a janela zera a seleção.

### Mobile e tablet

Navegação responsiva com botão de menu é obrigatória para smartphones e tablets. O CI testa desktop (1440 px), tablet (820 px) e smartphone (390 px), incluindo overflow horizontal, filtros, cards, busca interpretada e comparação.

## 4. Ciclo de vida dos artefatos

### `ACTIVE`

- interface pública product-first;
- três CSVs canônicos e classificação Brasil;
- scripts de build e validação;
- GitHub Pages e smoke pós-deploy;
- documentação pública/metodológica, citação e licenças;
- QA/QC, correções factuais/semânticas e bugs reais de UX.

### `PAUSED`

- inclusão de novas fontes, produtos ou distribuições sem nova curadoria factual explícita.

### `DERIVED`

- JSONs construídos a partir dos CSVs;
- `_site`;
- relatórios automáticos de qualidade;
- planilhas/workbooks do Drive quando regenerados.

### `HISTORICAL_EVIDENCE`

Materiais de fases anteriores e arquiteturas de projetos separados permanecem apenas por proveniência e não orientam desenvolvimento novo da Vitrine.

## 5. Documentação ativa

- `README.md` — entrada pública;
- `docs/PROJECT_STATE.md` — este estado canônico;
- `docs/PROJECT_SCIENTIFIC_DIRECTION.md` — direção científica;
- `docs/GOVERNANCE.md` — autoridade e gates;
- `docs/VITRINE_BOUNDARY.md` — fronteira de publicação;
- `docs/VITRINE_CANONICAL_DATA_CONTRACT.md` — schema vigente;
- `docs/VITRINE_OPERATING_MODEL.md` — operação e crescimento;
- `METHODOLOGY.md` — metodologia de curadoria;
- `CODEBOOK.md` — dicionário dos campos;
- `PRODUCT_CATALOG_MODEL.md` — modelo fonte/produto/distribuição;
- `SELECTION_AND_COVERAGE_POLICY.md` — seleção e prioridade Brasil;
- `WORKFLOW_STATUS.md` — estado corrente.

## 6. Gates contínuos

Antes de publicar mudança pública:

1. preservar IDs e relações;
2. não promover propriedades de produto para fonte;
3. não inferir metadados ausentes;
4. executar validadores de dados e frontend;
5. construir `_site` isolado;
6. testar navegador em desktop, tablet e smartphone;
7. reproduzir seleção/comparação e confirmar ausência de estado residual;
8. publicar somente após CI verde;
9. verificar o site publicado via smoke pós-deploy.

Nenhuma nova tag/release ou DOI deve ser criado sem instrução humana explícita.
