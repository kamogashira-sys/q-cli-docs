#!/bin/bash

# 設定ファイルパスの一括修正スクリプト
echo "🔧 設定ファイルパスを一括修正します..."

cd "$(dirname "$0")/.."

# ~/.config/amazonq/settings.json → ~/.local/share/amazon-q/settings.json
find docs/ -name "*.md" -type f -exec sed -i 's|~/.config/amazonq/settings.json|~/.local/share/amazon-q/settings.json|g' {} \;

# ~/.q/settings.json → ~/.local/share/amazon-q/settings.json (間違った例として残す場合は除く)
find docs/ -name "*.md" -type f -exec sed -i '/# これらの場所は使用されません/!s|~/.q/settings.json|~/.local/share/amazon-q/settings.json|g' {} \;

echo "✅ 設定ファイルパスの修正完了"

# 修正結果を確認
echo "📊 修正後の状況:"
echo "正しいパス (~/.local/share/amazon-q/settings.json): $(grep -r "~/.local/share/amazon-q/settings.json" docs/ | wc -l) 箇所"
echo "間違ったパス (~/.config/amazonq/settings.json): $(grep -r "~/.config/amazonq/settings.json" docs/ | wc -l) 箇所"
echo "間違ったパス (~/.q/settings.json): $(grep -r "~/.q/settings.json" docs/ | wc -l) 箇所"
