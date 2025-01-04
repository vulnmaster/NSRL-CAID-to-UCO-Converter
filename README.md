# NSRL-CAID to UCO Converter

This tool converts NSRL-CAID JSON files to UCO (Unified Cyber Ontology) format. It maps NSRL-CAID media objects to UCO observable:File objects with appropriate facets.

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

### Using default output folder ('output') to combine all files input json graph files into a single graph file:
```bash
python nsrl_to_uco.py data/ --combine
```

### Specifying custom output folder to combine all files input json graph files into a single graph file:
```bash
python nsrl_to_uco.py data/ -o custom_output/ --combine
```

## Mapping Details

The converter maps NSRL-CAID objects to UCO objects following these rules:

### Media Objects
- NSRL Media objects become `uco-observable:File` objects
- MediaID becomes the object's `@id` with prefix "kb:media-"
- Category maps to categories
- Includes FileFacet with size and HashFacet with MD5 and SHA1 hashes

### Media Files
- Each MediaFile becomes a `uco-observable:File` object
- Includes FileFacet with filename and filepath
- Includes HashFacet with MD5 hash

## Output Format

The output is JSON-LD with:
- UCO context definitions
- Graph of File objects with appropriate facets
- Each file has a unique kb:media- identifier
- Properties use proper UCO namespaces (observable:, types:)

## Dependencies
- Python 3.6+
- Standard library only (no external dependencies)

## Error Handling
- Reports processing errors for individual files
- Continues processing remaining files if one fails
- Creates output directory if it doesn't exist

