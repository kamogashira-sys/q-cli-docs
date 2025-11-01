"""Unit tests for validators."""

import pytest

from validators import (
    SettingValueValidator,
    EnumValueValidator,
    CommandOptionValidator,
    DataTypeValidator,
    SchemaValidator,
)


@pytest.fixture
def sample_normalized_data():
    """Sample normalized data for testing."""
    return {
        "settings": {
            "complete": {
                "name": "complete",
                "sources": ["source", "schema", "doc"],
                "source_type": "String",
                "schema_type": "string",
            },
            "no_schema": {
                "name": "no_schema",
                "sources": ["source", "doc"],
            },
            "no_doc": {
                "name": "no_doc",
                "sources": ["source", "schema"],
            },
            "type_mismatch": {
                "name": "type_mismatch",
                "sources": ["source", "schema"],
                "source_type": "String",
                "schema_type": "number",
            },
        },
        "enums": {
            "GoodEnum": {
                "name": "GoodEnum",
                "source_variants": ["A", "B"],
                "schema_values": ["A", "B"],
            },
            "BadEnum": {
                "name": "BadEnum",
                "source_variants": ["X", "Y"],
                "schema_values": ["X", "Z"],
            },
        },
        "commands": {
            "documented": {
                "name": "documented",
                "sources": ["source", "doc"],
            },
            "undocumented": {
                "name": "undocumented",
                "sources": ["source"],
            },
        },
    }


def test_setting_validator(sample_normalized_data):
    """Test setting value validator."""
    validator = SettingValueValidator()
    errors = validator.validate(sample_normalized_data)
    
    # Should find no_schema and no_doc
    assert len(errors) >= 2
    error_types = [e["type"] for e in errors]
    assert "missing_schema" in error_types
    assert "missing_doc" in error_types


def test_enum_validator(sample_normalized_data):
    """Test enum value validator."""
    validator = EnumValueValidator()
    errors = validator.validate(sample_normalized_data)
    
    # Should find BadEnum mismatch
    assert len(errors) == 1
    assert errors[0]["enum"] == "BadEnum"
    assert "Y" in errors[0]["missing_in_schema"]
    assert "Z" in errors[0]["missing_in_source"]


def test_command_validator(sample_normalized_data):
    """Test command option validator."""
    validator = CommandOptionValidator()
    errors = validator.validate(sample_normalized_data)
    
    # Should find undocumented command
    assert len(errors) == 1
    assert errors[0]["command"] == "undocumented"


def test_type_validator(sample_normalized_data):
    """Test data type validator."""
    validator = DataTypeValidator()
    errors = validator.validate(sample_normalized_data)
    
    # Should find type_mismatch
    assert len(errors) == 1
    assert errors[0]["setting"] == "type_mismatch"
    assert errors[0]["source_type"] == "String"
    assert errors[0]["schema_type"] == "number"


def test_schema_validator(sample_normalized_data):
    """Test schema validator."""
    validator = SchemaValidator()
    errors = validator.validate(sample_normalized_data)
    
    # Should find no_schema
    assert len(errors) == 1
    assert errors[0]["setting"] == "no_schema"


def test_all_validators_no_errors():
    """Test all validators with perfect data."""
    data = {
        "settings": {
            "perfect": {
                "name": "perfect",
                "sources": ["source", "schema", "doc"],
                "source_type": "String",
                "schema_type": "string",
            },
        },
        "enums": {
            "PerfectEnum": {
                "name": "PerfectEnum",
                "source_variants": ["A", "B"],
                "schema_values": ["A", "B"],
            },
        },
        "commands": {
            "perfect_cmd": {
                "name": "perfect_cmd",
                "sources": ["source", "doc"],
            },
        },
    }
    
    assert len(SettingValueValidator().validate(data)) == 0
    assert len(EnumValueValidator().validate(data)) == 0
    assert len(CommandOptionValidator().validate(data)) == 0
    assert len(DataTypeValidator().validate(data)) == 0
    assert len(SchemaValidator().validate(data)) == 0
