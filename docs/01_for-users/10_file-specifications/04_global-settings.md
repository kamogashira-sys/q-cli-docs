# グローバル設定ファイル (settings.json) 仕様書

[ホーム](../../../README.md) > [ユーザー向けドキュメント](../../README.md) > [ファイル仕様](README.md) > グローバル設定

---

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **ファイル名** | `settings.json` |
| **ファイル形式** | JSON |
| **エンコーディング** | UTF-8 |
| **改行コード** | LF (Unix形式) |
| **JSONスキーマ** | なし（コードで定義） |

### ファイル配置場所

| パス | 説明 |
|------|------|
| `~/.aws/amazonq/settings.json` | グローバル設定ファイル |

---

## 2. 目的と役割

### 目的

グローバル設定ファイルは、Q CLI全体の動作を制御する設定を保存します。

### 主な役割

| 役割 | 説明 |
|------|------|
| **テレメトリ制御** | 使用状況データの収集設定 |
| **Knowledge設定** | ナレッジベース機能の設定 |
| **チャット設定** | チャット機能の動作設定 |
| **API設定** | APIエンドポイントとタイムアウト |
| **MCP設定** | MCPサーバーのタイムアウト設定 |

### 使用場面

- テレメトリを無効化したい
- Knowledge機能をカスタマイズしたい
- チャットの動作を変更したい
- APIタイムアウトを調整したい
- デフォルトモデルを変更したい

---

## 3. ファイル構造

### 基本構成

```json
{
  "設定キー": 設定値
}
```

**特徴**: フラットなキー・バリューペア構造

### 完全な構成例

```json
{
  "telemetry.enabled": true,
  "codeWhisperer.shareCodeWhispererContentWithAWS": false,
  "chat.enableKnowledge": true,
  "knowledge.maxFiles": 1000,
  "knowledge.chunkSize": 1000,
  "knowledge.chunkOverlap": 200,
  "knowledge.indexType": "bm25",
  "chat.enableThinking": false,
  "chat.greeting.enabled": true,
  "chat.defaultModel": "anthropic.claude-3-5-sonnet-20241022-v2:0",
  "chat.defaultAgent": "my-agent",
  "chat.enableNotifications": false,
  "chat.disableMarkdownRendering": false,
  "chat.enableHistoryHints": true,
  "chat.enableTodoList": false,
  "chat.enableCheckpoint": false,
  "chat.enableDelegate": false,
  "api.timeout": 300,
  "mcp.initTimeout": 30000,
  "mcp.noInteractiveTimeout": 5000
}
```

---

## 4. 設定項目仕様

### 4.1 テレメトリ設定（3項目）

| 設定キー | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `telemetry.enabled` | boolean | true | テレメトリ収集の有効/無効 |
| `telemetryClientId` | string | - | レガシークライアントID（内部使用） |
| `codeWhisperer.shareCodeWhispererContentWithAWS` | boolean | - | コンテンツをAWSと共有 |

**telemetry.enabled**

テレメトリデータの収集を制御します。

| 値 | 説明 |
|----|------|
| `true` | テレメトリ収集を有効化（デフォルト） |
| `false` | テレメトリ収集を無効化 |

**例**
```json
{
  "telemetry.enabled": false
}
```

**codeWhisperer.shareCodeWhispererContentWithAWS**

コンテンツ（質問、コード、応答）をサービス改善に使用することを許可します。

| 値 | 説明 |
|----|------|
| `true` | コンテンツ共有を許可 |
| `false` | コンテンツ共有を拒否 |

**注意**: Pro/Enterpriseプランでは、この設定に関わらずコンテンツは共有されません。

### 4.2 Knowledge設定（8項目）

| 設定キー | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `chat.enableKnowledge` | boolean | - | Knowledge機能の有効/無効 |
| `knowledge.defaultIncludePatterns` | array | - | デフォルト包含パターン |
| `knowledge.defaultExcludePatterns` | array | - | デフォルト除外パターン |
| `knowledge.maxFiles` | number | - | 最大ファイル数 |
| `knowledge.chunkSize` | number | - | テキストチャンクサイズ |
| `knowledge.chunkOverlap` | number | - | チャンク間のオーバーラップ |
| `knowledge.indexType` | string | - | インデックスタイプ |

