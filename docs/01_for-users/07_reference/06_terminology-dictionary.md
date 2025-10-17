# 完全版用語辞書

**バージョン**: 2.1.0  
**最終更新**: 2025-10-18  
**総用語数**: 322用語

---

## 📋 このドキュメントについて

このドキュメントは、Amazon Q Developer CLI公式リポジトリから抽出した**全322用語**の完全版用語辞書です。

### 簡潔版との違い

- **[簡潔版用語集（glossary.md）](01_glossary.md)**: 主要な33用語の簡潔な説明
- **完全版用語辞書（本ドキュメント）**: 公式リポジトリから抽出した全用語を網羅

### 用語の分類


- **コア概念**: 54用語
- **機能**: 19用語
- **コマンド**: 9用語
- **技術用語**: 224用語
- **UI要素**: 9用語
- **実験的機能**: 7用語

---

## 📖 用語一覧


### コア概念

#### 1. Command-Line Specified Agent (1. Command-Line Specified Agent)

**注記**: 見出しは英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### 2. User-Defined Default Agent (2. User-Defined Default Agent)

**注記**: 見出しは英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### 3. Built-in Default Agent (3. Built-in Default Agent)

**注記**: 見出しは英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### `/knowledge add --name <name> --path <path> [--include pattern] [--exclude pattern] [--index-type Fast|Best]` (`/knowledge add --name <name> --path <path> [--include pattern] [--exclude pattern] [--index-type Fast|Best]`)

コア概念

**注記**: 英語のまま使用

#### `/knowledge cancel [operation_id]` (`/knowledge cancel [operation_id]`)

コア概念

**注記**: 英語のまま使用

#### `/knowledge clear` (`/knowledge clear`)

コア概念

**注記**: 英語のまま使用

#### `/knowledge remove <identifier>` (`/knowledge remove <identifier>`)

コア概念

**注記**: 英語のまま使用

#### `/knowledge show` (`/knowledge show`)

コア概念

**注記**: 英語のまま使用

#### `/knowledge update <path>` (`/knowledge update <path>`)

コア概念

**注記**: 英語のまま使用

#### Agent File Locations (Agentファイルの場所 / えーじぇんとふぁいるのばしょ)

Agent設定ファイルが保存される場所

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Agent Format (Agent形式 / えーじぇんとけいしき)

Agent設定ファイルの構造と書式

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Agent Not Found (Agentが見つかりません / えーじぇんとがみつかりません)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Agent Precedence (Agent優先順位 / えーじぇんとゆうせんじゅんい)

複数のAgentがある場合の優先順序

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Agent Selection Priority (Agent選択優先順位 / えーじぇんとせんたくゆうせんじゅんい)

複数のAgentがある場合の選択順序

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Agent Switching (Agent切り替え / えーじぇんときりかえ)

使用するAgentを変更すること

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Agent-Specific Knowledge Bases (Agent固有のKnowledge Base / えーじぇんとこゆうのなれっじべーす)

各Agentごとに独立したKnowledge Base

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### AgentSpawn (AgentSpawn / えーじぇんとすぽーん)

Agent起動時のフック

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### agentSpawn (agentSpawn)

Agent起動フックの設定キー

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Built-in Default Agent Details (ビルトインデフォルトAgentの詳細 / びるといんでふぉるとえーじぇんとのしょうさい)

ビルトインデフォルトAgentの設定内容

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Checkpointing (チェックポイント機能 / ちぇっくぽいんときのう)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Context Files (コンテキストファイル / こんてきすとふぁいる)

会話に追加されたファイル

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Context Usage Percentage (コンテキスト使用率 / こんてきすとしようりつ)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Creating a New Workspace Agent (新しいワークスペースAgentの作成)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Default Agent Behavior (デフォルトAgentの動作 / でふぉるとえーじぇんとのどうさ)

デフォルトAgentがどのように動作するか

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### EnabledCheckpointing (EnabledCheckpointing)

Checkpointing機能の有効化設定

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### EnabledContextUsagePercentage (EnabledContextUsagePercentage)

