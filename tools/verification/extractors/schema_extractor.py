"""Extract configuration from JSON schemas."""

from pathlib import Path
from typing import Dict, List, Any

from lib.errors import ExtractionError
from lib.logger import get_logger
from lib.utils import load_json

logger = get_logger(__name__)


class SchemaExtractor:
    """Extract configuration from JSON Schema files."""
    
    def __init__(self, schema_dir: Path):
        """
        Initialize schema extractor.
        
        Args:
            schema_dir: Path to schema directory
        """
        self.schema_dir = Path(schema_dir)
        if not self.schema_dir.exists():
            raise ExtractionError(
                f"Schema directory does not exist: {schema_dir}",
                details={"path": str(schema_dir)}
            )
    
    def extract_all(self) -> Dict[str, Any]:
        """
        Extract all configuration from schemas.
        
        Returns:
            Dictionary containing extracted configuration
        """
        logger.info("Extracting configuration from schemas")
        
        result = {
            "properties": {},
            "enums": {},
            "required": [],
        }
        
        # Find all JSON schema files
        schema_files = list(self.schema_dir.glob("**/*.json"))
        
        for schema_file in schema_files:
            schema = load_json(schema_file)
            self._extract_from_schema(schema, result, schema_file)
        
        logger.info(f"Extracted {len(result['properties'])} properties, "
                   f"{len(result['enums'])} enums from {len(schema_files)} schemas")
        
        return result
    
    def _extract_from_schema(
        self,
        schema: Dict[str, Any],
        result: Dict[str, Any],
        schema_file: Path,
        prefix: str = "",
    ) -> None:
        """
        Extract configuration from a single schema.
        
        Args:
            schema: JSON schema object
            result: Result dictionary to update
            schema_file: Path to schema file
            prefix: Property name prefix for nested properties
        """
        # Extract properties
        if "properties" in schema:
            for prop_name, prop_def in schema["properties"].items():
                full_name = f"{prefix}.{prop_name}" if prefix else prop_name
                
                result["properties"][full_name] = {
                    "type": prop_def.get("type"),
                    "description": prop_def.get("description"),
                    "default": prop_def.get("default"),
                    "enum": prop_def.get("enum"),
                    "file": str(schema_file.relative_to(self.schema_dir)),
                }
                
                # Extract enum values
                if "enum" in prop_def:
                    result["enums"][full_name] = {
                        "values": prop_def["enum"],
                        "file": str(schema_file.relative_to(self.schema_dir)),
                    }
                
                # Recursively process nested object properties
                if prop_def.get("type") == "object" and "properties" in prop_def:
                    self._extract_from_schema(prop_def, result, schema_file, full_name)
        
        # Extract required fields
        if "required" in schema:
            result["required"].extend(schema["required"])
        
        # Recursively process nested schemas
        if "definitions" in schema:
            for def_name, def_schema in schema["definitions"].items():
                self._extract_from_schema(def_schema, result, schema_file)
        
        if "$defs" in schema:
            for def_name, def_schema in schema["$defs"].items():
                self._extract_from_schema(def_schema, result, schema_file)
