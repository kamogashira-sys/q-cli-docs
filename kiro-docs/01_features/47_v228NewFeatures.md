[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.28 新機能

# 47. v2.28 新機能 — Classic からの 3.0 切替提案・[V3] Hook のカテゴリ一致・Workflows 委譲の一貫化

## 概要

Kiro CLI **v2.28.0**（2026-10-05）では、Classic の対話セッションから 3.0（V3）へ切り替える提案が表示されるようになり、V3 の Hook がツールのカテゴリで一致できるようになりました。長い V3 セッションの安定性も改善され、⚠ V3 の Workflows 有効時の委譲は常に Workflows 経由になりました。系列ページ（`changelog/cli/2-28/`）に Patches 節はなく、v2.28 系列の版は v2.28.0 のみです。

- **機能追加**: Classic の対話セッションからの 3.0 切替提案、[V3] ツールカテゴリによる Hook の一致
- **変更**: ⚠ [V3] `Workflows: sub-agent tool` の設定行を廃止（Workflows が有効なら常に Workflows で委譲）
- **改善**: ターン途中の `/model`・`/effort`、V3 の長いセッション、中断されたツールの状態表示、Full Screen の Copy on select、Windows の V2 の MCP サーバー引数、アクティビティトレイ
- **バグ修正**: 3 件

公式 Changelog の Learn more リンクは v2.28.0 の項目にありません。本ページの「公式ドキュメントでの確認」は、各機能に関連する公式ドキュメントの本文を取得して確認できた範囲です。確認できなかった点は「未確認」と書いています。

## Classic の対話セッションから 3.0 へ切り替える

公式 Changelog（v2.28.0）によると、3.0 を実行できるホストで対話型の Classic セッションを開始すると、Kiro が 3.0 への切り替えを提案します。

| 選択 | 動作 |
|------|------|
| **Switch to 3.0 and upgrade my agent configs** | 3.0 を既定として保存し、エージェント設定をアップグレードし、実行したコマンドを 3.0 で再実行する |
| 断る | 約 1 週間に 1 回、Kiro が再度案内する |

Classic インターフェースの非推奨通知（v2.26.0）は [45. v2.26 新機能](45_v226NewFeatures.md) を参照してください。

### 公式ドキュメントでの確認

- この提案そのものを説明する公式ドキュメントは見つかりませんでした。公式 [What's new in CLI V3](https://kiro.dev/docs/cli/v3/)（Page updated: 2026-10-13）は、V2 の対話チャットを開始したときの切り替え提案を記載しています。選択肢は **Switch to V3 and upgrade my configs**・**Remind me later**・**Don't ask again** の 3 つで、**Switch to V3 and upgrade my configs** は `chat.agentEngine` を `v3` として保存し、エージェント設定を今回と以後の起動でアップグレードすると説明されています。この提案は v2.30.0 で導入された起動時のプロンプトに対応します（→ [49. v2.30 新機能](49_v230NewFeatures.md)）。
- v2.28.0 の Classic 向けの提案（選択肢の名称が `3.0`）と、v2.30.0 の V2 向けの提案（選択肢の名称が `V3`）が同じ仕組みの別の表示なのか、別の提案なのかは、公式に記載がなく**未確認**です。
- `kiro-cli --v3` で V3 をいつでも試せることは、公式 [What's new in CLI V3](https://kiro.dev/docs/cli/v3/) に記載されています。
- Classic の位置づけは公式 [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/#using-the-classic-interface)（Page updated: 2026-10-20）に「Classic インターフェースは非推奨」と記載されています。

## [V3] Hook のツールカテゴリ一致

V3 セッションで、ツールの実行前後に動く Hook（`PreToolUse`・`PostToolUse`）が、内部のツール ID だけでなく、shell・read・write などのカテゴリ、または特定の MCP サーバー・ツールで一致できるようになりました（公式 Changelog v2.28.0）。

### 公式ドキュメントでの確認

公式 [Hook types](https://kiro.dev/docs/hooks/types/)（Page updated: 2026-10-10）の CLI タブは、`matcher` の書き方を次のように説明しています。

- `matcher` は、ツールのセレクターまたは正規表現を受け取る
- 正規表現のメタ文字（`\ ^ $ ( ) [ ] | +`）を含まない matcher はセレクターで、ツールの ID またはタグが一致する。`*` と `?` はワイルドカードとして ID とタグに対して働く
- タグには、カテゴリ `read`・`write`・`shell`・`web`・`subagent`・`spec`・`context`、ソースセレクター `@builtin`・`@mcp`・`@powers`、MCP ツール用の `@<server>`・`@<server>/<tool>` がある
- `execute_bash` と `execute_pwsh` は互いに一致するため、1 つのセレクターで両方の OS を扱える
- セレクターは範囲を限定しない正規表現としても評価されるため、`read` は ID に `read` を含むすべてのツールに一致する
- メタ文字を含む matcher は、ツール ID に対する正規表現としてだけ評価される。完全一致にするには `^...$` で囲む

| matcher の例（公式） | 一致するもの |
|---------------------|------------|
| `"shell"` | タグによるすべての shell ツール（`execute_bash` または `execute_pwsh`） |
| `"@mcp"` | すべての MCP ツール |
| `"@git/git_status"` | サーバーとツール名で指定した 1 つの MCP ツール |
| `"mcp_git_*"` | git MCP サーバーの内部ツール ID（ワイルドカード） |

スタンドアロンの Hook ファイル（`.kiro/hooks/*.json`）の書式は、公式 [Hooks migration](https://kiro.dev/docs/cli/v3/hooks-migration/)（Page updated: 2026-10-10）に次の例があります。

```json
{
  "version": "v1",
  "hooks": [
    {
      "name": "lint-before-read",
      "trigger": "PreToolUse",
      "matcher": "read",
      "action": { "type": "command", "command": "npm run lint" },
      "timeout": 30,
      "enabled": true
    }
  ]
}
```

同じ公式 Hook types は、「V3 は CLI 2.x のツール名を展開しない。`fs_read` と `grep` は V3 の ID でもタグでもないため、カテゴリのタグ（`read`）または V3 の ID（`read_file`、`grep_search`）を使う」と注意しています。CLI 2.x のツール名を V3 のタグへ書き換える `/upgrade-agent` の動作は、[48. v2.29 新機能](48_v229NewFeatures.md) と [34. /upgrade-agent](34_v214UpgradeAgent.md) を参照してください。Hook 全般は [22. Hooks](22_Hooks.md) を参照してください。

## ⚠ [V3] Workflows による委譲の一貫化

`/settings` > Features から **Workflows: sub-agent tool** の行が削除されました（公式 Changelog v2.28.0）。保存済みの設定値は動作を変えません。Workflows が有効な場合、V3 のチャットは常に Workflows で委譲します。同じ役割を共有する並列のサブエージェントには別々の行が表示され、それぞれを個別に確認・承認できます。

v2.27.0 で追加された設定（`chat.enableMainAgentSubagentTool`）の内容は [46. v2.27 新機能](46_v227NewFeatures.md) を参照してください。

### 公式ドキュメント間の食い違い

| 情報源 | 記述 |
|--------|------|
| 公式 Changelog v2.28.0（2026-10-05） | 行を削除。保存値は動作を変えない。Workflows が有効なら常に Workflows で委譲 |
| 実機 2.33.0 で確認（`kiro-cli settings list --all`） | `chat.enableMainAgentSubagentTool` の説明は「Legacy setting with no effect: while workflows is enabled, chat delegates only through workflows」 |
| 公式 [Workflows](https://kiro.dev/docs/workflows/)（Page updated: 2026-10-20） | CLI V3 で既定が有効の **Workflows: sub-agent tool** 設定が `invoke_sub_agent` による直接委譲を残し、オフにすると `run_workflow` 経由だけになる、と記載 |
| 公式 [In-session settings](https://kiro.dev/docs/cli/chat/settings/#settings-features)（Page updated: 2026-10-20） | **Workflows: sub-agent tool** が Workflows のトグルの直下に表示され、既定でオン、`chat.enableMainAgentSubagentTool` として保存される、と記載 |
| 公式 [Settings リファレンス](https://kiro.dev/docs/reference/settings/)（Page updated: 2026-10-15） | `chat.enableMainAgentSubagentTool` を「V3 で Workflows が有効なときの直接委譲を保つ設定（既定 `true`）」と記載 |

公式ドキュメント 3 ページは、ページ全体の更新日が v2.28.0 の公開日（2026-10-05）より新しいものの、この設定を有効なものとして記述しています。ページの更新日はそのページ全体の日付であり、この記述がいつ書かれたかを示すものではありません。公式がこの食い違いに言及している箇所は確認できませんでした。本サイトは、リリース内容の一次情報である公式 Changelog と、実機 2.33.0 の説明（いずれも設定は動作に影響しない）を採用しています。ドキュメント側の記述がどのバージョンに対応するかは**未確認**です。

## 操作性の改善

| 項目 | 内容 | 公式ドキュメントでの確認 |
|------|------|------------------------|
| ターン途中のモデル・effort の変更 | Kiro の作業中でも `/model` と `/effort` のピッカーが開く。選択は現在のターンが終わった後に適用される | 公式 Slash commands の `/model`・`/effort`（Page updated: 2026-10-20）に、作業中に開けること・適用時期の記載は確認できなかった（**未確認**） |
| V3 の長いセッション | 完了したターンをメモリに保持せず解放する。非常に長いチャットでの蓄積が減る | 公式ドキュメントに記載なし（**未確認**） |
| V3 の中断されたツールの状態表示 | ツール呼び出しへの応答がないままターンが終わった場合に、ツールが開始されなかったのか、完了したのか、結果が不明なのかを示す | 公式ドキュメントに記載なし（**未確認**） |
| Full Screen の Copy on select | `/settings` > Display > Full Screen に追加。off にすると fullscreen モードがテキスト選択を取り込まず、すでにコピーを処理している端末や tmux がその操作を担える | 公式 [Fullscreen mode](https://kiro.dev/docs/cli/fullscreen/)（Page updated: 2026-09-30）は、ドラッグでテキストをコピーする動作を説明しているが、この設定の記載はない。実機 2.33.0 で確認: 設定キー `chat.fullscreenCopyOnSelect`（boolean、既定 `true`、説明は「Copy dragged text in the fullscreen TUI; off leaves copying to the terminal」）。公式 Settings リファレンスにこのキーは掲載されていない |
| Windows での V2 の MCP サーバー引数 | Windows の V2 セッションで、`\|`・`&`・`%`・空白を含む引数が、直接解決される stdio MCP サーバーへそのまま届く | 公式ドキュメントに記載なし（**未確認**） |
| アクティビティトレイの拡張 | 展開したトレイが 6 件で止まらず、すべてのタスクを一覧する。fullscreen では一覧の高さを画面の約半分までに制限する。Lite のトレイは最大 6 件の Workflow を表示する（従来は 3 件） | 公式 [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/#activity-tray)（Page updated: 2026-10-20）は、`Ctrl+X` でタスクの進捗と待機中のメッセージを一覧できると説明しているが、件数の記載はない |

```bash
# Full Screen の Copy on select を無効にする（実機 2.33.0 で確認した設定キー）
kiro-cli settings chat.fullscreenCopyOnSelect false
```

## バグ修正（3 件）

- V2 TUI で、サブエージェントの終了後に会話が応答しなくなる問題
- 一部の端末で、エージェントモニターまたはセッションダッシュボードを離れた後に、チャット画面の位置がずれる問題
- 音声録音のヒントが、存在しない `/settings voice` を案内していた問題（ヒントは有効な `kiro-cli settings` コマンドを示す）

音声入力の機能は [37. Voice Mode](37_VoiceMode.md) を参照してください。修正項目の完全な一覧は [変更履歴の v2.28.0](../02_update/01_changelog.md) を正とします。

## 関連リンク

### 本サイト

- [46. v2.27 新機能](46_v227NewFeatures.md)
- [49. v2.30 新機能](49_v230NewFeatures.md)
- [22. Hooks](22_Hooks.md)
- [18. Terminal UI](18_TerminalUI.md)
- [45. v2.26 新機能](45_v226NewFeatures.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.28](https://kiro.dev/changelog/cli/2-28/)
- [What's new in CLI V3](https://kiro.dev/docs/cli/v3/)
- [Hook types](https://kiro.dev/docs/hooks/types/)
- [Hooks migration](https://kiro.dev/docs/cli/v3/hooks-migration/)
- [Workflows](https://kiro.dev/docs/workflows/)
- [In-session settings — `/settings features`](https://kiro.dev/docs/cli/chat/settings/#settings-features)
- [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)
- [Fullscreen mode](https://kiro.dev/docs/cli/fullscreen/)
- `kiro-cli settings list --all`（実機 2.33.0）

**最終更新**: 2026-10-21
**対象バージョン**: Kiro CLI v2.28.0+（Hook のカテゴリ一致・Workflows 委譲の一貫化は V3 Early Access）
