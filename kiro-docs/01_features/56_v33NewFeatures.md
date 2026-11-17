[ホーム](../README.md) > [機能詳細ガイド](README.md) > v3.1〜v3.3 新機能

# 56. v3.1〜v3.3 新機能 — compaction の Hook・セッションのクレジット・Output details・図の全画面ビューア・`/copy N`

## 概要

Kiro CLI の **v3.1.0**（2026-11-05）から **v3.3.0**（2026-11-12）までの 3 つの系列と、その間のパッチ版 v3.2.1 をまとめた文書です。いずれも V3 が既定になった v3.0.0（→ [55. v3.0 新機能](55_v30NewFeatures.md)）の後の版で、公式の記述は V3 を対象としています（V2 エージェントハーネスにも関係する項目は、本文で示します）。

- **v3.1.0**: `PreCompact`・`PostCompact` Hook、セッションのクレジット表示、`KIRO_DEFAULT_SETTINGS`、Session recap、サブエージェントによる親の Memory の読み取り、通知の 1 行化
- **v3.2.0**: Mermaid 図の全画面ビューア（`/diagram`）、クライアント登録なしの MCP サインイン、ワークフローのループの上限での選択
- **v3.2.1**: Output details（ツール呼び出しの詳細の量を選ぶ）、ツール呼び出しの見た目の統一、サインインの修正
- **v3.3.0**: `/copy N`・`/copy last N`、自動 compaction の開始点の設定、サブエージェントのタスクの表示、アップグレード時の許可ルールの縮小

