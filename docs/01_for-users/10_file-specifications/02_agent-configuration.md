# Agent設定ファイル (agent.json) 仕様書

[ホーム](../../../README.md) > [ユーザー向けドキュメント](../../README.md) > [ファイル仕様](README.md) > Agent設定

---

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **ファイル名** | `agent.json` |
| **ファイル形式** | JSON |
| **エンコーディング** | UTF-8 |
| **改行コード** | LF (Unix形式) |
| **JSONスキーマ** | `schemas/agent-v1.json` |
| **スキーマバージョン** | JSON Schema Draft-07 |

### ファイル配置場所

| 種別 | パス | 説明 |
|------|------|------|
| **グローバルAgent** | `~/.aws/amazonq/agents/*.json` | 全プロジェクトで使用可能 |
| **ワークスペースAgent** | `./.amazonq/agents/*.json` | プロジェクト固有 |
| **サンプル** | `~/.aws/amazonq/agents/example.example.json` | 自動生成されるサンプル |

**注意**: `.example.json`拡張子のファイルは読み込まれません。

---

## 2. 目的と役割

### 目的

Agent設定ファイルは、Q CLIの動作を宣言的にカスタマイズするための設定ファイルです。

### 主な役割

| 役割 | 説明 |
|------|------|
| **コンテキスト管理** | プロンプト、リソースファイルの指定 |
| **ツール管理** | 使用可能なツール、許可ツールの制御 |
| **MCP統合** | MCPサーバーの設定と管理 |
| **フック実行** | イベント発生時のコマンド実行 |
| **モデル選択** | 使用するAIモデルの指定 |

### 使用場面

- プロジェクト固有のコンテキストを設定したい
- 特定のツールのみを許可したい
- MCPサーバーを統合したい
- カスタムプロンプトを使用したい
- 特定のモデルを使用したい

---

## 3. ファイル構造

### 最小構成

```json
{
  "name": "my-agent"
}
```

**必須フィールド**: `name`のみ

### 完全な構成例

```json
{
  "$schema": "https://github.com/aws/amazon-q-developer-cli/blob/main/schemas/agent-v1.json",
  "name": "my-project-agent",
  "description": "プロジェクト専用のAgent設定",
  "prompt": "あなたはPythonの専門家です。",
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  },
  "tools": ["*"],
  "toolAliases": {
    "fs_read": "read_file"
  },
  "allowedTools": ["fs_read", "fs_write", "@filesystem/read_file"],
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ],
  "hooks": {
    "agentSpawn": [
      {
        "command": "echo 'Agent起動'"
      }
    ]
  },
  "toolsSettings": {
    "fs_read": {
      "allowedPaths": ["/path/to/project"]
    }
  },
  "useLegacyMcpJson": false,
  "model": "anthropic.claude-3-5-sonnet-20241022-v2:0"
}
```

---

## 4. フィールド仕様

### 4.1 基本フィールド

| フィールド名 | 型 | 必須 | デフォルト | 説明 |
|------------|-----|------|----------|------|
| `$schema` | string | ❌ | - | JSONスキーマURL |
| `name` | string | ✅ | - | Agent名（一意である必要がある） |
| `description` | string/null | ❌ | null | Agent説明（ユーザー向け） |
| `prompt` | string/null | ❌ | null | システムプロンプト（file://サポート） |
| `model` | string/null | ❌ | null | モデルID |

#### promptフィールドの詳細

**インラインテキスト**
```json
{
  "prompt": "あなたはPythonの専門家です。"
}
```

**file:// URI参照**
```json
{
  "prompt": "file://./my-prompt.md"
}
```

- 相対パス: Agent設定ファイルからの相対パス
- 絶対パス: システムの絶対パス
- ファイルが見つからない場合: エラー

### 4.2 mcpServersフィールド

MCPサーバーの設定を定義します。

**構造**
```json
{
  "mcpServers": {
    "サーバー名": {
      "type": "stdio",
      "command": "コマンド",
      "args": ["引数1", "引数2"],
      "env": {
        "環境変数名": "値"
      },
      "timeout": 120000,
      "disabled": false
    }
  }
}
```

