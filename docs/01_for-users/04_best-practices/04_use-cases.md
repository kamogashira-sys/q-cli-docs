[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [ベストプラクティス](README.md) > 04 Use Cases

---

# 実践的ユースケース

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
q agent set-default developer

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
q agent set-default developer

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
q agent set-default code-reviewer

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
q agent set-default code-reviewer

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
q agent set-default documentation-writer

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
q agent set-default aws-specialist

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

## 🧪 負荷テスト・パフォーマンステスト

### k6を使った負荷テストの自動化

Q CLIは、Playwright MCPとk6を組み合わせることで、負荷テストの準備から実行、分析、チューニングまでを自動化できます。

#### 実現できること

1. **シナリオの自動作成**
   - Playwright MCPでブラウザ操作をキャプチャ
   - ネットワークリクエストを記録してk6スクリプトを自動生成

2. **実用的なスクリプト生成**
   - パラメータ抽出（認証トークンなど）
   - エラーハンドリングとリクエストのグルーピング
   - タグ付けと集計機能

3. **自律的なテスト実行**
   - データベースのリセット
   - k6による負荷実行と結果の自動評価

4. **パフォーマンス分析とチューニング**
   - AWS X-Ray/CloudWatchからテレメトリ収集
   - ボトルネックの自動特定とコード修正

#### 使用例

```bash
# 負荷テスト用Agentに切り替え
q agent set-default load-test

# シナリオキャプチャ
q chat
```

チャット内で指示：
```
> Playwrightでログイン→カート投入→購入のシナリオをキャプチャして
> ネットワークリクエストをテキストファイルに保存して

> キャプチャしたリクエストからk6スクリプトを作成して
> 認証トークンの抽出とエラーハンドリングを含めて

> データベースをリセットしてk6で負荷テストを実行して
> 結果を分析してボトルネックを特定して
```

#### Agent設定例

`~/.aws/amazonq/agents/load-test.json`:

```json
{
  "name": "load-test",
  "description": "k6負荷テスト自動化エージェント",
  "instructions": [
    "Playwright MCPを使ってブラウザ操作をキャプチャする",
    "ネットワークリクエストからk6スクリプトを生成する",
    "実用的な要素（パラメータ抽出、エラーハンドリング）を含める",
    "k6を実行して結果を評価する",
    "AWS Observabilityサービスからテレメトリを収集・分析する",
    "ボトルネックを特定してコードを修正する"
  ],
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    }
  }
}
```

#### ユースケース

- **APIの疎通確認**: 本番環境へのデプロイ前の動作確認
- **負荷テスト**: スループット、レスポンスタイム、エラー率の測定
- **パフォーマンスチューニング**: ボトルネックの特定と改善
- **継続的な性能監視**: CI/CDパイプラインへの組み込み

#### 参考動画

**[生成 AI 時代の負荷テスト on AWS](https://www.youtube.com/watch?v=beR_FEwPo74)**  
AWS Summit 2024での発表動画。Q CLIとPlaywright MCP、k6を組み合わせた負荷テストの自動化について、シナリオキャプチャからスクリプト生成、実行、分析、チューニングまでの全工程をデモを交えて解説しています。

> **💡 詳細ガイド**: より詳しい手順やトラブルシューティングは、**[k6を使った負荷テストの自動化](05_load-testing-with-k6.md)** を参照してください。

---

## 💡 Tips

### Agent切り替えのショートカット

```bash
# よく使うAgentをエイリアス化
alias qdev='q agent set-default developer'
alias qreview='q agent set-default code-reviewer'
alias qdoc='q agent set-default documentation-writer'
alias qaws='q agent set-default aws-specialist'
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
q settings chat.enableDelegate true

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
q agent set-default auto-format
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

## 🎯 コンテキスト管理の実践例

### シナリオ1: 大規模プロジェクトでの作業

#### 課題
大量のファイルを参照しながら作業したいが、コンテキストウィンドウの制限がある。

#### 解決策

**1. 重要なファイルのみを追加**

```bash
# チャットセッションを開始
q chat

# コンテキストファイルを追加
/context add README.md
/context add docs/architecture.md
/context add src/main.rs
```

**2. 使用状況を定期的に確認**

```bash
# 使用率を確認
/usage

# 出力例:
# Context tokens: 45000
# Assistant tokens: 12000
# Tool tokens: 8000
# User tokens: 5000
# Total: 70000/200000 (35%)
```

**3. コンテキストファイルの状態を確認**

```bash
# コンテキストファイルを確認
/context show

# 出力例:
# Total tokens: 30000/150000 (20%)
# Files: 3
# - README.md: 5000 tokens
# - docs/architecture.md: 15000 tokens
# - src/main.rs: 10000 tokens
```

**4. 75%を超えそうな場合は不要なファイルを削除**

```bash
# 不要なファイルを削除
/context remove docs/old-design.md

# 再度確認
/context show
```

**ベストプラクティス**:
- 作業開始時に必要最小限のファイルを追加
- 定期的に`/usage`で使用率を確認
- 使用率が60%を超えたら不要なファイルを削除
- 作業が変わったらコンテキストをクリア

---

### シナリオ2: 長時間の会話セッション

#### 課題
長時間の会話でコンテキストウィンドウが一杯になる。

#### 解決策

**1. 定期的に使用率を確認**

```bash
# 使用率を確認
/usage

# 出力例:
# Context tokens: 120000
# Assistant tokens: 35000
# Tool tokens: 15000
# User tokens: 10000
# Total: 180000/200000 (90%)
```

**2. 80%を超えたら要約を実行**

```bash
# 最新の2個のメッセージペアを保持して要約
/compact --messages-to-exclude 2

# 要約後の使用率を確認
/usage

# 出力例:
# Total: 100000/200000 (50%)
```

**3. 重要な会話はCheckpointで保存**

```bash
# 重要な議論を保存
/checkpoint save important-discussion

# 後で復元
/checkpoint restore important-discussion
```

**4. 新しいトピックは新しいセッションで**

```bash
# 現在のセッションを終了
/clear

# 新しいセッションを開始
q chat
```

**ベストプラクティス**:
- 1時間ごとに`/usage`で使用率を確認
- 使用率が80%を超えたら`/compact`を実行
- 重要な会話は`/checkpoint`で保存
- トピックが変わったら新しいセッションを開始

**予防策**:
- 自動要約は有効のまま（デフォルト）
- 大きなファイルは分割して追加
- 不要なコンテキストファイルは削除

---

## 🔗 関連ドキュメント

- [Agent設定](../03_configuration/03_agent-configuration.md)
- [MCP設定](../03_configuration/04_mcp-configuration.md)
- [設定例集](../03_configuration/08_examples.md)
- [ベストプラクティス](../04_best-practices/01_configuration.md)
- [実験的機能](../02_features/07_experimental.md)
- [コンテキスト管理ガイド](../08_guides/README.md)

---

最終更新: 2025-10-26
---

**関連トピック**:
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)

---

最終更新: 2025-10-26
