"""Custom exceptions for verification tools."""


class VerificationError(Exception):
    """Base exception for verification errors."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ExtractionError(VerificationError):
    """Exception raised during data extraction."""
    pass


class ValidationError(VerificationError):
    """Exception raised during validation."""
    pass


class ConfigurationError(VerificationError):
    """Exception raised for configuration issues."""
    pass
