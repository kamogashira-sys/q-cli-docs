# MCP設定ファイル (mcp.json) 仕様書

[ホーム](../../../README.md) > [ユーザー向けドキュメント](../../README.md) > [ファイル仕様](README.md) > MCP設定

---

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **ファイル名** | `mcp.json` |
| **ファイル形式** | JSON |
| **エンコーディング** | UTF-8 |
| **改行コード** | LF (Unix形式) |
| **JSONスキーマ** | ローカル: `schemas/agent-v1.json`（mcpServersフィールド） / [GitHub](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json) |
| **スキーマバージョン** | JSON Schema Draft-07 |

### ファイル配置場所

| 種別 | パス | 説明 |
|------|------|------|
| **レガシーMCP設定** | `~/.aws/amazonq/mcp.json` | グローバルMCP設定（非推奨） |
| **Agent内MCP設定** | `agent.json`の`mcpServers`フィールド | 推奨される設定方法 |

**注意**: レガシーMCP設定（`mcp.json`）は後方互換性のために残されていますが、Agent設定内での定義が推奨されます。

---

## 2. 目的と役割

### 目的

MCP（Model Context Protocol）設定ファイルは、Q CLIが外部MCPサーバーと連携するための設定を定義します。

### 主な役割

| 役割 | 説明 |
|------|------|
| **MCPサーバー管理** | MCPサーバーの起動設定 |
| **トランスポート設定** | stdio/HTTP通信の設定 |
| **認証設定** | OAuth認証の設定 |
| **環境変数管理** | MCPサーバー用の環境変数 |
| **タイムアウト制御** | リクエストタイムアウトの設定 |

### 使用場面

- 外部ツールをQ CLIに統合したい
- ファイルシステムアクセスを提供したい
- データベースアクセスを提供したい
- カスタムAPIを統合したい
- HTTPベースのMCPサーバーを使用したい

---

## 3. ファイル構造

### 基本構成

```json
{
  "mcpServers": {
    "サーバー名": {
      "command": "コマンド"
    }
  }
}
```

**必須フィールド**: 各サーバーの`command`のみ

### 完全な構成例

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"],
      "env": {
        "NODE_ENV": "production",
        "API_KEY": "${env:MY_API_KEY}"
      },
      "timeout": 120000,
      "disabled": false
    },
    "database": {
      "type": "http",
      "url": "https://mcp-server.example.com",
      "headers": {
        "Authorization": "Bearer ${env:DB_TOKEN}"
      },
      "oauthScopes": ["openid", "email", "profile", "offline_access"],
      "oauth": {
        "redirectUri": "127.0.0.1:7778"
      },
      "timeout": 180000,
      "disabled": false
    }
  }
}
```

---

## 4. フィールド仕様

### 4.1 トップレベル構造

| フィールド名 | 型 | 必須 | 説明 |
|------------|-----|------|------|
| `mcpServers` | object | ✅ | MCPサーバー設定のマップ |

### 4.2 各MCPサーバーの設定

各サーバーは以下のフィールドを持ちます：

| フィールド名 | 型 | 必須 | デフォルト | 説明 |
|------------|-----|------|----------|------|
| `type` | "stdio"/"http" | ❌ | "stdio" | トランスポート種別 |
| `url` | string | ❌ | "" | HTTPエンドポイント |
| `headers` | object | ❌ | {} | HTTPヘッダー |
| `oauthScopes` | array[string] | ❌ | ["openid","email","profile","offline_access"] | OAuthスコープ |
| `oauth` | object/null | ❌ | - | OAuth設定 |
| `command` | string | ✅ | - | 起動コマンド |
| `args` | array[string] | ❌ | [] | コマンド引数 |
| `env` | object/null | ❌ | - | 環境変数 |
| `timeout` | integer | ❌ | 120000 | タイムアウト（ms） |
| `disabled` | boolean | ❌ | false | 無効化フラグ |

### 4.3 typeフィールド（TransportType）

MCPサーバーとの通信方式を指定します。

| 値 | 説明 | 使用場面 |
|----|------|---------|
| `"stdio"` | 標準入出力（デフォルト） | ローカルプロセスとの通信 |
| `"http"` | HTTPトランスポート | リモートサーバーとの通信 |

**stdio例**
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
}
```

**http例**
```json
{
  "type": "http",
  "url": "https://mcp-server.example.com",
  "headers": {
    "Authorization": "Bearer token"
  }
}
```

### 4.4 commandフィールド

MCPサーバーを起動するコマンドを指定します（stdio専用）。

**例**

| コマンド | 説明 |
|---------|------|
| `"npx"` | Node.jsパッケージの実行 |
| `"python"` | Pythonスクリプトの実行 |
| `"/path/to/binary"` | バイナリの実行 |
| `"uvx"` | Python uvxの実行 |

