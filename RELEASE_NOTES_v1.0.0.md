# Vitrine Ciência v1.0.0

**Release date:** 2026-08-19  
**Release type:** Dataset  
**Status:** first stable scientific release; prepared for immutable Git tag, GitHub Release and Zenodo deposition.

## Snapshot

- 135 sources (`DR####`)
- 833 products (`DP######`)
- 866 distributions (`DD######`)
- highest current identifiers: `DR0135`, `DP000861`, `DD000894`
- source verification dates through 2026-08-19
- canonical model: source → product → distribution
- schema: 34 source fields, 24 product fields, 15 distribution fields

## Scientific object

Vitrine Ciência is a curated discovery dataset. Its original scientific contribution is the structured curation of data-source identity, products, distributions, access mechanisms, spatial and temporal coverage, formats, methods where documented, licensing conditions, limitations, evidence and verification dates.

The release does **not** redistribute complete third-party datasets merely because they are catalogued. Users should cite both Vitrine Ciência and the original provider/dataset used in an analysis.

## Stability commitment

Version 1.0.0 marks deliberate stability of the public source → product → distribution contract. Future growth can add or correct records without changing the meaning of this release. Historical identifiers are not recycled.

Unknown or variable information is retained explicitly when the available evidence does not justify a more precise statement.

## Included canonical data

- `data/data_resources.csv`
- `data/data_products.csv`
- `data/product_distributions.csv`
- `data/brazil_scope_priorities.json`

Derived JSON files and the public site are rebuilt from the same canonical tables.

## Documentation and reproducibility

The release includes:

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

## Citation

Cite this release as:

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. Version 1.0.0. 2026.

ORCID: https://orcid.org/0000-0003-1164-9318

The Zenodo DOI should be appended after deposition and then propagated to the repository metadata and academic profiles without modifying the frozen scientific content.

## Release gate status

At preparation time:

- G1 identity: prepared
- G2 integrity: canonical validators in repository; final run required on release commit
- G3 semantics: contract stable; explicit unknown/variable states retained
- G4 licenses: separated between Vitrine and external providers
- G5 documentation: prepared for v1.0.0
- G6 publication: final Pages build must correspond to release commit
- G7 immutability: Git tag `v1.0.0` must be created after merge
- G8 deposit: Zenodo package must be inspected before publication
- G9 propagation: performed after DOI issuance

The release is not considered DOI-published until G1–G8 are satisfied on the immutable release commit.
