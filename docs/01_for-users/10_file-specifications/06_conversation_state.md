# 会話状態仕様書

最終更新: 2025-10-25  
**対象バージョン**: v1.18.1以降  
**ソースコード**: `crates/chat-cli/src/cli/chat/conversation.rs`

---

## 1. 概要

### 1.1 目的

会話状態（ConversationState）は、Q CLIの会話セッション全体の状態を管理する中核データ構造です。会話履歴、ツール設定、コンテキスト、チェックポイントなど、セッションに関連するすべての情報を保持します。

### 1.2 主要な特徴

| 特徴 | 説明 |
|------|------|
| **永続化** | JSON形式でシリアライズ可能 |
| **履歴管理** | VecDequeによる効率的な履歴操作 |
| **タンジェントモード** | メイン会話を保持したまま別会話を実行 |
| **コンテキスト統合** | スティッキーコンテキストとの連携 |
| **チェックポイント連携** | ファイル変更の追跡と復元 |

### 1.3 ライフサイクル

| フェーズ | 説明 |
|---------|------|
| **作成** | 会話セッション開始時に初期化 |
| **更新** | ユーザー入力とアシスタント応答ごとに更新 |
| **永続化** | セッション終了時にJSON保存 |
| **復元** | セッション再開時にJSONから復元 |

---

## 2. データ構造

### 2.1 ConversationState

会話セッション全体の状態を保持する主要構造体です。

| # | フィールド名 | 型 | 必須 | シリアライズ | 説明 |
|---|------------|-----|------|------------|------|
| 1 | `conversation_id` | String | ✅ | ✅ | ランダム生成される会話ID |
| 2 | `next_message` | Option\<UserMessage\> | ❌ | ✅ | 次に送信するユーザーメッセージ |
| 3 | `history` | VecDeque\<HistoryEntry\> | ✅ | ✅ | 会話履歴（最大10,000エントリ） |
| 4 | `valid_history_range` | (usize, usize) | ✅ | ✅ | バックエンドに送信可能な履歴範囲 |
| 5 | `transcript` | VecDeque\<String\> | ✅ | ✅ | 人間可読な会話記録 |
| 6 | `tools` | HashMap\<ToolOrigin, Vec\<Tool\>\> | ✅ | ✅ | 利用可能なツール |
| 7 | `context_manager` | Option\<ContextManager\> | ❌ | ✅ | コンテキストファイル管理 |
| 8 | `tool_manager` | ToolManager | ✅ | ❌ | ツール・MCP管理（実行時再構築） |
| 9 | `context_message_length` | Option\<usize\> | ❌ | ✅ | コンテキストメッセージ長のキャッシュ |
| 10 | `latest_summary` | Option\<(String, RequestMetadata)\> | ❌ | ✅ | 最新の会話要約（/compactで作成） |
| 11 | `agents` | Agents | ✅ | ❌ | Agent設定（実行時再構築） |
| 12 | `model` | Option\<String\> | ❌ | ✅ | 非推奨（後方互換性のみ、v1.13.3以前） |
| 13 | `model_info` | Option\<ModelInfo\> | ❌ | ✅ | ユーザー選択モデル情報 |
| 14 | `file_line_tracker` | HashMap\<String, FileLineTracker\> | ✅ | ✅ | ファイル変更追跡 |
| 15 | `checkpoint_manager` | Option\<CheckpointManager\> | ❌ | ✅ | チェックポイント管理 |
| 16 | `mcp_enabled` | bool | ✅ | ✅ | MCP有効化フラグ（デフォルト: true） |
| 17 | `tangent_state` | Option\<ConversationCheckpoint\> | ❌ | ✅ | タンジェントモード状態 |

### 2.2 HistoryEntry

会話履歴の1エントリを表す構造体です。

| # | フィールド名 | 型 | 必須 | 説明 |
|---|------------|-----|------|------|
| 1 | `user` | UserMessage | ✅ | ユーザーメッセージ |
| 2 | `assistant` | AssistantMessage | ✅ | アシスタント応答 |
| 3 | `request_metadata` | Option\<RequestMetadata\> | ❌ | リクエストメタデータ（トークン数等） |

### 2.3 ConversationCheckpoint

タンジェントモード用のチェックポイント構造体です。

| # | フィールド名 | 型 | 必須 | 説明 |
|---|------------|-----|------|------|
| 1 | `main_history` | VecDeque\<HistoryEntry\> | ✅ | メイン会話履歴 |
| 2 | `main_next_message` | Option\<UserMessage\> | ❌ | メイン会話の次メッセージ |
| 3 | `main_transcript` | VecDeque\<String\> | ✅ | メイン会話の記録 |
| 4 | `main_latest_summary` | Option\<(String, RequestMetadata)\> | ❌ | メイン会話の要約 |
| 5 | `tangent_start_time` | time::OffsetDateTime | ✅ | タンジェントモード開始時刻（UTC） |

---

## 3. 定数

### 3.1 会話履歴制限

