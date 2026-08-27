# Estado do workflow — Vitrine Ciência

Atualização: **2026-08-27** (`America/Sao_Paulo`)

## Direção ativa

A Vitrine Ciência é um catálogo público para descoberta de dados científicos relevantes ao Brasil. O modelo conceitual permanece **Fonte → Produto → Distribuição**, mas a experiência pública é **product-first**: pergunta de pesquisa → produto/dataset → comparação → fonte/proveniência → acesso original.

A fase corrente é de **QA/QC, manutenção e refinamento da experiência de descoberta**. A **expansão de novas fontes, produtos e distribuições está pausada**; sua retomada depende de instrução humana explícita e nova curadoria factual. Não há expansão automática do corpus neste pacote.

## Autoridade e snapshot

Estado corrente do snapshot científico `v1.0.0`: **135 fontes, 843 produtos e 876 distribuições**.

- repositório: `Ian-loc/vitrineciencia`;
- branch canônica: `main`;
- site: `https://ian-loc.github.io/vitrineciencia/`;
- release científica estável: `v1.0.0`;
- commit congelado: `27c545554f406b940662777e3f053e939ef3588c`;
- GitHub Release: `https://github.com/Ian-loc/vitrineciencia/releases/tag/v1.0.0`;
- Zenodo: `https://zenodo.org/records/22130831`;
- DOI: `10.5281/zenodo.22130831`;
- fontes do snapshot: `data/data_resources.csv` — **135** registros;
- produtos do snapshot: `data/data_products.csv` — **843** registros;
- distribuições do snapshot: `data/product_distributions.csv` — **876** registros;
- Drive: espelho/histórico derivado, não canônico.

A contagem de 135 corresponde a fontes, não a produtos. A `main` e a interface pública podem avançar após a release; análises reproduzíveis de `v1.0.0` devem usar a tag/commit e o depósito Zenodo.

## Estado consolidado

### Modelo científico

**CONSOLIDADO / ESTÁVEL.** Fonte, Produto e Distribuição continuam entidades distintas; a interface não promove atributos entre níveis.

### Descoberta pública

**PRODUCT-FIRST.** A busca principal abre produtos. A exploração temática contabiliza produtos. Fontes permanecem em página própria de proveniência/contexto institucional. `Sobre o acervo` é conteúdo secundário de `Sobre`.

Filtros principais: tema/variável, cobertura geográfica, período, resolução temporal, suporte espacial, resolução espacial, acesso, formato, licença e gratuidade. Filtros institucionais/operacionais ficam em seção complementar.

Busca interpretativa leve: sinônimos científicos, biomas, Brasil, anos e resolução espacial. Implementação determinística no navegador, sem LLM ou servidor.

Ranking: **relevância → dados para o Brasil → completude/documentação → origem da fonte → nome**.

### Cards e densidade

**CONSOLIDADO.** Produto é o card canônico. Onde/Quando/Escala/Acesso permanecem visíveis. O lote inicial mostra 18 produtos e a grade usa 3 colunas em desktop, 2 em tablet/desktop estreito e 1 em smartphone; a divulgação progressiva permite ampliar o conjunto sem carregar visualmente os 843 produtos de uma vez.

### Comparação

**CONSOLIDADO.** Um único estado de seleção vive em `assets/products.js`. A exportação CSV não mantém cópia da seleção. Produtos podem ser removidos dentro da comparação; fechar a janela limpa integralmente a seleção.

### Responsividade

**GATE DE PUBLICAÇÃO.** QA automática cobre 1440×1100, 820×1180 e 390×844, sem overflow horizontal e com menu responsivo funcional.

## Gates

Pipeline:

`estado vivo → correção/ajuste → validadores de dados → validação de interface → build _site → browser QA desktop/tablet/mobile → main → deploy → smoke público`

Critérios obrigatórios para o pacote product-first:

1. 135 fontes / 843 produtos / 876 distribuições preservados no snapshot `v1.0.0`;
2. busca inicial direcionada a produtos;
3. seis áreas temáticas mostrando contagens de produtos;
4. 18 cards no lote inicial com divulgação progressiva;
5. filtros científicos principais presentes e funcionais;
6. busca interpretada reconhecendo carbono/solo/Cerrado/Brasil/ano/resolução no caso de teste;
7. comparação refletindo exatamente os produtos selecionados;
8. remoção dentro da comparação;
9. reset completo ao fechar;
10. mobile/tablet sem overflow horizontal;
11. smoke pós-deploy verde.

## Estado de release e preservação

- `v1.0.0`: **PUBLICADA**;
- Git tag/GitHub Release: **CONCLUÍDOS**;
- depósito Zenodo Dataset: **CONCLUÍDO**;
- DOI `10.5281/zenodo.22130831`: **EMITIDO E PROPAGADO NO REPOSITÓRIO**;
- ORCID/Lattes e outros perfis externos: **AÇÃO ADMINISTRATIVA PENDENTE**, sem impacto sobre a imutabilidade do snapshot.

## Fora do caminho ativo

- adicionar produtos não auditados apenas para elevar contagem;
- colapsar Fonte, Produto e Distribuição;
- inferir licença, resolução ou cobertura ausentes;
- modificar retroativamente a release `v1.0.0`;
- criar nova release/tag/DOI sem instrução humana explícita.
