# 実践的ユースケース

**最終更新**: 2025-10-12  
**対象バージョン**: v1.17.0以降

---

## 📋 このガイドについて

このドキュメントでは、Q CLIの実践的な活用方法を紹介します。1日の作業フローでの使い方や、プロジェクト別の設定テンプレートを参考に、効率的な開発を実現してください。

---

## 📅 1日の作業フローでの活用

### 朝の作業開始（9:00-9:30）

#### タスクの整理

```bash
q chat "今日のタスクを整理して"
```

**Q CLIの応答例**:
```
今日のタスクを以下のように整理しました：

1. 優先度: 高
   - API エンドポイントのバグ修正
   - データベーススキーマの更新

2. 優先度: 中
   - ドキュメントの更新
   - コードレビュー

3. 優先度: 低
   - リファクタリング
```

#### プロジェクトの状況確認

```bash
q chat "このプロジェクトの最近の変更を教えて"
```

#### 環境のセットアップ

```bash
# 開発用Agentに切り替え
q agent use developer

# 環境変数を確認
q chat "必要な環境変数を教えて"
```

---

### コード開発（10:00-12:00）

#### 新機能の実装

```bash
# Agent切り替え
q agent use developer

# 実装方法を相談
q chat "ユーザー認証機能を実装したい。どのライブラリを使うべき？"

# コード生成
q chat "JWTを使った認証ミドルウェアを作成して"

# テストコード生成
q chat "このミドルウェアのテストコードを書いて"
```

#### バグ修正

```bash
# エラーログを確認
q chat "このエラーの原因を教えて: TypeError: Cannot read property 'id' of undefined"

# 修正方法を提案
q chat "このバグを修正する方法を教えて"

# 修正コードを生成
q chat "修正したコードを書いて"
```

#### リファクタリング

```bash
# コードレビューAgentに切り替え
q agent use code-reviewer

# リファクタリング提案
q chat "このコードをリファクタリングして"

# パフォーマンス改善
q chat "このコードのパフォーマンスを改善して"
```

---

### ランチ休憩（12:00-13:00）

```bash
# 作業を保存
> /checkpoint save lunch-break

# Q CLIを終了
> /quit
```

---

### コードレビュー（13:00-14:00）

#### PRのレビュー

```bash
# コードレビューAgentに切り替え
q agent use code-reviewer

# PRの内容を確認
q chat "このPRをレビューして"

# セキュリティチェック
q chat "このコードにセキュリティ上の問題はある？"

# パフォーマンスチェック
q chat "このコードのパフォーマンスは問題ない？"
```

#### レビューコメントの作成

```bash
q chat "このコードに対するレビューコメントを書いて"
```

---

### ドキュメント作成（14:00-15:00）

#### README作成

```bash
# ドキュメントAgentに切り替え
q agent use documentation-writer

# README生成
q chat "このプロジェクトのREADME.mdを作成して"

# API ドキュメント生成
q chat "このAPIのドキュメントを作成して"
```

#### コメント追加

```bash
q chat "このコードにJSDocコメントを追加して"
```

---

### AWS操作（15:00-16:00）

#### リソースの確認

```bash
# AWS SpecialistAgentに切り替え
q agent use aws-specialist

# リソース一覧
q chat "S3バケット、EC2インスタンス、Lambda関数の一覧を教えて"

# コスト確認
q chat "今月のAWS利用料金を教えて"
```

#### デプロイ

```bash
# デプロイ手順を確認
q chat "このアプリケーションをAWSにデプロイする手順を教えて"

# CloudFormationテンプレート生成
q chat "このアプリケーション用のCloudFormationテンプレートを作成して"
```

---

### 終業時（17:00-17:30）

#### 作業記録

```bash
q chat "今日の作業内容をまとめて"
```

**Q CLIの応答例**:
```markdown
# 作業記録 - 2025-10-12

## 完了したタスク
- ✅ API エンドポイントのバグ修正
- ✅ データベーススキーマの更新
- ✅ ドキュメントの更新

## 進行中のタスク
- 🔄 コードレビュー（3件中2件完了）

## 明日のタスク
- リファクタリング
- 新機能の設計
```

#### 設定の保存

```bash
# チェックポイント保存
> /checkpoint save end-of-day

# Q CLIを終了
> /quit
```

---

## 🎯 プロジェクト別設定テンプレート

### 1. Webアプリケーション開発

**対象**: React/Vue/Angular等のフロントエンド開発

**Agent設定**: `~/.aws/amazonq/cli-agents/web-developer.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "web-developer",
  "description": "Webアプリケーション開発用Agent",
  "prompt": "あなたは経験豊富なWebフロントエンド開発者です。React、TypeScript、モダンなWeb技術に精通しています。コードの品質、アクセシビリティ、パフォーマンスを重視してください。",
  "tools": [
    "fs_read",
    "fs_write",
    "execute_bash"
  ],
  "toolConfig": {
    "fs_read": {
      "enabled": true,
      "allowedPaths": [
        "${env:HOME}/projects"
      ]
    },
    "fs_write": {
      "enabled": true,
      "allowedPaths": [
        "${env:HOME}/projects"
      ]
    },
    "execute_bash": {
      "enabled": true
    }
  },
  "mcpServers": {
    "npm": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-npm"]
    }
  }
}
```

