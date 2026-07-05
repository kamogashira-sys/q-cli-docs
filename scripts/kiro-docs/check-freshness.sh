#!/bin/bash
# check-freshness.sh - Kiro CLI 新バージョン検知（公式フィード vs ドキュメント）
#
# 使用方法:
#   ./scripts/kiro-docs/check-freshness.sh
#   make check-kiro-freshness
#
# 機能:
#   - 公式 Atom フィードの最新 CLI エントリ（link/id の changelog/cli/X-Y）と
#     kiro-docs/02_update/01_changelog.md 先頭の ### vX.Y.Z を major.minor で比較
#   - 一致: exit 0 ／ 差分（新バージョン掲載済み）: exit 1
#   - フィード取得失敗: 手動確認を促して exit 0（fail-safe。外部依存で CI を壊さない）
#
# 設計メモ:
#   - フィードのエントリタイトルにはバージョン番号が含まれないため、
#     link/id の changelog/cli/X-Y パスからバージョンを特定する
#   - patch 版はフィード URL に現れない（X-Y 単位）ため major.minor 比較のみ
#   - check-kiro-all / CI には含めない（ネットワーク依存で flaky なため独立ターゲット）

set -euo pipefail

cd "$(dirname "$0")/../.."

FEED_URL="https://kiro.dev/changelog/feed.atom"
CHANGELOG="kiro-docs/02_update/01_changelog.md"

echo "=== Kiro CLI 新バージョン検知（フィード vs ドキュメント） ==="
echo ""

# ---- ドキュメント側の最新版（SSoT: changelog 先頭の ### vX.Y.Z） ----
doc_ver=$(grep -m1 -oP '^### v\K[0-9]+\.[0-9]+\.[0-9]+' "$CHANGELOG" || true)
if [ -z "$doc_ver" ]; then
    echo "❌ $CHANGELOG から最新版（### vX.Y.Z）を抽出できません"
    exit 1
fi
doc_mm=$(echo "$doc_ver" | cut -d. -f1-2)

# ---- フィード側の最新 CLI エントリ（changelog/cli/X-Y の最初の出現） ----
echo "🔍 公式フィードを取得中... ($FEED_URL)"
feed=$(curl -s --max-time 15 "$FEED_URL" || true)
feed_mm=$(echo "$feed" | grep -m1 -oP 'changelog/cli/\K[0-9]+-[0-9]+' | tr '-' '.' || true)
if [ -z "$feed_mm" ]; then
    echo "⚠️ フィードを取得できませんでした（ネットワーク or フィード形式変更）"
    echo "   手動確認: curl -s $FEED_URL | grep -oP 'changelog/cli/[0-9-]+' | head -3"
    exit 0
fi

echo "   フィード最新 CLI エントリ = $feed_mm / ドキュメント最新版 = $doc_ver ($doc_mm)"
echo ""
echo "=== チェック結果 ==="

if [ "$feed_mm" = "$doc_mm" ]; then
    echo "✅ ドキュメントは公式フィードの最新 CLI バージョンに追随しています"
    exit 0
fi

echo "❌ 新バージョン v$feed_mm が公式に掲載済みです（ドキュメントは v$doc_mm 止まり）"
echo "   → 手順書 Phase 0（情報収集）を開始してください"
exit 1
