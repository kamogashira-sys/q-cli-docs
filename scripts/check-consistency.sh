#!/bin/bash
# check-consistency.sh - 一貫性チェック
#
# 使用方法:
#   ./scripts/check-consistency.sh
#
# 機能:
#   - 重要な用語、パス、コマンドの表記揺れを検出
#   - 統一すべき表記の不一致を報告

set -euo pipefail

echo "=== 一貫性チェック ==="
echo ""

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

errors=0
total_checks=0

# チェック1: Q CLIの表記揺れ
echo "🔍 チェック中: Q CLI表記"
total_checks=$((total_checks + 1))

# Q-CLI や q-cli（除外パターン以外）を検索
matches=$(grep -rn -E '\bQ-CLI\b|\bq-cli\b' docs/ --include="*.md" | \
    grep -v "q-cli-docs" | \
    grep -v "q-cli.log" | \
    grep -v "q-cli-v" | \
    grep -v "q-cli@" | \
    grep -v "/q-cli-" | \
    grep -v "#.*q-cli" || true)

if [ -n "$matches" ]; then
    echo "❌ 不一致を検出: Q CLI"
    echo "   正しい表記: 'Q CLI' または 'q-cli-docs'（プロジェクト名）"
    echo "   誤った表記が見つかりました:"
    echo "$matches" | head -5 | sed 's/^/     /'
    
    count=$(echo "$matches" | wc -l)
    if [ "$count" -gt 5 ]; then
        echo "     ... 他 $((count - 5)) 件"
    fi
    
    errors=$((errors + 1))
    echo ""
fi

# チェック2: Agent設定パスの表記揺れ
echo "🔍 チェック中: Agent設定パス"
total_checks=$((total_checks + 1))

# 誤ったパス表記を検索（例示とツールドキュメントを除く）
matches=$(grep -rn -E '~/.amazonq/agents|~/.config/amazonq/agents' docs/ --include="*.md" | \
    grep -v "例:" | \
    grep -v "例）" | \
    grep -v "05_automation-tools.md" || true)

if [ -n "$matches" ]; then
    echo "❌ 不一致を検出: Agent設定パス"
    echo "   正しい表記: '~/.aws/amazonq/cli-agents'"
    echo "   誤った表記が見つかりました:"
    echo "$matches" | head -5 | sed 's/^/     /'
    
    count=$(echo "$matches" | wc -l)
    if [ "$count" -gt 5 ]; then
        echo "     ... 他 $((count - 5)) 件"
    fi
    
    errors=$((errors + 1))
    echo ""
fi

# チェック3: Amazon Q Developer CLIの表記揺れ
echo "🔍 チェック中: Amazon Q Developer CLI表記"
total_checks=$((total_checks + 1))

# 誤った表記を検索（ツールドキュメントと用語辞書を除く）
matches=$(grep -rn -E '\bAmazon Q CLI\b|\bAmazonQ CLI\b' docs/ --include="*.md" | \
    grep -v "05_automation-tools.md" | \
    grep -v "06_terminology-dictionary.md" || true)

if [ -n "$matches" ]; then
    echo "❌ 不一致を検出: Amazon Q Developer CLI"
    echo "   正しい表記: 'Amazon Q Developer CLI'"
    echo "   誤った表記が見つかりました:"
    echo "$matches" | head -5 | sed 's/^/     /'
    
    count=$(echo "$matches" | wc -l)
    if [ "$count" -gt 5 ]; then
        echo "     ... 他 $((count - 5)) 件"
    fi
    
    errors=$((errors + 1))
    echo ""
fi

# チェック4: コマンド表記の揺れ（q chat vs q-chat）
echo "🔍 チェック中: コマンド表記"
total_checks=$((total_checks + 1))

# q-chat（ハイフン付き）を検索（例示、アンカーリンク、ツールドキュメントを除く）
matches=$(grep -rn -E '\bq-chat\b' docs/ --include="*.md" | \
    grep -v "例:" | \
    grep -v "例）" | \
    grep -v "#q-chat" | \
    grep -v "05_automation-tools.md" || true)

if [ -n "$matches" ]; then
    echo "❌ 不一致を検出: コマンド表記"
    echo "   正しい表記: 'q chat'（スペース区切り）"
    echo "   誤った表記が見つかりました:"
    echo "$matches" | head -5 | sed 's/^/     /'
    
    count=$(echo "$matches" | wc -l)
    if [ "$count" -gt 5 ]; then
        echo "     ... 他 $((count - 5)) 件"
    fi
    
    errors=$((errors + 1))
    echo ""
fi

echo "=== チェック結果 ==="
echo "チェック項目: $total_checks"
echo "不一致: $errors"

if [ $errors -gt 0 ]; then
    echo ""
    echo "❌ 一貫性チェックに失敗しました"
    exit 1
else
    echo ""
    echo "✅ すべての表記が一貫しています"
    exit 0
fi
