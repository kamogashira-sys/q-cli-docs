# Agent設定ガイド

**最終更新**: 2025-10-11  
**対象バージョン**: v1.17.0以降

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
| `prompt` | string | null | システムプロンプト |
| `mcpServers` | object | {} | MCPサーバー設定 |
| `tools` | array | ["*"] | 利用可能ツール一覧 |
| `toolAliases` | object | {} | ツール名エイリアス |
| `allowedTools` | array | DEFAULT_APPROVE | 自動承認ツール一覧 |
| `resources` | array | デフォルトリソース | リソースファイル |
| `hooks` | object | {} | フック設定 |
| `toolsSettings` | object | {} | ツール固有設定 |
| `useLegacyMcpJson` | boolean | true | レガシーMCP設定の使用 |
| `model` | string | null | 使用モデルID |

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

### フック設定例

```json
{
  "hooks": {
    "AgentSpawn": {
      "command": "echo 'Agent started'",
      "async": false
    },
    "PreToolUse": {
      "command": "echo 'Executing tool: ${tool_name}'",
      "async": true
    },
    "Stop": {
      "command": "echo 'Response completed'",
      "async": false
    }
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
- [Agent設定のトラブルシューティング](../06_troubleshooting/02_common-issues.md#agent設定)
- [MCP設定のトラブルシューティング](../06_troubleshooting/02_common-issues.md#mcp設定)
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
my-agent           ~/.config/amazonq/agents
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
  "version": "1.0",
  "name": "test-agent",
  "systemPrompt": "You are a helpful assistant.",
  "tools": ["*"]
}
```

**Step 2: ツールを追加**
```json
{
  "version": "1.0",
  "name": "test-agent",
  "systemPrompt": "You are a helpful assistant.",
  "tools": ["fs_read", "fs_write"]
}
```

**Step 3: MCPサーバーを追加**
```json
{
  "version": "1.0",
  "name": "test-agent",
  "systemPrompt": "You are a helpful assistant.",
  "tools": ["fs_read", "fs_write"],
  "mcpServers": ["my-mcp-server"]
}
```

**Step 4: リソースやフックを追加**

各ステップで動作確認を行い、問題を早期に発見しましょう。

---

## 設定例

基本的な設定例については、[設定例集](07_examples.md)を参照してください。

**主な設定例**:
- Agent設定の実践例
- MCP設定の実践例
- ユースケース別設定
- セキュリティ設定

---
## 📚 関連ドキュメント

- **[MCP設定](06_mcp-configuration.md)** - MCPサーバーの設定
- **[MCP設定の読込フロー](06_mcp-configuration.md#-mcp設定の読込フロー)** - Agent設定とレガシーMCP設定の優先順位
- **[設定例集](07_examples.md)** - 実践的なAgent設定例
- **[ベストプラクティス](../04_best-practices/01_configuration.md)** - 設定のベストプラクティス
- **[トラブルシューティング](../06_troubleshooting/02_common-issues.md)** - よくある問題

---

## 🔗 外部リンク

- [Agent スキーマ](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json)
- [GitHub リポジトリ](https://github.com/aws/amazon-q-developer-cli)

---

**作成日**: 2025-10-11  
**最終更新日**: 2025-10-11
