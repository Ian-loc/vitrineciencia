# Vitrine Ciência — modelo operacional e pipeline de manutenção

Status: **ACTIVE OPERATING MODEL**

Baseline de referência: `main@ba80cc44d2d2d42d7bda54bff9d84ddff97a5c18`

## 1. Definição do produto

**Vitrine Ciência is a bounded scientific-data discovery catalog. Its conceptual product model is stable. Future development prioritizes data-volume growth, metadata correction, usability, maintenance and release management.**

Em português: a Vitrine Ciência é um catálogo delimitado para descoberta de dados científicos. O modelo conceitual do produto é estável. O desenvolvimento futuro prioriza aumento do volume de dados, correção de metadados, usabilidade, manutenção e gestão de releases.

A Vitrine deve permanecer simples: ela ajuda o usuário a descobrir, compreender, comparar e acessar fontes e produtos de dados científicos relevantes para o Brasil. Ela não pretende reconstruir a arquitetura interna dos provedores externos.

## 2. Autoridade atual

- repositório: `Ian-loc/vitrineciencia`;
- branch canônica: `main`;
- site público: `https://ian-loc.github.io/vitrineciencia/`;
- fontes canônicas: `data/data_resources.csv`;
- produtos canônicos: `data/data_products.csv`;
- distribuições/acessos: `data/product_distributions.csv`;
- código: MIT;
- metadados e curadoria original: CC BY 4.0.

O baseline atual contém **51 fontes, 11 produtos e 19 distribuições/acessos**. Essas contagens pertencem a tabelas diferentes e nunca devem ser somadas ou descritas como “81 fontes”.

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
- metodologia, frequência ou citação universal quando essas propriedades pertencem aos produtos individuais;
- expansão conceitual automática para acomodar uma fonte nova.

Uma nova entidade ou relação só deve ser criada quando a estrutura atual for comprovadamente incapaz de representar uma diferença material necessária à descoberta, compreensão ou acesso.

## 4. Classes de mudança

Toda mudança deve ser classificada antes da execução.

### DATA
Aumenta ou corrige conteúdo do catálogo. Exemplos: nova fonte, novo produto, correção de URL, licença, cobertura, metodologia, citação, formato, acesso ou metadado. É a classe normal de desenvolvimento futuro.

### FIX
Corrige defeito observável sem ampliar o modelo conceitual. Exemplos: busca quebrada, link incorreto, problema mobile, acessibilidade, overflow, filtro, comparação ou download.

### RELEASE
Empacota um estado estável e auditado. Exemplos: versão, changelog, tag, GitHub Release, snapshot e Zenodo.

### INFRA
Altera infraestrutura ou contrato estrutural. Exemplos: analytics, mudança incompatível de schema, novo backend ou nova dependência externa. INFRA é excepcional.

## 5. Gates proporcionais ao risco

Qualidade deve vir de evidência, validação, testes e auditoria; aprovação humana é reservada para decisões em que julgamento humano agrega proteção real.

### AUTO-SAFE
Pode avançar até merge e verificação pós-merge sem interromper o usuário quando todos os controles objetivos passam.

Inclui, por padrão:

- documentação e status sem efeito conceitual;
- saneamento reversível do repositório depois de preservada a proveniência;
- melhorias de QA/CI sem relaxar gates;
- correções factuais de metadados dentro do contrato canônico, com evidência oficial explícita e sem ambiguidade;
- novas fontes/produtos estritamente dentro do contrato congelado, em lotes pequenos e com evidência oficial suficiente;
- correções técnicas de baixo risco e reversíveis com testes adequados.

AUTO-SAFE exige: evidência adequada → implementação → CI/testes → diff audit → verificação pública quando aplicável → merge → verificação pós-merge.

### REVIEW
Exige uma autorização humana única para o pacote completo quando houver risco material que não seja conceitual/destrutivo.

Inclui, por padrão:

- lotes grandes de dados;
- mudança pública significativa de interface ou comportamento;
- correção factual com evidência conflitante ou ambiguidade relevante;
- alteração operacional cuja consequência seja difícil de avaliar apenas por testes automáticos.

