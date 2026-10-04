[ホーム](../../README.md) > [リファレンス](README.md) > Settings

# Kiro CLI Settings リファレンス

**出典**: [Settings - Kiro CLI Documentation](https://kiro.dev/docs/reference/settings/)（公式ページ最終更新: 2026-10-02、実機 2.27.1 で確認）

Kiro CLI の設定項目を網羅的に記述する辞書的リファレンスです。各設定の意味、型、設定例を一覧します。構成は公式リファレンスの8カテゴリに準拠し、公式未掲載ながら実機で確認できる設定は「[補遺](#補遺-公式リファレンス未掲載の設定実機確認)」に掲載しています。

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
  - [9. Voice（音声入力）](#9-voice音声入力)
- [補遺: 公式リファレンス未掲載の設定（実機確認）](#補遺-公式リファレンス未掲載の設定実機確認)
- [環境変数](#環境変数)
- [設定ファイルの場所](#設定ファイルの場所)
- [共通の設定例](#共通の設定例)
- [トラブルシューティング](#トラブルシューティング)
- [関連リンク](#関連リンク)

---

## 設定の操作

**出典**: [Accessing settings](https://kiro.dev/docs/reference/settings/#accessing-settings)

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
| `chat.modelDefaults` | object | モデルごとのデフォルト設定（Claude 系は `output_config.effort`、GPT-5.6 系は `reasoning.effort`／`reasoning.mode`。新セッション全体に適用。`/effort set-current-as-default` の保存先） | [Effort](https://kiro.dev/docs/models/effort/#persistent-defaults-cli) 参照 |
| ~~`chat.disableAutoDefaultModel`~~ | boolean | v2.12.3 で追加された `/model` の sticky default 化のオプトアウト。**v2.14.2 実機では存在しません**（下記注記参照） | — |
| ~~`chat.disableAutoDefaultEffort`~~ | boolean | v2.12.3 で追加された `/effort` の sticky default 化のオプトアウト。**v2.14.2 実機では存在しません**（下記注記参照） | — |
| `chat.enableContextUsageIndicator` | boolean | プロンプトにコンテキスト使用率を表示（classic のみ） | `kiro-cli settings chat.enableContextUsageIndicator true` |
| `chat.historyMode` | string | プロンプト履歴のスコープ: `session`（既定）/ `global`（v2.5.0+、次セッション反映）。v2.20.1 で `kiro-cli settings` が本キーを無効として拒否する不具合が修正され、CLI からも読み書き可能 | `kiro-cli settings chat.historyMode global` |

> **`chat.disableInheritingDefaultResources`** は **v2.10.0 で追加**された設定です。既定は `false`（カスタムエージェントは既定リソース steering / skills / AGENTS.md を継承）、`true` で継承を無効化できます（**組み込みエージェントは本設定に関わらず常に継承**）。v2.7.0 で導入された既定リソース自動継承のオプトアウト手段です。⚠️ 公式 [Settings リファレンス](https://kiro.dev/docs/reference/settings/)（公式ページ最終更新 2026-06-05）は本設定が未反映のため、本サイトは [カスタムエージェント設定リファレンス](https://kiro.dev/docs/custom-agents/configuration-reference/)（公式ページ最終更新 2026-06-26）を一次情報として採用しています。詳細: [31. v2.10 設定ホットリロード & リソース継承制御](../01_features/31_v210ConfigHotReload.md)

> **`chat.disableAutoDefaultModel` / `chat.disableAutoDefaultEffort`（v2.12.3 で追加 → 現行では廃止）**
>
> これらは **v2.12.3** で追加された、`/model`・`/effort` の sticky default 化（選択が恒久デフォルトとして新セッションへ自動適用される挙動）のオプトアウト設定でした。
>
> **v2.14.1（2026-07-23）で `/model`・`/effort` の選択がセッション限定に戻り**、既定化には `set-current-as-default` を明示実行する方式になったため、オプトアウト設定は不要になりました。**v2.14.2 実機では両キーが存在しません**:
>
> ```bash
> $ kiro-cli settings chat.disableAutoDefaultModel
> error: `chat.disableAutoDefaultModel` is not a valid setting     # キー自体が存在しない
>
> $ kiro-cli settings chat.terminalTitle
> error: No value associated with chat.terminalTitle               # 有効だが未設定（対照）
> ```
>
> 上記のとおり「無効なキー」と「有効だが未設定」はメッセージが異なるため区別できます。**削除された正確なバージョンは公式に記載がありません**（本サイトは v2.14.2 実機での事実のみ記載します）。
>
> 恒久デフォルトは `chat.defaultModel`（モデル）と `chat.modelDefaults`（モデルごとの effort 等）に保持されます。出典: [公式 Changelog v2.14](https://kiro.dev/changelog/cli/2-14/)（`#patch-2-14-1`）、`kiro-cli version --changelog=2.14.1`。詳細: [28. v2.6 新コマンド](../01_features/28_v26NewCommands.md)
>
> ✅ **公式ドキュメントの現行記述（公式ページ最終更新 2026-10-02）**: [In-session settings — Model and effort preferences](https://kiro.dev/docs/cli/chat/settings/#persistence) と [Reasoning effort](https://kiro.dev/docs/models/effort/) は、`/model` でのモデル選択は現在のセッションにのみ適用され既定化には `/model set-current-as-default` が必要、`/model` のピッカーで選んだ effort はそのモデルに対して自動的に保存され、`/effort <level>` は現在のセッションだけを変える、と説明しています（本サイトが以前「公式は自動永続化のまま未反映」と注記していた点は、公式側の更新で解消されました）。

#### 表示・アクセシビリティ（Display and accessibility、terminal UI）

以下は terminal UI の表示制御。3 項目（animations/asciiArt/icons）は即時反映。`showThinking` は起動時評価（次セッションから反映）。`/settings display` からもトグル可能。

| 設定 | 型 | 既定 | 説明 | 例 |
|------|-----|------|------|-----|
| `chat.allowAnimations` | boolean | `true` | アニメーション付きスピナー/シマー。`false` で静的フレーム | `kiro-cli settings chat.allowAnimations false` |
| `chat.allowAsciiArt` | boolean | `true` | Unicode/罫線記号。`false` でプレーン ASCII にフォールバック | `kiro-cli settings chat.allowAsciiArt false` |
| `chat.allowIcons` | boolean | `true` | ステータスアイコン（●○⚠）。`false` でテキストラベル | `kiro-cli settings chat.allowIcons false` |
| `chat.showThinking` | boolean | `true` | エージェントの推論（thinking）ブロックを表示（v2.5.0+、起動時のみ反映） | `kiro-cli settings chat.showThinking false` |
| `chat.showThinkingTips` | boolean | `true` | 応答待ち中、thinking indicator下に表示される**機能ヒント**の表示/非表示（v2.15.0+） | `kiro-cli settings chat.showThinkingTips false` |
| `chat.terminalTitle` | boolean | `false` | ターミナルタブのセッションタイトル表示/非表示（v2.7.0+） | `kiro-cli settings chat.terminalTitle true` |
| `chat.preserveScrollback` | boolean | `true`（v2.21.2+） | 全画面再描画時に端末の scrollback を消去せず、viewport のみを再描画。`false` で従来の clear-and-repaint 動作に戻す。`/settings display` の Preserve scrollback からも切替可能 | `kiro-cli settings chat.preserveScrollback false` |
| `chat.spinnerVerbs` | — | — | 待機中のビジーインジケーター（スピナー）に表示する動詞をカスタマイズ（v2.21.1+）。値の書式は公式リファレンスに未記載のため断定しません | — |
| `chat.enableCustomSpinnerVerbs` | boolean | — | `chat.spinnerVerbs` によるカスタム文言を有効化（v2.21.1+） | `kiro-cli settings chat.enableCustomSpinnerVerbs true` |
| `chat.defaultInterruptBehavior` | string | `steer` | Queue Steering の起動時既定モード（`steer`/`queue`、v2.7.0+） | `kiro-cli settings chat.defaultInterruptBehavior queue` |
| `chat.keybindings.toggleInterruptBehavior` | string | `ctrl+s` | Queue Steering の steer/queue モード切替キーバインド（v2.7.0+） | `kiro-cli settings chat.keybindings.toggleInterruptBehavior ctrl+shift+s` |
| `chat.sessionDashboard.indexResponses` | boolean | `true` | [V3] セッションダッシュボード（`/sessions`）の検索対象にエージェント応答を含める（v2.21.4+）。`/settings` の **Session search** で **Prompts only**（`false`）/ **Prompts and agent responses**（`true`）を切替。**ツール出力はどちらのモードでもインデックスされません** | `kiro-cli settings chat.sessionDashboard.indexResponses false` |
| `chat.sessionDashboard.scope` | string | `current` | [V3] `/sessions` のディレクトリ範囲。`current` は現在のディレクトリ、`all` はすべてのワークスペース（v2.24.1 で既定が現在のディレクトリに）。`current workspace only` フィルタを切り替えると Kiro が更新する | `kiro-cli settings chat.sessionDashboard.scope all` |
| `chat.sessionDashboard.sortBy` | string | — | [V3] `/sessions` のソート（v2.22.0 で最終使用・セッション名・メッセージ数のソートを記憶）。**公式リファレンス未掲載・実機 2.27.1 で確認**。取り得る値は公式に記載がないため断定しません | — |
| `chat.outputStyle` | string | エージェントの既定 | [V3] 応答の書式（v2.25.0+）。`/settings display` の **Output style** で選択（v2.25.0 時点はトップレベルの `/settings`、v2.27.0 で `/settings display` 配下へ移動）。ワークスペースの値がグローバルの値より優先 | `kiro-cli settings chat.outputStyle concise` |
| `chat.startFullscreen` | boolean | — | 対話 TUI セッションを fullscreen で開始する（v2.22.0+）。`/settings` → **Display** → **Full Screen** → **Start fullscreen** に対応。**公式リファレンス未掲載・実機 2.27.1 で確認** | `kiro-cli settings chat.startFullscreen true` |
| `chat.fullscreenWheelRows` | number | `2` | fullscreen の transcript がマウスホイール 1 回で動く行数（`1`・`2`・`3`、v2.25.0+）。**Full Screen** → **Scroll speed** に対応。**公式リファレンス未掲載・実機 2.27.1 で確認**（説明文「Rows the fullscreen TUI transcript moves per mouse wheel event: 1, 2, or 3 (number, default: 2)」） | `kiro-cli settings chat.fullscreenWheelRows 3` |
| `chat.sessionDashboard.groupBy` | — | — | [V3] セッションダッシュボードの一覧のグループ化。取り得る値は公式リファレンスに未記載のため断定しません | — |
| `chat.keybindings.toggleSessionDashboard` | string | — | [V3] セッションダッシュボードの表示切替キーバインド | — |

> **`KIRO_ASCII_MODE=1`** を設定すると `chat.allowAsciiArt` に関わらず ASCII モードが強制されます（環境変数節参照）。
> **v2.12.0+**: すべての TUI グリフ・記号が ASCII モード設定（`chat.allowAsciiArt` / `KIRO_ASCII_MODE`）を尊重するよう**適用範囲が拡大**しました（Unicode 非対応端末での互換性向上。新規設定の追加ではなく既存設定の挙動拡張）。
> **ターミナルタイトル**は v2.6.0 までは `/settings display` → Terminal title でのトグルのみで CLI 設定としては提供されていませんでしたが、**v2.7.0 で `chat.terminalTitle` 設定が追加され CLI 設定としても制御可能**になりました。⚠️ 公式 [Settings リファレンス](https://kiro.dev/docs/reference/settings/)（Page updated 2026-06-05）は v2.7.0 の追加が未反映のため、型・既定値は**実機 kiro-cli 2.10.0 の `kiro-cli settings list --all` の説明文**「Show dynamic title in terminal tab (boolean, default: false)」を一次情報として採用しています（boolean・既定 `false`。CLI 内蔵 changelog v2.7.0 の追加文言とも整合）。
> **Preserve scrollback（既定値が変わりました）**: v2.20.0 で `/settings display` にトグルが追加された時点の既定は `false` でしたが、**v2.21.2 で [V3] が再描画をまたいで端末履歴を既定で保持するよう変更**され、実機 2.21.4 では既定が `true` です（設定パネル定義の `defaultValue` が真値であることを確認）。従来の clear-and-repaint 動作に戻すには `false` を設定します。ターミナル全体を消去せず viewport だけを再描画するため、左側ステータスバーが再描画境界をまたぐ場合は継ぎ目に隙間（seam gap）が表示される制約があります。なお v2.21.4 では左ステータスレール自体が撤去され、エージェント色のドット表示に置き換わりました。設定キー自体の初出バージョンは、確認できた一次情報から断定しません。
> **v2.22.0〜v2.27.0 で追加された表示関連の設定**: `chat.sessionDashboard.scope`・`chat.outputStyle` は公式 Settings リファレンス（公式ページ最終更新 2026-10-02）に掲載されています。`chat.startFullscreen`・`chat.fullscreenWheelRows`・`chat.sessionDashboard.sortBy` は公式リファレンスに未掲載で、実機 2.27.1 の `kiro-cli settings list --all` で確認しました。詳細: [41](../01_features/41_v222NewFeatures.md)・[43](../01_features/43_v224NewFeatures.md)・[44](../01_features/44_v225NewFeatures.md)・[46](../01_features/46_v227NewFeatures.md)
> **スピナー文言とセッションダッシュボードの設定**: `chat.spinnerVerbs` / `chat.enableCustomSpinnerVerbs`（v2.21.1）、`chat.sessionDashboard.indexResponses` / `chat.sessionDashboard.groupBy` / `chat.keybindings.toggleSessionDashboard` は、いずれも実機 2.21.4 に設定キーとして存在することを確認しています。型・既定値・取り得る値が公式リファレンスに記載されていない項目は、本表で「—」とし断定しません。詳細: [40. v2.21 新機能](../01_features/40_v221NewFeatures.md)
> **`chat.agentEngine` について**: 公式 Changelog v2.21.4 は `--v2` の説明で「保存された `chat.agentEngine` 値より優先される」と述べていますが、**実機 2.21.4 に `chat.agentEngine` という設定キーは存在しません**（`chat.` で始まる設定キーを全列挙して該当なし）。エンジン選択の実機経路は `--agent-engine v1|v2|v3`・`--v2`／`--v3`・環境変数 `KIRO_AGENT_ENGINE` です。詳細: [CLI コマンドリファレンス](03_cli-commands.md)
> `chat.showThinking`（モデル自身の推論表示、本節）と `chat.enableThinking`（thinking ツールの有効化、Feature toggles 節）は**別物**です。`chat.showThinkingTips`（機能ヒントの表示、本節）はさらに別物で、いずれも独立してON/OFF可能です。
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
| `chat.tangentModeKey` | char | tangent モード切替キー（V2 classic版`/tangent`のみ。V3版`/tangent`には非適用） | `kiro-cli settings chat.tangentModeKey "t"` |
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
| `chat.enableTangentMode` | boolean | tangent mode 有効化（classic のみ。v2.16.0で追加されたV3版`/tangent`（名前付き・ネスト可能）にはこの設定は**適用されません**。公式ページに当該設定の言及なし → [04_reference/02_slash-commands.md](02_slash-commands.md#tangent)） | `kiro-cli settings chat.enableTangentMode true` |
| `introspect.tangentMode` | boolean | introspect で自動的に tangent mode（classic のみ。同上、V3版には非適用） | `kiro-cli settings introspect.tangentMode true` |
| `chat.enableTodoList` | boolean | todo リスト有効化（classic のみ）。⚠️ v2.27.0 以降、V3 は `todo_list` ツールを提供しないため V3 では効果なし（公式 Settings リファレンスも同旨） | `kiro-cli settings chat.enableTodoList true` |
| `chat.enableWorkflows` | boolean | [V3] Workflows を有効化（v2.26.0+。アカウントで利用可能な場合のみ）。変更後は Kiro CLI の再起動が必要。`/settings features` の **Workflows** に対応 | `kiro-cli settings chat.enableWorkflows true` |
| `chat.enableMainAgentSubagentTool` | boolean | [V3] Workflows 有効時に、メインチャットからサブエージェントへの直接の委譲を残す（v2.27.0+、既定 `true`）。`false` でメインチャットの委譲を Workflows 経由に限定。`/settings features` の **Workflows: sub-agent tool** に対応 | `kiro-cli settings chat.enableMainAgentSubagentTool false` |
| `chat.enableCheckpoint` | boolean | checkpoint 有効化（classic のみ） | `kiro-cli settings chat.enableCheckpoint true` |
| `chat.enableDelegate` | boolean | delegate ツール有効化（classic のみ） | `kiro-cli settings chat.enableDelegate true` |
| `app.disableAutoupdates` | boolean | バックグラウンド自動更新を無効化。v2.20.1 で Windows の更新ダウンロードも停止し、temp ディレクトリに installer が蓄積しないよう修正 | `kiro-cli settings app.disableAutoupdates true` |

### 8. API and service / MCP

#### API

| 設定 | 型 | 説明 | 例 |
|------|-----|------|-----|
| `api.timeout` | number | ストリーミング応答の全体タイムアウト（秒、既定 `3600`）。応答の全期間を計測するため、1時間の既定値で長い応答も完了できる。より短い上限を強制する場合は低い値を設定 | `kiro-cli settings api.timeout 600` |
| `api.streamIdleSoftTimeout` | number | ストリーム無応答が続いた際にstall警告を表示するまでの秒数（既定 `60`） | `kiro-cli settings api.streamIdleSoftTimeout 120` |
| `api.streamIdleHardTimeout` | number | ストリーム無応答が続いた際にリクエストを中止するまでの秒数（既定 `300`） | `kiro-cli settings api.streamIdleHardTimeout 600` |
| `api.subagentTimeout` | number | サブエージェントがアイドル状態でいられる秒数（既定 `3600`）。超過すると親ターンをブロックせず自動タイムアウト | `kiro-cli settings api.subagentTimeout 1800` |

> スロットリング・5xxエラー・接続切断（ミッドストリームリセット含む）は自動でバックオフ付きリトライされるため、設定は不要です（v2.19.0〜）。

#### MCP（Model Context Protocol）

| 設定 | 型 | 説明 | 例 |
|------|-----|------|-----|
| `mcp.initTimeout` | number | MCP サーバー初期化タイムアウト | `kiro-cli settings mcp.initTimeout 10` |
| `mcp.noInteractiveTimeout` | number | 非対話的 MCP タイムアウト | `kiro-cli settings mcp.noInteractiveTimeout 5` |
| `mcp.loadedBefore` | boolean | 過去にロードされた MCP サーバーを追跡 | `kiro-cli settings mcp.loadedBefore true` |

### 9. Voice（音声入力）🆕

**出典**: [Voice mode - Kiro CLI Documentation](https://kiro.dev/docs/cli/voice/)（Page updated: 2026-08-14）

Whisper によるオンデバイス音声文字起こし（`/voice`、v2.18.0+）の設定。詳細は [37. Voice Mode](../01_features/37_VoiceMode.md)。

| 設定 | 型 | 既定値 | 説明 | 例 |
|------|-----|--------|------|-----|
| `voice.modelSize` | string | `base` | Whisper モデルサイズ（`base` または `small`） | `kiro-cli settings voice.modelSize "small"` |
| `voice.language` | string | `en` | 文字起こし言語（`auto` で自動検出） | `kiro-cli settings voice.language "auto"` |
| `voice.silenceTimeout` | integer | `5` | 無音による録音自動停止までの秒数 | `kiro-cli settings voice.silenceTimeout 10` |
| `voice.maxSessionTime` | integer | `300` | 最大録音時間（秒） | `kiro-cli settings voice.maxSessionTime 600` |
| `voice.autoSubmit` | boolean | `true` | 文字起こし結果を自動送信するか（`false` で確認待ち） | `kiro-cli settings voice.autoSubmit false` |
| `voice.serverUrl` | string | なし | クラウドデスクトップ向けリモート音声サーバー URL（`kiro-cli voice-cloud-setup` で設定） | `kiro-cli settings voice.serverUrl "http://localhost:8765"` |

> 環境変数 `KIRO_VOICE_SERVER_URL` でも `voice.serverUrl` と同等の指定が可能です（環境変数節参照）。

---

## 補遺: 公式リファレンス未掲載の設定（実機確認）

上記の8カテゴリは公式 [Settings リファレンス](https://kiro.dev/docs/reference/settings/)（Page updated 2026-06-05）の構成に準拠しています。一方、**実機の `kiro-cli settings list --all`**（kiro-cli 2.10.0、2026-07-04 確認）には公式リファレンス未掲載の設定が存在します。うち本サイトの機能文書・changelog で解説済みのものを補遺として掲載します。

| 設定 | 型 | 既定 | 説明（実機 `list --all` の説明文に基づく） | 例 |
|------|-----|------|------|-----|
| `cleanup.periodDays` | number | - | 古い会話・データを自動削除するまでの日数（v1.27.3+） | `kiro-cli settings cleanup.periodDays 90` |
| `hooks.showStatus` | boolean | `true` | フック実行ステータスメッセージの表示（v1.29.0+） | `kiro-cli settings hooks.showStatus false` |
| `introspect.progressiveMode` | boolean | - | introspect でセマンティック検索の代わりに progressive loading を使用（埋め込みモデルをダウンロードできない環境向け） | `kiro-cli settings introspect.progressiveMode true` |
| `autocomplete.disable` | boolean | - | オートコンプリートの無効化（`true` で無効。キー名が **disable** である点に注意） | `kiro-cli settings autocomplete.disable true` |

> - `autocomplete.disable` は実機 2.10.0 で `kiro-cli settings autocomplete.disable` による読み書きは可能ですが、`settings list --all` の一覧には表示されません（2026-07-04 実機確認）。
> - このほか実機の `list --all` には `api.*`（サービスエンドポイント系）、`chat.agentEngine`、`chat.disableTrustAllConfirmation`、`chat.enableCodeIntelligence`、`chat.enableSubagent`、`chat.hasSeenLogo` 等の**内部向け・未文書化キー**が存在しますが、公式ドキュメントに説明がなく通常利用で変更する必要がないため、本リファレンスでは一覧掲載を見送っています。
> - 詳細解説: [22. Smart Hooks](../01_features/22_Hooks.md)（`hooks.showStatus`）、[25. Auto Complete](../01_features/25_AutoComplete.md)（`autocomplete.disable`）、[04. Built-in Tools](04_built-in-tools.md)（`introspect.progressiveMode`）

---

## 環境変数

**出典**: [Environment variables](https://kiro.dev/docs/reference/settings/#environment-variables)

| 変数 | 説明 |
|------|------|
| `KIRO_HOME` | `~/.kiro` ディレクトリ（グローバル agents/prompts/skills/steering/settings/sessions）の上書き先。同マシンで複数の独立した Kiro プロファイルを保持する用途 |
| `KIRO_LOG_NO_COLOR` | `1` でカラーログ出力を無効化 |
| `KIRO_ASCII_MODE` | `1` で ASCII モードを強制（`chat.allowAsciiArt` の設定値に優先、v2.5.0+） |
| `NO_COLOR` | 任意の値で TUI のすべてのカラー出力を無効化 |
| `KIRO_ACP_RECORD_PATH` | TUI ACP ワイヤートラフィックを記録する JSONL ファイルパス。エージェント通信プロトコル問題のデバッグ用途 |
| `KIRO_CLI_TOOL_SEARCH_MATCHING_THRESHOLD` | Tool Search キーワード結果の最低関連度スコア（既定: `1.5`） |
| `KIRO_SKIP_BINARY_PINNING` | `1` でバイナリの固定（pinning）を省略する。インストールしたバイナリが固定のパスに残るストレージ制約のある環境向け（v2.22.0+）。セッション中にインストーラーがバイナリを置き換え・削除しうる場合は使わない（公式 Changelog v2.22） |
| `KIRO_HEADLESS_WORKFLOW_TIMEOUT_SECS` | [V3] `--no-interactive` 実行で Workflows の完了を待つ上限（6 時間）を短くする（v2.27.1+。CLI 内蔵 changelog のみで確認） |
| `NODE_USE_SYSTEM_CA` | [V3] は既定で OS の証明書ストアを信頼する（v2.26.1+）。明示した値（`0` を含む）がある場合はその値が優先される（公式 Changelog v2.26） |

> ⚠️ **v2.24.0 以降、プロジェクトの `.env` ファイルは chat セッション・MCP サーバー・ツールへ自動で読み込まれません。** 必要な変数は Kiro の起動前にシェルで export し、MCP サーバーでは設定の `env` で `${変数名}` として参照します（公式 [MCP Configuration](https://kiro.dev/docs/mcp/configuration/#environment-variables)、→ [43. v2.24 新機能](../01_features/43_v224NewFeatures.md)）。
| `KIRO_VOICE_SERVER_URL` | クラウドデスクトップ向けリモート音声サーバー URL（`voice.serverUrl` 設定と同等、v2.18.0+） |

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
# 60分の既定タイムアウトを10分に短縮（ストリーミング応答の全体タイムアウト、v2.19.0〜）
kiro-cli settings api.timeout 600

# 遅い接続向けにstall警告までの時間を延長
kiro-cli settings api.streamIdleSoftTimeout 120

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
- [22. Smart Hooks](../01_features/22_Hooks.md) 🆕 — `hooks.showStatus` 設定
- [23. Agent Steering](../01_features/23_Steering.md) 🆕 — `KIRO_HOME` による Steering ディレクトリ変更
- [24. @file references](../01_features/24_FileReferences.md) 🆕 — Manage Prompts 関連設定
- [25. Auto Complete](../01_features/25_AutoComplete.md) 🆕 — `autocomplete.disable` 設定
- [26. Agent Toolkit for AWS](../01_features/26_AgentToolkitForAWS.md) 🌟 — `~/.kiro/settings/mcp.json` での AWS MCP Server 統合設定
- [37. Voice Mode](../01_features/37_VoiceMode.md) 🆕 — `voice.*` 設定の解説

### リファレンス（本ディレクトリ）

- [02. Slash Commands](02_slash-commands.md)
- [03. CLI Commands](03_cli-commands.md)
- [04. Built-in Tools](04_built-in-tools.md)

### 公式情報源

- [Settings - Kiro CLI Documentation](https://kiro.dev/docs/reference/settings/)（公式ページ最終更新: 2026-10-02）
- [Custom Agents Configuration Reference](https://kiro.dev/docs/custom-agents/configuration-reference/)

---

**Page updated**: 2026-10-04（v2.22.0〜v2.27.1 対応: `chat.sessionDashboard.scope`・`chat.outputStyle`・`chat.enableWorkflows`・`chat.enableMainAgentSubagentTool` を公式リファレンスに基づき追加、`chat.startFullscreen`・`chat.fullscreenWheelRows`・`chat.sessionDashboard.sortBy` を実機 2.27.1 に基づき追加、`chat.sessionDashboard.indexResponses` の既定 `true` を公式に基づき記入、`chat.enableTodoList` に V3 で無効の注記、環境変数 `KIRO_SKIP_BINARY_PINNING`・`KIRO_HEADLESS_WORKFLOW_TIMEOUT_SECS`・`NODE_USE_SYSTEM_CA` と `.env` 自動読み込み廃止の注記を追加）
**前回更新**: 2026-09-13（v2.21.2 で `chat.preserveScrollback` の既定が `false` → `true` に変更されたことを反映（実機 2.21.4 の設定パネル定義で `defaultValue` が真値であることを確認）。v2.21.1 の `chat.spinnerVerbs`・`chat.enableCustomSpinnerVerbs`、v2.21.4 の `chat.sessionDashboard.indexResponses`、および `chat.sessionDashboard.groupBy`・`chat.keybindings.toggleSessionDashboard` を追加。公式が言及する `chat.agentEngine` が実機に存在しない旨の注記を追加。前回 2026-08-29: v2.20.0 の Preserve scrollback toggle と v2.20.1 の `chat.historyMode` CLI 設定拒否修正、Windows における `app.disableAutoupdates` 修正を反映）
**公式ページ最終更新**: 2026-10-02
