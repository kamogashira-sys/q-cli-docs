"""
Environment variable validator for Q CLI documentation.

Validates that environment variables in documentation are correctly named
and documented.
"""

from typing import Dict, List, Set
import re


class EnvValidator:
    """Validates environment variables in documentation."""
    
    # Known Q CLI environment variables from source code and documentation
    KNOWN_ENV_VARS = {
        # Core
        'Q_LOG_LEVEL',
        'Q_LOG_STDOUT',
        'Q_CLI_CLIENT_APPLICATION',
        'Q_DISABLE_TELEMETRY',
        'Q_TELEMETRY_ENABLED',
        'Q_TELEMETRY_CLIENT_ID',
        
        # Chat configuration
        'Q_CHAT_MODEL',
        'Q_CHAT_TEMPERATURE',
        'Q_CHAT_MAX_TOKENS',
        'Q_MAX_CONTEXT_TOKENS',
        'Q_CHAT_SHELL',
        
        # Agent configuration
        'Q_AGENT_NAME',
        'Q_AGENT_PATH',
        'Q_AGENT_CONFIG',
        'Q_AGENT',
        
        # MCP configuration
        'Q_MCP_CONFIG_PATH',
        
        # Knowledge configuration
        'Q_KNOWLEDGE_ENABLED',
        'Q_KNOWLEDGE_PATH',
        
        # qterm related
        'QTERM_SESSION_ID',
        'Q_PARENT',
        'Q_SET_PARENT',
        'Q_SET_PARENT_CHECK',
        'Q_TERM',
        'Q_SHELL',
        'Q_ZDOTDIR',
        
        # Debug/Development
        'Q_DEBUG',
        'Q_DEBUG_SHELL',
        'Q_FAKE_IS_REMOTE',
        'Q_CODESPACES',
        'Q_CI',
        'Q_BUNDLE_METADATA_PATH',
        'Q_DISABLE_TRUECOLOR',
        'Q_MOCK_CHAT_RESPONSE',
        
        # Other Q-related
        'PROCESS_LAUNCHED_BY_Q',
        'Q_USING_ZSH_AUTOSUGGESTIONS',
        'Q_ENABLE_THINKING',
        
        # AWS authentication
        'AMAZON_Q_SIGV4',
        'Q_SIGV',
        
        # Hook related
        'Q_HOOK_TRIGGER',
        'Q_HOOK_TOOL_NAME',
        'Q_HOOK_TOOL_PARAMS',
        
        # System (used by Q CLI)
        'HOME',
        'EDITOR',
        'TERM',
        'CI',
        'CODESPACES',
        'PATH',
        'USER',
        'PWD',
        
        # AWS
        'AWS_PROFILE',
        'AWS_REGION',
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_SESSION_TOKEN',
        'AWS_ACCOUNT',
        'AWS_EXECUTION_ENV',
        'AWS_TOOLING_USER_AGENT',
        
        # XDG
        'XDG_DATA_HOME',
        'XDG_CONFIG_HOME',
        'XDG_CURRENT_DESKTOP',
        'XDG_SESSION_TYPE',
        
        # OAuth
        'Q_OAUTH_REDIRECT_URI',
        
        # Build/Internal (not for users)
        'Q_BUILD_DATETIME',
        'Q_BUILD_HASH',
        'Q_DEVELOPER',
        'Q_DEVELOPER_STANDALONE',
        'Q_DEVELOPER_STANDALONE_FREE',
        'Q_DEVELOPER_STANDALONE_POWER',
        'Q_DEVELOPER_STANDALONE_PRO',
        'Q_DEVELOPER_STANDALONE_PRO_PLUS',
        'Q_DEV_BEXT',
        'Q_FILENAME',
        'Q_LOG_LEVEL_GLOBAL',
    }
    
    # Pattern prefixes that are valid (for dynamic variables)
    VALID_PREFIXES = {
        'Q_MCP_SERVER_',  # MCP server-specific variables
        'Q_HOOK_',        # Hook-related variables
    }
    
    def __init__(self):
        """Initialize the environment variable validator."""
        self.warnings: List[Dict] = []
    
    def validate_content(self, content: str, file_path: str) -> Dict:
        """
        Validate environment variables in the given content.
        
        Args:
            content: The content to validate
            file_path: Path to the file being validated (for error reporting)
            
        Returns:
            Dictionary with validation results
        """
        warnings = []
        
        # Find all environment variable references
        # Pattern: export VAR_NAME, $VAR_NAME, ${VAR_NAME}, ${env:VAR_NAME}, `VAR_NAME`
        # Note: Order matters - more specific patterns first
        patterns = [
            r'export\s+([A-Z_][A-Z0-9_]*)=',   # export VAR_NAME=
            r'\$\{env:([A-Z_][A-Z0-9_]*)\}',   # ${env:VAR_NAME}
            r'\$\{([A-Z_][A-Z0-9_]*)\}',       # ${VAR_NAME}
            r'\$([A-Z_][A-Z0-9_]*)',           # $VAR_NAME
            r'\|.*`([A-Z_][A-Z0-9_]*)`.*\|',   # | `VAR_NAME` | (in table cells)
            r'`([A-Z_][A-Z0-9_]*)`',           # `VAR_NAME` (in tables/code)
        ]
        
        found_vars = set()
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                var_name = match.group(1)
                # Skip very short names (likely prefixes or examples)
                if len(var_name) <= 2:
                    continue
                # Only consider Q_ or AWS_ or system vars
                if var_name.startswith(('Q_', 'AWS_', 'XDG_')) or var_name in {'HOME', 'EDITOR', 'TERM', 'CI', 'CODESPACES', 'PATH', 'USER', 'PWD', 'QTERM_SESSION_ID', 'PROCESS_LAUNCHED_BY_Q', 'AMAZON_Q_SIGV4'}:
                    found_vars.add((var_name, match.start()))
        
        # Check each found variable
        for var_name, pos in found_vars:
            if not self._is_valid_var(var_name):
                # Get line number
                line_num = content[:pos].count('\n') + 1
                
                # Get context
                lines = content.split('\n')
                context = lines[line_num - 1] if line_num <= len(lines) else ""
                
                warnings.append({
                    'warning_type': 'unknown_env_var',
                    'file': file_path,
                    'line': line_num,
                    'var_name': var_name,
                    'context': context.strip(),
                    'suggestion': self._get_suggestion(var_name)
                })
        
        return {
            'file': file_path,
            'warnings': warnings,
            'warning_count': len(warnings),
            'is_valid': len(warnings) == 0,
            'found_vars': sorted(list(set(v[0] for v in found_vars)))
        }
    
    def _is_valid_var(self, var_name: str) -> bool:
        """Check if a variable name is valid."""
        # Check if it's a known variable
        if var_name in self.KNOWN_ENV_VARS:
            return True
        
        # Check if it matches a valid prefix pattern
        for prefix in self.VALID_PREFIXES:
            if var_name.startswith(prefix):
                return True
        
        # Check if it's a placeholder/example variable
        placeholder_keywords = ['VARIABLE', 'VAR', 'NEW', 'OLD', 'CUSTOM', 'MY_', 'YOUR_', 'EXAMPLE', 'AGENT']
        if any(keyword in var_name for keyword in placeholder_keywords):
            return True
        
        return False
    
    def _get_suggestion(self, var_name: str) -> str:
        """Get suggestion for an unknown variable."""
        # Try to find similar known variables
        similar = []
        for known_var in self.KNOWN_ENV_VARS:
            if self._similarity(var_name, known_var) > 0.7:
                similar.append(known_var)
        
        if similar:
            return f"Did you mean: {', '.join(similar[:3])}?"
        
        return "Unknown environment variable. Check if it's documented."
    
    def _similarity(self, s1: str, s2: str) -> float:
        """Calculate simple similarity between two strings."""
        if s1 == s2:
            return 1.0
        
        # Simple character overlap ratio
        s1_chars = set(s1.lower())
        s2_chars = set(s2.lower())
        
        if not s1_chars or not s2_chars:
            return 0.0
        
        intersection = len(s1_chars & s2_chars)
        union = len(s1_chars | s2_chars)
        
        return intersection / union if union > 0 else 0.0
    
    def get_known_vars(self) -> Set[str]:
        """Get the set of known environment variables."""
        return self.KNOWN_ENV_VARS.copy()