**chat.enableKnowledge**

Knowledge機能（ナレッジベース）を有効化します。

```json
{
  "chat.enableKnowledge": true
}
```

**knowledge.maxFiles**

インデックス化する最大ファイル数を指定します。

```json
{
  "knowledge.maxFiles": 1000
}
```

**knowledge.chunkSize**

テキストを分割するチャンクのサイズ（文字数）を指定します。

```json
{
  "knowledge.chunkSize": 1000
}
```

**knowledge.chunkOverlap**

チャンク間のオーバーラップ（文字数）を指定します。

```json
{
  "knowledge.chunkOverlap": 200
}
```

**knowledge.indexType**

使用するインデックスタイプを指定します。

| 値 | 説明 |
|----|------|
| `"bm25"` | BM25アルゴリズム |
| その他 | 実装依存 |

```json
{
  "knowledge.indexType": "bm25"
}
```

### 4.3 チャット設定（15項目）

| 設定キー | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `chat.enableThinking` | boolean | - | Thinking機能 |
| `chat.skimCommandKey` | char | - | ファジー検索キー |
| `chat.autocompletionKey` | char | - | オートコンプリートキー |
| `chat.enableTangentMode` | boolean | - | Tangentモード |
| `chat.tangentModeKey` | char | - | Tangentモードキー |
| `chat.delegateModeKey` | char | - | Delegateモードキー |
| `chat.greeting.enabled` | boolean | - | 挨拶メッセージ表示 |
| `chat.editMode` | boolean | - | 編集モード |
| `chat.enableNotifications` | boolean | - | デスクトップ通知 |
| `chat.defaultModel` | string | - | デフォルトAIモデル |
| `chat.disableMarkdownRendering` | boolean | - | Markdown無効化 |
| `chat.defaultAgent` | string | - | デフォルトAgent |
| `chat.disableAutoCompaction` | boolean | - | 自動要約無効化 |
| `chat.enableHistoryHints` | boolean | - | 履歴ヒント表示 |
| `chat.enableTodoList` | boolean | - | TODOリスト機能 |
| `chat.enableCheckpoint` | boolean | - | チェックポイント機能 |
| `chat.enableContextUsageIndicator` | boolean | - | コンテキスト使用率表示 |
| `chat.enableDelegate` | boolean | - | Delegate機能 |

**chat.enableThinking**

複雑な推論のためのThinking機能を有効化します。

```json
{
  "chat.enableThinking": true
}
```

**chat.greeting.enabled**

チャット開始時の挨拶メッセージを表示します。

```json
{
  "chat.greeting.enabled": true
}
```

**chat.defaultModel**

デフォルトで使用するAIモデルを指定します。

```json
{
  "chat.defaultModel": "anthropic.claude-3-5-sonnet-20241022-v2:0"
}
```

**chat.defaultAgent**

デフォルトで使用するAgent設定を指定します。

```json
{
  "chat.defaultAgent": "my-agent"
}
```

**chat.enableNotifications**

デスクトップ通知を有効化します。

```json
{
  "chat.enableNotifications": true
}
```

**chat.disableMarkdownRendering**

Markdownレンダリングを無効化します。

```json
{
  "chat.disableMarkdownRendering": false
}
```

**chat.disableAutoCompaction**

会話の自動要約を無効化します。

```json
{
  "chat.disableAutoCompaction": false
}
```

**chat.enableHistoryHints**

会話履歴のヒントを表示します。

```json
{
  "chat.enableHistoryHints": true
}
```

**chat.enableTodoList**

TODOリスト機能を有効化します。

```json
{
  "chat.enableTodoList": true
}
```

**chat.enableCheckpoint**

チェックポイント機能を有効化します。

```json
{
  "chat.enableCheckpoint": true
}
```

**chat.enableContextUsageIndicator**

プロンプトにコンテキスト使用率を表示します。

