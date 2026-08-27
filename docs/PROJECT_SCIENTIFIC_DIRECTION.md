# Direção científica — Vitrine Ciência

**Status:** vigente  
**Atualização:** 27 de agosto de 2026  
**Fase operacional atual:** QA/QC, manutenção e refinamento da descoberta pública. O estado vivo deve ser consultado em `docs/PROJECT_STATE.md` e `WORKFLOW_STATUS.md`.

## 1. Missão

A **Vitrine Ciência** facilita a identificação, seleção, comparação e acesso a produtos de dados científicos relevantes ao Brasil. Seu valor está na curadoria estruturada: mostrar o que existe, onde e quando se aplica, em qual escala, como pode ser acessado, quem mantém e quais limitações precisam ser conhecidas antes do uso.

A Vitrine é um catálogo de descoberta e triagem, não um repositório integral dos dados externos e não um motor universal de análise ou comparabilidade.

## 2. Unidade científica e ordem de descoberta

O modelo ativo permanece:

```text
Fonte
  └── Produto
        └── Distribuição
```

- **Fonte:** plataforma, portal, programa, catálogo, repositório, rede ou infraestrutura responsável ou intermediária; é contexto de proveniência e responsabilidade institucional.
- **Produto:** oferta materialmente distinta por conteúdo, finalidade, método, cobertura, suporte, coleção/versão ou condição de acesso; é a **unidade principal de descoberta pública**.
- **Distribuição:** rota concreta de acesso a um produto, como download, API, serviço geoespacial, catálogo ou aplicação.

A interface pública adota a ordem **pergunta científica → produto → comparação → proveniência/fonte → distribuição/acesso**. Essa decisão não altera nem colapsa o modelo Fonte → Produto → Distribuição.

## 3. Critérios de descoberta científica

Para selecionar produtos, a interface deve priorizar dimensões que afetam diretamente a adequação à pergunta:

1. tema / variável;
2. cobertura geográfica;
3. período;
4. resolução temporal;
5. escala / suporte espacial;
6. resolução espacial;
7. forma de acesso;
8. formato;
9. licença e gratuidade.

Fonte/provedor, tipo de produto, autenticação, estado e origem permanecem filtros complementares. A busca pode interpretar deterministicamente termos e sinônimos científicos, biomas, Brasil, anos e resoluções, sem substituir os filtros explícitos nem inferir propriedades ausentes.

O ranking padrão deve seguir **relevância da consulta → disponibilidade de dados para o Brasil → completude/documentação → origem da fonte → nome**. Origem brasileira é um sinal secundário; não substitui adequação científica do produto.

## 4. Triagem pública

O card canônico é o **card de produto**. Ele deve permitir que o usuário responda rapidamente:

- **Onde?** — cobertura geográfica;
- **Quando?** — cobertura temporal;
- **Escala?** — suporte/resolução espacial e resolução temporal;
- **Acesso?** — formato, protocolo/ferramenta e gratuidade quando conhecida.

Metodologia, limitações, licença, versão, proveniência e formas detalhadas de acesso permanecem disponíveis para escrutínio no detalhe expandido. A comparação lado a lado deve refletir exatamente a seleção ativa, permitir remoção durante a comparação e zerar seu estado ao ser fechada.

## 5. Escopo territorial e temático

O Brasil é o escopo territorial prioritário. A Vitrine inclui produtos de fontes brasileiras e fontes internacionais que oferecem informação útil sobre o país. A prioridade territorial não é nota de qualidade.

A regra operacional vigente é explícita: expansão de novas fontes, produtos e distribuições está **pausada** durante a fase corrente de QA/QC e refinamento. Sua retomada exige **instrução humana explícita** e curadoria factual compatível com os mesmos gates científicos aplicados ao catálogo canônico. Melhorias de busca, filtros, cards, ranking ou navegação não autorizam criação automática de registros.

## 6. Princípios científicos permanentes

1. **Não inventar.** Ausência de evidência permanece desconhecida, variável ou não localizada.
2. **Preservar níveis.** Propriedade de produto não é automaticamente propriedade da fonte; distribuição não define o significado científico do produto.
3. **Distinguir suporte de visualização.** Zoom, tile ou interface não comprovam resolução científica.
4. **Distinguir tempo.** Cobertura temporal, resolução temporal e frequência de atualização são propriedades diferentes.
5. **Distinguir observação e derivação.** Observado, administrativo, modelado, classificado, agregado e previsto não são equivalentes.
6. **Preservar proveniência.** O provedor e a documentação original permanecem referências primárias.
7. **Licença conservadora.** Registrar a licença no nível mais específico sustentado; não generalizar termos do portal.
8. **Granularidade mínima suficiente.** Novo produto somente quando a distinção melhora materialmente descoberta, compreensão ou acesso.
9. **Rastreabilidade proporcional.** Evidência deve sustentar a afirmação específica; CI verde não é prova factual externa.
10. **Encerramento.** Curadoria suficiente e tecnicamente defensável pode ser publicada com limitações explícitas.

## 7. Critério de sucesso

A Vitrine é bem-sucedida quando um estudante, pesquisador, docente ou profissional consegue, com baixo risco de interpretação enganosa:

- formular uma busca em termos próximos de sua pergunta;
- identificar rapidamente produtos candidatos;
- restringir por geografia, período, escala e acesso;
- comparar alternativas e seus trade-offs;
- reconhecer limitações e lacunas de metadados;
- identificar a fonte/provedor e a documentação original;
- acessar o produto pela distribuição adequada;
- registrar a versão/coleção efetivamente utilizada.

Contagens correntes e estado operacional não são replicados aqui; permanecem centralizados em `docs/PROJECT_STATE.md` e `WORKFLOW_STATUS.md` para evitar drift documental.
