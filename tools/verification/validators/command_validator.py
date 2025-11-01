"""Validate command options against implementation."""

from typing import Dict, Any, List

from lib.logger import get_logger

logger = get_logger(__name__)


class CommandOptionValidator:
    """Validate command options match implementation."""
    
    def validate(self, normalized_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate command options.
        
        Args:
            normalized_data: Normalized data from DataNormalizer
        
        Returns:
            List of validation errors
        """
        logger.info("Validating command options")
        
        errors = []
        
        for name, info in normalized_data.get("commands", {}).items():
            sources = set(info.get("sources", []))
            
            # Check if command is documented
            if "source" in sources and "doc" not in sources:
                errors.append({
                    "type": "undocumented_command",
                    "command": name,
                    "message": f"Command '{name}' exists in source but not documented",
                })
        
        return errors
