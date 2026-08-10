# Vitrine Ciência — auditoria científica DR0005–DR0010

Data: 2026-08-10 (`America/Sao_Paulo`)  
Base canônica: `main@1dc306ddb799686493137567090b7e5ff9360a37`  
Contrato: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`

## Método

Para cada registro:

`linha canônica → payload legado útil → fonte oficial atual → decisão campo a campo`

A fonte oficial atual prevalece sobre o legado. Ausência de evidência não é preenchida por inferência. Este documento registra decisões; alterações no CSV serão aplicadas em batch separado e estritamente auditado.

---

## DR0005 — CEMADEN

### Evidência oficial atual

- homepage institucional: `https://www.gov.br/cemaden/pt-br`
- Acesso à Informação: `https://www.gov.br/cemaden/pt-br/acesso-a-informacao`
- Mapa Interativo: `https://mapainterativo.cemaden.gov.br/`
- orientação recente sobre Plano de Dados Abertos: `https://www.gov.br/cemaden/pt-br/assuntos/noticias-cemaden/participe-da-construcao-do-plano-de-dados-abertos-do-cemaden`
- exemplo atual de produto/condições: `https://www.gov.br/cemaden/pt-br/assuntos/monitoramento/boletim-de-impactos-de-extremos-de-origem-hidro-geo-climatico-em-atividades-estrategicas-para-o-brasil/copy_of_boletim-de-impactos-de-extremos-de-origem-hidro-geo-climatico-em-atividades-estrategicas-para-o-brasil-09-04-2026-ano-09-no-89`

### Verificação

O CEMADEN continua operando monitoramento nacional de secas, ameaças geo-hidrológicas e rede observacional. O Mapa Interativo mantém downloads mensais de dados pluviométricos e outros tipos de PCD; alguns fluxos pedem nome/e-mail e entregam link por e-mail. O próprio CEMADEN alerta que dados brutos da rede no Mapa Interativo podem não ter passado por tratamento e podem conter inconsistências. Produtos específicos podem impor condições de reprodução/uso e exigência de atribuição.

### Decisão

**Manter** identidade, cobertura nacional, `free_download=parcial`, acesso heterogêneo e `authentication_required=parcial` como representação agregada conservadora.

**Candidato de correção:** `limitations` deve registrar explicitamente que dados brutos do Mapa Interativo podem conter inconsistências e que condições de uso podem variar por produto. Isso é mais informativo que a formulação atual sem generalizar a restrição de um produto para toda a instituição.

**Não promover licença do site/produto a licença universal da fonte.**

---

## DR0006 — PANORAMA / CENSIPAM

### Evidência oficial atual

- plataforma: `https://panorama.sipam.gov.br/` → `/home`
- catálogo de metadados: `https://panorama.sipam.gov.br/geonetwork/srv/search?type=dataset`
- API meteorológica: `https://panorama.sipam.gov.br/api/meteorologia/v1`

### Verificação

A página oficial define PANORAMA como infraestrutura de dados espaciais mantida pelo CENSIPAM para integração de dados, informações e produtos geoespaciais. A página reúne produtos, catálogo de geosserviços e catálogo de metadados. O GeoNetwork contém mais de mil datasets e registra origem, qualidade, representação, formatos/formas de acesso e frequências por recurso. A API meteorológica exige solicitação e duas chaves exclusivas.

### Decisão

**Manter** `programmatic_access=parcial`, `authentication_required=parcial` e a observação de que condições variam por produto.

**Correções candidatas:**

1. `verification_url` → `https://panorama.sipam.gov.br/`, porque a URL atual aponta apenas à API meteorológica e é estreita demais para verificar a identidade da infraestrutura;
2. `data_formats`: remover `visualização web`, que não é formato de dados. Usar formulação conservadora como `formatos geoespaciais e tabulares variados`, mantendo protocolos/serviços em `access_protocols`.

**Manter licença como não localizada no nível dos dados.** O rodapé licencia conteúdo do site em CC BY-ND 3.0, o que não é evidência suficiente de licença universal para todos os datasets federados.

---

## DR0007 — UrbVerde

### Evidência oficial atual

- `https://urbverde.iau.usp.br/`

### Verificação

A plataforma continua declarando missão de gerar dados socioambientais acessíveis e gratuitos para todo o Brasil e oferece mapas ambientais/sociais e dados estatísticos municipais. A página pública não apresenta, na evidência consultada, uma licença de dados universal nem um catálogo estruturado único de metadados.

### Decisão

A linha atual permanece suficientemente conservadora.

- manter `free_download=parcial`: gratuidade de acesso não prova download universal de todos os indicadores;
- não converter ausência visível de login em afirmação absoluta nova sem documentação específica;
- manter licença não localizada.

**Correção canônica imediata:** nenhuma.

---

## DR0008 — Portal Brasileiro de Dados Abertos / Catálogo Nacional de Dados

### Evidência oficial atual