### 4.5 argsフィールド

コマンドに渡す引数を配列で指定します。

**例**
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/path/to/project"
  ]
}
```

### 4.6 envフィールド

MCPサーバーに渡す環境変数を指定します。

**環境変数展開**

`${env:VAR_NAME}`構文でシステムの環境変数を参照できます。

```json
{
  "env": {
    "API_KEY": "${env:MY_API_KEY}",
    "NODE_ENV": "production",
    "DEBUG": "true"
  }
}
```

### 4.7 timeoutフィールド

MCPリクエストのタイムアウトをミリ秒で指定します。

| 値 | 説明 |
|----|------|
| `120000` | デフォルト（2分） |
| `60000` | 1分 |
| `300000` | 5分 |

**注意**: 長時間実行されるツールの場合は、タイムアウトを増やす必要があります。

### 4.8 disabledフィールド

MCPサーバーを一時的に無効化します。

| 値 | 説明 |
|----|------|
| `false` | 有効（デフォルト） |
| `true` | 無効（起動しない） |

**使用例**
```json
{
  "mcpServers": {
    "test-server": {
      "command": "test-command",
      "disabled": true
    }
  }
}
```

### 4.9 HTTP専用フィールド

#### urlフィールド

HTTPベースのMCPサーバーのエンドポイントを指定します。

```json
{
  "type": "http",
  "url": "https://mcp-server.example.com"
}
```

#### headersフィールド

HTTPリクエストに含めるヘッダーを指定します。

```json
{
  "headers": {
    "Authorization": "Bearer ${env:TOKEN}",
    "Content-Type": "application/json",
    "X-Custom-Header": "value"
  }
}
```

#### oauthScopesフィールド

OAuth認証で要求するスコープを指定します。

**デフォルトスコープ**
```json
["openid", "email", "profile", "offline_access"]
```

**カスタムスコープ**
```json
{
  "oauthScopes": ["openid", "email", "custom:scope"]
}
```

#### oauthフィールド

OAuth認証の詳細設定を指定します。

```json
{
  "oauth": {
    "redirectUri": "127.0.0.1:7778"
  }
}
```

| サブフィールド | 型 | 説明 |
|-------------|-----|------|
| `redirectUri` | string/null | リダイレクトURI（省略時はランダムポート） |

---

## 5. ファイル操作

### 5.1 読み込み処理

**処理フロー**

1. ファイル読み込み
2. JSONパース
3. `mcpServers`フィールド抽出
4. 各サーバー設定をデシリアライズ
5. 環境変数展開

**ソースコード参照**
- ファイル: `crates/chat-cli/src/cli/agent/mcp_config.rs`
- 関数: `McpServerConfig::load_from_file()`

### 5.2 書き込み処理

**処理フロー**

1. `{"mcpServers": {...}}`形式に変換
2. JSON生成（pretty print）
3. ファイル書き込み

**ソースコード参照**
- ファイル: `crates/chat-cli/src/cli/agent/mcp_config.rs`
- 関数: `McpServerConfig::save_to_file()`

### 5.3 Agent設定との統合

**Agent設定内での定義（推奨）**

```json
{
  "name": "my-agent",
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    }
  }
}
```

**レガシーMCP設定の統合**

Agent設定で`useLegacyMcpJson: true`を指定すると、`~/.aws/amazonq/mcp.json`が統合されます。

```json
{
  "name": "my-agent",
  "useLegacyMcpJson": true
}
```

**優先順位**
- Agent設定のMCPサーバー > レガシーMCP設定
- 同名のサーバーがある場合、Agent設定が優先

---

## 6. 使用例

### 6.1 ファイルシステムサーバー（stdio）

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/project"
      ],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

### 6.2 データベースサーバー（HTTP + OAuth）

```json
{
  "mcpServers": {
    "database": {
      "type": "http",
      "url": "https://db-mcp.example.com",
      "headers": {
        "Authorization": "Bearer ${env:DB_TOKEN}"
      },
      "oauthScopes": ["openid", "email", "database:read"],
      "oauth": {
        "redirectUri": "127.0.0.1:8080"
      },
      "timeout": 180000
    }
  }
}
```

### 6.3 複数のMCPサーバー

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/project"]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "/project"]
    },
    "database": {
      "type": "http",
      "url": "https://db-mcp.example.com",
      "headers": {
        "Authorization": "Bearer ${env:DB_TOKEN}"
      }
    }
  }
}
```

### 6.4 環境変数を使用した設定

```json
{
  "mcpServers": {
    "api-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "env": {
        "API_KEY": "${env:MY_API_KEY}",
        "API_URL": "${env:MY_API_URL}",
        "DEBUG": "false"
      }
    }
  }
}
```

---

## 7. セキュリティとプライバシー

### セキュリティ考慮事項

