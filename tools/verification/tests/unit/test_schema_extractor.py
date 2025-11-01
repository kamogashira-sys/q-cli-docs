"""Unit tests for schema extractor."""

import json
from pathlib import Path
import pytest

from extractors.schema_extractor import SchemaExtractor
from lib.errors import ExtractionError


def test_init_with_valid_path(tmp_path):
    """Test initialization with valid schema directory."""
    extractor = SchemaExtractor(tmp_path)
    assert extractor.schema_dir == tmp_path


def test_init_with_invalid_path():
    """Test initialization with invalid schema directory."""
    with pytest.raises(ExtractionError):
        SchemaExtractor(Path("/nonexistent/path"))


def test_extract_properties(tmp_path):
    """Test property extraction from schema."""
    # Create test schema
    schema_file = tmp_path / "test.json"
    schema = {
        "type": "object",
        "properties": {
            "setting1": {
                "type": "string",
                "description": "Test setting",
                "default": "value"
            },
            "setting2": {
                "type": "boolean",
                "default": True
            }
        }
    }
    schema_file.write_text(json.dumps(schema))
    
    extractor = SchemaExtractor(tmp_path)
    result = extractor.extract_all()
    
    assert "setting1" in result["properties"]
    assert "setting2" in result["properties"]
    assert result["properties"]["setting1"]["type"] == "string"
    assert result["properties"]["setting2"]["type"] == "boolean"


def test_extract_enums(tmp_path):
    """Test enum extraction from schema."""
    # Create test schema with enum
    schema_file = tmp_path / "test.json"
    schema = {
        "type": "object",
        "properties": {
            "mode": {
                "type": "string",
                "enum": ["Fast", "Best"]
            }
        }
    }
    schema_file.write_text(json.dumps(schema))
    
    extractor = SchemaExtractor(tmp_path)
    result = extractor.extract_all()
    
    assert "mode" in result["enums"]
    assert result["enums"]["mode"]["values"] == ["Fast", "Best"]


def test_extract_required(tmp_path):
    """Test required field extraction."""
    # Create test schema
    schema_file = tmp_path / "test.json"
    schema = {
        "type": "object",
        "properties": {
            "required_field": {"type": "string"}
        },
        "required": ["required_field"]
    }
    schema_file.write_text(json.dumps(schema))
    
    extractor = SchemaExtractor(tmp_path)
    result = extractor.extract_all()
    
    assert "required_field" in result["required"]


def test_extract_nested_schemas(tmp_path):
    """Test extraction from nested schemas."""
    # Create test schema with definitions
    schema_file = tmp_path / "test.json"
    schema = {
        "type": "object",
        "definitions": {
            "NestedType": {
                "type": "object",
                "properties": {
                    "nested_prop": {"type": "string"}
                }
            }
        }
    }
    schema_file.write_text(json.dumps(schema))
    
    extractor = SchemaExtractor(tmp_path)
    result = extractor.extract_all()
    
    assert "nested_prop" in result["properties"]
