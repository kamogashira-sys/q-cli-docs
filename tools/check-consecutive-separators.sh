#!/bin/bash
# Check for consecutive separator lines (--- followed by ---)

set -e

DOCS_DIR="${1:-docs}"

echo "Checking for consecutive separator lines in $DOCS_DIR..."
echo ""

# Find all markdown files and check for consecutive separators using awk
ERRORS=$(find "$DOCS_DIR" -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/venv/*" -exec awk '
/^---$/ {
    if (prev == "---" && NR - prev_line <= 2) {
        print FILENAME ":" prev_line "-" NR ": Consecutive separators"
        found = 1
    }
    prev = "---"
    prev_line = NR
}
END {
    if (found) exit 1
}
' {} \; | tee /dev/stderr | wc -l)

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ No consecutive separators found"
    exit 0
else
    echo "❌ Found $ERRORS file(s) with consecutive separators"
    exit 1
fi
