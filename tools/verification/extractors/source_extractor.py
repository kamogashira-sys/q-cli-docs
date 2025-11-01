"""Extract configuration from Rust source code."""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional

from lib.errors import ExtractionError
from lib.logger import get_logger

logger = get_logger(__name__)


class SourceCodeExtractor:
    """Extract configuration values from Rust source code."""
    
    def __init__(self, repo_path: Path):
        """
        Initialize source code extractor.
        
        Args:
            repo_path: Path to Q CLI repository
        """
        self.repo_path = Path(repo_path)
        if not self.repo_path.exists():
            raise ExtractionError(
                f"Repository path does not exist: {repo_path}",
                details={"path": str(repo_path)}
            )
    
    def extract_all(self) -> Dict[str, Any]:
        """
        Extract all configuration from source code.
        
        Returns:
            Dictionary containing extracted configuration
        """
        logger.info("Extracting configuration from source code")
        
        result = {
            "settings": self.extract_settings(),
            "enums": self.extract_enums(),
            "commands": self.extract_commands(),
            "env_vars": self.extract_env_vars(),
        }
        
        logger.info(f"Extracted {len(result['settings'])} settings, "
                   f"{len(result['enums'])} enums, "
                   f"{len(result['commands'])} commands, "
                   f"{len(result['env_vars'])} env vars")
        
        return result
    
    def extract_settings(self) -> Dict[str, Dict[str, Any]]:
        """
        Extract setting definitions from source code.
        
        Returns:
            Dictionary mapping setting names to their properties
        """
        settings = {}
        
        # Search for Config struct definitions
        config_files = self._find_files("**/config*.rs")
        
        for file_path in config_files:
            content = file_path.read_text(encoding="utf-8")
            
            # Extract struct fields with serde attributes
            struct_pattern = r'#\[derive\([^\]]*\)\]\s*pub struct (\w+Config)\s*\{([^}]+)\}'
            
            for match in re.finditer(struct_pattern, content, re.MULTILINE | re.DOTALL):
                struct_name = match.group(1)
                fields_text = match.group(2)
                
                # Extract individual fields
                field_pattern = r'pub\s+(\w+):\s*([^,\n]+)'
                for field_match in re.finditer(field_pattern, fields_text):
                    field_name = field_match.group(1)
                    field_type = field_match.group(2).strip()
                    
                    settings[field_name] = {
                        "type": field_type,
                        "struct": struct_name,
                        "file": str(file_path.relative_to(self.repo_path)),
                    }
        
        return settings
    
    def extract_enums(self) -> Dict[str, Dict[str, Any]]:
        """
        Extract enum definitions and their variants.
        
        Returns:
            Dictionary mapping enum names to their variants
        """
        enums = {}
        
        # Search for enum definitions
        rust_files = self._find_files("**/*.rs")
        
        for file_path in rust_files:
            content = file_path.read_text(encoding="utf-8")
            
            # Extract enum definitions
            enum_pattern = r'pub enum (\w+)\s*\{([^}]+)\}'
            
            for match in re.finditer(enum_pattern, content, re.MULTILINE | re.DOTALL):
                enum_name = match.group(1)
                variants_text = match.group(2)
                
                # Extract variants
                variant_pattern = r'(\w+)(?:\([^)]*\))?'
                variants = []
                
                for variant_match in re.finditer(variant_pattern, variants_text):
                    variant_name = variant_match.group(1).strip()
                    if variant_name and not variant_name.startswith('//'):
                        variants.append(variant_name)
                
                if variants:
                    enums[enum_name] = {
                        "variants": variants,
                        "file": str(file_path.relative_to(self.repo_path)),
                    }
        
        return enums
    
    def extract_commands(self) -> Dict[str, Dict[str, Any]]:
        """
        Extract CLI command definitions.
        
        Returns:
            Dictionary mapping command names to their options
        """
        commands = {}
        
        # Search for clap command definitions
        cli_files = self._find_files("**/cli*.rs") + self._find_files("**/main.rs")
        
        for file_path in cli_files:
            content = file_path.read_text(encoding="utf-8")
            
            # Extract subcommand enums
            subcommand_pattern = r'#\[derive\(.*Subcommand.*\)\]\s*pub enum (\w+)\s*\{([^}]+)\}'
            
            for match in re.finditer(subcommand_pattern, content, re.MULTILINE | re.DOTALL):
                enum_name = match.group(1)
                variants_text = match.group(2)
                
                # Extract command variants
                variant_pattern = r'(\w+)(?:\s*\{[^}]*\})?'
                
                for variant_match in re.finditer(variant_pattern, variants_text):
                    cmd_name = variant_match.group(1).strip()
                    if cmd_name and not cmd_name.startswith('//'):
                        commands[cmd_name.lower()] = {
                            "enum": enum_name,
                            "file": str(file_path.relative_to(self.repo_path)),
                        }
        
        return commands
    
    def extract_env_vars(self) -> Dict[str, Dict[str, Any]]:
        """
        Extract environment variable references.
        
        Returns:
            Dictionary mapping env var names to their usage
        """
        env_vars = {}
        
        rust_files = self._find_files("**/*.rs")
        
        for file_path in rust_files:
            content = file_path.read_text(encoding="utf-8")
            
            # Extract env::var calls
            env_pattern = r'env::var\(["\']([^"\']+)["\']\)'
            
            for match in re.finditer(env_pattern, content):
                var_name = match.group(1)
                
                if var_name not in env_vars:
                    env_vars[var_name] = {
                        "files": [],
                    }
                
                file_rel = str(file_path.relative_to(self.repo_path))
                if file_rel not in env_vars[var_name]["files"]:
                    env_vars[var_name]["files"].append(file_rel)
        
        return env_vars
    
    def _find_files(self, pattern: str) -> List[Path]:
        """
        Find files matching pattern.
        
        Args:
            pattern: Glob pattern
        
        Returns:
            List of matching file paths
        """
        return list(self.repo_path.glob(pattern))
