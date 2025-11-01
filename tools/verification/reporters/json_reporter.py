"""JSON reporter for verification results."""

import json
from typing import Dict, Any
from pathlib import Path

from lib.logger import get_logger
from lib.utils import save_json

logger = get_logger(__name__)


class JSONReporter:
    """Generate JSON output for verification results."""
    
    def report(self, results: Dict[str, Any], output_file: Path = None) -> str:
        """
        Generate JSON report.
        
        Args:
            results: Verification results
            output_file: Optional file path to save report
        
        Returns:
            JSON string
        """
        logger.info("Generating JSON report")
        
        report = {
            "status": "pass" if len(results.get("errors", [])) == 0 else "fail",
            "summary": {
                "total_errors": len(results.get("errors", [])),
                "total_warnings": len(results.get("warnings", [])),
            },
            "errors": results.get("errors", []),
            "warnings": results.get("warnings", []),
            "metadata": results.get("metadata", {}),
        }
        
        if output_file:
            save_json(report, output_file)
            logger.info(f"JSON report saved to {output_file}")
        
        return json.dumps(report, indent=2)
