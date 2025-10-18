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


### コア概念（54用語）

| 英語 | 日本語 | 説明 | 注記 |
|------|--------|------|------|
| 1. Command-Line Specified Agent | 1. Command-Line Specified Agent | - | [詳細](01_glossary.md)<br/>見出しは英語のまま使用 |
| 2. User-Defined Default Agent | 2. User-Defined Default Agent | - | [詳細](01_glossary.md)<br/>見出しは英語のまま使用 |
| 3. Built-in Default Agent | 3. Built-in Default Agent | - | [詳細](01_glossary.md)<br/>見出しは英語のまま使用 |
| `/knowledge add --name <name> --path <path> [--include pattern] [--exclude pattern] [--index-type Fast\|Best]` | `/knowledge add --name <name> --path <path> [--include pattern] [--exclude pattern] [--index-type Fast\|Best]` | コア概念 | 英語のまま使用 |
| `/knowledge cancel [operation_id]` | `/knowledge cancel [operation_id]` | コア概念 | 英語のまま使用 |
| `/knowledge clear` | `/knowledge clear` | コア概念 | 英語のまま使用 |
| `/knowledge remove <identifier>` | `/knowledge remove <identifier>` | コア概念 | 英語のまま使用 |
| `/knowledge show` | `/knowledge show` | コア概念 | 英語のまま使用 |
| `/knowledge update <path>` | `/knowledge update <path>` | コア概念 | 英語のまま使用 |
| Agent File Locations | Agentファイルの場所 | Agent設定ファイルが保存される場所 | [詳細](01_glossary.md) |
| Agent Format | Agent形式 | Agent設定ファイルの構造と書式 | [詳細](01_glossary.md) |
| Agent Not Found | Agentが見つかりません | - | [詳細](01_glossary.md) |
| Agent Precedence | Agent優先順位 | 複数のAgentがある場合の優先順序 | [詳細](01_glossary.md) |
| Agent Selection Priority | Agent選択優先順位 | 複数のAgentがある場合の選択順序 | [詳細](01_glossary.md) |
| Agent Switching | Agent切り替え | 使用するAgentを変更すること | [詳細](01_glossary.md) |
| Agent-Specific Knowledge Bases | Agent固有のKnowledge Base | 各Agentごとに独立したKnowledge Base | [詳細](01_glossary.md) |
| AgentSpawn | AgentSpawn | Agent起動時のフック | [詳細](01_glossary.md) |
| agentSpawn | agentSpawn | Agent起動フックの設定キー | [詳細](01_glossary.md) |
| Built-in Default Agent Details | ビルトインデフォルトAgentの詳細 | ビルトインデフォルトAgentの設定内容 | [詳細](01_glossary.md) |
| Checkpointing | チェックポイント機能 | - | [詳細](01_glossary.md) |
| Context Files | コンテキストファイル | 会話に追加されたファイル | [詳細](01_glossary.md) |
| Context Usage Percentage | コンテキスト使用率 | - | [詳細](01_glossary.md) |
| Creating a New Workspace Agent | 新しいワークスペースAgentの作成 | - | [詳細](01_glossary.md) |
| Default Agent Behavior | デフォルトAgentの動作 | デフォルトAgentがどのように動作するか | [詳細](01_glossary.md) |
| EnabledCheckpointing | EnabledCheckpointing | Checkpointing機能の有効化設定 | [詳細](01_glossary.md) |
| EnabledContextUsagePercentage | EnabledContextUsagePercentage | コンテキスト使用率表示の有効化設定 | [詳細](01_glossary.md) |
| EnabledKnowledge | EnabledKnowledge | Knowledge機能の有効化設定 | - |
| Global Agents (User-Wide) | グローバルAgent（ユーザー全体） | すべてのワークスペースで使用できるAgent | [詳細](01_glossary.md) |
| Global Context | グローバルコンテキスト | すべてのセッションで共有されるコンテキスト | [詳細](01_glossary.md) |
| How Agent Isolation Works | Agent分離の仕組み | Agentが互いに独立して動作する仕組み | [詳細](01_glossary.md) |
| Isolated Knowledge Storage | 分離されたKnowledgeストレージ | Agentごとに独立したKnowledge保存領域 | - |
| Knowledge | ナレッジ | - | [詳細](01_glossary.md) |
| Knowledge Management | Knowledge管理 | - | - |
| Legacy MCP Support | レガシーMCPサポート | 旧形式のMCP設定への対応 | [詳細](01_glossary.md) |
| Local Agents (Workspace-Specific) | ローカルAgent（ワークスペース固有） | 特定のワークスペースでのみ使用されるAgent | [詳細](01_glossary.md) |
| MCP Example | MCP例 | MCPの使用例 | [詳細](01_glossary.md) |
| MCP Servers | MCPサーバー | - | [詳細](01_glossary.md) |
| MCP Tool Patterns | MCPツールパターン | MCPツールを指定するためのパターン記法 | [詳細](01_glossary.md) |
| mcpServers | mcpServers | MCP設定のmcpServersフィールド | [詳細](01_glossary.md) |
| McpServers Field | mcpServersフィールド | Agent設定でMCPサーバーを定義するフィールド | [詳細](01_glossary.md) |
| Migrating Profiles to Agents | ProfileからAgentへの移行 | 旧Profile形式からAgent形式への変換 | [詳細](01_glossary.md) |
| Only sees the original project-docs, not agent-specific-docs | 元のproject-docsのみが表示され、Agent固有のドキュメントは表示されません | - | [詳細](01_glossary.md) |
| Override for Specific Sessions | 特定セッションでの上書き | - | - |
| Set a User Default Agent | ユーザーデフォルトAgentの設定 | - | [詳細](01_glossary.md) |
| Set up a preferred default agent | 優先デフォルトAgentの設定 | - | [詳細](01_glossary.md) |
| Switch to custom agent | カスタムAgentに切り替え | - | [詳細](01_glossary.md) |
| This creates a separate knowledge base for my-custom-agent | これによりmy-custom-agent用の独立したKnowledge Baseが作成されます | - | [詳細](01_glossary.md) |
| Use default agent (development-helper) | デフォルトAgent（development-helper）を使用 | - | [詳細](01_glossary.md) |
| Use Global Agents For: | グローバルAgentの用途: | - | [詳細](01_glossary.md) |
| Use Local Agents For: | ローカルAgentの用途: | - | [詳細](01_glossary.md) |
| useLegacyMcpJson | useLegacyMcpJson | レガシーMCP形式使用の設定キー | [詳細](01_glossary.md) |
| UseLegacyMcpJson Field | useLegacyMcpJsonフィールド | レガシーMCP設定形式を使用するかを指定するフィールド | [詳細](01_glossary.md) |
| Using Tool Settings in Agent Configuration | Agent設定でのツール設定の使用 | - | [詳細](01_glossary.md) |
| Working with default agent | デフォルトAgentでの作業 | - | [詳細](01_glossary.md) |

