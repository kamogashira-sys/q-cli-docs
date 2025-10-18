# Amazon Q CLI 設定ベストプラクティス

**作成日**: 2025-10-08  
最終更新: 2025-10-15  
**対象バージョン**: v1.18.0以降

## 概要

このドキュメントは、Amazon Q CLIの設定に関するベストプラクティスをまとめています。

---

## Agent設定のベストプラクティス

### 1. ローカルとグローバルの使い分け

**ローカルAgent: .amazonq/cli-agents/`）を使用すべき場合**:
- プロジェクト固有の設定
- チームで共有する設定（バージョン管理に含める）
- プロジェクト固有のツールやリソースが必要な場合

**グローバルAgent（`~/.aws/amazonq/cli-agents/`）を使用すべき場合**:
- 汎用的なAgent
- 個人の生産性向上ツール
- 複数プロジェクトで共通して使用するAgent

### 2. Agent命名規則

```bash
# 推奨: 目的が明確な名前
general-assistant
aws-specialist
code-reviewer
documentation-writer

# 非推奨: 曖昧な名前
agent1
my-agent
test
```

### 3. ツール権限の最小化

```json
{
  "tools": ["fs_read", "fs_write", "execute_bash"],
  "allowedTools": ["fs_read"]
}
```

**原則**:
- 必要最小限のツールのみを`tools`に含める
- 安全なツールのみを`allowedTools`に含める
- `"*"`ワイルドカードは慎重に使用

---

## MCP設定のベストプラクティス

### 1. 環境変数の使用

**推奨**:
```json
{
  "headers": {
    "Authorization": "Bearer ${env:API_TOKEN}"
  }
}
```

**非推奨**:
```json
{
  "headers": {
    "Authorization": "Bearer hardcoded_token_here"
  }
}
```

### 2. タイムアウト設定

```json
{
  "mcpServers": {
    "slow-service": {
      "type": "stdio",
      "command": "slow-mcp-server",
      "timeout": 180000
    }
  }
}
```

**推奨値**:
- 通常のサービス: 120000ms（デフォルト）
- 遅いサービス: 180000-300000ms
- 高速サービス: 60000ms

### 3. MCPサーバーの無効化

```json
{
  "mcpServers": {
    "unused-service": {
      "type": "stdio",
      "command": "unused-mcp-server",
      "disabled": true
    }
  }
}
```

**ユースケース**:
- 一時的に無効化したいサービス
- デバッグ時の切り分け
- 設定を削除せずに無効化

---

## セキュリティのベストプラクティス

### 1. ファイルアクセスの制限

```json
{
  "resources": [
    "file://README.md",
    "file://docs/**/*.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

**原則**:
- 必要なファイルのみを指定
- ワイルドカードは慎重に使用
- 機密情報を含むディレクトリは除外

### 2. execute_bash の使用制限

```json
{
  "tools": ["fs_read", "fs_write"],
  "allowedTools": ["fs_read"]
}
```

**推奨**:
- `execute_bash`は`allowedTools`に含めない
- 必要な場合のみ`tools`に含める
- 実行前に必ず確認

### 3. 環境変数の管理

```bash
# .envファイルを使用
echo "API_TOKEN=your_token_here" > .env

# .gitignoreに追加
echo ".env" >> .gitignore

# 環境変数を読み込み
export $(cat .env | xargs)
```

---

## パフォーマンス最適化

### 1. コンテキストウィンドウ管理

```bash
# コンテキスト使用率を監視
/experiment
# → Context Usage Percentage: ON

# 定期的に圧縮
# 使用率が80%を超えたら実行
/compact
```

### 2. Knowledge Base の活用

```bash
# プロジェクト開始時に追加
/knowledge add ./docs
/knowledge add ./README.md

# 定期的に更新
/knowledge update ./docs

# 不要になったら削除
/knowledge remove ./old-docs
```

### 3. Checkpointing の活用

```bash
# 重要な変更前にチェックポイント作成
# （Checkpointing機能が有効な場合、自動作成）

# 定期的にチェックポイント一覧を確認
/checkpoint list

# 不要なチェックポイントを削除
/checkpoint clean
```

---

## チーム開発のベストプラクティス

### 1. プロジェクト固有Agent の共有

```bash
# プロジェクトルートに作成
mkdir -p .aws/amazonq/cli-agents

# Agent設定を作成
cat > .aws/amazonq/cli-agents/project-helper.json << 'EOF'
{
  "description": "Project-specific helper",
  "tools": ["fs_read", "fs_write"],
  "allowedTools": ["fs_read"],
  "resources": [
    "file://README.md",
    "file://docs/**/*.md"
  ]
}
EOF

# バージョン管理に含める
git add .amazonq/
git commit -m "Add project-specific Amazon Q CLI agent"
```

### 2. ルールファイルの活用

```bash
# プロジェクトルールを作成
mkdir -p .amazonq/rules
cat > .amazonq/rules/coding-standards.md << 'EOF'
# Coding Standards

- Use TypeScript for all new code
- Follow ESLint rules
- Write unit tests for all functions
EOF

# Agent設定でルールを参照
{
  "resources": [
    "file://.amazonq/rules/**/*.md"
  ]
}
```

### 3. ドキュメントの整備

```bash
# プロジェクトREADMEにQ CLI設定を記載
cat >> README.md << 'EOF'

## Amazon Q CLI Setup

1. Install Amazon Q CLI
2. Use the project-specific agent:
   q chat --agent project-helper
3. Set as default (optional):
   q settings chat.defaultAgent project-helper
EOF
```

---

## よくある設定ミスと対処法

### 1. Agent名の競合

**問題**:
```
WARNING: Agent conflict for my-agent. Using workspace version.
```

**対処法**:
- ローカルとグローバルで異なる名前を使用
- 意図的な場合は警告を無視（ローカルが優先される）

### 2. MCP サーバーが起動しない

**問題**:
```
Error: Failed to start MCP server 'my-server'
```

**対処法**:
```bash
# コマンドのパスを確認
which npx

# 手動で実行してテスト
npx -y @modelcontextprotocol/server-filesystem /path
```

設定でタイムアウトを延長:
```json
{
  "timeout": 180000
}
```

### 3. 環境変数が展開されない

**問題**:
```
Error: Invalid token: ${env:API_TOKEN}
```

**対処法**:
```bash
# 環境変数が設定されているか確認
echo $API_TOKEN

# 環境変数を設定
export API_TOKEN=your_token_here

# Amazon Q CLIを再起動
q restart
```

### 4. リソースファイルが見つからない

**問題**:
```
Warning: Resource file not found: file://docs/guide.md
```

**対処法**:
```bash
# ファイルの存在を確認
ls -la docs/guide.md

# 相対パスを確認（カレントディレクトリからの相対パス）
pwd

# パスを修正
{
  "resources": [
    "file://./docs/guide.md"
  ]
}
```

---

## 設定のバージョン管理

### バージョン管理に含めるべきファイル

```gitignore
# .gitignore

# Amazon Q CLI設定（含める）
.aws/amazonq/cli-agents/
.amazonq/rules/

# Amazon Q CLI内部ファイル（除外）
.amazonq/cli-todo-lists/
.amazonq/.knowledge/
```

### チーム共有の推奨構成

```
project/
├── .amazonq/
│   ├── cli-agents/
│   │   ├── project-helper.json      # バージョン管理に含める
│   │   └── team-reviewer.json       # バージョン管理に含める
│   └── rules/
│       ├── coding-standards.md      # バージョン管理に含める
│       └── security-guidelines.md   # バージョン管理に含める
├── .gitignore
└── README.md
```

---

## 定期的なメンテナンス

### 月次メンテナンス

```bash
# 1. 設定の確認
q settings all

# 2. Agent一覧の確認
q agent list

# 3. 不要なTODOリストの削除
/todos clear-finished

# 4. Knowledge Baseのクリーンアップ
/knowledge show
# 不要なエントリを削除

# 5. チェックポイントのクリーンアップ
/checkpoint clean
```

### 四半期メンテナンス

```bash
# 1. Amazon Q CLIのアップデート
q update

# 2. Agent設定の見直し
# - 使用していないAgentの削除
# - ツール権限の見直し
# - リソースの更新

# 3. MCPサーバーの見直し
# - 使用していないサーバーの削除
# - タイムアウト設定の最適化
```

---

## 推奨設定項目

### 1. デフォルトAgent設定

**設定キー**: `chat.defaultAgent`

デフォルトで使用するAgentを指定します。

```bash
# 一般的な開発作業用
q settings chat.defaultAgent general-assistant

# AWS専門作業用
q settings chat.defaultAgent aws-specialist
```

**ユースケース別推奨**:
- **一般開発**: `general-assistant` - 汎用的な開発支援
- **AWS開発**: `aws-specialist` - AWS特化の支援
- **コードレビュー**: `code-reviewer` - コードレビュー専門
- **ドキュメント作成**: `documentation-writer` - ドキュメント作成支援

### 2. Tangentモード設定

**設定キー**: `chat.enableTangentMode`

会話のチェックポイントを作成し、サイドトピックを探索できる機能です。

```bash
# Tangentモードを有効化
q settings chat.enableTangentMode true

# キーボードショートカット設定（デフォルト: Ctrl+T）
q settings chat.tangentModeKey t
```

**ユースケース**:
- 複雑な問題の調査中に関連トピックを探索
- メインの会話を保持しながら実験的な質問
- コンテキストを失わずに複数の解決策を検討

### 3. TODOリスト機能

**設定キー**: `chat.enableTodoList`

Amazon Q CLIがTODOリストを自動作成・管理する機能を有効化します。

```bash
# TODOリスト機能を有効化（推奨）
q settings chat.enableTodoList true
```

**機能**:
- Qが適切なタイミングで自動的にTODOリストを作成
- `/todos`コマンドでTODOリストの管理
- `.amazonq/cli-todo-lists`に保存

### 4. コンテキスト使用率表示

**設定キー**: `chat.enableContextUsageIndicator`（実験的機能）

プロンプトにコンテキストウィンドウ使用率を表示します。

```bash
# /experimentコマンドで有効化（推奨）
/experiment
# → Context Usage Indicatorを選択してON

# または直接設定
q settings chat.enableContextUsageIndicator true
```

**表示例**:
```
[rust-agent] 6% >   # 緑色（<50%）
[rust-agent] 75% >  # 黄色（50-89%）
[rust-agent] 95% >  # 赤色（90-100%）
```

---

## ユースケース別推奨設定

### 1. 一般的な開発作業

```bash
# デフォルトAgent設定
q settings chat.defaultAgent general-assistant

# 実験的機能
/experiment
# → Context Usage Indicator: ON
# → TODO Lists: ON
# → Tangent Mode: ON

# その他の設定
q settings chat.enableHistoryHints true
```

### 2. AWS開発

```bash
# デフォルトAgent設定
q settings chat.defaultAgent aws-specialist

# 実験的機能
/experiment
# → Context Usage Percentage: ON
# → Knowledge: ON
# → TODO Lists: ON

# その他の設定
q settings chat.enableHistoryHints true
```

### 3. コードレビュー

```bash
# デフォルトAgent設定
q settings chat.defaultAgent code-reviewer

# 実験的機能
/experiment
# → Thinking: ON
# → Checkpointing: ON

# その他の設定
q settings chat.disableMarkdownRendering false
```

---

## Agent設定例

### 基本的なAgent設定

```json
{
  "name": "general-assistant",
  "description": "General purpose development assistant",
  "tools": ["*"],
  "allowedTools": ["fs_read"],
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ],
  "useLegacyMcpJson": true
}
```

### セキュリティ重視のAgent設定

```json
{
  "name": "secure-assistant",
  "description": "Security-focused assistant with limited permissions",
  "tools": ["fs_read", "introspect", "thinking"],
  "allowedTools": ["fs_read"],
  "resources": [
    "file://README.md"
  ],
  "useLegacyMcpJson": false
}
```

### AWS専門Agent設定

```json
{
  "name": "aws-specialist",
  "description": "AWS development specialist",
  "tools": ["*"],
  "allowedTools": ["fs_read", "use_aws"],
  "resources": [
    "file://README.md",
    "file://docs/aws/**/*.md"
  ],
  "mcpServers": {
    "aws-documentation": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_DOCUMENTATION_PARTITION": "aws"
      }
    }
  }
}
```

---

## v1.18.0新機能の推奨設定

### Stop Hook設定（v1.18.0+）

会話ターン終了時に自動処理を実行する推奨設定：

**コンパイル自動実行**:
```json
{
  "hooks": {
    "stop": {
      "command": "cargo build",
      "timeout": 60000
    }
  }
}
```

**テスト自動実行**:
```json
{
  "hooks": {
    "stop": {
      "command": "npm test",
      "timeout": 120000
    }
  }
}
```

**コードフォーマット自動実行**:
```json
{
  "hooks": {
    "stop": {
      "command": "prettier --write .",
      "timeout": 30000
    }
  }
}
```

### Delegate Tool設定（v1.18.0+）

バックグラウンドタスク管理の推奨設定：

**有効化**:
```bash
q settings set chat.enableDelegate true
```

**安全な使用のためのAgent設定**:
```json
{
  "name": "safe-delegate-agent",
  "tools": ["fs_read", "execute_bash"],
  "allowedPaths": [
    "/home/user/projects/test-project"
  ]
}
```

**推奨される使用シナリオ**:
- 大規模プロジェクトでの並行作業
- 複数のマイクロサービス開発
- 長時間実行タスクのバックグラウンド処理

---

## 参考リンク

- [Agent設定ガイド](../03_configuration/04_agent-configuration.md)
- [MCP設定ガイド](../03_configuration/06_mcp-configuration.md)
- [環境変数ガイド](../03_configuration/05_environment-variables.md)
- [トラブルシューティング](../06_troubleshooting/02_common-issues.md)
- [セキュリティベストプラクティス](02_security.md)
- [パフォーマンス最適化](03_performance.md)
- [GitHub Repository](https://github.com/aws/amazon-q-developer-cli)

---

**ドキュメント作成日**: 2025-10-08  
最終更新: 2025-10-15
---

**関連トピック**:
- [設定優先順位ガイド](../03_configuration/02_priority-rules.md)
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)
