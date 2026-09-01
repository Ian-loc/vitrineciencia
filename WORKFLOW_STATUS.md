# Estado do workflow — Vitrine Ciência

Atualização: **2026-09-01** (`America/Sao_Paulo`)

## Direção ativa

A Vitrine entra em fase de **QA/QC, manutenção e re-curadoria do corpus**. A **expansão de novas fontes, produtos e distribuições está pausada** e só pode ser retomada por instrução humana explícita.

A descoberta pública deixa de depender de busca livre e passa a priorizar perguntas socioecológicas e filtros controlados. A ordem de decisão é: **fenômeno/processo → território → tempo/escala → dado → acesso → fonte/proveniência**.

## Estado corrente

Corpus vivo restaurado: **51 fontes, 11 produtos e 19 distribuições**.

- origem do núcleo: auditoria oficial 51/51 consolidada em 10/08/2026;
- os 11 produtos e 19 acessos detalhados pertencem à camada de produtos existente nesse núcleo;
- expansão v1.0.0: preservada em `data/quarantine/v1.0.0-expanded/` para revisão;
- release `v1.0.0`: permanece publicada, imutável e citável;
- DOI: `10.5281/zenodo.22130831`.

A release congelada contém 135 fontes, 843 produtos e 876 distribuições. Essas contagens descrevem a release histórica, não a superfície viva que está sendo re-curada.

## Prioridades

1. retirar busca livre como mecanismo principal e manter filtros estáveis/controlados;
2. organizar a entrada por fenômenos e processos socioecológicos;
3. revisar links para separar dados, landing pages, serviços, visualizações e documentação;
4. marcar acessos incertos em vez de tratá-los como confirmados;
5. reavaliar a expansão registro a registro antes de qualquer reentrada;
6. manter fonte/provedor e nome técnico como contexto subordinado.

## Critérios do pacote atual

- 51 fontes / 11 produtos / 19 distribuições no corpus vivo;
- 135/843/876 preservados integralmente na quarentena da release;
- filtros principais controlados e sem campo de busca livre visível;
- atalhos de fenômenos/processos na home;
- catálogos/serviços identificados como contexto, não como dataset;
- auditoria de links regenerada a partir do corpus vivo;
- QA em desktop/tablet/mobile;
- CI verde antes do merge.

## Fora do caminho ativo

- reintroduzir em massa produtos técnicos apenas para aumentar contagem;
- tratar mapa/PDF/documentação como acesso a dados sem deixar isso explícito;
- inferir qualidade, licença, cobertura ou disponibilidade ausente;
- modificar retroativamente a release v1.0.0;
- criar nova release/tag/DOI sem instrução humana explícita.
