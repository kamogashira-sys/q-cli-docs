[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [リファレンス](README.md) > 01 Glossary

---

# 用語集

最終更新: 2025-10-11

---

## 📋 このドキュメントについて

Amazon Q CLI関連の用語を定義し、ドキュメント全体で一貫した用語使用を促進します。

---

## 🎯 コア概念

### Agent（エージェント）
Amazon Q CLIの動作をカスタマイズする設定ファイル。システムプロンプト、利用可能なツール、MCPサーバー連携、リソースファイルなどを定義します。

**用語の使い分け**:
- **Agent**（大文字）: 機能名・概念として使用
  - 例: "Agent機能", "Agent設定ガイド"
- **agent**（小文字）: 具体的なインスタンスとして使用
  - 例: "my-agent", "`q agent list`"

**関連用語**: Agent設定ファイル, ローカルAgent, グローバルAgent

---

### MCP (Model Context Protocol)
AIモデルと外部ツール・データソースを接続するための標準プロトコル。Q CLIの機能拡張の基盤となります。

**用語の使い分け**:
- **MCP**（大文字）: プロトコル名・概念として使用
  - 例: "MCPサーバー", "MCP設定"
- **mcp**（小文字）: 設定キー・ファイル名として使用
  - 例: "`mcpServers`", "`mcp-config.json`"

**関連用語**: MCPサーバー, MCPクライアント, MCP仕様

---

### MCPサーバー
MCPプロトコルを実装したサーバープロセス。Q CLIに追加機能（ツール、リソース、プロンプト）を提供します。

**種類**:
- **stdioサーバー**: ローカルプロセスとして実行
- **HTTPサーバー**: リモートサーバーとして実行（v1.17.0+）

**例**: `@modelcontextprotocol/server-filesystem`, カスタムMCPサーバー

---

### Knowledge Base（ナレッジベース）
プロジェクトのドキュメントやコードをインデックス化し、セマンティック検索を可能にする機能（ベータ版）。

**主な機能**:
- ドキュメントのインデックス化
- セマンティック検索（BM25サポート、v1.17.0+）
- コンテキストへの自動追加

**コマンド**: `/knowledge add`, `/knowledge search`, `/knowledge show`

**詳細**: [コンテキスト管理ガイド - Knowledge Bases](../08_guides/03_effects.md#34-knowledge-basesの特徴)

---

### Checkpoint（チェックポイント）
会話の状態をGitコミットとして保存する機能。会話履歴を管理し、特定の時点に戻ることができます。

**要件**: Gitリポジトリ内で使用

**コマンド**: `/checkpoint save`, `/checkpoint list`, `/checkpoint restore`

---

### Context（コンテキスト）
AIが参照する情報の集合。以下を含みます：
- 会話履歴
- 参照ファイル（Agent Resources, Session Context）
- Knowledge Base
- MCPリソース
- システムプロンプト

**管理コマンド**: `/context show`, `/context add`, `/context rm`, `/compact`（圧縮）, `/clear`（クリア）

**詳細**: [コンテキスト管理ガイド](../08_guides/README.md)

---

### コンテキストウィンドウ（Context Window）
AIモデルが一度に処理できるトークン数の上限。Q CLIのデフォルトは200,000トークン。

**制限**:
- モデルによって異なる（Claude Sonnet 4: 200,000トークン、GPT: 128,000トークンなど）
- ユーザーが変更不可
- コンテキストファイルは75%まで使用可能

**確認方法**: `/usage`コマンドで使用率を確認

**詳細**: [コンテキスト管理ガイド](../08_guides/README.md)

---

### コンパクション（Compaction）
会話履歴を要約してコンテキストウィンドウの使用量を削減する機能。

**種類**:
- **自動コンパクション**: コンテキストウィンドウがオーバーフローした際に自動実行
- **手動コンパクション**: `/compact`コマンドで実行

**制御**:
- `chat.disableAutoCompaction`設定で自動実行を無効化可能（非推奨）

**オプション**:
- `--messages-to-exclude <N>`: 最新のN個のメッセージペアを除外
- `--truncate-large-messages <true|false>`: 大きなメッセージを切り詰める
- `--max-message-length <N>`: メッセージの最大長
- `--show-summary`: 要約内容を表示

**詳細**: [コンテキスト管理ガイド](../08_guides/README.md)

---

### コンテキストファイル（Context Files）
`/context add`コマンドで追加されたファイル。AIがこれらのファイルを参照して応答を生成する。

**制限**:
- 合計サイズはコンテキストウィンドウの75%まで
- 超過すると自動的にドロップされる
- `--force`フラグで強制追加可能（注意が必要）

**管理コマンド**:
- `/context show`: 状態確認
- `/context add <file>`: ファイル追加
- `/context add --force <file>`: 強制追加
- `/context remove <pattern>`: ファイル削除
- `/context clear`: すべてクリア

**詳細**: [コンテキスト管理ガイド](../08_guides/README.md)

---

### Tool（ツール）
Amazon Q CLIが実行できる機能単位。ファイル操作、コマンド実行、AWS操作などを提供します。

**種類**:
- **ビルトインツール**: Amazon Q CLI標準搭載（`fs_read`, `execute_bash`など）
- **MCPツール**: MCPサーバーが提供

**権限管理**: Agent設定の`tools`配列で制御

---

## 🎨 実験的機能

### Tangent Mode（タンジェントモード）
通常の会話から一時的に脱線して、別のトピックを探索するモード。メインの会話コンテキストを保持したまま、サイドトピックを調査できます。

**使用方法**: `/tangent`（開始/終了）

---

### Delegate（デリゲート）
バックグラウンドで独立して動作するエージェントプロセスを起動・管理する機能（v1.18.0+）。複数のエージェントを並行して管理し、それぞれに1つのタスクを委譲できます。

**操作方法**: 
- `launch`: タスクの起動
- `status`: ステータス確認
- `list`: 利用可能なエージェント一覧

**技術的詳細**:
- 状態保存: `~/.aws/amazonq/.subagents/`
- PIDベースのプロセス監視
- 1エージェントにつき1タスク

**有効化**: `/experiment` で「Delegate」を選択

---

### Subagent（サブエージェント）
Delegateによってバックグラウンドで起動されるエージェントプロセス。メインの会話セッションとは独立して動作します。

---

### Context Usage Indicator（コンテキスト使用率インジケーター）
現在のコンテキストウィンドウ使用率を視覚的に表示する機能。

**表示形式**: パーセンテージ（0-100%）

**推奨アクション**: 90%以上で`/compact`実行

---

### Thinking（シンキング）
AIの思考過程を可視化する機能。推論ステップを表示します。

**有効化**: `/experiment` → Thinking → ON

---

## 🔧 技術用語

### stdio (Standard Input/Output)
標準入出力を使った通信方式。ローカルプロセス（MCPサーバー）との通信に使用します。

**特徴**:
- プロセス間通信
- 低レイテンシ
- ローカル実行のみ

---

### HTTP/SSE (Server-Sent Events)
HTTPベースの通信方式。リモートMCPサーバーとの通信に使用します（v1.17.0+）。

**特徴**:
- ネットワーク経由
- リモート実行可能
- OAuth認証サポート

---

### OAuth (Open Authorization)
認証プロトコル。外部サービスとの安全な連携に使用します。

**用途**: リモートMCPサーバーの認証

**設定**: `oauthClientId`, `oauthClientSecret`, `oauthRedirectUri`

---

### SigV4 (AWS Signature Version 4)
AWS APIへの認証方式。AWS サービスとの通信に使用します。

**用途**: AWS APIコール、S3アクセスなど

---

### ADC (Application Default Credentials)
アプリケーションのデフォルト認証情報。エンタープライズ環境での認証に使用します（計画中、#2600）。

---

## 📁 ファイル・ディレクトリ

### Agent設定ファイル
Agentの定義を含むJSONファイル。

**配置場所**:
- ローカル: `<project>/.amazonq/cli-agents/<name>.json`
- グローバル: `~/.aws/amazonq/cli-agents/<name>.json`

**形式**: JSON（Agent schema v1.0準拠）

---

### Hook（フック）
特定のイベント発生時に自動的に実行されるカスタムコマンド。Agent設定ファイルで定義します。

**Hook種類**:
- **AgentSpawn**: Agent起動時
- **UserPromptSubmit**: ユーザープロンプト送信時
- **PreToolUse**: ツール実行前
- **PostToolUse**: ツール実行後
- **Stop**: Assistantの応答完了時（v1.18.0+）

**用途**: コンパイル、テスト、フォーマット、クリーンアップなどの自動化

**詳細**: リポジトリの `docs/hooks.md` を参照

---

### Stop Hook（ストップフック）
会話ターン終了時（Assistantの応答完了時）に実行されるフック（v1.18.0+）。

**特徴**:
- 各会話ターンの終了時に自動実行
- デフォルトタイムアウト: 30秒
- 終了コード0で成功、その他はSTDERRを警告として表示

**使用例**: コンパイル、テスト実行、コードフォーマット

---

### グローバル設定ファイル
Amazon Q CLI全体の設定を含むJSONファイル。

**配置場所**: `~/.local/share/amazon-q/settings.json`

**管理コマンド**: `q settings`

---

### ログファイル
Amazon Q CLIの実行ログ（chatサブコマンドでのみ出力）。

**配置場所**: 
- Linux: `/run/user/$(id -u)/qlog/qchat.log` または `/tmp/qlog/qchat.log`
- macOS: `$TMPDIR/qlog/qchat.log`
- Windows: `%TEMP%\amazon-q\logs\qchat.log`

**確認方法**: `q doctor`

**重要**: ログファイル出力は `q chat` サブコマンドでのみ有効

---

## ⚙️ 設定関連

### 設定優先順位
設定値の決定順序：
1. コマンドライン引数
2. 環境変数
3. Agent設定
4. グローバル設定
5. デフォルト値

---

### 環境変数展開
Agent設定やMCP設定で環境変数を参照する機能。

**構文**: `${env:VARIABLE_NAME}`

**例**: `"apiKey": "${env:API_KEY}"`

**サポート**: v1.17.0+（HTTPヘッダー）

---

## 🔐 セキュリティ

### ツール権限
ツールの実行を制御する仕組み。

**設定方法**:
- `tools`: 利用可能なツール一覧
- `allowedTools`: 自動承認するツール
- `deniedTools`: 禁止するツール

---

### fs_read制限
ファイル読み取りツールの制限（v1.14.0+）。

**制限内容**: 
- ホームディレクトリ外の読み取り制限
- 機密ファイルの保護

---

## 📊 メトリクス

### テレメトリ
Amazon Q CLIの使用状況データ。

**収集データ**: コマンド実行回数、エラー発生率など

**制御**: `telemetry.enabled`設定

---

### アクティビティダッシュボード
使用状況を可視化するダッシュボード。

**アクセス**: AWS コンソール

---

## 🔄 バージョン管理

### スキーマバージョン
Agent設定ファイルのスキーマバージョン。

**現在**: v1.0

**フィールド**: `version`

---

### マイグレーション
バージョン間の設定移行。

**例**: v1.15 → v1.16（MCP設定形式変更）

---

## 📇 索引

### A-Z

- [Agent](#agentエージェント) - Amazon Q CLIの動作をカスタマイズする設定ファイル
- [Agent設定ファイル](#agent設定ファイル) - Agentの定義を含むJSONファイル
- [allowedPaths](#allowedpaths) - ファイルアクセス権限の設定

### あ行

- [アクティビティダッシュボード](#アクティビティダッシュボード) - 使用状況を可視化するダッシュボード

### か行

- [環境変数](#環境変数) - Amazon Q CLIの動作を制御するシステム環境変数
- [グローバルAgent](#グローバルagent) - ユーザー全体で使用可能なAgent
- [グローバル設定](#グローバル設定) - ユーザー全体のデフォルト設定

### さ行

- [スキーマバージョン](#スキーマバージョン) - Agent設定ファイルのスキーマバージョン

### た行

- [テレメトリ](#テレメトリ) - Amazon Q CLIの使用状況データ
- [ツール](#ツール) - Amazon Q CLIが提供する機能

### は行

- [バージョン管理](#バージョン管理) - 設定ファイルのバージョン管理

### ま行

- [マイグレーション](#マイグレーション) - バージョン間の設定移行

### ら行

- [ローカルAgent](#ローカルagent) - プロジェクト固有のAgent

### M

- [MCP](#mcp-model-context-protocol) - Model Context Protocol
- [MCPサーバー](#mcpサーバー) - MCPプロトコルを実装したサーバー

### K

- [Knowledge](#knowledge) - ドキュメント検索機能

---

## 📚 関連ドキュメント

- **[完全版用語辞書](06_terminology-dictionary.md)** - 322用語の詳細な説明と使用例
  - 本ドキュメントは主要な33用語の簡潔な説明
  - 完全版は公式リポジトリから抽出した全用語を網羅
- **[Agent設定ガイド](../03_configuration/03_agent-configuration.md)**
- **[MCP設定ガイド](../03_configuration/04_mcp-configuration.md)**
- **[設定優先順位](../03_configuration/07_priority-rules.md)**
- **[実験的機能](../02_features/07_experimental.md)**

---

---

## 🔗 外部リンク

- [MCP仕様](https://modelcontextprotocol.io/)
- [Agent スキーマ](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json)
- [GitHub リポジトリ](https://github.com/aws/amazon-q-developer-cli)

---

**作成日**: 2025-10-11  
最終更新: 2025-10-11
