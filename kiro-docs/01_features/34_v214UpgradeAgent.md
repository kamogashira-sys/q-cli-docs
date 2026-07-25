[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.14 /upgrade-agent（V2 → V3 エージェント設定移行）

---

# v2.14 /upgrade-agent（V2 → V3 エージェント設定移行）

## 概要

Kiro CLI **v2.14.0**（公式表示日 2026-07-22）で、**V2 のカスタムエージェント設定を V2/V3 の両方で動作する "universal" 形式へ変換する** `/upgrade-agent` が追加されました。**V3（`kiro-cli --v3`）のセッション内で実行**するコマンドです。

これまで V3 のエージェント設定（タグベースのツール指定・`permissions` ブロック）への移行は手作業で、公式も「移行ガイドは準備中」としていました。v2.14.0 以降は `/upgrade-agent` が既存設定を読み取り、**元ファイルをバックアップしたうえで**新形式の権限フィールドを追加した設定を生成します。

**対応バージョン**: Kiro CLI v2.14.0（V3 は Early Access）

> **注記**: V3 は **Early Access** であり、仕様変更の可能性があります。V3 の全体像・4 本柱・Breaking changes は専用セクション **[09_v3/](../09_v3/README.md)** にまとめています。最新は[公式 Changelog](https://kiro.dev/changelog/cli/) および [公式ドキュメント](https://kiro.dev/docs/cli/v3/upgrade-agent/) を参照してください。

---

## 使い方

```bash
# V3 セッションを起動
kiro-cli --v3
```

V3 セッション内で以下を実行します。

```
# エージェントをスキャンして選択メニューを開く（既定）
/upgrade-agent

# 上と同じ（サブコマンドを明示）
/upgrade-agent run

# 変換済みエージェントと変換時の警告を確認
/upgrade-agent diagnostics
```

`run`（既定）はワークスペースの `.kiro/agents/` とグローバルの `~/.kiro/agents/` をスキャンし、**スコープ別にグループ化した選択メニュー**を表示します。**更新が必要なエージェントだけが表示**され、すでに最新形式のものは表示されません。

選択メニューの例（公式ドキュメントより）:

```
V2 [3 agents]               Workspace    Upgrade to universal (V2 + V3) config
V2 [1 agent]                Global       Upgrade to universal (V2 + V3) config
```

変換後は「`Upgraded 3 agents (backed up to .json.bak)`」のような確認アラートが表示されます。

---

## 変換時の動作

エージェントのグループを選択すると、次の順で処理されます。

1. 元ファイルを `<filename>.json.bak` へコピー（バックアップ）
2. 既存の設定に**併存する形**で新形式の権限フィールドを追加
3. 元の設定（ツール名・許可コマンド・パス制限）を、新形式の同等ルールとして保持
4. 変換件数を示す確認アラートを表示

バックアップファイルが既に存在する場合は、`.bak.1`・`.bak.2` のように連番の接尾辞が付きます。

### 変換を取り消す

`.json.bak` を元の名前に戻します。

```bash
mv .kiro/agents/my-agent.json.bak .kiro/agents/my-agent.json
```

---

## 何が変換されるか

| 対象 | 変換内容 |
|------|---------|
| **ツール名** | 旧名（`fs_read`・`execute_bash` 等）を V3 の capability タグ（`read`・`shell` 等）へマップ。**両方が保持**され互換性を確保 |
| **`toolsSettings`** | ツール単位の allow/deny ルールを `permissions.rules` のエントリ（capability・match パターン・effect）へ変換 |
| **`allowedTools`** | 信頼済みツールのエントリを capability レベルの allow ルールへ変換 |
| **正規表現パターン** | 可能な範囲で単純なワイルドカード glob へ変換。安全に変換できない複雑なパターンは**警告**を生成 |
| **`autoAllowReadonly`** | read-only シェルのポリシーへ変換 |
| **オブジェクト形式の hooks** | V3 スキーマが要求する配列形式へ変換 |

**変換されず、そのまま引き継がれるフィールド**: `name`・`description`・`model`・`prompt`・`resources`・`mcpServers`・`welcomeMessage`

---

## 診断（`/upgrade-agent diagnostics`）

完全に変換できなかったパターンを確認します。出力例（公式ドキュメントより）:

```
2 Universal agents

  my-agent     Workspace   ⚠ regex-shell-pattern: ^git\s
  strict-dev   Global      ⚠ deny-by-default-readonly
```

### 警告の種類

| 警告 | 意味 | 対応 |
|------|------|------|
| `regex-shell-pattern` | シェルの正規表現を glob で近似した | `permissions.rules` の変換後パターンを確認 |
| `regex-web-pattern` | URL の正規表現を glob で近似した | 変換後の URL パターンを確認 |
| `unconvertible-pattern` | 正規表現を安全に変換できなかった | `permissions.rules` へ手動でルールを追加 |
| `unmapped-allowed-tool` | ツールのエントリを capability にマップできなかった | ツール名の変更・削除の有無を確認 |
| `deprecated-aws-tool` | `aws` / `use_aws` ツールが非推奨 | 非推奨ツールの参照を削除 |
| `deny-by-default-readonly` | deny-by-default と auto-allow-readonly が競合 | 権限の意図を見直して手動調整 |
| `file-prompt` | 絶対パスや `~/` のファイルプロンプトは環境によって解決されない場合がある | 相対パスを使用 |
| `unconvertible-hook` | hook を新形式へ変換できなかった | サポートされるトリガ形式で hook を作り直す |

---

## スキャン対象外

- バックアップファイル（`.bak`）
- 有効なエージェント設定でない JSON（`prompt`・`tools`・`hooks`・権限フィールドのいずれも持たないファイル）

---

## v2.14.0 のその他の V3 改善

`/upgrade-agent` と同時に、V3 では以下が改善されました（詳細は [変更履歴 v2.14.0](../02_update/01_changelog.md)）。

- **自動ストリームリトライ**: 空で届いた応答・ストリーム途中で切り詰められた応答を自動的に再試行。
- **待機中の機能ヒント**: 応答待ちの間、thinking インジケータの下に機能ヒントを表示（V2/V3 共通）。
- **バグ修正**: カスタムエージェント切替後の model・effort 選択肢の更新、`/plan` の複数確認質問によるデッドロック解消、自身のサブエージェント委譲リストからの除外、supervised モードのターン承認がセッション再開後も維持、`web_fetch` の二重リトライを 1 回へ統合、不正なツール入力時のエラーメッセージ改善。

---

## 注意点・制限事項

- **V3 専用**: `/upgrade-agent` は V3 セッション（`kiro-cli --v3`）内でのみ利用できます。V2 安定版のスラッシュコマンド一覧（[04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md)）には含めていません。
- **V3 は Early Access**: 破壊的変更・Known gaps（Amazon Linux 2 非対応・非 TUI モード非対応・セッション非互換）を伴います（→ [09_v3/](../09_v3/README.md)）。
- 変換は「universal（V2 + V3）」形式であり、元のフィールドを残したまま新しい権限ルールを追加します。V2 に戻して使う場合も設定は機能します。
- 変換後は `/upgrade-agent diagnostics` で警告を確認し、`regex-*` 系の近似変換は意図どおりか目視で確認してください。

---

## 関連リンク

- [09_v3/ Kiro CLI v3（Early Access）概要](../09_v3/README.md) — 4 本柱・Breaking changes・Known gaps
- [33. v2.13 Introspect サブエージェント・グローバル hooks](33_v213IntrospectGlobalHooks.md) — V3 の直前の追加機能
- [30. v2.8 / V3 プレビュー](30_v28V3Preview.md) — V3 Early Access の入口（v2.8.0）
- [変更履歴 v2.14.0](../02_update/01_changelog.md)
- [Upgrading agent configs（公式）](https://kiro.dev/docs/cli/v3/upgrade-agent/)
- [Agent config（公式 V3）](https://kiro.dev/docs/cli/v3/agent-config/) ／ [Permissions（公式 V3）](https://kiro.dev/docs/cli/v3/permissions/)
- [公式 Changelog v2.14](https://kiro.dev/changelog/cli/2-14/)

---

**最終更新**: 2026-07-25  
**対象バージョン**: Kiro CLI v2.14.0+（V3 は Early Access）
