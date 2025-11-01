"""Detect differences between normalized data sources."""

from typing import Dict, Any, List, Set

from lib.logger import get_logger

logger = get_logger(__name__)


class DiffDetector:
    """Detect differences and inconsistencies in normalized data."""
    
    def detect_all(self, normalized_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Detect all differences in normalized data.
        
        Args:
            normalized_data: Normalized data from DataNormalizer
        
        Returns:
            Dictionary of detected differences by category
        """
        logger.info("Detecting differences in normalized data")
        
        return {
            "missing_in_source": self._find_missing_in_source(normalized_data),
            "missing_in_schema": self._find_missing_in_schema(normalized_data),
            "missing_in_docs": self._find_missing_in_docs(normalized_data),
            "enum_mismatches": self._find_enum_mismatches(normalized_data),
            "type_mismatches": self._find_type_mismatches(normalized_data),
        }
    
    def _find_missing_in_source(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find items documented but not in source code."""
        missing = []
        
        for name, info in data.get("settings", {}).items():
            if "source" not in info.get("sources", []):
                missing.append({
                    "type": "setting",
                    "name": name,
                    "found_in": info.get("sources", []),
                })
        
        return missing
    
    def _find_missing_in_schema(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find items in source but not in schema."""
        missing = []
        
        for name, info in data.get("settings", {}).items():
            if "schema" not in info.get("sources", []):
                missing.append({
                    "type": "setting",
                    "name": name,
                    "found_in": info.get("sources", []),
                })
        
        return missing
    
    def _find_missing_in_docs(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find items in source/schema but not documented."""
        missing = []
        
        for name, info in data.get("settings", {}).items():
            if "doc" not in info.get("sources", []):
                missing.append({
                    "type": "setting",
                    "name": name,
                    "found_in": info.get("sources", []),
                })
        
        return missing
    
    def _find_enum_mismatches(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find enum value mismatches between sources."""
        mismatches = []
        
        for name, info in data.get("enums", {}).items():
            source_variants = set(info.get("source_variants", []))
            schema_values = set(info.get("schema_values", []))
            
            if source_variants and schema_values:
                if source_variants != schema_values:
                    mismatches.append({
                        "type": "enum",
                        "name": name,
                        "source_values": sorted(source_variants),
                        "schema_values": sorted(schema_values),
                        "missing_in_schema": sorted(source_variants - schema_values),
                        "missing_in_source": sorted(schema_values - source_variants),
                    })
        
        return mismatches
    
    def _find_type_mismatches(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find type mismatches between source and schema."""
        mismatches = []
        
        # Type mapping between Rust and JSON Schema
        type_mapping = {
            "String": "string",
            "bool": "boolean",
            "i32": "integer",
            "i64": "integer",
            "f32": "number",
            "f64": "number",
            "usize": "integer",
        }
        
        for name, info in data.get("settings", {}).items():
            source_type = info.get("source_type")
            schema_type = info.get("schema_type")
            
            if source_type and schema_type:
                # Normalize source type
                normalized_source = type_mapping.get(source_type, source_type)
                
                if normalized_source != schema_type:
                    mismatches.append({
                        "type": "type",
                        "name": name,
                        "source_type": source_type,
                        "schema_type": schema_type,
                    })
        
        return mismatches
