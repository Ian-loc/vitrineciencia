# Vitrine Ciência — modelo operacional e pipeline de manutenção

Status: **ACTIVE OPERATING MODEL**

Baseline de referência: `main@1645df4987cd45c64c40a88cf733e9ba5c1f4a40`

## 1. Definição do produto

**Vitrine Ciência is a bounded scientific-data discovery catalog. Its conceptual product model is stable. Future development prioritizes data-volume growth, metadata correction, usability, maintenance and release management.**

Em português: a Vitrine Ciência é um catálogo delimitado para descoberta de dados científicos. O modelo conceitual do produto é estável. O desenvolvimento futuro prioriza aumento do volume de dados, correção de metadados, usabilidade, manutenção e gestão de releases.

A Vitrine deve permanecer simples: ela ajuda o usuário a descobrir, compreender, comparar e acessar fontes e produtos de dados científicos relevantes para o Brasil. Ela não pretende reconstruir a arquitetura interna dos provedores externos.

## 2. Autoridade atual

A autoridade operacional é:

- repositório: `Ian-loc/vitrineciencia`;
- branch canônica: `main`;
- site público: `https://ian-loc.github.io/vitrineciencia/`;
- fontes canônicas: `data/data_resources.csv`;
- produtos canônicos: `data/data_products.csv`;
- distribuições/acessos de produtos: `data/product_distributions.csv`;
- código: MIT;
- metadados e curadoria original: CC BY 4.0.

O baseline atual contém 51 fontes, 11 produtos e 19 distribuições/acessos de produto. Essas três contagens representam tabelas diferentes e nunca devem ser somadas ou descritas como “81 fontes”.

## 3. Fronteira conceitual

### A Vitrine inclui

- catálogo estático de fontes e produtos;
- metadados necessários à descoberta e triagem;
- cobertura espacial e temporal quando sustentada;
- resolução/suporte quando sustentados;
- acesso, formatos, licença, metodologia e citação quando aplicáveis;
- busca, filtros, comparação, visão do catálogo e downloads;
- links para a fonte/produto original;
- documentação pública de método, limites e citação.

### A Vitrine não requer

- PostgreSQL/PostGIS;
- runtime do Simbiotrama;
- reconstrução de catálogos externos;
- genealogia universal produto → release → arquivo → asset;
- enumeração de tiles, bandas, layers, formatos ou endpoints como entidades autônomas;
- download ou cópia de dados de terceiros;
- uma metodologia, frequência ou citação universal quando essas propriedades pertencem a produtos individuais;
- expansão conceitual automática para acomodar uma fonte nova.

Uma nova entidade ou relação só deve ser criada quando a estrutura atual for comprovadamente incapaz de representar uma diferença material necessária à descoberta, compreensão ou acesso.

## 4. Classes de mudança

Toda mudança deve ser classificada antes da execução.

### DATA

Aumenta ou corrige conteúdo do catálogo.

Exemplos: nova fonte, novo produto, correção de URL, licença, cobertura, metodologia, citação, formato, acesso ou metadado.

Esta é a classe normal de desenvolvimento futuro.

### FIX

Corrige defeito observável sem ampliar o modelo conceitual.

Exemplos: busca quebrada, link incorreto, problema mobile, acessibilidade, overflow, filtro, comparação ou download.

### RELEASE

Empacota um estado estável e auditado.

Exemplos: atualização de versão, changelog, tag, GitHub Release, snapshot e Zenodo.

### INFRA

Altera infraestrutura ou contrato estrutural.

Exemplos: analytics, mudança incompatível de schema, novo backend ou nova dependência externa.

INFRA é excepcional e exige gate humano explícito e justificativa de benefício que não possa ser atendido por DATA/FIX.

## 5. Pipeline obrigatório por pacote

Cada pacote segue a mesma sequência:

