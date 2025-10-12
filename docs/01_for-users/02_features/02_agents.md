# Agent機能

**最終更新**: 2025-10-11  
**対象バージョン**: v1.17.0以降

---

## 📋 概要

Agentは、Amazon Q CLIの動作をカスタマイズする機能です。システムプロンプト、利用可能なツール、MCPサーバー連携などを設定できます。

---

## 🤖 Agentとは

### Agentでできること

Agentを使うことで以下をカスタマイズできます：

1. **システムプロンプト**
   - AIの振る舞いを定義
   - 専門分野に特化した応答

2. **利用可能なツール**
   - 使用するツールを制限
   - セキュリティ向上

3. **MCPサーバー連携**
   - 外部ツールとの統合
   - カスタム機能の追加

4. **リソースファイル**
   - コンテキストファイルの自動読み込み
   - プロジェクト固有の設定

---

## 📝 Agent管理

### Agent一覧の表示

```bash
q agent list
```

**出力例**:
```
aws-all            ~/.aws/amazonq/cli-agents
default            ~/.aws/amazonq/cli-agents
my-custom-agent    ~/.config/amazonq/agents
```

---

### Agent切り替え

#### 起動時に指定
```bash
q --agent my-agent
```

#### チャット内で切り替え
```
> /agent my-agent
```

---

### デフォルトAgent設定

```bash
# デフォルトAgentを設定
q settings chat.defaultAgent my-agent

# 確認
q settings chat.defaultAgent
```

---

## 🎨 Agent作成

### 基本的な作成方法

1. **設定ファイルを作成**
   ```bash
   mkdir -p ~/.aws/amazonq/cli-agents
   ```

2. **Agent定義ファイルを作成**
   ```bash
   vi ~/.aws/amazonq/cli-agents/my-agent.json
   ```

3. **設定内容を記述**
   ```json
   {
     "name": "my-agent",
     "description": "My custom agent",
     "prompt": "You are a helpful assistant specialized in...",
     "tools": ["fs_read", "fs_write", "execute_bash"],
     "mcpServers": ["my-mcp-server"]
   }
   ```

---

## 📚 詳細ガイド

より詳細な設定方法については、以下のドキュメントを参照してください：

- **[Agent設定ガイド](../03_configuration/04_agent-configuration.md)** - 詳細な設定方法
- **[設定例集](../03_configuration/07_examples.md)** - 実践的な設定例
- **[MCP設定ガイド](../03_configuration/06_mcp-configuration.md)** - MCPサーバー連携

---

## 💡 使用例

### 例1: AWS専門Agent

```json
{
  "name": "aws-expert",
  "description": "AWS専門家Agent",
  "prompt": "You are an AWS expert. Provide detailed AWS-specific guidance.",
  "tools": ["use_aws", "fs_read"]
}
```

### 例2: セキュアAgent

```json
{
  "name": "secure-agent",
  "description": "セキュリティ重視Agent",
  "prompt": "You are a security-focused assistant.",
  "tools": ["fs_read"]
}
```

---

## 🎯 実践的なユースケース

### フロントエンド開発Agent

フロントエンド開発に特化したAgentの設定例です。Figma Dev ModeのMCPサーバーと連携し、React開発に最適化されたコンテキストを提供します。

**設定例**:
```json
{
  "name": "front-end",
  "description": "フロントエンド開発専用Agent",
  "prompt": "You are a frontend development expert specializing in React and modern web technologies.",
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@figma/mcp-server-figma"],
      "env": {
        "FIGMA_PERSONAL_ACCESS_TOKEN": "${env:FIGMA_TOKEN}"
      }
    }
  },
  "tools": ["*"],
  "allowedTools": [
    "fs_read",
    "fs_write",
    "report_issues",
    "@figma"
  ],
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/react-preferences.md"
  ],
  "hooks": {
    "prePrompt": ["git status"]
  }
}
```

**特徴**:
- **Figma連携**: デザインファイルから直接コンポーネント情報を取得
- **React設定**: React固有のコーディング規約を自動読み込み
- **HTML/CSSコンテキスト**: フロントエンド開発に特化したコンテキスト最適化
- **Git状態確認**: 変更ファイルを自動的にコンテキストに含める

