# MCP設定ガイド

**最終更新**: 2025-10-11  
**対象バージョン**: v1.17.0以降

---

## 📋 このガイドについて

このドキュメントでは、Q CLIのMCP（Model Context Protocol）サーバー設定について詳しく説明します。

### 🔗 AWS公式MCPサーバー

AWS公式のMCPサーバーは以下のリポジトリで提供されています：
**[https://github.com/awslabs/mcp](https://github.com/awslabs/mcp)**

---

## 🎯 MCPとは

MCP（Model Context Protocol）は、AIモデルと外部ツールを接続するための標準プロトコルです。MCPサーバーを使用することで、Q CLIの機能を拡張できます。

### MCPでできること
- 外部APIとの連携
- データベースアクセス
- カスタムツールの追加
- サードパーティサービスとの統合

---

## 📁 MCP設定の配置場所

### Agent設定内に記述

```json
{
  "name": "my-agent",
  "mcpServers": {
    "server-name": {
      // MCP設定
    }
  }
}
```

### レガシーMCP設定（後方互換性）

```
~/.aws/amazonq/mcp.json          # グローバル
<workspace>/.amazonq/mcp.json    # ローカル
```

**注意**: レガシーMCP設定は後方互換性のために維持されています。Agent設定の`useLegacyMcpJson: true`で有効化できます。

---

## 🔧 MCP設定スキーマ

### 基本構造

```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "実行コマンド",
      "args": ["引数"],
      "env": {"環境変数": "値"},
      "timeout": 120000,
      "disabled": false
    }
  }
}
```

### 設定項目

| フィールド | 型 | デフォルト | 必須 | 説明 |
|-----------|-----|-----------|------|------|
| `type` | "stdio" \| "http" | "stdio" | No | トランスポートタイプ |
| `url` | string | "" | No | HTTPサーバーのURL |
| `headers` | object | {} | No | HTTPヘッダー |
| `oauthScopes` | array | ["openid", "email", "profile", "offline_access"] | No | OAuth スコープ |
| `command` | string | "" | Yes | 起動コマンド |
| `args` | array | [] | No | コマンド引数 |
| `env` | object | null | No | 環境変数 |
| `timeout` | integer | 120000 | No | タイムアウト（ミリ秒） |
| `disabled` | boolean | false | No | 無効化フラグ |

---

## 📝 トランスポートタイプ

### stdio（標準入出力）

ローカルプロセスとの通信に使用します。

```json
{
  "mcpServers": {
    "local-tool": {
      "type": "stdio",
      "command": "node",
      "args": ["./mcp-server.js"]
    }
  }
}
```

### HTTP

リモートサーバーとの通信に使用します。

```json
{
  "mcpServers": {
    "remote-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${env:API_TOKEN}"
      }
    }
  }
}
```

---

## 🔐 環境変数の使用

### 基本的な使い方

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com",
      "headers": {
        "Authorization": "token ${env:GITHUB_TOKEN}"
      }
    }
  }
}
```

### 環境変数の設定

```bash
# シェルで設定
export GITHUB_TOKEN="your-token-here"

