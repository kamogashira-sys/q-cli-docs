# 設定例集

**最終更新**: 2025-10-11  
**対象バージョン**: v1.17.0以降

---

## 📋 このガイドについて

このドキュメントでは、Q CLIの実践的な設定例を紹介します。ユースケース別の推奨設定やAgent設定例を参考に、自分に合った設定を見つけてください。

---

## 🎯 ユースケース別推奨設定

### 1. 一般的な開発作業

```bash
# デフォルトAgent設定
q settings chat.defaultAgent general-developer

# 実験的機能
q experiment
# → Context Usage Percentage: ON
# → TODO Lists: ON
# → Tangent Mode: ON

# その他の設定
q settings chat.enableHistoryHints true
q settings chat.enableTangentMode true
q settings chat.enableTodoList true
```

### 2. AWS開発

```bash
# デフォルトAgent設定
q settings chat.defaultAgent aws-specialist

# 実験的機能
q experiment
# → Context Usage Percentage: ON
# → Knowledge: ON
# → TODO Lists: ON

# その他の設定
q settings chat.enableHistoryHints true
q settings chat.enableKnowledge true
```

### 3. コードレビュー

```bash
# デフォルトAgent設定
q settings chat.defaultAgent code-reviewer

# 実験的機能
q experiment
# → Thinking: ON
# → Checkpointing: ON

# その他の設定
q settings chat.enableThinking true
q settings chat.enableCheckpoint true
q settings chat.disableMarkdownRendering false
```

### 4. ドキュメント作成

```bash
# デフォルトAgent設定
q settings chat.defaultAgent documentation-writer

# 実験的機能
q experiment
# → Knowledge: ON
# → TODO Lists: ON

# その他の設定
q settings chat.enableKnowledge true
q settings chat.enableTodoList true
q settings chat.disableMarkdownRendering false
```

---

## 🤖 Agent設定例

### 基本的なAgent設定

**ファイル**: `~/.aws/amazonq/cli-agents/general-developer.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "general-developer",
  "description": "一般的な開発作業用Agent",
  "prompt": "あなたは経験豊富なソフトウェアエンジニアです。コードの品質、保守性、パフォーマンスを重視してください。",
  "tools": [
    "fs_read",
    "fs_write",
    "execute_bash",
    "list_directory",
    "search_files"
  ],
  "allowedTools": [
    "fs_read",
    "list_directory",
    "search_files"
  ]
}
```

### セキュリティ重視のAgent設定

**ファイル**: `~/.aws/amazonq/cli-agents/secure-assistant.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "secure-assistant",
  "description": "セキュリティ重視のAgent",
  "prompt": "あなたはセキュリティを最優先するアシスタントです。すべての操作について、セキュリティリスクを考慮してください。",
  "tools": [
    "fs_read",
    "list_directory"
  ],
  "allowedTools": [],
  "toolsSettings": {
    "fs_read": {
      "allowedPaths": [
        "${env:HOME}/safe-projects"
      ]
    }
  }
}
```

### AWS専門Agent設定

**ファイル**: `~/.aws/amazonq/cli-agents/aws-specialist.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "aws-specialist",
  "description": "AWS専門家Agent",
  "prompt": "あなたはAWSのエキスパートです。AWSのベストプラクティスに基づいてアドバイスし、セキュリティ、コスト最適化、パフォーマンスを考慮してください。",
  "tools": [
    "fs_read",
    "fs_write",
    "execute_bash",
    "use_aws"
  ],
  "allowedTools": [
    "fs_read",
    "use_aws"
  ],
  "resources": [
    {
      "type": "file",
      "path": "aws-config.yaml",
      "description": "AWS設定ファイル"
    }
  ]
}
```

### プロジェクト固有Agent設定

**ファイル**: `.aws/amazonq/cli-agents/project-agent.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "project-agent",
  "description": "このプロジェクト専用Agent",
  "prompt": "あなたはこのプロジェクトの開発を支援するアシスタントです。プロジェクトのコーディング規約とアーキテクチャを理解しています。",
  "tools": [
    "fs_read",
    "fs_write",
    "execute_bash"
  ],
  "allowedTools": [
    "fs_read"
  ],
  "resources": [
    {
      "type": "file",
      "path": "README.md",
      "description": "プロジェクトREADME"
    },
    {
      "type": "file",
      "path": "CONTRIBUTING.md",
      "description": "コントリビューションガイド"
    },
    {
      "type": "directory",
      "path": "docs/",
      "description": "プロジェクトドキュメント"
    }
  ]
}
```

---

## 🔌 MCP設定例

### HTTP MCPサーバー（環境変数使用）

```json
{
  "name": "api-integration",
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com",
      "headers": {
        "Authorization": "token ${env:GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
      },
      "timeout": 60000
    },
    "slack": {
      "type": "http",
      "url": "https://slack.com/api",
      "headers": {
        "Authorization": "Bearer ${env:SLACK_TOKEN}"
      },
      "timeout": 30000
    }
  }
}
```

### STDIO MCPサーバー

