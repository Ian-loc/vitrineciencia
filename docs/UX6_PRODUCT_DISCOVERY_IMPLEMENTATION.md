# UX6 — descoberta e comparação de produtos

## Status

**Implementado e ampliado.** Este documento descreve a camada pública de produtos da Vitrine após a fase piloto. Em 18/08/2026, a interface opera sobre **125 fontes, 756 produtos e 787 distribuições**; não está mais restrita a TerraBrasilis/Google Earth Engine nem ao antigo baseline de 51 fontes.

## Objetivo

Transformar a camada fonte → produto → distribuição em experiência pública de descoberta científica sem expandir desnecessariamente o schema.

## Produto implementado

- página `products.html` separada do catálogo de fontes;
- `data/data_products.json` gerado no build;
- associação explícita produto → fonte → distribuições;
- busca por nomes, descrições, palavras-chave, fonte, formatos e protocolos;
- filtros e estado navegável;
- comparação de produtos;
- exposição de suporte/resolução espacial, cobertura/temporalidade, versão/coleção, origem e limitações;
- detalhamento das distribuições com URL, formato, protocolo, ferramenta, autenticação, licença e acesso;
- navegação integrada entre Fontes, Produtos, Análise e Método.

## Regras vigentes

- fonte, produto e distribuição são unidades distintas;
- três CSVs são canônicos; JSONs são derivados;
- formatos diferentes do mesmo produto não geram produto novo por si só;
- resolução não é inferida pelo visualizador;
- observação, previsão, indicador, classificação, catálogo e serviço permanecem semanticamente distintos;
- licença/provedor são registrados no nível mais específico disponível;
- megacatálogos usam enumeração seletiva ou `external_index`;
- a interface não certifica comparabilidade científica universal.

## Validação

O pipeline deve exigir, conforme o delta:

1. `validate_brazil_scope.py`;
2. `validate_product_catalog.py`;
3. `build_catalog.py`;
4. auditoria de papéis dos links;
5. validação geral da Vitrine;
6. build de `_site`;
7. sintaxe JavaScript;
8. QA de navegador/visual quando a interface mudar;
9. smoke pós-deploy.

## Evolução

A expansão ocorre fonte por fonte e produto por produto dentro do contrato 34/24/15. Melhorias futuras devem priorizar usabilidade, busca, filtros e clareza de metadados; mudança de schema só deve ocorrer se houver necessidade material recorrente.

## GitHub Pages

A publicação oficial usa GitHub Actions. O artefato público e sua fronteira são definidos em `docs/VITRINE_BOUNDARY.md` e `scripts/build_site_artifact.py`.
