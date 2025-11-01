#!/bin/bash
# scripts/validate_commands.sh
# コマンド検証スクリプト（GitHub Actions対応版）

set -e

echo "=== Q CLI コマンド検証 ==="

# 1. 実在するコマンドリストを生成
echo "1. 実在するコマンドを取得中..."

# Q CLIがインストールされているか確認
if command -v q &> /dev/null; then
  # ローカル環境: q --help-all から取得
  q --help-all 2>&1 | grep "^  " | awk '{print $1}' | sort > /tmp/valid_commands.txt
else
  # GitHub Actions環境: 既知のコマンドリストを使用
  cat > /tmp/valid_commands.txt << 'EOF'
agent
chat
debug
diagnostic
doctor
inline
login
logout
profile
settings
translate
user
whoami
EOF
fi

echo "   実在するコマンド数: $(wc -l < /tmp/valid_commands.txt)"

# 2. 全ドキュメントからCLIコマンドを抽出（コードブロック内のみ）
echo "2. ドキュメントからCLIコマンドを抽出中..."

# コードブロック内のコマンドのみを抽出
find docs -name "*.md" -type f | while read file; do
  # awkでコードブロック内のみを処理
  awk '
    /^```bash/ { in_code=1; next }
    /^```/ { in_code=0; next }
    in_code && /^q [a-z]/ { 
      # コメント行を除外
      if ($0 !~ /#/) {
        print FILENAME":"NR":"$0
      }
    }
  ' FILENAME="$file" "$file"
done | sed 's/:/ /' | awk '{print $1":"$2" "$3}' > /tmp/all_cli_commands.txt || true

echo "   抽出したコマンド行数: $(wc -l < /tmp/all_cli_commands.txt)"

# 3. チャット内コマンドとの混同を検出
echo "3. チャット内コマンドとの混同を検出中..."
CHAT_CMD_ERRORS=$(grep -E " q /(knowledge|context|agent|checkpoint|todos|experiment|compact|tangent|paste|save|load)" /tmp/all_cli_commands.txt || true)
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
ERRORS=""

while IFS=' ' read -r location cmd rest; do
  # cmdが空でないことを確認
  if [ -z "$cmd" ]; then
    continue
  fi
  
  # 実在するコマンドリストと照合
  if ! grep -q "^$cmd$" /tmp/valid_commands.txt; then
    ERRORS="${ERRORS}   ❌ $location: q $cmd\n"
    ERROR_COUNT=$((ERROR_COUNT + 1))
  fi
done < /tmp/all_cli_commands.txt

if [ $ERROR_COUNT -gt 0 ]; then
  echo "   存在しないコマンド: ${ERROR_COUNT}件"
  echo ""
  echo -e "$ERRORS" | head -50
  if [ $ERROR_COUNT -gt 50 ]; then
    echo "   ... (残り $((ERROR_COUNT - 50)) 件)"
  fi
  exit 1
else
  echo "   ✅ 全てのコマンドが実在"
fi

# 5. q agent edit のオプション検証
echo "5. q agent edit のオプションを検証中..."
AGENT_EDIT_ERRORS=$(grep " q agent edit [^-]" /tmp/all_cli_commands.txt | grep -v "\-\-name" || true)
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
