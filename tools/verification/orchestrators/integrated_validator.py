#!/usr/bin/env python3
"""
Integrated validator orchestrator.

Combines path validation and environment variable validation
with the existing verification framework.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.path_validator import PathValidator
from validators.env_validator import EnvValidator
from lib.logger import get_logger

logger = get_logger(__name__)


class IntegratedValidator:
    """Orchestrate integrated validation workflow."""
    
    def __init__(self):
        """Initialize validators."""
        self.path_validator = PathValidator()
        self.env_validator = EnvValidator()
    
    def validate_all(self, docs_dir: str) -> Dict[str, Any]:
        """
        Run all validations on documentation.
        
        Args:
            docs_dir: Path to documentation directory
            
        Returns:
            Combined validation results
        """
        logger.info(f"Starting integrated validation on {docs_dir}")
        
        results = {
            'docs_dir': docs_dir,
            'validations': {},
            'summary': {
                'total_errors': 0,
                'total_warnings': 0,
                'files_checked': 0,
                'is_valid': True
            }
        }
        
        # Run path validation
        logger.info("Running path validation...")
        path_results = self.path_validator.validate_directory(docs_dir, "*.md")
        results['validations']['paths'] = path_results
        results['summary']['total_errors'] += path_results['total_errors']
        results['summary']['files_checked'] = path_results['files_checked']
        
        if not path_results['is_valid']:
            results['summary']['is_valid'] = False
        
        # Run environment variable validation
        logger.info("Running environment variable validation...")
        env_results = self._validate_env_vars(docs_dir)
        results['validations']['env_vars'] = env_results
        results['summary']['total_warnings'] += env_results['total_warnings']
        
        logger.info(f"Validation complete: {results['summary']['total_errors']} errors, "
                   f"{results['summary']['total_warnings']} warnings")
        
        return results
    
    def _validate_env_vars(self, docs_dir: str) -> Dict[str, Any]:
        """
        Validate environment variables in all markdown files.
        
        Args:
            docs_dir: Path to documentation directory
            
        Returns:
            Environment variable validation results
        """
        import glob
        import os
        
        results = {
            'files_checked': 0,
            'total_warnings': 0,
            'results': []
        }
        
        # Find all markdown files
        pattern = os.path.join(docs_dir, '**', '*.md')
        files = glob.glob(pattern, recursive=True)
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                result = self.env_validator.validate_content(content, file_path)
                if result['warning_count'] > 0:
                    results['results'].append(result)
                    results['total_warnings'] += result['warning_count']
                
                results['files_checked'] += 1
            except Exception as e:
                logger.error(f"Error validating {file_path}: {e}")
        
        return results
    
    def print_results(self, results: Dict[str, Any]):
        """
        Print validation results to console.
        
        Args:
            results: Validation results
        """
        print("=" * 60)
        print("Integrated Validation Results")
        print("=" * 60)
        print()
        
        # Summary
        summary = results['summary']
        print(f"Files checked: {summary['files_checked']}")
        print(f"Total errors: {summary['total_errors']}")
        print(f"Total warnings: {summary['total_warnings']}")
        print()
        
        # Path validation results
        if results['validations']['paths']['total_errors'] > 0:
            print("Path Validation Errors:")
            print("-" * 60)
            for file_result in results['validations']['paths']['results']:
                if not file_result['is_valid']:
                    print(f"\n📄 {file_result['file']}")
                    for error in file_result['errors']:
                        print(f"  Line {error['line']}: {error['error_type']}")
                        print(f"  Found: {error['matched_text']}")
                        print(f"  Suggestion: {error['suggestion']}")
            print()
        
        # Environment variable validation results
        if results['validations']['env_vars']['total_warnings'] > 0:
            print("Environment Variable Warnings:")
            print("-" * 60)
            for file_result in results['validations']['env_vars']['results']:
                print(f"\n📄 {file_result['file']}")
                for warning in file_result['warnings']:
                    print(f"  Line {warning['line']}: {warning['var_name']}")
                    print(f"  Suggestion: {warning['suggestion']}")
            print()
        
        # Final status
        print("=" * 60)
        if summary['is_valid'] and summary['total_warnings'] == 0:
            print("✅ All validations passed!")
        elif summary['is_valid']:
            print(f"⚠️  Validation passed with {summary['total_warnings']} warnings")
        else:
            print(f"❌ Validation failed with {summary['total_errors']} errors")
        print("=" * 60)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run integrated validation')
    parser.add_argument('docs_dir', help='Path to documentation directory')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    
    args = parser.parse_args()
    
    validator = IntegratedValidator()
    results = validator.validate_all(args.docs_dir)
    
    if args.json:
        import json
        print(json.dumps(results, indent=2))
    else:
        validator.print_results(results)
    
    # Exit with appropriate code
    sys.exit(0 if results['summary']['is_valid'] else 1)


if __name__ == "__main__":
    main()
