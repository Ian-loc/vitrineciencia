# Estado do workflow — Vitrine Ciência

Atualização: 2026-08-10 (`America/Sao_Paulo`)

## Direção ativa

**Vitrine Ciência is a bounded scientific-data discovery catalog. Its conceptual product model is stable. Future development prioritizes data-volume growth, metadata correction, usability, maintenance and release management.**

Documentos centrais:
- `docs/VITRINE_OPERATING_MODEL.md`;
- `docs/VITRINE_CANONICAL_DATA_CONTRACT.md`;
- `docs/legacy/VITRINE_LEGACY_RECONCILIATION_2026-08-10.md`.

## Autoridade

- repositório: `Ian-loc/vitrineciencia`;
- branch: `main`;
- baseline consolidado atual: `9e83ffa3fa5fa6e74865f8f2986c30c7966ec239` (PR #79);
- site: `https://ian-loc.github.io/vitrineciencia/`;
- dados: 51 fontes, 11 produtos, 19 distribuições.

## Gates

- **AUTO-SAFE:** documentação/status, saneamento reversível, QA/CI, pequenas correções factuais inequívocas com evidência oficial e pequenas inclusões DATA dentro do contrato.
- **REVIEW:** lote grande, mudança pública relevante ou ambiguidade factual material.
- **HUMAN-DECISION:** escopo/schema incompatível, mudança destrutiva/em massa, nova infraestrutura, analytics/privacy, licença/autoria/citação oficial, `1.0.0`, Zenodo/DOI.

Pipeline:
`scope → evidence → implementation → validation → diff audit → public validation when relevant → risk classification → integration → post-merge verification → consolidation`

## Estado consolidado

### Interface
PRs #72–#75 e #77 consolidados e verificados.

### Governança
- PR #78: modelo operacional delimitado;
- PR #79: reconciliação legada + gates proporcionais;
- #58 e #59: fechados como `superseded`, sem merge e sem apagar histórico;
- #57 e #60–#69: mantidos como fontes temporárias de evidência a ser revalidada.

### Dados
Os três datasets canônicos permanecem estruturalmente validados, mas ainda não concluíram a nova auditoria factual integral.

## G0 — saneamento

### G0.1 baseline operacional
**CONSOLIDATED.**

### G0.2 reconciliação #57–#69
**CONSOLIDATED.** `main@9e83ffa3fa5fa6e74865f8f2986c30c7966ec239`.

### G0.3 salvamento científico
**IN PROGRESS.**

Fluxo:
`registro atual → legado útil → fonte oficial atual → decisão campo a campo → correção inequívoca → validação`.

Piloto executado em `DR0001–DR0004`; decisões em `docs/audits/VITRINE_SOURCE_AUDIT_PILOT_DR0001_DR0004_2026-08-10.md`.

### G0.4 legado
- #58/#59: **CLOSED / SUPERSEDED**;
- #57: manter até DETER Cerrado ser revalidado;
- #60–#69: manter até os lotes serem percorridos;
- remoção em massa/destrutiva continua HUMAN-DECISION.

### G0.5 analytics roadmap
PR #76 permanece obsoleto em relação ao `main`; seu conteúdo útil deverá ser recriado em branch limpa. Ativação de analytics continua HUMAN-DECISION.

## G1 — contrato canônico

**MATERIALIZED / VALIDATING — AUTO-SAFE.**

`docs/VITRINE_CANONICAL_DATA_CONTRACT.md` congela o schema existente sem novas colunas:
- fontes: 34 campos;
- produtos: 24 campos;
- distribuições: 15 campos;
- IDs/relações e critérios de granularidade definidos;
- informação sem campo semanticamente correto permanece na trilha de auditoria;
- mudança de contrato durante a auditoria é HUMAN-DECISION.

O piloto `DR0001–DR0004` confirmou que a auditoria pode avançar sem expansão imediata do schema.

## G2 — baseline científico

**STARTED VIA PILOT.**

Piloto identificou:
- DR0001 Clima Gerais: linha conceitualmente coerente; nenhuma correção inequívoca imediata;
- DR0002 IDE-Sisema: homepage atual é Geoportal 3.0; WMS/WFS/WCS/CSW confirmados; documentação oficial de webservices disponível; `data_formats` mistura protocolos e formatos e precisa correção;
- DR0003 AdaptaBrasil: termos oficiais confirmam dados públicos/abertos/gratuitos e licença CC BY-SA; licença e documentação de acesso precisam correção;
- DR0004 SIRENE: linha conceitualmente coerente; não promover licença geral do portal a licença universal dos dados.

Correções candidatas ainda não foram aplicadas ao CSV neste pacote documental.

Meta permanece: 51 fontes + 11 produtos + 19 distribuições.

## G3 — expansão

Bloqueada até G1 consolidado e auditoria inicial G2 estabilizada. Depois: batches pequenos, foco Brasil e apenas entidades materialmente distintas.

## G4 — qualidade

Pendente: QA de URLs/IDs/relações, acessibilidade, CI proporcional e browsers adicionais quando justificado.

## G5 — 1.0.0 + Zenodo

**HUMAN-DECISION / BLOQUEADO** até baseline científico, documentação, QA, versão/citação/licenças e snapshot estarem consolidados.

## G6 — analytics

**NOT IMPLEMENTED.** Ativação é HUMAN-DECISION.

## Próximas ações

1. integrar contrato + piloto se CI/diff estiverem verdes (`AUTO-SAFE`);
2. aplicar correções inequívocas de DR0002/DR0003 em pacote DATA pequeno;
3. continuar auditoria sequencial DR0001→DR0051, sem duplicar pesquisa já concluída;
4. fechar PRs #60–#69 gradualmente depois de decidir seus lotes;
5. reconstruir roadmap analytics em branch limpa quando não competir com a auditoria;
6. concluir 51 + 11 + 19;
7. iniciar expansão de volume.

## Fluxo normal

**discover → verify → curate → validate → publish → monitor → periodically release**.