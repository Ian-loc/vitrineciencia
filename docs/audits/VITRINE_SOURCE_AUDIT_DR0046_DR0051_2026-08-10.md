# Vitrine Ciência — auditoria científica DR0046–DR0051

Data: 2026-08-10 (`America/Sao_Paulo`)  
Base: `main@bc2d711e7c6df07ec710e7fd730ded9e9f53017b`  
Contrato: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`  
QA: `docs/VITRINE_SCIENTIFIC_AUDIT_CHECKLIST.md`

## Método

`linha canônica → legado como pista → fonte oficial atual → decisão campo a campo → checagem adversarial`

Este é o último bloco da auditoria de fontes. A fonte oficial atual prevalece. A revisão separa download de consulta pública, infraestrutura de dataset, formato de protocolo e conteúdo público de base integral não aberta.

---

## DR0046 — EDGAR

### Evidência oficial atual

- edição GHG 2025: `https://edgar.jrc.ec.europa.eu/dataset_ghg2025`
- metodologia: `https://edgar.jrc.ec.europa.eu/methodology`

A edição `EDGAR_2025_GHG` permanece a edição atual de referência do inventário global de gases de efeito estufa, cobrindo 1970–2024. A página fornece tabelas e grades por gás/setor/país e downloads diretos, inclusive NetCDF e formatos tabulares. A metodologia oficial mantém abordagem harmonizada por dados de atividade, tecnologia, abatimento e fatores de emissão.

A página de condições de uso declara que, salvo indicação em contrário, material de titularidade da União Europeia é licenciado sob **CC BY 4.0**. Componentes/dados derivados de terceiros, como IEA-EDGAR CO₂, mantêm obrigações de fonte/termos próprios. A página fornece citação explícita da edição.

### Checagem adversarial

`data_formats=... | mapas` mistura formato com produto de visualização. A licença atual pode ser registrada de forma mais precisa sem generalizar CC BY 4.0 para componentes não pertencentes à UE.

### Decisão

- `data_formats` → `NetCDF | XLSX | CSV`;
- `license` → `CC BY 4.0 para material da União Europeia salvo indicação contrária; componentes de terceiros mantêm termos/fonte próprios`;
- manter autenticação `não`, download aberto, edição/cobertura e limitações atuais;
- não criar campo de frequência de atualização da base: versões/edições são publicadas, mas não há cadência normativa única a mapear em `temporal_resolution`.

---

## DR0047 — Copernicus Data Space Ecosystem (CDSE)

### Evidência oficial atual

- homepage: `https://dataspace.copernicus.eu/`
- ecosystem: `https://documentation.dataspace.copernicus.eu/Ecosystem.html`
- APIs: `https://documentation.dataspace.copernicus.eu/APIs.html`
- S3: `https://documentation.dataspace.copernicus.eu/APIs/S3.html`

CDSE continua garantindo acesso aberto e gratuito a dados Copernicus e serviços centrais. A documentação distingue explicitamente:

1. serviços abertos/gratuitos disponíveis sem registro;
2. dados e serviços abertos/gratuitos disponíveis para usuários registrados com capacidade configurada;
3. serviços adicionais/federados/comerciais em partes do ecossistema.

O catálogo e os dados podem ser acessados por OData, STAC, Sentinel Hub APIs, openEO, S3 e serviços OGC. S3 exige conta e credenciais; serviços OGC podem exigir identificador/configuração de instância conforme o serviço.

### Checagem adversarial

A linha atual usa `authentication_required=sim` e `access_conditions=cadastro`, absolutos demais para uma infraestrutura que também oferece serviços públicos sem registro.

### Decisão

- `authentication_required` → `parcial`;
- `access_conditions` → `serviços/dados públicos gratuitos sem registro em canais selecionados | conta para serviços/capacidades registradas e credenciais de APIs específicas | serviços adicionais podem ter condições próprias`;
- manter `free_download=sim`, `programmatic_access=sim`, protocolos, formatos, política Copernicus e limitação de registrar missão/nível/resolução/data;
- manter artigo de 2026 como evidência acadêmica e página principal como verificação.

---

## DR0048 — Earth System Grid Federation (ESGF)

### Evidência oficial atual

- homepage: `https://esgf.github.io/`
- user guide/search API: `https://esgf.github.io/esgf-user-support/user_guide.html`
- FAQ: `https://esgf.github.io/esgf-user-support/faq.html`
- MetaGrid: `https://metagrid.esgf-west.org/` (destino oficial atual indicado pela homepage ESGF)

