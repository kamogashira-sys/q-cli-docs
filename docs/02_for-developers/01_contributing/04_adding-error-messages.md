[ホーム](../../README.md) > [開発者ガイド](../README.md) > [コントリビューション](README.md) > 06 エラーメッセージ追加ガイド

# エラーメッセージ追加

**ドキュメント対象バージョン**: v1.13.0以降  
**対象読者**: 開発者、コントリビューター

> **Note**: 本サイトではv1.13.0以降のエラーメッセージ追加方法を対象に記述しています。

---

## 📋 概要

このガイドでは、Q CLIに新しいエラーメッセージを追加する手順を説明します。

---

## 🚀 クイックスタート

### ステップ1: エラー型を選択または作成

既存のエラー型を使用するか、新しいエラー型を作成します。

**既存のエラー型を使用する場合**:
```rust
// crates/chat-cli/src/api_client/error.rs
#[derive(Debug, Error)]
pub enum ApiClientError {
    // 既存のバリアント
    #[error("quota has reached its limit")]
    QuotaBreach { ... },
    
    // 新しいバリアントを追加
    #[error("new error message here")]
    NewError { ... },
}
```

**新しいエラー型を作成する場合**:
```rust
// crates/chat-cli/src/my_module/mod.rs（例示用パス）
use thiserror::Error;

#[derive(Debug, Error)]
pub enum MyModuleError {
    #[error("error message")]
    MyError,
}
```

### ステップ2: エラーメッセージを定義

```rust
#[error("user-friendly error message")]
ErrorVariant {
    // 必要に応じてフィールドを追加
    context: String,
    status_code: Option<u16>,
},
```

### ステップ3: エラーを使用

```rust
fn my_function() -> Result<(), MyModuleError> {
    if condition {
        return Err(MyModuleError::MyError);
    }
    Ok(())
}
```

### ステップ4: ドキュメントを更新

1. [エラーメッセージ一覧](../../01_for-users/07_reference/10_error-messages.md)に追加
2. 必要に応じてトラブルシューティングガイドを更新

---

## 📝 詳細ガイド

### 1. エラー型の選択

#### 既存のエラー型を使用すべき場合

- 既存のモジュールに機能を追加する場合
- エラーが既存のカテゴリに属する場合

**主要なエラー型**:
- `ApiClientError` - API呼び出し関連
- `AuthError` - 認証関連
- `ChatError` - チャット機能関連
- `AgentConfigError` - Agent設定関連
- `McpClientError` - MCPクライアント関連
- `DatabaseError` - データベース操作関連

#### 新しいエラー型を作成すべき場合

- 新しいモジュールを追加する場合
- 既存のエラー型に適合しない場合
- エラーの責任範囲が明確に異なる場合

### 2. エラーメッセージの設計

#### 基本原則

1. **ユーザーフレンドリー**: 技術的な詳細よりも、ユーザーが理解しやすい表現
2. **実用的**: 可能な限り対処方法を含める
3. **簡潔**: 必要な情報のみを含める
4. **一貫性**: 既存のメッセージと表現を統一

#### メッセージのテンプレート

```rust
// パターン1: 固定メッセージ
#[error("the context window has overflowed")]
ContextWindowOverflow { status_code: Option<u16> },

// パターン2: 変数を含むメッセージ
#[error("Failed to load configuration from {path}")]
ConfigLoadError { path: String },

// パターン3: 対処方法を含むメッセージ
#[error(
    "Tool approval required but --no-interactive was specified. \
     Use --trust-all-tools to automatically approve tools."
)]
NonInteractiveToolApproval,

// パターン4: 複数の変数
#[error("Expected {expected} but got {actual}")]
ValidationError { expected: String, actual: String },
```

#### メッセージのスタイルガイド

✅ **推奨**:
- 小文字で開始（"Error: " が自動的に付くため）
- 簡潔で明確な表現
- 専門用語を避ける（必要な場合は説明を追加）

❌ **非推奨**:
- 大文字で開始
- 最後にピリオドを付ける
- 過度に技術的な表現
- 曖昧な表現

### 3. エラーバリアントの実装

#### 基本的なバリアント

```rust
#[derive(Debug, Error)]
pub enum MyError {
    // 最もシンプルな形式
    #[error("simple error message")]
    SimpleError,
    
    // コンテキスト情報を含む
    #[error("error with context: {context}")]
    ErrorWithContext { context: String },
    
    // 複数のフィールド
    #[error("error occurred at {location}: {message}")]
    DetailedError {
        location: String,
        message: String,
        timestamp: std::time::SystemTime,
    },
}
```

#### 他のエラーをラップ

```rust
#[derive(Debug, Error)]
pub enum MyError {
    // 透過的なラップ（元のエラーメッセージをそのまま表示）
    #[error(transparent)]
    Io(#[from] std::io::Error),
    
    // カスタム表示でラップ
    #[error("Failed to read file: {0}")]
    FileRead(#[from] std::io::Error),
    
    // Boxでラップ（サイズ削減）
    #[error("{0}")]
    Client(Box<ApiClientError>),
}
```

### 4. エラーの使用

#### 基本的な使用方法

```rust
fn my_function() -> Result<(), MyError> {
    // エラーを直接返す
    if condition {
        return Err(MyError::SimpleError);
    }
    
    // フィールド付きエラー
    if another_condition {
        return Err(MyError::ErrorWithContext {
            context: "additional information".to_string(),
        });
    }
    
    Ok(())
}
```

