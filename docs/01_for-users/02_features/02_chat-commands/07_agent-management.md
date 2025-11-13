[ホーム](../../../README.md) > [ユーザーガイド](../../README.md) > [機能ガイド](../README.md) > [チャット機能](../01_chat.md) > Agent管理

---

# Agent管理

**対象バージョン**: v1.13.0以降

## 📋 コマンド概要

Agent管理機能は、Q CLIで使用するAgentの確認・切り替えを行う機能です。Agentは、プロジェクトや用途に応じてAIの動作をカスタマイズする設定ファイルです。異なるプロジェクトや開発フェーズに応じて、最適なAgentを選択できます。

## 🚀 基本的な使い方

### Agent管理コマンド一覧

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/agent` | 現在使用中のAgent情報を表示。Agent名、設定内容、有効なツールを確認できる | 現在どのAgentを使っているか確認したい時 |
| `/agent list` | 利用可能なAgent一覧を表示。グローバルとローカルのAgentを確認できる | 切り替え可能なAgentを確認したい時 |
| `/agent switch <name>` | 指定したAgentに切り替え。プロジェクトや用途に応じてAgentを変更できる | 別のプロジェクトに切り替える時、専門的なAgentを使いたい時 |
| `/model [モデル名]` | 使用するAIモデルを表示または切り替え。モデル名省略時は現在のモデルを表示 | より高性能なモデルに切り替えたい時、コスト削減のため軽量モデルに変更する時 |

### 基本例

```bash
# 現在のAgent情報を確認
/agent

# 利用可能なAgent一覧を表示
/agent list

# 特定のAgentに切り替え
/agent switch development-agent

# 現在のモデルを確認
/model

# モデルを切り替え
/model claude-3-5-sonnet-20241022
```

## ⚙️ オプション・引数

### `/agent` コマンド

| サブコマンド | 説明 | 使用例 |
|-------------|------|--------|
| `[なし]` | 現在のAgent情報を表示 | `/agent` |
| `list` | 利用可能なAgent一覧を表示 | `/agent list` |
| `switch <name>` | 指定したAgentに切り替え | `/agent switch my-agent` |

### `/model` コマンド

| 引数 | 説明 | 必須 |
|------|------|------|
| `[モデル名]` | 切り替え先のモデル名（省略時は現在のモデルを表示） | いいえ |

### Agentの保存場所

| 場所 | パス | 用途 |
|------|------|------|
| **ローカル** | `.amazonq/cli-agents/` | プロジェクト固有のAgent |
| **グローバル** | `~/.aws/amazonq/cli-agents/` | 全プロジェクト共通のAgent |

### 利用可能なモデル

| モデル名 | 特徴 | 用途 |
|---------|------|------|
| `claude-3-5-sonnet-20241022` | 高性能・最新 | 複雑なタスク、高精度が必要な作業 |
| `claude-3-5-haiku-20241022` | 高速・軽量 | 簡単なタスク、コスト重視の作業 |
| `claude-3-opus-20240229` | 最高性能 | 最も複雑なタスク、創造的な作業 |

## 💡 実用例

### 例1: プロジェクト別Agent管理

**シナリオ**: 複数のプロジェクトで異なるAgentを使い分けたい

```bash
# 現在のAgent状況を確認
/agent

# 出力例:
# Current Agent: default
# Configuration: ~/.aws/amazonq/cli-agents/default.json
# Tools: fs_read, fs_write, execute_bash
# Hooks: none

# 利用可能なAgentを確認
/agent list

# 出力例:
# Available Agents:
# 📁 Local (.amazonq/cli-agents/):
#   - web-development
#   - data-analysis
# 🌐 Global (~/.aws/amazonq/cli-agents/):
#   - default
#   - security-audit

# Web開発用Agentに切り替え
/agent switch web-development

# 切り替え後の確認
/agent

# 出力例:
# Current Agent: web-development
# Configuration: .amazonq/cli-agents/web-development.json
# Tools: fs_read, fs_write, execute_bash, npm_commands
# Hooks: 
#   - preToolUse: eslint check
#   - postToolUse: prettier format
```

**結果**: プロジェクトに最適化されたツールとフックが利用できる

### 例2: 用途別モデル選択

**シナリオ**: タスクの複雑さに応じてモデルを使い分けたい

```bash
# 現在のモデルを確認
/model

# 出力例:
# Current model: claude-3-5-haiku-20241022

# 複雑なアーキテクチャ設計のため高性能モデルに切り替え
/model claude-3-5-sonnet-20241022

# モデル切り替えの確認
/model

# 出力例:
# Current model: claude-3-5-sonnet-20241022

