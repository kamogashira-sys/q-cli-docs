[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.27 新機能

# 46. v2.27 新機能 — Workflows の委譲設定・Steering のライブコンテキスト・保存済みプロンプトのコマンド化

## 概要

Kiro CLI **v2.27.0**（2026-10-01）と **v2.27.1**（2026-10-02）では、V3 で Workflows 有効時の委譲方法を選べるようになり、Steering がファイルやフォルダの内容をその場で取り込めるようになり、V3 で保存済みプロンプトがスラッシュコマンドになりました。

- **v2.27.0**: [V3] Workflows: sub-agent tool、Steering の `#[[file:...]]`・`#[[folder:...]]`、[V3] 保存済みプロンプトのスラッシュコマンド化、⚠️ [V3] `todo_list` ツールの廃止、🔒 `~/.kiro` の所有者限定アクセス
- **v2.27.1**: [V3] `/tangent merge`、モデルフォールバック、⚠️ 非対話実行の終了コード変更、[V3] 非対話実行の hooks・knowledge・code intelligence 対応、`--no-interactive` の Workflows の完了までの接続維持

> v2.27.1 は公式 [Changelog v2.27](https://kiro.dev/changelog/cli/2-27/#patch-2-27-1) の Patches 節（2026-10-02）に掲載されています。本ページの v2.27.1 の内容は、この Patches 節（14 項目）を出典とし、公式 [Exit codes](https://kiro.dev/docs/reference/exit-codes/)・[Slash commands](https://kiro.dev/docs/reference/slash-commands/)・[Headless mode](https://kiro.dev/docs/cli/headless/) で確認できた範囲を補っています。CLI 内蔵 changelog（`kiro-cli version --changelog=2.27.1`。18 項目）とは件数と分類が異なります（→ [変更履歴の v2.27.1 の注記](../02_update/01_changelog.md#v2271-cli2026-10-02)）。

## [V3] Workflows: sub-agent tool

Workflows（v2.26.0、→ [45. v2.26 新機能](45_v226NewFeatures.md)）を有効にすると、`/settings features` の Workflows トグルのすぐ下に **Workflows: sub-agent tool** が表示されます。

| 設定 | メインチャットの委譲 |
|------|-------------------|
| on（既定） | サブエージェントへ直接（`invoke_sub_agent`）、または Workflows 経由（`run_workflow`） |
| off | Workflows 経由（`run_workflow`）のみ。1 つのカスタムエージェントをバックグラウンドで動かすには `agent://<name>` を指定する |

> ⚠ **v2.28.0 での変更**: `/settings` > Features の **Workflows: sub-agent tool** の行は v2.28.0 で削除され、保存済みの値は動作に影響しなくなりました。Workflows が有効な V3 チャットは常に Workflows で委譲します。詳細と公式ドキュメント間の食い違いは [47. v2.28 新機能](47_v228NewFeatures.md) を参照してください。さらに、v2.33.1 で、Workflows を有効にしても Workflow は依頼したときだけ開始する動作になり、v2.34.0 で **Workflow use** により起動の方針を選べるようになりました（→ [53. v2.34 新機能](53_v234NewFeatures.md)）。以下は v2.27.0 時点の説明です。

off にしても、Workflow のステップ内のエージェントは、エージェント設定が許可していればサブエージェントを使えます。選択は `chat.enableMainAgentSubagentTool` として保存され、新しいセッションに適用されます（公式 [In-session settings](https://kiro.dev/docs/cli/chat/settings/#settings-features)・[Workflows](https://kiro.dev/docs/workflows/)）。

```bash
# メインチャットの委譲を Workflows 経由に限定する
kiro-cli settings chat.enableMainAgentSubagentTool false
```

公式 Workflows は、この設定が CLI V3 のものであり、他のクライアントは Workflows 有効時にメインセッションの委譲を Workflows 経由で行うと説明しています。

## Steering のライブコンテキスト — `#[[file:...]]`・`#[[folder:...]]`

Steering ファイルの中から、ワークスペースのファイルを参照して内容を最新に保てます。

```markdown
# ファイル全体（全サーフェス）
#[[file:<relative_file_name>]]

# 1 行、または両端を含む行範囲（CLI V3）
#[[file:<relative_file_name>:<line>]]
#[[file:<relative_file_name>:<start>-<end>]]

# 1 階層のフォルダ一覧（CLI V3）
#[[folder:<relative_folder_name>]]
```

公式 [Steering — File references](https://kiro.dev/docs/steering/#file-references) の例:

| 用途 | 書き方 |
|------|-------|
| API 仕様（全サーフェス） | `#[[file:api/openapi.yaml]]` |
| ルールの一部（CLI V3） | `#[[file:docs/api-guidelines.md:12-28]]` |
| 設定ディレクトリ（CLI V3） | `#[[folder:config]]` |

CLI V3 での動作は次のとおりです。

- 参照先は Steering 文書の読み込み時に展開される
- 相対パスの基準は、ワークスペースの Steering ならワークスペースのルート、グローバルの Steering なら `~/.kiro/steering/`、`AGENTS.md` ならそのファイルがあるフォルダ
- 参照はセッションのファイル読み取り権限と ignore ルールに従う
- 参照を解決できない場合、文書を黙って落とさず、未解決の参照であることを示すマーカーを Steering の内容に残す

Steering 全体は [23. Steering](23_Steering.md) を参照してください。チャット入力の `@ファイル` 参照（[24. ファイル参照](24_FileReferences.md)）とは別の仕組みです。

## [V3] 保存済みプロンプトをスラッシュコマンドとして実行

V3 では、ワークスペース・グローバル・MCP のプロンプトがスラッシュコマンドの補完に表示されます。`/` を入力して選ぶか、直接実行します。

```text
/prompt-name [arguments]
```

公式 [Manage prompts](https://kiro.dev/docs/cli/chat/manage-prompts/) によると、補完にはプロンプトの引数のヒントが表示され、Kiro はファイルテンプレートを展開するか MCP プロンプトの内容を取得してから、展開後のテキストをモデルへ送ります。V3 以外の CLI エンジンは引き続き `@prompt-name` 形式に対応しています。

| 保存場所 | 範囲 | 優先度 |
|---------|------|-------|
| `project/.kiro/prompts/` | 現在のプロジェクト | 最高 |
| `~/.kiro/prompts/` | すべてのプロジェクト | 中 |
| MCP サーバー | サーバーの設定による | 最低 |

V3 のファイルプロンプトでは、位置引数を `${1}`〜`${10}`、すべての引数を `$ARGUMENTS` または `${@}` で埋め込めます。

```text
/analyze "performance issue" "detailed"
```

## ⚠️ [V3] `todo_list` ツールの廃止

V3 は `todo_list` ツールを提供しなくなり、V3 では `chat.enableTodoList` は効果を持ちません。V2 の `todo` ツールと `/todos` コマンドの扱いは公式 changelog に記載がなく、本サイトの [組み込みツールリファレンス](../04_reference/04_built-in-tools.md) と [スラッシュコマンドリファレンス](../04_reference/02_slash-commands.md) の V2 向けの記述はそのまま残しています。

## その他の変更（v2.27.0）

| 種類 | 内容 |
|------|------|
| 🔒 ローカル状態のパーミッション | `~/.kiro` の状態と過去のセッションデータを所有者のみアクセス可能にした。CLI 内蔵 changelog は、対象にセッション transcript・ログ・プロンプト履歴・設定・エージェント・プロンプトが含まれ、以前のリリースで作られたファイルにも適用されると説明している |
| 🔒 Registry モードの MCP | 同名のローカル MCP エントリがあっても、registry サーバー自身のコマンドまたは URL を使い、サポートされるローカルの上書きだけを保つ |
| Output style の場所 | V3 の Output style（v2.25.0）が `/settings display` 配下へ移動（→ [44. v2.25 新機能](44_v225NewFeatures.md)） |
| 差分に絞ったファイル表示 | フル TUI の write カードが変更行と前後の文脈だけを表示する（既定で最大 40 行。`Ctrl+O` または `chat.autoExpandToolOutput` で全体） |
| `--effort` | 非対話実行にも適用される |
| `kiro-cli agent list` | V3 形式のエージェントも表示する |
| Workflow ステップの回復 | 接続失敗をその場で最大 24 時間再試行してから一時停止する |

## v2.27.1 の要点

### [V3] `/tangent merge [dest]`

tangent で得た結果を、親セッションまたは名前を指定したセッションへ取り込みます。tangent 自体は [35. v2.16 Tangent](35_v216Tangent.md) を参照してください。公式 [Slash commands](https://kiro.dev/docs/reference/slash-commands/#tangent)（公式更新日 2026-10-20）と公式 [Tangent](https://kiro.dev/docs/cli/v3/tangent/#merging-a-tangent-back)（公式更新日 2026-10-10）に、宛先（親・`root`・名前指定）と、取り込まれるのが要約であり元の tangent は残ることが記載されています。

### モデルフォールバック — `/model fallback`

**V1・V2 エンジン**で、モデルがターンを拒否した場合、設定済みのフォールバックモデルまたはサービスが提供するフォールバックモデルで再試行します。バックエンドが現在のモデルを利用不可とした場合は、設定済みのフォールバックモデルでのみ再試行します。確認・変更は `/model fallback` で行います（公式 [Changelog v2.27 の Patches 節](https://kiro.dev/changelog/cli/2-27/#patch-2-27-1)）。公式 [Slash commands](https://kiro.dev/docs/reference/slash-commands/#model)（公式更新日 2026-10-20）の `/model` の項は、`/model fallback [<model-id> | clear]` を V1・V2 に適用すると説明し、V3 の端末 UI ではフォールバックが transcript に通知として表示されると説明しています。

> CLI 内蔵 changelog（`kiro-cli version --changelog=2.27.1`）は、この項目を「拒否された、または容量超過のターンを既定で別のモデルで再試行する」と記載しています。公式 Changelog の Patches 節は上記のとおり V1・V2 エンジンと、設定済みまたはサービス提供のフォールバックモデルを挙げており、本ページは公式の記述を採用しています。

### ⚠️ 非対話実行の終了コード

| 状況 | v2.27.1 の動作 | 以前の動作 |
|------|--------------|----------|
| `--agent`（または V3 の `chat.defaultAgent`）で指定したエージェントが利用できない | **exit 4** で終了 | 既定エージェントで回答 |
| エージェントが利用できない以外の理由で `--agent` を適用できない | **exit 1** で終了 | 警告して回答 |

CI などで終了コードを分岐している場合は確認してください。公式 [Exit codes](https://kiro.dev/docs/reference/exit-codes/)（公式更新日 2026-10-05）は、終了コード 4 を「Requested Agent Not Found」として掲載し、非対話実行（`--no-interactive`、V2 または V3）が対象であること、名前を指定しない実行（`--agent` なしの再開を含む）は対象外であること、`--trust-all-tools` に関係なく適用されることを説明しています（→ [15. Exit Codes](15_ExitCodes.md)）。

### [V3] 非対話実行の拡張

- 非対話実行で hooks・knowledge・code intelligence に対応
- `--no-interactive` の Workflows が完了まで接続を維持する。待機の上限（既定 6 時間）は環境変数 `KIRO_HEADLESS_WORKFLOW_TIMEOUT_SECS` で短くできる。公式 [Headless mode](https://kiro.dev/docs/cli/headless/)（公式更新日 2026-10-20）は、この変数を「非対話の V3 実行が実行中の Workflow の完了を待つ秒数。既定 21600（6 時間）。無効な値・ゼロ・上限を超える値は既定値にフォールバックする」と説明しています

修正項目の完全な一覧は [変更履歴の v2.27.1・v2.27.0](../02_update/01_changelog.md) を正とします。

## 関連リンク

### 本サイト

- [45. v2.26 新機能](45_v226NewFeatures.md)
- [23. Steering](23_Steering.md)
- [35. v2.16 Tangent](35_v216Tangent.md)
- [15. Exit Codes](15_ExitCodes.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [Settings リファレンス](../04_reference/01_settings.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.27](https://kiro.dev/changelog/cli/2-27/)
- [In-session settings — `/settings features`](https://kiro.dev/docs/cli/chat/settings/#settings-features)
- [Workflows](https://kiro.dev/docs/workflows/)
- [Steering — File references](https://kiro.dev/docs/steering/#file-references)
- [Manage prompts](https://kiro.dev/docs/cli/chat/manage-prompts/)
- [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)
- [Exit codes](https://kiro.dev/docs/reference/exit-codes/)
- [Changelog v2.27 の Patches 節（v2.27.1）](https://kiro.dev/changelog/cli/2-27/#patch-2-27-1)
- [Slash commands](https://kiro.dev/docs/reference/slash-commands/)・[Headless mode](https://kiro.dev/docs/cli/headless/)
- `kiro-cli version --changelog=2.27.0`（v2.27.1 は実機 2.33.0 の内蔵 changelog に含まれません）

**最終更新**: 2026-10-25
**対象バージョン**: Kiro CLI v2.27.0+（Workflows・保存済みプロンプトのコマンド化・`/tangent merge` は V3 Early Access）
