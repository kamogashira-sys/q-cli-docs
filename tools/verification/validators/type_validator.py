"""Validate data types match between sources."""

from typing import Dict, Any, List

from lib.logger import get_logger

logger = get_logger(__name__)


class DataTypeValidator:
    """Validate data types match between source and schema."""
    
    # Type mapping between Rust and JSON Schema
    TYPE_MAPPING = {
        "String": "string",
        "bool": "boolean",
        "i32": "integer",
        "i64": "integer",
        "f32": "number",
        "f64": "number",
        "usize": "integer",
    }
    
    def validate(self, normalized_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate data types.
        
        Args:
            normalized_data: Normalized data from DataNormalizer
        
        Returns:
            List of validation errors
        """
        logger.info("Validating data types")
        
        errors = []
        
        for name, info in normalized_data.get("settings", {}).items():
            source_type = info.get("source_type")
            schema_type = info.get("schema_type")
            
            if source_type and schema_type:
                # Normalize source type
                normalized_source = self.TYPE_MAPPING.get(source_type, source_type)
                
                if normalized_source != schema_type:
                    errors.append({
                        "type": "type_mismatch",
                        "setting": name,
                        "message": f"Type mismatch for '{name}'",
                        "source_type": source_type,
                        "schema_type": schema_type,
                        "expected": normalized_source,
                    })
        
        return errors
