#!/usr/bin/env python3
"""
Certificate generation CLI tool
Usage:
    python generate.py              - Generate all certificates
    python generate.py --clear      - Clear all generated certificates
    python generate.py --clear-gen  - Clear and then generate
"""

import json
import sys
from app.generator import generate_certificate, clear_output_directory

DATA_PATH = "data/input.json"


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "--clear":
            print("Clearing output directory...")
            result = clear_output_directory()
            print(f"✓ {result['message']}")
            return
        
        elif command == "--clear-gen":
            print("Clearing output directory...")
            clear_result = clear_output_directory()
            print(f"✓ {clear_result['message']}")
            print("\nGenerating certificates...\n")
            generate_certificates()
            return
        
        elif command in ["-h", "--help"]:
            print(__doc__)
            return
        
        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            return
    
    # Default: generate certificates
    generate_certificates()


def generate_certificates():
    """Load data and generate all certificates"""
    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {DATA_PATH} not found!")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: {DATA_PATH} is not valid JSON!")
        return
    
    if not data:
        print("❌ No certificate data found in input.json")
        return
    
    print(f"Generating {len(data)} certificate(s)...\n")
    
    results = []
    for i, entry in enumerate(data, 1):
        try:
            path = generate_certificate(entry)
            results.append({
                "name": entry["name"],
                "sport": entry["sport"],
                "position": entry["position"],
                "file": path
            })
            print(f"✓ [{i}/{len(data)}] {entry['name']} ({entry['sport']}) - {path}")
        except KeyError as e:
            print(f"❌ [{i}/{len(data)}] Missing field {e} in entry: {entry.get('name', 'Unknown')}")
        except Exception as e:
            print(f"❌ [{i}/{len(data)}] Error generating certificate for {entry.get('name', 'Unknown')}: {str(e)}")
    
    print(f"\n✓ Successfully generated {len(results)}/{len(data)} certificate(s)")
    print(f"📁 Generated files are in the 'output/' directory organized by sport")


if __name__ == "__main__":
    main()