```json
{
  "chat.enableContextUsageIndicator": true
}
```

**chat.enableDelegate**

サブエージェント管理のためのDelegate機能を有効化します。

```json
{
  "chat.enableDelegate": true
}
```

### 4.4 API設定（3項目）

| 設定キー | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `api.timeout` | number | - | APIリクエストタイムアウト（秒） |
| `api.codewhisperer.service` | string | - | CodeWhispererエンドポイント |
| `api.q.service` | string | - | Qサービスエンドポイント |

**api.timeout**

APIリクエストのタイムアウトを秒単位で指定します。

```json
{
  "api.timeout": 300
}
```

**api.codewhisperer.service**

CodeWhispererサービスのエンドポイントURLを指定します。

```json
{
  "api.codewhisperer.service": "https://codewhisperer.us-east-1.amazonaws.com"
}
```

**api.q.service**

Qサービスのエンドポイントを指定します。

```json
{
  "api.q.service": "https://q.us-east-1.amazonaws.com"
}
```

### 4.5 MCP設定（3項目）

| 設定キー | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `mcp.initTimeout` | number | - | MCP初期化タイムアウト（ms） |
| `mcp.noInteractiveTimeout` | number | - | 非対話MCPタイムアウト（ms） |
| `mcp.loadedBefore` | boolean | - | MCP読み込み履歴（内部使用） |

**mcp.initTimeout**

MCPサーバー初期化のタイムアウトをミリ秒で指定します。

```json
{
  "mcp.initTimeout": 30000
}
```

**mcp.noInteractiveTimeout**

非対話的なMCP操作のタイムアウトをミリ秒で指定します。

```json
{
  "mcp.noInteractiveTimeout": 5000
}
```

### 4.6 Introspect設定（1項目）

| 設定キー | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `introspect.tangentMode` | boolean | - | Introspect質問で自動的にTangentモードに入る |

**introspect.tangentMode**

Introspect質問で自動的にTangentモードに入ります。

```json
{
  "introspect.tangentMode": true
}
```

---

## 5. ファイル操作

### 5.1 読み込み処理

**処理フロー**

1. ファイル存在確認
2. 存在しない場合: 空のJSONファイルを作成
3. ファイル読み込み
4. JSONパース
5. メモリに保持

**ソースコード参照**
- ファイル: `crates/chat-cli/src/database/settings.rs`
- 関数: `Settings::new()`

### 5.2 書き込み処理

**処理フロー**

1. 設定値の更新
2. JSON生成
3. ファイルロック取得
4. ファイル書き込み
5. ファイルロック解放

**ソースコード参照**
- ファイル: `crates/chat-cli/src/database/settings.rs`
- 関数: `Settings::set()`

### 5.3 コマンドライン操作

**設定の取得**
```bash
q settings <key>
```

**設定の更新**
```bash
q settings <key> <value>
```

**設定の削除**
```bash
q settings --delete <key>
```

**全設定の表示**
```bash
q settings list
```

**設定ファイルを開く**
```bash
q settings open
```

---

## 6. 使用例

### 6.1 テレメトリを無効化

```bash
q settings telemetry.enabled false
```

または直接編集：
```json
{
  "telemetry.enabled": false
}
```

### 6.2 Knowledge機能を有効化

```bash
q settings chat.enableKnowledge true
q settings knowledge.maxFiles 1000
q settings knowledge.indexType bm25
```

### 6.3 デフォルトモデルを変更

```bash
q settings chat.defaultModel "anthropic.claude-3-5-sonnet-20241022-v2:0"
```

### 6.4 デフォルトAgentを設定

```bash
q settings chat.defaultAgent "my-project-agent"
```

### 6.5 APIタイムアウトを延長

```bash
q settings api.timeout 600
```

### 6.6 複数設定の一括設定

```json
{
  "telemetry.enabled": false,
  "chat.enableKnowledge": true,
  "knowledge.maxFiles": 1000,
  "chat.defaultModel": "anthropic.claude-3-5-sonnet-20241022-v2:0",
  "chat.enableNotifications": true,
  "api.timeout": 300
}
```

---

