# Q CLI Documentation Verification Tools

## Overview

This directory contains automated verification tools for Q CLI documentation.
The tools ensure consistency between source code, JSON schemas, and documentation.

## Architecture

The verification system follows a 5-layer architecture:

1. **Data Extraction Layer** (`extractors/`)
   - Extract configuration from source code (Rust)
   - Extract configuration from JSON schemas
   - Extract configuration from documentation (Markdown)

2. **Data Transformation Layer** (`normalizers/`)
   - Normalize data into unified format
   - Detect differences between sources

3. **Validation Logic Layer** (`validators/`)
   - Validate setting values
   - Validate enum values
   - Validate command options
   - Validate data types
   - Validate schemas

4. **Reporting Layer** (`reporters/`)
   - Console output
   - JSON output
   - HTML reports

5. **Orchestration Layer** (`orchestrators/`)
   - Coordinate verification workflow
   - CI/CD integration

## Directory Structure

```
verification/
├── extractors/          # Data extraction from various sources
├── normalizers/         # Data normalization and transformation
├── validators/          # Validation logic
├── reporters/           # Report generation
├── orchestrators/       # Workflow orchestration
├── lib/                 # Shared libraries
├── tests/               # Test suites
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── e2e/            # End-to-end tests
├── config/             # Configuration files
├── docs/               # Documentation
└── examples/           # Usage examples
```

## Quick Start

### Installation

```bash
# Install dependencies
make install

# Or manually
pip install -r requirements.txt
pip install -e .
```

### Usage

```bash
# Run quick verification (< 10 seconds)
./orchestrators/verify.sh --repo /path/to/repo --schemas /path/to/schemas --docs /path/to/docs

# Run with JSON output
./orchestrators/verify.sh --repo /path/to/repo --schemas /path/to/schemas --docs /path/to/docs --format json

# Run with custom config
./orchestrators/verify.sh --repo /path/to/repo --schemas /path/to/schemas --docs /path/to/docs --config config/verification.yaml
```

### Example

```bash
# Verify Q CLI documentation
./orchestrators/verify.sh \
  --repo /tmp/q-cli-source \
  --schemas /tmp/q-cli-source/crates/amzn-toolkit-telemetry/schemas \
  --docs /home/user/q-cli-docs/docs
```

## Development Status

- **Phase**: Phase 2 Complete
- **Current Status**: Production Ready
- **Test Coverage**: 94%
- **Tests**: 62 passed, 1 skipped

## Success Criteria

- Test coverage: 80%+
- Quick verification: < 10 seconds
- Full verification: < 5 minutes
- False positive rate: < 1%
- False negative rate: 0%

## Documentation

- [User Guide](docs/user-guide.md)
- [Developer Guide](docs/developer-guide.md)
- [Architecture](docs/architecture.md)
- [API Reference](docs/api-reference.md)

## License

MIT License - See LICENSE file for details