コンテキスト使用率表示の有効化設定

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### EnabledKnowledge (EnabledKnowledge)

Knowledge機能の有効化設定

#### Global Agents (User-Wide) (グローバルAgent（ユーザー全体） / ぐろーばるえーじぇんと（ゆーざーぜんたい）)

すべてのワークスペースで使用できるAgent

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Global Context (グローバルコンテキスト / ぐろーばるこんてきすと)

すべてのセッションで共有されるコンテキスト

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### How Agent Isolation Works (Agent分離の仕組み / えーじぇんとぶんりのしくみ)

Agentが互いに独立して動作する仕組み

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Isolated Knowledge Storage (分離されたKnowledgeストレージ / ぶんりされたなれっじすとれーじ)

Agentごとに独立したKnowledge保存領域

#### Knowledge (ナレッジ / なれっじ)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Knowledge Management (Knowledge管理 / なれっじかんり)

#### Legacy MCP Support (レガシーMCPサポート / れがしーえむしーぴーさぽーと)

旧形式のMCP設定への対応

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Local Agents (Workspace-Specific) (ローカルAgent（ワークスペース固有） / ろーかるえーじぇんと（わーくすぺーすこゆう）)

特定のワークスペースでのみ使用されるAgent

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### MCP Example (MCP例 / えむしーぴーれい)

MCPの使用例

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### MCP Servers (MCPサーバー / えむしーぴーさーばー)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### MCP Tool Patterns (MCPツールパターン / えむしーぴーつーるぱたーん)

MCPツールを指定するためのパターン記法

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### mcpServers (mcpServers)

MCP設定のmcpServersフィールド

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### McpServers Field (mcpServersフィールド / えむしーぴーさーばーずふぃーるど)

Agent設定でMCPサーバーを定義するフィールド

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Migrating Profiles to Agents (ProfileからAgentへの移行 / ぷろふぁいるからえーじぇんとへのいこう)

旧Profile形式からAgent形式への変換

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Only sees the original project-docs, not agent-specific-docs (元のproject-docsのみが表示され、Agent固有のドキュメントは表示されません)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Override for Specific Sessions (特定セッションでの上書き / とくていせっしょんでのうわがき)

#### Set a User Default Agent (ユーザーデフォルトAgentの設定 / ゆーざーでふぉるとえーじぇんとのせってい)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Set up a preferred default agent (優先デフォルトAgentの設定)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Switch to custom agent (カスタムAgentに切り替え)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### This creates a separate knowledge base for my-custom-agent (これによりmy-custom-agent用の独立したKnowledge Baseが作成されます)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Use default agent (development-helper) (デフォルトAgent（development-helper）を使用)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Use Global Agents For: (グローバルAgentの用途:)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Use Local Agents For: (ローカルAgentの用途:)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### useLegacyMcpJson (useLegacyMcpJson)

レガシーMCP形式使用の設定キー

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### UseLegacyMcpJson Field (useLegacyMcpJsonフィールド / ゆーずれがしーえむしーぴーじぇいそんふぃーるど)

レガシーMCP設定形式を使用するかを指定するフィールド

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Using Tool Settings in Agent Configuration (Agent設定でのツール設定の使用)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Working with default agent (デフォルトAgentでの作業)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

---

### 機能

#### Auto-enter tangent mode for Q CLI help questions (Q CLIヘルプ質問で自動的にタンジェントモードに入る)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Auto-Tangent for Introspect (Introspect用自動タンジェント)

#### Auto-Tangent Mode (自動タンジェントモード / じどうたんじぇんともーど)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Delegate (デリゲート / でりげーと)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Enable auto-tangent for introspect questions (Introspect質問で自動タンジェントを有効化)

#### EnabledThinking (EnabledThinking)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Enabling Tangent Mode (Tangent Modeの有効化 / たんじぇんともーどのゆうこうか)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Enter Tangent Mode (Tangent Modeに入る / たんじぇんともーどにはいる)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Exit Tangent Mode (Tangent Modeを終了 / たんじぇんともーどをしゅうりょう)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Exit Tangent Mode with Tail (Tangent Modeを保持して終了)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### In Tangent Mode (Tangent Mode中 / たんじぇんともーどちゅう)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Lost in Tangent Mode (Lost in Tangent Mode)