ESGF permanece infraestrutura federada e open source para dados do sistema terrestre. A homepage oficial direciona usuários de CMIP para o MetaGrid em beta. Busca de projetos públicos pode ser feita sem conta; downloads de alguns projetos e recursos exigem conta/grupo/autorização. A busca possui RESTful API distribuída. Ferramentas como Wget, Globus, Synda e scripts Python são clientes/métodos, não protocolos do catálogo.

### Decisão

A linha atual está correta em `authentication_required=parcial`, licença por projeto/dataset, MetaGrid e natureza federada.

Correção semântica:

- `access_protocols` → `REST API de busca | HTTP/HTTPS download`.

Não converter clientes de linha de comando em protocolo. Não atribuir uma licença única à federação.

---

## DR0049 — ILTER / DEIMS-SDR

### Evidência oficial atual

- ILTER: `https://www.ilter.network/`
- DEIMS-SDR: `https://deims.org/`
- termos: `https://deims.org/terms`
- recuperação de dados: `https://deims.org/docs/export.html`

DEIMS-SDR é o registro de sítios/datasets/sensores associado ao ecossistema LTER e disponibiliza publicamente conteúdo próprio. Os termos atuais estabelecem **CC BY-NC 4.0** para o conteúdo/dados disponibilizados pelo serviço e uso não comercial; dados disponíveis no DEIMS-SDR podem ser usados sem conta. Conta é voltada principalmente à representação/gestão de registros.

O serviço oferece:

- REST API em JSON/CSV;
- WMS/WFS para sítios, com formatos derivados como Shapefile, GeoPackage, GeoJSON e CSV;
- CSW/OAI-PMH para metadados ISO 19139;
- pacote Python como ferramenta cliente.

A ILTER continua sendo rede de redes; datasets vinculados externamente podem estar em outros repositórios com condições próprias.

### Checagem adversarial

A linha atual usa `formatos variados` e `REST API DEIMS-SDR | exportação de metadados`, subdescrevendo interfaces oficiais. A licença `varia conforme o dataset` não representa corretamente o conteúdo próprio do DEIMS-SDR, embora continue válida para datasets externos associados.

### Decisão

- `data_formats` → `JSON | CSV | Shapefile | GeoPackage | GeoJSON; datasets associados podem variar`;
- `access_protocols` → `REST API | WMS | WFS | CSW | OAI-PMH | HTTP export`;
- `access_conditions` → `conteúdo DEIMS-SDR público e gratuito sem conta; uso não comercial sob termos do serviço; datasets externos associados podem ter condições próprias`;
- `license` → `DEIMS-SDR CC BY-NC 4.0 para conteúdo/registros do serviço; datasets externos associados podem ter licenças próprias`;
- manter `authentication_required=não` para o conteúdo disponibilizado diretamente pelo DEIMS-SDR; não promover restrições de repositórios externos a uma regra de login da plataforma;
- manter `free_download=parcial` porque a entrada ILTER agrega também dados externos cuja disponibilidade varia.

---

## DR0050 — ORNL Distributed Active Archive Center (ORNL DAAC)

### Evidência oficial atual

- centro NASA Earthdata: `https://www.earthdata.nasa.gov/centers/ornl-daac`
- login: `https://daac.ornl.gov/sign_in.shtml`
- submissão/curadoria: `https://daac.ornl.gov/submit/submit.html`
- exemplos atuais de datasets 2026 no catálogo NASA Earthdata/ORNL DAAC

ORNL DAAC continua publicando dados de ecologia terrestre, biogeoquímica, carbono, campanhas e produtos de missões com DOI, user guide, metadados estruturados no CMR e citação por dataset. Downloads de arquivos exigem NASA Earthdata Login; metadados e landing pages são publicamente consultáveis. Dados publicados podem ter múltiplos formatos e serviços, incluindo HTTP/cloud, THREDDS e serviços OGC em produtos/ferramentas apropriados.

O processo oficial de curadoria confirma revisão de qualidade, preparação de metadados, user guide, DOI e publicação no CMR/Earthdata Search. Datasets recentes de 2026 continuam exibindo citação por DOI e condição de compartilhamento conforme NASA Earthdata Data Use Guidance.

### Checagem adversarial

A linha atual já representa adequadamente autenticação de download, variedade por dataset e obrigação de citar DOI/versão. `verification_url`, porém, aponta para a tela de login, que verifica apenas autenticação e não a identidade/escopo do centro.

