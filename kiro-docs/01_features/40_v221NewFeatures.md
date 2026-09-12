[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.21 新機能

# 40. v2.21 新機能 — セッションダッシュボード・設定パネル・クラウド設定・`--v2`

## 概要

Kiro CLI **v2.21.0**（2026-09-01）から **v2.21.4**（2026-09-11）までの 11 日間に、V3 のセッション管理と設定確認を中心に機能が追加されました。

- **v2.21.0**: [V3] セッションダッシュボード（`/sessions`）、[V3] 設定パネル（`/config`）、[V3] ローカルセッションへのクラウド設定適用
- **v2.21.1**: スピナー文言のカスタマイズ（`chat.enableCustomSpinnerVerbs` / `chat.spinnerVerbs`）、ワークスペース `cli.json` の優先順位是正
- **v2.21.2**: [V3] 端末履歴の保持が既定に（`chat.preserveScrollback` の既定値変更）
- **v2.21.3**: [V3] インストール済み Powers を `/` コマンドピッカーに表示
- **v2.21.4**: [V3] セッション検索の範囲選択、`--v2` フラグ、設定メニューのキーボード操作統一

> ⚠️ **V3 限定機能について**: `/sessions`・`/config`・クラウド設定適用・Powers のピッカー表示・セッション検索は `kiro-cli --v3`（Early Access、内部識別子 KAS）の機能です。安定版（V2）のスラッシュコマンド数には含めません。V2 で `/sessions` を開こうとすると「Session dashboard is available on the V3 (KAS) engine only」の警告が表示されます。

## [V3] セッションダッシュボード — `/sessions`

V3 セッションで `/sessions` を開く、または起動時に `--sessions` を渡すと、ローカルまたはクラウドに保存された過去セッションを閲覧・検索・再開・整理できるダッシュボードが開きます。

```bash
# V3 エンジンで起動してからダッシュボードを開く
kiro-cli --v3
/sessions

# ダッシュボードへ直接起動する（閉じるとチャットに落ちずに終了する）
kiro-cli chat --sessions
```

`--sessions` のヘルプ本文は「Launch straight into the session dashboard (V3/KAS only); closing it exits rather than dropping into a chat」です。つまりダッシュボードを閉じた時点で、チャットに移行せずコマンドが終了します。

関連する設定キーとして、実機ではセッションのグループ化（`chat.sessionDashboard.groupBy`）と、ダッシュボードのトグルキー（`chat.keybindings.toggleSessionDashboard`）を確認できます。各値の詳細は [Settings リファレンス](../04_reference/01_settings.md) を参照してください。

### セッション検索の範囲選択（v2.21.4）

v2.21.4 で、`/sessions` の検索がセッションタイトル・自分のプロンプト・**エージェントの応答**をインデックスするようになりました。これにより「Kiro が何と答えたか」からセッションを探せます。

範囲は `/settings` の **Session search** で切り替えます。

| 選択肢 | インデックス対象 |
|--------|----------------|
| **Prompts only** | セッションタイトル、自分のプロンプト |
| **Prompts and agent responses** | 上記 ＋ エージェントの応答 |

**ツール出力はどちらのモードでもインデックスされません。** ローカルインデックスが現在 prompts only の場合、`/sessions` が再構築の可否を一度だけ確認します。

実機 2.21.4 で対応する設定キーは `chat.sessionDashboard.indexResponses` です。応答のインデックスはローカルで行われ、対象が増えるぶん処理時間とディスク使用量が増える可能性があります。

## [V3] 設定パネル — `/config`

ローカルまたはクラウドの V3 セッションで `/config` を実行すると、設定済みのリソースを 1 画面で確認できます。

対象は agents・MCP servers・Powers・Steering・Skills・Hooks です。ソース情報が利用可能な場合、各項目を **local**・**cloud**・**both** として識別表示します。

```bash
kiro-cli --v3
/config
```

クラウド設定を併用している環境では、どのリソースがローカルのファイル由来でどれが Kiro Web 由来かを、この識別表示で切り分けられます。

## [V3] ローカルセッションへのクラウド設定適用

Kiro Web の **Configuration Sync** で個人の `.kiro` 設定をアップロードしておくと、クラウドセッションはその設定を自動的に使用します。

さらに **Apply your cloud configuration to local sessions** を有効化すると、**新規のローカル CLI セッション**でもクラウド側の Steering・カスタムエージェント・Skills・Powers・Hooks が読み込まれます。

> **重要**: この読み込みは、ローカルの `.kiro` ディレクトリにファイルを書き込みません。クラウドの内容はクラウドに留まり、ローカルのファイルを置き換えることもありません。

有効化は Kiro Web 側の Configuration Sync ページで行います。手順は公式 [Cloud configuration](https://kiro.dev/docs/web/cloud-configuration/) を参照してください。

## `--v2` — 単一実行でのエージェントハーネス選択

v2.21.4 で、1 回の実行を V2 エージェントハーネスで走らせる `--v2` フラグが追加されました。`kiro-cli` と `kiro-cli chat` の両方で使えます。

```bash
# この 1 回だけ V2 ハーネスで実行する
kiro-cli --v2
kiro-cli chat --v2 "この作業を V2 で試す"
```

保存済みの既定設定を**上書きしません**。そのため、普段の既定を V3 にしていても、一時的に V2 の挙動を確認したいときに使えます。

### エンジン選択の経路（実機 2.21.4）

| 経路 | 内容 |
|------|------|
| `--v2` | この実行を V2 ハーネスで走らせる（v2.21.4 で追加） |
| `--v3` | 次世代 Kiro エージェント（Early Access）で起動 |
| `--agent-engine <ENGINE>` | `v1` / `v2`（既定）/ `v3` を明示指定 |
| `KIRO_AGENT_ENGINE` | 環境変数によるエンジン指定 |

> **公式記述との差異**: 公式 v2.21.4 の説明は「保存された `chat.agentEngine` 値より優先されるが上書きしない」と述べていますが、**実機 2.21.4 には `chat.agentEngine` という設定キーが存在しません**（`chat.` で始まる設定キーを全列挙して該当なし）。本ページでは公式記述をそのまま設定キーとして扱わず、上表の実機経路を正とします。

## スピナー文言のカスタマイズ（v2.21.1）

待機中に表示されるビジーインジケーター（スピナー）の動詞を、自分の文言に差し替えられるようになりました。

```bash
# カスタム文言を有効化
kiro-cli settings chat.enableCustomSpinnerVerbs true
```

文言そのものは `chat.spinnerVerbs` で指定します。値の書式は公式リファレンスに明記されていないため、本ページでは断定しません。設定キーの一覧は [Settings リファレンス](../04_reference/01_settings.md) を参照してください。

## 端末履歴の保持が既定に（v2.21.2）

v2.21.2 で、**V3 が再描画をまたいで端末履歴を既定で保持する**ようになりました。従来の clear-and-repaint 動作に戻すには、`chat.preserveScrollback` を `false` に設定します。

```bash
# 従来の clear-and-repaint 動作に戻す
kiro-cli settings chat.preserveScrollback false
```

このトグルは v2.20.0 で `/settings display` に追加されたもので、当時の既定は `false` でした。実機 2.21.4 では既定が `true` であることを確認しています。経緯は [39. v2.20 新機能](39_v220NewFeatures.md) と [Settings リファレンス](../04_reference/01_settings.md) にまとめています。

## 設定メニューのキーボード操作統一（v2.21.4）

すべての設定メニューが同一のキー割り当てに従うようになりました。対象は `/settings`・Display・Status line・Theme・`/verbosity` です。

| キー | 動作 |
|------|------|
| `Up` / `Down` | 行の移動 |
| `Right` または `Enter` | 値の変更、オプションの選択、サブメニューの展開 |
| `Left` | 値を逆方向へ変更 |
| `Esc` | 前の画面へ戻る |

あわせて表示面も変わりました。左側のステータスレールは撤去され、**エージェント色の小さなドット**が各エージェント応答を示す方式になりました。`/verbosity` 内のプレビュー切替は `Ctrl+X` に移り、hidden / mini / expanded を循環します（`Ctrl+P` も当面は機能します）。

## 後続修正の案内

v2.21.x には、V3 のセッション一覧・モデル選択・MCP ツール一覧・コードナビゲーション、`/usage` の非対話出力、tangent セッション再開時のチップ表示などの修正も含まれます。修正項目の完全な一覧は [変更履歴の v2.21.4 〜 v2.21.0](../02_update/01_changelog.md) を正とします。

## 関連リンク

### 本サイト

- [39. v2.20 新機能](39_v220NewFeatures.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [Cloud Sessions（クラウドセッション）](36_CloudSessions.md)
- [Terminal UI](18_TerminalUI.md)
- [Settings リファレンス](../04_reference/01_settings.md)
- [CLI コマンドリファレンス](../04_reference/03_cli-commands.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.21](https://kiro.dev/changelog/cli/2-21/)
- [Kiro CLI Changelog v2.21.4](https://kiro.dev/changelog/cli/2-21-4/)
- [Session management](https://kiro.dev/docs/cli/chat/session-management/)
- [Configuration](https://kiro.dev/docs/configuration/)
- [Cloud configuration](https://kiro.dev/docs/web/cloud-configuration/)
- [CLI commands](https://kiro.dev/docs/reference/cli-commands/)
- [Settings](https://kiro.dev/docs/reference/settings/)
- `kiro-cli version --changelog=2.21.4` / `kiro-cli version --changelog=2.21.3`
- `kiro-cli chat --help`

**最終更新**: 2026-09-13
**対象バージョン**: Kiro CLI v2.21.0+（`/sessions`・`/config`・クラウド設定適用・セッション検索は V3 Early Access）
