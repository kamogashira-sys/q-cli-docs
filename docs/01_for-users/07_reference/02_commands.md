# コマンドリファレンス

**最終更新**: 2025-10-12  
**対象バージョン**: v1.17.0以降

---

## 📋 概要

Amazon Q CLIの**全24コマンド**の完全リストです。このリファレンスは`q --help-all`の出力に基づいて作成されています。

## コマンド一覧（カテゴリ別）

### 基本・チャット（3コマンド）

| コマンド | 説明 |
|---------|------|
| [`q chat`](#q-chat) | AIアシスタントとの対話を開始 |
| [`q translate`](#q-translate) | 自然言語をシェルコマンドに翻訳 |
| [`q inline`](#q-inline) | インラインシェル補完を管理 |

### Agent管理（1コマンド）

| コマンド | 説明 |
|---------|------|
| [`q agent`](#q-agent) | Agentを管理（list, create, edit, validate） |

### 認証・ユーザー管理（5コマンド）

| コマンド | 説明 |
|---------|------|
| [`q login`](#q-login) | Amazon Qにログイン（Builder ID / Identity Center） |
| [`q logout`](#q-logout) | Amazon Qからログアウト |
| [`q whoami`](#q-whoami) | 現在のログイン情報を表示 |
| [`q profile`](#q-profile) | IDCユーザーのプロファイル情報を表示 |
| [`q user`](#q-user) | アカウントを管理（login, logout, whoami, profile） |

### 設定・診断（4コマンド）

| コマンド | 説明 |
|---------|------|
| [`q settings`](#q-settings) | 設定を管理（取得・変更・削除・ファイルを開く） |
| [`q diagnostic`](#q-diagnostic) | 診断テストを実行 |
| [`q doctor`](#q-doctor) | 一般的な問題を診断・修正 |
| [`q debug`](#q-debug) | アプリをデバッグ |

### アプリケーション管理（5コマンド）

| コマンド | 説明 |
|---------|------|
| [`q launch`](#q-launch) | デスクトップアプリを起動 |
| [`q quit`](#q-quit) | デスクトップアプリを終了 |
| [`q restart`](#q-restart) | デスクトップアプリを再起動 |
| [`q update`](#q-update) | Amazon Qアプリを更新 |
| [`q dashboard`](#q-dashboard) | ダッシュボードを開く |

### セットアップ・統合（3コマンド）

| コマンド | 説明 |
|---------|------|
| [`q setup`](#q-setup) | CLIコンポーネントをセットアップ |
| [`q init`](#q-init) | シェル用dotfilesを生成 |
| [`q integrations`](#q-integrations) | システム統合を管理 |

### その他（3コマンド）

| コマンド | 説明 |
|---------|------|
| [`q mcp`](#q-mcp) | MCPサーバーを管理（add, remove, list） |
| [`q theme`](#q-theme) | テーマを取得・設定 |
| [`q issue`](#q-issue) | GitHub issueテンプレートを開く |

> 💡 チャットセッション内で使用できるコマンド（`/help`, `/clear`, `/context`など）は [チャット内コマンド](#チャット内コマンド) を参照してください。

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

## 🚀 基本コマンド

### q translate
自然言語をシェルコマンドに翻訳します。

```bash
q translate [INPUT]...
```

**使用例**:
```bash
# 自然言語でコマンドを生成
q translate "現在のディレクトリのファイル一覧を表示"
```

---

### q inline
インラインシェル補完を管理します。

```bash
q inline <SUBCOMMAND>
```

**サブコマンド**:
- `enable` - インライン補完を有効化
- `disable` - インライン補完を無効化
- `status` - インライン補完の状態を表示
- `set-customization` - カスタマイズを選択
- `show-customizations` - 利用可能なカスタマイズを表示

**使用例**:
```bash
# インライン補完を有効化
q inline enable

# 状態確認
q inline status
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
- `create` - Agent設定を作成
- `edit <name>` - Agent設定を編集
- `validate <name>` - Agent設定を検証
- `migrate` - プロファイルをAgentに移行
- `set-default` - デフォルトAgentを設定

**使用例**:
```bash
# Agent一覧
q agent list

# Agent作成
q agent create

# Agent編集
q agent edit my-agent

# Agent検証
q agent validate my-agent

# デフォルトAgent設定
q agent set-default my-agent
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

### q user
アカウントを管理します（login, logout, whoami, profileのラッパー）。

```bash
q user <SUBCOMMAND>
```

**サブコマンド**:
- `login` - ログイン
- `logout` - ログアウト
- `whoami` - ユーザー情報を表示
- `profile` - プロファイル情報を表示

**使用例**:
```bash
# ログイン
q user login

# ユーザー情報表示
q user whoami
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
- `--format <format>` - 出力形式（plain/json/json-pretty）
- `--force` - 限定的な診断出力を強制

**使用例**:
```bash
# 診断実行
q diagnostic

# JSON形式で出力
q diagnostic --format json
```

---

### q doctor
一般的な問題を診断・修正します。

```bash
q doctor [OPTIONS]
```

**オプション**:
- `--all` - すべてのテストを実行（修正なし）
- `--strict` - 警告をエラーとして扱う

**使用例**:
```bash
# 問題を診断・修正
q doctor

# すべてのテストを実行
q doctor --all
```

---

### q debug
アプリをデバッグします。

```bash
q debug <SUBCOMMAND>
```

**サブコマンド**:
- `app` - アプリをデバッグ
- `logs` - デバッグログを表示
- `diagnostics` - 診断を監視
- `devtools` - 特定のWebビューのDevToolsを開く
- その他多数のデバッグ機能

**使用例**:
```bash
# デバッグログを表示
q debug logs

# 診断を監視
q debug diagnostics
```

---

## 🐛 問題報告コマンド

### q issue
GitHubのissueテンプレートを開きます。

```bash
q issue [OPTIONS] [DESCRIPTION]...
```

**オプション**:
- `--force` - issue作成を強制

**使用例**:
```bash
# issueテンプレートを開く
q issue "Bug: Command fails"
```

---

## 🖥️ アプリケーション管理コマンド

### q launch
デスクトップアプリを起動します。

```bash
q launch
```

---

### q quit
デスクトップアプリを終了します。

```bash
q quit
```

---

### q restart
デスクトップアプリを再起動します。

```bash
q restart
```

---

### q update
Amazon Qアプリを更新します。

```bash
q update [OPTIONS]
```

**オプション**:
- `--non-interactive` / `-y` - 確認なしで更新
- `--relaunch-dashboard` - 更新後にダッシュボードを再起動
- `--rollout` - ロールアウトを使用

**使用例**:
```bash
# 対話的に更新
q update

# 確認なしで更新
q update -y
```

---

### q dashboard
ダッシュボードを開きます。

```bash
q dashboard
```

---

## 🔧 セットアップ・統合コマンド

### q setup
CLIコンポーネントをセットアップします。

```bash
q setup [OPTIONS]
```

**オプション**:
- `--dotfiles` - シェル統合のみインストール
- `--input-method` - 入力メソッドのインストールをプロンプト
- `--no-confirm` - 自動インストールを確認しない
- `--force` - qを強制的にインストール
- `--global` - qをグローバルにインストール

**使用例**:
```bash
# セットアップ実行
q setup

# dotfilesのみインストール
q setup --dotfiles
```

---

### q init
シェル用dotfilesを生成します。

```bash
q init <SHELL> <WHEN>
```

**引数**:
- `<SHELL>` - シェルタイプ（bash/zsh/fish/nu）
- `<WHEN>` - タイミング（pre/post）

**使用例**:
```bash
# Bash用のpre dotfilesを生成
q init bash pre

# Zsh用のpost dotfilesを生成
q init zsh post
```

---

### q integrations
システム統合を管理します。

```bash
q integrations <SUBCOMMAND>
```

**サブコマンド**:
- `install` - 統合をインストール
- `uninstall` - 統合をアンインストール
- `reinstall` - 統合を再インストール
- `status` - 統合の状態を表示

**使用例**:
```bash
# 統合の状態を確認
q integrations status

# 統合をインストール
q integrations install
```

---

## 🎨 その他のコマンド

### q theme
テーマを取得・設定します。

```bash
q theme [OPTIONS] [THEME]
```

**オプション**:
- `--list` - 利用可能なテーマを一覧表示
- `--folder` - テーマフォルダを開く

**使用例**:
```bash
# テーマ一覧を表示
q theme --list

# テーマを設定
q theme dark
```

---

## 🔌 MCPコマンド

### q mcp
Model Context Protocol (MCP)を管理します。

```bash
q mcp <SUBCOMMAND>
```

**サブコマンド**:
- `add` - サーバーを追加または置換
- `remove` - サーバーを削除
- `list` - 設定済みサーバーを一覧表示
- `import` - 別ファイルからサーバー設定をインポート
- `status` - サーバーの状態を取得

**使用例**:
```bash
# MCPサーバー一覧
q mcp list

# MCPサーバーを追加
q mcp add

# MCPサーバーを削除
q mcp remove <server-name>

# MCPサーバーの状態を確認
q mcp status <server-name>

# 別ファイルから設定をインポート
q mcp import <config-file>
```

---

## 📚 チャット内コマンド

チャットセッション内で使用できるコマンドです。

### 基本コマンド

| コマンド | 説明 |
|---------|------|
| `/help` | ヘルプを表示 |
| `/clear` | 会話履歴をクリア |
| `/quit` | チャットを終了 |
| `/exit` | チャットを終了（`/quit`のエイリアス） |
| `/q` | チャットを終了（`/quit`のエイリアス） |

### Agent管理

| コマンド | 説明 |
|---------|------|
| `/agent` | Agent管理 |
| `/agent help` | ヘルプを表示 |
| `/agent list` | Agent一覧を表示 |
| `/agent create` | Agentを作成 |
| `/agent delete` | Agentを削除 |
| `/agent rename` | Agent名を変更 |
| `/agent set` | Agentを設定 |
| `/agent schema` | Agentスキーマを表示 |
| `/agent generate` | Agentを生成 |

### コンテキスト管理

| コマンド | 説明 |
|---------|------|
| `/context` | コンテキスト情報を表示 |
| `/context help` | ヘルプを表示 |
| `/context show` | コンテキストを表示 |
| `/context show --expand` | コンテキストを展開表示 |
| `/context add` | コンテキストを追加 |
| `/context rm` | コンテキストを削除 |
| `/context clear` | コンテキストをクリア |

### Knowledge管理

| コマンド | 説明 |
|---------|------|
| `/knowledge` | Knowledge情報を表示 |
| `/knowledge help` | ヘルプを表示 |
| `/knowledge show` | Knowledge情報を表示 |
| `/knowledge add` | ファイル/ディレクトリを追加 |
| `/knowledge remove` | ファイル/ディレクトリを削除 |
| `/knowledge clear` | Knowledgeをクリア |
| `/knowledge search` | Knowledgeを検索 |
| `/knowledge update` | Knowledgeを更新 |
| `/knowledge status` | Knowledgeステータスを表示 |
| `/knowledge cancel` | Knowledge処理をキャンセル |

### Checkpoint管理

| コマンド | 説明 |
|---------|------|
| `/checkpoint` | Checkpoint管理 |
| `/checkpoint help` | ヘルプを表示 |
| `/checkpoint init` | Checkpointを初期化 |
| `/checkpoint list` | Checkpoint一覧を表示 |
| `/checkpoint restore` | Checkpointを復元 |
| `/checkpoint expand` | Checkpointを展開 |
| `/checkpoint diff` | Checkpoint差分を表示 |
| `/checkpoint clean` | Checkpointをクリーンアップ |

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

### フック管理

| コマンド | 説明 |
|---------|------|
| `/hooks` | フック情報を表示 |
| `/hooks help` | ヘルプを表示 |
| `/hooks add` | フックを追加 |
| `/hooks rm` | フックを削除 |
| `/hooks enable` | フックを有効化 |
| `/hooks disable` | フックを無効化 |
| `/hooks enable-all` | すべてのフックを有効化 |
| `/hooks disable-all` | すべてのフックを無効化 |

### Tangent管理

| コマンド | 説明 |
|---------|------|
| `/tangent` | Tangentモードを切り替え |
| `/tangent tail` | Tangent履歴を表示 |

### その他のコマンド

| コマンド | 説明 |
|---------|------|
| `/editor` | エディタでプロンプトを作成 |
| `/reply` | 最新のアシスタントメッセージに返信 |
| `/issue` | GitHub ISSUEを作成 |
| `/mcp` | MCPサーバーを表示 |
| `/model` | モデルを選択 |
| `/experiment` | 実験機能を切り替え |
| `/prompts` | プロンプトを表示・取得 |
| `/compact` | 会話を要約 |
| `/compact help` | compactヘルプを表示 |
| `/usage` | コンテキスト使用状況を表示 |
| `/changelog` | 変更履歴を表示 |
| `/save` | 会話を保存 |
| `/load` | 会話を読み込み |
| `/subscribe` | Q Developer Proサブスクリプション |

### ツール管理

| コマンド | 説明 |
|---------|------|
| `/tools` | ツールと権限を表示 |
| `/tools trust` | ツールを信頼 |
| `/tools untrust` | ツールの信頼を解除 |
| `/tools trust-all` | すべてのツールを信頼 |
| `/tools reset` | ツール設定をリセット |

---

## 📚 関連ドキュメント

- [チャット機能ガイド](../02_features/01_chat.md)
- [Agent設定ガイド](../03_configuration/04_agent-configuration.md)
- [設定項目リファレンス](03_settings-reference.md)
- [環境変数リファレンス](../03_configuration/05_environment-variables.md)

---

## ⚠️ 注意事項

1. **実装に基づく**: このリファレンスは実装（v1.17.0）に基づいて作成されています
2. **バージョン依存**: コマンドはバージョンによって変更される可能性があります
3. **ヘルプコマンド**: 最新情報は`q --help`または`q <command> --help`で確認してください

---

最終更新: 2025-10-09
