#!/bin/bash
# check-changelog.sh - kiro-docs changelog 構造チェック
#
# 使用方法:
#   ./scripts/kiro-docs/check-changelog.sh
#
# 機能:
#   1. `### vX.Y.Z` セクションが降順（新しい順）に並んでいるか
#   2. 各バージョン見出しに `（YYYY-MM-DD）` の日付があるか
#   3. 件数注記 `**カテゴリ（N件）**:` の N と直後の箇条書き（`- ` 行）数が一致するか
#      （注記のない節はスキップ。カテゴリ: 機能追加/改善/バグ修正/セキュリティ 等）

set -euo pipefail

cd "$(dirname "$0")/../.."

CHANGELOG="kiro-docs/02_update/01_changelog.md"

echo "=== kiro-docs changelog 構造チェック ==="
echo ""

errors=0

# ---- 1. セクション順序（降順） ----
echo "🔍 セクション順序（降順）を検証中..."
versions=$(grep -oE '^### v[0-9]+\.[0-9]+\.[0-9]+' "$CHANGELOG" | sed 's/^### //')
sorted=$(echo "$versions" | sort -rV)
if [ "$versions" != "$sorted" ]; then
    echo "❌ バージョンセクションが降順ではありません:"
    echo "   実際の順序: $(echo "$versions" | tr '\n' ' ')"
    echo "   期待(降順): $(echo "$sorted" | tr '\n' ' ')"
    errors=$((errors + 1))
fi

# ---- 2. 日付書式 ----
echo "🔍 バージョン見出しの日付書式を検証中..."
bad_dates=$(grep -nE '^### v[0-9]+\.[0-9]+\.[0-9]+' "$CHANGELOG" \
    | grep -vE '（[0-9]{4}-[0-9]{2}-[0-9]{2}）' || true)
if [ -n "$bad_dates" ]; then
    echo "❌ 日付書式（YYYY-MM-DD）が無い見出し:"
    echo "$bad_dates" | sed 's/^/     /'
    errors=$((errors + 1))
fi

# ---- 3. カテゴリ件数 vs 箇条書き数 ----
echo "🔍 カテゴリ件数と箇条書き数の一致を検証中..."
mismatch=$(awk '
    function flush() {
        if (cat != "" && cnt != declared) {
            printf "  宣言 %d件 / 実際 %d件: %s\n", declared, cnt, cat
        }
    }
    /^### / { flush(); cat=""; next }
    /^\*\*/ {
        flush()
        if ($0 ~ /（[0-9]+件）\*\*:/) {
            cat=$0
            d=$0; sub(/件）.*/, "", d); sub(/.*（/, "", d); declared=d+0
            cnt=0
        } else {
            cat=""   # 注記/出典/主要な変更 等の非カテゴリ見出し
        }
        next
    }
    /^- / { if (cat != "") cnt++ }
    END { flush() }
' "$CHANGELOG")
if [ -n "$mismatch" ]; then
    echo "❌ カテゴリ件数と箇条書き数の不一致:"
    echo "$mismatch" | sed 's/^/   /'
    errors=$((errors + 1))
fi

echo ""
echo "=== チェック結果 ==="
echo "バージョンセクション数: $(echo "$versions" | grep -c . )"
echo "不一致カテゴリ数: $errors"

if [ "$errors" -gt 0 ]; then
    echo ""
    echo "❌ changelog 構造チェックに失敗しました"
    exit 1
else
    echo ""
    echo "✅ changelog 構造は健全です"
    exit 0
fi
