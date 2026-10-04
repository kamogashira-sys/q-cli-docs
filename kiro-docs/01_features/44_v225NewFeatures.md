[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.25 新機能

# 44. v2.25 新機能 — Powers の管理・V3 Output style・fullscreen のスクロール速度・`SessionEnd` Hook

## 概要

Kiro CLI **v2.25.0**（2026-09-28）では、Powers をチャットやコマンドラインからインストール・アンインストールできるようになり、V3 の応答の書式（Output style）、fullscreen のスクロール速度、V3 のセッション終了時の Hook が追加されました。v2.25 系にパッチ版はありません。

| 機能 | 対象 |
|------|------|
| Powers のインストールとアンインストール | `/powers install`・`/powers uninstall` は V3 のローカルセッション、`kiro-cli powers` はチャット外 |
| Output style | V3 |
| fullscreen のスクロール速度 | TUI の fullscreen |
| `SessionEnd` Hook | V3 |

## Powers のインストールとアンインストール

### チャット内（V3 のローカルセッション）

```text
/powers install <name|path>
/powers uninstall <name>
```

公式 [Install powers](https://kiro.dev/docs/powers/installation/) によると、次のように動作します。

- 引数が既存のディレクトリならそのディレクトリからインストールし、そうでなければ Powers カタログで完全一致する名前を探す
- ローカルの Power のディレクトリには `plugin.json`（Agent Plugins 形式）または `POWER.md`（旧形式）が必要
- 対話の `/powers` コマンドが成功すると、現在のセッションがすぐ更新される

### チャット外（`kiro-cli powers`）

```bash
kiro-cli powers install <name|path>
kiro-cli powers uninstall <name>
```

チャットを起動せずにローカルのレジストリを更新して終了し、次のセッションから更新後の Powers が読み込まれます。実機 2.27.1 の `kiro-cli powers --help` は、サブコマンドとして `install`（名前またはローカルパスで Power をインストール）と `uninstall`（名前で Power をアンインストール）を表示します。

> ⚠️ **クラウドセッションでは使えません**: これらのコマンドはローカルマシンを変更するため、クラウドセッションではインストール・アンインストールに対応していません（公式 Install powers）。
>
> ⚠️ 公式は、Powers はサードパーティのツールで別の利用規約の対象になる場合があり、信頼できる提供元からのみインストールするよう警告しています。

インストールした Power は、IDE と同じくプロンプト内のキーワードに応じて自動的に有効になります。Powers の表示（`/powers`）は v2.20.1、`/` コマンドピッカーへの表示は v2.21.3 で追加されています（→ [40. v2.21 新機能](40_v221NewFeatures.md)）。

## [V3] Output style

V3 セッションで Kiro の応答の書式を選べるようになりました。選択肢には、アップグレード済みのエージェントが提供する Output style も含まれます。

公式 [In-session settings](https://kiro.dev/docs/cli/chat/settings/) の説明は次のとおりです。

- 選択肢は、Display メニューを開いた時点の有効なエージェントから取得される。アップグレード済みのエージェントは CLI の更新なしで新しい選択肢を提供できる
- 選択はグローバルの `chat.outputStyle` として保存され、以降のプロンプトに適用される
- エージェントの既定を選ぶとグローバルの上書きが削除される
- ワークスペースの `chat.outputStyle` は引き続き優先される

> **場所の変更**: v2.25.0 では `/settings` のトップレベルにありましたが、**v2.27.0 で `/settings display` 配下へ移動**しました（→ [46. v2.27 新機能](46_v227NewFeatures.md)）。現在の公式 In-session settings は `/settings display` の **Output style** 行として説明しています。

## fullscreen のスクロール速度

`/settings display` → **Full Screen** → **Scroll speed** で、マウスホイール 1 回あたりの transcript の移動量を **1・2・3 行**から選べます。既定は **2 行**で、変更はすぐ反映されます。

```bash
# 実機 2.27.1 の設定キー（公式 Settings リファレンスには未掲載）
kiro-cli settings chat.fullscreenWheelRows 3
```

新しい **Full Screen** 画面には、既存の **Start fullscreen** も含まれます（→ [41. v2.22 新機能](41_v222NewFeatures.md)）。

> v2.24.0 では「ホイール 1 ノッチで 1 行」に変更されていました。v2.25.0 でこの設定が加わり、既定は 2 行になりました。

## [V3] `SessionEnd` Hook

新しいトリガー `SessionEnd` で、V3 セッションの終了時に Hook を実行できます。公式 changelog は、セッション単位の自動化に後片付けなどのための確実な終了イベントを提供するものと説明しています。

公式 [Hook types](https://kiro.dev/docs/hooks/types/) の記載は「The `SessionEnd` trigger fires when a CLI V3 session is torn down.」の 1 文のみで、Hook に渡される入力や終了コードの扱いは記載されていません。本ページでもそれ以上は扱いません。

V3 の Hooks 全体（`.kiro/hooks/<name>.json`、トリガー一覧）は [09_v3/](../09_v3/README.md) を参照してください。[22. Hooks](22_Hooks.md) は CLI 2.x 仕様の解説で、`SessionEnd` は含みません。

## その他の改善と修正

| 種類 | 内容 |
|------|------|
| 改善 | V2 のモデル容量の通知がモデル名・試行回数・待ち時間を表示、モデル拒否の通知がモデル名を表示、transcript でエージェント・ツール・推論の動作を見分けやすく、V3 の `/sessions` の高速化 |
| セキュリティ関連の修正 | V3 がファイルの読み取りと検索でワークスペースの `.kiroignore` に従う、V3 の `web_fetch` が別のオリジンや HTTP へのリダイレクトをブロック |
| その他の修正 | モデル一覧を取得できなくてもセッションを開始できる、V3 が V2・classic のセッションの履歴を再生する、Markdown の表の列崩れ、V3 の MCP OAuth の `redirectUri` 形式 |

修正項目の完全な一覧は [変更履歴の v2.25.0](../02_update/01_changelog.md) を正とします。

## 関連リンク

### 本サイト

- [43. v2.24 新機能](43_v224NewFeatures.md)
- [45. v2.26 新機能](45_v226NewFeatures.md)
- [41. v2.22 新機能](41_v222NewFeatures.md)（`/fullscreen`）
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [CLI コマンドリファレンス](../04_reference/03_cli-commands.md)
- [Settings リファレンス](../04_reference/01_settings.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.25](https://kiro.dev/changelog/cli/2-25/)
- [Install powers](https://kiro.dev/docs/powers/installation/)
- [In-session settings](https://kiro.dev/docs/cli/chat/settings/)
- [Fullscreen mode](https://kiro.dev/docs/cli/fullscreen/)
- [Hook types](https://kiro.dev/docs/hooks/types/)

**最終更新**: 2026-10-04
**対象バージョン**: Kiro CLI v2.25.0+（`/powers install|uninstall`・Output style・`SessionEnd` は V3 Early Access）
