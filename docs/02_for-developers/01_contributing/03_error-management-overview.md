[ホーム](../../README.md) > [開発者ガイド](../README.md) > [コントリビューション](README.md) > 05 エラー管理概要

# エラー管理概要

**対象バージョン**: v1.17.0以降  
**対象読者**: 開発者、コントリビューター

---

## 📋 概要

このドキュメントは、Q CLIにおけるエラーメッセージの管理方法を説明します。新しい機能を追加する際や、既存のエラーメッセージを修正する際の参考にしてください。

---

## 🏗️ エラーハンドリングの構造

### 使用しているクレート

Q CLIは以下のRustクレートを使用してエラーハンドリングを実装しています：

1. **thiserror** - カスタムエラー型の定義
2. **eyre** - エラーコンテキストの追加と伝播

```toml
# Cargo.toml
[dependencies]
thiserror = "..."
eyre = "..."
color-eyre = "..."  # エラー表示の改善
```

---

## 📂 エラー型の配置

Q CLIのエラー型は機能ごとに分散して定義されています：

### 主要なエラー型

| エラー型 | ファイルパス | 用途 |
|---------|------------|------|
| `ApiClientError` | `crates/chat-cli/src/api_client/error.rs` | API呼び出し関連 |
| `AuthError` | `crates/chat-cli/src/auth/mod.rs` | 認証関連 |
| `ChatError` | `crates/chat-cli/src/cli/chat/mod.rs` | チャット機能関連 |
| `AgentConfigError` | `crates/chat-cli/src/cli/agent/mod.rs` | Agent設定関連 |
| `McpClientError` | `crates/chat-cli/src/mcp_client/client.rs` | MCPクライアント関連 |
| `DatabaseError` | `crates/chat-cli/src/database/mod.rs` | データベース操作関連 |
| `RequestError` | `crates/chat-cli/src/request.rs` | リクエスト処理関連 |

### その他のエラー型

```bash
# すべてのエラー型を検索
rg "^pub enum.*Error" --type rust -g "crates/chat-cli/**"
```

**発見されたエラー型（20個）**:
- `Error` (logging.rs)
- `RequestError` (request.rs)
- `AuthError` (auth/mod.rs)
- `TelemetryError` (telemetry/mod.rs)
- `MessengerError` (mcp_client/messenger.rs)
- `OauthUtilError` (mcp_client/oauth_util.rs)
- `McpClientError` (mcp_client/client.rs)
- `DatabaseError` (database/mod.rs)
- `UtilError` (util/mod.rs)
- `FileUriError` (util/file_uri.rs)
- `Error` (util/open.rs)
- `KnowledgeError` (util/knowledge_store.rs)
- `DirectoryError` (util/directories.rs)
- `ApiClientError` (api_client/error.rs)
- `AgentConfigError` (cli/agent/mod.rs)
- `Error` (cli/chat/parse.rs)
- `RecvErrorKind` (cli/chat/parser.rs)
- `ChatError` (cli/chat/mod.rs)
- `ClipboardError` (cli/chat/util/clipboard.rs)
- `GetPromptError` (cli/chat/cli/prompts.rs)

---

## 🎨 エラー定義のパターン

