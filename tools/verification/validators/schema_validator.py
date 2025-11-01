"""Validate schema completeness and correctness."""

from typing import Dict, Any, List

from lib.logger import get_logger

logger = get_logger(__name__)


class SchemaValidator:
    """Validate schema completeness."""
    
    def validate(self, normalized_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate schema completeness.
        
        Args:
            normalized_data: Normalized data from DataNormalizer
        
        Returns:
            List of validation errors
        """
        logger.info("Validating schema completeness")
        
        errors = []
        
        # Check for settings without schema
        for name, info in normalized_data.get("settings", {}).items():
            if "schema" not in info.get("sources", []):
                errors.append({
                    "type": "missing_schema_definition",
                    "setting": name,
                    "message": f"Setting '{name}' has no schema definition",
                })
        
        return errors
