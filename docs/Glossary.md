# NSRL-to-UCO Converter Glossary

## Introduction
This glossary defines the primary terms used throughout the NSRL-to-UCO Converter's documentation and implementation. Understanding these terms will help developers navigate the codebase, understand the data transformations, and extend functionality. The converter currently targets UCO 1.3.0; future ontology updates may require changes to the converter and this documentation.

## Core Concepts

### NSRL CAID
The National Software Reference Library's Computer-Aided Investigative Data - a collection of file signatures and metadata maintained by NIST to support digital forensics.
Reference: https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl/about-nsrl

For implementation details, see [Data Model Design Document → Input Data Model].

### UCO (Unified Cyber Ontology)
A community-developed standard that provides a structured specification for representing cyber investigation information. UCO defines concepts that are used across various cyber investigation domains.
Reference: https://ontology.unifiedcyberontology.org/uco/uco/1.3.0

Example usage in converter output:
```json
{
  "@context": {
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/"
  }
}
```

## Data Model Terms

### Bundle
A UCO core concept that groups related cyber investigation information together, maintaining context and provenance of the data.
Reference: https://ontology.unifiedcyberontology.org/uco/core/1.3.0

Example in converter:
```json
{
  "@type": "uco-core:Bundle",
  "uco-core:objects": [],
  "uco-core:object": []
}
```
See [Data Model Design Document → Bundle Structure] for more details.

### ConfiguredTool
A UCO tool type representing a specific instance of a tool with its configuration, metadata, and usage context.
Reference: https://ontology.unifiedcyberontology.org/uco/tool/1.3.0

Used in the converter to represent itself:
```json
{
  "@type": "uco-tool:ConfiguredTool",
  "uco-core:name": "nsrl_to_uco.py",
  "uco-tool:creator": "Linux Foundation Cyber Domain Ontology Project"
}
```

### Facet
A UCO core concept that represents specific characteristics, properties, or aspects of an object. Facets are used to describe different views or aspects of the same object.
Reference: https://ontology.unifiedcyberontology.org/uco/core/1.3.0

Example of a FileFacet in converter output:
```json
{
  "@type": "uco-observable:FileFacet",
  "uco-observable:fileName": "example.exe",
  "uco-observable:hash": []
}
```

### ODATA
Open Data Protocol - the format used by NSRL CAID for structuring Project VIC JSON data with navigation properties and relationships.
Reference: https://www.odata.org/documentation/

See [Data Model Design Document → Input Data Model] for ODATA structure examples.

## Technical Terms

### JSON-LD
JSON for Linked Data - A W3C standard method for encoding Linked Data using JSON. UCO and CASE use JSON-LD as their primary serialization format to represent cyber investigation information.
Reference: https://www.w3.org/TR/json-ld11/

### Hash
A cryptographic representation of digital content, used in UCO for uniquely identifying and verifying the integrity of digital objects. Common hash methods include MD5 and SHA1.
Reference: https://ontology.unifiedcyberontology.org/uco/types/1.3.0

Example in converter:
```json
{
  "@type": "uco-types:Hash",
  "uco-types:hashMethod": "MD5",
  "uco-types:hashValue": "d41d8cd98f00b204e9800998ecf8427e"
}
```

### IRI
Internationalized Resource Identifier - A unique identifier used in JSON-LD and UCO/CASE to reference resources and concepts within the ontology.
Reference: https://www.w3.org/TR/json-ld11/#iris

### Provenance
The record of the origin and history of a piece of data or evidence, tracking its ownership, custody, and transformations over time. In UCO, provenance is captured through relationships like createdBy, derivedFrom, and processed, ensuring transparency and accountability in cyber-investigations.
Reference: https://ontology.unifiedcyberontology.org/uco/core/1.3.0

Example in converter:
```json
{
  "@type": "uco-core:Relationship",
  "uco-core:source": "kb:bundle-uuid",
  "uco-core:target": "kb:tool-uuid",
  "uco-core:kindOfRelationship": "createdBy",
  "uco-core:isDirectional": true
}
```
See [Data Model Design Document → Relationship Mappings] for details on how provenance is maintained.

## Relationship Types
The converter uses these relationships to establish provenance and connections between objects:

### createdBy
The identity that created a characterization of a concept. Used in the converter to indicate that the UCO Bundle was created by this tool.
Reference: https://ontology.unifiedcyberontology.org/uco/core/1.3.0

### derivedFrom
Indicates that an object is derived from another object, establishing provenance relationships in cyber investigations. Used to show that UCO output is derived from NSRL CAID input.
Reference: https://ontology.unifiedcyberontology.org/uco/core/1.3.0

### managedBy
Specifies the organization or entity responsible for maintaining or managing a particular resource. Used to indicate NIST's management of the NSRL dataset.
Reference: https://ontology.unifiedcyberontology.org/uco/core/1.3.0

### processed
Indicates that a tool or process has performed operations on specific input data, creating derived outputs. Shows that the converter processed the NSRL CAID input file.
Reference: https://ontology.unifiedcyberontology.org/uco/core/1.3.0

See [App Flow Document → Process Flow] for details on how these relationships are created during conversion. 