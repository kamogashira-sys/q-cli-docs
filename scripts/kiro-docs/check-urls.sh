#!/bin/bash
# check-urls.sh - kiro-docs 外部URL実在性チェック
#
# 使用方法:
#   ./scripts/kiro-docs/check-urls.sh              # kiro-docs 内の全URLをチェック
#   ./scripts/kiro-docs/check-urls.sh --dry-run    # URL抽出のみ
#   ./scripts/kiro-docs/check-urls.sh --sample 10  # 先頭10件のみ
#   ./scripts/kiro-docs/check-urls.sh --important  # v2.7.x 重要公式URLのみ確実にチェック
#
# 機能:
#   - kiro-docs/**/*.md の外部URLを抽出し HTTP ステータス（2xx/3xx）を確認
#   - 除外: .bak / *_update_plan.md / 06_embedded-docs / localhost / プレースホルダ / GitHub API

set -euo pipefail

MODE="all"
SAMPLE_SIZE=0
case "${1:-}" in
    --dry-run)   MODE="dry-run" ;;
    --sample)    MODE="sample"; SAMPLE_SIZE="${2:-10}" ;;
    --important) MODE="important" ;;
esac

cd "$(dirname "$0")/../.."

echo "=== kiro-docs 外部URL実在性チェック（mode=$MODE） ==="
echo ""

TEMP_URLS="/tmp/check-kiro-urls-$$.txt"
trap "rm -f $TEMP_URLS" EXIT

check_one() {
    # $1=URL  -> echo status, return 0 if 2xx/3xx
    local url="$1" status
    status=$(curl -I -s -o /dev/null -w "%{http_code}" "$url" \
        --max-time 15 --retry 2 --retry-delay 1 -L 2>/dev/null || echo "000")
    echo "$status"
}

# ---- important モード: 厳選した公式URL ----
if [ "$MODE" = "important" ]; then
    IMPORTANT_URLS=(
        "https://kiro.dev/changelog/cli/"
        "https://kiro.dev/changelog/cli/2-10/"
        "https://kiro.dev/changelog/cli/2-9/"
        "https://kiro.dev/changelog/cli/2-8/"
        "https://kiro.dev/changelog/cli/2-7/"
        "https://kiro.dev/changelog/cli/2-6/"
        "https://kiro.dev/docs/cli/chat/goal/"
        "https://kiro.dev/docs/cli/chat/queue-steering/"
        "https://kiro.dev/docs/cli/chat/rewind/"
        "https://kiro.dev/docs/cli/chat/settings/"
        "https://kiro.dev/docs/cli/reference/settings/"
        "https://kiro.dev/docs/cli/reference/slash-commands/"
        "https://kiro.dev/docs/cli/mcp/configuration/"
        "https://kiro.dev/docs/cli/custom-agents/configuration-reference/"
        "https://kiro.dev/docs/cli/v3/"
        "https://kiro.dev/docs/cli/v3/specs/"
        "https://kiro.dev/docs/cli/v3/feature-overview/"
        "https://kiro.dev/docs/cli/v3/permissions/"
        "https://kiro.dev/docs/cli/v3/hooks/"
        "https://kiro.dev/docs/cli/v3/agent-config/"
        "https://kiro.dev/docs/specs/"
    )
    errors=0
    for url in "${IMPORTANT_URLS[@]}"; do
        status=$(check_one "$url")
        if [[ "$status" =~ ^[23] ]]; then
            echo "✅ $status  $url"
        else
            echo "❌ $status  $url"
            errors=$((errors + 1))
        fi
    done
    echo ""
    echo "=== チェック結果 === 重要URL ${#IMPORTANT_URLS[@]} 件 / エラー $errors 件"
    [ "$errors" -gt 0 ] && { echo "❌ 重要URLチェックに失敗しました"; exit 1; }
    echo "✅ すべての重要URLが有効です"; exit 0
fi

# ---- URL抽出（kiro-docs/、除外適用） ----
echo "🔍 URLを抽出中..."
find kiro-docs -name "*.md" -type f \
    ! -name "*.bak" ! -name "*_update_plan.md" \
    -not -path "*/06_embedded-docs/*" \
    -exec grep -hoP 'https?://[^\s\)\]]+' {} \; \
    | sed 's/[,;:."'\''`]*$//' \
    | grep -v -E '(localhost|127\.0\.0\.1|0\.0\.0\.0|example\.(com|org)|[「」（）`]|\$|XXXX|vX\.Y\.Z|api\.github\.com)' \
    | sort -u > "$TEMP_URLS"

total=$(wc -l < "$TEMP_URLS")
echo "   抽出したURL数: $total"
echo ""

if [ "$MODE" = "dry-run" ]; then
    echo "=== ドライラン（抽出のみ、最初の10件） ==="
    head -10 "$TEMP_URLS" | sed 's/^/  /'
    echo "✅ URL抽出完了"; exit 0
fi

if [ "$MODE" = "sample" ]; then
    head -n "$SAMPLE_SIZE" "$TEMP_URLS" > "${TEMP_URLS}.s" && mv "${TEMP_URLS}.s" "$TEMP_URLS"
    total=$(wc -l < "$TEMP_URLS")
    echo "=== サンプルモード（先頭 ${SAMPLE_SIZE} 件） ==="
fi

errors=0; checked=0
echo "🔍 URLをチェック中..."
while IFS= read -r url; do
    [ -z "$url" ] && continue
    checked=$((checked + 1))
    [ $((checked % 10)) -eq 0 ] && echo "   進捗: $checked/$total"
    status=$(check_one "$url")
    if [[ "$status" =~ ^[23] ]]; then
        :
    elif [ "$status" = "000" ]; then
        echo "❌ タイムアウト: $url"; errors=$((errors + 1))
    else
        echo "❌ エラー ($status): $url"; errors=$((errors + 1))
    fi
done < "$TEMP_URLS"

echo ""
echo "=== チェック結果 === 対象 $total / 実施 $checked / エラー $errors"
if [ "$errors" -gt 0 ]; then
    echo "❌ URLチェックに失敗しました"; exit 1
fi
echo "✅ すべてのURLが有効です"; exit 0
