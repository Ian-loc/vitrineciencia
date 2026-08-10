# Vitrine Ciência — auditoria científica DR0011–DR0016

Data da auditoria: 2026-08-10  
Escopo: `DR0011`–`DR0016`  
Base canônica: `main@8367618449c735020bab94401128dc403932ad87`

## Regra

Esta auditoria usa a linha canônica atual como ponto de partida, o legado #63 apenas como pista e documentação oficial atual como autoridade. Nenhum valor é promovido por inferência. Fatos sem campo semanticamente adequado permanecem na trilha de auditoria.

Prioridade de evidência: produtor/provedor oficial → documentação/metadados oficiais → serviço/API oficial → publicação primária quando necessária.

## DR0011 — TerraBrasilis

### Estado atual

A entrada representa corretamente o TerraBrasilis como plataforma do INPE para descoberta e acesso a produtos de monitoramento da vegetação nativa, distinguindo produtos como PRODES e DETER.

### Evidência oficial atual

- Catálogo GeoNetwork TerraBrasilis: https://terrabrasilis.dpi.inpe.br/geonetwork/
- O catálogo oficial registra datasets com formatos como Shapefile, GeoPackage, GeoTIFF, CSV e outros, variando por produto.
- Metadados oficiais registram serviços OGC, incluindo WMS/WFS, no nível de recursos/produtos.

### Avaliação

**Conceito: coerente.**

Há, porém, uma mistura semântica no campo `data_formats`: `serviços OGC` não é formato de arquivo; é mecanismo/protocolo de acesso. O campo `access_protocols` já é o lugar correto para WMS/WFS.

Também convém evitar tratar `GeoNetwork` como protocolo científico; ele é catálogo/serviço de metadados. A documentação de acesso atual pode continuar apontando ao GeoNetwork/API.

### Correção inequívoca candidata

- `data_formats`: remover `serviços OGC` e manter apenas formatos efetivamente documentados, com indicação de variação por produto.

Nenhuma frequência única de atualização deve ser inventada no nível da plataforma.

---

## DR0012 — Programa Queimadas / BDQueimadas

### Evidência oficial atual

- Portal oficial: https://terrabrasilis.dpi.inpe.br/queimadas/portal/
- FAQ oficial: https://terrabrasilis.dpi.inpe.br/queimadas/portal/informacoes/perguntas-frequentes/
- O BDQueimadas mantém acervo histórico de focos desde 1998 e oferece produtos operacionais de fogo.
- A documentação oficial informa atualização de focos em intervalo operacional curto e disponibilização pública/gratuita.
- O ecossistema oferece WMS/WFS e exportações/downloads por produto.

### Avaliação

**Conceito: coerente.** A limitação atual — foco de calor não equivale automaticamente a incêndio ou área queimada — deve ser preservada.

O campo `data_formats` mistura formatos, serviços OGC e `visualização web`. Serviços e interface não são formatos.

### Correção inequívoca candidata

- `data_formats`: manter apenas formatos de dados documentados; remover `serviços OGC` e `visualização web` do campo.

WMS/WFS permanecem corretamente no domínio de `access_protocols`.

Não converter a cadência operacional de atualização dos focos em `temporal_resolution`: são conceitos diferentes.

---

## DR0013 — speciesLink

### Evidência oficial atual

Política de compartilhamento: https://specieslink.net/data_sharing_policy

A política oficial sustenta:

- acesso e compartilhamento aberto dos dados da rede;
- CC BY 4.0 para dados textuais da rede;
- CC BY-SA 4.0 para imagens;
- necessidade de preservar atribuição e condições adicionais quando estabelecidas pela coleção/provedor.

### Avaliação

**Linha atual coerente.** A distinção de licenças e a cautela com condições por coleção já estão corretamente representadas.

A entrada também registra que a API exige chave; nenhuma modificação é aplicada nesta auditoria sem uma nova necessidade material.

### Decisão

- nenhuma correção inequívoca imediata.

---

## DR0014 — SiBBr

### Evidência oficial atual

Embora o acesso automatizado à página principal do SiBBr possa ser limitado por regras do site, fontes governamentais atuais confirmam sua função ativa:

