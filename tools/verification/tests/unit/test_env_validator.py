"""
Unit tests for EnvValidator.
"""

import pytest
from validators.env_validator import EnvValidator


class TestEnvValidator:
    """Test cases for EnvValidator."""
    
    def test_known_vars_no_warnings(self):
        """Test that known variables produce no warnings."""
        validator = EnvValidator()
        
        content = """
        # Known environment variables
        export Q_LOG_LEVEL=debug
        export AWS_PROFILE=default
        export HOME=/home/user
        """
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is True
        assert result['warning_count'] == 0
        assert 'Q_LOG_LEVEL' in result['found_vars']
        assert 'AWS_PROFILE' in result['found_vars']
    
    def test_unknown_var_warning(self):
        """Test that unknown variables produce warnings."""
        validator = EnvValidator()
        
        content = "export Q_TOTALLY_UNKNOWN=value"
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is False
        assert result['warning_count'] == 1
        assert result['warnings'][0]['var_name'] == 'Q_TOTALLY_UNKNOWN'
    
    def test_placeholder_vars_allowed(self):
        """Test that placeholder variables are allowed."""
        validator = EnvValidator()
        
        content = """
        export Q_VARIABLE_NAME=value
        export MY_CUSTOM_VAR=value
        export YOUR_API_KEY=value
        """
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is True
        assert result['warning_count'] == 0
    
    def test_mcp_server_prefix_allowed(self):
        """Test that Q_MCP_SERVER_ prefix is allowed."""
        validator = EnvValidator()
        
        content = "export Q_MCP_SERVER_MY_SERVER_API_KEY=secret"
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is True
        assert result['warning_count'] == 0
    
    def test_hook_prefix_allowed(self):
        """Test that Q_HOOK_ prefix is allowed."""
        validator = EnvValidator()
        
        content = """
        Q_HOOK_TRIGGER=agentSpawn
        Q_HOOK_TOOL_NAME=git
        """
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is True
        assert result['warning_count'] == 0
    
    def test_env_expansion_syntax(self):
        """Test ${env:VAR_NAME} syntax."""
        validator = EnvValidator()
        
        content = '"api_key": "${env:MY_API_KEY}"'
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is True  # MY_ prefix is placeholder
    
    def test_table_format_vars(self):
        """Test variables in table format."""
        validator = EnvValidator()
        
        content = """
        | Variable | Description |
        |----------|-------------|
        | `Q_LOG_LEVEL` | Log level |
        | `AWS_REGION` | AWS region |
        """
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is True
        assert 'Q_LOG_LEVEL' in result['found_vars']
        assert 'AWS_REGION' in result['found_vars']
    
    def test_line_number_reporting(self):
        """Test that line numbers are correctly reported."""
        validator = EnvValidator()
        
        content = """Line 1
Line 2
export Q_TOTALLY_UNKNOWN=value
Line 4"""
        
        result = validator.validate_content(content, "test.md")
        
        assert len(result['warnings']) > 0
        assert result['warnings'][0]['line'] == 3
    
    def test_get_known_vars(self):
        """Test that known variables list is available."""
        validator = EnvValidator()
        
        known_vars = validator.get_known_vars()
        
        assert 'Q_LOG_LEVEL' in known_vars
        assert 'AWS_PROFILE' in known_vars
        assert 'HOME' in known_vars
        assert len(known_vars) > 50  # Should have many known vars
