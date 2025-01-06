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

import argparse
import datetime
from datetime import UTC
import hashlib
import json
import logging
import logging.handlers
import os
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path
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

@dataclass
class NSRLConverter:
    """Converts NSRL CAID JSON to UCO format."""
    
    input_path: Union[str, Path]
    output_dir: Union[str, Path]
    combine: bool = False
    validate: bool = False
    log_file: Optional[str] = None
    processed_files: Set[str] = field(default_factory=set)
    
    def __post_init__(self) -> None:
        """Initialize converter with logging and tool info."""
        self._setup_logging()
        self.tool_id = self._generate_tool_id()
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.debug(f"Initialized converter with tool_id: {self.tool_id}")

    def _setup_logging(self) -> None:
        """Configure logging with file and console handlers."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)  # Always set to DEBUG for class logger
        
        # Remove any existing handlers
        self.logger.handlers = []
        
        # Console handler
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)  # Set console handler to DEBUG
        console.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(console)
        
        # File handler if specified
        if self.log_file:
            file_handler = logging.handlers.RotatingFileHandler(
                self.log_file,
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)  # Set file handler to DEBUG
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
            ))
            self.logger.addHandler(file_handler)
            
        self.logger.debug("Logging initialized at DEBUG level")

    def _generate_tool_id(self) -> str:
        """Generate deterministic tool ID based on script contents."""
        with open(__file__, 'rb') as f:
            content = f.read()
        tool_hash = hashlib.sha256(content).hexdigest()
        return f"kb:tool-{tool_hash[:8]}"

    def _create_constant_objects(self) -> Dict:
        """Create constant UCO objects (Tool, Organization, Source)."""
        current_time = datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
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

    def _create_bundle(self) -> Dict:
        """Create UCO Bundle object with relationships."""
        bundle_id = f"kb:bundle-{uuid.uuid4()}"
        constant_objects = self._create_constant_objects()
        current_time = datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
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
                "uco-core:source": bundle_id,
                "uco-core:target": self.tool_id,
                "uco-core:kindOfRelationship": "createdBy",
                "uco-core:isDirectional": True,
                "uco-core:objectCreatedTime": current_time,
                "uco-core:specVersion": "1.3.0"
            },
            {
                "@id": f"kb:relationship-{uuid.uuid4()}",
                "@type": "uco-observable:ObservableRelationship",
                "uco-core:source": "kb:source-nsrl-caid",
                "uco-core:target": "kb:org-nist",
                "uco-core:kindOfRelationship": "managedBy",
                "uco-core:isDirectional": True,
                "uco-core:objectCreatedTime": current_time,
                "uco-core:specVersion": "1.3.0"
            }
        ])
        
        return bundle

    def _create_file_facet(self, media_file: MediaFile, media: Dict, facet_id: str) -> FileFacet:
        """Create UCO FileFacet from NSRL MediaFile and parent Media object."""
        current_time = datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        hashes = []
        
        # Add MD5 hash from MediaFile
        if "MD5" in media_file:
            hashes.append({
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
            hashes.append({
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

    def process_file(self, input_file: Path) -> Optional[Dict]:
        """Process single NSRL CAID JSON file to UCO format."""
        try:
            self.logger.info(f"Processing {input_file}")
            current_time = datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            
            self.logger.debug(f"Reading input file: {input_file}")
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.logger.debug(f"File content length: {len(content)} bytes")
                    try:
                        data = json.loads(content)
                        self.logger.debug("Successfully parsed JSON content")
                    except json.JSONDecodeError as je:
                        self.logger.error(f"JSON decode error at line {je.lineno}, column {je.colno}: {je.msg}")
                        self.logger.error(f"Error context: {content[max(0, je.pos-50):je.pos+50]}")
                        raise
            except Exception as e:
                self.logger.error(f"Error reading file: {str(e)}")
                raise
                
            if "value" not in data:
                self.logger.error("Invalid NSRL CAID JSON format: missing 'value' key")
                self.logger.debug(f"Available keys: {list(data.keys())}")
                raise ValueError("Invalid NSRL CAID JSON format: missing 'value' key")
                
            self.logger.debug(f"Found {len(data['value'])} media objects")
            
            bundle = self._create_bundle()
            input_id = f"kb:input-{uuid.uuid4()}"
            
            # Add input file object and its relationship
            input_file_obj = {
                "@id": input_id,
                "@type": "uco-observable:File",
                "uco-core:name": input_file.name,
                "uco-core:objectCreatedTime": current_time,
                "uco-core:specVersion": "1.3.0",
                "uco-core:hasFacet": [
                    {
                        "@id": f"kb:file-facet-{uuid.uuid4()}",
                        "@type": "uco-observable:FileFacet",
                        "uco-observable:fileName": input_file.name,
                        "uco-observable:extension": input_file.suffix[1:] if input_file.suffix else "",
                        "uco-observable:isDirectory": False,
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
                ]
            }
            
            input_relationship = {
                "@id": f"kb:relationship-{uuid.uuid4()}",
                "@type": "uco-observable:ObservableRelationship",
                "uco-core:source": input_id,
                "uco-core:target": "kb:source-nsrl-caid",
                "uco-core:kindOfRelationship": "derivedFrom",
                "uco-core:isDirectional": True,
                "uco-core:specVersion": "1.3.0",
                "uco-core:objectCreatedTime": current_time
            }
            
            bundle["uco-core:object"].extend([input_file_obj, input_relationship])
            
            # Process each media object
            for media in data["value"]:
                self.logger.debug(f"Processing media object with ID: {media.get('MediaID')}")
                
                file_obj = {
                    "@id": f"kb:media-{uuid.uuid4()}",
                    "@type": "uco-observable:File",
                    "uco-observable:categories": media.get("Category"),
                    "uco-core:specVersion": "1.3.0",
                    "uco-core:objectCreatedTime": current_time,
                    "uco-core:hasFacet": []
                }
                
                # Add file facets from MediaFiles
                for media_file in media.get("MediaFiles", []):
                    file_facet_id = f"kb:file-facet-{uuid.uuid4()}"
                    content_facet_id = f"kb:content-data-facet-{uuid.uuid4()}"
                    
                    file_obj["uco-core:hasFacet"].extend([
                        self._create_file_facet(media_file, media, file_facet_id),
                        self._create_content_data_facet(media_file, media, content_facet_id)
                    ])
                
                bundle["uco-core:object"].append(file_obj)
            
            result = {**UCO_CONTEXT, "@graph": [bundle]}
            
            if not self.combine:
                self._write_output(result, input_file)
            
            return result

        except Exception as e:
            self.logger.error(f"Error processing {input_file}: {str(e)}", exc_info=True)
            return None

    def _write_output(self, result: Dict, input_file: Path) -> None:
        """Write UCO output to file."""
        output_file = self.output_dir / f"uco-{input_file.stem}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        self.logger.info(f"Written output to {output_file}")

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