| 定数名 | 値 | 説明 |
|--------|-----|------|
| `MAX_CONVERSATION_STATE_HISTORY_LEN` | 10,000 | 会話履歴の最大エントリ数 |

### 3.2 コンテキストマーカー

| 定数名 | 値 | 説明 |
|--------|-----|------|
| `CONTEXT_ENTRY_START_HEADER` | `"--- CONTEXT ENTRY BEGIN ---\n"` | コンテキストエントリ開始マーカー |
| `CONTEXT_ENTRY_END_HEADER` | `"--- CONTEXT ENTRY END ---\n\n"` | コンテキストエントリ終了マーカー |

---

## 4. 初期化

### 4.1 新規作成

`ConversationState::new()`で新しい会話状態を作成します。

**必須パラメータ**:

| パラメータ | 型 | 説明 |
|-----------|-----|------|
| `conversation_id` | &str | 会話ID（通常はUUID） |
| `agents` | Agents | Agent設定 |
| `tool_config` | HashMap\<String, ToolSpec\> | ツール設定 |
| `tool_manager` | ToolManager | ツールマネージャー |
| `current_model_id` | Option\<String\> | 現在のモデルID |
| `os` | &Os | OS抽象化レイヤー |
| `mcp_enabled` | bool | MCP有効化フラグ |

**初期化処理**:

1. モデル情報の取得（model_idが指定されている場合）
2. ContextManagerの初期化（Agentから）
3. 各フィールドのデフォルト値設定

### 4.2 復元

JSON形式から会話状態を復元します。

**注意事項**:
- `tool_manager`と`agents`は非シリアライズフィールドのため、復元後に再設定が必要
- `model`フィールドは後方互換性のために保持されているが、`model_info`を優先使用

---

## 5. 会話履歴管理

### 5.1 履歴の追加

新しい会話エントリを履歴に追加します。

**制限**:
- 最大エントリ数: 10,000
- 超過時: 最古のエントリから削除（FIFO）

### 5.2 有効範囲管理

`valid_history_range`は、バックエンドに送信可能な履歴範囲を示します。

| フィールド | 説明 |
|-----------|------|
| `start` (inclusive) | 送信開始インデックス |
| `end` (exclusive) | 送信終了インデックス |

**用途**:
- トークン制限内に収めるための範囲調整
- `/compact`による要約後の範囲更新

### 5.3 トランスクリプト

`transcript`は人間可読な会話記録を保持します。

**特徴**:
- ユーザーメッセージは`> `プレフィックス付き
- エラーメッセージも含む
- バックエンドには送信されない（表示専用）

**制限**:
- 最大エントリ数: 10,000
- 超過時: 最古のエントリから削除

---

## 6. タンジェントモード

### 6.1 概要

タンジェントモードは、メイン会話を保持したまま別の会話を実行する機能です。

**使用例**:
- メイン会話の途中で別のトピックを調査
- 実験的な操作を試す
- メイン会話に影響を与えずに情報収集

### 6.2 モード遷移

| 操作 | メソッド | 説明 |
|------|---------|------|
| **開始** | `enter_tangent_mode()` | メイン会話をチェックポイントとして保存 |
| **確認** | `is_in_tangent_mode()` | タンジェントモード中かチェック |
| **期間取得** | `get_tangent_duration_seconds()` | タンジェントモード継続時間（秒） |
| **終了** | `exit_tangent_mode()` | メイン会話を完全復元 |
| **終了（保持）** | `exit_tangent_mode_with_tail()` | 最後のエントリを保持して復元 |

### 6.3 チェックポイント内容

タンジェントモード開始時、以下がチェックポイントとして保存されます：

| 項目 | 説明 |
|------|------|
| `main_history` | メイン会話履歴 |
| `main_next_message` | メイン会話の次メッセージ |
| `main_transcript` | メイン会話のトランスクリプト |
| `main_latest_summary` | メイン会話の要約 |
| `tangent_start_time` | 開始時刻（UTC） |

### 6.4 復元動作

| 復元方法 | 動作 |
|---------|------|
| **完全復元** | タンジェント会話を破棄し、メイン会話を完全復元 |
| **末尾保持復元** | タンジェント会話の最後のエントリをメイン会話に追加 |

---

## 7. コンテキスト管理

### 7.1 ContextManager統合

`context_manager`は、スティッキーコンテキストファイルを管理します。

**初期化**:
- Agent設定から自動初期化
- 最大サイズはモデルのコンテキストウィンドウに応じて計算

**機能**:
- ファイルの追加/削除
- コンテキストサイズの追跡
- コンテキストメッセージの生成

### 7.2 コンテキストメッセージ長キャッシュ

`context_message_length`は、生成されたコンテキストメッセージの長さをキャッシュします。

**目的**:
- トークン計算の高速化
- 不要な再計算の回避

---

## 8. ツール管理

### 8.1 ツール分類

`tools`フィールドは、ToolOriginごとにツールを分類します。

