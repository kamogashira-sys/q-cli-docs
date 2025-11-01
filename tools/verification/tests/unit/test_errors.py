"""Unit tests for error classes."""

import pytest

from lib.errors import (
    VerificationError,
    ExtractionError,
    ValidationError,
    ConfigurationError,
)


def test_verification_error():
    """Test VerificationError."""
    error = VerificationError("Test error", {"key": "value"})
    assert str(error) == "Test error"
    assert error.message == "Test error"
    assert error.details == {"key": "value"}


def test_verification_error_without_details():
    """Test VerificationError without details."""
    error = VerificationError("Test error")
    assert error.details == {}


def test_extraction_error():
    """Test ExtractionError."""
    error = ExtractionError("Extraction failed")
    assert isinstance(error, VerificationError)
    assert str(error) == "Extraction failed"


def test_validation_error():
    """Test ValidationError."""
    error = ValidationError("Validation failed")
    assert isinstance(error, VerificationError)
    assert str(error) == "Validation failed"


def test_configuration_error():
    """Test ConfigurationError."""
    error = ConfigurationError("Config error")
    assert isinstance(error, VerificationError)
    assert str(error) == "Config error"
