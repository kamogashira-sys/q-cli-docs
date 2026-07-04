[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.8 / V3 プレビュー

---

# v2.8 / V3 プレビュー（CLI v3 Early Access・MCP OAuth / spec 表示の改善）

## 概要

Kiro CLI **v2.8.0**（公式表示日 2026-06-17）で、**Kiro CLI V3 が Early Access（先行公開）**として登場しました。`kiro-cli --v3` でオプトイン的に試せ、既存の 2.x と併存します。続く **v2.8.1**（2026-06-17）は、MCP OAuth と spec ワークフロー表示まわりの改善・修正を含むパッチです。

V3 は単一機能ではなく、**統一エンジン＋仕様駆動開発（Spec-driven development）**を中心とした更新のため、詳細は専用セクション **[09_v3/](../09_v3/README.md)** に分けて解説しています。本ページは **v2.8.x の事実と入口**に絞ります。

**対応バージョン**: Kiro CLI v2.8.0 / v2.8.1（V3 は Early Access）

> **注記**: V3 は **Early Access** であり、仕様変更の可能性があります。最新は[公式 Changelog](https://kiro.dev/changelog/cli/) および [公式 CLI v3 ドキュメント](https://kiro.dev/docs/cli/v3/) を参照してください。

---

## v2.8.0 — Kiro CLI V3 Early Access

v2.8.0 の changelog 本体は **「Kiro CLI V3 の early release」** の 1 項目です。

```bash
# V3 エンジンを試す（既存 2.x はそのまま）
kiro-cli --v3
```

- **オプトイン**: `kiro-cli --v3` で V3 エンジンを起動。**設定は変更不要**で、2.x と併存します。
- **統一エンジン**: V3 は Kiro IDE / Web と同じエージェント基盤の上に構築され、エンジン改善が全クライアントへ同時に反映されます。
- **4 本柱（プレビュー）**: 仕様駆動開発（Spec agent / `/spec`）、capability ベースの権限（`permissions.yaml`）、強化版 Hooks（`.kiro/hooks/*.json`）、タグベースの Agent 設定。
- **Breaking changes / Known gaps あり**: 権限・Hooks・Agent 設定の非互換、`aws_tool` 削除、セッション形式非互換、Supervised mode 削除、AL2 非対応、非 TUI（classic）モード非対応 など。

> 📘 **詳細は専用セクションへ**: 4 本柱・Breaking changes・Known gaps・IDE 版との比較は **[09_v3/ Kiro CLI v3（Early Access）](../09_v3/README.md)** にまとめています。

> **日付の注記**: CLI 内蔵 changelog の日付（2026-06-16）と公式サイト表示日（2026-06-17）に差異があります。本サイトは**公式サイト表示日（2026-06-17）を採用**しています。

---

## v2.8.1 — MCP OAuth / spec 表示の改善（パッチ）

| 分類 | 内容 |
|------|------|
| **改善** | MCP OAuth パネルが、認可 URL を**クリップボードにコピーした際に確認表示**するように |
| **改善** | Welcome 画面のリンクを **V3 ドキュメント**へ更新 |
| **バグ修正** | V2 モードの MCP OAuth が認可 URL を**クリップボードにコピー**するよう修正（従来は無言で失敗） |
| **バグ修正** | **spec ワークフロー中**の subagent ツール呼び出し・承認プロンプトが**メインビューに表示**されるよう修正 |

> spec ワークフロー中の表示修正は、V3 の spec 機能が Early Access で実際に使われ始めていることの裏付けでもあります。

---

## 関連リンク

### 本サイトの関連文書
- [09_v3/ Kiro CLI v3（Early Access）概要](../09_v3/README.md) — 4 本柱・Breaking changes・Known gaps
- [09_v3/01. 仕様駆動開発](../09_v3/01_spec-driven-development.md) — `/spec` を使った CLI での実践
- [09_v3/02. Kiro IDE 版との比較](../09_v3/02_kiro-ide-vs-cli.md)
- [02_update/01_changelog.md](../02_update/01_changelog.md) — v2.8.1 / v2.8.0 / v2.7.1 の変更履歴

### 公式情報源
- [公式 CLI v3 ドキュメント](https://kiro.dev/docs/cli/v3/)
- [公式 Changelog v2.8](https://kiro.dev/changelog/cli/2-8/)

---

**最終更新**: 2026-06-21
**対象バージョン**: Kiro CLI v2.8.0 / v2.8.1（V3 は Early Access、`--v3` で提供）
