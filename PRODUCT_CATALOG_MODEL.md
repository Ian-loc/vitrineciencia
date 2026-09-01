# Modelo do catálogo — Vitrine Ciência

**Status:** MODELO LEGADO / SOB AUDITORIA ONTOLÓGICA  
**Atualização:** 2026-09-01

## Estado

A estrutura histórica:

```text
Fonte (DR####)
  └── Produto (DP######)
        └── Distribuição (DD######)
```

permanece necessária para reproduzir `v1.0.0`, preservar IDs e operar o branch candidato do PR #267. Ela **não é mais declarada como arquitetura canônica final**.

`DR####` deve ser tratado como identificador legado até que a auditoria 51/51 determine o tipo real de cada entidade.

## Problema em correção

O nível `Fonte` reuniu objetos conceitualmente diferentes: instituição/provedor, programa, plataforma, catálogo, infraestrutura, dataset/coleção, serviço e portal. Isso impede assumir uma relação única `Fonte → Produto` para todos os casos.

## Regras que permanecem válidas

- IDs legados são preservados e não reciclados;
- arquivo, banda, tile, formato ou endpoint técnico não criam automaticamente um novo dataset;
- API/serviço não é dataset por padrão;
- distribuição representa uma forma concreta de acesso a dados quando isso é comprovado;
- visualizador, PDF ou documentação não devem ser tratados como acesso a dados sem qualificação explícita;
- propriedades específicas não devem ser generalizadas para entidade mais ampla;
- desconhecido permanece desconhecido.

## Modelo em avaliação

A auditoria deve testar a necessidade e as relações entre:

- Provider/Institution;
- Program/Initiative;
- Platform;
- Catalog/Repository;
- Data Infrastructure;
- Dataset/Collection;
- Distribution;
- DataService;
- Portal/Viewer.

O novo modelo só será chamado de canônico depois de G0–G4 PASS, com crosswalk dos 51 registros e validadores.

Estado corrente: `docs/PROJECT_STATE.md`. Workflow e Definition of Done: `WORKFLOW_STATUS.md`.
