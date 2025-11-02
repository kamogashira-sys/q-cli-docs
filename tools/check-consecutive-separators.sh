#!/bin/bash
# Check for consecutive separator lines (--- followed by ---)
# Detects separators with only blank lines in between (no meaningful content)

set -e

DOCS_DIR="${1:-docs}"

echo "Checking for consecutive separator lines in $DOCS_DIR..."
echo ""

# Find all markdown files and check for consecutive separators using awk
ERRORS=$(find "$DOCS_DIR" -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/venv/*" -exec awk '
/^---$/ {
    if (prev == "---") {
        gap = NR - prev_line
        # Check if gap is 1-3 lines (direct consecutive or up to 2 blank lines)
        if (gap <= 3) {
            # Check if all lines between separators are blank
            all_blank = 1
            for (i = prev_line + 1; i < NR; i++) {
                if (lines[i] !~ /^[[:space:]]*$/) {
                    all_blank = 0
                    break
                }
            }
            if (all_blank) {
                print FILENAME ":" prev_line "-" NR ": Consecutive separators (gap: " gap " lines, all blank)"
                found = 1
            }
        }
    }
    prev = "---"
    prev_line = NR
}
{
    lines[NR] = $0
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
