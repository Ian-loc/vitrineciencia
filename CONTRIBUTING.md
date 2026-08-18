# Como contribuir — Vitrine Ciência

Contribuições são bem-vindas para corrigir registros, propor fontes/produtos, melhorar a interface e fortalecer validações.

## Princípios

1. `main` é a autoridade.
2. As fontes de dados canônicas são `data/data_resources.csv`, `data/data_products.csv` e `data/product_distributions.csv`.
3. JSONs e `_site` são derivados e não devem ser editados manualmente.
4. Evidência deve sustentar a afirmação específica alterada.
5. Propriedades de produto/distribuição não devem ser generalizadas para a fonte inteira.
6. Novas fontes devem demonstrar vínculo com o Brasil ou justificativa explícita.
7. IDs existentes são estáveis e não são reciclados.
8. Desconhecido é preferível a inferência sem base.

## Propor nova fonte

Informar:

- nome e instituição responsável;
- homepage e acesso aos dados;
- vínculo territorial com o Brasil;
- descrição objetiva;
- tipos de produtos relevantes;
- condições de acesso e autenticação;
- licença ou indicação de que não foi localizada;
- documentação oficial atual;
- limitações relevantes;
- classificação Brasil sugerida, quando possível.

A inclusão deve passar por duplicidade/escopo, revisão factual, produtos/distribuições pertinentes e validação.

## Propor produto

Indicar:

- fonte pai (`resource_id`);
- identidade e diferença material em relação aos produtos existentes;
- `product_kind` e `enumeration_scope`;
- cobertura e suporte/resolução quando sustentados;
- temporalidade/atualização;
- coleção/versão quando relevante;
- metodologia e limitações;
- ao menos uma rota de distribuição.

Não criar produto apenas para outro arquivo, banda, formato, tile ou endpoint equivalente.

## Corrigir registro

Toda correção factual deve indicar:

- ID afetado (`DR`, `DP` ou `DD`);
- campo/valor atual;
- valor proposto;
- URL da evidência;
- data de acesso/verificação;
- justificativa curta;
- impacto em relações, classificação Brasil ou distribuições.

Artigo de aplicação não é prova suficiente para licença, endpoint, autenticação ou versão atual.

## Fluxo

1. criar branch a partir de `main`;
2. limitar escopo;
3. editar arquivos canônicos/documentação-fonte;
4. executar validações pertinentes;
5. revisar o diff;
6. abrir PR com evidências e testes;
7. aguardar gates aplicáveis;
8. verificar publicação quando o delta for público.

## Validações principais

```bash
python3 scripts/validate_brazil_scope.py
python3 scripts/validate_product_catalog.py
python3 scripts/build_catalog.py
python3 scripts/audit_link_roles.py --write
python3 scripts/validate_vitrine.py
python3 scripts/build_site_artifact.py
```

Para frontend, execute também os checks JavaScript e QA de navegador aplicáveis.

## Pull request

O PR deve declarar:

- o que mudou e por quê;
- registros/usuários afetados;
- evidências;
- validações executadas;
- efeitos na superfície pública;
- o que ficou fora do escopo.

Alterações sem relação direta devem ser separadas.

## Drive

Não corrija o workbook do Drive como fonte primária. Primeiro materialize a mudança no GitHub; depois um espelho pode ser regenerado e verificado conforme `DRIVE_MIRROR_CONTRACT.md`.
