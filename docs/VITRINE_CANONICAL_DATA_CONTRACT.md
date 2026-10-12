# Vitrine Ciência — contrato de dados físico e transição pública

**Status:** contrato físico legado ativo; modelo público v1 implementado; v2 planejado  
**Atualização:** 12 de outubro de 2026

## 1. Escopo

Este documento define como interpretar o contrato físico `DR → DP → DD` no estado atual da Vitrine.

O contrato continua necessário para:

- preservar IDs;
- validar o catálogo vivo;
- reproduzir a release histórica;
- gerar o site;
- manter rastreabilidade durante a transição para um modelo público mais expressivo.

Ele **não é a ontologia final**.

## 2. Estado material atual

As tabelas canônicas são:

- `data/data_resources.csv`;
- `data/data_products.csv`;
- `data/product_distributions.csv`.

O catálogo vivo contém:

- 58 registros DR;
- 11 produtos detalhados DP;
- 19 distribuições DD.

O núcleo `DR0001–DR0051` permanece preservado. As entradas pós-core são `DR0136–DR0142`.

A expansão histórica `v1.0.0` com 135/843/876 permanece em quarentena e não define o runtime atual.

## 3. Interpretação dos IDs

`DR####` é identificador estável de **Registro da Vitrine**.

Não prova que o objeto externo seja:

- provedor;
- plataforma;
- dataset;
- catálogo;
- programa;
- serviço.

`DP######` identifica um produto detalhado no contrato físico atual.

`DD######` identifica uma distribuição/forma concreta de acesso associada ao produto.

IDs não são reciclados.

## 4. Modelo público v1

O contrato `schema/public-record-v1.json` é derivado do estado canônico e materializa:

- uma página por DR;
- JSON individual;
- índice público agregado;
- rotas de acesso derivadas;
- produtos e distribuições quando existentes.

Esse modelo é estável como representação pública atual.

## 5. Limitação do v1

O v1 ainda comprime duas entidades:

```
Registro da Vitrine
Recurso externo descrito
```

O v2 deverá separar:

```
record
  └── describes → resource
```

Tipos como iniciativa, plataforma, base ou rede pertencem ao `resource`, não ao identificador catalográfico `DR`.

## 6. Estrutura alvo mínima

O contrato lógico alvo deverá comportar:

- `record`;
- `resource`;
- `offering/product`;
- `version/collection`;
- `distribution`;
- `data_service`;
- `access_route`;
- `agent/provenance role`;
- `reference/evidence`;
- `curation`.

Nem toda entidade precisa virar tabela imediatamente.

## 7. Regras permanentes

- identidade e proveniência devem ser preservadas;
- propriedades específicas não devem ser promovidas indevidamente ao nível do recurso;
- formato, protocolo e ferramenta são conceitos distintos;
- API/serviço não é dataset por padrão;
- viewer e documentação não comprovam distribuição;
- desconhecido não significa não;
- licença deve ser registrada no nível mais específico verificado;
- produto não é sinônimo de arquivo;
- versão deve ser distinguida quando afeta citação ou reprodutibilidade;
- CI comprova conformidade estrutural, não verdade externa.

## 8. Rotas de acesso

As rotas são representadas explicitamente em `data/access_routes.json`, sob `schema/access-routes-v1.json`.

Cada objeto registra, conforme aplicável:

- alvo;
- tipo;
- URL;
- protocolo;
- formato;
- autenticação;
- condição de acesso;
- licença;
- data de verificação;
- estado operacional.

A classificação A–E é uma avaliação de acesso e não deve ser confundida com o tipo da rota.

Durante a transição, `homepage_url`, `data_access_url` e as tabelas DD permanecem sincronizados e são usados por QA de compatibilidade. O read model v2, porém, consome `data/access_routes.json` diretamente.

Referências científicas e fontes de verificação são excluídas dessa autoridade e representadas em `references`.

## 9. Relação com API/federação

O contrato público futuro deve ser independente do mecanismo de ingestão.

Hoje:

`CSV/auditoria → read model → HTML/JSON`

Futuramente:

`API externa → staging → normalização → curadoria → read model → HTML/JSON/API`

A API da Vitrine não está implementada em produção.

## 10. Gate de evolução

`public-record-v2` só deve substituir o v1 quando:

1. record e resource estiverem separados;
2. houver compatibilidade com os 58 registros;
3. URLs públicas forem preservadas;
4. rotas forem semanticamente explícitas;
5. produtos/versões não forem inflados artificialmente;
6. validadores cobrarem o novo contrato;
7. HTML e JSON continuarem derivados do mesmo objeto.

O Integration Registry vem **depois** desse gate.

## 11. Release histórica

A release `v1.0.0`, sua tag, DOI e depósito permanecem imutáveis e reproduzíveis. A transição do modelo corrente não altera retrospectivamente essa release.

Referências:

- `CODEBOOK.md`;
- `docs/PROJECT_STATE.md`;
- `docs/PUBLIC_RECORD_PAGES_V1.md`;
- `docs/WEB_API_EVOLUTION_PLAN.md`.
