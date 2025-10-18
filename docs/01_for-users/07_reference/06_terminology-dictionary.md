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

<table>
<colgroup>
<col style="width: 30%;">
<col style="width: 25%;">
<col style="width: 30%;">
<col style="width: 15%;">
</colgroup>
<thead>
<tr>
<th>英語</th>
<th>日本語</th>
<th>説明</th>
<th>注記</th>
</tr>
</thead>
<tbody>
<tr>
<td>1. Command-Line Specified Agent</td>
<td>1. Command-Line Specified Agent</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a><br/>見出しは英語のまま使用</td>
</tr>
<tr>
<td>2. User-Defined Default Agent</td>
<td>2. User-Defined Default Agent</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a><br/>見出しは英語のまま使用</td>
</tr>
<tr>
<td>3. Built-in Default Agent</td>
<td>3. Built-in Default Agent</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a><br/>見出しは英語のまま使用</td>
</tr>
<tr>
<td>`/knowledge add --name &lt;name&gt; --path &lt;path&gt; [--include pattern] [--exclude pattern] [--index-type Fast\|Best]`</td>
<td>`/knowledge add --name &lt;name&gt; --path &lt;path&gt; [--include pattern] [--exclude pattern] [--index-type Fast\|Best]`</td>
<td>コア概念</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>`/knowledge cancel [operation_id]`</td>
<td>`/knowledge cancel [operation_id]`</td>
<td>コア概念</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>`/knowledge clear`</td>
<td>`/knowledge clear`</td>
<td>コア概念</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>`/knowledge remove &lt;identifier&gt;`</td>
<td>`/knowledge remove &lt;identifier&gt;`</td>
<td>コア概念</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>`/knowledge show`</td>
<td>`/knowledge show`</td>
<td>コア概念</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>`/knowledge update &lt;path&gt;`</td>
<td>`/knowledge update &lt;path&gt;`</td>
<td>コア概念</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Agent File Locations</td>
<td>Agentファイルの場所</td>
<td>Agent設定ファイルが保存される場所</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Agent Format</td>
<td>Agent形式</td>
<td>Agent設定ファイルの構造と書式</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Agent Not Found</td>
<td>Agentが見つかりません</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Agent Precedence</td>
<td>Agent優先順位</td>
<td>複数のAgentがある場合の優先順序</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Agent Selection Priority</td>
<td>Agent選択優先順位</td>
<td>複数のAgentがある場合の選択順序</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Agent Switching</td>
<td>Agent切り替え</td>
<td>使用するAgentを変更すること</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Agent-Specific Knowledge Bases</td>
<td>Agent固有のKnowledge Base</td>
<td>各Agentごとに独立したKnowledge Base</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>AgentSpawn</td>
<td>AgentSpawn</td>
<td>Agent起動時のフック</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>agentSpawn</td>
<td>agentSpawn</td>
<td>Agent起動フックの設定キー</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Built-in Default Agent Details</td>
<td>ビルトインデフォルトAgentの詳細</td>
<td>ビルトインデフォルトAgentの設定内容</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Checkpointing</td>
<td>チェックポイント機能</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Context Files</td>
<td>コンテキストファイル</td>
<td>会話に追加されたファイル</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Context Usage Percentage</td>
<td>コンテキスト使用率</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Creating a New Workspace Agent</td>
<td>新しいワークスペースAgentの作成</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Default Agent Behavior</td>
<td>デフォルトAgentの動作</td>
<td>デフォルトAgentがどのように動作するか</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>EnabledCheckpointing</td>
<td>EnabledCheckpointing</td>
<td>Checkpointing機能の有効化設定</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>EnabledContextUsagePercentage</td>
<td>EnabledContextUsagePercentage</td>
<td>コンテキスト使用率表示の有効化設定</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>EnabledKnowledge</td>
<td>EnabledKnowledge</td>
<td>Knowledge機能の有効化設定</td>
<td>-</td>
</tr>
<tr>
<td>Global Agents (User-Wide)</td>
<td>グローバルAgent（ユーザー全体）</td>
<td>すべてのワークスペースで使用できるAgent</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Global Context</td>
<td>グローバルコンテキスト</td>
<td>すべてのセッションで共有されるコンテキスト</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>How Agent Isolation Works</td>
<td>Agent分離の仕組み</td>
<td>Agentが互いに独立して動作する仕組み</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Isolated Knowledge Storage</td>
<td>分離されたKnowledgeストレージ</td>
<td>Agentごとに独立したKnowledge保存領域</td>
<td>-</td>
</tr>
<tr>
<td>Knowledge</td>
<td>ナレッジ</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Knowledge Management</td>
<td>Knowledge管理</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Legacy MCP Support</td>
<td>レガシーMCPサポート</td>
<td>旧形式のMCP設定への対応</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Local Agents (Workspace-Specific)</td>
<td>ローカルAgent（ワークスペース固有）</td>
<td>特定のワークスペースでのみ使用されるAgent</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>MCP Example</td>
<td>MCP例</td>
<td>MCPの使用例</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>MCP Servers</td>
<td>MCPサーバー</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>MCP Tool Patterns</td>
<td>MCPツールパターン</td>
<td>MCPツールを指定するためのパターン記法</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>mcpServers</td>
<td>mcpServers</td>
<td>MCP設定のmcpServersフィールド</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>McpServers Field</td>
<td>mcpServersフィールド</td>
<td>Agent設定でMCPサーバーを定義するフィールド</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Migrating Profiles to Agents</td>
<td>ProfileからAgentへの移行</td>
<td>旧Profile形式からAgent形式への変換</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Only sees the original project-docs, not agent-specific-docs</td>
<td>元のproject-docsのみが表示され、Agent固有のドキュメントは表示されません</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Override for Specific Sessions</td>
<td>特定セッションでの上書き</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Set a User Default Agent</td>
<td>ユーザーデフォルトAgentの設定</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Set up a preferred default agent</td>
<td>優先デフォルトAgentの設定</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Switch to custom agent</td>
<td>カスタムAgentに切り替え</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>This creates a separate knowledge base for my-custom-agent</td>
<td>これによりmy-custom-agent用の独立したKnowledge Baseが作成されます</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Use default agent (development-helper)</td>
<td>デフォルトAgent（development-helper）を使用</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Use Global Agents For:</td>
<td>グローバルAgentの用途:</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Use Local Agents For:</td>
<td>ローカルAgentの用途:</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>useLegacyMcpJson</td>
<td>useLegacyMcpJson</td>
<td>レガシーMCP形式使用の設定キー</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>UseLegacyMcpJson Field</td>
<td>useLegacyMcpJsonフィールド</td>
<td>レガシーMCP設定形式を使用するかを指定するフィールド</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Using Tool Settings in Agent Configuration</td>
<td>Agent設定でのツール設定の使用</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Working with default agent</td>
<td>デフォルトAgentでの作業</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
</tbody>
</table>

