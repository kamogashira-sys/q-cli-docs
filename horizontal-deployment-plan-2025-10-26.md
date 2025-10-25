# 水平展開作業計画書 - 2025-10-26

## 🎯 目的

**根本原因**: GitHubソースを参照せず、推測でドキュメントを作成した

**水平展開の目的**: サイト全体から推測記載を根絶し、GitHubソース準拠を保証する

---

## 📋 検証対象カテゴリ

### カテゴリ1: コマンド記載の正確性【最優先】

**リスク**: ユーザーが実行できないコマンドを記載

**検証項目**:
1. 全てのCLIコマンド（`q`で始まる）が実在するか
2. チャット内コマンド（`/`で始まる）との混同がないか
3. サブコマンドが正確か
4. オプション指定が正確か（必須オプション、位置引数）
5. コマンド例が実行可能か

---

### カテゴリ2: 設定ファイル仕様の正確性

**リスク**: 無効な設定を記載、ユーザーが設定できない

**検証項目**:
1. JSONスキーマと一致しているか
2. 設定キー名が正確か
3. 設定値の型が正確か
4. デフォルト値が正確か
5. 環境変数名が正確か

---

### カテゴリ3: 機能説明の正確性

**リスク**: 実装されていない機能を記載

**検証項目**:
1. 記載された機能が実装されているか
2. バージョン情報が正確か
3. 動作説明が実際の挙動と一致しているか
4. 制限事項が正確か

---

### カテゴリ4: トラブルシューティングの有効性

**リスク**: 無効な解決方法を記載

**検証項目**:
1. 解決方法が実際に有効か
2. エラーメッセージが正確か
3. 診断手順が正確か

---

## 🔍 検証方法

### 方法1: コマンド自動検証

**ツール**: `q --help-all`, `q <subcommand> --help`

**検証スクリプト**:
```bash
#!/bin/bash
# validate_all_commands.sh

# 実在するコマンドリストを生成
q --help-all 2>&1 | grep "^  " | awk '{print $1}' > /tmp/valid_commands.txt

# 全ドキュメントからコマンドを抽出
find docs -name "*.md" -type f -exec grep -h "^q [a-z]" {} \; | \
  sort -u > /tmp/documented_commands.txt

# チャット内コマンドを抽出（/で始まる）
find docs -name "*.md" -type f -exec grep -h "^/[a-z]" {} \; | \
  sort -u > /tmp/chat_commands.txt

# CLIコマンドとして誤って記載されているチャット内コマンドを検出
grep -E "^q /(knowledge|context|agent|checkpoint|todos)" /tmp/documented_commands.txt

# 存在しないCLIコマンドを検出
while read cmd; do
  base_cmd=$(echo "$cmd" | awk '{print $2}')
  if ! grep -q "^$base_cmd$" /tmp/valid_commands.txt; then
    echo "❌ 存在しないコマンド: $cmd"
  fi
done < /tmp/documented_commands.txt
```

---

### 方法2: GitHubソース照合

**参照先**:
- `schemas/agent-v1.json` - Agent設定スキーマ
- `schemas/mcp-v1.json` - MCP設定スキーマ
- `crates/amzn-toolkit-cli/src/cli.rs` - CLIコマンド定義
- `crates/amzn-consolas-chat/src/commands/` - チャット内コマンド定義

**検証手順**:
```bash
# 1. GitHubから最新ソースを取得
cd /tmp
git clone https://github.com/aws/amazon-q-developer-cli.git q-cli-source
cd q-cli-source

# 2. スキーマファイルを比較
diff schemas/agent-v1.json /path/to/docs/schemas/agent-v1.json

# 3. コマンド定義を確認
grep -r "pub enum Command" crates/amzn-toolkit-cli/src/cli.rs

# 4. チャット内コマンドを確認
ls crates/amzn-consolas-chat/src/commands/
```

---

### 方法3: 設定ファイル検証

