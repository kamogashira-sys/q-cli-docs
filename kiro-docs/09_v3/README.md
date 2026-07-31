[ホーム](../README.md) > Kiro CLI v3（Early Access）

# 09. Kiro CLI v3（Early Access）概要

> ⚠️ **Early Access の注意**: Kiro CLI v3（公式表記「**CLI 3.0**」「**V3**」）は **Early Access（先行公開）** です。**v2.8.0 以降の 2.x に `--v3` フラグで同梱**され、オプトインで試せます。GA（正式版）としての「3.0.0」はまだリリースされていません。**仕様は変更される可能性があり**、本セクションの内容は公式ドキュメント更新に追従して見直します。

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
- **Hooks**: `.kiro/hooks/<name>.json`（`"version": "v1"`）に定義。**command**（シェル実行、stdin に JSON、終了コード 0=成功 / 2=ブロック）と **agent**（プロンプトを文脈へ追記）の 2 型。トリガは `SessionStart` / `Stop` / `PreToolUse` / `PostToolUse` / `UserPromptSubmit` / `PostFileCreate` / `PostFileSave` のほか、**3.0 新規**の `PreTaskExec` / `PostTaskExec` / `PostFileDelete` / `Manual`。旧 hooks は `kiro-cli agent migrate` で新形式へ変換できます。**v2.13.0（2026-07-17）** では、`~/.kiro/hooks/` に置いた**グローバル hooks** が追加され、**全ワークスペースへ自動適用**されるようになりました（従来のワークスペース単位 `.kiro/hooks/` に加えた、ユーザーグローバルの適用先）。
- **Agent 設定**: Markdown の本文がシステムプロンプト、フロントマターに `description` / `model` / `tools`（タグ）/ `mcpServers` / `resources` / `permissions` / `welcomeMessage` を記述（JSON でも等価）。タグは `read` / `write` / `shell` / `web` / `subagent` / `knowledge` / `todo_list` / `@mcp` / `@builtin` / `*`。新しいツールがカテゴリに追加されると**自動で取り込まれます**。配置は `.kiro/agents/`（ワークスペース）・`~/.kiro/agents/`（ユーザー）。

### v2.13.0 での追加（Introspect サブエージェント・グローバル hooks）

**v2.13.0（2026-07-17）** で、V3（Early Access）に2つの機能が追加されました。

- **Introspect サブエージェント**: Kiro の機能に関する質問に答え、**カスタムエージェント・hooks・steering の作成を支援**する組み込みサブエージェント。Spec agent（仕様駆動）に加わる新しい組み込みエージェントで、v3 の設定（上記 4 本柱）を書く際の対話的なガイドとして使えます。
- **グローバル hooks**: `~/.kiro/hooks/` に置いた hooks が**全ワークスペースへ自動適用**されます（詳細は上記「Hooks」ポイント）。プロジェクト横断で共通のフック（例: セッション開始時の共通セットアップ）をユーザー単位で一元管理できます。