---

### 機能（19用語）

<table>
<colgroup>
<col style="width: 30%;">
<col style="width: 25%;">
<col style="width: 30%;">
<col style="width: 15%;">
</colgroup>
<thead>
<tr>
<th>英語</th>
<th>日本語</th>
<th>説明</th>
<th>注記</th>
</tr>
</thead>
<tbody>
<tr>
<td>Auto-enter tangent mode for Q CLI help questions</td>
<td>Q CLIヘルプ質問で自動的にタンジェントモードに入る</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Auto-Tangent for Introspect</td>
<td>Introspect用自動タンジェント</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Auto-Tangent Mode</td>
<td>自動タンジェントモード</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Delegate</td>
<td>デリゲート</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Enable auto-tangent for introspect questions</td>
<td>Introspect質問で自動タンジェントを有効化</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>EnabledThinking</td>
<td>EnabledThinking</td>
<td>Rust内部実装用の型</td>
<td><a href="01_glossary.md">詳細</a><br/>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Enabling Tangent Mode</td>
<td>Tangent Modeの有効化</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Enter Tangent Mode</td>
<td>Tangent Modeに入る</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Exit Tangent Mode</td>
<td>Tangent Modeを終了</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Exit Tangent Mode with Tail</td>
<td>Tangent Modeを保持して終了</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>In Tangent Mode</td>
<td>Tangent Mode中</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Lost in Tangent Mode</td>
<td>Lost in Tangent Mode</td>
<td>機能</td>
<td><a href="01_glossary.md">詳細</a><br/>英語のまま使用</td>
</tr>
<tr>
<td>model</td>
<td>model</td>
<td>機能</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Model Field</td>
<td>modelフィールド</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Tangent Mode</td>
<td>タンジェントモード</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Tangent Mode Not Working</td>
<td>Tangent Mode Not Working</td>
<td>機能</td>
<td><a href="01_glossary.md">詳細</a><br/>英語のまま使用</td>
</tr>
<tr>
<td>Thinking</td>
<td>シンキング</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>TODO Management</td>
<td>TODO管理</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>When to Use Tangent Mode</td>
<td>Tangent Modeを使用するタイミング</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
</tbody>
</table>

