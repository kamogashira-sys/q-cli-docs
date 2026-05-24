[ホーム](../README.md) > [機能詳細ガイド](README.md) > Hooks（フック）

# Kiro CLI Smart Hooks機能

**出典**: [Hooks - Kiro CLI Documentation](https://kiro.dev/docs/cli/hooks/)、[Agent Configuration Reference - hooks field](https://kiro.dev/docs/cli/custom-agents/configuration-reference#hooks-field)、[公式Changelog v1.29.0](https://kiro.dev/changelog/cli/1-29/)、CLI changelog v1.29.6

## 概要

### Smart Hooksとは

Smart Hooks は、エージェントのライフサイクルおよびツール実行の特定のタイミングでカスタムコマンドを実行する仕組みです。セキュリティ検証、ロギング、フォーマット、コンテキスト収集などの独自処理を組み込めます。

Hooks の概念は **Amazon Q Developer CLI 時代から存在し**（本サイト [Q CLI時代の hooks 比較](../../docs/01_for-users/04_best-practices/05_agent-hooks-comparison.md) 参照）、Kiro CLI v1.20.0 時点で継承されました。その後、v1.29.0 で `hooks.showStatus` 設定、v1.29.6 で `/hooks` スラッシュコマンドが追加され、運用面が強化されています。

### 主な特徴

1. **5種類のフックポイント** — `agentSpawn` / `userPromptSubmit` / `preToolUse` / `postToolUse` / `stop`
2. **JSON ベースの入出力** — STDIN で hook event を JSON 受信、STDOUT/STDERR で結果返却
3. **Exit Code による制御** — `0` 成功 / `2` ブロック（PreToolUse のみ）/ その他 警告
4. **Tool Matching** — canonical 名（`fs_write`）と alias 名（`write`）の両対応
5. **タイムアウトとキャッシュ** — `timeout_ms`（既定 30,000ms）、`cache_ttl_seconds`

### なぜ Smart Hooks が必要なのか

エージェントの自動化には次のような課題があります：

- 危険なコマンド実行を未然に防ぎたい（セキュリティ検証）
- ファイル変更後に自動でフォーマッタを走らせたい（後処理）
- 起動時に作業ディレクトリの状態（git status 等）を文脈に取り込みたい（コンテキスト収集）
- ツール使用ログを残し、監査証跡として活用したい（ロギング）

Smart Hooks は、これらの要求を **エージェント設定ファイルに宣言的に記述** することで実現します。

**公式ドキュメント原文**:

> Hooks allow you to execute custom commands at specific points during agent lifecycle and tool execution. This enables security validation, logging, formatting, context gathering, and other custom behaviors.

---

## 📋 目次

- [Hookの定義方法](#hookの定義方法)
- [Hook Event（STDIN）](#hook-eventstdin)
- [Hook Output（Exit Code）](#hook-outputexit-code)
- [Tool Matching](#tool-matching)
- [Hook Types（5種類）](#hook-types5種類)
- [MCP ツールでの例](#mcp-ツールでの例)
- [タイムアウト](#タイムアウト)
- [キャッシュ](#キャッシュ)
- [ユースケース](#ユースケース)
- [トラブルシューティング](#トラブルシューティング)
- [関連リンク](#関連リンク)

---

## Hookの定義方法

**出典**: [Hooks - Defining hooks](https://kiro.dev/docs/cli/hooks/#defining-hooks)、[Agent Configuration Reference - hooks field](https://kiro.dev/docs/cli/custom-agents/configuration-reference#hooks-field)

Hook はエージェント設定ファイル（`agent.json`）の `hooks` フィールドに記述します。エージェント設定ファイルは以下のいずれかに配置します：

| 配置場所 | スコープ | 優先度 |
|---------|---------|-------|
| `<workspace>/.kiro/agents/<name>.json` | プロジェクト固有 | 高 |
| `~/.kiro/agents/<name>.json` | ユーザー全体（グローバル） | 低 |

### `hooks` フィールドの基本書式

5種すべてのフックポイントを `[{command, matcher?}]` の配列形式で記述します：

```json
{
  "name": "secure-agent",
  "description": "セキュリティ検証付きの開発エージェント",
  "prompt": "...",
  "hooks": {
    "agentSpawn": [
      {"command": "git status --porcelain"}
    ],
    "userPromptSubmit": [
      {"command": "date '+%Y-%m-%d %H:%M:%S'"}
    ],
    "preToolUse": [
      {"matcher": "execute_bash", "command": "/usr/local/bin/validate-shell.sh"}
    ],
    "postToolUse": [
      {"matcher": "fs_write", "command": "cargo fmt --all"}
    ],
    "stop": [
      {"command": "npm test --silent"}
    ]
  }
}
```

> **重要**: `matcher` は `preToolUse` と `postToolUse` のみで有効です。`agentSpawn` / `userPromptSubmit` / `stop` は特定ツールに紐づかないため、`matcher` は記述しません。

### フィールド詳細

| フィールド | 必須 | 適用フック | 説明 |
|----------|------|----------|------|
| `command` | ✅ | 全種 | 実行するコマンド（シェル経由） |
| `matcher` | — | `preToolUse` / `postToolUse` のみ | 対象ツール名（[Tool Matching](#tool-matching) 参照） |
| `timeout_ms` | — | 全種 | タイムアウト（ミリ秒、既定 30,000） |
| `cache_ttl_seconds` | — | 全種（agentSpawn を除く） | キャッシュ有効期間（秒） |

完全な書式は [Agent Configuration Reference - hooks field](https://kiro.dev/docs/cli/custom-agents/configuration-reference#hooks-field) を参照してください。

---

## Hook Event（STDIN）

**出典**: [Hooks - Hook event](https://kiro.dev/docs/cli/hooks/#hook-event)

Hook 実行時、Kiro CLI は **JSON 形式の Hook Event を STDIN 経由で渡します**。コマンドはこの JSON を読み取り、必要に応じて処理を分岐します。

### 共通フィールド

すべての Hook Event に含まれる：

| フィールド | 説明 |
|----------|------|
| `hook_event_name` | フック種別（`agentSpawn` / `userPromptSubmit` / `preToolUse` / `postToolUse` / `stop`） |
| `cwd` | 現在の作業ディレクトリ |
| `session_id` | セッション UUID |

### ツール関連フックの追加フィールド

`preToolUse` / `postToolUse` では追加で以下が含まれる：

| フィールド | 適用フック | 説明 |
|----------|----------|------|
| `tool_name` | preToolUse / postToolUse | 実行されるツール名（canonical 形式） |
| `tool_input` | preToolUse / postToolUse | ツール固有のパラメータ |
| `tool_response` | postToolUse のみ | ツール実行結果 |

### 例：PreToolUse の Hook Event

```json
{
  "hook_event_name": "preToolUse",
  "cwd": "/current/working/directory",
  "session_id": "abc123-def456-789",
  "tool_name": "read",
  "tool_input": {
    "operations": [
      {
        "mode": "Line",
        "path": "/current/working/directory/docs/hooks.md"
      }
    ]
  }
}
```

---

## Hook Output（Exit Code）

**出典**: [Hooks - Hook output](https://kiro.dev/docs/cli/hooks/#hook-output)

Kiro CLI は Hook の **Exit Code** で動作を分岐します。

| Exit Code | 適用フック | 動作 |
|---------|----------|------|
| `0` | 全種 | 成功。STDOUT は文脈追加または非表示（フック種別による） |
| `2` | **PreToolUse のみ** | **ツール実行をブロック**。STDERR が LLM に返される |
| その他 | 全種 | フック失敗。STDERR が警告としてユーザーに表示される |

### Exit Code の意味（フック種別ごと）

| フック | Exit 0 | Exit 2 | その他 |
|------|-------|-------|------|
| AgentSpawn | STDOUT を文脈に追加 | — | STDERR 警告表示 |
| UserPromptSubmit | STDOUT を文脈に追加 | — | STDERR 警告表示 |
| **PreToolUse** | ツール実行を許可 | **ツール実行をブロック**（STDERR を LLM へ） | 警告表示後、実行は許可 |
| PostToolUse | 成功 | — | 警告表示（ツールは既に実行済み） |
| Stop | 成功 | — | STDERR 警告表示 |

> **PreToolUse の Exit Code 2** は、危険コマンドの自動ブロックなどセキュリティ用途の中核機能です。例えば `rm -rf /` のような破壊的コマンドを検出して `exit 2` を返せば、ツール実行を確実に防げます。

---

## Tool Matching

**出典**: [Hooks - Tool matching](https://kiro.dev/docs/cli/hooks/#tool-matching)

`matcher` フィールドで、フックを適用する対象ツールを指定します。**canonical 名**（`fs_read`、`fs_write`、`execute_bash`、`use_aws`）と **alias 名**（`read`、`write`、`shell`、`aws`）の両方が利用可能です。

### Matcher の書式と例

| 書式 | 意味 |
|------|------|
| `"fs_write"` または `"write"` | write ツールにマッチ |
| `"fs_read"` または `"read"` | read ツールにマッチ |
| `"execute_bash"` または `"shell"` | shell コマンド実行にマッチ |
| `"use_aws"` または `"aws"` | AWS CLI ツールにマッチ |
| `"@git"` | git MCP サーバーの全ツール |
| `"@git/status"` | git MCP サーバーの特定ツール |
| `"*"` | 全ツール（ビルトイン + MCP） |
| `"@builtin"` | ビルトインツールのみ全部 |
| matcher 省略 | 全ツールに適用 |

> **💡ワンポイント**: matcher は **内部ツール名（canonical）** を使うのが推奨です。alias 名（`read`/`write`/`shell`/`aws`）は人間に読みやすい一方、内部実装変更時に挙動が変わる可能性があります。

完全なツール名一覧は [Agent Configuration Reference - tools field](https://kiro.dev/docs/cli/custom-agents/configuration-reference#tools-field) を参照してください。

---

## Hook Types（5種類）

**出典**: [Hooks - Hook types](https://kiro.dev/docs/cli/hooks/#hook-types)

### 1. AgentSpawn

エージェントが起動された時点で1回だけ実行されます。ツール文脈なし。

**典型ユースケース**: 起動時のプロジェクト状態取得（`git status`、`pwd`、環境情報）

**Hook Event**:

```json
{
  "hook_event_name": "agentSpawn",
  "cwd": "/current/working/directory",
  "session_id": "abc123-def456-789"
}
```

**Exit Code 動作**:
- `0`: 成功。STDOUT がエージェントの文脈に追加される
- その他: STDERR を警告として表示

> **注**: AgentSpawn は **キャッシュ対象外** です（必ず最新の状態を取得するため）。

### 2. UserPromptSubmit

ユーザーがプロンプトを送信した時点で実行されます。出力は会話文脈に追加されます。

**典型ユースケース**: タイムスタンプ付与、ユーザー入力のロギング、文脈強化

**Hook Event**:

```json
{
  "hook_event_name": "userPromptSubmit",
  "cwd": "/current/working/directory",
  "session_id": "abc123-def456-789",
  "prompt": "user's input prompt"
}
```

**Exit Code 動作**:
- `0`: 成功。STDOUT が文脈に追加される
- その他: STDERR を警告として表示

### 3. PreToolUse

ツール実行の **直前** に実行されます。ツール使用を検証し、必要に応じてブロックできます。

**典型ユースケース**: 危険コマンドのブロック、許可リスト方式の権限制御、外部監査システム連携

**Hook Event**:

```json
{
  "hook_event_name": "preToolUse",
  "cwd": "/current/working/directory",
  "session_id": "abc123-def456-789",
  "tool_name": "read",
  "tool_input": {
    "operations": [
      {"mode": "Line", "path": "/path/to/file"}
    ]
  }
}
```

**Exit Code 動作**:
- `0`: ツール実行を許可
- `2`: **ツール実行をブロック**。STDERR が LLM に返される
- その他: 警告表示後、ツール実行は許可

### 4. PostToolUse

ツール実行の **直後** に、ツール結果へのアクセス権を持って実行されます。

**典型ユースケース**: ファイル書き込み後のフォーマッタ実行、変更ファイルの再ビルド、結果ロギング

**Hook Event**:

```json
{
  "hook_event_name": "postToolUse",
  "cwd": "/current/working/directory",
  "session_id": "abc123-def456-789",
  "tool_name": "read",
  "tool_input": {
    "operations": [{"mode": "Line", "path": "/path/to/file"}]
  },
  "tool_response": {
    "success": true,
    "result": ["# Hooks\n\nHooks allow you to execute..."]
  }
}
```

**Exit Code 動作**:
- `0`: 成功
- その他: STDERR 警告表示（ツールは既に実行済み）

### 5. Stop

アシスタントがユーザーへの応答を完了した時点（各ターンの最後）に実行されます。応答後の後処理に最適です。

**典型ユースケース**: コードのコンパイル、テスト、フォーマッタ、クリーンアップ

**Hook Event**:

```json
{
  "hook_event_name": "stop",
  "cwd": "/current/working/directory",
  "session_id": "abc123-def456-789"
}
```

**Exit Code 動作**:
- `0`: 成功
- その他: STDERR 警告表示

> **注**: Stop フックは特定ツールに紐づかないため、`matcher` は使用しません。

---

## MCP ツールでの例

**出典**: [Hooks - MCP example](https://kiro.dev/docs/cli/hooks/#mcp-example)

MCP ツールの場合、`tool_name` には MCP サーバー名を含む完全な名前空間付きの形式が使われます。

**例：postgres MCP サーバーの query ツール実行前のフック**:

```json
{
  "hook_event_name": "preToolUse",
  "cwd": "/current/working/directory",
  "session_id": "abc123-def456-789",
  "tool_name": "@postgres/query",
  "tool_input": {
    "sql": "SELECT * FROM orders LIMIT 10;"
  }
}
```

`agent.json` 側では：

```json
{
  "hooks": {
    "preToolUse": [
      {"matcher": "@postgres/query", "command": "/usr/local/bin/audit-sql.sh"},
      {"matcher": "@postgres", "command": "/usr/local/bin/audit-postgres-all.sh"}
    ]
  }
}
```

---

## タイムアウト

**出典**: [Hooks - Timeout](https://kiro.dev/docs/cli/hooks/#timeout)

既定のタイムアウトは **30秒（30,000ms）** です。`timeout_ms` フィールドで変更できます。

```json
{
  "hooks": {
    "preToolUse": [
      {
        "matcher": "execute_bash",
        "command": "/usr/local/bin/slow-validator.sh",
        "timeout_ms": 60000
      }
    ]
  }
}
```

タイムアウト超過時、フックは強制終了され、警告がユーザーに表示されます（PreToolUse の場合、ツールは実行されない）。

---

## キャッシュ

**出典**: [Hooks - Caching](https://kiro.dev/docs/cli/hooks/#caching)

成功したフック結果は `cache_ttl_seconds` の値に応じてキャッシュされます：

| 設定値 | 動作 |
|------|------|
| `0`（既定） | キャッシュなし（毎回実行） |
| `> 0` | 指定秒数キャッシュ |
| AgentSpawn | **常にキャッシュなし**（設定に関係なく毎回実行） |

```json
{
  "hooks": {
    "userPromptSubmit": [
      {
        "command": "/usr/local/bin/lookup-context.sh",
        "cache_ttl_seconds": 300
      }
    ]
  }
}
```

キャッシュは同一セッション内で同一の入力（prompt、cwd 等）に対して有効です。

---

## ユースケース

### ユースケース1：セキュリティ検証（PreToolUse + Exit 2）

危険なシェルコマンドをブロックします。

**`agent.json`**:

```json
{
  "hooks": {
    "preToolUse": [
      {
        "matcher": "execute_bash",
        "command": "/usr/local/bin/block-dangerous.sh"
      }
    ]
  }
}
```

**`/usr/local/bin/block-dangerous.sh`**:

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -qE 'rm -rf /|:\(\)\{:\|:&\};:|sudo dd'; then
  echo "BLOCKED: 破壊的コマンドが検出されました: $COMMAND" >&2
  exit 2
fi
exit 0
```

→ 危険コマンドを検出すると `exit 2` でブロックし、STDERR が LLM に返されます。

### ユースケース2：自動フォーマット（PostToolUse）

ファイル書き込み後に自動的にフォーマッタを走らせます。

```json
{
  "hooks": {
    "postToolUse": [
      {"matcher": "fs_write", "command": "cargo fmt --all 2>&1"}
    ]
  }
}
```

### ユースケース3：起動時コンテキスト収集（AgentSpawn）

```json
{
  "hooks": {
    "agentSpawn": [
      {"command": "echo '## Git Status'; git status --short"},
      {"command": "echo '## TODO'; grep -rn 'TODO' src/ | head -10"}
    ]
  }
}
```

→ エージェント起動時に git の状態と TODO 一覧が文脈に追加されます。

### ユースケース4：ターン終了時の自動テスト（Stop）

```json
{
  "hooks": {
    "stop": [
      {"command": "cargo test --quiet 2>&1 | tail -20"}
    ]
  }
}
```

→ アシスタントの各応答後にテストが自動実行されます。

### ユースケース5：MCP ツール監査ログ

```json
{
  "hooks": {
    "preToolUse": [
      {"matcher": "@postgres", "command": "/usr/local/bin/log-sql.sh"}
    ],
    "postToolUse": [
      {"matcher": "@postgres", "command": "/usr/local/bin/log-sql-result.sh"}
    ]
  }
}
```

→ postgres MCP の全ツール呼び出しを監査ログに記録します。

---

## トラブルシューティング

### Hook が実行されない

1. **`agent.json` の構文確認**: JSON が valid か（`jq . agent.json`）
2. **エージェント有効化確認**: `kiro-cli agent show <name>` で確認
3. **`/hooks` コマンド**（v1.29.6+）: 現在の hook 状態を確認
4. **`hooks.showStatus` 設定**（v1.29.0+）: フック実行状況を表示するには `kiro-cli settings hooks.showStatus true`
5. **コマンドの実行権限確認**: `chmod +x` を確認

### PreToolUse でブロックが効かない

- Exit Code が **`2`** であることを確認（`1` や `255` ではブロックされない）
- STDERR にメッセージを書き込んでいるか確認（LLM への通知）
- `matcher` がツール名と一致しているか確認（canonical / alias どちらでも可）

### タイムアウトが頻発

- `timeout_ms` を増やす（既定 30,000ms）
- 重い処理は別プロセスで非同期実行し、フックは結果のみ返す
- `cache_ttl_seconds` で繰り返し実行を抑制

### Hook Event の JSON が読めない

```bash
#!/bin/bash
INPUT=$(cat)        # STDIN を全文読み取り
echo "$INPUT" | jq .  # デバッグ用：構造を確認
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
```

`jq` を活用すると JSON フィールド抽出が簡潔になります。

---

## 関連リンク

### 関連機能（本サイト）

- [02. Subagents](02_Subagents.md) — Subagent でも Hooks が継承されます
- [03. PlanAgent](03_PlanAgent.md) — Plan Agent と Hooks の組み合わせ
- [13. ACP](13_ACP.md) — ACP セッションでの hooks 動作
- [17. Granular Tool Trust](17_GranularToolTrust.md) — PreToolUse Hook と権限制御の併用
- [19. Tool Search](19_ToolSearch.md) — matcher の指定方法と Tool Search の関係

### リファレンス（辞書）

- [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md) — `/hooks` コマンド（v1.29.6+ TUI 専用）
- [04_reference/04_built-in-tools.md](../04_reference/04_built-in-tools.md) — Hook の `matcher` で対象指定可能な全 18 ビルトインツール一覧

### 関連 MCP サーバー

- [26. Agent Toolkit for AWS](26_AgentToolkitForAWS.md) 🌟 — `preToolUse`/`postToolUse` Hook で AWS MCP Server の `call_aws`/`run_script` を監査可能

### Q CLI 時代との比較

- [Q CLI Agent Hooks 比較ガイド](../../docs/01_for-users/04_best-practices/05_agent-hooks-comparison.md) — Amazon Q Developer CLI 時代の Hooks 機能との差分

### 公式情報源

- [Hooks - Kiro CLI Documentation](https://kiro.dev/docs/cli/hooks/)（公式ページ最終更新: 2026-04-13）
- [Agent Configuration Reference - hooks field](https://kiro.dev/docs/cli/custom-agents/configuration-reference#hooks-field)
- [Agent Configuration Reference - tools field](https://kiro.dev/docs/cli/custom-agents/configuration-reference#tools-field)

---

**Page updated**: 2026-05-24（本サイト初版）  
**公式ページ最終更新**: 2026-04-13
