# Vitrine Ciência — auditoria científica DR0011–DR0016

Data da auditoria: 2026-08-10  
Revisão cruzada: 2026-08-10  
Escopo: `DR0011`–`DR0016`  
Base inicial: `main@8367618449c735020bab94401128dc403932ad87`

## Regra

Esta auditoria usa a linha canônica como ponto de partida, o legado #63 apenas como pista e documentação oficial atual como autoridade. Nenhum valor é promovido por inferência. Fatos sem campo semanticamente adequado permanecem na trilha de auditoria.

Prioridade: produtor/provedor oficial → documentação/metadados oficiais → serviço/API oficial → publicação primária quando necessária.

A revisão cruzada posterior ao primeiro fechamento do bloco detectou omissões em autenticação e semântica de campos. Essas omissões foram corrigidas antes de qualquer alteração do CSV canônico.

---

## DR0011 — TerraBrasilis

### Evidência oficial atual

- plataforma: https://terrabrasilis.dpi.inpe.br/
- FAQ: https://terrabrasilis.dpi.inpe.br/faq/
- downloads: https://terrabrasilis.dpi.inpe.br/downloads/
- citações/licença: https://terrabrasilis.dpi.inpe.br/citacoes-e-licenca-de-uso/
- metadados: https://terrabrasilis.dpi.inpe.br/geonetwork/

A plataforma permanece o ambiente oficial do INPE para acesso, consulta, análise e disseminação de dados de programas como PRODES e DETER. A página de downloads atual documenta Shapefile, GeoPackage e GeoTIFF, além de variação por produto; metadados também registram CSV em recursos específicos.

A FAQ estabelece uma distinção relevante de acesso: os dados públicos são acessíveis livremente respeitando licença/citação, mas **acesso antecipado aos alertas DETER exige credenciais** concedidas exclusivamente a instituições responsáveis por controle e fiscalização.

A página de licença fornece citação da plataforma e informa CC BY-SA 4.0 para o Programa BiomasBR, sem justificar substituir automaticamente todas as condições/citações específicas de cada produto por uma única regra no nível da plataforma.

### Decisão

- conceito da entrada: **coerente**;
- `data_formats`: remover `serviços OGC`, que não é formato; usar apenas formatos de dados documentados e declarar variação;
- `authentication_required`: `não` → **`parcial`**, porque coexistem acesso público e acesso antecipado restrito do DETER;
- manter licença agregada cautelosa e remeter às condições/citações dos produtos/programas.

---

## DR0012 — Programa Queimadas / BDQueimadas

### Evidência oficial atual

- portal: https://terrabrasilis.dpi.inpe.br/queimadas/portal/
- dados abertos: https://terrabrasilis.dpi.inpe.br/queimadas/portal/pages/secao_downloads/dados-abertos/
- FAQ: https://terrabrasilis.dpi.inpe.br/queimadas/portal/pages/secao_informacoes/faq/

O portal atual oferece diversos sistemas e produtos, não apenas o BDQueimadas. A página de dados abertos documenta:

- focos: CSV/KML e atualização até tempo quase real;
- eventos de fogo: KML;
- área queimada: TIFF/Shapefile;
- risco de fogo e meteorologia: produtos observados e previstos;
- geosserviços OGC em área própria.

A FAQ mantém acesso público e sem custo aos produtos após geração.

### Decisão

- `data_formats`: substituir a mistura de formatos, OGC e visualização por **`CSV | KML | TIFF | Shapefile`**;
- `data_access_url`: preferir a página de dados abertos do Programa, porque a entrada representa a família completa e o antigo URL do BDQueimadas cobre apenas um componente;
- manter WMS/WFS em `access_protocols`, não em formatos;
- manter a limitação de que foco de calor não é sinônimo de incêndio nem de área queimada.

---

## DR0013 — speciesLink

### Evidência oficial atual

- API: https://specieslink.net/ws/1.0/
- política de compartilhamento: https://specieslink.net/data_sharing_policy

A política oficial sustenta compartilhamento aberto, CC BY 4.0 para dados textuais e CC BY-SA 4.0 para imagens, com necessidade de preservar atribuição e eventuais condições adicionais do provedor.

A documentação da API é explícita: o serviço web é aberto a todos, mas **cada chamada exige `apikey`**. As chamadas usam HTTP GET; respostas gerais são JSON e buscas de biodiversidade podem retornar GeoJSON. A consulta pública da rede continua distinta do acesso via API.

### Correção da avaliação anterior

A primeira versão desta auditoria considerou `authentication_required=sim` suficientemente coerente apenas porque a própria linha já mencionava chave de API. Isso era agregado demais: a entrada representa a rede, não somente sua API.

### Decisão

- `authentication_required`: `sim` → **`parcial`**;
- `data_formats`: incluir JSON/GeoJSON como formatos documentados da API;
- `access_protocols`: retirar JSON/GeoJSON e registrar **REST API / HTTP GET / exportação tabular**;
- preservar as licenças atuais e cautela por coleção.

---

## DR0014 — SiBBr

### Evidência oficial atual

O domínio principal apresenta limitações para inspeção automatizada, então a verificação foi triangulada apenas com fontes governamentais atuais, incluindo a página de dados ambientais de biodiversidade do MMA e referências institucionais recentes ao uso do SiBBr.

