# メッセージ構造仕様書

**対象バージョン**: v1.18.1以降  
**ソースコード**: `crates/chat-cli/src/cli/chat/message.rs`

---

## 1. 概要

### 1.1 目的

メッセージ構造は、Q CLIの会話における ユーザーメッセージとアシスタント応答の内部表現を定義します。これらの構造体は、会話履歴の保存、バックエンドとの通信、ツール実行結果の管理に使用されます。

### 1.2 主要な特徴

| 特徴 | 説明 |
|------|------|
| **型安全性** | Rust列挙型による厳密な型定義 |
| **コンテキスト統合** | タイムスタンプと環境情報の自動付与 |
| **ツール連携** | ツール使用と結果の構造化表現 |
| **切り詰め機能** | UTF-8境界を考慮した安全な切り詰め |
| **変換メソッド** | 用途に応じた柔軟な変換 |

### 1.3 メッセージフロー

```
ユーザー入力
    ↓
UserMessage (内部表現)
    ↓
UserInputMessage (バックエンド送信)
    ↓
Backend処理
    ↓
AssistantMessage (内部表現)
    ↓
HistoryEntry (履歴保存)
```

---

## 2. UserMessage

### 2.1 構造体定義

ユーザーからのメッセージを表現する構造体です。

| # | フィールド名 | 型 | 必須 | 説明 |
|---|------------|-----|------|------|
| 1 | `additional_context` | String | ✅ | 追加コンテキスト（空文字列可） |
| 2 | `env_context` | UserEnvContext | ✅ | 環境コンテキスト（OS、CWD） |
| 3 | `content` | UserMessageContent | ✅ | メッセージ内容 |
| 4 | `timestamp` | Option\<DateTime\<FixedOffset\>\> | ❌ | タイムスタンプ（RFC3339形式） |
| 5 | `images` | Option\<Vec\<ImageBlock\>\> | ❌ | 画像データ |

### 2.2 UserMessageContent列挙型

メッセージの内容を表す列挙型です。

| バリアント | フィールド | 説明 |
|-----------|-----------|------|
| **Prompt** | `prompt: String` | ユーザーが入力したプロンプト |
| **CancelledToolUses** | `prompt: Option<String>`<br>`tool_use_results: Vec<ToolUseResult>` | キャンセルされたツール使用<br>（オプションでプロンプト付き） |
| **ToolUseResults** | `tool_use_results: Vec<ToolUseResult>` | ツール実行結果のみ |

### 2.3 コンストラクタ

| メソッド | 用途 | 生成されるバリアント |
|---------|------|-------------------|
| `new_prompt()` | 通常のユーザープロンプト | `Prompt` |
| `new_cancelled_tool_uses()` | ツール使用のキャンセル | `CancelledToolUses` |
| `new_tool_use_results()` | ツール実行結果 | `ToolUseResults` |
| `new_tool_use_results_with_images()` | 画像付きツール実行結果 | `ToolUseResults` |

### 2.4 主要メソッド

| メソッド | 戻り値 | 説明 |
|---------|--------|------|
| `into_history_entry()` | UserInputMessage | 履歴保存用に変換 |
| `into_user_input_message()` | UserInputMessage | バックエンド送信用に変換 |
| `has_tool_use_results()` | bool | ツール結果を含むか |
| `tool_use_results()` | Option\<&[ToolUseResult]\> | ツール結果の参照 |
| `prompt()` | Option\<&str\> | プロンプトの参照 |
| `truncate_safe()` | void | 安全な切り詰め |
| `content_with_context()` | String | コンテキスト付きメッセージ生成 |

---

## 3. AssistantMessage

### 3.1 列挙型定義

アシスタントからの応答を表現する列挙型です。

| バリアント | フィールド | 説明 |
|-----------|-----------|------|
| **Response** | `message_id: Option<String>`<br>`content: String` | 通常応答（ツール使用なし） |
| **ToolUse** | `message_id: Option<String>`<br>`content: String`<br>`tool_uses: Vec<AssistantToolUse>` | ツール使用を含む応答 |

### 3.2 コンストラクタ

| メソッド | 用途 | 生成されるバリアント |
|---------|------|-------------------|
| `new_response()` | 通常応答 | `Response` |
| `new_tool_use()` | ツール使用応答 | `ToolUse` |

### 3.3 主要メソッド

| メソッド | 戻り値 | 説明 |
|---------|--------|------|
| `message_id()` | Option\<&str\> | メッセージIDの参照 |
| `content()` | &str | 応答内容の参照 |
| `tool_uses()` | Option\<&[AssistantToolUse]\> | ツール使用の参照 |

---

## 4. ToolUseResult

### 4.1 構造体定義

ツール実行結果を表現する構造体です。

| # | フィールド名 | 型 | 必須 | 説明 |
|---|------------|-----|------|------|
| 1 | `tool_use_id` | String | ✅ | ツールリクエストID |
| 2 | `content` | Vec\<ToolUseResultBlock\> | ✅ | ツール結果内容 |
| 3 | `status` | ToolResultStatus | ✅ | ツール結果ステータス |

