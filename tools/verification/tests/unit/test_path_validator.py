"""
Unit tests for PathValidator.
"""

import pytest
from validators.path_validator import PathValidator


class TestPathValidator:
    """Test cases for PathValidator."""
    
    def test_correct_paths_no_errors(self):
        """Test that correct paths produce no errors."""
        validator = PathValidator()
        
        content = """
        # Correct paths
        - Global agent: ~/.aws/amazonq/cli-agents
        - Workspace agent: .amazonq/cli-agents
        - MCP config: ~/.aws/amazonq/mcp.json
        - Settings: ~/.local/share/amazon-q/settings.json
        """
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is True
        assert result['error_count'] == 0
        assert len(result['errors']) == 0
    
    def test_agent_error_1_detected(self):
        """Test detection of ~/.amazonq/agents error."""
        validator = PathValidator()
        
        content = "Agent path: ~/.amazonq/agents/my-agent.json"
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is False
        assert result['error_count'] == 1
        assert result['errors'][0]['error_type'] == 'agent_error_1'
        assert '~/.aws/amazonq/cli-agents' in result['errors'][0]['suggestion']
    
    def test_agent_error_2_detected(self):
        """Test detection of ~/.config/amazonq/agents error."""
        validator = PathValidator()
        
        content = "Agent path: ~/.config/amazonq/agents/my-agent.json"
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is False
        assert result['error_count'] == 1
        assert result['errors'][0]['error_type'] == 'agent_error_2'
    
    def test_mcp_error_detected(self):
        """Test detection of MCP path errors."""
        validator = PathValidator()
        
        content = "MCP config: ~/.amazonq/mcp.json"
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is False
        assert result['error_count'] == 1
        assert result['errors'][0]['error_type'] == 'mcp_error_1'
    
    def test_settings_error_detected(self):
        """Test detection of settings path errors."""
        validator = PathValidator()
        
        content = """
        Settings path 1: ~/.config/amazonq/settings.json
        Settings path 2: ~/.amazonq/settings.json
        """
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is False
        assert result['error_count'] == 2
    
    def test_multiple_errors_in_file(self):
        """Test detection of multiple errors in one file."""
        validator = PathValidator()
        
        content = """
        # Configuration paths
        - Agent: ~/.amazonq/agents/
        - MCP: ~/.amazonq/mcp.json
        - Settings: ~/.config/amazonq/settings.json
        """
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is False
        assert result['error_count'] == 3
    
    def test_line_number_reporting(self):
        """Test that line numbers are correctly reported."""
        validator = PathValidator()
        
        content = """Line 1
Line 2
Error on line 3: ~/.amazonq/agents/
Line 4"""
        
        result = validator.validate_content(content, "test.md")
        
        assert result['errors'][0]['line'] == 3
    
    def test_get_correct_paths(self):
        """Test that correct paths are available."""
        validator = PathValidator()
        
        paths = validator.get_correct_paths()
        
        assert 'global_agent_dir' in paths
        assert paths['global_agent_dir'] == '~/.aws/amazonq/cli-agents'
        assert 'global_settings' in paths
        assert paths['global_settings'] == '~/.local/share/amazon-q/settings.json'
    
    def test_cli_agents_not_flagged_as_error(self):
        """Test that correct .amazonq/cli-agents is not flagged."""
        validator = PathValidator()
        
        content = "Workspace agent: .amazonq/cli-agents/my-agent.json"
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is True
        assert result['error_count'] == 0
    
    def test_subagents_not_flagged_as_error(self):
        """Test that correct .amazonq/.subagents is not flagged."""
        validator = PathValidator()
        
        content = "Subagents: .amazonq/.subagents/"
        
        result = validator.validate_content(content, "test.md")
        
        assert result['is_valid'] is True
        assert result['error_count'] == 0
