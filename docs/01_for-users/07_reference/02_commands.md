[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [リファレンス](README.md) > 02 Commands

---

# コマンドリファレンス

最終更新: 2025-10-12  
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
q chat [OPTIONS] [INPUT]
```

**引数**:
- `[INPUT]` - 最初に質問する内容

**オプション**:
- `--agent <name>` - 使用するAgentを指定
- `--model <model>` - 使用するモデルを指定
- `-r, --resume` - このディレクトリの前回の会話を再開
- `-a, --trust-all-tools` - 確認なしで全てのツールの使用を許可
- `--trust-tools <TOOL_NAMES>` - 特定のツールのみ信頼（例: `--trust-tools=fs_read,fs_write`）
- `--no-interactive` - ユーザー入力を期待せずに実行
- `-w, --wrap <WRAP>` - 行の折り返し動作を制御（always/never/auto）

**使用例**:
```bash
# デフォルトAgentでチャット開始
q chat

# 特定のAgentでチャット開始
q chat --agent aws-specialist

# 質問を指定して開始
q chat "Pythonでファイルを読み込む方法は？"

# 前回の会話を再開
q chat --resume

# 特定のモデルを使用
q chat --model anthropic.claude-3-5-sonnet-20241022-v2:0

# 全てのツールを自動承認
q chat --trust-all-tools
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
- `list` - Agent一覧を表示（グローバル + ローカル）
- `create` - Agent設定を作成
  - `--name` (`-n`): Agent名
  - `--directory` (`-d`): 保存先ディレクトリ（省略時はグローバル）
  - `--from` (`-f`): ベースとなるAgent名
- `edit` - Agent設定を編集
  - `--name` (`-n`): Agent名
- `validate` - Agent設定を検証
  - `--path` (`-p`): 設定ファイルパス
- `migrate` - プロファイルをAgentに移行
  - `--force`: 既存Agentを上書き
- `set-default` - デフォルトAgentを設定
  - `--name` (`-n`): Agent名

**使用例**:
```bash
# Agent一覧
q agent list

# Agent作成（グローバル）
q agent create --name my-agent

# 既存Agentをベースに作成
q agent create --name new-agent --from my-agent

# ローカルディレクトリに作成
q agent create --name local-agent --directory ./.amazonq/cli-agents

# Agent編集
q agent edit --name my-agent

# Agent検証
q agent validate --path ~/.aws/amazonq/cli-agents/my-agent.json

# デフォルトAgent設定
q agent set-default --name my-agent
```

**チャット内コマンドとの違い**:
- **CLI (`q agent`)**: Agent設定の管理（作成、編集、検証）
- **チャット内 (`/agent`)**: ランタイムでのAgent切り替え、AI生成、スキーマ表示

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
- `--format <format>` - 出力形式（plain/json/json-pretty）

**使用例**:
```bash
# テキスト形式で表示
q whoami

# JSON形式で表示
q whoami --format json

# 整形されたJSON形式で表示
q whoami --format json-pretty
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

チャットセッション内で使用できるコマンドです。`/`で始まるコマンドを入力することで、会話の管理、設定の変更、機能の利用ができます。

**全25コマンド**: 基本操作(5) / 会話管理(4) / Agent・設定(4) / タスク管理(2) / Knowledge・情報管理(2) / 開発者向け(5) / 情報表示(4) / 問題報告(1)

---

### 基本操作

#### `/help` - ヘルプ表示

**目的**: チャット内コマンドの一覧とヘルプ情報を表示する

**使用シーン**: 利用可能なコマンドを確認する / コマンドの使い方を思い出す

**使用方法**: `/help`

**関連コマンド**: `/whatsnew`, `/changelog`

---

#### `/clear` - 会話履歴クリア

**目的**: 現在のセッションの会話履歴をクリアする

**使用シーン**: 新しいトピックを開始する / コンテキストウィンドウをリセットする / 機密情報を含む会話をクリアする

**使用方法**: `/clear`

**注意点**:
- ⚠️ クリアした会話履歴は復元できません
- ⚠️ `/knowledge` で追加した情報は削除されません

**関連コマンド**: `/save`, `/tangent`

---

#### `/quit` / `/exit` / `/q` - チャット終了

**目的**: チャットセッションを終了する

**使用方法**: `/quit` または `/exit` または `/q`

**注意点**: 重要な会話は `/save` で保存してから終了

---

### 会話管理

#### `/save` - 会話保存

**目的**: 現在の会話をファイルに保存する

**使用シーン**: 重要な会話を記録する / 作業を中断して後で再開する

**使用方法**:
```
/save [ファイル名]
```

**使用例**:
```bash
/save                      # デフォルトのファイル名で保存
/save my-conversation.json # 指定したファイル名で保存
```

**関連コマンド**: `/load`

---

#### `/load` - 会話読み込み

**目的**: 保存した会話をファイルから読み込む

**使用シーン**: 中断した作業を再開する / 過去の会話を参照する

**使用方法**:
```
/load [ファイル名]
```

**注意点**: 読み込む前に現在の会話を `/save` で保存することを推奨

**関連コマンド**: `/save`

---

#### `/context` - コンテキスト管理

**目的**: 現在のセッションのコンテキスト情報を管理する

**使用シーン**: コンテキストウィンドウの使用状況を確認する / どの情報がコンテキストに含まれているか確認する

**使用方法**: 
```
/context [サブコマンド] [オプション]
```

**サブコマンド**:
- `show`: コンテキスト情報を表示
  - `--expand`: 各ファイルの内容を展開表示
- `add <path>`: ファイルをコンテキストに追加
  - `--force` (`-f`): サイズ制限を無視して強制追加
- `remove <pattern>` (alias: `rm`): ファイルをコンテキストから削除
- `clear`: すべてのコンテキストファイルをクリア

**コンテキストファイルの制限**:
- 最大サイズ: コンテキストウィンドウの75%
- 超過時: 自動的にドロップされ、警告が表示される

**使用例**:
```bash
# コンテキスト情報を表示
/context show

# 詳細表示（ファイル内容を展開）
/context show --expand

# ファイルを追加
/context add README.md

# サイズ制限を無視して追加（注意が必要）
/context add --force large-file.md

# パターンで削除
/context remove "*.test.js"

# エイリアスを使用して削除
/context rm "*.test.js"

# すべてクリア
/context clear
```

**警告メッセージ**:
```
Total token count exceeds limit: 150000.
The following files will be automatically dropped when interacting with Q.
Consider removing them.
```

**関連コマンド**: `/clear`, `/knowledge`, `/experiment`, `/compact`

**実験的機能**: `Context Usage Percentage` を有効にすると、プロンプトにコンテキスト使用率が表示されます

**詳細**: [コンテキスト管理ガイド](../08_guides/README.md) - コンテキストの概念、管理方法、ベストプラクティスを包括的に解説

---

#### `/tangent` - Tangentモード

**目的**: 会話のチェックポイントを作成し、サイドトピックを探索後に元の会話に戻る

**説明**: メインの会話を保持したまま、別のトピックを探索し、後で元の会話に戻ることができます。

**使用シーン**: メインの会話を中断せずに別の質問をしたい / 代替案を探索したい / Q CLIの使い方を確認したい

**使用方法**:
```
/tangent          # Tangentモードに入る/戻る
Ctrl+T            # キーボードショートカット
```

**有効化方法**:
```bash
q settings set chat.enableTangentMode true
# または /experiment で有効化
```

**注意点**:
- ⚠️ 実験的機能（デフォルトで無効）
- ⚠️ チェックポイント以降の会話は保存されない

**関連コマンド**: `/checkpoint`, `/experiment`

---

### Agent・設定

#### `/agent` - Agent管理

**目的**: Agentの管理と切り替え

**使用シーン**: プロジェクト固有のAgent設定を使用する / 異なるタスクに最適化されたAgentに切り替える

**主要サブコマンド**:
```
/agent list                    # Agent一覧を表示
/agent swap [Agent名]          # Agentを切り替え（引数なしで対話的選択）
/agent create --name <name>    # 新しいAgentを作成
/agent edit --name <name>      # 既存のAgentを編集
/agent generate                # AIを使ってAgent設定を生成
/agent schema                  # Agent設定のスキーマを表示
/agent set-default --name <name>  # デフォルトAgentを設定
```

**使用例**:
```bash
/agent list              # Agent一覧を表示
/agent swap              # 対話的にAgentを選択
/agent swap rust-agent   # 特定のAgentに切り替え
```

**関連コマンド**: `/tools`, `/hooks`, `/mcp`, `/prompts`

---

#### `/model` - モデル切り替え

**目的**: 使用するAIモデルを切り替える

**使用シーン**: 複雑なタスクに高性能モデルを使用する / コストを最適化する

**使用方法**: `/model [モデル名]`

**注意点**: モデルによってコストと能力が異なる

---

#### `/experiment` - 実験的機能管理

**目的**: 実験的機能のON/OFFを切り替え、新機能を試す

**説明**: 対話的なメニューで実験的機能を管理します。

**使用方法**: `/experiment`

**実験的機能一覧**:
1. **Checkpointing** - ファイル変更のGitベーストラッキング
2. **Context Usage Percentage** - コンテキスト使用率の表示
3. **Knowledge** - 永続的なナレッジベース
4. **Thinking** - 複雑な推論プロセスの表示
5. **Tangent Mode** - 会話の分岐機能
6. **Delegate** - 非同期タスクプロセス管理
7. **TODO Lists** - TODOリスト管理

**関連コマンド**: `/checkpoint`, `/knowledge`, `/tangent`, `/todos`

---

#### `/prompts` - プロンプト管理

**目的**: カスタムプロンプトを管理する

**使用シーン**: 現在のAgentのプロンプトを確認する / プロンプトの効果を理解する

**使用方法**: `/prompts`

**関連コマンド**: `/agent`, `/model`

---

### タスク管理

#### `/todos` - TODO管理

**目的**: 永続的なTODOリストを管理し、複雑なタスクを追跡・再開する

**説明**: Q CLIが複雑なタスクを分解した際に自動作成されるTODOリストを管理します。

**使用シーン**: 複雑なタスクの進捗を確認したい / 中断した作業を再開したい

**使用方法**:
```
/todos view              # TODO一覧を表示
/todos resume            # TODOを再開
/todos clear-finished    # 完了済みTODOをクリア
/todos delete            # TODOを削除
```

**有効化方法**:
```bash
q settings set chat.enableTodoList true
# または /experiment で有効化
```

**保存場所**: `.amazonq/cli-todo-lists/`

**関連コマンド**: `/checkpoint`, `/experiment`

---

#### `/checkpoint` - Checkpointing

**目的**: ファイル変更をGitベースでトラッキングし、任意の時点に復元できるチェックポイントを管理する

**説明**: セッション中のファイル変更をシャドウGitリポジトリにスナップショットとして保存します。

**使用シーン**: コード変更を段階的に追跡する / 実験的な変更を試してから元に戻す

**使用方法**:
```
/checkpoint init                      # チェックポイントを初期化
/checkpoint list [--limit N]         # チェックポイント一覧を表示
/checkpoint expand <tag>              # 詳細を表示
/checkpoint diff <tag1> [tag2|HEAD]  # 差分を表示
/checkpoint restore [<tag>] [--hard] # 復元
/checkpoint clean                     # クリーンアップ
```

**有効化方法**:
```bash
q settings set EnabledCheckpointing true
# または /experiment で有効化
```

**注意点**:
- ⚠️ 実験的機能（デフォルトで無効）
- ⚠️ Gitリポジトリ内では自動有効化
- ⚠️ `--hard` オプションは完全復元（チェックポイント後に作成されたファイルも削除）

**関連コマンド**: `/tangent`, `/experiment`

---

### Knowledge・情報管理

#### `/knowledge` - Knowledge管理

**目的**: プロジェクトドキュメントやコードを永続的なナレッジベースとして保存し、セッション間で情報を共有する

**説明**: ファイルやディレクトリをインデックス化して永続的なナレッジベースを構築します。セマンティック検索により、関連する情報を効率的に取得できます。

**使用シーン**: プロジェクトドキュメントをインデックス化する / 大規模なコードベースから関連情報を検索する

**使用方法**:
```
/knowledge show                    # ナレッジベース情報を表示（v1.18.0+: statusと統合）
/knowledge add <path>              # ファイル/ディレクトリを追加
/knowledge add -n <name> -p <path> # 名前とパスを指定して追加（v1.18.0+）
/knowledge remove <path>           # エントリを削除（alias: rm）
/knowledge update <path>           # エントリを更新
/knowledge clear                   # すべてのエントリを削除
/knowledge cancel [operation_id]   # バックグラウンド処理をキャンセル（IDなしで最新をキャンセル）
```

**v1.18.0の変更点**:
- `show` と `status` コマンドが統合されました
- `--path` (`-p`) と `--name` (`-n`) 引数が追加されました
- より一貫性のあるインターフェースを提供

**有効化方法**:
```bash
q settings set chat.enableKnowledge true
# または /experiment で有効化
```

**使用例**:
```bash
# プロジェクトドキュメントをインデックス化
/knowledge add -n docs -p docs/ --include "*.md"

# インデックスタイプを指定（Fast: 高速、Best: 高精度）
/knowledge add -n myproject -p /path/to/project --index-type Best

# ソースコードを追加（テストファイルを除外）
/knowledge add -n src -p src/ --exclude "*.test.js" --exclude "node_modules/**"

# エントリを削除
/knowledge remove docs/
/knowledge rm docs/  # エイリアスを使用

# バックグラウンド処理をキャンセル
/knowledge cancel              # 最新の処理をキャンセル
/knowledge cancel abc123       # 特定の処理をキャンセル

# 統合されたshowコマンド（エントリと操作の両方を表示）
/knowledge show
```

**注意点**:
- ⚠️ ベータ機能（デフォルトで無効）
- ⚠️ BM25サポート（v1.17.0以降）
- ⚠️ インデックスデータは `.amazonq/` に保存

**関連コマンド**: `/experiment`, `/context`, `/subscribe`

**詳細**: [コンテキスト管理ガイド - Knowledge Bases](../08_guides/03_effects.md#34-knowledge-basesの特徴) - Knowledge Basesの特徴、使い方、ベストプラクティスを解説

---

#### `/subscribe` - 購読管理

**目的**: 情報の購読を管理する

**使用シーン**: 新機能のお知らせを受け取る / 重要な更新を見逃さない

**使用方法**: `/subscribe [オプション]`

---

### 開発者向け

#### `/logdump` - ログ収集（v1.18.0+）

**目的**: サポート調査のためにログファイルを収集し、ZIPアーカイブとして出力する

**説明**: トラブルシューティング時に必要なログファイルを自動的に収集し、タイムスタンプ付きのZIPファイルとして保存します。

**使用シーン**: 問題発生時にログを収集してサポートチームに提出する / デバッグ情報を効率的に収集する

**使用方法**: `/logdump`

**出力形式**: `q-logs-YYYY-MM-DDTHH-MM-SSZ.zip`

**使用例**:
```
> /logdump

Collecting logs...
✓ Successfully created q-logs-2025-10-14T07-11-01Z.zip with 5 log files
```

**注意点**:
- ⚠️ ログファイルには機密情報が含まれる可能性があります
- ⚠️ 提出前に内容を確認してください

**関連コマンド**: `/help`, `/version`

---

#### `/tools` - ツール一覧

**目的**: 現在のAgentで利用可能なツールの一覧を表示する

**使用シーン**: 利用可能なツールを確認する / MCPツールが正しく読み込まれているか確認する

**使用方法**: `/tools`

**関連コマンド**: `/mcp`, `/agent`, `/hooks`

---

#### `/mcp` - MCP管理

**目的**: Model Context Protocol (MCP) サーバーを管理する

**使用シーン**: MCPサーバーの状態を確認する / どのMCPサーバーが利用可能か確認する

**使用方法**: `/mcp`

**関連コマンド**: `/tools`, `/agent`

---

#### `/hooks` - Hooks管理

**目的**: カスタムコマンドをAgent実行時やツール実行時に自動実行する

**説明**: 特定のイベント（Agent起動、ツール実行前後など）で自動的にコマンドを実行できます。

**使用シーン**: ツール実行前にセキュリティチェックを実行したい / コマンド実行をログに記録したい / 会話ターン終了時に後処理を実行したい

**Hook種類**:
- **AgentSpawn** - Agent起動時
- **UserPromptSubmit** - ユーザープロンプト送信時
- **PreToolUse** - ツール実行前
- **PostToolUse** - ツール実行後
- **Stop** - Assistantの応答完了時（v1.18.0+）

**Stop Hook（v1.18.0+）**:
- 各会話ターンの終了時に自動実行
- コンパイル、テスト、フォーマット、クリーンアップなどの後処理に最適
- デフォルトタイムアウト: 30秒（設定可能）
- 終了コード0で成功、その他はSTDERRを警告として表示

**使用方法**: `/hooks`

**注意点**: Hooksはagent設定ファイルで定義

**関連コマンド**: `/tools`, `/agent`

**詳細**: リポジトリの `docs/hooks.md` を参照

---

#### `/editor` - エディタ設定

**目的**: 外部エディタの設定を管理する

**使用シーン**: 好みのエディタを設定する / 長いプロンプトを作成したい

**使用方法**: `/editor [エディタコマンド]`

**使用例**:
```bash
/editor              # 現在のエディタ設定を表示
/editor code         # VS Codeを設定
/editor "code --wait"
```

---

#### `/reply` - 応答設定

**目的**: AIの応答スタイルを設定する

**使用シーン**: 簡潔な応答が欲しい時 / 詳細な説明が欲しい時

**使用方法**: `/reply [オプション]`

---

### 情報表示

#### `/usage` - 使用状況表示

**目的**: Q CLIの使用状況を表示する

**使用シーン**: トークン使用量を確認する / コストを把握する / コンテキストウィンドウの使用率を確認する

**使用方法**: `/usage`

**表示内容**:
- コンテキストトークン数
- アシスタントトークン数
- ツールトークン数
- ユーザートークン数
- 合計使用率（%）

**使用率の計算式**:
```
使用率 = (合計トークン数 / コンテキストウィンドウサイズ) × 100
```

**推奨アクション**:
- 使用率が70%を超えたら: `/compact`の実行を検討
- 使用率が90%を超えたら: `/compact`の実行を推奨
- 使用率が100%に近づくと: 自動要約が実行される

**関連コマンド**: `/context`, `/model`, `/compact`

---

#### `/changelog` - 変更履歴表示

**目的**: Q CLIの変更履歴を表示する

**使用シーン**: 最新の変更を確認する / 新機能を発見する

**使用方法**: `/changelog`

**関連コマンド**: `/whatsnew`, `/issue`

---

#### `/whatsnew` - 新機能表示

**目的**: 最新バージョンの新機能を表示する

**使用シーン**: アップデート後に新機能を確認する / 実験的機能を発見する

**使用方法**: `/whatsnew`

**関連コマンド**: `/changelog`, `/experiment`, `/help`

---

#### `/compact` - 会話履歴の要約

**目的**: 会話履歴を要約してコンテキストスペースを解放する

**使用シーン**: 
- トークン使用量が高い時（70%以上）
- 長時間の会話でメモリ制約に達した時
- 新しいトピックを始める前
- 複雑なツール操作の後

**使用方法**: 
```
/compact [オプション]
```

**オプション**:
- `--messages-to-exclude <N>`: 最新のN個のメッセージペアを要約から除外（デフォルト: 0）
- `--truncate-large-messages <true|false>`: 大きなメッセージを切り詰める（デフォルト: false）
- `--max-message-length <N>`: メッセージの最大長（デフォルト: 400,000文字）
- `--show-summary`: 要約内容を表示

**使用例**:
```bash
# 基本的な要約
/compact

# 最新の2個のメッセージペアを除外
/compact --messages-to-exclude 2

# 大きなメッセージを切り詰める
/compact --truncate-large-messages true --max-message-length 100000

# 要約を表示
/compact --show-summary
```

**動作**: 
- AI生成の要約を作成
- 重要な情報、コード、ツール実行結果を保持
- 会話履歴をクリアしてスペースを解放
- 以降の応答では要約を参照

**自動実行**: コンテキストウィンドウがオーバーフローすると自動実行される  
**無効化**: `q settings set chat.disableAutoCompaction true`

**関連コマンド**: `/context`, `/usage`

**詳細**: [コンテキスト管理ガイド - パフォーマンス最適化](../08_guides/04_best-practices.md#451-トークン使用量の監視方法)

---

### 問題報告

#### `/issue` - Issue報告

**目的**: Q CLIの問題やフィードバックを報告する

**使用シーン**: バグを報告する / 機能リクエストを送る / フィードバックを提供する

**使用方法**: `/issue`

**自動的に含まれる情報**: Q CLIのバージョン / OS情報 / 実行環境 / エラーログ

**注意点**: 報告内容に機密情報が含まれないよう注意

**関連コマンド**: `/changelog`, `/whatsnew`

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

最終更新: 2025-10-12
