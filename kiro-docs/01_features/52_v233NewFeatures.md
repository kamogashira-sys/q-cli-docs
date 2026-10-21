[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.33 新機能

# 52. v2.33 新機能 — [V3] フォルダ信頼確認・Workflow 計画ツリー・セキュリティ修正（CLI 内蔵 changelog のみ）

## 概要

Kiro CLI **v2.33.0**（2026-10-20）では、[V3] で Kiro がフォルダの hooks・agents・MCP サーバー・workflows を読み込む前に、そのフォルダを信頼するかを確認するようになりました。Workflow の計画承認は、詳細を展開できるコンパクトなステップツリーで表示されます。`grep` ツールの並列検索による高速化、サブグラフを含む Mermaid フローチャートの描画、[V3] の長いセッションでのメモリ削減も加わりました。セキュリティ面では、[V3] のサンドボックスのネットワーク規則がホスト名の大文字小文字に関係なく一致し、Windows の hook コマンドが作業ディレクトリの同名プログラムを実行しなくなりました。

> **出典について（重要）**: v2.33.0 は**公式サイトの Changelog に掲載されていません**。公式 Changelog の `kiro.dev/changelog/cli/2-33/` は HTTP 404 を返し、`changelog/cli/2-33-0/` も同様です。本ページの出典は **`kiro-cli version --changelog=2.33.0`（CLI 内蔵 changelog）のみ**で、日付 2026-10-20 も CLI 内蔵 changelog の日付です。公式サイトに掲載された場合は、公式 Changelog を出典に差し替えてください。

- **機能追加 2 件**: [V3] フォルダの信頼確認、[V3] Workflow の計画承認のステップツリー
- **変更 4 件**: `grep` ツールの高速化、Mermaid のサブグラフ、[V3] 長いセッションのメモリ、[V3] Workflow の GitHub PR ウォッチ
- **セキュリティ 2 件**: [V3] サンドボックスのネットワーク規則、[V3] Windows の hook コマンド
- **バグ修正 20 件**

内蔵 changelog の項目のうち `[V3]` の表記がないものは、**V2 専用か V3 との両対応かが内蔵 changelog にも公式ドキュメントにも記載がない**ため、本ページでは「未確認」と示します。公式ドキュメントとの対応は、関連する公式ページの本文を取得して確認した範囲だけを書き、確認できなかった点は「未確認」と明記しています。

## [V3] フォルダの信頼確認

Kiro が、フォルダの hooks・agents・MCP サーバー・workflows を読み込む前に、そのフォルダを信頼するかを確認します（CLI 内蔵 changelog v2.33.0）。

### 関連する公式ドキュメント

公式 [Permissions の Workspace trust](https://kiro.dev/docs/permissions/#workspace-trust)（Page updated: 2026-10-20）と、公式 [New features in CLI V3 の Trusted workspaces](https://kiro.dev/docs/cli/v3/new-features/)（Page updated: 2026-10-10）は、ワークスペースの信頼を次のように説明しています。

- リポジトリ内にあるエージェントの入力（`.kiro/agents/` のカスタムエージェント、`.kiro/steering/` の Steering、ワークスペースの MCP サーバー設定、Skills、Workflow のファイル）は、クローンしたリポジトリがエージェントの動作を変えるのに使える。そのため Kiro は、信頼するまでワークスペースを信頼しないものとして扱う。信頼の判断はワークスペースの外に保存されるため、リポジトリ自身は信頼の状態を変えられない
- CLI は最初にワークスペースを開いたときに信頼を尋ねる
- 信頼するまで、Kiro はワークスペースのカスタムエージェント・Steering・MCP サーバー設定・Skills・Workflow のファイルを読み込まない。すべての shell コマンドと MCP ツールの呼び出しの前に、保存済みのルールが許可していても確認を求める。Kiro の設定ディレクトリへの書き込みの前にも確認を求める

### 内蔵 changelog と公式ドキュメントの違い（未確認事項）

| 項目 | 内蔵 changelog v2.33.0 | 公式ドキュメント |
|------|------------------------|------------------|
| 確認の単位 | 「フォルダ」 | 「ワークスペース」 |
| 読み込み前の確認の対象 | hooks・agents・MCP サーバー・workflows | カスタムエージェント・Steering・MCP サーバー設定・Skills・Workflow のファイル（hooks は挙げられていない） |

- 公式 Permissions ページの更新日（2026-10-20）は v2.33.0 の内蔵 changelog の日付と同じですが、そのページが v2.33.0 のこの項目を説明しているかは記載がなく、**未確認**です。本サイトは、内蔵 changelog の記述を v2.33.0 の項目として示し、公式のワークスペース信頼の説明を関連情報として併記します
- hooks の読み込み前の確認が、公式のワークスペース信頼の説明に含まれるかは**未確認**です
- **非対話実行（`--no-interactive`）で、このフォルダの信頼確認がどう扱われるかは、内蔵 changelog に記載がなく、取得した公式ページにも確認できませんでした（未確認）**。公式 Headless mode（Page updated: 2026-10-20）は、承認を求められない非対話実行向けに `--trust-all-tools` と `--trust-tools` を説明していますが、フォルダの信頼との関係は記載されていません
- 実機 2.33.0 で V3 セッションを起動して確認することは、今回していません（**実機では未確認**）

権限全般は [17. Granular Tool Trust](17_GranularToolTrust.md)、V3 の概要は [09_v3/](../09_v3/README.md) を参照してください。

## [V3] Workflow の計画承認のステップツリーと GitHub PR ウォッチ

### 計画承認のステップツリー（機能追加）

Workflow の計画承認が、詳細を展開できるコンパクトなステップツリーを表示します（CLI 内蔵 changelog v2.33.0）。

関連する公式の説明（[Workflows の Start from the agent](https://kiro.dev/docs/workflows/#start-from-the-agent)、Page updated: 2026-10-20）: V3 のセッションでは、Kiro がどのステップも実行する前に、提案する計画を承認のために表示する。Kiro CLI V3 では、`/workflow run` のピッカーでレシピを選ぶと計画プレビュー付きの確認フォームが開く（v2.32.0 → [51. v2.32 新機能](51_v232NewFeatures.md)）。公式 Workflows ページには、計画承認がステップツリーで表示されることの記載を確認できませんでした（**未確認**）。

### GitHub PR ウォッチ（変更）

[V3] Workflow の GitHub PR ウォッチが、マージコンフリクト、失敗したチェック、回答済みのスレッドに対応します（CLI 内蔵 changelog v2.33.0）。

公式 [Author workflows の Watch a pull request with `github-pr`](https://kiro.dev/docs/workflows/authoring/)（Page updated: 2026-10-20）の説明:

- `github-pr` ハンドラーは、PR の URL、または最上位の `url` フィールドに PR の URL を持つワークスペースの JSON ファイルを指す。PR がマージまたはクローズされると `terminal-state` を報告する
- 新しい活動があるとき、ペイロードに `newComments`・`newReviews`・`inlineComments`・`newFailedChecks`・`headSha`・`passingCheckCount`・`pendingCheckCount` などが入る
- CI のチェックの失敗もウォッチを起こす。同じヘッドコミット・チェック名・詳細 URL・完了時刻の失敗は 1 回だけ報告される

公式のこのページに、マージコンフリクトと回答済みのスレッドの扱いの記載は確認できませんでした（**未確認**）。失敗したチェックについては上記の記載があります。内蔵 changelog が v2.33.0 の変更として挙げる内容と、このページの記述のどこまでが同じ挙動かは**未確認**です。

## V2／V3 の適用範囲が未確認の変更

内蔵 changelog で `[V3]` の表記がない次の 5 項目は、V2 専用か V3 との両対応か、内蔵 changelog にも公式ドキュメントにも記載がありません。

| 項目 | 内蔵 changelog v2.33.0 | 適用範囲 | 公式ドキュメントでの確認 |
|------|------------------------|----------|------------------------|
| `grep` ツールの高速化（変更） | 大規模なプロジェクトで、ファイルを CPU コア全体で並列にスキャンする | 公式に記載なし（**未確認**） | 公式 [Built-in tools](https://kiro.dev/docs/reference/built-in-tools/)（Page updated: 2026-10-13）の `grep` の節に並列スキャンの記載は確認できなかった（**未確認**）。`grep` ツールは [05. Grep/Glob](05_GrepGlob.md) を参照 |
| Mermaid のサブグラフ（変更） | サブグラフを含む Mermaid のフローチャートが、ソースを表示せず、チャット内に描画される | 公式に記載なし（**未確認**） | 公式 [Terminal UI の Mermaid diagrams](https://kiro.dev/docs/cli/terminal-ui/#mermaid-diagrams)（Page updated: 2026-10-20）は、対応する図の種類（フローチャート・シーケンス図・状態遷移図・ER 図）と、未対応の構文ではソースを表示することを説明しているが、サブグラフの記載は確認できなかった（**未確認**）。Mermaid の導入は v2.31.1（→ [50. v2.31 新機能](50_v231NewFeatures.md)） |
| Mermaid のノード説明（バグ修正） | ノード説明が最大 4 行に折り返され、それより長いテキストは省略記号で示される | 公式に記載なし（**未確認**） | 上記の Terminal UI に折り返しの記載は確認できなかった（**未確認**） |
| ホームディレクトリでのグローバルエージェントの重複表示（バグ修正） | ホームディレクトリから Kiro を起動しても、グローバルのエージェントが 2 回表示されない | 公式に記載なし（**未確認**） | 公式 [Custom agents](https://kiro.dev/docs/custom-agents/)（Page updated: 2026-10-10）は、グローバルを `~/.kiro/agents/`、プロジェクトを `.kiro/agents/` に置くと説明している。重複表示の修正の記載は確認できなかった（**未確認**） |
| `/model ` の後の Tab 補完（バグ修正） | `/model ` の後に Tab を押すと、`set-current-as-default` をモデルピッカー内のモデルとして一覧せず、サブコマンドとして再び表示する | 公式に記載なし（**未確認**） | 公式 [Slash commands の `/model`](https://kiro.dev/docs/reference/slash-commands/#model)（Page updated: 2026-10-20）は `set-current-as-default` を `/model` のサブコマンドとして掲載しているが、Tab 補完の修正の記載は確認できなかった（**未確認**） |

## [V3] セキュリティ修正

| 内容（CLI 内蔵 changelog v2.33.0） | 公式ドキュメントでの確認 |
|----------------------------------|------------------------|
| [V3] サンドボックスのネットワーク規則が、ホスト名の大文字小文字に関係なく一致する | 公式 [Local command sandbox](https://kiro.dev/docs/sandbox/)（Page updated: 2026-10-15）は、`sandbox_network` ルールのパターンが大文字小文字を区別せず、完全一致のホスト名と `*.suffix` のワイルドカードに対応すると説明している。この説明は v2.33.0 の前から公式ページにあり、v2.33.0 の修正との関係は記載されていない（**未確認**）。サンドボックスは [50. v2.31 新機能](50_v231NewFeatures.md) を参照 |
| [V3] Windows で、hook コマンドが作業ディレクトリにある同名のプログラムを実行しない | 取得した公式ページの範囲では記載を確認できなかった（**未確認**）。Hook は [22. Hooks](22_Hooks.md) を参照 |

## バグ修正の要点（V3）

[V3] と表記された修正のうち、関連する公式ドキュメントが確認できたものを先に示します。

| 内容（CLI 内蔵 changelog v2.33.0） | 公式ドキュメントでの確認 |
|----------------------------------|------------------------|
| `chat.terminalTitle` が有効なとき、端末タイトルにセッションのタイトルが表示される | 実機 2.33.0 の `kiro-cli settings list --all` は `chat.terminalTitle` を「Set terminal window/tab title to current session info (boolean, default: false)」と表示する（公式 Settings リファレンスには掲載されていない）。公式 Slash commands の `/title` は、端末タイトルの機能を `/settings display` の **Terminal title** で有効にすると説明している。この 2 つが同じ設定かは記載がなく**未確認** |
| `/sessions` が、検索インデックスの追従中に数秒間固まらない | 公式 Slash commands は `/sessions` を V3 のセッションダッシュボードと説明している（V3 のみ）。修正そのものの記載は確認できなかった（**未確認**） |
| フォールバックモデルを `/model` ペインと `/model fallback` から再び設定できる | ⚠ 公式の記述と食い違いがあります。下の「公式間の食い違い」を参照 |
| `kiro-cli chat --agent <agent> @agent-sop:<name>` が、入力したテキストをそのまま送らず SOP を実行する。`--no-interactive` でも同様 | 取得した公式ページの範囲では `@agent-sop:` の記載を確認できなかった（**未確認**） |
| [V3] `/code` が、クラウドセッションでサンドボックスのワークスペースルートと `lsp.json` のパスを表示する。`code` ツールが Python などの応答の遅い言語サーバーの診断を報告する。`/code summary` が、コードインテリジェンスの概要からコードベースのドキュメントを生成する | 公式 Slash commands の `/code` の節は `init`・`overview`・`status`・`logs` を掲載し、`summary` の記載は確認できなかった（**未確認**）。ほかの 2 項目の記載も確認できなかった（**未確認**）。コードインテリジェンスは [01. LSP](01_LSP.md) を参照 |
| スロットリングエラーが、モデルの過負荷とユーザー自身のレート制限を区別して伝える | 公式 Settings リファレンスはスロットリング・5xx・接続切断を自動でバックオフ付きで再試行すると説明しているが、エラー表示の区別の記載は確認できなかった（**未確認**） |

次の修正は、関連する公式の記載を確認できませんでした（**未確認**）。

- [V3] Kiro が自発的に開始する返信（Workflow の完了後など）が、数語で途切れない
- [V3] `/agent`・`/model`・`/effort` が、入力途中の引数をインラインで再び補完する
- [V3] `permissions.yaml` のサンドボックスのネットワーク規則を編集すると、実行中のサンドボックスに適用される
- [V3] ホームディレクトリで `/sandbox` がグローバルのサンドボックス設定をプロジェクト設定として扱わない。そこでプロジェクト設定を変更しても、グローバル設定を上書きしたり削除したりしない
- [V3] 応答が返らないリクエストの後も、クラウド設定の同期が続く。クラウド設定が空のとき、セッションにクラウド設定の同期カードが表示されない
- [V3] Windows の Workflow が、ドライブ文字の大文字小文字が異なるレシピファイルを拒否しない
- [V3] Workflow の review loop が、レビュー担当が承認した時点で止まり、上限まで実行し続けない（review loop の一時停止は v2.32.0 → [51. v2.32 新機能](51_v232NewFeatures.md)）
- [V3] 組織が Auto モデルを無効にしていても、Workflow が失敗せずに実行される

### 公式間の食い違い（フォールバックモデルの設定）

- CLI 内蔵 changelog v2.33.0 は「[V3] フォールバックモデルを `/model` ペインと `/model fallback` から再び設定できる」と記載しています
- 公式 [Slash commands の `/model`](https://kiro.dev/docs/reference/slash-commands/#model)（Page updated: 2026-10-20）は、`/model fallback` が V1 と V2 に適用され、V3 のターミナル UI セッションでは、拒否や利用不可でターンが別のモデルに移ったことを transcript が報告する、と説明しています
- 公式ページの更新日は v2.33.0 の内蔵 changelog の日付と同じ 2026-10-20 で、どちらを新しいとも判断できません。本サイトは両方の記述を併記し、V3 で `/model fallback` が使えるかは**未確認**とします。V1／V2 の `/model fallback` は [46. v2.27 新機能](46_v227NewFeatures.md)、V3 の通知は [49. v2.30 新機能](49_v230NewFeatures.md) を参照してください

## 実機 2.33.0 で確認した事項

- `kiro-cli --version` は `kiro-cli 2.33.0` を表示する
- `kiro-cli version --changelog=2.33.0` が本ページの出典（28 項目）
- 実機で V3 セッションを起動する確認（フォルダの信頼確認、`/sandbox`、`/model fallback` など）は、今回していないため**実機では未確認**

## 関連リンク

### 本サイト

- [51. v2.32 新機能](51_v232NewFeatures.md)
- [50. v2.31 新機能](50_v231NewFeatures.md)
- [49. v2.30 新機能](49_v230NewFeatures.md)
- [05. Grep/Glob](05_GrepGlob.md)
- [17. Granular Tool Trust](17_GranularToolTrust.md)
- [22. Hooks](22_Hooks.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog（一覧）](https://kiro.dev/changelog/)（v2.33.0 は未掲載）
- [Permissions — Workspace trust](https://kiro.dev/docs/permissions/#workspace-trust)
- [New features in CLI V3](https://kiro.dev/docs/cli/v3/new-features/)
- [Workflows](https://kiro.dev/docs/workflows/)
- [Author workflows](https://kiro.dev/docs/workflows/authoring/)
- [Local command sandbox](https://kiro.dev/docs/sandbox/)
- [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)
- [Slash commands](https://kiro.dev/docs/reference/slash-commands/)
- [Built-in tools](https://kiro.dev/docs/reference/built-in-tools/)
- `kiro-cli version --changelog=2.33.0` / `kiro-cli settings list --all`（実機 2.33.0）

**最終更新**: 2026-10-21
**対象バージョン**: Kiro CLI v2.33.0（CLI 内蔵 changelog のみ。フォルダの信頼確認・Workflow の拡張・セキュリティ修正は V3 Early Access）
