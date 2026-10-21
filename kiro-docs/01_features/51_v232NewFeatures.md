[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.32 新機能

# 51. v2.32 新機能 — [V3] フォルダ単位の書き込み承認・非対話クラウドセッション・Workflow の計画プレビュー

## 概要

Kiro CLI **v2.32.0**（2026-10-15）では、V3 のセッションがファイルの書き込みを求めたとき、選んだ**フォルダ全体**を許可できるようになりました。V3 のクラウドセッションを**非対話実行**（`--cloud`／`--repo`）から使えるようになり、Workflow は**どのステップも実行される前に計画を表示**します。V3 の出力スタイルが 3 種追加され、Workflow の特定のステップで Powers と MCP サーバーを使えるようになりました。⚠ 動作が変わる項目として、V3 の Workflow はステップのセッションがタスクで開き、review loop が 2 回の却下で一時停止します。また、V2 のサブエージェントが親セッションのモデルフォールバック設定に従います。

- **変更（⚠）3 件**: Workflow ステップのセッション、Workflow の review loop、V2 のサブエージェントのモデルフォールバック
- **改善 11 件**: フォルダの書き込み承認、非対話のクラウドセッション、Workflow の計画プレビュー、承認スコープの表示、Workflow への平易な言葉での変更、Workflow ステップでの Powers と MCP、新しい出力スタイル、What's new での Memory の紹介、端末のプログラム状態（OSC 7501）、セッション一覧の更新、ネイティブライブラリの削減
- **バグ修正 18 件**

公式 Changelog（`changelog/cli/2-32/`）は 32 項目（Improvements 14／Fixes 18）、CLI 内蔵 changelog は 34 項目（Added 7／Changed 9／Fixed 18）で、件数と分類が異なります。内蔵の「Powers」と「MCP servers」は公式では 1 項目、内蔵の「`/workflow run` の確認フォーム」と「プロンプトから作る Workflow の計画表示」は公式では 1 項目にまとめられています。本ページは公式を正として書き、分類も公式に従います（詳細は[変更履歴の v2.32.0](../02_update/01_changelog.md#v2320-cli2026-10-15)の注記）。系列ページに Patches 節はなく、v2.32 系列の版は v2.32.0 のみです。

公式 Changelog の Learn more リンクが指す公式ドキュメントの本文を取得し、確認できた範囲を書いています。確認できなかった点は「未確認」と明記しています。公式 Workflows・Permissions ページは Kiro IDE・CLI・Web を扱うため、本ページには **CLI（V3）の記述だけ**を採っています。

## [V3] 書き込み承認でフォルダを許可する

V3 のセッションがファイルの書き込みの承認を求めたとき、選んだフォルダをこのセッションで許可できます。ワークスペース内のフォルダはワークスペーススコープも使え、ワークスペース外のフォルダはユーザースコープを使えます。そのフォルダ内への以降の書き込みは、`ask` または `deny` ルールが適用されない限り、この許可を再利用します（公式 Changelog v2.32.0）。

公式 [Permissions の Approval scopes in CLI V3](https://kiro.dev/docs/permissions/#approval-scopes-in-cli-v3)（Page updated: 2026-10-20）の説明:

- 書き込みの承認では **Allow a folder** を選ぶと、選んだフォルダとその下のすべてのフォルダへのアクセスを許可する。現在のセッションでは、対象にできる任意のフォルダを許可できる。ワークスペース内のフォルダはワークスペーススコープも使え、ワークスペース外のフォルダはユーザースコープを使える。以降の一致する書き込みは、`ask` または `deny` ルールが適用されない限り、この許可を再利用する
- 選んだフォルダは、保留中の書き込みのすべてのパスを含んでいなければならない。ワークスペース内のフォルダにはワークスペース相対パスを、ワークスペース外のフォルダにはフルパスを入力する。フォルダのパターン、`..`、`~` は受け付けられない

### Always Allow ページの承認スコープの表示（改善）

V3 の Always Allow ページが選択中のスコープを表示し、`s` を押すと session・workspace・user を切り替えられます（公式 Changelog v2.32.0）。公式 Permissions の説明:

- 選択肢（**Trust** の match scope）は、コマンドに応じて、完全一致のコマンド・任意の引数を許す基本コマンド・ツール全体の 3 つ（例: `git pull --rebase`、`git *`、`*`）
- ピッカーは既定で現在のセッションを使う。`s` を押すと、保存する前に永続化のスコープを **session**・**workspace**・**user** の間で切り替えられる
- session の承認はセッションが終わるまでメモリに保持される。workspace と user の承認は V3 の権限ストアに永続化される
- パイプや `&&` でつないだコマンドは、Kiro がそれぞれのコマンドを別々に評価する
- ⚠ どのスコープの `deny` ルールも、承認のプロンプトなしにコマンドをブロックする。セッションの信頼も別スコープの `allow` ルールも `deny` を上書きできない。明示的な `ask` ルールは毎回プロンプトを出し、永続的な **Always** の許可を提示しない

権限全般は [17. Granular Tool Trust](17_GranularToolTrust.md) も参照してください。

## 非対話実行の `--cloud`／`--repo`（改善）と関連する修正

V3 の非対話実行が `--cloud` と `--repo` に対応します。プレーンテキスト出力にクラウドセッション ID が出力されるため、後でそのセッションを再開または削除できます（公式 Changelog v2.32.0）。

公式 [Headless mode の Cloud sessions in V3](https://kiro.dev/docs/cli/headless/#cloud-sessions-in-v3)（Page updated: 2026-10-20）の説明:

- `--cloud` を付けると、V3 の非対話タスクをクラウドセッションで実行する。`--repo` で 1 つ以上のリポジトリから始められる。パイプで渡した指示は両方のフラグで使える
- プレーンテキスト出力はクラウドセッション ID を出力する。ID を保存しておくと、後でセッションを再開または削除できる

```bash
kiro-cli chat --v3 --no-interactive --cloud --repo owner/repository "Review the open pull request"
printf '%s\n' "Run the tests" | kiro-cli chat --v3 --no-interactive --cloud --repo owner/repository
kiro-cli chat --v3 --no-interactive --resume-id <SESSION_ID> "Continue the task"
kiro-cli chat --delete-session <SESSION_ID>
```

- 公式 [CLI commands](https://kiro.dev/docs/reference/cli-commands/)（Page updated: 2026-10-20）は `--cloud` を「V3 のセッションをマネージドのクラウドサンドボックスで実行する」と説明している
- 実機 2.33.0 の `kiro-cli chat --help` は、`--cloud` を「Run this session in a cloud sandbox (V3/KAS only), interactively or with --no-interactive」、`--repo` を「Repository to open in a cloud session, as name or owner/name (comma-separated for multiple). Only meaningful with --cloud」と表示する（公式の説明と一致）

### 関連するバグ修正

| 内容（公式 Changelog v2.32.0） | 公式ドキュメントでの確認 |
|-----------------------------|------------------------|
| [V3] 非対話実行でクラウドセッションを `--resume-id` で指定すると、空のローカルセッションを開始せず、そのセッションを再開する | 公式 Headless mode の上記の例と、公式 Cloud sessions の `kiro-cli --resume-id <session-id>` に記載あり。「空のローカルセッションを開始していた」点は changelog のみ |
| プレーンテキストの非対話実行が、ターンがキャンセルまたは拒否された理由、あるいはセッションを開始できなかった理由を説明する | 公式 Headless mode の「Plain-text failures and exit status」に同じ趣旨の記載あり |
| stdout が閉じられている場合に、非対話実行がターンを完了せず、非 0 で終了する | 公式 Headless mode の同じ節に「stdout が完了前に閉じた場合、Kiro は非 0 のステータスで終了する」と記載あり。終了コードの値は記載がない。公式 [Exit codes](https://kiro.dev/docs/reference/exit-codes/) にも該当する記載がなく、値は**未確認** |

非対話実行全般は [15. Exit Codes](15_ExitCodes.md)、クラウドセッションは [36. Cloud Sessions](36_CloudSessions.md) を参照してください。

## [V3] セッションアーカイブ

V3 の `/chat save` を `.zip` なしの名前で実行すると、そのファイルが zip のセッションアーカイブであることを表示します。V3 の `/chat load` は、保存後に改変されたセッションアーカイブについて説明します（公式 Changelog v2.32.0）。

公式 [Session management の From chat](https://kiro.dev/docs/cli/chat/session-management/#from-chat)（Page updated: 2026-10-20）の説明: V3 の `/chat save` は zip のセッションアーカイブを書き込む。`.zip` の名前を使う。拡張子を省いても、Kiro は保存したファイルを zip のアーカイブとして識別する。`/chat load` はアーカイブを検査し、保存後に改変されていた場合に説明する。CLI 2.x は JSON のセッションファイルを使い、読み込み時に `.json` の拡張子は省略できる。

```bash
/chat save backup.zip
/chat load backup.zip
```

## [V3] Workflows の拡張

公式 [Workflows](https://kiro.dev/docs/workflows/)（Page updated: 2026-10-20）は Kiro IDE・CLI・Web で共有されるページです。以下は CLI（V3）に関する記述です。

### 実行前の計画プレビュー（改善）

V3 の `/workflow run` のピッカーで選択すると、Workflow の開始前に計画プレビュー付きの確認フォームが開きます。プロンプトから Workflow を作成する場合も、どのステップも実行される前に承認用の計画が表示されます（公式 Changelog v2.32.0）。

公式 Workflows の「Start from the agent」の説明: V3 のセッションでは、Kiro がどのステップも実行する前に、提案する計画を承認のために表示する。開始前にステップとエージェントを確認できる。Kiro CLI V3 では、`/workflow run` のピッカーでレシピを選ぶと、計画プレビュー付きの確認フォームが開く。Kiro がプロンプトから Workflow を作る場合にも同じ承認の手順が出る。

### 実行中の Workflow への平易な言葉での変更（改善）

V3 の Workflow は、実行中に、残りのステップへの平易な言葉による変更を受け付けます（公式 Changelog v2.32.0）。公式 [Run and manage workflows の Revise work that has not started](https://kiro.dev/docs/workflows/manage/#revise-work-that-has-not-started)（Page updated: 2026-10-20）の説明:

- 実行中または一時停止中の Workflow は、すでに実行したノードを保ったまま、残りの最上位の計画を置き換えられる
- 完了済みの作業と、現在実行中の作業は変更されない
- ステップが実行中なら、Kiro は置き換えを次のステップの境界まで待機させる。実行中のステップがなければ（一時停止中を含む）、Kiro は置き換えをすぐに適用できる
- 修正後のツリー全体が、スキーマ・ID・ネスト・ステップ数・テンプレート・エージェント・watch の検証を通らなければならない。待機中の置き換えが検証に失敗すると、Kiro はそれを拒否して元の計画で続ける
- この公式ページが、変更の入力方法として「平易な言葉」と書いているかは確認できなかった（**未確認**）

### ステップでの Powers と MCP（改善）

V3 の Workflow のコーディング・計画・設計ステップが Powers を使えます。設計ステップは、設定済みの MCP サーバーも使えます（公式 Changelog v2.32.0）。公式 [Author workflows](https://kiro.dev/docs/workflows/authoring/)（Page updated: 2026-10-20）の説明: ステップのツールアクセスはエージェントの定義から決まる。同梱の `wf-planner`・`wf-coder`・`wf-design` エージェントはインストール済みの Powers を使える。同梱の `wf-design` エージェントは、設定済みの MCP サーバーも使える。無人のステップには範囲を絞ったエージェントを使い、Workflow を起動する前に各エージェントが意味する権限を確認することが勧められている。

### ⚠ review loop（変更）

V3 の Workflow の review loop が、レビューが 2 回却下されると一時停止し、続行方法を確認します（公式 Changelog v2.32.0）。公式 [Run and manage workflows の Review-loop decisions in V3](https://kiro.dev/docs/workflows/manage/#review-loop-decisions-in-v3)（Page updated: 2026-10-20）の説明: Workflow の review loop が作業を 2 回却下すると、Kiro は実行を一時停止する。親セッションが、もう 1 回レビューの機会を与えるか、先へ進むかを尋ねる。選択は、完了済みの作業を再実行せずに、残りのループを制御する。

### ⚠ ステップのセッションがタスクで開く（変更）

V3 の Workflow ステップのセッションが、親の会話のコピーではなく、そのステップのタスクで開きます（公式 Changelog v2.32.0）。公式 Workflows は「各ステップは、新しいコンテキストを持つ自分のセッションで動く」と説明しています。この説明は、親の会話のコピーで開く挙動からの変更点を述べたものではなく、v2.32.0 での変更そのものは公式ドキュメントで確認できませんでした（**未確認**）。

### Workflow に関するバグ修正

| 内容（公式 Changelog v2.32.0） | 公式ドキュメントでの確認 |
|-----------------------------|------------------------|
| [V3] 並列ブランチで一時停止した Workflow ステップが、成功または失敗を報告したときに終了する | 公式 Run and manage workflows に、一時停止したステップが `send_message` の `success`／`error` で進む旨の記載はあるが、並列ブランチの修正そのものの記載は確認できなかった（**未確認**） |
| [V3] エージェントの再起動中にバッファされた Workflow のメッセージが、再起動後も残る | 記載を確認できなかった（**未確認**） |
| [V3] 終了済みの Workflow ステップが、親へ追加情報を送れる | 記載を確認できなかった（**未確認**） |
| [V3] Workflow の一時停止メッセージが、実行が自動的に再開すると表示しない。実行を再開するとステップが再試行される | 記載を確認できなかった（**未確認**） |

## [V3] 出力スタイル（改善）

V3 の `/settings display` が **Proactive**・**Explanatory**・**Learning** の出力スタイルを選べるようになりました（公式 Changelog v2.32.0）。公式 [In-session settings の Output styles in V3](https://kiro.dev/docs/cli/chat/settings/#output-styles-in-v3)（Page updated: 2026-10-20）の説明:

- V3 のセッションで `/settings display` を実行し、**Output style** の行で応答の整え方を選ぶ。組み込みの選択肢に **Proactive**・**Explanatory**・**Learning** が含まれる。アクティブなエージェントが、Display メニューが開いたときに別の選択肢を提供することもある
- 選択はグローバルの `chat.outputStyle` として保存され、以降のプロンプトに適用される。エージェントの既定を選ぶとグローバルの上書きが外れる。ワークスペースレベルの `chat.outputStyle` の値は引き続き優先され、その場合、行はアクティブなワークスペースのスタイルを表示する
- 実機 2.33.0 の `kiro-cli settings list --all` は `chat.outputStyle` を「Prompt-scoped KAS response style (string)」と表示する

Output style の導入は [44. v2.25 新機能](44_v225NewFeatures.md) を参照してください。

## 端末のプログラム状態（OSC 7501）（改善）

OSC 7501 に対応する端末が、Kiro CLI がアイドル・作業中・完了・承認または回答の待機中・エラーによる停止のどれかを表示できます。`KIRO_NO_PROGRAM_STATUS` を設定すると無効にできます（公式 Changelog v2.32.0）。changelog に V2／V3 の記載はありません。

公式 [Terminal UI の Program status for supporting terminals](https://kiro.dev/docs/cli/terminal-ui/#program-status-for-supporting-terminals)（Page updated: 2026-10-20）の説明: Kiro CLI **V2 と V3** が、対話的な端末で OSC 7501 を通じて状態を報告する。対応する端末は、Kiro がアイドル、作業中、完了、承認または回答の待機中、エラーによる停止のどれかを表示できる。起動前に `KIRO_NO_PROGRAM_STATUS=1` を設定すると、この更新を無効にできる。本サイトは、changelog に記載がない V2／V3 の適用範囲を、公式 Terminal UI の記述から V2／V3 の両方と書いています。

```bash
KIRO_NO_PROGRAM_STATUS=1 kiro-cli chat
```

`KIRO_NO_PROGRAM_STATUS` は、公式 Terminal UI にだけ記載があり、公式 Settings リファレンスと CLI commands リファレンスには記載がありません（Page updated: それぞれ 2026-10-15、2026-10-20）。Terminal UI は [18. Terminal UI](18_TerminalUI.md) を参照してください。

## V2 のモデルフォールバック

### ⚠ サブエージェントが親のフォールバック設定に従う（変更）

V2 セッションから起動されたサブエージェントが、そのセッションのモデルフォールバック設定に従います（公式 Changelog v2.32.0）。

### ピッカーの None とベンダー既定の表示（バグ修正）

V2 の `/model` フォールバックピッカーで None を選ぶと、このマシンとプロファイルでフォールバックが off になります。ターゲットが未設定のとき、フォールバックの行は、拒否に応答するベンダー既定を名前で示します（公式 Changelog v2.32.0）。

公式 [Slash commands の `/model`](https://kiro.dev/docs/reference/slash-commands/#model)（Page updated: 2026-10-20）の「Model fallback (V1 and V2)」の説明:

- 現在のモデルがターンを拒否した場合、Kiro は設定したフォールバック、またはサービスが提供するフォールバックを試せる
- バックエンドが現在のモデルを利用不可とした場合、Kiro は設定したフォールバックだけを試せる
- V2 のセッションでは、フォールバックのピッカーで **None** を選ぶと、このマシンとプロファイルでフォールバックが off になる
- ターゲットが未設定のとき、フォールバックの行は、拒否に応答できるベンダー既定を名前で示す
- V2 のセッションから起動されたサブエージェントは、そのセッションのフォールバック設定に従う
- モデルは自分自身をフォールバックにできない
- `/model fallback` は V1 と V2 に適用される。V3 のターミナル UI セッションでは、拒否や利用不可でターンが別のモデルに移ったことを transcript が報告する（→ [49. v2.30 新機能](49_v230NewFeatures.md)）

`/model fallback` の導入は [46. v2.27 新機能](46_v227NewFeatures.md) を参照してください。

## MCP と起動画面

### [V3] 組織の MCP レジストリの `oauth`／`oauthScopes`（バグ修正）

V3 の、組織の MCP レジストリのサーバーが、レジストリの `oauth` と `oauthScopes` の設定を使うようになりました（公式 Changelog v2.32.0）。公式 [MCP Registry の OAuth for remote registry servers](https://kiro.dev/docs/mcp/registry/#oauth-for-remote-registry-servers)（Page updated: 2026-10-20）の説明:

- Kiro CLI V3 は、組織のレジストリが提供するリモートサーバーの `oauth` と `oauthScopes` の設定を使う
- 一致するレジストリの上書きは、ローカルの設定に対してそれらの値を置き換えられる。これらのフィールドの形式は、`mcp.json` のリモートサーバーと同じ
- 公式の同ページは、上書きできるフィールドとして、リモート（HTTP）サーバーの `headers`・`timeout`・`oauth`・`oauthScopes` を挙げている

MCP の OAuth 全般は [32. MCP OAuth Management](32_MCPOAuthManagement.md) を参照してください。

### 起動画面と OAuth リンク

| 内容（公式 Changelog v2.32.0） | 公式ドキュメントでの確認 |
|-----------------------------|------------------------|
| 起動時の What's new が Memory を紹介し、使用中のエンジンとメモリ設定に応じた次の手順を示す（改善） | 公式 [Memory](https://kiro.dev/docs/memory/)（Page updated: 2026-10-20）は Memory を説明しているが、起動時の What's new の記載は確認できなかった（**未確認**）。Memory は [48. v2.29 新機能](48_v229NewFeatures.md) を参照 |
| MCP OAuth のリンクがサーバーの接続時に消え、通知にサーバー名が表示される | 記載を確認できなかった（**未確認**）。OAuth の認可 URL の表示は v2.29.0 の項目（→ [48. v2.29 新機能](48_v229NewFeatures.md)） |

## そのほかの改善とバグ修正

| 内容（公式 Changelog v2.32.0） | 公式ドキュメントでの確認 |
|-----------------------------|------------------------|
| [V3] セッション一覧が、バックグラウンドのディレクトリスキャンを待たずにすぐ表示される（改善） | 記載を確認できなかった（**未確認**） |
| [V3] Kiro CLI が、ネイティブ画像ライブラリ `sharp` と `libvips` を同梱しなくなった（改善） | 記載を確認できなかった（**未確認**） |
| [V3] コマンド承認が、コマンドを実行するシェル向けにシェル構文を検査する。fish を含め、承認プロンプトがシェルによるコマンドの解析と一致する | 公式 Permissions の「Shell command parsing」節は、複合コマンドの分割と各コマンドの個別の評価を説明している。fish を含む、実行するシェルごとの構文検査の記載は確認できなかった（**未確認**） |
| ステージを開始できない V2 の crew が、永遠に待たず、そのステージのエラーで失敗する | 記載を確認できなかった（**未確認**） |
| [V3] モデルが出力予算をすべて推論に使っても、ターンが早く終わらない | 記載を確認できなかった（**未確認**） |
| [V3] プロバイダーが大きすぎるとして拒否した画像を、ターンを失敗させず、プロバイダーのサイズ上限で再試行する | 記載を確認できなかった（**未確認**） |
| [V3] 再開したセッションが、モデル一覧の読み込み前に、保存済みのモデルと effort を表示する | 記載を確認できなかった（**未確認**） |

修正項目の完全な一覧は [変更履歴の v2.32.0](../02_update/01_changelog.md#v2320-cli2026-10-15) を正とします。

## 関連リンク

### 本サイト

- [50. v2.31 新機能](50_v231NewFeatures.md)
- [52. v2.33 新機能](52_v233NewFeatures.md)
- [46. v2.27 新機能](46_v227NewFeatures.md)
- [44. v2.25 新機能](44_v225NewFeatures.md)
- [15. Exit Codes](15_ExitCodes.md)
- [17. Granular Tool Trust](17_GranularToolTrust.md)
- [18. Terminal UI](18_TerminalUI.md)
- [32. MCP OAuth Management](32_MCPOAuthManagement.md)
- [36. Cloud Sessions](36_CloudSessions.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.32](https://kiro.dev/changelog/cli/2-32/)
- [Permissions](https://kiro.dev/docs/permissions/)
- [Headless mode](https://kiro.dev/docs/cli/headless/)
- [Session management](https://kiro.dev/docs/cli/chat/session-management/)
- [In-session settings](https://kiro.dev/docs/cli/chat/settings/)
- [Workflows](https://kiro.dev/docs/workflows/)
- [Author workflows](https://kiro.dev/docs/workflows/authoring/)
- [Run and manage workflows](https://kiro.dev/docs/workflows/manage/)
- [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)
- [Slash commands](https://kiro.dev/docs/reference/slash-commands/)
- [MCP Registry](https://kiro.dev/docs/mcp/registry/)
- [Memory](https://kiro.dev/docs/memory/)
- `kiro-cli chat --help` / `kiro-cli settings list --all`（実機 2.33.0）

**最終更新**: 2026-10-21
**対象バージョン**: Kiro CLI v2.32.0+（フォルダ単位の書き込み承認・非対話クラウドセッション・Workflow の拡張・出力スタイルは V3 Early Access）
