# Vitrine Ciência — operational boundary

Decision date: 2026-08-09
Structural separation merge: PR #70 → `36211e96edc86fa0e2bb31c703141cd7c5df5480`

## Status

This repository is the authoritative home of the **Vitrine Ciência**, the continuously available public static catalog.

The **Simbiotrama** is now an independent work front in `Ian-loc/simbiotrama`. Its migration is governed separately and must not become a runtime or deployment dependency of this repository.

## Public artifact contract

GitHub Pages may publish only:

- `index.html`;
- `products.html`;
- `analytics.html`;
- `about.html`;
- the CSS/JS assets required by those pages;
- static catalog datasets explicitly required by those pages;
- licenses and optional site metadata.

The Pages artifact must not include:

- Simbiotrama/Simbioscópio explorer or roadmap pages;
- relational database/schema material;
- migration or curation runtime scripts;
- internal docs/audits;
- Simbiotrama CI/configuration;
- `data/federated_layers.json`.

## CI and availability contract

Vitrine CI owns only:

1. validation of the static catalog inputs;
2. deterministic generation of public JSON/build metadata;
3. HTML/CSS/JavaScript integrity and accessibility checks;
4. search/filter product-interface contracts;
5. construction of the isolated `_site` artifact;
6. GitHub Pages deployment.

PostgreSQL/PostGIS, Simbiotrama schemas, migration scripts and Instance 1 jobs are forbidden dependencies of the Vitrine deployment graph.

A failure in Simbiotrama must not block a Vitrine deployment. A failure in the Vitrine must not alter or block Simbiotrama development.

## Repository ownership

The following are owned by the Vitrine:

- public catalog interface;
- public static datasets used by the interface;
- Vitrine-specific build/validation scripts;
- GitHub Pages workflow;
- Vitrine citation, licensing and public-method documentation.

The following are not owned by the Vitrine:

- Simbiotrama relational architecture and database;
- Simbiotrama curatorial/evidence pipelines;
- future Simbiotrama Instances 2 and 3;
- Simbiotrama migration/governance state.

## Migration safeguard

Historical Simbiotrama branches, PRs and files may remain temporarily in this Git history while protected migration is completed. They are **preservation evidence**, not active Vitrine authority.

Rules until migration closure:

- do not merge Simbiotrama work into Vitrine `main`;
- do not delete source branches/PRs before target coverage is verified in `Ian-loc/simbiotrama`;
- do not make public Vitrine code depend on migration-preserved files;
- remove remaining Simbiotrama-owned active-tree material only through a later cleanup PR after migration verification.

## Completion and regression test

The separation remains valid only while all statements below are true:

1. Vitrine CI passes without any Simbiotrama job;
2. Pages publishes only the Vitrine artifact;
3. homepage, navigation, search, filters, product comparison, analytics and downloads remain functional;
4. the canonical public URL is `https://ian-loc.github.io/vitrineciencia/`;
5. a Simbiotrama failure cannot block or remove the Vitrine;
6. a Vitrine failure cannot corrupt or block Simbiotrama;
7. no public page presents Simbiotrama as the identity or continuation of the Vitrine.

See `docs/STRUCTURAL_SEPARATION_MILESTONE_2026-08-09.md` for the milestone record.