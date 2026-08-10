# Vitrine Ciência — piloto de auditoria científica DR0001–DR0004

Data: 2026-08-10 (`America/Sao_Paulo`)  
Escopo: testar o contrato canônico existente antes da auditoria sequencial 51/51.  
Autoridade factual: páginas/documentação oficiais atuais.  
Legado: usado apenas como pista; nunca como autoridade automática.

## Regra do piloto

Para cada fonte:

`linha canônica atual → payload legado correspondente → fonte oficial atual → decisão campo a campo`

Este pacote **não altera o CSV canônico**. Ele identifica correções inequívocas e testa se os 34 campos atuais são suficientes sem expansão de schema.

## DR0001 — Clima Gerais

### Evidência oficial atual

- `https://clima-gerais.meioambiente.mg.gov.br/`
- `https://clima-gerais.meioambiente.mg.gov.br/vulnerabilidade-territorial`

A página oficial identifica Clima Gerais como ferramenta de apoio aos municípios mineiros para desenvolvimento de baixo carbono e adaptação territorial e como produto do Plano de Energia e Mudanças Climáticas de Minas Gerais. O módulo de vulnerabilidade apresenta resultados por município/território, índice composto por sensibilidade, exposição e capacidade de adaptação, e disponibiliza tabela do banco de dados.

### Decisão

A linha atual permanece semanticamente coerente para identidade, finalidade, cobertura de Minas Gerais, tipo de informação e limitação de uso do índice. `free_download=parcial` continua prudente porque existe download em módulo específico, mas isso não prova download universal de todo conteúdo.

Manter `authentication_required=desconhecido`: navegação pública sem login não é, isoladamente, prova suficiente de que todo acesso da plataforma nunca exige autenticação.

Manter licença como não localizada no nível dos dados: o rodapé protege concepção/produção do site, mas não estabelece de forma inequívoca uma licença de dados reutilizável.

**Correção canônica imediata identificada:** nenhuma.

## DR0002 — IDE-Sisema

### Evidência oficial atual

- Geoportal atual: `https://geoportal.meioambiente.mg.gov.br/`
- Geovisualizador: `https://visualizador.idesisema.meioambiente.mg.gov.br/`
- Webservices/documentação: `https://geoportal.meioambiente.mg.gov.br/webservices`
- Catálogo de metadados: `https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/search?type=dataset`

O Geoportal atual se apresenta como **IDE-Sisema 3.0** e organiza Geovisualizador, Geoserviços, Metadados e histórico de atualizações. A documentação oficial confirma WMS, WFS, WCS e CSW; o catálogo registra metadados, formatos, escalas e frequências por camada. O Geovisualizador atual permanece acessível no domínio já registrado.

### Correções inequívocas candidatas

1. `homepage_url`
   - atual: `https://idesisema.meioambiente.mg.gov.br/`
   - candidato: `https://geoportal.meioambiente.mg.gov.br/`
   - motivo: o domínio atual da homepage pública institucional é o Geoportal 3.0; `idesisema...` permanece relevante como catálogo/serviço específico.

2. `access_protocols`
   - atual: `WMS | WFS`
   - candidato: `WMS | WFS | WCS | CSW`
   - motivo: os quatro protocolos são explicitamente documentados pelo Geoportal.

3. `access_documentation_url`
   - atual: vazio
   - candidato: `https://geoportal.meioambiente.mg.gov.br/webservices`
   - motivo: documentação oficial diretamente correspondente ao acesso programático/protocolos.

4. `verification_url`
   - candidato: `https://geoportal.meioambiente.mg.gov.br/`

### Correção semântica recomendada para etapa de implementação

`data_formats` atualmente mistura protocolos (`WMS | WFS`) com formatos. O catálogo oficial registra, entre outros, GeoJSON, KML, Shapefile e XLSX, enquanto a documentação de WCS trata formatos raster variáveis. A implementação deve remover protocolos de `data_formats` e preservar os protocolos em `access_protocols`, sem tentar enumerar todos os formatos de todas as camadas.

## DR0003 — AdaptaBrasil MCTI

### Evidência oficial atual

