#!/bin/bash
# check-dates.sh - 日付整合性チェック
#
# 使用方法:
#   ./scripts/check-dates.sh
#
# 機能:
#   - Git更新日とドキュメント内日付の比較
#   - 不一致の検出
#   - 不一致リストの出力

set -euo pipefail

echo "=== 日付整合性チェック ==="
echo ""

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

errors=0
checked=0

find docs -name "*.md" -type f | while read file; do
    # Git更新日
    git_date=$(git log -1 --format="%ad" --date=format:"%Y-%m-%d" -- "$file" 2>/dev/null || echo "")
    
    if [ -z "$git_date" ]; then
        continue
    fi
    
    # ドキュメント内の日付（複数パターン対応）
    doc_date=$(grep -E "(最終更新|最終更新日):? [0-9]{4}-[0-9]{2}-[0-9]{2}" "$file" 2>/dev/null | tail -1 | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}" || echo "")
    
    if [ -z "$doc_date" ]; then
        continue
    fi
    
    checked=$((checked + 1))
    
    # 比較
    if [ "$git_date" != "$doc_date" ]; then
        echo "❌ $file"
        echo "   Git: $git_date, Doc: $doc_date"
        errors=$((errors + 1))
    fi
done

echo ""
echo "チェック対象: $checked ファイル"

if [ $errors -eq 0 ]; then
    echo "✅ 全ての日付が一致しています"
    exit 0
else
    echo "❌ $errors 件の不一致があります"
    exit 1
fi
