#!/bin/bash

# 公開前最終チェックスクリプト
# 使用方法: ./scripts/final-check.sh

echo "🔍 公開前最終チェックを開始します..."

cd "$(dirname "$0")/.."

RESULT_FILE="final-check-results.txt"
echo "公開前最終チェック結果 - $(date)" > "$RESULT_FILE"
echo "=================================" >> "$RESULT_FILE"

ISSUES=0

echo "1. 必須ファイルの存在確認..."
REQUIRED_FILES=(
    "LICENSE"
    "README.md"
    "CODE_OF_CONDUCT.md"
    "docs/CONTRIBUTING.md"
    ".github/ISSUE_TEMPLATE/bug_report.yml"
    ".github/ISSUE_TEMPLATE/feature_request.yml"
    ".github/pull_request_template.md"
    "docs/_config.yml"
    "docs/index.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "❌ 必須ファイル不足: $file" | tee -a "$RESULT_FILE"
        ((ISSUES++))
    else
        echo "✅ $file" >> "$RESULT_FILE"
    fi
done

echo -e "\n2. 機密情報チェック..."
SENSITIVE_PATTERNS=(
    "password"
    "secret"
    "api_key"
    "token"
    "credential"
    "private_key"
)

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    matches=$(find . -type f -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.sh" | xargs grep -i "$pattern" 2>/dev/null || true)
    if [[ -n "$matches" ]]; then
        echo "⚠️  機密情報の可能性: $pattern" | tee -a "$RESULT_FILE"
        echo "$matches" | head -3 >> "$RESULT_FILE"
    fi
done

echo -e "\n3. 免責事項・ライセンス確認..."
if ! grep -q "非公式" README.md; then
    echo "❌ 免責事項不足: README.md" | tee -a "$RESULT_FILE"
    ((ISSUES++))
fi

if ! grep -q "MIT License" README.md; then
    echo "❌ ライセンス表記不足: README.md" | tee -a "$RESULT_FILE"
    ((ISSUES++))
fi

echo -e "\n4. リンク切れチェック実行..."
./scripts/check-links.sh > /dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "⚠️  リンクチェックでエラー" | tee -a "$RESULT_FILE"
fi

echo -e "\n5. 品質チェック実行..."
./scripts/quality-check.sh > /dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "⚠️  品質チェックでエラー" | tee -a "$RESULT_FILE"
fi

echo -e "\n6. Git状態確認..."
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  未コミットの変更あり" | tee -a "$RESULT_FILE"
    git status --porcelain >> "$RESULT_FILE"
fi

echo -e "\n7. ファイルサイズチェック..."
large_files=$(find . -type f -size +1M -not -path "./.git/*")
if [[ -n "$large_files" ]]; then
    echo "⚠️  大きなファイル（1MB以上）:" | tee -a "$RESULT_FILE"
    echo "$large_files" >> "$RESULT_FILE"
fi

echo ""
echo "📊 最終チェック完了!"
echo "発見された問題数: $ISSUES"

if [[ $ISSUES -eq 0 ]]; then
    echo "✅ 公開準備完了！すべてのチェックに合格しました。"
    echo "✅ 公開準備完了！" >> "$RESULT_FILE"
else
    echo "⚠️  $ISSUES 個の問題が見つかりました。"
    echo "詳細は $RESULT_FILE を確認してください。"
fi
