# Amazon Q CLI 設定項目完全リファレンス

**作成日**: 2025-10-08  
**ソースコード**: `crates/chat-cli/src/database/settings.rs`  
**対象バージョン**: v1.17.0以降

## 概要

このドキュメントは、Amazon Q CLIの全設定項目を網羅的にリストアップしたリファレンスです。ソースコードから直接抽出した正確な情報を提供します。

**更新履歴**:
- 2025-10-08: 初版作成（38項目と記載したが誤り）
- 2025-10-08 18:07 JST: 正確な項目数に修正（35項目）、項目36-38を削除
- 2025-10-09 13:06 JST: 実装確認により33項目に修正、DelegateModeKey追加、項目番号調整
- 2025-10-09 16:30 JST: 再度実装確認により35項目に修正（OldClientId、ShareCodeWhispererContentを復元）

---

## 設定項目一覧（全35項目）

| # | 設定キー | 型 | 説明 | カテゴリ |
|---|---------|-----|------|---------|
| 1 | `telemetry.enabled` | Boolean | テレメトリ収集の有効/無効 | テレメトリ |
| 2 | `telemetryClientId` | String | テレメトリ用クライアント識別子（新形式） | テレメトリ |
| 3 | `oldClientId` | String | テレメトリ用レガシークライアント識別子（旧形式） | テレメトリ |
| 4 | `codeWhisperer.shareCodeWhispererContentWithAWS` | Boolean | CodeWhispererサービスとのコンテンツ共有 | CodeWhisperer |
| 5 | `shareCodeWhispererContent` | Boolean | CodeWhispererコンテンツ共有（レガシー設定） | CodeWhisperer |
| 6 | `chat.enableThinking` | Boolean | 複雑な推論のためのThinkingツール有効化 | 実験的機能 |
| 7 | `chat.enableKnowledge` | Boolean | Knowledge Base機能の有効化 | 実験的機能 |
| 8 | `knowledge.defaultIncludePatterns` | Array | Knowledge Baseに含めるデフォルトファイルパターン | Knowledge |
| 9 | `knowledge.defaultExcludePatterns` | Array | Knowledge Baseから除外するデフォルトファイルパターン | Knowledge |
| 10 | `knowledge.maxFiles` | Number | Knowledgeインデックス作成の最大ファイル数 | Knowledge |
| 11 | `knowledge.chunkSize` | Number | Knowledge処理のテキストチャンクサイズ | Knowledge |
| 12 | `knowledge.chunkOverlap` | Number | テキストチャンク間のオーバーラップ | Knowledge |
| 13 | `knowledge.indexType` | String | 使用するKnowledgeインデックスのタイプ | Knowledge |
| 14 | `chat.skimCommandKey` | String (1文字) | ファジー検索コマンドのキーバインド | キーバインド |
| 15 | `chat.autocompletionKey` | String (1文字) | オートコンプリートヒント受け入れのキーバインド | キーバインド |
| 16 | `chat.enableTangentMode` | Boolean | Tangentモード機能の有効化 | 実験的機能 |
| 17 | `chat.tangentModeKey` | String (1文字) | Tangentモードトグルのキーバインド | キーバインド |
| 18 | `chat.delegateModeKey` | String (1文字) | Delegateコマンドのキーバインド | キーバインド |
| 19 | `introspect.tangentMode` | Boolean | introspectクエリで自動的にTangentモードに入る | Introspect |
| 20 | `chat.greeting.enabled` | Boolean | チャット開始時の挨拶メッセージ表示 | チャットUI |
| 21 | `api.timeout` | Number | APIリクエストのタイムアウト（秒） | API |
| 22 | `chat.editMode` | Boolean | チャットインターフェースの編集モード有効化 | チャットUI |
| 23 | `chat.enableNotifications` | Boolean | デスクトップ通知の有効化 | チャットUI |
| 24 | `api.codewhisperer.service` | String | CodeWhispererサービスエンドポイントURL | API |
| 25 | `api.q.service` | String | QサービスエンドポイントURL | API |
| 26 | `mcp.initTimeout` | Number | MCPサーバー初期化タイムアウト | MCP |
| 27 | `mcp.noInteractiveTimeout` | Number | 非対話型MCPタイムアウト | MCP |
| 28 | `mcp.loadedBefore` | Boolean | 以前にロードされたMCPサーバーの追跡 | MCP |
| 29 | `chat.enableContextUsageIndicator` | Boolean | プロンプトにコンテキスト使用率パーセンテージ表示 | 実験的機能 |
| 30 | `chat.defaultModel` | String | 会話のデフォルトAIモデル | チャット |
| 31 | `chat.disableMarkdownRendering` | Boolean | チャットでのMarkdownフォーマット無効化 | チャットUI |
| 32 | `chat.defaultAgent` | String | デフォルトAgent設定 | Agent |
| 33 | `chat.disableAutoCompaction` | Boolean | 自動会話要約の無効化 | チャット |
| 34 | `chat.enableHistoryHints` | Boolean | 会話履歴ヒントの表示 | チャットUI |
| 35 | `chat.enableTodoList` | Boolean | TODOリスト機能の有効化 | 実験的機能 |
| 36 | `chat.enableCheckpoint` | Boolean | チェックポイント機能の有効化 | 実験的機能 |
| 37 | `chat.enableDelegate` | Boolean | サブエージェント管理のためのDelegateツール有効化 | 実験的機能 |

---

## カテゴリ別設定項目

### テレメトリ設定

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `telemetry.enabled` | Boolean | テレメトリ収集の有効/無効 |
| `telemetryClientId` | String | クライアント識別子（新形式） |
| `oldClientId` | String | レガシークライアント識別子（旧形式） |

### CodeWhisperer設定

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `codeWhisperer.shareCodeWhispererContentWithAWS` | Boolean | コンテンツ共有（新形式） |
| `shareCodeWhispererContent` | Boolean | コンテンツ共有（レガシー） |

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
q settings all
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

- [推奨設定ガイド](../best-practices/configuration.md)
- [環境変数ガイド](../configuration/environment-variables.md)
- [設定優先順位](../configuration/priority-rules.md)
- [ベストプラクティス](../best-practices/configuration.md)

---

**ドキュメント作成日**: 2025-10-08  
**最終更新**: 2025-10-08  
**ソースコード**: `crates/chat-cli/src/database/settings.rs` (v1.17.0)