# または.envファイルで管理
echo "GITHUB_TOKEN=your-token-here" >> .env
```

### env設定

```json
{
  "mcpServers": {
    "custom-tool": {
      "type": "stdio",
      "command": "python",
      "args": ["tool.py"],
      "env": {
        "API_KEY": "${env:MY_API_KEY}",
        "DEBUG": "true"
      }
    }
  }
}
```

---

## 🔑 OAuth設定

### OAuth対応MCPサーバー

```json
{
  "mcpServers": {
    "oauth-service": {
      "type": "http",
      "url": "https://api.service.com",
      "oauthScopes": [
        "openid",
        "email",
        "profile",
        "offline_access",
        "custom_scope"
      ]
    }
  }
}
```

### OAuth認証フロー

1. Amazon Q CLIがブラウザを開く
2. ユーザーが認証
3. トークンが自動的に管理される

---

## ⏱️ タイムアウト設定

### デフォルトタイムアウト

```json
{
  "mcpServers": {
    "slow-service": {
      "type": "http",
      "url": "https://slow-api.example.com",
      "timeout": 300000  // 5分
    }
  }
}
```

### タイムアウトの推奨値

- **高速API**: 30000（30秒）
- **通常API**: 120000（2分、デフォルト）
- **低速API**: 300000（5分）

---

## 🎨 設定例

### AWS Documentation MCP Server（推奨）

```json
{
  "name": "aws-docs-agent",
  "mcpServers": {
    "awslabs.aws-documentation-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@1.1.8"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_DOCUMENTATION_PARTITION": "aws"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

> **⚠️ 重要: uvxキャッシュによるストレージ逼迫に注意**
>
> **問題**: `@latest`を使用すると、MCPサーバー起動のたびに新しいキャッシュが作成され、ストレージを圧迫します（1サーバーあたり約30MB/回）。
>
> **原因**: uvxは実行時に仮想環境をキャッシュディレクトリ（`~/.cache/uv`）に作成しますが、`@latest`指定時はキャッシュが再利用されず、毎回新規作成されます。
>
> **対策（いずれかを選択）**:
>
> 1. **バージョンを明示する（推奨）**
>    ```json
>    "args": ["awslabs.aws-documentation-mcp-server@1.1.8"]
>    ```
>    - キャッシュが再利用され、ストレージ消費を抑制
>    - バージョン更新時は手動で変更が必要
>
> 2. **定期的にキャッシュをクリーンアップ**
>    ```bash
>    # 未使用キャッシュを削除
>    uv cache prune
>    
>    # すべてのキャッシュを削除
>    uv cache clean
>    
>    # crontabで1時間ごとに自動実行（例）
>    1 * * * * /path/to/uv cache prune
>    ```
>
> **キャッシュ確認方法**:
> ```bash
> # キャッシュディレクトリの場所を確認
> uv cache dir
> 
> # キャッシュサイズを確認
> du -sh ~/.cache/uv
> ```
>
> 参考: [uvxでローカルMCPサーバーを利用する場合はキャッシュによるストレージ逼迫にご注意ください](https://blog.serverworks.co.jp/warnings-to-use-local-mcp)

### AWS Knowledge MCP Server（リモート）

```json
{
  "name": "aws-knowledge-agent",
  "mcpServers": {
    "aws-knowledge-mcp-server": {
      "url": "https://knowledge-mcp.global.api.aws"
    }
  }
}
```

### GitHub API連携

```json
{
  "name": "github-agent",
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com",
      "headers": {
        "Authorization": "token ${env:GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
      },
      "timeout": 60000
    }
  }
}
```

### ローカルPythonツール

```json
{
  "name": "python-tools",
  "mcpServers": {
    "data-processor": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "env": {
        "PYTHONPATH": "${env:HOME}/my-tools"
      }
    }
  }
}
```

### 複数MCPサーバー

```json
{
  "name": "multi-service",
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com",
      "headers": {
        "Authorization": "token ${env:GITHUB_TOKEN}"
      }
    },
    "slack": {
      "type": "http",
      "url": "https://slack.com/api",
      "headers": {
        "Authorization": "Bearer ${env:SLACK_TOKEN}"
      }
    },
    "local-db": {
      "type": "stdio",
      "command": "node",
      "args": ["./db-mcp-server.js"]
    }
  }
}
```

---

## 🔄 MCPサーバーの管理

### MCPサーバーの確認

```bash
# Agent設定を確認
q agent show my-agent
```

### MCPサーバーの無効化

```json
{
  "mcpServers": {
    "temporary-disabled": {
      "type": "stdio",
      "command": "node",
      "args": ["server.js"],
      "disabled": true  // 一時的に無効化
    }
  }
}
```

---

## ベストプラクティス

詳細なベストプラクティスは以下を参照してください：
- [設定のベストプラクティス](../best-practices/configuration.md)
- [セキュリティベストプラクティス](../best-practices/security.md)
- [パフォーマンス最適化](../best-practices/performance.md)

---

## トラブルシューティング

MCP設定に関する問題が発生した場合は、[トラブルシューティングガイド](../troubleshooting/common-issues.md)を参照してください。

**関連トピック**:
- [MCP設定のトラブルシューティング](../troubleshooting/common-issues.md#mcp設定)
- [Agent設定のトラブルシューティング](../troubleshooting/common-issues.md#agent設定)
- [よくある質問](../troubleshooting/faq.md)

---

## 設定例

基本的な設定例については、[設定例集](examples.md)を参照してください。

**主な設定例**:
- Agent設定の実践例
- MCP設定の実践例
- ユースケース別設定
- セキュリティ設定

---
## 📚 関連ドキュメント

- **[Agent設定](agent-configuration.md)** - Agent設定の詳細
- **[環境変数](environment-variables.md)** - 環境変数の使い方
- **[設定例集](examples.md)** - 実践的な設定例

---

---

## 🔗 外部リンク

- [MCP 公式サイト](https://modelcontextprotocol.io/)
- [MCP GitHub](https://github.com/modelcontextprotocol)
- [Amazon Q CLI GitHub](https://github.com/aws/amazon-q-developer-cli)

---

**作成日**: 2025-10-11  
**最終更新日**: 2025-10-11
