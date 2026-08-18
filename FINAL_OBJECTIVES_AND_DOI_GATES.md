# Objetivos finais e critérios para release citável e DOI

## 1. Produto

A **Vitrine Ciência** é um catálogo público, estático, versionável e citável de fontes e produtos de dados científicos relevantes ao Brasil para pesquisa, ensino e extensão.

A Vitrine não hospeda, por padrão, cópias integrais dos datasets de terceiros. Seu produto científico original é a **curadoria estruturada**: identidade de fontes, produtos e distribuições; cobertura; acesso; formatos; versões/coleções; metodologia quando disponível; licenças; limitações; evidências e datas de verificação.

## 2. Objetivo geral

Facilitar descoberta, comparação de metadados e avaliação inicial de fontes e produtos relevantes ao Brasil, preservando rastreabilidade, granularidade suficiente e distinções metodológicas que reduzam interpretações incorretas.

## 3. Objetivos específicos

1. **Descoberta:** localizar fontes e produtos por tema, cobertura e mecanismo de acesso.
2. **Comparação:** distinguir fonte, produto, catálogo/serviço e distribuição.
3. **Avaliação científica:** registrar suporte, temporalidade, natureza do dado, limitações e evidência.
4. **Transparência:** separar fatos documentados, classificação curatorial e lacunas.
5. **Reprodutibilidade:** manter tabelas canônicas, validadores, histórico Git e releases.
6. **Acessibilidade:** oferecer interface pública sem infraestrutura privada obrigatória.
7. **Citação e preservação:** publicar snapshots estáveis com metadados e DOI quando decidido.
8. **Manutenção sustentável:** permitir crescimento sem renumerar IDs ou transformar governança em fim em si mesma.

## 4. Modelo canônico

- repositório: https://github.com/Ian-loc/vitrineciencia
- site: https://ian-loc.github.io/vitrineciencia/
- `data/data_resources.csv` — fontes;
- `data/data_products.csv` — produtos;
- `data/product_distributions.csv` — distribuições.

JSONs e o site são derivados deterministicamente.

## 5. Snapshot de referência

Em **18 de agosto de 2026**:

- **125 fontes**;
- **752 produtos**;
- **783 distribuições**;
- IDs correntes chegam a `DR0125`, `DP000756` e `DD000787`, com lacunas preservadas;
- verificações de fonte registradas até **2026-08-18**.

Essas contagens são snapshot, não gate, teto ou requisito arquitetural.

## 6. Completude suficiente

Uma entrada pode ser materializada quando, conforme aplicável, possui:

- identidade e tipo definidos;
- relação fonte → produto → distribuição válida;
- URL oficial/rota de acesso sustentada;
- cobertura espacial/temporal documentada ou explicitamente desconhecida;
- coleção/versão quando necessária;
- natureza/metodologia suficientemente descrita para não induzir interpretação falsa;
- licença/condição de uso registrada conservadoramente;
- limitações relevantes;
- evidência apropriada;
- data de verificação;
- ausência de duplicação material conhecida sem tratamento.

Desconhecido é permitido quando a evidência não sustenta precisão maior.

## 7. Critérios para release científica estável

Uma release candidata a DOI deve satisfazer:

1. tabelas canônicas validadas e sem relações quebradas;
2. IDs únicos e preservados;
3. duplicações materiais conhecidas resolvidas ou tratadas de forma explícita;
4. artefatos derivados reconstruídos do mesmo snapshot;
5. interface pública validada;
6. README, licenças, `CITATION.cff`, metodologia e documentação coerentes;
7. autoria, ORCID, título e URL canônicos consistentes;
8. changelog/release notes suficientes;
9. tag Git imutável;
10. pacote de depósito inspecionado.

Novas possibilidades de curadoria ou melhorias não críticas não impedem release de um snapshot tecnicamente defensável.

## 8. Estratégia de preservação

- **GitHub Pages:** produto vivo e navegável;
- **GitHub:** desenvolvimento, histórico, tags e releases;
- **Zenodo:** preservação e DOI do snapshot científico;
- **ORCID/Lattes:** exposição profissional/citação após emissão.

O depósito deve ser do tipo **Dataset**, porque o objeto científico principal é o catálogo curado e suas tabelas.

## 9. Conteúdo mínimo do depósito

- três CSVs canônicos;
- JSONs derivados necessários à reutilização;
- README;
- metodologia/codebook;
- `CITATION.cff`;
- `LICENSE-DATA.md` e `LICENSE`;
- changelog/release notes;
- versão/tag e commit-fonte.

Não incluir cópias de datasets externos apenas por estarem catalogados.

## 10. Gates objetivos para DOI

- **G1 — identidade:** nome, autoria, ORCID, URL e repositório coerentes.
- **G2 — integridade:** tabelas, IDs e relações validados.
- **G3 — semântica:** fonte/produto/distribuição e limitações sem contradições bloqueantes.
- **G4 — licenças:** curadoria separada das licenças externas.
- **G5 — documentação:** README, metodologia, codebook, citação e release notes consistentes.
- **G6 — publicação:** site construído do mesmo snapshot.
- **G7 — imutabilidade:** tag e commit registrados.
- **G8 — depósito:** arquivos/metadados do Zenodo conferidos antes de publicar.
- **G9 — propagação:** DOI inserido no projeto e perfis após emissão.

## 11. Regra de decisão

**GO para DOI** quando G1–G8 estiverem concluídos para um snapshot estável, reproduzível e tecnicamente defensável, após decisão humana explícita de release/depósito.

**NO-GO** para falhas materialmente relevantes: integridade quebrada, identidade incoerente, licença do próprio catálogo incorreta, snapshot não reproduzível, tag ausente ou depósito divergente.

O Drive não é gate de DOI: um espelho desatualizado deve ser rotulado como tal e pode ser regenerado depois sem invalidar uma release correta no GitHub/Zenodo.
