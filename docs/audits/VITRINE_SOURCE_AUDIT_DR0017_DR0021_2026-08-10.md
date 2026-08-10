# Vitrine Ciência — auditoria científica DR0017–DR0021

Data: 2026-08-10 (`America/Sao_Paulo`)  
Base: `main@7dc6a5d9d901abea2f825f1d7c12105cdd7ebe53`  
Contrato: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`  
QA científico: `docs/VITRINE_SCIENTIFIC_AUDIT_CHECKLIST.md`

## Método

`linha canônica → legado como pista → fonte oficial atual → decisão campo a campo → checagem adversarial`

A fonte oficial atual prevalece. Nenhum valor é preenchido por inferência. A checagem adversarial separa acesso público de autenticação, formato de protocolo, resolução temporal de frequência de atualização e plataforma de produto/componente.

---

## DR0017 — SNIRH / HidroWeb

### Evidência oficial atual

- SNIRH/ANA: `https://www.gov.br/ana/pt-br/assuntos/gestao-das-aguas/politica-nacional-de-recursos-hidricos/sistema-de-informacoes-sobre-recursos-hidricos/sistema-nacional-de-informacoes-sobre-recursos-hidricos`
- acesso a sistemas: `https://www.gov.br/ana/pt-br/servicos/acesso-a-sistemas/acesso-aos-sistemas`
- manuais HidroWebservice atualizados em 2026: `https://www.gov.br/ana/pt-br/assuntos/monitoramento-e-eventos-criticos/monitoramento-hidrologico/orientacoes-manuais/manuais-de-sistemas-e-servicos-de-disponibilizacao-de-dados-hidrologicos`

A ANA continua definindo o SNIRH como sistema para reunir, dar consistência e divulgar informações sobre recursos hídricos, com atualização permanente. O HidroWeb permanece sistema finalístico para o acervo hidrológico. A ANA mantém manual específico da API HidroWebservice atualizado em fevereiro de 2026. Fontes oficiais também reafirmam que as informações do SNIRH são públicas e disponibilizadas gratuitamente.

### Decisão

- identidade/cobertura/uso científico: manter;
- `data_formats`: remover `serviços web`, que é mecanismo de acesso, preservando os formatos já registrados e a indicação de variação;
- `access_protocols`: manter REST API e download tabular;
- `authentication_required=parcial`: manter, pois a entrada combina acesso público e canal API com condições próprias já documentadas;
- `verification_url`: substituir a página estreita da API por página institucional representativa do SNIRH;
- `license`: `dados públicos da ANA` não é uma licença. Usar formulação conservadora que preserve publicidade dos dados sem inventar licença de dados específica.

Não mapear “atualizar permanentemente” para `temporal_resolution`.

---

## DR0018 — BDMEP / INMET

### Evidência oficial atual

- `https://bdmep.inmet.gov.br/`

A página oficial atual oferece dois fluxos materialmente distintos:

1. **download imediato** de pacotes anuais de todas as estações automáticas;
2. solicitação personalizada por estação/período/variáveis, que exige fornecimento e confirmação de e-mail, entra em fila de processamento e gera link temporário; os dados são apagados após 48 horas.

A página também encaminha consultas horárias curtas ao sistema TEMPO.

### Checagem adversarial

A linha atual usa `authentication_required=sim`, mas não há conta/login universal no BDMEP. A confirmação de e-mail aplica-se ao fluxo personalizado; o pacote anual possui download imediato. A classificação agregada mais precisa é, portanto, `parcial`.

### Decisão

- `authentication_required`: `sim` → `parcial`;
- `access_conditions`: explicitar os dois fluxos, mantendo a confirmação por e-mail e retenção de 48 h no fluxo personalizado;
- `access_protocols`: `não se aplica` é excessivo porque existe download direto pela web; registrar HTTP download;
- formatos/temporalidade: manter CSV e as resoluções já documentadas pela própria interface;
- não alterar licença sem evidência específica de licença dos dados.

---

## DR0019 — Google Earth Engine Data Catalog

### Evidência oficial atual

- acesso: `https://developers.google.com/earth-engine/guides/access`
- níveis não comerciais: `https://developers.google.com/earth-engine/guides/noncommercial_tiers`
- exportação de tabelas: `https://developers.google.com/earth-engine/guides/exporting_tables`
- exportação de imagens: `https://developers.google.com/earth-engine/reference/rest/v1/ImageFileExportOptions`

