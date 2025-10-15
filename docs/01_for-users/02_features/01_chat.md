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

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/help` | チャット内コマンドのヘルプを表示。利用可能なコマンド一覧と簡単な説明を確認できる | コマンドの使い方を忘れた時、利用可能なコマンドを確認したい時 |
| `/quit` | チャットセッションを終了してターミナルに戻る。会話履歴は保存される | 作業を終了する時、別のタスクに切り替える時 |
| `/exit` | `/quit`と同じ。チャットセッションを終了する | 作業を終了する時（`/quit`の別名） |
| `/clear` | 現在の会話履歴をクリア。新しい話題を始める時に便利 | 会話が長くなりすぎた時、全く別の話題に切り替える時 |

### 会話管理

| コマンド | 詳細説明 | 使用シーン |
|---------|------|-----------|
| `/save [ファイル名]` | 現在の会話をJSONファイルに保存。ファイル名省略時は自動生成される | 重要な会話を記録したい時、後で参照したい会話を保存する時 |
| `/load [ファイル名]` | 保存した会話をファイルから読み込んで復元。過去の会話を継続できる | 以前の会話を再開したい時、別のセッションで保存した会話を引き継ぐ時 |
| `/tangent` | Tangentモード（会話の分岐）に入る/戻る。キーボードショートカット: `Ctrl+T` | メインの会話を保持したまま、別の話題を試したい時 |

> **🧪 実験的機能**: Tangent Mode機能は開発中です。`q settings set chat.enableTangentMode true`または`/experiment`で有効化してください。

### コンテキスト管理

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/context` | 現在のコンテキスト情報を表示。使用中のトークン数、コンテキストウィンドウの使用率を確認できる | コンテキストの使用状況を確認したい時、トークン制限に近づいているか確認する時 |
| `/compact` | 応答をコンパクトに表示するモードをオン/オフ切り替え。長い応答を簡潔に表示 | 応答が長すぎる時、要点だけを素早く確認したい時 |

### Knowledge管理

> **🧪 実験的機能**: Knowledge機能は開発中です。`q settings set chat.enableKnowledge true`で有効化してください。

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/knowledge show` | 現在のKnowledge情報を表示。インデックス化されたファイル数、合計サイズ、最終更新日時を確認できる（v1.18.0+: statusと統合） | プロジェクトのどのファイルがAIの参照対象になっているか確認したい時 |
| `/knowledge add <path>` | 指定したファイル/ディレクトリをKnowledgeに追加してインデックス化。`--include`オプションでパターン指定可能（例: `--include "*.md"`） | 新しいドキュメントフォルダをAIの参照対象に追加したい時 |
| `/knowledge add -n <name> -p <path>` | 名前とパスを指定してKnowledgeに追加（v1.18.0+） | 複数のプロジェクトを管理する時、わかりやすい名前を付けたい時 |
| `/knowledge remove <path>` | 指定したパスのエントリをKnowledgeから削除。インデックスから除外される | 不要になった古いドキュメントをAIの参照対象から外したい時 |
| `/knowledge update <path>` | 指定したエントリを再インデックス化。ファイル内容を更新した後に実行すると、最新の内容がAIに反映される | ドキュメントを編集した後、変更内容をAIに認識させたい時 |
| `/knowledge clear` | すべてのKnowledgeエントリを削除してインデックスをリセット。プロジェクト切り替え時に便利 | 別のプロジェクトに切り替える時、前のプロジェクトの情報をクリアしたい時 |
| `/knowledge cancel` | バックグラウンドで実行中のインデックス化処理をキャンセル | 誤って大量のファイルを追加した時、処理を中断したい時 |

### Checkpoint管理

> **🧪 実験的機能**: Checkpoint機能は開発中です。`q settings set EnabledCheckpointing true`で有効化してください。詳細は[Checkpoint機能ガイド](05_checkpoints.md)を参照してください。

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| [`/checkpoint init`](05_checkpoints.md#使い方) | Checkpoint機能を初期化。会話の保存ポイントを作成できるようになる | 長い会話セッションを開始する前に、保存機能を有効化したい時 |
| [`/checkpoint list`](05_checkpoints.md#checkpoint一覧) | 保存されているCheckpointの一覧を表示。`--limit`オプションで表示数を制限可能 | 過去のどの時点に戻れるか確認したい時 |
| `/checkpoint expand <tag>` | 指定したタグのCheckpoint詳細を表示。会話内容のプレビューを確認できる | Checkpointの内容を確認してから復元するか判断したい時 |
| `/checkpoint diff <tag1> [tag2]` | 2つのCheckpoint間の差分を表示。会話の変化を比較できる | どの時点でどんな変更があったか確認したい時 |
| [`/checkpoint restore [<tag>]`](05_checkpoints.md#checkpoint復元) | 指定したCheckpointに会話を復元。タグ省略時は最新のCheckpointに戻る | 会話が脱線した時、以前の状態に戻りたい時 |
| [`/checkpoint restore <tag> --hard`](05_checkpoints.md#復元モード) | Checkpointに完全復元。復元後の会話履歴は削除される | 完全に以前の状態からやり直したい時 |
| `/checkpoint clean` | 古いCheckpointを削除してストレージを整理 | Checkpointが増えすぎた時、不要なものを削除したい時 |

### TODO管理

> **🧪 実験的機能**: TODO機能は開発中です。`q settings set chat.enableTodoList true`で有効化してください。

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/todos view` | 現在のTODOリストを表示。未完了のタスク一覧を確認できる | 残っているタスクを確認したい時 |
| `/todos resume` | TODOを再開。中断していたタスクに戻る | 一時中断していたタスクを再開したい時 |
| `/todos clear-finished` | 完了済みのTODOをリストから削除。未完了のタスクのみ残る | 完了したタスクを整理してリストをすっきりさせたい時 |
| `/todos delete` | すべてのTODOを削除。リストを完全にクリアする | プロジェクトが終了した時、TODOリストをリセットしたい時 |

