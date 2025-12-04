# NSRL-CAID to UCO Converter

This tool converts NSRL-CAID JSON files to UCO (Unified Cyber Ontology) format. It maps NSRL-CAID media objects to UCO observable:File objects with appropriate facets and relationships to support data provenance.

NSRL-CAID JSON files are available from https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl/nsrl-download/non-rds-hash 

## Usage

### Process a single file
```bash
python nsrl_to_uco.py data/NSRL-CAID-WMV.json
```

### Process all JSON files in a directory
```bash
python nsrl_to_uco.py data/
```

### Specify custom output directory
```bash
python nsrl_to_uco.py data/ -o custom_output/
```

### Process all files and create a combined graph
When using the --combine flag, the script will:
1. Create individual UCO files for each input
2. Create an additional combined graph file

Using default output folder:
```bash
python nsrl_to_uco.py data/ --combine
```

Using custom output folder:
```bash
python nsrl_to_uco.py data/ -o custom_output/ --combine
```

### Additional Options
```bash
# Enable debug logging
python nsrl_to_uco.py data/ --debug

# Write logs to file
python nsrl_to_uco.py data/ --log-file conversion.log

# Enable output validation
python nsrl_to_uco.py data/ --validate
```

## Mapping Details

The converter maps NSRL-CAID objects to UCO objects following these rules:

### Media Objects
- NSRL Media objects become `uco-observable:File` objects
- MediaID becomes the object's `@id` with prefix "kb:media-"
- Category maps to `uco-observable:categories`
- Includes FileFacet with:
  - File name and path
  - Size in bytes from MediaSize
  - MD5 hash from MediaFile (as `xsd:hexBinary`)
  - SHA1 hash from parent Media object (as `xsd:hexBinary`)
  - Hash methods using `uco-vocabulary:HashNameVocab`

### Media Files
- Each MediaFile becomes a `uco-observable:File` object
- Includes FileFacet with filename and filepath
- Includes HashFacet with MD5 hash (as `xsd:hexBinary`)
- All timestamps in UTC format

## Output Format

### Individual Files
Each input file produces a corresponding UCO JSON-LD file containing:
- Full UCO context definitions with all required namespaces
- Bundle with tool, organization, and source objects
- File objects with appropriate facets
- Provenance relationships with timestamps
- Compliant with UCO 1.3.0 specification

### Combined Output
When using --combine, an additional uco-combined.json is created containing:
- Single UCO context with all namespaces
- All bundles from individual files
- Preserved relationships and provenance
- Validated against CASE/UCO standards

## Dependencies
- Python 3.9+
- CASE Utilities Python package
- Standard library

## Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install case_utils
```

## Error Handling
- Reports processing errors for individual files
- Continues processing remaining files if one fails
- Creates output directory if it doesn't exist
- Detailed logging with optional file output
- Progress tracking for batch processing
- Validation error reporting

## Validation
The tool uses CASE Utilities to validate output against UCO 1.4.0:
- Validates JSON-LD structure
- Checks UCO ontology compliance
- Verifies relationship integrity
- Ensures proper timestamp formats
- Reports validation errors

## Documentation
For details on how NSRL CAID fields map to UCO, see [Data Model Design Document](docs/Data_Model_Design_Document.md)