---

### 機能（19用語）

| 英語 | 日本語 | 説明 | 注記 |
|------|--------|------|------|
| Auto-enter tangent mode for Q CLI help questions | Q CLIヘルプ質問で自動的にタンジェントモードに入る | - | [詳細](01_glossary.md) |
| Auto-Tangent for Introspect | Introspect用自動タンジェント | - | - |
| Auto-Tangent Mode | 自動タンジェントモード | - | [詳細](01_glossary.md) |
| Delegate | デリゲート | - | [詳細](01_glossary.md) |
| Enable auto-tangent for introspect questions | Introspect質問で自動タンジェントを有効化 | - | - |
| EnabledThinking | EnabledThinking | Rust内部実装用の型 | [詳細](01_glossary.md)<br/>Rust型名は英語のまま使用 |
| Enabling Tangent Mode | Tangent Modeの有効化 | - | [詳細](01_glossary.md) |
| Enter Tangent Mode | Tangent Modeに入る | - | [詳細](01_glossary.md) |
| Exit Tangent Mode | Tangent Modeを終了 | - | [詳細](01_glossary.md) |
| Exit Tangent Mode with Tail | Tangent Modeを保持して終了 | - | [詳細](01_glossary.md) |
| In Tangent Mode | Tangent Mode中 | - | [詳細](01_glossary.md) |
| Lost in Tangent Mode | Lost in Tangent Mode | 機能 | [詳細](01_glossary.md)<br/>英語のまま使用 |
| model | model | 機能 | 英語のまま使用 |
| Model Field | modelフィールド | - | - |
| Tangent Mode | タンジェントモード | - | [詳細](01_glossary.md) |
| Tangent Mode Not Working | Tangent Mode Not Working | 機能 | [詳細](01_glossary.md)<br/>英語のまま使用 |
| Thinking | シンキング | - | [詳細](01_glossary.md) |
| TODO Management | TODO管理 | - | - |
| When to Use Tangent Mode | Tangent Modeを使用するタイミング | - | [詳細](01_glossary.md) |

