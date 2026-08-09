# Structural separation milestone — Vitrine Ciência × Simbiotrama

Date: 2026-08-09
Timezone: America/Sao_Paulo

## Decision

The former combined line has been split into two independently governed repositories:

- **Vitrine Ciência** — `Ian-loc/vitrineciencia`
- **Simbiotrama** — `Ian-loc/simbiotrama`

The Vitrine is a stable public static product. Simbiotrama is a separate scientific/data-architecture development project. Historical continuity exists, but neither project is a runtime dependency of the other.

## Vitrine milestone

Separation PR: `Ian-loc/vitrineciencia#70`

Authorized PR head:

`1fe074455d26e1e40af2a2e75c78c358ef145fea`

Resulting `main` commit:

`36211e96edc86fa0e2bb31c703141cd7c5df5480`

The merge:

- removed Simbiotrama/Simbioscópio surfaces from the Pages artifact;
- changed canonical repository and Pages URLs to the renamed Vitrine repository;
- removed PostgreSQL/PostGIS and Instance 1 from the Vitrine deployment dependency graph;
- added an explicit Vitrine boundary validator;
- retained the 51-source public catalog and product/filter logic without scientific-data changes;
- retained historical source branches and PRs for protected migration rather than deleting them.

The separation PR CI passed at head `1fe074455d...` before merge. The first run exposed a stale repository URL in the README; it was corrected and the subsequent validation run passed all Vitrine data/interface/artifact gates.

## Simbiotrama handoff

The protected migration target is `Ian-loc/simbiotrama`.

The source baseline immediately before the Vitrine-only separation is:

`a831612a23c44b30913a30c35e2981c6960708b7`

The active unmerged source chain is preserved from PR #58 through PR #69, with the current top source head:

`cfde00033b8bf542c1d0147685acc31278cef8f3`

These source PRs are preservation evidence until their target representation is materialized and validated in the Simbiotrama repository.

## Governance consequences

From this milestone forward:

1. new Simbiotrama development must occur in `Ian-loc/simbiotrama`;
2. no Simbiotrama PR is to be merged into Vitrine `main`;
3. Vitrine Pages must remain independently deployable;
4. Vitrine public data/interface maintenance may proceed without waiting for Simbiotrama;
5. Simbiotrama architecture, database, curatorial pipelines and future instances may evolve without changing or redeploying the Vitrine;
6. shared historical material must have explicit provenance and one active owner after migration;
7. migration completion is a materialization/verification claim, not a documentation claim.

## Availability contract

The Vitrine is considered operational only when:

- the Pages build is successful;
- the public site is reachable at `https://ian-loc.github.io/vitrineciencia/`;
- navigation, search, filters, product comparison, analytics and downloads work;
- the public artifact contains no Simbiotrama runtime surface.

The repository-level CI protects the code/data side of this contract. External reachability must additionally be checked after each deployment because hosting configuration is an external state.

## Retention rule

No historical source branch or migration-critical PR is deleted merely because the repository split occurred. Cleanup is authorized only after target coverage is recorded and verified in the Simbiotrama migration ledger.