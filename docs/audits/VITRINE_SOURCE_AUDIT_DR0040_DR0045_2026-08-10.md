# Vitrine Ciência — auditoria científica DR0040–DR0045

Data: 2026-08-10 (`America/Sao_Paulo`)  
Base: `main@53f7dac647248e23454f57ab0665868e644774c5`  
Contrato: `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`  
QA: `docs/VITRINE_SCIENTIFIC_AUDIT_CHECKLIST.md`

## Método

`linha canônica → legado como pista → fonte oficial atual → decisão campo a campo → checagem adversarial`

A auditoria preserva condições por dataset/sítio/contribuidor, não transforma ferramentas em protocolos e trata mudança de nome institucional como continuidade quando a própria fonte declara continuidade do serviço.

---

## DR0040 — TRY Plant Trait Database

### Evidência oficial atual

- política de uso: `https://www.try-db.org/TryWeb/DataUsePolicy.php`
- solicitação de dados: `https://www.try-db.org/TryWeb/Prop0.php`
- File Archive/termos: página Data.php e Terms of Service do TRY File Archive

TRY mantém dois regimes principais: registros públicos e registros temporariamente restritos. A solicitação atual declara que, por padrão, trait records públicos estão disponíveis em open access sob **CC BY**; registros restritos exigem permissão dos proprietários. O Data Use Policy proíbe redistribuir os dados a terceiros para evitar versões concorrentes. Solicitações exigem registro e aceite das Intellectual Property Guidelines. O File Archive, complementar ao banco principal, pode ter condições próprias por dataset.

### Decisão

A linha atual representa corretamente cadastro/solicitação, acesso parcial e dependência dos contribuidores, mas `license=termos TRY e dos contribuidores` está pouco informativo.

Correções:
- `access_conditions` → registro + solicitação; dados públicos sob CC BY; registros restritos dependem de permissão; redistribuição não permitida;
- `license` → `CC BY para trait records públicos; registros restritos/arquivos seguem TRY IPG e condições do proprietário`.

Manter `free_download=parcial`, pois parte do acervo pode não ser liberada automaticamente, apesar de não haver cobrança indicada.

---

## DR0041 — BIEN

### Evidência oficial atual

- homepage: `https://bien.nceas.ucsb.edu/bien/`
- Data & Access: `https://bien.nceas.ucsb.edu/bien/data-and-access/`
- RBIEN: `https://bien.nceas.ucsb.edu/bien/tools/rbien/`
- APIs/serviços: páginas dos serviços BIEN, por exemplo NSR/GNRS API

BIEN 4.2 é apresentado como ecossistema integrado e versionado de ocorrências, parcelas, traits e produtos de distribuição. O acesso pode ocorrer por Data Portal, RBIEN, ShinyApps e serviços/APIs. Os serviços de validação aceitam/retornam JSON; o pacote R é uma **ferramenta cliente**, não protocolo. A documentação enfatiza versionamento, filtros de validação e limitações de cobertura.

### Checagem adversarial

`data_formats=CSV | acesso por pacote R e banco` mistura formato com ferramenta/infraestrutura. `access_protocols=pacote R RBIEN | API de serviços BIEN` também mistura ferramenta com protocolo.

### Decisão

- `data_formats` → `CSV | formatos variados conforme produto/serviço`;
- `access_protocols` → `APIs/serviços web BIEN | HTTP download`;
- manter `programmatic_access=sim`, autenticação `não`, versão 4.2, licença variável por fonte e limitações de amostragem/modelagem.

---

## DR0042 — AmeriFlux

### Evidência oficial atual

- data policy: `https://ameriflux.lbl.gov/data/data-policy/`
- download: `https://ameriflux.lbl.gov/data/download-data/`
- API: documentação oficial já registrada na linha canônica

A política atual confirma que a maioria dos sítios usa CC BY 4.0 e parte permanece sob AmeriFlux Legacy Data Policy. Quando um projeto mistura dados CC BY e Legacy, deve seguir a política Legacy para o conjunto combinado. O portal de download coleta a finalidade de uso e fornece DOI/citação por sítio. AmeriFlux possui Data API e pacote `amerifluxr`, mas o pacote é ferramenta cliente, não protocolo.

### Decisão

A linha atual já representa corretamente licença majoritariamente CC BY 4.0, política legada, autenticação e variação por sítio.

Correção semântica:
- `access_protocols` → `Data API | HTTP download`.

Manter `programmatic_access=sim`, `access_documentation_url`, formatos e limitações atuais.

---

## DR0043 — FLUXNET

### Evidência oficial atual

- data policy: `https://fluxnet.org/data/data-policy/`
- portal: `https://data.fluxnet.org/`

FLUXNET mantém políticas distintas por coleção/sítio. O Shuttle segue política open/FAIR CC BY. FLUXNET2015 inclui dados CC BY 4.0 e sítios Tier Two com obrigações adicionais de colaboração/consulta; misturas que incluam Tier Two devem seguir a política mais restritiva. O fluxo oficial de download usa formulário/portal e fornece DOIs/citações por sítio.

### Checagem adversarial

`access_protocols=download por portal | ferramentas comunitárias` não contém protocolos propriamente ditos. A auditoria não encontrou evidência suficiente nesta rodada para declarar uma API pública universal da FLUXNET.

