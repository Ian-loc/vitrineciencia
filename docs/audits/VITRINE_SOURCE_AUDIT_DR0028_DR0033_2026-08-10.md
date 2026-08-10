# Vitrine Ciência — auditoria científica DR0028–DR0033

Data: 2026-08-10 (`America/Sao_Paulo`)  
Base: `main@d331562b8c7ee22b542fe8f446354cbfdcbb1ab0`  
Contrato: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`  
QA: `docs/VITRINE_SCIENTIFIC_AUDIT_CHECKLIST.md`

## Método

`linha canônica → legado como pista → fonte oficial atual → decisão campo a campo → checagem adversarial`

A fonte oficial atual prevalece. Não preencher lacunas por inferência. Plataformas/federações são avaliadas no nível agregado sem transformar a condição de um único dataset em regra universal.

---

## DR0028 — Movebank

### Evidência oficial atual

- política de dados: `https://www.movebank.org/cms/movebank-content/data-policy`
- contas: `https://www.movebank.org/cms/movebank-content/user-accounts`
- acesso: `https://www.movebank.org/cms/movebank-content/access-data`
- permissões: `https://www.movebank.org/cms/movebank-content/permissions-and-sharing`

Movebank continua sendo plataforma/repositório de rastreamento animal e biologging em que os proprietários controlam a visibilidade e o download por estudo. Visitantes sem conta podem navegar e baixar estudos disponibilizados ao público; conta gratuita é necessária para funções avançadas e para solicitar/receber acesso a dados não públicos. Estudos públicos podem adotar CC0, CC BY ou CC BY-NC; estudos restritos podem ter termos customizados e embargo. Os downloads documentados incluem CSV e formatos para Google Earth, Excel e ESRI ArcGIS.

### Checagem adversarial

A linha atual já usa `authentication_required=parcial`, o que representa corretamente acesso público sem conta + funções/restrições autenticadas. Entretanto `access_conditions=cadastro | aberto ou restrito por estudo` sugere cadastro como condição geral, quando não é necessário para estudos públicos. `access_protocols` mistura REST API com pacotes R e fluxos ao vivo, que são ferramentas/ingestão, não protocolos de acesso.

### Decisão

- `access_conditions` → acesso público sem conta quando autorizado pelo estudo; conta para funções avançadas e solicitação de dados restritos; licenças/embargos por estudo;
- `access_protocols` → `REST API | HTTP download`;
- manter `authentication_required=parcial`, `free_download=parcial`, licença por estudo e limitações de precisão/completude.

---

## DR0029 — NEON

### Evidência oficial atual

- notificação de 23/06/2026: `https://www.neonscience.org/impact/observatory-blog/next-week-required-logins-and-data-licensing-updates`
- homepage atual: `https://www.neonscience.org/`

A partir de **30 de junho de 2026**, downloads exigem conta NEON e login no portal ou token para API/neonUtilities. Os produtos de dados e amostras passaram de CC0 para **CC BY 4.0**. Consulta de informações e visualizações limitadas continua possível sem autenticação.

### Decisão

A linha canônica já incorpora corretamente essa mudança recente:

- `authentication_required=sim` para download/API;
- condições de acesso com conta/token;
- licença CC BY 4.0 para dados obtidos sob a nova política;
- limitação registrando a mudança de 30/06/2026.

**Correção imediata:** nenhuma.

Nota: não remover a referência histórica a CC0 sem verificar a condição jurídica dos downloads efetivamente realizados antes da mudança; a linha atual preserva essa distinção temporal de forma útil.

---

## DR0030 — DataONE

### Evidência oficial atual

- sobre: `https://www.dataone.org/about/`
- participação/busca: `https://www.dataone.org/participate/`
- APIs: `https://dataoneorg.github.io/api-documentation/apis/index.html`
- autenticação/autorização: `https://dataoneorg.github.io/api-documentation/design/Authentication.html`

DataONE permanece uma **federação**, não um repositório único. A busca integrada dá acesso a centenas de milhares de datasets de dezenas de repositórios. A arquitetura REST prevê explicitamente tanto leitura pública anônima (Tier 1) quanto leitura com autenticação/controle de acesso (Tier 2), e cada objeto pode ter política própria.

### Checagem adversarial

A linha atual diz `authentication_required=não`, mas simultaneamente reconhece `aberto ou restrito conforme o dataset`. Isso é semanticamente inconsistente: a federação admite objetos públicos e controlados. `access_protocols` também mistura REST API com clientes R/Python.

### Decisão

- `authentication_required` → `parcial`;
- `access_protocols` → `REST API DataONE | HTTPS/HTTP download`;
- manter `free_download=parcial`, licença/formato/qualidade por dataset e descrição de federação.

Não usar os novos planos DataONE Member/Plus para inferir cobrança sobre acesso científico aos datasets; esses planos dizem respeito a serviços para repositórios/comunidades, não ao regime de cada objeto federado.

---

## DR0031 — KNB

### Evidência oficial atual

