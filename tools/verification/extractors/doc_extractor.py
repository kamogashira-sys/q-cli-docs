"""Extract configuration from documentation."""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional

from lib.errors import ExtractionError
from lib.logger import get_logger

logger = get_logger(__name__)


class DocumentationExtractor:
    """Extract configuration from Markdown documentation."""
    
    def __init__(self, docs_dir: Path):
        """
        Initialize documentation extractor.
        
        Args:
            docs_dir: Path to documentation directory
        """
        self.docs_dir = Path(docs_dir)
        if not self.docs_dir.exists():
            raise ExtractionError(
                f"Documentation directory does not exist: {docs_dir}",
                details={"path": str(docs_dir)}
            )
    
    def extract_all(self) -> Dict[str, Any]:
        """
        Extract all configuration from documentation.
        
        Returns:
            Dictionary containing extracted configuration
        """
        logger.info("Extracting configuration from documentation")
        
        result = {
            "settings": {},
            "env_vars": {},
            "commands": {},
            "values": {},
        }
        
        # Find all markdown files
        md_files = list(self.docs_dir.glob("**/*.md"))
        
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            self._extract_from_doc(content, result, md_file)
        
        logger.info(f"Extracted from {len(md_files)} documentation files")
        
        return result
    
    def _extract_from_doc(
        self,
        content: str,
        result: Dict[str, Any],
        doc_file: Path,
    ) -> None:
        """
        Extract configuration from a single document.
        
        Args:
            content: Document content
            result: Result dictionary to update
            doc_file: Path to document file
        """
        # Extract setting names from tables
        # Pattern: | `setting.name` | ... | (first column only)
        # Match lines that start with | and contain backticks in first column
        for line in content.split('\n'):
            # Skip table separator lines
            if '|---' in line or '|===' in line:
                continue
            
            # Extract first column value
            if line.strip().startswith('|'):
                columns = [col.strip() for col in line.split('|')]
                if len(columns) >= 3:  # At least | col1 | col2 |
                    first_col = columns[1]  # Index 0 is empty before first |
                    
                    # Extract setting name from backticks
                    match = re.match(r'`([a-zA-Z_]+(?:\.[a-zA-Z_]+)*)`', first_col)
                    if match:
                        setting_name = match.group(1)
                        
                        # Skip common markdown table headers (case-insensitive)
                        if setting_name.lower() in ['name', 'setting', 'type', 'default', 'description']:
                            continue
                        
                        # Store setting
                        result["settings"][setting_name] = {
                            "file": str(doc_file.relative_to(self.docs_dir)),
                        }
        
        # Extract environment variables
        # Pattern: Q_* or AWS_* (including numbers)
        env_pattern = r'`(Q_[A-Z0-9_]+|AWS_[A-Z0-9_]+)`'
        
        for match in re.finditer(env_pattern, content):
            env_var = match.group(1)
            
            if env_var not in result["env_vars"]:
                result["env_vars"][env_var] = {
                    "files": [],
                }
            
            file_rel = str(doc_file.relative_to(self.docs_dir))
            if file_rel not in result["env_vars"][env_var]["files"]:
                result["env_vars"][env_var]["files"].append(file_rel)
        
        # Extract command names
        # Pattern: q chat, q context, etc.
        command_pattern = r'`q\s+([a-z]+)`'
        
        for match in re.finditer(command_pattern, content):
            command = match.group(1)
            
            if command not in result["commands"]:
                result["commands"][command] = {
                    "files": [],
                }
            
            file_rel = str(doc_file.relative_to(self.docs_dir))
            if file_rel not in result["commands"][command]["files"]:
                result["commands"][command]["files"].append(file_rel)
        
        # Extract enum values from code blocks
        # Pattern: "value1" | "value2"
        enum_pattern = r'"([a-zA-Z][a-zA-Z0-9_-]*)"(?:\s*\|\s*"([a-zA-Z][a-zA-Z0-9_-]*)")*'
        
        for match in re.finditer(enum_pattern, content):
            values = [v for v in match.groups() if v]
            if len(values) > 1:  # Multiple values suggest enum
                key = "_".join(values[:2])  # Use first two values as key
                result["values"][key] = {
                    "values": values,
                    "file": str(doc_file.relative_to(self.docs_dir)),
                }