- apresentação: `https://adaptabrasil.mcti.gov.br/index.php/sobre`
- metodologia: `https://adaptabrasil.mcti.gov.br/sobre/metodologia`
- índices e indicadores: `https://adaptabrasil.mcti.gov.br/sobre/lista-de-indicadores`
- termos de uso: `https://adaptabrasil.mcti.gov.br/sobre/termos-de-uso`

A página oficial confirma a identidade de **Sistema de Informações e Análises sobre Impactos das Mudanças do Clima**, objetivo de consolidar/integrar/disseminar informação sobre impactos observados e projetados no território nacional e governança MCTI–INPE–RNP. A metodologia é organizada por setores estratégicos. Os termos de uso declaram todos os dados públicos, abertos e gratuitos e informam licença **Creative Commons CC-BY-SA**, além de formato explícito de referência da fonte.

### Correções inequívocas candidatas

1. `license`
   - atual: `não localizada`
   - candidato: `CC BY-SA (versão não especificada na página oficial consultada)`

2. `access_documentation_url`
   - atual: vazio
   - candidato: `https://adaptabrasil.mcti.gov.br/sobre/termos-de-uso`

3. `verification_url`
   - manter uma página oficial de apresentação; a rota `https://adaptabrasil.mcti.gov.br/index.php/sobre` continua adequada.

### Campos mantidos conservadoramente

`free_download=parcial` não deve ser promovido automaticamente a `sim` apenas porque os termos dizem dados públicos/abertos/gratuitos; o campo canônico descreve **download**, e o piloto não verificou uma única rota de download universal para todo o sistema.

`authentication_required=desconhecido` permanece até evidência oficial específica de autenticação do sistema/rotas de acesso.

## DR0004 — SIRENE

### Evidência oficial atual

- seção SIRENE no MCTI: `https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene`
- descrição institucional indexada: `https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/indicadores/paginas/backup/dados-abertos-mctic/sirene-sistema-de-registro-nacional-de-emissoes`
- emissões por UF: `https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/publicacoes/emissoes-por-unidade-federativa`

A documentação oficial continua descrevendo o SIRENE como instrumento oficial para disponibilização dos resultados nacionais de emissões e remoções de GEE, com função de transparência/MRV. A série histórica começa em 1990; resultados e produtos variam por edição/setor. Páginas atuais do SIRENE continuam publicando fatores de emissão, inventários e materiais em formatos como XLSX.

### Decisão

Identidade, descrição, cobertura nacional, início temporal em 1990, variabilidade por edição e limitações atuais permanecem coerentes.

Manter `license=dados públicos; licença específica não localizada`: a licença geral do conteúdo do portal `gov.br` não deve ser automaticamente promovida a licença universal de todos os datasets/produtos do SIRENE.

**Correção canônica imediata identificada:** nenhuma.

## Resultado do teste do contrato

O piloto não encontrou necessidade de nova coluna para concluir a triagem das quatro fontes.

Informações como URL de metodologia, catálogo de metadados e orientação de citação são úteis como **evidência de auditoria**, mas não devem ser empurradas para campos semanticamente incorretos. No modelo delimitado atual:

- metodologia específica de produto já possui `methodology_url` na tabela de produtos;
- evidência oficial adicional pode ficar na trilha de auditoria;
- uma futura proposta de nova coluna deve provar ganho material de descoberta e será mudança de contrato, não reação automática a uma fonte específica.

## Correções candidatas prontas para implementação

### DR0002
- atualizar homepage para Geoportal IDE-Sisema 3.0;
- adicionar WCS e CSW aos protocolos;
- registrar página oficial de webservices como documentação de acesso;
- separar formatos de dados de protocolos;
- atualizar URL representativa de verificação.

### DR0003
- registrar licença CC BY-SA com versão não especificada na página consultada;
- registrar os Termos de Uso como documentação de acesso.

### DR0001 e DR0004
- nenhuma correção inequívoca necessária no piloto.

## Próximo passo

1. integrar o contrato e este relatório como pacote `AUTO-SAFE`;
2. aplicar as correções candidatas em um pequeno pacote DATA, preservando exatamente as outras 49 linhas e todos os campos não afetados;
3. validar build/dados/diff;
4. iniciar a auditoria sequencial a partir de `DR0001`, registrando `last_verified` apenas quando a linha completa tiver sido efetivamente revalidada.