**検証スクリプト**:
```bash
#!/bin/bash
# validate_config_keys.sh

# Agent設定のキーを抽出
jq -r '.. | objects | keys[]' schemas/agent-v1.json 2>/dev/null | sort -u > /tmp/valid_agent_keys.txt

# ドキュメントから設定キーを抽出
grep -rh '"[a-zA-Z]' docs/01_for-users/10_file-specifications/02_agent-configuration.md | \
  grep -o '"[^"]*"' | tr -d '"' | sort -u > /tmp/documented_agent_keys.txt

# 存在しないキーを検出
comm -13 /tmp/valid_agent_keys.txt /tmp/documented_agent_keys.txt
```

---

## 📊 検証対象ファイル一覧

### 優先度1: コマンド記載が多いファイル【最優先】

| ファイル | コマンド数（推定） | リスク | 検証方法 |
|---------|------------------|--------|---------|
| `docs/01_for-users/07_reference/02_commands.md` | 100+ | 高 | 全コマンド実行確認 |
| `docs/01_for-users/07_reference/08_quick-reference.md` | 50+ | 高 | 全コマンド実行確認 |
| `docs/01_for-users/03_configuration/01_overview.md` | 30+ | 中 | コマンド抽出→検証 |
| `docs/01_for-users/02_features/01_chat.md` | 20+ | 中 | チャット内コマンド確認 |
| `docs/01_for-users/02_features/02_agents.md` | 20+ | 中 | Agentコマンド確認 |

### 優先度2: 設定ファイル仕様

| ファイル | 検証項目 | リスク | 検証方法 |
|---------|---------|--------|---------|
| `docs/01_for-users/10_file-specifications/02_agent-configuration.md` | Agent設定キー | 高 | スキーマ照合 |
| `docs/01_for-users/10_file-specifications/03_mcp-configuration.md` | MCP設定キー | 高 | スキーマ照合 |
| `docs/01_for-users/10_file-specifications/04_global-settings.md` | グローバル設定キー | 高 | 設定ファイル照合 |
| `docs/01_for-users/03_configuration/05_environment-variables.md` | 環境変数名 | 中 | ソースコード照合 |

### 優先度3: 機能説明

| ファイル | 検証項目 | リスク | 検証方法 |
|---------|---------|--------|---------|
| `docs/01_for-users/02_features/*.md` | 機能の実装状況 | 中 | リリースノート照合 |
| `docs/03_for-community/01_updates/03_version-history-v1.13-latest.md` | バージョン情報 | 中 | GitHubリリース照合 |
| `docs/03_for-community/01_updates/02_roadmap.md` | 完了機能 | 中 | リリースノート照合 |

### 優先度4: トラブルシューティング

| ファイル | 検証項目 | リスク | 検証方法 |
|---------|---------|--------|---------|
| `docs/01_for-users/06_troubleshooting/*.md` | 解決方法の有効性 | 低 | 実際に再現→解決確認 |
| `docs/01_for-users/07_reference/10_error-messages.md` | エラーメッセージ | 低 | ソースコード照合 |

---

## 🔧 作業手順

### フェーズ1: 自動検証スクリプトの作成（30分）

#### タスク1.1: コマンド検証スクリプト

