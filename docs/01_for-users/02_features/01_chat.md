[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [機能ガイド](README.md) > 01 Chat

---

# チャット機能

**対象バージョン**: v1.17.0以降

---

## 📋 概要

Amazon Q CLIの中心となるチャット機能について説明します。AIアシスタントとの対話を通じて、コード生成、質問応答、タスク実行などを行えます。

### 参考リンク

- [Amazon Q CLI GitHub](https://github.com/aws/amazon-q-developer-cli) - 公式リポジトリ
- [AWS公式ドキュメント](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html) - コマンドライン機能の詳細

---

## 🚀 基本操作

### Amazon Q CLIの起動

```bash
# デフォルトAgentでチャット開始
q chat

# 特定のAgentでチャット開始
q chat --agent aws-specialist
```

> **⚠️ v1.18.0での重要な変更**
> 
> v1.18.0以降、`--resume` フラグの動作が変更されました：
> - **新しい動作**: `--resume` を明示的に指定した場合のみ前回の会話を読み込みます
> - **以前の動作**: チャット開始時に自動的に前回の会話を読み込もうとしていました
> 
> この変更により、起動が高速化され、Checkpoint機能が正常に動作するようになりました。

#### 会話の開始と再開

**新しい会話を開始（デフォルト）**:
```bash
# 常に新しい会話として開始
q chat
```

**前回の会話を再開**:
```bash
# 前回の会話を明示的に再開
q chat --resume
```

#### 使い分けガイド

| 状況 | コマンド | 説明 |
|------|---------|------|
| 新しいトピックで質問 | `q chat` | 新規会話として開始 |
| 前回の続きを質問 | `q chat --resume` | 会話履歴を引き継ぐ |
| 同じディレクトリで別の質問 | `q chat` | 独立した新規会話 |

**💡 Tip**: 常に会話を再開したい場合は、エイリアスを設定できます：
```bash
alias qr='q chat --resume'
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

**出典**: [AWS公式ドキュメント - チャットコマンド](https://docs.aws.amazon.com/ja_jp/amazonq/latest/qdeveloper-ug/command-line-chat-commands.html)

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

> **🧪 実験的機能**: Tangent Mode機能は開発中です。`q settings chat.enableTangentMode true`または`/experiment`で有効化してください。

### コンテキスト管理

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/context` | 現在のコンテキスト情報を表示。使用中のトークン数、コンテキストウィンドウの使用率を確認できる | コンテキストの使用状況を確認したい時、トークン制限に近づいているか確認する時 |
| `/compact` | 応答をコンパクトに表示するモードをオン/オフ切り替え。長い応答を簡潔に表示 | 応答が長すぎる時、要点だけを素早く確認したい時 |

### Knowledge管理

> **🧪 実験的機能**: Knowledge機能は開発中です。`q settings chat.enableKnowledge true`で有効化してください。

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/knowledge show` | 現在のKnowledge情報を表示。インデックス化されたファイル数、合計サイズ、最終更新日時を確認できる（v1.18.0+: statusと統合） | プロジェクトのどのファイルがAIの参照対象になっているか確認したい時 |
| `/knowledge add <path>` | 指定したファイル/ディレクトリをKnowledgeに追加してインデックス化。`--include`オプションでパターン指定可能（例: `--include "*.md"`） | 新しいドキュメントフォルダをAIの参照対象に追加したい時 |
| `/knowledge add -n <name> -p <path>` | 名前とパスを指定してKnowledgeに追加（v1.18.0+） | 複数のプロジェクトを管理する時、わかりやすい名前を付けたい時 |
| `/knowledge remove <path>` | 指定したパスのエントリをKnowledgeから削除。インデックスから除外される | 不要になった古いドキュメントをAIの参照対象から外したい時 |
| `/knowledge update <path>` | 指定したエントリを再インデックス化。ファイル内容を更新した後に実行すると、最新の内容がAIに反映される | ドキュメントを編集した後、変更内容をAIに認識させたい時 |
| `/knowledge clear` | すべてのKnowledgeエントリを削除してインデックスをリセット。プロジェクト切り替え時に便利 | 別のプロジェクトに切り替える時、前のプロジェクトの情報をクリアしたい時 |
| `/knowledge cancel` | バックグラウンドで実行中のインデックス化処理をキャンセル | 誤って大量のファイルを追加した時、処理を中断したい時 |

#### サポートファイル形式（v1.18.0+）

Knowledge機能は以下のファイル形式をサポートしています：

- **テキストファイル**: `.txt`, `.md`
- **ソースコード**: `.py`, `.js`, `.ts`, `.java`, `.go`, etc.
- **PDF**: `.pdf` ← **v1.19.0で追加**

**PDF対応の特徴**:
- ✅ テキストベースのPDFファイルに対応
- ✅ ドキュメント、マニュアル、仕様書などを直接インデックス化
- ⚠️ スキャン画像のみのPDFは非対応の可能性
- ⚠️ パスワード保護されたPDFは非対応の可能性

**使用例**:
```bash
# PDFファイルを含むディレクトリをインデックス化
> /knowledge add ./docs

# 特定のPDFファイルをインデックス化
> /knowledge add ./manual.pdf
```


### Checkpoint管理

> **🧪 実験的機能**: Checkpoint機能は開発中です。`q settings chat.enableCheckpoint true`で有効化してください。詳細は[Checkpoint機能ガイド](05_checkpoints.md)を参照してください。

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

> **🧪 実験的機能**: TODO機能は開発中です。`q settings chat.enableTodoList true`で有効化してください。

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
| `/usage` | コンテキストウィンドウの使用状況を詳細表示（[詳細](#usageコマンドの詳細)） | コンテキストの使用状況を詳しく確認したい時 |
| `/changelog` | Q CLIの変更履歴を表示。バージョンごとの新機能、バグ修正、変更点を確認できる | 最近のアップデート内容を確認したい時、特定バージョンの変更を調べる時 |
| `/whatsnew` | 最新バージョンの新機能を表示。アップデート後の新機能をハイライト表示 | アップデート後に何が変わったか確認したい時 |
| `/subscribe [オプション]` | 情報の購読を管理。アップデート通知、ニュースレターの設定を変更できる | 通知設定を変更したい時、情報の受信を管理する時 |

### 問題報告

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/issue` | Q CLIの問題やフィードバックを報告。GitHubのissue作成画面を開き、バグ報告や機能要望を送信できる | バグを見つけた時、新機能を提案したい時、改善要望を伝えたい時 |

#### /usageコマンドの詳細

`/usage`コマンドは、コンテキストウィンドウの使用状況を詳細に表示します。

**表示内容**:

1. **全体の使用状況**
   - 使用トークン数 / 最大トークン数
   - 使用率（パーセンテージ）
   - プログレスバー

2. **4つの内訳**
   - **Context files**: コンテキストファイルが使用するトークン
   - **Tools**: ツール実行結果が使用するトークン
   - **AI responses**: AIの応答が使用するトークン
   - **Your prompts**: ユーザーのプロンプトが使用するトークン

3. **Pro Tips**
   - `/compact`: 会話履歴を要約に置き換え
   - `/clear`: チャット履歴を完全消去
   - `/context show`: コンテキストファイルごとのトークン数を表示

**使用例**:
```bash
> /usage

Current context window (112530 of 200k tokens used) 56.27%

Context files: ~3090 tokens (1.54%)
Tools: ~52480 tokens (26.24%)
AI responses: ~32830 tokens (16.42%)
Your prompts: ~24130 tokens (12.07%)

Pro Tips:
- Run /compact to replace the conversation history with its summary
- Run /clear to erase the entire chat history
- Run /context show to see tokens per context file
```

**💡 活用方法**:
- 使用率が60%を超えたら、どの要素が多いか確認
- **Toolsが多い場合**: 不要なツール実行結果を削除
- **AI responsesが多い場合**: `/compact`で要約
- **Context filesが多い場合**: 不要なファイルを削除

---

## 🛠️ AIツールの機能

Q CLIのAIは、以下の内部ツール（ネイティブツール）を使ってファイル操作やコマンド実行を行います。

**出典**: Q CLI内部実装（`/tools`コマンドで確認可能）、[GitHubリポジトリ](https://github.com/aws/amazon-q-developer-cli)

### 内部ツール一覧

| ツール名 | 機能 | 主な用途 |
|---------|------|---------|
| **fs_read** | ファイル/ディレクトリ読み込み | テキストファイル、画像、ディレクトリ一覧の取得 |
| **fs_write** | ファイル書き込み | ファイルの作成、編集、追加、文字列置換 |
| **execute_bash** | Bashコマンド実行 | シェルコマンドの実行 |
| **use_aws** | AWS CLI実行 | AWSリソースの操作・管理 |
| **introspect** | Q CLI機能問い合わせ | Q CLIの機能やコマンドのヘルプ |
| **thinking** | 思考プロセス表示 | AIの推論過程の可視化 |
| **todo_list** | TODO管理 | タスクの作成・管理 |
| **knowledge** | Knowledge管理 | ナレッジベースの操作 |
| **delegate** | デリゲートツール | 他ツールへの処理委譲 |
| **report_issue** | Issue報告 | GitHub Issueの作成 |

> 💡 **ツール確認**: `/tools`コマンドで現在利用可能なツール一覧を表示できます

---

### ファイル読み込み（fs_read）

ファイルやディレクトリの内容を読み取ります。

#### サポートモード

| モード | 説明 | 対象 |
|--------|------|------|
| Line | ファイルの行を読み取る | テキストファイル |
| Directory | ディレクトリの内容を一覧表示 | ディレクトリ |
| Search | ファイル内を検索 | テキストファイル |
| **Image** | 画像ファイルを読み込む | 画像ファイル |

#### 画像ファイル対応（Image モード）

**サポート形式**:
- jpg, jpeg, png, gif, webp

**特徴**:
- ✅ バイナリデータとして読み込み、AIに送信
- ✅ Amazon Bedrockの画像入力機能を活用
- ✅ 画像の内容をAIが認識・分析可能

**制限事項**:
- 最大画像サイズ: 10MB
- 1リクエストあたりの最大画像数: 10枚

**使用例**:
```bash
# 画像ファイルを読み込んでAIに分析させる
> この画像を説明して
> [画像ファイルをドラッグ&ドロップ]

# 複数の画像を比較
> これらの画像の違いを説明して
> [複数の画像ファイルを指定]

# スクリーンショットの分析
> このエラー画面を見て、問題を診断して

# 図表の説明
> このアーキテクチャ図を説明して

# コード画像の認識
> この画像のコードをテキストに変換して
```

**💡 Tip**: 
- スクリーンショット、図表、コード画像などを直接AIに見せることができます
- 画像内のテキストも認識可能です
- 画像は10MB以下に圧縮し、必要な部分だけをトリミングすると効果的です

#### 画像ペースト対応（v1.19.0以降）

**新機能**: チャット内で画像を直接ペーストできます

**サポート形式**:
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)

**制限事項**:
- 最大サイズ: 10MB/枚
- 最大枚数: 10枚/リクエスト

**使用方法**:
1. クリップボードに画像をコピー（スクリーンショット等）
2. チャット入力欄でペースト（`Ctrl+V` / `Cmd+V`）
3. 画像が自動的にアップロード

**または `/paste` コマンドを使用**:
```bash
> /paste
# クリップボードの画像を自動的に読み込み
```

**メリット**:
- ✅ ファイル保存不要
- ✅ スクリーンショットを即座に共有
- ✅ ワークフロー効率化

**出典**: [PR #3088](https://github.com/aws/amazon-q-developer-cli/pull/3088)

---

### ファイル書き込み（fs_write）

ファイルの作成、編集、追加、文字列置換を行います。

**主な操作**:
- `create` - 新規ファイル作成
- `str_replace` - 文字列置換（既存内容の一部を変更）
- `insert` - 指定行に挿入
- `append` - ファイル末尾に追加

**使用例**:
```bash
# 新規ファイル作成
> README.mdを作成して

# 既存ファイルの一部を変更
> main.pyの関数名をupdateに変更して

# ファイルに追記
> TODOリストに新しいタスクを追加して
```

---

### コマンド実行（execute_bash）

Bashコマンドを実行します。

**使用例**:
```bash
# ファイル操作
> カレントディレクトリのファイル一覧を表示して

# Git操作
> 変更をコミットして

# パッケージ管理
> npm installを実行して
```

**セキュリティ**: 実行前に確認プロンプトが表示されます

---

### AWS操作（use_aws）

AWS CLIコマンドを実行してAWSリソースを操作します。

**使用例**:
```bash
# S3操作
> S3バケット一覧を表示して

# EC2操作
> 実行中のEC2インスタンスを確認して

# Lambda操作
> Lambda関数一覧を取得して
```

**前提条件**: AWS CLIの設定（認証情報）が必要

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

## 🔄 パイプライン処理（v1.19.3以降）

v1.19.3以降、chat出力がstdoutに出力されるため、シェルのパイプライン処理やリダイレクトが可能になりました。

### 基本的な使用例

**ファイルへのリダイレクト**:
```bash
# レポートをファイルに保存
q chat "今日のタスクをまとめて" > daily-report.txt

# エラーログの分析結果を保存
q chat "エラーログを分析して" > analysis.txt
```

**パイプライン処理**:
```bash
# Markdown出力をフィルタリング
q chat "ファイル一覧を取得" | grep ".md"

# JSON出力を整形
q chat "設定をJSON形式で出力" | jq '.'

# 複数のコマンドを連携
q chat "データを取得" | sort | uniq
```

### 実用例

**ログ分析パイプライン**:
```bash
# エラーログを分析して結果を保存
q chat "エラーログを分析" | tee analysis.txt

# 分析結果をメール送信
q chat "レポートを生成" | mail -s "Daily Report" team@example.com
```

**データ変換パイプライン**:
```bash
# CSVをJSONに変換して処理
q chat "CSVをJSONに変換" | jq '.' | python process.py

# データを取得して可視化
q chat "統計データを取得" | gnuplot -e "plot '-' with lines"
```

**CI/CDパイプライン統合**:
```bash
# コードレビューの自動化
git diff | q chat "このdiffをレビューして" > review.txt

# テスト結果の分析
pytest --json | q chat "テスト結果を分析して" > test-analysis.txt
```

### シェルスクリプトとの統合

```bash
#!/bin/bash
# daily-report.sh - 日次レポート生成スクリプト

# Q CLIでレポート生成
q chat "今日のタスクをまとめて" > /tmp/daily-report.txt

# レポートをSlackに送信
curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\":\"$(cat /tmp/daily-report.txt)\"}" \
  $SLACK_WEBHOOK_URL

# クリーンアップ
rm /tmp/daily-report.txt
```

### 注意事項

- **非対話モード推奨**: パイプライン処理では `--no-interactive` オプションの使用を推奨
- **エラー処理**: パイプラインでエラーが発生した場合の処理を考慮
- **タイムアウト**: 長時間実行される処理では適切なタイムアウト設定を

**出典**: PR #3277

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
- [グローバル設定](../03_configuration/02_global-settings.md)
- [コマンドリファレンス](../07_reference/02_commands.md)



---

最終更新: 2025-10-26