### Decisão

- `verification_url` → `https://www.earthdata.nasa.gov/centers/ornl-daac`;
- manter `authentication_required=sim` porque downloads/pedidos de dados exigem Earthdata Login, apesar de metadados públicos;
- manter `license=política de dados NASA; licença por dataset` de forma conservadora;
- manter CMR/API/OGC/download e formatos variáveis por produto.

---

## DR0051 — Project COSMOS

### Evidência oficial atual

- homepage: `https://interactive.carbonbrief.org/cosmos/index.html`
- metodologia/acesso: `https://interactive.carbonbrief.org/cosmos/methodology/index.html`

Project Cosmos foi lançado pelo Carbon Brief em junho de 2026. A metodologia atual confirma **1.816.639 publicações únicas** e pouco mais de 40 milhões de relações de citação, construídas a partir do corpus IPCC, citações, 22 periódicos climáticos, OpenAlex e Google Scholar. Os estudos dos periódicos climáticos foram extraídos até **31 de dezembro de 2025**.

A metodologia é explícita sobre acesso:

- a base integral **não é open source**;
- Carbon Brief deliberadamente não a disponibiliza abertamente devido a risco de scraping/uso por bots;
- pesquisadores podem enviar propostas para estudos/projetos coautorados;
- a base será **atualizada e expandida ao fim de cada ano-calendário**;
- produtos públicos incluem rankings, mapa e metodologia.

O conteúdo público do artigo/metodologia é publicado sob licença CC para reprodução não adaptada e não comercial com crédito ao Carbon Brief; isso não torna a base integral aberta.

### Checagem adversarial

`data_formats=visualização web | ...` usa interface como formato. A atualização anual é frequência de manutenção da base e **não** deve ser colocada em `temporal_resolution`.

### Decisão

- `data_formats` → `não se aplica — base integral sem formato público de download; metadados selecionados são exibidos na interface`;
- `limitations` → atualizar para explicitar base não open source, propostas de colaboração e atualização/expansão ao fim de cada ano-calendário;
- manter `free_download=não`, `programmatic_access=não`, `authentication_required=não`, produtos públicos e cobertura bibliográfica até 31-12-2025;
- manter licença do conteúdo público separada da indisponibilidade da base integral.

---

## Resumo

| ID | Resultado | Correções candidatas |
|---|---|---|
| DR0046 | VERIFIED_WITH_CORRECTION | data_formats; license |
| DR0047 | VERIFIED_WITH_CORRECTION | authentication_required; access_conditions |
| DR0048 | VERIFIED_WITH_CORRECTION | access_protocols |
| DR0049 | VERIFIED_WITH_CORRECTION | data_formats; access_protocols; access_conditions; license |
| DR0050 | VERIFIED_WITH_CORRECTION | verification_url |
| DR0051 | VERIFIED_WITH_CORRECTION | data_formats; limitations |

## Checagem adversarial final

- autenticação de serviços específicos do CDSE não foi promovida a requisito universal;
- ferramentas/clients ESGF não foram tratadas como protocolos;
- licença do conteúdo próprio DEIMS-SDR foi separada das licenças de datasets externos;
- login ORNL para download não foi confundido com acesso público a metadados;
- conteúdo público do Cosmos não foi confundido com abertura da base integral;
- atualização anual do Cosmos não foi mapeada para resolução temporal;
- nenhum campo novo foi necessário.

## Marco 51/51

Com este bloco, as **51 fontes canônicas (`DR0001`–`DR0051`) possuem audit trail atual baseado em fontes oficiais**, incluindo filas estruturadas de correção ou decisão explícita de não alterar.

Isso ainda não significa que o CSV canônico foi corrigido: as mudanças permanecem nas filas para uma etapa de aplicação controlada e auditada.

## Próxima ação

1. integrar este audit trail como `AUTO-SAFE` após CI/diff/threads;
2. consolidar todas as filas de correção `DR0001–DR0051`;
3. executar auditoria cruzada final para detectar contradições/duplicações entre filas;
4. aplicar o conjunto aprovado ao `data/data_resources.csv` em atualização governada com diff completo;
5. executar validadores/build e verificar que continuam 51 fontes, 11 produtos e 19 distribuições;
6. classificar a atualização canônica como `REVIEW` se o delta agregado for materialmente grande, mesmo que cada correção individual seja inequívoca;
7. depois iniciar auditoria científica 11/11 produtos e 19/19 distribuições.