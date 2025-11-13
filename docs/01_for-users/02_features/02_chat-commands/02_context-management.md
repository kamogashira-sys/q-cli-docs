[ホーム](../../../README.md) > [ユーザーガイド](../../README.md) > [機能ガイド](../README.md) > [チャット機能](../01_chat.md) > コンテキスト管理

---

# コンテキスト管理

**対象バージョン**: v1.13.0以降

## 📋 コマンド概要

Q CLIのコンテキスト管理機能は、AIが参照するファイルやフォルダの管理、会話履歴の最適化、自動実行スクリプト（フック）の管理を行います。効率的なAI支援を実現するための重要な機能群です。

## 🚀 基本的な使い方

### コンテキスト管理コマンド一覧

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/context <サブコマンド>` | チャットセッションのコンテキストファイルを管理。現在のAgentから派生したコンテキストルールを表示・追加・削除できる。ファイル名やglobパターンで指定可能。変更はセッション間で保持されない | プロジェクトの特定ファイルをAIに認識させたい時、コンテキストルールを確認・変更したい時 |
| `/compact [プロンプト] [オプション]` | 会話履歴を要約してコンテキストスペースを解放。重要な情報を保持しながら、長時間の会話でメモリ制約に達するのを防ぐ。コンテキストウィンドウがオーバーフローすると自動実行される | メモリ制約の警告が表示された時、会話が長時間続いている時、同じセッション内で新しい話題を始める前 |
| `/hooks` | Agent設定で定義されたフック（自動実行スクリプト）の一覧を表示。フックはツール実行前後やAgent起動時に自動実行される。セキュリティチェック、ログ記録、コード整形、監査、自動化などに使用 | Agent設定のフックが正しく設定されているか確認したい時、どのフックが有効になっているか知りたい時、フックのトラブルシューティングをする時 |

### 基本例

```bash
# コンテキストルールの確認
/context list

# 特定ファイルをコンテキストに追加
/context add src/main.rs

# 会話履歴の要約
/compact

# 設定されたフックの確認
/hooks
```

## ⚙️ オプション・引数

### `/context` コマンド

| サブコマンド | 説明 | 使用例 |
|-------------|------|--------|
| `list` | 現在のコンテキストルールを表示 | `/context list` |
| `add <パス>` | ファイル/フォルダをコンテキストに追加 | `/context add src/` |
| `remove <パス>` | コンテキストから削除 | `/context remove src/test.rs` |
| `clear` | すべてのコンテキストルールをクリア | `/context clear` |

**パス指定方法**:
- 相対パス: `src/main.rs`
- 絶対パス: `/home/user/project/src/main.rs`
- Globパターン: `src/**/*.rs`、`*.md`

### `/compact` コマンド

| 引数・オプション | 説明 | 必須 |
|-----------------|------|------|
| `[プロンプト]` | 要約時の追加指示 | いいえ |
| `--preserve-last <数>` | 最後のN個のメッセージを保持 | いいえ |

### `/hooks` コマンド

引数なし。現在のAgent設定で定義されたフックを表示します。

## 💡 実用例

### 例1: プロジェクトファイルのコンテキスト管理

**シナリオ**: Rustプロジェクトで特定のファイルをAIに認識させたい

```bash
# 現在のコンテキストを確認
/context list

# メインファイルを追加
/context add src/main.rs

# 設定ファイルを追加
/context add Cargo.toml

# すべてのRustファイルを追加
/context add "src/**/*.rs"

# テストファイルは除外
/context remove "src/**/*test*.rs"
```

**結果**: AIが関連ファイルを参照して、より適切なコード提案を行える

### 例2: 長時間会話でのメモリ最適化

**シナリオ**: 長時間の開発セッションでメモリ制約の警告が表示された

```bash
# 重要な情報を保持して会話を要約
/compact "重要な設計決定とエラー解決方法を保持してください"

# 最後の5つのメッセージを保持して要約
/compact --preserve-last 5

# 新しい話題を開始
"新しい機能の実装について相談したい"
```

**結果**: メモリ制約を解決しながら、重要な情報を保持して会話を継続できる

### 例3: フックを使った自動化ワークフロー

**シナリオ**: コード変更時に自動的にフォーマットと監査ログを実行したい

```bash
# 現在のフック設定を確認
/hooks

# 出力例:
# agentSpawn:
#   - git status
#   - echo "Agent started in $(pwd)"
# 
# preToolUse:
#   - echo "Tool execution: $(date)" >> /tmp/audit.log
# 
# postToolUse:
#   - cargo fmt --all
#   - npm run lint
```

**Agent設定ファイル例** (`.amazonq/cli-agents/my-agent.json`):
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

**結果**: ファイル変更時に自動的にコードフォーマットが実行され、監査ログが記録される

## 🔧 トラブルシューティング

### よくある問題

#### 問題1: `/context add` でファイルが追加されない

**症状**: ファイルパスを指定してもコンテキストに追加されない

**原因**: ファイルパスの指定ミス、または権限の問題

**解決策**:
```bash
# 相対パスで再試行
/context add ./src/main.rs

# 絶対パスで試行
/context add /home/user/project/src/main.rs

# 現在のディレクトリを確認
pwd
```

#### 問題2: `/compact` 後に重要な情報が失われる

**症状**: 会話要約後に必要な情報が参照できなくなる

**原因**: 要約時の指示が不十分、または保持設定の問題

**解決策**:
```bash
# 具体的な保持指示を追加
/compact "エラー解決方法、設計決定、重要なコード例を必ず保持してください"

# 最後のメッセージを多めに保持
/compact --preserve-last 10
```

#### 問題3: フックが実行されない

**症状**: Agent設定でフックを定義したが実行されない

**原因**: Agent設定ファイルの構文エラー、またはコマンドパスの問題

**解決策**:
```bash
# フック設定を確認
/hooks

# Agent設定ファイルの構文を確認
cat .amazonq/cli-agents/my-agent.json | jq .

# コマンドのパスを確認
which cargo
which npm
```

#### 問題4: Globパターンが期待通りに動作しない

**症状**: `src/**/*.rs` などのパターンが正しく展開されない

**原因**: シェルのGlob展開の問題、またはパターンの記述ミス

**解決策**:
```bash
# クォートで囲んで試行
/context add "src/**/*.rs"

# 個別にファイルを追加
/context add src/main.rs
/context add src/lib.rs

# パターンを確認
ls src/**/*.rs
```

#### 問題5: コンテキストが多すぎてパフォーマンスが低下

**症状**: 大量のファイルを追加後、応答が遅くなる

**原因**: コンテキストサイズの制限に近づいている

**解決策**:
```bash
# 不要なファイルを削除
/context remove "**/*.log"
/context remove "node_modules/**"

# コンテキストをリセット
/context clear

# 必要最小限のファイルのみ追加
/context add src/main.rs
/context add README.md
```

## 🔗 関連コマンド

- [基本コマンド・会話管理](01_basic-commands.md) - `/save`、`/load`による会話の永続化
- [Agent管理](07_agent-management.md) - Agent設定とフック設定の管理
- [開発者向けコマンド](08_developer-commands.md) - `/usage`によるコンテキスト使用量の監視

## 📖 参照元

- [チャット機能概要](../01_chat.md#コンテキスト管理) - コンテキスト管理の概要
- [Agent設定ガイド](../../03_configuration/03_agent-configuration.md) - フック設定の詳細

---

最終更新: 2025年11月13日
