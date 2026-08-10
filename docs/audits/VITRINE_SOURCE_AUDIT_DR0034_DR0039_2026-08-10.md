# Vitrine Ciência — auditoria científica DR0034–DR0039

Data: 2026-08-10 (`America/Sao_Paulo`)  
Base: `main@3cbb99ad79d4ce223f41325889587e3950ea0ab5`  
Contrato: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`  
QA: `docs/VITRINE_SCIENTIFIC_AUDIT_CHECKLIST.md`

## Método

`linha canônica → legado como pista → fonte oficial atual → decisão campo a campo → checagem adversarial`

A auditoria distingue software, serviço, dataset, catálogo e infraestrutura. Gratuidade não é sinônimo de ausência de autenticação; formatos não são protocolos; frequência de atualização não é resolução temporal.

---

## DR0034 — iNaturalist

### Evidência oficial atual

- API v2: `https://api.inaturalist.org/v2/docs/`
- developers/datasets: `https://www.inaturalist.org/pages/developers`
- ajuda de download: `https://help.inaturalist.org/en/support/solutions/articles/151000170342-how-can-i-download-data-from-inaturalist-`
- licenças: `https://help.inaturalist.org/en/support/solutions/articles/151000175695`

A API v2 usa JSON e exige autenticação para PUT/POST e algumas leituras sensíveis; leitura pública de observações permanece disponível. Exportação CSV pela interface exige conta. O ecossistema também disponibiliza dados em Darwin Core Archive via GBIF, atualizado semanalmente para observações Research Grade com licenças elegíveis. Licenças são definidas separadamente para observações, fotos e sons; o padrão atual é CC BY-NC, mas usuários podem escolher outras licenças ou manter direitos reservados.

### Checagem adversarial

`authentication_required=não` é absoluto demais: navegação/read API é pública, mas exportação CSV e operações privadas/escrita exigem autenticação. `exportação CSV` e `integração GBIF` são rotas/processos, não protocolos.

### Decisão

- `authentication_required` → `parcial`;
- `access_conditions` → consulta pública/read API; conta para exportação CSV; autenticação para escrita ou acesso autorizado a informação privada;
- `access_protocols` → `REST API | HTTP export/download`;
- `access_documentation_url` → API v2 atual;
- `data_formats` → `CSV | JSON | Darwin Core | KML; varia conforme a rota de acesso`;
- manter licença por observação/mídia e limitações de coordenadas/viés.

---

## DR0035 — Climate Data Guide

### Evidência oficial atual

- homepage: `https://climatedataguide.ucar.edu/`
- dados/guias: `https://climatedataguide.ucar.edu/climate-data`
- sobre: `https://climatedataguide.ucar.edu/about`

O Climate Data Guide continua sendo um **portal de conhecimento curado**, com mais de 200 datasets/índices descritos e comentários especializados. Com exceção de um pequeno conjunto de índices, o Guide não hospeda datasets e não é ponto de download; fornece links aos provedores. A citação do Guide e das contribuições especializadas é documentada separadamente da citação dos datasets originais.

### Decisão

A linha atual representa corretamente o papel de guia, ausência de download próprio e dependência do provedor para licença/versão/acesso.

**Correção imediata:** nenhuma.

---

## DR0036 — FRED

### Evidência oficial atual

- homepage: `https://roots.ornl.gov/`
- release/acesso: `https://roots.ornl.gov/public-release`
- Data Use Guidelines: `https://roots.ornl.gov/guidelines`

FRED 3.0 permanece publicamente disponível e sem cobrança, mas o download passa por formulário com nome, e-mail, finalidade/uso e afiliação; o usuário recebe por e-mail token temporário de 24 horas para a interface filtrável. As Data Use Guidelines pedem citação da versão/DOI do FRED, rastreabilidade e, quando possível, citação das fontes originais. FRED é projeto do Oak Ridge National Laboratory/TES SFA; a evidência consultada não sustenta tratá-lo como dataset do ORNL DAAC.

### Decisão

- `data_access_url` → página `public-release`;
- `license`: substituir `termos do ORNL DAAC / dataset` por `FRED Data Use Guidelines; acesso aberto e sem cobrança; citar FRED e, quando possível, fontes originais`;
- manter `free_download=sim`, formulário + token de 24h, `authentication_required=sim` como representação do credential gate de download, e `programmatic_access=não`.

Não inventar uma licença Creative Commons quando a página consultada fornece diretrizes de uso/citação, não uma licença CC explícita.

---

## DR0037 — SoilGrids

### Evidência oficial atual

