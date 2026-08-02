#!/bin/bash
# Verify all check tools have corresponding test files
#
# 走査対象:
#   tools/check-*.sh    -> tools/test-check-*.sh
#   scripts/check-*.sh  -> tools/test-check-*.sh
#   scripts/check-*.py  -> tools/test-check-*.sh
#
# 以前は tools/check-*.sh のみを走査していたため、実際のチェックツールが
# 置かれている scripts/ 配下を一切見ておらず、常に「Total tools: 1」と
# 報告していた。完了条件として機能していなかったため走査範囲を拡張した。

set -e

cd "$(dirname "$0")/.."

MISSING=0
TOTAL=0

echo "Verifying tool tests..."
echo ""

for tool in tools/check-*.sh scripts/check-*.sh scripts/check-*.py; do
    # Skip if no tools found (glob did not match)
    if [ ! -f "$tool" ]; then
        continue
    fi

    TOTAL=$((TOTAL + 1))
    tool_name=$(basename "$tool")
    # 拡張子を .sh に正規化してテストファイル名を決める
    # （check-completeness.py -> tools/test-check-completeness.sh）
    test_file="tools/test-${tool_name%.*}.sh"

    if [ ! -f "$test_file" ]; then
        echo "❌ Missing test: $test_file  (for $tool)"
        MISSING=$((MISSING + 1))
    else
        echo "✅ $tool has test: $test_file"
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
