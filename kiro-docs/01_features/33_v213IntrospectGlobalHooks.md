[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.13 Introspect サブエージェント・グローバル hooks

---

# v2.13 Introspect サブエージェント・グローバル hooks（CLI v3 Early Access）

## 概要

Kiro CLI **v2.13.0**（公式表示日 2026-07-17）で、**Kiro CLI V3（Early Access）** に2つの機能が追加されました。

- **Introspect サブエージェント**: Kiro の機能に関する質問に答え、**カスタムエージェント・hooks・steering の作成を支援**する組み込みサブエージェント。
- **グローバル hooks**: `~/.kiro/hooks/` に置いた hooks が**全ワークスペースへ自動適用**される。

いずれも V3（`kiro-cli --v3`）向けの機能であり、V3 の全体像・4 本柱・Breaking changes は専用セクション **[09_v3/](../09_v3/README.md)** にまとめています。本ページは **v2.13.0 の事実と入口**に絞ります。あわせて v2.13.0 では全ユーザー向けのエラー表示改善（モデル拒否エラーのスクロールバック表示化、レート制限エラーの永続表示）も行われました。

**対応バージョン**: Kiro CLI v2.13.0（V3 は Early Access）

> **注記**: V3 は **Early Access** であり、仕様変更の可能性があります。最新は[公式 Changelog](https://kiro.dev/changelog/cli/) および [公式 CLI v3 ドキュメント](https://kiro.dev/docs/cli/v3/) を参照してください。

---

## Introspect サブエージェント

Kiro の機能について質問に答え、**カスタム agent / hooks / steering の作成を支援**する組み込みサブエージェントです。V3 の設定（仕様駆動開発・`permissions.yaml`・強化版 Hooks・タグベース Agent 設定の 4 本柱）を書く際の、対話的なガイドとして利用できます。

- V3 に組み込まれる**新しい組み込みサブエージェント**（仕様駆動の Spec agent に加わるもの）。
- 用途: Kiro の機能説明、カスタムエージェント・hooks・steering ファイルの作成支援。

> 詳細な V3 の 4 本柱・エージェント設定は [09_v3/ Kiro CLI v3（Early Access）](../09_v3/README.md) を参照してください。

---

## グローバル hooks（`~/.kiro/hooks/`）

従来、V3 の hooks はワークスペース単位（`.kiro/hooks/<name>.json`）で定義していましたが、v2.13.0 で **ユーザーグローバルの適用先 `~/.kiro/hooks/`** が追加されました。

- `~/.kiro/hooks/` に置いた hooks は**全ワークスペースへ自動適用**されます。
- プロジェクト横断で共通のフック（例: セッション開始時の共通セットアップ）を**ユーザー単位で一元管理**できます。
- hooks のスキーマ・アクション型（command / agent）・トリガ種別は従来どおり（→ [09_v3/ 強化版 Hooks](../09_v3/README.md)）。

| スコープ | 配置場所 | 適用範囲 |
|---------|---------|---------|
| ワークスペース | `.kiro/hooks/*.json` | 当該ワークスペースのみ |
| **ユーザーグローバル（v2.13.0 追加）** | `~/.kiro/hooks/*.json` | **全ワークスペースへ自動適用** |

---

## その他の v2.13.0 の変更（全ユーザー向け）

- **モデル拒否エラーの表示変更**: プロンプトバー上部にトーストを固定表示せず、スクロールバック行のみで表示（v2.12.1 の「モデル拒否通知」の表示挙動を洗練）。
- **レート制限エラーの永続表示**: トーストが消えた後もスクロールバックにメッセージが残る。
- **[V3] バグ修正**: Always-accept 承認がバックスラッシュエスケープを含むシェルコマンドでループしない、バックエンド API 接続で `HTTP_PROXY`・`HTTPS_PROXY` を尊重。

詳細は [変更履歴 v2.13.0](../02_update/01_changelog.md) を参照してください。

---

## 注意点・制限事項

- 本機能は **V3（Early Access）** 向けです。V3 は破壊的変更・Known gaps（Amazon Linux 2 非対応・非 TUI モード非対応・セッション非互換）を伴うため、[09_v3/ Breaking changes / Known gaps](../09_v3/README.md) を確認してください。
- Introspect サブエージェントの挙動・グローバル hooks の詳細仕様は今後変更される可能性があります（Early Access）。

---

## 関連リンク

- [09_v3/ Kiro CLI v3（Early Access）概要](../09_v3/README.md) — 4 本柱・Breaking changes・Known gaps
- [30. v2.8 / V3 プレビュー](30_v28V3Preview.md) — V3 Early Access の入口（v2.8.0）
- [変更履歴 v2.13.0](../02_update/01_changelog.md)
- [公式 Hooks（CLI v3）](https://kiro.dev/docs/cli/v3/hooks/)
- [公式 Changelog v2.13](https://kiro.dev/changelog/cli/2-13/)

---

**最終更新**: 2026-07-20  
**対象バージョン**: Kiro CLI v2.13.0+（V3 は Early Access）