**推奨設定**:
```bash
# デフォルトAgent設定
q settings chat.defaultAgent web-developer

# 実験的機能
q settings chat.enableKnowledge true
q settings chat.enableTodoList true

# Knowledge設定
q settings knowledge.indexType "bm25"
q settings knowledge.defaultExcludePatterns '["**/node_modules/**", "**/dist/**", "**/build/**"]'
```

**よく使うコマンド**:
```bash
# コンポーネント生成
q chat "Reactのユーザープロフィールコンポーネントを作成して"

# スタイリング
q chat "このコンポーネントにTailwind CSSでスタイルを追加して"

# テスト
q chat "このコンポーネントのJestテストを書いて"

# パフォーマンス最適化
q chat "このコンポーネントのパフォーマンスを改善して"
```

---

### 2. インフラ構築（IaC）

**対象**: AWS CDK/CloudFormation/Terraform

**Agent設定**: `~/.aws/amazonq/cli-agents/infrastructure-engineer.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "infrastructure-engineer",
  "description": "インフラ構築用Agent",
  "prompt": "あなたは経験豊富なインフラエンジニアです。AWS CDK、CloudFormation、Terraformに精通しています。セキュリティ、コスト最適化、可用性を重視してください。",
  "tools": [
    "fs_read",
    "fs_write",
    "execute_bash"
  ],
  "toolConfig": {
    "fs_read": {
      "enabled": true
    },
    "fs_write": {
      "enabled": true
    },
    "execute_bash": {
      "enabled": true
    }
  },
  "mcpServers": {
    "aws-cli": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-aws-cli"]
    }
  }
}
```

**推奨設定**:
```bash
# デフォルトAgent設定
q settings chat.defaultAgent infrastructure-engineer

# 実験的機能
q settings chat.enableThinking true
```

**よく使うコマンド**:
```bash
# CDKスタック生成
q chat "VPC、ECS、RDSを含むCDKスタックを作成して"

# セキュリティチェック
q chat "このCloudFormationテンプレートのセキュリティ問題を確認して"

# コスト最適化
q chat "このインフラのコストを最適化する方法を教えて"

# デプロイ
q chat "このCDKスタックをデプロイする手順を教えて"
```

---

### 3. データ分析

**対象**: Python/Pandas/Jupyter

**Agent設定**: `~/.aws/amazonq/cli-agents/data-analyst.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "data-analyst",
  "description": "データ分析用Agent",
  "prompt": "あなたは経験豊富なデータアナリストです。Python、Pandas、NumPy、Matplotlibに精通しています。データの可視化、統計分析、機械学習を得意としています。",
  "tools": [
    "fs_read",
    "fs_write",
    "execute_bash"
  ],
  "toolConfig": {
    "fs_read": {
      "enabled": true
    },
    "fs_write": {
      "enabled": true
    },
    "execute_bash": {
      "enabled": true
    }
  }
}
```

**推奨設定**:
```bash
# デフォルトAgent設定
q settings chat.defaultAgent data-analyst

# 実験的機能
q settings chat.enableKnowledge true
```

**よく使うコマンド**:
```bash
# データ読み込み
q chat "CSVファイルを読み込んでPandas DataFrameに変換して"

# データクリーニング
q chat "このデータの欠損値を処理して"

# データ可視化
q chat "このデータを棒グラフで可視化して"

# 統計分析
q chat "このデータの基本統計量を計算して"
```

---

### 4. API開発

**対象**: REST API/GraphQL

**Agent設定**: `~/.aws/amazonq/cli-agents/api-developer.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "api-developer",
  "description": "API開発用Agent",
  "prompt": "あなたは経験豊富なAPI開発者です。REST API、GraphQL、OpenAPIに精通しています。セキュリティ、パフォーマンス、ドキュメントを重視してください。",
  "tools": [
    "fs_read",
    "fs_write",
    "execute_bash"
  ],
  "toolConfig": {
    "fs_read": {
      "enabled": true
    },
    "fs_write": {
      "enabled": true
    },
    "execute_bash": {
      "enabled": true
    }
  }
}
```

**推奨設定**:
```bash
# デフォルトAgent設定
q settings chat.defaultAgent api-developer

# 実験的機能
q settings chat.enableTodoList true
```

**よく使うコマンド**:
```bash
# エンドポイント生成
q chat "ユーザー管理のREST APIエンドポイントを作成して"

# OpenAPI仕様生成
q chat "このAPIのOpenAPI仕様を作成して"

# テスト
q chat "このAPIエンドポイントのテストを書いて"

# ドキュメント
q chat "このAPIのドキュメントを作成して"
```

---

## 💡 Tips

### Agent切り替えのショートカット

```bash
# よく使うAgentをエイリアス化
alias qdev='q agent use developer'
alias qreview='q agent use code-reviewer'
alias qdoc='q agent use documentation-writer'
alias qaws='q agent use aws-specialist'
```

### チェックポイントの活用

```bash
# 重要な作業前にチェックポイント保存
> /checkpoint save before-refactoring

# 問題が発生したら復元
> /checkpoint restore before-refactoring
```

### Knowledge機能の活用

```bash
# プロジェクトのインデックス作成
q settings knowledge.enabled true

# 検索
q chat "このプロジェクトでJWTはどこで使われている？"
```

---

## 🔗 関連ドキュメント

- [Agent設定](configuration/agent-configuration.md)
- [MCP設定](configuration/mcp-configuration.md)
- [設定例集](configuration/examples.md)
- [ベストプラクティス](best-practices/configuration.md)

---

**最終更新**: 2025-10-12
