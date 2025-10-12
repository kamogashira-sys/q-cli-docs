# コマンドリファレンス

**最終更新**: 2025-10-11  
**対象バージョン**: v1.17.0以降

---

## 📋 概要

Amazon Q CLIの全コマンドの完全リストです。このリファレンスは実装に基づいて作成されています。

---

## 🚀 基本コマンド

### q chat
AIアシスタントとの対話を開始します。

```bash
q chat [OPTIONS]
```

**オプション**:
- `--agent <name>` - 使用するAgentを指定

**使用例**:
```bash
# デフォルトAgentでチャット開始
q chat

# 特定のAgentでチャット開始
q chat --agent aws-specialist
```

---

## 🤖 Agentコマンド

### q agent
Agentを管理します。

```bash
q agent <SUBCOMMAND>
```

**サブコマンド**:
- `list` - Agent一覧を表示
- `show <name>` - Agent詳細を表示
- `validate <name>` - Agent設定を検証
- `edit <name>` - Agent設定を編集

**使用例**:
```bash
# Agent一覧
q agent list

# Agent詳細
q agent show my-agent

# Agent検証
q agent validate my-agent

# Agent編集
q agent edit my-agent
```

---

## 🔐 認証コマンド

### q login
Amazon Qにログインします。

```bash
q login [OPTIONS]
```

**オプション**:
- `--license <type>` - ライセンスタイプ（pro/free）
- `--identity-provider <url>` - Identity Center URL
- `--region <region>` - リージョン
- `--use-device-flow` - デバイスフローで認証（ブラウザリダイレクトなし）

**使用例**:
```bash
# Builder IDでログイン
q login

# Identity Centerでログイン
q login --license pro --identity-provider https://my-org.awsapps.com/start

# デバイスフローでログイン
q login --use-device-flow
```

---

### q logout
Amazon Qからログアウトします。

```bash
q logout
```

---

### q whoami
現在のログイン情報を表示します。

```bash
q whoami [OPTIONS]
```

**オプション**:
- `--format <format>` - 出力形式（text/json）

**使用例**:
```bash
# テキスト形式で表示
q whoami

# JSON形式で表示
q whoami --format json
```

---

### q profile
現在のIDCユーザーに関連付けられたプロファイルを表示します。

```bash
q profile
```

---

## ⚙️ 設定コマンド

### q settings
設定を管理します。

```bash
q settings [OPTIONS] [KEY] [VALUE]
```

**サブコマンド**:
- `open` - 設定ファイルをエディタで開く
- `all` - すべての設定を表示

**オプション**:
- `--delete` - 設定を削除
- `--format <format>` - 出力形式（text/json）

**使用例**:
```bash
# すべての設定を表示
q settings all

# 特定の設定を取得
q settings chat.enableThinking

# 設定を変更
q settings chat.enableThinking true

# 設定を削除
q settings --delete chat.enableThinking

# 設定ファイルを開く
q settings open
```

---

## 🔍 診断コマンド

### q diagnostic
診断テストを実行します。

```bash
q diagnostic [OPTIONS]
```

**オプション**:
- `--format <format>` - 出力形式（text/json）

**使用例**:
```bash
# 診断実行
q diagnostic

# JSON形式で出力
q diagnostic --format json
```

---

## 🐛 問題報告コマンド

### q issue
GitHubのissueテンプレートを開きます。

```bash
q issue [OPTIONS]
```

**オプション**:
- `--title <title>` - issueのタイトル
- `--actual-behavior <text>` - 実際の動作
- `--expected-behavior <text>` - 期待される動作
- `--steps-to-reproduce <text>` - 再現手順

**使用例**:
```bash
# issueテンプレートを開く
q issue --title "Bug: Command fails"
```

---

## 🔌 MCPコマンド

### q mcp
Model Context Protocol (MCP)を管理します。

```bash
q mcp <SUBCOMMAND>
```

**サブコマンド**:
- `list` - MCPサーバー一覧を表示
- `install <name>` - MCPサーバーをインストール
- `uninstall <name>` - MCPサーバーをアンインストール

**使用例**:
```bash
# MCPサーバー一覧
q mcp list

# MCPサーバーをインストール
q mcp install my-server

# MCPサーバーをアンインストール
q mcp uninstall my-server
```

---

## 📚 チャット内コマンド

チャットセッション内で使用できるコマンドです。

### 基本コマンド

| コマンド | 説明 |
|---------|------|
| `/help` | ヘルプを表示 |
| `/clear` | 会話履歴をクリア |
| `/exit` | チャットを終了 |
| `/quit` | チャットを終了 |

### コンテキスト管理

| コマンド | 説明 |
|---------|------|
| `/context` | コンテキスト情報を表示 |
| `/context clear` | コンテキストをクリア |

### Knowledge管理

| コマンド | 説明 |
|---------|------|
| `/knowledge` | Knowledge情報を表示 |
| `/knowledge add <path>` | ファイル/ディレクトリを追加 |
| `/knowledge remove <path>` | ファイル/ディレクトリを削除 |
| `/knowledge clear` | Knowledgeをクリア |

### Checkpoint管理

| コマンド | 説明 |
|---------|------|
| `/checkpoint init` | Checkpointを初期化 |
| `/checkpoint list` | Checkpoint一覧を表示 |
| `/checkpoint restore <tag>` | Checkpointを復元 |

### TODO管理

| コマンド | 説明 |
|---------|------|
| `/todos` | TODO管理 |
| `/todos help` | ヘルプを表示 |
| `/todos view` | TODO一覧を表示 |
| `/todos clear-finished` | 完了済みTODOをクリア |
| `/todos resume` | TODOを再開 |
| `/todos delete` | TODOを削除 |
| `/todos delete --all` | すべてのTODOを削除 |

### 開発者向け

| コマンド | 説明 |
|---------|------|
| `/debug` | デバッグ情報を表示 |
| `/tools` | 利用可能なツール一覧を表示 |

---

## 📚 関連ドキュメント

- [チャット機能ガイド](../features/chat.md)
- [Agent設定ガイド](../configuration/agent-configuration.md)
- [設定項目リファレンス](settings-reference.md)
- [環境変数リファレンス](../configuration/environment-variables.md)

---

## ⚠️ 注意事項

1. **実装に基づく**: このリファレンスは実装（v1.17.0）に基づいて作成されています
2. **バージョン依存**: コマンドはバージョンによって変更される可能性があります
3. **ヘルプコマンド**: 最新情報は`q --help`または`q <command> --help`で確認してください

---

最終更新: 2025-10-09
