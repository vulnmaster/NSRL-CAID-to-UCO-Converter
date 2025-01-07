#!/usr/bin/env python3
"""
NSRL CAID to UCO Converter.

This tool converts NSRL CAID JSON files from ODATA format to UCO (Unified Cyber Ontology) 
compliant JSON-LD format. It maps NSRL CAID media objects to UCO observable:File objects 
with appropriate facets and relationships.

Copyright: Linux Foundation Cyber Domain Ontology Project
License: Apache 2.0
Author: Cyber Domain Ontology Developers: @vulnmaster
Version: 1.0.0
UCO Version: 1.3.0
Ontology Compliance: UCO Core, Observable, and Types
"""

# Debug statements to help diagnose import issues
import sys
print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Python path:", sys.path)

try:
    import json
    print("Successfully imported json module")
except ImportError as e:
    print("Failed to import json module:", str(e))
    print("Attempting to find json module in:", [p for p in sys.path if 'json' in str(p).lower()])
    sys.exit(1)

import argparse
import datetime
from datetime import timezone
import hashlib
import logging
import logging.handlers
import os
from pathlib import Path
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Union, TypedDict

# Type definitions for improved clarity
class HashInfo(TypedDict):
    """Type definition for hash information."""
    hashMethod: str
    hashValue: str

class FileFacet(TypedDict):
    """Type definition for UCO FileFacet."""
    fileName: str
    filePath: str
    hash: List[HashInfo]
    sizeInBytes: Optional[int]

class MediaFile(TypedDict):
    """Type definition for NSRL MediaFile."""
    FileName: str
    FilePath: str
    MD5: str
    SHA1: Optional[str]

# UCO Namespaces and Context
UCO_CONTEXT = {
    "@context": {
        "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
        "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
        "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
        "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
        "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "kb": "http://example.org/kb/"
    }
}

def generate_uuid():
    return str(uuid.uuid4())

def get_current_time():
    """Get current time in ISO format with UTC timezone."""
    return datetime.datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

