# Vitrine Ciência v1.0.0 — primeira release científica estável

**Snapshot date:** 2026-08-19  
**Release type:** Dataset  
**Git tag:** `v1.0.0`  
**Frozen scientific commit:** `27c545554f406b940662777e3f053e939ef3588c`  
**GitHub Release:** https://github.com/Ian-loc/vitrineciencia/releases/tag/v1.0.0  
**Zenodo record:** https://zenodo.org/records/22130831  
**DOI:** https://doi.org/10.5281/zenodo.22130831  
**Status:** published and preserved.

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

The release does **not** redistribute complete third-party datasets merely because they are catalogued. Users should cite both Vitrine Ciência and the original provider/dataset used in an analysis.

## Stability commitment

Version 1.0.0 marks the first deliberately frozen scientific snapshot of the source → product → distribution contract. Historical identifiers are not recycled. Unknown or variable information is retained explicitly when the available evidence does not justify a more precise statement.

The living `main` branch and public interface may continue to evolve after this release. Reproducibility for v1.0.0 is anchored to the immutable tag, frozen commit and Zenodo deposit, not to the later state of `main`.

## Included canonical data

- `data/data_resources.csv`
- `data/data_products.csv`
- `data/product_distributions.csv`
- `data/brazil_scope_priorities.json`

Derived JSON files and release metadata were generated from the same frozen scientific snapshot.

## Documentation and reproducibility

The release package includes the core scientific documentation and metadata required to interpret and reuse the curated catalog, including README, methodology, codebook, citation metadata, licenses, changelog/release notes, DOI-gate documentation, schema/provenance metadata and validation evidence.

Automated validation covered canonical structure, source/product/distribution relationships, build generation, normalization, link roles, schema identity and public-interface integrity. The released scientific archive is:

`vitrine-ciencia-v1.0.0.zip`

SHA-256:

`b2e7a996b075d45ef4caca853bf57618b54998724fc9b4bdea3afe3b6159d6f0`

## Licensing

- repository software/code: MIT License;
- original Vitrine Ciência metadata and curation: CC BY 4.0;
- third-party datasets, services and publications retain their own licenses and terms. Their inclusion in the catalogue does not relicense them.

## Citation

> CLEMENTE, Ian. *Vitrine Ciência: catálogo de fontes de dados científicos sobre o Brasil para pesquisa, ensino e extensão*. Version 1.0.0. Zenodo, 2026. https://doi.org/10.5281/zenodo.22130831

ORCID: https://orcid.org/0000-0003-1164-9318

For reproducible scientific use, cite the Vitrine Ciência release actually used and separately cite each original source/dataset that supplied data to the analysis.

## Release gate status

- G1 identity: substantially complete; GitHub repository Homepage metadata remains an administrative item to confirm/correct
- G2 integrity: complete
- G3 semantics: complete
- G4 licenses: complete
- G5 documentation: complete
- G6 publication: public interface operational; the living site may advance beyond the frozen DOI snapshot
- G7 immutability: complete — annotated tag `v1.0.0` and GitHub Release published
- G8 deposit: complete — validated Dataset deposited in Zenodo record `22130831`
- G9 propagation: partially complete — DOI propagated through repository metadata/documentation; external academic-profile propagation remains administrative