### 4.2 ToolUseResultBlock列挙型

ツール結果の内容を表す列挙型です。

| バリアント | 説明 | 用途 |
|-----------|------|------|
| **Json** | `serde_json::Value` | JSON形式の構造化データ |
| **Text** | `String` | テキスト形式のデータ |

### 4.3 ToolResultStatus

| ステータス | 説明 |
|-----------|------|
| `Success` | ツール実行成功 |
| `Error` | ツール実行エラー |

---

## 5. AssistantToolUse

### 5.1 構造体定義

アシスタントによるツール使用リクエストを表現する構造体です。

| # | フィールド名 | 型 | 必須 | 説明 |
|---|------------|-----|------|------|
| 1 | `id` | String | ✅ | ツールリクエストID |
| 2 | `name` | String | ✅ | モデルに公開されるツール名 |
| 3 | `orig_name` | String | ✅ | 元のツール名 |
| 4 | `args` | serde_json::Value | ✅ | モデルに公開される入力 |
| 5 | `orig_args` | serde_json::Value | ✅ | 元の入力 |

### 5.2 名前と引数の変換

| フィールド | 説明 |
|-----------|------|
| `name` / `orig_name` | ツール名の変換（例: 名前空間の追加/削除） |
| `args` / `orig_args` | 引数の変換（例: スキーマ適合のための変換） |

---

## 6. UserEnvContext

### 6.1 構造体定義

ユーザーの環境コンテキストを表現する構造体です。

| # | フィールド名 | 型 | 必須 | 説明 |
|---|------------|-----|------|------|
| 1 | `env_state` | Option\<EnvState\> | ❌ | 環境状態 |

### 6.2 EnvState

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `operating_system` | Option\<String\> | OS名（例: "linux", "macos", "windows"） |
| `current_working_directory` | Option\<String\> | カレントディレクトリ（最大256文字） |

### 6.3 生成メソッド

| メソッド | 説明 |
|---------|------|
| `generate_new()` | 現在の環境から自動生成 |

**生成内容**:
- OS: `env::consts::OS`から取得
- CWD: `env::current_dir()`から取得（256文字に切り詰め）

---

## 7. 定数

### 7.1 メッセージマーカー

| 定数名 | 値 | 説明 |
|--------|-----|------|
| `USER_ENTRY_START_HEADER` | `"--- USER MESSAGE BEGIN ---\n"` | ユーザーメッセージ開始マーカー |
| `USER_ENTRY_END_HEADER` | `"--- USER MESSAGE END ---\n\n"` | ユーザーメッセージ終了マーカー |
| `CONTEXT_ENTRY_START_HEADER` | `"--- CONTEXT ENTRY BEGIN ---\n"` | コンテキストエントリ開始マーカー |
| `CONTEXT_ENTRY_END_HEADER` | `"--- CONTEXT ENTRY END ---\n\n"` | コンテキストエントリ終了マーカー |

### 7.2 サイズ制限

| 定数名 | 値 | 説明 |
|--------|-----|------|
| `MAX_USER_MESSAGE_SIZE` | 400,000 | ユーザーメッセージ最大サイズ（バイト） |
| `MAX_CURRENT_WORKING_DIRECTORY_LEN` | 256 | CWDパス最大長（バイト） |

---

## 8. コンテキスト付きメッセージ生成

### 8.1 生成フォーマット

`content_with_context()`メソッドは、以下の形式でメッセージを生成します。

```
--- CONTEXT ENTRY BEGIN ---
Current time: {weekday}, {RFC3339 timestamp}
--- CONTEXT ENTRY END ---

{additional_context}

--- USER MESSAGE BEGIN ---
{user prompt}
--- USER MESSAGE END ---
```

### 8.2 生成ルール

| 条件 | 動作 |
|------|------|
| **タイムスタンプあり** | コンテキストエントリとして追加 |
| **追加コンテキストあり** | タイムスタンプの後に追加 |
| **コンテキストなし** | プロンプトのみ（マーカーなし） |
| **コンテキストあり** | プロンプトをマーカーで囲む |

### 8.3 タイムスタンプフォーマット

| 要素 | 形式 | 例 |
|------|------|-----|
| **曜日** | 英語フルネーム | "Monday", "Friday" |
| **日時** | RFC3339（ミリ秒精度） | "2025-10-25T14:53:00.123+09:00" |

---

## 9. 切り詰め機能

### 9.1 切り詰めメソッド

| メソッド | 対象 | 説明 |
|---------|------|------|
| `truncate_safe()` | UserMessageContent | メッセージ内容を切り詰め |
| `truncate_safe_in_place()` | String | 文字列を直接切り詰め |
| `truncate_safe_tool_use_results()` | Vec\<ToolUseResult\> | ツール結果を切り詰め |

### 9.2 切り詰めルール

| ルール | 説明 |
|--------|------|
| **UTF-8境界** | 文字境界を考慮して切り詰め |
| **サフィックス** | `"...content truncated due to length"`を追加 |
| **均等分割** | 複数ツール結果は均等に分割 |

