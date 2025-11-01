"""E2E Test: Error Handling (Scenario 5)."""

import json
from pathlib import Path
import pytest

from orchestrators import VerificationOrchestrator
from lib.errors import ExtractionError


def test_nonexistent_repo_path(tmp_path):
    """Test handling of nonexistent repository path."""
    orchestrator = VerificationOrchestrator()
    
    # Create valid schema and docs dirs
    schema_dir = tmp_path / "schemas"
    docs_dir = tmp_path / "docs"
    schema_dir.mkdir()
    docs_dir.mkdir()
    
    with pytest.raises(ExtractionError) as exc_info:
        orchestrator.verify(
            repo_path=Path("/nonexistent/path"),
            schema_dir=schema_dir,
            docs_dir=docs_dir,
        )
    
    assert "does not exist" in str(exc_info.value)


def test_nonexistent_schema_path(tmp_path):
    """Test handling of nonexistent schema path."""
    orchestrator = VerificationOrchestrator()
    
    # Create valid repo and docs dirs
    repo_dir = tmp_path / "repo"
    docs_dir = tmp_path / "docs"
    repo_dir.mkdir()
    docs_dir.mkdir()
    
    with pytest.raises(ExtractionError) as exc_info:
        orchestrator.verify(
            repo_path=repo_dir,
            schema_dir=Path("/nonexistent/schemas"),
            docs_dir=docs_dir,
        )
    
    assert "does not exist" in str(exc_info.value)


def test_nonexistent_docs_path(tmp_path):
    """Test handling of nonexistent docs path."""
    orchestrator = VerificationOrchestrator()
    
    # Create valid repo and schema dirs
    repo_dir = tmp_path / "repo"
    schema_dir = tmp_path / "schemas"
    repo_dir.mkdir()
    schema_dir.mkdir()
    
    with pytest.raises(ExtractionError) as exc_info:
        orchestrator.verify(
            repo_path=repo_dir,
            schema_dir=schema_dir,
            docs_dir=Path("/nonexistent/docs"),
        )
    
    assert "does not exist" in str(exc_info.value)


def test_empty_directories(tmp_path):
    """Test handling of empty directories."""
    empty_repo = tmp_path / "empty_repo"
    empty_schemas = tmp_path / "empty_schemas"
    empty_docs = tmp_path / "empty_docs"
    
    empty_repo.mkdir()
    empty_schemas.mkdir()
    empty_docs.mkdir()
    
    orchestrator = VerificationOrchestrator()
    
    # Should not crash with empty directories
    results = orchestrator.verify(
        repo_path=empty_repo,
        schema_dir=empty_schemas,
        docs_dir=empty_docs,
    )
    
    # Should return valid results
    assert "status" in results
    assert "errors" in results
    assert "warnings" in results
    
    # Should have no errors (nothing to validate)
    assert len(results["errors"]) == 0


def test_invalid_json_schema(tmp_path):
    """Test handling of invalid JSON schema files."""
    repo = tmp_path / "repo"
    schemas = tmp_path / "schemas"
    docs = tmp_path / "docs"
    
    repo.mkdir()
    schemas.mkdir()
    docs.mkdir()
    
    # Create invalid JSON file
    (schemas / "broken.json").write_text("invalid json {{{")
    
    # Create valid JSON file
    (schemas / "valid.json").write_text(json.dumps({
        "type": "object",
        "properties": {
            "test": {"type": "string"}
        }
    }))
    
    orchestrator = VerificationOrchestrator()
    
    # Should raise ConfigurationError for invalid JSON
    from lib.errors import ConfigurationError
    with pytest.raises(ConfigurationError):
        results = orchestrator.verify(
            repo_path=repo,
            schema_dir=schemas,
            docs_dir=docs,
        )


def test_unicode_in_files(tmp_path):
    """Test handling of Unicode characters in files."""
    repo = tmp_path / "repo"
    schemas = tmp_path / "schemas"
    docs = tmp_path / "docs"
    
    repo.mkdir()
    schemas.mkdir()
    docs.mkdir()
    
    # Create files with Unicode
    (repo / "config.rs").write_text("""
        pub struct Config {
            pub 設定: String,  // Japanese
            pub configuración: String,  // Spanish
        }
    """, encoding="utf-8")
    
    (docs / "config.md").write_text("""
        # 設定ガイド
        
        | Setting | Type |
        |---------|------|
        | `設定` | string |
    """, encoding="utf-8")
    
    orchestrator = VerificationOrchestrator()
    
    # Should handle Unicode without crashing
    results = orchestrator.verify(
        repo_path=repo,
        schema_dir=schemas,
        docs_dir=docs,
    )
    
    assert "status" in results


def test_large_files(tmp_path):
    """Test handling of large files."""
    repo = tmp_path / "repo"
    schemas = tmp_path / "schemas"
    docs = tmp_path / "docs"
    
    repo.mkdir()
    schemas.mkdir()
    docs.mkdir()
    
    # Create large source file (10,000 lines)
    large_content = "\n".join([
        f"pub struct Config{i} {{ pub field{i}: String }}"
        for i in range(10000)
    ])
    (repo / "large.rs").write_text(large_content)
    
    orchestrator = VerificationOrchestrator()
    
    # Should handle large files without crashing
    results = orchestrator.verify(
        repo_path=repo,
        schema_dir=schemas,
        docs_dir=docs,
    )
    
    assert "status" in results
    assert "elapsed_time" in results["metadata"]