### HUMAN-DECISION
Sempre exige decisão humana explícita antes da mudança material.

Inclui:

- mudança do escopo ou modelo conceitual;
- mudança incompatível de schema/contrato;
- remoção destrutiva ou em massa;
- novo backend/infraestrutura estrutural;
- ativação de analytics/tracking ou decisão de privacidade;
- mudança de licença, autoria ou política oficial de citação;
- release `1.0.0`;
- publicação Zenodo/DOI.

Uma mudança que cruza categorias assume o nível de risco mais alto aplicável.

## 6. Pipeline obrigatório por pacote

1. **Scope** — problema, classe, arquivos afetados, fora de escopo e critério de conclusão.
2. **Evidence** — evidência oficial atual para afirmações factuais ou evidência reproduzível para defeitos técnicos.
3. **Implementation** — executar somente o delta necessário em branch criada do `main` atual.
4. **Automated validation** — validadores proporcionais ao delta.
5. **Diff audit** — confirmar arquivos alterados e ausência de efeitos incidentais.
6. **Rendered/public validation** — quando interface ou artefato público puder mudar.
7. **Risk classification** — `AUTO-SAFE`, `REVIEW` ou `HUMAN-DECISION`.
8. **Integration decision** — AUTO-SAFE integra quando todos os gates objetivos passam; REVIEW/HUMAN-DECISION aguardam autorização humana aplicável.
9. **Merge/deploy** — integrar por método governado e publicar quando aplicável.
10. **Post-merge verification** — comprovar que `main`, deploy e comportamento correspondem ao pacote validado.
11. **Consolidation** — somente então registrar o pacote como concluído.

Estados de progresso:

`PLANNED → EXECUTED → MATERIALIZED → VERIFIED → CONSOLIDATED`.

CI verde comprova estrutura/testes, **não verdade factual externa**.

## 7. Sequência de intervenções

### P0 — saneamento e autoridade

1. manter este modelo operacional e `WORKFLOW_STATUS.md` como direção ativa;
2. auditar e resolver a cadeia legada #57–#69;
3. classificar legado como `SALVAGE`, `HISTORICAL`, `SUPERSEDED` ou `REMOVE`;
4. recuperar seletivamente metadados científicos úteis sem importar arquitetura antiga;
5. limpar/arquivar material operacional obsoleto apenas depois da preservação da evidência útil;
6. reconstruir o roadmap de analytics sobre `main` atual antes de qualquer merge do PR #76 ou sucessor.

### P1 — contrato e baseline científico

7. congelar o contrato canônico de fonte/produto/distribuição;
8. auditar 51/51 fontes contra evidência oficial atual;
9. auditar 11/11 produtos e 19/19 distribuições;
10. corrigir somente o que estiver sustentado por evidência rastreável;
11. registrar lacunas sem inferência.

### P2 — expansão de volume

12. expandir produtos de alto valor materialmente distintos;
13. adicionar fontes relevantes ao Brasil em lotes coerentes;
14. usar batches pequenos, normalmente 5–10 entradas;
15. nunca transformar arquivos/bandas/endpoints em produtos sem justificativa material.

### P3 — qualidade operacional

16. fortalecer QA de dados, links e relações;
17. acrescentar acessibilidade automatizada e testes de teclado/foco;
18. ampliar cobertura de browser quando o benefício justificar custo;
19. tornar CI proporcional: data-only, frontend e release executam suites diferentes;
20. manter smoke externo após deploy.

### P4 — release

21. normalizar documentação ativa e versionamento;
22. concluir critérios para Vitrine Ciência 1.0.0;
23. criar tag/GitHub Release após baseline científico auditado e decisão humana;
24. gerar snapshot arquivável;
25. depositar release estável no Zenodo somente após decisão humana e verificar DOI/metadata.

### P5 — analytics

26. executar A0 apenas após baseline/release estável: política de privacidade e escolha de provedor;
27. A1: instrumentação mínima, reversível e não bloqueante;
28. A2: histórico durável apenas de agregados;
29. A3: visão interna;
30. A4: pequeno painel público agregado após histórico suficiente e nova auditoria de privacidade.

