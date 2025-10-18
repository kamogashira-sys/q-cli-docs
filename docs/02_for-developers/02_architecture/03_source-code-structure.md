[ホーム](../../README.md) > [開発者ガイド](../README.md) > [アーキテクチャ](README.md) > 03 Source Code Structure

---

# Amazon Q CLI ソースコード構造マップ

**作成日**: 2025-10-08  
**対象バージョン**: v1.17.0  
**ソースコード**: `crates/chat-cli/src/`

## 概要

このドキュメントは、Amazon Q CLIの設定関連ソースコードの構造を視覚的に説明します。開発者向けの技術資料です。

---

## 設定関連ファイルの構造

```mermaid
graph TD
    subgraph CLI["CLI Layer (cli/)"]
        CliMod[cli/mod.rs<br/>CLI引数解析]
        Settings[cli/settings.rs<br/>設定コマンド実装]
        Agent[cli/agent/mod.rs<br/>Agent管理]
        McpConfig[cli/agent/mcp_config.rs<br/>MCP設定]
    end
    
    subgraph Database["Database Layer (database/)"]
        DbSettings[database/settings.rs<br/>Setting enum<br/>Settings struct<br/>設定の永続化]
    end
    
    subgraph Util["Utility Layer (util/)"]
        Consts[util/consts.rs<br/>環境変数定義<br/>Q_LOG_LEVEL等]
        Directories[util/directories.rs<br/>パス定義<br/>settings_path等]
    end
    
    subgraph MCP["MCP Layer (mcp_client/)"]
        McpClient[mcp_client/client.rs<br/>環境変数展開<br/>substitute_env_vars]
    end
    
    CliMod --> Settings
    Settings --> DbSettings
    Agent --> DbSettings
    Agent --> McpConfig
    McpConfig --> McpClient
    McpClient --> Consts
    DbSettings --> Directories
    
    style CLI fill:#e3f2fd
    style Database fill:#fff3e0
    style Util fill:#f3e5f5
    style MCP fill:#e8f5e9
```

---

## Setting enumのクラス図

```mermaid
classDiagram
    class Setting {
        <<enumeration>>
        +TelemetryEnabled
        +OldClientId
        +ShareCodeWhispererContent
        +EnabledThinking
        +EnabledKnowledge
        +KnowledgeDefaultIncludePatterns
        +KnowledgeDefaultExcludePatterns
        +KnowledgeMaxFiles
        +KnowledgeChunkSize
        +KnowledgeChunkOverlap
        +KnowledgeIndexType
        +SkimCommandKey
        +AutocompletionKey
        +EnabledTangentMode
        +TangentModeKey
        +DelegateModeKey
        +IntrospectTangentMode
        +ChatGreetingEnabled
        +ApiTimeout
        +ChatEditMode
        +ChatEnableNotifications
        +ApiCodeWhispererService
        +ApiQService
        +McpInitTimeout
        +McpNoInteractiveTimeout
        +McpLoadedBefore
        +EnabledContextUsageIndicator
        +ChatDefaultModel
        +ChatDisableMarkdownRendering
        +ChatDefaultAgent
        +ChatDisableAutoCompaction
        +ChatEnableHistoryHints
        +EnabledTodoList
        +EnabledCheckpoint
        +EnabledDelegate
        +as_ref() &str
    }
    
    class Settings {
        -Map~String, Value~ 0
        +new() Result~Self~
        +get(key: Setting) Option~Value~
        +set(key: Setting, value) Result
        +remove(key: Setting) Result
        +get_bool(key: Setting) Option~bool~
        +get_string(key: Setting) Option~String~
        +get_int(key: Setting) Option~i64~
        +get_int_or(key: Setting, default: usize) usize
        +save_to_file() Result
        +map() Map~String, Value~
    }
    
    Settings --> Setting : uses
```

**Setting enumの特徴**:
- 35項目の設定を定義
- `as_ref()`で設定キー文字列に変換（例: `TelemetryEnabled` → `"telemetry.enabled"`）
- `strum`クレートで説明メッセージを付与

**Settings構造体の特徴**:
- JSON形式で設定を保存（`Map<String, Value>`）
- 型安全なアクセスメソッド（`get_bool`, `get_string`, `get_int`）
- ファイルへの永続化（`save_to_file()`）