| ToolOrigin | 説明 |
|-----------|------|
| `Builtin` | Q CLI組み込みツール |
| `Custom` | カスタムツール |
| `Mcp` | MCPサーバー提供ツール |

### 8.2 ToolManager

`tool_manager`は、ツールとMCPサーバーの実行時管理を担当します。

**特徴**:
- 非シリアライズ（実行時に再構築）
- MCPサーバーとの通信管理
- ツール実行の調整

---

## 9. モデル管理

### 9.1 モデル情報

| フィールド | 説明 | 状態 |
|-----------|------|------|
| `model` | モデルID文字列 | 非推奨（v1.13.3以前との互換性） |
| `model_info` | ModelInfo構造体 | 推奨 |

### 9.2 ModelInfo

モデルの詳細情報を保持します。

**含まれる情報**:
- モデルID
- コンテキストウィンドウサイズ
- トークン制限
- サポート機能

---

## 10. ファイル変更追跡

### 10.1 FileLineTracker

`file_line_tracker`は、ファイルごとの変更を追跡します。

**用途**:
- Agent変更とユーザー変更の区別
- 変更履歴の管理
- コンフリクト検出

**キー**: ファイルパス（String）  
**値**: FileLineTracker構造体

---

## 11. チェックポイント連携

### 11.1 CheckpointManager統合

`checkpoint_manager`は、ファイル変更のチェックポイント機能を提供します。

**初期化条件**:
- Gitリポジトリ内
- `git`コマンドが利用可能

**機能**:
- ターンごとのチェックポイント作成
- ツール実行後のチェックポイント作成
- 以前の状態への復元

### 11.2 復元時の動作

チェックポイントから復元する際、会話履歴も同時に復元されます。

**復元内容**:
- ファイルシステムの状態
- 会話履歴（history_snapshot）
- 有効範囲（valid_history_range）

---

## 12. 会話要約

### 12.1 latest_summary

`/compact`コマンドで作成された会話要約を保持します。

**構造**:
```rust
Option<(String, RequestMetadata)>
```

| 要素 | 型 | 説明 |
|------|-----|------|
| 要約テキスト | String | 会話の要約 |
| メタデータ | RequestMetadata | トークン数等の情報 |

### 12.2 要約の用途

- 長い会話履歴の圧縮
- トークン制限内への収容
- コンテキストの効率的な伝達

---

## 13. シリアライゼーション

### 13.1 シリアライズ対象

| フィールド | シリアライズ | 理由 |
|-----------|------------|------|
| `conversation_id` | ✅ | 会話識別に必要 |
| `history` | ✅ | 会話継続に必要 |
| `tools` | ✅ | ツール設定の保持 |
| `tool_manager` | ❌ | 実行時に再構築 |
| `agents` | ❌ | 実行時に再構築 |
| `checkpoint_manager` | ✅ | チェックポイント状態の保持 |

### 13.2 後方互換性

| フィールド | 対応 |
|-----------|------|
| `model` | v1.13.3以前との互換性のため保持 |
| `skip_serializing_if` | Noneの場合はシリアライズをスキップ |

---

## 14. エラーハンドリング

### 14.1 履歴制限超過

履歴が10,000エントリを超える場合、最古のエントリから自動削除されます。

**警告**: 削除されたエントリは復元できません。

### 14.2 モデル情報取得失敗

モデル情報の取得に失敗した場合、デフォルト値を使用します。

**ログ**: 警告レベルでログ出力

---

## 15. 使用例

### 15.1 新規会話の開始

```rust
let conversation = ConversationState::new(
    &conversation_id,
    agents,
    tool_config,
    tool_manager,
    Some("anthropic.claude-3-5-sonnet-20241022-v2:0".to_string()),
    &os,
    true, // mcp_enabled
).await;
```

### 15.2 タンジェントモードの使用

```rust
// タンジェントモード開始
conversation.enter_tangent_mode();

// タンジェント会話を実行
// ...

// メイン会話に戻る（最後のエントリを保持）
conversation.exit_tangent_mode_with_tail();
```

### 15.3 会話履歴のクリア

```rust
conversation.clear();
```

### 15.4 タンジェントモード期間の取得

```rust
if let Some(duration) = conversation.get_tangent_duration_seconds() {
    println!("Tangent mode duration: {} seconds", duration);
}
```

---

## 関連ドキュメント

- [CLI Bash History仕様書](./01_cli-bash-history.md) - 会話履歴の詳細構造
- [Checkpoint仕様書](./05_checkpoint.md) - チェックポイント機能の詳細
- [Agent設定ガイド](../03_configuration/03_agent-configuration.md) - Agent設定との連携
- [コンテキスト管理ガイド](../08_guides/README.md) - コンテキスト管理の実践

---

**注意事項**:
- 会話状態は大量のデータを保持する可能性があるため、定期的な`/compact`実行を推奨
- タンジェントモードは実験的な機能であり、予期しない動作が発生する可能性があります
- チェックポイント機能はGitリポジトリ内でのみ使用可能です
- 非シリアライズフィールド（tool_manager、agents）は復元後に再設定が必要です