#### bail!マクロの使用

```rust
use eyre::{bail, Result};

fn my_function() -> Result<()> {
    if condition {
        bail!("The EDITOR environment variable is not set");
    }
    Ok(())
}
```

#### エラーコンテキストの追加

```rust
use eyre::{Context, Result};

fn my_function() -> Result<()> {
    std::fs::read_to_string("config.json")
        .context("Failed to read configuration file")?;
    Ok(())
}
```

### 5. エラーメソッドの実装

#### status_code()メソッド

HTTPステータスコードを返す場合：

```rust
impl MyError {
    pub fn status_code(&self) -> Option<u16> {
        match self {
            Self::QuotaBreach { status_code } => *status_code,
            Self::NotFound => Some(404),
            _ => None,
        }
    }
}
```

#### reason_code()メソッド

テレメトリ用のエラーコード：

```rust
impl ReasonCode for MyError {
    fn reason_code(&self) -> String {
        match self {
            Self::QuotaBreach => "QuotaBreachError".to_string(),
            Self::NotFound => "NotFoundError".to_string(),
            _ => "UnknownError".to_string(),
        }
    }
}
```

### 6. テストの追加

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_error_message() {
        let error = MyError::SimpleError;
        assert_eq!(error.to_string(), "simple error message");
    }

    #[test]
    fn test_error_with_context() {
        let error = MyError::ErrorWithContext {
            context: "test context".to_string(),
        };
        assert_eq!(error.to_string(), "error with context: test context");
    }

    #[test]
    fn test_status_code() {
        let error = MyError::NotFound;
        assert_eq!(error.status_code(), Some(404));
    }
}
```

---

## 📚 実装例

### 例1: 新しいAPI エラーの追加

```rust
// crates/chat-cli/src/api_client/error.rs

#[derive(Debug, Error)]
pub enum ApiClientError {
    // 既存のバリアント...
    
    // 新しいエラーを追加
    #[error("Rate limit exceeded. Please try again in {retry_after} seconds")]
    RateLimitExceeded {
        retry_after: u64,
        status_code: Option<u16>,
    },
}

// status_code()メソッドに追加
impl ApiClientError {
    pub fn status_code(&self) -> Option<u16> {
        match self {
            // 既存のケース...
            Self::RateLimitExceeded { status_code, .. } => *status_code,
        }
    }
}

// reason_code()メソッドに追加
impl ReasonCode for ApiClientError {
    fn reason_code(&self) -> String {
        match self {
            // 既存のケース...
            Self::RateLimitExceeded { .. } => "RateLimitExceeded".to_string(),
        }
    }
}
```

### 例2: 新しいモジュールエラーの作成

```rust
// crates/chat-cli/src/my_module/error.rs（例示用パス）

use thiserror::Error;

#[derive(Debug, Error)]
pub enum MyModuleError {
    #[error("configuration file not found at {path}")]
    ConfigNotFound { path: String },
    
    #[error("invalid configuration: {reason}")]
    InvalidConfig { reason: String },
    
    #[error(transparent)]
    Io(#[from] std::io::Error),
    
    #[error(transparent)]
    SerdeJson(#[from] serde_json::Error),
}

impl MyModuleError {
    pub fn is_recoverable(&self) -> bool {
        matches!(self, Self::ConfigNotFound { .. })
    }
}
```

### 例3: bail!マクロの使用

```rust
use eyre::{bail, Result};

fn validate_config(config: &Config) -> Result<()> {
    if config.name.is_empty() {
        bail!("Configuration name cannot be empty");
    }
    
    if config.timeout < 0 {
        bail!("Timeout must be a positive number, got {}", config.timeout);
    }
    
    Ok(())
}
```

---

## ✅ チェックリスト

新しいエラーメッセージを追加する際のチェックリスト：

### コード

- [ ] エラーバリアントを定義した
- [ ] エラーメッセージが明確でユーザーフレンドリー
- [ ] 必要に応じて`status_code()`メソッドを更新
- [ ] 必要に応じて`reason_code()`メソッドを更新
- [ ] エラーの使用箇所を実装
- [ ] ユニットテストを追加

### ドキュメント

- [ ] [エラーメッセージ一覧](../../01_for-users/07_reference/10_error-messages.md)に追加
  - エラーメッセージ
  - 原因
  - 対処方法
  - 関連情報
- [ ] 必要に応じてトラブルシューティングガイドを更新
- [ ] コード内にドキュメントコメントを追加

### レビュー

- [ ] エラーメッセージのスタイルガイドに準拠
- [ ] 既存のエラーメッセージと一貫性がある
- [ ] テストが通過する
- [ ] ドキュメントが正確

---

## 🔗 関連ドキュメント

- [エラーメッセージ管理の概要](03_error-management-overview.md)
- [エラーメッセージ一覧](../../01_for-users/07_reference/10_error-messages.md)
- [コントリビューションガイド](README.md)

---

## 📚 外部リソース

- [thiserror documentation](https://docs.rs/thiserror/)
- [eyre documentation](https://docs.rs/eyre/)
- [Rust Error Handling Book](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

---

[ホーム](../../README.md) > [開発者ガイド](../README.md) > [コントリビューション](README.md) > 06 エラーメッセージ追加ガイド

---

最終更新: 2025-11-01
