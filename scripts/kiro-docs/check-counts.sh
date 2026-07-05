#!/bin/bash
# check-counts.sh - kiro-docs 数値整合チェック（機能数・コマンド数の水平展開）
#
# 使用方法:
#   ./scripts/kiro-docs/check-counts.sh
#
# 機能:
#   - 機能数の正準値 = kiro-docs/01_features/README.md の機能テーブル行数
#   - コマンド数の正準値 = kiro-docs/04_reference/02_slash-commands.md の `### /...` 見出し数
#   - 各所の「N機能」「スラッシュコマンドN種 / 全Nコマンド」記述が正準値と一致するか検証
#   - 過去に繰り返した水平展開漏れ（機能数・コマンド数）を 0 にすることが目的
#
# 設計メモ:
#   - 「N機能」はカテゴリ/サブセット件数や別概念も混在するため、明確な非総数表現は allowlist で除外
#   - CLI コマンド数「16種/全16コマンド」はスラッシュコマンドと別概念なので対象外

set -euo pipefail

# scripts/kiro-docs/ -> リポジトリルート（2階層上）
cd "$(dirname "$0")/../.."

echo "=== kiro-docs 数値整合チェック（機能数・コマンド数） ==="
echo ""

FEATURE_TABLE="kiro-docs/01_features/README.md"
SLASH_DOC="kiro-docs/04_reference/02_slash-commands.md"

errors=0

# 走査対象から除外するパス（grep の出力行に対して適用）
exclude_paths() {
    grep -v '\.bak' \
        | grep -v '_update_plan' \
        | grep -v '06_embedded-docs' \
        | grep -v 'kiro-docs/05_meta'
}

# 総数ではない「N機能」（カテゴリ/サブセット/別概念）の許可パターン
allow_feature_nontotal() {
    grep -vE '以下 [0-9]+ ?機能' \
        | grep -vE '将来予定の [0-9]+ ?機能'
}

# ---- 1. 機能数 ----
echo "🔍 機能数の正準値を抽出中..."
FEATURE_COUNT=$(grep -cE '^\|.*\]\([0-9]{2}_[^)]+\.md\)' "$FEATURE_TABLE")
echo "   正準値（機能テーブル行数）= $FEATURE_COUNT"

echo "🔍 「N機能」記述を検証中..."
feature_lines=$(grep -rnE '[0-9]+ ?機能' kiro-docs/ README.md --include="*.md" \
    | exclude_paths | allow_feature_nontotal || true)

feature_bad=""
if [ -n "$feature_lines" ]; then
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        # 行中の「N機能」をすべて取り出して数値比較
        nums=$(echo "$line" | grep -oE '[0-9]+ ?機能' | grep -oE '[0-9]+')
        for n in $nums; do
            if [ "$n" != "$FEATURE_COUNT" ]; then
                feature_bad+="$line"$'\n'
                break
            fi
        done
    done <<< "$feature_lines"
fi

if [ -n "$feature_bad" ]; then
    echo "❌ 機能数の不一致（正準値 $FEATURE_COUNT と異なる「N機能」）:"
    echo "$feature_bad" | sed '/^$/d' | sed 's/^/     /'
    errors=$((errors + 1))
fi
echo ""

# ---- 2. コマンド数 ----
echo "🔍 コマンド数の正準値を抽出中..."
CMD_COUNT=$(grep -cE '^### `/' "$SLASH_DOC")
echo "   正準値（スラッシュコマンド見出し数）= $CMD_COUNT"

echo "🔍 コマンド数記述を検証中..."
# (A) 「スラッシュコマンドN種」を全スコープから
cmd_lines_a=$(grep -rnE 'スラッシュコマンド[（(]?[0-9]+ ?種' kiro-docs/ README.md --include="*.md" \
    | exclude_paths || true)
# (B) 「全Nコマンド」は 02_slash-commands.md（本文の件数根拠）に限定
cmd_lines_b=$(grep -nE '全 ?[0-9]+ ?コマンド' "$SLASH_DOC" | sed "s#^#$SLASH_DOC:#" || true)

cmd_bad=""
for block in "$cmd_lines_a" "$cmd_lines_b"; do
    [ -z "$block" ] && continue
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        nums=$(echo "$line" | grep -oE '[0-9]+ ?(種|コマンド)' | grep -oE '[0-9]+')
        for n in $nums; do
            if [ "$n" != "$CMD_COUNT" ]; then
                cmd_bad+="$line"$'\n'
                break
            fi
        done
    done <<< "$block"
done

if [ -n "$cmd_bad" ]; then
    echo "❌ コマンド数の不一致（正準値 $CMD_COUNT と異なる記述）:"
    echo "$cmd_bad" | sed '/^$/d' | sed 's/^/     /'
    errors=$((errors + 1))
fi
echo ""

# ---- 結果 ----
echo "=== チェック結果 ==="
echo "機能数の正準値: $FEATURE_COUNT / コマンド数の正準値: $CMD_COUNT"
echo "不一致カテゴリ数: $errors"

if [ "$errors" -gt 0 ]; then
    echo ""
    echo "❌ 数値整合チェックに失敗しました"
    exit 1
else
    echo ""
    echo "✅ 機能数・コマンド数は全箇所で正準値と一致しています"
    exit 0
fi
