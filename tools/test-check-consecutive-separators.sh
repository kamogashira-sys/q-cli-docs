#!/bin/bash
# Test for check-consecutive-separators
# Purpose: Verify check-consecutive-separators detects known bugs

set -e

TOOL="./tools/check-consecutive-separators.sh"
TEST_DIR="/tmp/test_check_consecutive_separators_$$"

# ===== Setup =====

echo "Setting up test environment..."
mkdir -p "$TEST_DIR"

# ===== Test 1: Known bug detection (REQUIRED) =====

echo ""
echo "Test 1: Known bug detection"
cat > "$TEST_DIR/bug.md" << 'EOF'
# Test

---

---

Content
EOF

if $TOOL "$TEST_DIR" 2>&1 | grep -q "bug.md"; then
    echo "✅ Test 1 passed: Known bug detected"
else
    echo "❌ Test 1 failed: Known bug NOT detected"
    rm -rf "$TEST_DIR"
    exit 1
fi

# Clean up bug file for Test 2
rm "$TEST_DIR/bug.md"

# ===== Test 2: Normal case (REQUIRED) =====

echo ""
echo "Test 2: Normal case"
cat > "$TEST_DIR/normal.md" << 'EOF'
# Normal Document

---

Content here

---
EOF

if $TOOL "$TEST_DIR" > /dev/null 2>&1; then
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
