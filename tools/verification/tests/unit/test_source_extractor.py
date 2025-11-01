"""Unit tests for source code extractor."""

from pathlib import Path
import pytest

from extractors.source_extractor import SourceCodeExtractor
from lib.errors import ExtractionError


def test_init_with_valid_path(tmp_path):
    """Test initialization with valid repository path."""
    extractor = SourceCodeExtractor(tmp_path)
    assert extractor.repo_path == tmp_path


def test_init_with_invalid_path():
    """Test initialization with invalid repository path."""
    with pytest.raises(ExtractionError):
        SourceCodeExtractor(Path("/nonexistent/path"))


def test_extract_settings(tmp_path):
    """Test settings extraction."""
    # Create test Rust file
    config_file = tmp_path / "config.rs"
    config_file.write_text("""
        #[derive(Debug, Serialize, Deserialize)]
        pub struct TestConfig {
            pub setting1: String,
            pub setting2: bool,
        }
    """)
    
    extractor = SourceCodeExtractor(tmp_path)
    settings = extractor.extract_settings()
    
    assert "setting1" in settings
    assert "setting2" in settings
    assert settings["setting1"]["type"] == "String"
    assert settings["setting2"]["type"] == "bool"


def test_extract_enums(tmp_path):
    """Test enum extraction."""
    # Create test Rust file
    enum_file = tmp_path / "types.rs"
    enum_file.write_text("""
        pub enum TestEnum {
            Variant1,
            Variant2,
            Variant3,
        }
    """)
    
    extractor = SourceCodeExtractor(tmp_path)
    enums = extractor.extract_enums()
    
    assert "TestEnum" in enums
    assert "Variant1" in enums["TestEnum"]["variants"]
    assert "Variant2" in enums["TestEnum"]["variants"]


def test_extract_env_vars(tmp_path):
    """Test environment variable extraction."""
    # Create test Rust file
    env_file = tmp_path / "env.rs"
    env_file.write_text("""
        use std::env;
        
        fn get_config() {
            let var1 = env::var("TEST_VAR_1");
            let var2 = env::var("TEST_VAR_2");
        }
    """)
    
    extractor = SourceCodeExtractor(tmp_path)
    env_vars = extractor.extract_env_vars()
    
    assert "TEST_VAR_1" in env_vars
    assert "TEST_VAR_2" in env_vars


def test_extract_all(tmp_path):
    """Test extracting all configuration."""
    # Create test files
    (tmp_path / "config.rs").write_text("""
        pub struct Config {
            pub test: String,
        }
    """)
    
    extractor = SourceCodeExtractor(tmp_path)
    result = extractor.extract_all()
    
    assert "settings" in result
    assert "enums" in result
    assert "commands" in result
    assert "env_vars" in result
