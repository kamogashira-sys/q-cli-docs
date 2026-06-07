# Kiro CLI 変更履歴（Changelog）

このページでは、Kiro CLI（旧Amazon Q Developer CLI）の主要なバージョンアップデートと変更内容を記録しています。

## 📋 目次

- [最新バージョン](#最新バージョン)
- [バージョン履歴](#バージョン履歴)
- [変更カテゴリについて](#変更カテゴリについて)
- [移行情報](#移行情報)

---

## 最新バージョン

### v2.6.0 CLI（2026-06-05）

**主要な変更**:

**機能追加（4件）**:
- 📋 **/transcript save**: 会話を Markdown / プレーンテキスト / JSON でエクスポート
  - `/transcript save conversation.md`（既定 Markdown）、`--plain`（テキスト）、`--json`（JSON）
  - `--plain`/`--json` はページャ内の表示形式もインライン切替。形式はファイル拡張子ではなくフラグで決定
  - 詳細: [公式スラッシュコマンドリファレンス](https://kiro.dev/docs/cli/reference/slash-commands/#transcript)
- 🪟 **/title**: ターミナルウィンドウタイトルの設定・クリア・表示（表示形式 `kiro: <text>`）
  - セッショントピックまたはワークスペースパスから自動導出。手動設定は sticky（`--clear` まで保持）。60文字で truncate
  - 有効化: `/settings display` → Terminal title（OSC 0 使用。tmux は `set-titles on` が必要）
  - 詳細: [公式スラッシュコマンドリファレンス](https://kiro.dev/docs/cli/reference/slash-commands/#title)
- 🧠 **--effort フラグ**: `kiro-cli chat` 起動時に初期 effort レベル（low/medium/high/xhigh/max）を指定
- 🔧 **/knowledge update（引数なし）**: 全ナレッジベースを一括再インデックス（従来の `/knowledge update <path>` は単一エントリ）

**改善（4件）**:
- ⚙️ **/model・/effort の自動永続化**: 選択が自動保存され、`/model set-current-as-default` が不要に（[永続化の詳細](https://kiro.dev/docs/cli/chat/settings/#persistence)）
- 💡 URL をハイパーリンク化し、行折返しをまたいでもクリック可能に
- 🎨 `/settings display` パネルが Enter で完全に閉じる、フッターヒント更新
- 💡 `/transcript` がページャを最下部で開き、最新メッセージを先頭表示

**バグ修正（10件、主なもの）**:
- 🔧 `/code init` が必須言語サーバーの PATH 不在を警告
- 🔧 V2 agent のディレクトリ一覧が `.git`/`node_modules`/build ディレクトリを既定除外
- 🔒 `toolsSettings.web_fetch.trusted`/`.blocked` の URL パターンが V2 モードで適用
- 🧠 `/effort`・`--effort` が `reasoning.effort` 配下のモデルに適用
- 💡 Markdown のコードブロック・blockquote が設定 wrap モードを尊重
- 🔧 `mcp.json` の env/header/timeout オーバーライドが registry 型 MCP に反映
- 🔧 `mcp.json` 定義の MCP サーバーが registry 有効時に registry 管理サーバーと併存ロード
- 💡 プロンプト起動後の Tab パス補完が機能
- 🎨 tmux/zellij でオートコンプリートメニュー表示時の二重カーソルを修正
- 🔧 リトライ後の空レスポンスをエラーとして表示

**注記**:
- CLI内蔵changelogの日付（2026-06-04）と公式サイト表示日（2026-06-05）に差異あり。公式サイト表示日を採用。
- CLI内蔵changelogは `/title` 有効化に `chat.terminalTitle` 設定を挙げているが、公式設定リファレンス（更新 2026-06-05）は「terminal title は `/settings display` → Terminal title でトグルし、CLI 設定としては提供されない」と明記。本サイトは公式リファレンスに従う。

**出典**: `kiro-cli version --changelog=all`、[公式Changelog v2.6](https://kiro.dev/changelog/cli/2-6/)、[公式Atomフィード](https://kiro.dev/changelog/feed.atom)

---

### v2.5.1 CLI（2026-06-01）

**主要な変更**:

**改善（1件）**:
- 📡 **APIエンドポイントを `*.kiro.dev` へ移行**: アウトバウンド通信を制限している環境では、許可リストに必要なドメインを追加する必要があります（[ファイアウォール設定ガイド](https://kiro.dev/docs/privacy-and-security/firewalls/)）

**出典**: `kiro-cli version --changelog=all`、[公式Changelog v2.5](https://kiro.dev/changelog/cli/2-5/)（`#patch-2-5-1`）

---

### v2.5.0 CLI（2026-05-29）

**主要な変更**:

**機能追加（4件）**:
- 🧠 **Thinking display（推論のリアルタイム表示）**: エージェントの推論プロセスをリアルタイムで表示。**既定で有効**
  - `/settings` > Display > Show thinking でトグル（変更は次回チャットセッションから反映）
  - 設定キー `chat.showThinking`（boolean、既定 `true`、起動時のみ反映）
  - ※v2.2.0 の Adaptive Thinking（マルチターンでの推論「保持」）とは別機能（こちらは推論の「表示」）
  - 詳細: [27. Thinking Display](../01_features/27_ThinkingDisplay.md)
- 🔄 **Subagent pipelines の review loops**: reviewer ステージが implementer に作業を差し戻し、基準を満たすまで自動でループ。自己修正型のマルチエージェントワークフローを実現
  - 詳細: [02. Subagents](../01_features/02_Subagents.md)
- 📋 **Prompt history がセッション単位に（既定）**: Up/Down 矢印の履歴がセッションごとに分離。`/settings` → history で session/global を切替
  - 設定キー `chat.historyMode`（`session`(既定)/`global`、次セッションから反映）
- 🎨 **/settings display**: animations / ASCII art / icons を即時トグル

**改善（8件、主なもの）**:
- ⚡ ストリーミング中のメッセージ・シェル出力レンダリング高速化（増分更新）
- 🔧 MCP ツールコールサマリーが全パラメータ表示（4個切り詰めを廃止）
- 🔧 メニューのスクリーンリーダー対応（`/model` が現行モデルを `[active]` 表示）
- 💡 What's New ポップアップが既定で新機能のみ表示（ctrl+o で全変更）
- 🔧 ツール信頼時、同一ツールの保留呼び出しを同バッチ内で自動承認
- 🔧 ターミナルフォーカス時の通知抑制
- 🔧 誤サスペンド防止のため Ctrl+Z を2回必須に（LLM ストリーミング中）

**バグ修正（15件、主なもの）**:
- 🔒 シェル出力リダイレクトのパス検証（許可ディレクトリ外への書込み防止）
- 🔐 registry 型 MCP サーバーの OAuth 認証完了
- 🔧 `/rewind` ピッカーの小ペイン適応、`/spawn` 背景セッションの権限ダイアログ表示・起動失敗回復
- 🔧 設定ファイル I/O の NFS4 対応、COLORTERM 未設定時の Truecolor 自動検出、tmux の不可視制御文字混入防止
- 🔧 作業ディレクトリ=ホーム時の steering/skill 二重注入排除、再開セッションは直近10ターンのみ再生
- 🔧 クリップボード履歴・undo スタックの上限化、web_fetch の不正HTML回復、セッション間の設定リーク防止 ほか

**注記**:
- CLI内蔵changelogの日付（2026-05-28）と公式サイト表示日（2026-05-29）に差異あり。公式サイト表示日を採用。

**出典**: `kiro-cli version --changelog=all`、[公式Changelog v2.5](https://kiro.dev/changelog/cli/2-5/)、[公式Atomフィード](https://kiro.dev/changelog/feed.atom)

---

## バージョン履歴

### v2.4.2 CLI（2026-05-26）

**主要な変更**:

**バグ修正（1件）**:
- 🔧 **Windows: 端末入力処理のクラッシュ修正** — koffi/createRequire 起因で Windows 環境で発生していたクラッシュを修正

**影響対象**: Windows 環境（CLI 内蔵 changelog 原文に `on Windows` と明記）

**出典**: `kiro-cli version --changelog=all`、[公式Changelog v2.4](https://kiro.dev/changelog/cli/2-4/)（`#patch-2-4-2`）

---

### v2.4.1 CLI（2026-05-21）

**主要な変更**:

**バグ修正（1件）**:
- 🔧 MCPサーバー設定での`${VAR_NAME}`環境変数展開構文が認識されない問題を修正

**出典**: `kiro-cli version --changelog=all`、[公式Changelog v2.4](https://kiro.dev/changelog/cli/2-4/)

---

### v2.4.0 CLI（2026-05-20）

**主要な変更**:

**機能追加（8件）**:
- ⏪ **/rewind**: 会話の任意のプロンプトに戻り、新セッションで別方向に継続
  - 元のスレッドを失わずに代替アプローチを探索可能
  - 詳細: [公式ドキュメント](https://kiro.dev/docs/cli/chat/rewind/)
- 🧠 **/effort**: モデル推論レベル設定（low/medium/high/xhigh/max）
  - 低レベル: 高速・低コスト（単純なタスク向け）、高レベル: 複雑な問題に深い推論
  - 詳細: [公式ドキュメント](https://kiro.dev/docs/cli/chat/effort/)
- 🔧 **/settings統合メニュー**: theme/keybindings/terminal設定を統合管理
  - `/settings theme`: カラーカスタマイズ
  - `/settings keybindings`: ショートカット確認
  - `/settings terminal`: Shift+Enter / Option+Enter でマルチライン入力有効化
  - `/theme` は引き続きショートカットとして動作
  - 詳細: [公式ドキュメント](https://kiro.dev/docs/cli/chat/settings/)
- 📋 **/changelog**: リリースノートをCLI内で直接表示
- 🔧 **KIRO_ACP_RECORD_PATH**: TUI ACP wire trafficをJSONLトレースファイルに記録（デバッグ用環境変数）
- 🔧 **Per-model default settings**: `cli.json`でモデルごとのデフォルト設定を全新規セッションに適用（例: effortレベル）（→ 詳細: [04_reference/01_settings.md](../04_reference/01_settings.md)）
- 💡 **In-session surveys**: Kiro CLI体験、プラン品質、実装品質を評価するオプションアンケート
- 🔧 **Current model in agent context**: 現在のモデル名をエージェントコンテキストに含め、スキルやプロンプトがモデルに応じた動作を可能に

**改善（4件）**:
- ⚡ **Workspace初期化88%高速化**: 652ms → 76ms（ファイル監視セットアップをバックグラウンドに移動）
- 🔧 **Shell escape が $SHELL を使用**: `!` コマンドがハードコードされたbashではなく`$SHELL`のデフォルトシェルを使用（zsh/fishユーザーに恩恵）
- 💡 **モデル利用不可時のエラー改善**: `/model`の使用を提案する明確なエラーメッセージ。不明なモデルIDはサイレントフォールバックせずバックエンドに送信
- 🔧 **MCP無効時のリメディエーション**: プロファイルAPI失敗でMCPが無効化された際に具体的な修正手順を表示

**バグ修正（12件）**:
- MCPサーバー環境変数がシェル環境変数で上書きされる問題を修正
- tree-sitterパーサーの未対応言語でのパニックに対するパターン検索・書き換えの堅牢化
- `/clear`でロードされたスキルがfrontmatter-onlyに戻らない問題を修正
- macOSでのMallocStackLogging警告を修正
- リモートMCPサーバーOAuth discovery失敗時のエラーメッセージ改善
- `@`ファイルピッカーがネストされた`.gitignore`を無視し大規模ディレクトリで遅延する問題を修正
- `--help`出力に`--classic`フラグを表示
- バリデーションエラー（画像サイズ超過等）が生のreasonコードを表示する問題を修正
- ビルトインコマンドをスキルよりスラッシュコマンド補完で優先
- knowledgeBaseリソースが通常コンテキストファイルとしてロードされ重複する問題を修正
- エージェント切替時にknowledge storeが更新されず前エージェントのデータが残る問題を修正
- 引数なしMCPツール呼び出し時の無限リトライループを修正

**出典**: `kiro-cli version --changelog=all`、[公式Changelog v2.4](https://kiro.dev/changelog/cli/2-4/)、[公式Atomフィード](https://kiro.dev/changelog/feed.atom)

---

### v2.3.0 CLI（2026-05-12）

**主要な変更**:

**機能追加（8件）**:
- 🔧 **OAuth clientId設定**: DCR（Dynamic Client Registration）非対応のHTTP MCPサーバー（Slack, GitHub, Figma等）に接続するための`oauth.clientId`設定を追加
  - 詳細: [公式Agent設定リファレンス](https://kiro.dev/docs/cli/custom-agents/configuration-reference/#oauth-configuration)
- 🔧 **KIRO_HOME環境変数**: `~/.kiro`ディレクトリの場所をオーバーライドする環境変数を追加。global agents, prompts, skills, steering, settings, sessionsに適用（→ 詳細: [04_reference/01_settings.md](../04_reference/01_settings.md)）
  - 用途: 複数マシン間のdotfiles管理、仕事/個人プロファイル分離、コンテナ環境でのKiro状態隔離
  - 詳細: [公式設定リファレンス](https://kiro.dev/docs/cli/reference/settings/#environment-variables)
- 🔧 **V2 TUIキーバインド設定**: cancel（`chat.keybindings.cancelStream`）、close menu（`chat.keybindings.closeMenu`）、quit（`chat.keybindings.quit`）アクションのキーリマップが可能に
  - 修飾キー: `ctrl+`, `shift+`, `alt+`/`meta+` + 単一キー
  - 詳細: [公式設定リファレンス](https://kiro.dev/docs/cli/reference/settings/#key-bindings-terminal-ui)
  - ※v2.4.0で`/settings keybindings`コマンドから現在のショートカットを確認可能に
- 📡 **Agent Output Side Channels**: シェルコマンド実行時に`$AGENT_DISPLAY_OUT`（TUI表示のみ）と`$AGENT_CONTEXT_OUT`（ツール結果の`agent_notes`に含まれる）の2つのサイドチャネルを追加（→ 詳細: [04_reference/04_built-in-tools.md#side-channelsv230](../04_reference/04_built-in-tools.md#side-channelsv230)）
  - 詳細: [公式ビルトインツールリファレンス](https://kiro.dev/docs/cli/reference/built-in-tools/#side-channels-for-wrapper-scripts)
- ⚙️ **/session-idコマンド**: 現在のチャットセッションIDを表示。`kiro-cli chat --resume-id <ID>`でのセッション再開に使用。終了時にもresume hintを表示
  - 詳細: [公式スラッシュコマンドリファレンス](https://kiro.dev/docs/cli/reference/slash-commands/#session-id)
- 🔧 **LSP file_patterns**: `lsp.json`の言語設定で`file_patterns`グロブマッチングをサポート。標準拡張子を持たないファイル（Dockerfile等）をターゲット可能に
  - 詳細: [公式Code Intelligence](https://kiro.dev/docs/cli/code-intelligence/#custom-language-servers)
- 💡 **ペーストチップ展開**: 折りたたまれたペーストチップ上でTabキーを押すと、インライン編集可能なテキストに展開
- 📋 **サブエージェントセッションID記録**: 永続化されたサブエージェントセッションに親セッションIDを記録

**バグ修正（8件）**:
- HTTP retry警告がサイレントログではなくTUIに表示されるように修正
- Skillスラッシュコマンドで`$ARGUMENTS`や`${N}`プレースホルダーがない場合、末尾テキストをコンテキストとして渡すよう修正
- 複数の折りたたみテキストをペースト後のカーソル位置を修正
- リモートSSHでの描画問題を修正
- MCP registry npm/pypiサーバーでパッケージ識別子にバージョンタグが含まれる場合の動作を修正
- TUI: ツール呼び出し失敗時にツール名、試行した引数、実際の失敗理由を表示するよう修正
- ctrl-Cでターンをキャンセルした後もユーザープロンプトを会話履歴に保持するよう修正
- Registry型MCPサーバーのagent.json環境変数がTUIモードで正しく適用され、/mcp add変更がセッション間で永続化されるよう修正

**出典**: `kiro-cli version --changelog=all`、[公式Changelog v2.3](https://kiro.dev/changelog/cli/2-3/)、[公式Atomフィード](https://kiro.dev/changelog/feed.atom)

**注記**:
- CLI内蔵changelogの日付（2026-05-06）と公式サイト表示日付（2026-05-12、Atomフィード published: 2026-05-12T16:00:00Z = JST 2026-05-13 01:00）に差異あり
- 既存ドキュメントの方針に従い、**公式サイト表示日付を採用**

### v2.2.2 CLI（2026-05-05）

**主要な変更**:

**セキュリティ（1件）**:
- 🔐 **MCPガバナンス強制適用**: V2 TUIモードで、エンタープライズおよびAPI keyユーザー向けに「Kiro console MCP toggle」によるMCPガバナンスを強制適用
  - 関連: [公式MCPガバナンスドキュメント](https://kiro.dev/docs/enterprise/governance/mcp/)

**出典**: `kiro-cli version --changelog=all`
※公式Changelogサイト未掲載。CLI内蔵changelogのみで確認。

---

### v2.2.1 CLI（2026-05-04）

**主要な変更**:

**機能追加（3件）**:
- 🔧 **`chat.disableWrap`設定**: チャット出力のハード改行無効化設定を追加
  - 長い行は端末ソフトラップで視覚的に折り返されるが、論理的には単一行として保持
  - クリーンなコピー&ペースト用途
  - 型: boolean、使用例: `kiro-cli settings chat.disableWrap true`
  - 詳細: [公式設定リファレンス](https://kiro.dev/docs/cli/reference/settings/)

- ⚙️ **`/model set-current-as-default` 保存先の変更**: モデル選択の永続化先パスを変更
  - 変更前（v1.23.0時点）: `~/.kiro/settings.json`
  - 変更後（v2.2.1以降）: `~/.kiro/settings/cli.json`
  - ※本コマンド自体は v1.23.0 で初回導入。v2.2.1で保存先が変更された。
  - ※**v2.6.0で `/model`・`/effort` は選択が自動永続化され、`set-current-as-default` は不要**になりました（本ページ「最新バージョン」の v2.6.0 を参照）。
  - 詳細: [公式スラッシュコマンドリファレンス](https://kiro.dev/docs/cli/reference/slash-commands/#model)

- 💡 **TUI: `/agent swap <name>` オートコンプリート拡張**: シャドウテキスト（ゴーストテキスト）補完に対応
  - 既存の `/agent <name>` と同じ挙動
  - 詳細: [公式スラッシュコマンドリファレンス](https://kiro.dev/docs/cli/reference/slash-commands/#agent)

**セキュリティ（1件）**:
- 🔒 **code tool のワークスペース外読み込み承認必須化**: codeツールがワークスペース外のファイル読み込み時に承認を要求するように

**バグ修正（9件）**:
- 非us-east-1リージョンユーザーでのAPI key認証失敗を修正
- tmux detached セッションアタッチ時の画面フリーズと無制限メモリ増加を修正
- 端末リサイズ信号（tmuxペインフォーカス、attach/detach）での不要な再レンダリング防止（dimension guard追加）
- 非常に小さい端末幅へのリサイズ時のOOMクラッシュを修正
- CRLF（Windows）改行コードを含むファイルでの `fs_write str_replace` 失敗を修正
- TUI: `/Makefile` のような貼り付けファイルパスを「Unknown command」ではなくメッセージとして扱うよう修正
- プロセスがバックグラウンドデーモンをフォーク時のシェルコマンドハングを修正（Linux/macOS）
- `truncate_safe` による UTF-8 安全な文字列切り捨てでマルチバイト文字パニックを防止
- 組み込みbunを 1.3.12 → 1.3.13 へアップデート（端末リサイズ時の黒画面、レイアウト時間改善）

**出典**: `kiro-cli version --changelog=all`、[公式Atomフィード](https://kiro.dev/changelog/feed.atom)、[公式Changelog v2.2](https://kiro.dev/changelog/cli/2-2/)

**注記**:
- CLI内蔵changelogの日付（2026-04-29）と公式サイト表示日付（2026-05-04、Atomフィード published: 2026-05-04T00:00:00Z = JST 2026-05-04 09:00）に差異あり
- 既存ドキュメントの方針に従い、**公式サイト表示日付を採用**
- `/model set-current-as-default` は CLI内蔵changelog では「Added」と記載されているが、実態は保存先パスの変更（v1.23.0で初回導入済み）

---

### v2.2.0 CLI（2026-04-27）

**主要な変更**:
- 🧠 **Adaptive Thinking**: マルチターン会話でモデルの推論を保持し、応答品質を向上

**バグ修正（1件）**:
- サブエージェントのツールディスパッチが、MCPサーバーイベントによるキャッシュ済みツールスペック無効化時にサイレントに失敗する問題を修正

**出典**: `kiro-cli version --changelog=all`、[公式Changelog v2.2](https://kiro.dev/changelog/cli/2-2/)

---

### v2.1.0 CLI（2026-04-24）

**主要な変更**:
- 📡 **Real-Time Shell Output Streaming**: シェルコマンド出力がプロセス完了を待たずリアルタイムで行単位ストリーミング
  - ビルド、テストスイート、デプロイメントの進捗を即座に確認可能

- 🔍 **Tool Search**: MCPツールをオンデマンドでロードし、コンテキストウィンドウ使用量を削減
  - `kiro-cli settings toolSearch.enabled true`で有効化

- ⚡ **Skills as Slash Commands**: `.kiro/skills/`のSkillsを`/skill-name`スラッシュコマンドとして直接呼び出し
  - エージェント切り替えやプロンプトコピー不要

- 🔐 **Device Flow認証**: SSH、コンテナ、クラウドワークスペースからポートフォワーディング不要でGoogle/GitHub認証
  - URLとワンタイムコードをブラウザで入力（Builder ID/IAM Identity Centerと同じフロー）

- 🐧 **RHEL対応**: Red Hat Enterprise Linux上でターミナルUIが動作

**動作変更**:
- シェルコマンドの大量出力時のレンダリングパフォーマンス改善

**バグ修正（9件）**:
- Markdownテーブルレンダリングのワードラップ対応
- denyByDefault設定時の危険なシェルコマンドの承認プロンプト動作修正
- セッションピッカーのタイトル切り詰め修正
- マルチライン入力履歴のセッション間分割修正
- TUIカラーのANSIパレット再マッピング対応（`/theme`ベーステーマ切替、`NO_COLOR`環境変数対応）
- `@`メニューからファイル選択時のプロンプトヒントクリア
- スラッシュプレフィックス入力の切り詰め修正
- シェルエスケープコマンド後のペースト分割修正
- 処理中のキュー済み`!`シェルエスケープコマンドの拒否

**パッチ**:
- v2.1.1（2026-04-24）: パッチ（公式サイトにパッチ表示あり、CLI出力に詳細なし）

**出典**: `kiro-cli version --changelog=all`、[公式Changelog](https://kiro.dev/changelog/cli/2-1/)

---

### v2.0.0 CLI（2026-04-13）

**主要な変更**:
- 🪟 **Windows Support**: Kiro CLIがWindows 11上でネイティブ動作
  - PowerShellからインストール、バックグラウンド自動更新

- 🤖 **Headless Mode**: CI/CDパイプライン、自動化スクリプト向け非インタラクティブモード
  - `KIRO_API_KEY`環境変数でAPI認証
  - `--no-interactive`でプロンプト実行
  - `--trust-all-tools`または`--trust-tools`でツール権限事前付与
  - Pro、Pro+、Power契約者向け

**動作変更**:
- ⚠️ **Terminal UIがデフォルトに**: 新TUIがデフォルトチャットインターフェース
  - `Ctrl+G`: Crew Monitor（サブエージェント活動リアルタイム追跡）
  - `/theme`: カラーカスタマイズ
  - `/copy`: SSH越しクリップボードアクセス
  - `/transcript`: 会話履歴をページャーで表示
  - `/guide`: オンボーディングエージェントに切替
  - `/spawn`: 並列エージェントセッション実行
  - サブエージェントのタスク依存関係サポート
  - `--classic`または`kiro-cli settings chat.ui "classic"`で従来UIに切替可能

**新規設定・環境変数**:
- `KIRO_API_KEY`: Headless Mode用API認証
- `chat.ui`: チャットUIの選択（`"tui"`/`"classic"`）

**パッチ**:
- v2.0.1（2026-04-16）: `--trust-all-tools`が非インタラクティブモードで無視される問題を修正

**出典**: `kiro-cli version --changelog=all`、[公式Changelog](https://kiro.dev/changelog/cli/2-0/)

---

### v1.29.x CLI（2026-04-01〜04-11）

公式Changelogサイトに独立ページなし。`kiro-cli version --changelog=all`にのみ存在する9バージョン（v1.29.0〜v1.29.8）。TUIのコア機能追加とバグ修正が集中したリリース期間。

**主要な変更**:
- 🖥️ **TUI全コア機能対応**（v1.29.0）: サブエージェント、Code Intelligence、タスク管理がTUIで利用可能に
- 🎨 **`/theme`コマンド**（v1.29.3）: テーマカラーのカスタマイズ、コードdiffカラー設定
- 📋 **`/guide`コマンド**（v1.29.7）: Kiroガイドエージェントへの切替
- 📖 **`/transcript`コマンド**（v1.29.7）: 会話履歴を`$PAGER`で表示（`Ctrl+T`）
- 📎 **`@prompt`構文**（v1.29.6）: TUI/CLI引数でプロンプトをトリガー
- 🔍 **`Ctrl+R`逆インクリメンタル検索**（v1.29.6）: TUIプロンプト入力での履歴検索
- 🔌 **MCP Registry対応**（v1.29.4）: V2 ACPコードパスでのMCPレジストリサポート
- 🛡️ **`--trust-all-tools`確認**（v1.29.8）: 確認プロンプトと警告を追加
- 💬 **`/chat new` in TUI**（v1.29.0）: TUI内でCLI再起動なしに新会話開始
- 🔧 **`/hooks`コマンド**（v1.29.6）: V2 TUIでのフック管理（→ 詳細: [01_features/22_Hooks.md](../01_features/22_Hooks.md)）

**新規設定**:
- `hooks.showStatus`: フックステータスメッセージの抑制（v1.29.0）（→ 詳細: [01_features/22_Hooks.md](../01_features/22_Hooks.md)）

**バグ修正（主要なもの）**:
- YAML frontmatterのCRLF改行対応（v1.29.0）
- 破損した履歴ファイルでのパニック修正（v1.29.0）
- V1サブエージェントのファイル読み取りアクセス修正（v1.29.1）
- ターミナルマルチプレクサでのIME入力修正（v1.29.1）
- セッション注入MCPサーバーのモードスワップ間消失修正（v1.29.2）
- Kittyプロトコルシーケンスリーク修正（v1.29.2）
- tmuxペインタイトルのAPC破損修正（v1.29.3）
- 孤立bunプロセス修正（v1.29.4）
- MCP OAuth再認証・トークン期限検出修正（v1.29.4）
- TUIモードでの入力遅延修正（v1.29.8）
- セッション再開時のツール実行中表示修正（v1.29.8）

**出典**: `kiro-cli version --changelog=all`
※公式Changelogサイトに独立ページなし

---

### v1.28.0 CLI（2026-03-20）

**主要な変更**:
- 🖥️ **新ターミナルUI（実験的）**: `kiro-cli --tui`フラグで有効化
  - ライブステータスバー、リッチMarkdownレンダリング（構文ハイライト付きコードブロック）
  - インタラクティブパネル（コンテキスト、セッション、ツール管理）
  - コンテキストオーバーレイ（ツール、ヘルプ）
  - `kiro-cli settings chat.ui "tui"`で永続設定可能

- 💬 **`/chat new`コマンド**: CLI再起動なしで新しい会話を開始

- 📋 **`--list-models`フラグ**: 利用可能なモデルを非インタラクティブに一覧表示

**バグ修正（3件）**:
- `--resume-picker`が多数のセッションがあるディレクトリで新チャットにフォールスルーする問題を修正
- `Ctrl+C`が大規模ディレクトリ走査中のglob/grepツールを中断しない問題を修正
- 単一イベントツールコールがサイレントにドロップされることによるthinkingツール無限ループを修正

**パッチ**:
- v1.28.1（2026-03-20）: シェルコマンド信頼パターンの元コマンドパス保持修正、サブエージェントへのプロンプト参照解決修正
- v1.28.2（2026-03-26）: TUI v2拡張（`/code`コマンド、`/agent create & edit`、ファイルシステムパスタブ補完、ターミナル通知、プロンプト毎クレジット/時間表示、OSC 9対応、挨拶設定）、ナレッジベースinclude/excludeパターン修正、`/clear`セッション履歴永続化修正、ACP/TUIでのdisabledTools設定対応、セッション・モデル信頼性修正、TUI非ラテン文字入力・レンダリング修正
- v1.28.3（2026-03-28）: "profileArn is required but no profiles are available"エラー修正

**出典**: `kiro-cli version --changelog=all`、[公式Changelog](https://kiro.dev/changelog/cli/1-28/)

---

### v1.27.0 CLI（2026-03-02）

**主要な変更**:
- 🤖 **Simplified Agent Creation**: `/agent create`がAI支援モードをデフォルト化
  - 従来の`/agent generate`ワークフローを統合
  - `--manual`フラグで従来のエディタベース作成も可能
  - 起動時に作成引数を直接指定してインタラクティブメニューをバイパス可能

- 🔒 **Granular Tool Trust**: ツール使用時のインタラクティブピッカーで信頼スコープを選択
  - **shellコマンド**: 完全一致/引数任意/ワイルドカードの段階的スコープ
  - **read/writeツール**: ファイルパス/ディレクトリ/ツール全体でスコープ指定
  - チェーンされたシェルコマンドの自動処理

- ⚙️ **Session Settings Tool**: セッション内で一時的に設定変更可能（→ 詳細: [04_reference/04_built-in-tools.md#sessionsession-settings-tool](../04_reference/04_built-in-tools.md#sessionsession-settings-tool)）
  - モデル選択、機能トグル、動作調整
  - 全セッションオーバーライドはインメモリで、セッション終了時に自動リセット

- 🧠 **Tree-sitter Fallback**: LSPサーバーが`textDocument/documentSymbol`をサポートしない場合のフォールバック

- 🐧 **Linux ARM対応**: aarch64でのembeddings有効化

**動作変更**:
- ⚠️ **`/agent create`と`/agent generate`の統合**: `/agent create`がAI支援モードをデフォルトに（`--manual`で従来動作）
- ツールバリデーションエラーメッセージの改善（必須フィールド表示、内部詳細非表示）

**バグ修正（18件）**:
- エージェントスワップ時のコンテキスト使用率リセット
- MCPトランスポートクローズエラーメッセージの改善
- Unix慣例に従い`$VISUAL`を`$EDITOR`より優先
- LSPクライアントのサーバー機能・動的登録の尊重
- `/agent list`のソースロケーション表示修正
- `--directory`フラグでのエージェント配置修正
- `--from`フラグのパフォーマンス改善
- 非インタラクティブモードでのASCIIバナー・UIノイズ非表示
- エージェント編集コマンドの一時ファイルバリデーション
- AI支援エージェント作成のデフォルトディレクトリ修正
- パイプされたstdioでのrawモードパニック防止
- サブエージェント/ACPエージェント設定のfile:// URI相対解決
- `/model`でのモデル切替時コンテキスト使用率リセット
- `Ctrl+C`の割り込み・プロンプト復帰動作修正
- サブエージェントのmodelフィールド尊重修正
- `Ctrl+C`でのカーソル復元・子プロセス終了
- 不正なPDFファイルのナレッジベースインデックス時クラッシュ修正
- macOSでのTLS証明書キャッシュによる起動時間1-2秒短縮

**パッチ**:
- v1.27.1（2026-03-05）: bashコマンドがターミナルアクセス時にハングする問題を修正（SIGTTIN）
- v1.27.2（2026-03-09）: マルチサブエージェント権限プロンプトでのエージェント名・クエリ表示、シンボリックリンク追跡・エージェント設定重複排除、ナレッジ検索のUTF-8マルチバイト境界パニック修正、ホームディレクトリでの不要なエージェント競合警告防止
- v1.27.3（2026-03-18）: `cleanup.periodDays`設定追加（古い会話/セッション/ナレッジベースの自動削除）、stopフックイベントペイロードにアシスタント応答を含める、同時セッション間でのTODOリスト共有修正、glob展開での読み取り不可ファイルスキップ、CLI履歴の入力毎永続化、信頼シェルコマンドパターンのallowedCommands上書き修正、git/npmコマンドのreadonly判定修正、複数承認待ちサブエージェントのスタック修正、無効なJSON応答リトライ時のツール使用履歴保持、SIGTERM時のMCP子プロセスクリーンアップ

**新規設定**:
- `cleanup.periodDays`: 古い会話/セッション/ナレッジベースの自動削除期間（v1.27.3）

**出典**: `kiro-cli version --changelog=all`、[公式Changelog](https://kiro.dev/changelog/cli/1-27/)

---

### v1.26.0 CLI（2026-02-12）

**主要な変更**:
- 📎 **@file/@directory展開**: インラインコンテンツ参照の展開機能（→ 詳細: [01_features/24_FileReferences.md](../01_features/24_FileReferences.md)）
  - チャット入力で`@file`、`@directory`を使用してファイル/ディレクトリ内容を直接参照
  
- 🔗 **統合エントリポイント**: `kiro-cli integrations install kiro-command-router`
  - Kiro統合コマンドルーターのインストール
  
- 📚 **Skills自動読み込み**: `.kiro/skills/`と`~/.kiro/skills/`のSkillsがデフォルトエージェントに自動提供（Custom Agents との関係 → [01_features/23_Steering.md](../01_features/23_Steering.md)）
  - Agent設定での明示的な`skill://`指定が不要に
  
- 🔧 **Shell tool working_dirパラメータ**: cdプレフィックス不要でワーキングディレクトリ指定
  
- 📊 **トークン数表示**: `/tools`出力でツールごとの推定トークン数とオリジン別合計を表示
  
- 💡 **UX改善**:
  - Agent名タブ補完（`/agent swap`、`/agent delete`）にゴーストテキストヒント
  - 動的モデルタブ補完（`/model`コマンド、ファジーマッチング・ゴーストテキスト）
  - `/help --legacy <command>`でコマンド固有のレガシーヘルプ
  - `chat.enablePromptHints`設定で起動時ヒント表示制御（デフォルト: true）
  
- 🔌 **ACP強化**: `--agent`フラグ対応、ACP/subagent用`code`ツール追加

**動作変更**:
- ⚠️ **Agent名が位置引数に変更**: `kiro-cli agent create my-agent`（旧: `--name my-agent`）
- ⚠️ **Agent editデフォルト変更**: 引数なしで現在のエージェントを編集
- ツール説明の切り詰め廃止（大きな説明は警告表示に変更）
- introspect検索アルゴリズム改善

**新規設定・環境変数**:
- `KIRO_LOG_NO_COLOR`: カラーログ出力の無効化
- `chat.enablePromptHints`: 起動時ヒント表示制御（デフォルト: true）

**バグ修正（11件）**:
- インタラクティブシェルプロンプトの即時表示（改行待ち不要に）
- Opus 4.6のコンテキストウィンドウオーバーフロー対応
- subagentインジケーターの`--no-interactive`フラグ対応
- `/context show`でglobパターン表示
- subagentツール・ACPでのCompaction失敗修正
- ファイル名とname fieldが異なるエージェントの検索対応
- LSPクライアントのclientInfo報告
- ACPのデフォルトエージェント読み込み修正
- `/clear`コマンドのANSI出力文字化け修正
- ホームディレクトリでのsteering重複排除（`/context show`）
- CLI終了時のMCPサーバープロセス正常終了

**出典**: `kiro-cli version --changelog=all`（CLI起動メッセージ）

**パッチ**:
- v1.26.2（2026-02-17）: コンテキストウィンドウオーバーフローエラー時のAuto compaction修正

---

### v1.25.1 CLI（2026-02-12）

**主要な変更**:
- 🔐 **External Identity Provider対応**: Okta/Microsoft Entra IDによるEnterprise SSO
  - IAM Identity Centerと併用可能
  - SCIM自動プロビジョニング
  - IDE/CLI共通設定
  - ブラウザベースOAuthフロー

**詳細**: [Kiro CLI v1.25.1 Changelog](https://kiro.dev/changelog/cli/external-identity-provider-support-for-kiro-cli/)

---

### v1.25.0 CLI（2026-02-04）

**主要な変更**:
- 🔌 **Agent Client Protocol (ACP)**: JetBrains IDEs、Zed等のACP対応エディタでKiroをカスタムエージェントとして使用可能
  - `kiro-cli acp`コマンドでJSON-RPC over stdin/stdout通信
  - 標準ACPメソッド + Kiro拡張（スラッシュコマンド、MCPツール、セッション管理）
  - セッション保存: `~/.kiro/sessions/cli/`
  
- 💡 **Help Agent**: Kiro CLIドキュメントを使用した組み込みヘルプエージェント
  - `/help`コマンドで切り替え、`/help <質問>`で直接質問
  - コマンド、ツール、設定、機能について即座に回答
  - `.kiro/`ディレクトリに設定ファイルを作成可能
  
- 🔒 **Enterprise Web Tools Governance**: 組織全体でweb_search/web_fetchツールを無効化可能
  - 管理者がKiroコンソールから設定
  - 無効化時、ユーザーは`/tools`で通知を確認
  
- 🎯 **Subagent Access Control**: サブエージェントの細粒度アクセス制御
  - `availableAgents`: 起動可能なエージェントを制限
  - `trustedAgents`: 承認プロンプトなしで実行可能なエージェントを指定
  - Globパターン（`test-*`等）をサポート
  
- 🚀 **Exit Codes for CI/CD**: 構造化された終了コードで自動化をサポート
  - コード0: 成功、コード1: 一般的な失敗、コード3: MCPサーバー起動失敗
  - `--require-mcp-startup`オプションでMCPサーバー必須化

**詳細**: [Kiro CLI v1.25.0 Changelog](https://kiro.dev/changelog/cli/1-25/)

---

### v1.24.0 CLI（2026-01-16）

**主要な変更**:
- 📚 **Skills**: 大規模ドキュメント向けの段階的コンテキストロード機能
  - メタデータのみ起動時ロード、本文はオンデマンド
  - YAMLフロントマター（name、description）必須
  - `skill://` URIスキームでリソース指定
- 🎨 **Custom Diff Tools**: 外部Diffツール統合機能
  - delta、difftastic、VS Code等15種類のツール対応
  - `chat.diffTool`設定で選択可能
  - ターミナルツール8種類、GUIツール7種類をサポート
- 🔍 **AST Pattern Tools**: 構文木ベースのコード検索・変換ツール
  - **pattern-search**: 構文構造を理解した精密な検索
  - **pattern-rewrite**: ASTパターンによる安全なコード変換
  - 文字列リテラル・コメント内の誤検出を排除
- 🧠 **Improved Code Intelligence**: 18言語で組み込みコード理解機能
  - LSPセットアップ不要で即座に利用開始
  - `/code overview`コマンドで完全なワークスペース概要取得
  - `--silent`オプションでクリーンな出力
  - Bash, C, C++, C#, Elixir, Go, Java, JavaScript, Kotlin, Lua, PHP, Python, Ruby, Rust, Scala, Swift, TSX, TypeScript対応
- 📦 **Conversation Compaction**: 会話履歴の圧縮機能
  - `/compact`コマンドで手動実行
  - コンテキストウィンドウオーバーフロー時に自動実行
  - `compaction.excludeMessages`、`compaction.excludeContextWindowPercent`で設定可能
  - 新セッション作成、`/chat resume`で元のセッションに復帰可能
- 🔒 **Granular URL Permissions**: web_fetchツールのURL権限細粒度制御
  - 正規表現パターンで信頼ドメイン自動許可
  - ブロックパターンで特定サイト遮断
  - 信頼パターン外のURLは承認プロンプト表示
- 🌐 **Remote Authentication**: リモートマシンでのGoogle/GitHub認証対応
  - SSH、SSM、コンテナ環境でポートフォワーディング対応
  - Builder ID、IAM Identity Centerはデバイスコード認証標準対応

**詳細**: [Kiro CLI v1.24.0 Changelog](https://kiro.dev/changelog/cli/1-24/)

**パッチ**:
- v1.24.1（2026-01-25）: プロンプトとツールスペックの更新によるエージェント機能拡張

---

### v1.23.1 CLI（2025-12-23）

**主要な変更**:
- 🔧 **Grep/Glob Tools改善**: 実行詳細情報の追加
- 🛡️ **Subagent Security**: デフォルトエージェントでのsubagentツールを非信頼に変更
- 🐛 **Plan Agent修正**: 書き込みツールアクセスを削除
- 🔧 **コマンド改善**: /save、/loadコマンドの非推奨警告でパラメータ受け入れを修正
- 🐛 **MCP表示修正**: 無効化されたMCPサーバーが初期化中として表示される問題を修正
- 🐛 **MCP Tool名解析**: メインチャットとsubagent間でのMCPツール名解析の不整合を修正

**詳細**: [Kiro CLI v1.23.1 Changelog](https://kiro.dev/changelog/)

---

### v1.23.0 CLI（2025-12-18）

**主要な変更**:
- 🎉 **Subagents**: 複雑なタスクを専門エージェントに委譲、ライブ進捗追跡機能
- 🧠 **Plan Agent**: アイデアを構造化された実装計画に変換（Shift + Tab または /plan コマンド）
- 🔍 **Grep/Glob Tools**: 高速ファイル検索ツール（.gitignore対応）
- 💬 **Multi-Session Support**: 複数チャットセッション管理機能
- 🔌 **MCP Registry Support**: MCPツールのガバナンス機能
- 🤖 **Default Agent Prompt**: Kiro CLI機能をハイライトするデフォルトエージェントプロンプト
- ⚙️ **Model Persistence**: /model set-current-as-defaultコマンドでモデル選択を永続化（保存先: `~/.kiro/settings.json`。※v2.2.1で `~/.kiro/settings/cli.json` に変更。※v2.6.0で `/model`・`/effort` は自動永続化され `set-current-as-default` は不要）
- 🚀 **LSP Performance**: Code Intelligenceツールの読み込み時間改善

**詳細**: [Kiro CLI v1.23.0 Changelog](https://kiro.dev/changelog/subagents-plan-agent-grep-glob-tools-and-mcp-registry/)

---

### v1.22.0 CLI（2025-12-11）

**主要な変更**:
- 🧠 **Code Intelligence**: Language Server Protocol (LSP)統合による高精度コード理解機能
  - **Go-to-definition**: 関数・変数の定義箇所への即座のジャンプ
  - **Find references**: シンボルの使用箇所を全コードベースから検索
  - **Hover情報**: カーソル位置での詳細情報表示
  - **Diagnostics**: リアルタイムエラー・警告検出
  - **Kiro IDEとの統合**: IDEと同等のコード理解機能をCLIで提供
  - **コンテキスト認識**: より正確なコードナビゲーション・リファクタリング提案

- 📚 **Knowledge Index**: Agent設定での知識ベース構成と自動インデックス化
  - **カスタム知識ソース**: Agent設定でドメイン固有の知識源を定義
  - **自動同期**: コードベースとの自動同期でコンテキストを最新状態に維持
  - **ドメイン固有コンテキスト**: プロジェクト特有の知識を自動的に提供
  - **Agent Schema Configuration**: 知識ベースの構造化設定

- 🔧 **Enhanced Auto-compaction**: 長い会話の自動要約機能強化
  - **コンテキスト管理**: 会話履歴の効率的な圧縮
  - **メモリ最適化**: 重要な情報を保持しながら容量削減

- 🛡️ **Improved Guardrails**: ファイル読み取りの安全性向上
  - **アクセス制御**: ファイル操作の権限管理強化
  - **セキュリティ**: 不正なファイルアクセスの防止

**詳細**: [Code Intelligence and Knowledge Index](https://kiro.dev/changelog/code-intelligence-and-knowledge-index/)

---

### v1.21.0 CLI（2025-11-25）

**主要な変更**:
- 🌐 **Web Search & Fetch**: リアルタイムインターネット情報アクセス機能
  - **Web検索**: 最新ドキュメント・技術情報の即座検索
  - **コンテンツ取得**: URLからの直接コンテンツフェッチ
  - **ライブラリ情報**: 最新バージョン・リリース情報の取得
  - **技術問題解決**: Stack Overflow、GitHub Issues等からの解決策リサーチ
  - **ワークフロー統合**: ブラウザ切り替え不要の開発環境

- 🔧 **Built-in Tools拡張**: Web関連ツールの標準搭載
  - **web_search**: キーワードベースのWeb検索ツール
  - **web_fetch**: URL指定でのコンテンツ取得ツール
  - **開発効率化**: 情報収集からコード実装まで一元化

- 📊 **Real-time Information**: 動的情報への即座アクセス
  - **API仕様**: 最新のAPI仕様・変更点の確認
  - **ベストプラクティス**: 最新の開発手法・パターンの取得
  - **エラー解決**: リアルタイムでのエラー情報・解決策検索

**詳細**: [Web Search and Fetch for Kiro CLI](https://kiro.dev/changelog/web-search-and-fetch-for-kiro-cli/)

---

### v1.20.2 CLI（2025-11-25）

**主要な変更**:
- 🔧 **Context Management改善**: コンテキスト管理機能の向上
  - 会話履歴の効率的な管理
  - プロジェクト固有のコンテキスト保持
- 📝 **TODO Lists強化**: タスク管理機能の改善
  - タスクの構造化
  - 進捗追跡の向上
- 🐛 **バグ修正**: 安定性向上のための修正

**詳細**: [Improvements to Context Management and Todo Lists](https://kiro.dev/changelog/improvements-to-context-management-and-todo-lists/)

---

### v1.20.1 CLI（2025-11-24）

**主要な変更**:
- 🔧 **Agent修正**: Agent機能の安定性向上
  - カスタムエージェントの動作改善
  - エージェント切り替えの安定化
- 🔌 **MCP with Workspaces**: ワークスペース対応MCP機能の修正
  - マルチルートワークスペースでのMCP動作改善
- 🎨 **Code Block Styling**: コードブロック表示の改善
  - 構文ハイライトの向上
  - 表示レイアウトの最適化

**詳細**: [Fixes for Agents, MCP with Workspaces, and Code Block Styling](https://kiro.dev/changelog/fixes-for-agents-mcp-with-workspaces-and-code-block-styling/)

---

### Kiro CLI初回リリース（2025-11-17）

**🎉 Kiro CLI誕生**:
- 🚀 **Amazon Q Developer CLIからの移行**: 既存技術基盤を継承
- 🤖 **Auto Agent**: パフォーマンス・効率・品質のバランス最適化
- 🔐 **Social Login**: ソーシャルログイン対応
- 🧠 **Claude Haiku 4.5**: 新モデル対応
- 🔧 **Agent Mode**: カスタムエージェント機能
- 🔌 **MCP Support**: Model Context Protocol統合
- 📝 **Steering Files**: プロジェクト固有の設定管理（→ 詳細: [01_features/23_Steering.md](../01_features/23_Steering.md)）

**インストール**:
```bash
curl -fsSL https://cli.kiro.dev/install | bash
```

**詳細**: [Introducing Kiro CLI](https://kiro.dev/blog/introducing-kiro-cli/)

---

## 変更カテゴリについて

| カテゴリ | 記号 | 説明 |
|----------|------|------|
| **新機能** | 🎉 | 新しい機能の追加や既存機能の大幅な拡張 |
| **改善** | 🔧 | 既存機能のパフォーマンス向上や使いやすさの改善 |
| **セキュリティ** | 🛡️ | セキュリティ関連の修正や強化 |
| **バグ修正** | 🐛 | 不具合の修正 |
| **AI機能** | 🧠 | AI・機械学習関連の新機能や改善 |
| **統合機能** | 🔌 | 外部ツール・サービスとの統合機能 |
| **Web機能** | 🌐 | Web関連の新機能（検索、フェッチ等） |

---

## 移行情報

### Amazon Q Developer CLI → Kiro CLI

#### 移行タイムライン
- **2025-11-17**: Amazon Q Developer CLI v1.19.7（最終版）リリース
- **2025-11-17**: Kiro CLI初回リリース発表
- **継続性**: 既存ワークフロー・購読は継続

#### 主要な変更点

**開発形態**:
- **旧**: オープンソース（MIT License）
- **新**: クローズドソース（AWS Intellectual Property License）

**技術継承**:
- ✅ Agent機能（カスタムエージェント、設定管理）
- ✅ MCP統合（Model Context Protocol）
- ✅ Steering Files（プロジェクト固有設定）
- ✅ 既存のワークフロー・コマンド体系

**新機能追加**:
- 🆕 Auto Agent（最適化されたデフォルトエージェント）
- 🆕 Social Login（ソーシャルログイン）
- 🆕 Claude Haiku 4.5対応
- 🆕 Web Search & Fetch機能
- 🆕 Code Intelligence（LSP統合）
- 🆕 Subagents（並列タスク実行）

#### 移行方法

**既存ユーザー**:
1. Amazon Q Developer CLI v1.19.7は継続利用可能
2. Kiro CLIへの移行は任意
3. 設定・ワークフローは基本的に互換性あり

**新規ユーザー**:
```bash
# Kiro CLI インストール
curl -fsSL https://cli.kiro.dev/install | bash

# 基本的な使用方法は同じ
kiro chat "Hello, world!"
```

---

## 📚 関連リンク

- [Kiro CLI公式サイト](https://kiro.dev/cli/) - 最新情報とドキュメント
- [Kiro CLI Changelog](https://kiro.dev/changelog/) - 公式変更履歴
- [GitHub Repository](https://github.com/kirodotdev/Kiro) - Issue報告・機能要望
- [Discord Community](https://discord.gg/kirodotdev) - コミュニティサポート
- [旧Amazon Q Developer CLI](https://github.com/aws/amazon-q-developer-cli) - 旧バージョン（OSS）

---

## 🔄 更新頻度

このChangelogは以下のタイミングで更新されます：
- 新しいバージョンのリリース時
- 重要な機能追加・変更時
- セキュリティアップデートのリリース時
- コミュニティからの重要なフィードバック時

**最終更新**: 2026-06-07（v2.6.0/v2.5.1/v2.5.0対応追加、v2.4.2/v2.4.1/v2.4.0をバージョン履歴へ移動）
