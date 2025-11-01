"""Unit tests for diff detector."""

import pytest

from normalizers.diff_detector import DiffDetector


@pytest.fixture
def normalized_data():
    """Sample normalized data for testing."""
    return {
        "settings": {
            "model": {
                "name": "model",
                "sources": ["source", "schema", "doc"],
                "source_type": "String",
                "schema_type": "string",
            },
            "temperature": {
                "name": "temperature",
                "sources": ["source", "schema"],
                "source_type": "f32",
                "schema_type": "number",
            },
            "undocumented": {
                "name": "undocumented",
                "sources": ["source", "schema"],
            },
        },
        "enums": {
            "IndexType": {
                "name": "IndexType",
                "sources": ["source", "schema"],
                "source_variants": ["Fast", "Best"],
                "schema_values": ["Fast", "Best"],
            },
            "MismatchEnum": {
                "name": "MismatchEnum",
                "sources": ["source", "schema"],
                "source_variants": ["Value1", "Value2"],
                "schema_values": ["Value1", "Value3"],
            },
        },
    }


def test_find_missing_in_docs(normalized_data):
    """Test finding items missing in documentation."""
    detector = DiffDetector()
    result = detector.detect_all(normalized_data)
    
    missing = result["missing_in_docs"]
    
    # Should find temperature and undocumented
    assert len(missing) >= 2
    names = [item["name"] for item in missing]
    assert "temperature" in names
    assert "undocumented" in names


def test_find_enum_mismatches(normalized_data):
    """Test finding enum value mismatches."""
    detector = DiffDetector()
    result = detector.detect_all(normalized_data)
    
    mismatches = result["enum_mismatches"]
    
    # Should find MismatchEnum
    assert len(mismatches) == 1
    assert mismatches[0]["name"] == "MismatchEnum"
    assert "Value2" in mismatches[0]["missing_in_schema"]
    assert "Value3" in mismatches[0]["missing_in_source"]


def test_find_type_mismatches(normalized_data):
    """Test finding type mismatches."""
    # Add a type mismatch
    normalized_data["settings"]["bad_type"] = {
        "name": "bad_type",
        "sources": ["source", "schema"],
        "source_type": "String",
        "schema_type": "number",  # Mismatch!
    }
    
    detector = DiffDetector()
    result = detector.detect_all(normalized_data)
    
    mismatches = result["type_mismatches"]
    
    # Should find bad_type
    assert len(mismatches) == 1
    assert mismatches[0]["name"] == "bad_type"
    assert mismatches[0]["source_type"] == "String"
    assert mismatches[0]["schema_type"] == "number"


def test_no_differences():
    """Test with no differences."""
    data = {
        "settings": {
            "perfect": {
                "name": "perfect",
                "sources": ["source", "schema", "doc"],
                "source_type": "String",
                "schema_type": "string",
            },
        },
        "enums": {},
    }
    
    detector = DiffDetector()
    result = detector.detect_all(data)
    
    assert len(result["missing_in_docs"]) == 0
    assert len(result["enum_mismatches"]) == 0
    assert len(result["type_mismatches"]) == 0