# 簡単なコード修正のため軽量モデルに戻す
/model claude-3-5-haiku-20241022
```

**結果**: タスクに応じて最適なコストパフォーマンスでAIを利用できる

### 例3: セキュリティ監査用Agent設定

**シナリオ**: セキュリティ監査専用のAgentを作成・使用したい

```bash
# セキュリティ監査用Agentに切り替え
/agent switch security-audit

# Agent設定の確認
/agent

# 出力例:
# Current Agent: security-audit
# Configuration: ~/.aws/amazonq/cli-agents/security-audit.json
# Tools: fs_read, execute_bash, security_scan
# Hooks:
#   - preToolUse: security_check
#   - postToolUse: audit_log
# Context Rules:
#   - Include: *.py, *.js, *.ts, *.json
#   - Exclude: node_modules/*, .git/*
# Prompts:
#   - security-review
#   - vulnerability-scan

# セキュリティ専用プロンプトを使用
@security-review

# 監査ログの確認
cat /var/log/q-cli-security-audit.log
```

**Agent設定ファイル例** (`~/.aws/amazonq/cli-agents/security-audit.json`):
```json
{
  "name": "security-audit",
  "description": "Security audit and vulnerability assessment",
  "model": "claude-3-5-sonnet-20241022",
  "tools": {
    "allowed": ["fs_read", "execute_bash"],
    "restricted": ["fs_write"]
  },
  "hooks": {
    "preToolUse": [
      {
        "matcher": "execute_bash",
        "command": "echo \"$(date): Security scan initiated\" >> /var/log/q-cli-security-audit.log"
      }
    ],
    "postToolUse": [
      {
        "matcher": "*",
        "command": "echo \"$(date): Action completed - $(cat)\" >> /var/log/q-cli-security-audit.log"
      }
    ]
  },
  "context": {
    "include": ["*.py", "*.js", "*.ts", "*.json", "*.yaml", "*.yml"],
    "exclude": ["node_modules/**", ".git/**", "*.log"]
  }
}
```

**結果**: セキュリティに特化した環境で安全に監査作業を実行できる

## 🔧 トラブルシューティング

### よくある問題

#### 問題1: Agentが見つからない

**症状**: `/agent switch` でAgentが見つからないエラーが発生

**原因**: Agent名の間違い、またはファイルが存在しない

**解決策**:
```bash
# 利用可能なAgentを確認
/agent list

# Agent設定ファイルの存在確認
ls -la .amazonq/cli-agents/
ls -la ~/.aws/amazonq/cli-agents/

# 正確なAgent名で再試行
/agent switch web-development
```

#### 問題2: Agent切り替え後にツールが使用できない

**症状**: Agent切り替え後、特定のツールが利用できない

**原因**: Agent設定でツールが制限されている

**解決策**:
```bash
# 現在のAgent設定を確認
/agent

# Agent設定ファイルを確認
cat .amazonq/cli-agents/my-agent.json

# 必要に応じて設定を修正
# または別のAgentに切り替え
/agent switch default
```

#### 問題3: モデル切り替えができない

**症状**: `/model` でモデル名を指定してもエラーが発生

**原因**: モデル名の間違い、または利用権限の問題

**解決策**:
```bash
# 現在のモデルを確認
/model

# 利用可能なモデルを確認（Q CLI設定で）
q settings list | grep model

# 正確なモデル名で再試行
/model claude-3-5-sonnet-20241022

# Q CLIの認証状態を確認
q --version
```

#### 問題4: Agent設定が反映されない

**症状**: Agent設定ファイルを変更しても反映されない

**原因**: 設定ファイルの構文エラー、またはキャッシュの問題

**解決策**:
```bash
# 設定ファイルの構文を確認
cat .amazonq/cli-agents/my-agent.json | jq .

# チャットを再起動
/quit
q chat

# Agent を再選択
/agent switch my-agent
```

#### 問題5: フックが実行されない

**症状**: Agent設定でフックを定義したが実行されない

**原因**: フック設定の構文エラー、またはコマンドパスの問題

**解決策**:
```bash
# フック設定を確認
/hooks

# Agent設定のフック部分を確認
cat .amazonq/cli-agents/my-agent.json | jq .hooks

# コマンドのパスを確認
which eslint
which prettier

# 手動でコマンドをテスト
eslint --version
```

## 🔗 関連コマンド

- [コンテキスト管理](02_context-management.md) - `/hooks`によるフック確認
- [基本コマンド・会話管理](01_basic-commands.md) - Agent設定の保存・復元
- [開発者向けコマンド](08_developer-commands.md) - `/experiment`による機能有効化

## 📖 参照元

- [チャット機能概要](../01_chat.md#agent管理) - Agent管理の概要
- [Agent設定ガイド](../../03_configuration/03_agent-configuration.md) - Agent設定の詳細
- [Agent機能ガイド](../02_agents.md) - Agent機能の包括的な説明

---

最終更新: 2025年11月13日