- documentação Metacat/KNB: `https://knb.ecoinformatics.org/knb/docs/dataone.html`
- acesso/submissão: `https://knb.ecoinformatics.org/knb/docs/submitting.html`

KNB usa Metacat e participa da federação DataONE. A interface suporta busca/acesso e políticas finas de controle. O serviço DataONE implementado pelo Metacat distingue acesso público anônimo de acesso autenticado/controlado. Para submissão é necessário login via ORCID; datasets podem ter políticas públicas ou restritas.

### Checagem adversarial

Assim como DataONE, `authentication_required=não` é absoluto demais para uma entrada que admite `aberto ou restrito conforme o dataset`. `clientes R e Python` são ferramentas/clientes, não protocolos.

### Decisão

- `authentication_required` → `parcial`;
- `access_protocols` → `REST API DataONE | HTTPS/HTTP download`;
- manter licença/formato/acesso variáveis por dataset e a limitação de possível duplicação com DataONE.

---

## DR0032 — PANGAEA

### Evidência oficial atual

- acesso/reuso: `https://wiki.pangaea.de/wiki/Data_Access_and_Reuse`
- licença: `https://wiki.pangaea.de/wiki/Licence`
- status/moratória: `https://wiki.pangaea.de/wiki/Password`
- OAI-PMH: `https://wiki.pangaea.de/wiki/OAI-PMH`

PANGAEA publica dados Open Access com DOI e metadados públicos; uma pequena fração pode ficar sob moratória, normalmente até dois anos. Datasets protegidos exigem autenticação/autorização; metadados permanecem públicos. Licenças são explícitas por dataset, incluindo CC BY 4.0, CC BY-SA 4.0, CC0 e acordos específicos. Há acesso programático por HTTP/content negotiation e OAI-PMH.

### Checagem adversarial

A linha atual já reconhece “aberto; alguns embargos”, mas usa `authentication_required=não`. Isso contradiz moratórias autenticadas. A condição agregada correta é `parcial`.

### Decisão

- `authentication_required` → `parcial`;
- `access_conditions` → `open access após publicação; pequena fração pode permanecer sob moratória/autenticação; metadados públicos`;
- `license` → `licença explícita por dataset, geralmente Creative Commons; consultar metadados`;
- manter REST/OAI-PMH/download HTTP e DOI por dataset.

---

## DR0033 — Dryad

### Evidência oficial atual

- missão: `https://datadryad.org/mission`
- política de publicação: `https://datadryad.org/publication_policy`
- API: `https://datadryad.org/api`
- busca/API: documentação de descoberta em Dryad
- requisitos de arquivos: `https://datadryad.org/help/submission_steps/files`

Dryad se define atualmente como plataforma comunitária de publicação aberta de **dados de pesquisa em todas as áreas**, não apenas arquivos associados a artigos. Datasets aceitos são publicados ao público sob **CC0**, com DOI. Consulta/download público não requer conta; a API pode ser usada anonimamente e contas/tokens aumentam limites ou permitem criar/modificar submissões. Arquivos não compatíveis com CC0, como software ou certos materiais suplementares, podem ser encaminhados ao Zenodo em publicação associada.

### Checagem adversarial

`authentication_required=não` continua correto para descoberta/download de datasets públicos. `REST API | download HTTP` também está semanticamente correto. A descrição e `data_product_types`, porém, ficaram estreitas ao enfatizar dados associados a publicações e “arquivos suplementares”.

### Decisão

- `description` → repositório multidisciplinar de dados de pesquisa para publicação aberta, curadoria, preservação e reutilização;
- `data_product_types` → `datasets | arquivos de dados | metadados com DOI`;
- manter CC0 1.0, acesso público, API e limitações de que materiais incompatíveis com CC0 não são publicados como dados no Dryad.

---

## Resumo

| ID | Resultado | Correções candidatas |
|---|---|---|
| DR0028 | VERIFIED_WITH_CORRECTION | access_conditions; access_protocols |
| DR0029 | VERIFIED_NO_CHANGE | — |
| DR0030 | VERIFIED_WITH_CORRECTION | authentication_required; access_protocols |
| DR0031 | VERIFIED_WITH_CORRECTION | authentication_required; access_protocols |
| DR0032 | VERIFIED_WITH_CORRECTION | authentication_required; access_conditions; license |
| DR0033 | VERIFIED_WITH_CORRECTION | description; data_product_types |

## Checagem adversarial final

- acesso público foi separado de funções/datasets autenticados;
- clientes R/Python e pacotes não foram tratados como protocolos;
- licenças foram mantidas no nível de estudo/dataset;
- nenhum regime comercial de serviço foi confundido com acesso científico ao conteúdo federado;
- moratórias não foram generalizadas como restrição de todo o repositório;
- nenhum campo novo foi necessário.

## Próxima ação

Materializar a fila de correções e integrar o audit trail como `AUTO-SAFE`. Depois seguir para `DR0034–DR0039`. A aplicação no CSV continua acumulada para uma única atualização canônica auditada após a auditoria 51/51.