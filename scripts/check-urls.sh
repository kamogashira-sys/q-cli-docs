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
#
# 終了コード:
#   0 = 問題なし / 1 = 問題検出 / 2 = ツール自体のエラー

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

# 依存コマンドの確認（ツール自体のエラーは exit 2）
for cmd in curl grep sed sort; do
    if ! command -v "$cmd" > /dev/null 2>&1; then
        echo "❌ 必要なコマンドが見つかりません: $cmd" >&2
        exit 2
    fi
done

# 一時ファイル
TEMP_URLS="/tmp/check-urls-$$.txt"
trap 'rm -f "$TEMP_URLS"' EXIT

# ---------------------------------------------------------------------------
# スキップ対象の定義
#
# 設計原則（Phase 2-C）:
#   ホスト単位のスキップは禁止。真のリンク切れを永久に隠すため。
#   スキップは「URL完全一致」または「明確に非リンクな用途」に限定する。
#   例: desktop-release.q.us-east-1.amazonaws.com はホスト単位でスキップして
#       はならない（存在しないキーへの 403 が実在するリンク切れだった）。
# ---------------------------------------------------------------------------

# プレースホルダ（ドキュメント内の記入例。実在しないのが正しい）
SKIP_PLACEHOLDER='(YOUR_USERNAME|your-repo|your-profile\.awsapps\.com|example\.(com|org)|XXXX|vX\.Y\.Z|username:|password@)'

# 疎通確認用エンドポイント（設定値・curl -I の引数として登場。ブラウザで開く
# 対象ではなく、HTTP で 2xx を返す性質のものではない）
declare -A SKIP_EXACT=(
    ["https://telemetry.aws.amazon.com"]="テレメトリ送信先の設定値（02_configuration-system.md）"
    ["https://q.us-east-1.amazonaws.com"]="疎通確認用エンドポイント（02_common-issues.md の curl -I 例）"
    ["https://codewhisperer.us-east-1.amazonaws.com"]="旧エンドポイントの設定値（04_global-settings.md）"
    # Cloudflare のbot対策によりブラウザUA付きGETでも403を返すため判定不能。
    # URL自体はブラウザからは到達可能。
    ["https://stackoverflow.com/questions/tagged/amazon-q"]="Cloudflare bot対策により自動判定不能"
)

# ---------------------------------------------------------------------------
# URLを抽出（重複除去）
#
# 止め文字に ' " ` > < を含めることが重要（Phase 2-A）。
# これらを止め文字にしないと Mermaid 図中の HTML リンク
#   <a href='https://.../01_chat.md'>チャット機能</a>
# を丸ごと URL として拾い、必ず 404 になる偽陽性を生む。
# ---------------------------------------------------------------------------
echo "🔍 URLを抽出中..."
find docs/ -name "*.md" -type f ! -name "*.bak" \
    -exec grep -hoP "https?://[^\s\)\]'\"\`><]+" {} \; | \
    sed 's/[,;:."'\''`]*$//' | \
    grep -v -E '(localhost|127\.0\.0\.1|0\.0\.0\.0|[「」（）`]|\$|proxy\.|\.service\.)' | \
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

# ブラウザ相当の User-Agent（bot対策で HEAD/GET を拒むサイト向け）
BROWSER_UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# ---------------------------------------------------------------------------
# 3段フォールバックで到達性を判定（Phase 2-B）
#
# HEAD 単独だと HEAD を拒むサイトが全て偽陽性になる（実測で10件）。
#   1. HEAD              … 最も軽量
#   2. GET -r 0-0        … 先頭1バイトのみ。206 で判定でき転送量を抑えられる
#   3. GET -r 0-0 + UA   … bot対策サイト向け
# ---------------------------------------------------------------------------
probe_url() {
    local url="$1" status

    status=$(curl -I -s -o /dev/null -w "%{http_code}" "$url" \
        --max-time 10 --retry 2 --retry-delay 1 -L 2>/dev/null || echo "000")
    if [[ "$status" =~ ^[23] ]]; then
        echo "$status HEAD"; return 0
    fi

    status=$(curl -s -r 0-0 -o /dev/null -w "%{http_code}" "$url" \
        --max-time 15 --retry 2 --retry-delay 1 -L 2>/dev/null || echo "000")
    if [[ "$status" =~ ^[23] ]]; then
        echo "$status GET"; return 0
    fi

    status=$(curl -s -r 0-0 -A "$BROWSER_UA" -o /dev/null -w "%{http_code}" "$url" \
        --max-time 15 --retry 2 --retry-delay 1 -L 2>/dev/null || echo "000")
    if [[ "$status" =~ ^[23] ]]; then
        echo "$status GET+UA"; return 0
    fi

    echo "$status GET+UA"; return 1
}

