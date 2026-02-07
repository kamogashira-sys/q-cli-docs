# Kiro CLI Help Agent

**出典**: [Help Agent - Kiro CLI Documentation](https://kiro.dev/docs/cli/chat/help-agent/)

## 概要

Kiro CLI v1.25.0（2026年2月4日リリース）で追加されたHelp Agent機能について詳細に解説します。この機能により、Kiro CLIの使い方、コマンド、ツール、設定について、実際のドキュメントに基づいた正確な回答を即座に得ることができます。

### Help Agentとは

Help Agentは、**Kiro CLIドキュメントを使用した組み込みヘルプエージェント**です。一般的なAI応答ではなく、実際のKiro CLIドキュメントから情報を取得して回答します。

### 主な特徴

- **ドキュメントベース**: 実際のKiro CLIドキュメントから回答
- **即座に回答**: `/help`コマンドで即座に切り替え
- **設定ファイル作成**: `.kiro/`ディレクトリに設定ファイルを作成可能
- **レガシーモード**: `--legacy`オプションで従来のコマンド一覧表示

### なぜHelp Agentが必要なのか

従来、Kiro CLIの使い方を調べるには、以下の方法がありました：

1. **公式ドキュメント**: ブラウザで検索
2. **`--help`オプション**: コマンドラインヘルプ
3. **一般的なAI**: 不正確な情報の可能性

Help Agentは、これらの問題を解決し、正確で即座に利用可能なヘルプを提供します。

## 📋 目次

- [使用方法](#使用方法)
- [質問できる内容](#質問できる内容)
- [設定ファイルの作成](#設定ファイルの作成)
- [実用例](#実用例)
- [元のエージェントに戻る](#元のエージェントに戻る)
- [ベストプラクティス](#ベストプラクティス)
- [関連リンク](#関連リンク)

---

## 使用方法

### 基本的な使い方

Help Agentに切り替えるには、`/help`コマンドを使用します。

```bash
> /help
✔ Switched to agent: kiro_help

[help] > 
```

プロンプトが`[help] >`に変わり、Help Agentモードになります。

### 直接質問

`/help`コマンドに質問を続けて、直接質問できます。

```bash
> /help How do I configure MCP servers?
```

この場合、Help Agentに切り替えずに、質問の回答のみを取得します。

### レガシーモード

従来のコマンド一覧を表示するには、`--legacy`オプションを使用します。

```bash
> /help --legacy
```

これにより、利用可能なコマンドの一覧が表示されます。

---

## 質問できる内容

Help Agentは、Kiro CLIの包括的なドキュメントにアクセスできます。

### コマンド

**スラッシュコマンド**:
- `/chat` - チャットセッション管理
- `/agent` - エージェント管理
- `/context` - コンテキスト管理
- `/tools` - ツール一覧表示
- `/help` - Help Agent

**CLIコマンド**:
- `kiro-cli chat` - チャット開始
- `kiro-cli settings` - 設定管理
- `kiro-cli acp` - ACP統合

**質問例**:
```bash
[help] > How do I save a conversation?
```

### ツール

**ビルトインツール**:
- `fs_read` - ファイル読み込み
- `fs_write` - ファイル書き込み
- `code` - コード理解
- `grep` - パターン検索
- `glob` - ファイル検索

**質問例**:
```bash
[help] > What does the code tool do?
```

### 設定

**設定項目**:
- `chat.diffTool` - Diffツール設定
- `chat.enableTangentMode` - Tangent Mode設定
- `toolsSettings.subagent` - サブエージェント設定
- `mcp.servers` - MCPサーバー設定

**質問例**:
```bash
[help] > How do I enable tangent mode?
```

### 機能

**主要機能**:
- Tangent Mode - 並列会話モード
- Hooks - イベントフック
- MCP - Model Context Protocol
- Code Intelligence - コード理解
- Subagents - サブエージェント

**質問例**:
```bash
[help] > What is Tangent Mode?
```

### ショートカット

**キーボードショートカット**:
- `Ctrl+C` - 実行中断
- `Ctrl+D` - セッション終了
- `Ctrl+R` - 履歴検索

**質問例**:
```bash
[help] > What keyboard shortcuts are available?
```

---

## 設定ファイルの作成

Help Agentは、`.kiro/`ディレクトリに設定ファイルを作成できます。

### エージェント作成

**質問例**:
```bash
[help] > Create an agent for writing tests
```

**結果**:
```
✔ Created .kiro/agents/test-writer.yaml

I've created a test-writing agent. Switch to it with:
/agent swap test-writer
```

**作成されるファイル**:
```
.kiro/agents/test-writer.yaml
```

### プロンプト作成

**質問例**:
```bash
[help] > Create a prompt for code review
```

**結果**:
```
✔ Created .kiro/prompts/code-review.md

I've created a code review prompt. Use it with:
/context add .kiro/prompts/code-review.md
```

**作成されるファイル**:
```
.kiro/prompts/code-review.md
```

### LSP設定作成

**質問例**:
```bash
[help] > Create LSP config for Python
```

**結果**:
```
✔ Created .kiro/lsp-config.yaml

I've created an LSP config for Python. Restart Kiro to apply.
```

**作成されるファイル**:
```
.kiro/lsp-config.yaml
```

---

## 実用例

### 例1: コマンドについて質問

**質問**:
```bash
[help] > How do I save a conversation?
```

**回答**:
```
Use `/chat save` to save your current conversation:

/chat save ~/my-session.json   # Save to a specific path

Saved conversations can be loaded later with /chat load.
```

### 例2: ツールについて質問

**質問**:
```bash
[help] > What does the code tool do?
```

**回答**:
```
The code tool provides code intelligence:

• search_symbols - Find symbol definitions by name
• lookup_symbols - Get details for specific symbols  
• get_document_symbols - List all symbols in a file
• pattern_search - AST-based structural search

It uses AST parsing for accurate code understanding across languages.
```

### 例3: 設定について質問

**質問**:
```bash
[help] > How do I enable tangent mode?
```

**回答**:
```
Enable Tangent Mode with:

kiro-cli settings chat.enableTangentMode true

Or use /tangent during a chat session to toggle it.
```

### 例4: エージェント作成

**質問**:
```bash
[help] > Create an agent for writing documentation
```

**回答**:
```
✔ Created .kiro/agents/docs-writer.yaml

I've created a documentation-writing agent with:
- Focus on clear, concise documentation
- Markdown formatting
- Code examples

Switch to it with:
/agent swap docs-writer
```

---

## 元のエージェントに戻る

Help Agentから元のエージェントに戻るには、再度`/help`コマンドを実行します。

```bash
[help] > /help
✔ Switched to agent: kiro_default
```

または、`/agent swap`コマンドで特定のエージェントに切り替えます。

```bash
[help] > /agent swap my-agent
✔ Switched to agent: my-agent
```

---

## ベストプラクティス

### 1. 具体的な質問をする

**良い例**:
```bash
[help] > How do I configure MCP servers?
```

**悪い例**:
```bash
[help] > MCP
```

具体的な質問をすることで、より正確な回答が得られます。

### 2. コマンド名を含める

**良い例**:
```bash
[help] > What does /context add do?
```

**悪い例**:
```bash
[help] > How do I add context?
```

コマンド名を含めることで、より具体的な回答が得られます。

### 3. 設定ファイル作成を活用

Help Agentは、設定ファイルを作成できます。手動で作成するよりも、Help Agentに依頼する方が効率的です。

**例**:
```bash
[help] > Create an agent for testing
[help] > Create a prompt for code review
[help] > Create LSP config for TypeScript
```

### 4. レガシーモードを使い分ける

コマンド一覧を確認したい場合は、`--legacy`オプションを使用します。

```bash
> /help --legacy
```

### 5. 直接質問を活用

Help Agentに切り替えずに、直接質問できます。

```bash
> /help How do I save a conversation?
```

これにより、現在のエージェントを維持したまま、ヘルプを取得できます。

---

## 関連リンク

### 公式ドキュメント
- [Help Agent - Kiro CLI Documentation](https://kiro.dev/docs/cli/chat/help-agent/)
- [Kiro CLI v1.25.0 Changelog](https://kiro.dev/changelog/cli/1-25/)

### 関連機能
- [Agent Client Protocol (ACP)](13_ACP.md) - エディタ統合
- [サブエージェント機能](02_Subagents.md) - エージェント委譲
- [Planエージェント機能](03_PlanAgent.md) - 実装計画作成

### スラッシュコマンド
- `/chat` - チャットセッション管理
- `/agent` - エージェント管理
- `/context` - コンテキスト管理
- `/tools` - ツール一覧表示

---

**最終更新**: 2026年2月7日
