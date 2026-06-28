[ホーム](../../README.md) > [リファレンス](README.md) > Settings

# Kiro CLI Settings リファレンス

**出典**: [Settings - Kiro CLI Documentation](https://kiro.dev/docs/cli/reference/settings/)（公式ページ最終更新: 2026-06-05）

Kiro CLI のすべての設定項目を網羅的に記述する辞書的リファレンスです。各設定の意味、型、設定例を一覧します。

---

## 📋 目次

- [設定の操作](#設定の操作)
- [設定一覧（公式8カテゴリ）](#設定一覧公式8カテゴリ)
  - [1. Telemetry and privacy（テレメトリとプライバシー）](#1-telemetry-and-privacyテレメトリとプライバシー)
  - [2. Chat interface（チャットインターフェース）](#2-chat-interfaceチャットインターフェース)
  - [3. Knowledge base（ナレッジベース）](#3-knowledge-baseナレッジベース)
  - [4. Key bindings - classic（キーバインディング・クラシック）](#4-key-bindings---classicキーバインディングクラシック)
  - [5. Key bindings - terminal UI（キーバインディング・TUI）](#5-key-bindings---terminal-uiキーバインディングtui)
  - [6. Tool Search（ツール検索）](#6-tool-searchツール検索)
  - [7. Feature toggles（機能トグル）](#7-feature-toggles機能トグル)
  - [8. API and service / MCP](#8-api-and-service--mcp)
- [環境変数](#環境変数)
- [設定ファイルの場所](#設定ファイルの場所)
- [共通の設定例](#共通の設定例)
- [トラブルシューティング](#トラブルシューティング)
- [関連リンク](#関連リンク)

---

## 設定の操作

**出典**: [Accessing settings](https://kiro.dev/docs/cli/reference/settings/#accessing-settings)

```bash
# 設定済みのすべての設定を一覧
kiro-cli settings list

# 利用可能なすべての設定を説明付きで一覧
kiro-cli settings list --all

# 特定の設定を表示
kiro-cli settings telemetry.enabled

# 設定を変更
kiro-cli settings telemetry.enabled true

# 設定を削除
kiro-cli settings --delete chat.defaultModel

# 設定ファイルをエディタで開く
kiro-cli settings open
```

### 出力形式

```bash
# プレーンテキスト（デフォルト）
kiro-cli settings list

# JSON
kiro-cli settings list --format json

# 整形済み JSON
kiro-cli settings list --format json-pretty
```

---

## 設定一覧（公式8カテゴリ）

### 1. Telemetry and privacy（テレメトリとプライバシー）

| 設定 | 型 | 説明 | 例 |
|------|-----|------|-----|
| `telemetry.enabled` | boolean | テレメトリ収集の有効化/無効化 | `kiro-cli settings telemetry.enabled true` |
| `telemetryClientId` | string | テレメトリ用のクライアント識別子 | `kiro-cli settings telemetryClientId "client-123"` |

### 2. Chat interface（チャットインターフェース）

| 設定 | 型 | 説明 | 例 |
|------|-----|------|-----|
| `chat.defaultModel` | string | 会話のデフォルト AI モデル | `kiro-cli settings chat.defaultModel "claude-3-sonnet"` |
| `chat.defaultAgent` | string | デフォルトエージェント設定 | `kiro-cli settings chat.defaultAgent "my-agent"` |
| `chat.diffTool` | string | 外部 diff ツール（classic UI のみ） | `kiro-cli settings chat.diffTool "delta"` |
| `chat.greeting.enabled` | boolean | チャット開始時の挨拶表示 | `kiro-cli settings chat.greeting.enabled false` |
| `chat.editMode` | boolean | Vi 編集モード有効化（classic のみ） | `kiro-cli settings chat.editMode true` |
| `chat.enableNotifications` | boolean | デスクトップ通知有効化 | `kiro-cli settings chat.enableNotifications true` |
| `chat.notificationMethod` | string | 通知方式: `auto`/`bel`/`osc9` | `kiro-cli settings chat.notificationMethod "osc9"` |
| `chat.disableMarkdownRendering` | boolean | Markdown フォーマット無効化（classic） | `kiro-cli settings chat.disableMarkdownRendering false` |
| `chat.disableWrap` | boolean | コピペ向けにハード改行を無効化（v2.2.1+） | `kiro-cli settings chat.disableWrap true` |
| `chat.disableAutoCompaction` | boolean | 自動会話圧縮を無効化 | `kiro-cli settings chat.disableAutoCompaction true` |
| `chat.disableInheritingDefaultResources` | boolean | カスタムエージェントが既定リソース（steering / skills / AGENTS.md）を継承しないようにする（v2.10.0+、既定 `false`、global/workspace 上書き可）。※組み込みエージェントは本設定に関わらず常に継承 | `kiro-cli settings chat.disableInheritingDefaultResources true` |
| `compaction.excludeMessages` | number | 圧縮時に保持する最低メッセージペア数（既定: 2） | `kiro-cli settings compaction.excludeMessages 2` |
| `compaction.excludeContextWindowPercent` | number | 圧縮時に保持する最低コンテキストウィンドウ% | `kiro-cli settings compaction.excludeContextWindowPercent 2` |
| `chat.enablePromptHints` | boolean | 起動時ヒント表示（v1.26.0+、既定 true） | `kiro-cli settings chat.enablePromptHints false` |
| `chat.enableHistoryHints` | boolean | 履歴ヒント表示（classic のみ） | `kiro-cli settings chat.enableHistoryHints true` |
| `chat.uiMode` | string | UI バリアント | `kiro-cli settings chat.uiMode "compact"` |
| `chat.ui` | string | UI エンジン: `tui`（既定）または `classic` | `kiro-cli settings chat.ui "classic"` |
| `chat.disableGranularTrust` | boolean | 段階的信頼オプション無効化（TUI のみ） | `kiro-cli settings chat.disableGranularTrust true` |
| `chat.autoExpandToolOutput` | boolean | ツール出力を自動展開（TUI のみ） | `kiro-cli settings chat.autoExpandToolOutput true` |
| `chat.modelDefaults` | object | モデルごとのデフォルト設定（effort 等、新セッション全体に適用） | [Effort](https://kiro.dev/docs/cli/chat/effort/#persistent-defaults) 参照 |
| `chat.enableContextUsageIndicator` | boolean | プロンプトにコンテキスト使用率を表示（classic のみ） | `kiro-cli settings chat.enableContextUsageIndicator true` |
| `chat.historyMode` | string | プロンプト履歴のスコープ: `session`（既定）/ `global`（v2.5.0+、`/settings history` で設定、次セッション反映） | `kiro-cli settings chat.historyMode global` |

> **`chat.disableInheritingDefaultResources`** は **v2.10.0 で追加**された設定です。既定は `false`（カスタムエージェントは既定リソース steering / skills / AGENTS.md を継承）、`true` で継承を無効化できます（**組み込みエージェントは本設定に関わらず常に継承**）。v2.7.0 で導入された既定リソース自動継承のオプトアウト手段です。⚠️ 公式 [Settings リファレンス](https://kiro.dev/docs/cli/reference/settings/)（公式ページ最終更新 2026-06-05）は本設定が未反映のため、本サイトは [カスタムエージェント設定リファレンス](https://kiro.dev/docs/cli/custom-agents/configuration-reference/)（公式ページ最終更新 2026-06-26）を一次情報として採用しています。詳細: [31. v2.10 設定ホットリロード & リソース継承制御](../01_features/31_v210ConfigHotReload.md)

#### 表示・アクセシビリティ（Display and accessibility、terminal UI）

以下は terminal UI の表示制御。3 項目（animations/asciiArt/icons）は即時反映。`showThinking` は起動時評価（次セッションから反映）。`/settings display` からもトグル可能。

| 設定 | 型 | 既定 | 説明 | 例 |
|------|-----|------|------|-----|
| `chat.allowAnimations` | boolean | `true` | アニメーション付きスピナー/シマー。`false` で静的フレーム | `kiro-cli settings chat.allowAnimations false` |
| `chat.allowAsciiArt` | boolean | `true` | Unicode/罫線記号。`false` でプレーン ASCII にフォールバック | `kiro-cli settings chat.allowAsciiArt false` |
| `chat.allowIcons` | boolean | `true` | ステータスアイコン（●○⚠）。`false` でテキストラベル | `kiro-cli settings chat.allowIcons false` |
| `chat.showThinking` | boolean | `true` | エージェントの推論（thinking）ブロックを表示（v2.5.0+、起動時のみ反映） | `kiro-cli settings chat.showThinking false` |
| `chat.terminalTitle` | boolean ※ | 実装時確認 | ターミナルタブのセッションタイトル表示/非表示（v2.7.0+） | `kiro-cli settings chat.terminalTitle true` |
| `chat.defaultInterruptBehavior` | string | `steer` | Queue Steering の起動時既定モード（`steer`/`queue`、v2.7.0+） | `kiro-cli settings chat.defaultInterruptBehavior queue` |
| `chat.keybindings.toggleInterruptBehavior` | string | `ctrl+s` | Queue Steering の steer/queue モード切替キーバインド（v2.7.0+） | `kiro-cli settings chat.keybindings.toggleInterruptBehavior ctrl+shift+s` |

> **`KIRO_ASCII_MODE=1`** を設定すると `chat.allowAsciiArt` に関わらず ASCII モードが強制されます（環境変数節参照）。
> **ターミナルタイトル**は v2.6.0 までは `/settings display` → Terminal title でのトグルのみで CLI 設定としては提供されていませんでしたが、**v2.7.0 で `chat.terminalTitle` 設定が追加され CLI 設定としても制御可能**になりました。⚠️ 公式 [Settings リファレンス](https://kiro.dev/docs/cli/reference/settings/)（Page updated 2026-06-05）は v2.7.0 の追加が未反映（2026-06-21 取得時点）のため、本サイトは CLI 内蔵 changelog の v2.7.0 追加文言「`chat.terminalTitle setting to show or hide the session title in the terminal tab`」を一次情報として採用しています。
> ※ `chat.terminalTitle` の型は CLI 内蔵 changelog の「show or hide」表現から **boolean** と判定。既定値は公式リファレンス未反映のため**実装時確認**が必要。
> `chat.showThinking`（モデル自身の推論表示、本節）と `chat.enableThinking`（thinking ツールの有効化、Feature toggles 節）は**別物**です。
> 詳細: [27. Thinking Display](../01_features/27_ThinkingDisplay.md)、[29. v27NewCommands](../01_features/29_v27NewCommands.md)、[公式 Queue Steering](https://kiro.dev/docs/cli/chat/queue-steering/)

### 3. Knowledge base（ナレッジベース）

| 設定 | 型 | 説明 | 例 |
|------|-----|------|-----|
| `chat.enableKnowledge` | boolean | ナレッジベース機能を有効化 | `kiro-cli settings chat.enableKnowledge true` |
| `knowledge.defaultIncludePatterns` | array | デフォルト包含パターン | `kiro-cli settings knowledge.defaultIncludePatterns '["*.py", "*.js"]'` |
| `knowledge.defaultExcludePatterns` | array | デフォルト除外パターン | `kiro-cli settings knowledge.defaultExcludePatterns '["*.log", "node_modules"]'` |
| `knowledge.maxFiles` | number | インデックス対象の最大ファイル数 | `kiro-cli settings knowledge.maxFiles 1000` |
| `knowledge.chunkSize` | number | テキストチャンクサイズ | `kiro-cli settings knowledge.chunkSize 512` |
| `knowledge.chunkOverlap` | number | チャンク間オーバーラップ | `kiro-cli settings knowledge.chunkOverlap 50` |
| `knowledge.indexType` | string | インデックス種別: `Fast`/`Best` | `kiro-cli settings knowledge.indexType "fast"` |

### 4. Key bindings - classic（キーバインディング・クラシック）

> これらは **classic インターフェースのみ有効**。TUI では効果なし。

| 設定 | 型 | 説明 | 例 |
|------|-----|------|-----|
| `chat.skimCommandKey` | char | あいまい検索コマンドのキー | `kiro-cli settings chat.skimCommandKey "f"` |
| `chat.autocompletionKey` | char | 自動補完受け入れキー | `kiro-cli settings chat.autocompletionKey "Tab"` |
| `chat.tangentModeKey` | char | tangent モード切替キー | `kiro-cli settings chat.tangentModeKey "t"` |
| `chat.delegateModeKey` | char | delegate コマンド用キー | `kiro-cli settings chat.delegateModeKey "d"` |

### 5. Key bindings - terminal UI（キーバインディング・TUI）

TUI のショートカットを上書き。`ctrl+`、`shift+`、`alt+`/`meta+` 修飾子と単一キーを組み合わせて指定（例: `ctrl+shift+q`、`esc`）。無効値はビルトインのデフォルトにフォールバックします。

| 設定 | 型 | デフォルト | 説明 | 例 |
|------|-----|--------|------|-----|
| `chat.keybindings.cancelStream` | string | `esc` | ストリーミング中の応答をキャンセル | `kiro-cli settings chat.keybindings.cancelStream "ctrl+x"` |
| `chat.keybindings.closeMenu` | string | `esc` | オーバーレイパネル/ピッカーを閉じる | `kiro-cli settings chat.keybindings.closeMenu "ctrl+["` |
| `chat.keybindings.quit` | string | `ctrl+c` | チャットセッション終了 | `kiro-cli settings chat.keybindings.quit "ctrl+shift+q"` |

### 6. Tool Search（ツール検索）

オンデマンドな MCP ツール発見の設定。詳細は [19_ToolSearch.md](../01_features/19_ToolSearch.md)。

| 設定 | 型 | 説明 | 例 |
|------|-----|------|-----|
| `toolSearch.enabled` | boolean | Tool Search 有効化（既定: false） | `kiro-cli settings toolSearch.enabled true` |
| `toolSearch.minPct` | number | コンテキストウィンドウのこの%超過で起動（既定: 5） | `kiro-cli settings toolSearch.minPct 0` |
| `toolSearch.minTokens` | number | このトークン数超過で起動（既定: 50000） | `kiro-cli settings toolSearch.minTokens 0` |

### 7. Feature toggles（機能トグル）

| 設定 | 型 | 説明 | 例 |
|------|-----|------|-----|
| `chat.enableThinking` | boolean | thinking ツール有効化（複雑な推論用。`chat.showThinking`＝モデル自身の推論表示とは別物） | `kiro-cli settings chat.enableThinking true` |
| `chat.enableTangentMode` | boolean | tangent mode 有効化（classic のみ） | `kiro-cli settings chat.enableTangentMode true` |
| `introspect.tangentMode` | boolean | introspect で自動的に tangent mode（classic のみ） | `kiro-cli settings introspect.tangentMode true` |
| `chat.enableTodoList` | boolean | todo リスト有効化（classic のみ） | `kiro-cli settings chat.enableTodoList true` |
| `chat.enableCheckpoint` | boolean | checkpoint 有効化（classic のみ） | `kiro-cli settings chat.enableCheckpoint true` |
| `chat.enableDelegate` | boolean | delegate ツール有効化（classic のみ） | `kiro-cli settings chat.enableDelegate true` |
| `app.disableAutoupdates` | boolean | バックグラウンド自動更新を無効化 | `kiro-cli settings app.disableAutoupdates true` |

### 8. API and service / MCP

#### API

| 設定 | 型 | 説明 | 例 |
|------|-----|------|-----|
| `api.timeout` | number | API リクエストタイムアウト（秒） | `kiro-cli settings api.timeout 30` |

#### MCP（Model Context Protocol）

| 設定 | 型 | 説明 | 例 |
|------|-----|------|-----|
| `mcp.initTimeout` | number | MCP サーバー初期化タイムアウト | `kiro-cli settings mcp.initTimeout 10` |
| `mcp.noInteractiveTimeout` | number | 非対話的 MCP タイムアウト | `kiro-cli settings mcp.noInteractiveTimeout 5` |
| `mcp.loadedBefore` | boolean | 過去にロードされた MCP サーバーを追跡 | `kiro-cli settings mcp.loadedBefore true` |

---

## 環境変数

**出典**: [Environment variables](https://kiro.dev/docs/cli/reference/settings/#environment-variables)

| 変数 | 説明 |
|------|------|
| `KIRO_HOME` | `~/.kiro` ディレクトリ（グローバル agents/prompts/skills/steering/settings/sessions）の上書き先。同マシンで複数の独立した Kiro プロファイルを保持する用途 |
| `KIRO_LOG_NO_COLOR` | `1` でカラーログ出力を無効化 |
| `KIRO_ASCII_MODE` | `1` で ASCII モードを強制（`chat.allowAsciiArt` の設定値に優先、v2.5.0+） |
| `NO_COLOR` | 任意の値で TUI のすべてのカラー出力を無効化 |
| `KIRO_ACP_RECORD_PATH` | TUI ACP ワイヤートラフィックを記録する JSONL ファイルパス。エージェント通信プロトコル問題のデバッグ用途 |
| `KIRO_CLI_TOOL_SEARCH_MATCHING_THRESHOLD` | Tool Search キーワード結果の最低関連度スコア（既定: `1.5`） |

---

## 設定ファイルの場所

設定は `~/.kiro/settings/cli.json` に保存されます。

直接編集も可能ですが、**検証のため `kiro-cli settings` コマンドの使用が推奨**されます。

> **`KIRO_HOME` を設定している場合**: `<KIRO_HOME>/settings/cli.json` が使われます。

---

## 共通の設定例

### 基本セットアップ

```bash
# テレメトリ有効化
kiro-cli settings telemetry.enabled true

# デフォルトチャットモデル設定
kiro-cli settings chat.defaultModel "claude-3-sonnet"

# 起動時挨拶を無効化
kiro-cli settings chat.greeting.enabled false
```

### ナレッジベース設定

```bash
# ナレッジベース有効化
kiro-cli settings chat.enableKnowledge true

# 包含パターン
kiro-cli settings knowledge.defaultIncludePatterns '["*.py", "*.js", "*.md", "*.txt"]'

# 除外パターン
kiro-cli settings knowledge.defaultExcludePatterns '["*.log", "node_modules", ".git", "*.pyc"]'

# インデックス対象最大ファイル数
kiro-cli settings knowledge.maxFiles 2000
```

### 実験的機能の有効化

```bash
# thinking ツール
kiro-cli settings chat.enableThinking true

# tangent mode
kiro-cli settings chat.enableTangentMode true

# todo リスト
kiro-cli settings chat.enableTodoList true

# checkpoint
kiro-cli settings chat.enableCheckpoint true

# キーバインド設定
kiro-cli settings chat.tangentModeKey "t"
kiro-cli settings chat.delegateModeKey "d"
```

### パフォーマンスチューニング

```bash
# 遅い接続向けに API タイムアウトを延長
kiro-cli settings api.timeout 60

# ナレッジベースのチャンクサイズ調整
kiro-cli settings knowledge.chunkSize 1024

# 長い会話で自動圧縮を無効化
kiro-cli settings chat.disableAutoCompaction true
```

---

## トラブルシューティング

### 値の形式エラー

**boolean 値**: `true` または `false`（小文字）

```bash
kiro-cli settings telemetry.enabled true  # ✓ 正
kiro-cli settings telemetry.enabled True  # ✗ 誤
```

**配列値**: シングルクォートで JSON 形式

```bash
kiro-cli settings knowledge.defaultIncludePatterns '["*.py", "*.js"]'  # ✓ 正
```

**文字列値**: スペースを含む場合はクォート

```bash
kiro-cli settings chat.defaultModel "claude-3-sonnet"  # ✓ 正
```

### 設定リセット

個別設定の削除：

```bash
kiro-cli settings --delete setting.name
```

設定ファイルを手動編集：

```bash
kiro-cli settings open
```

現在の設定確認：

```bash
kiro-cli settings list --all
```

### 設定ファイル破損時

1. **現在の設定をバックアップ**:
   ```bash
   kiro-cli settings list --format json > backup.json
   ```
2. **設定ファイルを開く**:
   ```bash
   kiro-cli settings open
   ```
3. **JSON 構文を確認、または backup から復元**

---

## 関連リンク

### 機能文書（本サイト）

- [10. Conversation Compaction](../01_features/10_ConversationCompaction.md) — `compaction.*` 設定の解説
- [16. v2 Major Update](../01_features/16_v2MajorUpdate.md) — `chat.ui` 設定の TUI/classic 切替
- [17. Granular Tool Trust](../01_features/17_GranularToolTrust.md) — `chat.disableGranularTrust` 設定
- [19. Tool Search](../01_features/19_ToolSearch.md) — `toolSearch.*` 設定の解説
- [21. v2.4 New Commands](../01_features/21_v24NewCommands.md) — `chat.modelDefaults`（effort 設定）
- [22. Smart Hooks](../01_features/22_Hooks.md) 🆕 — `hooks.showStatus`、`hooks.timeoutMs` 設定
- [23. Agent Steering](../01_features/23_Steering.md) 🆕 — `KIRO_HOME` による Steering ディレクトリ変更
- [24. @file references](../01_features/24_FileReferences.md) 🆕 — Manage Prompts 関連設定
- [25. Auto Complete](../01_features/25_AutoComplete.md) 🆕 — `autocomplete.disable` 設定
- [26. Agent Toolkit for AWS](../01_features/26_AgentToolkitForAWS.md) 🌟 — `~/.kiro/settings/mcp.json` での AWS MCP Server 統合設定

### リファレンス（本ディレクトリ）

- [02. Slash Commands](02_slash-commands.md)
- [03. CLI Commands](03_cli-commands.md)
- [04. Built-in Tools](04_built-in-tools.md)

### 公式情報源

- [Settings - Kiro CLI Documentation](https://kiro.dev/docs/cli/reference/settings/)（公式ページ最終更新: 2026-06-05）
- [Custom Agents Configuration Reference](https://kiro.dev/docs/cli/custom-agents/configuration-reference/)

---

**Page updated**: 2026-05-24（本サイト初版）  
**公式ページ最終更新**: 2026-06-05