> **出典**: 公式 Changelog [v3.1](https://kiro.dev/changelog/cli/3-1/)・[v3.2](https://kiro.dev/changelog/cli/3-2/)・[v3.2.1](https://kiro.dev/changelog/cli/3-2-1/)・[v3.3](https://kiro.dev/changelog/cli/3-3/)（表示日は各節のとおり）と、公式の [Hook types](https://kiro.dev/docs/hooks/types/)・[Settings](https://kiro.dev/docs/reference/settings/)・[Slash commands](https://kiro.dev/docs/reference/slash-commands/)・[Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)・[In-session settings](https://kiro.dev/docs/cli/chat/settings/)・[MCP configuration](https://kiro.dev/docs/mcp/configuration/)・[Memory](https://kiro.dev/docs/memory/) です。v3.2.1 と v3.3.0 は、CLI 内蔵 changelog（実機 3.3.0）とも突き合わせました。実機は v3.2.0 以前の内蔵 changelog を保持しないため、それ以前は公式のみが出典です。

- **v3.3.0**: 17 項目（公式の主要節 2／Improvements 4／Fixes 11）
- **v3.2.1**: 17 項目（公式の専用ページの Improvements 3／Fixes 14）
- **v3.2.0**: 21 項目（公式の主要節 2／Improvements 4／Fixes 15）
- **v3.1.0**: 53 項目（公式の主要節 2／Improvements 10／Fixes 41）

各項目の一覧は [変更履歴](../02_update/01_changelog.md) にあります。以下は、機能として説明が要るものです。

## compaction の前後で Hook を動かす（v3.1.0）

CLI V3 のセッションで、会話の compaction の前後に Hook を動かせます（公式 [Hook types](https://kiro.dev/docs/hooks/types/)、Page updated: 2026-11-12）。compaction は、`/compact` を実行したとき、自動の要約が始まったとき、コンテキストの溢れから回復するとき、別のモデルへ引き継ぐときに動きます。

| トリガー | 動くタイミング | 動作 |
|---------|--------------|------|
| `PreCompact` | compaction の前 | 終了コード 0 は compaction を続け、CLI V3 では標準出力（3,000 文字まで）をエージェントのコンテキストに加える。終了コード 2 は compaction を取り消し、会話はそのまま残る |
| `PostCompact` | 要約が古い履歴に置き換わったあと | 標準入力の JSON に `summary`（要約のテキスト 3,000 文字まで）と `summary_path`（要約全体のファイル）が入る。Hook は compaction を取り消せず、要約も変えられない。トリガーはマッチャーを取らない |

用途の例は、公式が挙げるとおり、古い履歴が要約される前に作業のスナップショットを保存する、Kiro の外で追跡しているタスクが開いている間は compaction を拒否する、要約を保管して確認する、です。Hook の全体は [22. Hooks](22_Hooks.md) を参照してください。

## セッションのクレジットを見る（v3.1.0）

`/usage` がセッションのこれまでの使用クレジットを示します。`/settings display` の任意の **Session credits** セグメントをオンにすると、ステータス行にその合計を出し続けます（既定は非表示）。ワークフローモニターでは、各ステップ行にそのステップの使用クレジットが出ます。フッターの合計は、セッションを開き直してもリセットされません（v3.1.0 の修正）。

## 環境の既定設定 `KIRO_DEFAULT_SETTINGS`（v3.1.0）

macOS と Linux で、環境変数 `KIRO_DEFAULT_SETTINGS` に既定設定のファイルの絶対パスを設定すると、その値が**最も低い設定の層**になり、利用者のグローバルまたはワークスペースの `cli.json` の値が上書きします（公式 [Settings](https://kiro.dev/docs/reference/settings/)、Page updated: 2026-11-12）。

- ファイルは root 所有の通常ファイルで、グループとその他に書き込み権がなく、1 MiB 以下の JSON オブジェクトであること
- 相対パスや、検査に通らないファイルは、警告を 1 回示して無視される
- `kiro-cli settings` と `/settings` は、値の出所としてこのファイルを示す。`kiro-cli settings` はこのファイルの値を設定・削除できない

## Session recap（v3.1.0）

`/settings` > Features の Session recap、または `chat.enableSessionRecap`（既定はオフ）で、プロンプトの上に短い要約を示します。要約ごとに追加のモデル呼び出しが発生し、クレジットを使います。設定を変えたら、新しいセッションを始めます。

> **公式と実機の食い違い**: 公式の Changelog は「数秒のアイドルのあと」、公式の Settings は「各ターンの完了後に追加のモデル呼び出しを 1 回行い、フルのターミナル UI が 3 アイドル秒後に表示する」と書いています。実機 `kiro-cli 3.3.0` の `kiro-cli settings list --all` は「when you return to the terminal after 3 minutes away」と説明しています。どちらが正しいかは、実機で要約の表示を試していないため**未確認**です。

## サブエージェントが親の Memory を読む（v3.1.0）

CLI 3.1.0 以降、サブエージェントは、自分を呼び出したエージェントの memories を読めます。追加・変更・削除はできません（公式 [Memory](https://kiro.dev/docs/memory/)、Page updated: 2026-11-10）。Memory の全体は [48. v2.29 新機能](48_v229NewFeatures.md) を参照してください。

## そのほかの v3.1.0 の改善

- **通知の 1 行化**: 通知が緊急度の高い順に 1 行に並び、`+N waiting` の件数を示す。警告とエラーは、キー操作で閉じるまで残る
- **エージェントのリソースの上限**: `file://` リソースは 32 ファイル、100,000 文字までで、大きなファイルは切り詰めるか読み飛ばす
- **`web_fetch` が Markdown を要求**: ドキュメントのコードブロックとリンクが残る
- **MCP の状態を所有者のみに**: macOS と Linux で、リモート MCP の登録・認証情報のファイルは所有者のみが読み書きでき、新しい認証情報のフォルダは所有者のみの権限で作られる
- **サインインのトークンを得られないとき**: プロンプトをセッションに保存せず、サインインの案内を表示する
- **V2 エージェントハーネスの承認**: `GIT_DIR`・`GIT_WORK_TREE` を接頭辞に付けた `git` コマンドが、実行前に承認を求める

## Mermaid 図の全画面ビューア（v3.2.0）

端末に収まらない幅広い Mermaid 図は、ソースと通知、プロンプトの上の入口を表示します。`Ctrl+]` または `/diagram` で、最新の幅広い図を全幅の専用画面で開きます（公式 [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)、Page updated: 2026-11-16）。矢印キーとマウスホイールで動かし、`Tab` で古い図へ進み、`Esc` でチャットに戻ります（下書きは保たれます）。キーは `chat.keybindings.viewDiagram`（既定 `ctrl+]`）で変えます。

```bash
kiro-cli settings chat.keybindings.viewDiagram "ctrl+shift+d"
```

Mermaid 図の描画そのものは [18. Terminal UI](18_TerminalUI.md) と [54. v2.35〜v2.37 新機能](54_v237NewFeatures.md) を参照してください。

## クライアント登録なしの MCP サインイン（v3.2.0）

Client ID Metadata Documents（CIMD）に対応し、動的クライアント登録（DCR）を提供しない認可サーバー（例: Tableau のホスト型 MCP）へ、Kiro が自身のホスト型のクライアントメタデータドキュメントでサインインします。設定に `oauth` ブロックは要りません（公式 [MCP configuration](https://kiro.dev/docs/mcp/configuration/)）。

- DCR を提供するサーバーは、従来どおり DCR を使う
- 設定した `clientId` と `clientMetadataUrl` は、引き続き優先される
- 公式は、`clientMetadataUrl` を使うときは `oauth.redirectUri` を固定するよう警告している。Kiro は既定でランダムなループバックのポートを割り当てるため、固定しないとコールバックが拒否される

MCP の OAuth は [32. MCP OAuth Management](32_MCPOAuthManagement.md) を参照してください。

## ワークフローのループの上限・autonomous モード（v3.2.0）

- **ループの上限**: 反復回数を使い切って一時停止したループが、ワークフローモニターと一時停止した行の下に、**あと 1 回反復する**か、**ループを完了にして実行を続ける**かの選択肢を示します
- **autonomous モード**: autonomous モードでワークフローを頼むと、依頼を渡さずに、そのモードではワークフローが動かないと伝えます（→ [50. v2.31 新機能](50_v231NewFeatures.md)）
- 同じ版の修正として、ワークフローの実行はチェックアウト中のブランチに着地します（v3.1.0）。Workflows がオフのときに `/goal` などを打つと、オンにする方法を案内します（v3.2.1）

## Output details とツール呼び出しの見た目（v3.2.1）

`/settings` の **Output details**、または `/settings output-details` で、ツール呼び出しの詳細の量を選びます（公式 [In-session settings](https://kiro.dev/docs/cli/chat/settings/)）。

| 行 | 内容 |
|----|------|
| Density preset | `collapsed`（ツール呼び出しごとに 1 行: 題名・時間・状態）、`lean`（引数をインライン、推論なし）、`default`、`full`（エージェントが見るすべて。出力フィルタをすべてオンにし、切り詰めなし）、または **custom**（行ごとに設定） |
| Tool calls | ツールの引数を、オフ・題名・インライン・ブロックから選ぶ。エージェントの推論と経過時間のオン・オフ |
| Subagent | サブエージェントのステップ、ステップの指示、ステップの役割ラベル、完全な出力。V2 のセッションでは **Show response summary** も出る（V3 は常に応答を表示する） |

- **thinking の表示**（`chat.showThinking`）は、`/settings display` からここへ移りました。コマンドラインの `kiro-cli settings chat.showThinking <mode>` は、次のセッションの開始から適用されます。Output details での変更は、現在のセッションに適用されます
- `/settings verbosity` は同じメニューを開き、プリセットが有効なとき、`/verbosity` は密度の選択を開きます
- **ツール呼び出しの見た目**: shell・検索・汎用のツール出力がツール呼び出しの隅にぶら下がり、`read` は返したファイルの行を示し、完了したツール呼び出しが 2 件以上続くと 1 つの要約行にたたまれて `Ctrl+O` で展開できます。承認待ちのファイル書き込みのカードは差分の全体を示し、完了した検索は結果の件数だけをスクロールバックに残します（公式 [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)）

そのほか v3.2.1 では、グラフィカルなセッションのない Linux で、ターミナルの `kiro-cli login` がデバイスフロー（コードと URL の表示）を使い、`kiro-cli login --license pro` に `--identity-provider` と `--region` を付けても「No region was given」で失敗しなくなりました。

## `/copy N`・`/copy last N`（v3.3.0）

公式 [Slash commands の `/copy`](https://kiro.dev/docs/reference/slash-commands/#copy)（Page updated: 2026-11-16）の説明は次のとおりです。

```text
> /copy          最新の回答
> /copy 2        2 番目に新しい回答（`/copy` と `/copy 1` は同じ）
> /copy last 3   直近 3 件のメッセージ（古い順）
```

- `/copy last N` は、プロンプトも回答も数える。プロンプトには `**You:**`、回答には `**Kiro:**` のラベルが付く
- ツール呼び出しをはさんだ 1 つの回答は 1 件で、途中の steer は別の 1 件
- `N` は正の整数。会話の件数より大きいときは、件数を知らせる
- 会話の全体は `/transcript` を使う

## 自動 compaction の開始点（v3.3.0）

V3 のセッションで `/settings` の **Compaction** を開くと、現在のセッションの閾値と、グローバルの既定を設定する編集画面が出ます（公式 [In-session settings](https://kiro.dev/docs/cli/chat/settings/)）。

- 値は、自動 compaction を始めるコンテキスト使用率（%）で、小数点以下 2 桁までの数
- `d` を押すと、エージェントハーネスの既定に従う。実機 3.3.0 の `kiro-cli settings list --all` は、範囲を [0, 100]、現在の既定を 80 と表示し、「requires KAS engine」と書く
- 設定キーは `compaction.autoCompactionThreshold`。次に開始または読み込むセッションから適用され、ワークスペースの `cli.json` で上書きできる
- 同じ画面で、自動 compaction のオン・オフを切り替える

```bash
kiro-cli settings compaction.autoCompactionThreshold 70
```

## そのほかの v3.3.0 の改善

- **サブエージェントのタスクの表示**: サブエージェントに渡されたタスクが、インラインのパネルと `Ctrl+G` のモニターで読め、モニターは最終回答も示す
- **`/model` の操作**: `Tab`・`Shift+Tab` で、モデル一覧とモデル設定のパネルを行き来する。一覧の先頭で `Up` を押すと検索・並べ替え・編集の操作に移る
- **許可ルールが広がらない（セキュリティ）**: V2 エージェントを V3 へアップグレードするとき、どの glob にも正確に対応しない `allowedCommands` と `web_fetch.trusted` の正規表現は、広い glob にせず、`unconvertible-pattern` の警告とともに削除する。V3 は、正規表現が許可していた操作の前に承認を尋ねる。書き直し方は `kiro-cli agent upgrade` と `/upgrade-agent diagnostics` に出る（→ [34. /upgrade-agent](34_v214UpgradeAgent.md)）
- **停止したワークフローセッション**: エージェントの再起動後に、メッセージを再送せずに再読み込みされる

ヘッドレスの修正として、V3 の `--no-interactive` で `--trust-tools` が V2 のツール名・`@server`・`@server/tool`・`@builtin`・`*`／`?` のパターンを受け付け（V3 のツール ID に加えて）、`--resume` が会話のある最新のセッションを開きます。

## 実機での確認（kiro-cli 3.3.0・Linux）

- `kiro-cli settings list --all` に `chat.enableSessionRecap`・`chat.keybindings.viewDiagram`・`compaction.autoCompactionThreshold` が表示される（説明文は上記のとおり）
- 次は実機で動作を確かめていないため**実機では未確認**: `PreCompact`・`PostCompact` Hook の動作、セッションのクレジット表示、`KIRO_DEFAULT_SETTINGS`、Session recap、`/diagram`、CIMD によるサインイン、ワークフローのループの選択肢、Output details、`/copy N`、`/settings` の Compaction

## 関連リンク

### 本サイト

- [55. v3.0 新機能](55_v30NewFeatures.md)
- [54. v2.35〜v2.37 新機能](54_v237NewFeatures.md)
- [48. v2.29 新機能（Memory）](48_v229NewFeatures.md)
- [34. /upgrade-agent](34_v214UpgradeAgent.md)
- [22. Hooks](22_Hooks.md)
- [18. Terminal UI](18_TerminalUI.md)
- [09_v3/（Kiro CLI v3）](../09_v3/README.md)
- [設定リファレンス](../04_reference/01_settings.md)
- [スラッシュコマンドリファレンス](../04_reference/02_slash-commands.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v3.3](https://kiro.dev/changelog/cli/3-3/)
- [Kiro CLI Changelog v3.2](https://kiro.dev/changelog/cli/3-2/)
- [Kiro CLI Changelog v3.2.1](https://kiro.dev/changelog/cli/3-2-1/)
- [Kiro CLI Changelog v3.1](https://kiro.dev/changelog/cli/3-1/)
- [Hook types](https://kiro.dev/docs/hooks/types/)
- [Settings リファレンス](https://kiro.dev/docs/reference/settings/)
- [Slash commands](https://kiro.dev/docs/reference/slash-commands/)
- [In-session settings](https://kiro.dev/docs/cli/chat/settings/)
- [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)
- [MCP configuration](https://kiro.dev/docs/mcp/configuration/)
- [Memory](https://kiro.dev/docs/memory/)
- `kiro-cli version --changelog=all` / `kiro-cli settings list --all`（実機 3.3.0）

**最終更新**: 2026-11-17
**対象バージョン**: Kiro CLI v3.3.0（v3.1.0〜v3.3.0 とパッチ版 v3.2.1。V3 が既定のハーネス）
