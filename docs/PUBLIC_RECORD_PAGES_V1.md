# Páginas públicas de registro — contrato v1

**Status:** decisão arquitetural implementada na camada pública estática  
**Unidade pública:** `registro da Vitrine` (`DR####`)  
**Rota:** `/registros/<resource_id em minúsculas>/`

## 1. Decisão

A Vitrine Ciência publica uma página persistente por **registro**, e não uma página por dataset, arquivo, produto, release, asset, camada, cena ou endpoint.

O registro é a unidade agregadora da navegação pública. Ele preserva a identidade histórica `DR####` e pode representar, conforme a evidência, uma iniciativa, plataforma, catálogo, infraestrutura, base/coleção, rede/observatório ou referência.

Elementos subordinados podem ser descritos dentro da página:

- produtos e famílias de dados;
- coleções e versões/releases;
- distribuições e arquivos;
- serviços de dados e APIs;
- visualizadores;
- metodologia e documentação;
- publicações e evidências.

Esses elementos **não criam páginas públicas independentes por padrão**. A granularidade pode aumentar no modelo de dados sem aumentar a profundidade da navegação.

## 2. Hierarquia pública

A experiência pública segue:

```
pergunta científica
  → exploração dos registros
    → página do registro
      → produto/coleção/release (quando descrito)
        → distribuição, serviço ou visualizador
          → provedor original
```

A navegação pública usa o termo **registro** porque `DR####` não representa uma única classe ontológica.

## 3. Tipos públicos de registro

Os tipos públicos são deliberadamente mais amplos que a tipagem semântica interna:

1. **Iniciativa ou programa de dados**
2. **Plataforma ou sistema de informação**
3. **Catálogo ou repositório de dados**
4. **Infraestrutura ou serviço de dados**
5. **Base ou coleção de dados**
6. **Rede ou observatório**
7. **Registro, guia ou referência**

A tipagem detalhada permanece preservada para curadoria. O mapeamento para a interface está em `schema/public-record-v1.json`.

Exemplo: MapBiomas Brasil é tratado publicamente como **Iniciativa ou programa de dados**; suas famílias de mapas, tabelas e produtos podem ser enriquecidas dentro do mesmo registro sem gerar novas páginas de alto nível.

## 4. Estrutura das páginas

Cada página é gerada automaticamente e contém blocos condicionais:

- Sobre este registro
- Como acessar
- O que você encontra aqui
- Cobertura espacial e temporal
- Produtos, coleções e releases descritos em detalhe
- Possibilidades de uso em pesquisa
- Cuidados e limitações
- Proveniência
- Condições de uso e licença
- Referências e documentação
- Curadoria da Vitrine

A ausência de um produto detalhado não é preenchida artificialmente. O usuário é informado de que a Vitrine ainda não enumerou itens nesse nível.

## 5. Rotas de acesso

Links deixam de ser tratados apenas como campos soltos. A representação pública constrói objetos de rota com:

- identificador da rota;
- URL;
- papel(is);
- rótulo em português;
- indicação de rota principal;
- classe de acesso A–E quando aplicável;
- data de verificação.

Papéis atuais:

- dado direto;
- página de dados;
- serviço de dados;
- visualizador/página de consulta;
- acesso ainda não confirmado;
- site oficial;
- documentação de acesso;
- referência científica/técnica;
- fonte usada na verificação.

Se a mesma URL cumprir mais de um papel, ela permanece uma única rota com múltiplos papéis.

## 6. Relação com produtos e distribuições

O modelo físico continua preservando `DR → DP → DD` por compatibilidade.

Nas páginas públicas:

- `DR` define a página agregadora;
- `DP` aparece como produto/coleção/release subordinado;
- `DD` aparece como forma de acesso do produto;
- serviços, viewers e documentos são apresentados de acordo com sua função real.

Atualmente os 11 produtos detalhados pertencem a apenas dois registros. Isso não impede a geração das demais páginas.

## 7. Representação estática para futura API

O build produz:

- `/data/public_records.json` — índice completo da camada pública;
- `/data/registros/dr####.json` — representação individual;
- `/registros/dr####/` — representação HTML.

HTML e JSON são derivados do mesmo objeto público.

Isso cria o contrato necessário para uma API futura sem tornar a página dependente de APIs externas.

### Estratégia futura

O comportamento planejado é **static-first / stale-while-revalidate**:

1. a página HTML e o JSON estático respondem imediatamente;
2. uma camada futura pode avaliar se o registro está vencido;
3. o acesso do usuário pode disparar uma atualização assíncrona na origem;
4. falhas da API externa não impedem a consulta ao snapshot;
5. respostas novas entram em staging, validação e curadoria;
6. somente dados aceitos substituem o snapshot público.

Endpoint conceitual futuro:

`GET /api/v1/records/{resource_id}`

O motor de atualização não deve escrever diretamente no estado público apenas porque um usuário abriu uma página.

## 8. Lições de plataformas externas

A decisão acompanha padrões observados em infraestruturas maduras:

- Planet distingue **coleções, itens e assets**, mantendo produtos e formas de entrega subordinados à organização superior do catálogo: https://docs.planet.com/develop/apis/data/
- STAC distingue **Collection, Item e Asset**, permitindo navegação hierárquica sem transformar cada asset em coleção: https://stacspec.org/
- GBIF separa **dataset**, organização, registros de ocorrência e downloads derivados; páginas de dataset são alimentadas pelo Registry API, enquanto downloads possuem identidade própria: https://techdocs.gbif.org/en/openapi/v1/registry-principal-methods

A Vitrine adota a mesma ideia estrutural, mas preserva `DR####` como unidade pública transitória e persistente até a ontologia canônica futura estar estabilizada.

## 9. Regras de idioma

A interface usa português brasileiro.

Rótulos públicos não expõem nomes internos como `entity_type`, `source_origin`, `access_role` ou `dataset_page`.

Termos técnicos consolidados permanecem quando necessários, por exemplo: API REST, STAC, WFS, GeoTIFF, Shapefile, NetCDF e Google Earth Engine.

Estados públicos:

- `sim` → **Sim**
- `não` → **Não**
- `parcial` → **Parcial**
- `desconhecido` → **Não confirmado**
- `não se aplica` → **Não se aplica**

## 10. QA e persistência

A publicação só é válida quando:

- o conjunto das páginas é exatamente igual ao conjunto dos IDs canônicos vivos;
- cada registro possui exatamente uma página e um JSON individual;
- cada página possui canonical próprio, um `h1`, um `main` e seções obrigatórias;
- cada registro possui exatamente uma rota principal;
- produtos e distribuições subordinados preservam as contagens canônicas;
- o sitemap contém todas as páginas;
- o artefato continua funcional sem consultar APIs externas.

A página `/registros/dr####/` deve sobreviver à futura decomposição ontológica do registro em Provider, Platform, Dataset, Distribution, DataService etc. Ela é uma superfície pública persistente da curadoria da Vitrine, não a ontologia em si.
