#!/bin/bash
# check-consistency.sh - kiro-docs 用語・日付整合チェック
#
# 使用方法:
#   ./scripts/kiro-docs/check-consistency.sh
#
# 機能:
#   (a) 取得日混入: 公開テキストに `YYYY-MM-DD取得` を書かない（編集注記の「取得時点」は許可）
#   (b) バージョンタグ鮮度: `（vX.Y.Z対応）` が changelog 最新版と一致するか
#   (c) 出典日書式: リファレンス文書に「公式ページ最終更新/ Page updated: YYYY-MM-DD」が存在するか
#   (d) 更新日書式: フッターの「最終更新/Page updated」は ISO（YYYY-MM-DD）に統一（YYYY年M月D日 は禁止）
#   (e) 裸URL直後の全角文字: GitHub autolink が全角文字まで URL に含めてリンク切れになるため禁止
#
# 設計メモ:
#   - 用語の表記揺れ検出は誤検知を避けるため初版では最小限（明確な違反のみ）。
#     "時点"（as-of 日付）は正当なので取得日チェックの対象外。
#   - 除外: .bak / *_update_plan.md / 06_embedded-docs / 05_meta 手順書

set -euo pipefail

cd "$(dirname "$0")/../.."

CHANGELOG="kiro-docs/02_update/01_changelog.md"

echo "=== kiro-docs 用語・日付整合チェック ==="
echo ""

errors=0

exclude_paths() {
    grep -v '\.bak' \
        | grep -v '_update_plan' \
        | grep -v '06_embedded-docs' \
        | grep -v '05_meta/10_version-update-guide.md'
}

# ---- (a) 取得日混入 ----
echo "🔍 (a) 取得日混入を検証中..."
acq=$(grep -rnE '[0-9]{4}-[0-9]{2}-[0-9]{2}取得' kiro-docs/ README.md --include="*.md" \
    | exclude_paths | grep -v '取得時点' || true)
if [ -n "$acq" ]; then
    echo "❌ 公開テキストに取得日（YYYY-MM-DD取得）が混入:"
    echo "$acq" | sed 's/^/     /'
    errors=$((errors + 1))
fi

# ---- (b) バージョンタグ鮮度 ----
echo "🔍 (b) （vX.Y.Z対応）の鮮度を検証中..."
LATEST=$(grep -oE '^### v[0-9]+\.[0-9]+\.[0-9]+' "$CHANGELOG" | head -1 | sed 's/^### //')
echo "   changelog 最新版 = $LATEST"
tag_lines=$(grep -rnoE '（v[0-9]+\.[0-9]+\.[0-9]+対応）' kiro-docs/ README.md --include="*.md" \
    | exclude_paths || true)
tag_bad=""
if [ -n "$tag_lines" ]; then
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        ver=$(echo "$line" | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+')
        if [ "$ver" != "$LATEST" ]; then
            tag_bad+="$line"$'\n'
        fi
    done <<< "$tag_lines"
fi
if [ -n "$tag_bad" ]; then
    echo "❌ 最新版（$LATEST）と異なる（vX.Y.Z対応）タグ:"
    echo "$tag_bad" | sed '/^$/d' | sed 's/^/     /'
    errors=$((errors + 1))
fi

# ---- (c) 出典日書式 ----
echo "🔍 (c) リファレンス出典日の書式存在を検証中..."
for ref in kiro-docs/04_reference/02_slash-commands.md kiro-docs/04_reference/01_settings.md; do
    if ! grep -qE '(公式ページ最終更新|Page updated|公式更新日)[:： ].*[0-9]{4}-[0-9]{2}-[0-9]{2}' "$ref"; then
        echo "❌ 出典日（公式ページ最終更新/Page updated: YYYY-MM-DD）が見つからない: $ref"
        errors=$((errors + 1))
    fi
done

# ---- (d) 更新日書式（ISO 統一） ----
echo "🔍 (d) フッター更新日の ISO 書式（YYYY-MM-DD）を検証中..."
noniso=$(grep -rnE '\*\*(最終更新|Page updated)\*\*[:： ]+[0-9]{4}年' kiro-docs/ README.md --include="*.md" \
    | exclude_paths || true)
if [ -n "$noniso" ]; then
    echo "❌ 更新日が ISO 書式（YYYY-MM-DD）でないフッター:"
    echo "$noniso" | sed 's/^/     /'
    errors=$((errors + 1))
fi

# ---- (e) 裸URL直後の全角文字（GitHub autolink 境界事故） ----
# 裸 URL（[text](URL) や <URL> や `URL` で囲まれていないもの）の直後に全角文字があると、
# GitHub の autolink は空白まで URL とみなすため全角文字込みのリンクになり 404 になる。
# URL 文字クラスは ASCII 印字文字から ) > ] ` を除外（明示リンク・<URL>・コードは末尾が
# これらの ASCII 文字で終わるため誤検知しない）。
echo "🔍 (e) 裸 URL 直後の全角文字（autolink 境界）を検証中..."
autolink=$(grep -rnP 'https?://[\x21-\x28\x2A-\x3D\x3F-\x5C\x5E\x5F\x61-\x7E]*[^\x00-\x7F]' kiro-docs/ README.md --include="*.md" \
    | exclude_paths || true)
if [ -n "$autolink" ]; then
    echo "❌ 裸 URL の直後に全角文字（GitHub 上で全角文字まで URL 扱いになりリンク切れ）:"
    echo "$autolink" | sed 's/^/     /'
    echo "   → [URL](URL) の明示リンク、<URL>、または \`URL\` に修正してください"
    errors=$((errors + 1))
fi

echo ""
echo "=== チェック結果 ==="
echo "不一致カテゴリ数: $errors"

if [ "$errors" -gt 0 ]; then
    echo ""
    echo "❌ 用語・日付整合チェックに失敗しました"
    exit 1
else
    echo ""
    echo "✅ 用語・日付整合は問題ありません"
    exit 0
fi
