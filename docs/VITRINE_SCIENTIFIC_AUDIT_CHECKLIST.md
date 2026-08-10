# Vitrine Ciência — checklist adversarial de auditoria científica

Status: **ACTIVE QA CHECK**

Aplicar antes de consolidar cada fila de correções factual.

## 1. Identidade e granularidade

- a afirmação descreve a fonte/plataforma inteira ou apenas um produto/componente?
- uma propriedade específica de dataset foi promovida indevidamente ao nível da fonte?
- a entrada continua representando uma entidade materialmente útil sem fragmentação excessiva?

## 2. Acesso e autenticação

Verificar separadamente:

- consulta pública;
- download;
- API;
- acesso antecipado/operacional;
- área administrativa/restrita.

Nunca usar `sim`/`não` de autenticação com base apenas em um desses canais quando a entrada agrega vários. Quando coexistem acesso público e canal autenticado material, considerar `parcial` se esse for o vocabulário canônico adequado.

## 3. Formato × protocolo × ferramenta × interface

- CSV, JSON, GeoJSON, GeoTIFF, Shapefile, KML etc. → `data_formats`;
- HTTP, REST, WMS, WFS, WCS, CSW, STAC, CKAN API etc. → `access_protocols`;
- GeoNetwork, Earthdata Search, geovisualizador etc. → ferramenta/interface, não protocolo por definição;
- mapa/dashboard/visualização web → `visualization_types`, nunca `data_formats`.

## 4. Tempo

- `temporal_coverage` = período coberto pelos dados;
- `temporal_resolution` = granularidade temporal da observação/produto;
- frequência de atualização/publicação = outro conceito.

**Nunca converter frequência de atualização em `temporal_resolution`.**

## 5. Evidência

Para cada valor novo:

- existe afirmação explícita ou demonstração inequívoca em fonte oficial atual?
- a URL é representativa da entidade ou apenas de um componente estreito?
- a evidência está atualizada o suficiente para o atributo em questão?
- existe evidência oficial contraditória?

Se houver conflito material ou interpretação necessária, subir de `AUTO-SAFE` para `REVIEW`.

## 6. Licença e citação

- licença do site não é automaticamente licença dos dados;
- licença de um produto não é automaticamente licença da plataforma inteira;
- citação institucional não substitui citação de datasets/produtos quando a proveniência exige granularidade específica;
- não preencher licença/citação por analogia.

## 7. Ausência

- `unknown`, `not_found`, `not_applicable`, `partial` e “varia por produto” não são equivalentes;
- não preencher lacunas para melhorar completude aparente;
- informação útil sem campo semanticamente correto fica no audit trail até decisão de contrato.

## 8. Auditoria da própria auditoria

Antes de fechar o lote:

1. reler as linhas canônicas atuais;
2. confrontar cada correção proposta com a semântica do campo no contrato;
3. procurar uma explicação alternativa plausível para o valor atual;
4. procurar omissões relevantes, não apenas erros do que foi revisado;
5. verificar se todos os valores novos estão sustentados por fonte oficial atual;
6. confirmar que a fila não contém valores inventados, extrapolados ou mais específicos que a evidência;
7. confirmar que `last_verified` só será alterado após revisão integral da linha;
8. somente então classificar o pacote por risco.

CI valida estrutura; este checklist protege a **qualidade factual e semântica**.