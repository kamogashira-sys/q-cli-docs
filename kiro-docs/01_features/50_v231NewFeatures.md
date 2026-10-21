[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.31 新機能

# 50. v2.31 新機能 — [V3] ローカルコマンドサンドボックスと autonomous モード

## 概要

Kiro CLI **v2.31.0**（2026-10-13）では、V3 のローカルセッションで **ローカルコマンドサンドボックス**（`/sandbox`）と **ローカル autonomous モード**（`/autonomous`）がすべての V3 ユーザーに提供されました。あわせて、V3 が MCP ツールの定義を必要なときにだけ読み込むようになり、`KIRO_HOME` が V3 のグローバル設定・サインイン・セッション・エージェント状態に適用されるようになりました。**v2.31.1**（2026-10-14）では、エージェントの返信内の **Mermaid 図**がチャットに描画されるようになり、保存済みの設定が V3 の非対話実行で効くようになりました。v2.31.1 は専用ページ（`changelog/cli/2-31-1/`、HTTP 200）を持ちます。

- **v2.31.0**: 機能追加 2 件（`/sandbox`、`/autonomous`）、⚠ 変更 2 件（`KIRO_HOME`、保存済み `sandbox.json` の V3 ヘッドレス実行への適用）、改善 1 件（オンデマンドの MCP ツール）、バグ修正 7 件
- **v2.31.1**: 改善 1 件（Mermaid 図）、バグ修正 9 件

公式 Changelog の Learn more リンクが指す公式ドキュメントの本文を取得し、確認できた範囲を書いています。確認できなかった点は「未確認」と明記しています。公式 Local command sandbox ページは Kiro IDE と Kiro CLI の両方を扱うため、本ページには **CLI の記述だけ**を採っています。

## [V3] ローカルコマンドサンドボックス（`/sandbox`）

`/sandbox` は、エージェントが実行する shell コマンドと、その子プロセスを、オペレーティングシステムのサンドボックスの中に置きます（公式 Changelog v2.31.0）。外向きのネットワークアクセスを、ブロック・よく使われる開発用ホストに限定・開放のいずれにするかを選べます。ローカルの stdio MCP サーバーを同じサンドボックスの中で実行することもできます。

公式 [Local command sandbox](https://kiro.dev/docs/sandbox/)（Page updated: 2026-10-15）は、Kiro CLI では 2.31 以降のローカル V3 セッションで利用でき、既定では off であると説明しています。

### サンドボックスが対象にするもの

| 範囲 | 内容 |
|------|------|
| サンドボックスの内側 | エージェントが実行する端末コマンドと、それらが起動するすべての子プロセス。MCP のラッピングを有効にした場合は、stdio MCP サーバーのプロセスも内側に入る |
| サンドボックスの外側 | エージェントのハーネスとモデルとの会話、組み込みのファイルツール（権限ルールは引き続き読み書きを制御する）、リモートの HTTP／SSE MCP サーバー（ネットワーク通信はサンドボックスの規則に従わない） |

- shell コマンドが始まる前に、[権限](https://kiro.dev/docs/permissions/)がそのコマンドを実行してよいかを決め、そのあとサンドボックスが実行中のコマンドと子プロセスの到達範囲を制限する
- サンドボックスはローカルで動くセッションにだけ適用される。クラウドセッションは、管理されたクラウドのサンドボックスを使う
- サンドボックスはコマンドにできることを減らすが、隔離を保証するものではない。提案されたコマンドの確認を続け、決して実行してはならない操作には `deny` ルールを残す

### プラットフォームの要件

| プラットフォーム | 要件 |
|-----------------|------|
| macOS | なし。`sandbox-exec` 経由で組み込みの Seatbelt サンドボックスを使う |
| Linux | `PATH` 上の Bubblewrap（`bwrap`）。Kiro は自動でインストールしない。`COMMON_DEPENDENCIES`、および許可ホストを指定した `DEFAULT_BLOCKED` には `socat` も必要 |
| Windows | `COMMON_DEPENDENCIES` または `DEFAULT_ALLOWED` でコマンドを実行する前に、管理者によるセットアップを 1 回行う。Kiro CLI では `/sandbox setup` を実行する。`DEFAULT_BLOCKED` はセットアップ前でも動作する |

プラットフォームのバックエンドがないとき、Kiro はサンドボックスを利用できないと報告します。現在のモードが保護を必須としていない限り、コマンドはオペレーティングシステムの隔離なしで実行されます。

### 使い方

ローカルの V3 セッションで `/sandbox` を実行すると設定パネルが開きます。サブコマンドを直接使うこともできます（公式 Local command sandbox と公式 [Slash commands の `/sandbox`](https://kiro.dev/docs/reference/slash-commands/)、Page updated: 2026-10-20）。

```text
/sandbox                  サンドボックスの設定を開く
/sandbox on               グローバルのサンドボックスを有効にする
/sandbox off              グローバルのサンドボックスを無効にする
/sandbox project on       このプロジェクトでサンドボックスを有効にする
/sandbox project off      このプロジェクトに enabled:false を書き込む
/sandbox network          ネットワークモードを選ぶ
/sandbox setup            Windows の管理者セットアップを実行する
```

- 変更は `sandbox.json` に保存され、再起動なしで実行中のセッションに適用される
- グローバルのポリシーが有効なとき、プロジェクトのファイルが `enabled` を `false` にしても、グローバルのポリシーは有効のまま
- `/sandbox` はクラウドセッションでは利用できない（公式 Slash commands）

### 設定ファイルとキー

| 範囲 | パス | 用途 |
|------|------|------|
| グローバル（Kiro CLI） | `KIRO_HOME` が設定されていれば `$KIRO_HOME/settings/sandbox.json`、なければ `~/.kiro/settings/sandbox.json` | すべてのプロジェクトに共通する既定のポリシー |
| プロジェクト | `<workspace-root>/.kiro/settings/sandbox.json` | 1 つのリポジトリでサンドボックスを有効にする、または厳しくする |

| キー | 必須 | 値 | 既定 |
|------|------|-----|------|
| `enabled` | はい | `true`、`false` | |
| `networkAccess` | いいえ | `DEFAULT_BLOCKED`、`COMMON_DEPENDENCIES`、`DEFAULT_ALLOWED` | `DEFAULT_BLOCKED` |
| `mcpSandboxing` | いいえ | `true`、`false` | `false` |

`networkAccess` の値は大文字小文字を区別します。未知のキーは無視されます。

```json
{
  "enabled": true,
  "networkAccess": "COMMON_DEPENDENCIES"
}
```

グローバルとプロジェクトの組み合わせ方（公式 Local command sandbox）:

- グローバルのポリシーが有効なとき、プロジェクトのファイルは厳しくする方向にしか変更できない。プロジェクトは `enabled` を `false` にすること、より開放的なネットワークモードを選ぶこと、グローバルで有効にした MCP のラッピングを無効にすることができない
- グローバルのファイルがない、または `enabled: false` のとき、`enabled: true` のプロジェクトのファイルが、そのプロジェクトのサンドボックスを有効にする
- クローンしたリポジトリは、プロジェクトのファイルでネットワークアクセスを開放したり、有効なグローバルのポリシーを無効にしたりできない

### ネットワークモード

| モード | 外向きのネットワーク |
|--------|--------------------|
| `DEFAULT_BLOCKED` | ブロック。`sandbox_network` ルールが許可したホストを除く。既定 |
| `COMMON_DEPENDENCIES` | よく使われるパッケージ・ソース・ビルド・コンテナのサービスに到達できる。ほかのホストは、ルールが許可しない限りブロック |
| `DEFAULT_ALLOWED` | 開放。サンドボックス内のコマンドは任意のホストに到達できる。このモードでは `sandbox_network` の deny ルールに頼らない |

最も厳しいネットワーク制御には `DEFAULT_BLOCKED` を使います。インストールやビルドでよく使われる開発サービスが必要な場合は `COMMON_DEPENDENCIES`、ネットワークのフィルタリングが不要な場合だけ `DEFAULT_ALLOWED` を使います（公式の説明）。

特定のホストを許可するには、`permissions.yaml` に `sandbox_network` ルールを書きます。公式 Local command sandbox の説明:

- `sandbox_network` は[権限のケイパビリティ](https://kiro.dev/docs/permissions/)で、ホストのルールは書かれた順に適用され、最初に一致したルールが決定する。ほかの権限のケイパビリティのように `deny` が常に勝つわけではない。具体的なホストを、それに一致する広いワイルドカードより前に書く
- パターンは大文字小文字を区別せず、完全一致のホスト名と `*.suffix` のワイルドカードに対応する
- `sandbox_network` は `all` メタケイパビリティに含まれない。`capability: all, effect: allow` はサンドボックス内のネットワークアクセスを開放しない。`fs_read` と `fs_write` のルールも、サンドボックス内のコマンドが見られる・書けるパスを形づくる

```yaml
# ~/.kiro/settings/permissions.yaml
rules:
  - capability: sandbox_network
    match: ['packages.internal.example.com']
    effect: allow

  # このルールは下のワイルドカードより前に置く
  - capability: sandbox_network
    match: ['uploads.example-corp.net']
    effect: deny

  - capability: sandbox_network
    match: ['*.example-corp.net']
    effect: allow
```

### stdio MCP サーバーのラッピング

`mcpSandboxing` を `true` にすると、stdio MCP サーバーのプロセスが shell コマンドと同じサンドボックスの中で起動します。リモートの HTTP／SSE MCP サーバーは影響を受けません。`mcpSandboxing` を変更するとローカルの MCP サーバーが再起動し、約 1 分かかることがあります。サーバーのラッピングに失敗しても、コマンドのサンドボックスは有効のままで、Kiro はそのサーバーが対象外であると報告します（公式 Local command sandbox）。

### エラーと復旧（公式 Local command sandbox）

| 状況 | 公式の説明 |
|------|-----------|
| コマンドがホストに到達できない | `sandbox_network` の allow ルールを追加する。よく使われる開発サービスなら `COMMON_DEPENDENCIES` も使える |
| サンドボックスを利用できない | Linux では `bwrap` が `PATH` にあるかを確認する。プロキシのフィルタリングが必要なら `socat` をインストールする。Windows では管理者セットアップを完了する。原因を直すまでコマンドは隔離なしで実行される。直したあとは新しい CLI セッションを開始する |
| Windows が `COMMON_DEPENDENCIES` または `DEFAULT_ALLOWED` を拒否する | CLI で `/sandbox setup` を実行する。`DEFAULT_BLOCKED` はセットアップ前でも使える |
| MCP サーバーが対象外 | 1 つ以上の stdio サーバーでラッピングに失敗した。shell コマンドのサンドボックスは有効のまま。サーバーのコマンドと MCP のログを確認する |
| `--sandbox` 付きのヘッドレス実行が早く終了する | コマンドのサンドボックスを有効にできなかった、または要求した MCP のラッピングが利用できなかった。名前の挙がった原因を直す |

### 実機 2.33.0 で確認した事項と未確認事項

- 実機 2.33.0 の `kiro-cli settings list --all` に、サンドボックス関連の設定キーは表示されませんでした
- 実機 2.33.0 の `kiro-cli chat --help`（`--v3` を付けても同じ出力）には、`--cloud`・`--repo`・`--resume-id` は表示されますが、`--sandbox` は表示されませんでした。公式 [CLI commands](https://kiro.dev/docs/reference/cli-commands/)（Page updated: 2026-10-20）と公式 Headless mode は `--sandbox` を掲載しています。この差の理由は**未確認**です
- `/sandbox` の各サブコマンドと、プラットフォームごとのサンドボックスの動作は、V3 セッションを起動して確認していないため、実機 2.33.0 では**未確認**です。上の説明は公式ドキュメントに基づきます

## [V3] ローカル autonomous モード（`/autonomous`）

V3 のローカルセッションで `/autonomous on` を実行すると、shell コマンドごとの承認を求められずに、Kiro がタスクを進めます。Kiro は Default エージェントに切り替え、先にローカルコマンドサンドボックスを有効にします（公式 Changelog v2.31.0）。

公式 Local command sandbox の「Use local autonomous mode」と公式 [Slash commands の `/autonomous`](https://kiro.dev/docs/reference/slash-commands/)（Page updated: 2026-10-20）の説明:

```text
/autonomous               on／off のピッカーを開く
/autonomous on            autonomous モードを開始する
/autonomous off           autonomous モードを終了する（サンドボックスは on のまま）
```

- 強制されるサンドボックスは、外向きのネットワークアクセスをブロックした状態で始まる。有効なグローバルとプロジェクトの設定は、そのポリシーを厳しくする方向にしか変更できない
- Kiro がサンドボックスの保護を確認できない場合、autonomous モードは開始しない
- 後から保護が失われた場合、Kiro はコマンドを続ける前に autonomous モードを終了する
- `/autonomous off` で autonomous モードを終了する。サンドボックスは on のまま残る
- `/autonomous` はローカルの V3 セッションのコマンドです。公式 Slash commands の `/autonomous` の節に、クラウドセッションでの扱いの記載は確認できませんでした（**未確認**）

## [V3] MCP ツールのオンデマンド読み込み

V3 が MCP ツールの定義を必要なときにだけ読み込み、モデルのコンテキストをより多く作業に残します（公式 Changelog v2.31.0）。

公式 [Tool Search](https://kiro.dev/docs/mcp/tool-search/)（Page updated: 2026-10-15）の説明:

- Tool Search は、使われていない MCP ツールの定義を各リクエストから外す。Kiro CLI 2.31 以降のローカル V3 セッションでは既定で使われる。MCP サーバーを設定していなければ効果はない
- Kiro は接続した MCP サーバーのツールの名前と説明を索引化し、モデルには完全な定義の代わりにコンパクトな一覧を渡す。必要なツールの完全な説明と入力スキーマは、その都度読み込む。実行は、ほかのツールと同じ権限と Hook の検査を通る
- ローカルの V3 セッションでは、`tool_load` が正確なツール ID を読み込み、`tool_call` が実行する。MCP ツールでは `tool_load` が `tool_call` の前に表示されることがある
- V2 セッションでは Tool Search は引き続きオプトイン。`kiro-cli settings toolSearch.enabled true` で有効にする。V2 では、MCP ツールの定義がコンテキストウィンドウの 5%、または既定で 50,000 トークンのどちらかのしきい値を超えると有効になる

V2 の Tool Search の詳細は [19. Tool Search](19_ToolSearch.md) を参照してください。

## ⚠ `KIRO_HOME` が V3 のグローバル設定とセッションに適用される

`KIRO_HOME` を絶対パスに設定すると、仕事用と個人用など別々の Kiro プロファイルを保てます。V3 は、グローバル設定、サインイン、セッション、エージェントの状態をそこに保存します。既存の MCP サインインは 1 回だけそこへコピーされます（公式 Changelog v2.31.0）。

| 公式ページ | 内容 |
|-----------|------|
| [Configuration scopes](https://kiro.dev/docs/configuration/#file-paths)（Page updated: 2026-10-13） | V3 は、グローバル設定、サインイン、セッション、エージェントの状態をそこに保存する。パスを初めて使うときに、既存の MCP サインインを 1 回コピーする。相対パス、ファイルシステムのルート、ホームディレクトリ、またはその親ディレクトリは無視され、`~/.kiro` が使われる |
| [Settings リファレンス](https://kiro.dev/docs/reference/settings/)（Page updated: 2026-10-15） | `KIRO_HOME` は、V3 ではグローバルな Kiro ディレクトリを上書きする。ルート、ホームディレクトリ、その親、または相対パスは `~/.kiro` にフォールバックする |
| [CLI commands](https://kiro.dev/docs/reference/cli-commands/)（Page updated: 2026-10-20） | MCP の設定とサインイン、権限、セッション、Powers、設定、カスタムエージェント、Skills、Steering、Workflows、そのほかの V3 のエージェントの状態に使うグローバルディレクトリを上書きする |

v2.31.0 のバグ修正には、`KIRO_HOME` が相対パス、ファイルシステムのルート、ホームディレクトリ、またはその親ディレクトリのとき、Kiro が `~/.kiro` にフォールバックする項目があります。changelog の記述に V3 の限定はありません。`KIRO_HOME` の導入は [v2.3.0 の変更履歴](../02_update/01_changelog.md#v230-cli2026-05-12)を参照してください。

## ⚠ ヘッドレス実行と保存済みの `sandbox.json`

グローバルまたはプロジェクトの `sandbox.json` で `enabled: true` の設定が、V3 のヘッドレス実行に適用されるようになりました（公式 Changelog v2.31.0）。実行を保護なしで続けず停止させたい場合は `--sandbox` を付けます。

公式 Local command sandbox の「Require the sandbox in headless runs」と公式 [Headless mode](https://kiro.dev/docs/cli/headless/)（Page updated: 2026-10-20）の説明:

- ヘッドレスの V3 セッションも、同じグローバルとプロジェクトの `sandbox.json` を読む。解決された設定が `enabled: true` なら、追加のフラグなしでサンドボックスを要求する
- Kiro がサンドボックスを有効にできない場合、実行は警告を出して、サンドボックスなしで続く。要求した MCP のラッピングに失敗した場合、shell コマンドは保護されたままだが、影響を受けた MCP サーバーは保護されない
- 保護がそろわなければ停止させたいスクリプトや CI には `--sandbox` を渡す。`--no-interactive` または `--output-format stream-json` が必要
- `--sandbox` を付けると、コマンドのサンドボックスを有効にできない場合、またはラッピングが要求されていて利用できない場合に、タスクの開始前に実行が失敗する

```bash
kiro-cli chat --v3 --sandbox --no-interactive "Run the test suite and summarize failures"
```

## v2.31.1 — Mermaid 図と V3 非対話実行の保存済み設定

### Mermaid 図をチャットに描画する（改善）

エージェントの返信内のフローチャート、シーケンス図、状態遷移図、ER 図が、端末内のアートとして描画されます。未対応の構文、大きすぎる図、または ASCII アートが off の場合は、Kiro が Mermaid のソースを表示します（公式 Changelog v2.31.1）。

公式 [Terminal UI の Mermaid diagrams](https://kiro.dev/docs/cli/terminal-ui/#mermaid-diagrams)（Page updated: 2026-10-20）の説明:

| Mermaid の見出し | 図 |
|------------------|----|
| `graph`、`flowchart` | フローチャート |
| `sequenceDiagram` | シーケンス図 |
| `stateDiagram`、`stateDiagram-v2` | 状態遷移図 |
| `erDiagram` | ER 図 |

- Kiro CLI 2.31.1 以降が、エージェントの返信内の対応する Mermaid コードブロックを端末アートとして描画する
- 未完成のブロックがストリーミングされている間は **Drawing diagram** と表示される
- 図が広すぎる、大きすぎる、未対応、または未対応の構文を使っている場合、Kiro はソースと理由を表示する
- [ASCII アートが off](https://kiro.dev/docs/cli/chat/settings/#settings-display) のとき、または `KIRO_ASCII_MODE=1` が設定されているとき、Kiro は常にソースを表示する。`chat.allowAsciiArt` は、off にすると braille 点・罫線・Unicode 記号を平易な ASCII に置き換える設定（公式 In-session settings、Page updated: 2026-10-20）
- 公式 Terminal UI のこの節は、V2／V3 のどちらに適用されるかを明記していません（**未確認**）。v2.33.0 では、サブグラフを含むフローチャートの描画と、ノード説明の折り返しが加わっています（→ [52. v2.33 新機能](52_v233NewFeatures.md)）

### V3 非対話実行に保存済みの compaction と Tool Search の設定を適用（バグ修正）

V3 の非対話実行が、保存済みの compaction と Tool Search の設定を適用し、対話セッションと一致するようになりました（公式 Changelog v2.31.1）。公式 Headless mode の「Saved V3 settings」（Page updated: 2026-10-20）の説明:

| 目的 | 設定 |
|------|------|
| 自動 compaction | `chat.disableAutoCompaction`、`compaction.excludeMessages`、`compaction.excludeContextWindowPercent` |
| Tool Search | `toolSearch.enabled`、`toolSearch.minPct`、`toolSearch.minTokens` |

- Kiro CLI 2.31.1 以降が、保存済みの compaction と Tool Search の設定を V3 の非対話実行に適用する
- 保存済みの Tool Search のしきい値を適用するには、`toolSearch.enabled true` も保存する
- 値は対話セッションと同じく `kiro-cli settings` で保存する。アップグレード後にヘッドレス実行の動作が変わった場合は、`kiro-cli settings list` で保存済みの `compaction.*` や `toolSearch.*` の値を探す。不要なグローバルの値は `kiro-cli settings --delete <name>` で削除できる。`(workspace)` と表示される値には `settings` の後に `--workspace` を付ける。削除は対話セッションにも影響する

```bash
kiro-cli settings compaction.excludeMessages 4
kiro-cli settings toolSearch.enabled true
```

### Windows の `/sandbox setup`（バグ修正）

Windows の `/sandbox setup` が一時フォルダの外で実行されるようになり、ポリシーがそこでのプログラムをブロックしている場合の失敗を避けられるようになりました（公式 Changelog v2.31.1）。公式 Local command sandbox の「Errors and recovery」は、ポリシーが `%TEMP%` のプログラムをブロックしてセットアップが失敗する場合、Kiro CLI 2.31.1 以降に更新して再実行するよう説明しています。

### v2.31.1 のその他のバグ修正

| 内容（公式 Changelog v2.31.1） | 公式ドキュメントでの確認 |
|-----------------------------|------------------------|
| `chat.disableWrap` のセッションと Lite ペインからコピーしたプロンプトの先頭に、余分な空白が 2 つ付かない | 公式 Settings リファレンスは `chat.disableWrap` を「コピー＆ペースト用に、ハードな改行なしで出力する」設定として掲載。修正そのものの記載は確認できなかった（**未確認**） |
| ターミナルペインマネージャーの Herdr が、権限または回答を待つ V3 セッションをブロック中として表示する | 本ページで参照した公式ページの範囲では記載を確認できなかった（**未確認**） |
| モデルが応答テキストなしで拒否した場合も、モデルフォールバックが実行される | 公式 Slash commands は、V1／V2 の `/model fallback` を説明している。応答テキストなしの拒否の扱いの記載は確認できなかった（**未確認**）。V2／V3 の適用範囲も changelog に記載がない |
| compaction が、モデルの拒否を会話の要約として保存しない | 記載を確認できなかった（**未確認**） |
| `/changelog` がリリースノートの各エントリを別々の行に表示する | 記載を確認できなかった（**未確認**） |
| IAM Identity Center のサインインが、隔離された AWS パーティションでも動作する | 公式 Authentication ページは AWS GovCloud (US) のリージョンで IAM Identity Center が使えることを説明している。隔離されたパーティション全般の記載は確認できなかった（**未確認**） |
| [V3] `/workflow` で、Workflow のレシピのテキストが端末のエスケープシーケンスを出力できない | 記載を確認できなかった（**未確認**） |

## v2.31.0 のその他のバグ修正

| 内容（公式 Changelog v2.31.0） | 公式ドキュメントでの確認 |
|-----------------------------|------------------------|
| `KIRO_HOME` が相対パス等のとき `~/.kiro` にフォールバックする | 公式 Configuration scopes と Settings リファレンスに記載あり（上記） |
| V1 の `--no-interactive` 実行が、無関係なツール承認エラーを報告せず、ターンを終わらせたエラーで終了する | 記載を確認できなかった（**未確認**） |
| アニメーション WebP 画像内のテキストが、V3 セッションで最初のフレームを読むときも鮮明に保たれる | 記載を確認できなかった（**未確認**） |
| V3 のクラウド設定と Kiro サービスへのリクエストが、停滞しても固まらず 15 秒で停止する | 記載を確認できなかった（**未確認**） |
| streamable HTTP サーバー上の V3 の MCP ツールが、サーバーがセッションを切断した後も動作し続ける | 記載を確認できなかった（**未確認**） |
| V3 のクラウドセッションで、コードインテリジェンスのインジケーターと `/code` パネルがクラウドのワークスペースを反映する | 記載を確認できなかった（**未確認**） |
| トークンの更新中に認証サービスが一時的なエラーを返しても、GitHub と Google のサインインが終了しない | 記載を確認できなかった（**未確認**） |

修正項目の完全な一覧は [変更履歴の v2.31.1](../02_update/01_changelog.md#v2311-cli2026-10-14) と [v2.31.0](../02_update/01_changelog.md#v2310-cli2026-10-13) を正とします。

## 関連リンク

### 本サイト

- [49. v2.30 新機能](49_v230NewFeatures.md)
- [51. v2.32 新機能](51_v232NewFeatures.md)
- [52. v2.33 新機能](52_v233NewFeatures.md)
- [19. Tool Search](19_ToolSearch.md)
- [18. Terminal UI](18_TerminalUI.md)
- [17. Granular Tool Trust](17_GranularToolTrust.md)
- [36. Cloud Sessions](36_CloudSessions.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [Settings リファレンス](../04_reference/01_settings.md)
- [CLI コマンド リファレンス](../04_reference/03_cli-commands.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.31](https://kiro.dev/changelog/cli/2-31/)
- [Kiro CLI Changelog v2.31.1](https://kiro.dev/changelog/cli/2-31-1/)
- [Local command sandbox](https://kiro.dev/docs/sandbox/)
- [Tool Search](https://kiro.dev/docs/mcp/tool-search/)
- [Configuration scopes](https://kiro.dev/docs/configuration/)
- [Terminal UI — Mermaid diagrams](https://kiro.dev/docs/cli/terminal-ui/#mermaid-diagrams)
- [Headless mode](https://kiro.dev/docs/cli/headless/)
- [Slash commands](https://kiro.dev/docs/reference/slash-commands/)
- [Settings リファレンス](https://kiro.dev/docs/reference/settings/)
- [CLI commands リファレンス](https://kiro.dev/docs/reference/cli-commands/)
- `kiro-cli settings list --all` / `kiro-cli chat --help`（実機 2.33.0）

**最終更新**: 2026-10-21
**対象バージョン**: Kiro CLI v2.31.0+（サンドボックス・autonomous モード・オンデマンドの MCP ツール・保存済み `sandbox.json` の適用は V3 Early Access）