# 各URLをチェック
errors=0
checked=0
skipped=0
SKIP_LOG=()

echo "🔍 URLをチェック中..."
while IFS= read -r url; do
    [ -z "$url" ] && continue

    # ローカルホストURL
    if [[ "$url" =~ ^https?://(localhost|127\.0\.0\.1|0\.0\.0\.0) ]]; then
        skipped=$((skipped + 1))
        SKIP_LOG+=("$url … ローカルホスト")
        continue
    fi

    # 不正なURL（非印字文字や全角括弧を含む）
    if [[ "$url" =~ [^[:print:]] ]] || [[ "$url" =~ [「」（）] ]]; then
        skipped=$((skipped + 1))
        SKIP_LOG+=("$url … 非印字文字/全角括弧を含む")
        continue
    fi

    # GitHub APIは認証が必要
    if [[ "$url" =~ ^https://api\.github\.com ]]; then
        skipped=$((skipped + 1))
        SKIP_LOG+=("$url … GitHub API（認証が必要）")
        continue
    fi

    # プレースホルダ
    if [[ "$url" =~ $SKIP_PLACEHOLDER ]]; then
        skipped=$((skipped + 1))
        SKIP_LOG+=("$url … プレースホルダ（記入例）")
        continue
    fi

    # URL完全一致のスキップ（設定値・疎通確認用エンドポイント等）
    if [[ -v SKIP_EXACT["$url"] ]]; then
        skipped=$((skipped + 1))
        SKIP_LOG+=("$url … ${SKIP_EXACT[$url]}")
        continue
    fi

    checked=$((checked + 1))

    # 進捗表示（10件ごと）
    if [ $((checked % 10)) -eq 0 ]; then
        echo "   進捗: $checked/$total"
    fi

    if result=$(probe_url "$url"); then
        : # 到達可能
    else
        status="${result%% *}"
        method="${result##* }"
        if [[ "$status" == "000" ]]; then
            echo "❌ 到達不可（タイムアウト/名前解決失敗）: $url"
        else
            echo "❌ エラー ($status, $method まで試行): $url"
        fi
        errors=$((errors + 1))
    fi
done < "$TEMP_URLS"

echo ""

# ---------------------------------------------------------------------------
# スキップの可視化（Phase 2-D）
#
# 件数だけを表示して中身を隠すと、スキップ設計の誤りに気付けない。
# 14_tool-creation-checklist.md の「結果を捨てない」原則に従い全件出力する。
# ---------------------------------------------------------------------------
if [ ${#SKIP_LOG[@]} -gt 0 ]; then
    echo "=== スキップしたURL（${#SKIP_LOG[@]}件）==="
    for entry in "${SKIP_LOG[@]}"; do
        echo "  ⏭️  $entry"
    done
    echo ""
fi

echo "=== チェック結果 ==="
echo "チェック対象: $total URL"
echo "チェック実施: $checked URL"
echo "スキップ: $skipped URL"
echo "エラー: $errors URL"

if [ "$errors" -gt 0 ]; then
    echo ""
    echo "❌ URLチェックに失敗しました"
    exit 1
else
    echo ""
    echo "✅ すべてのURLが有効です"
    exit 0
fi
