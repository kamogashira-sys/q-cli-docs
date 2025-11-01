"""
v2.0 Validator のユニットテスト
"""

import pytest
from pathlib import Path
import tempfile
import json
from validators.v2_validator import (
    V2Validator,
    CrossValidator,
    ValidationError,
    ValidationResult,
    SourceLoader
)


@pytest.fixture
def temp_data_file():
    """テスト用データファイルを作成"""
    data = {
        "sources": {
            "source_code": {
                "paths": {
                    "agent_dir": "~/.aws/amazonq/cli-agents"
                },
                "env_vars": {
                    "Q_LOG_LEVEL": {
                        "default": "info",
                        "type": "string"
                    },
                    "Q_TELEMETRY_ENABLED": {
                        "default": "true",
                        "type": "boolean"
                    }
                }
            }
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = Path(f.name)
    
    yield temp_path
    temp_path.unlink()


@pytest.fixture
def temp_docs_dir():
    """テスト用ドキュメントディレクトリを作成"""
    with tempfile.TemporaryDirectory() as tmpdir:
        docs_dir = Path(tmpdir)
        yield docs_dir


def test_source_loader(temp_data_file):
    """SourceLoaderのテスト"""
    loader = SourceLoader()
    sources = loader.load(temp_data_file)
    
    assert "paths" in sources
    assert "env_vars" in sources
    assert sources["paths"]["agent_dir"] == "~/.aws/amazonq/cli-agents"


def test_cross_validator_init(temp_data_file):
    """CrossValidatorの初期化テスト"""
    loader = SourceLoader()
    sources = loader.load(temp_data_file)
    validator = CrossValidator(sources)
    
    assert validator.sources == sources
    assert len(validator.path_patterns) > 0
    assert isinstance(validator.env_patterns, dict)


def test_validate_correct_path(temp_data_file, temp_docs_dir):
    """正しいパスの検証テスト"""
    # 正しいパスを含むファイルを作成
    test_file = temp_docs_dir / "test.md"
    test_file.write_text("Path: ~/.aws/amazonq/cli-agents\n")
    
    loader = SourceLoader()
    sources = loader.load(temp_data_file)
    validator = CrossValidator(sources)
    
    errors = validator.validate_file(test_file)
    assert len(errors) == 0


def test_validate_incorrect_path(temp_data_file, temp_docs_dir):
    """誤ったパスの検証テスト"""
    # 誤ったパスを含むファイルを作成
    test_file = temp_docs_dir / "test.md"
    test_file.write_text("Path: ~/.amazonq/agents\n")
    
    loader = SourceLoader()
    sources = loader.load(temp_data_file)
    validator = CrossValidator(sources)
    
    errors = validator.validate_file(test_file)
    assert len(errors) == 1
    assert errors[0].severity == "error"
    assert "~/.aws/amazonq/cli-agents" in errors[0].expected


def test_validate_known_env_var(temp_data_file, temp_docs_dir):
    """既知の環境変数の検証テスト"""
    test_file = temp_docs_dir / "test.md"
    test_file.write_text("export Q_LOG_LEVEL=debug\n")
    
    loader = SourceLoader()
    sources = loader.load(temp_data_file)
    validator = CrossValidator(sources)
    
    errors = validator.validate_file(test_file)
    # 既知の変数なので警告なし
    warnings = [e for e in errors if e.severity == "warning"]
    assert len(warnings) == 0


def test_validate_unknown_env_var(temp_data_file, temp_docs_dir):
    """未知の環境変数の検証テスト"""
    test_file = temp_docs_dir / "test.md"
    test_file.write_text("export Q_UNKNOWN_VAR=value\n")
    
    loader = SourceLoader()
    sources = loader.load(temp_data_file)
    validator = CrossValidator(sources)
    
    errors = validator.validate_file(test_file)
    # 未知の変数なので警告あり
    warnings = [e for e in errors if e.severity == "warning"]
    assert len(warnings) == 1
    assert "Q_UNKNOWN_VAR" in warnings[0].actual


def test_validate_placeholder_var(temp_data_file, temp_docs_dir):
    """プレースホルダー変数の検証テスト"""
    test_file = temp_docs_dir / "test.md"
    test_file.write_text("export MY_VARIABLE=value\n")
    
    loader = SourceLoader()
    sources = loader.load(temp_data_file)
    validator = CrossValidator(sources)
    
    errors = validator.validate_file(test_file)
    # プレースホルダーなので警告なし
    warnings = [e for e in errors if e.severity == "warning"]
    assert len(warnings) == 0


def test_v2_validator_init(temp_data_file):
    """V2Validatorの初期化テスト"""
    validator = V2Validator(temp_data_file)
    
    assert validator.data_path == temp_data_file
    assert validator.sources is not None
    assert validator.validator is not None


def test_v2_validator_validate_directory(temp_data_file, temp_docs_dir):
    """ディレクトリ検証のテスト"""
    # テストファイルを作成
    (temp_docs_dir / "test1.md").write_text("Correct path: ~/.aws/amazonq/cli-agents\n")
    (temp_docs_dir / "test2.md").write_text("Wrong path: ~/.amazonq/agents\n")
    
    validator = V2Validator(temp_data_file)
    result = validator.validate_directory(temp_docs_dir)
    
    assert result.metrics.files_checked == 2
    assert result.metrics.total_errors == 1
    assert len(result.errors) == 1


def test_v2_validator_generate_report(temp_data_file, temp_docs_dir):
    """レポート生成のテスト"""
    (temp_docs_dir / "test.md").write_text("Path: ~/.aws/amazonq/cli-agents\n")
    
    validator = V2Validator(temp_data_file)
    result = validator.validate_directory(temp_docs_dir)
    report = validator.generate_report(result)
    
    assert "v2.0 Validation Report" in report
    assert "Files checked:" in report
    assert "✅ All validations passed!" in report


def test_validation_error_dataclass():
    """ValidationErrorデータクラスのテスト"""
    error = ValidationError(
        file="test.md",
        line=10,
        message="Test error",
        expected="expected",
        actual="actual",
        source="test"
    )
    
    assert error.file == "test.md"
    assert error.line == 10
    assert error.severity == "error"  # デフォルト値


def test_validation_result_dataclass():
    """ValidationResultデータクラスのテスト"""
    result = ValidationResult()
    
    assert len(result.errors) == 0
    assert len(result.warnings) == 0
    assert result.metrics.files_checked == 0


def test_multiple_errors_in_file(temp_data_file, temp_docs_dir):
    """1ファイル内の複数エラー検出テスト"""
    test_file = temp_docs_dir / "test.md"
    test_file.write_text("""
    Path1: ~/.amazonq/agents
    Path2: ~/.config/amazonq/agents
    Path3: ~/.aws/amazonq/.subagents
    """)
    
    loader = SourceLoader()
    sources = loader.load(temp_data_file)
    validator = CrossValidator(sources)
    
    errors = validator.validate_file(test_file)
    assert len(errors) == 3


def test_consistency_rate_calculation(temp_data_file, temp_docs_dir):
    """一貫性率の計算テスト"""
    (temp_docs_dir / "test1.md").write_text("Correct\n")
    (temp_docs_dir / "test2.md").write_text("Wrong: ~/.amazonq/agents\n")
    
    validator = V2Validator(temp_data_file)
    result = validator.validate_directory(temp_docs_dir)
    
    # 2ファイル中1エラー = 50%の一貫性率
    assert result.metrics.consistency_rate == 0.5


def test_coverage_metrics(temp_data_file, temp_docs_dir):
    """カバレッジメトリクスのテスト"""
    (temp_docs_dir / "test.md").write_text("Test\n")
    
    validator = V2Validator(temp_data_file)
    result = validator.validate_directory(temp_docs_dir)
    
    assert "source_code" in result.metrics.coverage
    assert "research" in result.metrics.coverage
    assert result.metrics.coverage["source_code"] == 1.0
