# Makefile - 自動化ツール一括実行
#
# 使用方法:
#   make check-all    # すべてのチェックを実行
#   make check-quick  # 高速チェックのみ実行
#   make check-urls   # URLチェックのみ実行
#   make help         # ヘルプを表示

.PHONY: help check-all check-quick check-urls check-consistency check-commands check-impact check-completeness

# デフォルトターゲット
.DEFAULT_GOAL := help

# ヘルプ
help:
	@echo "=== 自動化ツール一括実行 ==="
	@echo ""
	@echo "使用方法:"
	@echo "  make check-all        # すべてのチェックを実行"
	@echo "  make check-quick      # 高速チェックのみ実行"
	@echo "  make check-urls       # URLチェックのみ実行"
	@echo "  make check-consistency # 一貫性チェックのみ実行"
	@echo "  make check-commands   # コマンド構文チェックのみ実行"
	@echo "  make check-impact     # 影響範囲分析のみ実行"
	@echo "  make check-completeness # 完全性チェックのみ実行"
	@echo ""
	@echo "個別ツール:"
	@echo "  ./scripts/check-urls.sh --dry-run"
	@echo "  ./scripts/check-consistency.sh"
	@echo "  ./scripts/check-commands.sh"
	@echo "  ./scripts/check-impact.sh [file]"
	@echo "  ./scripts/check-completeness.py [file]"

# すべてのチェックを実行
check-all: check-consistency check-commands check-completeness check-urls
	@echo ""
	@echo "✅ すべてのチェックが完了しました"

# 高速チェックのみ実行（URLチェックを除く）
check-quick: check-consistency check-commands check-completeness
	@echo ""
	@echo "✅ 高速チェックが完了しました"

# URLチェック
check-urls:
	@echo "🔍 URLチェック中..."
	@./scripts/check-urls.sh --sample 10

# 一貫性チェック
check-consistency:
	@echo "🔍 一貫性チェック中..."
	@./scripts/check-consistency.sh

# コマンド構文チェック
check-commands:
	@echo "🔍 コマンド構文チェック中..."
	@./scripts/check-commands.sh

# 影響範囲分析
check-impact:
	@echo "🔍 影響範囲分析中..."
	@./scripts/check-impact.sh

# 完全性チェック
check-completeness:
	@echo "🔍 完全性チェック中..."
	@./scripts/check-completeness.py || echo "⚠️  完全性チェックで問題が見つかりました（警告のみ）"

# ============================================================
# kiro-docs/ 専用チェック（scripts/kiro-docs/）
# ============================================================
.PHONY: check-kiro-all check-kiro-quick check-kiro-counts check-kiro-links check-kiro-consistency check-kiro-changelog check-kiro-structure check-kiro-notation check-kiro-urls check-kiro-freshness

# kiro-docs 全チェック（URL含む）
check-kiro-all: check-kiro-counts check-kiro-links check-kiro-consistency check-kiro-changelog check-kiro-structure check-kiro-notation check-kiro-urls
	@echo ""
	@echo "✅ kiro-docs 全チェックが完了しました"

# kiro-docs 高速チェック（URL除く）
check-kiro-quick: check-kiro-counts check-kiro-links check-kiro-consistency check-kiro-changelog check-kiro-structure check-kiro-notation
	@echo ""
	@echo "✅ kiro-docs 高速チェックが完了しました"

# 数値整合チェック（機能数・コマンド数の SSoT と各所記述の一致）
check-kiro-counts:
	@./scripts/kiro-docs/check-counts.sh

# 内部リンクチェック（相対リンク実在＋アンカー見出し検査）
check-kiro-links:
	@./scripts/kiro-docs/check-links.py --check-anchors

# 用語・日付整合チェック（取得日混入・バージョンタグ鮮度・出典日書式・ISO日付・裸URL境界）
check-kiro-consistency:
	@./scripts/kiro-docs/check-consistency.sh

# changelog 構造チェック（バージョン降順・日付書式・「N件」と箇条書き数の一致）
check-kiro-changelog:
	@./scripts/kiro-docs/check-changelog.sh

# 構造整合チェック（機能テーブル末尾・NN欠番・必須セクション・相互参照・changelog⇔機能文書リンク・更新履歴先頭行）
check-kiro-structure:
	@./scripts/kiro-docs/check-structure.py

# コマンド表記チェック（実在しないコマンド・フラグ表記の混入検出）
check-kiro-notation:
	@./scripts/kiro-docs/check-notation.sh

# 重要公式URLチェック（HTTP 2xx/3xx 確認）
check-kiro-urls:
	@./scripts/kiro-docs/check-urls.sh --important

# 新バージョン検知（外部フィード依存のため check-kiro-all / CI には含めない手動ターゲット）
check-kiro-freshness:
	@./scripts/kiro-docs/check-freshness.sh