**各MCPサーバーのフィールド**

| フィールド名 | 型 | 必須 | デフォルト | 説明 |
|------------|-----|------|----------|------|
| `type` | "stdio"/"http" | ❌ | "stdio" | トランスポート種別 |
| `url` | string | ❌ | "" | HTTPエンドポイント（type="http"時） |
| `headers` | object | ❌ | {} | HTTPヘッダー（type="http"時） |
| `oauthScopes` | array[string] | ❌ | ["openid","email","profile","offline_access"] | OAuthスコープ |
| `oauth` | object/null | ❌ | - | OAuth設定 |
| `command` | string | ✅ | - | 起動コマンド |
| `args` | array[string] | ❌ | [] | コマンド引数 |
| `env` | object/null | ❌ | - | 環境変数 |
| `timeout` | integer | ❌ | 120000 | タイムアウト（ミリ秒） |
| `disabled` | boolean | ❌ | false | 無効化フラグ |

**環境変数展開**

`env`フィールドでは`${env:VAR_NAME}`構文で環境変数を参照できます。

```json
{
  "env": {
    "API_KEY": "${env:MY_API_KEY}"
  }
}
```

### 4.3 toolsフィールド

使用可能なツールを指定します。

| 値 | 説明 |
|----|------|
| `"*"` | 全てのツール |
| `"@builtin"` | ビルトインツールのみ |
| `"@サーバー名"` | 特定のMCPサーバーの全ツール |
| `"@サーバー名/ツール名"` | 特定のMCPサーバーの特定ツール |
| `"ツール名"` | ビルトインツール名 |

**例**
```json
{
  "tools": [
    "*",
    "@filesystem",
    "@filesystem/read_file",
    "fs_read"
  ]
}
```

### 4.4 toolAliasesフィールド

ツール名のエイリアスを定義します。

**構造**
```json
{
  "toolAliases": {
    "元のツール名": "新しいツール名"
  }
}
```

**MCPツールの場合**
```json
{
  "toolAliases": {
    "@filesystem/read_file": "read"
  }
}
```

### 4.5 allowedToolsフィールド

明示的に許可するツールを指定します。

**特徴**
- 重複不可（uniqueItems: true）
- 空配列の場合: 全てのツールが許可される
- 指定した場合: 指定したツールのみ許可

**デフォルト許可ツール**

ソースコードより、以下のツールがデフォルトで許可されています：

```typescript
// DEFAULT_APPROVE定義より
const DEFAULT_APPROVE = [
  // 実際の値はソースコード参照
];
```

### 4.6 resourcesフィールド

コンテキストに含めるファイルを指定します。

**制約**
- 全て`file://`で始まる必要がある
- グロブパターン（`**/*.md`）をサポート
- 相対パス: Agent設定ファイルからの相対パス

