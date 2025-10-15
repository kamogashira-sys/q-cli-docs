# 実践的ユースケース

**最終更新**: 2025-10-15  
**対象バージョン**: v1.18.0以降

---

## 📋 このガイドについて

このドキュメントでは、Q CLIの実践的な活用方法を紹介します。1日の作業フローでの使い方や、プロジェクト別の設定テンプレートを参考に、効率的な開発を実現してください。

---

## 📅 1日の作業フローでの活用

### 朝の作業開始（9:00-9:30）

#### タスクの整理

```bash
# チャットセッションを開始
q chat
```

チャット内で質問：
```
> 今日のタスクを整理して
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
# チャットセッションを開始
q chat
```

チャット内で質問：
```
> このプロジェクトの最近の変更を教えて
```

#### 環境のセットアップ

```bash
# 開発用Agentに切り替え
q agent use developer

# 環境変数を確認
q chat
```

チャット内で質問：
```
> 必要な環境変数を教えて
```

---

### コード開発（10:00-12:00）

#### 新機能の実装

```bash
# Agent切り替え
q agent use developer

# 実装方法を相談
q chat
```

チャット内で質問：
```
> ユーザー認証機能を実装したい。どのライブラリを使うべき？

# コード生成
q chat
```

チャット内で質問：
```
> JWTを使った認証ミドルウェアを作成して

# テストコード生成
q chat
```

チャット内で質問：
```
> このミドルウェアのテストコードを書いて
```

#### バグ修正

```bash
# エラーログを確認
q chat
```

チャット内で質問：
```
> このエラーの原因を教えて: TypeError: Cannot read property 'id' of undefined

# 修正方法を提案
q chat
```

チャット内で質問：
```
> このバグを修正する方法を教えて

# 修正コードを生成
q chat
```

チャット内で質問：
```
> 修正したコードを書いて
```

#### リファクタリング

```bash
# コードレビューAgentに切り替え
q agent use code-reviewer

# リファクタリング提案
q chat
```

チャット内で質問：
```
> このコードをリファクタリングして

# パフォーマンス改善
q chat
```

チャット内で質問：
```
> このコードのパフォーマンスを改善して
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
q chat
```

チャット内で質問：
```
> このPRをレビューして

# セキュリティチェック
q chat
```

チャット内で質問：
```
> このコードにセキュリティ上の問題はある？

# パフォーマンスチェック
q chat
```

チャット内で質問：
```
> このコードのパフォーマンスは問題ない？
```

#### レビューコメントの作成

```bash
# チャットセッションを開始
q chat
```

チャット内で質問：
```
> このコードに対するレビューコメントを書いて
```

---

### ドキュメント作成（14:00-15:00）

#### README作成

```bash
# ドキュメントAgentに切り替え
q agent use documentation-writer

# README生成
q chat
```

チャット内で質問：
```
> このプロジェクトのREADME.mdを作成して

# API ドキュメント生成
q chat
```

チャット内で質問：
```
> このAPIのドキュメントを作成して
```

#### コメント追加

```bash
# チャットセッションを開始
q chat
```

チャット内で質問：
```
> このコードにJSDocコメントを追加して
```

---

### AWS操作（15:00-16:00）

#### リソースの確認

```bash
# AWS SpecialistAgentに切り替え
q agent use aws-specialist

# リソース一覧
q chat
```

チャット内で質問：
```
> S3バケット、EC2インスタンス、Lambda関数の一覧を教えて

# コスト確認
q chat
```

チャット内で質問：
```
> 今月のAWS利用料金を教えて
```

#### デプロイ

```bash
# デプロイ手順を確認
q chat
```

チャット内で質問：
```
> このアプリケーションをAWSにデプロイする手順を教えて

# CloudFormationテンプレート生成
q chat
```

チャット内で質問：
```
> このアプリケーション用のCloudFormationテンプレートを作成して
```

---

### 終業時（17:00-17:30）

#### 作業記録

```bash
# チャットセッションを開始
q chat
```

チャット内で質問：
```
> 今日の作業内容をまとめて
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
q chat
```

チャット内で質問：
```
> Reactのユーザープロフィールコンポーネントを作成して

# スタイリング
q chat
```

