[ホーム](../README.md) > Kiro CLI v3（Early Access）

# 09. Kiro CLI v3（Early Access）概要

> ⚠️ **Early Access の注意**: Kiro CLI v3（公式表記「**CLI 3.0**」「**V3**」）は **Early Access（先行公開）** です。**v2.8.0 以降の 2.x に `--v3` フラグで同梱**され、オプトインで試せます。GA（正式版）としての「3.0.0」はまだリリースされていません。**仕様は変更される可能性があり**、本セクションの内容は公式ドキュメント更新に追従して見直します。

> 💡 **どちらを読めばいい？**: 普段の利用では、まず **v2 系のドキュメント**（[機能詳細ガイド](../01_features/README.md)・[リファレンス](../04_reference/README.md)）を参照してください。本セクション（09_v3/）は「v3 を先行して試したい人」向けです。

**位置付け**: v3 は単一機能の追加ではなく、**エージェント実行基盤（エンジン）の刷新＋仕様駆動開発（Spec-driven development）の導入**という「開発パラダイムの更新」です。そのため本サイトでは独立セクション（`09_v3/`）にまとめています。

**出典（一次情報）**:
- [Kiro CLI v3 概要（公式・What's new in CLI 3.0）](https://kiro.dev/docs/cli/v3/)
- [Spec-driven development（公式・機能自体）](https://kiro.dev/docs/specs/)
- [新機能一覧（公式 New features in 3.0）](https://kiro.dev/docs/cli/v3/new-features/)
- [Permissions（公式・機能自体）](https://kiro.dev/docs/permissions/) ／ [Hooks（公式・機能自体）](https://kiro.dev/docs/hooks/) ／ [Agent config changes（公式・v3移行）](https://kiro.dev/docs/cli/v3/agent-config/)
- [公式 Changelog v2.8](https://kiro.dev/changelog/cli/2-8/)

> **出典URLについての注記**: kiro.dev は 2026-08-04〜08-12 に v3 関連ドキュメントを再構成しました。旧 `/docs/cli/v3/specs/` は `/docs/specs/` への移転スタブとなり、`/docs/cli/v3/feature-overview/` は存在しなくなりました（機能比較・Breaking changes は `/docs/cli/v3/` 本体のアンカーに統合）。`/docs/cli/v3/permissions/`・`/docs/cli/v3/hooks-migration/`・`/docs/cli/v3/agent-config/` は v3 移行ガイド専用ページとして現存します。本ページの出典は再構成後の現行 URL に更新済みです（2026-08-16 確認）。

---

## このセクションの構成

- **本ページ（README）** — v3 の全体像、4 本柱、Breaking changes / Known gaps、Early Access の位置付け
- **[01. 仕様駆動開発（Spec-driven development）](01_spec-driven-development.md)** — `/spec` を使った CLI での実践、`.kiro/specs/` の3ファイル、AI-DLC との違い
- **[02. Kiro IDE 版との比較](02_kiro-ide-vs-cli.md)** — 「同様にできること／IDE が優位なこと／CLI ならではのこと」を一次情報ベースで整理

---

## v3 とは（統一エンジンとメジャー更新）

Kiro CLI v3 の核心は **「統一エンジン（single engine for all Kiro surfaces）」** です。CLI 3.0 は Kiro IDE / Kiro Web と**同じエージェント基盤**の上に構築され、エンジン側の改善（新しいツール、計画立案、ツール選択など）が**全クライアントへ同時に届く**ようになりました。

- **試し方**: `kiro-cli --v3` で V3 エンジンを起動（オプトイン）。
- **併存**: 既存の **2.x と併存**します。設定を変えずにそのまま試せます。
- **提供形態**: v2.8.0（公式表示日 2026-06-17）で **Early Access** として先行公開されました。

```bash
# V3 エンジンを試す（既存 2.x はそのまま）
kiro-cli --v3
```

---

## v3 の 4 本柱

公式 v3 ドキュメントは、v3 の新規性を次の 4 つで説明しています。

| 柱 | 概要 | 詳細 |
|----|------|------|
| **仕様駆動開発**（Spec-driven development） | 組み込みの **Spec agent**。要件 → 設計 → タスク → 実行を計画してから進める | [01. 仕様駆動開発](01_spec-driven-development.md)、[公式](https://kiro.dev/docs/specs/) |
| **Capability ベースの権限**（Permissions） | `permissions.yaml` に許可/拒否ルールを宣言。`--trust-all-tools` / `/tools trust` を置換 | [公式 Permissions](https://kiro.dev/docs/cli/v3/permissions/) |
| **強化版 Hooks** | 独立ファイル `.kiro/hooks/*.json`（バージョン付きスキーマ）、2 アクション型（shell / agent）、新トリガ | [公式 Hooks migration](https://kiro.dev/docs/cli/v3/hooks-migration/) |
| **強化版 Agent 設定** | タグでツール種別を選択、`permissions` ブロック統合、Markdown 形式、inline MCP | [公式 Agent config](https://kiro.dev/docs/cli/v3/agent-config/) |

### 4 本柱のポイント（一次情報の要約）

- **Permissions**: 1 つのルールは `capability`（操作種別）/ `match`（グロブ）/ `exclude` / `effect`（`deny`・`ask`・`allow`）の 4 フィールド。効果は **deny > ask > allow** の順で厳しい方が勝ちます。ルールは **User**（`~/.kiro/settings/permissions.yaml`）と **Workspace**（`~/.kiro/workspace-roots/<hash>/permissions.yaml`、**リポジトリ外・ユーザー単位**で保持されるためクローンしたリポジトリが権限を注入できない）の2スコープ。CI 向けには `capability: all / effect: allow` の例が示されています。
- **Hooks**: `.kiro/hooks/<name>.json`（`"version": "v1"`）に定義。**command**（シェル実行、stdin に JSON、終了コード 0=成功 / 2=ブロック）と **agent**（プロンプトを文脈へ追記）の 2 型。トリガは `SessionStart` / `SessionEnd`（v2.25.0 追加）/ `Stop` / `PreToolUse` / `PostToolUse` / `UserPromptSubmit` / `PostFileCreate` / `PostFileSave` のほか、**3.0 新規**の `PreTaskExec` / `PostTaskExec` / `PostFileDelete` / `Manual`。旧 hooks は `kiro-cli agent migrate` で新形式へ変換できます。**v2.13.0（2026-07-17）** では、`~/.kiro/hooks/` に置いた**グローバル hooks** が追加され、**全ワークスペースへ自動適用**されるようになりました（従来のワークスペース単位 `.kiro/hooks/` に加えた、ユーザーグローバルの適用先）。
- **Agent 設定**: Markdown の本文がシステムプロンプト、フロントマターに `description` / `model` / `tools`（タグ）/ `mcpServers` / `resources` / `permissions` / `welcomeMessage` を記述（JSON でも等価）。タグは `read` / `write` / `shell` / `web` / `subagent` / `knowledge` / `todo_list` / `@mcp` / `@builtin` / `*`。新しいツールがカテゴリに追加されると**自動で取り込まれます**。配置は `.kiro/agents/`（ワークスペース）・`~/.kiro/agents/`（ユーザー）。

### v2.13.0 での追加（Introspect サブエージェント・グローバル hooks）

**v2.13.0（2026-07-17）** で、V3（Early Access）に2つの機能が追加されました。

- **Introspect サブエージェント**: Kiro の機能に関する質問に答え、**カスタムエージェント・hooks・steering の作成を支援**する組み込みサブエージェント。Spec agent（仕様駆動）に加わる新しい組み込みエージェントで、v3 の設定（上記 4 本柱）を書く際の対話的なガイドとして使えます。
- **グローバル hooks**: `~/.kiro/hooks/` に置いた hooks が**全ワークスペースへ自動適用**されます（詳細は上記「Hooks」ポイント）。プロジェクト横断で共通のフック（例: セッション開始時の共通セットアップ）をユーザー単位で一元管理できます。

出典: [公式 Hooks migration](https://kiro.dev/docs/cli/v3/hooks-migration/)、[公式 Changelog v2.13](https://kiro.dev/changelog/cli/2-13/)。

### v2.14.0 での追加（`/upgrade-agent`・自動ストリームリトライ）

**v2.14.0（2026-07-22）** で、V2 のカスタムエージェント設定を **V2/V3 両対応の universal 形式へ変換する `/upgrade-agent`** が追加されました。

- **`/upgrade-agent`**: V3 セッション内で実行し、`.kiro/agents/`（ワークスペース）と `~/.kiro/agents/`（ユーザー）をスキャンして変換対象を選択。元ファイルは `<filename>.json.bak` にバックアップされ、既存設定に併存する形で新形式の権限フィールドが追加されます。`/upgrade-agent diagnostics` で変換警告（`regex-shell-pattern` 等 8 種）を確認できます。
  → 詳細: [01_features/34. v2.14 /upgrade-agent](../01_features/34_v214UpgradeAgent.md)、[公式ドキュメント](https://kiro.dev/docs/cli/v3/upgrade-agent/)
- **自動ストリームリトライ**: 空で届いた応答・ストリーム途中で切り詰められた応答を自動的に再試行。
- **バグ修正**: カスタムエージェント切替後に model・effort の選択肢が更新される、`/plan` が複数の確認質問でデッドロックしない、アクティブなエージェントが自身のサブエージェント委譲リストに出ない、supervised モードのターン承認がセッション再開後も維持される、`web_fetch` の二重リトライを 1 回へ統合、不正なツール入力時のエラーメッセージ改善。

出典: [公式 Changelog v2.14](https://kiro.dev/changelog/cli/2-14/)、[Upgrading agent configs（公式）](https://kiro.dev/docs/cli/v3/upgrade-agent/)。

### v2.19.0 での追加（session resume タイトル要約・MCP protocol revision 対応）

**v2.19.0（2026-08-19）** で、V3 に2つの改善が追加されました。

- **session resume ピッカーのAI生成タイトル**: セッション再開ピッカーに、最初のプロンプトを要約した短いAI生成タイトルが表示されるようになりました。似た内容のセッションが並んでいても識別しやすくなります。
- **MCP protocol revision 2026-07-28 対応**: このprotocol revisionを要求するMCPサーバーへの接続に対応しました。

出典: `kiro-cli version --changelog=2.19.0`、[公式 Changelog v2.19](https://kiro.dev/changelog/cli/2-19/)。

### v2.20.x での追加（全画面 Spec 実行・`/powers`）

**v2.20.0（2026-08-26）** では、`/spec run` に専用の**全画面タスク実行ビュー**が追加されました。実行中の進捗をリアルタイムで追跡でき、実行開始前にタスクスコープを選択できます。

**v2.20.1（2026-08-27）** では、インストール済み Powers を表示する **`/powers`** が追加されました。Powers は Agent Plugins 形式で tools・Skills・ナレッジ・ワークフローをまとめ、会話のキーワードに応じてオンデマンドで活性化します。CLI での Powers の install / use / create は V3 対応です。

→ 詳細: [39. v2.20 新機能](../01_features/39_v220NewFeatures.md)、[Specs（公式）](https://kiro.dev/docs/specs/)、[Powers（公式）](https://kiro.dev/docs/powers/)

### v2.21.x での追加（セッションダッシュボード・設定パネル・クラウド設定・セッション検索）

**v2.21.0（2026-09-01）** では、V3 限定の機能が次のとおり追加されました。

- **セッションダッシュボード（`/sessions`）**: ローカルまたはクラウドに保存された過去セッションを閲覧・検索・再開・整理する。起動時に `kiro-cli chat --sessions` を渡すとダッシュボードへ直接入り、閉じるとチャットに落ちずに終了する。
- **設定パネル（`/config`）**: 設定済みの agents・MCP servers・Powers・Steering・Skills・Hooks を 1 画面で表示。ソース情報が利用可能な場合、各項目を local / cloud / both として識別する。
- **ローカルセッションへのクラウド設定適用**: Kiro Web の Configuration Sync でアップロードした個人の `.kiro` 設定を、新規ローカル V3 セッションへ適用する（**ローカルの `.kiro` にファイルは書き込まれない**）。

**v2.21.3（2026-09-10）** では、インストール済み Powers が **`/` コマンドピッカー**に表示されるようになりました（v2.20.1 の `/powers` に続く呼び出し経路の拡張）。

**v2.21.4（2026-09-11）** では、`/sessions` の検索がセッションタイトル・プロンプトに加えて**エージェントの応答**もインデックスするようになりました。`/settings` の **Session search** で **Prompts only** と **Prompts and agent responses** を切り替えます（**ツール出力はどちらのモードでもインデックスされない**）。実機 2.21.4 の対応キーは `chat.sessionDashboard.indexResponses` です。

あわせて **`--v2`** フラグが追加され、1 回の実行だけを V2 ハーネスで走らせられます（保存済み既定は上書きしない）。

> **V3 限定であることの確認**: セッションダッシュボードを V2 で開こうとすると「Session dashboard is available on the V3 (KAS) engine only」の警告が表示されます。`/sessions`・`/config` は V2 安定版のスラッシュコマンド数には含めず、本セクションで扱います。

→ 詳細: [40. v2.21 新機能](../01_features/40_v221NewFeatures.md)、[Session management（公式）](https://kiro.dev/docs/cli/chat/session-management/)、[Configuration（公式）](https://kiro.dev/docs/configuration/)、[Cloud configuration（公式）](https://kiro.dev/docs/web/cloud-configuration/)

### v2.22.0〜v2.27.1 での追加（Workflows・`/tools trust-all`・Output style・`SessionEnd` ほか）

V3 限定の追加・変更は次のとおりです（V2 でも使える `/fullscreen`・`/model` の推論設定は [41](../01_features/41_v222NewFeatures.md)・[42](../01_features/42_v223NewFeatures.md) を参照）。

| 版 | V3 の追加・変更 | 詳細 |
|----|---------------|------|
| v2.22.0 | `/sessions` の再設計（操作部と一覧の分離、ソートの記憶）、大きなツール結果をセッションへ保存しモデルにはプレビューを渡す | [41](../01_features/41_v222NewFeatures.md) |
| v2.23.0 | リポジトリ接続前のクラウドセッション（後から `/repo`） | [42](../01_features/42_v223NewFeatures.md) |
| v2.24.0 | **`/tools trust-all`**（セッション全体の自動承認。既定で安全警告と確認）、`/sessions` の Filter・Sort・Group とフィルタの組み合わせ | [43](../01_features/43_v224NewFeatures.md) |
| v2.24.1 | `/sessions` の既定が現在のディレクトリ（`chat.sessionDashboard.scope`）、引数なしの `/effort` が `/model` の Effort 設定を開く | [43](../01_features/43_v224NewFeatures.md) |
| v2.25.0 | **`/powers install <name\|path>`・`/powers uninstall <name>`**（ローカルセッションのみ）、**Output style**（`chat.outputStyle`）、**`SessionEnd` Hook トリガー** | [44](../01_features/44_v225NewFeatures.md) |
| v2.26.0 | **Workflows**（`/settings features` で有効化・再起動、`/workflow`）、Hook・LSP 書き込みのファイル単位承認、未信頼ワークスペースでの MCP・shell の都度承認、実行直前の承認再確認 | [45](../01_features/45_v226NewFeatures.md) |
| v2.26.1 | OS の証明書ストアを既定で信頼（`NODE_USE_SYSTEM_CA` の明示値が優先） | [45](../01_features/45_v226NewFeatures.md) |
| v2.27.0 | **Workflows: sub-agent tool**（`chat.enableMainAgentSubagentTool`）、Steering の行指定・行範囲・`#[[folder:...]]`、**保存済みプロンプトのスラッシュコマンド化**、⚠️ **`todo_list` ツールの廃止**（`chat.enableTodoList` は V3 で無効）、Output style が `/settings display` 配下へ移動 | [46](../01_features/46_v227NewFeatures.md) |
| v2.27.1 | **`/tangent merge [dest]`**、非対話実行での hooks・knowledge・code intelligence 対応、`--no-interactive` の Workflows の完了までの接続維持と進捗・使用量の計上（CLI 内蔵 changelog のみで確認、公式 Changelog 未掲載） | [46](../01_features/46_v227NewFeatures.md) |

**Hooks のトリガー**: v2.25.0 で `SessionEnd`（V3 セッションの終了時）が加わりました。公式 [Hook types](https://kiro.dev/docs/hooks/types/) の記載は「The `SessionEnd` trigger fires when a CLI V3 session is torn down.」の 1 文のみです。

> **V3 専用コマンドの扱い**: `/workflow`・`/sessions`・`/config`・`/powers` は V2 安定版のスラッシュコマンド数（[04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md)）に含めず、本セクションで扱います。公式 [Slash commands](https://kiro.dev/docs/reference/slash-commands/) には `/workflow` のサブコマンド（`run`・`new`・`list`・`status`・`pause`・`resume`・`cancel`・`retry`）が掲載されています（→ [45](../01_features/45_v226NewFeatures.md)）。

---

## Breaking changes（v2 → v3）

v3 は **後方互換ではない変更**を含みます。切り替え前に確認してください。

| 領域 | 変更内容 |
|------|----------|
| **権限** | `--trust-all-tools` / `/tools trust` を **`permissions.yaml`** で置換（※v2.24.0 で V3 にもセッション限定の自動承認 `/tools trust-all` が追加。公式 [Permissions](https://kiro.dev/docs/permissions/) は `--trust-all-tools` が CI 向けのセッション単位の上書きとして引き続き動作すると説明） |
| **Hooks** | 埋め込み hooks を**独立ファイル** `.kiro/hooks/*.json` へ。トリガ名は PascalCase |
| **Agent 設定** | `toolsSettings` を **`permissions`** フィールドへ、個別ツール ID を**タグ**へ |
| **aws_tool** | **削除**（MCP サーバーで代替） |
| **セッション形式** | v3 形式は**後方互換なし**。切り替え前に `~/.kiro/sessions/` をバックアップ推奨 |

> **移行手段（v2.14.0 で追加）**: V2 のカスタムエージェント設定は **`/upgrade-agent`**（V3 セッション内で実行）で V2/V3 両対応の universal 形式へ変換できます。公式 [v3 概要](https://kiro.dev/docs/cli/v3/) も同コマンドと [migration guide](https://kiro.dev/docs/cli/v3/upgrade-agent/) を案内しています。→ [01_features/34. v2.14 /upgrade-agent](../01_features/34_v214UpgradeAgent.md)
>
> ⚠️ **Supervised mode についての注記**: 公式 [Changelog v2.14](https://kiro.dev/changelog/cli/2-14/)（v2.14.0）のバグ修正には「[V3] supervised モードのターン承認がセッション再開後も維持される」という項目があり、当時 V3 に supervised モードが存在したことが分かります。しかし、**2026-08-16 時点の公式 v3 概要ページ（[What's new in CLI 3.0](https://kiro.dev/docs/cli/v3/)）の Feature overview 表・Breaking changes 表のいずれにも「Supervised mode」の記載は存在しません**（旧版で本サイトが出典としていた「Removed（permissions.yaml で代替）」という記載も現行ページには見当たりません）。現状は公式ドキュメント上で言及が確認できないため、本サイトも断定を避け、Changelog の事実のみを記録します。

### v2 の類似機能を置き換える新機能（Tangent）

Breaking changes（置換・削除）とは別に、v2 に**名前や見た目が似た機能があった**ため注意が必要な新機能もあります。

| 領域 | 状況 |
|------|------|
| **Tangent**（`/tangent`） | 公式 [Feature overview](https://kiro.dev/docs/cli/v3/)（2026-08-12 更新版）ではステータス **「✅ New」**、Change from 2.x は「Named, nestable side-conversations」。公式 [Tangent ページ](https://kiro.dev/docs/cli/v3/tangent/) は「This page covers tangent in CLI 3.0 ... The earlier experimental tangent mode behaves differently — a single checkpoint toggled with `/tangent` or `Ctrl+T`, with no naming or nesting」と明記し、V2 classic 版とは**別物**であることを明示。コマンド名 `/tangent` は同じですが、V3 版は名前付き・ネスト可能・ビジュアルピッカー（`/tangent ls`）対応という別仕様です（→ [01_features/35. v2.16 Tangent（V3側枝会話）](../01_features/35_v216Tangent.md)、[04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md#tangent)） |

> 📝 **旧記述の訂正（2026-08-16）**: 本サイトは以前、Tangent を「⬆️ Enhanced（強化）」と分類し、公式が「replace the single-checkpoint experiment」と記載していると引用していましたが、現行の公式 Feature overview 表のステータスは **「✅ New」** であり、該当の引用文は現行公式ページのいずれにも存在しません。上記表は現行記述に基づき修正しています。

---

## Known gaps（既知の制限）

| 制限 | 内容 |
|------|------|
| **Amazon Linux 2 非対応** | CLI 3.0 は **AL2 では動作しません**。AL2 が必要な環境は CLI 2.x を使用 |
| **Classic mode 非対応** | レガシーの**非 TUI モード**（`kiro-cli chat` を TUI なしで使う形態）は v3 エンジン非対応。**TUI を使用** |
| **セッション再開の非互換** | **V3 セッションは V2 で再開不可**。V2 に戻すと、作成済みの V3 セッションは利用できません |

---

## 環境の確認

v3 を試す前後の環境確認には `kiro-cli diagnostic` が使えます（公式 v3 ドキュメントでも環境検証ツールとして案内）。

```bash
# 環境の診断テストを実行（出力形式は plain / json / json-pretty）
kiro-cli diagnostic
kiro-cli diagnostic --format json-pretty
```

---

## 関連リンク

### 本セクション内
- [01. 仕様駆動開発（Spec-driven development）](01_spec-driven-development.md)
- [02. Kiro IDE 版との比較](02_kiro-ide-vs-cli.md)

### 本サイトの関連文書
- [01_features/30. v2.8 / V3 プレビュー](../01_features/30_v28V3Preview.md) — v2.8.0 / v2.8.1 の事実と `--v3` の入口
- [01_features/33. v2.13 Introspect サブエージェント・グローバル hooks](../01_features/33_v213IntrospectGlobalHooks.md) — v2.13.0 の V3 追加機能
- [01_features/34. v2.14 /upgrade-agent](../01_features/34_v214UpgradeAgent.md) — V2 → V3 エージェント設定移行（v2.14.0）
- [01_features/41〜46. v2.22〜v2.27 新機能](../01_features/46_v227NewFeatures.md) — Workflows・`/tools trust-all`・Output style・`SessionEnd`・保存済みプロンプトのコマンド化ほか（[41](../01_features/41_v222NewFeatures.md)・[42](../01_features/42_v223NewFeatures.md)・[43](../01_features/43_v224NewFeatures.md)・[44](../01_features/44_v225NewFeatures.md)・[45](../01_features/45_v226NewFeatures.md)・[46](../01_features/46_v227NewFeatures.md)）
- [07_aidlc/](../07_aidlc/README.md) — AI-DLC（AWS Labs OSS 方法論）。v3 の純正 Spec agent とは別物（→ [01. 仕様駆動開発](01_spec-driven-development.md) の比較表）
- [02_update/01_changelog.md](../02_update/01_changelog.md) — v2.8.0 / v2.8.1 の変更履歴

### 公式情報源
- [Kiro CLI v3 概要（What's new in CLI 3.0）](https://kiro.dev/docs/cli/v3/)
- [Spec-driven development（機能自体）](https://kiro.dev/docs/specs/)
- [新機能一覧（New features in 3.0）](https://kiro.dev/docs/cli/v3/new-features/)
- [Tangent](https://kiro.dev/docs/cli/v3/tangent/)
- [Permissions（機能自体）](https://kiro.dev/docs/permissions/) ／ [Hooks（機能自体）](https://kiro.dev/docs/hooks/) ／ [Agent config changes（v3移行）](https://kiro.dev/docs/cli/v3/agent-config/)
- [Upgrading agent configs（`/upgrade-agent`）](https://kiro.dev/docs/cli/v3/upgrade-agent/)
- [Workflows](https://kiro.dev/docs/workflows/) ／ [Hook types](https://kiro.dev/docs/hooks/types/) ／ [Install powers](https://kiro.dev/docs/powers/installation/)

---

**最終更新**: 2026-10-04（v2.22.0〜v2.27.1 の V3 追加・変更（Workflows、`/tools trust-all`、`/powers install`・`uninstall`、Output style、`SessionEnd` Hook、保存済みプロンプトのコマンド化、`todo_list` の廃止、`/tangent merge` ほか）を追加）
**対象バージョン**: Kiro CLI v3（Early Access）— v2.8.x 以降 ＋ `--v3` で提供。3.0.0 GA は未リリース。
