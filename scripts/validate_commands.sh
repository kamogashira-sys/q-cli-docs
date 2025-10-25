#!/bin/bash
# scripts/validate_commands.sh
# コマンド検証スクリプト

set -e

echo "=== Q CLI コマンド検証 ==="

# 1. 実在するコマンドリストを生成
echo "1. 実在するコマンドを取得中..."
q --help-all 2>&1 | grep "^  " | awk '{print $1}' | sort > /tmp/valid_commands.txt
echo "   実在するコマンド数: $(wc -l < /tmp/valid_commands.txt)"

# 2. 全ドキュメントからCLIコマンドを抽出（コメント行を除外）
echo "2. ドキュメントからCLIコマンドを抽出中..."
find docs -name "*.md" -type f -exec grep -hn "^q [a-z]" {} \; 2>/dev/null | grep -v "^[^:]*:#" > /tmp/all_cli_commands.txt || true
echo "   抽出したコマンド行数: $(wc -l < /tmp/all_cli_commands.txt)"

# 3. チャット内コマンドとの混同を検出
echo "3. チャット内コマンドとの混同を検出中..."
CHAT_CMD_ERRORS=$(grep -E "q /(knowledge|context|agent|checkpoint|todos|experiment|compact|tangent|paste|save|load)" /tmp/all_cli_commands.txt || true)
if [ -n "$CHAT_CMD_ERRORS" ]; then
  echo "   ❌ チャット内コマンドをCLIコマンドとして記載:"
  echo "$CHAT_CMD_ERRORS"
  exit 1
else
  echo "   ✅ チャット内コマンドとの混同なし"
fi

# 4. 存在しないサブコマンドを検出
echo "4. 存在しないサブコマンドを検証中..."
ERROR_COUNT=0
while IFS=: read -r file line cmd; do
  base_cmd=$(echo "$cmd" | awk '{print $2}')
  if ! grep -q "^$base_cmd$" /tmp/valid_commands.txt; then
    echo "   ❌ $file:$line: $cmd (サブコマンド '$base_cmd' が存在しない)"
    ERROR_COUNT=$((ERROR_COUNT + 1))
  fi
done < /tmp/all_cli_commands.txt

if [ $ERROR_COUNT -gt 0 ]; then
  echo "   存在しないコマンド: ${ERROR_COUNT}件"
  exit 1
else
  echo "   ✅ 全てのコマンドが実在"
fi

# 5. q agent edit のオプション検証
echo "5. q agent edit のオプションを検証中..."
AGENT_EDIT_ERRORS=$(grep -hn "q agent edit [^-]" /tmp/all_cli_commands.txt | grep -v "\-\-name" || true)
if [ -n "$AGENT_EDIT_ERRORS" ]; then
  echo "   ❌ q agent edit に --name オプションが不足:"
  echo "$AGENT_EDIT_ERRORS"
  exit 1
else
  echo "   ✅ q agent edit のオプション指定が正確"
fi

echo ""
echo "=== 検証完了 ==="
echo "✅ 全てのコマンドが正確です"
