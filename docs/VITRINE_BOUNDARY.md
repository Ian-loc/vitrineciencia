# Vitrine Ciência — fronteira operacional

Decisão de separação: **2026-08-09**  
Revisão atual: **2026-09-01**

## Status

`Ian-loc/vitrineciencia` é a autoridade da Vitrine Ciência. O Simbiotrama é projeto independente e não pode ser dependência de runtime, CI ou publicação.

A auditoria ontológica atual não altera esta fronteira: o schema físico legado pode continuar servindo o frontend enquanto o novo modelo é definido. Quarentena, crosswalk, auditorias e infraestrutura de integração permanecem internos até promoção explícita.

## Contrato do artefato público

O GitHub Pages publica somente a superfície necessária ao produto, incluindo:

- páginas HTML públicas vigentes;
- CSS/JavaScript necessários;
- JSONs/metadados estritamente necessários à interface;
- classificação territorial e metadados públicos aplicáveis;
- licenças e informações de citação necessárias.

O builder é `scripts/build_site_artifact.py`.

## Material proibido no artefato público

- documentação operacional e auditorias internas;
- scripts, workflows e configurações de desenvolvimento;
- matrizes/crosswalks curatoriais internos não destinados ao usuário;
- quarentena;
- segredos, tokens, logs ou credenciais;
- material do Simbiotrama/Simbioscópio;
- legados sem função pública necessária.

## CI

A CI deve validar, conforme aplicável:

1. integridade dos dados físicos vigentes;
2. geração determinística dos derivados;
3. integridade HTML/CSS/JavaScript;
4. filtros/navegação/comparação;
5. construção isolada de `_site`;
6. ausência de material proibido;
7. deploy quando em `main`;
8. smoke externo pós-deploy.

PostgreSQL/PostGIS e jobs do Simbiotrama permanecem proibidos no grafo de deploy.

## Estado e ontologia

Contagens e tipos de entidade são estado, não contrato da fronteira. Consultar `docs/PROJECT_STATE.md` e `WORKFLOW_STATUS.md`.

`DR → DP → DD` pode persistir como estrutura física transitória sem ser tratado como ontologia final. Uma futura implementação federada deve preservar a mesma regra de fronteira: a Vitrine publica metadados aprovados e rotas de acesso; dados externos permanecem, em regra, nos provedores.

## Teste de regressão

A fronteira permanece válida enquanto:

1. Vitrine CI funciona sem Simbiotrama;
2. `_site` contém apenas o produto público;
3. quarentena/auditoria/credenciais não aparecem no site;
4. site e rotas públicas permanecem funcionais;
5. URL canônica permanece `https://ian-loc.github.io/vitrineciencia/`;
6. falha de outro projeto não altera a Vitrine;
7. nenhuma documentação interna é apresentada como dado científico público.

O marco original permanece em `docs/STRUCTURAL_SEPARATION_MILESTONE_2026-08-09.md`.
