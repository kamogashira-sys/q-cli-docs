#!/bin/bash
# Test for check-consistency.sh
# Purpose: 基本的な実行可能性と終了コード規約を検証する
#
# 注記: このツールは本作業（make check-all の根本対処）では改修していない。
# verify-tool-tests.sh の走査範囲を scripts/ に拡張した際にテスト欠落が
# 露出したため、最低限の正常系テストを用意した。詳細な異常系テストは
# 当該ツールを改修する際に追加する。

set -e

cd "$(dirname "$0")/.."

TOOL="./scripts/check-consistency.sh"

# ===== Test 1: 実行可能であること =====

echo "Test 1: 実行可能ビットが立っていること"
if [ -x "$TOOL" ]; then
    echo "✅ Test 1 passed"
else
    echo "❌ Test 1 failed: $TOOL が実行可能でない"
    exit 1
fi

# ===== Test 2: 構文エラーがないこと =====

echo ""
echo "Test 2: bash 構文が正しいこと"
if bash -n "$TOOL" 2>/dev/null; then
    echo "✅ Test 2 passed"
else
    echo "❌ Test 2 failed: bash 構文エラー"
    bash -n "$TOOL"
    exit 1
fi

# ===== Test 3: 現状の docs/ で実行でき、終了コードが 0 または 1 であること =====
#
# 14_tool-creation-checklist.md の規約: 問題検出=1 / 問題なし=0 / ツールのエラー=2
# ツール自体のエラー（2）や予期しない終了コードでないことを確認する。

echo ""
echo "Test 3: 実行して終了コードが 0 または 1 であること"
set +e
"$TOOL" > /tmp/test_check-consistency_$$.txt 2>&1
rc=$?
set -e

if [ "$rc" -eq 0 ] || [ "$rc" -eq 1 ]; then
    echo "✅ Test 3 passed: exit $rc"
else
    echo "❌ Test 3 failed: exit $rc（期待値 0 または 1）"
    tail -20 /tmp/test_check-consistency_$$.txt | sed 's/^/    /'
    rm -f /tmp/test_check-consistency_$$.txt
    exit 1
fi
rm -f /tmp/test_check-consistency_$$.txt

echo ""
echo "✅ All tests passed"
exit 0
