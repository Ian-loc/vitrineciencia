# Vitrine Ciência — auditoria científica DR0022–DR0027

Data: 2026-08-10 (`America/Sao_Paulo`)  
Base: `main@da978ea82fc32817bbb3e9ce02d8abaa50095de5`  
Contrato: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`  
QA: `docs/VITRINE_SCIENTIFIC_AUDIT_CHECKLIST.md`

## Método

`linha canônica → legado como pista → fonte oficial atual → decisão campo a campo → checagem adversarial`

Somente evidência oficial atual sustenta correções. Informações de atualização, licença, autenticação e produto permanecem no nível semântico correto.

---

## DR0022 — WorldClim

### Evidência oficial atual

- `https://worldclim.org/about.html`
- `https://worldclim.org/data/index.html`

WorldClim continua oferecendo dados climáticos globais de alta resolução para download. A página oficial de licença é explícita: os dados podem ser usados gratuitamente para fins acadêmicos e outros usos não comerciais; redistribuição e uso comercial não são permitidos sem autorização prévia.

### Decisão

A linha atual está correta quanto a finalidade, cobertura, GeoTIFF e ausência de autenticação, mas `access_conditions=aberto` e `license=licença WorldClim; consultar versão` subdescrevem as restrições.

Correções:
- `access_conditions` → uso acadêmico/não comercial; redistribuição ou uso comercial requer permissão;
- `license` → termos WorldClim para uso acadêmico/não comercial, com permissão prévia para redistribuição/comercial.

Não tratar gratuidade de download como licença aberta irrestrita.

---

## DR0023 — CHELSA

### Evidência oficial atual

- `https://www.chelsa-climate.org/datasets/chelsa_climatologies`
- `https://www.chelsa-climate.org/datasets/chelsa_daily`
- `https://www.chelsa-climate.org/datasets/chelsaw5e5`

A plataforma atual apresenta datasets/versionamentos individualizados. CHELSA v2.1 permanece ativa e produtos atuais documentam formatos como COG (Cloud Optimized GeoTIFF) e NetCDF. As licenças variam efetivamente por dataset/produto: exemplos atuais incluem CC0 1.0 e CC BY 4.0.

### Decisão

- `data_formats`: `GeoTIFF | NetCDF; varia` → `COG (GeoTIFF) | NetCDF; varia`;
- manter `license=licença específica por versão` em sentido conservador, interpretando-a no nível do dataset/produto;
- não atribuir a licença do modelo/software CHELSA à licença dos datasets;
- manter resolução, cobertura e temporalidade como variáveis por produto.

---

## DR0024 — Protected Planet / WDPA

### Evidência oficial atual

- WDPA: `https://www.protectedplanet.net/en/thematic-areas/wdpa`
- API v4: `https://api.protectedplanet.net/documentation`
- API/request: `https://api.protectedplanet.net/request`

Mudanças materiais recentes:

1. em 1º de novembro de 2025, WDPA e WD-OECM foram integradas em uma base unificada, preservando diferenciação por tipo de sítio;
2. a API v4 é a versão atual; v3 foi descontinuada em 1º de maio de 2026;
3. WDPA é atualizada mensalmente;
4. exploração pública é possível sem autenticação, mas API exige token e downloads não comerciais são sujeitos a termos/fluxo próprio; uso comercial é direcionado ao IBAT.

### Checagem adversarial

`temporal_resolution=mensal` na linha atual é frequência de atualização, não resolução temporal científica. `authentication_required=sim` também é excessivamente absoluto para uma plataforma com exploração pública e canais autenticados.

### Decisão

- `temporal_resolution` → `não se aplica`;
- `authentication_required` → `parcial`;
- `access_conditions` → consulta pública; download não comercial sujeito a termos/cadastro; API com token; uso comercial via IBAT;
- `access_documentation_url` → documentação da API v4;
- `license` → termos de uso Protected Planet; uso comercial via IBAT;
- `limitations`: registrar unificação WDPA/WD-OECM e API v4, além de preservar necessidade de registrar edição mensal e cautela com precisão dos limites.

---

## DR0025 — IUCN Red List

### Evidência oficial atual

- API v4: `https://api.iucnredlist.org/`
- dados espaciais: `https://nrl.iucnredlist.org/resources/spatial-data-download`
- atualizações: `https://nrl.iucnredlist.org/assessment/updates`
- FAQ: `https://nrl.iucnredlist.org/about/faqs`

A API v3 foi removida em março de 2025; v4 é a API vigente e exige token. Consulta pública na web é aberta, enquanto downloads/funções avançadas e API usam conta/token. Os dados são disponibilizados gratuitamente para uso não comercial conforme os termos. A IUCN procura atualizar a Red List pelo menos duas vezes por ano; espécies individuais possuem datas próprias de avaliação/reavaliação. Em julho de 2026, os downloads espaciais atuais incluem Shapefile e CSV.

