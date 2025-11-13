[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [機能ガイド](README.md) > 01 Chat

---

# チャット機能

**ドキュメント対象バージョン**: v1.13.0以降

> **Note**: chat機能はv1.13.0以前から存在します。
> 本サイトではv1.13.0以降の機能を対象に記述しています。

## バージョン別主要機能

- **v1.13.0以前**: 基本的なchat機能（詳細は調査範囲外）
- **v1.13.0**: Agent機能の本格導入、ファイル操作の強化
- **v1.14.0**: Knowledge Beta改善（BM25サポート）
- **v1.15.0**: Tangent Mode、TODO Lists、Introspect Tool
- **v1.16.0**: MCP統合（rmcp移行、リモートMCP）
- **v1.17.0**: コンテキスト使用率表示、Checkpoint機能、プロンプト管理強化
- **v1.18.0**: Delegate機能追加
- **v1.19.0**: Knowledge PDF対応、画像ペースト対応
- **v1.19.5**: マルチラインコードブロック検出の改善

---

## 📋 概要

Amazon Q CLIの中心となるチャット機能について説明します。AIアシスタントとの対話を通じて、コード生成、質問応答、タスク実行などを行えます。

### 参考リンク

- [Amazon Q Developer CLI GitHub](https://github.com/aws/amazon-q-developer-cli) - 公式リポジトリ
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

チャットセッション内で使用できる特殊コマンドです。**全25コマンド**を機能別に分類しています。

**📋 コマンド分類**:

| カテゴリ | コマンド数 | 主要コマンド |
|----------|------------|--------------|
| [基本コマンド](#基本コマンド) | 5コマンド | help, quit, exit, clear, paste |
| [会話管理](#会話管理) | 3コマンド | save, load, tangent |
| [コンテキスト管理](#コンテキスト管理) | 3コマンド | context, compact, hooks |
| [プロンプト管理](#プロンプト管理) | 2コマンド | prompts, editor |
| [Knowledge管理](#knowledge管理) | 6コマンド | knowledge操作 |
| [Checkpoint管理](#checkpoint管理) | 6コマンド | checkpoint操作 |
| [TODO管理](#todo管理) | 4コマンド | todos操作 |
| [Agent管理](#agent管理) | 5コマンド | agent, model, experiment |
| [開発者向けコマンド](#開発者向けコマンド) | 4コマンド | logdump, tools, mcp, reply |
| [情報表示](#情報表示) | 3コマンド | usage, changelog, subscribe |
| [問題報告](#問題報告) | 1コマンド | issue |

**🔍 よく使うコマンド**:
- `/help` - コマンドヘルプ
- `/context add <ファイル>` - ファイルをコンテキストに追加
- `/prompts` - プロンプトテンプレート管理
- `/usage` - コンテキスト使用状況確認
- `/hooks` - フック設定確認

**💡 初心者向け**:
1. まず `/help` でコマンド一覧を確認
2. `/context` でファイルをAIに認識させる
3. `/prompts` で定型作業を効率化
4. `/usage` でコンテキスト使用量を監視

**出典**: [AWS公式ドキュメント - チャットコマンド](https://docs.aws.amazon.com/ja_jp/amazonq/latest/qdeveloper-ug/command-line-chat-commands.html)

### 基本コマンド

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/help [コマンド名]` | チャット内コマンドのヘルプを表示。コマンド名を指定すると、そのコマンドの詳細ヘルプを表示 | コマンドの使い方を忘れた時、利用可能なコマンドを確認したい時、特定のコマンドの詳細を知りたい時 |
| `/quit` | チャットセッションを終了してターミナルに戻る。会話履歴は保存される | 作業を終了する時、別のタスクに切り替える時 |
| `/exit` | チャットセッションを終了してターミナルに戻る（`/quit`と同じ） | 作業を終了する時、別のタスクに切り替える時 |
| `/clear` | 現在の会話履歴をクリア。新しい話題を始める時に便利 | 会話が長くなりすぎた時、全く別の話題に切り替える時 |
| `/paste` | クリップボードから画像を貼り付け | 画像をチャットに追加したい時、スクリーンショットを共有したい時 |

### 会話管理

| コマンド | 詳細説明 | 使用シーン |
|---------|------|-----------|
| `/save <パス> [オプション]` | 現在の会話をJSONファイルに保存。`-f`オプションで既存ファイルを上書き可能 | 重要な会話を記録したい時、後で参照したい会話を保存する時 |
| `/load <パス>` | 保存した会話をファイルから読み込んで復元。過去の会話を継続できる | 以前の会話を再開したい時、別のセッションで保存した会話を引き継ぐ時 |
| `/tangent [サブコマンド]` | （Beta）Tangentモード（会話の分岐）に入る/戻る。`tail`サブコマンドで最後のエントリを保持して終了。要設定: `q settings chat.enableTangentMode true` | メインの会話を保持したまま、別の話題を試したい時 |

> **🧪 Beta機能**: Tangent Mode機能は開発中です。`q settings chat.enableTangentMode true`または`/experiment`で有効化してください。

### コンテキスト管理

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/context <サブコマンド>` | チャットセッションのコンテキストファイルを管理。現在のAgentから派生したコンテキストルールを表示・追加・削除できる。ファイル名やglobパターンで指定可能。変更はセッション間で保持されない | プロジェクトの特定ファイルをAIに認識させたい時、コンテキストルールを確認・変更したい時 |
| `/compact [プロンプト] [オプション]` | 会話履歴を要約してコンテキストスペースを解放。重要な情報を保持しながら、長時間の会話でメモリ制約に達するのを防ぐ。コンテキストウィンドウがオーバーフローすると自動実行される | メモリ制約の警告が表示された時、会話が長時間続いている時、同じセッション内で新しい話題を始める前 |
| `/hooks` | **Agent設定で定義されたフック（自動実行スクリプト・hook・フック）の一覧を表示**。フックはツール実行前後やAgent起動時に自動実行される。セキュリティチェック、ログ記録、コード整形、監査、自動化などに使用 | Agent設定のフックが正しく設定されているか確認したい時、どのフックが有効になっているか知りたい時、フックのトラブルシューティングをする時 |

#### `/hooks` コマンドの詳細

**概要**: Agentに設定されたフック（自動実行スクリプト）の一覧を表示します。

**フックとは**:
- ツール実行の前後やAgent起動時に自動実行されるカスタムコマンド
- セキュリティ検証、監査ログ、コード整形、環境チェックなどに使用
- Agent設定ファイル（`.amazonq/cli-agents/`ディレクトリ内）で定義

**使用例**:
```bash
> /hooks
agentSpawn:
  - git status
  - echo "Agent started in $(pwd)"

preToolUse:
  - echo "Tool execution: $(date)" >> /tmp/audit.log

postToolUse:
  - cargo fmt --all  # Rustコード整形
  - npm run lint     # JavaScript/TypeScript lint
```

**フックの種類**:
- `agentSpawn`: Agent起動時に実行
- `userPromptSubmit`: ユーザーがプロンプトを送信した時に実行
- `preToolUse`: ツール実行前に実行（実行をブロック可能）
- `postToolUse`: ツール実行後に実行

**設定方法**:
1. Agent設定ファイルを編集:
   ```bash
   # ローカルAgent設定（例: my-agent.json）
   vim .amazonq/cli-agents/my-agent.json
   
   # グローバルAgent設定
   vim ~/.aws/amazonq/cli-agents/my-agent.json
   ```

2. hooks セクションを追加:
   ```json
   {
     "name": "development-agent",
     "hooks": {
       "agentSpawn": [
         {
           "command": "git status"
         }
       ],
       "preToolUse": [
         {
           "matcher": "execute_bash",
           "command": "echo 'Bash実行: $(date)' >> /tmp/bash_audit.log"
         }
       ],
       "postToolUse": [
         {
           "matcher": "fs_write",
           "command": "cargo fmt --all"
         }
       ]
     }
   }
   ```

**実用的な設定例**:

1. **セキュリティ監査**:
   ```json
   "preToolUse": [
     {
       "matcher": "execute_bash",
       "command": "echo \"$(date): Bash実行 - $(cat)\" >> /var/log/q-cli-audit.log"
     }
   ]
   ```

2. **自動コード整形**:
   ```json
   "postToolUse": [
     {
       "matcher": "fs_write",
       "command": "prettier --write ."
     }
   ]
   ```

3. **Git自動コミット**:
   ```json
   "postToolUse": [
     {
       "matcher": "*",
       "command": "git add -A && git commit -m 'Q CLI session: $(date)' || true"
     }
   ]
   ```

**トラブルシューティング**:
- フックが表示されない → Agent設定ファイルの構文を確認
- フックが実行されない → コマンドのパスと権限を確認
- エラーが発生する → `/logdump` でログを確認

**💡 Tip**: フックは強力な機能ですが、無限ループや権限エラーに注意してください。

**関連コマンド**:
- `/context` - コンテキストファイル管理
- `/agent` - Agent設定確認
- 参照: [Agent設定ガイド](../03_configuration/03_agent-configuration.md)

### Knowledge管理

> **🧪 Beta機能**: Knowledge機能は開発中です。`q settings chat.enableKnowledge true`で有効化してください。

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/knowledge show` | 現在のKnowledge情報を表示。インデックス化されたファイル数、合計サイズ、最終更新日時を確認できる（v1.18.0+: statusと統合） | プロジェクトのどのファイルがAIの参照対象になっているか確認したい時 |
| `/knowledge add -n <名前> -p <パス> [オプション]` | 指定したファイル/ディレクトリをKnowledgeに追加してインデックス化。`--include`でパターン指定、`--exclude`で除外パターン指定、`--index-type`でインデックスタイプ指定が可能 | 新しいドキュメントフォルダをAIの参照対象に追加したい時 |
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

> **🧪 Beta・実験的機能**: Checkpoint機能は開発中です。ワークスペースのチェックポイントを管理します（会話のチェックポイントではありません）。機能は変更・削除される可能性があります。`q settings chat.enableCheckpoint true`で有効化してください。詳細は[Checkpoint機能ガイド](05_checkpoints.md)を参照してください。

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| [`/checkpoint init`](05_checkpoints.md#使い方) | チェックポイントを手動で初期化 | チェックポイント機能を開始する時 |
| [`/checkpoint list`](05_checkpoints.md#checkpoint一覧) | 全てのチェックポイントを一覧表示 | 利用可能なチェックポイントを確認したい時 |
| [`/checkpoint restore [<tag>]`](05_checkpoints.md#checkpoint復元) | 指定したチェックポイントにワークスペースを復元 | 以前の状態に戻したい時 |
| `/checkpoint expand <tag>` | 指定したチェックポイントの詳細を表示 | チェックポイントの内容を確認したい時 |
| `/checkpoint diff <tag1> [tag2]` | 2つのチェックポイント間の差分を表示 | 変更内容を確認したい時 |
| [`/checkpoint restore <tag> --hard`](05_checkpoints.md#復元モード) | Checkpointに完全復元。復元後の会話履歴は削除される | 完全に以前の状態からやり直したい時 |
| `/checkpoint clean` | シャドウリポジトリを削除 | チェックポイントデータを完全に削除したい時 |

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

### プロンプト管理

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/prompts [サブコマンド]` | **再利用可能なプロンプトテンプレート（prompt・プロンプト・テンプレート）を作成・管理**。よく使う指示をテンプレート化して `@プロンプト名` で呼び出し可能。ローカル保存とMCPサーバー提供の両方に対応。定型文、雛形、スニペット管理にも活用 | 定型的な指示を効率化したい時、チーム共通のプロンプトを管理したい時、複雑な指示をテンプレート化したい時 |
| `/editor [初期テキスト]` | $EDITORでプロンプトを作成（デフォルト: vi）。長文のプロンプトを使い慣れたエディタで編集可能 | 長いプロンプトを書く時、使い慣れたエディタで編集したい時、複数行のプロンプトを整理したい時 |

#### `/prompts` コマンドの詳細

**概要**: 再利用可能なプロンプトテンプレートを作成・管理し、効率的にAIとやり取りできます。

**プロンプトテンプレートとは**:
- よく使う指示や質問をテンプレート化したもの
- `@プロンプト名` で簡単に呼び出し可能
- 引数を使って動的な内容に対応
- ローカル保存とMCPサーバー提供の両方をサポート

**基本的な使い方**:

1. **利用可能なプロンプト一覧を表示**:
   ```bash
   > /prompts
   # または
   > /prompts list
   ```

2. **プロンプトの詳細を確認**:
   ```bash
   > /prompts details code-review
   ```

3. **プロンプトを使用**:
   ```bash
   > @code-review
   # または
   > /prompts get code-review
   ```

**サブコマンド一覧**:

| サブコマンド | 説明 | 使用例 |
|-------------|------|--------|
| `list [検索語]` | 利用可能なプロンプト一覧を表示 | `/prompts list code` |
| `details <名前>` | プロンプトの詳細情報を表示 | `/prompts details review` |
| `get <名前> [引数...]` | プロンプトを取得して使用 | `/prompts get review main.py` |
| `create -n <名前> [--content <内容>]` | 新しいプロンプトを作成 | `/prompts create -n my-prompt` |
| `edit <名前>` | 既存のプロンプトを編集 | `/prompts edit my-prompt` |
| `remove <名前>` | プロンプトを削除 | `/prompts remove my-prompt` |

**プロンプトの保存場所**:
- **ローカル**: `.amazonq/prompts/` （プロジェクト固有）
- **グローバル**: `~/.aws/amazonq/prompts/` （全プロジェクト共通）
- **MCPサーバー**: 外部サーバーから提供

**実用的な設定例**:

1. **コードレビュー用プロンプト**:
   ```bash
   > /prompts create -n code-review --content "以下のコードをレビューしてください。セキュリティ、パフォーマンス、可読性の観点から改善点を指摘し、具体的な修正案を提示してください。"
   ```

2. **ドキュメント生成プロンプト**:
   ```bash
   > /prompts create -n doc-gen --content "以下のコードの詳細なドキュメントを作成してください。関数の目的、引数、戻り値、使用例を含めてください。"
   ```

3. **バグ分析プロンプト**:
   ```bash
   > /prompts create -n debug --content "以下のエラーログを分析し、原因と解決策を提示してください。再現手順も含めてください。"
   ```

**引数付きプロンプトの例**:
```bash
# プロンプト作成時
> /prompts create -n test-gen --content "{{language}}言語で{{function_name}}関数のユニットテストを作成してください。"

# 使用時
> /prompts get test-gen Python calculate_total
```

**MCPサーバーからのプロンプト**:
```bash
# MCPサーバーのプロンプト一覧
> /prompts list

# 特定のMCPサーバーのプロンプト
> /prompts details @git/commit-message

# MCPプロンプトの使用
> @git/commit-message "新機能追加"
```

**ファイル構造例**:
```
.amazonq/prompts/
├── code-review.txt
├── doc-gen.txt
└── debug.txt

~/.aws/amazonq/prompts/
├── global-review.txt
└── team-standards.txt
```

**プロンプトファイルの内容例**:
```
# .amazonq/prompts/code-review.txt
以下のコードをレビューしてください：

## チェック項目
1. セキュリティ脆弱性
2. パフォーマンスの問題
3. コードの可読性
4. ベストプラクティス準拠

## 出力形式
- 問題点: 具体的な指摘
- 修正案: 改善されたコード例
- 理由: なぜその修正が必要か
```

**トラブルシューティング**:
- プロンプトが見つからない → ファイル名とディレクトリを確認
- 作成できない → ディレクトリの権限を確認
- MCPプロンプトが表示されない → `/mcp` でサーバー状態を確認

**💡 Tips**:
- プロンプト名は短く覚えやすいものにする
- チーム共通のプロンプトはグローバルに保存
- 複雑なプロンプトは `/editor` で作成すると便利
- 引数を使って汎用的なテンプレートを作成

**関連コマンド**:
- `/editor` - エディタでプロンプト作成
- `/context` - コンテキスト管理
- 参照: [プロンプト管理ベストプラクティス](../04_best-practices/04_prompt-optimization.md)

### 開発者向けコマンド

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/logdump [オプション]` | サポート調査用のログファイルを収集してZIPアーカイブとして出力。`--mcp`でMCPログも含めることが可能（v1.18.0+） | 問題発生時にログを収集してサポートチームに提出する時、デバッグ情報を効率的に収集する時 |
| `/tools [サブコマンド]` | ツールと権限を管理。利用可能なツール一覧の表示、ツールの信頼設定、権限のリセットが可能。デフォルトでは、特定のツール使用時に確認を求める | どのツールが使えるか確認したい時、ツールを自動承認したい時、権限をリセットしたい時 |
| `/mcp` | MCPサーバーの状態を確認。接続状況、利用可能なツール、エラー情報を表示 | MCPサーバーが正常に動作しているか確認したい時、トラブルシューティングする時 |
| `/reply` | 最新のAI応答を引用して$EDITORで返信を作成 | 長文の返信を書きたい時、AI応答の特定部分にコメントしたい時 |

### 情報表示

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/usage` | コンテキストウィンドウの使用状況を詳細表示（[詳細](#usageコマンドの詳細)） | コンテキストの使用状況を詳しく確認したい時 |
| `/changelog` | Q CLIの変更履歴を表示。バージョンごとの新機能、バグ修正、変更点を確認できる | 最近のアップデート内容を確認したい時、特定バージョンの変更を調べる時 |
| `/subscribe [オプション]` | Q Developer Proサブスクリプションへのアップグレード。クエリ制限を増やすことができる | Proプランにアップグレードしたい時、クエリ制限を増やしたい時、既存のサブスクリプションを管理したい時（--manage） |

### 問題報告

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/issue [説明] [オプション]` | Q CLIの問題やフィードバックを報告。GitHubのissue作成画面を開き、バグ報告や機能要望を送信できる。`-f`で強制作成 | バグを見つけた時、新機能を提案したい時、改善要望を伝えたい時 |

### チャット内コマンド トラブルシューティング

#### よくある問題と解決策

**1. コマンドが認識されない**
```
問題: `/prompts` と入力しても「コマンドが見つかりません」と表示される
解決策:
- コマンドの先頭に `/` があることを確認
- スペルミスがないか確認（`/prompt` ではなく `/prompts`）
- `/help` でコマンド一覧を確認
```

**2. 権限エラーが発生する**
```
問題: `/hooks` や `/prompts create` で権限エラーが発生
解決策:
- ファイル・ディレクトリの書き込み権限を確認
- `chmod 755 .amazonq` でディレクトリ権限を設定
- `sudo` は使わず、ユーザー権限で実行
```

**3. 設定ファイルが見つからない**
```
問題: Agent設定やプロンプトファイルが見つからない
解決策:
- 正しいディレクトリにいるか確認（`pwd` で現在位置確認）
- `.amazonq/` ディレクトリが存在するか確認
- グローバル設定は `~/.aws/amazonq/` を確認
```

**4. フックが実行されない**
```
問題: 設定したフックが動作しない
解決策:
- Agent設定ファイルのJSON構文を確認
- コマンドのパスが正しいか確認（`which git` など）
- `/logdump` でエラーログを確認
- フックコマンドを手動実行してテスト
```

**5. プロンプトが呼び出せない**
```
問題: `@プロンプト名` で呼び出せない
解決策:
- `/prompts list` でプロンプト一覧を確認
- ファイル名とプロンプト名が一致しているか確認
- ファイルの文字エンコーディングを確認（UTF-8推奨）
- MCPサーバーの状態を `/mcp` で確認
```

#### 診断コマンド

**問題の特定に役立つコマンド**:
- `/help` - 利用可能なコマンド確認
- `/logdump` - 詳細なログ情報取得
- `/mcp` - MCPサーバー状態確認
- `/agent` - 現在のAgent設定確認
- `/usage` - コンテキスト使用状況確認

#### サポートリソース

**問題が解決しない場合**:
1. [トラブルシューティングガイド](../06_troubleshooting/02_common-issues.md)を確認
2. `/issue` コマンドでバグ報告
3. [GitHub Issues](https://github.com/aws/amazon-q-developer-cli/issues)で既知の問題を検索
4. [AWS公式ドキュメント](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html)を参照

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

### 6. マルチラインコードブロック入力を活用（v1.19.5改善）

**新機能**: トリプルバッククォート（```）を使用したマルチラインコードブロック入力時のヒント機能が追加されました。

**使用例**:

チャットで以下のように入力できます：

```
> 以下のコードを修正して
```

その後、コードブロックを入力：

```python
def hello():
    print("Hello World")
```

**改善点**:
- ✅ **ヒント表示**: マルチライン入力時に適切なガイダンスを表示
- ✅ **検出精度向上**: コードブロックの開始・終了をより正確に認識
- ✅ **自動補完制御**: 不要な自動補完をブロックして入力体験を改善

**💡 Tip**: 長いコードや複数行のテキストを貼り付ける際は、トリプルバッククォートで囲むことで、より正確に認識されます。

### 7. 開発ワークフローでの活用例

**プロジェクト開始時の設定**:
```bash
# 1. プロジェクトコンテキストを設定
> /context add src/
> /context add README.md
> /context add package.json

# 2. 開発用プロンプトを作成
> /prompts create -n code-review --content "コードレビューを実施してください。セキュリティ、パフォーマンス、可読性を重視してください。"
> /prompts create -n test-gen --content "以下の関数のユニットテストを作成してください。エッジケースも含めてください。"

# 3. 開発用フックを設定（Agent設定ファイル）
{
  "hooks": {
    "postToolUse": [
      {
        "matcher": "fs_write",
        "command": "npm run lint && npm run format"
      }
    ]
  }
}
```

### 8. プロジェクト管理での活用例

**日次作業管理**:
```bash
# 1. 作業開始時
> /checkpoint init
> /todos view

# 2. 作業中の進捗管理
> @code-review  # 定型プロンプトでコードレビュー
> /todos resume  # 中断したタスクを再開

# 3. 作業終了時
> /checkpoint list
> /todos clear-finished
> /save daily-work-$(date +%Y%m%d).json
```

### 9. コードレビューでの活用例

**効率的なレビュープロセス**:
```bash
# 1. レビュー用プロンプトテンプレート
> /prompts create -n security-review --content "セキュリティ観点でコードレビューを実施してください。SQLインジェクション、XSS、認証・認可の問題を重点的にチェックしてください。"

# 2. レビュー実行
> @security-review
> @performance-check
> @code-style-check

# 3. レビュー結果の記録
> /save code-review-$(date +%Y%m%d).json
```

### 10. チーム開発での活用例

**チーム共通設定の管理**:

1. **共通プロンプトの配布**:
   ```bash
   # チームリーダーが作成
   > /prompts create -n team-review --global --content "チーム標準に従ってコードレビューを実施してください。命名規則、エラーハンドリング、ドキュメント化を確認してください。"
   
   # チームメンバーが使用
   > @team-review
   ```

2. **プロジェクト標準化**:
   ```json
   // .amazonq/cli-agents/team-development.json（プロジェクトルートに配置）
   {
     "name": "team-development",
     "hooks": {
       "postToolUse": [
         {
           "matcher": "fs_write",
           "command": "npm run lint && npm run test"
         }
       ],
       "postToolUse": [
         {
           "matcher": "*",
           "command": "git add -A && git commit -m 'Auto-commit: $(date)' || true"
         }
       ]
     },
     "resources": [
       "file://src/**/*.js",
       "file://docs/**/*.md",
       "file://README.md"
     ]
   }
   ```

3. **ナレッジ共有**:
   ```bash
   # プロジェクト知識をインデックス化
   > /knowledge add -n project-docs -p ./docs
   > /knowledge add -n api-specs -p ./api-specs
   
   # チーム共通の質問テンプレート
   > /prompts create -n ask-architecture --content "このプロジェクトのアーキテクチャについて、以下の観点で説明してください：1. 全体構成 2. データフロー 3. 主要コンポーネント"
   ```

**💡 チーム開発のベストプラクティス**:
- グローバルプロンプトでチーム標準を統一
- プロジェクトルートのAgent設定で自動化を統一
- Knowledge機能でプロジェクト知識を共有
- 定期的な設定レビューで改善を継続

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

最終更新: 2025-11-01
