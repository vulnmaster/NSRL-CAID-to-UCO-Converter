import json
import os
from datetime import datetime
from typing import Dict, List
import uuid
from pathlib import Path
import argparse

class NSRLConverter:
    def __init__(self):
        self.context = {
            "@context": {
                "odata.metadata": "http://github.com/ICMEC/ProjectVic/DataModels/1.2.xml#Media",
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

    def generate_uuid(self) -> str:
        return str(uuid.uuid4())

    def create_file_facet(self, media_file: Dict) -> Dict:
        # Create single FileFacet with all properties
        facet = {
            "@type": "uco-observable:FileFacet",
            "observable:fileName": media_file.get("FileName"),
            "observable:filePath": media_file.get("FilePath"),
            "observable:sizeInBytes": int(media_file.get("MediaSize")) if media_file.get("MediaSize") else None,
            "observable:hash": []  # Initialize empty hash array
        }
        
        # Add hashes to the existing hash array
        if media_file.get("MD5"):
            facet["observable:hash"].append({
                "@type": "uco-types:Hash",
                "types:hashMethod": "MD5",
                "types:hashValue": media_file["MD5"]
            })
        if media_file.get("SHA1"):
            facet["observable:hash"].append({
                "@type": "uco-types:Hash",
                "types:hashMethod": "SHA1",
                "types:hashValue": media_file["SHA1"]
            })
        
        # Remove any None values and empty hash array
        return {k: v for k, v in facet.items() if v not in [None, []]}

    def convert_media_object(self, media: Dict) -> Dict:
        media_id = f"kb:media-{self.generate_uuid()}"
        
        # Create a single FileFacet combining all properties
        facet = {
            "@type": "uco-observable:FileFacet",
            "observable:sizeInBytes": int(media["MediaSize"]) if media.get("MediaSize") else None,
            "observable:fileName": media["MediaFiles"][0].get("FileName"),
            "observable:filePath": media["MediaFiles"][0].get("FilePath"),
            "observable:hash": []
        }
        
        # Add all hashes
        if media.get("MD5"):
            facet["observable:hash"].append({
                "@type": "uco-types:Hash",
                "types:hashMethod": "MD5",
                "types:hashValue": media["MD5"]
            })
        if media.get("SHA1"):
            facet["observable:hash"].append({
                "@type": "uco-types:Hash",
                "types:hashMethod": "SHA1",
                "types:hashValue": media["SHA1"]
            })
        
        # Create the main media object with single facet
        return {
            "@id": media_id,
            "@type": "uco-observable:File",
            "categories": media["Category"],
            "facets": [facet]
        }

    def convert_file(self, input_file: str) -> Dict:
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            case_objects = []
            for media in data["value"]:
                case_obj = self.convert_media_object(media)
                case_objects.append(case_obj)

            result = {
                **self.context,
                "@graph": case_objects
            }

            return result
        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}")
            return None

    def combine_results(self, output_dir: Path) -> Dict:
        """Combine all UCO JSON files in output directory into a single graph"""
        combined_graph = []
        
        for json_file in output_dir.glob('uco-*.json'):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                combined_graph.extend(data.get('@graph', []))
        
        return {
            "@context": self.context["@context"],
            "@graph": combined_graph
        }

def main():
    parser = argparse.ArgumentParser(description='Convert NSRL-CAID files to UCO format')
    parser.add_argument('input', help='Input file or directory path')
    parser.add_argument('-o', '--output', help='Output directory (default: output)', default='output')
    parser.add_argument('--combine', action='store_true', help='Combine all output files into a single JSON')
    args = parser.parse_args()

    converter = NSRLConverter()
    
    # Convert input path to Path object
    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)

    if input_path.is_file():
        input_files = [input_path]
    elif input_path.is_dir():
        # Get all JSON files in the directory
        input_files = list(input_path.glob('*.json'))
        print(f"Found {len(input_files)} JSON files in {input_path}")
    else:
        print(f"Error: {args.input} is not a valid file or directory")
        return

    for input_file in input_files:
        print(f"Processing {input_file}...")
        output_file = output_dir / f"uco-{input_file.name}"
        result = converter.convert_file(str(input_file))
        
        if result:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"Successfully converted {input_file} to {output_file}")
            except Exception as e:
                print(f"Error writing {output_file}: {str(e)}")
        else:
            print(f"Error processing {input_file}")

    # After processing, combine if requested
    if args.combine:
        combined_result = converter.combine_results(output_dir)
        combined_file = output_dir / "uco-combined.json"
        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump(combined_result, f, indent=2, ensure_ascii=False)
        print(f"Combined results written to {combined_file}")

if __name__ == "__main__":
    main()
