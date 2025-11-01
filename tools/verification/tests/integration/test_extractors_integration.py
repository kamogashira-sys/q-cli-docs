"""Integration tests for all extractors."""

import json
from pathlib import Path
import pytest

from extractors import SourceCodeExtractor, SchemaExtractor, DocumentationExtractor


@pytest.fixture
def test_repo(tmp_path):
    """Create a test repository structure."""
    # Create Rust source files
    config_rs = tmp_path / "config.rs"
    config_rs.write_text("""
        #[derive(Debug, Serialize, Deserialize)]
        pub struct ChatConfig {
            pub model: String,
            pub temperature: f32,
        }
        
        pub enum IndexType {
            Fast,
            Best,
        }
    """)
    
    # Create schema files
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()
    
    schema_file = schema_dir / "config.json"
    schema = {
        "type": "object",
        "properties": {
            "chat": {
                "type": "object",
                "properties": {
                    "model": {"type": "string", "default": "claude-3"},
                    "temperature": {"type": "number", "default": 0.7}
                }
            },
            "knowledge": {
                "type": "object",
                "properties": {
                    "indexType": {
                        "type": "string",
                        "enum": ["Fast", "Best"]
                    }
                }
            }
        }
    }
    schema_file.write_text(json.dumps(schema))
    
    # Create documentation files
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    
    doc_file = docs_dir / "config.md"
    doc_file.write_text("""
        # Configuration
        
        | Setting | Type | Default |
        |---------|------|---------|
        | `chat.model` | string | claude-3 |
        | `knowledge.indexType` | string | Fast |
        
        Environment variables:
        - `Q_CLI_CONFIG_PATH`: Configuration file path
        
        Commands:
        - `q chat`: Start chat session
    """)
    
    return {
        "repo": tmp_path,
        "schemas": schema_dir,
        "docs": docs_dir,
    }


def test_source_extractor_integration(test_repo):
    """Test source code extractor with real-like data."""
    extractor = SourceCodeExtractor(test_repo["repo"])
    result = extractor.extract_all()
    
    # Verify settings extraction
    assert "model" in result["settings"]
    assert "temperature" in result["settings"]
    
    # Verify enum extraction
    assert "IndexType" in result["enums"]
    assert "Fast" in result["enums"]["IndexType"]["variants"]
    assert "Best" in result["enums"]["IndexType"]["variants"]


def test_schema_extractor_integration(test_repo):
    """Test schema extractor with real-like data."""
    extractor = SchemaExtractor(test_repo["schemas"])
    result = extractor.extract_all()
    
    # Verify property extraction
    assert "chat" in result["properties"]
    assert "knowledge" in result["properties"]
    
    # Verify nested property extraction
    assert "chat.model" in result["properties"]
    assert "knowledge.indexType" in result["properties"]
    
    # Verify enum extraction
    assert "knowledge.indexType" in result["enums"]
    assert result["enums"]["knowledge.indexType"]["values"] == ["Fast", "Best"]


def test_doc_extractor_integration(test_repo):
    """Test documentation extractor with real-like data."""
    extractor = DocumentationExtractor(test_repo["docs"])
    result = extractor.extract_all()
    
    # Verify settings extraction
    assert "chat.model" in result["settings"]
    assert "knowledge.indexType" in result["settings"]
    
    # Verify env var extraction
    assert "Q_CLI_CONFIG_PATH" in result["env_vars"]
    
    # Verify command extraction
    assert "chat" in result["commands"]


def test_all_extractors_consistency(test_repo):
    """Test that all extractors produce consistent results."""
    source_extractor = SourceCodeExtractor(test_repo["repo"])
    schema_extractor = SchemaExtractor(test_repo["schemas"])
    doc_extractor = DocumentationExtractor(test_repo["docs"])
    
    source_result = source_extractor.extract_all()
    schema_result = schema_extractor.extract_all()
    doc_result = doc_extractor.extract_all()
    
    # Verify IndexType enum is found in all sources
    assert "IndexType" in source_result["enums"]
    assert "knowledge.indexType" in schema_result["enums"]
    assert "knowledge.indexType" in doc_result["settings"]
    
    # Verify enum values are consistent
    source_variants = source_result["enums"]["IndexType"]["variants"]
    schema_values = schema_result["enums"]["knowledge.indexType"]["values"]
    
    assert set(source_variants) == set(schema_values)
