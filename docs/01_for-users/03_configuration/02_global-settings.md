[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [設定ガイド](README.md) > 03 Global Settings

---

# グローバル設定

最終更新: %Y->-  
**対象バージョン**: v1.18.0以降

すべてのQ CLIセッションに適用される基本設定について説明します。

## 📋 目次

- [設定ファイルの場所](#設定ファイルの場所)
- [設定項目一覧](#設定項目一覧)
- [カテゴリ別設定](#カテゴリ別設定)
- [設定例](#設定例)
- [設定の変更方法](#設定の変更方法)

---

## 設定ファイルの場所

### macOS/Linux
```
~/.local/share/amazon-q/settings.json
```

### Windows
```
%USERPROFILE%\.config\amazonq\settings.json
```

---

## 設定項目一覧

> **💡 このセクションについて**
> 
> この設定項目一覧は、Q CLIのソースコード調査に基づいています。
> 
> **出典**: [ソースコード](https://github.com/aws/amazon-q-developer-cli/blob/main/crates/chat-cli/src/database/settings.rs) - `SettingKey` enumの定義
> 
> **検証方法**:
> - ソースコードで全設定キーを確認
> - 各設定項目の型と説明を確認
> - デフォルト値をソースコードで確認
> 
> **関連ドキュメント**: [設定リファレンス](../07_reference/03_settings-reference.md) - 全35項目の詳細説明

Q CLIは**35項目**の設定をサポートしています。

| # | 設定キー | 型 | 説明 |
|---|---------|-----|------|
| 1 | `telemetry.enabled` | boolean | テレメトリ収集の有効/無効 |
| 2 | `telemetryClientId` | string | テレメトリ用レガシークライアント識別子 |
| 3 | `codeWhisperer.shareCodeWhispererContentWithAWS` | boolean | CodeWhispererサービスとのコンテンツ共有 |
| 4 | `chat.enableThinking` | boolean | 複雑な推論のためのThinkingツール有効化 |
| 5 | `chat.enableKnowledge` | boolean | Knowledge機能の有効化 |
| 6 | `knowledge.defaultIncludePatterns` | array | Knowledgeに含めるデフォルトファイルパターン |
| 7 | `knowledge.defaultExcludePatterns` | array | Knowledgeから除外するデフォルトファイルパターン |
| 8 | `knowledge.maxFiles` | number | Knowledgeインデックス化の最大ファイル数 |
| 9 | `knowledge.chunkSize` | number | Knowledge処理のテキストチャンクサイズ |
| 10 | `knowledge.chunkOverlap` | number | テキストチャンク間のオーバーラップ |
| 11 | `knowledge.indexType` | string | 使用するKnowledgeインデックスのタイプ |
| 12 | `chat.skimCommandKey` | character | ファジー検索コマンドのキーバインド |
| 13 | `chat.autocompletionKey` | character | オートコンプリートヒント受け入れのキーバインド |
| 14 | `chat.enableTangentMode` | boolean | Tangentモード機能の有効化 |
| 15 | `chat.tangentModeKey` | character | Tangentモード切り替えのキーバインド |
| 16 | `chat.delegateModeKey` | character | Delegateコマンドのキーバインド |
| 17 | `introspect.tangentMode` | boolean | Introspect質問時の自動Tangentモード |
| 18 | `chat.greeting.enabled` | boolean | チャット開始時の挨拶メッセージ表示 |
| 19 | `api.timeout` | number | APIリクエストタイムアウト（秒） |
| 20 | `chat.editMode` | boolean | チャットインターフェースの編集モード有効化 |
| 21 | `chat.enableNotifications` | boolean | デスクトップ通知の有効化 |
| 22 | `api.codewhisperer.service` | string | CodeWhispererサービスエンドポイントURL |
| 23 | `api.q.service` | string | QサービスエンドポイントURL |
| 24 | `mcp.initTimeout` | number | MCPサーバー初期化タイムアウト |
| 25 | `mcp.noInteractiveTimeout` | number | 非インタラクティブMCPタイムアウト |
| 26 | `mcp.loadedBefore` | boolean | 以前にロードされたMCPサーバーの追跡 |
| 27 | `chat.enableContextUsageIndicator` | boolean | プロンプトでのコンテキスト使用率表示 |
| 28 | `chat.defaultModel` | string | 会話のデフォルトAIモデル |
| 29 | `chat.disableMarkdownRendering` | boolean | チャットでのMarkdownフォーマット無効化 |
| 30 | `chat.defaultAgent` | string | デフォルトAgent設定 |
| 31 | `chat.disableAutoCompaction` | boolean | 自動会話要約の無効化 |
| 32 | `chat.enableHistoryHints` | boolean | 会話履歴ヒントの表示 |
| 33 | `chat.enableTodoList` | boolean | TODOリスト機能の有効化 |
| 34 | `chat.enableCheckpoint` | boolean | Checkpoint機能の有効化 |
| 35 | `chat.enableDelegate` | boolean | サブエージェント管理のためのDelegateツール有効化 |

---

## カテゴリ別設定

### 1. テレメトリ設定

使用状況データの収集に関する設定です。

```json
{
  "telemetry.enabled": false,
  "telemetryClientId": "your-client-id",
  "codeWhisperer.shareCodeWhispererContentWithAWS": false
}
```

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `telemetry.enabled` | boolean | テレメトリ収集の有効/無効 |
| `telemetryClientId` | string | レガシークライアント識別子 |
| `codeWhisperer.shareCodeWhispererContentWithAWS` | boolean | CodeWhispererとのコンテンツ共有 |

### 2. チャット設定

チャットインターフェースの動作に関する設定です。

```json
{
  "chat.enableThinking": true,
  "chat.enableKnowledge": false,
  "chat.greeting.enabled": true,
  "chat.editMode": false,
  "chat.enableNotifications": false,
  "chat.defaultModel": "anthropic.claude-3-5-sonnet-20241022-v2:0",
  "chat.disableMarkdownRendering": false,
  "chat.defaultAgent": "default",
  "chat.disableAutoCompaction": false,
  "chat.enableHistoryHints": true,
  "chat.enableTodoList": true,
  "chat.enableCheckpoint": true,
  "chat.enableDelegate": true,
  "chat.enableTangentMode": true,
  "chat.enableContextUsageIndicator": true
}
```

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `chat.enableThinking` | boolean | Thinkingツールの有効化 |
| `chat.enableKnowledge` | boolean | Knowledge機能の有効化 |
| `chat.greeting.enabled` | boolean | 挨拶メッセージの表示 |
| `chat.editMode` | boolean | 編集モードの有効化 |
| `chat.enableNotifications` | boolean | デスクトップ通知の有効化 |
| `chat.defaultModel` | string | デフォルトAIモデル |
| `chat.disableMarkdownRendering` | boolean | Markdownレンダリングの無効化 |
| `chat.defaultAgent` | string | デフォルトAgent |
| `chat.disableAutoCompaction` | boolean | 自動要約の無効化 |
| `chat.enableHistoryHints` | boolean | 履歴ヒントの表示 |
| `chat.enableTodoList` | boolean | TODOリスト機能 |
| `chat.enableCheckpoint` | boolean | Checkpoint機能 |
| `chat.enableDelegate` | boolean | Delegateツール |
| `chat.enableTangentMode` | boolean | Tangentモード |
| `chat.enableContextUsageIndicator` | boolean | コンテキスト使用率表示 |

### 3. Knowledge設定

Knowledge機能に関する設定です。

```json
{
  "knowledge.defaultIncludePatterns": ["**/*.md", "**/*.py", "**/*.js"],
  "knowledge.defaultExcludePatterns": ["**/node_modules/**", "**/.git/**"],
  "knowledge.maxFiles": 1000,
  "knowledge.chunkSize": 1000,
  "knowledge.chunkOverlap": 200,
  "knowledge.indexType": "bm25"
}
```

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `knowledge.defaultIncludePatterns` | array | 含めるファイルパターン |
| `knowledge.defaultExcludePatterns` | array | 除外するファイルパターン |
| `knowledge.maxFiles` | number | 最大ファイル数 |
| `knowledge.chunkSize` | number | チャンクサイズ |
| `knowledge.chunkOverlap` | number | チャンクオーバーラップ |
| `knowledge.indexType` | string | インデックスタイプ（bm25/vector） |

### 4. キーバインド設定

キーボードショートカットに関する設定です。

```json
{
  "chat.skimCommandKey": "r",
  "chat.autocompletionKey": "→",
  "chat.tangentModeKey": "t",
  "chat.delegateModeKey": "d"
}
```

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `chat.skimCommandKey` | character | ファジー検索キー |
| `chat.autocompletionKey` | character | オートコンプリートキー |
| `chat.tangentModeKey` | character | Tangentモードキー |
| `chat.delegateModeKey` | character | Delegateモードキー |

### 5. API設定

APIエンドポイントとタイムアウトに関する設定です。

```json
{
  "api.timeout": 30,
  "api.codewhisperer.service": "https://codewhisperer.us-east-1.amazonaws.com",
  "api.q.service": "https://q.us-east-1.amazonaws.com"
}
```

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `api.timeout` | number | タイムアウト（秒） |
| `api.codewhisperer.service` | string | CodeWhispererエンドポイント |
| `api.q.service` | string | Qサービスエンドポイント |

### 6. MCP設定

MCPサーバーに関する設定です。

```json
{
  "mcp.initTimeout": 30000,
  "mcp.noInteractiveTimeout": 5000,
  "mcp.loadedBefore": false
}
```

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `mcp.initTimeout` | number | 初期化タイムアウト（ミリ秒） |
| `mcp.noInteractiveTimeout` | number | 非インタラクティブタイムアウト（ミリ秒） |
| `mcp.loadedBefore` | boolean | ロード済みサーバーの追跡 |

### 7. Introspect設定

Introspect機能に関する設定です。

```json
{
  "introspect.tangentMode": false
}
```

| 設定キー | 型 | 説明 |
|---------|-----|------|
| `introspect.tangentMode` | boolean | 自動Tangentモード |

---

## 設定例

### 最小構成
```json
{
  "telemetry.enabled": false
}
```

### 推奨構成
```json
{
  "telemetry.enabled": false,
  "chat.enableThinking": true,
  "chat.enableKnowledge": true,
  "chat.greeting.enabled": true,
  "chat.defaultAgent": "default",
  "knowledge.indexType": "bm25"
}
```

### パフォーマンス重視
```json
{
  "chat.disableMarkdownRendering": true,
  "chat.disableAutoCompaction": true,
  "knowledge.maxFiles": 500,
  "knowledge.chunkSize": 500,
  "api.timeout": 15
}
```

### 開発者向け
```json
{
  "telemetry.enabled": false,
  "chat.enableThinking": true,
  "chat.enableKnowledge": true,
  "chat.enableTodoList": true,
  "chat.enableCheckpoint": true,
  "chat.enableDelegate": true,
  "chat.editMode": true,
  "knowledge.defaultIncludePatterns": [
    "**/*.md",
    "**/*.py",
    "**/*.js",
    "**/*.ts",
    "**/*.java",
    "**/*.go"
  ],
  "knowledge.indexType": "bm25"
}
```

---

## 設定の変更方法

### 方法1: エディタで直接編集
```bash
q settings open
```

### 方法2: コマンドで設定
```bash
# 特定の設定を変更
q settings chat.enableThinking true

# 設定を確認
q settings chat.enableThinking

# 設定を削除
q settings --delete chat.enableThinking
```

### 方法3: すべての設定を表示
```bash
q settings list
```

### 方法4: 手動編集
```bash
# ファイルを直接編集
vim ~/.local/share/amazon-q/settings.json
```

---

## 📚 関連ドキュメント

- [設定システム概要](01_overview.md)
- [設定項目完全リファレンス](../07_reference/03_settings-reference.md)
- [設定例集](08_examples.md)
- [設定優先順位ガイド](07_priority-rules.md)

---

## ⚠️ 注意事項

1. **設定の型**: 各設定項目は指定された型（boolean、string、number、array、character）で設定してください
2. **JSON形式**: settings.jsonは有効なJSON形式である必要があります
3. **再起動不要**: ほとんどの設定は即座に反映されますが、一部の設定は再起動が必要です
4. **デフォルト値**: 設定を削除すると、デフォルト値が使用されます

---

最終更新: %Y->-
---

**関連トピック**:
- [設定優先順位ガイド](07_priority-rules.md)
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)

## 関連ドキュメント

- [テレメトリー設定](../03_configuration/05_telemetry.md) - テレメトリー設定の詳細