- MMA — mapas e dados de biodiversidade: https://www.gov.br/mma/pt-br/assuntos/biodiversidade-e-biomas/mapas-e-dados
- MMA — painéis de biodiversidade: https://www.gov.br/mma/pt-br/assuntos/biodiversidade-e-biomas/painel-de-dados
- ICMBio informa publicação/migração de dados de biodiversidade para o SiBBr: https://www.gov.br/icmbio/pt-br/assuntos/centros-de-pesquisa/biodiversidade-e-dados/portal-da-biodiversidade
- IBGE continua usando dados disponíveis no SiBBr em avaliações nacionais de biodiversidade.

### Avaliação

**Linha atual deliberadamente conservadora e adequada.** Identidade, função nacional e integração de dados são sustentadas. Autenticação, APIs e uma licença única continuam variando ou sem confirmação proporcional suficiente no nível da infraestrutura.

### Decisão

- nenhuma correção inequívoca imediata;
- não preencher `programmatic_access`, `access_protocols` ou `authentication_required` por aproximação.

---

## DR0015 — BDiA / IBGE

### Evidência oficial atual

Página oficial IBGE: https://www.ibge.gov.br/geociencias/informacoes-ambientais.html

O IBGE descreve o Banco de Dados e Informações Ambientais como plataforma pública para informações de Geologia, Geomorfologia, Pedologia e Vegetação, com visualização e download em diferentes formatos. A documentação atual informa ciclo de atualização bienal dos conteúdos e disponibiliza documentação metodológica temática.

### Avaliação

**Linha atual conceitualmente coerente.** O fato de haver atualização bienal é relevante para a trilha de auditoria, mas o schema de fonte atual não possui `update_frequency`. Ele não deve ser colocado em `temporal_resolution`.

### Decisão

- nenhuma correção canônica obrigatória nesta rodada;
- preservar atualização bienal como evidência até existir uso semanticamente adequado dentro do contrato atual.

---

## DR0016 — Cadastro Nacional de Unidades de Conservação (CNUC)

### Evidência oficial atual

- MMA — CNUC: https://www.gov.br/mma/pt-br/composicao/sbio/dap/cadastro-nacional-de-ucs/cadastro-nacional-de-ucs
- Serviço gov.br: https://www.gov.br/pt-br/servicos/consultar-o-cadastro-nacional-de-unidades-de-conservacao-da-natureza
- Dataset oficial: https://dados.gov.br/dados/conjuntos-dados/unidadesdeconservacao

A documentação atual confirma:

- CNUC é a base oficial das UCs do SNUC, gerida pelo MMA em colaboração com gestores federais, estaduais e municipais;
- consulta pública é gratuita e não exige cadastro/login;
- o dataset oficial possui atualização de março de 2026, compatível com a linha atual;
- relatórios e downloads públicos estão disponíveis em formatos documentados pelo serviço/dataset.

### Avaliação

A linha atual usa `authentication_required=não se aplica`. Para um serviço público que explicitamente não exige login, **`não` é semanticamente mais preciso**.

A página gov.br também é uma boa documentação de acesso e pode preencher `access_documentation_url` sem inferência.

A licença não deve ser alterada com base apenas na licença do conteúdo da página gov.br; licença do site e licença do dataset não são automaticamente equivalentes.

### Correções inequívocas candidatas

- `authentication_required`: `não se aplica` → `não`;
- `access_documentation_url`: preencher com o serviço gov.br oficial.

---

## Resumo do bloco

| ID | Resultado | Correção inequívoca candidata |
|---|---|---|
| DR0011 | coerente com ajuste semântico | remover serviço OGC de `data_formats` |
| DR0012 | coerente com ajuste semântico | remover serviço OGC/visualização de `data_formats` |
| DR0013 | coerente | nenhuma |
| DR0014 | coerente/conservador | nenhuma |
| DR0015 | coerente | nenhuma; frequência bienal permanece na auditoria |
| DR0016 | coerente com correção de acesso | autenticação=`não`; adicionar documentação oficial de acesso |

## Gate científico

As correções acima são candidatas a `AUTO-SAFE` porque não mudam escopo nem interpretação científica; elas corrigem classificação de campos ou fatos operacionais explicitamente sustentados por fonte oficial. O próximo pacote DATA deve alterar somente os campos listados na fila estruturada correspondente e verificar o diff linha a linha.
