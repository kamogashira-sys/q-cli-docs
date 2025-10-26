#!/bin/bash
# count-files.sh - ファイル数自動カウント
#
# 使用方法:
#   ./scripts/count-files.sh
#
# 機能:
#   - 全ファイル数のカウント
#   - カテゴリ別ファイル数のカウント
#   - README除外カウント

set -euo pipefail

echo "=== ファイル数カウント ==="
echo ""

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

# 全ファイル数
total=$(find docs -name "*.md" -type f 2>/dev/null | wc -l)
echo "全ファイル数: $total"
echo ""

# カテゴリ別
echo "カテゴリ別:"
for dir in docs/*/; do
    if [ -d "$dir" ]; then
        count=$(find "$dir" -name "*.md" -type f 2>/dev/null | wc -l)
        dirname=$(basename "$dir")
        echo "  $dirname: $count 文書"
    fi
done
echo ""

# README除外
total_no_readme=$(find docs -name "*.md" -type f ! -name "README.md" 2>/dev/null | wc -l)
echo "README除外: $total_no_readme 文書"
echo ""

# docs直下のファイル
docs_root=$(find docs -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)
echo "docs直下: $docs_root 文書"
