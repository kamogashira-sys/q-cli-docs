"""CLI interface for verification tool."""

import sys
from pathlib import Path
import click

from orchestrators.verification_orchestrator import VerificationOrchestrator


@click.command()
@click.option('--repo', type=click.Path(exists=True), required=True, help='Path to source repository')
@click.option('--schemas', type=click.Path(exists=True), required=True, help='Path to schema directory')
@click.option('--docs', type=click.Path(exists=True), required=True, help='Path to documentation directory')
@click.option('--format', type=click.Choice(['console', 'json']), default='console', help='Output format')
@click.option('--config', type=click.Path(exists=True), help='Path to configuration file')
def main(repo, schemas, docs, format, config):
    """Q CLI Documentation Verification Tool."""
    
    config_path = Path(config) if config else None
    orchestrator = VerificationOrchestrator(config_path)
    
    # Run verification
    results = orchestrator.verify(
        repo_path=Path(repo),
        schema_dir=Path(schemas),
        docs_dir=Path(docs),
    )
    
    # Generate report
    report = orchestrator.report(results, format=format)
    print(report)
    
    # Exit with appropriate code
    sys.exit(0 if results["status"] == "pass" else 1)


if __name__ == '__main__':
    main()
