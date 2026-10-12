# Versões e proveniência no modelo público v2

**Status:** contrato conservador ativo  
**Autoridades:** `data/offering_versions.json` e `data/provenance_statements.json`  
**Schemas:** `schema/offering-versions-v1.json` e `schema/provenance-v1.json`  
**Data:** 12 de outubro de 2026

## 1. Motivo da revisão

O primeiro crosswalk do `public-record-v2` preservava todo campo legado `version_or_collection` e, adicionalmente, criava um objeto `versions[]` para qualquer texto não vazio.

Esse comportamento era seguro como mecanismo de migração, mas semanticamente amplo demais. O campo legado contém conteúdos de naturezas diferentes, por exemplo:

- versão identificável;
- ano/edição;
- “coleção corrente”;
- condição experimental;
- descrição de acesso;
- estado operacional.

Portanto, texto em `version_or_collection` não é prova suficiente de uma entidade de versão.

Situação análoga ocorria com `owner_or_manager`: expressões como “MCTI / INPE / RNP” ou “Carbon Mapper, Inc.; produtos de diferentes provedores e sensores” não representam um único agente. Separar esses textos automaticamente criaria entidades e papéis sem evidência.

## 2. Regra para versões

O read model agora distingue:

### Resumo legado

`offering.version_or_collection_summary`

Preserva literalmente a informação histórica útil para a interface.

### Versão promovida

`versions[]`

Só existe quando a informação foi explicitamente promovida por curadoria em `data/offering_versions.json`.

O baseline atual promove **Dynamic World V1** porque o próprio registro de produto contém simultaneamente o rótulo `V1` e o identificador `GOOGLE/DYNAMICWORLD/V1`.

Os demais resumos legados permanecem em `unresolved_legacy_summaries` até revisão específica.

Isso não significa que eles “não sejam versões”. Significa apenas que a Vitrine não os transforma em entidades estruturadas sem evidência suficiente sobre sua semântica.

## 3. Regra para proveniência

A camada `data/provenance_statements.json` preserva uma declaração de responsabilidade para cada registro.

Exemplo conceitual:

```
responsibility_statement:
  "MCTI / INPE / RNP"

agent_resolution_status:
  "unresolved_legacy_statement"
```

A declaração pode conter uma ou várias instituições, redes, parceiros, provedores ou relações.

Ela **não é um Agent**.

## 4. Agents

`agents[]` passa a ser reservado a entidades individualizadas cuja identidade e papel foram efetivamente curados.

Papéis futuros admissíveis incluem, conforme evidência:

- produtor;
- mantenedor;
- publicador;
- host;
- distribuidor;
- responsabilidade metodológica;
- outro papel explicitamente curado.

Enquanto a cadeia de responsabilidade não estiver resolvida, `agents[]` permanece vazio.

Essa ausência é intencional e mais precisa do que criar um agente composto fictício.

## 5. Estado institucional

`institutional_status_summary` continua disponível como resumo no nível do recurso.

Ele não determina automaticamente o papel do agente.

Por exemplo, “público”, “consórcio” ou “empresa privada” descrevem a natureza institucional geral, não se a entidade é produtora, mantenedora ou hospedeira.

## 6. Autoridade

Versões promovidas:

`data/offering_versions.json`

Declarações de proveniência:

`data/provenance_statements.json`

O read model declara:

- `curation.version_authority`;
- `curation.provenance_authority`.

## 7. Validação

`scripts/validate_version_provenance.py` garante:

- version IDs únicos;
- offering alvo existente;
- cobertura integral dos textos legados por versão promovida ou resumo não promovido;
- nenhuma offering simultaneamente resolvida e não resolvida;
- preservação literal do resumo de origem;
- uma declaração de proveniência por DR;
- preservação de `owner_or_manager` durante a migração;
- preservação do resumo institucional;
- ausência de parsing automático obrigatório.

`scripts/validate_public_records_v2.py` confirma ainda que o read model publicado consome exatamente essas autoridades.

## 8. Consequência na interface

Não há perda de conteúdo visível:

- o resumo “Versão/coleção” continua aparecendo nas offerings;
- o responsável continua aparecendo na página e nos cards;
- a diferença é interna e semântica: a Vitrine deixa de afirmar que todo resumo é uma Version ou que toda cadeia de responsáveis é um único Agent.

## 9. Próxima curadoria

A próxima etapa não é dividir automaticamente todas as cadeias institucionais.

A resolução deve começar pelos casos em que os papéis fazem diferença material para interpretação ou atualização, por exemplo:

- produtor científico ≠ plataforma de hospedagem;
- produtor ≠ distribuidor;
- iniciativa ≠ provedor do dataset;
- serviço comercial ≠ parceiro científico.

Da mesma forma, versões devem ser promovidas quando forem necessárias para citação, comparabilidade ou reprodutibilidade.
