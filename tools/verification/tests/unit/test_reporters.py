"""Unit tests for reporters."""

import json
import pytest

from reporters import ConsoleReporter, JSONReporter


@pytest.fixture
def sample_results():
    """Sample verification results."""
    return {
        "status": "fail",
        "errors": [
            {
                "type": "missing_schema",
                "message": "Setting 'test' missing in schema",
                "details": {"setting": "test"},
            },
        ],
        "warnings": [
            {
                "type": "missing_in_docs",
                "message": "Setting 'other' not documented",
            },
        ],
        "metadata": {
            "elapsed_time": "1.23s",
            "total_settings": 10,
        },
    }


def test_console_reporter(sample_results):
    """Test console reporter."""
    reporter = ConsoleReporter()
    output = reporter.report(sample_results)
    
    assert "Verification Report" in output
    assert "FAIL" in output
    assert "Errors: " in output
    assert "Warnings: " in output
    assert "missing_schema" in output


def test_console_reporter_pass():
    """Test console reporter with passing results."""
    results = {
        "status": "pass",
        "errors": [],
        "warnings": [],
        "metadata": {},
    }
    
    reporter = ConsoleReporter()
    output = reporter.report(results)
    
    assert "PASS" in output
    assert "Verification passed" in output


def test_json_reporter(sample_results):
    """Test JSON reporter."""
    reporter = JSONReporter()
    output = reporter.report(sample_results)
    
    data = json.loads(output)
    
    assert data["status"] == "fail"
    assert len(data["errors"]) == 1
    assert len(data["warnings"]) == 1
    assert data["summary"]["total_errors"] == 1
    assert data["summary"]["total_warnings"] == 1


def test_json_reporter_save(sample_results, tmp_path):
    """Test JSON reporter with file save."""
    output_file = tmp_path / "report.json"
    
    reporter = JSONReporter()
    reporter.report(sample_results, output_file)
    
    assert output_file.exists()
    
    with open(output_file) as f:
        data = json.load(f)
    
    assert data["status"] == "fail"
