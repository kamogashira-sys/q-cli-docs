#!/bin/bash
# check-notation.sh - kiro-docs コマンド・フラグ表記の禁止パターンチェック
#
# 使用方法:
#   ./scripts/kiro-docs/check-notation.sh
#
# 機能:
#   実機（kiro-cli 2.10.0, 2026-07-04 検証）に存在しない、または本プロジェクトの
#   標準表記に反するコマンド・フラグ表記の混入を検出する。
#
# 禁止パターンと正表記:
#   (a) --legacy-ui            → --classic
#       ※ chat サブコマンドでは --legacy-ui が正式名（--classic はエイリアス）だが、
#         トップレベル kiro-cli --help-all には --classic のみ存在するため、
#         両文脈で通用する --classic を本プロジェクトの標準表記とする
#   (b) kiro auth              → kiro-cli login（auth サブコマンドは存在しない）
#   (c) settings set KEY       → kiro-cli settings KEY VALUE（set サブコマンドは存在しない）
#   (d) kiro chat / kiro login → kiro-cli chat / kiro-cli login
#       （`kiro` 単体は kiro-command-router 導入後のみ有効）
#
# 設計メモ:
#   - 除外: .bak / *_update_plan.md / 06_embedded-docs / 05_meta（手順書・テンプレ・事例集）
#     （check-consistency.sh と同一の除外ルール）
#   - `kiro chat` の検索は `kiro-cli chat` に誤マッチしない（`kiro` 直後が `-` のため）

set -euo pipefail

cd "$(dirname "$0")/../.."

echo "=== kiro-docs コマンド表記チェック ==="
echo ""

errors=0

exclude_paths() {
    grep -v '\.bak' \
        | grep -v '_update_plan' \
        | grep -v '06_embedded-docs' \
        | grep -v 'kiro-docs/05_meta'
}

check_pattern() {
    local pattern="$1"
    local correct="$2"
    local hits
    hits=$(grep -rnE --include="*.md" -e "$pattern" kiro-docs/ README.md \
        | exclude_paths || true)
    if [ -n "$hits" ]; then
        echo "❌ 禁止パターン '$pattern' を検出（正表記: $correct）:"
        echo "$hits" | sed 's/^/     /'
        errors=$((errors + 1))
    fi
}

echo "🔍 (a) --legacy-ui（標準表記は --classic）を検証中..."
check_pattern '\-\-legacy-ui' '--classic'

echo "🔍 (b) kiro auth（存在しないサブコマンド）を検証中..."
check_pattern 'kiro(-cli)? auth' 'kiro-cli login'

echo "🔍 (c) settings set（存在しないサブコマンド）を検証中..."
check_pattern 'settings set [a-zA-Z]' 'kiro-cli settings KEY VALUE'

echo "🔍 (d) kiro 単体コマンド（kiro chat / kiro login 等）を検証中..."
check_pattern 'kiro (chat|login|logout|settings|agent|mcp|update|doctor)\b' 'kiro-cli <subcommand>'

echo ""
echo "=== チェック結果 ==="
echo "検出カテゴリ数: $errors"

if [ "$errors" -gt 0 ]; then
    echo ""
    echo "❌ コマンド表記チェックに失敗しました"
    exit 1
else
    echo ""
    echo "✅ コマンド表記は問題ありません"
    exit 0
fi
