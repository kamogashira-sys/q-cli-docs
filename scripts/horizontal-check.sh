#!/bin/bash

# 水平展開チェックスクリプト
# 使用方法: ./scripts/horizontal-check.sh

echo "🔍 修正項目の水平展開チェックを開始します..."

cd "$(dirname "$0")/.."

RESULT_FILE="horizontal-check-results.txt"
echo "水平展開チェック結果 - $(date)" > "$RESULT_FILE"
echo "=================================" >> "$RESULT_FILE"

ISSUES=0

echo "1. ログファイルパス関連の修正チェック..."

# 間違ったログファイルパスの残存確認
WRONG_LOG_PATHS=(
    "~/.aws/amazonq/logs/q-cli.log"
    "q-cli.log"
    "~/.aws/amazonq/logs/"
)

echo -e "\n1. 間違ったログファイルパスの残存確認" >> "$RESULT_FILE"
for wrong_path in "${WRONG_LOG_PATHS[@]}"; do
    matches=$(grep -r "$wrong_path" docs/ 2>/dev/null | grep -v "# 間違った場所" || true)
    if [[ -n "$matches" ]]; then
        echo "❌ 間違ったログパス残存: $wrong_path" | tee -a "$RESULT_FILE"
        echo "$matches" | head -3 >> "$RESULT_FILE"
        ((ISSUES++))
    else
        echo "✅ $wrong_path - 修正済み" >> "$RESULT_FILE"
    fi
done

echo "2. q doctor vs q diagnostic コマンドの使い分けチェック..."

# q doctorの間違った使用例
WRONG_DOCTOR_USAGE=(
    "q doctor.*--format"
    "q doctor.*json"
    "q doctor.*でログ"
)

echo -e "\n2. q doctorの間違った使用例チェック" >> "$RESULT_FILE"
for pattern in "${WRONG_DOCTOR_USAGE[@]}"; do
    matches=$(grep -r -E "$pattern" docs/ 2>/dev/null || true)
    if [[ -n "$matches" ]]; then
        echo "❌ 間違ったq doctor使用: $pattern" | tee -a "$RESULT_FILE"
        echo "$matches" | head -3 >> "$RESULT_FILE"
        ((ISSUES++))
    else
        echo "✅ $pattern - 問題なし" >> "$RESULT_FILE"
    fi
done

echo "3. 設定ファイルパス関連の修正チェック..."

# 間違った設定ファイルパス
WRONG_CONFIG_PATHS=(
    "~/.config/amazonq/settings.json"
    "~/.q/settings.json"
)

echo -e "\n3. 間違った設定ファイルパスチェック" >> "$RESULT_FILE"
for wrong_path in "${WRONG_CONFIG_PATHS[@]}"; do
    matches=$(grep -r "$wrong_path" docs/ 2>/dev/null | grep -v "# これらの場所は使用されません" || true)
    if [[ -n "$matches" ]]; then
        echo "❌ 間違った設定パス残存: $wrong_path" | tee -a "$RESULT_FILE"
        echo "$matches" | head -3 >> "$RESULT_FILE"
        ((ISSUES++))
    else
        echo "✅ $wrong_path - 適切に処理済み" >> "$RESULT_FILE"
    fi
done

echo "4. 正しいパスの一貫性チェック..."

# 正しいパスが一貫して使用されているかチェック
CORRECT_PATHS=(
    "~/.local/share/amazon-q/settings.json"
    "/run/user/\$(id -u)/qlog/qchat.log"
    "qchat.log"
)

echo -e "\n4. 正しいパスの一貫性チェック" >> "$RESULT_FILE"
for correct_path in "${CORRECT_PATHS[@]}"; do
    count=$(grep -r "$correct_path" docs/ 2>/dev/null | wc -l)
    echo "ℹ️  $correct_path: $count 箇所で使用" >> "$RESULT_FILE"
done

echo "5. コマンド使用例の一貫性チェック..."

# q diagnosticの正しい使用例があるかチェック
DIAGNOSTIC_USAGE=(
    "q diagnostic --format json"
    "q diagnostic --format json-pretty"
    "q diagnostic"
)

echo -e "\n5. q diagnosticの使用例チェック" >> "$RESULT_FILE"
for usage in "${DIAGNOSTIC_USAGE[@]}"; do
    count=$(grep -r "$usage" docs/ 2>/dev/null | wc -l)
    if [[ $count -gt 0 ]]; then
        echo "✅ $usage: $count 箇所で使用" >> "$RESULT_FILE"
    else
        echo "⚠️  $usage: 使用例なし" >> "$RESULT_FILE"
    fi
done

echo "6. 環境変数の一貫性チェック..."

# 環境変数の正しい記載
ENV_VARS=(
    "Q_LOG_LEVEL"
    "RUST_LOG"
    "Q_LOG_STDOUT"
)

echo -e "\n6. 環境変数の一貫性チェック" >> "$RESULT_FILE"
for env_var in "${ENV_VARS[@]}"; do
    count=$(grep -r "$env_var" docs/ 2>/dev/null | wc -l)
    echo "ℹ️  $env_var: $count 箇所で使用" >> "$RESULT_FILE"
done

echo "7. chatサブコマンド制限の記載チェック..."

# chatサブコマンドでのみログ出力される旨の記載
CHAT_RESTRICTION_PATTERNS=(
    "chatサブコマンド"
    "chat.*ログ"
    "ログ.*chat"
)

echo -e "\n7. chatサブコマンド制限の記載チェック" >> "$RESULT_FILE"
for pattern in "${CHAT_RESTRICTION_PATTERNS[@]}"; do
    count=$(grep -r -i -E "$pattern" docs/ 2>/dev/null | wc -l)
    echo "ℹ️  $pattern: $count 箇所で言及" >> "$RESULT_FILE"
done

echo ""
echo "📊 水平展開チェック完了!"
echo "発見された問題数: $ISSUES"

if [[ $ISSUES -eq 0 ]]; then
    echo "✅ 水平展開チェックに合格しました!"
    echo "✅ 水平展開チェックに合格しました!" >> "$RESULT_FILE"
else
    echo "❌ $ISSUES 個の問題が見つかりました。"
    echo "詳細は $RESULT_FILE を確認してください。"
fi

echo ""
echo "📝 チェック項目:"
echo "- 間違ったログファイルパスの残存"
echo "- q doctor vs q diagnostic の使い分け"
echo "- 設定ファイルパスの一貫性"
echo "- 正しいパスの使用状況"
echo "- コマンド使用例の一貫性"
echo "- 環境変数の記載状況"
echo "- chatサブコマンド制限の説明"
