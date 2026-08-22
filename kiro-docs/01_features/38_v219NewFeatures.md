[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.19 新機能

---

# v2.19 新機能（サブエージェントタイムアウト・Spec Reviewマウス対応）

## 概要

Kiro CLI **v2.19.0**（2026-08-19）で追加された機能を解説します。**停止したサブエージェントが親ターンをハングさせなくなる**アイドルタイムアウト（`api.subagentTimeout`）、**Spec review screen へのマウス対応**、そして [V3] のセッション再開ピッカーとMCP接続の改善が中心です。

**対応バージョン**: Kiro CLI v2.19.0+

> **注記**: 本ページは v2.19.0 を対象としています。後続の v2.19.1（2026-08-21）はバグ修正・セキュリティ修正のみで新機能はありません（→ [02_update/01_changelog.md](../02_update/01_changelog.md)）。最新版は[公式 Changelog](https://kiro.dev/changelog/cli/) を参照してください。

---

## サブエージェントのアイドルタイムアウト（`api.subagentTimeout`）

サブエージェントは並列実行される子タスクですが、内部で無応答になった場合、従来は親ターン全体が応答を待ち続けてしまう問題がありました。v2.19.0では、各サブエージェントに**アイドル期限**が設定され、この期限を超えて無応答が続くと、サブエージェントが自動的にタイムアウトし、親ターンの実行は継続されます。

```bash
# サブエージェントのアイドルタイムアウトを1800秒（30分）に短縮
kiro-cli settings api.subagentTimeout 1800
```

- **設定キー**: `api.subagentTimeout`（number、既定 `3600` 秒）
- 詳細: [02. Subagents](02_Subagents.md)、[04_reference/01_settings.md](../04_reference/01_settings.md)

---

## Spec review screen のマウス対応

[V3] のspec review screen（v2.18.0で導入。`Ctrl+X`でフェーズ文書に行コメントをステージングする機能）に、v2.19.0でマウス対応が追加されました。

- **スクロール**でのナビゲーション
- **クリック**でのカーソル位置指定
- `m` キーでマウスモードをトグル

詳細: [18. Terminal UI](18_TerminalUI.md)

---

## [V3] session resume ピッカーのAI生成タイトル要約

session resume ピッカーに、最初のプロンプトを要約した短いAI生成タイトルが表示されるようになりました。似た内容のセッションが並んでいても識別しやすくなります。

詳細: [09_v3/README.md](../09_v3/README.md)

---

## [V3] MCP protocol revision 2026-07-28 対応

protocol revision 2026-07-28 を要求するMCPサーバーへの接続に対応しました。

詳細: [09_v3/README.md](../09_v3/README.md)

---

## その他の変更（Changed）

- エージェント実行中に入力したスラッシュコマンドが自動実行されるように変更: 読み取り専用コマンドは即時、それ以外はターン終了時に実行。
- 利用不可なツールへの呼び出しが、ターン終了まで持ち越されず即時に失敗するよう変更。

## バグ修正（25件）

ストリームアイドル監視（`api.streamIdleSoftTimeout`/`api.streamIdleHardTimeout`）、自動リトライ、コンテキストオーバーフロー自動圧縮など。全項目は [02_update/01_changelog.md](../02_update/01_changelog.md) を参照してください。

---

## 出典

### 公式情報源
- [公式 Changelog v2.19](https://kiro.dev/changelog/cli/2-19/)
- [Settings リファレンス](https://kiro.dev/docs/reference/settings/)（Page updated 2026-08-20）
- [Terminal UI 公式ドキュメント](https://kiro.dev/docs/cli/terminal-ui/)
- CLI 内蔵: `kiro-cli version --changelog=2.19.0`

### 本サイトの関連文書
- [02. Subagents](02_Subagents.md) — `api.subagentTimeout` の詳細解説
- [18. Terminal UI](18_TerminalUI.md) — Spec review screen の詳細解説
- [09_v3/README.md](../09_v3/README.md) — [V3] session resumeタイトル要約・MCP protocol revision対応
- [04_reference/01_settings.md](../04_reference/01_settings.md) — `api.subagentTimeout`・`api.streamIdleSoftTimeout`・`api.streamIdleHardTimeout` の設定キー
- [02_update/01_changelog.md](../02_update/01_changelog.md) — v2.19.0・v2.19.1 の全変更内容

---

**最終更新**: 2026-08-22
**対象バージョン**: Kiro CLI v2.19.0+
