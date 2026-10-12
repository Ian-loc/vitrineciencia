# Vitrine Ciência — índice do espelho no Drive

**Verificado em:** 12 de outubro de 2026 (`America/Sao_Paulo`).
**Autoridade:** [GitHub, branch main](https://github.com/Ian-loc/vitrineciencia). Este Drive contém documentação derivada e snapshots históricos.
**Commit-fonte verificado:** `bb7c21b13585c94dc57e37efdc3af45eeabf6178` (PR #284). Este SHA identifica a comparação desta data; o estado vivo continua sendo o HEAD validado de main.

## Estado material verificado

- 58 registros, 11 produtos detalhados e 19 distribuições.
- 58 páginas individuais persistentes e JSONs v1/v2.
- Baseline `VITRINE_PUBLIC_MODEL_V2` concluído: registro separado do recurso, offerings, rotas canônicas, versões curadas e proveniência conservadora.
- Impressão preserva acessos, URLs, documentação e referências.
- QA/QC e manutenção ativos; expansão automática/em lote pausada.
- Integration Registry é a próxima frente; API pública, conectores e harvesting automático ainda não estão implementados.
- Acesso principal no catálogo completo: A=2, B=39, C=0, D=14, E=3.
- Release histórica v1.0.0 e DOI `10.5281/zenodo.22130831` preservados.

## Instituições vinculadas ao projeto

UFLA, Programa de Pós-Graduação em Ecologia Aplicada da UFLA e FAPEMIG. Os logos estão nas páginas públicas, no README e no documento `Instituições vinculadas à Vitrine Ciência`, em `00_governanca`.

## Organização e arquivos vigentes

| Local | Arquivos e interpretação |
|---|---|
| `00_governanca` | `estado_projeto_2026-10-12.md` e `workflow_status_2026-10-12.md`: cópias dos documentos canônicos. Carta/plano de agosto identificados como históricos. |
| `01_dados` | Planilha de 08/10 e os três CSVs `data_resources.csv`, `data_products.csv`, `product_distributions.csv`: derivados 58/11/19. CSVs antigos `fontes.csv`, `produtos.csv`, `distribuicoes.csv`, prioridades e XLSX candidato: históricos 135/843/876. |
| `02_publicacao` | Pacote candidato antigo: histórico. Não é o catálogo vivo nem um novo depósito científico. |
| `03_qualidade` | `auditoria_drive_2026-10-12.md` e `.json`: comparação corrente. Estado Static 51 de setembro e validações de agosto: históricos. |
| `90_historico` | Legado e separação dos projetos: históricos. |

## Planilha de outubro

[Vitrine Ciência — espelho canônico 58-11-19 — 2026-10-08](https://docs.google.com/spreadsheets/d/1NHgAg-zumOrAwFt8e1tbAN_1Q9yPmtBaNhE74loUTHA/edit)

As três abas foram comparadas integralmente contra o commit-fonte acima: cabeçalhos, IDs, contagens e todos os valores coincidem. A planilha permanece como snapshot de 08/10, commit `ae1d662b612127b0682827ee0813ed30422226d9`; sua data não foi artificialmente alterada.

A igualdade das tabelas físicas não faz da planilha um espelho completo do modelo v2. Rotas, versões e proveniência estruturadas têm autoridades adicionais no GitHub: `data/access_routes.json`, `data/offering_versions.json` e `data/provenance_statements.json`.

## Documentação canônica para retomar o trabalho

- [Estado do projeto](https://github.com/Ian-loc/vitrineciencia/blob/main/docs/PROJECT_STATE.md).
- [Workflow e próximos passos](https://github.com/Ian-loc/vitrineciencia/blob/main/WORKFLOW_STATUS.md).
- [Contrato de espelhamento](https://github.com/Ian-loc/vitrineciencia/blob/main/DRIVE_MIRROR_CONTRACT.md).
- [Plano WEB/API](https://github.com/Ian-loc/vitrineciencia/blob/main/docs/WEB_API_EVOLUTION_PLAN.md).

O próximo passo de implementação é o Integration Registry, sem iniciar harvesting automático. Correções de curadoria permanecem incrementais e sustentadas por evidência.

## Controles verificados do commit-fonte

- Build/validação/deploy: [38294913997](https://github.com/Ian-loc/vitrineciencia/actions/runs/38294913997) — success.
- QA visual/responsivo: [38294913959](https://github.com/Ian-loc/vitrineciencia/actions/runs/38294913959) — success.
- Smoke pós-deploy: [38294967916](https://github.com/Ian-loc/vitrineciencia/actions/runs/38294967916) — success.

## Manutenção

Atualizar primeiro o GitHub; depois validar e regenerar os derivados. Preservar releases e evidências históricas. Não confundir o núcleo histórico 51, o snapshot expandido 135/843/876 ou um checkpoint de setembro com o catálogo vivo 58/11/19.
