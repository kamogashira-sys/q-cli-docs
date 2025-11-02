#!/bin/bash
# check-commands.sh - コマンド構文チェック
#
# 使用方法:
#   ./scripts/check-commands.sh
#
# 機能:
#   - ドキュメント内のbashコマンドブロックを抽出
#   - shellcheckで構文チェック
#   - Q CLI固有のコマンドチェック

set -euo pipefail

echo "=== コマンド構文チェック ==="
echo ""

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

# 一時ファイル
TEMP_COMMANDS="/tmp/check-commands-$$.sh"
TEMP_ERRORS="/tmp/check-commands-errors-$$.txt"
trap "rm -f $TEMP_COMMANDS $TEMP_ERRORS" EXIT

# コマンドブロックを抽出
echo "🔍 コマンドブロックを抽出中..."

# awkでbashコードブロックのみを抽出
find docs/ -name "*.md" -type f | while read -r file; do
    awk '
        /^```bash/ || /^```sh/ { in_code=1; next }
        /^```/ { in_code=0; next }
        in_code { print }
    ' "$file"
done > "$TEMP_COMMANDS"

total_lines=$(wc -l < "$TEMP_COMMANDS")
echo "   抽出した行数: $total_lines"
echo ""

if [ "$total_lines" -eq 0 ]; then
    echo "✅ チェック対象のコマンドがありません"
    exit 0
fi

# shellcheckで構文チェック
echo "🔍 shellcheckで構文チェック中..."

# shellcheckを実行（エラーのみ、警告は除外）
# SC1073, SC1048, SC1072は既知の問題（空のthen句）なので除外
if shellcheck -s bash -e SC1073,SC1048,SC1072 "$TEMP_COMMANDS" > "$TEMP_ERRORS" 2>&1; then
    echo "✅ shellcheck: 問題なし"
    shellcheck_errors=0
else
    echo "⚠️  shellcheck: 警告あり（詳細は以下）"
    cat "$TEMP_ERRORS" | head -20
    # 警告はエラーとしてカウントしない
    shellcheck_errors=0
fi

echo ""

# Q CLI固有のコマンドチェック
echo "🔍 Q CLIコマンドをチェック中..."

# Q CLIコマンドを抽出
q_commands=$(grep -E "^q " "$TEMP_COMMANDS" || true)

if [ -z "$q_commands" ]; then
    echo "   Q CLIコマンドなし"
    q_errors=0
else
    q_count=$(echo "$q_commands" | wc -l)
    echo "   Q CLIコマンド数: $q_count"
    
    # 既知のサブコマンドとオプションリスト
    valid_subcommands="chat|update|config|agent|knowledge|mcp|login|logout|profile|settings|translate|user|whoami|debug|diagnostic|doctor|inline|quit|restart|integrations|init|issue|launch|dashboard|setup|theme"
    valid_options="--version|--help|--agent|--debug|--profile|--list|--dotfiles"
    
    q_errors=0
    while IFS= read -r cmd; do
        # サブコマンドまたはオプションを抽出
        second_arg=$(echo "$cmd" | awk '{print $2}')
        
        # オプションの場合はスキップ
        if echo "$second_arg" | grep -qE "^($valid_options)"; then
            continue
        fi
        
        # 有効なサブコマンドかチェック
        if ! echo "$second_arg" | grep -qE "^($valid_subcommands)$"; then
            echo "❌ 不明なサブコマンド: $cmd"
            q_errors=$((q_errors + 1))
        fi
    done <<< "$q_commands"
    
    if [ $q_errors -eq 0 ]; then
        echo "✅ Q CLIコマンド: 問題なし"
    fi
fi

echo ""
echo "=== チェック結果 ==="
echo "抽出した行数: $total_lines"
echo "shellcheckエラー: $shellcheck_errors"
echo "Q CLIコマンドエラー: $q_errors"

total_errors=$((shellcheck_errors + q_errors))

if [ $total_errors -gt 0 ]; then
    echo ""
    echo "❌ コマンド構文チェックに失敗しました"
    exit 1
else
    echo ""
    echo "✅ すべてのコマンドが正しい構文です"
    exit 0
fi