---

### バックエンド開発Agent

バックエンド開発に特化したAgentの設定例です。PostgreSQL MCPサーバーと連携し、データベース操作とPython/SQL開発に最適化されています。

**設定例**:
```json
{
  "name": "back-end",
  "description": "バックエンド開発専用Agent",
  "prompt": "You are a backend development expert specializing in Python, SQL, and database design.",
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${env:DATABASE_URL}"
      }
    }
  },
  "tools": ["*"],
  "allowedTools": [
    "fs_read",
    "report_issues",
    "@postgres",
    "@postgres/get_table_schema"
  ],
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/python-preferences.md",
    "file://.amazonq/rules/sql-preferences.md"
  ],
  "hooks": {
    "prePrompt": ["git status"]
  }
}
```

**特徴**:
- **PostgreSQL連携**: データベーススキーマ情報を直接取得
- **Python/SQL設定**: 言語固有のコーディング規約を自動読み込み
- **データベースコンテキスト**: テーブル構造に特化したコンテキスト最適化
- **粒度制御**: MCPサーバー全体と特定ツールの両方を許可

---

## 🔧 高度な設定

### allowedToolsの粒度制御

`allowedTools`では、ツールの許可範囲を細かく制御できます。

**MCPサーバー全体を許可**:
```json
{
  "allowedTools": [
    "@figma",
    "@postgres"
  ]
}
```

**特定ツールのみ許可**:
```json
{
  "allowedTools": [
    "@postgres/get_table_schema",
    "@postgres/query_database"
  ]
}
```

**組み合わせ**:
```json
{
  "allowedTools": [
    "fs_read",
    "fs_write",
    "@figma",
    "@postgres/get_table_schema"
  ]
}
```

**セキュリティ考慮事項**:
- 最小権限の原則に従い、必要なツールのみを許可
- 本番環境では特定ツールのみの許可を推奨
- 開発環境では`"*"`（全ツール）も選択肢

---

### resourcesのglobパターン

`resources`では、ワイルドカードを使用して複数のファイルを一括指定できます。

**基本的なワイルドカード**:
```json
{
  "resources": [
    "file://.amazonq/rules/*.md",
    "file://docs/**/*.md"
  ]
}
```

**IDEプラグインルールの活用**:
```json
{
  "resources": [
    "file://.amazonq/rules/**/*.md"
  ]
}
```

これにより、Amazon Q Developer IDEプラグインで定義したルールをCLIでも活用できます。

**パス指定のベストプラクティス**:
- プロジェクトルートからの相対パスを使用
- `**`で再帰的なディレクトリ検索
- `*`で単一階層のワイルドカード
- 大きなファイルは個別指定を推奨

---

### hooksによる動的コンテキスト

`hooks`を使用すると、プロンプト実行前に自動的にコマンドを実行し、その結果をコンテキストに含めることができます。

**git status実行例**:
```json
{
  "hooks": {
    "prePrompt": ["git status"]
  }
}
```

**複数コマンドの実行**:
```json
{
  "hooks": {
    "prePrompt": [
      "git status",
      "git diff --stat"
    ]
  }
}
```

**プロジェクト状態の自動取得**:
```json
{
  "hooks": {
    "prePrompt": [
      "git status",
      "npm list --depth=0"
    ]
  }
}
```

**活用シーン**:
- 変更ファイルの自動検出
- 依存関係の状態確認
- ブランチ情報の取得
- ビルド状態の確認

---

## 📚 関連ドキュメント

- [Agent設定ガイド](../03_configuration/04_agent-configuration.md)
- [MCP設定ガイド](../03_configuration/06_mcp-configuration.md)
- [設定例集](../03_configuration/07_examples.md)

---

## 📚 参考資料

- [AWSブログ: Amazon Q Developer CLIのカスタムエージェントで開発の混乱を克服する](https://aws.amazon.com/jp/blogs/news/overcome-development-disarray-with-amazon-q-developer-cli-custom-agents/)

---

**情報源**:
- GitHubソース: `crates/chat-cli/src/cli/agent/`
- 確認バージョン: v1.17.0
- 確認日: 2025-10-09

**作成日**: 2025-10-11  
**最終更新日**: 2025-10-11

