# Direção científica — Vitrine Ciência

**Status:** vigente  
**Data:** 18 de agosto de 2026

## 1. Missão

A **Vitrine Ciência** facilita a descoberta, compreensão inicial e acesso a fontes e produtos de dados científicos relevantes ao Brasil. Seu valor original está na curadoria estruturada: identificar o que existe, quem mantém, o que representa, como pode ser acessado e quais limitações precisam ser conhecidas antes do uso.

A Vitrine é um catálogo de descoberta, não um repositório integral dos dados externos e não um motor universal de análise ou comparabilidade.

## 2. Unidade científica vigente

O modelo ativo possui três níveis:

```text
Fonte
  └── Produto
        └── Distribuição
```

- **Fonte:** plataforma, portal, programa, catálogo, repositório, rede ou infraestrutura que permite descobrir/acessar informação.
- **Produto:** oferta materialmente distinta por conteúdo, finalidade, método, cobertura, suporte, coleção/versão ou condição de acesso.
- **Distribuição:** rota concreta de acesso a um produto, como download, API, serviço geoespacial, catálogo ou aplicação.

O modelo não exige release, variável, ativo ou perfil espacial como entidades independentes. Informações desse tipo são registradas nos campos existentes quando sustentadas. Expansão de schema é excepcional.

## 3. Escopo territorial e temático

O Brasil é o escopo territorial prioritário. A Vitrine inclui fontes brasileiras e fontes internacionais que oferecem informação útil sobre o país. O catálogo pode cobrir, entre outros, biodiversidade, ecologia, clima, água, solos, uso da terra, sensoriamento remoto, saúde, educação, energia, agricultura, demografia, políticas públicas e infraestrutura científica.

A prioridade territorial não é nota de qualidade.

## 4. Princípios científicos permanentes

1. **Não inventar.** Ausência de evidência permanece desconhecida, variável ou não localizada.
2. **Preservar níveis.** Propriedade de produto não é automaticamente propriedade da fonte; formato/distribuição não define o significado científico do produto.
3. **Distinguir suporte de visualização.** Zoom, tile ou interface não comprovam resolução científica.
4. **Distinguir tempo.** Cobertura temporal, resolução temporal e frequência de atualização são propriedades diferentes.
5. **Distinguir observação e derivação.** Observado, administrativo, modelado, classificado, agregado e previsto não são equivalentes.
6. **Preservar proveniência.** O provedor e a documentação original permanecem referências primárias.
7. **Licença conservadora.** Registrar a licença no nível mais específico sustentado; não generalizar termos do portal a todos os datasets.
8. **Granularidade mínima suficiente.** Novo produto somente quando a distinção melhora materialmente descoberta, compreensão ou acesso.
9. **Rastreabilidade proporcional.** Evidência deve sustentar a afirmação específica; CI verde não é prova factual externa.
10. **Encerramento.** Curadoria suficiente e tecnicamente defensável pode ser publicada com limitações explícitas; não é necessário eliminar toda incerteza antes de avançar.

## 5. O que a Vitrine não representa

A inclusão de uma fonte/produto não significa:

- certificação de qualidade universal;
- endosso do provedor;
- garantia de disponibilidade futura;
- equivalência ou comparabilidade com outros produtos;
- autorização de uso além da licença/termos originais;
- completude do universo de dados existente sobre o Brasil.

## 6. Relação com o Simbiotrama

Arquitetura relacional, PostgreSQL/PostGIS, Instâncias 1–3 e composição territorial pertencem ao **Simbiotrama**, projeto separado desde 09/08/2026. Documentos antigos sobre essa arquitetura permanecem neste histórico apenas por proveniência e não definem a direção científica da Vitrine.

## 7. Critério de sucesso

A Vitrine é bem-sucedida quando permite responder, com baixo risco de interpretação enganosa:

- qual fonte oferece a informação;
- quais produtos materialmente distintos estão disponíveis;
- qual o alcance espacial e temporal relevante;
- qual a natureza do dado/produto;
- quais limitações condicionam o uso;
- como acessar os dados;
- quais evidências e datas sustentam o registro;
- qual versão ou coleção deve ser conferida no provedor original.

O crescimento do catálogo deve aumentar cobertura e utilidade sem sacrificar clareza semântica, rastreabilidade ou simplicidade operacional.
