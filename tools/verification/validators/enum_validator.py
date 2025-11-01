"""Validate enum values against implementation."""

from typing import Dict, Any, List

from lib.logger import get_logger

logger = get_logger(__name__)


class EnumValueValidator:
    """Validate enum values match between sources."""
    
    def validate(self, normalized_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate enum values.
        
        Args:
            normalized_data: Normalized data from DataNormalizer
        
        Returns:
            List of validation errors
        """
        logger.info("Validating enum values")
        
        errors = []
        
        for name, info in normalized_data.get("enums", {}).items():
            source_variants = set(info.get("source_variants", []))
            schema_values = set(info.get("schema_values", []))
            
            # Check if enum values match
            if source_variants and schema_values:
                if source_variants != schema_values:
                    missing_in_schema = source_variants - schema_values
                    missing_in_source = schema_values - source_variants
                    
                    errors.append({
                        "type": "enum_mismatch",
                        "enum": name,
                        "message": f"Enum '{name}' has mismatched values",
                        "missing_in_schema": sorted(missing_in_schema),
                        "missing_in_source": sorted(missing_in_source),
                    })
        
        return errors