### 9.3 切り詰め対象

| UserMessageContent | 切り詰め方法 |
|-------------------|------------|
| `Prompt` | プロンプト全体を切り詰め |
| `CancelledToolUses` | プロンプト（50%）とツール結果（50%）を切り詰め |
| `ToolUseResults` | ツール結果全体を切り詰め |

---

## 10. 変換メソッド

### 10.1 UserMessage変換

| メソッド | 戻り値 | 用途 | ツール情報 |
|---------|--------|------|-----------|
| `into_history_entry()` | UserInputMessage | 履歴保存 | 含まない |
| `into_user_input_message()` | UserInputMessage | バックエンド送信 | 含む |

### 10.2 変換時の処理

**共通処理**:
1. `content_with_context()`でコンテキスト付きメッセージ生成
2. 環境状態（EnvState）を含める
3. ツール結果を変換（該当する場合）

**差異**:
- `into_history_entry()`: ツール定義を含めない
- `into_user_input_message()`: ツール定義を含める

---

## 11. ツール結果の処理

### 11.1 ツール結果の置換

`replace_content_with_tool_use_results()`メソッドは、ツール結果をプロンプトに変換します。

**処理フロー**:
1. ツール結果を抽出
2. JSON/テキストを文字列に変換
3. スペースで結合
4. 400,000バイトに切り詰め
5. `Prompt`バリアントに置換

**用途**: ツール結果をモデルに送信する際の簡略化

### 11.2 空結果の処理

ツール結果が空の場合、`"<tool result redacted>"`を設定します。

**理由**: バックエンドのバリデーションエラーを回避

---

## 12. 画像サポート

### 12.1 画像フィールド

`UserMessage`は`images`フィールドで画像データをサポートします。

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `images` | Option\<Vec\<ImageBlock\>\> | 画像データのリスト |

### 12.2 画像付きメッセージ

`new_tool_use_results_with_images()`で画像付きツール結果を作成できます。

**用途**: 画像生成ツールの結果を含める

---

## 13. エラーハンドリング

### 13.1 環境情報取得エラー

| エラー | 処理 |
|--------|------|
| **CWD取得失敗** | エラーログを出力し、CWDをNoneに設定 |

### 13.2 JSON変換エラー

| エラー | 処理 |
|--------|------|
| **JSON→文字列失敗** | 警告ログを出力し、切り詰めをスキップ |

---

## 14. 使用例

### 14.1 通常プロンプトの作成

```rust
let timestamp = Some(DateTime::parse_from_rfc3339("2025-10-25T14:53:00+09:00").unwrap());
let message = UserMessage::new_prompt("Hello, Q!".to_string(), timestamp);
```

### 14.2 ツール結果の作成

```rust
let results = vec![
    ToolUseResult {
        tool_use_id: "tool_1".to_string(),
        content: vec![ToolUseResultBlock::Text("Success".to_string())],
        status: ToolResultStatus::Success,
    }
];
let message = UserMessage::new_tool_use_results(results);
```

### 14.3 キャンセルされたツール使用

```rust
let tool_ids = vec!["tool_1", "tool_2"];
let message = UserMessage::new_cancelled_tool_uses(
    Some("Cancel these tools".to_string()),
    tool_ids.iter().map(|s| *s),
    None,
);
```

### 14.4 バックエンド送信用変換

```rust
let tools = HashMap::new(); // ツール定義
let user_input = message.into_user_input_message(
    Some("anthropic.claude-3-5-sonnet-20241022-v2:0".to_string()),
    &tools,
);
```

### 14.5 アシスタント応答の作成

```rust
// 通常応答
let response = AssistantMessage::new_response(
    Some("msg_123".to_string()),
    "Here is the answer.".to_string(),
);

// ツール使用応答
let tool_uses = vec![
    AssistantToolUse {
        id: "tool_1".to_string(),
        name: "fs_read".to_string(),
        orig_name: "fs_read".to_string(),
        args: serde_json::json!({"path": "/tmp/file.txt"}),
        orig_args: serde_json::json!({"path": "/tmp/file.txt"}),
    }
];
let response = AssistantMessage::new_tool_use(
    Some("msg_124".to_string()),
    "Let me read that file.".to_string(),
    tool_uses,
);
```

---

## 関連ドキュメント

- [CLI Bash History仕様書](./01_cli-bash-history.md) - 会話履歴の詳細構造
- [Conversation State仕様書](./06_conversation_state.md) - 会話状態との連携
- [Agent設定ガイド](../03_configuration/03_agent-configuration.md) - Agent設定との連携
- [コンテキスト管理ガイド](../08_guides/README.md) - コンテキスト管理の実践

---

**注意事項**:
- メッセージサイズは400,000バイトに制限されています
- 切り詰めはUTF-8文字境界を考慮して行われます
- ツール結果が空の場合、バリデーションエラーを避けるためプレースホルダーが設定されます
- 環境情報（OS、CWD）は自動的に付与されます
- タイムスタンプはRFC3339形式（ミリ秒精度）で保存されます

---

最終更新: 2025-11-01