---

### コマンド（9用語）

<table>
<colgroup>
<col style="width: 30%;">
<col style="width: 25%;">
<col style="width: 30%;">
<col style="width: 15%;">
</colgroup>
<thead>
<tr>
<th>英語</th>
<th>日本語</th>
<th>説明</th>
<th>注記</th>
</tr>
</thead>
<tbody>
<tr>
<td>/clear-finished</td>
<td>/clear-finished</td>
<td>-</td>
<td>コマンドは英語のまま使用</td>
</tr>
<tr>
<td>/experiment</td>
<td>/experiment</td>
<td>-</td>
<td>コマンドは英語のまま使用</td>
</tr>
<tr>
<td>/issue</td>
<td>/issue</td>
<td>-</td>
<td>コマンドは英語のまま使用</td>
</tr>
<tr>
<td>/knowledge</td>
<td>/knowledge</td>
<td>-</td>
<td>コマンドは英語のまま使用</td>
</tr>
<tr>
<td>/load</td>
<td>/load</td>
<td>-</td>
<td>コマンドは英語のまま使用</td>
</tr>
<tr>
<td>/model</td>
<td>/model</td>
<td>-</td>
<td>コマンドは英語のまま使用</td>
</tr>
<tr>
<td>/save</td>
<td>/save</td>
<td>-</td>
<td>コマンドは英語のまま使用</td>
</tr>
<tr>
<td>/tangent</td>
<td>/tangent</td>
<td>-</td>
<td>コマンドは英語のまま使用</td>
</tr>
<tr>
<td>/todos</td>
<td>/todos</td>
<td>-</td>
<td>コマンドは英語のまま使用</td>
</tr>
</tbody>
</table>

---

### 技術用語（224用語）