---

## 設定読み込みのシーケンス図

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant CLI as CLI (cli/mod.rs)
    participant Settings as Settings<br/>(cli/settings.rs)
    participant DbSettings as Database<br/>(database/settings.rs)
    participant File as 設定ファイル<br/>(~/.local/share/amazon-q/settings.json)
    
    User->>CLI: q settings chat.defaultAgent my-agent
    CLI->>Settings: 設定コマンド実行
    Settings->>DbSettings: Settings::new()
    DbSettings->>File: ファイル存在確認
    
    alt ファイルが存在
        File-->>DbSettings: JSONを読み込み
    else ファイルが存在しない
        DbSettings->>File: 空のJSON {}を作成
    end
    
    DbSettings-->>Settings: Settings構造体を返す
    Settings->>DbSettings: set(ChatDefaultAgent, "my-agent")
    DbSettings->>DbSettings: 内部Mapを更新
    DbSettings->>File: save_to_file()
    File-->>DbSettings: 保存完了
    DbSettings-->>Settings: 成功
    Settings-->>CLI: 成功
    CLI-->>User: 設定完了メッセージ
```

---

## 環境変数展開の処理フロー

```mermaid
sequenceDiagram
    participant Agent as Agent設定
    participant McpClient as MCP Client<br/>(mcp_client/client.rs)
    participant Env as 環境変数<br/>(os::Env)
    participant Regex as 正規表現エンジン
    
    Agent->>McpClient: MCP設定を渡す<br/>"${env:API_KEY}"
    McpClient->>McpClient: substitute_env_vars()
    McpClient->>Regex: パターンマッチ<br/>r"\$\{env:([^}]+)\}"
    Regex-->>McpClient: "API_KEY"を抽出
    McpClient->>Env: get("API_KEY")
    
    alt 環境変数が存在
        Env-->>McpClient: "secret-key-123"
        McpClient->>McpClient: 値を置換
    else 環境変数が存在しない
        Env-->>McpClient: エラー
        McpClient->>McpClient: 元の文字列を保持<br/>"${env:API_KEY}"
    end
    
    McpClient-->>Agent: 展開済み設定を返す
```

**環境変数展開の実装**:

```rust
fn substitute_env_vars(input: &str, env: &crate::os::Env) -> String {
    let re = Regex::new(r"\$\{env:([^}]+)\}").unwrap();
    re.replace_all(input, |caps: &regex::Captures<'_>| {
        let var_name = &caps[1];
        env.get(var_name).unwrap_or_else(|_| format!("${{{}}}", var_name))
    }).to_string()
}
```

**特徴**:
- 正規表現で`${env:VAR_NAME}`パターンをマッチ
- 環境変数が存在しない場合は元の文字列を保持
- エラーを発生させず、安全にフォールバック

---

## 主要な関数とメソッド

### database/settings.rs

#### Settings::new()
```rust
pub async fn new() -> Result<Self, DatabaseError>
```
- 設定ファイルを読み込み、Settings構造体を初期化
- ファイルが存在しない場合は空のJSONを作成
- パス: `crate::util::directories::settings_path()`

#### Settings::get()
```rust
pub fn get(&self, key: Setting) -> Option<&Value>
```
- 設定値を取得
- 型変換は呼び出し側で実施

#### Settings::set()
```rust
pub async fn set(&mut self, key: Setting, value: impl Into<serde_json::Value>) -> Result<(), DatabaseError>
```
- 設定値を設定
- 自動的にファイルに保存

#### Settings::get_bool() / get_string() / get_int()
```rust
pub fn get_bool(&self, key: Setting) -> Option<bool>
pub fn get_string(&self, key: Setting) -> Option<String>
pub fn get_int(&self, key: Setting) -> Option<i64>
```
- 型安全なアクセスメソッド
- 型が一致しない場合は`None`を返す

### mcp_client/client.rs

#### substitute_env_vars()
```rust
fn substitute_env_vars(input: &str, env: &crate::os::Env) -> String
```
- `${env:VAR_NAME}`構文を環境変数の値に展開
- 環境変数が存在しない場合は元の文字列を保持

#### process_env_vars()
```rust
fn process_env_vars(env_vars: &mut HashMap<String, String>, env: &crate::os::Env)
```
- HashMap内の全ての値に対して環境変数展開を実行

---

## ファイルパスの定義

### util/directories.rs

```rust
// 設定ファイルのパス
pub fn settings_path() -> Result<PathBuf, DirectoryError> {
    // ~/.local/share/amazon-q/settings.json
}