---

### コマンド（9用語）

| 英語 | 日本語 | 説明 | 注記 |
|------|--------|------|------|
| /clear-finished | /clear-finished | - | コマンドは英語のまま使用 |
| /experiment | /experiment | - | コマンドは英語のまま使用 |
| /issue | /issue | - | コマンドは英語のまま使用 |
| /knowledge | /knowledge | - | コマンドは英語のまま使用 |
| /load | /load | - | コマンドは英語のまま使用 |
| /model | /model | - | コマンドは英語のまま使用 |
| /save | /save | - | コマンドは英語のまま使用 |
| /tangent | /tangent | - | コマンドは英語のまま使用 |
| /todos | /todos | - | コマンドは英語のまま使用 |

---

### 技術用語（224用語）

| 英語 | 日本語 | 説明 | 注記 |
|------|--------|------|------|
| $schema | $schema | 技術用語 | 英語のまま使用 |
| 1. Clone repo | 1. Clone repo | - | 見出しは英語のまま使用 |
| 2. Install the Rust toolchain using [Rustup](https://rustup.rs): | 2. Install the Rust toolchain using [Rustup](https://rustup.rs): | - | [詳細](01_glossary.md)<br/>見出しは英語のまま使用 |
| 3. Develop locally | 3. Develop locally | - | 見出しは英語のまま使用 |
| `/clear-finished` | `/clear-finished` | 技術用語 | 英語のまま使用 |
| `/todos delete [--all]` | `/todos delete [--all]` | 技術用語 | 英語のまま使用 |
| `/todos resume` | `/todos resume` | 技術用語 | 英語のまま使用 |
| `/todos view` | `/todos view` | 技術用語 | 英語のまま使用 |
| `todo_list` vs. `/todos` | `todo_list`と`/todos`の違い | - | - |
| AddContextRequest | AddContextRequest | Rust内部実装用の型 | [詳細](01_glossary.md)<br/>Rust型名は英語のまま使用 |
| allowedTools | allowedTools | 技術用語 | [詳細](01_glossary.md)<br/>英語のまま使用 |
| AllowedTools Field | allowedToolsフィールド | - | [詳細](01_glossary.md) |
| Amazon Q CLI | Amazon Q CLI | Amazon Q Developer CLIの略称 | - |
| args | args | 技術用語 | 英語のまま使用 |
| Asking Q to make a TODO list: | QにTODOリストを作成させる: | - | - |
| AsyncSemanticSearchClient | AsyncSemanticSearchClient | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Available Tools | 利用可能なツール | - | [詳細](01_glossary.md) |
| BackgroundWorker | BackgroundWorker | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Basic Usage | 基本的な使い方 | 基礎的な使用方法 | - |
| Behavior | 動作 | - | - |
| BenchmarkResults | BenchmarkResults | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Best | 最良 | 最も良い品質を示す（Knowledge indexのindex-type） | - |
| Best Practices | ベストプラクティス | - | - |
| BM25Context | BM25Context | Rust内部実装用の型 | [詳細](01_glossary.md)<br/>Rust型名は英語のまま使用 |
| BM25DataPoint | BM25DataPoint | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| BM25Index | BM25Index | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Builder | Builder | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Built-in Tools | ビルトインツール | - | [詳細](01_glossary.md) |
| Caching | キャッシング | - | - |
| CandleTextEmbedder | CandleTextEmbedder | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Change shortcut key (default: t) | ショートカットキーの変更（デフォルト: t） | - | - |
| ChatMessage | ChatMessage | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| ChatResponseStream | ChatResponseStream | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| ChatResponseStreamUnmarshaller | ChatResponseStreamUnmarshaller | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Check/reset shortcut key | Check/reset shortcut key | 技術用語または型名 | 英語のまま使用 |
| CitationTarget | CitationTarget | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Client | Client | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| command | コマンド | 実行する命令（小文字形式） | - |
| Commands | コマンド | 実行可能な命令 | - |
| Complete Example | Complete Example | 技術用語または型名 | 英語のまま使用 |
| Config | Config | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Configuration | 設定 | - | - |
| Configuration Options | 設定オプション | 設定可能な項目や選択肢 | - |
| ContextCreator | ContextCreator | Rust内部実装用の型 | [詳細](01_glossary.md)<br/>Rust型名は英語のまま使用 |
| ContextManager | ContextManager | Rust内部実装用の型 | [詳細](01_glossary.md)<br/>Rust型名は英語のまま使用 |
| ContextTruncationScheme | ContextTruncationScheme | Rust内部実装用の型 | [詳細](01_glossary.md)<br/>Rust型名は英語のまま使用 |
| Contributing | 貢献 | - | - |
| Create a Custom Default | カスタムデフォルトの作成 | - | - |
| Customizing Default Behavior | デフォルト動作のカスタマイズ | - | - |
| DataPoint | DataPoint | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Default | デフォルト | 初期設定、標準設定 | - |
| Default Resources | デフォルトリソース | - | - |
| Defining Hooks | フックの定義 | - | [詳細](01_glossary.md) |
| description | description | 技術用語 | 英語のまま使用 |
| Description Field | descriptionフィールド | - | - |
| Directory Creation | ディレクトリ作成 | - | - |
| disabled | disabled | 技術用語 | 英語のまま使用 |
| Effective Searching | Effective Searching | 技術用語または型名 | 英語のまま使用 |
| EmbeddingType | EmbeddingType | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| EnabledTodoList | EnabledTodoList | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| env | env | 技術用語 | 英語のまま使用 |
| Error | エラー | - | - |
| ErrorCodeClassifier | ErrorCodeClassifier | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| EventReceiver | EventReceiver | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Exact Matches | 完全一致 | - | - |
| Example 1: Exploring Alternatives | Example 1: Exploring Alternatives | 技術用語または型名 | 英語のまま使用 |
| Example 2: Getting Q CLI Help | Example 2: Getting Q CLI Help | 技術用語または型名 | 英語のまま使用 |
| Example 3: Clarifying Requirements | Example 3: Clarifying Requirements | 技術用語または型名 | 英語のまま使用 |
| Example 4: Keeping Useful Information | Example 4: Keeping Useful Information | 技術用語または型名 | 英語のまま使用 |
| Example Usage | Example Usage | 技術用語または型名 | 英語のまま使用 |
| Example Workflow | ワークフロー例 | - | - |
| ExampleErrorCodeClassifier | ExampleErrorCodeClassifier | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Examples | 例 | - | - |
| Execute_bash Tool | Execute_bashツール | Bashコマンド実行ツール | [詳細](01_glossary.md) |
| ExportResultArchive | ExportResultArchive | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| ExportResultArchiveError | ExportResultArchiveError | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Fast | 高速 | 処理速度が速いことを示す（Knowledge indexのindex-type） | - |
| File Type Support | File Type Support | 技術用語または型名 | 英語のまま使用 |
| File URI Examples | ファイルURI例 | - | - |
| File URI Path Resolution | ファイルURIパス解決 | - | - |
| FileProcessor | FileProcessor | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Files Not Being Indexed | Files Not Being Indexed | 技術用語または型名 | 英語のまま使用 |
| FileType | FileType | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Folder Structure | フォルダ構造 | - | - |
| ForeverSleep | ForeverSleep | 永続的なスリープ状態を表すRust型 | - |
| Fs_read Tool | Fs_readツール | ファイル読み取りツール | [詳細](01_glossary.md) |
| Fs_write Tool | Fs_writeツール | ファイル書き込みツール | [詳細](01_glossary.md) |
| Fuzzy Search Support | ファジー検索サポート | - | - |
| GenerateAssistantResponse | GenerateAssistantResponse | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| GenerateAssistantResponseError | GenerateAssistantResponseError | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| GenerateTaskAssistPlan | GenerateTaskAssistPlan | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| GenerateTaskAssistPlanError | GenerateTaskAssistPlanError | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Getting Started | はじめに | - | - |
| Global | グローバル | 全体に適用される設定や範囲 | - |
| headers | headers | 技術用語 | 英語のまま使用 |
| Hook Event | フックイベント | - | [詳細](01_glossary.md) |
| Hook Output | フック出力 | - | [詳細](01_glossary.md) |
| Hook Types | フックタイプ | - | [詳細](01_glossary.md) |
| Hooks | フック | 特定のイベント発生時に実行される処理 | [詳細](01_glossary.md) |
| hooks | hooks | 技術用語 | [詳細](01_glossary.md)<br/>英語のまま使用 |
| Hooks Field | Hooks Field | 技術用語または型名 | [詳細](01_glossary.md)<br/>英語のまま使用 |
| HostedModelClient | HostedModelClient | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| How It Works | 仕組み | 動作原理や内部構造の説明 | - |
| If development-helper doesn't exist, falls back to built-in default | If development-helper doesn't exist, falls back to built-in default | 技術用語または型名 | 英語のまま使用 |
| Important Limitations | 重要な制限事項 | - | - |
| Important Notes | 重要な注意事項 | - | - |
| Indexing Process | Indexing Process | 技術用語または型名 | 英語のまま使用 |
| IndexingJob | IndexingJob | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| IndexingParams | IndexingParams | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Installation | インストール | - | - |
| Interactive Selection | 対話的選択 | - | - |
| InternalServerExceptionReason | InternalServerExceptionReason | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Introspect Tool | Introspectツール | Q CLI自身の情報を提供するツール | [詳細](01_glossary.md) |
| Keyboard Shortcut | キーボードショートカット | - | - |
| Keyboard Shortcut Not Working | Keyboard Shortcut Not Working | 技術用語または型名 | 英語のまま使用 |
| KnowledgeContext | KnowledgeContext | Rust内部実装用の型 | [詳細](01_glossary.md)<br/>Rust型名は英語のまま使用 |
| Licensing | ライセンス | - | - |
| Limitations | 制限事項 | 機能の制約や限界 | - |
| Lists Not Loading | リストが読み込まれません | - | - |
| Managing Large Projects | Managing Large Projects | 技術用語または型名 | 英語のまま使用 |
| Managing Lists | リストの管理 | - | - |
| Metric | Metric | メトリクス測定用のRust型 | - |
| MockTextEmbedder | MockTextEmbedder | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| ModelConfig | ModelConfig | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| ModelDownloader | ModelDownloader | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| ModelType | ModelType | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| ModelValidator | ModelValidator | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| name | name | 技術用語 | 英語のまま使用 |
| Name Field | nameフィールド | - | - |
| Naming Conflicts | 名前の競合 | - | - |
| Native Tool Patterns | ネイティブツールパターン | - | [詳細](01_glossary.md) |
| No Lists Available | 利用可能なリストがありません | - | - |
| oauth | oauth | 技術用語 | [詳細](01_glossary.md)<br/>英語のまま使用 |
| oauthScopes | oauthScopes | 技術用語 | [詳細](01_glossary.md)<br/>英語のまま使用 |
| OnnxModelType | OnnxModelType | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| OperationHandle | OperationHandle | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| OperationManager | OperationManager | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| OperationStatus | OperationStatus | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| OperationType | OperationType | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Or enable via settings | Or enable via settings | 技術用語または型名 | 英語のまま使用 |
| Override for specific task | Override for specific task | 技術用語または型名 | 英語のまま使用 |
| Params | Params | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Pattern Filtering Best Practices | Pattern Filtering Best Practices | 技術用語または型名 | 英語のまま使用 |
| Pattern Issues | Pattern Issues | 技術用語または型名 | 英語のまま使用 |
| Pattern Matching Rules | パターンマッチングルール | - | - |
| PatternFilter | PatternFilter | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Performance Considerations | Performance Considerations | 技術用語または型名 | 英語のまま使用 |
| Performance Issues | Performance Issues | 技術用語または型名 | 英語のまま使用 |
| Persistence | Persistence | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| PostToolUse | PostToolUse | ツール使用後のフック | [詳細](01_glossary.md) |
| Prerequisites | 前提条件 | - | - |
| PreToolUse | PreToolUse | ツール使用前のフック | [詳細](01_glossary.md) |
| ProgressInfo | ProgressInfo | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| ProgressStatus | ProgressStatus | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Project Layout | プロジェクト構成 | - | - |
| redirectUri | redirectUri | 技術用語 | 英語のまま使用 |
| Related Features | 関連機能 | 関係する他の機能 | - |
| Report_issue Tool | Report_issueツール | 問題報告ツール | [詳細](01_glossary.md) |
| resources | resources | 技術用語 | 英語のまま使用 |
| Resources Field | resourcesフィールド | - | - |
| ResultArchiveStreamUnmarshaller | ResultArchiveStreamUnmarshaller | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Resuming a TODO list (after selecting): | Resuming a TODO list (after selecting): | 技術用語または型名 | 英語のまま使用 |
| Search Capabilities | Search Capabilities | 技術用語または型名 | 英語のまま使用 |
| Search Not Finding Expected Results | Search Not Finding Expected Results | 技術用語または型名 | 英語のまま使用 |
| SearchResult | SearchResult | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Security | セキュリティ | - | - |
| Selecting a TODO list to view: | 表示するTODOリストを選択: | - | - |
| SemanticContext | SemanticContext | Rust内部実装用の型 | [詳細](01_glossary.md)<br/>Rust型名は英語のまま使用 |
| SemanticSearchClient | SemanticSearchClient | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| SemanticSearchConfig | SemanticSearchConfig | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| SemanticSearchError | SemanticSearchError | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| SendMessage | SendMessage | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| SendMessageError | SendMessageError | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Server | サーバー | サービスを提供するシステム | - |
| ServiceQuotaExceededExceptionReason | ServiceQuotaExceededExceptionReason | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Set your preferred default | Set your preferred default | 技術用語または型名 | 英語のまま使用 |
| Settings Integration | 設定統合 | - | - |
| Stop | Stop | 停止時のフック | [詳細](01_glossary.md) |
| Storage | ストレージ | - | - |
| Storage and Persistence | Storage and Persistence | 技術用語または型名 | 英語のまま使用 |
| Summary | Summary | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Switch back to default | Switch back to default | 技術用語または型名 | 英語のまま使用 |
| SystemStatus | SystemStatus | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| TextEmbedder | TextEmbedder | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| TFTextEmbedder | TFTextEmbedder | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| The preserved entry (question + answer about debugging techniques) is now part of main conversation | The preserved entry (question + answer about debugging techniques) is now part of main conversation | 技術用語または型名 | 英語のまま使用 |
| This will override defaults with explicit patterns | This will override defaults with explicit patterns | 技術用語または型名 | 英語のまま使用 |
| This will use the default patterns | This will use the default patterns | 技術用語または型名 | 英語のまま使用 |
| This will use your default setting | This will use your default setting | 技術用語または型名 | 英語のまま使用 |
| ThrottlingExceptionReason | ThrottlingExceptionReason | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Timeout | タイムアウト | - | - |
| timeout | timeout | 技術用語 | 英語のまま使用 |
| Tips | Tips | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| TODO List Storage | TODOリストストレージ | - | - |
| TODO Lists | TODOリスト | - | - |
| Token | トークン | テキストの最小単位、コンテキストウィンドウの計測単位 | [詳細](01_glossary.md) |
| Tool Matching | ツールマッチング | - | [詳細](01_glossary.md) |
| Tool Permissions | ツール権限 | - | [詳細](01_glossary.md) |
| toolAliases | toolAliases | 技術用語 | [詳細](01_glossary.md)<br/>英語のまま使用 |
| ToolAliases Field | toolAliasesフィールド | - | [詳細](01_glossary.md) |
| tools | tools | 技術用語 | [詳細](01_glossary.md)<br/>英語のまま使用 |
| Tools Field | toolsフィールド | - | [詳細](01_glossary.md) |
| toolsSettings | toolsSettings | 技術用語 | [詳細](01_glossary.md)<br/>英語のまま使用 |
| ToolsSettings Field | toolsSettingsフィールド | - | [詳細](01_glossary.md) |
| TransformationDownloadArtifactType | TransformationDownloadArtifactType | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Troubleshooting | トラブルシューティング | - | - |
| Trusted Tools | 信頼されたツール | - | [詳細](01_glossary.md) |
| type | type | 技術用語 | 英語のまま使用 |
| Unhandled | Unhandled | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| UnknownVariantError | UnknownVariantError | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| UnknownVariantValue | UnknownVariantValue | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| UriModifierInterceptor | UriModifierInterceptor | URI変更を傍受するRust型 | - |
| url | url | 技術用語 | 英語のまま使用 |
| Usage | 使用方法 | - | [詳細](01_glossary.md) |
| Usage Examples | 使用例 | 実際の使い方の例 | - |
| Use_aws Tool | Use_awsツール | AWS操作ツール | [詳細](01_glossary.md) |
| User | ユーザー | システムの利用者 | - |
| User Default Not Found | ユーザーデフォルトが見つかりません | - | - |
| VectorIndex | VectorIndex | Rust内部実装用の型 | Rust型名は英語のまま使用 |
| Version | バージョン | ソフトウェアのリリース番号 | - |
| What It Provides | 提供される機能 | - | - |
| When NOT to Use | When NOT to Use | 技術用語または型名 | 英語のまま使用 |
| Wildcard Patterns | ワイルドカードパターン | - | - |
| Workflow Integration | ワークフロー統合 | - | - |

---

### UI要素（9用語）

| 英語 | 日本語 | 説明 | 注記 |
|------|--------|------|------|
| Error Messages | エラーメッセージ | - | - |
| File URI Prompt | ファイルURIプロンプト | - | - |
| Inline Prompt | インラインプロンプト | - | - |
| prompt | プロンプト | - | - |
| Prompt Field | promptフィールド | - | - |
| UserPromptSubmit | UserPromptSubmit | ユーザープロンプト送信時のフック | - |
| userPromptSubmit | userPromptSubmit | ユーザープロンプト送信イベント | - |
| Visual Indicators | 視覚的インジケーター | - | - |
| with warning message | 警告メッセージ付き | - | - |

---

### 実験的機能（7用語）

| 英語 | 日本語 | 説明 | 注記 |
|------|--------|------|------|
| Available Experiments | 利用可能な実験的機能 | - | - |
| Enable via experiment (select from list) | /experimentコマンドで有効化（リストから選択） | - | - |
| Experimental Features | 実験的機能 | - | - |
| Knowledge Tool (experimental) | Knowledgeツール（実験的） | Knowledge管理ツール | [詳細](01_glossary.md) |
| Managing Experiments | 実験的機能の管理 | - | - |
| Thinking Tool (experimental) | Thinkingツール（実験的） | 思考過程表示ツール | [詳細](01_glossary.md) |
| TODO List Tool (experimental) | TODO Listツール（実験的） | TODOリスト管理ツール | [詳細](01_glossary.md) |

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
| v2.1.0 | 2025-10-18 | サイト全体の用語チェックに基づき6用語追加（Server, Default, Version, Global, User, Token）<br/>表形式に変更（可読性向上、75%の行数削減） |
| v2.0.0 | 2025-10-18 | Phase 3完了: 全278用語の翻訳完了（100%達成） |
| v1.0.0 | 2025-10-18 | 初版リリース: 公式リポジトリから316用語を抽出 |

---

*このドキュメントは公式リポジトリ（aws/amazon-q-developer-cli）から自動抽出された用語を基に作成されています。*