Essas fontes sustentam a função do SiBBr como infraestrutura nacional de integração/disponibilização de dados de biodiversidade. Não sustentam proporcionalmente uma única regra atual de autenticação, API ou licença para todos os módulos.

### Decisão

- manter a entrada conservadora;
- não preencher `programmatic_access`, `access_protocols`, `authentication_required` ou licença por aproximação;
- nenhuma correção inequívoca nesta rodada.

---

## DR0015 — BDiA / IBGE

### Evidência oficial atual

Página técnica oficial:
https://www.ibge.gov.br/geociencias/informacoes-ambientais/vegetacao/23382-banco-de-informacoes-ambientais.html?lang=pt-BR

O IBGE descreve o BDiA como sistema público na web que integra Geologia, Geomorfologia, Pedologia e Vegetação, disponibiliza downloads em formatos diversos e informa atualização **a cada dois anos**. A página reúne acesso ao BDiAWeb, notas metodológicas 2025/2023 e publicações.

### Decisão

- não converter atualização bienal em `temporal_resolution`;
- preencher `access_documentation_url` com a página técnica oficial;
- usar a mesma página como `verification_url`, pois ela documenta identidade, escopo, acesso, método e atualização de forma mais representativa que o aplicativo isolado;
- demais valores permanecem conservadores.

---

## DR0016 — Cadastro Nacional de Unidades de Conservação (CNUC)

### Evidência oficial atual

- serviço gov.br: https://www.gov.br/pt-br/servicos/obter-informacoes-sobre-as-unidades-de-conservacao-ambiental-nacionais
- plataforma: https://cnuc.mma.gov.br/
- dados abertos MMA: https://dados.mma.gov.br/dataset/unidadesdeconservacao
- catálogo federal: https://dados.gov.br/dados/conjuntos-dados/unidadesdeconservacao

A ficha oficial do serviço informa que o CNUC é a plataforma oficial das UCs do SNUC, gratuita, on-line e aberta. Para consulta pública **não é necessário cadastro nem login**. A área restrita é separada e exclusiva para gestores responsáveis por inserir/manter informações.

O serviço permite relatórios em Excel/CSV/PDF e dados geoespaciais SHP/KML. O conjunto oficial também está no Portal de Dados Abertos do MMA, baseado em CKAN, com API do catálogo e recursos de download. O catálogo federal mantém recurso atualizado até março de 2026. Recursos do MMA registram licença Creative Commons Atribuição.

### Correções da avaliação anterior

A primeira versão corrigiu autenticação e documentação, mas deixou passar usos semanticamente incorretos ou desatualizados:

- `temporal_resolution=atualização administrativa` descreve processo/frequência de manutenção, não resolução temporal;
- `programmatic_access=não` ignora o caminho oficial via catálogo CKAN;
- `data_access_url` apontava apenas ao catálogo federal, embora a própria plataforma CNUC seja o canal primário de consulta e relatório.

### Decisão

- `data_access_url` → `https://cnuc.mma.gov.br/`;
- `data_formats` → `CSV | PDF | Shapefile | KML`;
- `authentication_required` → `não` para a consulta pública;
- `access_conditions` → explicitar consulta pública sem login e área restrita separada para gestores;
- `programmatic_access` → `parcial`, porque há catálogo CKAN/API e downloads HTTP, enquanto a plataforma primária permanece orientada à web;
- `access_protocols` → `CKAN API | HTTP download`;
- `access_documentation_url` → serviço gov.br;
- `temporal_resolution` → `não se aplica`;
- `verification_url` → serviço gov.br, mantendo o dataset como evidência complementar;
- manter licença Creative Commons Atribuição já registrada.

---

## Resumo revisado

| ID | Resultado | Correções candidatas |
|---|---|---|
| DR0011 | VERIFIED_WITH_CORRECTION | data_formats; authentication_required |
| DR0012 | VERIFIED_WITH_CORRECTION | data_formats; data_access_url |
| DR0013 | VERIFIED_WITH_CORRECTION | authentication_required; data_formats; access_protocols |
| DR0014 | VERIFIED_NO_CHANGE | — |
| DR0015 | VERIFIED_WITH_CORRECTION | access_documentation_url; verification_url |
| DR0016 | VERIFIED_WITH_CORRECTION | data_access_url; data_formats; authentication_required; access_conditions; programmatic_access; access_protocols; access_documentation_url; temporal_resolution; verification_url |

## Qualidade e lição operacional

A revisão cruzada demonstrou que **CI verde não prova completude científica da auditoria**. A partir deste bloco, a rotina deve incluir uma checagem adversarial mínima antes de consolidar uma fila:

1. procurar contradição entre acesso público e autenticação de API/área restrita;
2. verificar se formatos e protocolos foram separados corretamente;
3. testar se `temporal_resolution` não está recebendo frequência de atualização;
4. preferir evidência oficial representativa da entidade, não apenas de um componente;
5. conferir se toda afirmação nova aparece explicitamente na evidência oficial atual.

As correções permanecem candidatas `AUTO-SAFE` porque estão dentro do contrato congelado e são sustentadas por fontes oficiais, mas só podem tocar o CSV depois de checagem exata do valor atual e diff linha a linha.