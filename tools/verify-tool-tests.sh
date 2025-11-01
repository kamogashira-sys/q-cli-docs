#!/bin/bash
# Verify all check tools have corresponding test files

set -e

MISSING=0
TOTAL=0

echo "Verifying tool tests..."
echo ""

for tool in tools/check-*.sh; do
    # Skip if no tools found
    if [ ! -f "$tool" ]; then
        continue
    fi
    
    TOTAL=$((TOTAL + 1))
    tool_name=$(basename "$tool")
    test_file="tools/test-$tool_name"
    
    if [ ! -f "$test_file" ]; then
        echo "❌ Missing test: $test_file"
        MISSING=$((MISSING + 1))
    else
        echo "✅ $tool_name has test"
    fi
done

echo ""
echo "Summary:"
echo "  Total tools: $TOTAL"
echo "  With tests: $((TOTAL - MISSING))"
echo "  Missing tests: $MISSING"
echo ""

if [ "$MISSING" -eq 0 ]; then
    echo "✅ All tools have tests"
    exit 0
else
    echo "❌ $MISSING tool(s) missing tests"
    echo ""
    echo "To create a test file:"
    echo "  cp tools/templates/test-tool-template.sh tools/test-<tool-name>.sh"
    exit 1
fi
