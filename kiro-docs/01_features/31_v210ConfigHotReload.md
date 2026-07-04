[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.10 設定ホットリロード & リソース継承制御

---

# v2.10 設定ホットリロード & リソース継承制御

## 概要

Kiro CLI **v2.10.0**（公式表示日 2026-06-26）では、設定まわりに2つの機能が追加されました。

1. **MCP・エージェント設定のホットリロード** — `.kiro/agents` と `mcp.json` の保存変更を検知し、再起動なしで設定を反映。
2. **`chat.disableInheritingDefaultResources` 設定** — カスタムエージェントが既定リソース（steering / skills / AGENTS.md）を継承するか否かを制御（v2.7.0 で導入された自動継承のオプトアウト手段）。

いずれも日々の設定変更・エージェント運用を滑らかにする改善です。

**対応バージョン**: Kiro CLI v2.10.0+

> **注記**: 本ページは一次情報（CLI 内蔵 changelog・公式 Changelog・公式ドキュメント）に基づきます。最新は[公式 Changelog](https://kiro.dev/changelog/cli/) を参照してください。

---

## 1. MCP・エージェント設定のホットリロード

`.kiro/agents`（エージェント定義）と `mcp.json`（MCP サーバー設定）を監視する **file watcher** が、保存された変更を検知して**差分調整（diff reconciliation）**を行います。

- **変更サーバーのみ再起動**: 追加 / 削除 / 編集されたサーバー・エージェントのみを対象に再起動・再マージし、無関係なサーバーは稼働を継続します。
- **会話コンテキストの保持**: リロード時も現在の会話コンテキストは保持されます（セッションのやり直しは不要）。
- **順序非依存の差分**: 環境変数や JSON キーの並べ替えなど、**意味の変わらない変更は「変更」と見なさず**再起動しません。
- **セッション注入サーバーの保持**: `/mcp add` でセッションに注入したサーバーも、再マージ時に保持されます。
- **コマンド不要・アイドル境界で反映**: 反映のための明示的なコマンドは不要で、変更は**次のアイドル境界（ターン間）**で適用されます。

```bash
# 例: mcp.json を編集して保存するだけで、変更サーバーが再起動され反映される
#     （再起動コマンドや会話のやり直しは不要）
$EDITOR .kiro/agents/my-agent.json
```

詳細は公式ドキュメントを参照してください。

- 公式: [MCP 設定（Hot-Reload）](https://kiro.dev/docs/cli/mcp/configuration/)

---

## 2. カスタムエージェントの既定リソース継承制御（`chat.disableInheritingDefaultResources`）

v2.7.0 以降、カスタムエージェントは組み込みエージェントと同様に**既定リソース（steering / skills / AGENTS.md）を自動継承**します。v2.10.0 で追加された `chat.disableInheritingDefaultResources` 設定により、この自動継承を**オプトアウト**できます。

| 項目 | 値 |
|------|----|
| 設定キー | `chat.disableInheritingDefaultResources` |
| 型 | Boolean |
| 既定値 | `false`（カスタムエージェントは既定リソースを継承） |
| スコープ | グローバル、または workspace で上書き可 |
| `true` 時の挙動 | **カスタム（ユーザー定義）エージェント**が既定 steering / skills / AGENTS.md を継承しなくなる |
| 組み込みエージェント | 本設定に関わらず**常に継承**（影響を受けない） |

```bash
# グローバルで既定リソースの継承を無効化（カスタムエージェント対象）
kiro-cli settings chat.disableInheritingDefaultResources true

# 既定（継承する）に戻す
kiro-cli settings chat.disableInheritingDefaultResources false
```

- 既定リソースを明示的に管理したい場合や、カスタムエージェントに不要なコンテキストを含めたくない場合に有用です。
- 組み込みエージェントは常に既定リソースを継承するため、本設定の影響を受けません。
- 公式: [カスタムエージェント設定リファレンス](https://kiro.dev/docs/cli/custom-agents/configuration-reference/)

> **出典の注記**: 公式 [Settings リファレンス](https://kiro.dev/docs/cli/reference/settings/)（公式ページ最終更新 2026-06-05）には本設定が未反映のため、本サイトは[カスタムエージェント設定リファレンス](https://kiro.dev/docs/cli/custom-agents/configuration-reference/)（公式ページ最終更新 2026-06-26）を一次情報として採用しています。

---

## 関連リンク

### 本サイトの関連文書
- [02. Subagents](02_Subagents.md) — カスタムエージェント・サブエージェントの運用
- [23. Agent Steering](23_Steering.md) — steering（既定リソース）の仕組み
- [07. Skills](07_Skills.md) — skills（既定リソース）の仕組み
- [04_reference/01. Settings リファレンス](../04_reference/01_settings.md) — `chat.disableInheritingDefaultResources` を含む設定一覧
- [02_update/01_changelog.md](../02_update/01_changelog.md) — v2.10.0 / v2.9.0 の変更履歴

### 公式情報源
- [公式 Changelog v2.10](https://kiro.dev/changelog/cli/2-10/)
- [MCP 設定（Hot-Reload）](https://kiro.dev/docs/cli/mcp/configuration/)
- [カスタムエージェント設定リファレンス](https://kiro.dev/docs/cli/custom-agents/configuration-reference/)

---

**最終更新**: 2026-06-28
**対象バージョン**: Kiro CLI v2.10.0+
