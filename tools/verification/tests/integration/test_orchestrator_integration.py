"""Integration tests for verification orchestrator."""

import json
from pathlib import Path
import pytest

from orchestrators import VerificationOrchestrator


@pytest.fixture
def test_repo(tmp_path):
    """Create a complete test repository."""
    # Create source files
    (tmp_path / "config.rs").write_text("""
        pub struct Config {
            pub model: String,
        }
        
        pub enum Mode {
            Fast,
            Best,
        }
    """)
    
    # Create schema files
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()
    (schema_dir / "config.json").write_text(json.dumps({
        "type": "object",
        "properties": {
            "model": {"type": "string", "default": "claude-3"},
            "mode": {"type": "string", "enum": ["Fast", "Best"]},
        },
    }))
    
    # Create documentation
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "config.md").write_text("""
        # Configuration
        
        | Setting | Type | Default |
        |---------|------|---------|
        | `model` | string | claude-3 |
    """)
    
    return {
        "repo": tmp_path,
        "schemas": schema_dir,
        "docs": docs_dir,
    }


def test_orchestrator_complete_workflow(test_repo):
    """Test complete verification workflow."""
    orchestrator = VerificationOrchestrator()
    
    results = orchestrator.verify(
        repo_path=test_repo["repo"],
        schema_dir=test_repo["schemas"],
        docs_dir=test_repo["docs"],
    )
    
    # Check results structure
    assert "status" in results
    assert "errors" in results
    assert "warnings" in results
    assert "metadata" in results
    
    # Check metadata
    assert "elapsed_time" in results["metadata"]
    assert "total_settings" in results["metadata"]


def test_orchestrator_console_report(test_repo):
    """Test console report generation."""
    orchestrator = VerificationOrchestrator()
    
    results = orchestrator.verify(
        repo_path=test_repo["repo"],
        schema_dir=test_repo["schemas"],
        docs_dir=test_repo["docs"],
    )
    
    report = orchestrator.report(results, format="console")
    
    assert "Verification Report" in report
    assert "Summary" in report


def test_orchestrator_json_report(test_repo):
    """Test JSON report generation."""
    orchestrator = VerificationOrchestrator()
    
    results = orchestrator.verify(
        repo_path=test_repo["repo"],
        schema_dir=test_repo["schemas"],
        docs_dir=test_repo["docs"],
    )
    
    report = orchestrator.report(results, format="json")
    data = json.loads(report)
    
    assert "status" in data
    assert "summary" in data
    assert "errors" in data
    assert "warnings" in data
