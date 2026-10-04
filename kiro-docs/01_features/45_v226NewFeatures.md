[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.26 新機能

# 45. v2.26 新機能 — Workflows・Classic の非推奨化・V3 の承認チェック強化

## 概要

Kiro CLI **v2.26.0** と **v2.26.1**（いずれも 2026-09-30）では、V3 で再利用可能な複数ステップの **Workflows** をオプトインで使えるようになり、⚠️ **Classic インターフェースの起動時に非推奨の通知**が出るようになりました。V3 はファイル・ツール・shell の承認チェックを厳格化しています。

- **v2.26.0**: [V3] Workflows、⚠️ Classic の非推奨通知、V3 の承認チェック強化 4 点
- **v2.26.1**: [V3] OS の証明書ストアを既定で信頼、V2 ACP の `stopReason: refusal`、`--model` が V2 の `--no-interactive` に適用、Herdr でのローカル V3 会話の復元

## [V3] Workflows

Workflow は、エージェントのステップ・順次実行・ループ・並列分岐からなるグラフで、Kiro のランタイムが計画どおりに実行します。公式 [Workflows](https://kiro.dev/docs/workflows/) によると、各ステップは新しいコンテキストを持つ専用のセッションで実行され、Workflow はバックグラウンドで進むため、その間もメインの会話を続けられます。

### 有効化

1. `/settings` を実行する
2. **Features** を選ぶ
3. **Workflows** を有効にする
4. Kiro CLI を終了して再起動する（Workflow のコマンドはプロセスの起動時に決まる）

```bash
# 設定キー（公式 Settings リファレンスに掲載）
kiro-cli settings chat.enableWorkflows true
```

**Workflows** が表示されない場合は、そのアカウントではまだ利用できません（公式）。実機 2.27.1 の `chat.enableWorkflows` の説明は「Enable workflows feature when available in the KAS engine」で、V3（KAS）エンジンの機能です。

### 使い方

望む結果を伝えて Kiro に Workflow を作らせるか、`/workflow run` でレシピを起動します。

```text
# Workflow の履歴を開いて実行を選ぶ
/workflow

# ピッカーからレシピを起動する
/workflow run

# 名前付きレシピを入力付きで起動する（公式 Slash commands の例）
/workflow run investigate --brief "Trace timeout configuration" --report_path /path/to/report.md
```

公式 [Slash commands](https://kiro.dev/docs/reference/slash-commands/) の `/workflow` サブコマンドは次のとおりです。

| サブコマンド | 目的 |
|------------|------|
| `run [recipe] [inputs]` | 同梱・同期済み・ユーザー・プロジェクトのレシピを選んで起動 |
| `new <description>` | 目標の説明から再利用可能なレシピを作成 |
| `list` | 既知の実行を一覧 |
| `status <workflowId>` | 実行の現在の状態を表示 |
| `pause <workflowId>` | 次のノード境界での一時停止を要求 |
| `resume <workflowId>` | 一時停止した実行を再開 |
| `cancel <workflowId>` | 実行をすぐ停止（ファイルの変更は残る） |
| `retry <workflowId> [nodeId]` | 失敗・中断した作業を再試行（完了した実行には使えない） |

Workflow のモニター内では、`p` で一時停止、状態に応じて `r` で再開または再試行、`s` で選択中の一時停止ステップへの応答、`Ctrl+X` で停止します。

公式は、Kiro に同梱される 3 つのレシピとして `investigate`（読み取り専用の調査）・`feature-pipeline`（段階的な機能開発）・`publish-pr`（プルリクエストの作成とレビュー対応）を挙げています。レシピはワークスペースの `.kiro/workflows/` などに置けます。

> ⚠️ 公式は、Workflow は複数のエージェントを調整しレビューを繰り返すため、単一のセッションより多くのトークンを使うと説明しています。

### その後の変更

| 版 | 変更 |
|----|------|
| v2.27.0 | **Workflows: sub-agent tool** 設定（メインチャットの委譲方法の選択）、ステップの接続失敗を最大 24 時間再試行（→ [46. v2.27 新機能](46_v227NewFeatures.md)） |
| v2.27.1 | `--no-interactive` 実行で Workflows が完了まで接続を維持（`KIRO_HEADLESS_WORKFLOW_TIMEOUT_SECS`）（CLI 内蔵 changelog のみで確認） |

## ⚠️ Classic インターフェースの非推奨通知

Classic セッションの起動時に非推奨の通知が表示されるようになりました。通知は、Classic を選んだ要因（フラグ・環境変数・保存済み設定）を示し、ターミナル UI へ切り替える方法を案内します。

公式 [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/#using-the-classic-interface) は、Classic インターフェースは非推奨であり、ターミナル UI へ戻すには次のいずれかを行ってから Kiro CLI を再起動するよう説明しています。

| Classic を選んだ要因 | 戻し方 |
|--------------------|-------|
| フラグ | コマンドから `--classic` を外す |
| 環境変数 | `KIRO_CHAT_UI` を unset する |
| 保存済み設定 | `kiro-cli settings chat.ui "tui"` を実行する |

```bash
# 保存済み設定をターミナル UI に戻す
kiro-cli settings chat.ui "tui"
```

Classic とターミナル UI の違いは [18. Terminal UI](18_TerminalUI.md) を参照してください。

## V3 の承認チェック強化（v2.26.0）

| 強化点 | 内容 |
|-------|------|
| Hook・LSP の書き込みをファイル単位で承認 | Hook ファイルの書き込み前と、リネーム・フォーマット操作で変更する各ファイルの変更前に承認を求める |
| MCP ツールの承認を最新に保つ | 未信頼のワークスペースでは、MCP ツールが呼び出しと再試行のたびに承認を求める。すべての MCP 呼び出しは実行前に承認がまだ有効かを確認する |
| 未信頼ワークスペースでの shell 承認 | 保存済みまたは広い許可があっても、shell コマンドが起動のたびに承認を求める |
| ツール実行直前の承認再確認 | 動作の直前に各承認を再確認し、待機中に変更・取り消された承認は適用しない |

あわせて、macOS と Linux で同じファイルにシンボリックリンクや別表記のパスでアクセスした場合にも、V3 のファイル権限ルールが適用されるよう修正されました。

## v2.26.1 の要点

| 変更 | 内容 |
|------|------|
| [V3] 企業プロキシの TLS インスペクション | V3 は既定で OS の証明書ストアを信頼する。企業プロキシの証明書を OS のストアに導入していれば "No model available" と表示されない。`NODE_USE_SYSTEM_CA` を明示した場合（`0` を含む）はその値が優先される |
| V2 ACP | 最終応答がコンテンツフィルタの対象になったターンで、`end_turn` ではなく `stopReason: refusal` を返す（→ [13. ACP](13_ACP.md)） |
| `--model` | V2 の `--no-interactive` 実行に適用される。空でない値を明示すると、エージェントのモデルと再開したセッションの保存済みモデルを上書きする |
| `--resume-id` | ターミナル UI でローカルのセッションに一致しないとき、代わりの会話を始めない。クラウドセッションが有効ならクラウドのセッションストアも確認する |
| Herdr | ターミナルペインマネージャー Herdr が、サーバー再起動後に `kiro-cli chat --agent-engine=v3 --resume-id <session-id>` で既存のローカル V3 会話を復元できる |

修正項目の完全な一覧は [変更履歴の v2.26.1・v2.26.0](../02_update/01_changelog.md) を正とします。

## 関連リンク

### 本サイト

- [44. v2.25 新機能](44_v225NewFeatures.md)
- [46. v2.27 新機能](46_v227NewFeatures.md)
- [18. Terminal UI](18_TerminalUI.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [Settings リファレンス](../04_reference/01_settings.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.26](https://kiro.dev/changelog/cli/2-26/)
- [Workflows](https://kiro.dev/docs/workflows/)
- [Slash commands — `/workflow`](https://kiro.dev/docs/reference/slash-commands/)
- [Terminal UI — Using the classic interface](https://kiro.dev/docs/cli/terminal-ui/#using-the-classic-interface)

**最終更新**: 2026-10-04
**対象バージョン**: Kiro CLI v2.26.0+（Workflows・承認チェック強化は V3 Early Access）
