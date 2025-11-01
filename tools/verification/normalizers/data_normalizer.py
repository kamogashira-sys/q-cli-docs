"""Normalize extracted data into unified format."""

from typing import Dict, Any, List
from pathlib import Path

from lib.logger import get_logger

logger = get_logger(__name__)


class DataNormalizer:
    """Normalize data from different sources into unified format."""
    
    def normalize_all(
        self,
        source_data: Dict[str, Any],
        schema_data: Dict[str, Any],
        doc_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Normalize all extracted data.
        
        Args:
            source_data: Data from source code extractor
            schema_data: Data from schema extractor
            doc_data: Data from documentation extractor
        
        Returns:
            Normalized data in unified format
        """
        logger.info("Normalizing extracted data")
        
        return {
            "settings": self._normalize_settings(source_data, schema_data, doc_data),
            "enums": self._normalize_enums(source_data, schema_data),
            "commands": self._normalize_commands(source_data, doc_data),
            "env_vars": self._normalize_env_vars(source_data, doc_data),
        }
    
    def _normalize_settings(
        self,
        source_data: Dict[str, Any],
        schema_data: Dict[str, Any],
        doc_data: Dict[str, Any],
    ) -> Dict[str, Dict[str, Any]]:
        """Normalize settings from all sources."""
        normalized = {}
        
        # From source code
        for name, info in source_data.get("settings", {}).items():
            normalized[name] = {
                "name": name,
                "sources": ["source"],
                "source_type": info.get("type"),
                "source_file": info.get("file"),
            }
        
        # From schema
        for name, info in schema_data.get("properties", {}).items():
            if name not in normalized:
                normalized[name] = {
                    "name": name,
                    "sources": [],
                }
            normalized[name]["sources"].append("schema")
            normalized[name]["schema_type"] = info.get("type")
            normalized[name]["schema_default"] = info.get("default")
            normalized[name]["schema_file"] = info.get("file")
        
        # From documentation
        for name, info in doc_data.get("settings", {}).items():
            if name not in normalized:
                normalized[name] = {
                    "name": name,
                    "sources": [],
                }
            normalized[name]["sources"].append("doc")
            normalized[name]["doc_file"] = info.get("file")
        
        return normalized
    
    def _normalize_enums(
        self,
        source_data: Dict[str, Any],
        schema_data: Dict[str, Any],
    ) -> Dict[str, Dict[str, Any]]:
        """Normalize enums from source and schema."""
        normalized = {}
        
        # From source code
        for name, info in source_data.get("enums", {}).items():
            normalized[name] = {
                "name": name,
                "sources": ["source"],
                "source_variants": info.get("variants", []),
                "source_file": info.get("file"),
            }
        
        # From schema
        for name, info in schema_data.get("enums", {}).items():
            if name not in normalized:
                normalized[name] = {
                    "name": name,
                    "sources": [],
                }
            normalized[name]["sources"].append("schema")
            normalized[name]["schema_values"] = info.get("values", [])
            normalized[name]["schema_file"] = info.get("file")
        
        return normalized
    
    def _normalize_commands(
        self,
        source_data: Dict[str, Any],
        doc_data: Dict[str, Any],
    ) -> Dict[str, Dict[str, Any]]:
        """Normalize commands from source and documentation."""
        normalized = {}
        
        # From source code
        for name, info in source_data.get("commands", {}).items():
            normalized[name] = {
                "name": name,
                "sources": ["source"],
                "source_enum": info.get("enum"),
                "source_file": info.get("file"),
            }
        
        # From documentation
        for name, info in doc_data.get("commands", {}).items():
            if name not in normalized:
                normalized[name] = {
                    "name": name,
                    "sources": [],
                }
            normalized[name]["sources"].append("doc")
            normalized[name]["doc_files"] = info.get("files", [])
        
        return normalized
    
    def _normalize_env_vars(
        self,
        source_data: Dict[str, Any],
        doc_data: Dict[str, Any],
    ) -> Dict[str, Dict[str, Any]]:
        """Normalize environment variables from source and documentation."""
        normalized = {}
        
        # From source code
        for name, info in source_data.get("env_vars", {}).items():
            normalized[name] = {
                "name": name,
                "sources": ["source"],
                "source_files": info.get("files", []),
            }
        
        # From documentation
        for name, info in doc_data.get("env_vars", {}).items():
            if name not in normalized:
                normalized[name] = {
                    "name": name,
                    "sources": [],
                }
            normalized[name]["sources"].append("doc")
            normalized[name]["doc_files"] = info.get("files", [])
        
        return normalized