チャット内で質問：
```
> このコンポーネントにTailwind CSSでスタイルを追加して

# テスト
q chat
```

チャット内で質問：
```
> このコンポーネントのJestテストを書いて

# パフォーマンス最適化
q chat
```

チャット内で質問：
```
> このコンポーネントのパフォーマンスを改善して
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
q chat
```

チャット内で質問：
```
> VPC、ECS、RDSを含むCDKスタックを作成して

# セキュリティチェック
q chat
```

チャット内で質問：
```
> このCloudFormationテンプレートのセキュリティ問題を確認して

# コスト最適化
q chat
```

チャット内で質問：
```
> このインフラのコストを最適化する方法を教えて

# デプロイ
q chat
```

チャット内で質問：
```
> このCDKスタックをデプロイする手順を教えて
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
q chat
```

チャット内で質問：
```
> CSVファイルを読み込んでPandas DataFrameに変換して

# データクリーニング
q chat
```

チャット内で質問：
```
> このデータの欠損値を処理して

# データ可視化
q chat
```

チャット内で質問：
```
> このデータを棒グラフで可視化して

# 統計分析
q chat
```

チャット内で質問：
```
> このデータの基本統計量を計算して
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
q chat
```

チャット内で質問：
```
> ユーザー管理のREST APIエンドポイントを作成して

# OpenAPI仕様生成
q chat
```

チャット内で質問：
```
> このAPIのOpenAPI仕様を作成して

# テスト
q chat
```

チャット内で質問：
```
> このAPIエンドポイントのテストを書いて

# ドキュメント
q chat
```

チャット内で質問：
```
> このAPIのドキュメントを作成して
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
q chat
```

チャット内で質問：
```
> このプロジェクトでJWTはどこで使われている？
```

---

## 🆕 v1.18.0新機能の活用

### Delegate Toolでの並行作業（v1.18.0+）

**シナリオ**: メインの会話でアーキテクチャ設計を議論しながら、別のエージェントにテストコードの作成を委譲

```bash
# Delegate機能を有効化
q settings set chat.enableDelegate true

# チャットセッション内で
q chat
```

チャット内で質問：
```
> rust-agentにsnake gameを作成するタスクを委任して

# バックグラウンドでタスクが実行される

> rust-agentのステータスを確認して

# メインの会話は継続可能
> 次にAPIの設計について議論しましょう
```

**活用シーン**:
- 大規模プロジェクトでの並行作業
- 複数のマイクロサービス開発
- 長時間実行タスクのバックグラウンド処理

### Stop Hookでの自動化（v1.18.0+）

**シナリオ**: 会話ターン終了時に自動的にコードフォーマットを実行

**Agent設定（.amazonq/cli-agents/auto-format.json）**:
```json
{
  "name": "auto-format",
  "description": "Auto-format code after each turn",
  "hooks": {
    "stop": {
      "command": "prettier --write .",
      "timeout": 30000
    }
  }
}
```

**使用方法**:
```bash
q agent use auto-format
q chat
```

チャット内で質問：
```
> Reactコンポーネントを作成して

# AIが応答完了後、自動的にprettierが実行される
```

**活用シーン**:
- コンパイル自動実行
- テスト自動実行
- コードフォーマット
- クリーンアップ処理

### /logdumpでのトラブルシューティング（v1.18.0+）

**シナリオ**: 問題発生時にログを収集してサポートチームに提出

```bash
q chat
```

チャット内で実行：
```
> /logdump

Collecting logs...
✓ Successfully created q-logs-2025-10-15T07-11-01Z.zip with 5 log files
```

**活用シーン**:
- 問題発生時のログ収集
- サポートチームへの情報提供
- デバッグ情報の効率的な収集

---

## 🔗 関連ドキュメント

- [Agent設定](03_configuration/04_agent-configuration.md)
- [MCP設定](03_configuration/06_mcp-configuration.md)
- [設定例集](03_configuration/07_examples.md)
- [ベストプラクティス](04_best-practices/01_configuration.md)
- [実験的機能](02_features/07_experimental.md)

---

**最終更新**: 2025-10-15
