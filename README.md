# Vitrine Ciência

**Catálogo público, estático, versionado e citável de produtos e fontes de dados científicos relevantes ao Brasil para pesquisa, ensino e extensão.**

A Vitrine Ciência facilita a descoberta e a triagem de dados. A experiência pública é **product-first**: o usuário procura primeiro o produto/dataset capaz de responder à pergunta de pesquisa e, em seguida, consulta a fonte para proveniência, responsabilidade institucional e documentação. O modelo científico interno continua rigorosamente separado em **Fonte → Produto → Distribuição**.

## Produto público e autoridade

- site: https://ian-loc.github.io/vitrineciencia/
- repositório canônico: https://github.com/Ian-loc/vitrineciencia
- branch canônica de desenvolvimento: `main`
- candidata à primeira release científica estável: `v1.0.0` (`release/v1.0.0`)
- fontes: `data/data_resources.csv`
- produtos: `data/data_products.csv`
- distribuições/acessos: `data/product_distributions.csv`
- classificação territorial: `data/brazil_scope_priorities.json`
- código: MIT
- metadados e curadoria original: CC BY 4.0

### Snapshot candidato v1.0.0

- **135 fontes**;
- **843 produtos**;
- **876 distribuições**;
- os identificadores correntes chegam a `DR0135`, `DP000861` e `DD000894`, pois IDs removidos/consolidados não são reciclados;
- verificações de fontes registradas até **2026-08-19**.

**135 é a contagem de fontes, não de produtos.** O catálogo público de produtos contém 843 registros. O pacote de UX product-first não adiciona produtos não auditados nem infla contagens; ele torna os 843 produtos já canônicos diretamente descobríveis.

## Modelo científico vigente

```text
Fonte (DR####)
  └── Produto (DP######)
        └── Distribuição (DD######)
```

- **Fonte:** provedor, plataforma, programa, repositório ou infraestrutura; é contexto de proveniência.
- **Produto:** dataset, série, coleção, catálogo, serviço ou oferta materialmente distinta; é a unidade principal de descoberta pública.
- **Distribuição:** rota concreta de acesso ao produto, por exemplo arquivo, API, WMS/WFS, aplicação ou outro serviço.

A interface não colapsa esses níveis. A mudança é apenas na ordem de descoberta: **pergunta → produto → comparação → fonte/proveniência → acesso original**.

## Descoberta pública

A página pública prioriza:

1. tema / variável;
2. cobertura geográfica;
3. período;
4. resolução temporal;
5. escala / suporte espacial;
6. resolução espacial;
7. forma de acesso;
8. formato;
9. licença e gratuidade.

Fonte/provedor, tipo de produto, autenticação, estado, origem e disponibilidade específica para o Brasil permanecem como filtros complementares. A busca interpreta de forma determinística termos científicos e sinônimos, biomas, `Brasil`, anos e resoluções espaciais; não depende de LLM nem de servidor.

O ranking padrão segue: **relevância da consulta → disponibilidade de dados para o Brasil → completude/documentação → origem da fonte → nome**.

Cada card de produto mantém visíveis quatro dimensões de triagem: **Onde? · Quando? · Escala? · Acesso?**. Metodologia, limitações, licença, versão, proveniência e formas detalhadas de acesso permanecem disponíveis na expansão do card.

## Uso científico

Antes de utilizar um produto catalogado, confirme no provedor original:

- versão/coleção efetivamente usada;
- método e significado da variável;
- suporte/resolução espacial e temporal;
- licença, atribuição e condições de acesso;
- incertezas, limitações e atualizações posteriores.

A presença na Vitrine não certifica qualidade universal, comparabilidade ou adequação a uma análise específica.

## Manutenção e QA

Mudanças em `main` devem preservar integridade dos IDs e relações, geração determinística dos artefatos públicos e isolamento de `_site`. O CI valida dados, HTML/JavaScript, fronteira pública e comportamento em navegador. A QA visual cobre desktop, tablet e smartphone e inclui busca interpretativa, filtros, densidade dos cards, comparação, remoção de produtos e reset da seleção ao fechar.

Documentação ativa:

- `docs/PROJECT_STATE.md` — estado canônico do projeto;
- `docs/PROJECT_SCIENTIFIC_DIRECTION.md` — direção científica;
- `docs/VITRINE_CANONICAL_DATA_CONTRACT.md` — contrato de dados;
- `docs/VITRINE_OPERATING_MODEL.md` — operação e gates;
- `WORKFLOW_STATUS.md` — estado corrente e prioridades;
- `FINAL_OBJECTIVES_AND_DOI_GATES.md` — release citável e DOI;
- `RELEASE_NOTES_v1.0.0.md` — notas da candidata à primeira release científica estável.

## Release e citação

O snapshot `v1.0.0` está preparado como candidato à primeira release científica estável, mas ainda não possui tag Git imutável nem DOI. Até a publicação formal da release, análises reproduzíveis devem registrar o commit efetivamente utilizado e também citar a fonte/dataset original.

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. GitHub, 2026.

ORCID: https://orcid.org/0000-0003-1164-9318