O uso do Earth Engine continua exigindo projeto Google Cloud com API habilitada, projeto registrado e permissões apropriadas. Desde 27 de abril de 2026, projetos não comerciais possuem cotas mensais recorrentes de EECU conforme nível. Exportações tabulares suportam CSV, SHP, GeoJSON, KML, KMZ e TFRecord; exportações de imagem suportam GeoTIFF e TFRecord.

### Decisão

A linha atual representa corretamente autenticação, projeto Cloud, verificação não comercial e cotas.

Correção semântica:

- `data_formats`: retirar `assets Earth Engine`, que é objeto/armazenamento interno e não formato de exportação, e registrar apenas formatos explicitamente suportados de exportação.

Não converter cotas de computação em condição de download nem em propriedade científica do dataset.

---

## DR0020 — AppEEARS

### Evidência oficial atual

- homepage: `https://appeears.earthdatacloud.nasa.gov/`
- ajuda: `https://appeears.earthdatacloud.nasa.gov/help`
- changelog: `https://appeears.earthdatacloud.nasa.gov/changelog`

A documentação atual informa que AppEEARS oferece extração e transformação de dados geoespaciais de **diversos arquivos federais**, com parâmetros espaciais, temporais e por camada. A homepage lista LP DAAC, NSIDC DAAC, ORNL DAAC, USGS, National Park Service e Ocean Biology DAAC entre os provedores/arquivos integrados. Earthdata Login é obrigatório tanto para o site quanto para a API. O serviço continua ativo, com versão 3.124 em julho de 2026 e adição frequente de produtos.

### Checagem adversarial

A descrição canônica atual diz “produtos terrestres NASA” e `data_sources` lista apenas MODIS/VIIRS/modelos NASA. Isso ficou estreito demais para o serviço atual. A licença `política de dados abertos NASA` também é excessivamente universal, pois o serviço agrega produtos de múltiplos arquivos/provedores e a licença científica deve seguir o produto de origem.

### Decisão

- `description`: ampliar de “produtos terrestres NASA” para produtos geoespaciais de diversos arquivos federais;
- `data_sources`: atualizar para refletir provedores/arquivos federais diversos, sem tentar enumerar todos os produtos;
- `license`: substituir regra NASA universal por “varia conforme produto/provedor; consultar produto de origem”;
- autenticação, API, finalidade de recorte e limitação de citar/versionar o produto de origem: manter.

Não transformar o changelog rápido do software em frequência científica dos datasets.

---

## DR0021 — Copernicus Climate Data Store

### Evidência oficial atual

- CDS: `https://cds.climate.copernicus.eu/`
- documentação: Copernicus Knowledge Base / Climate Data Store documentation

A documentação atual mantém o CDS como infraestrutura central do C3S, com busca e recuperação por web/API. Os dados são gratuitos e abertos, sujeitos à concordância com a licença aplicável a cada dataset. Registro/login é necessário para acesso/download, e a API é suportada.

### Decisão

A linha atual está conceitualmente correta. `access_conditions=cadastro`, porém, está subdescrito.

Correção candidata:

- `access_conditions` → explicitar cadastro/login gratuito e necessidade de aceitar a licença aplicável ao dataset antes do download.

Manter `authentication_required=sim`, CDS API/Python, formatos variáveis e licença específica por dataset.

---

## Resumo do bloco

| ID | Resultado | Correções candidatas |
|---|---|---|
| DR0017 | VERIFIED_WITH_CORRECTION | data_formats; verification_url; license |
| DR0018 | VERIFIED_WITH_CORRECTION | authentication_required; access_conditions; access_protocols |
| DR0019 | VERIFIED_WITH_CORRECTION | data_formats |
| DR0020 | VERIFIED_WITH_CORRECTION | description; data_sources; license |
| DR0021 | VERIFIED_WITH_CORRECTION | access_conditions |

## Checagem adversarial final

- nenhum acesso público foi confundido com autenticação de API/admin;
- formatos e protocolos foram separados;
- frequência de atualização não foi mapeada para resolução temporal;
- condições de produto não foram promovidas automaticamente à plataforma;
- licenças genéricas foram evitadas quando o serviço agrega produtos de múltiplos provedores;
- todas as correções candidatas permanecem dentro do contrato canônico atual.

## Próxima ação

Materializar a fila estruturada, validar CI/diff e integrar este audit trail como `AUTO-SAFE`. Depois continuar em `DR0022–DR0027` e, separadamente, preparar a aplicação consolidada das filas ao CSV somente quando o mecanismo de escrita/diff for suficientemente seguro.