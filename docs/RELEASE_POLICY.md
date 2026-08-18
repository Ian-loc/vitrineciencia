# Política de releases — Vitrine Ciência

## Objetivo

Releases transformam o catálogo vivo em snapshots identificáveis, citáveis e reproduzíveis. O site pode continuar evoluindo entre releases; uma análise reprodutível deve indicar release/tag ou commit efetivamente utilizado.

## Estado atual

Em 18/08/2026, `CITATION.cff` permanece com `version: unreleased`. O snapshot operacional contém **125 fontes, 756 produtos e 787 distribuições**. Essa contagem não é requisito de versão.

## Versionamento

O projeto utiliza versionamento semântico:

- **patch** (`x.y.z+1`): correções compatíveis de dados, documentação, interface ou validação;
- **minor** (`x.y+1.0`): crescimento compatível relevante ou evolução de contrato que preserve compatibilidade documentada;
- **major** (`1.0.0` e seguintes): marco de estabilidade/contrato deliberadamente assumido ou mudança incompatível.

A versão não deve ser derivada automaticamente do número de fontes/produtos.

## Requisitos mínimos

Toda release científica deve incluir:

1. três tabelas canônicas validadas;
2. artefatos derivados regenerados do commit da release;
3. changelog/release notes;
4. `CITATION.cff` coerente;
5. interface e artefato Pages validados quando incluídos;
6. licenças e documentação pública coerentes;
7. tag Git imutável e GitHub Release;
8. registro do commit-fonte.

## Conteúdo compatível com patch/minor

Pode incluir, desde que o contrato permaneça compatível:

- correção de links/metadados;
- novas fontes, produtos e distribuições;
- correção de identidade/cobertura/licença;
- melhorias de interface e acessibilidade;
- QA/CI;
- documentação e higiene de repositório.

Uma nova fonte deve preservar schema, relações e classificação Brasil.

## Mudança de schema

Mudança incompatível exige decisão própria, atualização coordenada de contrato, codebook, metodologia, validadores, migração dos registros e interface. Não deve ser introduzida apenas para acomodar uma fonte específica.

## Release estável e DOI

Uma release `1.0.0` representa um snapshot científico e operacional tecnicamente defensável; não exige “curadoria perfeita” nem encerra a expansão futura.

DOI deve identificar um snapshot imutável arquivado como **Dataset**. Requisitos adicionais:

- integridade e identidade coerentes;
- licença do próprio catálogo confirmada;
- documentação e citação alinhadas;
- snapshot reproduzível;
- pacote inspecionado antes do depósito;
- correspondência entre tag e arquivos depositados;
- decisão humana explícita de publicação.

Consulte `FINAL_OBJECTIVES_AND_DOI_GATES.md`.

## Google Drive

O Drive é opcional para release. Um espelho pode ser regenerado para conveniência, mas não deve bloquear uma release válida. Se incluído/atualizado, deve declarar commit-fonte, data, escopo e contagens e passar comparação contra as tabelas canônicas.

O workbook legado atualmente no Drive não está sincronizado com a Vitrine de 18/08/2026 e deve permanecer rotulado como histórico até regeneração integral.

## Pós-release

Após uma release:

- manter a tag imutável;
- corrigir erros futuros em nova release;
- atualizar DOI/README/CITATION quando aplicável;
- preservar citação das fontes/datasets originais;
- continuar curadoria no `main` sem alterar retroativamente o snapshot publicado.