## 7. セキュリティとプライバシー

### セキュリティ考慮事項

| 項目 | 説明 |
|------|------|
| **テレメトリ** | `telemetry.enabled`で制御可能 |
| **コンテンツ共有** | `codeWhisperer.shareCodeWhispererContentWithAWS`で制御 |
| **APIエンドポイント** | カスタムエンドポイントを指定可能 |
| **ファイルアクセス** | 設定ファイルは`~/.aws/amazonq/`に保存 |

### プライバシー保護

1. **テレメトリ無効化**
   ```bash
   q settings telemetry.enabled false
   ```

2. **コンテンツ共有の拒否**
   ```bash
   q settings codeWhisperer.shareCodeWhispererContentWithAWS false
   ```

3. **Pro/Enterpriseプラン**
   - コンテンツは自動的に保護される
   - サービス改善に使用されない

---

## 8. ライフサイクル

### 作成

**自動作成**
- Q CLI初回起動時に自動作成

**手動作成**
```bash
mkdir -p ~/.aws/amazonq
echo '{}' > ~/.aws/amazonq/settings.json
```

### 読み込み

**読み込みタイミング**
- Q CLI起動時
- 設定変更時

### 更新

**コマンドライン**
```bash
q settings <key> <value>
```

**直接編集**
```bash
q settings open
# または
$EDITOR ~/.aws/amazonq/settings.json
```

### 削除

**特定の設定を削除**
```bash
q settings --delete <key>
```

**ファイル全体を削除**
```bash
rm ~/.aws/amazonq/settings.json
```

---

## 9. トラブルシューティング

### よくある問題

#### 問題1: 設定が反映されない

**症状**
```
設定を変更したが動作が変わらない
```

**解決方法**
1. Q CLIを再起動
2. 設定キーのスペルを確認
3. 設定値の型を確認（boolean/number/string）

#### 問題2: 設定ファイルが壊れた

**症状**
```
Failed to parse settings.json
```

**解決方法**
1. JSONリンターで検証（`jq . settings.json`）
2. 構文エラーを修正
3. バックアップから復元
4. ファイルを削除して再作成

#### 問題3: 設定が見つからない

**症状**
```
No value associated with <key>
```

**解決方法**
1. 設定キーのスペルを確認
2. `q settings list`で全設定を確認
3. デフォルト値が使用されている可能性

#### 問題4: 設定ファイルを開けない

**症状**
```
The EDITOR environment variable is not set
```

**解決方法**
```bash
export EDITOR=vim
q settings open
```

---

## 10. 関連ファイル

### 関連する設定ファイル

| ファイル | 関係 |
|---------|------|
| `agent.json` | Agent設定（設定より優先度が高い） |
| `mcp.json` | MCP設定（Agent設定に統合推奨） |

### 設定の優先順位

1. コマンドライン引数
2. 環境変数
3. Agent設定
4. グローバル設定（settings.json）
5. デフォルト値

### 関連するドキュメント

- [グローバル設定ガイド](../03_configuration/02_global-settings.md)
- [設定優先順位](../03_configuration/07_priority-rules.md)
- [Agent設定仕様書](02_agent-configuration.md)

---

## 11. バージョン履歴

| バージョン | 変更内容 | 日付 |
|----------|---------|------|
| v1 | 初版リリース | - |

**注意**: バージョン履歴の詳細は公式リポジトリのコミット履歴を参照してください。

---

## 12. 参考資料

### ソースコード

| ファイル | 説明 |
|---------|------|
| `crates/chat-cli/src/database/settings.rs` | Setting列挙型定義、Settings構造体 |
| `crates/chat-cli/src/cli/settings.rs` | 設定コマンド実装 |

**コミットハッシュ**: `63278298f451fd57ee439a2614bbac6a62da3870`  
**コミット日時**: 2025-10-13 12:44:25 -0700

### 公式ドキュメント

- [Amazon Q Developer CLI 公式リポジトリ](https://github.com/aws/amazon-q-developer-cli)

---

最終更新: 2025-10-25  
**ドキュメントバージョン**: 1.0
