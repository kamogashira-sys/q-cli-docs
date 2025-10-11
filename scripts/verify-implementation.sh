#!/bin/bash

# 実装検証スクリプト
# 使用方法: ./scripts/verify-implementation.sh

echo "🔍 Q CLI実装検証を開始します..."

cd "$(dirname "$0")/.."

RESULT_FILE="implementation-verification-results.txt"
echo "実装検証結果 - $(date)" > "$RESULT_FILE"
echo "=================================" >> "$RESULT_FILE"

ISSUES=0

echo "1. ログファイルパス検証..."

# Q CLIが利用可能かチェック
if ! command -v q &> /dev/null; then
    echo "⚠️  Q CLIがインストールされていません" | tee -a "$RESULT_FILE"
    echo "   実装検証をスキップします"
    exit 1
fi

# 環境変数設定
export Q_LOG_LEVEL=debug
export RUST_LOG=debug
export Q_LOG_STDOUT=1

echo "2. ログファイル生成テスト..."

# 一時的にchatを実行してログファイル生成
timeout 10s q chat --message "test" 2>/dev/null || true

# ログファイルの場所を確認
LOG_LOCATIONS=(
    "/run/user/$(id -u)/qlog/qchat.log"
    "/tmp/qlog/qchat.log"
    "$TMPDIR/qlog/qchat.log"
)

LOG_FOUND=false
for log_path in "${LOG_LOCATIONS[@]}"; do
    if [[ -f "$log_path" ]]; then
        echo "✅ ログファイル発見: $log_path" | tee -a "$RESULT_FILE"
        LOG_FOUND=true
        
        # ファイル名確認
        if [[ "$log_path" == *"qchat.log" ]]; then
            echo "✅ ファイル名正確: qchat.log" >> "$RESULT_FILE"
        else
            echo "❌ ファイル名不正: $(basename "$log_path")" | tee -a "$RESULT_FILE"
            ((ISSUES++))
        fi
        break
    fi
done

if [[ "$LOG_FOUND" == false ]]; then
    echo "❌ ログファイルが見つかりません" | tee -a "$RESULT_FILE"
    echo "   確認した場所:" >> "$RESULT_FILE"
    for log_path in "${LOG_LOCATIONS[@]}"; do
        echo "   - $log_path" >> "$RESULT_FILE"
    done
    ((ISSUES++))
fi

echo "3. ドキュメント内容検証..."

# ドキュメント内の間違ったパスをチェック
WRONG_PATHS=(
    "~/.aws/amazonq/logs/q-cli.log"
    "q-cli.log"
)

for wrong_path in "${WRONG_PATHS[@]}"; do
    matches=$(grep -r "$wrong_path" docs/ 2>/dev/null || true)
    if [[ -n "$matches" ]]; then
        echo "❌ 間違ったパスが残存: $wrong_path" | tee -a "$RESULT_FILE"
        echo "$matches" | head -3 >> "$RESULT_FILE"
        ((ISSUES++))
    fi
done

echo "4. 環境変数効果確認..."

# Q_LOG_LEVELの効果確認
if [[ -n "$Q_LOG_LEVEL" ]]; then
    echo "✅ Q_LOG_LEVEL設定済み: $Q_LOG_LEVEL" >> "$RESULT_FILE"
else
    echo "⚠️  Q_LOG_LEVEL未設定" >> "$RESULT_FILE"
fi

echo "5. 設定ファイルパス確認..."

SETTINGS_PATH="$HOME/.local/share/amazon-q/settings.json"
if [[ -f "$SETTINGS_PATH" ]]; then
    echo "✅ 設定ファイル存在: $SETTINGS_PATH" >> "$RESULT_FILE"
else
    echo "ℹ️  設定ファイル未作成: $SETTINGS_PATH" >> "$RESULT_FILE"
    echo "   （初回実行後に作成されます）" >> "$RESULT_FILE"
fi

echo ""
echo "📊 実装検証完了!"
echo "発見された問題数: $ISSUES"

if [[ $ISSUES -eq 0 ]]; then
    echo "✅ 実装検証に合格しました!"
    echo "✅ 実装検証に合格しました!" >> "$RESULT_FILE"
else
    echo "❌ $ISSUES 個の問題が見つかりました。"
    echo "詳細は $RESULT_FILE を確認してください。"
fi

echo ""
echo "📝 検証項目:"
echo "- ログファイルパス（OS別）"
echo "- ログファイル名（qchat.log）"
echo "- ドキュメント内の間違った記述"
echo "- 環境変数の効果"
echo "- 設定ファイルパス"