### Decisão

- `access_protocols` → `HTTP download`;
- `license` → `CC BY 4.0 para dados open; Tier Two e outras políticas específicas quando aplicáveis`;
- manter `programmatic_access=parcial` conservadoramente, sem inventar API pública;
- manter autenticação/acesso parciais e limitações por coleção/sítio.

---

## DR0044 — Global Forest Watch → Global Nature Watch

### Evidência oficial atual

- anúncio oficial, 01/07/2026: `https://www.globalforestwatch.org/blog/data-and-tools/gfw-now-global-nature-watch/`
- homepage atual: `https://www.globalforestwatch.org/`
- Global Nature Watch/Horizon: `https://www.globalnaturewatch.org/`
- Data API: `https://data-api.globalforestwatch.org/`

A organização anunciou que **Global Forest Watch está se tornando Global Nature Watch**. A mudança de nome reflete expansão para paisagens/ecossistemas além de florestas. A própria fonte informa que, neste momento, dados, ferramentas, áreas salvas, alertas, links e workflows existentes continuam disponíveis; portanto é continuidade do mesmo produto, não uma nova fonte separada.

A Data API continua ativa no domínio histórico `globalforestwatch.org`, expõe metadados/licença por dataset, downloads e autenticação/API keys para funções específicas. O domínio público também já apresenta branding Global Nature Watch.

### Checagem adversarial

Criar um novo `DR####` duplicaria semanticamente a mesma infraestrutura durante uma mudança de nome. O ID deve permanecer `DR0044`.

A linha atual também mistura `tiles | API` em `data_formats`.

### Decisão

- `resource_name` → `Global Nature Watch`;
- `acronym` → `GNW`;
- `official_identity` → `Plataforma online de monitoramento de natureza, florestas e mudanças em paisagens`;
- `description` → `Plataforma de monitoramento e análise de florestas e outros ecossistemas com dados de múltiplas fontes.`;
- `data_formats` → `GeoTIFF | Shapefile | CSV; varia conforme a camada`;
- `access_protocols` → `REST API | tile services | HTTP download`;
- manter `homepage_url=https://www.globalforestwatch.org/` enquanto a própria organização garante continuidade dos links/workflows e o endereço já serve o branding novo;
- manter licença por camada/provedor e autenticação parcial.

Registrar a antiga identidade Global Forest Watch no audit trail/histórico, não criar duplicata.

---

## DR0045 — Global Carbon Atlas

### Evidência oficial atual

- homepage: `https://globalcarbonatlas.org/`
- Country Emissions: `https://emissions.globalcarbonatlas.org/`
- data use: página `Project → Data use` do Global Carbon Atlas

O Atlas continua sendo plataforma de exploração/visualização de emissões e fluxos, com diferentes produtos e orçamentos. Country Emissions oferece download de datasets em **CSV e XLS**. A política de uso diz que dados e gráficos são disponibilizados gratuitamente para ampla disseminação científica, mas a disponibilidade gratuita **não constitui autorização irrestrita de publicação**; usuários devem dar crédito ao Global Carbon Atlas e às fontes de dados indicadas em cada produto. Métodos e fontes variam por série.

### Checagem adversarial

`data_formats=CSV | visualização web; varia` mistura formato e interface. `access_protocols=downloads e visualizações; API pública não documentada` também mistura mecanismo/interface com observação sobre ausência de API.

### Decisão

- `data_formats` → `CSV | XLS; varia conforme o produto`;
- `access_conditions` → `acesso gratuito; uso/publicação requer crédito ao Global Carbon Atlas e às fontes originais conforme o produto`;
- `access_protocols` → `HTTP download`;
- `license` → `Global Carbon Atlas data-use terms + condições/créditos das fontes originais por produto`;
- manter `programmatic_access=desconhecido`, sem inventar API pública;
- manter temporalidade/resolução variáveis por produto.

---

## Resumo

| ID | Resultado | Correções candidatas |
|---|---|---|
| DR0040 | VERIFIED_WITH_CORRECTION | access_conditions; license |
| DR0041 | VERIFIED_WITH_CORRECTION | data_formats; access_protocols |
| DR0042 | VERIFIED_WITH_CORRECTION | access_protocols |
| DR0043 | VERIFIED_WITH_CORRECTION | access_protocols; license |
| DR0044 | VERIFIED_WITH_CORRECTION | resource_name; acronym; official_identity; description; data_formats; access_protocols |
| DR0045 | VERIFIED_WITH_CORRECTION | data_formats; access_conditions; access_protocols; license |

## Checagem adversarial final

- mudança GFW→GNW foi tratada como renomeação/continuidade, não como nova fonte;
- licenças por contribuinte/sítio/dataset não foram promovidas indevidamente;
- ferramentas R e visualizações não foram classificadas como protocolos/formats;
- acesso gratuito não foi confundido com permissão irrestrita de publicação;
- ausência de API documentada não foi transformada em afirmação de inexistência;
- nenhuma expansão de schema foi necessária.

## Próxima ação

Materializar fila de correções e integrar o audit trail como `AUTO-SAFE`. Depois auditar `DR0046–DR0051`, completando 51/51 fontes. Só então aplicar todas as filas em uma única atualização canônica com diff integral e validação pós-escrita.