@dataclass
class NSRLConverter:
    """Converts NSRL CAID JSON to UCO format."""
    
    input_path: Path
    output_dir: str = "output"
    log_file: Optional[str] = None
    combine: bool = False
    processed_files: Set[str] = field(default_factory=set)
    uuids: Dict[str, str] = field(default_factory=dict)
    logger: logging.Logger = field(init=False)
    
    def __post_init__(self) -> None:
        """Initialize converter with logging and output directory."""
        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.log_file) if self.log_file else logging.NullHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Logging initialized at DEBUG level")

        # Create output directory
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _generate_tool_id(self) -> str:
        """Generate deterministic tool ID based on script contents."""
        with open(__file__, 'rb') as f:
            content = f.read()
        tool_hash = hashlib.sha256(content).hexdigest()
        return f"kb:tool-{tool_hash[:8]}"

    def _create_constant_objects(self) -> Dict:
        """Create constant UCO objects (Tool, Organization, Source)."""
        current_time = datetime.datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        return {
            "tool": {
                "@id": self.tool_id,
                "@type": "uco-tool:ConfiguredTool",
                "uco-core:name": "nsrl_to_uco.py",
                "uco-core:description": "Converts NSRL CAID JSON to UCO format",
                "uco-tool:creator": {
                    "@id": "kb:org-linux-foundation",
                    "@type": "uco-identity:Organization",
                    "uco-core:name": "Linux Foundation Cyber Domain Ontology Project"
                },
                "uco-core:objectCreatedTime": current_time,
                "uco-core:startTime": current_time,
                "uco-core:endTime": current_time,
                "uco-core:specVersion": "1.3.0"
            },
            "organization": {
                "@id": "kb:org-nist",
                "@type": "uco-identity:Organization",
                "uco-core:name": "National Institute of Standards and Technology"
            },
            "source": {
                "@id": "kb:source-nsrl-caid",
                "@type": "uco-observable:URL",
                "uco-observable:value": "https://s3.amazonaws.com/rds.nsrl.nist.gov/RDS/CAID/current/NSRL-CAID-JSONs.zip"
            }
        }

    def _format_datetime(self, dt: datetime.datetime) -> str:
        """Format datetime in UCO-compliant format."""
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    def _create_bundle(self) -> Dict:
        """Create UCO Bundle object with relationships."""
        bundle_id = f"kb:bundle-{uuid.uuid4()}"
        constant_objects = self._create_constant_objects()
        current_time = self._format_datetime(datetime.datetime.now(timezone.utc))
        
        # Create the bundle with proper description
        bundle = {
            "@id": bundle_id,
            "@type": "uco-core:Bundle",
            "uco-core:description": "NSRL CAID media file reference data",
            "uco-core:object": [
                constant_objects["tool"],
                constant_objects["organization"],
                constant_objects["source"]
            ]
        }
        
        # Add relationships
        bundle["uco-core:object"].extend([
            {
                "@id": f"kb:relationship-{uuid.uuid4()}",
                "@type": "uco-observable:ObservableRelationship",
                "uco-core:source": {"@id": bundle_id},
                "uco-core:target": {"@id": self.tool_id},
                "uco-core:kindOfRelationship": "createdBy",
                "uco-core:isDirectional": True,
                "uco-core:objectCreatedTime": {
                    "@type": "xsd:dateTime",
                    "@value": current_time
                },
                "uco-core:specVersion": "1.3.0"
            },
            {
                "@id": f"kb:relationship-{uuid.uuid4()}",
                "@type": "uco-observable:ObservableRelationship",
                "uco-core:source": {"@id": "kb:source-nsrl-caid"},
                "uco-core:target": {"@id": "kb:org-nist"},
                "uco-core:kindOfRelationship": "managedBy",
                "uco-core:isDirectional": True,
                "uco-core:objectCreatedTime": {
                    "@type": "xsd:dateTime",
                    "@value": current_time
                },
                "uco-core:specVersion": "1.3.0"
            }
        ])
        
        return bundle

    def _create_file_facet(self, media_file: MediaFile, media: Dict, facet_id: str) -> FileFacet:
        """Create UCO FileFacet from NSRL MediaFile and parent Media object."""
        current_time = self._format_datetime(datetime.datetime.now(timezone.utc))
        hashes = []
        
        # Add MD5 hash from MediaFile
        if "MD5" in media_file:
            hash_id = f"kb:hash-{uuid.uuid4()}"
            hashes.append({
                "@id": hash_id,
                "@type": "uco-types:Hash",
                "uco-types:hashMethod": {
                    "@type": "uco-vocabulary:HashNameVocab",
                    "@value": "MD5"
                },
                "uco-types:hashValue": {
                    "@type": "xsd:hexBinary",
                    "@value": media_file["MD5"]
                }
            })
            
        # Add SHA1 hash from parent Media object if present
        if "SHA1" in media:
            hash_id = f"kb:hash-{uuid.uuid4()}"
            hashes.append({
                "@id": hash_id,
                "@type": "uco-types:Hash",
                "uco-types:hashMethod": {
                    "@type": "uco-vocabulary:HashNameVocab",
                    "@value": "SHA1"
                },
                "uco-types:hashValue": {
                    "@type": "xsd:hexBinary",
                    "@value": media["SHA1"]
                }
            })
            
        # Create facet with all available information
        facet = {
            "@id": facet_id,
            "@type": "uco-observable:FileFacet",
            "uco-observable:fileName": media_file["FileName"],
            "uco-observable:filePath": media_file["FilePath"],
            "uco-observable:extension": os.path.splitext(media_file["FileName"])[1][1:] if "." in media_file["FileName"] else "",
            "uco-observable:isDirectory": False,
            "uco-observable:hash": hashes,
            "uco-observable:observableCreatedTime": {
                "@type": "xsd:dateTime",
                "@value": current_time
            },
            "uco-observable:modifiedTime": {
                "@type": "xsd:dateTime",
                "@value": current_time
            },
            "uco-observable:accessedTime": {
                "@type": "xsd:dateTime",
                "@value": current_time
            }
        }
        
        # Add size if available
        if "MediaSize" in media:
            try:
                facet["uco-observable:sizeInBytes"] = int(media["MediaSize"])
            except ValueError:
                self.logger.warning(f"Invalid MediaSize value: {media['MediaSize']}")
                
        return facet

    def _create_content_data_facet(self, media_file: MediaFile, media: Dict, facet_id: str) -> Dict:
        """Create ContentDataFacet for additional file metadata."""
        facet = {
            "@id": facet_id,
            "@type": "uco-observable:ContentDataFacet",
            "uco-observable:byteOrder": {
                "@type": "uco-vocabulary:EndiannessTypeVocab",
                "@value": "Big-endian"
            }
        }
        
        # Add MIME type based on file extension
        ext = os.path.splitext(media_file["FileName"])[1][1:].lower()
        mime_types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "bmp": "image/bmp",
            "doc": "application/msword",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "pdf": "application/pdf",
            "txt": "text/plain",
            "html": "text/html",
            "htm": "text/html",
            "xml": "application/xml",
            "json": "application/json"
        }
        if ext in mime_types:
            facet["uco-observable:mimeType"] = mime_types[ext]
        
        if "MediaSize" in media:
            try:
                facet["uco-observable:sizeInBytes"] = int(media["MediaSize"])
            except ValueError:
                self.logger.warning(f"Invalid MediaSize value: {media['MediaSize']}")
        
        return facet

    def get_uuid_for_id(self, prefix, id_str):
        key = f"{prefix}-{id_str}"
        if key not in self.uuids:
            self.uuids[key] = str(uuid.uuid4())
        return self.uuids[key]

    def create_identifier(self, prefix, id_str):
        uuid_str = self.get_uuid_for_id(prefix, id_str)
        return f"kb:{prefix}-{id_str}-{uuid_str}"

    def process_file(self, input_file: Path) -> Optional[Dict]:
        """Process single NSRL CAID JSON file to UCO format."""
        try:
            self.logger.info(f"Processing {input_file}")
            with open(input_file, 'r') as f:
                data = json.load(f)

            # Handle both direct value array and odata.metadata format
            if isinstance(data, dict) and "value" in data:
                media_list = data["value"]
            else:
                self.logger.error("Invalid NSRL CAID JSON format: missing 'value' key")
                return None

            current_time = get_current_time()

            # Create identifiers with UUIDs
            bundle_id = self.create_identifier("bundle", "nsrl-caid")
            tool_id = self.create_identifier("tool", "nsrl-to-uco")
            nist_id = self.create_identifier("org", "nist")
            source_id = self.create_identifier("source", "nsrl-caid")
            action_id = self.create_identifier("action", "conversion")

            # Create the base objects
            objects = [
                {
                    "@id": bundle_id,
                    "@type": "uco-core:Bundle",
                    "uco-core:description": "NSRL CAID media file reference data converted to UCO format",
                    "uco-core:objectCreatedTime": {
                        "@type": "xsd:dateTime",
                        "@value": current_time
                    }
                },
                {
                    "@id": nist_id,
                    "@type": "uco-identity:Organization",
                    "uco-core:name": "National Institute of Standards and Technology",
                    "uco-core:description": "NIST maintains the NSRL CAID repository"
                },
                {
                    "@id": source_id,
                    "@type": "uco-observable:URL",
                    "uco-core:name": "NSRL CAID Repository",
                    "uco-core:description": "National Software Reference Library - Comprehensive Application Identifier",
                    "uco-observable:value": "https://s3.amazonaws.com/rds.nsrl.nist.gov/RDS/CAID/current/NSRL-CAID-JSONs.zip"
                },
                {
                    "@id": tool_id,
                    "@type": "uco-tool:ConfiguredTool",
                    "uco-core:name": "nsrl_to_uco.py",
                    "uco-core:description": "Tool to convert NSRL CAID JSON to UCO format",
                    "uco-core:version": "1.0.0",
                    "uco-core:objectCreatedTime": {
                        "@type": "xsd:dateTime",
                        "@value": current_time
                    }
                },
                {
                    "@id": action_id,
                    "@type": "uco-action:Action",
                    "uco-core:name": "NSRL CAID to UCO Conversion",
                    "uco-core:description": "Conversion of NSRL CAID data to UCO format",
                    "uco-action:startTime": {
                        "@type": "xsd:dateTime",
                        "@value": current_time
                    },
                    "uco-action:endTime": {
                        "@type": "xsd:dateTime",
                        "@value": current_time
                    },
                    "uco-action:performer": {"@id": tool_id},
                    "uco-action:environment": {
                        "@type": "uco-configuration:ConfigurationSetting",
                        "uco-configuration:itemName": "Python Environment",
                        "uco-configuration:itemValue": f"Python {sys.version}"
                    }
                }
            ]

            # Add relationships
            objects.extend([
                {
                    "@id": self.create_identifier("relationship", "source-maintainer"),
                    "@type": "uco-core:Relationship",
                    "uco-core:source": {"@id": source_id},
                    "uco-core:target": {"@id": nist_id},
                    "uco-core:kindOfRelationship": "maintainedBy",
                    "uco-core:isDirectional": True,
                    "uco-core:objectCreatedTime": {
                        "@type": "xsd:dateTime",
                        "@value": current_time
                    }
                },
                {
                    "@id": self.create_identifier("relationship", "action-source"),
                    "@type": "uco-core:Relationship",
                    "uco-core:source": {"@id": action_id},
                    "uco-core:target": {"@id": source_id},
                    "uco-core:kindOfRelationship": "inputSource",
                    "uco-core:isDirectional": True,
                    "uco-core:objectCreatedTime": {
                        "@type": "xsd:dateTime",
                        "@value": current_time
                    }
                }
            ])

            # Process each media item
            for media in media_list:
                media_id = media.get("MediaID", "unknown")
                file_id = self.create_identifier("file", str(media_id))

                # Create file object
                file_obj = {
                    "@id": file_id,
                    "@type": "uco-observable:File",
                    "uco-core:objectCreatedTime": {
                        "@type": "xsd:dateTime",
                        "@value": current_time
                    },
                    "uco-core:hasFacet": []
                }

                # Add file facet for each media file
                for media_file in media.get("MediaFiles", []):
                    facet_id = self.create_identifier("facet", f"{media_id}-{media_file.get('MD5', 'unknown')}")
                    hash_id = self.create_identifier("hash", media_file.get("MD5", "unknown"))
                    
                    # Create hash object
                    hash_obj = {
                        "@id": hash_id,
                        "@type": "uco-types:Hash",
                        "uco-types:hashMethod": {
                            "@type": "uco-vocabulary:HashNameVocab",
                            "@value": "MD5"
                        },
                        "uco-types:hashValue": {
                            "@type": "xsd:hexBinary",
                            "@value": media_file.get("MD5", "").upper()
                        }
                    }
                    
                    # Create file facet
                    file_facet = {
                        "@id": facet_id,
                        "@type": "uco-observable:FileFacet",
                        "uco-observable:fileName": media_file.get("FileName", ""),
                        "uco-observable:filePath": media_file.get("FilePath", ""),
                        "uco-observable:hash": [{"@id": hash_id}]
                    }
                    
                    # Add reference to facet in file object
                    file_obj["uco-core:hasFacet"].append({"@id": facet_id})
                    
                    # Add facet and hash objects to graph
                    objects.append(file_facet)
                    objects.append(hash_obj)

                # Add relationship between action and file
                objects.append({
                    "@id": self.create_identifier("relationship", f"action-file-{media_id}"),
                    "@type": "uco-core:Relationship",
                    "uco-core:source": {"@id": action_id},
                    "uco-core:target": {"@id": file_id},
                    "uco-core:kindOfRelationship": "outputFile",
                    "uco-core:isDirectional": True,
                    "uco-core:objectCreatedTime": {
                        "@type": "xsd:dateTime",
                        "@value": current_time
                    }
                })

                objects.append(file_obj)

            # Create the UCO object
            uco_object = {
                "@context": {
                    "@vocab": "https://ontology.unifiedcyberontology.org/uco/",
                    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
                    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
                    "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
                    "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
                    "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
                    "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
                    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
                    "uco-configuration": "https://ontology.unifiedcyberontology.org/uco/configuration/",
                    "kb": "http://example.org/kb/",
                    "xsd": "http://www.w3.org/2001/XMLSchema#"
                },
                "@graph": objects
            }

            # Write output file
            output_file = self.output_dir / f"uco-{input_file.stem}.json"
            with open(output_file, 'w') as f:
                json.dump(uco_object, f, indent=2)
            self.logger.info(f"Wrote output to {output_file}")

            return uco_object

        except Exception as e:
            self.logger.error(f"Error processing file {input_file}: {str(e)}")
            return None

    def process_input(self) -> None:
        """Process input path (file or directory)."""
        input_path = Path(self.input_path)
        combined_results = []
        processed_count = 0
        error_count = 0
        
        # Process files and always write individual outputs
        if input_path.is_file():
            result = self.process_file(input_path)
            if result:
                processed_count += 1
                if self.combine:
                    combined_results.append(result["@graph"][0])
            else:
                error_count += 1
                
        elif input_path.is_dir():
            for file_path in input_path.glob("*.json"):
                result = self.process_file(file_path)
                if result:
                    # Always write individual output
                    self._write_output(result, file_path)
                    processed_count += 1
                    if self.combine:
                        combined_results.append(result["@graph"][0])
                else:
                    error_count += 1
                    
        # If combine flag is set, create additional combined file
        if self.combine and combined_results:
            combined = {
                **UCO_CONTEXT,
                "@graph": combined_results
            }
            output_file = self.output_dir / "uco-combined.json"
            with open(output_file, 'w') as f:
                json.dump(combined, f, indent=2)
            self.logger.info(f"Written combined output to {output_file}")
            
        self.logger.info(f"Processing complete. Processed: {processed_count}, Errors: {error_count}")

def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert NSRL CAID JSON to UCO format"
    )
    parser.add_argument(
        "input",
        help="Input JSON file or directory"
    )
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Output directory (default: output)"
    )
    parser.add_argument(
        "--combine",
        action="store_true",
        help="Combine all output into single graph"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate output against UCO schema"
    )
    parser.add_argument(
        "--log-file",
        help="Log file path (optional)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    # Configure root logger first
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
    
    # Remove any existing handlers
    root_logger.handlers = []
    
    # Add console handler to root logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if args.debug else logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    root_logger.addHandler(console_handler)
    
    if args.debug:
        root_logger.debug("Debug logging enabled")
    
    converter = NSRLConverter(
        args.input,
        args.output,
        args.combine,
        args.validate,
        args.log_file
    )
    converter.process_input()

if __name__ == "__main__":
    main()