1. **Scope** — definir problema, classe da mudança, arquivos afetados, fora de escopo e critério de conclusão.
2. **Evidence** — reunir evidência oficial atual para afirmações factuais ou evidência reproduzível para defeitos técnicos.
3. **Implementation** — executar somente o delta necessário em branch criada a partir de `main` atual.
4. **Automated validation** — executar os validadores apropriados ao tipo de mudança.
5. **Diff audit** — confirmar arquivos alterados, ausência de mudanças incidentais e preservação dos dados/contratos não relacionados.
6. **Rendered/public validation** — obrigatório quando a interface ou artefato público puder mudar.
7. **Freeze** — congelar o head final; qualquer alteração posterior invalida o gate anterior.
8. **Human merge gate** — merge somente após autorização humana explícita para o SHA exato quando o pacote exigir gate.
9. **Merge/deploy** — integrar por método governado e publicar quando aplicável.
10. **Post-merge verification** — comprovar que `main`, deploy e comportamento público correspondem ao pacote aprovado.
11. **Consolidation** — somente então registrar o pacote como concluído.

Estados permitidos no relato de progresso:

`PLANNED → EXECUTED → MATERIALIZED → VERIFIED → CONSOLIDATED`.

Somente `VERIFIED`/`CONSOLIDATED` podem ser descritos como realizados. CI verde comprova estrutura/testes, não verdade factual externa.

## 6. Sequência de intervenções

### P0 — saneamento e autoridade

1. tornar este modelo operacional e `WORKFLOW_STATUS.md` a direção ativa;
2. auditar e resolver a cadeia legada de PRs #57–#69;
3. classificar legado como `SALVAGE`, `HISTORICAL`, `SUPERSEDED` ou `REMOVE`;
4. recuperar seletivamente metadados científicos úteis sem importar a arquitetura antiga;
5. limpar/arquivar arquivos ativos obsoletos depois de verificar que sua evidência útil foi preservada;
6. reconstruir o roadmap de analytics sobre `main` atual antes de qualquer merge do PR #76 ou sucessor.

### P1 — contrato e baseline científico

7. congelar o contrato canônico de fonte/produto/distribuição;
8. auditar 51/51 fontes contra evidência oficial atual;
9. auditar 11/11 produtos e 19/19 distribuições;
10. corrigir metadados somente quando sustentados por evidência rastreável;
11. registrar lacunas sem inferência.

### P2 — expansão de volume

12. expandir produtos de alto valor que sejam materialmente distintos;
13. adicionar novas fontes relevantes ao Brasil em lotes coerentes;
14. usar batches pequenos, normalmente 5–10 entradas por PR;
15. nunca transformar arquivos/bandas/endpoints em produtos sem justificativa material.

### P3 — qualidade operacional

16. fortalecer QA de dados, links e relações;
17. acrescentar acessibilidade automatizada e testes de teclado/foco;
18. ampliar cobertura de browser quando o benefício justificar o custo;
19. tornar CI proporcional: data-only, frontend e release executam suites diferentes;
20. manter smoke externo após deploy.

### P4 — release

21. normalizar documentação ativa e política de versionamento;
22. concluir critérios para Vitrine Ciência 1.0.0;
23. criar tag e GitHub Release apenas após baseline científico auditado;
24. gerar snapshot arquivável;
25. depositar release estável no Zenodo e verificar DOI/metadata.

### P5 — analytics

26. somente após baseline/release estável, executar A0: política de privacidade e escolha de provedor;
27. A1: instrumentação mínima, reversível e não bloqueante;
28. A2: histórico durável apenas de agregados;
29. A3: visão interna de uso;
30. A4: pequeno painel público agregado somente após histórico suficiente e nova auditoria de privacidade.

## 7. Regras de curadoria científica

A prioridade de evidência é:

1. página oficial do produtor;
2. documentação/metadados oficiais;
3. API/catálogo oficial;
4. publicação científica primária quando necessária;
5. outras fontes apenas como apoio, nunca para substituir evidência oficial disponível.

Regras:

- não inferir valor ausente;
- não preencher propriedade da plataforma com propriedade de um produto específico;
- distinguir `não encontrado`, `não aplicável`, `desconhecido` e `parcial` quando o schema permitir;
- preservar a granularidade mínima suficiente;
- registrar a data de verificação;
- revalidar links e atributos temporais que podem mudar;
- não copiar datasets de terceiros para o repositório.

## 8. Critério para uma nova fonte

Uma nova fonte entra quando:

- oferece informação científica ou infraestrutura de descoberta relevante;
- tem utilidade material para pesquisa, ensino ou extensão relacionados ao Brasil;
- possui identidade institucional rastreável;
- pode ser descrita sem inventar propriedades não documentadas;
- não duplica semanticamente uma entrada existente sem diferença útil.

## 9. Critério para um novo produto

Um produto recebe linha própria quando possui identidade material independente, por exemplo diferença relevante em:

- finalidade científica;
- metodologia;
- cobertura geográfica;
- cobertura temporal;
- resolução/suporte;
- coleção/versão com significado científico;
- condições ou caminho de acesso.

Não criar produto apenas porque existe outro arquivo, tile, banda, formato ou endpoint.

## 10. Política de PRs e concorrência

- preferir **um pacote de implementação ativo por vez**;
- DATA batches podem coexistir somente se forem independentes e não alterarem as mesmas linhas/contratos;
- PRs legados não contam como trabalho ativo quando formalmente congelados/superseded;
- não empilhar longa cadeia de PRs dependentes;
- branch sempre nasce do `main` atual para pacote novo;
- nunca reutilizar autorização de merge depois que o head muda;
- nunca transferir autorização entre PRs;
- não mesclar pacote “porque o CI está verde” sem cumprir o gate humano aplicável.

## 11. Política de QA proporcional

### DATA-only

Executar no mínimo:

- schema/estrutura;
- IDs únicos;
- relações fonte–produto–distribuição;
- enums;
- URLs e campos obrigatórios;
- geração determinística;
- diff audit.

### FIX/frontend

Além do anterior:

- renderização em navegador real;
- desktop/mobile;
- busca/filtros;
- navegação;
- comparação;
- downloads;
- overflow;
- acessibilidade relevante ao delta.

### RELEASE

Além do anterior:

- suite completa;
- validação de citação/licenças/versão;
- artefato final;
- smoke externo;
- inspeção do snapshot a arquivar.

## 12. Versionamento

Até a auditoria integral do baseline, versões existentes permanecem históricas/pre-release conforme documentação ativa.

Meta para `1.0.0`:

- repositório saneado;
- contrato canônico estável;
- 51 fontes atuais auditadas;
- 11 produtos e 19 distribuições auditados;
- documentação ativa consistente;
- QA e deploy verdes;
- citação/licenças verificadas;
- snapshot reproduzível.

Depois de 1.0.0:

- `1.0.x`: correções compatíveis;
- `1.x.0`: crescimento de dados/produtos e melhorias compatíveis;
- `2.0.0`: somente mudança conceitual incompatível deliberada.

## 13. Recorrência e automação

Trabalho recorrente pode continuar avançando pacotes seguros, mas deve:

- começar do último estado verificado;
- trabalhar em um pacote coerente por rodada;
- nunca declarar execução em background sem tarefa realmente configurada;
- parar em gates humanos reais;
- não fazer merge sem autorização válida para o SHA exato;
- não avançar para arquitetura nova enquanto houver saneamento ou auditoria prioritária pendente;
- registrar somente progresso materializado e verificado.

## 14. Critério de sucesso de longo prazo

O fluxo normal da Vitrine deve convergir para:

**discover → verify → curate → validate → publish → monitor → periodically release**.

O projeto não deve voltar ao ciclo de redesenhar arquitetura continuamente. A maior parte do esforço futuro deve produzir mais conteúdo científico confiável, metadados melhores, correções observáveis e releases reproduzíveis.