- documentação: `https://docs.isric.org/globaldata/soilgrids/index.html`
- WCS: `https://docs.isric.org/globaldata/soilgrids/wcs.html`
- WebDAV: `https://docs.isric.org/globaldata/soilgrids/WebDav.html`
- licença: `https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_04.html`

SoilGrids mantém mapas globais modelados sob CC BY 4.0. A documentação atual recomenda WMS para visualização, WCS para subsets e modelagem, WebDAV/VRT para mapas globais completos e Google Earth Engine como plataforma adicional. WCS e WebDAV têm exemplos de acesso programático em R/Python/Linux. A REST API é complementar/beta e pode sofrer indisponibilidade; não é o único caminho programático.

### Checagem adversarial

`data_formats=GeoTIFF | VRT | WCS | mapas web` mistura formatos, protocolo e interface. `programmatic_access=parcial` subestima WCS/WebDAV programáticos estáveis. `Google Earth Engine` é plataforma, não protocolo.

### Decisão

- `data_formats` → `GeoTIFF | VRT`;
- `programmatic_access` → `sim`;
- `access_protocols` → `WMS | WCS | WebDAV | REST API beta`;
- manter documentação atual, CC BY 4.0, ausência de autenticação e limitação sobre predição modelada/incerteza.

---

## DR0038 — WoSIS

### Evidência oficial atual

- documentação: `https://docs.isric.org/globaldata/wosis/`
- FAQ/acesso: `https://docs.isric.org/globaldata/wosis/faq-wosis.html`
- WFS: `https://docs.isric.org/globaldata/wosis/Access_WoSIS_latest_from%20QGIS.html`

WoSIS serve dados de perfis de solo padronizados. `wosis_latest` é dinâmico e acessível via OGC WFS e GraphQL API; snapshots estáticos são distribuídos em TSV com DOI. Apenas dados de provedores com licenças públicas (tipicamente CC BY ou CC BY-NC) são redistribuídos; dados mais restritos podem ser processados internamente pelo ISRIC sem serem disponibilizados ao público.

### Checagem adversarial

`data_formats=TSV | WFS | formatos...` mistura formato e protocolo. `access_protocols` mistura protocolo com método de download e plataforma web.

### Decisão

- `data_formats` → `TSV | formatos geoespaciais e tabulares derivados conforme serviço`;
- `access_protocols` → `OGC WFS | GraphQL API | HTTP download`;
- manter `programmatic_access=sim`, `authentication_required=não` para o conjunto efetivamente servido ao público, licença por provedor e distinção entre dados públicos e restritos.

Não interpretar dados restritos usados internamente como canal autenticável para usuários externos.

---

## DR0039 — GBIF IPT

### Evidência oficial atual

- `https://www.gbif.org/ipt`
- `https://www.gbif.org/tool/81278/ipt-gbif-integrated-publishing-toolkit`

IPT continua sendo software livre/open source do GBIF para criar e administrar repositórios distribuídos de publicação de datasets de biodiversidade, com Darwin Core e EML. Pode ser self-hosted, operado por nós nacionais/temáticos ou hospedado regionalmente. O software é Apache License 2.0. Ele não é um catálogo agregador para consulta e o acesso aos datasets depende da instalação/publicação.

### Decisão

A linha atual está corretamente delimitada como **software de publicação** e não força atributos de datasets para o software.

**Correção imediata:** nenhuma.

---

## Resumo

| ID | Resultado | Correções candidatas |
|---|---|---|
| DR0034 | VERIFIED_WITH_CORRECTION | authentication_required; access_conditions; access_protocols; access_documentation_url; data_formats |
| DR0035 | VERIFIED_NO_CHANGE | — |
| DR0036 | VERIFIED_WITH_CORRECTION | data_access_url; license |
| DR0037 | VERIFIED_WITH_CORRECTION | data_formats; programmatic_access; access_protocols |
| DR0038 | VERIFIED_WITH_CORRECTION | data_formats; access_protocols |
| DR0039 | VERIFIED_NO_CHANGE | — |

## Checagem adversarial final

- software (IPT) não foi tratado como dataset/catalogador;
- Guide curado não foi tratado como host de dados;
- conta/export/API do iNaturalist foi separada da consulta pública;
- token FRED foi registrado como condição de acesso, sem inventar licença CC;
- WCS/WFS/GraphQL/WebDAV foram separados de formatos;
- acesso programático foi inferido apenas quando explicitamente documentado.

## Próxima ação

Materializar a fila de correções, validar e integrar este audit trail como `AUTO-SAFE`. Depois seguir para `DR0040–DR0045`. A escrita do CSV permanece acumulada para uma única atualização canônica auditada após 51/51.