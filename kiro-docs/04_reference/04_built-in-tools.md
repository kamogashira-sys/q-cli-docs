[ホーム](../../README.md) > [リファレンス](README.md) > Built-in Tools

# Kiro CLI Built-in Tools リファレンス

**出典**: [Built-in tools - Kiro CLI Documentation](https://kiro.dev/docs/cli/reference/built-in-tools/)（公式ページ最終更新: 2026-05-12）

Kiro CLI の組み込みツール（公式記載 18 種類）を網羅する辞書的リファレンスです。

> **世代差分注記**: Amazon Q Developer CLI 時代の組み込みツールは **9個** でしたが、Kiro CLI では **18個** に拡張されています（experimental 含む）。Q CLI 時代の記述（`kiro-docs/06_embedded-docs/kiro-cli/docs/built-in-tools.md`、197行。ローカル管理・GitHub 非公開）は **歴史的参考資料** として残置されています。本ファイルが Kiro CLI 一次情報に基づく正規版です。

---

## 📋 目次

- [ファイル系（read/glob/grep/write）](#ファイル系readglobgrepwrite)
- [実行系（shell/aws）](#実行系shellaws)
- [Web 系（web_search/web_fetch）](#web-系web_searchweb_fetch)
- [自己参照系（introspect/code）](#自己参照系introspectcode)
- [拡張系（tool_search/delegate/subagent）](#拡張系tool_searchdelegatesubagent)
- [補助系（report/knowledge/thinking/todo/session）](#補助系reportknowledgethinkingtodosession)
- [Side channels（v2.3.0+）](#side-channelsv230)
- [agent.json での設定方法](#agentjson-での設定方法)
- [ツール権限](#ツール権限)
- [Q CLI 時代との世代差分](#q-cli-時代との世代差分)
- [関連リンク](#関連リンク)

---

## ファイル系（read/glob/grep/write）

### `read`

**Aliases**: `fs_read`, `fsRead`  
**説明**: ファイル、フォルダ、画像を読み取る。

#### 設定オプション

| オプション | 型 | 必須 | 説明 |
|---------|-----|-----|------|
| `allowedPaths` | array of paths | No | プロンプトなしで読める許可パス |
| `deniedPaths` | array of paths | No | 拒否するパス |

パスは gitignore 同様のグロブパターンに対応。

```json
{
  "toolsSettings": {
    "read": {
      "allowedPaths": ["~/projects", "./src/**"],
      "deniedPaths": ["d1/denied/path/", "d2/denied/path/**/file.txt"]
    }
  }
}
```

### `glob`

**説明**: グロブパターンによる高速ファイル発見。`.gitignore` を尊重。bash の `find` より優先。

#### 設定オプション

| オプション | 型 | 既定値 | 説明 |
|---------|-----|------|------|
| `allowedPaths` | array of strings | `[]` | プロンプトなしで検索できる許可パス |
| `deniedPaths` | array of strings | `[]` | 拒否パス（allow より優先評価） |
| `allowReadOnly` | boolean | `false` | プロンプトなしですべての場所で検索を許可 |

```json
{
  "toolsSettings": {
    "glob": {
      "allowedPaths": ["~/projects", "./src/**"],
      "deniedPaths": ["/etc", "/var"],
      "allowReadOnly": true
    }
  }
}
```

### `grep`

**説明**: 正規表現による高速コンテンツ検索。`.gitignore` を尊重。bash の `grep`/`rg`/`ag` より優先。

#### 設定オプション

| オプション | 型 | 既定値 | 説明 |
|---------|-----|------|------|
| `allowedPaths` | array of strings | `[]` | プロンプトなしで検索できる許可パス |
| `deniedPaths` | array of strings | `[]` | 拒否パス |
| `allowReadOnly` | boolean | `false` | すべての場所で検索を許可 |

### `write`

**Aliases**: `fs_write`, `fsWrite`  
**説明**: ファイルの作成・編集ツール。

#### 設定オプション

| オプション | 型 | 必須 | 説明 |
|---------|-----|-----|------|
| `allowedPaths` | array of paths | No | プロンプトなしで書き込めるパス |
| `deniedPaths` | array of paths | No | 拒否パス |

```json
{
  "toolsSettings": {
    "write": {
      "allowedPaths": ["~/projects/output.txt", "./src/**"],
      "deniedPaths": ["/d1/denied/path/", "/d2/denied/path/**/file.txt"]
    }
  }
}
```

#### Custom diff tools

既定では組み込みのインライン diff を使用。外部 diff ツール（delta、difftastic、VS Code 等）を設定可能。詳細は [08. Custom Diff Tools](../01_features/08_CustomDiffTools.md)。

---

## 実行系（shell/aws）

### `shell`

**Aliases**: `execute_bash`, `execute_cmd`  
**説明**: 指定された bash コマンドを実行するツール。

#### 設定オプション

| オプション | 型 | 既定値 | 説明 |
|---------|-----|------|------|
| `allowedCommands` | array of strings | `[]` | プロンプトなしで許可するコマンド |
| `deniedCommands` | array of strings | `[]` | 拒否コマンド（allow より優先） |
| `autoAllowReadonly` | boolean | `false` | 読取専用コマンドを許可（書込は制限しない） |
| `denyByDefault` | boolean | `false` | `allowedCommands` 外＋`autoAllowReadonly` 非該当を拒否（プロンプト不可） |

```json
{
  "toolsSettings": {
    "shell": {
      "allowedCommands": ["git status", "git fetch"],
      "deniedCommands": ["git commit .*", "git push .*"],
      "autoAllowReadonly": true
    }
  }
}
```

> **正規表現**: `allowedCommands` と `deniedCommands` は正規表現（`\A`...`\z` で自動アンカー、look-ahead/behind 非対応）。

→ 詳細権限制御: [17. Granular Tool Trust](../01_features/17_GranularToolTrust.md)

### `aws`

**Aliases**: `use_aws`  
**説明**: 指定したサービス、操作、パラメータで AWS CLI を呼び出すツール。

```json
{
  "toolsSettings": {
    "aws": {
      "allowedServices": ["s3", "lambda", "ec2"],
      "deniedServices": ["eks", "rds"],
      "autoAllowReadonly": true
    }
  }
}
```

---

## Web 系（web_search/web_fetch）

Kiro エージェントがインターネット上の最新情報にリアルタイムアクセスする機能。**意味のある大量テキストを再生産しないよう設計**されており、ペイウォール・認証・アクセス制限の背後にあるページにはアクセスできません。

### `web_search`

**説明**: Web 検索ツール。

### `web_fetch`

**説明**: URL からコンテンツを取得するツール。

#### Fetch モード

| モード | 動作 | ユースケース |
|------|------|----------|
| `selective`（既定） | 検索語マッチ前後10文を返す。マッチなしなら20文 | ターゲット抽出 |
| `truncated` | 先頭8000文字 | クイックプレビュー |
| `full` | 完全なコンテンツ（最大10MB） | 包括分析 |

#### 設定

```json
{
  "toolsSettings": {
    "web_fetch": {
      "trusted": [".*docs\\.aws\\.amazon\\.com.*", ".*github\\.com.*"],
      "blocked": [".*pastebin\\.com.*"]
    }
  }
}
```

| オプション | 型 | 説明 |
|---------|-----|------|
| `trusted` | array of regex | プロンプトなしで自動許可する URL パターン |
| `blocked` | array of regex | 拒否する URL パターン（`trusted` より優先） |

> **パターン挙動**:
> - 自動的に `^` と `$` でアンカー
> - `blocked` は `trusted` より優先
> - `blocked` の不正規表現は **すべての URL を拒否**（fail-safe）
> - `trusted` の不正規表現はスキップ

#### 制限

- **サイズ**: ページ取得最大 10MB
- **タイムアウト**: リクエストごと 30 秒
- **リダイレクト**: 最大 10 回まで追跡
- **コンテンツタイプ**: text/html ページのみ
- **リトライ**: 失敗時に 3 回自動リトライ

→ 詳細URL権限: [11. URL Permissions](../01_features/11_URLPermissions.md)

---

## 自己参照系（introspect/code）

### `introspect`

**説明**: 公式ドキュメントを使い、Kiro CLI の機能・コマンド・機能性についての質問に答える自己認識ツール。

Kiro CLI 自身についての質問時に **自動的に有効化** されます。

#### 動作モード

**既定（セマンティック検索）**:
1. 埋め込みモデルをダウンロード
2. セマンティック検索で関連ドキュメントを発見
3. マッチしたドキュメントを直接返す

**Progressive モード**（エンタープライズ環境向け、モデルダウンロード不可な場合）:

```bash
kiro-cli settings introspect.progressiveMode true
```

→ モデルダウンロードをスキップし、ドキュメントインデックスを返す。LLM が必要に応じて取得。

> Progressive モードは複数回の introspect 呼出が必要な場合があり、セマンティック検索より遅くなる可能性があります。

#### Tangent モード自動入り

introspect 質問時に [tangent mode](https://kiro.dev/docs/cli/experimental/tangent-mode/) に自動的に入る：

```bash
kiro-cli settings introspect.tangentMode true
```

→ ヘルプ会話を本作業から分離。tangent mode は実験的機能（`kiro-cli settings chat.enableTangentMode true` で有効化）

> **💡質問のコツ**: 「How does Kiro CLI handle files?」のように **明示的に「Kiro CLI」と書く** とより正確な応答が得られます（「How do you handle files?」は曖昧）。

→ 詳細: [14. Help Agent](../01_features/14_HelpAgent.md)、[20. Guide Agent](../01_features/20_GuideAgent.md)

### `code`

**説明**: シンボル検索、LSP 統合、パターンベースのコード検索・書換を含むコードインテリジェンス機能。設定オプションなし。

#### 権限

- ワークスペース **内** のシンボル検索・コード編集はプロンプトなしで実行
- ワークスペース **外** をターゲットとする操作は **承認が必要**（認証情報、システム設定、他プロジェクトの誤読・誤書防止）

→ 詳細: [01. LSP](../01_features/01_LSP.md)、[09. AST Pattern Tools](../01_features/09_ASTPatternTools.md)

---

## 拡張系（tool_search/delegate/subagent）

### `tool_search`

**説明**: 全ツール定義をリクエストごとに送る代わりに、必要時に MCP ツールを動的に発見・ロード。

ユーザー権限プロンプトなしで自動許可（読取専用操作）。

#### パラメータ

| パラメータ | 型 | 必須 | 説明 |
|---------|-----|-----|------|
| `tool_id` | string | `tool_id` または `query` のどちらか必須 | `server_name::tool_name` 形式の正確な識別子 |
| `query` | string | 同上 | マッチするツール検索用のキーワード |
| `max_results` | integer | No | 返却最大件数（既定: 5） |

`tool_id` または `query` のどちらか **片方のみ** を指定。

→ 詳細: [19. Tool Search](../01_features/19_ToolSearch.md)

### `delegate`

**説明**: 非同期に動作するバックグラウンドエージェントにタスクを委任。即時結果が不要な長時間タスクに有用。設定オプションなし。

> **⚠️ 公式 Deprecation Notice**: 将来のリリースで [subagents](https://kiro.dev/docs/cli/chat/subagents/) ツールに置換予定。新規ワークフローでは subagents の使用を推奨。
>
> → 移行先: [02. Subagents](../01_features/02_Subagents.md)（本サイト）

### `subagent`

**Aliases**: `use_subagent`  
**説明**: 並列実行・分離コンテキストを持つ専門化された subagent に複雑なタスクを委任。

> **カスタムエージェント設定**: デフォルトエージェントには含まれます。カスタムエージェントでは `tools` 配列に明示的に `subagent` を追加するか、`@builtin` で含める必要があります。

#### 機能

- 同時に最大 **4 個** の subagent を起動可能
- 各 subagent は独立したコンテキストで動作（メイン会話の肥大化防止）
- 全実行中 subagent の状態をリアルタイム可視化
- subagent ごとに異なるエージェント設定をサポート
- 自動実行サマリ（ツール使用と所要時間メトリクス）

#### 設定

```json
{
  "toolsSettings": {
    "subagent": {
      "availableAgents": ["reviewer", "tester", "analyzer", "docs-*"],
      "trustedAgents": ["reviewer", "tester"]
    }
  }
}
```

| 設定 | 型 | 説明 |
|-----|-----|------|
| `availableAgents` | `string[]` | subagent として起動できるエージェントを制限（グロブ可: `docs-*`） |
| `trustedAgents` | `string[]` | 権限プロンプトなしで実行できるエージェント（グロブ可） |

→ 詳細: [02. Subagents](../01_features/02_Subagents.md)

---

## 補助系（report/knowledge/thinking/todo/session）

### `report`

**説明**: チャット問題、バグ、機能リクエストを報告するため、事前入力済みの GitHub issue テンプレートをブラウザで開く。設定オプションなし。

> 既定で trusted（権限プロンプトなし）。

### `knowledge`（実験的機能）

**説明**: チャットセッション間で情報をナレッジベースに保存・取得。ファイル、ディレクトリ、テキストコンテンツのセマンティック検索機能を提供。設定オプションなし。

**有効化**:
```bash
kiro-cli settings chat.enableKnowledge true
```

**インデックス種別**:
- **Fast**（BM25 lexical。キーワード関連度で順位付けする字句検索）: 高速、キーワード一致
- **Best**（semantic, `all-minilm-l6-v2`。埋め込みモデルによる意味検索）: 自然言語、関連概念検索

**保存先（OS別）**:
| OS | パス |
|----|------|
| macOS | `~/Library/Application Support/kiro-cli/knowledge_bases/` |
| Linux | `~/.local/share/kiro-cli/knowledge_bases/` |
| Windows | `%LOCALAPPDATA%\kiro-cli\knowledge_bases\` |

エージェント別に **独立した** ナレッジベース（クロスエージェント不可）。

→ 公式: https://kiro.dev/docs/cli/experimental/knowledge-management/

### `thinking`（実験的機能）

**説明**: 複雑なタスクをアトミックなアクションに分解することで品質を向上させる内部推論メカニズム。設定オプションなし。

**有効化**: `kiro-cli settings chat.enableThinking true`

### `todo`（実験的機能）

**説明**: マルチステップタスクを追跡する ToDo リストの作成・管理。設定オプションなし。

**有効化**: `kiro-cli settings chat.enableTodoList true`

### `session`（Session settings tool）

**説明**: 設定ファイルを変更せずに、現在のセッションの CLI 設定を一時的に上書き。すべてのセッション上書きはメモリに保存され、セッション終了時にリセット。

会話で操作可能：
- 「Disable markdown rendering for this session」
- 「Switch to compact UI mode」
- 「Turn on the thinking tool」

#### 操作

| 操作 | 説明 |
|------|------|
| `list` | 既定値以外のすべての設定を表示 |
| `get` | 特定設定の現在値を読取 |
| `set` | 現在のセッションで設定を上書き |
| `reset` | 個別設定または全セッション上書きをリセット |

セッションセーフとマークされた設定のみ変更可能。`set` と `reset` は常に **ユーザー確認が必要**。

設定オプションなし。

---

## Side channels（v2.3.0+）

**出典**: [Side channels for wrapper scripts](https://kiro.dev/docs/cli/reference/built-in-tools/#side-channels-for-wrapper-scripts)

shell ツール経由でコマンド実行時、Kiro CLI は **2つの環境変数** をエクスポートします（v2.3.0 で追加）：

| 変数 | ツール結果に含まれる？ | TUI にストリーム？ | 用途 |
|------|------------------|------------|------|
| `AGENT_DISPLAY_OUT` | No | Yes | エージェントコンテキストを膨張させない、ユーザー向け出力（冗長なビルドログ等） |
| `AGENT_CONTEXT_OUT` | Yes（`agent_notes` として） | Yes | エージェントが必要だが stdout で確実に届かない情報（grep/tail パイプ時等） |

`$AGENT_CONTEXT_OUT` への書き込みはツール結果の `agent_notes` フィールドに表示され、エージェントは stdout/stderr と並行して読み取れます。`$AGENT_DISPLAY_OUT` への書き込みは TUI のみに到達。

**ラッパースクリプト例**:

```bash
#!/usr/bin/env bash
# 冗長ビルドを実行し、ユーザーにログを表示、エージェントには場所を伝達
./gradlew build 2>&1 | tee "$AGENT_DISPLAY_OUT"
echo "Build finished. Full log at ./build/reports/build.log" > "$AGENT_CONTEXT_OUT"
echo "ok"  # 通常の stdout — 通常通り捕捉される
```

両変数はエージェントがコマンド駆動時のみ設定。ラッパースクリプトは空時に正常フォールバックすべき（`[ -n "${AGENT_CONTEXT_OUT:-}" ]` でテスト）。

---

## agent.json での設定方法

ツール設定は agent 設定ファイルの `toolsSettings` セクションに記述。各ツールはツール名をキーとして指定。

MCP サーバーツールは `@server_name/tool_name` 形式：

```json
{
  "toolsSettings": {
    "write": {
      "allowedPaths": ["~/projects"]
    },
    "@git/git_status": {
      "git_user": "$GIT_USER"
    }
  }
}
```

→ 完全な書式: [Agent Configuration Reference](https://kiro.dev/docs/cli/custom-agents/configuration-reference/)

---

## ツール権限

ツールは agent 設定の `allowedTools` セクションで明示的に許可可能：

```json
{
  "allowedTools": [
    "read",
    "knowledge",
    "@git/git_status"
  ]
}
```

`allowedTools` 一覧にないツールは、`toolSettings` に許可設定がない限り、使用時にユーザーに権限を確認します。

### 既定の権限挙動

| ツール | 既定動作 |
|------|---------|
| `report` | 既定で trusted |
| `read`, `grep`, `glob` | 現在のワーキングディレクトリで trusted |
| `shell`, `write`, `aws` | 既定で権限プロンプト（特定コマンド/パス/サービスの設定可能） |

→ 詳細権限制御: [17. Granular Tool Trust](../01_features/17_GranularToolTrust.md)

---

## Q CLI 時代との世代差分

Amazon Q Developer CLI 時代は **9個** のビルトインツールでした。Kiro CLI で **18個** に拡張。

### Q CLI 9ツール（参考）

`fs_read`、`fs_write`、`execute_bash`、`use_aws`、`report_issue`、`thinking`、`gh_issue`、`introspect`、`knowledge`

→ 出典: `kiro-docs/06_embedded-docs/kiro-cli/docs/built-in-tools.md`（Q CLI 時代のアーカイブ、197行。ローカル管理・GitHub 非公開）

### Kiro CLI 18ツール（本ファイル対象）

| 分類 | ツール |
|-----|------|
| ファイル系 | `read`, `glob`, `grep`, `write` |
| 実行系 | `shell`, `aws` |
| Web 系 | `web_search`, `web_fetch` |
| 自己参照系 | `introspect`, `code` |
| 拡張系 | `tool_search`, `delegate`, `subagent` |
| 補助系 | `report`, `knowledge`, `thinking`, `todo`, `session` |

### 新規追加（Kiro CLI 期）

`glob`（v1.20.0+）、`grep`（v1.20.0+）、`web_search`、`web_fetch`、`code`（v1.24.0+）、`tool_search`（v2.1.0+）、`delegate`（実験的）、`subagent`（v1.25.0+）、`session`（v1.27.0+）

### Deprecated/置換

- `gh_issue`（Q CLI）→ `report`（Kiro CLI）
- `delegate`（実験的）→ `subagent` への移行が推奨

---

## 関連リンク

### リファレンス（本ディレクトリ）

- [01. Settings](01_settings.md)
- [02. Slash Commands](02_slash-commands.md)
- [03. CLI Commands](03_cli-commands.md)

### 機能文書

- [01. LSP](../01_features/01_LSP.md) — `code` ツール（Code Intelligence）
- [02. Subagents](../01_features/02_Subagents.md) — `subagent` ツール、`delegate` の代替
- [05. GrepGlob](../01_features/05_GrepGlob.md) — `glob`、`grep` ツール
- [08. Custom Diff Tools](../01_features/08_CustomDiffTools.md) — `write` ツール用 Custom diff
- [09. AST Pattern Tools](../01_features/09_ASTPatternTools.md) — `code` ツール（AST）
- [11. URL Permissions](../01_features/11_URLPermissions.md) — `web_fetch` の URL 権限
- [14. Help Agent](../01_features/14_HelpAgent.md) — `introspect` 関連
- [17. Granular Tool Trust](../01_features/17_GranularToolTrust.md) — ツール権限の段階制御
- [19. Tool Search](../01_features/19_ToolSearch.md) — `tool_search` ツール
- [20. Guide Agent](../01_features/20_GuideAgent.md) — `introspect` 関連
- [22. Hooks](../01_features/22_Hooks.md) — `matcher` で本ツール群を指定
- [23. Agent Steering](../01_features/23_Steering.md) — `read` ツールでの Steering ファイル参照、`introspect` の関係
- [24. @file references](../01_features/24_FileReferences.md) — `read`/`glob`/`grep` 各ツールと `@file`/`@directory` 構文の使い分け
- [25. Auto Complete](../01_features/25_AutoComplete.md) — シェルコマンド実行時の Side Channels（`AGENT_DISPLAY_OUT`/`AGENT_CONTEXT_OUT`）と AI 補完の関係
- [26. Agent Toolkit for AWS](../01_features/26_AgentToolkitForAWS.md) 🌟 — ビルトイン `aws` ツール（ローカル AWS CLI）と AWS MCP Server の `call_aws` ツールの使い分け

### Q CLI 時代との比較（歴史的参考）

- `kiro-docs/06_embedded-docs/kiro-cli/docs/built-in-tools.md` — Q CLI 時代の 9 ツール記述（アーカイブ。ローカル管理・GitHub 非公開）

### 公式情報源

- [Built-in tools - Kiro CLI Documentation](https://kiro.dev/docs/cli/reference/built-in-tools/)（公式ページ最終更新: 2026-05-12）
- [Custom Agents Configuration Reference](https://kiro.dev/docs/cli/custom-agents/configuration-reference/)
- [Tangent Mode](https://kiro.dev/docs/cli/experimental/tangent-mode/) — `introspect.tangentMode`
- [Knowledge Management](https://kiro.dev/docs/cli/experimental/knowledge-management/) — `knowledge` ツール
- [Delegate (Deprecated)](https://kiro.dev/docs/cli/experimental/delegate/) — `delegate` ツール
- [Subagents](https://kiro.dev/docs/cli/chat/subagents/) — `subagent` ツールへの移行先

---

**Page updated**: 2026-07-04（`settings` サブコマンドの表記を実機準拠（`settings KEY VALUE`）に修正、06_embedded-docs 参照をローカル管理注記付きテキスト参照へ変更。本サイト初版 2026-05-24）  
**公式ページ最終更新**: 2026-05-12
