#!/bin/bash
# search-env-var.sh - 環境変数検索
#
# 使用方法:
#   ./scripts/search-env-var.sh ENV_VAR_NAME
#
# 機能:
#   - 環境変数の使用箇所検索
#   - 使用箇所数のカウント
#   - 削除可否の判定

set -euo pipefail

ENV_VAR=$1

if [ -z "$ENV_VAR" ]; then
    echo "Usage: $0 ENV_VAR_NAME"
    echo ""
    echo "例:"
    echo "  $0 Q_LOG_STDOUT"
    echo "  $0 Q_TELEMETRY_ENABLED"
    exit 1
fi

echo "=== 環境変数検索: $ENV_VAR ==="
echo ""

# Q CLIリポジトリのパスを確認
if [ ! -d "$HOME/repos/amazon-q-developer-cli" ]; then
    echo "⚠️  Q CLIリポジトリが見つかりません"
    echo "   パス: $HOME/repos/amazon-q-developer-cli"
    echo ""
    echo "リポジトリをクローンしてください:"
    echo "  git clone https://github.com/aws/amazon-q-developer-cli.git $HOME/repos/amazon-q-developer-cli"
    exit 1
fi

cd "$HOME/repos/amazon-q-developer-cli"

# 実装全体を検索
echo "実装での使用箇所:"
if rg "$ENV_VAR" --type rust 2>/dev/null; then
    echo ""
else
    echo "（使用箇所なし）"
    echo ""
fi

# 使用箇所数
count=$(rg "$ENV_VAR" --type rust 2>/dev/null | wc -l)
echo "使用箇所数: $count"
echo ""

# 削除可否判定
if [ $count -eq 0 ]; then
    echo "✅ 削除可能（使用箇所なし）"
    exit 0
else
    echo "❌ 削除不可（使用箇所あり）"
    echo ""
    echo "削除前に全ての使用箇所を確認してください"
    exit 1
fi
