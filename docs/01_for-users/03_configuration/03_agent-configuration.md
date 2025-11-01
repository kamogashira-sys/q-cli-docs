[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [設定ガイド](README.md) > 04 Agent Configuration

---

# Agent設定

**ドキュメント対象バージョン**: v1.13.0以降

> **Note**: 本サイトではv1.13.0以降のAgent設定を対象に記述しています。

---

## 📋 このガイドについて

このドキュメントでは、Q CLIのAgent設定について詳しく説明します。Agentは、Q CLIの動作をカスタマイズするための強力な機能です。

---

## 🎯 Agentとは

Agentは、Q CLIの動作を定義する設定ファイルです。以下をカスタマイズできます：

- システムプロンプト
- 利用可能なツール
- MCPサーバーとの連携
- リソースファイル
- フック（イベントハンドラ）

---

## 📁 Agent設定ファイルの配置場所

### グローバルAgent（ユーザー全体）
```
~/.aws/amazonq/cli-agents/
└── my-agent.json
```

### ローカルAgent（プロジェクト固有）
```
<project-root>/.amazonq/cli-agents/
└── my-agent.json
```

### 優先順位
1. **ローカルAgent**: `.amazonq/cli-agents/`（最優先）
2. **グローバルAgent**: `~/.aws/amazonq/cli-agents/`

同名のAgentが存在する場合、ローカルAgentが優先されます。

---

## 📝 Agent設定ファイルの形式

### ファイル形式
- **形式**: JSON
- **ファイル名**: `<agent-name>.json`
- **文字コード**: UTF-8

### スキーマ
```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json"
}
```

---

## 🔧 Agent設定スキーマ

### 必須フィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `name` | string | Agent名（ファイル名と一致させる） |

### オプションフィールド

| フィールド | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `$schema` | string | - | スキーマURL |
| `description` | string | null | Agent説明 |
| `prompt` | string | null | システムプロンプト。文字列または `file://` URIで外部ファイルを参照可能（v1.19.0+） |
| `mcpServers` | object | {} | MCPサーバー設定（[詳細](#mcpservers設定)） |
| `tools` | array | [] | 利用可能ツール一覧。`@{SERVER}/tool`形式でMCPツールを指定 |
| `toolAliases` | object | {} | ツール名エイリアス |
| `allowedTools` | array | [] | 明示的に許可されたツール一覧 |
| `resources` | array | [] | リソースファイル（`file://`形式、[詳細](../08_guides/README.md)） |
| `hooks` | object | {} | フック設定（`userPromptSubmit`, `agentSpawn`, `preToolUse`, `postToolUse`, `stop`） |
| `toolsSettings` | object | {} | ツール固有設定 |
| `useLegacyMcpJson` | boolean | false | レガシーMCP設定（`~/.aws/amazonq/mcp.json`）の使用 |
| `model` | string | null | 使用モデルID |

#### mcpServers設定

MCPサーバーの詳細設定：

| フィールド | 型 | デフォルト | 必須 | 説明 |
|-----------|-----|-----------|------|------|
| `type` | string | "stdio" | No | トランスポートタイプ（`stdio` or `http`） |
| `command` | string | - | Yes | 起動コマンド |
| `args` | array | [] | No | コマンド引数 |
| `env` | object | null | No | 環境変数 |
| `url` | string | "" | No | HTTPエンドポイント（type=httpの場合） |
| `headers` | object | {} | No | HTTPヘッダー（type=httpの場合） |
| `oauth` | object | null | No | OAuth設定 |
| `oauth.redirectUri` | string | null | No | リダイレクトURI（例: "127.0.0.1:7778"） |
| `oauthScopes` | array | ["openid", "email", "profile", "offline_access"] | No | OAuthスコープ |
| `timeout` | integer | 120000 | No | タイムアウト（ミリ秒） |
| `disabled` | boolean | false | No | 無効化フラグ |

---

## 📄 基本的なAgent設定例

### シンプルなAgent

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "my-assistant",
  "description": "汎用アシスタント",
  "prompt": "あなたは親切で知識豊富なアシスタントです。"
}
```

### プロンプトの外部ファイル化（v1.19.0+）

長く複雑なプロンプトは、外部ファイルとして管理できます。

#### 基本的な使い方

**従来の方法（インラインプロンプト）**:
```json
{
  "name": "my-agent",
  "prompt": "あなたは親切で知識豊富なアシスタントです。"
}
```

**新機能（File URI参照）**:
```json
{
  "name": "my-agent",
  "prompt": "file://./prompts/system.txt"
}
```

#### パス解決ルール

##### 1. 相対パス
Agent設定ファイル（.json）のディレクトリを基準に解決されます。

```json
{
  "prompt": "file://./prompt.md"
}
```
→ Agent設定ファイルと同じディレクトリの`prompt.md`

```json
{
  "prompt": "file://../shared/prompt.md"
}
```
→ 親ディレクトリの`shared/prompt.md`

##### 2. 絶対パス
そのまま使用されます。

```json
{
  "prompt": "file:///home/user/prompts/agent.md"
}
```

#### 実用例

##### 例1: プロジェクト内のプロンプト管理

**ディレクトリ構造**:
```
~/.aws/amazonq/cli-agents/
├── aws-expert.json
└── prompts/
    └── aws-expert.md
```

**Agent設定ファイル（aws-expert.json）**:
```json
{
  "name": "aws-expert",
  "description": "AWS infrastructure specialist",
  "prompt": "file://./prompts/aws-expert.md"
}
```

**プロンプトファイル（aws-expert.md）**:
```markdown
# AWS Infrastructure Expert

あなたは経験豊富なAWSインフラストラクチャスペシャリストです。

## 専門分野
- EC2、Lambda、ECS/Fargateなどのコンピューティングサービス
- VPC、Route 53、CloudFrontなどのネットワーキング
- IAM、Security Groups、NACLなどのセキュリティ

## 回答方針
1. AWSのベストプラクティスに基づいて回答
2. コスト最適化を考慮
3. セキュリティを最優先
4. 具体的なコード例を提供
```

##### 例2: 共有プロンプトの利用

複数のAgentで同じプロンプトを共有:

```json
// agent1.json
{
  "name": "agent1",
  "prompt": "file://../shared/base-prompt.md"
}

// agent2.json
{
  "name": "agent2",
  "prompt": "file://../shared/base-prompt.md"
}
```

##### 例3: チーム間でのプロンプト共有

```json
{
  "prompt": "file:///team/shared-prompts/standard-agent.md"
}
```

#### メリット

- ✅ **可読性**: 長いプロンプトをMarkdownファイルで管理
- ✅ **保守性**: バージョン管理、編集が容易
- ✅ **再利用性**: 複数Agentでプロンプトを共有
- ✅ **柔軟性**: 相対パス・絶対パスの両方をサポート
- ✅ **互換性**: 既存のインラインプロンプトも引き続き動作

#### ベストプラクティス

##### 1. ファイル配置

**推奨構造**:
```
~/.aws/amazonq/cli-agents/
├── my-agent.json
└── prompts/
    ├── my-agent.md
    ├── shared-context.md
    └── templates/
        └── base.md
```

##### 2. プロンプトファイルの命名

- Agent名と一致させる: `aws-expert.json` → `aws-expert.md`
- 用途を明確にする: `rust-debugging.md`, `aws-security.md`

##### 3. バージョン管理

```bash
# プロンプトファイルをGit管理
cd ~/.aws/amazonq/cli-agents/prompts
git init
git add *.md
git commit -m "Initial prompt templates"
```

##### 4. 相対パスの活用

```json
{
  "prompt": "file://./prompts/agent.md"  // ✅ 推奨
}
```

絶対パスは環境依存になるため、可能な限り相対パスを使用。

#### promptとresourcesの違い

| 項目 | prompt | resources |
|------|--------|-----------|
| **相対パスの基準** | Agent設定ファイルのディレクトリ | 作業ディレクトリ（cwd） |
| **Glob対応** | ❌ 非対応 | ✅ 対応（`**/*.md`など） |
| **用途** | 単一プロンプトファイル参照 | 複数リソースファイル参照 |
| **複数ファイル** | ❌ 非対応 | ✅ 対応 |

#### エラーハンドリング

ファイルが見つからない場合、明確なエラーメッセージが表示されます:

```
Error: File not found: /path/to/prompt.md
```

**よくあるエラー**:
- 無効なURI形式（`http://`など）
- ファイルが存在しない
- ファイル読み込み権限がない

#### 注意事項

1. **後方互換性**: インラインプロンプトは引き続きサポート
2. **セキュリティ**: ファイルシステムへのアクセス権限が必要
3. **Glob非対応**: ワイルドカード（`*`, `?`）は使用不可

---

### ツールを制限したAgent

```json
{
  "name": "readonly-assistant",
  "description": "読み取り専用アシスタント",
  "tools": ["fs_read", "execute_bash"],
  "allowedTools": ["fs_read"]
}
```

---

## 🛠️ ツール設定

### ツール指定（tools）

利用可能なツールを指定します。

```json
{
  "tools": [
    "fs_read",
    "fs_write",
    "execute_bash",
    "use_aws"
  ]
}
```

### 自動承認ツール（allowedTools）

ユーザーの承認なしで自動実行されるツールを指定します。

```json
{
  "allowedTools": [
    "fs_read",
    "list_directory"
  ]
}
```

### ワイルドカードパターン

```json
{
  "allowedTools": [
    "fs_*",           // fs_read, fs_write等すべて
    "*_read",         // 読み取り系すべて
    "execute_*"       // 実行系すべて
  ]
}
```

**注意**: ワイルドカードは慎重に使用してください。

---

## 📚 リソース設定

Agentが参照できるファイルを指定します。

```json
{
  "resources": [
    {
      "type": "file",
      "path": "docs/README.md",
      "description": "プロジェクトのREADME"
    },
    {
      "type": "directory",
      "path": "src/",
      "description": "ソースコード"
    }
  ]
}
```

---

## 🪝 フック設定

特定のイベント時に実行される処理を定義します。

### 利用可能なフック

| フック名 | タイミング | 説明 |
|---------|-----------|------|
| `AgentSpawn` | Agent起動時 | Agent生成時にトリガー |
| `UserPromptSubmit` | ユーザーメッセージ送信時 | ユーザーメッセージ送信ごとにトリガー |
| `PreToolUse` | ツール実行前 | ツール実行前にトリガー |
| `PostToolUse` | ツール実行後 | ツール実行後にトリガー |
| `Stop` | アシスタント応答完了時 | アシスタントの応答完了時にトリガー |

#### フックの詳細仕様

##### AgentSpawn
- **タイミング**: Agent起動時（1回のみ）
- **用途**: 環境初期化、設定検証、依存関係チェック
- **終了コード**: 0=成功、その他=失敗（Agent起動中止）

##### UserPromptSubmit
- **タイミング**: ユーザーがプロンプトを送信した直後
- **用途**: プロンプト検証、コンテキスト追加、ログ記録
- **終了コード**: 0=成功、その他=失敗（プロンプト処理中止）

##### PreToolUse
- **タイミング**: ツール実行直前
- **用途**: ツール実行の許可/拒否、パラメータ検証、セキュリティチェック
- **終了コード**: 0=許可、2=ブロック、その他=失敗

##### PostToolUse
- **タイミング**: ツール実行直後
- **用途**: 結果の検証、ログ記録、後処理
- **終了コード**: 0=成功、その他=失敗

##### Stop
- **タイミング**: アシスタント応答完了時（会話ターン終了時）
- **用途**: コンパイル、テスト実行、コードフォーマット、クリーンアップ処理
- **終了コード**: 0=成功、その他=警告として表示

#### フック設定項目

各フックで設定可能な項目：

| 項目 | 型 | デフォルト | 説明 |
|------|----|-----------|----- |
| `command` | string | - | 実行するコマンド（必須） |
| `timeout_ms` | number | 30000 | タイムアウト時間（ミリ秒） |
| `max_output_size` | number | 10240 | 最大出力サイズ（バイト） |
| `cache_ttl_seconds` | number | 0 | キャッシュ有効期限（秒、0=無効） |
| `matcher` | string | - | ツール名マッチングパターン（preToolUse/postToolUseのみ） |

#### Tool Matcher

Tool Matcherは、どのツールに対してHookを実行するかを指定します：

**サポートされるパターン**:
- `fs_*`: ワイルドカード（すべてのファイルシステムツール）
- `@git`: MCPサーバー全体
- `@git/status`: MCPサーバーの特定ツール
- `execute_bash`: 特定ツール
- `fs_write`: 特定ツール
- `use_aws`: 特定ツール

**主要ツール名一覧**:
- **ファイル操作**: `fs_read`, `fs_write`
- **実行系**: `execute_bash`, `use_aws`
- **MCP**: `@{server_name}`, `@{server_name}/{tool_name}`

**Globパターン詳細**:
- `*`: 任意の文字列
- `?`: 任意の1文字
- `[abc]`: 文字クラス
- `{a,b}`: 選択肢

**設定例**:
```json
{
  "hooks": {
    "preToolUse": [
      {
        "matcher": "fs_*",
        "command": "./scripts/check-file-access.sh",
        "timeout_ms": 5000,
        "cache_ttl_seconds": 60
      },
      {
        "matcher": "@git",
        "command": "./scripts/check-git-access.sh",
        "max_output_size": 2048
      },
      {
        "matcher": "execute_bash",
        "command": "./scripts/security-scan.sh",
        "timeout_ms": 10000
      }
    ]
  }
}
```

#### キャッシング機能

重複実行を回避するためのキャッシング機能：

```json
{
  "hooks": {
    "preToolUse": [
      {
        "matcher": "fs_*",
        "command": "./scripts/expensive-check.sh",
        "cache_ttl_seconds": 300,
        "timeout_ms": 15000
      }
    ]
  }
}
```

- **cache_ttl_seconds**: キャッシュの有効期限（秒、デフォルト: 0）
- **用途**: 高コストな処理の重複実行を回避

#### タイムアウト制御

```json
{
  "hooks": {
    "preToolUse": [
      {
        "matcher": "execute_bash",
        "command": "./scripts/security-scan.sh",
        "timeout_ms": 5000,
        "max_output_size": 4096
      }
    ]
  }
}
```

- **デフォルト**: 30,000ms（30秒）
- **timeout_ms**: ミリ秒単位でタイムアウトを指定
- **max_output_size**: 出力サイズ制限（デフォルト: 10,240バイト）

#### 環境変数

Hookスクリプトで利用可能な環境変数：

| 環境変数 | 説明 | 例 |
|---------|------|-----|
| `Q_HOOK_TRIGGER` | トリガータイプ | `PreToolUse` |
| `Q_HOOK_TOOL_NAME` | ツール名 | `fs_write` |
| `Q_HOOK_TOOL_PARAMS` | ツールパラメータ（JSON） | `{"path": "/tmp/file.txt"}` |

**使用例**:
```bash
#!/bin/bash
FILE_PATH=$(echo "${Q_HOOK_TOOL_PARAMS}" | jq -r '.path')
echo "Processing: $FILE_PATH"
```

### フック設定例

```json
{
  "hooks": {
    "agentSpawn": [
      {
        "command": "echo 'Agent started'"
      }
    ],
    "preToolUse": [
      {
        "command": "echo 'Executing tool: ${tool_name}'"
      }
    ],
    "stop": [
      {
        "command": "echo 'Response completed'"
      }
    ]
  }
}
```

---

## 🎨 高度な設定例

### AWS専門家Agent

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "aws-specialist",
  "description": "AWS専門家アシスタント",
  "prompt": "あなたはAWSのエキスパートです。AWSのベストプラクティスに基づいてアドバイスしてください。",
  "tools": ["fs_read", "fs_write", "execute_bash", "use_aws"],
  "allowedTools": ["fs_read", "use_aws"],
  "resources": [
    {
      "type": "file",
      "path": "aws-config.yaml",
      "description": "AWS設定ファイル"
    }
  ]
}
```

### セキュアなAgent

```json
{
  "name": "secure-assistant",
  "description": "セキュアなアシスタント",
  "tools": ["fs_read"],
  "allowedTools": [],
  "toolsSettings": {
    "fs_read": {
      "allowedPaths": ["/home/user/safe-dir"]
    }
  }
}
```

---

## 🔄 Agent管理コマンド

### Agent一覧の表示

```bash
q agent list
```

### Agentの切り替え

```bash
# 起動時に指定
q --agent my-agent

# チャット内で切り替え
> /agent my-agent
```

### デフォルトAgentの設定

```bash
q settings chat.defaultAgent my-agent
```

### Agent設定の検証

```bash
q agent validate my-agent
```

---

## 🎯 Agent選択の優先順位

1. **コマンドライン引数**: `q --agent my-agent`
2. **ユーザー設定**: `q settings chat.defaultAgent`
3. **ビルトインデフォルト**: 組み込みAgent

---

## ベストプラクティス

詳細なベストプラクティスは以下を参照してください：
- [設定のベストプラクティス](../04_best-practices/01_configuration.md)
- [セキュリティベストプラクティス](../04_best-practices/02_security.md)
- [パフォーマンス最適化](../04_best-practices/03_performance.md)

---

## トラブルシューティング

Agent設定に関する問題が発生した場合は、[トラブルシューティングガイド](../06_troubleshooting/02_common-issues.md)を参照してください。

**関連トピック**:
- [Agent設定のトラブルシューティング](../06_troubleshooting/02_common-issues.md#agent関連の問題)
- [MCP設定のトラブルシューティング](../06_troubleshooting/02_common-issues.md#mcp関連の問題)
- [よくある質問](../06_troubleshooting/01_faq.md)

---

## ✅ Agent設定の検証

Agent設定を作成・変更した後は、必ず検証を行いましょう。

### 1. 構文検証

**JSON構文チェック**:
```bash
# jqコマンドで検証
jq . ~/.aws/amazonq/cli-agents/my-agent.json

# エラーがなければ整形されたJSONが表示される
```

**スキーマ検証**:
```bash
# 公式スキーマと照合（ajvなどのツールを使用）
ajv validate -s agent-v1.json -d my-agent.json
```

### 2. Agent認識確認

**Agent一覧表示**:
```bash
q agent list
```

**期待される出力**:
```
my-agent           ~/.aws/amazonq/cli-agents
default            ~/.aws/amazonq/cli-agents
```

**確認ポイント**:
- 作成したAgentが表示されるか
- `(local)`または`(global)`の表示が正しいか
- ファイル名とAgent名が一致しているか

### 3. Agent詳細確認

**Agent設定の表示**:
```bash
q agent list my-agent
```

**確認ポイント**:
- `systemPrompt`が正しく設定されているか
- `tools`配列に必要なツールが含まれているか
- `mcpServers`が正しく参照されているか
- `resources`が正しく設定されているか

### 4. 実行テスト

**Agentを使用してチャット**:
```bash
q chat --agent my-agent
```

**テスト項目**:
1. **システムプロンプトの動作確認**
   - 期待通りの応答が返ってくるか
   - 役割や制約が反映されているか

2. **ツールの動作確認**
   - 指定したツールが利用可能か
   - 制限したツールが使用できないか

3. **MCPサーバーの動作確認**
   - MCPツールが正しく呼び出せるか
   - 環境変数が正しく展開されているか

4. **リソースの動作確認**
   - リソースファイルが読み込まれるか
   - 内容が正しく参照されるか

### 5. 検証チェックリスト

Agent設定の検証時に確認すべき項目：

- [ ] JSON構文エラーがない
- [ ] 必須フィールド（`version`, `name`）が存在する
- [ ] `tools`配列が空でない（ツールを使用する場合）
- [ ] `mcpServers`の参照先が存在する
- [ ] 環境変数（`${env:VAR}`）が正しく設定されている
- [ ] ファイルパスが正しい（絶対パスまたは相対パス）
- [ ] `q agent list`でAgentが表示される
- [ ] `q agent list`で設定内容が正しく表示される
- [ ] 実際のチャットで期待通りに動作する

### 6. デバッグ方法

**詳細ログの有効化**:
```bash
# デバッグモードでチャット実行
Q_LOG_LEVEL=debug q chat --agent my-agent
```

**ログ出力先**:
```
# Linux
/run/user/$(id -u)/qlog/
└── qchat.log

# macOS
$TMPDIR/qlog/
└── qchat.log

# Windows
%TEMP%\amazon-q\logs\
└── qchat.log
```

**よくあるエラーと対処法**:

| エラーメッセージ | 原因 | 対処法 |
|----------------|------|--------|
| `Agent not found` | ファイル配置ミス | ファイルパスとAgent名を確認 |
| `Failed to parse` | JSON構文エラー | jqで構文チェック |
| `Invalid schema` | スキーマ違反 | 公式スキーマと照合 |
| `MCP server not found` | MCP参照エラー | グローバル設定を確認 |
| `Tool not available` | ツール名ミス | ツール名のスペルを確認 |

### 7. 段階的な検証アプローチ

複雑なAgent設定を作成する場合は、段階的に検証しましょう：

**Step 1: 最小構成で動作確認**
```json
{
  "$schema": "https://github.com/aws/amazon-q-developer-cli/blob/main/schemas/agent-v1.json",
  "name": "test-agent",
  "prompt": "You are a helpful assistant.",
  "tools": ["*"]
}
```

**Step 2: ツールを追加**
```json
{
  "$schema": "https://github.com/aws/amazon-q-developer-cli/blob/main/schemas/agent-v1.json",
  "name": "test-agent",
  "prompt": "You are a helpful assistant.",
  "tools": ["fs_read", "fs_write"]
}
```

**Step 3: MCPサーバーを追加**
```json
{
  "$schema": "https://github.com/aws/amazon-q-developer-cli/blob/main/schemas/agent-v1.json",
  "name": "test-agent",
  "prompt": "You are a helpful assistant.",
  "tools": ["fs_read", "fs_write"],
  "mcpServers": {
    "my-mcp-server": {
      "command": "node",
      "args": ["server.js"]
    }
  }
}
}
```

**Step 4: リソースやフックを追加**

各ステップで動作確認を行い、問題を早期に発見しましょう。

---

## 設定例

基本的な設定例については、[設定例集](08_examples.md)を参照してください。

**主な設定例**:
- Agent設定の実践例
- MCP設定の実践例
- ユースケース別設定
- セキュリティ設定

---

## Agent設定の実践ガイド

Agent設定の実践的な使い方とベストプラクティスは、[コンテキスト管理ガイド](../08_guides/README.md)を参照してください。

### 推奨ガイド

**設計と実装**:
- [ベストプラクティス編](../08_guides/04_best-practices.md) - Agent設定の設計原則
- [実践ガイド編](../08_guides/05_practical-guide.md) - プロジェクト別の実装例

**問題解決**:
- [トラブルシューティング編](../08_guides/06_troubleshooting.md) - Agent設定の問題解決

**最適化**:
- [上級編](../08_guides/07_advanced.md) - パフォーマンス最適化とチーム開発

### 学習の進め方

1. **基本を理解する**: 本ドキュメント（Agent設定の仕様）
2. **設計を学ぶ**: [ベストプラクティス編](../08_guides/04_best-practices.md)
3. **実装する**: [実践ガイド編](../08_guides/05_practical-guide.md)
4. **最適化する**: [上級編](../08_guides/07_advanced.md)

---
## 📚 関連ドキュメント

- **[MCP設定](04_mcp-configuration.md)** - MCPサーバーの設定
- **[MCP設定の読込フロー](04_mcp-configuration.md#-mcp設定の読込フロー)** - Agent設定とレガシーMCP設定の優先順位
- **[設定例集](08_examples.md)** - 実践的なAgent設定例
- **[ベストプラクティス](../04_best-practices/01_configuration.md)** - 設定のベストプラクティス
- **[トラブルシューティング](../06_troubleshooting/02_common-issues.md)** - よくある問題

---

## 🔗 外部リンク

- [Agent スキーマ](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json)
- [GitHub リポジトリ](https://github.com/aws/amazon-q-developer-cli)

---


## 関連ドキュメント

- [セキュリティ概要](../09_security/01_security-overview.md) - Agent設定のセキュリティ
- [セキュリティチェックリスト](../05_deployment/03_security-checklist.md) - Agent設定の確認項目
- [エンタープライズ展開ガイド](../05_deployment/01_enterprise-deployment.md) - 組織でのAgent管理

---

最終更新: 2025-11-01
