# Data Model Design Document: NSRL-to-UCO Converter

## Input Data Model (NSRL CAID)

### Media Object
```json
{
  "odata.id": "Media(588cd1c0e48916d8e7403310402d0a68)",
  "MediaFiles@odata.navigationLinkUrl": "/Media(588cd1c0e48916d8e7403310402d0a68)/MediaFiles",
  "MediaFiles": [
    {
      "Media@odata.navigationLinkUrl": "/MediaFiles(FileName='build2.art',FilePath='Like a Dragon Gaiden- The Man Who Erased His Name/Content/runtime/media/ylad8/data/artisan',MD5=588cd1c0e48916d8e7403310402d0a68)",
      "MD5": "588cd1c0e48916d8e7403310402d0a68",
      "FileName": "build2.art",
      "FilePath": "Like a Dragon Gaiden- The Man Who Erased His Name/Content/runtime/media/ylad8/data/artisan"
    }
  ],
  "MediaID": 0,
  "MD5": "588cd1c0e48916d8e7403310402d0a68",
  "SHA1": "e65706b487c73e992bab2a50707a9fd8b0bd6866",
  "Category": 8,
  "MediaSize": "488"
}
```

### Relationships
- Media to MediaFiles (one-to-many)
- MediaFiles to Media (reference)

## Output Data Model (UCO)

### Bundle Structure
```json
{
  "@context": {
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
    "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
    "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
    "kb": "http://example.org/kb/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "kb:bundle-uuid",
      "@type": "uco-core:Bundle",
      "uco-core:objects": [],
      "uco-core:object": []
    }
  ]
}
```

### File Object
```json
{
  "@id": "kb:media-uuid",
  "@type": "uco-observable:File",
  "uco-observable:categories": "category",
  "uco-core:hasFacet": [
    {
      "@type": "uco-observable:FileFacet",
      "uco-observable:fileName": "name",
      "uco-observable:filePath": "path",
      "uco-observable:hash": [
        {
          "@type": "uco-types:Hash",
          "uco-types:hashMethod": {
            "@type": "uco-vocabulary:HashNameVocab",
            "@value": "MD5"
          },
          "uco-types:hashValue": {
            "@type": "xsd:hexBinary",
            "@value": "588cd1c0e48916d8e7403310402d0a68"
          }
        }
      ]
    }
  ]
}
```

### Tool Object
```json
{
  "@id": "kb:tool-uuid",
  "@type": "uco-tool:ConfiguredTool",
  "uco-core:name": "name",
  "uco-core:description": "description",
  "uco-core:createdBy": {
    "@id": "kb:org-uuid",
    "@type": "uco-identity:Organization",
    "uco-core:name": "creator"
  },
  "uco-core:hasFacet": []
}
```

## Data Mapping Rules

### Object Mappings
1. NSRL Media → UCO File
2. NSRL MediaFiles → UCO FileFacet
3. Tool Information → UCO ConfiguredTool

### Property Mappings
1. Hash Values
   - MD5 → uco-types:Hash with xsd:hexBinary value
   - SHA1 → uco-types:Hash with xsd:hexBinary value

2. File Properties
   - FileName → uco-observable:fileName
   - FilePath → uco-observable:filePath
   - MediaSize → uco-observable:sizeInBytes
   - Category → uco-observable:categories

### Relationship Mappings
1. Tool Relationships
   - Tool → Input (processed)
   - Bundle → Tool (createdBy)

2. Data Source Relationships
   - Input → Source (derivedFrom)
   - Source → Organization (managedBy)

## Validation Rules

### Input Validation
1. Required Fields
   - MD5 hash
   - File name
   - File path

2. Format Validation
   - Valid JSON structure
   - ODATA compliance
   - Hash format verification

### Output Validation
1. Schema Compliance
   - Valid JSON-LD
   - UCO ontology compliance (CASE 1.3.0)
   - Required properties present

2. Relationship Integrity
   - Valid references
   - Complete graph structure
   - No orphaned objects

## Example Mappings

### Input Example
```json
{
  "odata.metadata":"http://github.com/ICMEC/ProjectVic/DataModels/1.2.xml#Media","value":[
    {
      "odata.id":"Media(\"588cd1c0e48916d8e7403310402d0a68\")","MediaFiles@odata.navigationLinkUrl":"/Media(588cd1c0e48916d8e7403310402d0a68)/MediaFiles","MediaFiles":[
      {
        "Media@odata.navigationLinkUrl":"/MediaFiles(FileName='build2.art',FilePath='Like a Dragon Gaiden- The Man Who Erased His Name/Content/runtime/media/ylad8/data/artisan',MD5=588cd1c0e48916d8e7403310402d0a68)","MD5":"588cd1c0e48916d8e7403310402d0a68","FileName":"build2.art","FilePath":"Like a Dragon Gaiden- The Man Who Erased His Name/Content/runtime/media/ylad8/data/artisan"
      }
      ],"MediaID":0,"MD5":"588cd1c0e48916d8e7403310402d0a68","SHA1":"e65706b487c73e992bab2a50707a9fd8b0bd6866","Category":8,"MediaSize":"488"
    }
  ]
}
```

### Output Example
```json
{
  "@context": {
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
    "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
    "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
    "kb": "http://example.org/kb/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "kb:bundle-d1a404ee-ebfb-4826-9c91-0f5bb235e371",
      "@type": "uco-core:Bundle",
      "uco-core:objects": [
        {
          "@id": "kb:media-73e05c84-9bd1-443a-804b-bb332f7849f2",
          "@type": "uco-observable:File",
          "uco-observable:categories": 8,
          "uco-core:hasFacet": [
            {
              "@type": "uco-observable:FileFacet",
              "uco-observable:sizeInBytes": 488,
              "uco-observable:fileName": "build2.art",
              "uco-observable:filePath": "Like a Dragon Gaiden- The Man Who Erased His Name/Content/runtime/media/ylad8/data/artisan",
              "uco-observable:hash": [
                {
                  "@type": "uco-types:Hash",
                  "uco-types:hashMethod": {
                    "@type": "uco-vocabulary:HashNameVocab",
                    "@value": "MD5"
                  },
                  "uco-types:hashValue": {
                    "@type": "xsd:hexBinary",
                    "@value": "588cd1c0e48916d8e7403310402d0a68"
                  }
                },
                {
                  "@type": "uco-types:Hash",
                  "uco-types:hashMethod": {
                    "@type": "uco-vocabulary:HashNameVocab",
                    "@value": "SHA1"
                  },
                  "uco-types:hashValue": {
                    "@type": "xsd:hexBinary",
                    "@value": "e65706b487c73e992bab2a50707a9fd8b0bd6866"
                  }
                }
              ]
            }
          ]
        }
      ],
      "uco-core:object": [
        {
          "@type": "uco-core:Relationship",
          "uco-core:source": "kb:bundle-d1a404ee-ebfb-4826-9c91-0f5bb235e371",
          "uco-core:target": "kb:tool-9e1f5859-2f54-4408-b579-45dc4b012b1d",
          "uco-core:kindOfRelationship": "createdBy",
          "uco-core:isDirectional": true,
          "uco-core:objectCreatedTime": "2024-01-05T08:00:00Z",
          "uco-core:specVersion": "1.3.0"
        }
      ]
    }
  ]
}
```
