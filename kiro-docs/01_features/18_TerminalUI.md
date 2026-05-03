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
- [プラットフォームサポート](#プラットフォームサポート)
- [制限事項](#制限事項)
- [トラブルシューティング](#トラブルシューティング)
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
| `/guide` | Kiroガイドエージェントに切り替え（ヘルプとオンボーディング） |
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

### クラシックインターフェースの使用

```bash
# 永続的に切り替え
kiro-cli settings chat.ui "classic"

# 単一セッションのみ
kiro-cli --classic
```

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

## 関連リンク

- [Terminal UI 公式ドキュメント](https://kiro.dev/docs/cli/terminal-ui/)
- [Terminal UI vs Classic 比較](https://kiro.dev/docs/cli/terminal-ui/comparison/)
- [公式Changelog v1.28.0](https://kiro.dev/changelog/cli/1-28/)
- [公式Changelog v2.0.0](https://kiro.dev/changelog/cli/2-0/)
- [スラッシュコマンドリファレンス](https://kiro.dev/docs/cli/reference/slash-commands/)
- [設定リファレンス](https://kiro.dev/docs/cli/reference/settings/)
- [v2.0.0メジャーアップデート解説](16_v2MajorUpdate.md)
- [Granular Tool Trust機能](17_GranularToolTrust.md)
- [サブエージェント機能](02_Subagents.md)

---

**最終更新**: 2026年05月03日
