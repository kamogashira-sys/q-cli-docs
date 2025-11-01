#!/bin/bash
# Test for [TOOL_NAME]
# Purpose: Verify [TOOL_NAME] detects known bugs

set -e

TOOL="./tools/[TOOL_NAME].sh"
TEST_DIR="/tmp/test_[TOOL_NAME]_$$"

# ===== Setup =====

echo "Setting up test environment..."
mkdir -p "$TEST_DIR"

# ===== Test 1: Known bug detection (REQUIRED) =====

echo ""
echo "Test 1: Known bug detection"
cat > "$TEST_DIR/bug.md" << 'EOF'
# TODO: Add known bug content here
# Example:
# ---
# 
# ---
EOF

if $TOOL "$TEST_DIR" 2>&1 | grep -q "bug.md"; then
    echo "✅ Test 1 passed: Known bug detected"
else
    echo "❌ Test 1 failed: Known bug NOT detected"
    rm -rf "$TEST_DIR"
    exit 1
fi

# ===== Test 2: Normal case (REQUIRED) =====

echo ""
echo "Test 2: Normal case"
cat > "$TEST_DIR/normal.md" << 'EOF'
# TODO: Add normal content here
# Example:
# # Normal Document
# 
# Content here
EOF

if $TOOL "$TEST_DIR" 2>&1 | grep -q "No issues found"; then
    echo "✅ Test 2 passed: No false positive"
else
    echo "❌ Test 2 failed: False positive detected"
    rm -rf "$TEST_DIR"
    exit 1
fi

# ===== Cleanup =====

rm -rf "$TEST_DIR"

echo ""
echo "✅ All tests passed"
exit 0
