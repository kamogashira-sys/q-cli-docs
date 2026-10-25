[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.29 新機能

# 48. v2.29 新機能 — [V3] Memory・ディレクトリ単位のエージェントアップグレード・V3 ACP／MCP の挙動変更

## 概要

Kiro CLI **v2.29.0**（2026-10-09）と **v2.29.1**（2026-10-10）では、ローカルの V3 セッションで作業から得た有用なコンテキストを後のチャットセッションで呼び出せる **Memory**（`/memories`）が追加されました。あわせて、`kiro-cli agent upgrade <dir>` によるディレクトリ単位のエージェントアップグレード、V2 TUI の Hook のグループ一致、Classic と V2 の Knowledge 検索の修正が入りました。⚠ V3 の ACP のサインイン既定と、V3 の MCP サーバーの起動・環境が変わっています。

- **v2.29.0**: [V3] Memory、⚠ [V3] ACP のサインイン、⚠ [V3] MCP サーバーの起動、⚠ [V3] MCP サーバーの環境、プロファイルごとの Device flow 制御、`kiro-cli agent upgrade <dir>`、V2 TUI の Hook グループと `tool_tags`、バグ修正 16 件
- **v2.29.1**: Classic と V2 の MCP OAuth サインインを、issuer を要求するサーバーで動作するよう修正（系列ページ `changelog/cli/2-29/` の Patches 節の 1 件）

公式 Changelog の Learn more リンクがあるのは Memory だけです（`/docs/memory/`）。それ以外の項目は、関連する公式ドキュメントの本文を取得して確認できた範囲だけを書いています。確認できなかった点は「未確認」と明記しています。

## [V3] Memory — チャットセッションをまたぐコンテキスト

Kiro が作業から有用なコンテキストを学び、後のセッションで必要になったときに呼び出します。たとえば、デバッグ中に「リポジトリの結合テストは、ローカルデータベースを投入するまで失敗する」と学んでいれば、後のセッションは原因を調べ直さず、先にデータベースを投入できます（公式 Changelog v2.29.0 および公式 [Memory](https://kiro.dev/docs/memory/)）。

### 仕組み

公式 Memory（Page updated: 2026-10-20）は次のように説明しています。

- Memory は Kiro のエージェントハーネスの一部で、リポジトリのコマンドや規約、訂正、デバッグで得た知見、すでに除外した方法、好みの作業の進め方を覚えられる
- 各メモリは、タイトル・説明・内容を持つ記録で、過去の会話のコピーではない
- メモリはユーザーアカウントごとにローカルへ保存され、ワークスペースごとではない。同じマシンの Kiro IDE と Kiro CLI は保存されたメモリを共有するが、Memory の設定は各アプリが別々に持つ
- Memory は現在の会話・Steering・参照資料を置き換えない。常に守らせたいルールは Steering に書く（→ [23. Steering](23_Steering.md)）
- Kiro CLI の Memory には V3 が必要

### アクセスレベルの設定（`/memories` > `config`）

ローカルの V3 セッションで `/memories` と入力し、`config` を選んで、アクセスレベルを選びます。`read & write` を選んだ場合は、**Automatic memory updates** のオン・オフを選べます。

| アクセス | 動作（公式 Memory） |
|---------|--------------------|
| `read & write` | Kiro がメモリを使い、権限の範囲で変更できる。メモリの追加・更新・削除ができるのはこのレベルだけ |
| `read only` | 既存のメモリを使うが、変更も自動更新もしない |
| `off` | メモリを使わず、変更もしない |

- アクセスの変更は、新しい Kiro CLI セッションを開始したときに適用される
- **Automatic memory updates** は、Kiro が自分でメモリを管理する設定。ヘルプテキストは「Automatically create and refine memories, including after a session ends.」で、`read & write` が必要。この設定の変更は即座に適用される
- `read & write` でも、信頼していないワークスペースでは、チャットからメモリを追加・変更・削除できない。読み取りはできる

### 保存済みメモリの確認（`/memories` > `list`）

`/memories` を入力して `list` を選ぶと、保存されたメモリを閲覧・プレビューできます。

- メモリには、情報の種類を示す **type** と、適用先を示す **scope** がある。1 つのリポジトリに結び付いたメモリの scope は `repo:github/<owner>/<repository>` の形で表示される
- 入力して一覧を絞り込める。一覧には保存されているメモリの件数が表示される
- 各行にタイトル・1 行の説明・更新からの経過時間が表示される
- `ctrl+p` またはクリックでプレビュー（type・scope・更新時刻・説明）、`Enter` またはダブルクリックで全体（内容・ID・タイムスタンプを追加）を開く
- 一覧では閲覧とプレビューができる。メモリの修正は、チャットで Kiro に依頼する（`read & write` の信頼済みワークスペースでのみ可能）。v2.34.0 以降は、一覧または詳細の画面で `Ctrl+D` を押すと、選択したメモリを削除できる（`y` で確認、`n` で残す。→ [53. v2.34 新機能](53_v234NewFeatures.md)）

### セッションでの表示

Kiro がメモリを使うとき、作業中のチャットに **Memory** のエントリが表示されます。エントリには、Kiro がメモリを読んだことを示す `command=get` と、メモリのタイトルが含まれます。

```text
Memory
command=get, title=seed-db-before-integration-tests
```

### 実機 2.33.0 で確認した設定キー

公式 Settings リファレンス（Page updated: 2026-10-15）には Memory の設定キーが掲載されていません。実機 2.33.0 の `kiro-cli settings list --all` には次の 2 つが表示されます。

| 設定キー | 実機の説明 |
|---------|----------|
| `memory.mode` | Default memory access for new sessions: `read_write`, `read_only`, or `disabled`; requires the KAS engine |
| `memory.reflection` | Automatic memory updates for new sessions; takes effect only with `read_write` access（boolean） |

`/memories` の `config` 画面の項目（`read & write`・`read only`・`off`、**Automatic memory updates**）と、上の設定キーの値（`read_write`・`read_only`・`disabled`、`reflection`）の対応は、公式に記載がありません。実機の説明文の対応は読み取れますが、画面操作との対応は**未確認**です。説明にある「KAS engine」と V3 の対応関係も公式に記載がなく**未確認**です。

### 公式ドキュメントでの確認状況

- 公式 [Slash commands リファレンス](https://kiro.dev/docs/reference/slash-commands/)（Page updated: 2026-10-20）に `/memories` の見出しはありません。本サイトの [スラッシュコマンドリファレンス](../04_reference/02_slash-commands.md)（コマンド数の SSoT）にも載せていません。V3 専用コマンドの扱いは [09_v3/](../09_v3/README.md) を参照してください。
- Memory の保存場所のパス、保存件数の上限、メモリの内容を作成・更新する条件の詳細は、公式 Memory に記載がなく**未確認**です。
- 公式 Memory は IDE と Web の Memory も説明しています。IDE は **Kiro Agent: Memory** という単一のユーザー設定（既定は Off）、Web は「Memory support coming soon」と記載されています。本ページは CLI の記述だけを採っています。

## `kiro-cli agent upgrade <dir>` — ディレクトリ単位のアップグレード

トップレベルのエージェント JSON ファイルを、V2 と V3 の両方が読み込める形式にアップグレードします。`--dry-run` で書き込まずに変更をプレビューでき、`--no-backup` で既定のバックアップを省略できます（公式 Changelog v2.29.0）。V3 の `/upgrade-agent`（→ [34. /upgrade-agent](34_v214UpgradeAgent.md)）を説明する公式 Upgrading agent configs の「Upgrade one directory from the shell」節に、このコマンドの説明があります。

```bash
# 書き込まずに変更と警告をプレビューする
kiro-cli agent upgrade <directory> --dry-run

# アップグレードする（各ファイルのバックアップを残す）
kiro-cli agent upgrade <directory>
```

公式 [Upgrading agent configs](https://kiro.dev/docs/cli/v3/upgrade-agent/)（Page updated: 2026-10-13）の説明:

- 対象はディレクトリ直下の `*.json` で、サブディレクトリは検索しない
- 変更したファイルごとに `.bak` のバックアップを作る（既定）。`--no-backup` は、別の復旧用コピーがある場合だけ使う
- ドライランは、変更内容と変換の警告を報告する。macOS と Linux では、本番の実行で書き込めないファイルも報告する。どのファイルも変更しない
- エージェントでない JSON、外部管理のエージェント、regular file でないもの、同期が取れていない universal 設定、同じファイルへの重複パス、ディレクトリの外を指すシンボリックリンクはスキップする
- 終了コード: `0` はすべてのファイルがアップグレード・変更なし・スキップのいずれか、`1` は少なくとも 1 つのファイルが失敗、`2` はパスが存在しない・読めない・ディレクトリでない

実機 2.33.0 で確認した事項:

- `kiro-cli agent --help` の `upgrade` の説明は「Upgrade agent configs in a directory to the universal format both engines load. Rewrites top-level *.json files in place (subdirectories are not searched); already-universal, V3-only, out-of-sync, and externally managed agents are left untouched」で、公式の説明と一致する
- `kiro-cli agent upgrade <DIR> --dry-run` を、`fs_read` を使う `preToolUse` Hook を持つ V2 形式のエージェント 1 件の一時ディレクトリで実行すると、`would upgrade`（警告 1 件）と、警告 `widened-hook-matcher`（matcher `fs_read` が `read` になり、`grep`・`glob`・`code`・`introspect`・`tool_search` にも一致するようになる旨）が表示され、ファイルは変更されなかった

## Hook のグループ一致 — V2 TUI と `/upgrade-agent`

### V2 TUI の Hook グループと `tool_tags`

v2.29.0 では、V2 TUI の Hook で `read` などのマッチャーが、そのグループのすべてのツールを対象にするようになりました。ブロックする `preToolUse` Hook は、グループ内のどのツールも止められます。ツールの Hook は `tool_tags` を受け取り、スクリプトがツールのグループを確認できます（公式 Changelog v2.29.0）。

公式 [Hooks migration](https://kiro.dev/docs/cli/v3/hooks-migration/)（Page updated: 2026-10-10）の説明:

| マッチャー | V2 のグループに含まれるツール |
|-----------|-------------------------|
| `read` | `fs_read`・`grep`・`glob`・`code`・`introspect`・`tool_search` |
| `write` | `fs_write`・`code` |
| `shell` | `execute_bash` |
| `web` | `web_fetch`・`web_search` |
| `subagent` | `use_subagent` |

```json
{
  "tool_name": "fs_read",
  "tool_tags": ["read", "@builtin"],
  "tool_input": {}
}
```

- V2 エンジンで動くツール Hook が `tool_tags` を `tool_name`・`tool_input` とともに受け取る。Classic と V3 のエンジンは `tool_tags` を送らない
- Classic エンジンは `read`・`write`・`shell`・`subagent` を 1 つのツールの別名として扱い、`@mcp` マッチャーとタグのグロブには対応しない

### V3 `/upgrade-agent` の旧マッチャーの書き換え

V3 の `/upgrade-agent` は、`fs_read` などの旧形式の Hook マッチャーを、動作するように書き換え、書き換えでマッチが広がる場合は警告します（公式 Changelog v2.29.0 のバグ修正）。公式 Hooks migration によると、`fs_read` は `read` に、`execute_cmd` は `shell` になります。`fs_read` の書き換えは `grep`・`glob`・`code`・`introspect`・`tool_search` にも一致します。

V3 での Hook のカテゴリ一致（v2.28.0）は [47. v2.28 新機能](47_v228NewFeatures.md)、Hook 全般は [22. Hooks](22_Hooks.md) を参照してください。

## ⚠ [V3] ACP のサインインと MCP の挙動変更

### [V3] ACP のサインイン

`kiro-cli acp` が既定で Kiro CLI のログインを使うようになりました。接続するクライアントがサインインを扱う場合は `--auth-method=client` を渡します（公式 Changelog v2.29.0）。

公式 [Migrate an ACP client to CLI V3](https://kiro.dev/docs/cli/v3/acp-migration/)（Page updated: 2026-10-09）の説明:

```bash
# CLI V3 サーバーを明示的に起動する（既定は Kiro CLI のログインでアクセストークンを解決する）
/full/path/to/kiro-cli acp --agent-engine=v3
```

- CLI V3 の既定は、アクセストークンの要求を Kiro CLI のログインで処理する
- クライアントが、エージェントからクライアントへの `_kiro/auth/getAccessToken` 要求に応答する必要がある場合は `--auth-method=client` を渡す。サーバーを `--auth-method=client` で起動したときは、この要求への応答が必須になる
- クライアントがサインインを担う場合は、トークンの値をログや診断に出さないよう保護する

実機 2.33.0 の `kiro-cli acp --help` で確認した事項:

| オプション | 実機の説明 |
|----------|----------|
| `--agent-engine <ENGINE>` | `v1`・`v2`・`v3` から選ぶ。既定は `v2` |
| `--auth-method <METHOD>` | 「Authentication owner for the v3 engine」。既定は `cli`（Kiro CLI の認証情報ストアから解決）。`client` はエンジンのアクセストークン要求を ACP クライアントへ転送する |

したがって、`--auth-method` が効くのは V3 エンジンを選んだときです。V2 エンジン（既定）での `--auth-method` の扱いは公式に記載がなく**未確認**です。公式 [ACP](https://kiro.dev/docs/cli/acp/)（Page updated: 2026-10-02）は CLI v2 の ACP サーバーの説明で、`--auth-method` の記載はありません。ACP 全般は [13. ACP](13_ACP.md) を参照してください。

### [V3] MCP サーバーの起動と環境

| 変更（公式 Changelog v2.29.0） | 公式ドキュメントでの確認 |
|----------------------------|------------------------|
| カスタムエージェントは、ツール設定が許可する `mcp.json` のサーバーだけを起動する | 公式 [Agent config changes](https://kiro.dev/docs/cli/v3/agent-config/)（Page updated: 2026-10-10）は `includeMcpJson` を「ワークスペースの `.kiro/settings/mcp.json` のサーバーを含める」と説明しているが、「ツール設定が許可するサーバーだけを起動する」という記述は確認できなかった（**未確認**） |
| `stdio` の MCP サーバーが、エージェントの環境全体を継承する | 公式 [MCP configuration](https://kiro.dev/docs/mcp/configuration/)（Page updated: 2026-10-07）は `env` を「サーバープロセスの環境変数」と説明しているが、環境全体の継承に関する記述は確認できなかった（**未確認**） |
| サブエージェントとして起動された V3 のカスタムエージェントが、自身の `mcpServers` を読み込む（バグ修正） | 公式 [Sub-agents](https://kiro.dev/docs/custom-agents/subagents/)（Page updated: 2026-10-02）は、MCP サーバーがメインエージェントと共有されると説明しているが、この修正に関する記述は確認できなかった（**未確認**） |

これら 2 件は公式 Changelog の「変更」に分類された挙動変更で、V3 でカスタムエージェントを使っている場合は、`mcp.json` のサーバーの起動と stdio サーバーの環境が従来と異なります。公式ドキュメントに詳細がないため、自分の環境で確認してください。

### Device flow サインインの制御

管理者は Kiro のプロファイルごとに Device flow サインインを無効にできます。CLI は Device flow でのログインとプロファイル切り替えの際にそれらのプロファイルを非表示にし、ブラウザでのサインインは引き続き利用できます（公式 Changelog v2.29.0）。

公式 [Authentication](https://kiro.dev/docs/getting-started/authentication/)（Page updated: 2026-10-17）は同じ内容を説明し、利用できるプロファイルが残らない場合は、ブラウザでサインインできるマシンで `kiro-cli login` を実行するよう案内しています。Device flow は [12. Remote Authentication](12_RemoteAuth.md) を参照してください。

## Knowledge 検索・MCP OAuth・その他の修正

### Classic と V2 の Knowledge 検索

Classic と V2 の Knowledge 検索が、すべてのベースにわたる 1 つにまとまった結果セットを返し、ページネーションを共有し、指定した上限とファイル種別を検索全体に適用するようになりました（公式 Changelog v2.29.0 のバグ修正）。

- 公式 [Knowledge Management](https://kiro.dev/docs/cli/experimental/knowledge-management/)（Page updated: 2026-08-04）は、この結果セットの統合の動作を記述していません（**未確認**）。
- 公式 [Slash commands の `/knowledge`](https://kiro.dev/docs/reference/slash-commands/#knowledge) は、V3 で knowledge が既定で有効であり、V1 と V2 では experimental で `kiro-cli settings chat.enableKnowledge true` により有効にすると記載しています。

### MCP OAuth（v2.29.0 と v2.29.1）

- **v2.29.0**: V2 と V3 が MCP OAuth の認可 URL を表示し、SSH や tmux のセッションからも開けるよう修正された。
- **v2.29.1**: Classic と V2 の MCP OAuth サインインが、issuer を要求するサーバーで動作するよう修正された（系列ページの Patches 節）。

公式 [MCP configuration](https://kiro.dev/docs/mcp/configuration/)（Page updated: 2026-10-07）は、OAuth で保護されたリモート MCP サーバーのブラウザ認証を Kiro が処理すること、認可サーバーの `issuer` が RFC 8414 に従って一致する必要があることを記載しています。ただし、これらの修正（認可 URL の表示、issuer を要求するサーバーへの対応）との対応関係は公式に記載がなく**未確認**です。OAuth の管理は [32. MCP OAuth 認証管理](32_MCPOAuthManagement.md) を参照してください。

### その他のバグ修正（v2.29.0）

公式ドキュメントでの確認ができていない項目を含め、changelog の記述を要約します。完全な一覧は [変更履歴の v2.29.0](../02_update/01_changelog.md) を正とします。

| 分類 | 内容 |
|------|------|
| 🔒 セキュリティ | Classic の `fs_write` が、シンボリックリンクによって `allowedPaths` の外へ向けられた書き込みを自動承認しない |
| モデル | Classic と V2 のモデルフォールバックの変更が、再起動なしで現在のセッションに反映される。V3 が、既定のモデルが effort に対応している場合に、セッション開始時に effort セレクターを表示する |
| テレメトリ | V3 の非対話実行が、`telemetry.enabled` と `KIRO_DISABLE_TELEMETRY` に従う（公式 Settings リファレンスに `telemetry.enabled` はあるが、`KIRO_DISABLE_TELEMETRY` の記載は確認できなかった） |
| V3 の安定性 | 高負荷時にセッションが閉じられる可能性があった問題、JSON でないエラーページを返されたときの再試行メッセージ、新しいプロンプトが届いたときに終了しかけていたターンの履歴保持、MCP サーバーの起動中に送信したプロンプトの Stop によるキャンセル |
| V3 のセッション再開・Steering | 再開したセッションが `UserPromptSubmit` Hook の出力を会話に保持する。プロンプトの途中にスラッシュコマンドが現れた場合も手動の Steering ファイルを読み込む |
| V3 の入出力 | 選択したモデルに収まるよう画像をリサイズする。`us-east-1` 以外で発行された `KIRO_API_KEY` が、そのホームリージョンで認証される |

## 関連リンク

### 本サイト

- [47. v2.28 新機能](47_v228NewFeatures.md)
- [49. v2.30 新機能](49_v230NewFeatures.md)
- [34. /upgrade-agent](34_v214UpgradeAgent.md)
- [22. Hooks](22_Hooks.md)
- [13. ACP](13_ACP.md)
- [12. Remote Authentication](12_RemoteAuth.md)
- [32. MCP OAuth 認証管理](32_MCPOAuthManagement.md)
- [23. Steering](23_Steering.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.29](https://kiro.dev/changelog/cli/2-29/)
- [Memory](https://kiro.dev/docs/memory/)
- [Upgrading agent configs](https://kiro.dev/docs/cli/v3/upgrade-agent/)
- [Hooks migration](https://kiro.dev/docs/cli/v3/hooks-migration/)
- [Migrate an ACP client to CLI V3](https://kiro.dev/docs/cli/v3/acp-migration/)
- [ACP](https://kiro.dev/docs/cli/acp/)
- [Authentication](https://kiro.dev/docs/getting-started/authentication/)
- [MCP configuration](https://kiro.dev/docs/mcp/configuration/)
- [Knowledge Management](https://kiro.dev/docs/cli/experimental/knowledge-management/)
- `kiro-cli settings list --all` / `kiro-cli agent --help` / `kiro-cli agent upgrade --help` / `kiro-cli acp --help`（実機 2.33.0）

**最終更新**: 2026-10-25
**対象バージョン**: Kiro CLI v2.29.0+（Memory・V3 ACP／MCP の挙動変更は V3 Early Access、`agent upgrade` は V2・V3 の両方が読む形式へ変換するコマンド）
