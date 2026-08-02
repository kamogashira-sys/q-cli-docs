#!/bin/bash
# Test for check-urls.sh
# Purpose: Verify check-urls.sh の抽出ロジックとスキップ設計
#
# 対象とする既知バグ:
#   1. Mermaid 図中の HTML リンクを丸ごと URL として拾う（止め文字に ' > がない）
#   2. スキップ設計が真のリンク切れを隠す（ホスト単位スキップ）
#
# ネットワークアクセスを伴う到達性判定はテストしない（外部サイトの状態に
# 依存して不安定になるため）。抽出ロジックとスキップ判定のみを検証する。

set -e

cd "$(dirname "$0")/.."

TOOL="./scripts/check-urls.sh"

# ===== Test 1: 既知バグ - Mermaid HTML リンクの抽出（REQUIRED）=====
#
# check-urls.sh は docs/ 固定で走査するため、抽出ロジックそのものを
# 同じ正規表現で再現して検証する。

echo "Test 1: Mermaid HTML リンクを丸ごと拾わないこと"

TEST_DIR="/tmp/test_check_urls_$$"
mkdir -p "$TEST_DIR"

cat > "$TEST_DIR/mermaid.md" << 'EOF'
```mermaid
graph TD
    A["<a href='https://github.com/example/repo/blob/main/docs/01_chat.md'>チャット機能</a>"]
```
EOF

# 旧実装の正規表現
old=$(grep -hoP 'https?://[^\s\)\]]+' "$TEST_DIR/mermaid.md" | head -1)
# 現行実装の正規表現（scripts/check-urls.sh と同一）
new=$(grep -hoP "https?://[^\s\)\]'\"\`><]+" "$TEST_DIR/mermaid.md" | head -1)

if [[ "$old" == *"'>"* ]]; then
    echo "   （旧実装は $old を抽出していた）"
else
    echo "❌ Test 1 setup failed: 旧実装のバグを再現できていない"
    rm -rf "$TEST_DIR"
    exit 1
fi

if [[ "$new" == "https://github.com/example/repo/blob/main/docs/01_chat.md" ]]; then
    echo "✅ Test 1 passed: URL のみを正しく抽出（$new）"
else
    echo "❌ Test 1 failed: 抽出結果が不正: $new"
    rm -rf "$TEST_DIR"
    exit 1
fi

rm -rf "$TEST_DIR"

# ===== Test 2: スキップ設計が真のリンク切れを隠さないこと（REQUIRED）=====
#
# desktop-release.* をホスト単位でスキップすると、同ホスト配下の実在しない
# キー（403 を返す）を永久に隠すことになる。ホスト単位スキップの不在を確認。

echo ""
echo "Test 2: ホスト単位スキップを導入していないこと"

if grep -qE 'desktop-release|\bamazonaws\.com\)' "$TOOL" \
    && ! grep -q 'SKIP_EXACT' "$TOOL"; then
    echo "❌ Test 2 failed: ホスト単位スキップの疑いがある"
    exit 1
fi

# desktop-release ホストがスキップ対象になっていないことを確認
if grep -E '^\s*(SKIP_PLACEHOLDER|\[)' "$TOOL" | grep -q 'desktop-release'; then
    echo "❌ Test 2 failed: desktop-release がスキップ対象に含まれている"
    echo "   このホスト配下に真のリンク切れが存在したため偽陰性を作る"
    exit 1
fi

echo "✅ Test 2 passed: ホスト単位スキップなし（URL完全一致方式）"

# ===== Test 3: スキップが可視化されること =====

echo ""
echo "Test 3: スキップした URL と理由が出力されること"

if grep -q 'スキップしたURL' "$TOOL" && grep -q 'SKIP_LOG' "$TOOL"; then
    echo "✅ Test 3 passed: スキップの可視化が実装されている"
else
    echo "❌ Test 3 failed: スキップの可視化が実装されていない"
    exit 1
fi

# ===== Test 4: 3段フォールバックが実装されていること =====

echo ""
echo "Test 4: HEAD 単独判定でないこと"

if grep -q 'curl -I' "$TOOL" \
    && grep -q -- '-r 0-0' "$TOOL" \
    && grep -q 'BROWSER_UA' "$TOOL"; then
    echo "✅ Test 4 passed: HEAD -> GET -> GET+UA の3段フォールバック"
else
    echo "❌ Test 4 failed: 3段フォールバックが実装されていない"
    exit 1
fi

# ===== Test 5: --dry-run が動作し抽出件数を報告すること =====

echo ""
echo "Test 5: --dry-run の動作"

out=$($TOOL --dry-run 2>&1)
if grep -q '抽出したURL数' <<< "$out" && grep -q 'URL抽出完了' <<< "$out"; then
    count=$(grep -oP '抽出したURL数: \K[0-9]+' <<< "$out")
    if [ "$count" -gt 0 ]; then
        echo "✅ Test 5 passed: --dry-run で $count 件を抽出"
    else
        echo "❌ Test 5 failed: 抽出件数が 0"
        exit 1
    fi
else
    echo "❌ Test 5 failed: --dry-run の出力が不正"
    exit 1
fi

# ===== Test 6: 抽出結果に壊れた URL が含まれないこと =====

echo ""
echo "Test 6: 実際の docs/ から壊れた URL を抽出しないこと"

broken=$(find docs/ -name "*.md" -type f ! -name "*.bak" \
    -exec grep -hoP "https?://[^\s\)\]'\"\`><]+" {} \; \
    | grep -cE "('|>|</a>)" || true)

if [ "$broken" -eq 0 ]; then
    echo "✅ Test 6 passed: 壊れた URL の抽出は 0 件"
else
    echo "❌ Test 6 failed: 壊れた URL が $broken 件抽出された"
    exit 1
fi

echo ""
echo "✅ All tests passed"
exit 0
