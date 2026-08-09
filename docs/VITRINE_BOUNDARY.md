# Vitrine Ciência — operational boundary

Decision date: 2026-08-09

## Scope

This repository is the home of the **Vitrine Ciência**, the continuously available static catalog.

The Simbiotrama development line has moved to `Ian-loc/simbiotrama` and is being migrated under a protected, non-destructive process.

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

## CI contract

Vitrine CI validates only static data generation, frontend integrity, search/filter contracts and the isolated Pages artifact. PostgreSQL/PostGIS and Simbiotrama architecture are forbidden dependencies of the Vitrine deploy job.

## Migration safeguard

Simbiotrama branches and PRs already present in this repository are historical/source evidence during migration. They must not be deleted or merged into Vitrine `main` until their target representation in `Ian-loc/simbiotrama` is materialized and verified.

## Completion test

The Vitrine separation is complete when:

1. its CI is green without any Simbiotrama job;
2. Pages publishes only the Vitrine artifact;
3. public navigation, search and filters work from the new repository URL;
4. a Simbiotrama failure cannot block Vitrine deployment.
