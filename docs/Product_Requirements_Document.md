# Product Requirements Document: NSRL-to-UCO Converter

## Overview
The NSRL-to-UCO Converter is a Python tool developed by the Linux Foundation's Cyber Domain Ontology project to convert NIST's National Software Reference Library (NSRL) CAID data from it's native ODATA JSON format into UCO (Unified Cyber Ontology) compliant JSON-LD format. The NSRL provides file hash sets that serve as digital fingerprints for known files, supporting digital forensics investigations and file identification. This converter enables NSRL CAID data to be integrated with digital forensic tools that implement the CASE/UCO specification.

## Objectives
- Convert NSRL CAID JSON data to UCO-compliant JSON-LD format for use in CASE/UCO tools
- Maintain data integrity through accurate property mapping
- Preserve file hash values and metadata
- Support provenance tracking of data transformations
- Enable interoperability with CASE/UCO-compliant forensic tools
- Ensure compliance with UCO 1.4.0 specification

## Background
The National Software Reference Library (NSRL), maintained by the National Institute of Standards and Technology (NIST), provides a collection of digital signatures of known files. The NSRL CAID dataset is part of their Non-RDS hash sets, containing file signatures in JSON format. By converting this data to UCO format, it can be integrated into modern digital forensic workflows that use the CASE/UCO standards for representing cyber-investigation information.

## Functional Requirements

### Core Functionality
1. File Conversion
   - Convert NSRL CAID ODATA JSON files to UCO-compliant JSON-LD
   - Support batch processing of multiple files
   - Maintain original file relationships and hierarchies
   - Generate consistent and valid JSON-LD output
   - Ensure compliance with UCO 1.4.0

2. Data Mapping
   - Map NSRL media objects to UCO File objects
   - Preserve all hash values (MD5, SHA1) with proper typing
   - Maintain file metadata (size, path, name)
   - Convert categories using proper namespaces
   - Generate UTC timestamps for all temporal data

3. Provenance Tracking
   - Record tool information including self-hashes
   - Document NIST's NSRL as authoritative source
   - Maintain relationships between objects
   - Track input/output file associations
   - Include timestamps for all provenance records

4. Output Management
   - Generate individual UCO files for each input
   - Option to combine multiple outputs into single graph
   - Create consistent output directory structure
   - Handle file naming and versioning
   - Validate output using CASE Utilities

### Technical Requirements

1. Tool Implementation
   - Implement as a ConfiguredTool in UCO
   - Include tool self-hashing capability
   - Generate deterministic tool identifiers
   - Document tool creator and purpose
   - Support UTC timestamps

2. Data Validation
   - Validate input JSON format
   - Verify UCO compliance using CASE Utilities
   - Check hash integrity and format
   - Handle missing or malformed data
   - Validate timestamp formats

3. Error Handling
   - Graceful handling of malformed input
   - Clear error messages and logging
   - Recovery from processing failures
   - Input validation and sanitization
   - Validation error reporting

## Non-Functional Requirements

1. Performance
   - Efficient processing of large files
   - Minimal memory footprint
   - Support for batch processing
   - Reasonable conversion times
   - Efficient validation processing

2. Usability
   - Clear command-line interface
   - Helpful error messages
   - Progress indicators
   - Documentation and examples
   - Validation status reporting

3. Maintainability
   - Well-documented code
   - Modular design
   - Version control
   - Test coverage
   - Validation test suite

4. Compatibility
   - Python 3.9+ support
   - Cross-platform functionality
   - CASE Utilities dependency
   - UCO 1.4.0 ontology compliance
   - Standard library dependencies

## Constraints and Assumptions
- Input files follow NSRL CAID JSON/OData format
- UCO ontology version 1.4.0 compatibility
- Python 3.9+ environment availability
- CASE Utilities installation
- File system access permissions
- Access to NSRL CAID dataset

## Success Criteria
1. Successful conversion of NSRL CAID files to UCO format
2. Preservation of all critical data and relationships
3. Valid JSON-LD output that passes CASE validation
4. Accurate provenance tracking with timestamps
5. Reliable tool operation with proper error handling

## Future Considerations
1. Support for additional NSRL data formats
2. Integration with other CASE/UCO tools
3. GUI interface development
4. Enhanced reporting capabilities
5. Additional validation features

## User Stories

1. Digital Forensic Analyst
   "As a digital forensic analyst, I need to convert NSRL CAID data to UCO format so I can correlate file hashes across multiple evidence sources in my graph database. Having a tool that helps me understand the provenance of the data and analysis steps is important as it makes my analysis defensible and reproducible."
   
   Acceptance Criteria:
   - Successfully converts NSRL CAID JSON to valid UCO JSON-LD
   - Preserves all hash values and file metadata
   - Processes files under 5 seconds for typical input
   - Maintains relationships between objects
   - Passes CASE validation

2. Forensic Tool Developer
   "As a forensic tool developer, I need to batch process multiple NSRL CAID files and combine them into a single UCO graph while avoiding ID collisions."
   
   Acceptance Criteria:
   - Processes multiple input files
   - Combines results without ID conflicts
   - Maintains consistent relationship structure
   - Reports any conversion errors
   - Validates combined output

3. Data Scientist
   "As a data scientist, I need to validate that converted UCO data maintains integrity with the original NSRL CAID data for statistical analysis."
   
   Acceptance Criteria:
   - Validates all hash values match
   - Preserves all metadata fields
   - Provides validation reporting
   - Handles large datasets efficiently
   - Ensures timestamp consistency

## Constraints & Risks

### Technical Constraints
- Input files can be multiple gigabytes
- Memory usage must be managed for large files
- Python 3.9+ environment required
- UCO ontology version 1.4.0 compatibility
- CASE Utilities dependency

### Known Risks
- ID collisions in combined output
- Incomplete ODATA navigation properties
- Memory overflow with large files
- Schema validation performance impact
- Validation tool compatibility

### Mitigation Strategies
- Implement chunk-based processing
- Use deterministic UUID generation
- Add progress monitoring
- Optimize validation routines
- Regular CASE Utilities updates
