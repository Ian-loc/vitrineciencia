# Rotas de acesso canônicas — access-routes-v1

**Status:** contrato canônico ativo  
**Autoridade:** `data/access_routes.json`  
**Schema:** `schema/access-routes-v1.json`  
**Data de estabelecimento:** 12 de outubro de 2026

## 1. Problema resolvido

Até esta etapa, o papel das rotas públicas era reconstruído durante o build a partir de campos legados como `homepage_url`, `data_access_url`, `access_documentation_url`, auditorias A–E e distribuições DD.

Esse mecanismo permitiu construir as primeiras páginas, mas criava uma dependência indesejada: o renderer precisava inferir o significado de cada URL.

O `access-routes-v1` transforma essa inferência em dado curado explícito.

## 2. Unidade

Uma rota de acesso representa:

- um destino concreto HTTPS; ou
- um estado explícito de acesso sem URL, quando a avaliação principal é E.

Cada rota possui identidade própria e aponta para:

- um **recurso catalogado**; ou
- uma **offering**.

A mesma URL pode cumprir mais de um papel. Nesses casos existe uma única rota com múltiplos `roles`.

## 3. O que pertence a access_routes

Papéis de recurso:

- `direct_data`;
- `data_page`;
- `data_service`;
- `viewer`;
- `unconfirmed_access`;
- `official_site`;
- `access_documentation`.

No nível de offering:

- `distribution`.

## 4. O que não pertence a access_routes

Não são rotas de acesso:

- referência científica;
- artigo;
- documentação metodológica usada como evidência;
- fonte usada para verificação curatorial.

Esses objetos permanecem em `references[]` no read model v2.

Essa separação elimina a ambiguidade anterior em que uma URL de evidência podia aparecer no mesmo array das rotas de acesso.

## 5. Relação com A–E

A–E continua sendo uma **avaliação curatorial da rota principal**, não um tipo de entidade.

Cada DR possui exatamente uma rota principal no nível do recurso:

- A → `direct_data`;
- B → `data_page`;
- C → `data_service`;
- D → `viewer`;
- E → `unconfirmed_access`.

O catálogo vivo preserva:

- A=2;
- B=39;
- C=0;
- D=14;
- E=3.

Uma rota principal D pode coexistir com serviços programáticos secundários. A classificação principal não apaga outras capacidades.

## 6. Identificadores

As rotas principais de recurso usam:

`DR####-ACCESS`

Rotas secundárias usam, quando distintas:

`DR####-SITE`

`DR####-ACCESS-DOC`

Distribuições existentes preservam seus IDs:

`DD######`

A preservação dos DD evita criar uma segunda identidade para a mesma forma de distribuição já curada.

## 7. Campos

Cada rota pode registrar:

- `route_id`;
- `record_id`;
- `target_type`;
- `target_id`;
- `route_type`;
- `roles`;
- `label`;
- `url`;
- `primary`;
- `access_assessment`;
- `protocol`;
- `format`;
- `tool`;
- `free_download`;
- `authentication_required`;
- `access_conditions`;
- `license`;
- `attribution_required`;
- `subset_support`;
- `notes`;
- `verified_at`;
- `status`;
- `source`.

Campos específicos podem ser `null` quando não são aplicáveis ou ainda não foram confirmados.

## 8. Migração inicial

O arquivo inicial foi produzido uma única vez a partir de:

- `data/data_resources.csv`;
- `data/product_distributions.csv`;
- `data/static_core_51_access_audit.json`;
- `data/post_core_access_audit.json`.

Baseline:

- 58 recursos;
- 11 offerings/produtos detalhados;
- 19 distribuições;
- 135 rotas no nível do recurso;
- 154 rotas totais.

Após o gate de migração, `data/access_routes.json` passa a ser a autoridade de rotas.

Os campos legados continuam temporariamente sincronizados para compatibilidade e são usados pelo validador como proteção contra regressões durante a transição.

## 9. Read model público

`scripts/build_public_records_v2.py` não infere mais as rotas do v2.

Ele:

1. lê `data/access_routes.json`;
2. seleciona as rotas do DR;
3. associa distribuições às offerings;
4. incorpora os objetos sem reclassificá-los;
5. declara `curation.access_route_authority = data/access_routes.json`.

Consequentemente, HTML e JSON consomem a mesma autoridade.

## 10. Validação

`scripts/validate_access_routes.py` exige, entre outros pontos:

- IDs únicos;
- todos os 58 DR cobertos;
- exatamente uma rota principal por DR;
- classe principal coincidente com as auditorias A–E;
- URL principal compatível com o campo legado durante a migração;
- site oficial e documentação de acesso preservados;
- nenhuma duplicação da mesma URL no nível do recurso;
- referências/evidências fora de `access_routes`;
- todos os 19 DD preservados;
- target offering válido;
- atributos de distribuição iguais ao catálogo físico canônico;
- URL presente sempre HTTPS.

## 11. Relação com o Integration Registry

`access_routes` e Integration Registry são objetos diferentes.

**Access route** responde:

> Onde e de que forma o usuário acessa este recurso ou produto?

**Integration Registry** responderá:

> Como a Vitrine consulta tecnicamente este provedor para verificar ou atualizar metadados?

Um endpoint pode aparecer nos dois contextos, mas os papéis não são equivalentes.

## 12. Próxima evolução

Depois deste contrato, as próximas melhorias estruturais são:

1. revisar versões/coleções materialmente relevantes;
2. estruturar papéis de proveniência;
3. criar o Integration Registry;
4. somente depois implementar conectores/harvesting.

A API futura deverá expor as rotas canônicas presentes no read model, não reconstruí-las novamente.
