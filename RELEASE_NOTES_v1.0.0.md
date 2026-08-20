# Vitrine Ciência v1.0.0 — candidata à primeira release científica estável

**Candidate snapshot date:** 2026-08-19  
**Release type planned:** Dataset  
**Status:** release candidate prepared; not yet published as an immutable Git tag, GitHub Release or Zenodo deposit.

## Snapshot

- 135 sources (`DR####`)
- 843 products (`DP######`)
- 876 distributions (`DD######`)
- highest current identifiers: `DR0135`, `DP000861`, `DD000894`
- source verification dates through 2026-08-19
- canonical model: source → product → distribution
- schema: 34 source fields, 24 product fields, 15 distribution fields

## Scientific object

Vitrine Ciência is a curated discovery dataset. Its original scientific contribution is the structured curation of data-source identity, products, distributions, access mechanisms, spatial and temporal coverage, formats, methods where documented, licensing conditions, limitations, evidence and verification dates.

The candidate does **not** redistribute complete third-party datasets merely because they are catalogued. Users should cite both Vitrine Ciência and the original provider/dataset used in an analysis.

## Stability commitment proposed for v1.0.0

Version 1.0.0 is intended to mark deliberate stability of the public source → product → distribution contract once the immutable tag/release is explicitly approved and created. Historical identifiers are not recycled.

Unknown or variable information is retained explicitly when the available evidence does not justify a more precise statement.

## Included canonical data

- `data/data_resources.csv`
- `data/data_products.csv`
- `data/product_distributions.csv`
- `data/brazil_scope_priorities.json`

Derived JSON files and the public site are rebuilt from the same canonical tables.

## Documentation and reproducibility

The candidate includes:

- `README.md`
- `METHODOLOGY.md`
- `CODEBOOK.md`
- `PRODUCT_CATALOG_MODEL.md`
- `CITATION.cff`
- `LICENSE`
- `LICENSE-DATA.md`
- `CHANGELOG.md`
- `FINAL_OBJECTIVES_AND_DOI_GATES.md`
- `docs/RELEASE_POLICY.md`

Automated validation covers canonical structure, source/product/distribution relationships, build generation and public-interface checks.

## Licensing

- repository software/code: MIT License;
- original Vitrine Ciência metadata and curation: CC BY 4.0;
- third-party datasets, services and publications retain their own licenses and terms. Their inclusion in the catalogue does not relicense them.

## Citation before formal release

Until an immutable `v1.0.0` tag/GitHub Release exists, cite the project and record the exact commit used for reproducibility:

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. GitHub, 2026.

ORCID: https://orcid.org/0000-0003-1164-9318

After the release is explicitly approved and published, the citation should include `Version 1.0.0`. The Zenodo DOI should be appended only after deposition and then propagated to repository metadata and academic profiles without modifying the frozen scientific content.

## Release gate status

Current candidate state:

- G1 identity: prepared
- G2 integrity: canonical validators available and repeatedly exercised; final release-commit run still required
- G3 semantics: contract stable; explicit unknown/variable states retained
- G4 licenses: separated between Vitrine and external providers
- G5 documentation: candidate documentation prepared and under QA/QC
- G6 publication: final Pages build must correspond to the eventual release commit
- G7 immutability: Git tag `v1.0.0` has **not** been created
- G8 deposit: Zenodo package has **not** been published
- G9 propagation: performed only after DOI issuance

The candidate is not a formal scientific release until the applicable release gates are completed and the human decision to publish the immutable tag/release is explicit.
