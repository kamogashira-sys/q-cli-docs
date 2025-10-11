#!/bin/bash

# リンク切れチェックスクリプト
# 使用方法: ./scripts/check-links.sh

echo "🔍 リンク切れチェックを開始します..."

# 作業ディレクトリを設定
cd "$(dirname "$0")/.."

# 結果ファイル
RESULT_FILE="link-check-results.txt"
echo "リンク切れチェック結果 - $(date)" > "$RESULT_FILE"
echo "=================================" >> "$RESULT_FILE"

# 内部リンクチェック
echo "📄 内部リンクをチェック中..."
BROKEN_LINKS=0

# Markdownファイル内のリンクを抽出してチェック
find docs -name "*.md" -type f | while read -r file; do
    echo "チェック中: $file"
    
    # 相対パスリンクを抽出
    grep -n "](.*\.md)" "$file" | while IFS=: read -r line_num link_line; do
        # リンクパスを抽出
        link_path=$(echo "$link_line" | sed -n 's/.*](\([^)]*\.md\)).*/\1/p')
        
        if [[ -n "$link_path" ]]; then
            # 相対パスを絶対パスに変換
            if [[ "$link_path" == /* ]]; then
                # 絶対パス
                full_path="$link_path"
            else
                # 相対パス
                dir_path=$(dirname "$file")
                full_path="$dir_path/$link_path"
            fi
            
            # ファイルの存在確認
            if [[ ! -f "$full_path" ]]; then
                echo "❌ BROKEN: $file:$line_num -> $link_path" | tee -a "$RESULT_FILE"
                ((BROKEN_LINKS++))
            fi
        fi
    done
done

echo ""
echo "📊 チェック完了!"
echo "壊れたリンク数: $BROKEN_LINKS"

if [[ $BROKEN_LINKS -eq 0 ]]; then
    echo "✅ すべてのリンクが正常です!"
    echo "✅ すべてのリンクが正常です!" >> "$RESULT_FILE"
else
    echo "⚠️  $BROKEN_LINKS 個の壊れたリンクが見つかりました。"
    echo "詳細は $RESULT_FILE を確認してください。"
fi
