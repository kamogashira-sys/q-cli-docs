[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.33 新機能

# 52. v2.33 新機能 — [V3] ワークスペースの信頼確認・Workflow 計画ツリー・V3 のモデルフォールバック

## 概要

Kiro CLI **v2.33.0**（2026-10-20）では、[V3] の対話セッションで、Kiro がフォルダの hooks・agents・MCP サーバー・steering・workflows・言語サーバー設定を読み込む前に、そのフォルダを信頼するかを確認するようになりました。クローンしたリポジトリは、利用者が承認するまでエージェントの動作を変えられません。V3 でモデルフォールバックを再び設定でき、Workflow の計画承認は、詳細を展開できるコンパクトなステップツリーで表示されます。V2 の `grep` ツールの並列検索による高速化、サブグラフを含む Mermaid フローチャートの描画、[V3] の長いセッションでのメモリ削減も加わりました。セキュリティ面では、[V3] のサンドボックスのネットワーク規則がホスト名の大文字小文字に関係なく一致し、Windows の hook コマンドが作業ディレクトリの同名プログラムを実行しなくなりました。

> **出典について**: 本ページの一次情報は公式 [Changelog v2.33](https://kiro.dev/changelog/cli/2-33/)（表示日 2026-10-20）です。v2.33.0 は、前回の反映時には公式サイトの Changelog に掲載されておらず、`kiro-cli version --changelog=2.33.0`（CLI 内蔵 changelog）だけを出典にしていましたが、その後に公式 Changelog へ掲載されたため、出典と分類を公式に差し替えました。公式は 29 項目（主要節 2／Improvements 6／Fixes 21）、CLI 内蔵 changelog は 28 項目で、差は[変更履歴の v2.33.0 の注記](../02_update/01_changelog.md#v2330-cli2026-10-20)に示しています。

- **機能追加 2 件**: [V3] ワークスペースの信頼確認、[V3] モデルフォールバックの設定
- **改善 6 件**: [V3] Workflow 計画のステップツリー、Mermaid のサブグラフ・色・折り返しラベル、[V3] PR ウォッチのコンフリクト・チェック・スレッド対応、V2 の `grep` の並列検索、[V3] 長いセッションのメモリ、[V3] スロットリングエラーの区別
- **セキュリティ 2 件**: [V3] サンドボックスのネットワーク規則、[V3] Windows の hook コマンド
- **バグ修正 19 件**

changelog で `[V3]` の表記がない項目のうち、公式にも V2 専用か両対応かの記載がないものは、本ページで「未確認」と示します。

## [V3] ワークスペースの信頼確認

対話型の V3 セッションをフォルダで初めて始めるとき、Kiro CLI は、そのフォルダの hooks・agents・MCP サーバー・steering・workflows・言語サーバー設定を読み込む前に、**Trust this workspace?** 画面を表示します。**Trust, continue** か **Don't trust, exit** を選びます。

- 回答は、ワークスペースのルートごとに `~/.kiro/workspace-roots/` に保存されるため、画面はフォルダごとに 1 回表示されます
- ホームディレクトリの信頼は保存されず、起動のたびに確認します
- 回答を変えるには、画面が示すワークスペースごとのファイルから `workspaceTrusted` を削除します

### 公式 Permissions の説明（確認できた範囲）

公式 [Permissions の Workspace trust](https://kiro.dev/docs/permissions/#workspace-trust)（Page updated: 2026-10-24）は、次のように説明しています。

- リポジトリ内にあるエージェントの入力（`.kiro/agents/` のカスタムエージェント、`.kiro/steering/` の Steering、ワークスペースの MCP サーバー設定、Skills、Workflow のファイル）は、クローンしたリポジトリがエージェントの動作を変えるのに使える。そのため Kiro は、信頼するまでワークスペースを信頼しないものとして扱う。信頼の判断はワークスペースの外に保存されるため、リポジトリ自身は信頼の状態を変えられない
- 信頼するまで、Kiro はワークスペースのカスタムエージェント・Steering・MCP サーバー設定・Skills・Workflow のファイルを読み込まない。すべての shell コマンドと、すべての MCP ツールの呼び出しの前に、保存済みのルールが許可していても確認を求める（一致する `deny` ルールは拒否する）
- 信頼していないワークスペースでは、エージェントは Memory・ナレッジベース・リモートの学習内容を追加・変更・削除できない。読むことはできる
- **非対話実行（`--no-interactive`）と V1・V2 のセッションは、この確認の対象ではない**。確認なしにワークスペースの設定を読み込む。この画面は Kiro CLI 固有である

> 前回の反映時は、非対話実行での扱いが公式に記載されておらず「未確認」としていました。現在の公式 Permissions に上記の記載があるため、解消しました。V3 の概要は [09_v3/](../09_v3/README.md)、権限全般は [17. Granular Tool Trust](17_GranularToolTrust.md) を参照してください。

### v2.34.0 の `--trust-workspace`

v2.34.0 で、V3 を `--trust-workspace` 付きで起動すると、選択を保存せずに 1 回の起動だけ信頼確認を省略できるようになりました（→ [53. v2.34 新機能](53_v234NewFeatures.md)）。

## [V3] モデルフォールバックの設定

V3 のセッションで、モデルフォールバックを再び設定できるようになりました。`/model` の設定ペインの **Fallback** 行と `/model fallback` のコマンドが、エージェントが対応していれば、フォールバックの設定を保存します。保存した選択は現在のセッションに適用され、以降のセッションにも保持されます。`/model` を開いて **Fallback** 行を読むと、保存した選択を確認できます。

公式 [Slash commands の `/model`](https://kiro.dev/docs/reference/slash-commands/#model)（Page updated: 2026-10-24）の「Model fallback (V3)」は、次のように説明しています。

- 引数なしの `/model fallback` は、現在のモデルのフォールバックのピッカーを開く。**None** を選ぶとフォールバックを off にし、拒否されてもターンは現在のモデルに留まる。選択を解除すると、拒否にはベンダー既定のモデルが答える
- モデルは自分自身をフォールバックにできない
- エージェントがフォールバックの設定に対応していないときは、`This agent does not support configuring a model fallback` と表示する。セッションの認証情報が設定を保存できないときは、**Fallback** 行が `read-only` と表示される
- ターンが別のモデルに移ると、transcript がそれを報告する。→ [Model fallback notices](https://kiro.dev/docs/cli/terminal-ui/#model-fallback-notices)

> **前回の「公式間の食い違い」は解消しました**: 前回は、CLI 内蔵 changelog が「V3 でフォールバックを再び設定できる」と記載する一方、公式 Slash commands が「`/model fallback` は V1 と V2 に適用される」と説明していたため、両論を併記していました。現在の公式 Slash commands は、V1・V2 向けと V3 向けの節を分けて、v2.33 以降の V3 での設定を説明しています。V1・V2 の `/model fallback` は [46. v2.27 新機能](46_v227NewFeatures.md)、V3 の通知は [49. v2.30 新機能](49_v230NewFeatures.md) を参照してください。

## [V3] Workflow の計画承認と PR ウォッチ

### 計画承認のステップツリー

V3 の Workflow が計画の承認を求めるとき、承認はコンパクトなステップツリーを表示します。公式 [Workflows の Start from the agent](https://kiro.dev/docs/workflows/#start-from-the-agent)（Page updated: 2026-10-24）の説明は次のとおりです。

- ツリーには、各ステップとそのエージェントが並び、計画がモデルと effort を設定していれば、それらも表示される
- **Tab** でツリーに移動し、**Enter** でステップの詳細の表示・非表示を切り替え、もう一度 **Tab** で選択肢に戻る
- 答えるまで何も実行されない
- `/tools trust-all` が on のときは、ルールを保存せず、1 回限りの Allow で計画に答える
- 組織が Auto モデルを無効にしていても、Workflow は失敗せずに開始する（2.33 以降）

v2.32.0 の計画プレビューは [51. v2.32 新機能](51_v232NewFeatures.md)、v2.34.0 の計画への変更案の入力は [53. v2.34 新機能](53_v234NewFeatures.md) を参照してください。

### PR ウォッチがコンフリクト・チェック・スレッドに対応

GitHub の PR を監視する V3 の Workflow が、PR にマージコンフリクトがあるとき、チェックが失敗したとき、レビューのスレッドに回答が付いたときに動きます。これらのイベントが届くまでは、モデルのターンなしで待ちます。公式 [Author workflows の Watch a pull request with `github-pr`](https://kiro.dev/docs/workflows/authoring/)（Page updated: 2026-10-21）の説明は次のとおりです。

- 2.33 以降、ベースブランチとのマージコンフリクトもウォッチを起こす（2.33 より前は、コンフリクトしている PR に対してウォッチは何もしなかった）。`mergeable` は `MERGEABLE`・`CONFLICTING`・`UNKNOWN`（GitHub が状態を計算中）のいずれかで、コンフリクトは、ヘッドコミットとベースブランチの先頭の組ごとに 1 回だけ報告される
- 失敗した CI のチェックもウォッチを起こす。ペイロードの `newFailedChecks` に、`name`・`workflowName`・`conclusion`・`detailsUrl`・`runId`・`startedAt`・`completedAt` が入り、失敗は、ヘッドコミット・チェック名・詳細 URL・完了時刻ごとに 1 回だけ報告される
- 2.33 以降、配信されるインラインコメントは `threadId`（レビューのスレッドの ID。読めなければ `null`）を持つ。応答する側が、答えたスレッドを解決できる

実際の Workflow の例は、公式 [Workflow patterns の Publish and respond](https://kiro.dev/docs/workflows/patterns/#publish-and-respond) を参照してください。

### review loop の停止条件

[V3] Workflow の review loop が、レビュー担当が承認した時点で止まります。`fileCheck` の `jsonPath` が `$.` で始まる場合（`$.verdict` など）に、指定したフィールドを読みます。公式 [Author workflows の Define stop conditions](https://kiro.dev/docs/workflows/authoring/#define-stop-conditions) は、`verdict` と `$.verdict` が同じフィールドを読むこと、2.33 以降は `[`・`]`・`*`・`..`、または 2 番目以降の `$` の区間を含む `jsonPath` が検証に失敗し、エラーが最初の未対応のトークンを示すことを説明しています。2.33 より前は、そのようなパスは一致せず、警告もなく上限まで繰り返されました。review loop の一時停止は v2.32.0（→ [51. v2.32 新機能](51_v232NewFeatures.md)）です。

## Mermaid のサブグラフ・色・折り返しラベル

チャット内の Mermaid フローチャートが、サブグラフをタイトル付きの枠として描画し、スタイルクラスの色を適用し、`<br/>` を 2 行目として描画します。ノードのラベルは最大 4 行に折り返され、それより長いテキストは省略記号で終わります。公式 [Terminal UI の Mermaid diagrams](https://kiro.dev/docs/cli/terminal-ui/#mermaid-diagrams)（Page updated: 2026-10-21）の説明は次のとおりです。

- 2.33 以降、フローチャートは `subgraph ... end` のブロックをタイトル付きの枠として描画し、`<br/>` で新しいラベルの行を始め、ノードの枠を最初のスタイルクラス（`A:::focal` または `class A,B focal`）の色で塗る。色が付くのは、テーマがそのクラス名（`function`・`class`・`file`・`directory`・`external`・`focal`）を知っているとき
- ネストされたサブグラフは未対応で、Kiro はソースを表示する。`classDef`・`style`・`linkStyle` の文は読み飛ばされ、色は図ではなくテーマから決まる
- 図が広すぎる・大きすぎる・未対応、または未対応の構文を使うときは、ソースと理由を表示する。[ASCII art が off](https://kiro.dev/docs/cli/chat/settings/#settings-display) のとき、または `KIRO_ASCII_MODE=1` のときは、常にソースを表示する

Mermaid の導入は v2.31.1（→ [50. v2.31 新機能](50_v231NewFeatures.md)）、描画の追加の修正は v2.34.0（→ [53. v2.34 新機能](53_v234NewFeatures.md)）です。公式 Terminal UI のこの節は、V2 と V3 のどちらに適用されるかを明記していません（**未確認**）。

## V2 の `grep` ツールの並列検索

公式 Changelog v2.33 は、「V2 の `grep` ツールが、ファイルを CPU コア全体で並列にスキャンするため、大規模なプロジェクトでの検索が速く終わる」と説明しています。前回は、CLI 内蔵 changelog に `[V3]` の表記がなく V2／V3 の適用範囲が**未確認**でしたが、公式が「V2」と明記しているため、V2 の項目として確定しました。`grep` ツールは [05. Grep/Glob](05_GrepGlob.md) を参照してください。なお、公式 [Built-in tools](https://kiro.dev/docs/reference/built-in-tools/)（Page updated: 2026-10-13）の `grep` の節には、並列スキャンの記載はありません。

## [V3] セキュリティ修正

| 内容（公式 Changelog v2.33） | 公式ドキュメントでの確認 |
|----------------------------|------------------------|
| [V3] サンドボックスのネットワーク規則が、ホスト名の大文字小文字に関係なく一致する。`example.com` と書いた規則は `Example.COM` にも適用される | 公式 [Local command sandbox](https://kiro.dev/docs/sandbox/)（Page updated: 2026-10-15）は、`sandbox_network` のパターンが大文字小文字を区別せず、完全一致のホスト名と `*.suffix` のワイルドカードに対応すると説明している。サンドボックスは [50. v2.31 新機能](50_v231NewFeatures.md) を参照 |
| [V3] Windows で、hook コマンドが作業ディレクトリにある同名のプログラムを実行しない | 取得した公式ページの範囲では、この修正の記載を確認できなかった（**未確認**）。Hook は [22. Hooks](22_Hooks.md) を参照 |

## バグ修正の要点

公式 Changelog v2.33 の Fixes のうち、関連する公式ドキュメントが確認できたものを先に示します。

| 内容（公式 Changelog v2.33） | 公式ドキュメントでの確認 |
|----------------------------|------------------------|
| [V3] `chat.terminalTitle` が有効なとき、端末タイトルがセッションのタイトルを表示する | 公式 [Settings リファレンス](https://kiro.dev/docs/reference/settings/)（Page updated: 2026-10-24）の `chat.terminalTitle` は、名前を `/title` で付けていればその名前、なければセッションのタイトル、なければワークスペースのフォルダ名を端末タイトルにすると説明し、2.33 以降は V3 のセッションがセッションのタイトルを表示する、と明記している |
| `kiro-cli chat --agent <agent> @agent-sop:<name>` が、入力したテキストをそのまま送らず SOP を実行する。`--no-interactive` でも同様 | 公式 [Headless mode](https://kiro.dev/docs/cli/headless/)（Page updated: 2026-10-21）は、2.33 以降、最初のメッセージが `@<prompt-name>` で始まると、テキストをそのまま送らずにそのプロンプトを実行する（対話セッションでも `--no-interactive` でも）と説明している。名前は、ワークスペース・グローバル・MCP のプロンプトに大文字小文字を区別せず一致し、`@agent-sop:<name>` は名前付きの SOP を実行する。名前の後のテキストはプロンプトの引数になる |
| [V3] Workflow の review loop が、レビュー担当の承認で止まる | 上の「review loop の停止条件」を参照 |
| [V3] `/code summary` が、コードインテリジェンスの概要からコードベースのドキュメントを生成する | 公式 Slash commands の `/code` の節は `init`・`overview`・`status`・`logs` を掲載し、`summary` の記載は確認できなかった（**未確認**）。コードインテリジェンスは [01. LSP](01_LSP.md) を参照 |
| `/sessions` が、検索インデックスの追従中に数秒間固まらない | 公式 Slash commands は `/sessions` を V3 のセッションダッシュボードと説明している（V3 のみ）。修正そのものの記載は確認できなかった（**未確認**） |

次の修正は、関連する公式の記載を確認できませんでした（**未確認**）。

- [V3] Kiro が自発的に開始する返信（Workflow の完了後など）が、数語で途切れない
- [V3] `/agent`・`/model`・`/effort` が、入力途中の引数をインラインで再び補完する
- 自動モデルリトライの通知が、モデル名を示さない（V2／V3 の適用範囲も**未確認**）
- ホームディレクトリから Kiro CLI を起動しても、グローバルのエージェントが 2 回表示されない（V2／V3 の適用範囲も**未確認**）
- [V3] ホームディレクトリで `/sandbox` がグローバルのサンドボックス設定をプロジェクト設定として扱わない。そこでプロジェクト設定を変更しても、グローバル設定を上書きしたり削除したりしない
- [V3] `permissions.yaml` のサンドボックスのネットワーク規則を編集すると、実行中のサンドボックスに適用される。以前は、`/sandbox off` と `/sandbox on` の後に新しい規則が有効になった
- [V3] 応答が返らないリクエストの後も、クラウド設定の同期が続く（リクエストはタイムアウトして再試行される）。クラウド設定が空のとき、セッションにクラウド設定の同期カードが表示されない。クラウドセッションの `/code` が、サンドボックスのワークスペースルートと `lsp.json` のパスを表示する（→ [36. Cloud Sessions](36_CloudSessions.md)）
- [V3] `code` ツールが、実際のエラーがある Python ファイルで「No diagnostics found」と報告せず、Python などの応答の遅い言語サーバーの報告を待つ
- [V3] Windows の Workflow が、ドライブ文字の大文字小文字が異なるレシピファイルを拒否しない
- セマンティック検索のモデルのダウンロードが、モデルのディレクトリの外にファイルを展開しない（公式も CLI 内蔵 changelog もセキュリティと分類していない。V2／V3 の適用範囲も**未確認**）
- `/model ` の後に Tab を押すと、`set-current-as-default` をサブコマンドとして再び表示する（V2／V3 の適用範囲も**未確認**）

### スロットリングエラー・長いセッションのメモリ

[V3] のスロットリングエラーは、モデルの過負荷なのか、利用者自身のレート制限に達したのかを伝えるようになりました。[V3] の長いセッションが保持するメモリは時間とともに減ります。公式 [Settings リファレンス](https://kiro.dev/docs/reference/settings/)は、スロットリング・5xx・接続切断を、バックオフ付きで自動的に再試行すると説明していますが、エラー表示の区別とメモリの削減の記載は確認できませんでした（**未確認**）。

## 実機で確認した事項

実機 `kiro-cli 2.34.0` の `kiro-cli version --changelog=2.33.0` は、実機が v2.33.0 の内蔵 changelog を保持していないため表示できません（`kiro-cli version --changelog=all` は 2.34.0 と 2.33.1 の 2 件のみ保持）。本ページの項目は公式 Changelog v2.33 を一次情報としています。V3 セッションを起動して確認する作業（ワークスペースの信頼確認、`/sandbox`、`/model fallback` など）は、今回していないため**実機では未確認**です。

## 関連リンク

### 本サイト

- [53. v2.34 新機能](53_v234NewFeatures.md)
- [51. v2.32 新機能](51_v232NewFeatures.md)
- [50. v2.31 新機能](50_v231NewFeatures.md)
- [49. v2.30 新機能](49_v230NewFeatures.md)
- [46. v2.27 新機能](46_v227NewFeatures.md)
- [05. Grep/Glob](05_GrepGlob.md)
- [17. Granular Tool Trust](17_GranularToolTrust.md)
- [22. Hooks](22_Hooks.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.33](https://kiro.dev/changelog/cli/2-33/)
- [Permissions — Workspace trust](https://kiro.dev/docs/permissions/#workspace-trust)
- [Workflows](https://kiro.dev/docs/workflows/)
- [Author workflows](https://kiro.dev/docs/workflows/authoring/)
- [Workflow patterns](https://kiro.dev/docs/workflows/patterns/)
- [Local command sandbox](https://kiro.dev/docs/sandbox/)
- [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)
- [Slash commands](https://kiro.dev/docs/reference/slash-commands/)
- [Settings リファレンス](https://kiro.dev/docs/reference/settings/)
- [Headless mode](https://kiro.dev/docs/cli/headless/)
- [Built-in tools](https://kiro.dev/docs/reference/built-in-tools/)

**最終更新**: 2026-10-25
**対象バージョン**: Kiro CLI v2.33.0（公式 Changelog v2.33 を一次情報とする。ワークスペースの信頼確認・Workflow の拡張・モデルフォールバックの設定・セキュリティ修正は V3 Early Access）
