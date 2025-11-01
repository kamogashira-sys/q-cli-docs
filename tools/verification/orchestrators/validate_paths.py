#!/usr/bin/env python3
"""
CLI tool for validating file paths in Q CLI documentation.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.path_validator import PathValidator


def main():
    """Main entry point."""
    # Default to docs directory
    docs_dir = "/home/katoh/projects/q-cli-docs/docs"
    
    if len(sys.argv) > 1:
        docs_dir = sys.argv[1]
    
    if not os.path.exists(docs_dir):
        print(f"❌ Error: Directory not found: {docs_dir}")
        sys.exit(1)
    
    print("=" * 60)
    print("Q CLI Documentation Path Validation")
    print("=" * 60)
    print(f"\nValidating: {docs_dir}")
    print()
    
    validator = PathValidator()
    result = validator.validate_directory(docs_dir, "*.md")
    
    if result['is_valid']:
        print(f"✅ All paths are correct!")
        print(f"\nFiles checked: {result['files_checked']}")
        print(f"Total errors: {result['total_errors']}")
        sys.exit(0)
    else:
        print(f"❌ Found {result['total_errors']} path errors in {result['files_checked']} files")
        print()
        
        # Group errors by file
        files_with_errors = [r for r in result['results'] if not r['is_valid']]
        
        for file_result in files_with_errors:
            print(f"\n📄 {file_result['file']}")
            print(f"   Errors: {file_result['error_count']}")
            
            for error in file_result['errors']:
                print(f"\n   Line {error['line']}: {error['error_type']}")
                print(f"   Found: {error['matched_text']}")
                print(f"   Suggestion: {error['suggestion']}")
                if error.get('context'):
                    print(f"   Context: {error['context'][:80]}...")
        
        print()
        print("=" * 60)
        print(f"Summary: {result['total_errors']} errors found")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
