# チャット機能

**最終更新**: 2025-10-11  
**対象バージョン**: v1.17.0以降

---

## 📋 概要

Amazon Q CLIの中心となるチャット機能について説明します。AIアシスタントとの対話を通じて、コード生成、質問応答、タスク実行などを行えます。

---

## 🚀 基本操作

### Amazon Q CLIの起動

```bash
# デフォルトAgentでチャット開始
q chat

# 特定のAgentでチャット開始
q chat --agent aws-specialist
```

### 質問する

```
> What is Python?
> Pythonでファイルを読み込む方法を教えて
> AWSのベストプラクティスは？
```

### コマンド実行を依頼

```
> Run ls -la
> ディレクトリ構造を表示して
> Gitの状態を確認して
```

### コード生成を依頼

```
> Pythonでファイルを読み込むコードを書いて
> REST APIクライアントを作成して
> データベース接続のコードを生成して
```

---

## ⌨️ チャット内コマンド

チャットセッション内で使用できる特殊コマンドです。

### 基本コマンド

| コマンド | 説明 | 使用例 |
|---------|------|--------|
| `/help` | ヘルプを表示 | `/help` |
| `/quit` | チャットを終了 | `/quit` |
| `/exit` | チャットを終了 | `/exit` |
| `/clear` | 会話履歴をクリア | `/clear` |

### コンテキスト管理

| コマンド | 説明 | 使用例 |
|---------|------|--------|
| `/context` | コンテキスト情報を表示 | `/context` |
| `/context clear` | コンテキストをクリア | `/context clear` |

### Knowledge管理

| コマンド | 説明 | 使用例 |
|---------|------|--------|
| `/knowledge` | Knowledge情報を表示 | `/knowledge` |
| `/knowledge add <path>` | ファイル/ディレクトリを追加 | `/knowledge add src/` |
| `/knowledge remove <path>` | ファイル/ディレクトリを削除 | `/knowledge remove src/` |
| `/knowledge clear` | Knowledgeをクリア | `/knowledge clear` |

### Checkpoint管理

| コマンド | 説明 | 使用例 |
|---------|------|--------|
| `/checkpoint init` | Checkpointを初期化 | `/checkpoint init` |
| `/checkpoint list` | Checkpoint一覧を表示 | `/checkpoint list` |
| `/checkpoint restore <tag>` | Checkpointを復元 | `/checkpoint restore 3` |
| `/checkpoint restore <tag> --hard` | 完全復元 | `/checkpoint restore 3 --hard` |

### TODO管理

> **⚠️ 注意**: todos機能は実験的機能です。`q experiment`で有効化してください。

| コマンド | 説明 | 使用例 |
|---------|------|--------|
| `/todos` | TODO一覧を表示 | `/todos` |
| `/todos help` | ヘルプを表示 | `/todos help` |
| `/todos clear-finished` | 完了済みをクリア | `/todos clear-finished` |
| `/todos delete` | TODOを削除 | `/todos delete` |
| `/todos delete --all` | 全削除 | `/todos delete --all` |

### Agent管理

| コマンド | 説明 | 使用例 |
|---------|------|--------|
| `/agent` | 現在のAgent情報を表示 | `/agent` |
| `/agent list` | Agent一覧を表示 | `/agent list` |
| `/agent switch <name>` | Agentを切り替え | `/agent switch aws-specialist` |

### 開発者向けコマンド

| コマンド | 説明 | 使用例 |
|---------|------|--------|
| `/debug` | デバッグ情報を表示 | `/debug` |
| `/tools` | 利用可能なツール一覧を表示 | `/tools` |
| `/introspect` | Q CLIの機能を問い合わせ | `/introspect` |

---

## 🎯 実践的な使い方

### ファイル操作

```
> src/main.pyの内容を確認して
> README.mdを作成して
> package.jsonを更新して
```

### コード生成

```
> Pythonでファイルを読み込むコードを書いて
> TypeScriptでREST APIクライアントを作成して
> テストコードを生成して
```

### AWS操作

```
> S3バケット一覧を表示して
> EC2インスタンスの状態を確認して
> CloudFormationスタックを作成して
```

### デバッグ支援

```
> このエラーの原因を教えて
> コードをレビューして
> パフォーマンスを改善して
```

---

## 💡 効果的な使い方のTips

### 1. 明確な指示

❌ 悪い例:
```
> ファイルを作って
```

✅ 良い例:
```
> Pythonでログファイルを読み込んでエラー行を抽出するスクリプトを作成して
```

### 2. 段階的に進める

複雑なタスクは小さく分けて進めましょう：

```
> まず、ファイルを読み込む関数を作成して
> 次に、データを解析する関数を追加して
> 最後に、結果を保存する機能を実装して
```

### 3. コンテキストを活用

```
> /knowledge add src/
> このプロジェクトの構造を説明して
```

### 4. Checkpointで安全に作業

```
> /checkpoint init
> （作業を進める）
> /checkpoint list
> /checkpoint restore 3  # 必要に応じて復元
```

### 5. TODOで作業を管理

```
> /todos view
> /todos delete
> /todos clear-finished
```

---

## ⚙️ チャット設定

### 設定項目

```bash
# Thinking機能を有効化
q settings chat.enableThinking true

# 実験的機能を有効化（推奨: /experimentコマンドを使用）
> /experiment

# または、設定コマンドで個別に有効化
# Knowledge機能を有効化
q settings chat.enableKnowledge true

# Checkpoint機能を有効化
q settings chat.enableCheckpoint true

# TODOリスト機能を有効化
q settings chat.enableTodoList true

# Tangent Mode機能を有効化
q settings chat.enableTangentMode true

# Delegate機能を有効化
q settings chat.enableDelegate true

# 挨拶メッセージを有効化
q settings chat.greeting.enabled true

# Markdownレンダリングを無効化
q settings chat.disableMarkdownRendering false

# 自動要約を無効化
q settings chat.disableAutoCompaction false

# 履歴ヒントを有効化
q settings chat.enableHistoryHints true
```

---

## トラブルシューティング

問題が発生した場合は、[トラブルシューティングガイド](../06_troubleshooting/02_common-issues.md)を参照してください。

**関連トピック**:
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)

---

## 📚 関連ドキュメント

- [最初の一歩](../01_getting-started/03_first-steps.md)
- [Agent機能](02_agents.md)
- [Knowledge機能](../04_best-practices/03_performance.md#knowledge機能の最適化)
- [Checkpoint機能](05_checkpoints.md)
- [グローバル設定](../03_configuration/03_global-settings.md)
- [コマンドリファレンス](../07_reference/commands.md)

---

## 🔗 参考リンク

- [Amazon Q CLI GitHub](https://github.com/aws/amazon-q-developer-cli)
- [AWS公式ドキュメント](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html)

---

最終更新: 2025-10-09
