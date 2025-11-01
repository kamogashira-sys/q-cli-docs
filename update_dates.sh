#!/bin/bash
# update_dates.sh - Git最終更新日に基づいてドキュメント日付を更新

set -e

# 作業ディレクトリ
DOCS_DIR="docs"
LOG_FILE="/tmp/date_update_log.txt"

echo "=== 日付更新開始 ===" > "$LOG_FILE"
echo "開始時刻: $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

updated_count=0

# 更新対象ファイルを取得（05_metaを除外）
find "$DOCS_DIR" -name "*.md" -type f | grep -v "05_meta" | while read -r file; do
  # Git最終更新日を取得
  git_date=$(git log -1 --format=%cd --date=short "$file" 2>/dev/null)
  
  if [ -z "$git_date" ]; then
    echo "⚠️  Git日付取得失敗: $file" >> "$LOG_FILE"
    continue
  fi
  
  # ドキュメント記載日を取得（複数パターン対応）
  doc_date=$(grep -E '\*\*最終更新\*\*: [0-9]{4}-[0-9]{2}-[0-9]{2}' "$file" | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' || echo "")
  
  if [ -z "$doc_date" ]; then
    # 別パターンを試す
    doc_date=$(grep -E '最終更新: [0-9]{4}-[0-9]{2}-[0-9]{2}' "$file" | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' || echo "")
  fi
  
  if [ -z "$doc_date" ]; then
    echo "⚠️  ドキュメント日付なし: $file" >> "$LOG_FILE"
    continue
  fi
  
  # 日付が一致しない場合のみ更新
  if [ "$git_date" != "$doc_date" ]; then
    echo "📝 更新: $file" >> "$LOG_FILE"
    echo "   Git: $git_date, Doc: $doc_date" >> "$LOG_FILE"
    
    # 日付を更新
    sed -i "s/\*\*最終更新\*\*: ${doc_date}/\*\*最終更新\*\*: ${git_date}/" "$file"
    sed -i "s/最終更新: ${doc_date}/最終更新: ${git_date}/" "$file"
    
    echo "   → 更新完了" >> "$LOG_FILE"
    updated_count=$((updated_count + 1))
  fi
done

echo "" >> "$LOG_FILE"
echo "=== 日付更新完了 ===" >> "$LOG_FILE"
echo "更新ファイル数: $updated_count" >> "$LOG_FILE"
echo "完了時刻: $(date)" >> "$LOG_FILE"

# ログを表示
cat "$LOG_FILE"
