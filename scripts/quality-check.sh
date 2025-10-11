#!/bin/bash

# 品質チェックスクリプト
# 使用方法: ./scripts/quality-check.sh

echo "🔍 ドキュメント品質チェックを開始します..."

cd "$(dirname "$0")/.."

RESULT_FILE="quality-check-results.txt"
echo "品質チェック結果 - $(date)" > "$RESULT_FILE"
echo "=================================" >> "$RESULT_FILE"

ISSUES=0

echo "📄 Markdownファイルの基本チェック..."

# 1. 空のファイルチェック
echo "1. 空のファイルチェック" >> "$RESULT_FILE"
find docs -name "*.md" -empty | while read -r file; do
    echo "❌ 空のファイル: $file" | tee -a "$RESULT_FILE"
    ((ISSUES++))
done

# 2. タイトル（H1）の存在チェック
echo -e "\n2. H1タイトルの存在チェック" >> "$RESULT_FILE"
find docs -name "*.md" -type f | while read -r file; do
    if ! grep -q "^# " "$file"; then
        echo "⚠️  H1タイトルなし: $file" | tee -a "$RESULT_FILE"
        ((ISSUES++))
    fi
done

# 3. 長すぎる行のチェック（120文字以上）
echo -e "\n3. 長い行のチェック（120文字以上）" >> "$RESULT_FILE"
find docs -name "*.md" -type f | while read -r file; do
    long_lines=$(awk 'length > 120 {print NR ": " $0}' "$file")
    if [[ -n "$long_lines" ]]; then
        echo "⚠️  長い行あり: $file" >> "$RESULT_FILE"
        echo "$long_lines" | head -3 >> "$RESULT_FILE"
    fi
done

# 4. TODOやFIXMEの残存チェック
echo -e "\n4. TODO/FIXMEチェック" >> "$RESULT_FILE"
find docs -name "*.md" -type f -exec grep -Hn "TODO\|FIXME\|XXX" {} \; | while read -r match; do
    echo "⚠️  要対応項目: $match" | tee -a "$RESULT_FILE"
    ((ISSUES++))
done

# 5. 日本語文字化けチェック
echo -e "\n5. 文字エンコーディングチェック" >> "$RESULT_FILE"
find docs -name "*.md" -type f | while read -r file; do
    if ! file "$file" | grep -q "UTF-8"; then
        echo "❌ UTF-8以外: $file" | tee -a "$RESULT_FILE"
        ((ISSUES++))
    fi
done

echo ""
echo "📊 品質チェック完了!"
echo "発見された問題数: $ISSUES"

if [[ $ISSUES -eq 0 ]]; then
    echo "✅ 品質チェックに合格しました!"
    echo "✅ 品質チェックに合格しました!" >> "$RESULT_FILE"
else
    echo "⚠️  $ISSUES 個の問題が見つかりました。"
    echo "詳細は $RESULT_FILE を確認してください。"
fi
