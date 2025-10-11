#!/bin/bash

OUTPUT_FILE="work_records/20251011/file_move_mapping.csv"

echo "OldPath,NewPath,Category" > "$OUTPUT_FILE"

cd docs

# for-users/への移動
find getting-started -name "*.md" -type f 2>/dev/null | while read file; do
    new_path="for-users/$file"
    echo "\"$file\",\"$new_path\",\"for-users\"" >> "../$OUTPUT_FILE"
done

find user-guide/configuration -name "*.md" -type f 2>/dev/null | while read file; do
    new_path=$(echo "$file" | sed 's|user-guide/|for-users/|')
    echo "\"$file\",\"$new_path\",\"for-users\"" >> "../$OUTPUT_FILE"
done

find user-guide/features -name "*.md" -type f 2>/dev/null | while read file; do
    new_path=$(echo "$file" | sed 's|user-guide/|for-users/|')
    echo "\"$file\",\"$new_path\",\"for-users\"" >> "../$OUTPUT_FILE"
done

find user-guide/best-practices -name "*.md" -type f 2>/dev/null | while read file; do
    new_path=$(echo "$file" | sed 's|user-guide/|for-users/|')
    echo "\"$file\",\"$new_path\",\"for-users\"" >> "../$OUTPUT_FILE"
done

find user-guide/troubleshooting -name "*.md" -type f 2>/dev/null | while read file; do
    new_path=$(echo "$file" | sed 's|user-guide/|for-users/|')
    echo "\"$file\",\"$new_path\",\"for-users\"" >> "../$OUTPUT_FILE"
done

if [ -f "user-guide/enterprise-deployment.md" ]; then
    echo "\"user-guide/enterprise-deployment.md\",\"for-users/deployment/enterprise-deployment.md\",\"for-users\"" >> "../$OUTPUT_FILE"
fi

find reference -name "*.md" -type f 2>/dev/null | while read file; do
    new_path="for-users/$file"
    echo "\"$file\",\"$new_path\",\"for-users\"" >> "../$OUTPUT_FILE"
done

# for-developers/への移動
find developer-guide -name "*.md" -type f 2>/dev/null | while read file; do
    new_path=$(echo "$file" | sed 's|developer-guide|for-developers|')
    echo "\"$file\",\"$new_path\",\"for-developers\"" >> "../$OUTPUT_FILE"
done

# for-community/への移動
find updates -name "*.md" -type f 2>/dev/null | while read file; do
    new_path="for-community/$file"
    echo "\"$file\",\"$new_path\",\"for-community\"" >> "../$OUTPUT_FILE"
done

find community -name "*.md" -type f 2>/dev/null | while read file; do
    new_path="for-community/$file"
    echo "\"$file\",\"$new_path\",\"for-community\"" >> "../$OUTPUT_FILE"
done

find analysis -name "*.md" -type f 2>/dev/null | while read file; do
    new_path="for-community/$file"
    echo "\"$file\",\"$new_path\",\"for-community\"" >> "../$OUTPUT_FILE"
done

# meta/への移動
for file in CONTRIBUTING.md QUALITY_ASSURANCE.md IMPLEMENTATION_VERIFICATION_CHECKLIST.md VERIFICATION_CHECKLIST.md; do
    if [ -f "$file" ]; then
        echo "\"$file\",\"meta/$file\",\"meta\"" >> "../$OUTPUT_FILE"
    fi
done

cd ..
echo "移動マッピング作成完了: $OUTPUT_FILE"
wc -l "$OUTPUT_FILE"
