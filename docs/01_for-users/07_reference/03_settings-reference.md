[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [リファレンス](README.md) > 03 Settings Reference

---

# Amazon Q CLI 設定項目完全リファレンス

**作成日**: 2025-10-08  
最終更新: %Y->-  
**ソースコード**: `crates/chat-cli/src/database/settings.rs`  
**対象バージョン**: v1.18.0以降

---

## 📚 このドキュメントの使い方

- **初めての方**: [初心者向けクイックスタート](#-初心者向けクイックスタート) を参照（5分）
- **すべての設定を確認したい方**: [全設定項目一覧](#-全設定項目一覧全35項目) を参照

---

## 🚀 初心者向けクイックスタート

Q CLIを始めるために**最低限必要な設定**と**便利な設定**を紹介します。

### ステップ1: 必須設定（2項目）

まずはこの2つを設定してください。

```bash
# 1. デフォルトAgentを設定
q settings chat.defaultAgent my-agent

# 2. テレメトリを設定（プライバシー重視の場合は無効化）
q settings telemetry.enabled false
```

| 設定キー | 説明 | デフォルト値 |
|---------|------|-------------|
| `chat.defaultAgent` | デフォルトで使用するAgent名 | なし |
| `telemetry.enabled` | 使用状況データの収集（プライバシー設定） | `true` |

---

### ステップ2: 推奨設定（5項目）

より便利に使うための設定です。必要に応じて有効化してください。

```bash
# 複雑な推論機能を有効化（推奨）
q settings chat.enableThinking true

# Knowledge Base機能を有効化（コードベース検索）
q settings chat.enableKnowledge true

# 履歴ヒントを表示（過去の会話を参照）
q settings chat.enableHistoryHints true

# TODOリスト機能を有効化
q settings chat.enableTodoList true

# チェックポイント機能を有効化（会話の保存・復元）
q settings chat.enableCheckpoint true
```

| 設定キー | 説明 | デフォルト値 |
|---------|------|-------------|
| `chat.enableThinking` | 複雑な推論のためのThinkingツール | `false` |
| `chat.enableKnowledge` | Knowledge Base機能（コードベース検索） | `false` |
| `chat.enableHistoryHints` | 会話履歴ヒントの表示 | `false` |
| `chat.enableTodoList` | TODOリスト機能 | `false` |
| `chat.enableCheckpoint` | チェックポイント機能（会話の保存・復元） | `false` |

---

### 設定の確認

```bash
# すべての設定を確認
q settings list

# 特定の設定を確認
q settings chat.enableThinking
```

---

### 次のステップ

- より詳細な設定は [全設定項目一覧](#-全設定項目一覧全35項目) を参照
- 設定の優先順位は [設定優先順位ガイド](../03_configuration/07_priority-rules.md) を参照
- 推奨設定は [推奨設定ガイド](../04_best-practices/01_configuration.md) を参照

---

## 📋 全設定項目一覧（全35項目）

すべての設定項目の完全リストです。上級者向けの詳細設定も含まれます。

> 💡 **初心者の方へ**: このセクションは参考情報です。[クイックスタート](#-初心者向けクイックスタート)の設定だけで十分使えます。

### 設定方法

これらの設定項目は以下の方法で設定できます：

1. **コマンドラインから設定**:
   ```bash
   q settings <設定キー> <値>
   # 例: q settings chat.defaultAgent my-agent
   ```

2. **設定ファイルで設定**:
   - グローバル設定: `~/.local/share/amazon-q/settings.json`
   - Agent設定: `.amazonq/cli-agents/<agent-name>.json`

3. **環境変数で設定**:
   - 一部の設定項目は環境変数でも設定可能

詳細は [設定優先順位ガイド](../03_configuration/07_priority-rules.md) を参照してください。

---

### 全項目リスト

| # | 設定キー | 型 | 説明 | カテゴリ |
|---|---------|-----|------|---------|
| 1 | `telemetry.enabled` | Boolean | テレメトリ収集の有効/無効 | テレメトリ |
| 2 | `telemetryClientId` | String | テレメトリ用クライアント識別子 | テレメトリ |
| 3 | `codeWhisperer.shareCodeWhispererContentWithAWS` | Boolean | CodeWhispererサービスとのコンテンツ共有 | CodeWhisperer |
| 4 | `chat.enableThinking` | Boolean | 複雑な推論のためのThinkingツール有効化 | 実験的機能 |
| 5 | `chat.enableKnowledge` | Boolean | Knowledge Base機能の有効化 | 実験的機能 |
| 6 | `knowledge.defaultIncludePatterns` | Array | Knowledge Baseに含めるデフォルトファイルパターン | Knowledge |
| 7 | `knowledge.defaultExcludePatterns` | Array | Knowledge Baseから除外するデフォルトファイルパターン | Knowledge |
| 8 | `knowledge.maxFiles` | Number | Knowledgeインデックス作成の最大ファイル数 | Knowledge |
| 9 | `knowledge.chunkSize` | Number | Knowledge処理のテキストチャンクサイズ | Knowledge |
| 10 | `knowledge.chunkOverlap` | Number | テキストチャンク間のオーバーラップ | Knowledge |
| 11 | `knowledge.indexType` | String | 使用するKnowledgeインデックスのタイプ | Knowledge |
| 12 | `chat.skimCommandKey` | String (1文字) | ファジー検索コマンドのキーバインド | キーバインド |
| 13 | `chat.autocompletionKey` | String (1文字) | オートコンプリートヒント受け入れのキーバインド | キーバインド |
| 14 | `chat.enableTangentMode` | Boolean | Tangentモード機能の有効化 | 実験的機能 |
| 15 | `chat.tangentModeKey` | String (1文字) | Tangentモードトグルのキーバインド | キーバインド |
| 16 | `chat.delegateModeKey` | String (1文字) | Delegateコマンドのキーバインド | キーバインド |
| 17 | `introspect.tangentMode` | Boolean | introspectクエリで自動的にTangentモードに入る | Introspect |
| 18 | `chat.greeting.enabled` | Boolean | チャット開始時の挨拶メッセージ表示 | チャットUI |
| 19 | `api.timeout` | Number | APIリクエストのタイムアウト（秒） | API |
| 20 | `chat.editMode` | Boolean | チャットインターフェースの編集モード有効化 | チャットUI |
| 21 | `chat.enableNotifications` | Boolean | デスクトップ通知の有効化 | チャットUI |
| 22 | `api.codewhisperer.service` | String | CodeWhispererサービスエンドポイントURL | API |
| 23 | `api.q.service` | String | QサービスエンドポイントURL | API |
| 24 | `mcp.initTimeout` | Number | MCPサーバー初期化タイムアウト | MCP |
| 25 | `mcp.noInteractiveTimeout` | Number | 非対話型MCPタイムアウト | MCP |
| 26 | `mcp.loadedBefore` | Boolean | 以前にロードされたMCPサーバーの追跡 | MCP |
| 27 | `chat.enableContextUsageIndicator` | Boolean | プロンプトにコンテキスト使用率パーセンテージ表示 | 実験的機能 |
| 28 | `chat.defaultModel` | String | 会話のデフォルトAIモデル | チャット |
| 29 | `chat.disableMarkdownRendering` | Boolean | チャットでのMarkdownフォーマット無効化 | チャットUI |
| 30 | `chat.defaultAgent` | String | デフォルトAgent設定 | Agent |
| 31 | `chat.disableAutoCompaction` | Boolean | 自動会話要約の無効化 | チャット |
| 32 | `chat.enableHistoryHints` | Boolean | 会話履歴ヒントの表示 | チャットUI |
| 33 | `chat.enableTodoList` | Boolean | TODOリスト機能の有効化 | 実験的機能 |
| 34 | `chat.enableCheckpoint` | Boolean | チェックポイント機能の有効化 | 実験的機能 |
| 35 | `chat.enableDelegate` | Boolean | サブエージェント管理のためのDelegateツール有効化 | 実験的機能 |

---

## カテゴリ別設定項目

### テレメトリ設定

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `telemetry.enabled` | Boolean | テレメトリ収集の有効/無効 |
| `telemetryClientId` | String | クライアント識別子 |

### CodeWhisperer設定

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `codeWhisperer.shareCodeWhispererContentWithAWS` | Boolean | コンテンツ共有 |

### チャット設定

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `chat.defaultModel` | String | デフォルトAIモデル |
| `chat.defaultAgent` | String | デフォルトAgent |
| `chat.disableAutoCompaction` | Boolean | 自動要約の無効化 |

### チャットUI設定

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `chat.greeting.enabled` | Boolean | 挨拶メッセージ表示 |
| `chat.editMode` | Boolean | 編集モード |
| `chat.enableNotifications` | Boolean | デスクトップ通知 |
| `chat.disableMarkdownRendering` | Boolean | Markdown無効化 |
| `chat.enableHistoryHints` | Boolean | 履歴ヒント表示 |

### 実験的機能設定

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `chat.enableThinking` | Boolean | Thinkingツール |
| `chat.enableKnowledge` | Boolean | Knowledge Base |
| `chat.enableTangentMode` | Boolean | Tangentモード |
| `chat.enableContextUsageIndicator` | Boolean | コンテキスト使用率表示 |
| `chat.enableTodoList` | Boolean | TODOリスト |
| `chat.enableCheckpoint` | Boolean | チェックポイント |
| `chat.enableDelegate` | Boolean | Delegateツール |

### Knowledge設定

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `knowledge.defaultIncludePatterns` | Array | 含めるファイルパターン |
| `knowledge.defaultExcludePatterns` | Array | 除外するファイルパターン |
| `knowledge.maxFiles` | Number | 最大ファイル数 |
| `knowledge.chunkSize` | Number | チャンクサイズ |
| `knowledge.chunkOverlap` | Number | チャンクオーバーラップ |
| `knowledge.indexType` | String | インデックスタイプ |

### キーバインド設定

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `chat.skimCommandKey` | String (1文字) | ファジー検索 |
| `chat.autocompletionKey` | String (1文字) | オートコンプリート |
| `chat.tangentModeKey` | String (1文字) | Tangentモード |
| `chat.delegateModeKey` | String (1文字) | Delegateコマンド |

### API設定

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `api.timeout` | Number | APIタイムアウト（秒） |
| `api.codewhisperer.service` | String | CodeWhispererエンドポイント |
| `api.q.service` | String | Qサービスエンドポイント |

### MCP設定

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `mcp.initTimeout` | Number | 初期化タイムアウト |
| `mcp.noInteractiveTimeout` | Number | 非対話型タイムアウト |
| `mcp.loadedBefore` | Boolean | ロード履歴追跡 |

### その他

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `introspect.tangentMode` | Boolean | introspect自動Tangent |

---

## 設定方法

### コマンドラインから設定

```bash
# 設定の取得
q settings <key>

# 設定の変更
q settings <key> <value>

# 設定の削除
q settings --delete <key>

# 全設定の表示
q settings list
```

### 設定ファイルを直接編集

```bash
# エディタで設定ファイルを開く
q settings open

# 設定ファイルの場所
# Linux/WSL: ~/.local/share/amazon-q/settings.json
# macOS: ~/Library/Application Support/amazon-q/settings.json
# Windows: %LOCALAPPDATA%\amazon-q\settings.json
```

---

## 設定例

### 基本設定

```bash
# デフォルトAgentを設定
q settings chat.defaultAgent my-agent

# Markdownレンダリングを無効化
q settings chat.disableMarkdownRendering true

# 履歴ヒントを有効化
q settings chat.enableHistoryHints true
```

### 実験的機能の有効化

```bash
# Thinkingツールを有効化
q settings chat.enableThinking true

# Knowledge Baseを有効化
q settings chat.enableKnowledge true

# Tangentモードを有効化
q settings chat.enableTangentMode true
```

### Knowledge設定

```bash
# 最大ファイル数を設定
q settings knowledge.maxFiles 1000

# チャンクサイズを設定
q settings knowledge.chunkSize 1000

# チャンクオーバーラップを設定
q settings knowledge.chunkOverlap 200
```

### MCP設定

```bash
# MCP初期化タイムアウトを設定（ミリ秒）
q settings mcp.initTimeout 180000

# 非対話型MCPタイムアウトを設定
q settings mcp.noInteractiveTimeout 60000
```

---

## 設定ファイルの構造

設定は`~/.local/share/amazon-q/settings.json`にJSON形式で保存されます。

```json
{
  "telemetry.enabled": true,
  "chat.defaultAgent": "my-agent",
  "chat.enableThinking": true,
  "chat.enableKnowledge": true,
  "chat.disableMarkdownRendering": false,
  "chat.enableHistoryHints": true,
  "knowledge.maxFiles": 1000,
  "knowledge.chunkSize": 1000,
  "knowledge.chunkOverlap": 200,
  "mcp.initTimeout": 180000
}
```

---

## ⚙️ ハードコードされた制限値（設定不可）

以下の値はソースコード（`crates/chat-cli/src/cli/chat/consts.rs`）で定義されており、**ユーザーが変更できません**。

### メッセージサイズ制限

| 項目 | 制限値 | 説明 |
|------|--------|------|
| ユーザーメッセージ | 400,000文字 | 実際のサービス制限は600,000文字 |
| ツールレスポンス | 400,000文字 | 実際のサービス制限は800,000文字 |
| 会話履歴 | 10,000メッセージ | 会話履歴の最大長 |
| カレントディレクトリパス | 256文字 | パスの最大長 |

### 画像関連制限

| 項目 | 制限値 |
|------|--------|
| 1リクエストあたりの最大画像数 | 10枚 |
| 1画像あたりの最大サイズ | 10MB (10,485,760バイト) |

### コンテキストウィンドウ

| 項目 | 値 | 説明 |
|------|-----|------|
| デフォルトコンテキストウィンドウ | 200,000トークン | モデル情報が取得できない場合のデフォルト値 |
| コンテキストファイル最大サイズ | コンテキストウィンドウの75% | 計算式: `context_window_tokens * 3 / 4` |

**計算例**:
- Claude Sonnet 4 (200,000トークン): コンテキストファイル最大 150,000 トークン
- GPT (128,000トークン): コンテキストファイル最大 96,000 トークン

### コンパクション（要約）のデフォルト戦略

| パラメータ | デフォルト値 | 説明 |
|-----------|------------|------|
| `messages_to_exclude` | 0 | 要約から除外するメッセージペア数 |
| `truncate_large_messages` | false | 大きなメッセージの切り詰め |
| `max_message_length` | 400,000文字 | メッセージの最大長 |

**注意**: これらの値は`/compact`コマンドのオプションで一時的に変更できますが、設定ファイルでのデフォルト値変更はできません。

---

## 注意事項

### 型の扱い

- **Boolean**: `true` または `false`
- **Number**: 整数値（例: `1000`, `180000`）
- **String**: 文字列（例: `"my-agent"`, `"t"`）
- **Array**: JSON配列（例: `["**/*.md", "**/*.py"]`）

### 設定の反映

設定を変更した後、Q CLIを再起動する必要がある場合があります：

```bash
q restart
```

### 設定のバックアップ

```bash
# 設定ファイルをバックアップ
cp ~/.local/share/amazon-q/settings.json ~/.local/share/amazon-q/settings.json.backup
```

---

## 参考リンク

- [推奨設定ガイド](../04_best-practices/01_configuration.md)
- [環境変数ガイド](../03_configuration/06_environment-variables.md)
- [設定優先順位](../03_configuration/07_priority-rules.md)
- [ベストプラクティス](../04_best-practices/01_configuration.md)
- [コンテキスト管理ガイド](../08_guides/04_best-practices.md#コンテキストサイズとチューニング)

---

**ドキュメント作成日**: 2025-10-08  
最終更新: %Y->-  
**ソースコード**: `crates/chat-cli/src/database/settings.rs`, `crates/chat-cli/src/cli/chat/consts.rs` (v1.18.0)
