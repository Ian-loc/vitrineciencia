# Vitrine Ciência — auditoria cruzada das correções 51/51

Data: 2026-08-10 (`America/Sao_Paulo`)  
Base: `main@097f58a81e3de17e60c977688b0b344942d8683e`

## Objetivo

Transformar as oito filas científicas produzidas pela auditoria `DR0001–DR0051` em uma **proposta única, determinística e verificável** antes de qualquer modificação do CSV canônico.

Este pacote não altera `data/data_resources.csv`.

## Baseline auditado

- fontes: **51/51** com audit trail atual baseado em fontes oficiais;
- produtos: 11 — auditoria específica ainda pendente;
- distribuições: 19 — auditoria específica ainda pendente;
- schema de fontes: 34 campos, congelado;
- IDs: `DR0001`–`DR0051`, sem adição/remoção;
- filas de correção: 8.

## Delta factual agregado esperado

As filas contêm:

- **119 correções**;
- **43 fontes** com ao menos uma correção;
- **8 fontes sem correção factual imediata**: `DR0001`, `DR0004`, `DR0007`, `DR0009`, `DR0014`, `DR0029`, `DR0035`, `DR0039`.

Como todas as 51 linhas foram efetivamente reavaliadas em 2026-08-10, a aplicação final também deve definir `last_verified=2026-08-10` para as 51 fontes. O número real de mudanças de data é calculado pelo validador contra o CSV atual; não é presumido.

## Normalizações de integração

Duas correções de fila precisam de normalização antes da escrita canônica:

1. `DR0019|data_formats`
   - usar `Shapefile`, não a abreviação `SHP`, mantendo vocabulário consistente;
   - candidato final: `GeoTIFF | CSV | Shapefile | GeoJSON | KML | KMZ | TFRecord; varia conforme a exportação`.

2. `DR0051|data_formats`
   - candidato final no campo: `não se aplica`;
   - a explicação sobre ausência de formato público da base integral permanece em `limitations`, onde pertence semanticamente.

As normalizações ficam em `config/source_correction_overrides_2026-08-10.json` e só são aceitas se houver correção correspondente na fila.

## Validador determinístico

`scripts/validate_source_correction_queues.py`:

1. lê o CSV canônico sem modificá-lo;
2. exige 51 fontes, 34 colunas e ordem exata `DR0001→DR0051`;
3. descobre exatamente as 8 filas;
4. aceita o formato histórico `status=READY` da primeira fila e `decision` das posteriores;
5. ignora apenas linhas explicitamente `no_change`;
6. rejeita duplicação de `(resource_id, field)`;
7. exige que cada campo exista no contrato;
8. proíbe alteração de `resource_id` e `last_verified` via fila factual;
9. exige correspondência **exata** entre `current_value` da fila e valor atual no CSV;
10. exige `evidence_url` HTTPS;
11. exige candidato não vazio e diferente do valor atual;
12. verifica exatamente 119 correções / 43 fontes corrigidas / complemento de 8 fontes sem correção;
13. aplica somente os overrides explícitos acima;
14. atualiza `last_verified` apenas na proposta em memória/cópia;
15. preserva IDs, ordem, número de linhas e schema;
16. nunca permite `--output` apontar para o próprio CSV canônico.

## Validação da proposta completa

O workflow read-only `.github/workflows/validate-source-corrections.yml`:

- tem apenas `contents: read`;
- gera `/tmp/data_resources.corrected.csv` e um summary JSON;
- cria uma cópia temporária do repositório;
- substitui o CSV **somente nessa cópia**;
- executa os validadores existentes da Vitrine, geração do catálogo e build do site;
- prova que fontes/IDs/ordem/schema permanecem 51/DR0001–DR0051/34;
- prova que `data_products.csv` e `product_distributions.csv` não mudam;
- guarda proposta + sumário como artifact por 14 dias;
- não possui permissão para push/commit/deploy.

## Política de risco

### Este pacote de QA

**AUTO-SAFE.** Apenas scripts/config/workflow read-only/documentação; não altera dados públicos.

### Aplicação futura ao CSV canônico

**REVIEW.** Embora cada correção seja individualmente inequívoca, o delta agregado é grande. A aplicação canônica terá uma única autorização humana depois de:

1. este validador passar;
2. a proposta temporária passar por todo o build/QA;
3. o total real de mudanças ser conhecido;
4. o diff proposto estar disponível para revisão;
5. nenhuma alteração de ID/schema/linhas/produtos/distribuições ser detectada.

Não haverá uma autorização por fonte nem por commit.

## Critério de conclusão

Este cross-audit só é consolidado quando o CI prova que as filas atuais geram uma proposta estruturalmente válida e reproduzível sem tocar no catálogo canônico.
