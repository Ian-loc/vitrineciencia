# Objetivos finais e critérios para release citável e DOI

## 1. Produto

A **Vitrine Ciência** é um catálogo público, estático, versionado e citável de fontes e produtos de dados científicos sobre o Brasil para pesquisa, ensino e extensão.

A Vitrine não hospeda, por padrão, cópias integrais dos datasets de terceiros. Seu produto científico original é a **curadoria estruturada**: identidade de fontes, produtos e distribuições; cobertura; acesso; formatos; versões; metodologia; licenças; limitações; evidências e datas de verificação.

## 2. Objetivo geral

Facilitar a descoberta, comparação e avaliação inicial de fontes de dados científicos relevantes ao Brasil, preservando rastreabilidade, granularidade suficiente e distinções metodológicas que reduzam interpretações incorretas.

## 3. Objetivos específicos

1. **Descoberta:** localizar fontes e produtos por tema, cobertura, formato e mecanismo de acesso.
2. **Comparação:** distinguir fonte, produto, família/série, catálogo, serviço e distribuição.
3. **Avaliação científica:** registrar escala, temporalidade, metodologia, limitações, evidência e data de verificação.
4. **Transparência:** separar fatos documentados, classificação curatorial e lacunas/ambiguidade.
5. **Reprodutibilidade:** manter tabelas canônicas, artefatos derivados, validadores, histórico Git e releases.
6. **Acessibilidade:** oferecer interface pública navegável e reutilizável sem depender de infraestrutura privada.
7. **Citação e preservação:** publicar releases estáveis com metadados coerentes e DOI.
8. **Manutenção sustentável:** permitir crescimento contínuo sem renumerar IDs, duplicar objetos ou transformar governança em fim em si mesma.

## 4. Modelo canônico atual

A autoridade ativa do projeto é o repositório:

- https://github.com/Ian-loc/vitrineciencia

A superfície pública é:

- https://ian-loc.github.io/vitrineciencia/

As tabelas canônicas são:

- `data/data_resources.csv` — fontes;
- `data/data_products.csv` — produtos;
- `data/product_distributions.csv` — distribuições.

Artefatos JSON e o site são derivados das tabelas canônicas e devem poder ser reconstruídos deterministicamente.

## 5. Estado de referência desta revisão

Em 18 de agosto de 2026, o estado materializado era:

- **125 fontes**;
- **752 produtos**;
- **783 distribuições**;
- verificação das fontes chegando a **18/08/2026**.

Essas contagens são um **snapshot**, não um requisito fixo de arquitetura nem um gate de release. O catálogo continua crescendo por lotes auditados.

## 6. Critério mínimo de completude

Uma fonte ou produto pode ser considerado suficientemente completo para materialização quando, conforme aplicável, possui:

- identidade e tipo claramente definidos;
- relação fonte → produto → distribuição válida;
- URL oficial ou mecanismo de acesso sustentado;
- cobertura espacial e temporal documentada ou explicitamente desconhecida;
- versão/coleção ou referência temporal quando necessária;
- metodologia ou natureza do objeto suficientemente descrita;
- licença/condição de uso registrada de modo conservador;
- limitações científicas e semânticas relevantes;
- evidência oficial/técnica ou acadêmica apropriada;
- data de verificação;
- ausência de duplicação material ou inferência não sustentada.

Valores desconhecidos são permitidos quando a evidência não sustenta preenchimento mais específico.

## 7. Critérios para uma release científica estável

Uma release estável candidata a DOI deve satisfazer simultaneamente:

1. tabelas canônicas validadas e sem FKs quebradas;
2. IDs únicos e preservados;
3. ausência de duplicações materiais conhecidas que alterem a interpretação do catálogo;
4. artefatos derivados reconstruídos e coerentes com o snapshot;
5. interface pública validada e publicável;
6. README, licença, `CITATION.cff`, metodologia e documentação de release coerentes;
7. autoria, ORCID, título e URL canônicos consistentes;
8. changelog/release notes suficientes para identificar o snapshot;
9. tag Git imutável da versão;
10. pacote de depósito inspecionado antes da publicação do DOI.

Nenhum número histórico de fontes, produtos ou campos é, por si só, gate de release.

## 8. Estratégia de DOI

A estratégia recomendada para a Vitrine Ciência é:

- **GitHub Pages:** produto vivo e navegável;
- **GitHub:** desenvolvimento, histórico, issues e releases;
- **Zenodo:** preservação e DOI da release científica;
- **ORCID/Lattes:** exposição profissional e citação.

O depósito deve ser do tipo **Dataset**, porque o principal objeto científico original é o catálogo curado e suas tabelas, mesmo que a release também arquive código e documentação.

Quando a integração GitHub–Zenodo estiver ativa, cada release científica importante pode receber um DOI de versão; o DOI conceitual deve representar o conjunto da Vitrine ao longo das versões.

## 9. Conteúdo mínimo do depósito

O snapshot depositado deve incluir, no mínimo:

- `data/data_resources.csv`;
- `data/data_products.csv`;
- `data/product_distributions.csv`;
- JSONs derivados necessários à reutilização;
- README;
- metodologia/codebook relevante;
- `CITATION.cff`;
- `LICENSE-DATA.md` e `LICENSE`;
- changelog ou release notes;
- versão/tag e commit-fonte claramente identificados.

O depósito não deve incluir cópias de datasets externos apenas por estarem catalogados na Vitrine.

## 10. Portões objetivos para DOI

- **G1 — identidade:** nome Vitrine Ciência, autoria, ORCID, URL e repositório canônicos coerentes.
- **G2 — integridade:** tabelas, IDs e relações validados.
- **G3 — semântica:** tipos fonte/produto/distribuição e principais limitações sem contradições bloqueantes.
- **G4 — licenças:** licença da curadoria separada das licenças dos dados externos.
- **G5 — documentação:** README, metodologia, citação e release notes consistentes.
- **G6 — publicação:** site público gerado a partir do mesmo snapshot da release.
- **G7 — imutabilidade:** tag Git criada e commit-fonte registrado.
- **G8 — depósito:** arquivos e metadados do Zenodo conferidos antes da publicação.
- **G9 — propagação:** DOI inserido em `CITATION.cff`, README, site e perfis acadêmicos após emissão.

## 11. Regra de decisão

**GO para DOI** quando G1–G8 estiverem concluídos para uma release estável e o pacote depositado puder ser reproduzido a partir do commit/tag indicado.

**NO-GO** apenas para falhas materialmente relevantes: integridade quebrada, identidade incoerente, licença incorreta, snapshot não reproduzível, tag ausente ou depósito divergente da release.

Pendências de curadoria não críticas, novos produtos elegíveis ou melhorias futuras não impedem uma release se o snapshot corrente estiver tecnicamente defensável e suas limitações estiverem explícitas.