**例**
```json
{
  "resources": [
    "file://README.md",
    "file://docs/**/*.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

**デフォルトリソース**

```json
[
  "file://AmazonQ.md",
  "file://AGENTS.md",
  "file://README.md",
  "file://.amazonq/rules/**/*.md"
]
```

### 4.7 hooksフィールド

イベント発生時に実行するコマンドを定義します。

**フック種別**

| フック名 | 発生タイミング |
|---------|-------------|
| `userPromptSubmit` | ユーザーがプロンプトを送信した時 |
| `agentSpawn` | Agentが起動した時 |

**構造**
```json
{
  "hooks": {
    "agentSpawn": [
      {
        "command": "echo 'Agent起動'"
      }
    ],
    "userPromptSubmit": [
      {
        "command": "echo 'プロンプト送信'"
      }
    ]
  }
}
```

### 4.8 toolsSettingsフィールド

ツール固有の設定を定義します。

**構造**
```json
{
  "toolsSettings": {
    "ツール名": {
      "設定項目": "値"
    }
  }
}
```

**例: fs_read/fs_writeの設定**
```json
{
  "toolsSettings": {
    "fs_read": {
      "allowedPaths": ["/path/to/project"]
    },
    "fs_write": {
      "allowedPaths": ["/path/to/project"]
    }
  }
}
```

### 4.9 useLegacyMcpJsonフィールド

レガシーMCP設定（`~/.aws/amazonq/mcp.json`）を統合するかを制御します。

| 値 | 説明 |
|----|------|
| `true` | レガシーMCP設定を統合 |
| `false` | レガシーMCP設定を無視（デフォルト） |

**注意**: Agent設定とレガシーMCP設定で同名のサーバーがある場合、Agent設定が優先されます。

---

## 5. ファイル操作

### 5.1 読み込み処理

**処理フロー**

1. ファイル読み込み
2. JSONパース
3. スキーマ検証
4. Cold→Warm変換（`thaw()`）
   - `path`フィールドの設定
   - `prompt`のfile:// URI解決
   - レガシーMCP統合（`useLegacyMcpJson=true`の場合）

**ソースコード参照**
- ファイル: `crates/chat-cli/src/cli/agent/mod.rs`
- 関数: `Agent::load()` (行375-405)

### 5.2 書き込み処理

**処理フロー**

1. Warm→Cold変換（`freeze()`）
   - レガシーMCPサーバーを除外
2. JSON生成（pretty print）
3. ファイル書き込み

### 5.3 検証処理

**JSONスキーマ検証**

- スキーマファイル: `schemas/agent-v1.json`
- 検証ライブラリ: `jsonschema` crate
- 検証タイミング: ファイル読み込み時

**検証エラー例**

```
Agent config is malformed at /name: 'name' is a required property
```

---

## 6. 使用例

### 6.1 基本的なAgent

```json
{
  "name": "basic-agent",
  "description": "基本的なAgent設定",
  "prompt": "あなたは親切なアシスタントです。"
}
```

### 6.2 MCPサーバーを使用するAgent

```json
{
  "name": "mcp-agent",
  "description": "MCPサーバーを使用するAgent",
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
    }
  },
  "tools": ["@filesystem"],
  "allowedTools": ["@filesystem/read_file", "@filesystem/write_file"]
}
```

### 6.3 プロジェクト固有のAgent

```json
{
  "name": "python-project",
  "description": "Pythonプロジェクト用Agent",
  "prompt": "file://./agent-prompt.md",
  "resources": [
    "file://README.md",
    "file://docs/**/*.md",
    "file://.amazonq/rules/**/*.md"
  ],
  "toolsSettings": {
    "fs_read": {
      "allowedPaths": ["/path/to/project"]
    },
    "fs_write": {
      "allowedPaths": ["/path/to/project"]
    }
  }
}
```

### 6.4 カスタムモデルを使用するAgent

```json
{
  "name": "custom-model-agent",
  "description": "カスタムモデルを使用するAgent",
  "model": "anthropic.claude-3-5-sonnet-20241022-v2:0"
}
```

---

## 7. セキュリティとプライバシー

### セキュリティ考慮事項

| 項目 | 説明 |
|------|------|
| **ファイルアクセス** | `resources`で指定したファイルがコンテキストに含まれる |
| **ツール実行** | `allowedTools`で許可したツールのみ実行可能 |
| **MCPサーバー** | 任意のコマンドを実行可能（信頼できるサーバーのみ使用） |
| **環境変数** | `env`フィールドで環境変数を設定可能 |
| **フック** | 任意のコマンドを実行可能（信頼できるコマンドのみ使用） |

### ベストプラクティス

1. **最小権限の原則**
   - 必要なツールのみを`allowedTools`に指定
   - `fs_read`/`fs_write`の`allowedPaths`を制限

2. **機密情報の保護**
   - API キーは環境変数で管理（`${env:API_KEY}`）
   - 機密ファイルを`resources`に含めない

3. **MCPサーバーの検証**
   - 信頼できるソースからのみインストール
   - `disabled: true`で一時的に無効化可能

---

## 8. ライフサイクル

### 作成

**自動作成**
- Q CLI初回起動時に`example.example.json`が自動生成される

**手動作成**
```bash
# グローバルAgent
mkdir -p ~/.aws/amazonq/agents
cat > ~/.aws/amazonq/agents/my-agent.json << 'EOF'
{
  "name": "my-agent"
}
EOF

