"""Unit tests for documentation extractor."""

from pathlib import Path
import pytest

from extractors.doc_extractor import DocumentationExtractor
from lib.errors import ExtractionError


def test_init_with_valid_path(tmp_path):
    """Test initialization with valid docs directory."""
    extractor = DocumentationExtractor(tmp_path)
    assert extractor.docs_dir == tmp_path


def test_init_with_invalid_path():
    """Test initialization with invalid docs directory."""
    with pytest.raises(ExtractionError):
        DocumentationExtractor(Path("/nonexistent/path"))


def test_extract_settings(tmp_path):
    """Test settings extraction from documentation."""
    # Create test markdown file
    doc_file = tmp_path / "test.md"
    doc_file.write_text("""
        # Configuration
        
        | Setting | Type | Default |
        |---------|------|---------|
        | `chat.model` | string | claude-3 |
        | `telemetry.enabled` | boolean | true |
    """)
    
    extractor = DocumentationExtractor(tmp_path)
    result = extractor.extract_all()
    
    assert "chat.model" in result["settings"]
    assert "telemetry.enabled" in result["settings"]


def test_extract_env_vars(tmp_path):
    """Test environment variable extraction."""
    # Create test markdown file
    doc_file = tmp_path / "test.md"
    doc_file.write_text("""
        # Environment Variables
        
        - `Q_CLI_CONFIG_PATH`: Configuration file path
        - `AWS_PROFILE`: AWS profile name
    """)
    
    extractor = DocumentationExtractor(tmp_path)
    result = extractor.extract_all()
    
    assert "Q_CLI_CONFIG_PATH" in result["env_vars"]
    assert "AWS_PROFILE" in result["env_vars"]


def test_extract_commands(tmp_path):
    """Test command extraction."""
    # Create test markdown file
    doc_file = tmp_path / "test.md"
    doc_file.write_text("""
        # Commands
        
        - `q chat`: Start chat session
        - `q context`: Manage context
    """)
    
    extractor = DocumentationExtractor(tmp_path)
    result = extractor.extract_all()
    
    assert "chat" in result["commands"]
    assert "context" in result["commands"]


def test_extract_from_multiple_files(tmp_path):
    """Test extraction from multiple documentation files."""
    # Create multiple markdown files
    (tmp_path / "doc1.md").write_text("`Q_VAR_1` is used for...")
    (tmp_path / "doc2.md").write_text("`Q_VAR_2` is used for...")
    
    extractor = DocumentationExtractor(tmp_path)
    result = extractor.extract_all()
    
    assert "Q_VAR_1" in result["env_vars"]
    assert "Q_VAR_2" in result["env_vars"]


def test_skip_table_headers(tmp_path):
    """Test that table headers are skipped."""
    # Create test markdown file
    doc_file = tmp_path / "test.md"
    doc_file.write_text("""
        | Name | Type | Default |
        |------|------|---------|
        | `my_setting` | string | value |
    """)
    
    extractor = DocumentationExtractor(tmp_path)
    result = extractor.extract_all()
    
    # Headers should not be extracted
    assert "name" not in result["settings"]
    assert "Name" not in result["settings"]
    assert "type" not in result["settings"]
    assert "Type" not in result["settings"]
    assert "default" not in result["settings"]
    assert "Default" not in result["settings"]
    
    # Actual setting should be extracted (with backticks)
    assert "my_setting" in result["settings"]
