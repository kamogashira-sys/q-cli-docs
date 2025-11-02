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
