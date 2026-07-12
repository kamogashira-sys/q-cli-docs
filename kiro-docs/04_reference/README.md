[ホーム](../README.md) > リファレンス

# 04_reference: Kiro CLI リファレンス集

このディレクトリは、Kiro CLI の **辞書的・網羅的なリファレンス** を集約しています。機能解説（読み物）と性質が異なるため、独立したディレクトリで管理しています。

> **目次の方針**: 各リファレンスは公式情報源を一次情報として、設定キー、コマンド、ツールパラメータ等を **網羅的かつ正確に** 記述します。例は最小限にとどめ、具体的なユースケース・ストーリー説明は [01_features/](../01_features/) の各機能文書に委ねます。

---

## 📋 リファレンス一覧

| # | ファイル | 内容 | 公式情報源 | 公式更新日 |
|---|--------|------|----------|----------|
| 01 | [Settings](01_settings.md) | 全設定項目（公式8カテゴリ）と環境変数 | https://kiro.dev/docs/cli/reference/settings/ | 2026-06-05 |
| 02 | [Slash Commands](02_slash-commands.md) | 全スラッシュコマンド（40種）とキーボードショートカット | https://kiro.dev/docs/cli/reference/slash-commands/ | 2026-06-12 |
| 03 | [CLI Commands](03_cli-commands.md) | `kiro-cli` コマンド全16種、グローバル引数、セッション管理 | https://kiro.dev/docs/cli/reference/cli-commands/ | 2026-05-12 |
| 04 | [Built-in Tools](04_built-in-tools.md) | 組み込みツール18種（read/glob/grep/write/shell/aws/web_search/web_fetch/introspect/code/tool_search/delegate/subagent/report/knowledge/thinking/todo/session） | https://kiro.dev/docs/cli/reference/built-in-tools/ | 2026-05-12 |

---

## 🗂️ 使い分けガイド

### こんな時にどのリファレンスを見るか

| 知りたいこと | 参照先 |
|----------|------|
| 「`chat.disableWrap` の意味は？」 | [01_settings.md](01_settings.md) |
| 「`/effort` コマンドのレベル一覧は？」 | [02_slash-commands.md](02_slash-commands.md) |
| 「`kiro-cli login --use-device-flow` の意味は？」 | [03_cli-commands.md](03_cli-commands.md) |
| 「`fs_write` ツールの `allowedPaths` 書式は？」 | [04_built-in-tools.md](04_built-in-tools.md) |
| 「`AGENT_DISPLAY_OUT` 環境変数とは？」 | [04_built-in-tools.md](04_built-in-tools.md)（Side channels） |
| 「`KIRO_HOME` の挙動は？」 | [01_settings.md](01_settings.md)、[03_cli-commands.md](03_cli-commands.md) |

### 機能文書（読み物）との関係

リファレンスはあくまで **辞書** です。実際の使用例、ストーリー、シナリオは以下の機能文書を参照してください：

| 設定/コマンド/ツール | 関連機能文書 |
|----------------|-----------|
| `chat.modelDefaults`、`/effort`、`/rewind`、`/settings` | [21. v24NewCommands](../01_features/21_v24NewCommands.md) |
| `toolSearch.*`、`tool_search` ツール | [19. Tool Search](../01_features/19_ToolSearch.md) |
| `compaction.*`、`/compact` | [10. Conversation Compaction](../01_features/10_ConversationCompaction.md) |
| `knowledge.*`、`knowledge` ツール、`/knowledge` | [07. Skills](../01_features/07_Skills.md)（補強） |
| `chat.diffTool`、`write` ツールの diff | [08. Custom Diff Tools](../01_features/08_CustomDiffTools.md) |
| `web_fetch` の URL 権限 | [11. URL Permissions](../01_features/11_URLPermissions.md) |
| `shell` の段階的信頼 | [17. Granular Tool Trust](../01_features/17_GranularToolTrust.md) |
| `KIRO_API_KEY`、`chat.ui` | [16. v2 Major Update](../01_features/16_v2MajorUpdate.md) |
| `kiro-cli login`（リモート認証） | [12. Remote Auth](../01_features/12_RemoteAuth.md) |
| Hooks の matcher 対象ツール | [22. Hooks](../01_features/22_Hooks.md) |
| `@file/@directory` 構文 | [24. File References](../01_features/24_FileReferences.md) |
| Steering と Custom Agents | [23. Steering](../01_features/23_Steering.md) |
| `kiro-cli inline`、`/theme` | [25. AutoComplete](../01_features/25_AutoComplete.md) |
| AWS MCP Server / Skills / `mcp.json` | [26. Agent Toolkit for AWS](../01_features/26_AgentToolkitForAWS.md) 🌟 |

---

## 📌 公式情報源

**Kiro CLI 公式リファレンスインデックス**: https://kiro.dev/docs/cli/reference/

各リファレンスファイルの末尾に詳細な公式情報源リンクを記載しています。本サイトのリファレンスは公式ページの **日本語訳・補足版** であり、最新の正確な情報は常に公式を参照してください。

### 公式リファレンス公開日（取得時点）

| 公式ページ | 更新日 |
|----------|------|
| Settings | 2026-06-05 |
| Slash Commands | 2026-06-12 |
| CLI Commands | 2026-05-12 |
| Built-in Tools | 2026-05-12 |

---

## ⚠️ 注意事項

- 本ディレクトリの各文書は **2026-06-21 時点** の情報に基づいています（Slash Commands は公式 2026-06-12 版、Settings は公式 2026-06-05 版を反映。Settings の v2.7.0 追加項目 `chat.terminalTitle`/`chat.defaultInterruptBehavior` は CLI 内蔵 changelog から補完し、`chat.terminalTitle` の型・既定値と公式未掲載設定の補遺は実機 kiro-cli 2.10.0 の `settings list --all` で確認・2026-07-04）
- Kiro CLI は活発に開発されており、公式の更新が反映されていない可能性があります
- 重要な設定変更前は **必ず公式ページを確認** してください

---

## 関連リンク

### 本サイト

- [機能詳細ガイド (01_features/)](../01_features/README.md) — 32機能の詳細解説
- [アップデート情報 (02_update/)](../02_update/README.md) — バージョン履歴と主要変更
- [デプロイ・環境構築 (03_deployment/)](../03_deployment/README.md) — インストール手順
- [メタドキュメント (05_meta/)](../05_meta/) — 品質保証関連

### 公式情報源

- [Kiro CLI Documentation](https://kiro.dev/docs/cli/) — 公式トップ
- [Kiro CLI Reference](https://kiro.dev/docs/cli/reference/) — 公式リファレンスインデックス
- [Kiro CLI Changelog](https://kiro.dev/changelog/cli/) — 公式 changelog

---

**Page updated**: 2026-06-28（v2.7.0/v2.6.1対応: Slash Commands を公式 2026-06-12 版に更新、`/goal`・Queue Steering キーバインド追加、Settings は公式 2026-06-05 版のまま（v2.7.0 未反映）／ v2.8.0・V3 Early Access 対応: v3（`--v3`）コマンドは [09_v3/](../09_v3/README.md) 参照の注記を追加、機能数 30 に同期 ／ v2.10.0・v2.9.0対応: Settings に `chat.disableInheritingDefaultResources` を追記（出典: カスタムエージェント設定リファレンス 2026-06-26）、機能数 31 に同期）