```bash
#!/bin/bash
# scripts/validate_commands.sh

set -e

echo "=== Q CLI コマンド検証 ==="

# 1. 実在するコマンドリストを生成
echo "1. 実在するコマンドを取得中..."
q --help-all 2>&1 | grep "^  " | awk '{print $1}' | sort > /tmp/valid_commands.txt
echo "   実在するコマンド数: $(wc -l < /tmp/valid_commands.txt)"

# 2. 全ドキュメントからCLIコマンドを抽出
echo "2. ドキュメントからCLIコマンドを抽出中..."
find docs -name "*.md" -type f -exec grep -hn "^q [a-z]" {} \; > /tmp/all_cli_commands.txt
echo "   抽出したコマンド行数: $(wc -l < /tmp/all_cli_commands.txt)"

# 3. チャット内コマンドとの混同を検出
echo "3. チャット内コマンドとの混同を検出中..."
CHAT_CMD_ERRORS=$(grep -E "^[^:]+:q /(knowledge|context|agent|checkpoint|todos|experiment|compact|tangent|paste|save|load)" /tmp/all_cli_commands.txt || true)
if [ -n "$CHAT_CMD_ERRORS" ]; then
  echo "   ❌ チャット内コマンドをCLIコマンドとして記載:"
  echo "$CHAT_CMD_ERRORS"
  exit 1
else
  echo "   ✅ チャット内コマンドとの混同なし"
fi

# 4. 存在しないサブコマンドを検出
echo "4. 存在しないサブコマンドを検出中..."
INVALID_CMDS=""
while IFS=: read -r file line cmd; do
  base_cmd=$(echo "$cmd" | awk '{print $2}')
  if ! grep -q "^$base_cmd$" /tmp/valid_commands.txt; then
    INVALID_CMDS="${INVALID_CMDS}${file}:${line}: $cmd\n"
  fi
done < /tmp/all_cli_commands.txt

if [ -n "$INVALID_CMDS" ]; then
  echo "   ❌ 存在しないコマンド:"
  echo -e "$INVALID_CMDS"
  exit 1
else
  echo "   ✅ 全てのコマンドが実在"
fi

# 5. 各サブコマンドのオプション検証
echo "5. サブコマンドのオプションを検証中..."
# q agent edit --name が必須
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
```

#### タスク1.2: 設定キー検証スクリプト

```bash
#!/bin/bash
# scripts/validate_config_keys.sh

set -e

echo "=== 設定キー検証 ==="

# 1. Agent設定キーの検証
echo "1. Agent設定キーを検証中..."
if [ -f "schemas/agent-v1.json" ]; then
  # スキーマから有効なキーを抽出
  jq -r '.properties | keys[]' schemas/agent-v1.json > /tmp/valid_agent_keys.txt
  
  # ドキュメントから記載されているキーを抽出
  grep -rh '"[a-zA-Z]' docs/01_for-users/10_file-specifications/02_agent-configuration.md | \
    grep -o '"[^"]*":' | tr -d '":' | sort -u > /tmp/documented_agent_keys.txt
  
  # 存在しないキーを検出
  INVALID_KEYS=$(comm -13 <(sort /tmp/valid_agent_keys.txt) <(sort /tmp/documented_agent_keys.txt) || true)
  if [ -n "$INVALID_KEYS" ]; then
    echo "   ❌ 存在しない設定キー:"
    echo "$INVALID_KEYS"
    exit 1
  else
    echo "   ✅ 全ての設定キーが有効"
  fi
else
  echo "   ⚠️  スキーマファイルが見つかりません"
fi

# 2. 環境変数名の検証
echo "2. 環境変数名を検証中..."
# Q_で始まる環境変数を抽出
grep -rh "Q_[A-Z_]*" docs/01_for-users/03_configuration/05_environment-variables.md | \
  grep -o "Q_[A-Z_]*" | sort -u > /tmp/documented_env_vars.txt

echo "   記載されている環境変数数: $(wc -l < /tmp/documented_env_vars.txt)"
echo "   ⚠️  環境変数の実在確認はソースコード照合が必要"

echo ""
echo "=== 検証完了 ==="
```

#### タスク1.3: pre-commitフックの作成

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 コマンド検証を実行中..."

if [ -f "scripts/validate_commands.sh" ]; then
  bash scripts/validate_commands.sh
  if [ $? -ne 0 ]; then
    echo ""
    echo "❌ コマンド検証に失敗しました"
    echo "   上記の問題を修正してから再度コミットしてください"
    echo ""
    echo "   検証をスキップする場合: git commit --no-verify"
    exit 1
  fi
