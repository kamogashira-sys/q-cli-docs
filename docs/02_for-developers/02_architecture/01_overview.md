[ホーム](../../README.md) > [開発者ガイド](../README.md) > [アーキテクチャ](README.md) > 01 Overview

---

# アーキテクチャ概要

最終更新: 2025-10-13  
**対象バージョン**: v1.18.0

---

## 🏗️ システム構成

> **💡 このセクションについて**
> 
> このシステム構成は、Q CLIのソースコード調査に基づいています。
> 
> **出典**: [Cargo.toml](https://github.com/aws/amazon-q-developer-cli/blob/main/Cargo.toml) - Workspace構成の定義
> 
> **検証方法**:
> - Cargo.tomlで全crateのメンバーを確認
> - 各crateのディレクトリ構造を確認
> - 依存関係をCargo.tomlで確認

Amazon Q CLIは、Rustで実装されたモノレポ構成のプロジェクトです。

### Workspace構成（8つのcrate）

```mermaid
graph TB
    subgraph "Amazon Q Developer CLI"
        CLI[chat-cli<br/>メインアプリケーション]
    end
    
    subgraph "AWS API Clients"
        CW[amzn-codewhisperer-client]
        CWS[amzn-codewhisperer-streaming-client]
        CON[amzn-consolas-client]
        QDS[amzn-qdeveloper-streaming-client]
        TEL[amzn-toolkit-telemetry-client]
    end
    
    subgraph "Support Libraries"
        TELD[aws-toolkit-telemetry-definitions]
        SEM[semantic-search-client]
    end
    
    CLI --> CW
    CLI --> CWS
    CLI --> CON
    CLI --> QDS
    CLI --> TEL
    CLI --> TELD
    CLI --> SEM
    
    TEL --> TELD
    
    style CLI fill:#e3f2fd
    style CW fill:#fff3cd
    style CWS fill:#fff3cd
    style CON fill:#fff3cd
    style QDS fill:#fff3cd
    style TEL fill:#fff3cd
```

---

## 🔄 レイヤー構造

> **💡 このセクションについて**
> 
> このレイヤー構造は、chat-cliのソースコード構造に基づいています。
> 
> **出典**: [crates/chat-cli/src/](https://github.com/aws/amazon-q-developer-cli/tree/main/crates/chat-cli/src) - ディレクトリ構造
> 
> **検証方法**:
> - ソースコードのディレクトリ構造を確認
> - 各モジュールの責務を確認
> - モジュール間の依存関係を確認
> 
> **レイヤー分類**:
> - **Presentation Layer**: cli/, theme/
> - **Application Layer**: cli/chat/, cli/agent/, cli/experiment/, cli/settings/, cli/user/
> - **Domain Layer**: auth/, mcp_client/, api_client/
> - **Infrastructure Layer**: database/, os/, util/, telemetry/

chat-cliは4層アーキテクチャで構成されています：

```mermaid
graph TB
    subgraph "Presentation Layer"
        CLI[CLI Interface<br/>コマンドライン処理]
        THEME[Theme<br/>テーマ管理]
    end
    
    subgraph "Application Layer"
        CHAT[Chat<br/>チャット機能]
        AGENT[Agent<br/>Agent管理]
        EXP[Experiment<br/>実験的機能]
        SETTINGS[Settings<br/>設定管理]
        USER[User<br/>ユーザー管理]
    end
    
    subgraph "Domain Layer"
        AUTH[Auth<br/>認証]
        MCP[MCP Client<br/>MCP統合]
        API[API Client<br/>AWS API呼び出し]
    end
    
    subgraph "Infrastructure Layer"
        DB[Database<br/>SQLite]
        OS[OS<br/>OS固有処理]
        UTIL[Util<br/>ユーティリティ]
        TEL[Telemetry<br/>テレメトリ]
    end
    
    CLI --> CHAT
    CLI --> AGENT
    CLI --> EXP
    CLI --> SETTINGS
    CLI --> USER
    
    CHAT --> AUTH
    CHAT --> MCP
    CHAT --> API
    
    AGENT --> DB
    SETTINGS --> DB
    USER --> AUTH
    
    AUTH --> OS
    MCP --> OS
    API --> TEL
    
    DB --> UTIL
    OS --> UTIL
```

### 主要モジュール

| レイヤー | モジュール | 責務 |
|---------|-----------|------|
| **Presentation** | CLI Interface | コマンドライン処理とルーティング |
| | Theme | テーマ管理 |
| **Application** | Chat | チャット機能の実装 |
| | Agent | Agent管理機能 |
| | Experiment | 実験的機能 |
| | Settings | 設定管理 |
| | User | ユーザー管理 |
| **Domain** | Auth | 認証・認可 |
| | MCP Client | MCP統合 |
| | API Client | AWS API呼び出し |
| **Infrastructure** | Database | データ永続化（SQLite） |
| | OS | OS固有処理の抽象化 |
| | Util | 共通ユーティリティ |
| | Telemetry | テレメトリデータ送信 |

---

## 🔄 データフロー

### チャットセッションのフロー

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Chat
    participant Agent
    participant MCP
    participant API
    participant DB
    
    User->>CLI: q chat
    CLI->>Agent: Load Agent
    Agent->>DB: Get Agent Config
    DB-->>Agent: Agent Config
    Agent->>MCP: Initialize MCP Servers
    MCP-->>Agent: MCP Ready
    Agent-->>CLI: Agent Ready
    
    CLI->>Chat: Start Chat Session
    Chat->>DB: Load Context
    DB-->>Chat: Context Data
    
    User->>Chat: User Message
    Chat->>API: Send to Q Developer
    API-->>Chat: AI Response
    Chat->>MCP: Execute Tools
    MCP-->>Chat: Tool Results
    Chat->>DB: Save History
    Chat-->>User: Display Response
```

### 設定管理フロー

```mermaid
graph LR
    subgraph "設定ソース"
        CMD[コマンドライン引数]
        ENV[環境変数]
        AGENT[Agent設定]
        GLOBAL[グローバル設定]
        DEFAULT[デフォルト値]
    end
    
    subgraph "設定マージ"
        MERGE[Settings Merger]
    end
    
    subgraph "設定保存"
        DB[(SQLite)]
        FILE[設定ファイル]
    end
    
    CMD --> MERGE
    ENV --> MERGE
    AGENT --> MERGE
    GLOBAL --> MERGE
    DEFAULT --> MERGE
    
    MERGE --> DB
    MERGE --> FILE
```

---

## 🛠️ 技術スタック

### 言語・フレームワーク

- **言語**: Rust (Edition 2024)
- **UI**: crossterm, rustyline, dialoguer
- **非同期**: tokio, futures
- **プロトコル**: MCP

### AWS SDK

- aws-config, aws-sdk-ssooidc, aws-sdk-cognitoidentity
- aws-smithy-* (Smithy runtime)

### データ処理

- **シリアライゼーション**: serde, serde_json
- **データベース**: rusqlite, r2d2
- **パターンマッチング**: regex, glob, globset

### ネットワーク

- **HTTP**: reqwest, hyper
- **TLS**: rustls

### パフォーマンス

- **メモリ**: mimalloc
- **並行処理**: rayon
- **ロック**: parking_lot

---

## 🔒 セキュリティ機能

### 認証

- Builder ID認証
- Identity Center認証
- トークン管理

### 権限管理

- ツール実行権限チェック
- ファイルアクセス制御
- コマンド実行制限

### データ保護

- 設定ファイルの暗号化
- トークンの安全な保存
- 機密情報のマスキング

---

## 📚 詳細情報

- [ソースコード構造](03_source-code-structure.md)
- [設定システム詳細](02_configuration-system.md)

---

**作成日**: 2025-10-11  
**更新日**: 2025-10-13
