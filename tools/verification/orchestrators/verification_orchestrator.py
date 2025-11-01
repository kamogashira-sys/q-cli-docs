"""Orchestrate the verification workflow."""

from pathlib import Path
from typing import Dict, Any, List
import time

from extractors import SourceCodeExtractor, SchemaExtractor, DocumentationExtractor
from normalizers import DataNormalizer, DiffDetector
from validators import (
    SettingValueValidator,
    EnumValueValidator,
    CommandOptionValidator,
    DataTypeValidator,
    SchemaValidator,
)
from reporters import ConsoleReporter, JSONReporter
from lib.logger import get_logger, setup_logging
from lib.utils import load_yaml

logger = get_logger(__name__)


class VerificationOrchestrator:
    """Orchestrate the complete verification workflow."""
    
    def __init__(self, config_path: Path = None):
        """
        Initialize orchestrator.
        
        Args:
            config_path: Path to configuration file
        """
        if config_path and config_path.exists():
            self.config = load_yaml(config_path)
        else:
            self.config = self._default_config()
        
        setup_logging(level=self.config.get("log_level", "INFO"))
    
    def verify(self, repo_path: Path, schema_dir: Path, docs_dir: Path) -> Dict[str, Any]:
        """
        Run complete verification workflow.
        
        Args:
            repo_path: Path to source code repository
            schema_dir: Path to schema directory
            docs_dir: Path to documentation directory
        
        Returns:
            Verification results
        """
        logger.info("Starting verification workflow")
        start_time = time.time()
        
        # Step 1: Extract data
        logger.info("Step 1: Extracting data from sources")
        source_data = SourceCodeExtractor(repo_path).extract_all()
        schema_data = SchemaExtractor(schema_dir).extract_all()
        doc_data = DocumentationExtractor(docs_dir).extract_all()
        
        # Step 2: Normalize data
        logger.info("Step 2: Normalizing data")
        normalizer = DataNormalizer()
        normalized = normalizer.normalize_all(source_data, schema_data, doc_data)
        
        # Step 3: Detect differences
        logger.info("Step 3: Detecting differences")
        diff_detector = DiffDetector()
        diffs = diff_detector.detect_all(normalized)
        
        # Step 4: Run validators
        logger.info("Step 4: Running validators")
        errors = []
        warnings = []
        
        validators = [
            SettingValueValidator(),
            EnumValueValidator(),
            CommandOptionValidator(),
            DataTypeValidator(),
            SchemaValidator(),
        ]
        
        for validator in validators:
            validator_errors = validator.validate(normalized)
            errors.extend(validator_errors)
        
        # Convert diffs to warnings
        for category, items in diffs.items():
            for item in items:
                warnings.append({
                    "type": category,
                    "message": f"{category}: {item.get('name', 'unknown')}",
                    "details": item,
                })
        
        # Step 5: Generate results
        elapsed_time = time.time() - start_time
        
        results = {
            "status": "pass" if len(errors) == 0 else "fail",
            "errors": errors,
            "warnings": warnings,
            "metadata": {
                "elapsed_time": f"{elapsed_time:.2f}s",
                "total_settings": len(normalized.get("settings", {})),
                "total_enums": len(normalized.get("enums", {})),
                "total_commands": len(normalized.get("commands", {})),
                "total_env_vars": len(normalized.get("env_vars", {})),
            },
        }
        
        logger.info(f"Verification completed in {elapsed_time:.2f}s")
        return results
    
    def report(self, results: Dict[str, Any], format: str = "console") -> str:
        """
        Generate report from results.
        
        Args:
            results: Verification results
            format: Report format (console or json)
        
        Returns:
            Formatted report
        """
        if format == "json":
            reporter = JSONReporter()
        else:
            reporter = ConsoleReporter()
        
        return reporter.report(results)
    
    def _default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "log_level": "INFO",
            "validation": {
                "setting_values": {"enabled": True},
                "enum_values": {"enabled": True},
                "command_options": {"enabled": True},
                "data_types": {"enabled": True},
                "schema": {"enabled": True},
            },
        }
