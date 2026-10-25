[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.34 新機能

# 53. v2.34 新機能 — [V3] MCP elicitation・Workflow の起動方針と計画の修正・Memory の削除・`/model edit`

## 概要

Kiro CLI **v2.34.0**（2026-10-23）では、[V3] のローカルセッションで、MCP ツールがフォームやリンクで利用者に入力を求められるようになりました（**MCP elicitation**）。Workflow は、計画の承認に変更案を直接入力でき、`/settings` の **Workflow use** で Kiro が Workflow を始める頻度を選べます。`/memories` から Memory を削除でき、`/model edit` で `/model` のピッカーに出すモデルを選べ、`--trust-workspace` でワークスペースの信頼確認を 1 回の起動だけ省略できます。直前の **v2.33.1**（2026-10-21）では、[V3] の Workflows が、有効にしても自動では始まらず、依頼したときだけ実行されるようになりました。

> **出典**: 公式 [Changelog v2.34](https://kiro.dev/changelog/cli/2-34/)（表示日 2026-10-23）と、公式 [Changelog v2.33.1](https://kiro.dev/changelog/cli/2-33-1/)（表示日 2026-10-21）です。CLI 内蔵 changelog（実機 `kiro-cli 2.34.0` の `kiro-cli version --changelog=2.34.0`・`--changelog=2.33.1`）も取得し、公式と項目の内容が 1 対 1 で一致することを確認しました（分類だけが異なります）。

- **v2.34.0**: 機能追加 1 件、改善 5 件、変更 4 件、セキュリティ 1 件、バグ修正 17 件（公式の主要節 1／Improvements 9／Fixes 18 に対応）
- **v2.33.1**: 変更 1 件、バグ修正 15 件（公式の Improvements 1／Fixes 15 に対応）

changelog で `[V3]` の表記がない項目のうち、公式にも V2 専用か両対応かの記載がないものは、本ページで「未確認」と示します。

## [V3] MCP elicitation（v2.34.0）

ローカルの V3 セッションで、MCP ツールが追加情報を必要とするとき、ツールは一時停止して、フォームまたはリンクを表示します。必要な情報を入力する、別のページで操作を完了する、要求を拒否する、のいずれかができ、ツールは呼び出しをやり直さずに続行します。

公式 [MCP usage の MCP elicitation](https://kiro.dev/docs/mcp/usage/#mcp-elicitation)（Page updated: 2026-10-24）の説明は次のとおりです。

- Kiro CLI は、**ローカルの V3 セッションで、バージョン 2.34 以降**、elicitation に対応する。MCP の仕様では、サーバーが実行中に追加情報を求める仕組みである（[MCP elicitation の仕様](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation)）
- **フォーム型**: ツールが要求を送ると、Kiro は実行のタイムラインにインラインのフォームを描画する。フィールドは、求められるデータの種類による

| フィールドの種類 | 描画される部品 |
|-----------------|---------------|
| Text | テキスト入力（メールや日付などの形式のヒントを含むことがある） |
| Number | 数値入力 |
| Yes/No | チェックボックス |
| Choice | 選択のドロップダウン |

- 必須のフィールドには印が付き、サーバーが既定値を渡していれば、あらかじめ入力される
- フォームを確認した後は、回答を送信する、要求を拒否する、フォームを閉じる、のいずれかができる。拒否または閉じた場合にどう進むかはサーバーが決める（代替案を示す、そのステップを省くなど）
- **URL 型**: サーバーによっては、OAuth の認可フローを完了するためなどに、外部の URL を開くよう求める。Kiro は URL と **Open** ボタンを実行のタイムラインに表示し、外部の操作が終わるとツールが続行する
- Kiro は、どのサーバーが何のデータを求めているかを常に表示する。要求はいつでも拒否できる。サーバーが、パスワードのような機密情報を elicitation で求めるべきではなく、そのような要求を見たらサーバーを信頼できるかを検討するよう、公式は注意している

MCP サーバーの設定は [MCP 関連の機能ガイド](32_MCPOAuthManagement.md)、権限は [17. Granular Tool Trust](17_GranularToolTrust.md) を参照してください。V3 のヘッドレス実行で elicitation がどう扱われるかは、公式 MCP usage に記載がなく**未確認**です（v2.34.0 の別の修正として、ヘッドレスモードは「エージェントの質問に答えず、信頼されたツールを指定しない要求を承認しない」ことが変更履歴に記載されています）。

## Workflow の起動方針と計画の修正

### v2.33.1: Workflows は依頼したときだけ開始（⚠ 動作変更）

[V3] のセッションで Workflows を有効にしても、Workflow は、利用者が明示的に依頼したときだけ実行されます。機能を有効にしただけでは始まりません。公式 [Workflows の Start from the agent](https://kiro.dev/docs/workflows/#start-from-the-agent)（Page updated: 2026-10-24）は、Kiro CLI 2.33.1 以降、Workflows を有効にしても Workflow は自動では始まらず、明示的に依頼したときだけ実行される、と説明しています。V3 のセッションでは、Kiro がどのステップも実行する前に、提案する計画を承認のために表示します。

### v2.34.0: Workflow use（起動方針の選択）

`/settings` の **Features** で **Workflows** を有効にすると、その下に **Workflow use** が表示されます（Kiro CLI 2.34 以降）。Kiro がメインのチャットから Workflow を始める頻度を、次から選びます。公式 [Settings の Features](https://kiro.dev/docs/cli/chat/settings/#settings-features)（Page updated: 2026-10-24）の説明は次のとおりです。

| 選択肢 | 動作 |
|--------|------|
| **Only when asked**（既定） | 利用者が依頼したときだけ Workflow を始める |
| **Only for large tasks** | 複数のステップにわたる作業や、より多くのコンテキストが必要な作業には、Kiro が自分で始めることがある |
| **As much as possible** | コードの読み取り・実装・テスト・レビューの作業の大半を Workflow 経由にしようとする |

- 選択は `chat.workflowLaunch` に保存され、現在のセッションに（可能なら）適用され、その後は新しいセッションに適用される
- 公式 [Settings リファレンス](https://kiro.dev/docs/reference/settings/)（Page updated: 2026-10-24）は、`chat.workflowLaunch` の値を `when-asked`（既定）・`large-tasks`・`delegate-all` と列挙し、実機 `kiro-cli 2.34.0` の `kiro-cli settings list --all` も同じ 3 つの値を説明している。選択肢の名称と値の対応（Only when asked ↔ `when-asked` など）を公式は明記していないため、対応は**未確認**
- **Workflows** が表示されない場合は、そのアカウントでは利用できない。`chat.enableWorkflows` を変更した後は Kiro CLI を再起動する（Workflow のコマンドはプロセスの開始時に決まる）

設定の手順: `/settings` → **Features** で **Workflows** を有効にします。**Workflows** を有効にすると、その下に **Workflow use** が表示されます。公式は、`chat.enableWorkflows` を変更した後に Kiro CLI を再起動するよう説明しています。**Workflow use** を選ぶ操作と再起動の前後関係は、公式に記載がなく**未確認**です。

> 前回までの記載との関係: v2.28.0 では「Workflows が有効な V3 チャットは常に Workflows で委譲する」と説明されていました（→ [47. v2.28 新機能](47_v228NewFeatures.md)）。v2.33.1 で「依頼したときだけ開始」に変わり、v2.34.0 で起動方針を選べるようになりました。

### v2.34.0: 計画の承認に変更案を入力

[V3] の Workflow の計画承認に、変更案を直接入力できます。Kiro は、どのステップも実行される前に計画を更新します。公式 Workflows（上記ページ）は、Kiro CLI 2.34 以降、承認に変更案を入力して計画を修正でき、答えるまで何も実行されないと説明しています。計画承認のステップツリー（v2.33.0）は [52. v2.33 新機能](52_v233NewFeatures.md)、計画のプレビュー（v2.32.0）は [51. v2.32 新機能](51_v232NewFeatures.md) を参照してください。

関連する修正:

- [V3] Workflow が、再起動後に再計画や完了済みステップの繰り返しをせず、続きから再開する（v2.34.0）。実機 `kiro-cli 2.34.0` の `kiro-cli settings list --all` には、関連しうる `chat.workflow.continueInterrupted`（"Continue interrupted workflows after reconnecting"）と `chat.workflowMonitor.mouseEnabled`（"Enable workflow monitor mouse controls"）が表示されますが、この修正との関係は公式に記載がなく**未確認**です
- [V3] Workflow モニターのツール承認が、現在の呼び出しで開き、`q` で閉じる（v2.34.0）
- [V3] Workflow の計画承認が、最初の選択肢をハイライトした状態で開き、Enter で選べる（v2.33.1）

## [V3] CLI から Memory を削除（v2.34.0）

`/memories` を開いて Memory を選び、`Ctrl+D` を押すと削除できます。公式 [Memory の Review what Kiro remembers](https://kiro.dev/docs/memory/#review-what-kiro-remembers)（Page updated: 2026-10-24）の説明は次のとおりです。

- `/memories` から `list` を選ぶと、保存された Memory を閲覧・プレビューできる
- Kiro CLI 2.34 以降は、一覧または詳細の画面で `Ctrl+D` を押すと、選択した Memory を削除する。`y` で確認、`n` で残す
- Memory の内容を直したいときは、チャットで Kiro に頼む。Kiro が変更できるのは、`read & write` のアクセスで、信頼したワークスペースにいるときだけ
- Memory は V3 が必要で、保存先はユーザーアカウントごと（ワークスペースごとではない）

Memory の全体は [48. v2.29 新機能](48_v229NewFeatures.md) を参照してください。信頼していないワークスペースでの削除の扱いは、公式 Permissions が「エージェントは Memory を追加・変更・削除できない」と説明していますが、利用者が `Ctrl+D` で行う削除に同じ制限が及ぶかは記載がなく**未確認**です。

## `/model edit` — ピッカーに出すモデルを選ぶ（v2.34.0）

`/model edit` を実行すると **Models in /model** が開き、`/model` のピッカーに表示するモデルを選べます。公式 [Slash commands の `/model`](https://kiro.dev/docs/reference/slash-commands/#model)（Page updated: 2026-10-24）の説明は次のとおりです。

- Space または Enter で、モデル・プロバイダー・すべてのモデルのどれかを切り替える
- 隠したモデルも、`/model <model-id>`・`--model`・エージェント設定・フォールバック設定では引き続き使える
- 実機 `kiro-cli 2.34.0` の `kiro-cli settings list --all` には、`chat.modelPicker.hiddenModels`（"Model ids the /model picker leaves out (array of strings)"）が表示される。この設定キーは公式 Settings リファレンスに記載がなく、実機のみで確認した
- changelog に `[V3]` の表記はなく、公式にも V2／V3 の記載がない。**V2 でも使えるかは未確認**

## `--trust-workspace` — ワークスペースの信頼を 1 回の起動だけ（v2.34.0）

V3 を `--trust-workspace` 付きで起動すると、選択を保存せずにワークスペースの信頼確認を省略できます。公式 [Permissions の Trust a workspace in Kiro CLI](https://kiro.dev/docs/permissions/#trust-a-workspace-in-kiro-cli)（Page updated: 2026-10-24）は、次のように説明しています。

- フラグは確認画面を省略し、`workspaceTrusted` を保存しない。そのため、以前に信頼を保存したフォルダでない限り、次の起動では再び確認される
- 信頼を取り消すには、確認画面が示したファイルから `workspaceTrusted` の行を削除する

実機 `kiro-cli 2.34.0` の `kiro-cli chat --help` は、このフラグを「Skip the "Trust this workspace?" prompt for this launch only (V3 only)」と説明し、この起動ではフォルダの hooks・agents・MCP サーバー・workflows が確認なしに読み込まれ、決定は保存されない、と表示します。公式の [CLI commands](https://kiro.dev/docs/reference/cli-commands/)（Page updated: 2026-10-20）には、このフラグは掲載されていません。ワークスペースの信頼確認そのもの（v2.33.0）は [52. v2.33 新機能](52_v233NewFeatures.md) を参照してください。

## 変更（v2.34.0）

changelog に記載された次の 4 件の変更について、公式 Changelog 以外の公式ページで詳細を確認できた範囲を示します。

| 変更 | 公式ドキュメントでの確認 |
|------|------------------------|
| [V3] ツール承認が **Allow once** と **Deny once** を先頭に並べ、続いて許可または拒否のルールを保存する選択肢を並べる | 取得した公式ページの範囲では、選択肢の並び順の記載は確認できなかった（**未確認**）。権限は [17. Granular Tool Trust](17_GranularToolTrust.md) を参照 |
| [V3] セッションダッシュボードが、セッションを削除する前に確認する | 公式 [Session management](https://kiro.dev/docs/cli/chat/session-management/)（Page updated: 2026-10-20）は、セッションを選んで `Ctrl+D` で削除を準備し、`y` で確認、それ以外のキーで取り消すと説明している。この確認が v2.34.0 の変更と同じものかは記載がなく**未確認**。ダッシュボードは [40. v2.21 新機能](40_v221NewFeatures.md) を参照 |
| [V3] 解析できない shell コマンドを、承認を求めずに拒否する | 取得した公式ページの範囲では記載を確認できなかった（**未確認**） |
| [V3] サブエージェントが、親エージェントがインラインで宣言した MCP サーバーを受け取らない | 取得した公式ページの範囲では記載を確認できなかった（**未確認**）。サブエージェントは [02. Subagents](02_Subagents.md) を参照 |

## [V3] セキュリティ（v2.34.0）

HTTP 経由のリモート MCP サーバーが、同一オリジンのリダイレクトだけに従います。公式 Changelog v2.34 は、これを Fixes の末尾に置き、CLI 内蔵 changelog は security に分類しています。公式 MCP 関連ページに、リダイレクトの扱いの記載は確認できませんでした（**未確認**）。

## バグ修正の要点

### v2.34.0

| 内容 | 公式ドキュメントでの確認・適用範囲 |
|------|----------------------------------|
| [V3] ヘッドレスモードが、エージェントの質問に答えたり、信頼されたツールを指定しない要求を承認したりしない。ヘッドレスモードは、対話セッションで保存された MCP サインインを再利用する | 公式 [Headless mode](https://kiro.dev/docs/cli/headless/)（Page updated: 2026-10-21）は、承認する人がいない非対話実行向けに `--trust-all-tools` と `--trust-tools` を説明している。個々の修正の記載は確認できなかった（**未確認**） |
| `/usage` にエンタープライズの超過利用（overage）の状況と消費済みクレジットが表示される | 公式 Slash commands の `/usage` の節は、非対話実行で `/usage` が使用状況の全内訳を出力すると説明している。超過利用の表示の記載は確認できなかった。**V2／V3 の適用範囲は未確認** |
| `chat.allowIcons` が off のとき、端末が罫線文字とブロック文字を使わず、矢印キーを単語として読み上げる | 公式 [Settings](https://kiro.dev/docs/cli/chat/settings/)（Page updated: 2026-10-24）は、`chat.allowIcons` を「off にすると状態アイコン（●、○、⚠）を隠し、テキストだけのラベルにする」と、`chat.allowAsciiArt` を「off にすると、点字の点・罫線・Unicode の記号を ASCII に置き換える」と説明している。この修正の記載は確認できなかった。**V2／V3 の適用範囲は未確認** |
| V2 の Rust エンジンと V3 が、モデルの拒否の後も部分的な返信を保持する。フォールバックモデルは、プロンプトにもう一度答えるのではなく、その続きから返信する | 公式 Changelog v2.34 が「V2 の Rust エンジンと V3」と明記している。フォールバックの設定は [52. v2.33 新機能](52_v233NewFeatures.md) と [46. v2.27 新機能](46_v227NewFeatures.md) を参照 |
| [V3] `kiro-cli acp` が、エージェントの実行中に終了しない | ACP は [13. ACP](13_ACP.md) を参照。この修正の記載は公式の取得範囲では確認できなかった（**未確認**） |
| [V3] `/agent` で切り替えたエージェントが宣言した Skills を読み込む | Skills は [07. Skills](07_Skills.md) を参照。この修正の記載は確認できなかった（**未確認**） |
| [V3] `/rewind` が失敗した、または完了しなかったターンで正しい位置から分岐する。deny ルールが選んだスコープに保存される。`/sessions` が多数の保存済みセッションでも固まらない | 個々の修正の記載は確認できなかった（**未確認**） |
| [V3] macOS のサンドボックスで `ssh` と `ssh-keygen` が `No user exists for uid` で失敗しない。[V3] Windows でワークスペースのフォルダ外のファイルを削除できる | サンドボックスは [50. v2.31 新機能](50_v231NewFeatures.md) を参照。個々の修正の記載は確認できなかった（**未確認**） |

次の修正は、関連する公式の記載を確認できませんでした（**未確認**。V2／V3 の適用範囲も changelog にありません）。

- エージェントがツール呼び出しの準備中に静かになったとき、画面が固まったように見えず `Working...` を表示する
- チャット内の Mermaid 図が、生の HTML を表示したり描画に失敗したりせず、より多くの場合に描画される（Mermaid は [52. v2.33 新機能](52_v233NewFeatures.md)・[50. v2.31 新機能](50_v231NewFeatures.md)）
- 貼り付けた画像と、メニューやピッカーのフィルターに貼り付けた、または音声入力したテキストが動作する

### v2.33.1

| 内容 | 公式ドキュメントでの確認・適用範囲 |
|------|----------------------------------|
| `kiro-cli mcp add --agent` が、`tools` リストに新しいサーバーを含まないエージェントにもそのサーバーを付与し、`chat.enableAutoAgentUpgrade` が on のとき V3 向けにエージェントファイルをアップグレードする | 公式 [MCP configuration の Adding servers to a specific agent](https://kiro.dev/docs/mcp/configuration/#adding-servers-to-a-specific-agent)（Page updated: 2026-10-23）が、`kiro-cli mcp add --name git-server --agent rust-dev` の例とともに同じ説明をしている。実機 `kiro-cli 2.34.0` の `kiro-cli mcp add --help` も `--agent <AGENT>` を表示する（エージェント名を指定しないときは、グローバルの `mcp.json` に追加する）。`chat.enableAutoAgentUpgrade` は [34. `/upgrade-agent`](34_v214UpgradeAgent.md) と[設定リファレンス](../04_reference/01_settings.md)を参照 |
| スクリーンリーダーが有効なとき、`/tools` が各ツールをフィールドごとに 1 行・ラベル付きで一覧する | スクリーンリーダー対応は [49. v2.30 新機能](49_v230NewFeatures.md) を参照。**V2／V3 の適用範囲は未確認** |
| [V3] V2 のセッションを V3 で再開したとき、保存済みのツール承認が引き継がれなかったことと、V3 で承認を保つ方法を伝える | 取得した公式ページの範囲では記載を確認できなかった（**未確認**）。権限は [17. Granular Tool Trust](17_GranularToolTrust.md) を参照 |
| [V3] 利用できないオプションの Power の MCP サーバーがプロンプトのターンをブロックしない。MCP サインインの後、固定された OAuth コールバックポートを占有したままにしない。V3 のレジストリから追加した MCP サーバーが、カタログのパッケージバージョンで起動する | Powers は [44. v2.25 新機能](44_v225NewFeatures.md)、MCP OAuth は [32. MCP OAuth](32_MCPOAuthManagement.md) を参照。個々の修正の記載は確認できなかった（**未確認**） |
| [V3] モデルが履歴内の画像を拒否しても compaction が失敗せず、画像なしで再試行する。画像が多い長いセッションが、古い画像を省略して上限内に収める | 取得した公式ページの範囲では記載を確認できなかった（**未確認**）。compaction は [10. Conversation Compaction](10_ConversationCompaction.md) を参照 |
| [V3] サブエージェントとして動くカスタム V3 エージェントが自身のナレッジベースを検索できる。起動された V3 サブエージェントが自身の Skills を読み込む。`@builtin` を使う V3 エージェントが Web 検索を含む。ホームフォルダで V3 セッションを開始してもユーザーエージェントのファイルの allow・deny ルールが失われない | 取得した公式ページの範囲では記載を確認できなかった（**未確認**）。サブエージェントは [02. Subagents](02_Subagents.md) を参照 |
| [V3] spec タスクの実行後に送ったメッセージが、そのタスクを更新し続けられる | 取得した公式ページの範囲では記載を確認できなかった（**未確認**） |
| コードプレビュー内の HTML の doctype とタグの括弧が、読みやすいコントラストのテーマ色を使う | 取得した公式ページの範囲では記載を確認できなかった。**V2／V3 の適用範囲は未確認** |

## 実機で確認した事項

- `kiro-cli --version` は `kiro-cli 2.34.0` を表示する
- `kiro-cli version --changelog=2.34.0`・`--changelog=2.33.1` が、公式 Changelog との突合に使った内蔵 changelog（それぞれ 28 項目・16 項目）。実機が保持する内蔵 changelog はこの 2 版だけで、v2.33.0 は保持しない
- `kiro-cli chat --help` に `--trust-workspace` が表示される
- `kiro-cli settings list --all` に `chat.workflowLaunch`・`chat.modelPicker.hiddenModels`・`chat.workflow.continueInterrupted`・`chat.workflowMonitor.mouseEnabled` が表示される
- `kiro-cli mcp add --help` に `--agent <AGENT>` が表示される
- V3 セッションを起動して確認する作業（MCP elicitation、Workflow use、`/memories` の `Ctrl+D`、`/model edit`）は、今回していないため**実機では未確認**

## 関連リンク

### 本サイト

- [52. v2.33 新機能](52_v233NewFeatures.md)
- [51. v2.32 新機能](51_v232NewFeatures.md)
- [48. v2.29 新機能](48_v229NewFeatures.md)
- [47. v2.28 新機能](47_v228NewFeatures.md)
- [32. MCP OAuth Management](32_MCPOAuthManagement.md)
- [17. Granular Tool Trust](17_GranularToolTrust.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [設定リファレンス](../04_reference/01_settings.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.34](https://kiro.dev/changelog/cli/2-34/)
- [Kiro CLI Changelog v2.33.1](https://kiro.dev/changelog/cli/2-33-1/)
- [MCP usage — MCP elicitation](https://kiro.dev/docs/mcp/usage/#mcp-elicitation)
- [Workflows](https://kiro.dev/docs/workflows/)
- [Settings — Features](https://kiro.dev/docs/cli/chat/settings/#settings-features)
- [Memory](https://kiro.dev/docs/memory/)
- [Slash commands — /model](https://kiro.dev/docs/reference/slash-commands/#model)
- [Permissions — Workspace trust](https://kiro.dev/docs/permissions/#trust-a-workspace-in-kiro-cli)
- [MCP configuration](https://kiro.dev/docs/mcp/configuration/#adding-servers-to-a-specific-agent)
- `kiro-cli version --changelog=2.34.0` / `kiro-cli settings list --all` / `kiro-cli chat --help` / `kiro-cli mcp add --help`（実機 2.34.0）

**最終更新**: 2026-10-25
**対象バージョン**: Kiro CLI v2.34.0（v2.33.1 を含む。MCP elicitation・Workflow の起動方針・Memory の削除・`--trust-workspace` は V3 Early Access）