```json
{
  "name": "local-tools",
  "mcpServers": {
    "database": {
      "type": "stdio",
      "command": "node",
      "args": ["./mcp-servers/database.js"],
      "env": {
        "DB_HOST": "${env:DB_HOST}",
        "DB_PORT": "${env:DB_PORT}"
      }
    },
    "file-processor": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_file_processor"],
      "env": {
        "PYTHONPATH": "${env:HOME}/my-tools"
      }
    }
  }
}
```

---

## ⚙️ グローバル設定例

### 開発者向け設定

```bash
# デフォルトAgent
q settings chat.defaultAgent general-developer

# UI設定
q settings chat.enableHistoryHints true
q settings chat.disableMarkdownRendering false

# 実験的機能
q settings chat.enableContextUsageIndicator true
q settings chat.enableTodoList true
q settings chat.enableTangentMode true

# Knowledge設定
q settings chat.enableKnowledge true
q settings knowledge.maxFiles 1000
q settings knowledge.chunkSize 1000
```

### ミニマリスト設定

```bash
# デフォルトAgent
q settings chat.defaultAgent minimal-assistant

# UI設定（シンプル）
q settings chat.enableHistoryHints false
q settings chat.disableMarkdownRendering true
q settings chat.greeting.enabled false

# 実験的機能（最小限）
q settings chat.enableContextUsageIndicator true
```

---

## 🔐 セキュリティ設定例

### ツール権限の制限

```json
{
  "name": "restricted-agent",
  "tools": [
    "fs_read",
    "list_directory"
  ],
  "allowedTools": [],
  "toolsSettings": {
    "fs_read": {
      "allowedPaths": [
        "${env:HOME}/projects",
        "${env:HOME}/documents"
      ],
      "deniedPaths": [
        "${env:HOME}/.ssh",
        "${env:HOME}/.aws"
      ]
    }
  }
}
```

### 環境変数の安全な使用

```bash
# .envファイルで管理
cat > .env << EOF
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
SLACK_TOKEN=xoxb-xxxxxxxxxxxx
API_KEY=sk-xxxxxxxxxxxx
EOF

# .gitignoreに追加
echo ".env" >> .gitignore

# シェルで読み込み
export $(cat .env | xargs)
```

---

## 🚀 パフォーマンス最適化設定

### コンテキストウィンドウ管理

```bash
# コンテキスト使用率表示を有効化
q settings chat.enableContextUsageIndicator true

# 自動コンパクション無効化（手動管理）
q settings chat.disableAutoCompaction true

# 使用率が80%を超えたら手動でコンパクション
# > /compact
```

### Knowledge Base活用

```bash
# Knowledge機能を有効化
q settings chat.enableKnowledge true

# Knowledge設定
q settings knowledge.maxFiles 1000
q settings knowledge.chunkSize 1000
q settings knowledge.chunkOverlap 200
q settings knowledge.indexType "bm25"

# プロジェクトドキュメントを追加
# > /knowledge add docs/
```

---

## 🎨 チーム開発設定例

### プロジェクトルートに配置

**ファイル**: `.aws/amazonq/cli-agents/team-agent.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "team-agent",
  "description": "チーム共通Agent",
  "prompt": "プロジェクトのコーディング規約に従ってください。\n\n## コーディング規約\n- インデント: 2スペース\n- 命名規則: camelCase\n- コメント: JSDoc形式",
  "tools": [
    "fs_read",
    "fs_write",
    "execute_bash"
  ],
  "allowedTools": [
    "fs_read"
  ],
  "resources": [
    {
      "type": "file",
      "path": "CODING_STANDARDS.md"
    }
  ]
}
```

### Gitで管理

```bash
# Agent設定をコミット
git add .aws/amazonq/cli-agents/team-agent.json
git commit -m "Add team agent configuration"

# チームメンバーがpull
git pull

# デフォルトAgentに設定
q settings chat.defaultAgent team-agent
```

---

## 💡 Tips

### 設定の確認

```bash
# 全設定を確認
q settings all

# 特定の設定を確認
q settings chat.defaultAgent
```

### 設定のバックアップ

```bash
# 設定をエクスポート
q settings all > ~/q-settings-backup.txt

# Agent設定をバックアップ
cp -r ~/.aws/amazonq/cli-agents ~/q-agents-backup
```

### 設定のリセット

```bash
# 特定の設定を削除
q settings --delete chat.defaultAgent

# 設定ファイルを削除（完全リセット）
rm ~/.aws/amazonq/settings.json
```

---

## 📚 関連ドキュメント

- **[設定システム概要](01_overview.md)** - 設定の全体像
- **[Agent設定](04_agent-configuration.md)** - Agent設定の詳細
- **[MCP設定](06_mcp-configuration.md)** - MCP設定の詳細
- **[環境変数](05_environment-variables.md)** - 環境変数の使い方
- **[優先順位ルール](02_priority-rules.md)** - 設定の優先順位

---

---

**作成日**: 2025-10-11  
**最終更新日**: 2025-10-11
