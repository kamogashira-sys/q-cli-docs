"""
File path validator for Q CLI documentation.

Validates that file paths in documentation match the actual paths
defined in the source code.
"""

from typing import Dict, List, Set
import re


class PathValidator:
    """Validates file paths in documentation against source code definitions."""
    
    # Correct paths from source code (directories.rs)
    CORRECT_PATHS = {
        # Agent configuration
        'global_agent_dir': '~/.aws/amazonq/cli-agents',
        'workspace_agent_dir': '.amazonq/cli-agents',
        
        # Subagents
        'workspace_subagents_dir': '.amazonq/.subagents',
        
        # MCP configuration
        'global_mcp_config': '~/.aws/amazonq/mcp.json',
        'workspace_mcp_config': '.amazonq/mcp.json',
        
        # Global settings
        'global_settings': '~/.local/share/amazon-q/settings.json',
        
        # Prompts
        'workspace_prompts_dir': '.amazonq/prompts',
        'global_prompts_dir': '~/.aws/amazonq/cli-agents/prompts',
    }
    
    # Known incorrect patterns to detect
    INCORRECT_PATTERNS = {
        # Agent configuration errors (order matters - most specific first)
        'agent_error_2': r'~/\.config/amazonq/agents',
        'agent_error_1': r'~/\.amazonq/agents(?!/cli-agents)',
        'agent_error_3': r'(?<!~/)\.amazonq/agents(?!/cli-agents|/\.subagents)',
        
        # Subagents errors
        'subagents_error_1': r'~/\.aws/amazonq/\.subagents',
        
        # MCP configuration errors
        'mcp_error_1': r'~/\.amazonq/mcp\.json',
        'mcp_error_2': r'~/\.config/amazonq/mcp\.json',
        
        # Global settings errors
        'settings_error_1': r'~/\.config/amazonq/settings\.json',
        'settings_error_2': r'~/\.amazonq/settings\.json',
        
        # Prompts errors
        'prompts_error_1': r'~/\.amazonq/prompts',
    }
    
    def __init__(self):
        """Initialize the path validator."""
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
    
    def validate_content(self, content: str, file_path: str) -> Dict:
        """
        Validate file paths in the given content.
        
        Args:
            content: The content to validate
            file_path: Path to the file being validated (for error reporting)
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        
        for error_name, pattern in self.INCORRECT_PATTERNS.items():
            matches = list(re.finditer(pattern, content))
            for match in matches:
                # Get line number
                line_num = content[:match.start()].count('\n') + 1
                
                # Get context (the line containing the error)
                lines = content.split('\n')
                context = lines[line_num - 1] if line_num <= len(lines) else ""
                
                errors.append({
                    'error_type': error_name,
                    'file': file_path,
                    'line': line_num,
                    'matched_text': match.group(0),
                    'context': context.strip(),
                    'suggestion': self._get_suggestion(error_name)
                })
        
        return {
            'file': file_path,
            'errors': errors,
            'error_count': len(errors),
            'is_valid': len(errors) == 0
        }
    
    def _get_suggestion(self, error_name: str) -> str:
        """Get correction suggestion for an error type."""
        suggestions = {
            'agent_error_1': '~/.aws/amazonq/cli-agents',
            'agent_error_2': '~/.aws/amazonq/cli-agents',
            'agent_error_3': '.amazonq/cli-agents',
            'subagents_error_1': '.amazonq/.subagents',
            'mcp_error_1': '~/.aws/amazonq/mcp.json',
            'mcp_error_2': '~/.aws/amazonq/mcp.json',
            'settings_error_1': '~/.local/share/amazon-q/settings.json',
            'settings_error_2': '~/.local/share/amazon-q/settings.json',
            'prompts_error_1': '.amazonq/prompts or ~/.aws/amazonq/cli-agents/prompts',
        }
        return suggestions.get(error_name, 'Unknown')
    
    def validate_directory(self, directory: str, file_pattern: str = "*.md") -> Dict:
        """
        Validate all files in a directory.
        
        Args:
            directory: Directory to validate
            file_pattern: File pattern to match (default: *.md)
            
        Returns:
            Dictionary with validation results for all files
        """
        import glob
        import os
        
        results = []
        total_errors = 0
        
        # Find all matching files
        pattern = os.path.join(directory, '**', file_pattern)
        files = glob.glob(pattern, recursive=True)
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                result = self.validate_content(content, file_path)
                results.append(result)
                total_errors += result['error_count']
            except Exception as e:
                results.append({
                    'file': file_path,
                    'errors': [{'error_type': 'read_error', 'message': str(e)}],
                    'error_count': 1,
                    'is_valid': False
                })
                total_errors += 1
        
        return {
            'directory': directory,
            'files_checked': len(results),
            'total_errors': total_errors,
            'results': results,
            'is_valid': total_errors == 0
        }
    
    def get_correct_paths(self) -> Dict[str, str]:
        """Get the dictionary of correct paths."""
        return self.CORRECT_PATHS.copy()
