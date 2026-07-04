[ホーム](../README.md) > Kiro CLI v3（Early Access）

# 09. Kiro CLI v3（Early Access）概要

> ⚠️ **Early Access の注意**: Kiro CLI v3（公式表記「**CLI 3.0**」「**V3**」）は **Early Access（先行公開）** です。現状は **v2.8.x に `--v3` フラグで同梱**され、オプトインで試せます。GA（正式版）としての「3.0.0」はまだリリースされていません。**仕様は変更される可能性があり**、本セクションの内容は公式ドキュメント更新に追従して見直します。

> 💡 **どちらを読めばいい？**: 普段の利用では、まず **v2 系のドキュメント**（[機能詳細ガイド](../01_features/README.md)・[リファレンス](../04_reference/README.md)）を参照してください。本セクション（09_v3/）は「v3 を先行して試したい人」向けです。

**位置付け**: v3 は単一機能の追加ではなく、**エージェント実行基盤（エンジン）の刷新＋仕様駆動開発（Spec-driven development）の導入**という「開発パラダイムの更新」です。そのため本サイトでは独立セクション（`09_v3/`）にまとめています。

**出典（一次情報）**:
- [Kiro CLI v3 概要（公式）](https://kiro.dev/docs/cli/v3/)
- [Spec-driven development（公式 CLI specs）](https://kiro.dev/docs/cli/v3/specs/)
- [機能比較 v2 → v3（公式 feature-overview）](https://kiro.dev/docs/cli/v3/feature-overview/)
- [Permissions（公式）](https://kiro.dev/docs/cli/v3/permissions/) ／ [Hooks（公式）](https://kiro.dev/docs/cli/v3/hooks/) ／ [Agent config（公式）](https://kiro.dev/docs/cli/v3/agent-config/)
- [公式 Changelog v2.8](https://kiro.dev/changelog/cli/2-8/)

---

## このセクションの構成

- **本ページ（README）** — v3 の全体像、4 本柱、Breaking changes / Known gaps、Early Access の位置付け
- **[01. 仕様駆動開発（Spec-driven development）](01_spec-driven-development.md)** — `/spec` を使った CLI での実践、`.kiro/specs/` の3ファイル、AI-DLC との違い
- **[02. Kiro IDE 版との比較](02_kiro-ide-vs-cli.md)** — 「同様にできること／IDE が優位なこと／CLI ならではのこと」を一次情報ベースで整理

---

## v3 とは（統一エンジンとメジャー更新）

Kiro CLI v3 の核心は **「統一エンジン（single engine for all Kiro surfaces）」** です。CLI 3.0 は Kiro IDE / Kiro Web と**同じエージェント基盤**の上に構築され、エンジン側の改善（新しいツール、計画立案、ツール選択など）が**全クライアントへ同時に届く**ようになりました。

- **試し方**: `kiro-cli --v3` で V3 エンジンを起動（オプトイン）。
- **併存**: 既存の **2.x と併存**します。設定を変えずにそのまま試せます。
- **提供形態**: v2.8.0（公式表示日 2026-06-17）で **Early Access** として先行公開されました。

```bash
# V3 エンジンを試す（既存 2.x はそのまま）
kiro-cli --v3
```

---

## v3 の 4 本柱

公式 v3 ドキュメントは、v3 の新規性を次の 4 つで説明しています。

| 柱 | 概要 | 詳細 |
|----|------|------|
| **仕様駆動開発**（Spec-driven development） | 組み込みの **Spec agent**。要件 → 設計 → タスク → 実行を計画してから進める | [01. 仕様駆動開発](01_spec-driven-development.md)、[公式](https://kiro.dev/docs/cli/v3/specs/) |
| **Capability ベースの権限**（Permissions） | `permissions.yaml` に許可/拒否ルールを宣言。`--trust-all-tools` / `/tools trust` を置換 | [公式 Permissions](https://kiro.dev/docs/cli/v3/permissions/) |
| **強化版 Hooks** | 独立ファイル `.kiro/hooks/*.json`（バージョン付きスキーマ）、2 アクション型（shell / agent）、新トリガ | [公式 Hooks](https://kiro.dev/docs/cli/v3/hooks/) |
| **強化版 Agent 設定** | タグでツール種別を選択、`permissions` ブロック統合、Markdown 形式、inline MCP | [公式 Agent config](https://kiro.dev/docs/cli/v3/agent-config/) |

### 4 本柱のポイント（一次情報の要約）

- **Permissions**: 1 つのルールは `capability`（操作種別）/ `match`（グロブ）/ `exclude` / `effect`（`deny`・`ask`・`allow`）の 4 フィールド。効果は **deny > ask > allow** の順で厳しい方が勝ちます。ルールは **User**（`~/.kiro/settings/permissions.yaml`）と **Workspace**（`~/.kiro/workspace-roots/<hash>/permissions.yaml`、**リポジトリ外・ユーザー単位**で保持されるためクローンしたリポジトリが権限を注入できない）の2スコープ。CI 向けには `capability: all / effect: allow` の例が示されています。
- **Hooks**: `.kiro/hooks/<name>.json`（`"version": "v1"`）に定義。**command**（シェル実行、stdin に JSON、終了コード 0=成功 / 2=ブロック）と **agent**（プロンプトを文脈へ追記）の 2 型。トリガは `SessionStart` / `Stop` / `PreToolUse` / `PostToolUse` / `UserPromptSubmit` / `PostFileCreate` / `PostFileSave` のほか、**3.0 新規**の `PreTaskExec` / `PostTaskExec` / `PostFileDelete` / `Manual`。旧 hooks は `kiro-cli agent migrate` で新形式へ変換できます。
- **Agent 設定**: Markdown の本文がシステムプロンプト、フロントマターに `description` / `model` / `tools`（タグ）/ `mcpServers` / `resources` / `permissions` / `welcomeMessage` を記述（JSON でも等価）。タグは `read` / `write` / `shell` / `web` / `subagent` / `knowledge` / `todo_list` / `@mcp` / `@builtin` / `*`。新しいツールがカテゴリに追加されると**自動で取り込まれます**。配置は `.kiro/agents/`（ワークスペース）・`~/.kiro/agents/`（ユーザー）。

---

## Breaking changes（v2 → v3）

v3 は **後方互換ではない変更**を含みます。切り替え前に確認してください。

| 領域 | 変更内容 |
|------|----------|
| **権限** | `--trust-all-tools` / `/tools trust` を **`permissions.yaml`** で置換 |
| **Hooks** | 埋め込み hooks を**独立ファイル** `.kiro/hooks/*.json` へ。トリガ名は PascalCase |
| **Agent 設定** | `toolsSettings` を **`permissions`** フィールドへ、個別ツール ID を**タグ**へ |
| **aws_tool** | **削除**（MCP サーバーで代替） |
| **セッション形式** | v3 形式は**後方互換なし**。切り替え前に `~/.kiro/sessions/` をバックアップ推奨 |
| **Supervised mode** | **削除**（`permissions.yaml` で代替） |

> **移行ガイド**: 公式は「v2 設定を変換する移行ガイドは **coming soon（準備中）**」としています。本サイトでは移行手順を断定せず、上記の breaking changes の一覧提示にとどめます。

---

## Known gaps（既知の制限）

| 制限 | 内容 |
|------|------|
| **Amazon Linux 2 非対応** | CLI 3.0 は **AL2 では動作しません**。AL2 が必要な環境は CLI 2.x を使用 |
| **Classic mode 非対応** | レガシーの**非 TUI モード**（`kiro-cli chat` を TUI なしで使う形態）は v3 エンジン非対応。**TUI を使用** |
| **セッション再開の非互換** | **V3 セッションは V2 で再開不可**。V2 に戻すと、作成済みの V3 セッションは利用できません |

---

## 環境の確認

v3 を試す前後の環境確認には `kiro-cli diagnostic` が使えます（公式 v3 ドキュメントでも環境検証ツールとして案内）。

```bash
# 環境の診断テストを実行（出力形式は plain / json / json-pretty）
kiro-cli diagnostic
kiro-cli diagnostic --format json-pretty
```

---

## 関連リンク

### 本セクション内
- [01. 仕様駆動開発（Spec-driven development）](01_spec-driven-development.md)
- [02. Kiro IDE 版との比較](02_kiro-ide-vs-cli.md)

### 本サイトの関連文書
- [01_features/30. v2.8 / V3 プレビュー](../01_features/30_v28V3Preview.md) — v2.8.0 / v2.8.1 の事実と `--v3` の入口
- [07_aidlc/](../07_aidlc/README.md) — AI-DLC（AWS Labs OSS 方法論）。v3 の純正 Spec agent とは別物（→ [01. 仕様駆動開発](01_spec-driven-development.md) の比較表）
- [02_update/01_changelog.md](../02_update/01_changelog.md) — v2.8.0 / v2.8.1 の変更履歴

### 公式情報源
- [Kiro CLI v3 概要](https://kiro.dev/docs/cli/v3/)
- [Spec-driven development](https://kiro.dev/docs/cli/v3/specs/)
- [機能比較 v2 → v3](https://kiro.dev/docs/cli/v3/feature-overview/)
- [Permissions](https://kiro.dev/docs/cli/v3/permissions/) ／ [Hooks](https://kiro.dev/docs/cli/v3/hooks/) ／ [Agent config](https://kiro.dev/docs/cli/v3/agent-config/)

---

**最終更新**: 2026-06-21
**対象バージョン**: Kiro CLI v3（Early Access）— v2.8.x ＋ `--v3` で提供。3.0.0 GA は未リリース。