機能

**注記**: 英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### model (model)

機能

**注記**: 英語のまま使用

#### Model Field (modelフィールド / もでるふぃーるど)

#### Tangent Mode (タンジェントモード / たんじぇんともーど)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Tangent Mode Not Working (Tangent Mode Not Working)

機能

**注記**: 英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Thinking (シンキング / しんきんぐ)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### TODO Management (TODO管理 / とぅーどぅーかんり)

#### When to Use Tangent Mode (Tangent Modeを使用するタイミング)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

---

### コマンド

#### /clear-finished (/clear-finished)

**注記**: コマンドは英語のまま使用

#### /experiment (/experiment)

**注記**: コマンドは英語のまま使用

#### /issue (/issue)

**注記**: コマンドは英語のまま使用

#### /knowledge (/knowledge)

**注記**: コマンドは英語のまま使用

#### /load (/load)

**注記**: コマンドは英語のまま使用

#### /model (/model)

**注記**: コマンドは英語のまま使用

#### /save (/save)

**注記**: コマンドは英語のまま使用

#### /tangent (/tangent)

**注記**: コマンドは英語のまま使用

#### /todos (/todos)

**注記**: コマンドは英語のまま使用

---

### 技術用語

#### $schema ($schema)

技術用語

**注記**: 英語のまま使用

#### 1. Clone repo (1. Clone repo)

**注記**: 見出しは英語のまま使用

#### 2. Install the Rust toolchain using [Rustup](https://rustup.rs): (2. Install the Rust toolchain using [Rustup](https://rustup.rs):)

**注記**: 見出しは英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### 3. Develop locally (3. Develop locally)

**注記**: 見出しは英語のまま使用

#### `/clear-finished` (`/clear-finished`)

技術用語

**注記**: 英語のまま使用

#### `/todos delete [--all]` (`/todos delete [--all]`)

技術用語

**注記**: 英語のまま使用

#### `/todos resume` (`/todos resume`)

技術用語

**注記**: 英語のまま使用

#### `/todos view` (`/todos view`)

技術用語

**注記**: 英語のまま使用

#### `todo_list` vs. `/todos` (`todo_list`と`/todos`の違い)

#### AddContextRequest (AddContextRequest)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### allowedTools (allowedTools)

技術用語

**注記**: 英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### AllowedTools Field (allowedToolsフィールド / あらうどつーるずふぃーるど)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Amazon Q CLI (Amazon Q CLI / あまぞんきゅーしーえるあい)

Amazon Q Developer CLIの略称

#### args (args)

技術用語

**注記**: 英語のまま使用

#### Asking Q to make a TODO list: (QにTODOリストを作成させる:)

#### AsyncSemanticSearchClient (AsyncSemanticSearchClient)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Available Tools (利用可能なツール / りようかのうなつーる)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### BackgroundWorker (BackgroundWorker)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Basic Usage (基本的な使い方 / きほんてきなつかいかた)

基礎的な使用方法

#### Behavior (動作 / どうさ)

#### BenchmarkResults (BenchmarkResults)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Best (最良 / さいりょう)

最も良い品質を示す（Knowledge indexのindex-type）

#### Best Practices (ベストプラクティス / べすとぷらくてぃす)

#### BM25Context (BM25Context)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### BM25DataPoint (BM25DataPoint)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### BM25Index (BM25Index)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Builder (Builder)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Built-in Tools (ビルトインツール / びるといんつーる)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Caching (キャッシング / きゃっしんぐ)

#### CandleTextEmbedder (CandleTextEmbedder)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Change shortcut key (default: t) (ショートカットキーの変更（デフォルト: t）)

#### ChatMessage (ChatMessage)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### ChatResponseStream (ChatResponseStream)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### ChatResponseStreamUnmarshaller (ChatResponseStreamUnmarshaller)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Check/reset shortcut key (Check/reset shortcut key)

技術用語または型名

**注記**: 英語のまま使用

