#!/bin/bash
# check-urls.sh - URL実在性確認
#
# 使用方法:
#   ./scripts/check-urls.sh              # 通常モード（全URLチェック）
#   ./scripts/check-urls.sh --dry-run    # ドライランモード（URL抽出のみ）
#   ./scripts/check-urls.sh --sample 10  # サンプルモード（最初の10URLのみチェック）
#
# 機能:
#   - ドキュメント内のすべてのURLを抽出
#   - 各URLの実在性を確認（HTTP status code）
#   - 無効なURLを検出

set -euo pipefail

# モードの判定
DRY_RUN=false
SAMPLE_SIZE=0

if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
elif [[ "${1:-}" == "--sample" ]]; then
    SAMPLE_SIZE="${2:-10}"
fi

echo "=== URL実在性チェック ==="
echo ""

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

# 一時ファイル
TEMP_URLS="/tmp/check-urls-$$.txt"
trap "rm -f $TEMP_URLS" EXIT

# URLを抽出（重複除去）
echo "🔍 URLを抽出中..."
find docs/ -name "*.md" -type f -exec grep -hoP 'https?://[^\s\)\]]+' {} \; | \
    sed 's/[,;:."'\'']*$//' | \
    grep -v -E '(localhost|127\.0\.0\.1|0\.0\.0\.0|example\.(com|org)|[「」（）`]|\$|XXXX|vX\.Y\.Z|proxy\.|username:|password@|\.service\.)' | \
    sort -u > "$TEMP_URLS"

total=$(wc -l < "$TEMP_URLS")
echo "   抽出したURL数: $total"
echo ""

# ドライランモードの場合はここで終了
if [ "$DRY_RUN" = true ]; then
    echo "=== ドライランモード ==="
    echo "抽出したURL（最初の10件）:"
    head -10 "$TEMP_URLS" | sed 's/^/  /'
    echo ""
    echo "✅ URL抽出完了（チェックはスキップ）"
    exit 0
fi

# サンプルモードの場合はURLを制限
if [ "$SAMPLE_SIZE" -gt 0 ]; then
    echo "=== サンプルモード（最初の${SAMPLE_SIZE}件のみチェック） ==="
    head -n "$SAMPLE_SIZE" "$TEMP_URLS" > "${TEMP_URLS}.sample"
    mv "${TEMP_URLS}.sample" "$TEMP_URLS"
    total=$(wc -l < "$TEMP_URLS")
fi

# 各URLをチェック
errors=0
checked=0
skipped=0

echo "🔍 URLをチェック中..."
while IFS= read -r url; do
    # ローカルホストURLをスキップ
    if [[ "$url" =~ ^https?://(localhost|127\.0\.0\.1|0\.0\.0\.0) ]]; then
        skipped=$((skipped + 1))
        continue
    fi
    
    # 不正なURL（日本語や特殊文字を含む）をスキップ
    if [[ "$url" =~ [^[:print:]] ]] || [[ "$url" =~ [「」（）] ]]; then
        skipped=$((skipped + 1))
        continue
    fi
    
    # GitHub APIは認証が必要なため、スキップ
    if [[ "$url" =~ ^https://api\.github\.com ]]; then
        skipped=$((skipped + 1))
        continue
    fi
    
    checked=$((checked + 1))
    
    # 進捗表示（10件ごと）
    if [ $((checked % 10)) -eq 0 ]; then
        echo "   進捗: $checked/$total"
    fi
    
    # curlでHTTPステータスコードを取得
    status=$(curl -I -s -o /dev/null -w "%{http_code}" "$url" \
        --max-time 10 \
        --retry 2 \
        --retry-delay 1 \
        -L \
        2>/dev/null || echo "000")
    
    # ステータスコードをチェック
    if [[ "$status" =~ ^[23] ]]; then
        # 200番台、300番台は成功
        : # 何もしない
    elif [[ "$status" == "000" ]]; then
        echo "❌ タイムアウト: $url"
        errors=$((errors + 1))
    else
        echo "❌ エラー ($status): $url"
        errors=$((errors + 1))
    fi
done < "$TEMP_URLS"

echo ""
echo "=== チェック結果 ==="
echo "チェック対象: $total URL"
echo "チェック実施: $checked URL"
echo "スキップ: $skipped URL"
echo "エラー: $errors URL"

if [ $errors -gt 0 ]; then
    echo ""
    echo "❌ URLチェックに失敗しました"
    exit 1
else
    echo ""
    echo "✅ すべてのURLが有効です"
    exit 0
fi
