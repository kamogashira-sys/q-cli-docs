[ホーム](../README.md) > [機能詳細ガイド](README.md) > Terminal UI

---

# Kiro CLI Terminal UI機能

**出典**: [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)、[公式Changelog v1.28.0](https://kiro.dev/changelog/cli/1-28/)、[公式Changelog v2.0.0](https://kiro.dev/changelog/cli/2-0/)、CLI changelog v1.28.0〜v2.0.0

## 概要

### Terminal UIとは

Terminal UIは、Kiro CLIのデフォルトチャットインターフェースです。シンタックスハイライト付きMarkdownレンダリング、インタラクティブなオーバーレイパネル、ツール実行の視覚的な進捗表示、キーボードショートカットを提供します。

### 主な特徴

1. **リッチなMarkdownレンダリング** — シンタックスハイライト、テーブル、リスト、ブロッククォート
2. **インタラクティブパネル** — コンテキスト、セッション、ツールの管理をターミナル内で完結
3. **スラッシュコマンド** — 豊富なコマンドセットによる操作
4. **キーボードショートカット** — Emacs風キルリング含む効率的な操作
5. **Crew Monitor** — サブエージェントのリアルタイム監視

### なぜTerminal UIが必要なのか

従来のクラシックインターフェースはプレーンテキストベースでした。Terminal UIにより、IDE並みのリッチな表示とインタラクティブな操作がターミナル内で実現されます。

### バージョン別進化

```
v1.28.0（2026-03-20）  実験的導入
  │  --tuiフラグで有効化、リッチMarkdown、オーバーレイパネル
  │  /chat new、--list-models
  ↓
v1.29.x（2026-04）     機能充実
  │  /theme、/guide、/transcript、/copy、/spawn
  │  @prompt、Ctrl+R、/hooks、Crew Monitor（サブエージェント対応）
  ↓
v2.0.0（2026-04-13）   デフォルト化（GA）
     Crew Monitor、タスク依存関係、安定性修正
     --classicでクラシックに切り替え可能
  ↓
v2.19.0（2026-08-19）  Spec review screenのマウス対応
     スクロール/クリック操作、`m`キーでトグル
  ↓
v2.20.0（2026-08-26）  Preserve scrollbackトグル
     `/settings display` で端末履歴保持を切替
```

## 📋 目次

- [クイックスタート](#クイックスタート)
- [チャット体験](#チャット体験)
- [エージェントとの対話](#エージェントとの対話)
- [UIコンポーネント](#uiコンポーネント)
- [スラッシュコマンド一覧](#スラッシュコマンド一覧)
- [キーボードショートカット一覧](#キーボードショートカット一覧)
- [ターミナル機能](#ターミナル機能)
- [設定](#設定)
- [Terminal UI vs Classic比較](#terminal-ui-vs-classic比較)
- [プラットフォームサポート](#プラットフォームサポート)
- [制限事項](#制限事項)
- [トラブルシューティング](#トラブルシューティング)
- [v2.22.0〜v2.33.0での進化](#v2220v2330での進化)
- [関連リンク](#関連リンク)

---

## クイックスタート

**出典**: [Terminal UI - Quick start](https://kiro.dev/docs/cli/terminal-ui/#quick-start)

```bash
# Terminal UI（デフォルト）で起動
kiro-cli chat

# クラシックインターフェースで起動
kiro-cli --classic
```

---

## チャット体験

**出典**: [Terminal UI - Chat experience](https://kiro.dev/docs/cli/terminal-ui/#chat-experience)

メッセージはエージェントの作業に合わせてインクリメンタルにストリーミングされます。レスポンスはフルMarkdownサポートで表示されます: シンタックスハイライト付きコードブロック、テーブル、リスト、ブロッククォート、ネストされたフォーマット。同期出力をサポートするターミナルではフリッカーフリーの更新が行われます。

長いレスポンスは矢印キーでスクロールできます。

### ツール表示

各ツールタイプに専用のビジュアルコンポーネントがあります。ツール実行中は以下が表示されます:

- 説明的なタイトルとスピナー
- 完了時のステータスアイコン: ✓（成功）、✗（エラー）、⏸（承認待ち）
- 折りたたみ可能な出力（`Ctrl+O`でサマリーとフル出力を切り替え）
- 長時間実行のMCP操作のプログレスバー

### セッション

`/chat`コマンドでファジーピッカーが開き、タイトルとタイムスタンプ付きの過去のセッションが表示されます。セッションはカレントワーキングディレクトリにスコープされ、クラシックインターフェースのセッションもTerminal UIで問題なくロードされます。

```bash
# 特定のセッションを再開
kiro-cli chat --resume-id <SESSION_ID>
```

---

## エージェントとの対話

**出典**: [Terminal UI - Interacting with the agent](https://kiro.dev/docs/cli/terminal-ui/#interacting-with-the-agent)

### 承認UX

ツールが権限を必要とする場合、入力欄の上に通知バーが表示され、Yes、Trust、Noのオプションが提示されます。複数のツールが同時に権限を必要とする場合、承認はキューに入り1つずつ表示されます。承認にドリルインしてバイナリのyes/noの代わりにフィードバックを提供することもできます。

シェルコマンドの信頼は異なるレベルでスコープ可能です。詳細は[Granular Tool Trust機能](17_GranularToolTrust.md)を参照してください。

### 入力方法

| 機能 | 操作方法 |
|------|---------|
| 改行 | `Shift+Enter`、`Ctrl+J`、`Alt+Enter` |
| ファイル/ディレクトリ参照 | `@path`（タブ補完ピッカー付き） |
| 画像貼り付け | `/paste`またはクリップボードから貼り付け |
| 入力キューイング | エージェント処理中に次のメッセージを入力、送信前に編集可能 |
| コマンド履歴 | `Up`/`Down`矢印キー（セッション間で永続） |
| 逆方向履歴検索 | `Ctrl+R` |
| マルチライン編集 | `/editor`で`$EDITOR`を起動（デフォルト: `vi`） |

### シェルエスケープ

`!`プレフィックスでエージェントを経由せずにシェルコマンドを実行:

```bash
!npm run build
```

出力はリアルタイムでストリーミングされます。長い出力はhead + tailビューに折りたたまれ、`Ctrl+O`で展開できます。

### リアルタイムシェル出力

**出典**: [Terminal UI - Real-time shell output](https://kiro.dev/docs/cli/terminal-ui/#real-time-shell-output)

エージェントからのシェルコマンド出力が、コマンド完了を待たずに1行ずつリアルタイムでストリーミングされます。ビルド進捗、テスト出力、デプロイメントの状況をリアルタイムで確認できます。

> **注意**: ユーザー入力を必要とするインタラクティブコマンド（`rm -i`、`npm init`、`sudo`、`ssh`ホストキープロンプト）はサポートされず、即座に終了します。`npm init -y`や`-i`なしの`rm`など非対話的な代替手段を使用してください。

---

## UIコンポーネント

**出典**: [Terminal UI - UI components](https://kiro.dev/docs/cli/terminal-ui/#ui-components)

### オーバーレイパネル

`/help`、`/context`、`/tools`、`/mcp`、`/knowledge`、`/code`などのコマンドはオーバーレイパネルとして開きます。各パネルは検索可能、スクロール可能で、`Esc`で閉じられます。

### Activity Tray

`Ctrl+X`でタスク進捗とキューに入ったメッセージを一覧表示。会話履歴をスクロールせずに状況を把握できます。

### Crew Monitor（サブエージェント）

`Ctrl+G`でマルチエージェントセッション中のサブエージェント活動をリアルタイム監視。`Ctrl+D`/`Ctrl+U`でサブエージェント間を移動、`q`で閉じます。

サブエージェントの設定と使用方法については[サブエージェント機能](02_Subagents.md)を参照してください。

### Spec review screen（`[V3]`）

**出典**: [公式Changelog v2.18](https://kiro.dev/changelog/cli/2-18/)、[公式Changelog v2.19](https://kiro.dev/changelog/cli/2-19/)

v2.18.0で導入された、V3 spec ワークフロー専用のレビュー画面です。spec フェーズのチェックポイントで `Ctrl+X` を押すと、フェーズ文書をその場で読み、変更したい箇所に**行コメントをステージング**できます。チェックポイント質問への回答時に、ステージング済みの全コメントが1件の修正依頼としてまとめてエージェントへ送信されます。

v2.19.0では、この画面に**マウス対応**が追加されました。スクロールでのナビゲーションと、クリックでのカーソル位置指定が可能になり、`m` キーでマウスモードをトグルできます。

### テーマ

3つの組み込みテーマ: dark、light、safe（SSH等の制約のあるターミナル向けANSIフォールバック）。UIはターミナルの背景を自動検出して適切なテーマを選択します。`/theme`でカラーカスタマイズとベーステーマの切り替えが可能です。

テーマはハードコードされたhex値の代わりに名前付きANSIカラーを使用するため、カラーパレットを再マッピングしたターミナルでも正しく表示されます。`NO_COLOR`環境変数を設定すると全カラー出力が無効になります。

---

## スラッシュコマンド一覧

**出典**: [Terminal UI - Slash commands](https://kiro.dev/docs/cli/terminal-ui/#slash-commands)

全パネルはファジー検索をサポートし、`Esc`で閉じられます。

| コマンド | 説明 |
|---------|------|
| `/help` | 利用可能な全コマンドを表示 |
| `/context` | ファイルごとのトークン割合付きコンテキスト内訳。`add`、`remove`、`show`、`clear`サブコマンド対応 |
| `/usage` | プログレスバーと超過情報付き使用量制限 |
| `/knowledge` | Knowledge Base管理 |
| `/prompts` | MCPおよびファイルベースのプロンプト（詳細ドリルイン付き選択メニュー） |
| `/editor` | `$EDITOR`でマルチラインプロンプトを作成 |
| `/feedback` | Kiro CLIについてのフィードバックを送信 |
| `/paste` | クリップボードから画像を貼り付け |
| `/chat` | ファジーピッカーで過去のセッションを切り替え |
| `/plan` | プランモードに入る（`Shift+Tab`でも可） |
| `/agent` | エージェントを切り替え |
| `/model` | アクティブモデルを切り替え |
| `/mcp` | MCPサーバーとレジストリのステータスを表示 |
| `/tools` | ツール権限の表示とリセット。`/tools reset`で全ランタイム権限をクリア |
| `/code` | Code Intelligenceパネル |
| `/hooks` | 設定されたフックを表示 |
| `/guide` | **[Kiro guide agent](20_GuideAgent.md)** に切り替え（ヘルプとオンボーディング、TUI専用、v1.29.7追加） 🆕 |
| `/transcript` | `$PAGER`で会話トランスクリプトを開く（`Ctrl+T`でも可） |
| `/theme` | プロンプトとレスポンステキストのテーマカラーをオーバーライド |
| `/copy` | 最後のアシスタントレスポンスをクリップボードにコピー（SSH越しでも動作） |
| `/spawn` | タスクを指定して並列エージェントセッションを実行 |
| `/clear` | 会話表示をクリア |
| `/compact` | コンパクトメッセージ表示を切り替え |
| `/reply` | 最後のメッセージに返信 |
| `/exit` | セッションを終了（`/quit`のエイリアス） |
| `/skill-name` | Skillを名前で直接呼び出し（例: `/pr-review`） |

---

## キーボードショートカット一覧

**出典**: [Terminal UI - Keyboard shortcuts](https://kiro.dev/docs/cli/terminal-ui/#keyboard-shortcuts)

### テキスト編集

Emacs風キルリングを含むコア編集ショートカット。

| ショートカット | アクション |
|--------------|----------|
| `Shift+Enter` | 改行を挿入 |
| `Ctrl+J` | 改行を挿入 |
| `Alt+Enter` | 改行を挿入 |
| `Alt+Backspace` | 前の単語を削除 |
| `Ctrl+W` | 前の単語を削除（キルリング） |
| `Ctrl+K` | 行末まで削除 |
| `Ctrl+U` | 行頭まで削除 |
| `Ctrl+Y` | ヤンク（キルリングから貼り付け） |
| `Ctrl+_` | 最後の編集を元に戻す |

### ナビゲーションと履歴

| ショートカット | アクション |
|--------------|----------|
| `Up` / `Down` | コマンド履歴をナビゲート |
| 矢印キー | 行単位でスクロール |
| `Ctrl+R` | 逆方向インクリメンタル履歴検索 |

### パネルとビュー

| ショートカット | アクション |
|--------------|----------|
| `Ctrl+G` | Crew Monitorを開く |
| `Ctrl+D` / `Ctrl+U` | サブエージェント間をナビゲート（Crew Monitor内） |
| `q` | Crew Monitorを閉じる |
| `Ctrl+X` | Activity Trayを切り替え |
| `Ctrl+T` | `$PAGER`で会話トランスクリプトを開く |
| `Ctrl+O` | ツール出力の展開/折りたたみ |
| `Esc` | パネルを閉じる、エージェントをキャンセル、プロンプトキューをクリア |

### エージェント操作

| ショートカット | アクション |
|--------------|----------|
| `Tab` | 承認オプションにドリルイン / ファイル参照のオートコンプリート |
| `Shift+Tab` | プランモードに入る |
| `Ctrl+C` | セッションを終了 |
| `Ctrl+D` | セッションを終了（チャット入力から） |

---

## ターミナル機能

**出典**: [Terminal UI - Terminal features](https://kiro.dev/docs/cli/terminal-ui/#terminal-features)

Terminal UIはターミナルの機能を検出して自動的に適応します。

| 機能 | 詳細 |
|------|------|
| プログレスインジケーター | ターミナルタブ/タイトルバーにエージェント状態を表示（ストリーミング、承認待ち、エラー） |
| クリッカブルハイパーリンク | iTerm2、WezTerm、kitty、GhosttyでMarkdownリンクがクリック可能 |
| テーマ検出 | ターミナル背景からダーク/ライトモードを自動検出 |
| 256色フォールバック | truecolor非対応ターミナルでのグレースフルデグラデーション |
| 非ASCII文字サポート | CJK文字、絵文字、アクセント付き文字が正しくレンダリング |

---

## 設定

**出典**: [Terminal UI - Configuration](https://kiro.dev/docs/cli/terminal-ui/#configuration)

### UIエンジンの優先順位

UIエンジンは以下の順序で決定されます（優先度高→低）:

1. CLIフラグ: `--tui` または `--classic`
2. 環境変数: `KIRO_CHAT_UI`
3. 設定: `chat.ui`
4. デフォルト: `tui`

### 個別機能の無効化

環境変数で特定のターミナル機能をオプトアウトできます:

```bash
KIRO_NO_HYPERLINKS=1 kiro-cli chat    # クリッカブルリンクを無効化
KIRO_NO_PROGRESS=1 kiro-cli chat      # プログレスインジケーターを無効化
KIRO_NO_SYNCHRONIZED=1 kiro-cli chat  # 同期出力を無効化
```

### キーバインドのカスタマイズ（v2.3.0〜）

**出典**: [Settings - Key bindings (terminal UI)](https://kiro.dev/docs/reference/settings/#key-bindings-terminal-ui)

V2 TUIのcancel、close menu、quitアクションのキーを変更できます。tmuxプレフィックスやターミナルバインディングとの競合を回避する場合に有用です。

| 設定キー | デフォルト | 説明 |
|---------|----------|------|
| `chat.keybindings.cancelStream` | `esc` | ストリーミング中のエージェント応答をキャンセル |
| `chat.keybindings.closeMenu` | `esc` | オーバーレイパネル・ピッカーを閉じる |
| `chat.keybindings.quit` | `ctrl+c` | チャットセッションを終了 |

修飾キー書式: `ctrl+`, `shift+`, `alt+`/`meta+` + 単一キー（例: `ctrl+shift+q`, `esc`）。無効な値はビルトインデフォルトにフォールバック。

```bash
# 例: quitをctrl+shift+qに変更
kiro-cli settings chat.keybindings.quit "ctrl+shift+q"
```

### Preserve scrollback（v2.20.0）

v2.20.0 で `/settings display` に **Preserve scrollback** トグルが追加されました。現行 CLI の `chat.preserveScrollback` は boolean、既定 `false` で、全画面再描画時にターミナルの scrollback を消去せず viewport のみを再描画します。

```bash
kiro-cli settings chat.preserveScrollback true
```

左側ステータスバーが再描画境界をまたぐ場合、継ぎ目に隙間（seam gap）が表示される制約があります。設定キー自体の初出バージョンは今回確認した一次情報から断定しません。詳細は [Settings リファレンス](../04_reference/01_settings.md) を参照してください。

### クラシックインターフェースの使用

> ⚠️ **v2.26.0（2026-09-30）以降、Classic インターフェースは非推奨です。** Classic セッションの起動時に、Classic を選んだ要因（フラグ・環境変数・設定）を示す通知が表示されます。ターミナル UI へ戻すには、`--classic` をコマンドから外す、`KIRO_CHAT_UI` を unset する、または `kiro-cli settings chat.ui "tui"` を実行してから Kiro CLI を再起動します（公式 [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/#using-the-classic-interface)、→ [45. v2.26 新機能](45_v226NewFeatures.md)）。

```bash
# 永続的に切り替え
kiro-cli settings chat.ui "classic"

# 単一セッションのみ
kiro-cli --classic
```

---

## Terminal UI vs Classic比較

**出典**: [Terminal UI vs classic](https://kiro.dev/docs/cli/terminal-ui/comparison/)（2026-04-13更新、v2.0.0時点）

Terminal UIとClassicインターフェースでは、利用可能なスラッシュコマンドと機能に差異があります。TUI専用の機能（Overlay panels、Crew Monitor、キーボードショートカット等）については、本ドキュメントの各セクションを参照してください。

### TUI専用コマンド

以下のコマンドはTerminal UIでのみ利用可能です。Classicモード（`Ctrl+S`のコマンド一覧）には表示されません。

| コマンド | 説明 |
|---------|------|
| `/theme` | テーマカラーのカスタマイズ（ライブプレビュー付き） |
| `/guide` | **[Kiro guide agent](20_GuideAgent.md)** に切り替え（ヘルプとオンボーディング、TUI専用、v1.29.7追加） 🆕 |
| `/transcript` | `$PAGER`で会話トランスクリプトを開く（`Ctrl+T`でも可） |
| `/copy` | 最後のレスポンスをクリップボードにコピー（SSH越しでも動作） |
| `/spawn` | タスクを指定して並列エージェントセッションを実行 |
| `/feedback` | フィードバックを送信（Classicの`/issue`を置き換え） |

### Classicのみ対応（TUIでは未対応）

以下のコマンド/機能はTUIではまだ利用できません。

| コマンド/機能 | TUIでのワークアラウンド |
|-------------|----------------------|
| `/changelog` | Kiro公式サイトでリリースノートを確認 |
| `/logdump` | チャット外で`kiro-cli`コマンドを使用 |
| `/experiment` | KnowledgeとTasksは常時有効。他の実験機能は再評価中 |
| `/tangent`（V2 classic版） | TUIでは未対応（V3版`/tangent`はV3セッション専用のためこの表の対象外。→ [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md#tangent)） |
| `/settings`（チャット内） | シェルから`kiro-cli settings`を使用 |
| `/issue` | TUIでは`/feedback`に置き換え |
| Vi edit mode | TUIではEmacs keybindingsのみ |
| External diff tools | TUIでは組み込みDiffビューアーを使用（[制限事項](#制限事項)も参照） |
| Inline hints and tips | TUIでは未対応 |

### 動作が異なる機能

| 項目 | Classic | Terminal UI |
|------|---------|-------------|
| Shell tool output | リアルタイムストリーミング | v2.1.0でリアルタイムストリーミングに対応（v2.0.0時点ではバッファ方式） |
| Interactive commands | `rm -i`、`sudo`、`ssh`プロンプトが動作 | 非対応（非対話的代替手段を使用） |
| `/help` | ヘルプエージェントを起動（対話型Q&A） | 検索可能なコマンドパネルを表示 |
| Approval flow | y/n/tテキストメニュー | 通知バー + ドリルインフィードバック |
| Multi-line input | `Alt+Enter`、`Ctrl+J`、バックスラッシュ継続 | `Shift+Enter`、`Alt+Enter`、`Ctrl+J`（バックスラッシュなし） |
| Prompt indicators | プロファイル、コンテキスト% | エージェントチップ、モデルチップ、コンテキスト%、gitブランチ、cwd |
| Notifications | システム通知 | システム通知 + アプリ内通知バー |

---

## プラットフォームサポート

**出典**: [Terminal UI - Platform support](https://kiro.dev/docs/cli/terminal-ui/#platform-support)

Terminal UIはmacOS、Linux（Red Hat Enterprise Linux含む）、Windowsでサポートされています。

---

## 制限事項

**出典**: [Terminal UI - Limitations](https://kiro.dev/docs/cli/terminal-ui/#limitations)

- ビルドに埋め込みアセットが必要。利用できない場合、Kiroはクラシックインターフェースにフォールバック
- エージェントのシェルツールはユーザー入力を必要とするインタラクティブコマンドをサポートしない
- 外部Diffツール（`chat.diffTool`設定）は未対応。全Diffは組み込みビューアーを使用
- 一部のターミナルエミュレーターでは全機能がサポートされない場合がある（ハイパーリンク、プログレスインジケーター、同期出力）

---

## トラブルシューティング

**出典**: [Terminal UI - Troubleshooting](https://kiro.dev/docs/cli/terminal-ui/#troubleshooting)

### Terminal UIが読み込まれない

設定を確認:

```bash
kiro-cli settings list | grep chat.ui
```

設定が正しいのにTerminal UIが読み込まれない場合は、Kiro CLIを最新バージョンに更新してください。

### レンダリングの問題

視覚的なアーティファクトや壊れたレンダリングが表示される場合:

1. 別のターミナルを試す。iTerm2、WezTerm、kitty、Ghosttyが最良の体験を提供
2. 同期出力を無効化: `KIRO_NO_SYNCHRONIZED=1 kiro-cli chat`
3. ターミナルがtruecolorをサポートしているか確認（ほとんどのモダンターミナルは対応）

---

## v2.22.0〜v2.33.0での進化

### v2.22.0（2026-09-16リリース）: `/fullscreen`

`/fullscreen` で、現在の会話をシェル履歴から独立した専用のターミナル画面（alternate screen）へ移せます。もう一度入力すると inline に戻ります。V2・V3 の両方で、対話の TUI と Lite で使えます。今後のセッションを fullscreen で始めるには `/settings` → **Display** → **Full Screen** → **Start fullscreen** を on にします（v2.25.0 で **Scroll speed** も追加）。詳細は [41. v2.22 新機能](41_v222NewFeatures.md) を参照してください。

### v2.26.0（2026-09-30リリース）: Classic の非推奨通知

Classic インターフェースは非推奨になり、起動時に通知が表示されます。戻し方は [クラシックインターフェースの使用](#クラシックインターフェースの使用) を参照してください。

### v2.28.0（2026-10-05リリース）: Classic からの 3.0 への切り替え提案・Copy on select・アクティビティトレイ

- **Classic の対話セッションから 3.0 への切り替えを提案**: 3.0 を実行できるホストで対話型の Classic セッションを開始すると、Kiro が 3.0 への切り替えを提案します。**Switch to 3.0 and upgrade my agent configs** を選ぶと、3.0 を既定として保存し、エージェント設定をアップグレードし、実行したコマンドを 3.0 で再実行します。断ると約 1 週間に 1 回、再度案内されます（公式 [Changelog v2.28](https://kiro.dev/changelog/cli/2-28/)。詳細は [47. v2.28 新機能](47_v228NewFeatures.md)）。
- **Full Screen の Copy on select**: `/settings` → **Display** → **Full Screen** に追加された項目です。off にすると fullscreen モードがテキスト選択を取り込まず、すでにコピーを処理している端末や tmux がその操作を担えます。公式 [Fullscreen mode](https://kiro.dev/docs/cli/fullscreen/)（公式更新日 2026-09-30）はドラッグでのコピーを説明していますが、この項目の記載はありません。設定キー `chat.fullscreenCopyOnSelect`（boolean、既定 `true`）は**実機 2.33.0 で確認**したものです（→ [設定リファレンス](../04_reference/01_settings.md)）。
- **アクティビティトレイの拡張**: 展開したトレイが 6 件で止まらず、すべてのタスクを一覧します（fullscreen では一覧の高さを画面の約半分までに制限）。Lite のトレイは最大 6 件の Workflow を表示します（公式 Changelog v2.28.0）。トレイの操作（`Ctrl+X`）は上の「[Activity Tray](#activity-tray)」を参照してください。

### v2.30.0（2026-10-12リリース）: モデルフォールバックの通知・スクリーンリーダー

- **モデルフォールバックの通知**: 公式 [Terminal UI の Model fallback notices](https://kiro.dev/docs/cli/terminal-ui/#model-fallback-notices)（公式更新日 2026-10-20）によると、V3 の端末 UI セッションでは、モデルがターンを拒否した場合や利用できなかった場合に別のモデルへ移ったことが transcript に通知されます。通知は、そのターンに応答したモデル、モデルが会話のモデルになったか、または応答したモデルがなかったことを示し、応答したモデルがない場合は `/model` で別のモデルを選びます。V2 の端末 UI ではターン単位のフォールバックが既定で有効で（v2.27.1 で追加。→ [46. v2.27 新機能](46_v227NewFeatures.md)）、`/model fallback` で確認・変更します（V1・V2 に適用）。
- **スクリーンリーダー対応**: 公式 [In-session settings の Screen reader support](https://kiro.dev/docs/cli/chat/settings/#screen-reader-support)（公式更新日 2026-10-20）によると、フル端末 UI で、返信がストリーミングされ、プロンプトが空の間は、非表示の端末カーソルが返信テキストを追います。入力を始める、メニューを開く、承認に応答すると、カーソルは入力に戻ります。設定 `chat.screenReader` は `auto`（既定）・`on`・`off` で、グローバルのみです。`auto` はローカルの Mac で VoiceOver が動作していることを検出した場合に有効になり、SSH などのリモート接続・他のプラットフォーム・検出の失敗や時間切れでは無効のままなので、その場合は `on` を選びます。起動 1 回だけ上書きするには環境変数 `KIRO_SCREEN_READER` に `auto`・`on`・`off` を設定します。有効なとき IME 入力の位置が変わることがあります。

### v2.31.1（2026-10-14リリース）・v2.33.0（2026-10-20リリース）・v2.34.0（2026-10-23リリース）: Mermaid 図の描画

公式 [Terminal UI の Mermaid diagrams](https://kiro.dev/docs/cli/terminal-ui/#mermaid-diagrams)（公式更新日 2026-10-20）は、Kiro CLI 2.31.1 以降が、エージェントの返信に含まれる対応する Mermaid のコードブロックを端末上のアートとして描画すると説明しています。

| Mermaid の見出し | 図 |
|-----------------|----|
| `graph`・`flowchart` | フローチャート |
| `sequenceDiagram` | シーケンス図 |
| `stateDiagram`・`stateDiagram-v2` | 状態遷移図 |
| `erDiagram` | ER 図 |

未完了のブロックがストリーミングされている間は **Drawing diagram** と表示されます。図が広すぎる・大きすぎる・未対応、または未対応の構文を使っている場合は、ソースと理由が表示されます。ASCII アートが off の場合、または `KIRO_ASCII_MODE=1` の場合は、常にソースが表示されます。

**v2.33.0 以降**: 公式 [Terminal UI の Mermaid diagrams](https://kiro.dev/docs/cli/terminal-ui/#mermaid-diagrams)（公式更新日 2026-10-21）によると、フローチャートは `subgraph ... end` のブロックをタイトル付きの枠として描画し、`<br/>` で新しいラベルの行を始め、ノードの枠を最初のスタイルクラス（`A:::focal` または `class A,B focal`）の色で塗ります。色が付くのは、テーマがクラス名（`function`・`class`・`file`・`directory`・`external`・`focal`）を知っているときです。ノードのラベルは最大 4 行に折り返され、それより長いテキストは省略記号で終わります。ネストされたサブグラフは未対応で、Kiro はソースを表示します。`classDef`・`style`・`linkStyle` の文は読み飛ばされ、色は図ではなくテーマから決まります。公式 Changelog v2.33 と公式 Terminal UI は、これらが V2 専用か両対応かを明記していないため**未確認**です（→ [52. v2.33 新機能](52_v233NewFeatures.md)）。

**v2.34.0**: チャット内の Mermaid 図が、生の HTML を表示したり描画に失敗したりせず、より多くの場合に描画されるよう修正されました（公式 [Changelog v2.34](https://kiro.dev/changelog/cli/2-34/)。V2／V3 の適用範囲は**未確認**。→ [53. v2.34 新機能](53_v234NewFeatures.md)）。また、`chat.allowIcons` が off のとき、端末が罫線文字とブロック文字を使わず、矢印キーを単語として読み上げるよう修正されました（公式 Changelog v2.34。V2／V3 の適用範囲は**未確認**）。

### v2.32.0（2026-10-15リリース）: 端末へのプログラム状態の報告（OSC 7501）

公式 [Terminal UI の Program status for supporting terminals](https://kiro.dev/docs/cli/terminal-ui/#program-status-for-supporting-terminals)（公式更新日 2026-10-20）は、Kiro CLI の V2 と V3 が、対話型の端末で OSC 7501 を通じて状態を報告すると説明しています。対応する端末は、Kiro がアイドル・作業中・完了・承認または回答の待機中・エラーで停止、のどれであるかを表示できます。起動前に `KIRO_NO_PROGRAM_STATUS=1` を設定すると、この更新を無効にできます。

```bash
KIRO_NO_PROGRAM_STATUS=1 kiro-cli chat
```

公式 Changelog v2.32.0 はこの項目に V2・V3 の区別を書いていません。V2・V3 の両対応という記述は公式 Terminal UI によるものです。詳細は [51. v2.32 新機能](51_v232NewFeatures.md) を参照してください。

---

## 関連リンク

- [Terminal UI 公式ドキュメント](https://kiro.dev/docs/cli/terminal-ui/)
- [Terminal UI vs Classic 比較](https://kiro.dev/docs/cli/terminal-ui/comparison/)
- [公式Changelog v1.28.0](https://kiro.dev/changelog/cli/1-28/)
- [公式Changelog v2.0.0](https://kiro.dev/changelog/cli/2-0/)
- [スラッシュコマンドリファレンス](https://kiro.dev/docs/reference/slash-commands/)
- [設定リファレンス](https://kiro.dev/docs/reference/settings/)
- [v2.0.0メジャーアップデート解説](16_v2MajorUpdate.md)
- [Granular Tool Trust機能](17_GranularToolTrust.md)
- [サブエージェント機能](02_Subagents.md)
- [Kiro CLI の新しいチャット体験！TUI v2 を試してみよう](https://zenn.dev/aws_japan/articles/ad5eee399b08a5) - Zenn記事 by konippi（TUI v2のスクリーンショット付き解説）

### 本サイトの関連文書
- [25. Auto Complete](25_AutoComplete.md) 🆕 — Terminal UI と統合された AI 補完機能
- [21. v2.4 New Commands](21_v24NewCommands.md) — `/theme`、`/settings` の TUI 統合メニュー
- [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md) — TUI で使える全スラッシュコマンド42種の正規仕様
- [04_reference/01_settings.md](../04_reference/01_settings.md) — TUI 用 keybindings、`chat.ui` 設定

---

**最終更新**: 2026-10-25
**対象バージョン**: Kiro CLI v1.28.0+（v2.0.0 でデフォルト UI 化、v2.18.0 Spec review screen導入、v2.19.0 マウス対応、v2.20.0 Preserve scrollbackトグル追加、v2.22.0 `/fullscreen`、v2.26.0 Classic 非推奨、v2.28.0 Classic からの 3.0 切替提案、v2.30.0 スクリーンリーダー、v2.31.1 Mermaid 図、v2.32.0 OSC 7501、v2.33.0 Mermaid のサブグラフ、v2.34.0 Mermaid の描画の修正）