#### CitationTarget (CitationTarget)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Client (Client)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### command (コマンド / こまんど)

実行する命令（小文字形式）

#### Commands (コマンド / こまんど)

実行可能な命令

#### Complete Example (Complete Example)

技術用語または型名

**注記**: 英語のまま使用

#### Config (Config)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Configuration (設定 / せってい)

#### Configuration Options (設定オプション / せっていおぷしょん)

設定可能な項目や選択肢

#### ContextCreator (ContextCreator)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### ContextManager (ContextManager)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### ContextTruncationScheme (ContextTruncationScheme)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Contributing (貢献 / こうけん)

#### Create a Custom Default (カスタムデフォルトの作成 / かすたむでふぉるとのさくせい)

#### Customizing Default Behavior (デフォルト動作のカスタマイズ / でふぉるとどうさのかすたまいず)

#### DataPoint (DataPoint)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Default (デフォルト / でふぉると)

初期設定、標準設定

#### Default Resources (デフォルトリソース / でふぉるとりそーす)

#### Defining Hooks (フックの定義 / ふっくのていぎ)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### description (description)

技術用語

**注記**: 英語のまま使用

#### Description Field (descriptionフィールド / でぃすくりぷしょんふぃーるど)

#### Directory Creation (ディレクトリ作成 / でぃれくとりさくせい)

#### disabled (disabled)

技術用語

**注記**: 英語のまま使用

#### Effective Searching (Effective Searching)

技術用語または型名

**注記**: 英語のまま使用

#### EmbeddingType (EmbeddingType)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### EnabledTodoList (EnabledTodoList)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### env (env)

技術用語

**注記**: 英語のまま使用

#### Error (エラー / えらー)

#### ErrorCodeClassifier (ErrorCodeClassifier)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### EventReceiver (EventReceiver)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Exact Matches (完全一致 / かんぜんいっち)

#### Example 1: Exploring Alternatives (Example 1: Exploring Alternatives)

技術用語または型名

**注記**: 英語のまま使用

#### Example 2: Getting Q CLI Help (Example 2: Getting Q CLI Help)

技術用語または型名

**注記**: 英語のまま使用

#### Example 3: Clarifying Requirements (Example 3: Clarifying Requirements)

技術用語または型名

**注記**: 英語のまま使用

#### Example 4: Keeping Useful Information (Example 4: Keeping Useful Information)

技術用語または型名

**注記**: 英語のまま使用

#### Example Usage (Example Usage)

技術用語または型名

**注記**: 英語のまま使用

#### Example Workflow (ワークフロー例 / わーくふろーれい)

#### ExampleErrorCodeClassifier (ExampleErrorCodeClassifier)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Examples (例 / れい)

#### Execute_bash Tool (Execute_bashツール)

Bashコマンド実行ツール

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### ExportResultArchive (ExportResultArchive)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### ExportResultArchiveError (ExportResultArchiveError)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Fast (高速 / こうそく)

処理速度が速いことを示す（Knowledge indexのindex-type）

#### File Type Support (File Type Support)

技術用語または型名

**注記**: 英語のまま使用

#### File URI Examples (ファイルURI例 / ふぁいるゆーあーるあいれい)

#### File URI Path Resolution (ファイルURIパス解決 / ふぁいるゆーあーるあいぱすかいけつ)

#### FileProcessor (FileProcessor)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Files Not Being Indexed (Files Not Being Indexed)

技術用語または型名

**注記**: 英語のまま使用

#### FileType (FileType)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Folder Structure (フォルダ構造 / ふぉるだこうぞう)

#### ForeverSleep (ForeverSleep)

永続的なスリープ状態を表すRust型

#### Fs_read Tool (Fs_readツール)

ファイル読み取りツール

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Fs_write Tool (Fs_writeツール)

ファイル書き込みツール

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Fuzzy Search Support (ファジー検索サポート / ふぁじーけんさくさぽーと)

#### GenerateAssistantResponse (GenerateAssistantResponse)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### GenerateAssistantResponseError (GenerateAssistantResponseError)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### GenerateTaskAssistPlan (GenerateTaskAssistPlan)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### GenerateTaskAssistPlanError (GenerateTaskAssistPlanError)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Getting Started (はじめに / はじめに)

