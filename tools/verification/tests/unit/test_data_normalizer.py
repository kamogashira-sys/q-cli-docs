"""Unit tests for data normalizer."""

import pytest

from normalizers.data_normalizer import DataNormalizer


@pytest.fixture
def sample_data():
    """Sample extracted data for testing."""
    return {
        "source": {
            "settings": {
                "model": {"type": "String", "file": "config.rs"},
                "temperature": {"type": "f32", "file": "config.rs"},
            },
            "enums": {
                "IndexType": {"variants": ["Fast", "Best"], "file": "types.rs"},
            },
            "commands": {
                "chat": {"enum": "Commands", "file": "cli.rs"},
            },
            "env_vars": {
                "Q_CONFIG": {"files": ["config.rs"]},
            },
        },
        "schema": {
            "properties": {
                "model": {"type": "string", "default": "claude-3", "file": "config.json"},
                "temperature": {"type": "number", "default": 0.7, "file": "config.json"},
            },
            "enums": {
                "indexType": {"values": ["Fast", "Best"], "file": "config.json"},
            },
        },
        "doc": {
            "settings": {
                "model": {"file": "config.md"},
            },
            "commands": {
                "chat": {"files": ["commands.md"]},
            },
            "env_vars": {
                "Q_CONFIG": {"files": ["env.md"]},
            },
        },
    }


def test_normalize_settings(sample_data):
    """Test settings normalization."""
    normalizer = DataNormalizer()
    result = normalizer.normalize_all(
        sample_data["source"],
        sample_data["schema"],
        sample_data["doc"],
    )
    
    settings = result["settings"]
    
    # Check model setting
    assert "model" in settings
    assert set(settings["model"]["sources"]) == {"source", "schema", "doc"}
    assert settings["model"]["source_type"] == "String"
    assert settings["model"]["schema_type"] == "string"
    
    # Check temperature setting
    assert "temperature" in settings
    assert set(settings["temperature"]["sources"]) == {"source", "schema"}


def test_normalize_enums(sample_data):
    """Test enum normalization."""
    normalizer = DataNormalizer()
    result = normalizer.normalize_all(
        sample_data["source"],
        sample_data["schema"],
        sample_data["doc"],
    )
    
    enums = result["enums"]
    
    # Check IndexType enum
    assert "IndexType" in enums
    assert "source" in enums["IndexType"]["sources"]
    assert enums["IndexType"]["source_variants"] == ["Fast", "Best"]


def test_normalize_commands(sample_data):
    """Test command normalization."""
    normalizer = DataNormalizer()
    result = normalizer.normalize_all(
        sample_data["source"],
        sample_data["schema"],
        sample_data["doc"],
    )
    
    commands = result["commands"]
    
    # Check chat command
    assert "chat" in commands
    assert set(commands["chat"]["sources"]) == {"source", "doc"}


def test_normalize_env_vars(sample_data):
    """Test environment variable normalization."""
    normalizer = DataNormalizer()
    result = normalizer.normalize_all(
        sample_data["source"],
        sample_data["schema"],
        sample_data["doc"],
    )
    
    env_vars = result["env_vars"]
    
    # Check Q_CONFIG
    assert "Q_CONFIG" in env_vars
    assert set(env_vars["Q_CONFIG"]["sources"]) == {"source", "doc"}


def test_normalize_empty_data():
    """Test normalization with empty data."""
    normalizer = DataNormalizer()
    result = normalizer.normalize_all({}, {}, {})
    
    assert result["settings"] == {}
    assert result["enums"] == {}
    assert result["commands"] == {}
    assert result["env_vars"] == {}