fi

echo "✅ コマンド検証に成功しました"
```

---

### フェーズ2: 優先度1ファイルの検証（2時間）

#### タスク2.1: commands.mdの全コマンド検証

**対象**: `docs/01_for-users/07_reference/02_commands.md`

**手順**:
```bash
# 1. 全コマンド例を抽出
grep -n "^q " docs/01_for-users/07_reference/02_commands.md > /tmp/commands_md_cmds.txt
grep -n "^/" docs/01_for-users/07_reference/02_commands.md > /tmp/commands_md_chat_cmds.txt

# 2. CLIコマンドを1つずつ検証
while IFS=: read -r line cmd; do
  base_cmd=$(echo "$cmd" | awk '{print $2}')
  echo "検証中: $cmd"
  
  # helpで確認
  if ! q "$base_cmd" --help &>/dev/null; then
    echo "❌ Line $line: $cmd - コマンドが存在しない"
  fi
done < /tmp/commands_md_cmds.txt

# 3. チャット内コマンドを確認
echo "チャット内コマンド数: $(wc -l < /tmp/commands_md_chat_cmds.txt)"
```

**検証項目**:
- [ ] 全CLIコマンドが実在する
- [ ] チャット内コマンドが`/`で始まる
- [ ] オプション指定が正確
- [ ] サブコマンドが正確
- [ ] コマンド例が実行可能

#### タスク2.2: quick-reference.mdの検証

**対象**: `docs/01_for-users/07_reference/08_quick-reference.md`

**手順**:
```bash
# コマンド抽出→検証スクリプト実行
grep -n "^q " docs/01_for-users/07_reference/08_quick-reference.md | \
  while IFS=: read -r line cmd; do
    echo "Line $line: $cmd"
    # 実行可能性を確認
  done
