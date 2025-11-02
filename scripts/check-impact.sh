#!/bin/bash
# check-impact.sh - 影響範囲分析
#
# 使用方法:
#   ./scripts/check-impact.sh [file]
#
# 機能:
#   - 変更されたファイルの影響範囲を分析
#   - ファイル内のキーワードを抽出
#   - 同じキーワードを含むファイルを検索

set -euo pipefail

echo "=== 影響範囲分析 ==="
echo ""

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

# 分析対象ファイルの決定
if [ $# -eq 1 ]; then
    # 引数で指定されたファイル
    changed_files="$1"
    echo "📝 指定されたファイルを分析: $changed_files"
else
    # Gitで変更されたファイル
    changed_files=$(git diff --name-only HEAD~1 2>/dev/null || echo "")
    
    if [ -z "$changed_files" ]; then
        echo "⚠️  変更されたファイルがありません"
        echo ""
        echo "使用方法:"
        echo "  ./scripts/check-impact.sh [file]"
        exit 0
    fi
    
    echo "📝 変更されたファイル:"
    echo "$changed_files" | sed 's/^/  - /'
fi

echo ""

# 各ファイルを分析
total_affected=0

while IFS= read -r file; do
    # ファイルが存在しない場合はスキップ
    if [ ! -f "$file" ]; then
        continue
    fi
    
    # Markdownファイルのみを対象
    if [[ ! "$file" =~ \.md$ ]]; then
        continue
    fi
    
    echo "🔍 分析中: $file"
    
    # ファイル内の重要なキーワードを抽出
    # - 大文字で始まる単語（固有名詞）
    # - 技術用語（Agent, MCP, Knowledge など）
    keywords=$(grep -oE '\b(Agent|MCP|Knowledge|Q CLI|Amazon Q Developer CLI|環境変数|設定|コマンド)\b' "$file" 2>/dev/null | sort -u || true)
    
    if [ -z "$keywords" ]; then
        echo "   キーワードなし"
        continue
    fi
    
    echo "   抽出したキーワード:"
    echo "$keywords" | sed 's/^/     - /'
    
    # 各キーワードについて影響範囲を検索
    while IFS= read -r keyword; do
        # 同じキーワードを含むファイルを検索（変更ファイル自身は除外）
        affected=$(grep -rl "$keyword" docs/ --include="*.md" 2>/dev/null | grep -v "^$file$" || true)
        
        if [ -n "$affected" ]; then
            count=$(echo "$affected" | wc -l)
            total_affected=$((total_affected + count))
            
            echo "   '$keyword' を含むファイル: $count 件"
            
            # 最初の3件のみ表示
            echo "$affected" | head -3 | sed 's/^/     - /'
            
            if [ "$count" -gt 3 ]; then
                echo "     ... 他 $((count - 3)) 件"
            fi
        fi
    done <<< "$keywords"
    
    echo ""
done <<< "$changed_files"

echo "=== 分析結果 ==="
echo "影響を受ける可能性のあるファイル: $total_affected 件"
echo ""

if [ $total_affected -gt 0 ]; then
    echo "⚠️  変更の影響範囲を確認してください"
    echo ""
    echo "推奨アクション:"
    echo "  1. 影響を受けるファイルをレビュー"
    echo "  2. 必要に応じて更新"
    echo "  3. 一貫性チェックを実行: ./scripts/check-consistency.sh"
else
    echo "✅ 影響範囲は限定的です"
fi