<table>
<colgroup>
<col style="width: 30%;">
<col style="width: 25%;">
<col style="width: 30%;">
<col style="width: 15%;">
</colgroup>
<thead>
<tr>
<th>英語</th>
<th>日本語</th>
<th>説明</th>
<th>注記</th>
</tr>
</thead>
<tbody>
<tr>
<td>$schema</td>
<td>$schema</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>1. Clone repo</td>
<td>1. Clone repo</td>
<td>-</td>
<td>見出しは英語のまま使用</td>
</tr>
<tr>
<td>2. Install the Rust toolchain using [Rustup](https://rustup.rs):</td>
<td>2. Install the Rust toolchain using [Rustup](https://rustup.rs):</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a><br/>見出しは英語のまま使用</td>
</tr>
<tr>
<td>3. Develop locally</td>
<td>3. Develop locally</td>
<td>-</td>
<td>見出しは英語のまま使用</td>
</tr>
<tr>
<td>`/clear-finished`</td>
<td>`/clear-finished`</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>`/todos delete [--all]`</td>
<td>`/todos delete [--all]`</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>`/todos resume`</td>
<td>`/todos resume`</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>`/todos view`</td>
<td>`/todos view`</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>`todo_list` vs. `/todos`</td>
<td>`todo_list`と`/todos`の違い</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>AddContextRequest</td>
<td>AddContextRequest</td>
<td>Rust内部実装用の型</td>
<td><a href="01_glossary.md">詳細</a><br/>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>allowedTools</td>
<td>allowedTools</td>
<td>技術用語</td>
<td><a href="01_glossary.md">詳細</a><br/>英語のまま使用</td>
</tr>
<tr>
<td>AllowedTools Field</td>
<td>allowedToolsフィールド</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Amazon Q CLI</td>
<td>Amazon Q CLI</td>
<td>Amazon Q Developer CLIの略称</td>
<td>-</td>
</tr>
<tr>
<td>args</td>
<td>args</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Asking Q to make a TODO list:</td>
<td>QにTODOリストを作成させる:</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>AsyncSemanticSearchClient</td>
<td>AsyncSemanticSearchClient</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Available Tools</td>
<td>利用可能なツール</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>BackgroundWorker</td>
<td>BackgroundWorker</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Basic Usage</td>
<td>基本的な使い方</td>
<td>基礎的な使用方法</td>
<td>-</td>
</tr>
<tr>
<td>Behavior</td>
<td>動作</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>BenchmarkResults</td>
<td>BenchmarkResults</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Best</td>
<td>最良</td>
<td>最も良い品質を示す（Knowledge indexのindex-type）</td>
<td>-</td>
</tr>
<tr>
<td>Best Practices</td>
<td>ベストプラクティス</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>BM25Context</td>
<td>BM25Context</td>
<td>Rust内部実装用の型</td>
<td><a href="01_glossary.md">詳細</a><br/>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>BM25DataPoint</td>
<td>BM25DataPoint</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>BM25Index</td>
<td>BM25Index</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Builder</td>
<td>Builder</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Built-in Tools</td>
<td>ビルトインツール</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Caching</td>
<td>キャッシング</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>CandleTextEmbedder</td>
<td>CandleTextEmbedder</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Change shortcut key (default: t)</td>
<td>ショートカットキーの変更（デフォルト: t）</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>ChatMessage</td>
<td>ChatMessage</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>ChatResponseStream</td>
<td>ChatResponseStream</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>ChatResponseStreamUnmarshaller</td>
<td>ChatResponseStreamUnmarshaller</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Check/reset shortcut key</td>
<td>Check/reset shortcut key</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>CitationTarget</td>
<td>CitationTarget</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Client</td>
<td>Client</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>command</td>
<td>コマンド</td>
<td>実行する命令（小文字形式）</td>
<td>-</td>
</tr>
<tr>
<td>Commands</td>
<td>コマンド</td>
<td>実行可能な命令</td>
<td>-</td>
</tr>
<tr>
<td>Complete Example</td>
<td>Complete Example</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Config</td>
<td>Config</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Configuration</td>
<td>設定</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Configuration Options</td>
<td>設定オプション</td>
<td>設定可能な項目や選択肢</td>
<td>-</td>
</tr>
<tr>
<td>ContextCreator</td>
<td>ContextCreator</td>
<td>Rust内部実装用の型</td>
<td><a href="01_glossary.md">詳細</a><br/>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>ContextManager</td>
<td>ContextManager</td>
<td>Rust内部実装用の型</td>
<td><a href="01_glossary.md">詳細</a><br/>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>ContextTruncationScheme</td>
<td>ContextTruncationScheme</td>
<td>Rust内部実装用の型</td>
<td><a href="01_glossary.md">詳細</a><br/>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Contributing</td>
<td>貢献</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Create a Custom Default</td>
<td>カスタムデフォルトの作成</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Customizing Default Behavior</td>
<td>デフォルト動作のカスタマイズ</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>DataPoint</td>
<td>DataPoint</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Default</td>
<td>デフォルト</td>
<td>初期設定、標準設定</td>
<td>-</td>
</tr>
<tr>
<td>Default Resources</td>
<td>デフォルトリソース</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Defining Hooks</td>
<td>フックの定義</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>description</td>
<td>description</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Description Field</td>
<td>descriptionフィールド</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Directory Creation</td>
<td>ディレクトリ作成</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>disabled</td>
<td>disabled</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Effective Searching</td>
<td>Effective Searching</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>EmbeddingType</td>
<td>EmbeddingType</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>EnabledTodoList</td>
<td>EnabledTodoList</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>env</td>
<td>env</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Error</td>
<td>エラー</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>ErrorCodeClassifier</td>
<td>ErrorCodeClassifier</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>EventReceiver</td>
<td>EventReceiver</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Exact Matches</td>
<td>完全一致</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Example 1: Exploring Alternatives</td>
<td>Example 1: Exploring Alternatives</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Example 2: Getting Q CLI Help</td>
<td>Example 2: Getting Q CLI Help</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Example 3: Clarifying Requirements</td>
<td>Example 3: Clarifying Requirements</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Example 4: Keeping Useful Information</td>
<td>Example 4: Keeping Useful Information</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Example Usage</td>
<td>Example Usage</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Example Workflow</td>
<td>ワークフロー例</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>ExampleErrorCodeClassifier</td>
<td>ExampleErrorCodeClassifier</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Examples</td>
<td>例</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Execute_bash Tool</td>
<td>Execute_bashツール</td>
<td>Bashコマンド実行ツール</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>ExportResultArchive</td>
<td>ExportResultArchive</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>ExportResultArchiveError</td>
<td>ExportResultArchiveError</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Fast</td>
<td>高速</td>
<td>処理速度が速いことを示す（Knowledge indexのindex-type）</td>
<td>-</td>
</tr>
<tr>
<td>File Type Support</td>
<td>File Type Support</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>File URI Examples</td>
<td>ファイルURI例</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>File URI Path Resolution</td>
<td>ファイルURIパス解決</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>FileProcessor</td>
<td>FileProcessor</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Files Not Being Indexed</td>
<td>Files Not Being Indexed</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>FileType</td>
<td>FileType</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Folder Structure</td>
<td>フォルダ構造</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>ForeverSleep</td>
<td>ForeverSleep</td>
<td>永続的なスリープ状態を表すRust型</td>
<td>-</td>
</tr>
<tr>
<td>Fs_read Tool</td>
<td>Fs_readツール</td>
<td>ファイル読み取りツール</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Fs_write Tool</td>
<td>Fs_writeツール</td>
<td>ファイル書き込みツール</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Fuzzy Search Support</td>
<td>ファジー検索サポート</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>GenerateAssistantResponse</td>
<td>GenerateAssistantResponse</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>GenerateAssistantResponseError</td>
<td>GenerateAssistantResponseError</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>GenerateTaskAssistPlan</td>
<td>GenerateTaskAssistPlan</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>GenerateTaskAssistPlanError</td>
<td>GenerateTaskAssistPlanError</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Getting Started</td>
<td>はじめに</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Global</td>
<td>グローバル</td>
<td>全体に適用される設定や範囲</td>
<td>-</td>
</tr>
<tr>
<td>headers</td>
<td>headers</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Hook Event</td>
<td>フックイベント</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Hook Output</td>
<td>フック出力</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Hook Types</td>
<td>フックタイプ</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Hooks</td>
<td>フック</td>
<td>特定のイベント発生時に実行される処理</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>hooks</td>
<td>hooks</td>
<td>技術用語</td>
<td><a href="01_glossary.md">詳細</a><br/>英語のまま使用</td>
</tr>
<tr>
<td>Hooks Field</td>
<td>Hooks Field</td>
<td>技術用語または型名</td>
<td><a href="01_glossary.md">詳細</a><br/>英語のまま使用</td>
</tr>
<tr>
<td>HostedModelClient</td>
<td>HostedModelClient</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>How It Works</td>
<td>仕組み</td>
<td>動作原理や内部構造の説明</td>
<td>-</td>
</tr>
<tr>
<td>If development-helper doesn't exist, falls back to built-in default</td>
<td>If development-helper doesn't exist, falls back to built-in default</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Important Limitations</td>
<td>重要な制限事項</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Important Notes</td>
<td>重要な注意事項</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Indexing Process</td>
<td>Indexing Process</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>IndexingJob</td>
<td>IndexingJob</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>IndexingParams</td>
<td>IndexingParams</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Installation</td>
<td>インストール</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Interactive Selection</td>
<td>対話的選択</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>InternalServerExceptionReason</td>
<td>InternalServerExceptionReason</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Introspect Tool</td>
<td>Introspectツール</td>
<td>Q CLI自身の情報を提供するツール</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Keyboard Shortcut</td>
<td>キーボードショートカット</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Keyboard Shortcut Not Working</td>
<td>Keyboard Shortcut Not Working</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>KnowledgeContext</td>
<td>KnowledgeContext</td>
<td>Rust内部実装用の型</td>
<td><a href="01_glossary.md">詳細</a><br/>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Licensing</td>
<td>ライセンス</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Limitations</td>
<td>制限事項</td>
<td>機能の制約や限界</td>
<td>-</td>
</tr>
<tr>
<td>Lists Not Loading</td>
<td>リストが読み込まれません</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Managing Large Projects</td>
<td>Managing Large Projects</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Managing Lists</td>
<td>リストの管理</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Metric</td>
<td>Metric</td>
<td>メトリクス測定用のRust型</td>
<td>-</td>
</tr>
<tr>
<td>MockTextEmbedder</td>
<td>MockTextEmbedder</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>ModelConfig</td>
<td>ModelConfig</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>ModelDownloader</td>
<td>ModelDownloader</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>ModelType</td>
<td>ModelType</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>ModelValidator</td>
<td>ModelValidator</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>name</td>
<td>name</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Name Field</td>
<td>nameフィールド</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Naming Conflicts</td>
<td>名前の競合</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Native Tool Patterns</td>
<td>ネイティブツールパターン</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>No Lists Available</td>
<td>利用可能なリストがありません</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>oauth</td>
<td>oauth</td>
<td>技術用語</td>
<td><a href="01_glossary.md">詳細</a><br/>英語のまま使用</td>
</tr>
<tr>
<td>oauthScopes</td>
<td>oauthScopes</td>
<td>技術用語</td>
<td><a href="01_glossary.md">詳細</a><br/>英語のまま使用</td>
</tr>
<tr>
<td>OnnxModelType</td>
<td>OnnxModelType</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>OperationHandle</td>
<td>OperationHandle</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>OperationManager</td>
<td>OperationManager</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>OperationStatus</td>
<td>OperationStatus</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>OperationType</td>
<td>OperationType</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Or enable via settings</td>
<td>Or enable via settings</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Override for specific task</td>
<td>Override for specific task</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Params</td>
<td>Params</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Pattern Filtering Best Practices</td>
<td>Pattern Filtering Best Practices</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Pattern Issues</td>
<td>Pattern Issues</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Pattern Matching Rules</td>
<td>パターンマッチングルール</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>PatternFilter</td>
<td>PatternFilter</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Performance Considerations</td>
<td>Performance Considerations</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Performance Issues</td>
<td>Performance Issues</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Persistence</td>
<td>Persistence</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>PostToolUse</td>
<td>PostToolUse</td>
<td>ツール使用後のフック</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Prerequisites</td>
<td>前提条件</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>PreToolUse</td>
<td>PreToolUse</td>
<td>ツール使用前のフック</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>ProgressInfo</td>
<td>ProgressInfo</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>ProgressStatus</td>
<td>ProgressStatus</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Project Layout</td>
<td>プロジェクト構成</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>redirectUri</td>
<td>redirectUri</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Related Features</td>
<td>関連機能</td>
<td>関係する他の機能</td>
<td>-</td>
</tr>
<tr>
<td>Report_issue Tool</td>
<td>Report_issueツール</td>
<td>問題報告ツール</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>resources</td>
<td>resources</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Resources Field</td>
<td>resourcesフィールド</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>ResultArchiveStreamUnmarshaller</td>
<td>ResultArchiveStreamUnmarshaller</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Resuming a TODO list (after selecting):</td>
<td>Resuming a TODO list (after selecting):</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Search Capabilities</td>
<td>Search Capabilities</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Search Not Finding Expected Results</td>
<td>Search Not Finding Expected Results</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>SearchResult</td>
<td>SearchResult</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Security</td>
<td>セキュリティ</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Selecting a TODO list to view:</td>
<td>表示するTODOリストを選択:</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>SemanticContext</td>
<td>SemanticContext</td>
<td>Rust内部実装用の型</td>
<td><a href="01_glossary.md">詳細</a><br/>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>SemanticSearchClient</td>
<td>SemanticSearchClient</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>SemanticSearchConfig</td>
<td>SemanticSearchConfig</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>SemanticSearchError</td>
<td>SemanticSearchError</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>SendMessage</td>
<td>SendMessage</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>SendMessageError</td>
<td>SendMessageError</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Server</td>
<td>サーバー</td>
<td>サービスを提供するシステム</td>
<td>-</td>
</tr>
<tr>
<td>ServiceQuotaExceededExceptionReason</td>
<td>ServiceQuotaExceededExceptionReason</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Set your preferred default</td>
<td>Set your preferred default</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Settings Integration</td>
<td>設定統合</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Stop</td>
<td>Stop</td>
<td>停止時のフック</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Storage</td>
<td>ストレージ</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Storage and Persistence</td>
<td>Storage and Persistence</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Summary</td>
<td>Summary</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Switch back to default</td>
<td>Switch back to default</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>SystemStatus</td>
<td>SystemStatus</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>TextEmbedder</td>
<td>TextEmbedder</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>TFTextEmbedder</td>
<td>TFTextEmbedder</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>The preserved entry (question + answer about debugging techniques) is now part of main conversation</td>
<td>The preserved entry (question + answer about debugging techniques) is now part of main conversation</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>This will override defaults with explicit patterns</td>
<td>This will override defaults with explicit patterns</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>This will use the default patterns</td>
<td>This will use the default patterns</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>This will use your default setting</td>
<td>This will use your default setting</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>ThrottlingExceptionReason</td>
<td>ThrottlingExceptionReason</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Timeout</td>
<td>タイムアウト</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>timeout</td>
<td>timeout</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Tips</td>
<td>Tips</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>TODO List Storage</td>
<td>TODOリストストレージ</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>TODO Lists</td>
<td>TODOリスト</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Token</td>
<td>トークン</td>
<td>テキストの最小単位、コンテキストウィンドウの計測単位</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Tool Matching</td>
<td>ツールマッチング</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Tool Permissions</td>
<td>ツール権限</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>toolAliases</td>
<td>toolAliases</td>
<td>技術用語</td>
<td><a href="01_glossary.md">詳細</a><br/>英語のまま使用</td>
</tr>
<tr>
<td>ToolAliases Field</td>
<td>toolAliasesフィールド</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>tools</td>
<td>tools</td>
<td>技術用語</td>
<td><a href="01_glossary.md">詳細</a><br/>英語のまま使用</td>
</tr>
<tr>
<td>Tools Field</td>
<td>toolsフィールド</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>toolsSettings</td>
<td>toolsSettings</td>
<td>技術用語</td>
<td><a href="01_glossary.md">詳細</a><br/>英語のまま使用</td>
</tr>
<tr>
<td>ToolsSettings Field</td>
<td>toolsSettingsフィールド</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>TransformationDownloadArtifactType</td>
<td>TransformationDownloadArtifactType</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Troubleshooting</td>
<td>トラブルシューティング</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Trusted Tools</td>
<td>信頼されたツール</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>type</td>
<td>type</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Unhandled</td>
<td>Unhandled</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>UnknownVariantError</td>
<td>UnknownVariantError</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>UnknownVariantValue</td>
<td>UnknownVariantValue</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>UriModifierInterceptor</td>
<td>UriModifierInterceptor</td>
<td>URI変更を傍受するRust型</td>
<td>-</td>
</tr>
<tr>
<td>url</td>
<td>url</td>
<td>技術用語</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Usage</td>
<td>使用方法</td>
<td>-</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Usage Examples</td>
<td>使用例</td>
<td>実際の使い方の例</td>
<td>-</td>
</tr>
<tr>
<td>Use_aws Tool</td>
<td>Use_awsツール</td>
<td>AWS操作ツール</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>User</td>
<td>ユーザー</td>
<td>システムの利用者</td>
<td>-</td>
</tr>
<tr>
<td>User Default Not Found</td>
<td>ユーザーデフォルトが見つかりません</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>VectorIndex</td>
<td>VectorIndex</td>
<td>Rust内部実装用の型</td>
<td>Rust型名は英語のまま使用</td>
</tr>
<tr>
<td>Version</td>
<td>バージョン</td>
<td>ソフトウェアのリリース番号</td>
<td>-</td>
</tr>
<tr>
<td>What It Provides</td>
<td>提供される機能</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>When NOT to Use</td>
<td>When NOT to Use</td>
<td>技術用語または型名</td>
<td>英語のまま使用</td>
</tr>
<tr>
<td>Wildcard Patterns</td>
<td>ワイルドカードパターン</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Workflow Integration</td>
<td>ワークフロー統合</td>
<td>-</td>
<td>-</td>
</tr>
</tbody>
</table>

---

### UI要素（9用語）

<table>
<colgroup>
<col style="width: 30%;">
<col style="width: 25%;">
<col style="width: 30%;">
<col style="width: 15%;">
</colgroup>
<thead>
<tr>
<th>英語</th>
<th>日本語</th>
<th>説明</th>
<th>注記</th>
</tr>
</thead>
<tbody>
<tr>
<td>Error Messages</td>
<td>エラーメッセージ</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>File URI Prompt</td>
<td>ファイルURIプロンプト</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Inline Prompt</td>
<td>インラインプロンプト</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>prompt</td>
<td>プロンプト</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Prompt Field</td>
<td>promptフィールド</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>UserPromptSubmit</td>
<td>UserPromptSubmit</td>
<td>ユーザープロンプト送信時のフック</td>
<td>-</td>
</tr>
<tr>
<td>userPromptSubmit</td>
<td>userPromptSubmit</td>
<td>ユーザープロンプト送信イベント</td>
<td>-</td>
</tr>
<tr>
<td>Visual Indicators</td>
<td>視覚的インジケーター</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>with warning message</td>
<td>警告メッセージ付き</td>
<td>-</td>
<td>-</td>
</tr>
</tbody>
</table>

---

### 実験的機能（7用語）

<table>
<colgroup>
<col style="width: 30%;">
<col style="width: 25%;">
<col style="width: 30%;">
<col style="width: 15%;">
</colgroup>
<thead>
<tr>
<th>英語</th>
<th>日本語</th>
<th>説明</th>
<th>注記</th>
</tr>
</thead>
<tbody>
<tr>
<td>Available Experiments</td>
<td>利用可能な実験的機能</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Enable via experiment (select from list)</td>
<td>/experimentコマンドで有効化（リストから選択）</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Experimental Features</td>
<td>実験的機能</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Knowledge Tool (experimental)</td>
<td>Knowledgeツール（実験的）</td>
<td>Knowledge管理ツール</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>Managing Experiments</td>
<td>実験的機能の管理</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>Thinking Tool (experimental)</td>
<td>Thinkingツール（実験的）</td>
<td>思考過程表示ツール</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
<tr>
<td>TODO List Tool (experimental)</td>
<td>TODO Listツール（実験的）</td>
<td>TODOリスト管理ツール</td>
<td><a href="01_glossary.md">詳細</a></td>
</tr>
</tbody>
</table>

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
| v2.1.0 | 2025-10-18 | サイト全体の用語チェックに基づき6用語追加（Server, Default, Version, Global, User, Token）<br/>表形式に変更（可読性向上、75%の行数削減）<br/>列幅を明示的に指定（英語30%, 日本語25%, 説明30%, 注記15%） |
| v2.0.0 | 2025-10-18 | Phase 3完了: 全278用語の翻訳完了（100%達成） |
| v1.0.0 | 2025-10-18 | 初版リリース: 公式リポジトリから316用語を抽出 |

---

*このドキュメントは公式リポジトリ（aws/amazon-q-developer-cli）から自動抽出された用語を基に作成されています。*