### Agent管理

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| [`/agent`](02_agents.md) | 現在使用中のAgent情報を表示。Agent名、設定内容、有効なツールを確認できる | 現在どのAgentを使っているか確認したい時 |
| [`/agent list`](02_agents.md#agent一覧の表示) | 利用可能なAgent一覧を表示。グローバルとローカルのAgentを確認できる | 切り替え可能なAgentを確認したい時 |
| [`/agent switch <name>`](02_agents.md#agentの切り替え) | 指定したAgentに切り替え。プロジェクトや用途に応じてAgentを変更できる | 別のプロジェクトに切り替える時、専門的なAgentを使いたい時 |
| `/model [モデル名]` | 使用するAIモデルを表示または切り替え。モデル名省略時は現在のモデルを表示 | より高性能なモデルに切り替えたい時、コスト削減のため軽量モデルに変更する時 |
| [`/experiment`](07_experimental.md) | 実験的機能のON/OFF切り替え。Knowledge、Checkpoint、TODO等のベータ機能を有効化 | 新機能を試したい時、実験的機能を有効化/無効化する時 |
| `/prompts` | カスタムプロンプトを管理。独自のプロンプトテンプレートを作成・編集できる | 頻繁に使う指示をテンプレート化したい時 |

### 開発者向けコマンド

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/logdump` | サポート調査用のログファイルを収集してZIPアーカイブとして出力（v1.18.0+） | 問題発生時にログを収集してサポートチームに提出する時、デバッグ情報を効率的に収集する時 |
| `/tools` | 利用可能なツール一覧を表示。ネイティブツールとMCPツールの両方を確認できる | どのツールが使えるか確認したい時、MCPサーバーが正しく読み込まれているか確認する時 |
| `/mcp` | MCPサーバーの状態を確認。接続状況、利用可能なツール、エラー情報を表示 | MCPサーバーが正常に動作しているか確認したい時、トラブルシューティングする時 |
| `/hooks` | カスタムコマンドをAgent実行時に自動実行。起動時の初期化処理を設定できる | Agent起動時に毎回実行したいコマンドがある時、環境のセットアップを自動化したい時 |
| `/editor [エディタコマンド]` | 外部エディタの設定を管理。長文入力時に使用するエディタを指定できる | 長いプロンプトを書く時、使い慣れたエディタで編集したい時 |
| `/reply [オプション]` | AIの応答スタイルを設定。詳細度、フォーマット、言語などを調整できる | 応答の形式を変更したい時、より詳細な説明が欲しい時 |

### 情報表示

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/usage` | Q CLIの使用状況を表示。トークン使用量、API呼び出し回数、コスト情報を確認できる | 使用量を確認したい時、コストを把握したい時 |
| `/changelog` | Q CLIの変更履歴を表示。バージョンごとの新機能、バグ修正、変更点を確認できる | 最近のアップデート内容を確認したい時、特定バージョンの変更を調べる時 |
| `/whatsnew` | 最新バージョンの新機能を表示。アップデート後の新機能をハイライト表示 | アップデート後に何が変わったか確認したい時 |
| `/subscribe [オプション]` | 情報の購読を管理。アップデート通知、ニュースレターの設定を変更できる | 通知設定を変更したい時、情報の受信を管理する時 |

### 問題報告

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/issue` | Q CLIの問題やフィードバックを報告。GitHubのissue作成画面を開き、バグ報告や機能要望を送信できる | バグを見つけた時、新機能を提案したい時、改善要望を伝えたい時 |

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
- [Knowledge機能](../04_best-practices/03_performance.md#-knowledge-base最適化)
- [Checkpoint機能](05_checkpoints.md)
- [グローバル設定](../03_configuration/03_global-settings.md)
- [コマンドリファレンス](../07_reference/02_commands.md)

---

## 🔗 参考リンク

- [Amazon Q CLI GitHub](https://github.com/aws/amazon-q-developer-cli)
- [AWS公式ドキュメント](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html)

---

最終更新: 2025-10-09
