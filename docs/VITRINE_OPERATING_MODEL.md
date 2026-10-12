# Vitrine Ciência — modelo operacional

**Status:** catálogo estático operacional; evolução WEB/API em planejamento controlado  
**Atualização:** 12 de outubro de 2026

## 1. Produto

A Vitrine Ciência é um catálogo científico curado de descoberta, interpretação e encaminhamento para dados relevantes aos socioecossistemas brasileiros.

O objetivo não é reproduzir integralmente os catálogos dos provedores. O valor agregado da Vitrine é:

- organizar recursos heterogêneos em uma linguagem comparável;
- orientar a descoberta por pergunta científica;
- distinguir recurso, produto, distribuição, serviço, visualização e documentação;
- registrar proveniência, acesso e limitações;
- encaminhar o usuário ao ponto de acesso correto;
- manter uma superfície pública resiliente mesmo quando provedores externos estão indisponíveis.

## 2. Estado operacional atual

O site público é um cliente estático publicado por GitHub Pages.

Estado canônico atual:

- 58 registros;
- 11 produtos detalhados;
- 19 distribuições;
- 58 páginas `/registros/dr####/`;
- JSON público agregado e por registro;
- build e validação em Python;
- frontend HTML/CSS/JavaScript;
- GitHub Actions para build, QA visual e smoke.

Runtime validado: `378e3d43c71988f3c7966e33f3d4f5cb879b1443`.

Não há backend obrigatório para servir o catálogo atual.

A fase corrente é de **QA/QC, manutenção e desenho do modelo público v2**. A expansão de novas fontes, produtos e distribuições está **pausada** como processo automático/em lote; adições pontuais exigem **instrução humana explícita** e curadoria documentada.

## 3. Arquitetura pública corrente

A descoberta prioriza:

**pergunta científica → fenômeno/processo → território → tipo de informação → registro relevante → dado/produto → acesso → proveniência**

A URL individual pertence ao Registro da Vitrine.

O contrato v1 ainda trata registro e recurso descrito de modo parcialmente fundido; isso será corrigido no modelo v2.

## 4. Arquitetura alvo

A camada conceitual alvo é:

```
CatalogRecord da Vitrine
        │ descreve
        ▼
Recurso catalogado
        ├── oferta científica
        │     └── versão/coleção
        │            └── distribuição / DataService
        ├── visualizadores
        ├── documentação
        └── agentes/proveniência
```

Essa estrutura deve ser suficientemente rica para representar MapBiomas, TerraBrasilis, GEE, GBIF, Carbon Mapper, Planet, bases estáticas e catálogos institucionais sem forçar todos à mesma ontologia.

## 5. Regra de granularidade

Uma nova entidade pública só deve ser criada quando a distinção altera materialmente descoberta, interpretação científica, versionamento, proveniência ou acesso.

Normalmente não criam nova entidade pública de alto nível:

- formato;
- arquivo;
- tile;
- banda;
- endpoint;
- viewer;
- página de documentação;
- cópia técnica da mesma distribuição.

Produtos, versões e distribuições podem existir como entidades internas sem receber página própria.

## 6. Cliente web

O cliente corrente é deliberadamente leve e estático.

Princípios:

- conteúdo primário pré-renderizado;
- JavaScript como melhoria progressiva;
- filtros controlados em vez de busca livre como entrada principal;
- páginas individuais permanentes;
- dependências locais verificadas no build;
- acessibilidade e responsividade validadas;
- nenhuma chamada a APIs externas necessária para renderizar uma ficha.

A próxima revisão do cliente deve remover redundância dos cards e fazer a página individual assumir integralmente o conteúdo aprofundado.

## 7. Federação

A federação é uma arquitetura futura de **metadados e acesso**, não uma obrigação de copiar os dados científicos.

Princípio:

**federado na origem; indexado localmente na descoberta; descentralizado no acesso.**

Pipeline alvo:

`provider → connector → raw/staging → normalization → deduplication → classification → access validation → curation gate → public snapshot`

O catálogo local deve continuar sendo a fonte consultada pelo usuário.

## 8. Static-first / stale-while-revalidate

A futura API não deve transformar cada page view em fan-out para dezenas de provedores.

Fluxo planejado:

1. servir snapshot atual;
2. avaliar freshness;
3. se vencido, agendar refresh;
4. aplicar TTL/cooldown/rate limit;
5. buscar no provedor;
6. armazenar resultado em staging;
7. normalizar e comparar;
8. promover somente após os gates aplicáveis.

Uma API externa lenta, quebrada ou autenticada não pode indisponibilizar o registro público.

## 9. Integration Registry

Antes de harvesting, cada integração deverá possuir um perfil explícito com:

- objeto científico atendido;
- provedor;
- endpoint/documentação;
- tecnologia;
- autenticação;
- licenciamento;
- escopo de redistribuição;
- paginação;
- limites;
- frequência;
- status operacional;
- IDs externos;
- semântica de versão;
- prioridade.

A existência de um endpoint não implica autorização para harvesting ou republicação.

## 10. Gates

### Gate WEB

Nenhuma alteração pública é aceita sem build e validação proporcional.

### Gate de modelo

O modelo v2 deve estar estável antes de tornar harvesting uma dependência arquitetural.

### Gate de integração

Nenhum conector entra sem Integration Registry.

### Gate de curadoria

Resultado bruto nunca é publicado diretamente.

### Gate de release

Releases científicas são decisões explícitas e não efeitos colaterais do runtime.

## 11. Protótipos históricos

A branch `agent/federated-explorer-mvp` é um experimento antigo de composição cartográfica WMS/WMTS.

Ela não é base para merge nem representa o estado da federação atual. Conceitos úteis podem ser reaproveitados por reimplementação.

## 12. Marco seguinte

O próximo marco é `VITRINE_PUBLIC_MODEL_V2`.

Depois dele, a execução passa para Integration Registry e pilotos de conectores.

Detalhamento: `docs/WEB_API_EVOLUTION_PLAN.md`.
