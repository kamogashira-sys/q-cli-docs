#!/bin/bash

OUTPUT_FILE="work_records/20251011/all_links_before.csv"

echo "SourceFile,LinkText,LinkTarget,LineNumber" > "$OUTPUT_FILE"

cd docs

find . -name "*.md" -type f | sort | while read file; do
    grep -n '\[.*\](.*\.md)' "$file" 2>/dev/null | while IFS=: read line_num content; do
        echo "$content" | grep -oP '\[.*?\]\(.*?\.md\)' | while read link; do
            text=$(echo "$link" | sed -n 's/\[\(.*\)\](.*/\1/p')
            target=$(echo "$link" | sed -n 's/.*\](\(.*\))/\1/p')
            echo "\"$file\",\"$text\",\"$target\",$line_num"
        done
    done
done >> "$OUTPUT_FILE"

echo "リンク抽出完了: $OUTPUT_FILE"
wc -l "$OUTPUT_FILE"
