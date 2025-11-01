"""Console reporter for verification results."""

from typing import Dict, Any, List
from colorama import Fore, Style, init

from lib.logger import get_logger

# Initialize colorama
init(autoreset=True)

logger = get_logger(__name__)


class ConsoleReporter:
    """Generate console output for verification results."""
    
    def report(self, results: Dict[str, Any]) -> str:
        """
        Generate console report.
        
        Args:
            results: Verification results
        
        Returns:
            Formatted console output
        """
        logger.info("Generating console report")
        
        lines = []
        lines.append(self._header())
        lines.append(self._summary(results))
        
        if results.get("errors"):
            lines.append(self._errors_section(results["errors"]))
        
        if results.get("warnings"):
            lines.append(self._warnings_section(results["warnings"]))
        
        lines.append(self._footer(results))
        
        return "\n".join(lines)
    
    def _header(self) -> str:
        """Generate report header."""
        return f"\n{Fore.CYAN}{'=' * 80}\n  Q CLI Documentation Verification Report\n{'=' * 80}{Style.RESET_ALL}\n"
    
    def _summary(self, results: Dict[str, Any]) -> str:
        """Generate summary section."""
        total_errors = len(results.get("errors", []))
        total_warnings = len(results.get("warnings", []))
        
        status = f"{Fore.GREEN}PASS" if total_errors == 0 else f"{Fore.RED}FAIL"
        
        lines = [
            f"\n{Fore.YELLOW}Summary:{Style.RESET_ALL}",
            f"  Status: {status}{Style.RESET_ALL}",
            f"  Errors: {Fore.RED if total_errors > 0 else Fore.GREEN}{total_errors}{Style.RESET_ALL}",
            f"  Warnings: {Fore.YELLOW if total_warnings > 0 else Fore.GREEN}{total_warnings}{Style.RESET_ALL}",
        ]
        
        return "\n".join(lines)
    
    def _errors_section(self, errors: List[Dict[str, Any]]) -> str:
        """Generate errors section."""
        lines = [f"\n{Fore.RED}Errors:{Style.RESET_ALL}"]
        
        for i, error in enumerate(errors, 1):
            lines.append(f"\n  {i}. {error.get('type', 'unknown')}")
            lines.append(f"     {error.get('message', 'No message')}")
            
            if "details" in error:
                for key, value in error["details"].items():
                    lines.append(f"     {key}: {value}")
        
        return "\n".join(lines)
    
    def _warnings_section(self, warnings: List[Dict[str, Any]]) -> str:
        """Generate warnings section."""
        lines = [f"\n{Fore.YELLOW}Warnings:{Style.RESET_ALL}"]
        
        for i, warning in enumerate(warnings, 1):
            lines.append(f"\n  {i}. {warning.get('type', 'unknown')}")
            lines.append(f"     {warning.get('message', 'No message')}")
        
        return "\n".join(lines)
    
    def _footer(self, results: Dict[str, Any]) -> str:
        """Generate report footer."""
        total_errors = len(results.get("errors", []))
        status = "✓ Verification passed" if total_errors == 0 else "✗ Verification failed"
        color = Fore.GREEN if total_errors == 0 else Fore.RED
        
        return f"\n{color}{status}{Style.RESET_ALL}\n{'=' * 80}\n"