#### Global (グローバル / ぐろーばる)

全体に適用される設定や範囲

#### headers (headers)

技術用語

**注記**: 英語のまま使用

#### Hook Event (フックイベント / ふっくいべんと)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Hook Output (フック出力 / ふっくしゅつりょく)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Hook Types (フックタイプ / ふっくたいぷ)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Hooks (フック / ふっく)

特定のイベント発生時に実行される処理

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### hooks (hooks)

技術用語

**注記**: 英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Hooks Field (Hooks Field)

技術用語または型名

**注記**: 英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### HostedModelClient (HostedModelClient)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### How It Works (仕組み / しくみ)

動作原理や内部構造の説明

#### If development-helper doesn't exist, falls back to built-in default (If development-helper doesn't exist, falls back to built-in default)

技術用語または型名

**注記**: 英語のまま使用

#### Important Limitations (重要な制限事項 / じゅうようなせいげんじこう)

#### Important Notes (重要な注意事項 / じゅうようなちゅういじこう)

#### Indexing Process (Indexing Process)

技術用語または型名

**注記**: 英語のまま使用

#### IndexingJob (IndexingJob)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### IndexingParams (IndexingParams)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Installation (インストール / いんすとーる)

#### Interactive Selection (対話的選択 / たいわてきせんたく)

#### InternalServerExceptionReason (InternalServerExceptionReason)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Introspect Tool (Introspectツール / いんとろすぺくとつーる)

Q CLI自身の情報を提供するツール

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Keyboard Shortcut (キーボードショートカット / きーぼーどしょーとかっと)

#### Keyboard Shortcut Not Working (Keyboard Shortcut Not Working)

技術用語または型名

**注記**: 英語のまま使用

#### KnowledgeContext (KnowledgeContext)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Licensing (ライセンス / らいせんす)

#### Limitations (制限事項 / せいげんじこう)

機能の制約や限界

#### Lists Not Loading (リストが読み込まれません)

#### Managing Large Projects (Managing Large Projects)

技術用語または型名

**注記**: 英語のまま使用

#### Managing Lists (リストの管理 / りすとのかんり)

#### Metric (Metric)

メトリクス測定用のRust型

#### MockTextEmbedder (MockTextEmbedder)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### ModelConfig (ModelConfig)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### ModelDownloader (ModelDownloader)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### ModelType (ModelType)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### ModelValidator (ModelValidator)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### name (name)

技術用語

**注記**: 英語のまま使用

#### Name Field (nameフィールド / ねーむふぃーるど)

#### Naming Conflicts (名前の競合 / なまえのきょうごう)

#### Native Tool Patterns (ネイティブツールパターン / ねいてぃぶつーるぱたーん)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### No Lists Available (利用可能なリストがありません)

#### oauth (oauth)

技術用語

**注記**: 英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### oauthScopes (oauthScopes)

技術用語

**注記**: 英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### OnnxModelType (OnnxModelType)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### OperationHandle (OperationHandle)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### OperationManager (OperationManager)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### OperationStatus (OperationStatus)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### OperationType (OperationType)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Or enable via settings (Or enable via settings)

技術用語または型名

**注記**: 英語のまま使用

#### Override for specific task (Override for specific task)

技術用語または型名

**注記**: 英語のまま使用

#### Params (Params)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Pattern Filtering Best Practices (Pattern Filtering Best Practices)

技術用語または型名

**注記**: 英語のまま使用

#### Pattern Issues (Pattern Issues)

技術用語または型名

**注記**: 英語のまま使用

#### Pattern Matching Rules (パターンマッチングルール / ぱたーんまっちんぐるーる)

#### PatternFilter (PatternFilter)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Performance Considerations (Performance Considerations)

技術用語または型名

**注記**: 英語のまま使用

#### Performance Issues (Performance Issues)

技術用語または型名

**注記**: 英語のまま使用

#### Persistence (Persistence)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### PostToolUse (PostToolUse / ぽすとつーるゆーず)