### パターン1: thiserrorを使用したカスタムエラー型

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum MyError {
    // 固定メッセージ
    #[error("quota has reached its limit")]
    QuotaBreach {
        message: &'static str,
        status_code: Option<u16>,
    },
    
    // 変数を含むメッセージ
    #[error("Failed to swap to agent: {0}")]
    AgentSwapError(eyre::Report),
    
    // 他のエラーをラップ（透過的）
    #[error(transparent)]
    Io(#[from] std::io::Error),
    
    // 他のエラーをラップ（カスタム表示）
    #[error("{}", SdkErrorDisplay(.0))]
    GenerateCompletions(#[from] SdkError<GenerateCompletionsError, HttpResponse>),
}
```

### パターン2: eyreを使用した即座のエラー返却

```rust
use eyre::{bail, Result};

fn my_function() -> Result<()> {
    if condition {
        bail!("The EDITOR environment variable is not set");
    }
    Ok(())
}
```

### パターン3: エラーコンテキストの追加

```rust
use eyre::{Context, Result};

fn my_function() -> Result<()> {
    std::fs::read_to_string("config.json")
        .context("Failed to read configuration file")?;
    Ok(())
}
```

---

## 🔢 エラーコードの管理

Q CLIは**明示的なエラーコード（E001, E002等）を使用していません**。

代わりに、以下の方法でエラーを識別します：

### 1. reason_code()メソッド

```rust
impl ReasonCode for ApiClientError {
    fn reason_code(&self) -> String {
        match self {
            Self::QuotaBreach { .. } => "QuotaBreachError".to_string(),
            Self::ContextWindowOverflow { .. } => "ContextWindowOverflow".to_string(),
            Self::AuthError(_) => "AuthError".to_string(),
            // ...
        }
    }
}
```

### 2. status_code()メソッド

HTTPステータスコードを返す：

```rust
impl ApiClientError {
    pub fn status_code(&self) -> Option<u16> {
        match self {
            Self::QuotaBreach { status_code, .. } => *status_code,
            Self::ContextWindowOverflow { status_code } => *status_code,
            // ...
        }
    }
}
```

---

## 📝 エラーメッセージのベストプラクティス

### 1. ユーザーフレンドリーなメッセージ

❌ **悪い例**:
```rust
#[error("ctx win overflow")]
```

✅ **良い例**:
```rust
#[error("the context window has overflowed")]
```

### 2. 対処方法を含める（可能な場合）

✅ **良い例**:
```rust
#[error(
    "Tool approval required but --no-interactive was specified. Use --trust-all-tools to automatically approve tools."
)]
NonInteractiveToolApproval,
```

### 3. 変数を適切に使用

```rust
// 変数を含める
#[error("Failed to swap to agent: {0}")]
AgentSwapError(eyre::Report),

// 複数の変数
#[error("OAuth state mismatch. Actual: {} | Expected: {}", .actual, .expected)]
OAuthStateMismatch { actual: String, expected: String },
```

### 4. 一貫性のある表現

- 文頭は小文字で開始（エラーメッセージの前に "Error: " が付くため）
- 句読点は不要（最後にピリオドを付けない）
- 簡潔で明確な表現

---

## 🔄 エラー伝播のパターン

### パターン1: ?演算子による伝播

```rust
fn my_function() -> Result<(), MyError> {
    let data = std::fs::read_to_string("file.txt")?;  // Io errorに自動変換
    Ok(())
}
```

### パターン2: map_errによる変換

```rust
fn my_function() -> Result<(), MyError> {
    let data = std::fs::read_to_string("file.txt")
        .map_err(|e| MyError::Custom(format!("Failed to read file: {}", e)))?;
    Ok(())
}
```

### パターン3: contextによるコンテキスト追加

```rust
use eyre::Context;

fn my_function() -> eyre::Result<()> {
    let data = std::fs::read_to_string("file.txt")
        .context("Failed to read configuration file")?;
    Ok(())
}
```

---

## 🧪 エラーのテスト

### ユニットテスト例

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_error_display() {
        let error = MyError::QuotaBreach {
            message: "test",
            status_code: Some(429),
        };
        assert_eq!(error.to_string(), "quota has reached its limit");
    }

    #[test]
    fn test_error_status_code() {
        let error = MyError::QuotaBreach {
            message: "test",
            status_code: Some(429),
        };
        assert_eq!(error.status_code(), Some(429));
    }
}
```

---

## 📊 エラー統計

**調査日**: 2025-10-24  
**対象バージョン**: v1.17.0

- **エラー型の総数**: 20個
- **`#[error(...)]`定義**: 155個
- **`bail!(...)`使用**: 53箇所
- **主要エラーカテゴリ**: 7カテゴリ

---

## 🔗 関連ドキュメント

- [エラーメッセージ一覧](../../01_for-users/07_reference/10_error-messages.md) - ユーザー向けエラー一覧
- [エラーメッセージ追加ガイド](04_adding-error-messages.md) - 新規エラーの追加方法
- [コントリビューションガイド](README.md) - コントリビューション全般

---

## 📚 外部リソース

- [thiserror documentation](https://docs.rs/thiserror/)
- [eyre documentation](https://docs.rs/eyre/)
- [Rust Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

---

[ホーム](../../README.md) > [開発者ガイド](../README.md) > [コントリビューション](README.md) > 05 エラー管理概要

---

最終更新: 2025-10-26
