# Metodologia de curadoria — Vitrine Ciência

**Status:** TRANSITÓRIA / ONTOLOGIA EM REVISÃO  
**Atualização:** 2026-09-01

## Escopo

A Vitrine Ciência é uma camada de descoberta e acesso a dados científicos relevantes ao Brasil. A fase atual não busca ampliar o catálogo: busca determinar corretamente o que representam os 51 registros legados `DR0001–DR0051` e preparar um modelo canônico simples e verificável.

A estrutura histórica `Fonte → Produto → Distribuição` permanece como referência de armazenamento e rastreabilidade, não como ontologia final.

## Método atual

Para cada DR:

1. confirmar a identidade oficial;
2. identificar o responsável/provedor;
3. determinar o tipo real da entidade;
4. separar plataforma, catálogo, infraestrutura, dataset/coleção, serviço e portal quando aplicável;
5. identificar datasets/famílias efetivamente disponibilizados;
6. identificar formas reais de acesso;
7. registrar evidência oficial e confiança;
8. registrar ambiguidade sem completar por inferência;
9. propor ação de migração preservando o ID legado.

## Evidência

Prioridade:

1. página/documentação oficial da entidade ou instituição responsável;
2. documentação técnica oficial, API/schema/catálogo oficial;
3. auditorias já verificadas no repositório;
4. literatura ou fontes secundárias apenas como apoio.

Cada evidência sustenta somente a afirmação que contém.

## Regras científicas

- dado ≠ serviço ≠ visualização ≠ documentação;
- API não é dataset por padrão;
- homepage não comprova licença ou acesso aos dados;
- HTTP 200 não comprova disponibilidade de dados utilizáveis;
- zoom/interface não comprova resolução científica;
- propriedades específicas não são generalizadas para entidade mais ampla;
- desconhecido permanece desconhecido;
- proveniência do provedor original é preservada;
- volume de registros não substitui relevância ou utilidade.

## Descoberta pública

A hierarquia desejada é:

**fenômeno/processo → território → tempo/escala → dado utilizável → acesso → provedor/proveniência**.

Busca livre não é mecanismo primário. Filtros controlados e termos científicos consistentes têm prioridade.

## Federação

Federação por APIs/serviços ocorre somente após a auditoria 51/51 e o Integration Registry. O primeiro piloto é MapBiomas Alerta; nenhum recurso descoberto por API entra automaticamente no catálogo público.

## QA

Toda alteração material deve ter evidência, validação, diff audit e read-back. CI verde comprova integridade do repositório, não verdade factual externa.

Estado: `docs/PROJECT_STATE.md`. Workflow e critério de término: `WORKFLOW_STATUS.md`.