// Agent設定ディレクトリ
pub fn chat_agents_dir() -> Result<PathBuf, DirectoryError> {
    // ~/.aws/amazonq/cli-agents/
}

// グローバルMCP設定（レガシー）
pub fn chat_legacy_global_mcp_config() -> Result<PathBuf, DirectoryError> {
    // ~/.aws/amazonq/mcp.json
}
```

---

## 環境変数の定義

### util/consts.rs

```rust
pub mod env_var {
    pub const Q_LOG_LEVEL: &str = "Q_LOG_LEVEL";
    pub const Q_LOG_STDOUT: &str = "Q_LOG_STDOUT";
    pub const Q_CLI_CLIENT_APPLICATION: &str = "Q_CLI_CLIENT_APPLICATION";
    // ... 他13項目
    
    pub const ALL: &[&str] = &[
        QTERM_SESSION_ID,
        Q_PARENT,
        Q_SET_PARENT,
        // ... 全ての環境変数
    ];
}
```

**特徴**:
- マクロで環境変数を定義
- `ALL`配列で全ての環境変数を管理
- ドキュメントコメント付き

---

## データフロー

### 設定の読み込み

```
ユーザー
  ↓
CLI引数解析 (cli/mod.rs)
  ↓
設定コマンド (cli/settings.rs)
  ↓
Settings::new() (database/settings.rs)
  ↓
ファイル読み込み (~/.local/share/amazon-q/settings.json)
  ↓
Settings構造体
```

### 設定の保存

```
ユーザー
  ↓
設定コマンド (cli/settings.rs)
  ↓
Settings::set() (database/settings.rs)
  ↓
内部Map更新
  ↓
save_to_file()
  ↓
ファイル保存 (~/.local/share/amazon-q/settings.json)
```

### 環境変数展開

```
Agent設定読み込み
  ↓
MCP設定解析 (cli/agent/mcp_config.rs)
  ↓
環境変数展開 (mcp_client/client.rs)
  ↓
substitute_env_vars()
  ↓
正規表現マッチ
  ↓
環境変数取得 (os::Env)
  ↓
値の置換
  ↓
展開済み設定
```

---

## 開発者向けの注意事項

### 1. 設定の追加方法

新しい設定項目を追加する場合：

1. **Setting enumに追加** (`database/settings.rs`)
   ```rust
   #[strum(message = "説明文 (型)")]
   NewSetting,
   ```

2. **as_ref()に追加**
   ```rust
   Self::NewSetting => "category.newSetting",
   ```

3. **TryFromに追加**
   ```rust
   "category.newSetting" => Ok(Self::NewSetting),
   ```

### 2. 環境変数の追加方法

新しい環境変数を追加する場合：

1. **util/consts.rsに追加**
   ```rust
   /// 説明文
   NEW_VAR = "NEW_VAR",
   ```

2. **使用箇所で参照**
   ```rust
   use crate::util::consts::env_var::NEW_VAR;
   std::env::var(NEW_VAR)
   ```

### 3. テスト

設定関連のテストは`database/settings.rs`の`#[cfg(test)]`モジュールに記載。

---

## 参考リンク

- [設定優先順位ガイド](../../01_for-users/03_configuration/02_priority-rules.md) - 設定の優先順位と図解
- [設定項目完全リファレンス](../../01_for-users/07_reference/03_settings-reference.md) - 全設定項目の一覧
- [環境変数ガイド](../../01_for-users/03_configuration/05_environment-variables.md) - 環境変数の完全リスト
- [Agent設定ファイル完全仕様](../../01_for-users/03_configuration/04_agent-configuration.md) - Agent設定の詳細

---

**ドキュメント作成日**: 2025-10-08  
最終更新: 2025-10-08  
**対象バージョン**: v1.17.0  
**ソースコード**: `crates/chat-cli/src/` (amazon-q-developer-cli)