ツール使用後のフック

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Prerequisites (前提条件 / ぜんていじょうけん)

#### PreToolUse (PreToolUse / ぷれつーるゆーず)

ツール使用前のフック

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### ProgressInfo (ProgressInfo)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### ProgressStatus (ProgressStatus)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Project Layout (プロジェクト構成 / ぷろじぇくとこうせい)

#### redirectUri (redirectUri)

技術用語

**注記**: 英語のまま使用

#### Related Features (関連機能 / かんれんきのう)

関係する他の機能

#### Report_issue Tool (Report_issueツール)

問題報告ツール

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### resources (resources)

技術用語

**注記**: 英語のまま使用

#### Resources Field (resourcesフィールド / りそーせすふぃーるど)

#### ResultArchiveStreamUnmarshaller (ResultArchiveStreamUnmarshaller)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Resuming a TODO list (after selecting): (Resuming a TODO list (after selecting):)

技術用語または型名

**注記**: 英語のまま使用

#### Search Capabilities (Search Capabilities)

技術用語または型名

**注記**: 英語のまま使用

#### Search Not Finding Expected Results (Search Not Finding Expected Results)

技術用語または型名

**注記**: 英語のまま使用

#### SearchResult (SearchResult)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Security (セキュリティ / せきゅりてぃ)

#### Selecting a TODO list to view: (表示するTODOリストを選択:)

#### SemanticContext (SemanticContext)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### SemanticSearchClient (SemanticSearchClient)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### SemanticSearchConfig (SemanticSearchConfig)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### SemanticSearchError (SemanticSearchError)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### SendMessage (SendMessage)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### SendMessageError (SendMessageError)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Server (サーバー / さーばー)

サービスを提供するシステム

#### ServiceQuotaExceededExceptionReason (ServiceQuotaExceededExceptionReason)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Set your preferred default (Set your preferred default)

技術用語または型名

**注記**: 英語のまま使用

#### Settings Integration (設定統合 / せっていとうごう)

#### Stop (Stop)

停止時のフック

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Storage (ストレージ / すとれーじ)

#### Storage and Persistence (Storage and Persistence)

技術用語または型名

**注記**: 英語のまま使用

#### Summary (Summary)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Switch back to default (Switch back to default)

技術用語または型名

**注記**: 英語のまま使用

#### SystemStatus (SystemStatus)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### TextEmbedder (TextEmbedder)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### TFTextEmbedder (TFTextEmbedder)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### The preserved entry (question + answer about debugging techniques) is now part of main conversation (The preserved entry (question + answer about debugging techniques) is now part of main conversation)

技術用語または型名

**注記**: 英語のまま使用

#### This will override defaults with explicit patterns (This will override defaults with explicit patterns)

技術用語または型名

**注記**: 英語のまま使用

#### This will use the default patterns (This will use the default patterns)

技術用語または型名

**注記**: 英語のまま使用

#### This will use your default setting (This will use your default setting)

技術用語または型名

**注記**: 英語のまま使用

#### ThrottlingExceptionReason (ThrottlingExceptionReason)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Timeout (タイムアウト / たいむあうと)

#### timeout (timeout)

技術用語

**注記**: 英語のまま使用

#### Tips (Tips)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### TODO List Storage (TODOリストストレージ / とぅーどぅーりすとすとれーじ)

#### TODO Lists (TODOリスト / とぅーどぅーりすと)

#### Token (トークン / とーくん)

テキストの最小単位、コンテキストウィンドウの計測単位

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Tool Matching (ツールマッチング / つーるまっちんぐ)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Tool Permissions (ツール権限 / つーるけんげん)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### toolAliases (toolAliases)

技術用語

**注記**: 英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### ToolAliases Field (toolAliasesフィールド / つーるえいりあせすふぃーるど)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### tools (tools)

技術用語

**注記**: 英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Tools Field (toolsフィールド / つーるずふぃーるど)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### toolsSettings (toolsSettings)

技術用語

