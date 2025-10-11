#!/bin/bash

set -e

MAPPING_FILE="work_records/20251011/file_move_mapping.csv"
LOG_FILE="work_records/20251011/move_log.txt"

echo "=== ファイル移動開始 ===" | tee "$LOG_FILE"
echo "開始時刻: $(date)" | tee -a "$LOG_FILE"

cd docs

# CSVを読み込んで移動
tail -n +2 "../$MAPPING_FILE" | while IFS=, read -r old_path new_path category; do
    # クォートを削除
    old_path=$(echo "$old_path" | tr -d '"')
    new_path=$(echo "$new_path" | tr -d '"')
    
    if [ -f "$old_path" ]; then
        # 移動先ディレクトリを作成
        mkdir -p "$(dirname "$new_path")"
        
        # ファイル移動
        mv "$old_path" "$new_path"
        echo "MOVED: $old_path -> $new_path" | tee -a "../$LOG_FILE"
    else
        echo "SKIP: $old_path (not found)" | tee -a "../$LOG_FILE"
    fi
done

cd ..
echo "=== ファイル移動完了 ===" | tee -a "$LOG_FILE"
echo "完了時刻: $(date)" | tee -a "$LOG_FILE"
