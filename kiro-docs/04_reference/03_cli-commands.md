[ホーム](../../README.md) > [リファレンス](README.md) > CLI Commands

# Kiro CLI Commands リファレンス

**出典**: [CLI commands - Kiro CLI Documentation](https://kiro.dev/docs/cli/reference/cli-commands/)（公式ページ最終更新: 2026-05-12）

Kiro CLI の `kiro-cli` コマンドおよびその引数を網羅する辞書的リファレンスです。

> **注**: `kiro-cli acp`（Agent Client Protocol）コマンドは [/docs/cli/acp/](https://kiro.dev/docs/cli/acp/) に独立した詳細記述があります。本ファイルでは `kiro-cli acp` の詳細は扱いません（[13. ACP](../01_features/13_ACP.md) 参照）。

---

## 📋 目次

- [グローバル引数](#グローバル引数)
- [コマンド一覧（公式16コマンド）](#コマンド一覧公式16コマンド)
- [セッション管理](#セッション管理)
- [ログファイル](#ログファイル)
- [環境変数](#環境変数)
- [関連リンク](#関連リンク)

---

## グローバル引数

**出典**: [Global arguments](https://kiro.dev/docs/cli/reference/cli-commands/#global-arguments)

すべての Kiro CLI コマンドで使用可能：

| 引数 | 短縮 | 説明 |
|------|------|------|
| `--verbose` | `-v` | ログ詳細度を上げる（`-v`、`-vv`、`-vvv` で繰り返し可能） |
| `--agent` | — | 特定のカスタムエージェント設定で会話を開始 |
| `--help` | `-h` | ヘルプ情報を表示 |
| `--version` | `-V` | バージョン情報を表示 |
| `--help-all` | — | すべてのサブコマンドのヘルプを表示 |

---

## コマンド一覧（公式16コマンド）

### 1. `kiro-cli agent`

エージェント設定を管理。**v1.26.0+ でエージェント名は位置引数** に変更（`--name my-agent` → `my-agent`）。

```bash
kiro-cli agent [SUBCOMMAND] [AGENT_NAME] [OPTIONS]
```

**サブコマンド**:

| サブコマンド | 説明 |
|------------|------|
| `list` | 利用可能なエージェント一覧 |
| `create <name>` | エージェント設定を作成（v1.26.0+ で位置引数） |
| `edit [name]` | エージェント設定を編集（指定なしなら現在のエージェント、v1.26.0+） |
| `validate` | 指定パスの設定を検証 |
| `migrate` | プロファイルをエージェントに移行（既存エージェントに破壊的の可能性あり） |
| `set-default` | セッション開始時のデフォルトエージェント設定 |

**例**:

```bash
kiro-cli agent list

# v1.26.0+: エージェント名は位置引数
kiro-cli agent create my-agent
kiro-cli agent edit my-agent
kiro-cli agent edit                  # 現在のエージェント

# 旧構文（互換性維持）
kiro-cli agent validate ./my-agent.json
kiro-cli agent set-default my-agent
```

### 2. `kiro-cli chat`

Kiro とのインタラクティブチャットセッションを開始。**サブコマンドなしで `kiro` を実行すると `kiro-cli chat` がデフォルト**。

```bash
kiro-cli chat [OPTIONS] [INPUT]
```

| 引数 | 説明 |
|------|------|
| `--no-interactive` | インタラクティブモードを使わず最初の応答を STDOUT に出力 |
| `--resume` / `-r` | 当該ディレクトリの直前の会話を再開 |
| `--resume-picker` | セッションピッカーで再開対象を選択 |
| `--resume-id <ID>` | 特定 ID のセッションを再開 |
| `--list-sessions` | 当該ディレクトリの保存済みセッション一覧 |
| `--list-models` | 利用可能なモデルを表示 |
| `--delete-session <ID>` | 保存済みセッションを ID で削除 |
| `--agent` | 使用するエージェントを指定 |
| `--trust-all-tools` | 全ツールを確認なしで使用 |
| `--trust-tools` | 特定ツールのみ信頼（カンマ区切り） |
| `--require-mcp-startup` | MCP サーバー起動失敗時に exit code 3 で終了 |
| `--wrap` | 行折返しモード: `always`/`never`/`auto`（既定） |
| `INPUT` | 最初の質問（位置引数） |

**例**:

```bash
# インタラクティブチャット開始
kiro-cli

# 直接質問
kiro-cli chat "How do I list files in Linux?"

# 非インタラクティブ＋全ツール信頼
kiro-cli chat --no-interactive --trust-all-tools "Show me the current directory"

# 直前会話を再開
kiro-cli chat --resume

# 特定 ID のセッション再開
kiro-cli chat --resume-id abc123-def456

# セッションピッカー
kiro-cli chat --resume-picker

# 特定エージェントで開始
kiro-cli chat --agent my-agent "Help me with AWS CLI"
```

### 3. `kiro-cli translate`

自然言語をシェルコマンドに翻訳。

```bash
kiro-cli translate [OPTIONS] [INPUT...]
```

| 引数 | 短縮 | 説明 |
|------|------|------|
| `--n` | `-n` | 生成する候補数（最大5） |
| `INPUT` | — | 自然言語記述（位置引数） |

```bash
kiro-cli translate "list all files in the current directory"
kiro-cli translate "find all Python files modified in the last week"
kiro-cli translate -n 3 "search for text in files"
```

### 4. `kiro-cli doctor`

インストール・設定の問題を診断・修正。

```bash
kiro-cli doctor [OPTIONS]
```

| 引数 | 短縮 | 説明 |
|------|------|------|
| `--all` | `-a` | 修正なしで全診断テスト実行 |
| `--strict` | `-s` | 警告でもエラー扱い |
| `--format` | `-f` | 出力形式: `plain`/`json`/`json-pretty` |

```bash
kiro-cli doctor
kiro-cli doctor --all
kiro-cli doctor --strict
```

### 5. `kiro-cli update`

Kiro CLI を最新版に更新。

```bash
kiro-cli update [OPTIONS]
```

| 引数 | 短縮 | 説明 |
|------|------|------|
| `--non-interactive` | `-y` | 確認プロンプトなし |
| `--relaunch-dashboard` | — | 更新後にダッシュボードを再起動（既定: true） |

```bash
kiro-cli update
kiro-cli update --non-interactive
```

### 6. `kiro-cli theme`

オートコンプリートドロップダウンメニューの視覚テーマを取得・設定。

```bash
kiro-cli theme [OPTIONS] [THEME]
```

| 引数 | 説明 |
|------|------|
| `--list` | 利用可能なテーマ一覧 |
| `--folder` | テーマディレクトリパス表示 |
| `THEME` | テーマ名: `dark`/`light`/`system` |

```bash
kiro-cli theme --list
kiro-cli theme dark
kiro-cli theme light
kiro-cli theme system
```

### 7. `kiro-cli integrations`

Kiro のシステム統合を管理。

```bash
kiro-cli integrations [SUBCOMMAND] [OPTIONS]
```

**サブコマンド**:

| サブコマンド | 説明 |
|------------|------|
| `install [integration]` | 統合をインストール（例: kiro-command-router） |
| `uninstall [integration]` | 統合をアンインストール |
| `reinstall [integration]` | 再インストール |
| `status` | 統合状態を確認 |

**オプション**:
- `--silent` / `-s`: 状態メッセージを抑制
- `--format` / `-f`: 出力形式（status コマンド用）

#### Kiro Command Router（v1.26.0+）

`kiro` コマンドを CLI または IDE に振り分ける統合エントリポイント。

**問題**: 既定では `kiro` コマンドが Kiro IDE を起動。多くのユーザーは CLI 起動を好む（IDE はアプリアイコンから起動するため）。

**インストール**:

```bash
# ルーターをインストール
kiro-cli integrations install kiro-command-router

# CLI をデフォルトに設定
kiro set-default cli

# または IDE をデフォルトに設定
kiro set-default ide
```

**インストール後の動作**:
- `kiro` — デフォルト（CLI または IDE）を起動
- `kiro-cli` — 常に CLI を起動
- `kiro ide` — 常に IDE を起動

### 8. `kiro-cli inline`

入力中に表示されるインラインサジェスト（ゴーストテキスト）を管理。

```bash
kiro-cli inline [SUBCOMMAND] [OPTIONS]
```

**サブコマンド**:

| サブコマンド | 説明 |
|------------|------|
| `enable` | インラインサジェスト有効化 |
| `disable` | 無効化 |
| `status` | 現在の状態表示 |
| `set-customization` | カスタマイズモデル選択 |
| `show-customizations` | 利用可能カスタマイズ表示 |

```bash
kiro-cli inline enable
kiro-cli inline disable
kiro-cli inline status
kiro-cli inline show-customizations --format json
```

→ 詳細: [25. AutoComplete](../01_features/25_AutoComplete.md)

### 9. `kiro-cli login`

Builder ID、Identity Center、ソーシャルログイン（Google/GitHub）で認証。

```bash
kiro-cli login [OPTIONS]
```

| オプション | 説明 |
|---------|------|
| `--license <TYPE>` | ライセンス種別: `pro`（Identity Center）または `free`（Builder ID/Google/GitHub） |
| `--identity-provider <URL>` | Identity Provider URL（Identity Center 用） |
| `--region <REGION>` | AWS リージョン（Identity Center 用） |
| `--social <PROVIDER>` | ソーシャルプロバイダー: `google` または `github` |
| `--use-device-flow` | デバイスフロー強制（リモート/SSH 環境用） |
| `--verbose` | ログ詳細度（繰返し可） |
| `--help` | ヘルプ表示 |

**認証方式**:

| 環境 | 動作 |
|------|------|
| **ローカル** | ブラウザを開いて統一認証ポータルを表示。`--license`、`--social` 等のフラグはローカルでは通常無視される |
| **リモート（SSH）** | デバイスフローを自動使用。デバイスコードと URL を表示 |

```bash
# 基本ログイン（ローカルではブラウザ、リモートではデバイスコード）
kiro-cli login

# Identity Center
kiro-cli login --license pro --identity-provider https://my-org.awsapps.com/start --region us-east-1

# ソーシャルログイン
kiro-cli login --social google

# デバイスフロー強制（SSH セッション用）
kiro-cli login --use-device-flow
```

→ 詳細: [12. RemoteAuth](../01_features/12_RemoteAuth.md)

### 10. `kiro-cli logout`

サインアウトして認証情報をクリア。

```bash
kiro-cli logout
```

**クリアされるもの**: 認証トークン、セッション認証情報、ユーザープロファイル情報

**保持されるもの**: エージェント設定、保存会話、設定、MCP サーバー設定

> **注**: ログアウトはユーザー全体に作用し、すべてのワークスペースに影響します。

### 11. `kiro-cli whoami`

現在のユーザーと認証状態を表示。

```bash
kiro-cli whoami [OPTIONS]
```

| オプション | 短縮 | 説明 |
|---------|------|------|
| `--format` | `-f` | 出力形式: `plain`/`json`/`json-pretty` |
| `--verbose` | `-v` | ログ詳細度（繰返し可） |

```bash
kiro-cli whoami
kiro-cli whoami --format json-pretty
```

**出力情報**: ユーザー名/ID、認証方式（Builder ID / Identity Center / Social）、セッション状態、プロファイル情報

### 12. `kiro-cli settings`

`kiro-cli` の設定を管理。

```bash
kiro-cli settings [SUBCOMMAND] [OPTIONS] [KEY] [VALUE]
```

| 引数 | 短縮 | 説明 |
|------|------|------|
| `--delete` | `-d` | 設定を削除 |
| `--format` | `-f` | 出力形式 |
| `KEY` | — | 設定キー（位置） |
| `VALUE` | — | 設定値（位置） |

**サブコマンド**:

| サブコマンド | 説明 |
|------------|------|
| `open` | デフォルトエディタで設定ファイルを開く |
| `list` | 設定済みの設定一覧 |
| `list --all` | 利用可能な全設定を説明付きで一覧 |

```bash
kiro-cli settings list                              # 全設定
kiro-cli settings list --all                        # 全利用可能設定
kiro-cli settings telemetry.enabled                 # 特定設定取得
kiro-cli settings telemetry.enabled true            # 設定変更
kiro-cli settings --delete chat.defaultModel        # 削除
kiro-cli settings open                              # ファイルを開く
kiro-cli settings list --format json-pretty         # JSON 出力
```

→ 詳細: [01. Settings リファレンス](01_settings.md)

### 13. `kiro-cli diagnostic`

診断テストを実行し、トラブルシューティング用システム情報レポートを生成。

```bash
kiro-cli diagnostic [OPTIONS]
```

| オプション | 短縮 | 説明 |
|---------|------|------|
| `--format` | `-f` | 出力形式: `plain`/`json`/`json-pretty`（既定: `plain`） |
| `--force` | — | 限定的診断（高速、アプリ未起動でも動作） |
| `--verbose` | `-v` | ログ詳細度 |

**動作**:
- **`--force` なし**: Kiro CLI アプリの起動が必要（先に `kiro-cli launch`）。包括的な診断 |
- **`--force` あり**: スタンドアロン。アプリ未起動でも動作。限定だが高速 |

**出力情報**: システム情報（OS、アーキ、メモリ）、Kiro CLI バージョン、設定状態、環境変数、依存関係、潜在的問題

```bash
kiro-cli diagnostic
kiro-cli diagnostic --format json-pretty
kiro-cli diagnostic --force
```

### 14. `kiro-cli issue`

GitHub issue を作成（フィードバック・バグ報告用）。

```bash
kiro-cli issue [OPTIONS] [DESCRIPTION...]
```

| 引数 | 短縮 | 説明 |
|------|------|------|
| `--force` | `-f` | 強制作成 |
| `DESCRIPTION` | — | issue 説明（位置） |

```bash
kiro-cli issue
kiro-cli issue "Autocomplete not working in zsh"
```

### 15. `kiro-cli version`

バージョン情報と changelog を表示。

```bash
kiro-cli version [OPTIONS]
```

| 引数 | 説明 |
|------|------|
| `--changelog` | 現在バージョンの changelog |
| `--changelog=all` | 全バージョン changelog |
| `--changelog=x.x.x` | 特定バージョン changelog |

```bash
kiro-cli version
kiro-cli version --changelog
kiro-cli version --changelog=all
kiro-cli version --changelog=1.5.0
```

### 16. `kiro-cli mcp`

Model Context Protocol（MCP）サーバーを管理。

```bash
kiro-cli mcp [SUBCOMMAND] [OPTIONS]
```

#### `kiro-cli mcp add`

MCP サーバーを追加・置換。

| 引数 | 説明 |
|------|------|
| `--name` | サーバー名（必須） |
| `--command` | 起動コマンド（必須） |
| `--scope` | スコープ: `workspace` または `global` |
| `--env` | 環境変数: `key1=value1,key2=value2` |
| `--timeout` | 起動タイムアウト（ミリ秒） |
| `--force` | 既存サーバーを上書き |

```bash
kiro-cli mcp add --name my-server --command "node server.js" --scope workspace
```

#### `kiro-cli mcp remove`

```bash
kiro-cli mcp remove --name my-server --scope workspace
```

#### `kiro-cli mcp list`

```bash
kiro-cli mcp list                  # 全スコープ
kiro-cli mcp list workspace
kiro-cli mcp list global
```

#### `kiro-cli mcp import`

設定ファイルからインポート。

| 引数 | 説明 |
|------|------|
| `--file` | 設定ファイル（必須） |
| `--force` | 既存サーバー上書き |
| `SCOPE` | スコープ |

```bash
kiro-cli mcp import --file config.json workspace
```

#### `kiro-cli mcp status`

```bash
kiro-cli mcp status --name my-server
```

---

## セッション管理

**出典**: [Session management](https://kiro.dev/docs/cli/reference/cli-commands/#session-management)

Kiro CLI は会話のすべてのターンを自動保存。任意のセッションを再開可能。

### コマンドラインから

```bash
# 直近のセッションを再開
kiro-cli chat --resume

# セッションピッカー
kiro-cli chat --resume-picker

# 当該ディレクトリのセッション一覧
kiro-cli chat --list-sessions

# 保存済みセッションを ID で削除
kiro-cli chat --delete-session <SESSION_ID>
```

### チャットセッション内で

`/chat` コマンドを使用：

```bash
/chat new                            # 新規開始（現セッションは自動保存）
/chat new <PROMPT>                   # 初期プロンプト付き新規
/chat resume                         # セッション選択
/chat save <FILE_PATH>               # ファイルに保存
/chat load <FILE_PATH>               # ファイルから読込
```

`.json` 拡張子は省略可（Kiro が両方を試行）。

### カスタムセッションストレージ

任意の場所（VCS、クラウド、DB 等）にセッションを保存可能：

```bash
/chat save-via-script <SCRIPT_PATH>  # stdin で JSON 受信
/chat load-via-script <SCRIPT_PATH>  # stdout に JSON 出力
```

**ヒント**:
- セッション ID は UUID
- セッションはディレクトリ単位で保存（プロジェクトごとに分離）
- 最近更新されたセッションが上に表示

---

## ログファイル

**出典**: [Log files](https://kiro.dev/docs/cli/reference/cli-commands/#log-files)

トラブルシューティング用にログを保持：

| OS | 場所 |
|----|------|
| macOS | `$TMPDIR/kiro-log/` |
| Linux | `$XDG_RUNTIME_DIR` または `/tmp/kiro-log/` |

### 環境変数

| 変数 | 値 | 説明 |
|------|---|------|
| `KIRO_HOME` | path | `~/.kiro` ディレクトリ（agents/prompts/skills/steering/settings/sessions）の上書き |
| `KIRO_LOG_LEVEL` | `error`/`warn`/`info`/`debug`/`trace` | ログ詳細度（既定: `error`） |
| `KIRO_LOG_NO_COLOR` | `1`/`true`/`yes` | カラーログ無効化（v1.26.0+） |

### ログレベル

| レベル | 内容 |
|------|------|
| `error` | エラーのみ（既定） |
| `warn` | 警告とエラー |
| `info` | 情報、警告、エラー |
| `debug` | デバッグ情報以上 |
| `trace` | 詳細トレースを含む全メッセージ |

```bash
# debug ログ有効化
export KIRO_LOG_LEVEL=debug
kiro-cli chat

# カラー出力無効化（CI/CD 用、v1.26.0+）
export KIRO_LOG_NO_COLOR=1
kiro-cli chat

# fish shell
set -x KIRO_LOG_LEVEL debug
set -x KIRO_LOG_NO_COLOR 1
```

> **⚠️警告**: ログファイルにはファイルパス、コードスニペット、コマンド出力等の機密情報が含まれる可能性があります。共有時は注意してください。

---

## 環境変数

設定や挙動を制御する Kiro CLI 関連環境変数：

| 変数 | 説明 |
|------|------|
| `KIRO_HOME` | `~/.kiro` ディレクトリの上書き先 |
| `KIRO_LOG_LEVEL` | ログレベル: `error`/`warn`/`info`/`debug`/`trace` |
| `KIRO_LOG_NO_COLOR` | `1`/`true`/`yes` でカラーログ無効化（v1.26.0+） |
| `KIRO_API_KEY` | Headless Mode 用 API キー（v2.0.0+、[16. v2 Major Update](../01_features/16_v2MajorUpdate.md) 参照） |
| `KIRO_ACP_RECORD_PATH` | TUI ACP 通信を記録する JSONL ファイルパス |
| `KIRO_CLI_TOOL_SEARCH_MATCHING_THRESHOLD` | Tool Search キーワード結果の最低スコア（既定: 1.5） |
| `NO_COLOR` | TUI のすべてのカラー出力を無効化 |
| `HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY` | プロキシ設定（[03_official-installation](../03_deployment/03_official-installation.md) 参照） |

---

## 関連リンク

### リファレンス（本ディレクトリ）

- [01. Settings](01_settings.md)
- [02. Slash Commands](02_slash-commands.md)
- [04. Built-in Tools](04_built-in-tools.md)

### 機能文書

- [12. RemoteAuth](../01_features/12_RemoteAuth.md) — `kiro-cli login` のリモート認証
- [13. ACP](../01_features/13_ACP.md) — `kiro-cli acp`（本ファイル対象外）
- [15. ExitCodes](../01_features/15_ExitCodes.md) — `--require-mcp-startup` 関連
- [16. v2 Major Update](../01_features/16_v2MajorUpdate.md) — `KIRO_API_KEY`、Headless Mode
- [25. AutoComplete](../01_features/25_AutoComplete.md) — `kiro-cli inline` コマンド

### デプロイ

- [03. Official Installation](../03_deployment/03_official-installation.md) — インストール手順、プロキシ設定

### 公式情報源

- [CLI commands - Kiro CLI Documentation](https://kiro.dev/docs/cli/reference/cli-commands/)（公式ページ最終更新: 2026-05-12）
- [ACP](https://kiro.dev/docs/cli/acp/) — `kiro-cli acp` の詳細

---

**Page updated**: 2026-05-24（本サイト初版）  
**公式ページ最終更新**: 2026-05-12
