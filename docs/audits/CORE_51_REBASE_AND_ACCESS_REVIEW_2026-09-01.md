# Rebase do núcleo 51 e revisão de acesso — 2026-09-01

## Decisão materializada neste pacote

A superfície viva volta ao conjunto auditado de **51 fontes** consolidado em 10/08/2026, com os **11 produtos** e **19 distribuições** então existentes. O ponto de restauração das fontes é o conteúdo incorporado pelo merge `4caa4b866b3e84af2ad0b04b9f152e641721ad83`, posterior à auditoria oficial 51/51.

A expansão posterior da release v1.0.0 (135/843/876) não é apagada: suas três tabelas são preservadas sem alteração em `data/quarantine/v1.0.0-expanded/` e continuam sendo a referência local para validar o DOI histórico.

## Por que 51, e não “58”

A evidência canônica de 09–10/08/2026 registra **51 fontes** preservadas e auditadas. Não foi encontrada uma baseline estável de 58 fontes que tivesse autoridade superior a esse estado 51/51. Por isso, 51 é o núcleo tecnicamente defensável para restauração.

## Achados de acesso já conhecidos

A auditoria oficial 51/51 registrou correções factuais em 43 fontes e manteve incertezas explícitas em parte do catálogo. A revisão de produto/distribuição naquela etapa ainda era parcial. O pacote atual, portanto, não converte lacunas em certeza.

A nova regra pública usa cinco classes de triagem:

- **A — download direto**: arquivo ou endpoint de download estável;
- **B — landing page do dataset**: página específica com caminho explícito de download;
- **C — portal/API de dados**: consulta, recorte ou extração claramente disponível;
- **D — visualização/documentação**: mapa, PDF, ficha técnica ou documentação sem rota suficiente de obtenção dos dados;
- **E — restrito/quebrado/incerto**: acesso não demonstrado ou dependente de revisão.

A–C podem ser destinos principais. D–E devem ser identificados como revisão/contexto e não como “download de dados”.

## Produtos do núcleo

Dos 11 produtos históricos, PRODES, DETER, TerraClass, vegetação secundária e Dynamic World são datasets/séries. `Serviços interoperáveis TerraBrasilis`, `Earth Engine Public Data Catalog`, `Earth Engine Publisher Data Catalogs` e `Earth Engine Processing and Export Service` são infraestrutura de serviço/descoberta e devem aparecer com esse papel explícito, não como datasets equivalentes.

## Itens que exigem atenção humana

1. fontes em que `homepage_url` e `data_access_url` coincidem;
2. fontes com `free_download` e `programmatic_access` ainda desconhecidos;
3. destinos PDF/documentação/visualização sem caminho demonstrado para obtenção dos dados;
4. produtos/serviços que apenas indexam datasets de terceiros;
5. qualquer registro reintroduzido da expansão v1.0.0.

O objetivo da quarentena é permitir revisão registro a registro sem perder proveniência nem reescrever a release.
