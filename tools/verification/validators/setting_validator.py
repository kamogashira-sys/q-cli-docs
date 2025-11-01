"""Validate setting values against implementation."""

from typing import Dict, Any, List

from lib.logger import get_logger
from lib.errors import ValidationError

logger = get_logger(__name__)


class SettingValueValidator:
    """Validate setting values match implementation."""
    
    def validate(self, normalized_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate setting values.
        
        Args:
            normalized_data: Normalized data from DataNormalizer
        
        Returns:
            List of validation errors
        """
        logger.info("Validating setting values")
        
        errors = []
        
        for name, info in normalized_data.get("settings", {}).items():
            # Check if setting exists in all required sources
            sources = set(info.get("sources", []))
            
            if "source" in sources and "schema" not in sources:
                errors.append({
                    "type": "missing_schema",
                    "setting": name,
                    "message": f"Setting '{name}' exists in source but not in schema",
                })
            
            if "source" in sources and "doc" not in sources:
                errors.append({
                    "type": "missing_doc",
                    "setting": name,
                    "message": f"Setting '{name}' exists in source but not documented",
                })
        
        return errors
