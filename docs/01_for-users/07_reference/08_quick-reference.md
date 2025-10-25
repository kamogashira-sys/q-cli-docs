[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [リファレンス](README.md) > 08 Quick Reference

---

# クイックリファレンス

よく使うコマンド、設定、トラブルシューティングを1ページにまとめた早見表です。

---

## 📋 目次

- [基本コマンド](#基本コマンド)
- [チャット操作](#チャット操作)
- [Agent操作](#agent操作)
- [設定管理](#設定管理)
- [よく使う設定項目](#よく使う設定項目)
- [環境変数](#環境変数)
- [トラブルシューティング](#トラブルシューティング)
- [ショートカットキー](#ショートカットキー)

---

## 基本コマンド

### インストール・更新

```bash
# Homebrewでインストール
brew install amazon-q

# 更新
brew upgrade amazon-q

# バージョン確認
q --version
```

### 初期設定

```bash
# 初回ログイン
q

# 設定確認
q settings list

# グローバル設定編集
q settings open
```

---

## チャット操作

### 基本的な使い方

```bash
# チャット開始
q chat

# 1回だけ質問
q chat "質問内容"

# Agentを指定してチャット
q chat --agent my-agent

# 特定のファイルをコンテキストに含める
q chat --context-file ./src/main.rs
```

### チャット中のコマンド

| コマンド | 説明 |
|---------|------|
| `/quit` | チャット終了 |
| `/clear` | 会話履歴をクリア |
| `/help` | ヘルプ表示 |
| `/context` | 現在のコンテキスト表示 |

---

## Agent操作

### Agent管理

```bash
# Agent一覧表示
q agent list

# Agent作成
q agent create my-agent

# Agent編集
q agent edit my-agent

# Agent削除
q agent delete my-agent

# Agent情報表示
q agent show my-agent
```

### Agent設定ファイル

**場所**: `./.q/agents/<agent-name>.json`

**基本構造**:

```json
{
  "name": "my-agent",
  "description": "説明",
  "instructions": "エージェントへの指示",
  "context": {
    "include": ["src/**/*.rs"],
    "exclude": ["target/**"]
  }
}
```

---

## 設定管理

### 設定の優先順位

1. **コマンドライン引数** (最優先)
2. **環境変数**
3. **Agent設定** (`./.q/agents/<name>.json`)
4. **グローバル設定** (`~/.amazonq/config.toml`)
5. **デフォルト値** (最低優先)

### 設定ファイルの場所

| 設定 | パス |
|------|------|
| グローバル設定 | `~/.amazonq/config.toml` |
| Agent設定 | `./.q/agents/<name>.json` |
| MCP設定 | `~/.amazonq/mcp.json` |

---

## よく使う設定項目

### グローバル設定 (`~/.amazonq/config.toml`)

```toml
# テレメトリー無効化
[telemetry]
enabled = false

# チャット設定
[chat]
model = "anthropic.claude-3-5-sonnet-20241022-v2:0"
temperature = 0.7
max_tokens = 4096

# Knowledge機能
[knowledge]
enabled = true
```

### Agent設定 (`./.q/agents/<name>.json`)

```json
{
  "name": "rust-dev",
  "instructions": "Rustの開発を支援してください",
  "context": {
    "include": ["src/**/*.rs", "Cargo.toml"],
    "exclude": ["target/**"]
  },
  "chat": {
    "model": "anthropic.claude-3-5-sonnet-20241022-v2:0"
  }
}
```

---

## 環境変数

### 重要な環境変数

| 変数名 | 説明 | 例 |
|--------|------|-----|
| `Q_TELEMETRY_ENABLED` | テレメトリー制御 | `false` |
| `Q_CHAT_MODEL` | チャットモデル | `anthropic.claude-3-5-sonnet-20241022-v2:0` |
| `Q_KNOWLEDGE_ENABLED` | Knowledge機能 | `true` |
| `Q_MCP_CONFIG_PATH` | MCP設定パス | `~/.amazonq/mcp.json` |
| `AWS_PROFILE` | AWSプロファイル | `default` |
| `AWS_REGION` | AWSリージョン | `us-east-1` |

### 設定例

```bash
# テレメトリー無効化
export Q_TELEMETRY_ENABLED=false

# モデル指定
export Q_CHAT_MODEL="anthropic.claude-3-5-sonnet-20241022-v2:0"

# Knowledge有効化
export Q_KNOWLEDGE_ENABLED=true
```

---

## トラブルシューティング

### よくある問題と解決方法

#### 1. ログインできない

```bash
# 認証情報をクリア
rm -rf ~/.amazonq/credentials

# 再ログイン
q
```

#### 2. チャットが応答しない

```bash
# 設定確認
q settings list

# ログ確認
tail -f ~/.amazonq/logs/q.log
```

#### 3. Agentが見つからない

```bash
# Agent一覧確認
q agent list

# カレントディレクトリ確認
pwd
ls -la .q/agents/
```

#### 4. コンテキストが大きすぎる

```json
{
  "context": {
    "exclude": [
      "node_modules/**",
      "target/**",
      "dist/**",
      "*.log"
    ]
  }
}
```

#### 5. MCP接続エラー

```bash
# MCP設定確認
cat ~/.amazonq/mcp.json

# MCPサーバー再起動
# (MCPサーバーのドキュメント参照)
```

---

## ショートカットキー

### チャット中

| キー | 説明 |
|------|------|
| `Ctrl+C` | 入力キャンセル |
| `Ctrl+D` | チャット終了 |
| `↑` / `↓` | 履歴移動 |
| `Tab` | 補完 |

### エディタ操作

| キー | 説明 |
|------|------|
| `Ctrl+E` | エディタで編集 |
| `Ctrl+S` | 保存 |
| `Ctrl+Q` | 保存せず終了 |

---

## 関連ドキュメント

### 詳細ガイド

- **[インストール](../01_getting-started/01_installation.md)** - インストール手順
- **[クイックスタート](../01_getting-started/02_quick-start.md)** - 5分で始める
- **[チャット機能](../02_features/01_chat.md)** - チャット機能の詳細
- **[Agent機能](../02_features/02_agents.md)** - Agent機能の詳細
- **[設定概要](../03_configuration/01_overview.md)** - 設定システムの全体像
- **[環境変数](../03_configuration/06_environment-variables.md)** - 環境変数の詳細
- **[コマンドリファレンス](./02_commands.md)** - 全コマンド一覧

### トラブルシューティング

- **[FAQ](../06_troubleshooting/01_faq.md)** - よくある質問
- **[一般的な問題](../06_troubleshooting/02_common-issues.md)** - トラブルシューティング

### コンテキスト管理

- **[コンテキスト管理完全ガイド](../08_guides/README.md)** - 8章構成の包括的ガイド
- **[ベストプラクティス](../08_guides/04_best-practices.md)** - 設計原則と実装パターン
- **[実践ガイド](../08_guides/05_practical-guide.md)** - プロジェクト別実装例

---

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2025-10-18 | 初版作成 |
