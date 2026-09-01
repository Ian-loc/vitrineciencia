# Estado canônico — Vitrine Ciência

**Data de referência:** 1 de setembro de 2026  
**Fuso:** `America/Sao_Paulo`  
**Estado global:** fase ativa de QA/QC e manutenção; expansão pausada; núcleo público em re-curadoria.

A release científica `v1.0.0` publicada permanece imutável e preservada no Zenodo com DOI `10.5281/zenodo.22130831`. A `main` é um produto vivo e, a partir deste pacote, volta ao núcleo auditado anterior à expansão para corrigir problemas de utilidade, granularidade e acesso sem reescrever a release.

## 1. Autoridade

1. `main` de `Ian-loc/vitrineciencia` para o estado vivo;
2. tag/release `v1.0.0` e Zenodo para o snapshot científico imutável;
3. CSVs canônicos vivos em `data/`;
4. snapshot expandido congelado em `data/quarantine/v1.0.0-expanded/`;
5. validadores, documentação ativa e auditorias.

## 2. Corpus vivo

O núcleo restaurado é o conjunto auditado de 51 fontes consolidado após a auditoria oficial 51/51 de 10/08/2026. O estado vivo contém:

- **51 fontes**;
- **11 produtos**;
- **19 distribuições**.

Os produtos detalhados ainda cobrem apenas parte das 51 fontes. Isso é explicitamente tratado como lacuna de curadoria, não como autorização para recolocar centenas de registros técnicos sem revisão.

A expansão de novas fontes, produtos e distribuições está **pausada**. Reentrada a partir da quarentena exige instrução humana explícita, evidência de acesso a dados e ganho científico material.

## 3. Snapshot científico v1.0.0

A release histórica contém 135 fontes, 843 produtos e 876 distribuições no commit `27c545554f406b940662777e3f053e939ef3588c`. Essas tabelas foram copiadas sem alteração para `data/quarantine/v1.0.0-expanded/` para manter validação local do DOI e revisão registro a registro. A quarentena não muda tag, release, DOI ou arquivo Zenodo.

## 4. Direção da experiência pública

A descoberta deve responder primeiro à pergunta científica do usuário:

**fenômeno/processo → território → tempo/escala → dado utilizável → acesso → provedor/proveniência**.

Fonte, acrônimo, nível de processamento, plataforma e formato são contexto; não devem dominar a entrada da navegação. A busca livre deixa de ser mecanismo primário. A superfície pública prioriza vocabulários controlados, filtros determinísticos e resultados com papel explícito.

Catálogos, visualizadores e serviços permanecem úteis, mas devem ser identificados como infraestrutura de descoberta/acesso e não confundidos com datasets.

## 5. Regra de acesso

Um destino público deve distinguir:

- arquivo/download direto;
- landing page de dataset com download explícito;
- portal de consulta/API que permita extração;
- visualização/documentação sem acesso suficiente aos dados;
- acesso restrito, quebrado ou incerto.

Casos incertos permanecem marcados para revisão; não se converte desconhecido em “sim”. Links de fonte e de produto são auditados separadamente.

## 6. Ciclo de vida

### ACTIVE
- núcleo vivo 51 fontes / 11 produtos / 19 distribuições;
- descoberta por fenômenos/processos e filtros controlados;
- QA/QC de links, classificações e utilidade;
- GitHub Pages e CI.

### QUARANTINE_REVIEW
- expansão v1.0.0 de 135/843/876 enquanto passa por nova triagem de acesso, granularidade e significado.

### RELEASED
- `v1.0.0`, tag, GitHub Release, Zenodo e DOI, imutáveis.

### PAUSED
- expansão factual sem revisão e decisão humana explícita.

## 7. Gates

Antes de publicar mudança pública:

1. preservar IDs, proveniência e relações;
2. executar validadores de dados e interface;
3. gerar JSONs e relatórios apenas como derivados do corpus vivo;
4. testar desktop, tablet e smartphone;
5. verificar navegação sem dependência de busca livre;
6. distinguir dado, serviço/catálogo e documentação;
7. construir `_site` isolado;
8. exigir CI verde antes de qualquer merge;
9. verificar o site após deploy.

Nenhum merge, tag, release ou novo DOI é autorizado por este documento.
