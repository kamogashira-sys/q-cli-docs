[ホーム](../README.md) > [機能詳細ガイド](README.md) > v3.0 新機能

# 55. v3.0 新機能 — V3 の既定化・Classic／デスクトップアプリ／オートコンプリートの廃止

## 概要

Kiro CLI **v3.0.0**（2026-11-03）は、**V3 を、動作する環境の対話型セッションの既定のエージェントハーネスにした**メジャーリリースです。同時に、Kiro CLI は単一のスタンドアロンの `kiro-cli` バイナリになり、**Classic インターフェース、デスクトップアプリ、インラインのオートコンプリートが廃止されました**。

> **出典**: 公式 [Changelog v3.0](https://kiro.dev/changelog/cli/3-0/)（表示日 2026-11-03）、公式 [Upgrade from CLI 2.x](https://kiro.dev/docs/cli/v3/)（Page updated: 2026-11-03）、公式 [Choose an agent harness](https://kiro.dev/docs/cli/agent-harness/)（Page updated: 2026-11-03）、公式 [Installation の Moving from the Kiro CLI desktop app](https://kiro.dev/docs/getting-started/installation/)（Page updated: 2026-11-12）。実機 `kiro-cli 3.3.0`（Linux）で確認できたコマンドの廃止は、該当の節に書いています。

公式 Changelog は、本文のほかに次の 2 節だけを載せています（項目数は 2）。

- **Breaking changes**: Classic インターフェース、デスクトップアプリ、オートコンプリートとインライン提案（関連コマンドを含む）の廃止
- **Start on V3 by default**: 対話型・ヘッドレス・ACP の既定の変更

> 📌 **これまでの経緯**: V3 は v2.8.0（2026-06-17）から `--v3` で先行公開（Early Access）されていました（→ [09_v3/](../09_v3/README.md)、[30. v2.8 V3 プレビュー](30_v28V3Preview.md)）。v2.30.0 で、起動時に V3 への切り替えを促すプロンプトが段階的に展開されていました（→ [49. v2.30 新機能](49_v230NewFeatures.md)）。

## V3 が既定になる（Start on V3 by default）

`--v3` は不要になりました。起動の種類ごとの既定は、公式 [Choose an agent harness](https://kiro.dev/docs/cli/agent-harness/) の表のとおりです。

| 起動の種類 | 既定のハーネス |
|-----------|---------------|
| 対話型（`kiro-cli`、`kiro-cli chat`） | 動作する環境では **V3**。glibc が古い Linux では V2 |
| ローカルのヘッドレス（`--no-interactive`、または標準入力が端末でない） | **V2**。ただし `--trust-all-tools` は対話型と同じ既定（V3）、`--cloud`・`--repo`・V3 のセッション ID を指定すると V3 |
| ACP クライアント（`kiro-cli acp`） | 動作する環境では **V3**。例外あり（下記） |
| `--cloud`・`--repo` | V3 |
| V1 または V2 が作ったセッションを指す `--resume-id` | V2 |

ハーネスは次の順で決まります（公式の説明）。

1. 起動行の `--v3` または `--v2`
2. `kiro-cli chat --agent-engine <値>`
3. `--cloud`・`--repo` が意味する V3
4. 保存済みの `chat.agentEngine` 設定
5. 上の表の既定

`--v2` と `--v3` は同時に指定できず、`--agent-engine`・root の旧 UI フラグとも組み合わせられません。保存する場合は、グローバル設定の `chat.agentEngine` に `v3` または `v2` を保存します（ワークスペースでは上書きできません）。

```bash
# この 1 回だけ V3／V2 で起動
kiro-cli --v3
kiro-cli --v2

# 既定として保存
kiro-cli settings chat.agentEngine v3
kiro-cli settings chat.agentEngine v2
```

ヘッドレスのスクリプトは、既定の変更に左右されないよう、ハーネスを明示します（公式の推奨）。

```bash
kiro-cli chat --v3 --no-interactive "your prompt here"
kiro-cli chat --v2 --no-interactive "your prompt here"
```

### 初回起動の選択プロンプト

3.0.0 以降の初回の対話型起動で、**保存済みの Kiro CLI 2.x のセッションがあり、ハーネスを一度も選んでいない**場合は、V3 を適用する前に確認します。新規インストール、またはセッションのないアップグレードは、確認なしで V3 で始まります。

| 答え | 動作 |
|------|------|
| **Continue with V3** | `chat.agentEngine` を `v3` に保存し、このセッションを V3 で始める |
| **Stay on V2, remind me later** | `chat.agentEngine` を `v2` に保存し、V2 で始める。14 日後に再度尋ねる |
| **Stay on V2, don't ask again** | `chat.agentEngine` を `v2` に保存し、V2 で始める |

アップグレード前に `chat.agentEngine` を `v2` に保存していた場合は、プロンプトの代わりに **Switch to V3** と **Keep V2** の 1 回限りの通知が出ます。起動行がすでにハーネスを指定している場合、`--resume-id`、`--sessions`、ヘッドレス、V3 が動かない環境では、プロンプトは出ません。

V3 が始まると、V2 形式のエージェント設定は、`chat.enableAutoAgentUpgrade` が `false` でない限り自動でアップグレードされます（→ [34. /upgrade-agent](34_v214UpgradeAgent.md)、[54. v2.35〜v2.37 新機能](54_v237NewFeatures.md)）。

### ACP の既定の例外

`kiro-cli acp` は、`--agent-engine` フラグも `acp.agentEngine` 設定もハーネスを指定しないとき V3 で始まります。例外は次の 3 つで、いずれも V2 のままです（公式の説明）。

- 起動行に V2 専用のフラグ（`--agent`・`--model`・`--effort`・`--trust-all-tools`・`--trust-tools`）がある
- V2 が必要なクライアントと Kiro が認識した
- V3 を動かせない環境

ハーネスを明示すると、それが常に優先されます。`--agent-engine v3` の指定と V2 専用フラグは同時に使えません。`chat.agentEngine` は `kiro-cli acp` では参照されません。V3 の ACP の移行は公式 [Migrate an ACP client to CLI V3](https://kiro.dev/docs/cli/v3/acp-migration/) を参照してください（→ [13. ACP](13_ACP.md)）。

### 古い glibc の Linux

glibc が V3 に必要な版より古い Linux では、ハーネスを指定しない起動は、V2 のターミナル UI で開きます。そこで `kiro-cli --v3` を実行すると「V3 is currently not supported on this system」で止まります。macOS と Windows は、常に V3 を動かせます（公式の説明）。

### どちらのハーネスで動いているかの確認

セッションの最初の行を読みます（公式の説明）。

- V3: **Welcome to Kiro CLI V3**。以前の体験で起動する方法として `kiro-cli --v2` を示す
- V2: **Kiro CLI V3 is here. This version will no longer receive feature updates. To upgrade, run: kiro-cli --v3**

保存済みの既定は `kiro-cli settings chat.agentEngine`（ACP は `kiro-cli settings acp.agentEngine`）で確認します。V2 は動き続けますが、新機能は届きません。V2 に戻すには、1 回だけなら `kiro-cli --v2`、既定にするなら `kiro-cli settings chat.agentEngine v2` です。V3 と V2 は別のセッションストアを持ち、V3 は V2 のセッションを V3 のコピーとして再開できますが、**V2 は V3 のセッションを開けません**（→ [09_v3/](../09_v3/README.md)）。

## Classic インターフェースの廃止（Breaking changes）

Classic（V1）の対話型の体験は、どちらのハーネスでも動かなくなりました。Classic を選ぶ次のいずれかが残っていると、**Kiro CLI 3.0 のメッセージが表示され、2 つの選択肢**が出ます（公式 [If a launch still selects Classic](https://kiro.dev/docs/cli/agent-harness/#if-a-launch-still-selects-classic)）。

- `--classic` または root の旧 UI フラグ
- `--agent-engine v1`
- 環境変数 `KIRO_CHAT_UI`
- `chat.ui` 設定
- `chat.agentEngine` が `v1`

選択肢は、**Continue with V3**（`chat.agentEngine` を保存し、ターミナル UI で再実行する）と **Exit**（ハーネスを変えず、起動を終える）です。V3 が動かない環境では、ボタンが **Switch to the terminal UI and launch** になり、`chat.agentEngine` を `v2` に保存します。保存済みの `v2` または `v3` の値は、シェルのエイリアスに残った Classic のフラグより優先されるため、一度 **Continue with V3** を選べばエイリアスは動き続けます。ヘッドレスの実行が Classic を選んでいるときは、ヘッドレスの既定へ移され、通知が出ます。

実機 `kiro-cli 3.3.0` の `kiro-cli chat --help` は、`--agent-engine` の説明で「Classic (v1) no longer runs」と述べ、`v1` と Classic の UI の選択（root の旧 UI フラグ、`KIRO_CHAT_UI` など）を、V1 は動かないものとして扱います。root の旧 UI フラグ（別名 `--classic`）自体は、`kiro-cli --help` に「Launch chat in legacy UI mode」、`kiro-cli chat --help` に「Use the legacy harness」の説明で残っています。

## デスクトップアプリとオートコンプリートの廃止（Breaking changes）

Kiro CLI はデスクトップアプリを同梱せず、**単一のスタンドアロンの `kiro-cli` バイナリ**になりました。デスクトップアプリとともに、次の機能が廃止されました（公式 Changelog と Installation の記述）。

- インラインの shell のオートコンプリートと、インライン提案（スタンドアロンの代替はない。→ [25. AutoComplete](25_AutoComplete.md)）
- `kiro-cli translate`
- ダッシュボード（`kiro-cli dashboard`）
- `kiro-cli doctor`（`kiro-cli diagnostic` または `kiro-cli issue` を使う）
- `kiro-cli inline`、`kiro-cli theme`、`kiro-cli autocomplete`（公式 Changelog が、利用できないコマンドとして挙げている）

実機 `kiro-cli 3.3.0` では、次を確認しました。

- `kiro-cli doctor` が「`kiro-cli doctor` has been removed. Run `kiro-cli diagnostic` for system info, or `kiro-cli issue` to report a problem.」と表示する
- `kiro-cli translate`・`theme`・`inline`・`autocomplete`・`dashboard` が「unrecognized subcommand」になる
- `kiro-cli --help` のコマンド一覧にこれらが出ない

あなたのチャット、設定、ログインは 3.0.0 に引き継がれます。初めて 3.0.0 でチャットを開始すると、デスクトップアプリが残したファイルとシェルの統合が削除されます（公式の説明）。

### デスクトップアプリからの移行

公式 [Installation](https://kiro.dev/docs/getting-started/installation/#moving-from-the-kiro-cli-desktop-app) の手順は、デスクトップアプリの入れ方ごとに次のとおりです。移行後は `kiro-cli --version` が 3.0.0 以降を示すことを確認します。

| 入れ方 | 手順 |
|--------|------|
| macOS デスクトップアプリ（DMG） | 自動で Kiro CLI に移る。すぐ移すなら `kiro-cli update`。まだ 2.x と表示されるなら、もう一度 `kiro-cli update` |
| macOS（Homebrew） | `brew upgrade --cask kiro-cli` |
| そのほかの macOS | インストールスクリプト `curl -fsSL https://cli.kiro.dev/install \| bash` |
| Linux AppImage | `kiro-cli update`（`~/.local/bin/kiro-cli` に入る）。2.x と表示されるなら、もう一度 |
| Linux zip | `kiro-cli update` |
| Ubuntu .deb | `kiro-cli.deb` を取得し直して `sudo dpkg -i kiro-cli.deb` |
| Amazon Linux の RPM リポジトリ | `sudo dnf upgrade kiro-cli` |

インストールスクリプトが `Caution:` で始まるメッセージを出した場合は、公式 Installation の「Caution message after installing」を参照してください。

## V3 で使える機能（公式の紹介）

Changelog の本文は、V2 にない V3 の機能を次のように紹介しています。個別の機能は、それぞれの文書で扱っています。

- **クラウドセッション**: 切断しても動き続け、あとで `/sessions` から再開できる
- **Memory**: 有効にすると、リポジトリのコンテキストを次のセッションへ引き継ぐ（→ [48. v2.29 新機能](48_v229NewFeatures.md)）
- **Approve for me**: 有効にすると、定型的な操作を承認し、危険な操作をブロックし、残りを尋ねる。deny・ask・allow のルールが先に判定する（→ [54. v2.35〜v2.37 新機能](54_v237NewFeatures.md)）
- **`/sandbox`**: shell コマンドを隔離する。**`/autonomous on`** は、サンドボックスをオンにして、コマンドごとの承認なしでタスクを進める（→ [50. v2.31 新機能](50_v231NewFeatures.md)）
- **Workflows**: 開始前に計画を示す。`/settings` > **Features** でオンにする（→ [45. v2.26 新機能](45_v226NewFeatures.md)）

## 破壊的変更の全体像（公式 Upgrade from CLI 2.x）

公式の v3 概要ページの Breaking changes の表は、3.0.0 の時点で次の項目を挙げています（このうち、Classic・デスクトップアプリ・コマンドの廃止が 3.0.0 の Changelog の内容です）。

| 変更 | 2.x | V3 |
|------|-----|----|
| 組み込みの AWS ツール | `use_aws`（別名 `aws`） | MCP サーバーで AWS にアクセスする |
| セッション形式 | V2 のセッションストア | 別の V3 のセッションストア。V3 は V2 を V3 のコピーとして取り込み、V2 は V3 を開けない |
| Hook の形式・トリガー名 | camelCase のオブジェクト（`agentSpawn`） | PascalCase の配列（`SessionStart`） |
| 永続的な信頼の設定 | ツール単位の `toolsSettings` | capability ベースの `permissions.yaml` |
| サブエージェントのツール呼び出し | サブエージェント自身の承認済みツールが、親が許可しなくてもプロンプトなしで動いた | 親のセッションのポリシーも許可するときだけプロンプトなしで動く。ヘッドレスでは拒否される |
| Classic インターフェース | `--classic`・root の旧 UI フラグで非 TUI | 起動すると V3 を提案される |
| デスクトップアプリ・インラインのオートコンプリート | デスクトップアプリ | スタンドアロンの `kiro-cli` |
| デスクトップアプリのコマンド | `autocomplete`・`inline`・`translate`・`theme`・`dashboard`・`doctor` | `autocomplete`・`inline`・`translate`・`theme`・`dashboard` は使えない。`doctor` は `diagnostic` か `issue` を案内 |
| 「Vibe」の概念 | （CLI にはない） | 「Default」モードが標準の名前 |

公式の移行手順（7 ステップ）は、V3 を始める → `/upgrade-agent` → 権限の確認 → エージェント設定のフィールドの確認 → AWS ツールを MCP サーバーに置き換える → ツール名の対応を更新する → `kiro-cli agent validate` で検証する、の順です。詳細は公式 [Migration guide](https://kiro.dev/docs/cli/v3/migration-guide/) と本サイトの [09_v3/](../09_v3/README.md) を参照してください。

## 実機での確認（kiro-cli 3.3.0・Linux）

- `kiro-cli --help` のコマンド一覧に `translate`・`doctor`・`theme`・`inline`・`dashboard` がなく、`--v3` の説明が「the default for interactive chat where it can run」になっている
- `kiro-cli doctor` が廃止のメッセージを表示し、`translate`・`theme`・`inline`・`autocomplete`・`dashboard` は「unrecognized subcommand」になる
- `kiro-cli chat --help` の `--agent-engine` の説明に、何も選ばないときの既定（対話型は V3、ヘッドレスと標準入力のパイプは V2、`--trust-all-tools` は V3、V1・V2 のセッションの `--resume-id` と V3 を動かせない環境は V2）が書かれている
- 次は実機の環境（既存の V2 セッションと設定がない）では試していないため**実機では未確認**: 初回起動の選択プロンプト、デスクトップアプリからの移行、Classic を選んだ起動の **Continue with V3** の表示、glibc が古い Linux での挙動

## 関連リンク

### 本サイト

- [56. v3.1〜v3.3 新機能](56_v33NewFeatures.md)
- [54. v2.35〜v2.37 新機能](54_v237NewFeatures.md)
- [49. v2.30 新機能（V3 への切り替えプロンプト）](49_v230NewFeatures.md)
- [34. /upgrade-agent](34_v214UpgradeAgent.md)
- [25. AutoComplete（3.0.0 で廃止）](25_AutoComplete.md)
- [18. Terminal UI](18_TerminalUI.md)
- [13. ACP](13_ACP.md)
- [09_v3/（Kiro CLI v3）](../09_v3/README.md)
- [CLI コマンドリファレンス](../04_reference/03_cli-commands.md)
- [設定リファレンス](../04_reference/01_settings.md)
- [公式インストール手順](../03_deployment/03_official-installation.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v3.0](https://kiro.dev/changelog/cli/3-0/)
- [Upgrade from CLI 2.x](https://kiro.dev/docs/cli/v3/)
- [Choose an agent harness](https://kiro.dev/docs/cli/agent-harness/)
- [Migration guide](https://kiro.dev/docs/cli/v3/migration-guide/)
- [Installation — Moving from the Kiro CLI desktop app](https://kiro.dev/docs/getting-started/installation/#moving-from-the-kiro-cli-desktop-app)
- [Migrate an ACP client to CLI V3](https://kiro.dev/docs/cli/v3/acp-migration/)
- `kiro-cli --help` / `kiro-cli chat --help` / `kiro-cli doctor`（実機 3.3.0）

**最終更新**: 2026-11-17
**対象バージョン**: Kiro CLI v3.0.0（v3.3.0 時点の公式ドキュメントと実機で確認）
