# NSRL-CAID to UCO Ontology Mapping

## Object Mappings

### Media Object
NSRL-CAID Media -> uco-observable:File
- MediaID -> @id (with prefix "kb:media-")
- facets:
  - type: "uco-observable:FileFacet"
    - observable:fileName: <FileName>
    - observable:filePath: <FilePath>
    - observable:sizeInBytes: <MediaSize>
    - observable:hash:
      - type: "uco-types:Hash"
        - types:hashMethod: "MD5"
        - types:hashValue: <MD5>
      - type: "uco-types:Hash"
        - types:hashMethod: "SHA1"
        - types:hashValue: <SHA1>
- Category -> categories

### MediaFiles Object
NSRL-CAID MediaFiles -> uco-observable:File
- facets:
  - type: "uco-observable:FileFacet"
    - observable:fileName: <FileName>
    - observable:filePath: <FilePath>
    - observable:hash:
      - type: "uco-types:Hash"
        - types:hashMethod: "MD5"
        - types:hashValue: <MD5>

## Property Mappings

### Hash Properties
Hash values are included within the FileFacet using observable:hash:
- MD5 hash values map to uco-types:Hash with:
  - types:hashMethod: "MD5"
  - types:hashValue: <value>
- SHA1 hash values map to uco-types:Hash with:
  - types:hashMethod: "SHA1"
  - types:hashValue: <value>

### File Properties
All file properties are contained within uco-observable:FileFacet:
- FilePath -> observable:filePath (string)
- FileName -> observable:fileName (string)
- MediaSize -> observable:sizeInBytes (integer)
- Hashes -> observable:hash

Optional properties available but not used in this mapping:
- observable:isDirectory (boolean)
- observable:accessedTime (dateTime)
- observable:metadataChangeTime (dateTime)
- observable:modifiedTime (dateTime)
- observable:observableCreatedTime (dateTime)
- observable:allocationStatus (string)
- observable:extension (string)

### Context
```json
{
"@context": {
"odata.metadata":"http://github.com/ICMEC/ProjectVic/DataModels/1.2.xml#Media",
"uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
"uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
"uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
"uco-vocabulary": "https://ontology.unifiedcyberontology.org/vocabulary/",
"kb": "http://example.org/kb/",
"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
"rdfs": "http://www.w3.org/2000/01/rdf-schema#",
"xsd": "http://www.w3.org/2001/XMLSchema#"
}
}
```

### Facets
- File objects use uco-observable:FileFacet for all file properties including hashes
- Hash values are included directly in the FileFacet using observable:hash property