```

#### タスク2.3: 設定関連ドキュメントの検証

**対象**: `docs/01_for-users/03_configuration/*.md`

**手順**:
```bash
# q settings コマンドを全て抽出
grep -rn "q settings" docs/01_for-users/03_configuration/ | \
  grep -v "q settings list\|q settings open\|q settings <key>\|q settings --delete"

# 上記で検出されたものは誤り
```

---

### フェーズ3: 優先度2ファイルの検証（1時間）

#### タスク3.1: Agent設定スキーマ照合

```bash
# 1. GitHubから最新スキーマを取得
curl -s https://raw.githubusercontent.com/aws/amazon-q-developer-cli/main/schemas/agent-v1.json > /tmp/agent-schema-latest.json

# 2. ローカルスキーマと比較
diff schemas/agent-v1.json /tmp/agent-schema-latest.json

# 3. ドキュメントの設定例を検証
# JSONサンプルを抽出してスキーマ検証
```

#### タスク3.2: MCP設定スキーマ照合

```bash
# 同様にMCPスキーマを検証
curl -s https://raw.githubusercontent.com/aws/amazon-q-developer-cli/main/schemas/mcp-v1.json > /tmp/mcp-schema-latest.json
diff schemas/mcp-v1.json /tmp/mcp-schema-latest.json
```

#### タスク3.3: 環境変数名の照合

```bash
# GitHubソースから環境変数を抽出
git clone --depth 1 https://github.com/aws/amazon-q-developer-cli.git /tmp/q-cli-source
grep -r "env::var\|std::env" /tmp/q-cli-source/crates/ | grep "Q_" | \
  grep -o "Q_[A-Z_]*" | sort -u > /tmp/source_env_vars.txt

# ドキュメントと比較
diff /tmp/source_env_vars.txt /tmp/documented_env_vars.txt
```

---

### フェーズ4: 優先度3-4ファイルの検証（1時間）

#### タスク4.1: バージョン情報の照合

```bash
# GitHubリリースと照合
curl -s https://api.github.com/repos/aws/amazon-q-developer-cli/releases | \
  jq -r '.[].tag_name' > /tmp/github_releases.txt

# ドキュメントのバージョン情報と比較
grep -rh "v1\.[0-9]*\.[0-9]*" docs/03_for-community/01_updates/ | \
  grep -o "v1\.[0-9]*\.[0-9]*" | sort -u > /tmp/documented_versions.txt

comm -13 /tmp/github_releases.txt /tmp/documented_versions.txt
```

#### タスク4.2: 機能の実装状況確認

```bash
# roadmapの完了機能がリリースノートに存在するか確認
grep -A 50 "完了した機能" docs/03_for-community/01_updates/02_roadmap.md | \
  grep "^- ✅" | \
  while read -r line; do
    feature=$(echo "$line" | sed 's/^- ✅ //')
    if ! grep -q "$feature" docs/03_for-community/01_updates/03_version-history-v1.13-latest.md; then
      echo "❌ roadmapに記載されているが、version-historyに存在しない: $feature"
    fi
  done
```

---

### フェーズ5: 修正と再検証（2時間）

#### タスク5.1: 検出された問題の修正

**修正手順**:
1. 問題をリスト化
2. 優先度順に修正
3. 修正ごとにコミット
4. 検証スクリプトで再確認

#### タスク5.2: 修正内容のドキュメント化

**記録項目**:
- 修正箇所
- 修正内容
- 修正理由
- 参照したGitHubソース

---

## 📊 成果物

### 1. 検証スクリプト

- `scripts/validate_commands.sh` - コマンド検証
- `scripts/validate_config_keys.sh` - 設定キー検証
- `.git/hooks/pre-commit` - pre-commitフック

### 2. 検証レポート

- `validation-report-2025-10-26.md` - 検証結果の詳細レポート
- 検出された問題のリスト
- 修正内容のサマリー

### 3. 修正コミット

- 各修正ごとに個別コミット
- コミットメッセージに参照ソースを記載

---

## ✅ 完了基準

### 品質基準

| 項目 | 基準 | 検証方法 |
|------|------|---------|
| **コマンド正確性** | 100% | 全コマンドが`q --help`で確認済み |
| **設定キー正確性** | 100% | 全キーがスキーマに存在 |
| **環境変数正確性** | 100% | 全変数がソースコードに存在 |
| **バージョン情報正確性** | 100% | 全バージョンがGitHubリリースに存在 |
| **推測記載** | 0件 | 全て参照ソース明記 |

### 完了チェックリスト

- [ ] フェーズ1: 自動検証スクリプト作成完了
- [ ] フェーズ2: 優先度1ファイル検証完了
- [ ] フェーズ3: 優先度2ファイル検証完了
- [ ] フェーズ4: 優先度3-4ファイル検証完了
- [ ] フェーズ5: 全修正完了・再検証完了
- [ ] 検証レポート作成完了
- [ ] pre-commitフック導入完了

---

## 📅 スケジュール

| フェーズ | 所要時間 | 開始予定 | 完了予定 |
|---------|---------|---------|---------|
| フェーズ1 | 30分 | 06:45 | 07:15 |
| フェーズ2 | 2時間 | 07:15 | 09:15 |
| フェーズ3 | 1時間 | 09:15 | 10:15 |
| フェーズ4 | 1時間 | 10:15 | 11:15 |
| フェーズ5 | 2時間 | 11:15 | 13:15 |
| **合計** | **6.5時間** | **06:45** | **13:15** |

---

## 🚨 エスカレーション基準

以下の場合は作業を中断し、報告：

1. **GitHubソースとの重大な乖離を発見**
   - 50箇所以上の修正が必要
   - スキーマの大幅な変更

2. **自動検証が不可能な項目を発見**
   - 手動検証が必要な項目が多数

3. **予定時間を大幅に超過**
   - 各フェーズで予定時間の2倍を超過

---

*この水平展開により、サイト全体の信頼性を回復し、再発を防止します。*