出典: [公式 Hooks](https://kiro.dev/docs/cli/v3/hooks/)、[公式 Changelog v2.13](https://kiro.dev/changelog/cli/2-13/)。

### v2.14.0 での追加（`/upgrade-agent`・自動ストリームリトライ）

**v2.14.0（2026-07-22）** で、V2 のカスタムエージェント設定を **V2/V3 両対応の universal 形式へ変換する `/upgrade-agent`** が追加されました。

- **`/upgrade-agent`**: V3 セッション内で実行し、`.kiro/agents/`（ワークスペース）と `~/.kiro/agents/`（ユーザー）をスキャンして変換対象を選択。元ファイルは `<filename>.json.bak` にバックアップされ、既存設定に併存する形で新形式の権限フィールドが追加されます。`/upgrade-agent diagnostics` で変換警告（`regex-shell-pattern` 等 8 種）を確認できます。
  → 詳細: [01_features/34. v2.14 /upgrade-agent](../01_features/34_v214UpgradeAgent.md)、[公式ドキュメント](https://kiro.dev/docs/cli/v3/upgrade-agent/)
- **自動ストリームリトライ**: 空で届いた応答・ストリーム途中で切り詰められた応答を自動的に再試行。
- **バグ修正**: カスタムエージェント切替後に model・effort の選択肢が更新される、`/plan` が複数の確認質問でデッドロックしない、アクティブなエージェントが自身のサブエージェント委譲リストに出ない、supervised モードのターン承認がセッション再開後も維持される、`web_fetch` の二重リトライを 1 回へ統合、不正なツール入力時のエラーメッセージ改善。

出典: [公式 Changelog v2.14](https://kiro.dev/changelog/cli/2-14/)、[Upgrading agent configs（公式）](https://kiro.dev/docs/cli/v3/upgrade-agent/)。

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
| **Supervised mode** | 公式 v3 ドキュメントは **削除**（`permissions.yaml` で代替）と記載（下記注記も参照） |

> **移行手段（v2.14.0 で追加）**: V2 のカスタムエージェント設定は **`/upgrade-agent`**（V3 セッション内で実行）で V2/V3 両対応の universal 形式へ変換できます。公式 [v3 概要](https://kiro.dev/docs/cli/v3/) も同コマンドと [migration guide](https://kiro.dev/docs/cli/v3/upgrade-agent/) を案内しています。→ [01_features/34. v2.14 /upgrade-agent](../01_features/34_v214UpgradeAgent.md)
>
> ⚠️ **Supervised mode の扱いに公式内で差異があります**: 公式 [v3 概要](https://kiro.dev/docs/cli/v3/) と [機能比較](https://kiro.dev/docs/cli/v3/feature-overview/) は「Supervised mode = Removed（`permissions.yaml` で代替）」と記載していますが、[公式 Changelog v2.14](https://kiro.dev/changelog/cli/2-14/)（v2.14.0）のバグ修正には「[V3] supervised モードのターン承認がセッション再開後も維持される」という項目があります。本サイトは双方を出典付きで併記し、どちらかを断定しません。

### 機能強化（v2 → v3、置換ではなく拡張）

上記の Breaking changes（置換・削除）とは異なり、v2 の機能名をそのまま引き継ぎつつ**仕様が拡張**された例もあります。

| 領域 | 変更内容 |
|------|----------|
| **Tangent**（`/tangent`） | v2.16.0 でV3版が追加。名前付き・ネスト可能な側枝会話とビジュアルピッカーが、単一チェックポイントのV2 classic版を置き換える形で強化。公式 [Feature comparison](https://kiro.dev/docs/cli/v3/feature-overview/) は「⬆️ Enhanced — Named, nestable side-conversations with a visual picker replace the single-checkpoint experiment」と明記。V2 classic版のコマンド名は同じだが動作は別物（→ [01_features/35. v2.16 Tangent（V3側枝会話）](../01_features/35_v216Tangent.md)、[04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md#tangent)） |

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
- [01_features/33. v2.13 Introspect サブエージェント・グローバル hooks](../01_features/33_v213IntrospectGlobalHooks.md) — v2.13.0 の V3 追加機能
- [01_features/34. v2.14 /upgrade-agent](../01_features/34_v214UpgradeAgent.md) — V2 → V3 エージェント設定移行（v2.14.0）
- [07_aidlc/](../07_aidlc/README.md) — AI-DLC（AWS Labs OSS 方法論）。v3 の純正 Spec agent とは別物（→ [01. 仕様駆動開発](01_spec-driven-development.md) の比較表）
- [02_update/01_changelog.md](../02_update/01_changelog.md) — v2.8.0 / v2.8.1 の変更履歴

### 公式情報源
- [Kiro CLI v3 概要](https://kiro.dev/docs/cli/v3/)
- [Spec-driven development](https://kiro.dev/docs/cli/v3/specs/)
- [機能比較 v2 → v3](https://kiro.dev/docs/cli/v3/feature-overview/)
- [Permissions](https://kiro.dev/docs/cli/v3/permissions/) ／ [Hooks](https://kiro.dev/docs/cli/v3/hooks/) ／ [Agent config](https://kiro.dev/docs/cli/v3/agent-config/)
- [Upgrading agent configs（`/upgrade-agent`）](https://kiro.dev/docs/cli/v3/upgrade-agent/)

---

**最終更新**: 2026-08-01
**対象バージョン**: Kiro CLI v3（Early Access）— v2.8.x 以降 ＋ `--v3` で提供。3.0.0 GA は未リリース。
