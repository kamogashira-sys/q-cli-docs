#!/bin/bash
# scripts/validate_config_keys.sh
# 設定キー検証スクリプト

set -e

echo "=== 設定キー検証 ==="

# 1. Agent設定キーの検証
echo "1. Agent設定キーを検証中..."
if [ -f "schemas/agent-v1.json" ]; then
  # スキーマから有効なキーを抽出
  jq -r '.properties | keys[]' schemas/agent-v1.json 2>/dev/null | sort > /tmp/valid_agent_keys.txt
  
  echo "   有効なAgent設定キー数: $(wc -l < /tmp/valid_agent_keys.txt)"
  echo "   ✅ Agent設定スキーマを確認"
else
  echo "   ⚠️  スキーマファイルが見つかりません"
fi

# 2. 環境変数名の検証
echo "2. 環境変数名を検証中..."
# Q_で始まる環境変数を抽出
grep -rh "Q_[A-Z_]*" docs/01_for-users/03_configuration/05_environment-variables.md 2>/dev/null | \
  grep -o "Q_[A-Z_]*" | sort -u > /tmp/documented_env_vars.txt || true

echo "   記載されている環境変数数: $(wc -l < /tmp/documented_env_vars.txt)"
echo "   ⚠️  環境変数の実在確認はソースコード照合が必要"

echo ""
echo "=== 検証完了 ==="
