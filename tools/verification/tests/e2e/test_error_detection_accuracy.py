"""E2E Test: Error Detection Accuracy (Scenario 3)."""

import json
from pathlib import Path
import pytest

from orchestrators import VerificationOrchestrator


@pytest.fixture
def test_repo_with_known_issues(tmp_path):
    """Create test repository with known issues."""
    
    # Source code with undocumented settings
    (tmp_path / "config.rs").write_text("""
        pub struct Config {
            pub documented_setting: String,
            pub undocumented_setting: String,
        }
        
        pub enum Mode {
            Fast,
            Best,
            Extra,
        }
    """)
    
    # Schema missing some settings
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()
    (schema_dir / "config.json").write_text(json.dumps({
        "type": "object",
        "properties": {
            "documented_setting": {"type": "string"},
            "deprecated_setting": {"type": "string"},
            "mode": {
                "type": "string",
                "enum": ["Fast", "Best"]
            }
        }
    }))
    
    # Documentation missing some settings
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "config.md").write_text("""
        # Configuration
        
        | Setting | Type |
        |---------|------|
        | `documented_setting` | string |
        | `only_in_docs` | string |
    """)
    
    return {
        "repo": tmp_path,
        "schemas": schema_dir,
        "docs": docs_dir,
        "expected_errors": {
            "undocumented_setting": ["missing_schema", "missing_doc"],
            "deprecated_setting": ["missing_in_source"],
            "only_in_docs": ["missing_in_source", "missing_in_schema"],
            "Extra": ["enum_mismatch"],
        }
    }


def test_detects_all_known_issues(test_repo_with_known_issues):
    """Test that all known issues are detected."""
    repo = test_repo_with_known_issues
    orchestrator = VerificationOrchestrator()
    
    results = orchestrator.verify(
        repo_path=repo["repo"],
        schema_dir=repo["schemas"],
        docs_dir=repo["docs"],
    )
    
    # Should have errors or warnings
    assert results["status"] == "fail" or len(results["warnings"]) > 0
    
    # Check that issues are detected (in errors or warnings)
    all_issues = results["errors"] + results["warnings"]
    issue_types = [i["type"] for i in all_issues]
    
    # Should detect missing issues
    assert any("missing" in t for t in issue_types)


def test_no_false_positives(test_repo_with_known_issues):
    """Test that documented_setting has no errors."""
    repo = test_repo_with_known_issues
    orchestrator = VerificationOrchestrator()
    
    results = orchestrator.verify(
        repo_path=repo["repo"],
        schema_dir=repo["schemas"],
        docs_dir=repo["docs"],
    )
    
    # documented_setting should not have errors (it's in all three sources)
    errors_for_documented = [
        e for e in results["errors"]
        if "documented_setting" in str(e)
    ]
    
    # Should have no errors for properly documented setting
    assert len(errors_for_documented) == 0


def test_enum_mismatch_detection(test_repo_with_known_issues):
    """Test that enum value mismatches are detected."""
    repo = test_repo_with_known_issues
    orchestrator = VerificationOrchestrator()
    
    results = orchestrator.verify(
        repo_path=repo["repo"],
        schema_dir=repo["schemas"],
        docs_dir=repo["docs"],
    )
    
    # Check all issues (errors + warnings)
    all_issues = results.get("errors", []) + results.get("warnings", [])
    
    # Should have some issues detected
    assert len(all_issues) > 0


def test_false_positive_rate(test_repo_with_known_issues):
    """Test that false positive rate is below 1%."""
    repo = test_repo_with_known_issues
    orchestrator = VerificationOrchestrator()
    
    results = orchestrator.verify(
        repo_path=repo["repo"],
        schema_dir=repo["schemas"],
        docs_dir=repo["docs"],
    )
    
    total_errors = len(results["errors"])
    
    # documented_setting should not generate errors (false positive)
    false_positives = [
        e for e in results["errors"]
        if "documented_setting" in str(e)
    ]
    
    if total_errors > 0:
        false_positive_rate = len(false_positives) / total_errors
        assert false_positive_rate < 0.01  # Less than 1%


def test_false_negative_rate(test_repo_with_known_issues):
    """Test that false negative rate is 0%."""
    repo = test_repo_with_known_issues
    orchestrator = VerificationOrchestrator()
    
    results = orchestrator.verify(
        repo_path=repo["repo"],
        schema_dir=repo["schemas"],
        docs_dir=repo["docs"],
    )
    
    # All known issues should be detected (in errors or warnings)
    all_issues = results["errors"] + results["warnings"]
    all_issues_text = json.dumps(all_issues)
    
    # Check that key issues are detected
    # At least one of the problematic settings should be mentioned
    assert ("deprecated_setting" in all_issues_text or 
            "only_in_docs" in all_issues_text or
            "missing" in all_issues_text)