### Checagem adversarial

`temporal_resolution=irregular por espécie` descreve cadência de atualização/reavaliação, não resolução temporal dos dados. `authentication_required=sim` ignora a consulta web pública.

### Decisão

- `temporal_resolution` → `não se aplica`;
- `authentication_required` → `parcial`;
- `access_conditions` → consulta pública; conta/termos para downloads; API v4 com token; uso dos dados sujeito a condições não comerciais;
- `license` → IUCN Red List Terms of Use; dados disponibilizados para uso não comercial;
- `limitations`: substituir referência a API v3 “em fim de vida” por v3 removida / usar v4 e manter diferenças de data/abrangência das avaliações.

---

## DR0026 — OBIS

### Evidência oficial atual

- `https://obis.org/data/access/`
- `https://manual.obis.org/access`

OBIS continua integrando ocorrências de milhares de datasets. A documentação atual recomenda caminhos distintos por escala: mapper, busca, pacote R, REST API, AWS Open Data/GeoParquet e full exports. Formatos explicitamente documentados para o dataset integrado incluem TSV, JSON via API e GeoParquet. Cada export acompanha as licenças dos datasets subjacentes.

### Checagem adversarial

A linha atual mistura `visualização web` em `data_formats` e mistura pacote R/GeoParquet em `access_protocols`.

### Decisão

- `data_formats` → `TSV | GeoParquet | JSON; varia por dataset`;
- `access_protocols` → `REST API | AWS Open Data | HTTP download`;
- `access_documentation_url` → página geral de Data Access;
- manter autenticação não, acesso aberto e licença variável por dataset;
- manter limitações sobre esforço amostral, qualidade e precisão.

---

## DR0027 — eBird

### Evidência oficial atual

- uso científico: `https://science.ebird.org/en/use-ebird-data`
- suporte/download: `https://support.ebird.org/en/support/solutions/articles/48000838205-download-ebird-data`
- API: `https://documenter.getpostman.com/view/664302/S1ENwy59`

A documentação atual declara dados eBird open-access e gratuitos. O EBD é atualizado mensalmente no dia 15, exige login e breve formulário de projeto e é entregue como arquivo de texto tabulado. A API usa JSON e exige chave pessoal vinculada à conta na maioria dos endpoints. Produtos Status and Trends possuem fluxos próprios de solicitação/download. Dados sensíveis podem permanecer obscurecidos/restritos em outputs públicos.

### Checagem adversarial

`pacote EBD` não é formato; `pacote R` não é protocolo. `free_download=parcial` confunde gratuidade com requisito de solicitação/autenticação: os dados distribuídos são gratuitos, embora o acesso a alguns produtos exija login/formulário.

### Decisão

- `data_formats` → `texto tabulado (EBD) | JSON; formatos derivados variam por produto`;
- `free_download` → `sim`;
- `access_conditions` → login + formulário para EBD; API key para API; produtos derivados podem exigir solicitação;
- `access_protocols` → `REST API | HTTP download`;
- `access_documentation_url` → página oficial de uso/download de dados;
- `license` → eBird Terms of Use; dados brutos gratuitos para uso não comercial;
- manter `authentication_required=parcial` para representar navegação pública + canais autenticados.

---

## Resumo

| ID | Resultado | Correções candidatas |
|---|---|---|
| DR0022 | VERIFIED_WITH_CORRECTION | access_conditions; license |
| DR0023 | VERIFIED_WITH_CORRECTION | data_formats |
| DR0024 | VERIFIED_WITH_CORRECTION | temporal_resolution; authentication_required; access_conditions; access_documentation_url; license; limitations |
| DR0025 | VERIFIED_WITH_CORRECTION | temporal_resolution; authentication_required; access_conditions; license; limitations |
| DR0026 | VERIFIED_WITH_CORRECTION | data_formats; access_protocols; access_documentation_url |
| DR0027 | VERIFIED_WITH_CORRECTION | data_formats; free_download; access_conditions; access_protocols; access_documentation_url; license |

## Checagem adversarial final

- nenhuma frequência de atualização foi mantida como resolução temporal;
- autenticação foi avaliada por canal, não por uma única interface;
- formatos, protocolos e ferramentas foram separados;
- licenças/termos de uso não foram promovidos entre software, plataforma e datasets;
- informação de produto/dataset permaneceu no nível apropriado;
- todas as correções propostas cabem no contrato congelado.

## Próxima ação

Materializar a fila de correções e integrar o audit trail como `AUTO-SAFE`. Depois seguir para `DR0028–DR0033` e manter a aplicação do CSV acumulada para uma atualização canônica única e auditada após a auditoria 51/51.