**注記**: 英語のまま使用

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### ToolsSettings Field (toolsSettingsフィールド / つーるずせってぃんぐずふぃーるど)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### TransformationDownloadArtifactType (TransformationDownloadArtifactType)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Troubleshooting (トラブルシューティング / とらぶるしゅーてぃんぐ)

#### Trusted Tools (信頼されたツール / しんらいされたつーる)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### type (type)

技術用語

**注記**: 英語のまま使用

#### Unhandled (Unhandled)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### UnknownVariantError (UnknownVariantError)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### UnknownVariantValue (UnknownVariantValue)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### UriModifierInterceptor (UriModifierInterceptor)

URI変更を傍受するRust型

#### url (url)

技術用語

**注記**: 英語のまま使用

#### Usage (使用方法 / しようほうほう)

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Usage Examples (使用例 / しようれい)

実際の使い方の例

#### Use_aws Tool (Use_awsツール)

AWS操作ツール

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### User (ユーザー / ゆーざー)

システムの利用者

#### User Default Not Found (ユーザーデフォルトが見つかりません / ゆーざーでふぉるとがみつかりません)

#### VectorIndex (VectorIndex)

Rust内部実装用の型

**注記**: Rust型名は英語のまま使用

#### Version (バージョン / ばーじょん)

ソフトウェアのリリース番号

#### What It Provides (提供される機能 / ていきょうされるきのう)

#### When NOT to Use (When NOT to Use)

技術用語または型名

**注記**: 英語のまま使用

#### Wildcard Patterns (ワイルドカードパターン / わいるどかーどぱたーん)

#### Workflow Integration (ワークフロー統合 / わーくふろーとうごう)

---

### UI要素

#### Error Messages (エラーメッセージ / えらーめっせーじ)

#### File URI Prompt (ファイルURIプロンプト / ふぁいるゆーあーるあいぷろんぷと)

#### Inline Prompt (インラインプロンプト / いんらいんぷろんぷと)

#### prompt (プロンプト / ぷろんぷと)

#### Prompt Field (promptフィールド / ぷろんぷとふぃーるど)

#### UserPromptSubmit (UserPromptSubmit / ゆーざーぷろんぷとさぶみっと)

ユーザープロンプト送信時のフック

#### userPromptSubmit (userPromptSubmit)

ユーザープロンプト送信イベント

#### Visual Indicators (視覚的インジケーター / しかくてきいんじけーたー)

#### with warning message (警告メッセージ付き / けいこくめっせーじつき)

---

### 実験的機能

#### Available Experiments (利用可能な実験的機能 / りようかのうなじっけんてききのう)

#### Enable via experiment (select from list) (/experimentコマンドで有効化（リストから選択）)

#### Experimental Features (実験的機能 / じっけんてききのう)

#### Knowledge Tool (experimental) (Knowledgeツール（実験的）)

Knowledge管理ツール

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### Managing Experiments (実験的機能の管理 / じっけんてききのうのかんり)

#### Thinking Tool (experimental) (Thinkingツール（実験的）)

思考過程表示ツール

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

#### TODO List Tool (experimental) (TODO Listツール（実験的）)

TODOリスト管理ツール

**簡潔版**: [glossary.md](01_glossary.md)に詳細な説明があります

---


## 📚 関連ドキュメント

- **[簡潔版用語集](01_glossary.md)** - 主要な33用語の詳細な説明
- **[コマンドリファレンス](02_commands.md)** - コマンドの詳細仕様
- **[設定リファレンス](03_settings-reference.md)** - 設定項目の詳細
- **[コンテキスト管理ガイド](../08_guides/README.md)** - コンテキストの詳細解説

---

## 🔄 更新履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| v2.1.0 | 2025-10-18 | サイト全体の用語チェックに基づき6用語追加（Server, Default, Version, Global, User, Token） |
| v2.0.0 | 2025-10-18 | Phase 3完了: 全278用語の翻訳完了（100%達成） |
| v1.0.0 | 2025-10-18 | 初版リリース: 公式リポジトリから316用語を抽出 |

---

*このドキュメントは公式リポジトリ（aws/amazon-q-developer-cli）から自動抽出された用語を基に作成されています。*

