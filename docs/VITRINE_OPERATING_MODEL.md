# Vitrine Ciência — modelo operacional e pipeline de manutenção

Status: **ACTIVE OPERATING MODEL**  
Atualização: **2026-08-20**

## 1. Produto

A Vitrine Ciência é um catálogo delimitado para descoberta de dados científicos relevantes ao Brasil. Seu modelo conceitual estável é:

`fonte → produto → distribuição`

A Vitrine ajuda a descobrir, compreender inicialmente, comparar metadados e acessar recursos externos. Não reconstrói integralmente a arquitetura de cada provedor e não hospeda, por padrão, os datasets catalogados.

## 2. Autoridade e estado

- repositório: `Ian-loc/vitrineciencia`;
- branch: `main`;
- site: `https://ian-loc.github.io/vitrineciencia/`;
- fontes: `data/data_resources.csv`;
- produtos: `data/data_products.csv`;
- distribuições: `data/product_distributions.csv`;
- código: MIT;
- curadoria/metadados originais: CC BY 4.0.

Contagens e maiores IDs são estado operacional e não devem ser duplicados neste documento. O snapshot corrente é mantido em `docs/PROJECT_STATE.md` e `data/data_quality_report.json`. Lacunas de IDs são preservadas e IDs não são reciclados.

## 3. Fronteira conceitual

### Inclui

- identidade de fontes e produtos;
- cobertura espacial e temporal quando sustentada;
- suporte/resolução e atualização quando sustentados;
- acesso, formatos, autenticação, licença e metodologia quando aplicáveis;
- limitações e evidências;
- busca, filtros, comparação, análise descritiva do catálogo e downloads dos próprios metadados;
- links para os provedores originais.

### Não exige

- PostgreSQL/PostGIS;
- runtime do Simbiotrama;
- enumeração de cada arquivo, banda, tile ou endpoint como entidade;
- cópia de datasets externos;
- inferência de valores não documentados;
- comparabilidade científica universal entre produtos.

## 4. Classes de mudança

- **DATA:** correção de fonte, produto, distribuição ou classificação territorial. Durante a fase atual, expansão de novas entidades está pausada.
- **FIX:** defeito de interface, build, acesso, navegação ou regressão.
- **DOC:** documentação, estado e explicitação de contratos sem mudança conceitual.
- **RELEASE:** congelamento de snapshot, versão, tag, pacote e depósito.
- **INFRA:** mudança estrutural de schema/runtime/dependência; excepcional.

## 5. Gates proporcionais

- **AUTO-SAFE:** DOC, QA/CI, correções pequenas inequívocas e saneamentos reversíveis dentro do contrato.
- **REVIEW:** lote grande, mudança pública relevante ou ambiguidade factual material.
- **HUMAN-DECISION:** retomada de expansão de escopo, schema incompatível, destruição, tracking/privacidade, licença/autoria/citação oficial, `1.0.0` e DOI.

## 6. Pipeline obrigatório por pacote

1. **Scope:** problema e critério de conclusão.
2. **Evidence:** evidência oficial/primária proporcional às afirmações.
3. **Implementation:** delta mínimo em branch derivada de `main`.
4. **Validation:** validadores do contrato e testes pertinentes.
5. **Diff audit:** ausência de efeitos incidentais.
6. **Public validation:** quando interface/artefato público puder mudar.
7. **Integration:** conforme classe de risco.
8. **Post-merge verification:** `main`, deploy e comportamento observável.
9. **Consolidation:** registrar somente trabalho materializado e verificado.

Estados: `PLANNED → EXECUTED → VERIFIED → CONSOLIDATED`.

## 7. Curadoria científica

Prioridade de evidência:

1. página oficial do produtor;
2. documentação/metadados oficiais;
3. API/catálogo oficial;
4. publicação científica primária quando necessária;
5. documentação técnica institucional;
6. fontes secundárias apenas como apoio.

Regras:

- não inferir valor ausente;
- diferenciar fonte, produto e distribuição;
- preservar a fonte/provedor primário;
- separar resolução, suporte e escala;
- separar cobertura temporal, resolução temporal e atualização;
- registrar natureza observada/modelada/classificada/administrativa quando relevante;
- tratar licença no nível mais específico sustentado;
- revalidar atributos temporariamente instáveis;
- nunca usar CI verde como prova factual externa.

## 8. Entrada e granularidade

A expansão de novas fontes, produtos e distribuições está **pausada** durante a fase atual de QA/QC. As regras de granularidade abaixo continuam válidas para correções do catálogo existente e para eventual retomada mediante instrução humana explícita.

### Nova fonte

Quando a expansão for retomada, deve ter identidade institucional rastreável, utilidade científica/operacional relevante ao Brasil, evidência suficiente e não duplicar semanticamente uma fonte existente sem benefício de descoberta.

### Novo produto

Quando a expansão for retomada, recebe linha própria somente quando há diferença material em finalidade, conteúdo, método, cobertura, suporte/resolução, coleção/versão ou acesso. Arquivo, formato, banda, tile ou endpoint isolado não bastam.

### Distribuição

Representa a rota concreta de acesso e pode registrar formato, protocolo, ferramenta, gratuidade, autenticação, licença e suporte a recorte.

## 9. Qualidade

O relatório `data/data_quality_report.json` é diagnóstico de preenchimento, não certificação. Seus valores são voláteis e devem ser lidos diretamente do artefato regenerado, não replicados manualmente aqui. A prioridade atual é corrigir defeitos e riscos com maior impacto científico, operacional ou de publicação, sem perseguir completude artificial.

## 10. Drive

O Drive é derivado/histórico. Regeneração de espelho é útil, mas não é gate obrigatório para uma release válida. Um espelho deve declarar commit-fonte, data e contagens e passar comparação antes de ser chamado de sincronizado.

## 11. Release

O projeto permanece `unreleased`. Uma release científica deve congelar um snapshot reproduzível, atualizar citação/changelog, criar tag e GitHub Release e, quando decidido, depositar como Dataset no Zenodo. O DOI não depende de atingir uma contagem arbitrária de registros.

## 12. Relação com o Simbiotrama

Materiais de Instância 1, PostgreSQL/PostGIS e roadmaps Simbiotrama presentes no histórico são `HISTORICAL_EVIDENCE`. O Simbiotrama é um projeto independente e não define o pipeline ativo da Vitrine.

## 13. Critério de sucesso

Na fase atual, o fluxo normal deve convergir para:

**inspect → verify → fix → validate → publish → monitor**.

Quando a expansão for explicitamente retomada, a descoberta/curadoria de novas entidades volta a integrar esse ciclo. Qualidade, governança e auditoria são meios para um catálogo útil e não justificam alterações cosméticas ou escopo novo durante a fase de QA/QC.