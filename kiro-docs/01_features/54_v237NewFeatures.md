[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.35〜v2.37 新機能

# 54. v2.35〜v2.37 新機能 — Approve for me・V2 エージェントの自動アップグレード・ACP のサインインとエンジン選択・root 起動の警告

## 概要

Kiro CLI の **v2.35.0**（2026-10-27）から **v2.37.1**（2026-10-31）までの 3 つの系列と、その間のパッチ版（v2.34.1・v2.34.2・v2.35.1・v2.35.2・v2.37.1）をまとめた文書です。

- **v2.35.0**: root／Administrator で起動したときの警告（`app.warnOnElevatedPrivileges`）、[V3] が組織の MCP と Web ツールの設定に従う動作、fullscreen で長い回答からプロンプトへ戻る操作、[V3] の `/mcp` が組織のレジストリに隠されたサーバーを表示する動作
- **v2.36.0**（2026-10-29）: [V3] **Approve for me**（Kiro が定型的な操作を代わりに承認する）、サブコマンド単位の承認ルール、`kiro-cli agent upgrade` の権限の警告、`kiro-cli acp` のエンジンを選ぶ `acp.agentEngine`
- **v2.37.0**（2026-10-30）: [V3] の起動時に V2 形式のエージェントを自動でアップグレードする動作が既定で有効になった（⚠ 既定の動作の変更）、ACP クライアントのターミナルでのサインイン、Mermaid のノードの形状と入れ子の subgraph、`KIRO_RUNTIME_DIR`

> **出典**: 公式の Changelog [v2.35](https://kiro.dev/changelog/cli/2-35/)・[v2.36](https://kiro.dev/changelog/cli/2-36/)・[v2.37](https://kiro.dev/changelog/cli/2-37/)（表示日は各節のとおり）です。v2.37.0 と v2.37.1 は、CLI 内蔵 changelog（実機 `kiro-cli 2.37.1` の `kiro-cli version --changelog=all`）とも突き合わせました。実機は v2.36.0 以前の内蔵 changelog を保持しないため、それ以前は公式のみが出典です。

- **v2.37.1**: 項目 5 件（公式の Patches 節は分類しない）
- **v2.37.0**: 機能追加 2 件、改善 6 件、バグ修正 6 件（公式の主要節 2／Improvements 6／Fixes 6）
- **v2.36.0**: 機能追加 1 件、改善 8 件、バグ修正 3 件（公式の主要節 1／Improvements 8／Fixes 3）
- **v2.35.0**: 機能追加 2 件、改善 3 件、バグ修正 10 件（公式の主要節 2／Improvements 3／Fixes 10）
- **パッチ**: v2.35.2・v2.35.1・v2.34.2・v2.34.1 は各 1 件

changelog で `[V3]` の表記がない項目のうち、公式にも V2 専用か両対応かの記載がないものは、本ページで「未確認」と示します。

## root／Administrator での起動の警告（v2.35.0）

macOS と Linux で root として、Windows で Administrator として Kiro CLI を起動すると、警告が表示されます。ツール、shell コマンド、Hooks、MCP サーバーがその権限で動き、root 所有のファイルを作ったり、システムの設定を変えたりし得るためです。警告は何もブロックしません。

公式 [Settings リファレンス](https://kiro.dev/docs/reference/settings/)（Page updated: 2026-11-02）の `app.warnOnElevatedPrivileges` の説明は次のとおりです。

- 型は boolean で、**既定は on**
- **グローバル設定のみ**で、ワークスペースの `.kiro/settings/cli.json` では上書きできない
- 意図して昇格した権限で実行するときは、次のコマンドで止める

```bash
kiro-cli settings app.warnOnElevatedPrivileges false
```

実機 `kiro-cli 2.37.1` の `kiro-cli settings list --all` も、このキーを「Warn when execution sessions run as root or Administrator (boolean, default: true)」と表示します。警告そのものの表示は、root での起動を実機で試していないため**実機では未確認**です。

## [V3] 組織の MCP と Web ツールの設定に従う（v2.35.0）

V3 のセッションが、組織の Kiro 設定に従って、MCP サーバーと `web_search`・`web_fetch` ツールを有効・無効にします。changelog に記載があるのはこの 1 文だけで、組織の設定を管理する画面や設定項目は、取得した公式ドキュメントの範囲では確認できませんでした（**未確認**）。

## fullscreen で長い回答からプロンプトへ戻る（v2.35.0）

TUI で長い回答までスクロールすると、最上行にその回答のプロンプトの最初の行が表示されます。その行をクリックするとプロンプトへ戻れます。公式 [Fullscreen](https://kiro.dev/docs/cli/fullscreen/)（Page updated: 2026-10-30）の説明は次のとおりです。

- 対象は **TUI** で、その回答のプロンプト自体が画面の最上部に来ると、この行は消える
- 行の上をドラッグすると、ジャンプではなくテキストの選択になる

Fullscreen の全体は [41. v2.22 新機能](41_v222NewFeatures.md) を参照してください。

## [V3] レジストリが隠した MCP サーバーの表示（v2.35.0）

組織が MCP レジストリを有効にしていると、レジストリにないサーバーは起動しません。V3 の `/mcp` は、レジストリが隠した設定済みのサーバーを一覧し、レジストリが提供するサーバーを宣言する方法を示します。公式 [MCP registry](https://kiro.dev/docs/mcp/registry/)（Page updated: 2026-10-30）の説明は次のとおりです。

- Kiro CLI の V3 では、名前が一致するだけでは足りない。`mcp.json` のエントリが `{"type": "registry"}` として宣言されているときだけ、そのサーバーが動く。レジストリの名前と一致していても、独自の `command` や `url` を持つエントリはスキップされる（公式の `.md` 版ではこのコード片が空になるため、HTML 版で確認した）
- `kiro-cli mcp list` は、これらのサーバーを有効ではなく「スキップ」と示す（v2.35.0 の修正）

MCP の設定は [32. MCP OAuth Management](32_MCPOAuthManagement.md) を参照してください。

## [V3] Approve for me（v2.36.0）

対話型の V3 セッションで、Kiro が定型的な操作を代わりに承認します。Kiro は、安全と判断した操作を承認し、危険と判断した操作をブロックし、判断できないときは利用者に尋ねます。公式 [V3 Permissions の Approve for me](https://kiro.dev/docs/cli/v3/permissions/#approve-for-me)（Page updated: 2026-10-31）の説明は次のとおりです。

- 対象は **Kiro CLI 2.36 以降の、対話型のローカル V3 セッション**。`/permissions` はクラウドセッションでは使えない
- `/permissions` → **Policies** で **approve for me** を選ぶ。この選択肢は、Approve for me が使えるセッションにだけ表示される。使えないセッションでは、Policies のページがその旨を示し、Kiro は尋ね続ける
- 選択は**ワークスペース単位**で、`approve-for-me` のポリシープリセットが、ワークスペースの権限ファイル（`~/.kiro/workspace-roots/<hash>/permissions.yaml`）に追加される

```yaml
policies:
  - approve-for-me
```

- 承認した各操作は、ツールカードに **Approved for you** と表示され、オンの間はステータス行に **Approve for me** が表示される
- 権限のルールの評価順は deny > ask > allow > **evaluate** で、`evaluate` はこのプリセットが加える最も弱い効果。既存の deny・ask・allow のルールが先に判定し、Approve for me は、ルールで決まらない操作だけを扱う。プリセットは、ワークスペース内の読み取りと書き込み、読み取り専用の shell コマンドを、判定を待たずに許可する
- オフにするには、`/permissions` → **Policies** → **ask for approval** を選ぶ。ユーザーの `~/.kiro/settings/permissions.yaml` にプリセットを書いていた場合は、手で削除する
- 確認するには、`/permissions` → **Policies** で **approve for me** が `[active]` と表示されるか見る

サブコマンドを直接指定する形式は、公式 [Slash commands の `/permissions`](https://kiro.dev/docs/reference/slash-commands/#permissions)（Page updated: 2026-10-30）に、`/permissions policies approve-for-me`（プリセットを追加）と `/permissions policies ask-for-approval`（プリセットを削除）として載っています。`/permissions policies` は Policies のページを開き、現在の選択に `[active]` が付きます。

**セキュリティ上の注意**（公式の記載）:

- オンの間、Kiro は、ルールで決まらないワークスペース内の shell コマンドなどを、尋ねずに実行し得る
- 公式は、Approve for me が各操作の判定に **Claude Sonnet 4.6** を使うと説明している（記載時点の動作）
- `--trust-all-tools` や `/tools trust-all` は、deny されない操作をすべて信頼するが、Approve for me は操作をブロックしたり尋ねたりできる点で異なる
- セキュリティ統制の代わりにはならない。実行させたくない操作には `deny` のルールを残し、[ローカルコマンドサンドボックス](50_v231NewFeatures.md)を併用して、承認されたコマンドの到達範囲も制限する
- ワークスペースの外のファイル操作は Approve for me の判定対象外で、既存の承認プロンプトが出る。信頼の分類器（trust classifier）が使えないときは、プリセットはルールを追加せず、Kiro は尋ね続ける

権限の全体は [17. Granular Tool Trust](17_GranularToolTrust.md)、V3 の承認の経緯は [43. v2.24 新機能](43_v224NewFeatures.md)・[51. v2.32 新機能](51_v232NewFeatures.md) を参照してください。

## [V3] サブコマンド単位の承認ルール（v2.36.0）

V3 のセッションが shell コマンドの承認を求めるとき、ルールの選択肢に最大 3 つの階層が並びます。公式 [V3 Permissions の Approval rule tiers](https://kiro.dev/docs/cli/v3/permissions/#approval-rule-tiers)（Page updated: 2026-10-31）の説明は次のとおりです。

| 階層 | `git stash pop` の例 | 範囲 |
|------|---------------------|------|
| 完全一致 | `git stash pop` | 書かれたとおりのコマンドだけ |
| サブコマンド（v2.36.0 で追加） | `git stash *` | コマンドの先頭 2 語と、任意の引数 |
| パターン | `git *` | 基底のコマンドと、任意の引数 |

- サブコマンドの階層は、コマンドの 2 語目が `stash` や `Makefile` のような、記号でも `sudo`／`env` でもない語（公式の表現は plain word）で、コマンド自体と異なるときに現れる
- `sudo` や `env` のような権限・環境のラッパーで始まるコマンド、または環境変数の代入で始まるコマンドには、サブコマンドもパターンも提示されない
- 同じ操作を繰り返す（`git stash` など）ならサブコマンドの階層を、コマンド全体を信頼するならパターンの階層を選ぶ

## `kiro-cli agent upgrade` の権限の警告（v2.36.0）

アップグレード後の V3 のルールが、V2 で許可されていたものを拒否・非表示・承認要求にするときに、警告が出ます。公式 [Upgrading agent configs](https://kiro.dev/docs/cli/v3/upgrade-agent/)（Page updated: 2026-11-02）の説明は次のとおりです。

- Kiro CLI 2.36 以降の `kiro-cli agent upgrade` は、結果の表で、アップグレードしたファイルごとに `(N warnings)` を示す。`--dry-run` でも警告が出る
- v2.36.0 で加わった警告は 3 つで、いずれも「V2 で許可されていたものを、V3 のルールが拒否・非表示・承認要求にする」権限の食い違いを示す

| 警告 | 意味 | 対処 |
|------|------|------|
| `deny-by-default-trusted-shell` | `allowedTools` が shell を信頼していたため V2 は全コマンドを実行した。V3 は `allowedCommands` にないコマンドを拒否する | `denyByDefault` を外すか、`allowedTools` から `shell` を外して許可するコマンドを列挙する |
| `hidden-tool` | deny がツールのできることをすべて覆うため、V3 はそのツールをエージェントから外す | deny を狭めるか、許可するコマンドやパスを追加する |
| `allow-read-only-dropped` | `allowReadOnly` で V2 は任意のファイルを尋ねずに読めたが、V3 にはそれに当たるルールがなく、ワークスペース外の読み取りは尋ねる | `allowedTools` で read ツールを信頼するか、`allowedPaths` にパスを追加する |

- V3 のセッションも、V2 で許可されていたものをルールがブロックするエージェントごとに、セッションにつき 1 回、V2 へ戻る方法とともに通知する

関連: [34. /upgrade-agent](34_v214UpgradeAgent.md)

## [V3] V2 エージェントの自動アップグレードが既定で有効に（v2.37.0）⚠ 既定の動作の変更

V3 のセッションの開始時に、V2 形式のエージェントを V3 形式へ自動でアップグレードします。公式 [Upgrading agent configs の Automatic upgrade when V3 starts](https://kiro.dev/docs/cli/v3/upgrade-agent/)（Page updated: 2026-11-02）の説明は次のとおりです。

- **Kiro CLI 2.37 以降**で、`chat.enableAutoAgentUpgrade` が**未設定**のときも起動時の移行が動く。2.37 より前は、未設定のとき、起動時の移行は自動では動かなかった。明示的な `false` は、これまでどおり無効のまま
- 対象は、ワークスペースの `.kiro/agents/` とグローバルの `~/.kiro/agents/`。`KIRO_AGENT_CONFIG_DIR` を設定している場合は、そのディレクトリだけを走査し、ワークスペースの走査は行わない。ほかのディレクトリは走査しない
- 各ファイルは、書き換える前に `<ファイル名>.json.bak` へ複製される。すでに V3 形式または universal 形式のエージェントはスキップされる
- 走査したディレクトリの `.json` がシンボリックリンクなら、Kiro はリンクをたどり、ディレクトリの外にあるリンク先でも書き換える（公式が注意している点）
- 設定は**グローバルのみ**で、ワークスペースの `.kiro/settings/cli.json` では上書きできない
- V2 のままにするには、次のコマンドを実行する。この場合、対話型の V3 の起動で、まだアップグレードが必要なエージェントの数を示す通知が表示される

```bash
kiro-cli settings chat.enableAutoAgentUpgrade false
```

- アップグレードしたエージェントは、`/upgrade-agent diagnostics` で Universal agents として確認できる

実機 `kiro-cli 2.37.1` の `kiro-cli settings list --all` は、このキーを「Auto-upgrade V2 agent configs, workspace and global, to the V3 format on V3 launches (boolean, default: true). When false, interactive V3 launches show a notice while any are pending.」と表示します。実機で V3 を起動して自動アップグレードが動く様子は確認していないため、**実機では未確認**です。

⚠ 共有している、またはバージョン管理しているエージェントのファイルは、V3 の起動で書き換わります。変換を 1 件ずつ確認してから反映したい場合は、`false` にします。

関連: [34. /upgrade-agent](34_v214UpgradeAgent.md)・[47. v2.28 新機能](47_v228NewFeatures.md)・[48. v2.29 新機能](48_v229NewFeatures.md)

## ACP のサインインとエンジン選択（v2.36.0・v2.37.0）

### ACP クライアントからのサインイン（v2.37.0）

`kiro-cli acp` がサインアウト状態で起動したとき、ターミナル認証を宣言する ACP クライアントは、ターミナルから Kiro にサインインできます。公式 [ACP の Sign in from an ACP client](https://kiro.dev/docs/cli/acp/#sign-in-from-an-acp-client)（Page updated: 2026-11-02）の説明は次のとおりです。

- Kiro CLI 2.37 以降で、サインアウト中に `kiro-cli acp` が起動すると、クライアントの `initialize` リクエストに認証方法を 1 つ返し、サインインするまで、ほかのリクエストには認証が必要というエラーを返す
- クライアントが `initialize` でターミナル認証を宣言していれば、**Log in to Kiro** という名前の方法が提示され、選ぶとクライアントが開くターミナルで Kiro のサインインが走る。宣言の形式は次の 3 つのどれでもよい: `clientCapabilities.auth.terminal: true`、標準化前の `clientCapabilities._meta["terminal-auth"]: true`、ACP v2 の `capabilities.auth.terminal` オブジェクト
- 宣言しないクライアントには、`kiro-cli login` を自分で実行するよう求める方法が提示される
- サインインの後でクライアントから再接続すると、新しい `kiro-cli acp` のプロセスが認証情報を見つけてエージェントを起動する。確認するには、セッションを作成し、`session/new` が認証エラーではなく成功することを見る

### `kiro-cli acp` のエンジンを選ぶ（v2.36.0）

新しい `acp.agentEngine` 設定が、ACP セッションのエンジンを選びます。公式 [ACP の Choose the engine](https://kiro.dev/docs/cli/acp/#choose-the-engine)（Page updated: 2026-11-02）と [Settings リファレンス](https://kiro.dev/docs/reference/settings/)（Page updated: 2026-11-02）の説明は次のとおりです。

- 値は `v1`・`v2`・`v3`。`--agent-engine` フラグが設定より優先され、どちらもなければ `kiro-cli acp` は `v2` で動く
- `chat.agentEngine` は `kiro-cli chat` に適用され、`kiro-cli acp` のエンジンは変えない

```bash
kiro-cli settings acp.agentEngine v3
kiro-cli settings acp.agentEngine   # 保存した値の確認
```

実機 `kiro-cli 2.37.1` では、`kiro-cli acp --help` が `--agent-engine <ENGINE>`（"v1", "v2", or "v3"。`acp.agentEngine` 設定を上書きし、どちらもなければ v2）と `--auth-method <METHOD>` を表示します。一方、`kiro-cli settings list --all` の `acp.agentEngine` の説明は「'v2' (default) or 'v3'」で、公式の 3 値（`v1`・`v2`・`v3`）と書き方が異なります。公式を正とし、`v1` を `acp.agentEngine` に設定したときの動作は実機で確かめていないため**未確認**です。

V3 の ACP クライアントの移行は [13. ACP](13_ACP.md) と、公式 [Migrate an ACP client to CLI V3](https://kiro.dev/docs/cli/v3/acp-migration/) を参照してください。

## Mermaid 図の描画（v2.36.0・v2.37.0）

- **v2.36.0**: Mermaid 図が、`title:` と図全体の注記を描画の上に表示する
- **v2.37.0**: フローチャートがノードの形状（決定のひし形、スタジアム、角丸、二重の枠）と種類の色を保つ。入れ子の `subgraph` は、ソースの表示ではなく、入れ子の枠として描画され、ノードに `Group 1` のようなグループの印が付く。長いラベルは狭い端末に収まるよう折り返される

公式 [Terminal UI の Mermaid diagrams](https://kiro.dev/docs/cli/terminal-ui/#mermaid-diagrams)（Page updated: 2026-11-02）は、2.37 より前は入れ子の subgraph で Kiro がソースを表示したこと、`classDef`・`style`・`linkStyle` は読み飛ばされ色はテーマから決まることを説明しています。Mermaid の基本は [50. v2.31 新機能](50_v231NewFeatures.md)、2.33 での拡張は [52. v2.33 新機能](52_v233NewFeatures.md) を参照してください。

## `KIRO_RUNTIME_DIR`（v2.37.0）

`KIRO_RUNTIME_DIR` に**絶対パス**を設定すると、Kiro の同梱ランタイムを、ホームディレクトリではなくそのパスへ展開します。公式 [CLI commands の環境変数](https://kiro.dev/docs/reference/cli-commands/)（Page updated: 2026-11-02）は、相対パスの値は無視されると、[Setup のトラブルシューティング](https://kiro.dev/docs/cli/setup/)（Page updated: 2026-11-02）は、空の値も無視されると説明しています。CloudShell のようにホームディレクトリの容量が小さい環境で、同梱ランタイムがホームを埋めるときに使います。設定した後は、`kiro-cli chat` を起動して、そのディレクトリにランタイムができたことを確認します。

## 承認プロンプトと画面の変更

| 版 | 変更 | 公式ドキュメントでの確認 |
|----|------|------------------------|
| v2.37.0 | [V3] メインチャットの承認プロンプトは、複数行のコマンドの先頭の 1 行だけを表示し、`Ctrl+O` で残りを表示する | 公式 [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/) のキー一覧に `Ctrl+O` は「ツール出力と thinking の展開・折りたたみ」とある。承認プロンプトでの扱いの記載は確認できなかった（**未確認**） |
| v2.37.0 | [V3] 承認ルールのページが、スコープの選択肢を `s` のヒントとともに強調し、ツール全体の行がツール名（Shell など）を示す | 公式 [Permissions](https://kiro.dev/docs/permissions/)（Page updated: 2026-10-31）に、ルールの選択画面の階層表（Entire tool など）と、`s` で保存先のスコープ（session／workspace／user）を切り替える説明はある。v2.37.0 の「強調」と「ツール名を示す」変更そのものの記載は確認できなかった（**未確認**） |
| v2.37.0 | Kiro の ghost が待機中も本来の色を保ち、コマンドメニューやパネルが開いている間もホーム画面に残る（v2.35.0 で、元の ghost が起動時に迎え、会話の中にも残るようになった） | 取得した公式ページの範囲では記載を確認できなかった（**未確認**） |
| v2.36.0 | `/fullscreen` で Kiro のロゴの ghost をクリックすると、5 つのアニメーションの次が再生される | 取得した公式ページの範囲では記載を確認できなかった（**未確認**） |
| v2.36.0 | [V3] `/spec` の要件の質問が進捗の件数を表示する | 取得した公式ページの範囲では記載を確認できなかった（**未確認**） |
| v2.36.0 | [V3] ツールの reasoning と引数を表示する設定のとき、shell ツールカードがモデルの説明を題名にし、コマンドをその下に表示する | 取得した公式ページの範囲では記載を確認できなかった（**未確認**） |
| v2.36.0 | V2 セッションで、`GIT_CONFIG_GLOBAL` のような環境変数で git の設定を変える shell コマンドは、実行前に承認を求める | 取得した公式ページの範囲では記載を確認できなかった（**未確認**）。V2 の権限は [17. Granular Tool Trust](17_GranularToolTrust.md) を参照 |

## パッチ版

| 版 | 日付 | 内容 | 補足 |
|----|------|------|------|
| v2.37.1 | 2026-10-31 | 起動時の通知・エージェントの welcome 行・What's new が題名と詳細を分けて表示される。V3 の welcome 画面は、ドキュメントへのリンクとコマンドを題名の下にまとめ、起動時のヒントを表示しない。`/fullscreen` の最下部ボタンがホバーで変わり、新着でドットが緑になる。[V3] 出力上限で打ち切られた回答でその旨を示し、続きを頼むよう案内する。macOS・Linux でアイドル時の V3 セッションの CPU 使用が減る。[V3] この版で開始した V3 セッションは、後の更新後もサインインが維持される | 内蔵 changelog は 4 項目で、サインインの維持を含まない。公式の記述に合わせた |
| v2.35.2 | 2026-10-28 | autocomplete のデスクトップアプリの廃止を段階的に展開する。より多くの macOS のデスクトップアプリのインストールが、次の更新確認でスタンドアロンの Kiro CLI に切り替わり、元へ戻すコマンドを示す起動時の通知が出る | 展開の対象や条件は公式に記載がなく**未確認** |
| v2.35.1 | 2026-10-28 | 性能の改善を含む | 改善の内容は公式に記載がない |
| v2.34.2 | 2026-10-26 | 対象となるすべてのユーザーに、対話型の V2 チャットの開始時に V3 の案内を表示する | 「対象となる」条件は公式に記載がなく**未確認**。V3 への切替の案内は [47. v2.28 新機能](47_v228NewFeatures.md)・[49. v2.30 新機能](49_v230NewFeatures.md) を参照 |
| v2.34.1 | 2026-10-26 | 空行を含む待ち行列のメッセージが、アクティビティトレイと Workflow モニターで 1 件の保留メッセージとして数えられ、表示される | Workflow は [53. v2.34 新機能](53_v234NewFeatures.md) を参照 |

## バグ修正の要点

### v2.37.0

| 内容 | 公式ドキュメントでの確認・適用範囲 |
|------|----------------------------------|
| `--no-interactive` の実行が、エージェントが見つからず止まったとき、別のエージェントにフォールバックしたとは伝えず `stopping (exit 4)` と表示する。V3 で V2 形式のエージェントを名指しして止まったときは、`kiro-cli agent upgrade <directory>` を案内する | 公式 [Exit codes の Requested agent not found](https://kiro.dev/docs/reference/exit-codes/#requested-agent-not-found)（Page updated: 2026-11-02）が、終了コード 4 の条件と、この表示を説明している。終了コードは [15. Exit Codes](15_ExitCodes.md) を参照 |
| macOS で `kiro-cli update` が `brew upgrade --cask kiro-cli` を案内する（cask は `--greedy` なしでアップグレードできる） | 公式 [Installation](https://kiro.dev/docs/getting-started/installation/) に `brew upgrade --cask kiro-cli` の記載がある |
| fullscreen がプロンプトを最下部の行に保つ（transcript が短いとき、`Ctrl+L` の後） | 取得した公式ページの範囲では記載を確認できなかった（**未確認**）。**V2／V3 の適用範囲も未確認** |
| fullscreen でのクリック（最下部へ戻るボタンを含む）が、上の行が折り返されていても、クリックした行に当たる | 同上（**未確認**） |
| AWS CloudShell や古い tmux の端末で、`/fullscreen` のマウスホイールによるスクロールが動く | 公式 [Fullscreen](https://kiro.dev/docs/cli/fullscreen/) に tmux の設定の説明はあるが、この修正の記載は確認できなかった（**未確認**） |
| [V3] `/spec` のプロンプト、レビューコメント、`/spec view` の要約が、spec の本文にあるエスケープシーケンスを出力しない | 取得した公式ページの範囲では記載を確認できなかった（**未確認**）。内蔵 changelog はこれを security に分類している |

### v2.36.0

| 内容 | 公式ドキュメントでの確認・適用範囲 |
|------|----------------------------------|
| [V3] 承認プロンプトのルール行が、長いパスのファイル名を途中で切らずに保つ | 取得した公式ページの範囲では記載を確認できなかった（**未確認**） |
| 非 ASCII の名前を持つ、利用できない MCP ツールを列挙するエージェント設定を、クラッシュせず読み込む | 取得した公式ページの範囲では記載を確認できなかった（**未確認**）。**V2／V3 の適用範囲も未確認** |
| 折り返されたツールコマンドのインデントされた行が、狭い端末で空の行にならず、テキストを保つ | 同上（**未確認**） |

### v2.35.0

| 内容 | 公式ドキュメントでの確認・適用範囲 |
|------|----------------------------------|
| V2 セッションで Auto を選んでいるときに、拒否された応答でターンが終わっていたのを、ターンを再試行して別のモデルが答えるようにする。V2 のモデルフォールバックが、拒否された応答にツール呼び出しが含まれるときに止まらない | V2 セッションの修正。モデルフォールバックは [52. v2.33 新機能](52_v233NewFeatures.md)・[46. v2.27 新機能](46_v227NewFeatures.md) を参照 |
| [V3] ツールの結果の直後にモデルが出力なしで拒否したとき、V3 セッションがループせずターンを終える | 取得した公式ページの範囲では記載を確認できなかった（**未確認**） |
| [V3] V2 のセッションを再開したとき、エージェント `default` が見つからないという警告を出さず、planner を落とさない。[V3] Linux で、再起動後に V3 セッションを再開しても、別の端末で開かれているとは報告しない | セッションの再開は公式 [Session management](https://kiro.dev/docs/cli/chat/session-management/) を参照。個々の修正の記載は確認できなかった（**未確認**） |
| `/chat` または `--resume` が大きなセッション履歴を一覧するとき、タイムアウトを報告するまで 10 秒ではなく最大 30 秒待つ | 取得した公式ページの範囲では記載を確認できなかった（**未確認**）。**V2／V3 の適用範囲も未確認** |
| 音声入力の「scratch that」のようなコマンドや Backspace の連打が、チャットのプロンプトと検索欄でテキストを削除する | 音声入力は [37. Voice Mode](37_VoiceMode.md) を参照。この修正の記載は確認できなかった（**未確認**）。**V2／V3 の適用範囲も未確認** |
| [V3] `kiro-cli mcp list` が、スキップされたレジストリのサーバーを有効と表示しない | 公式 MCP registry が「スキップとして示す」と説明している（上の節） |
| [V3] プロトコルの確認に HTTP 403 で答える HTTP の MCP サーバーに接続できる。[V3] 要求されたオフセットがファイルの末尾を過ぎているとき、`read_file` が存在しないと報告しない | 取得した公式ページの範囲では記載を確認できなかった（**未確認**） |

## 古い系列で漏れていたパッチ版

今回の点検（公式の全系列と本サイトの突き合わせ）で、前回までの反映から漏れていた 2 版を履歴に追加しました。

- **v2.19.2**（2026-08-25）: 22 項目。非対話モードの `--output-format stream-json`（V2 と V3）、[V3] MCP OAuth の URL 指定と登録済みコールバック URL への対応、[V3] エージェント設定の自動アップグレードの提案、サブエージェントの `/tools trust-all` の継承、端末のエスケープシーケンスによる TUI の表示の乱れの修正（V2 と V3）、[V3] Windows の `cmd` の解析が fail closed になる修正ほか（[変更履歴](../02_update/01_changelog.md#v2192-cli2026-08-25)）
- **v2.20.2**（2026-08-31）: 2 項目。アンケートが毎セッション出る問題の修正と、[V3] で再開したチャットがツール結果の内容と書式を保持する修正（[変更履歴](../02_update/01_changelog.md#v2202-cli2026-08-31)）

## 実機で確認した事項

- `kiro-cli --version` は `kiro-cli 2.37.1` を表示する
- `kiro-cli version --changelog=all` が保持するのは 2.37.0 と 2.37.1 だけ。`--changelog=2.36.0`・`2.35.0`・`2.34.2` は「No changelog information available」を返す
- `kiro-cli settings list --all` に `app.warnOnElevatedPrivileges`・`acp.agentEngine`・`chat.enableAutoAgentUpgrade`・`chat.agentEngine`・`chat.workflowLaunch` が表示される
- `kiro-cli acp --help` に `--agent-engine <ENGINE>` と `--auth-method <METHOD>` が表示される
- `kiro-cli agent upgrade --help` に `--no-backup` と `--dry-run` が表示される
- 次は実機で動作を確かめていないため**実機では未確認**: root での起動の警告、Approve for me（`/permissions` の Policies）、V3 の起動時の自動アップグレード、ACP のターミナルでのサインイン、Mermaid の入れ子の subgraph、`KIRO_RUNTIME_DIR`

## 関連リンク

### 本サイト

- [53. v2.34 新機能](53_v234NewFeatures.md)
- [52. v2.33 新機能](52_v233NewFeatures.md)
- [34. /upgrade-agent](34_v214UpgradeAgent.md)
- [17. Granular Tool Trust](17_GranularToolTrust.md)
- [13. ACP](13_ACP.md)
- [15. Exit Codes](15_ExitCodes.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [設定リファレンス](../04_reference/01_settings.md)
- [CLI コマンドリファレンス](../04_reference/03_cli-commands.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.37](https://kiro.dev/changelog/cli/2-37/)
- [Kiro CLI Changelog v2.36](https://kiro.dev/changelog/cli/2-36/)
- [Kiro CLI Changelog v2.35](https://kiro.dev/changelog/cli/2-35/)
- [V3 Permissions — Approve for me](https://kiro.dev/docs/cli/v3/permissions/#approve-for-me)
- [Upgrading agent configs](https://kiro.dev/docs/cli/v3/upgrade-agent/)
- [ACP — Sign in from an ACP client](https://kiro.dev/docs/cli/acp/#sign-in-from-an-acp-client)
- [Settings リファレンス](https://kiro.dev/docs/reference/settings/)
- [MCP registry](https://kiro.dev/docs/mcp/registry/)
- [Fullscreen](https://kiro.dev/docs/cli/fullscreen/)
- [Terminal UI — Mermaid diagrams](https://kiro.dev/docs/cli/terminal-ui/#mermaid-diagrams)
- `kiro-cli version --changelog=all` / `kiro-cli settings list --all` / `kiro-cli acp --help` / `kiro-cli agent upgrade --help`（実機 2.37.1）

**最終更新**: 2026-11-03
**対象バージョン**: Kiro CLI v2.37.1（v2.35.0〜v2.37.1 とその間のパッチ版。Approve for me・V2 エージェントの自動アップグレード・MCP registry の表示は V3 Early Access）