# ワークスペースAgent
mkdir -p .amazonq/agents
cat > .amazonq/agents/project-agent.json << 'EOF'
{
  "name": "project-agent"
}
EOF
```

### 読み込み

**読み込みタイミング**
- `q chat`コマンド実行時
- `q chat --agent <agent-name>`で特定のAgentを指定

**読み込み順序**
1. ワークスペースAgent（`./.amazonq/agents/*.json`）
2. グローバルAgent（`~/.aws/amazonq/agents/*.json`）

### 更新

**手動更新**
- JSONファイルを直接編集
- 次回`q chat`実行時に反映

**プログラム更新**
```bash
q agent edit --name <agent-name>
```

### 削除

```bash
# グローバルAgent
rm ~/.aws/amazonq/agents/my-agent.json

# ワークスペースAgent
rm .amazonq/agents/project-agent.json
```

---

## 9. トラブルシューティング

### よくある問題

#### 問題1: Agent設定が読み込まれない

**症状**
```
Agent 'my-agent' not found
```

**原因と解決方法**

| 原因 | 解決方法 |
|------|---------|
| ファイル名が`.json`で終わっていない | `.json`拡張子に変更 |
| `.example.json`拡張子になっている | `.json`に変更 |
| ファイルが正しいディレクトリにない | `~/.aws/amazonq/agents/`または`./.amazonq/agents/`に配置 |

#### 問題2: JSON構文エラー

**症状**
```
Json supplied at /path/to/agent.json is invalid: expected `,` or `}` at line 5 column 3
```

**解決方法**
1. JSONリンターで検証（`jq . agent.json`）
2. 構文エラーを修正
3. 再度実行

#### 問題3: スキーマ検証エラー

**症状**
```
Agent config is malformed at /name: 'name' is a required property
```

**解決方法**
1. 必須フィールド（`name`）を追加
2. フィールド名のスペルを確認（camelCase）
3. スキーマファイル（`schemas/agent-v1.json`）を参照

#### 問題4: file:// URIが解決できない

**症状**
```
File URI not found: file://./my-prompt.md (resolved to /path/to/my-prompt.md)
```

**解決方法**
1. ファイルが存在するか確認
2. パスが正しいか確認（相対パスはAgent設定ファイルからの相対パス）
3. ファイルの読み取り権限を確認

#### 問題5: MCPサーバーが起動しない

**症状**
```
Failed to start MCP server 'filesystem'
```

**解決方法**

| 原因 | 解決方法 |
|------|---------|
| コマンドが見つからない | `command`のパスを確認 |
| 引数が間違っている | `args`を確認 |
| タイムアウト | `timeout`を増やす |
| 環境変数が設定されていない | `env`を確認 |

---

## 10. 関連ファイル

### 関連する設定ファイル

| ファイル | 関係 |
|---------|------|
| `mcp.json` | レガシーMCP設定（`useLegacyMcpJson`で統合） |
| `settings.json` | グローバル設定（Agentより優先度が低い） |
| `.cli_bash_history` | コマンド履歴（Agentとは独立） |

### 関連するドキュメント

- [Agent設定ガイド](../03_configuration/03_agent-configuration.md)
- [MCP設定ガイド](../03_configuration/04_mcp-configuration.md)
- [設定優先順位](../03_configuration/07_priority-rules.md)

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
| `crates/chat-cli/src/cli/agent/mod.rs` | Agent構造体定義、読み込み/書き込み処理 |
| `schemas/agent-v1.json` | JSONスキーマ定義 |

**コミットハッシュ**: `63278298f451fd57ee439a2614bbac6a62da3870`  
**コミット日時**: 2025-10-13 12:44:25 -0700

### 公式ドキュメント

- [Amazon Q Developer CLI 公式リポジトリ](https://github.com/aws/amazon-q-developer-cli)
- [Agent設定ガイド](https://github.com/aws/amazon-q-developer-cli/blob/main/docs/AGENTS.md)

---

**最終更新**: 2025-10-25  
**ドキュメントバージョン**: 1.0
