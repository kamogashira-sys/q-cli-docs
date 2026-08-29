[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.20 新機能

# 39. v2.20 新機能 — 全画面 Spec 実行・Preserve scrollback・Powers

## 概要

Kiro CLI **v2.20.0**（2026-08-26）と **v2.20.1**（2026-08-27）で追加・改善された機能を解説します。v2.20.0 では、V3 の `/spec run` に全画面タスク実行ビューが追加され、`/settings display` に Preserve scrollback トグルが加わりました。v2.20.1 では、V3 でインストール済み Powers を確認する `/powers` が追加されました。

> ⚠️ **V3 限定**: `/spec run` の全画面実行と `/powers` は `kiro-cli --v3` の Early Access 機能です。安定版（V2）のスラッシュコマンド数には含めません。

## [V3] 全画面 Spec タスク実行

V3 セッションで `/spec run <name>` を実行すると、専用の**全画面タスク実行ビュー**が開きます。実行中はタスクの進捗をリアルタイムで確認でき、開始前に実行するタスクのスコープを選択できます。

```bash
# V3 エンジンで起動
kiro-cli --v3

# 指定した spec のタスクを実行
/spec run add-user-auth
```

公式一次情報で確認できる範囲は、全画面ビュー、リアルタイム進捗追跡、実行前のタスクスコープ選択です。画面内の個別操作やタスク粒度は公式に記載されていないため、本ページでは断定しません。

詳細な Spec のワークフロー、タスク依存関係、並列 wave 実行は [09-01. 仕様駆動開発](../09_v3/01_spec-driven-development.md) を参照してください。IDE との比較は [09-02. Kiro IDE 版との比較](../09_v3/02_kiro-ide-vs-cli.md) にまとめています。

## Preserve scrollback

v2.20.0 で、`/settings display` に **Preserve scrollback** トグルが追加されました。現行 CLI では設定キー `chat.preserveScrollback`（boolean、既定 `false`）としても確認できます。

有効にすると、overflow や端末リサイズ時の全画面再描画でターミナルの scrollback を消去せず、viewport のみを再描画します。

```bash
# Preserve scrollback を有効化
kiro-cli settings chat.preserveScrollback true
```

> **表示上の制約**: 左側ステータスバーが再描画境界をまたぐ場合、継ぎ目に隙間（seam gap）が表示されることがあります。
>
> **初出バージョンの扱い**: v2.20.0 で確認できるのは `/settings display` のトグル追加です。設定キー `chat.preserveScrollback` 自体の初出バージョンは、今回確認した一次情報から断定していません。

設定の一覧と関連する表示オプションは [Settings リファレンス](../04_reference/01_settings.md) を参照してください。

## [V3] `/powers` — インストール済み Powers の確認

v2.20.1 で、V3 セッションからインストール済み Powers を表示する `/powers` が追加されました。

```text
/powers
```

Powers は、MCP tools・Skills・ナレッジ・ワークフローを Agent Plugins 形式でまとめ、会話中のキーワードに応じて必要なコンテキストとツールをオンデマンドで活性化する仕組みです。Powers の Agent Plugin 形式読込は v2.16.2 で V3 セッションに対応済みであり、v2.20.1 はインストール済み Powers を確認する操作面を追加したものです。

Powers のインストール・作成手順は、今回の changelog の範囲外です。公式 [Powers](https://kiro.dev/docs/powers/) と関連する公式ページを参照してください。

## 後続修正の案内

v2.20.x には会話再開、大容量出力、認証、MCP、Windows 自動更新、`chat.historyMode` などの修正も含まれます。修正項目の完全な一覧は [変更履歴の v2.20.1 / v2.20.0](../02_update/01_changelog.md) を正とします。

## 関連リンク

### 本サイト

- [09-01. 仕様駆動開発](../09_v3/01_spec-driven-development.md)
- [09-02. Kiro IDE 版との比較](../09_v3/02_kiro-ide-vs-cli.md)
- [Terminal UI](18_TerminalUI.md)
- [Settings リファレンス](../04_reference/01_settings.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.20](https://kiro.dev/changelog/cli/2-20/)
- [Specs](https://kiro.dev/docs/specs/)
- [Powers](https://kiro.dev/docs/powers/)
- [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)
- [Settings](https://kiro.dev/docs/reference/settings/)
- `kiro-cli version --changelog=2.20.0` / `kiro-cli version --changelog=2.20.1`
- `kiro-cli settings list --all`

**最終更新**: 2026-08-29
**対象バージョン**: Kiro CLI v2.20.0+（`/spec run` 全画面実行と `/powers` は V3 Early Access）