| 項目 | 説明 |
|------|------|
| **コマンド実行** | `command`で任意のコマンドを実行可能 |
| **環境変数** | 機密情報を環境変数で管理 |
| **HTTPヘッダー** | 認証トークンをヘッダーに含める |
| **OAuth** | OAuth認証でセキュアな認証 |
| **タイムアウト** | DoS攻撃を防ぐためのタイムアウト |

### ベストプラクティス

1. **機密情報の管理**
   - API キーは環境変数で管理（`${env:API_KEY}`）
   - トークンをファイルに直接書かない

2. **MCPサーバーの検証**
   - 信頼できるソースからのみインストール
   - 公式MCPサーバーを優先

3. **最小権限の原則**
   - 必要なスコープのみを`oauthScopes`に指定
   - 不要なサーバーは`disabled: true`で無効化

4. **タイムアウト設定**
   - 適切なタイムアウトを設定
   - 長時間実行されるツールは個別に設定

---

## 8. ライフサイクル

### 作成

**レガシーMCP設定の作成**
```bash
mkdir -p ~/.aws/amazonq
cat > ~/.aws/amazonq/mcp.json << 'EOF'
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    }
  }
}
EOF
```

**Agent設定内での作成（推奨）**
```bash
# agent.jsonのmcpServersフィールドに追加
```

### 読み込み

**読み込みタイミング**
- `q chat`コマンド実行時
- Agent設定読み込み時

**読み込み順序**
1. Agent設定の`mcpServers`フィールド
2. レガシーMCP設定（`useLegacyMcpJson: true`の場合）

### 更新

**手動更新**
- JSONファイルを直接編集
- 次回`q chat`実行時に反映

### 削除

```bash
# レガシーMCP設定の削除
rm ~/.aws/amazonq/mcp.json

# Agent設定からの削除
# agent.jsonのmcpServersフィールドから削除
```

---

## 9. トラブルシューティング

### よくある問題

#### 問題1: MCPサーバーが起動しない

**症状**
```
Failed to start MCP server 'filesystem'
```

**原因と解決方法**

| 原因 | 解決方法 |
|------|---------|
| コマンドが見つからない | `command`のパスを確認（`which npx`） |
| 引数が間違っている | `args`を確認 |
| 環境変数が設定されていない | `env`を確認、`${env:VAR}`が解決されるか確認 |
| タイムアウト | `timeout`を増やす |

#### 問題2: 環境変数が展開されない

**症状**
```
Environment variable MY_API_KEY not found
```

**解決方法**
1. 環境変数が設定されているか確認（`echo $MY_API_KEY`）
2. `${env:VAR_NAME}`構文を使用
3. Q CLIを再起動

#### 問題3: HTTPサーバーに接続できない

**症状**
```
Failed to connect to MCP server at https://example.com
```

**解決方法**

| 原因 | 解決方法 |
|------|---------|
| URLが間違っている | `url`を確認 |
| 認証エラー | `headers`の`Authorization`を確認 |
| ネットワークエラー | サーバーが起動しているか確認 |
| タイムアウト | `timeout`を増やす |

#### 問題4: OAuth認証が失敗する

**症状**
```
OAuth authentication failed
```

**解決方法**
1. `oauthScopes`が正しいか確認
2. `redirectUri`が正しいか確認
3. ブラウザでOAuth認証を完了

#### 問題5: レガシーMCP設定が読み込まれない

**症状**
```
MCP server from mcp.json not loaded
```

**解決方法**
1. Agent設定で`useLegacyMcpJson: true`を設定
2. `~/.aws/amazonq/mcp.json`が存在するか確認
3. JSON構文が正しいか確認

---

## 10. 関連ファイル

### 関連する設定ファイル

| ファイル | 関係 |
|---------|------|
| `agent.json` | Agent設定内の`mcpServers`フィールド（推奨） |
| `settings.json` | グローバル設定（MCPとは独立） |

### 関連するドキュメント

- [MCP設定ガイド](../03_configuration/04_mcp-configuration.md)
- [Agent設定ガイド](../03_configuration/03_agent-configuration.md)
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
| `crates/chat-cli/src/cli/agent/mcp_config.rs` | McpServerConfig構造体定義 |
| `crates/chat-cli/src/cli/chat/tools/custom_tool.rs` | CustomToolConfig構造体定義 |
| `schemas/agent-v1.json` ([GitHub](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json)) | JSONスキーマ定義（mcpServersフィールド） |

**コミットハッシュ**: `63278298f451fd57ee439a2614bbac6a62da3870`  
**コミット日時**: 2025-10-13 12:44:25 -0700

### 公式ドキュメント

- [Amazon Q Developer CLI 公式リポジトリ](https://github.com/aws/amazon-q-developer-cli)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [MCP Servers](https://github.com/modelcontextprotocol/servers)

---

最終更新: 2025-10-25
