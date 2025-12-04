# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-12-04

### Added
- Integrated automated SHACL validation using `case_validate` from `case-utils`.
- Added `.gitignore` configuration to exclude development artifacts and `.cursorrules`.
- Added `pyshacl` and `rdflib` dependencies for local validation.

### Changed
- Updated target ontology version from UCO 1.3.0 to UCO 1.4.0.
- Updated `nsrl_to_uco.py` to map file hashes to `ContentDataFacet` in compliance with UCO standards.
- Fixed logic error where `hasFacet` was being overwritten, ensuring both `FileFacet` and `ContentDataFacet` are preserved.
- Updated `uco-types:hashMethod` and `uco-observable:byteOrder` to use `xsd:string` literals instead of vocabulary references for UCO 1.4.0 compliance.
- Updated project documentation to reflect UCO 1.4.0 requirements and new validation workflow.
- Updated dependencies in `requirements.txt` to latest versions.

## [1.0.0] - 2024-01-05

### Added
- Initial release of NSRL-CAID to UCO Converter.
- Support for converting NSRL CAID ODATA JSON to UCO 1.3.0 JSON-LD.
- Support for MD5 and SHA1 hash mapping.
- Batch processing and combined graph output capabilities.

