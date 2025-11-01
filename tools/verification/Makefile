.PHONY: help install test lint clean quick full

help:
	@echo "Q CLI Verification Tools - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run all tests"
	@echo "  lint       - Run linters"
	@echo "  clean      - Clean temporary files"
	@echo "  quick      - Run quick verification (< 10s)"
	@echo "  full       - Run full verification (< 5min)"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

lint:
	pylint extractors/ normalizers/ validators/ reporters/ orchestrators/ lib/
	mypy extractors/ normalizers/ validators/ reporters/ orchestrators/ lib/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache/ .coverage htmlcov/
	rm -rf reports/

quick:
	./orchestrators/verify.sh --quick

full:
	./orchestrators/verify.sh --full
