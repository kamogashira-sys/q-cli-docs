[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.22 新機能

# 41. v2.22 新機能 — fullscreen チャット・セッションダッシュボードの再設計

## 概要

Kiro CLI **v2.22.0**（2026-09-16）と **v2.22.1**（2026-09-17）では、会話を専用のターミナル画面で扱う `/fullscreen` が追加され、V3 のセッションダッシュボードが再設計されました。

- **v2.22.0**: `/fullscreen`（V2・V3 の両方）、[V3] `/sessions` の再設計、大きなツール結果の保存（V3）、`KIRO_SKIP_BINARY_PINNING`
- **v2.22.1**: モデル切替時の transcript 通知、V3 のクラウドセッション・compaction・MCP 接続の修正、Windows の終了処理の修正

> **V2 と V3 の区別**: `/fullscreen` は V2・V3 の両方で使える安定版のコマンドで、[スラッシュコマンドリファレンス](../04_reference/02_slash-commands.md)に掲載しています。`/sessions` は V3（`kiro-cli --v3`、Early Access）限定です。

## `/fullscreen` — 専用画面でのチャット

`/fullscreen` を入力すると、現在の会話が専用のターミナル画面（ターミナルの alternate screen）へ移ります。もう一度 `/fullscreen` を入力すると inline 表示に戻ります。

```text
/fullscreen
```

| 現在のモード | コマンド | 結果 |
|-------------|---------|------|
| Inline | `/fullscreen` | fullscreen に入る |
| Fullscreen | `/fullscreen` | inline に戻る |

公式 [Fullscreen mode](https://kiro.dev/docs/cli/fullscreen/) によると、次の性質があります。

- 会話がシェル履歴から独立してスクロールする。inline に戻ると、fullscreen 中のメッセージは inline の transcript に追加される
- モードを切り替えても会話はリセットされず、新しいセッションも始まらない
- モード切替のキーボードショートカットは無い（`/fullscreen` のみ）
- `/fullscreen` は対話の TUI と Lite で使える。非対話セッションでは使えない

### 操作

| 操作 | 動作 |
|------|------|
| マウスホイール・タッチパッド | スクロール |
| `PageUp` / `PageDown` | 1 ページ上下 |
| `Home` | プロンプトが空のとき最古の内容へ |
| `End` | スクロール中に最新の内容へ戻る |
| `Ctrl+O` | 直近 20 件のツール出力を展開・折りたたみ |
| クリック＆ドラッグ | 選択したテキストをクリップボードへコピー |

コピーは `pbcopy`（macOS）・`Set-Clipboard`（Windows）・`wl-copy` / `xclip` / `xsel`（Linux）を使い、いずれも使えない場合（SSH 先のリモートホストなど）は OSC 52 のエスケープシーケンスで行います。tmux は既定で OSC 52 を通さないため、公式は `~/.tmux.conf` に `set -g set-clipboard on` を追加する方法を案内しています。

> v2.27.0 で、ドラッグコピーが画面上の折り返し行ではなく元のメッセージテキストをコピーするよう修正されました（→ [46. v2.27 新機能](46_v227NewFeatures.md)）。

### fullscreen で起動する

`/fullscreen` は現在のセッションだけを切り替えます。今後の対話 TUI セッションを fullscreen で開始するには、`/settings` → **Display** → **Full Screen** → **Start fullscreen** を on にします（次回の起動から有効）。

```bash
# 実機 2.27.1 の設定キー（公式 Settings リファレンスには未掲載）
kiro-cli settings chat.startFullscreen true
```

> **画面構成の変化**: v2.22.0 の公式 changelog は「`/settings` → **Display** → **Start fullscreen**」と案内していました。v2.25.0 で **Full Screen** 画面が新設され、**Start fullscreen** はその中に移りました（→ [44. v2.25 新機能](44_v225NewFeatures.md)）。

## [V3] セッションダッシュボードの再設計

`/sessions` が再設計され、検索・フィルタ・ソート・グルーピングの操作がセッション一覧から分離されました。

- 最終使用順のフラットな一覧で開く
- 最終使用・セッション名・メッセージ数でソートでき、選んだソートを記憶する（実機 2.27.1 の設定キーは `chat.sessionDashboard.sortBy`。公式 Settings リファレンス未掲載）
- `Tab` で操作部と結果の間を移動する

その後の版で次の変更が続きました。

| 版 | 変更 | 解説 |
|----|------|------|
| v2.23.1 | メインセッションへの絞り込み（Tangent・rewind・サブエージェントの子セッションを隠す） | [変更履歴](../02_update/01_changelog.md) |
| v2.24.0 | Filter・Sort・Group の選択肢をその場に表示、フィルタの組み合わせ、`includes empty` | [43. v2.24 新機能](43_v224NewFeatures.md) |
| v2.24.1 | 既定の表示範囲が現在のディレクトリに | [43. v2.24 新機能](43_v224NewFeatures.md) |

## 長時間の作業の安定性

| 改善 | 内容 |
|------|------|
| compaction 中の継続性 | 自動 compaction の実行中も応答と Thinking 表示が見えたままで、キューに入れたプロンプトは compaction 後に続行する |
| 大きなツール結果（V3） | 大きな結果をセッションとともに保存し、モデルには短いプレビューを渡す。完全な出力を失わずにコンテキスト使用量を減らす |
| 長時間のセッション | サブエージェントの動作が多いときの TUI のメモリ使用量を削減 |

### `KIRO_SKIP_BINARY_PINNING`

インストールしたバイナリが固定のパスに残るストレージ制約のある環境向けの環境変数です。

```bash
export KIRO_SKIP_BINARY_PINNING=1
```

> ⚠️ 公式は「セッション中にインストーラーがバイナリを置き換えたり削除したりする可能性がある場合は使わないこと」と注意しています。

## `--require-mcp-startup` の V3 非対話実行（v2.22.0 の修正）

`--require-mcp-startup` が、非対話の V3 実行の開始前に設定済みの MCP サーバーの起動を待ち、起動に失敗した場合は終了コード 3 で終了するようになりました。詳細は [15. Exit Codes](15_ExitCodes.md) を参照してください。

## v2.22.1 の要点

- ターンが別のモデルへ移ったとき、モデル名と理由を transcript に通知する
- V3 の容量エラーが影響を受けたモデルを示し、V3 の shell ツールカードがコマンドを平易な言葉で説明する
- V3 のクラウドセッションがターン途中の接続リセットから回復する
- `offline_access` を拒否する認可サーバーでも V3 の MCP 接続が動作する
- Windows で `Ctrl+Break` やコンソールウィンドウを閉じる操作で正常に終了する

修正項目の完全な一覧は [変更履歴の v2.22.1・v2.22.0](../02_update/01_changelog.md) を正とします。

## 関連リンク

### 本サイト

- [40. v2.21 新機能](40_v221NewFeatures.md)
- [42. v2.23 新機能](42_v223NewFeatures.md)
- [Terminal UI](18_TerminalUI.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [スラッシュコマンドリファレンス](../04_reference/02_slash-commands.md)
- [Settings リファレンス](../04_reference/01_settings.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.22](https://kiro.dev/changelog/cli/2-22/)
- [Fullscreen mode](https://kiro.dev/docs/cli/fullscreen/)
- [Session management](https://kiro.dev/docs/cli/chat/session-management/)
- [Slash commands](https://kiro.dev/docs/reference/slash-commands/)

**最終更新**: 2026-10-04
**対象バージョン**: Kiro CLI v2.22.0+（`/sessions` は V3 Early Access）
