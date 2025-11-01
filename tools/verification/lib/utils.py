"""Utility functions for verification tools."""

import hashlib
import json
from pathlib import Path
from typing import Any, Dict

import yaml

from .errors import ConfigurationError
from .logger import get_logger

logger = get_logger(__name__)


def load_yaml(file_path: Path) -> Dict[str, Any]:
    """
    Load YAML file.
    
    Args:
        file_path: Path to YAML file
    
    Returns:
        Parsed YAML content
    
    Raises:
        ConfigurationError: If file cannot be loaded
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise ConfigurationError(
            f"Failed to load YAML file: {file_path}",
            details={"error": str(e)}
        )


def load_json(file_path: Path) -> Dict[str, Any]:
    """
    Load JSON file.
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        Parsed JSON content
    
    Raises:
        ConfigurationError: If file cannot be loaded
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise ConfigurationError(
            f"Failed to load JSON file: {file_path}",
            details={"error": str(e)}
        )


def save_json(data: Dict[str, Any], file_path: Path, indent: int = 2) -> None:
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        file_path: Path to output file
        indent: JSON indentation level
    """
    ensure_dir(file_path.parent)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    logger.debug(f"Saved JSON to {file_path}")


def ensure_dir(dir_path: Path) -> None:
    """
    Ensure directory exists.
    
    Args:
        dir_path: Directory path to create
    """
    dir_path.mkdir(parents=True, exist_ok=True)


def get_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
    """
    Calculate file hash.
    
    Args:
        file_path: Path to file
        algorithm: Hash algorithm (md5, sha1, sha256)
    
    Returns:
        Hex digest of file hash
    """
    hash_obj = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()
