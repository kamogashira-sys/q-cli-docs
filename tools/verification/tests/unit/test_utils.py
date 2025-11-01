"""Unit tests for utility functions."""

import json
from pathlib import Path

import pytest
import yaml

from lib.utils import (
    load_yaml,
    load_json,
    save_json,
    ensure_dir,
    get_file_hash,
)
from lib.errors import ConfigurationError


def test_load_yaml(tmp_path):
    """Test load_yaml function."""
    yaml_file = tmp_path / "test.yaml"
    data = {"key": "value", "number": 42}
    
    with open(yaml_file, "w") as f:
        yaml.dump(data, f)
    
    result = load_yaml(yaml_file)
    assert result == data


def test_load_yaml_invalid_file():
    """Test load_yaml with invalid file."""
    with pytest.raises(ConfigurationError):
        load_yaml(Path("/nonexistent/file.yaml"))


def test_load_json(tmp_path):
    """Test load_json function."""
    json_file = tmp_path / "test.json"
    data = {"key": "value", "number": 42}
    
    with open(json_file, "w") as f:
        json.dump(data, f)
    
    result = load_json(json_file)
    assert result == data


def test_load_json_invalid_file():
    """Test load_json with invalid file."""
    with pytest.raises(ConfigurationError):
        load_json(Path("/nonexistent/file.json"))


def test_save_json(tmp_path):
    """Test save_json function."""
    json_file = tmp_path / "output.json"
    data = {"key": "value", "number": 42}
    
    save_json(data, json_file)
    
    assert json_file.exists()
    with open(json_file) as f:
        result = json.load(f)
    assert result == data


def test_ensure_dir(tmp_path):
    """Test ensure_dir function."""
    new_dir = tmp_path / "nested" / "directory"
    ensure_dir(new_dir)
    assert new_dir.exists()
    assert new_dir.is_dir()


def test_ensure_dir_existing(tmp_path):
    """Test ensure_dir with existing directory."""
    ensure_dir(tmp_path)
    assert tmp_path.exists()


def test_get_file_hash(tmp_path):
    """Test get_file_hash function."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")
    
    hash_value = get_file_hash(test_file)
    assert len(hash_value) == 64  # SHA256 produces 64 hex characters
    
    # Same content should produce same hash
    hash_value2 = get_file_hash(test_file)
    assert hash_value == hash_value2


def test_get_file_hash_different_algorithm(tmp_path):
    """Test get_file_hash with different algorithm."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")
    
    md5_hash = get_file_hash(test_file, algorithm="md5")
    assert len(md5_hash) == 32  # MD5 produces 32 hex characters