- homepage: `https://dados.gov.br/`
- catálogo: `https://dados.gov.br/dados/conjuntos-dados`
- sobre: `https://dados.gov.br/dados/conteudo/sobre`
- API: `https://dados.gov.br/swagger-ui/index.html`

### Verificação

A homepage atual apresenta o serviço como **Portal Brasileiro de Dados Abertos e Catálogo Nacional de Dados**. A documentação explica que o portal funciona como catálogo federado e que a área de dados abertos contém apenas dados abertos. A API REST mantém operações GET públicas de consulta. Entretanto, a interface atual de conjuntos de dados informa que o novo portal exige cadastro/login gov.br para acesso à área correspondente.

### Decisão

**Correções candidatas:**

1. `official_identity` → `Portal Brasileiro de Dados Abertos e Catálogo Nacional de Dados`;
2. `authentication_required`: `não` → `parcial`, pois a condição atual depende do canal — consultas API públicas coexistem com interface web que informa necessidade de cadastro gov.br;
3. `access_conditions`: substituir `aberto` por formulação que preserve abertura dos dados e a condição operacional de acesso web, por exemplo `dados abertos; catálogo web pode exigir login gov.br`.

**Manter** `programmatic_access=sim`, REST API e licença variável conforme conjunto.

---

## DR0009 — GBIF

### Evidência oficial atual

- `https://www.gbif.org/what-is-gbif`
- `https://www.gbif.org/citation-guidelines`
- `https://techdocs.gbif.org/en/openapi/`

### Verificação

GBIF continua sendo rede internacional e infraestrutura de dados que fornece acesso aberto a dados de biodiversidade. A API é REST e a maior parte das consultas não exige autenticação; downloads e algumas operações exigem conta. Diretrizes atuais exigem preservar a citação dos datasets/downloads, normalmente por DOI, e licenças permanecem no nível dos datasets.

### Decisão

A linha atual representa corretamente:

- acesso aberto;
- autenticação parcial;
- API REST;
- licenças variáveis por dataset;
- obrigação de citar dados efetivamente utilizados.

**Correção canônica imediata:** nenhuma.

---

## DR0010 — MapBiomas Brasil

### Evidência oficial atual

- termos: `https://brasil.mapbiomas.org/termos-de-uso/`
- coleções: `https://brasil.mapbiomas.org/colecoes-mapbiomas/`
- downloads: `https://brasil.mapbiomas.org/downloads/`
- metodologia: `https://brasil.mapbiomas.org/visao-geral-da-metodologia/`
- Coleção 10.1: `https://brasil.mapbiomas.org/2026/02/09/mapbiomas-publica-colecao-10-1-de-mapas-anuais-de-cobertura-e-uso-da-terra-no-brasil/`

### Verificação

Os termos atuais declaram os dados do MapBiomas públicos, abertos e gratuitos sob licença Creative Commons **CC-BY**, com referência obrigatória da fonte. A página de coleções confirma Coleção 10.1 para Cobertura e Uso da Terra e Desmatamento/Vegetação Secundária. A comunicação de fevereiro de 2026 confirma série 1985–2024 para a Coleção 10.1. A página de downloads fornece rotas explícitas de acesso e a metodologia mantém Landsat/30 m para cobertura e uso da terra, com ATBDs por produto.

### Decisão

**Correções candidatas:**

1. `license`: `licença MapBiomas; consultar produto` → `CC BY; atribuição da fonte obrigatória`;
2. `access_documentation_url`: vazio → `https://brasil.mapbiomas.org/downloads/`.

**Manter** a ressalva de que método, coleção e detalhes variam por produto; o licenciamento geral não elimina a necessidade de citar corretamente a coleção/produto usado.

---

## Resumo do bloco

| ID | Estado | Correção candidata |
|---|---|---|
| DR0005 | VERIFIED_WITH_CORRECTION | limitations |
| DR0006 | VERIFIED_WITH_CORRECTION | data_formats; verification_url |
| DR0007 | VERIFIED_NO_CHANGE | — |
| DR0008 | VERIFIED_WITH_CORRECTION | official_identity; authentication_required; access_conditions |
| DR0009 | VERIFIED_NO_CHANGE | — |
| DR0010 | VERIFIED_WITH_CORRECTION | license; access_documentation_url |

## Política de `last_verified`

Este bloco revisou as fontes de forma ampla, mas a atualização de `last_verified` no CSV será feita somente no pacote DATA depois da validação campo a campo do delta final. Não alterar data por simples existência deste relatório.

## Próxima ação

1. combinar as correções inequívocas já identificadas em `DR0002`, `DR0003`, `DR0005`, `DR0006`, `DR0008` e `DR0010`;
2. realizar uma única atualização controlada do CSV para o primeiro bloco `DR0001–DR0010`;
3. provar por diff que somente os registros/campos autorizados pelo audit trail mudaram;
4. executar validadores e build;
5. integrar como `AUTO-SAFE` somente se não houver ambiguidade ou alteração incidental;
6. continuar a auditoria em `DR0011–DR0020`.