## 8. Regras de curadoria científica

Prioridade de evidência:

1. página oficial do produtor;
2. documentação/metadados oficiais;
3. API/catálogo oficial;
4. publicação científica primária quando necessária;
5. outras fontes apenas como apoio.

Regras:

- não inferir valor ausente;
- não preencher propriedade da plataforma com propriedade de um produto específico;
- distinguir `não encontrado`, `não aplicável`, `desconhecido` e `parcial` quando o schema permitir;
- preservar granularidade mínima suficiente;
- registrar data de verificação;
- revalidar links e atributos temporais que podem mudar;
- não copiar datasets de terceiros para o repositório;
- legado é pista de auditoria, nunca autoridade automática.

## 9. Critério para nova fonte

Uma fonte entra quando oferece informação científica ou infraestrutura de descoberta relevante; possui utilidade material para pesquisa, ensino ou extensão relacionados ao Brasil; tem identidade institucional rastreável; pode ser descrita sem inventar propriedades; e não duplica semanticamente uma entrada existente sem diferença útil.

## 10. Critério para novo produto

Um produto recebe linha própria quando possui identidade material independente, por exemplo diferença relevante em finalidade, metodologia, cobertura, resolução/suporte, coleção/versão científica ou condições/caminho de acesso.

Não criar produto apenas porque existe outro arquivo, tile, banda, formato ou endpoint.

## 11. Política de PRs e concorrência

- preferir **um pacote de implementação ativo por vez**;
- DATA batches só coexistem quando independentes e sem disputa de linhas/contratos;
- PRs legados congelados não contam como trabalho ativo;
- evitar cadeias longas de PRs empilhados;
- branch nova nasce do `main` atual;
- autorização humana, quando necessária, vale apenas para o pacote/head que foi efetivamente revisado;
- AUTO-SAFE não deve ser artificialmente bloqueado por autorização humana repetitiva;
- nunca usar CI verde como substituto de evidência factual externa.

## 12. QA proporcional

### DATA-only
- schema/estrutura;
- IDs únicos;
- relações fonte–produto–distribuição;
- enums;
- URLs e campos obrigatórios;
- geração determinística;
- diff audit;
- evidência oficial para valores factuais alterados.

### FIX/frontend
Além do anterior, quando aplicável:
- navegador real;
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
- citação/licenças/versão;
- artefato final;
- smoke externo;
- inspeção do snapshot.

## 13. Versionamento

Meta para `1.0.0`:

- repositório saneado;
- contrato canônico estável;
- 51 fontes atuais auditadas;
- 11 produtos e 19 distribuições auditados;
- documentação ativa consistente;
- QA e deploy verdes;
- citação/licenças verificadas;
- snapshot reproduzível;
- decisão humana explícita de release.

Depois de 1.0.0:

- `1.0.x`: correções compatíveis;
- `1.x.0`: crescimento de dados/produtos e melhorias compatíveis;
- `2.0.0`: mudança conceitual incompatível deliberada.

## 14. Recorrência e melhoria contínua

A tarefa recorrente deve:

- começar do último estado verificado;
- trabalhar em um pacote coerente por rodada;
- aplicar gates proporcionais ao risco;
- concluir AUTO-SAFE sem interrupção humana desnecessária;
- parar somente em REVIEW/HUMAN-DECISION reais, bloqueio externo ou ambiguidade científica relevante;
- revisar criticamente o próprio processo e remover gargalos que não aumentam qualidade;
- não criar arquitetura nova enquanto houver saneamento/auditoria prioritária;
- registrar somente progresso materializado e verificado.

## 15. Critério de sucesso de longo prazo

O fluxo normal deve convergir para:

**discover → verify → curate → validate → publish → monitor → periodically release**.

O projeto não deve voltar ao ciclo de redesenhar arquitetura continuamente. A maior parte do esforço futuro deve produzir mais conteúdo científico confiável, metadados melhores, correções observáveis e releases reproduzíveis.