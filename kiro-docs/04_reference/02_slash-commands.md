[ホーム](../../README.md) > [リファレンス](README.md) > Slash Commands

# Kiro CLI Slash Commands リファレンス

**出典**: [Slash commands - Kiro CLI Documentation](https://kiro.dev/docs/cli/reference/slash-commands/)（公式ページ最終更新: 2026-06-12）

Kiro CLI のインタラクティブチャットセッション内で使用できるすべてのスラッシュコマンドを網羅する辞書的リファレンスです。

---

## 📋 目次

- [概要](#概要)
- [スラッシュコマンド一覧](#スラッシュコマンド一覧)
- [Skill ベースのスラッシュコマンド](#skill-ベースのスラッシュコマンド)
- [キーボードショートカット](#キーボードショートカット)
- [関連リンク](#関連リンク)

---

## 概要

**出典**: [Slash commands - Overview](https://kiro.dev/docs/cli/reference/slash-commands/#overview)

スラッシュコマンドは、インタラクティブチャットセッション内で会話を中断せずにアクションを実行する特殊コマンドです。**フォワードスラッシュ（`/`）で始まり**、よくあるタスクのショートカットを提供します。

### 使用方法

スラッシュコマンドは **インタラクティブチャットモードのみ** で利用可能です：

```bash
kiro chat
> /help
```

---

## スラッシュコマンド一覧

公式ページに記載されている全コマンド（公式更新日: 2026-06-12 時点）。**本ページには全 40 コマンドを掲載**しています（`/help`〜`/stats` の見出し数。`/save` / `/load` は 1 見出しに集約）。

### `/help`

Help Agent に切り替えて Kiro CLI 機能について質問、または classic ヘルプテキストを表示。

```bash
> /help                          # Help Agent に切替
> /help How do I configure MCP?  # 直接質問
> /help --legacy                 # classic ヘルプテキスト
> /help --legacy /context        # 特定コマンドのヘルプ
```

→ 詳細: [14. HelpAgent](../01_features/14_HelpAgent.md)

### `/quit`

インタラクティブチャットセッションを終了。

```bash
> /quit
```

エイリアス: `/exit`、`/q`

### `/clear`

現在の会話履歴をクリア（表示のみ。保存済み会話には影響しない）。

```bash
> /clear
```

### `/context`

コンテキストファイルを管理し、コンテキストウィンドウ使用率を確認。

```bash
> /context show                       # コンテキストルール設定とマッチファイル表示
> /context add src/app.js             # コンテキストルール追加（ファイル）
> /context add "*.py"                 # グロブパターンで追加
> /context add "src/**/*.js"          # 再帰的グロブで追加
> /context remove src/app.js          # 指定ルール削除
> /context clear                      # 全ルール削除
```

**サブコマンド**: `show` / `add` / `remove`

> **注意**: コンテキスト変更はチャットセッション間で **保持されない**。永続化するにはエージェント設定ファイルを編集する必要があります。

### `/model`

セッションの AI モデルを選択。

```bash
> /model                               # 対話的ピッカー
> /model claude-opus-4.6              # 直接指定
> /model clau<Tab>                    # Tab 補完
> /model set-current-as-default       # 現在のモデルをデフォルト保存（v2.6.0で不要に）
```

> **自動永続化（v2.6.0+）**: `/model` の選択は自動的に保存され、将来のセッションに引き継がれます。`/model set-current-as-default` を手動実行する必要はなくなりました（[永続化の詳細](https://kiro.dev/docs/cli/chat/settings/#persistence)）。

**特徴**:
- Tab 補完（API から取得した利用可能モデル）
- ゴーストテキストヒント（マッチするモデル名を表示）
- ファジーマッチング
- 大文字小文字を区別しないマッチング

### `/agent`

エージェントの管理と切替。

```bash
> /agent list                         # 全エージェント一覧
> /agent create my-agent              # AI 支援で新規作成
> /agent create my-agent -D "説明"    # 説明と MCP サーバー指定
> /agent create my-agent --manual     # エディタモードで作成
> /agent edit                         # 現在のエージェント編集
> /agent edit my-agent                # 名前指定で編集
> /agent schema                       # エージェント設定スキーマ表示
> /agent set-default my-agent         # デフォルトエージェント設定
> /agent swap code-reviewer           # 実行時にエージェント切替
```

**サブコマンド**: `list` / `create` / `edit` / `generate`（create のエイリアス） / `schema` / `set-default` / `swap`

> **エージェント保存場所**:
> - グローバル: `~/.kiro/agents/`
> - ワークスペース: `.kiro/agents/`
>
> **編集中の安全性**: 一時ファイルで編集 → 検証 → 失敗時に再編集を促す。元のファイルは失敗時に上書きされない。

### `/spawn`

> **V2 TUI で追加**: このコマンドは V2 TUI モード（v2.0.0+ デフォルト）で追加されました。macOS・Windows（PowerShell）・Linux で動作します。Legacy UI（`--legacy-ui`）では利用できません。

メインの会話と並行してタスクを実行する新しいエージェントセッションを起動。

```bash
> /spawn Analyze the test coverage in src/utils
> /spawn --name test-analysis Review all failing tests
```

**特徴**:
- メイン会話をブロックせずに並列実行
- `Ctrl+G` でクルーモニターを開いて状態を監視
- タスク説明は **必須**

→ Subagents との違い: subagents はタスクグラフ内で agent が委任、`/spawn` はユーザー駆動で長時間セッションを起動

詳細: [02. Subagents](../01_features/02_Subagents.md)

### `/chat`

チャットセッションの管理（保存/読込/切替）。Kiro CLI は会話の各ターンで自動保存。

```bash
> /chat new                          # 新規会話開始
> /chat new how do I set up React    # 初期プロンプト付き
> /chat resume                       # セッションピッカーで再開
> /chat save /path/to/session.json   # 現在のセッションを保存
> /chat load /path/to/session.json   # セッション読込
> /chat save-via-script ./save.sh    # カスタムスクリプト保存
> /chat load-via-script ./load.sh    # カスタムスクリプト読込
```

**カスタムセッションストレージ**: バージョン管理、クラウド、データベース等、任意の場所に保存可能。

詳細: [04. MultiSession](../01_features/04_MultiSession.md)

### `/session-id`

> **V2 TUI で追加**: このコマンドは V2 TUI モード（v2.0.0+ デフォルト）で追加されました。macOS・Windows（PowerShell）・Linux で動作します。Legacy UI（`--legacy-ui`）では利用できません。

現在のチャットセッション ID を表示。

```bash
> /session-id
```

→ `kiro-cli chat --resume-id <ID>` で正確に再開可能。

### `/save` / `/load`

> **⚠️ deprecated（v2.4.1）**: 実機では `⚠ The /save command is deprecated. Use /chat save instead.` / `⚠ The /load command is deprecated. Use /chat load instead.` と警告が表示されます。`/chat save` / `/chat load` を使用してください。

### `/editor`

デフォルトエディタを開いて長文プロンプトを作成。

```bash
> /editor
```

`$EDITOR`（既定: vi）を起動。マルチラインメッセージ作成に有用。

### `/reply`

直前のアシスタント応答を引用してエディタで返信を作成。

```bash
> /reply
```

### `/checkpoint`

ワークスペースのチェックポイント管理（ファイル変更追跡と復元）。

```bash
> /checkpoint init                    # 新規チェックポイント作成
> /checkpoint list                    # 一覧
> /checkpoint restore                 # 対話的ピッカーで復元
> /checkpoint restore 2               # 特定チェックポイント復元
> /checkpoint restore 2 --hard        # 完全一致モード（新ファイルも削除）
> /checkpoint expand 1                # 詳細表示
> /checkpoint diff 1 2                # チェックポイント間差分
> /checkpoint clean                   # データクリーンアップ
```

**仕組み**:
- シャドウ bare git リポジトリでファイル変更を追跡
- 会話ターンごとにチェックポイント作成
- ツール使用ごとにサブチェックポイント
- 復元時に会話履歴も巻き戻し
- git リポジトリでは自動有効（エフェメラルモード）

> **実験的機能**: `kiro-cli settings chat.enableCheckpoint true` で有効化

### `/plan`

複雑なアイデアを実装計画に分解する Plan Agent に切替。

```bash
> /plan
> /plan Build a REST API for user management
```

`Shift+Tab` で前のエージェントに戻る。

詳細: [03. PlanAgent](../01_features/03_PlanAgent.md)

### `/guide`

> **V2 TUI で追加**: このコマンドは V2 TUI モード（v2.0.0+ デフォルト）で追加されました。macOS・Windows（PowerShell）・Linux で動作します。Legacy UI（`--legacy-ui`）では利用できません。

ドキュメントベースのヘルプとオンボーディング向け Guide Agent に切替。

```bash
> /guide
```

> **注**: `/guide` は **TUI のみ**。classic では `/help` を使用。

詳細: [20. GuideAgent](../01_features/20_GuideAgent.md)

### `/knowledge`

ナレッジベース管理（ファイル/ディレクトリへのセマンティック検索）。

```bash
> /knowledge show
> /knowledge add --name my-docs --path ./docs
> /knowledge add --name src --path ./src --include "*.ts" --exclude "*.test.ts"
> /knowledge add --name api --path ./api --index-type Best
> /knowledge search "authentication flow"
> /knowledge remove ./docs
> /knowledge update ./docs            # 単一エントリを再インデックス
> /knowledge update                   # 全ナレッジベースを一括再インデックス（v2.6.0+）
> /knowledge clear
> /knowledge cancel
```

**サブコマンド**: `show` / `add` / `search` / `remove`（`rm` 別名） / `update` / `clear` / `cancel` / `fix`

**add オプション**: `--name, -n`（必須）/ `--path, -p`（必須） / `--include` / `--exclude` / `--index-type`（Fast/Best）

> **v2.6.0+**: `update` を引数なしで実行すると、全ナレッジベースを一括で再インデックスします。

> **実機追加確認（v2.4.1）**: `fix` サブコマンド — エージェントファイルパス変更後のナレッジベースディレクトリ名を修正

> **実験的機能**: `kiro-cli settings chat.enableKnowledge true` で有効化

### `/compact`

会話を要約してコンテキスト空間を解放。

```bash
> /compact
```

→ 詳細: [10. Conversation Compaction](../01_features/10_ConversationCompaction.md)

### `/paste`

クリップボードから画像を会話に貼り付け（PNG/JPEG 等）。

```bash
> /paste
```

### `/tools`

ツールと権限を表示・管理。

```bash
> /tools                              # 全ツール、トークン数、権限
> /tools schema                       # 入力スキーマ
> /tools trust write                  # セッション中信頼
> /tools untrust write                # リクエストごと確認に戻す
> /tools trust-all                    # 全ツール信頼
> /tools reset                        # 全権限デフォルトリセット
```

**出力カラム**:
- `~Tokens` — 各ツールスキーマの推定トークン数（1000+ は `k`）
- `Permission` — 現在の権限状態（Trusted / Ask / Allowed）
- `Total` — オリジン別トークン合計

詳細: [17. Granular Tool Trust](../01_features/17_GranularToolTrust.md)

### `/prompts`

プロンプトの表示・取得（再利用可能なテンプレート）。

```bash
> /prompts list                       # 全プロンプト一覧
> /prompts details code-review        # 詳細情報
> /prompts get code-review [arg]      # 取得
> @code-review [arg]                  # 短縮形（@ プレフィックス）
> /prompts create my-prompt           # 新規作成
> /prompts edit my-prompt             # 編集
> /prompts remove my-prompt           # 削除
```

**サブコマンド**: `list` / `details` / `get` / `create` / `edit` / `remove`

詳細: [24. File References](../01_features/24_FileReferences.md)（解決順序を参照）

### `/hooks`

コンテキストフックを表示。

```bash
> /hooks
```

→ 詳細: [22. Hooks](../01_features/22_Hooks.md)（v1.29.6+ で追加）

### `/usage`

請求とクレジット情報を表示。

```bash
> /usage
```

→ 詳細: [06. Usage Command](../01_features/06_UsageCommand.md)

### `/mcp`

MCP サーバーとレジストリ状態を表示・管理。

```bash
> /mcp                                # デフォルト: サーバー一覧表示
> /mcp list                           # 全 MCP サーバー一覧
> /mcp add                            # レジストリからサーバー追加（管理者設定時のみ）
> /mcp remove                         # 有効なサーバーを削除（管理者設定時のみ）
```

**サブコマンド**（実機検証済み）:
- `list` — 全 MCP サーバー一覧（レジストリ設定時はレジストリサーバー、それ以外はローカル設定サーバー）
- `add` — レジストリからサーバー追加（管理者がレジストリ設定済みの場合のみ利用可能）
- `remove` — 有効なサーバーを削除（管理者がレジストリ設定済みの場合のみ利用可能）

> **MCP ガバナンス**: 組織管理者が無効化している場合、メッセージが表示される（IAM Identity Center および API key ユーザーに適用）。

### `/theme`

> **V2 TUI で追加**: このコマンドは V2 TUI モード（v2.0.0+ デフォルト）で追加されました。macOS・Windows（PowerShell）・Linux で動作します。Legacy UI（`--legacy-ui`）では利用できません。

プロンプトと応答テキストのテーマカラーを上書き。

```bash
> /theme
```

### `/copy`

> **V2 TUI で追加**: このコマンドは V2 TUI モード（v2.0.0+ デフォルト）で追加されました。macOS・Windows（PowerShell）・Linux で動作します。Legacy UI（`--legacy-ui`）では利用できません。

直前のアシスタント応答をクリップボードにコピー。

```bash
> /copy
```

OSC 52 エスケープシーケンス経由で SSH/tmux/Zellij でも動作。100KB 超は無視。

### `/title`

> **追加バージョン**: v2.6.0。ターミナルタイトル機能が有効な場合に利用可能。

ターミナルウィンドウタイトルを設定・クリア・表示（v2.6.0+）。タイトルは `kiro: <text>` の形式で表示される。

```bash
> /title                              # 現在のタイトルを表示
> /title weekly standup notes         # カスタムタイトルを設定（sticky）
> /title --clear                      # カスタムタイトルをクリア
```

**特徴**:
- タイトルはセッショントピックまたはワークスペースパスから自動導出
- 手動設定したタイトルは sticky（`--clear` まで保持）
- 60 文字で truncate。OSC 0 エスケープシーケンスを使用（無視する端末あり）。tmux は `set-titles on` が必要
- **有効化**: `/settings display` → Terminal title（無効時は `/title` が有効化方法を案内）

> **注**: ターミナルタイトルは `/settings display` でトグルする機能で、CLI 設定（`kiro-cli settings`）としては提供されない（公式設定リファレンス準拠）。

### `/transcript`

> **V2 TUI で追加**: このコマンドは V2 TUI モード（v2.0.0+ デフォルト）で追加されました。macOS・Windows（PowerShell）・Linux で動作します。Legacy UI（`--legacy-ui`）では利用できません。

会話のトランスクリプトをページャで開く、またはファイルへエクスポート（`save` は v2.6.0+）。

```bash
> /transcript                         # ページャで開く
> /transcript --plain                 # プレーンテキストでレンダリング
> /transcript --json                  # JSON でレンダリング
> /transcript save conversation.md    # ファイルへエクスポート（既定: Markdown）
> /transcript save conversation.txt --plain   # プレーンテキストでエクスポート
> /transcript save conversation.json --json   # JSON でエクスポート
```

`$PAGER`（既定: `less`、Windows: `notepad`）で開く。`q` で終了。`Ctrl+T` でも起動可能。v2.6.0以降はページャを最下部で開き、最新メッセージを先頭表示。

**サブコマンド**:
- `save` — 会話を Markdown（既定）/ プレーンテキスト / JSON でファイルにエクスポート（v2.6.0+）

**フォーマットフラグ**: `--plain`（プレーンテキスト）/ `--json`（JSON）。形式はファイル拡張子ではなくフラグで決定。

→ 詳細: [28. v26NewCommands](../01_features/28_v26NewCommands.md)

### `/code`

コードインテリジェンスの設定とフィードバック管理。

```bash
> /code init                          # LSP 初期化
> /code init -f                       # 強制再初期化
> /code overview                      # ワークスペース全体把握
> /code overview --silent             # 簡潔出力
> /code status                        # ワークスペース・LSP 状態
> /code logs                          # 直近20件のERRORログ
> /code logs -l INFO                  # INFO レベル以上
> /code logs -n 50                    # 直近50件
> /code logs -p ./lsp-logs.json       # JSON ファイルに出力
```

**サブコマンド**: `init` / `overview` / `status` / `logs` / `summary`

> **実機追加確認（v2.4.1）**: `summary` — エージェント分析による包括的なコードベースドキュメント生成

詳細: [01. LSP](../01_features/01_LSP.md)

### `/experiment`

実験的機能の有効/無効を切替。

```bash
> /experiment
```

### `/tangent`

会話チェックポイントを作成して脇道のトピックを探求。

```bash
> /tangent                            # tangent モード切替（入る/出る）
> /tangent tail                       # tangent を抜けつつ最後の会話エントリを保持
> /tangent forget                     # 直近 N 件の会話エントリを履歴から削除
```

`Ctrl+T` でも切替可能（有効化時）。

**サブコマンド**（実機検証済み）:
- `tail` — tangent モードを終了し、最後の会話エントリ（質問 + 応答）を保持
- `forget` — 直近 N 件の会話エントリを履歴から削除

### `/todos`

> **出典**: 実機 kiro-cli 2.4.1（2026-05-24 検証）

To-do リストの表示・管理・再開。

```bash
> /todos clear-finished               # 完了済みリストを削除
> /todos resume                       # 選択したリストを再開
> /todos view                         # リストを表示
> /todos delete                       # リストを削除
```

**サブコマンド**（実機検証済み）:
- `clear-finished` — 完了済み to-do リストを削除
- `resume` — 選択した to-do リストを再開
- `view` — to-do リストを表示
- `delete` — to-do リストを削除

> **注**: to-do リストへの項目追加（`add`）や完了マーク（`complete`）は、スラッシュコマンドではなく **AI ツール（`todo_list`）** 経由で行われます。エージェントがタスク管理時に自動的に使用します。

### `/issue`

新しい GitHub issue または機能リクエストを作成。

```bash
> /issue
```

### `/logdump`

ログを zip にしてサポート調査用に作成。

```bash
> /logdump                            # チャットログのみ
> /logdump --mcp                      # MCP サーバーログ含む
```

**出力**: `q-logs-YYYY-MM-DDTHH-MM-SSZ.zip` を現在のディレクトリに作成。

### `/settings`

> **V2 TUI で追加**: このコマンドは v2.4.0 で追加されました。TUI モード（デフォルト）で利用可能です。Legacy UI（`--legacy-ui`）では利用できません。

テーマ、キーバインド、ターミナル入力、表示設定をインタラクティブに変更（v2.4.0+）。

```bash
> /settings                           # メインメニュー
> /settings theme                     # テーマ色
> /settings keybindings               # キーボードショートカット
> /settings terminal                  # マルチライン入力
> /settings display                   # 表示オプション
> /settings history                   # プロンプト履歴のスコープ（v2.5.0+）
```

**サブコマンド**:
- `theme` — プロンプトと応答色を live preview でカスタマイズ
- `keybindings` — 設定可能なキーボードショートカットを表示（読み取り専用）
- `terminal` — `Shift+Enter`/`Option+Enter` のマルチライン入力（VS Code、Alacritty、Zed、Apple Terminal 等を自動設定）
- `display` — アニメーション、ASCII アート、アイコン表示、**Show thinking（推論のリアルタイム表示、v2.5.0+）**、Terminal title（端末タイトル、v2.6.0+）を切替
- `history` — プロンプト履歴のスコープを `session`（既定）/ `global` で切替（v2.5.0+、設定キー `chat.historyMode`）

> `terminal` サブコマンドはターミナル設定ファイル変更前に `.bak` を作成。
> アニメーション/ASCII/アイコンは即時反映。Show thinking と history は次回セッションから反映。

> **v2.7.0 での進化**:
> - 全サブコマンド（theme/keybindings/terminal/display/history）で**統一された overlay frame、footer hints、ESC で戻るナビゲーション**を採用
> - `theme Custom` が**ステップ式ウィザード**化。ライブプレビューが実会話レンダリングに整合
> - `terminal` → `interrupt behaviour` で Queue Steering の起動時既定モード（`steer`/`queue`）を変更可能

→ 詳細: [21. v24NewCommands](../01_features/21_v24NewCommands.md)、[27. Thinking Display](../01_features/27_ThinkingDisplay.md)、[29. v27NewCommands](../01_features/29_v27NewCommands.md)

### `/effort`

> **V2 TUI で追加**: このコマンドは v2.4.0 で追加されました。TUI モード（デフォルト）で利用可能です。Legacy UI（`--legacy-ui`）では利用できません。

セッションのモデル推論エフォートレベルを設定（v2.4.0+）。

```bash
> /effort                             # 対話的ピッカー
> /effort high                        # 高
> /effort max                         # 最大
```

**レベル**: `low` / `medium` / `high` / `xhigh` / `max`

利用可能レベルはアクティブモデルに依存。高いレベルほどトークン消費は増えますが、複雑なタスクへの応答は徹底的になります。

> **起動時指定（v2.6.0+）**: `kiro-cli chat --effort <level>` でセッション起動時に初期 effort レベルを指定できます。
>
> **自動永続化（v2.6.0+）**: `/effort` の選択は自動的に保存され、将来のセッションに引き継がれます（`set-current-as-default` 相当の手動操作は不要）。

**永続的なデフォルト設定**:
```json
{
  "chat": {
    "modelDefaults": {
      "claude-sonnet-4": { "effort": "high" },
      "claude-opus-4": { "effort": "max" }
    }
  }
}
```

**優先順位**: ロード済みセッション effort > cli.json のユーザーデフォルト > ビルトインデフォルト

→ 詳細: [21. v24NewCommands](../01_features/21_v24NewCommands.md)

### `/rewind`

> **V2 TUI で追加**: このコマンドは v2.4.0 で追加されました。TUI モード（デフォルト）で利用可能です。Legacy UI（`--legacy-ui`）では利用できません。

会話を過去のターンで分岐し別のパスを探求（v2.4.0+）。

```bash
> /rewind                             # 対話的ターンピッカー
> /rewind 4                           # インデックス指定
```

**特徴**:
- 元のセッションは保持される（破壊的書換ではない）
- `/chat load` または `/chat resume` で元に戻れる
- 各ターンのプロンプトプレビューとコンテキスト使用率を表示
- **v2.7.0**: ターンピッカーが各ターンの**ツール呼び出し詳細**、**ファイル変更**、**実行コマンド**、**コンテキスト使用量**を併記表示し、分岐ポイントを特定しやすく（Enriched preview）

→ 詳細: [21. v24NewCommands](../01_features/21_v24NewCommands.md)、[29. v27NewCommands](../01_features/29_v27NewCommands.md)

### `/goal`

> **V2 TUI で追加**: このコマンドは v2.7.0 で追加されました。TUI モード（デフォルト）で利用可能です。

受入基準を満たすまで自己検証を繰り返す goal 駆動の自律ループを起動（v2.7.0+）。

```bash
> /goal refactor the auth module to use JWT tokens and ensure all tests pass
> /goal --max 10 migrate the entire test suite from Jest to Vitest
> /goal clear                         # アクティブな goal をキャンセル
```

**動作**:
- Plans → Implements → Verifies → 失敗時 corrections → 完了 のサイクル
- 既定で**最大5反復**（`--max <number>` で上限変更）
- 受入基準は goal 文から推論されるため、「all tests pass」「no TypeScript errors」など**完了条件を明示**するのが効果的

**サブコマンド**:
- `clear` — アクティブな goal ループをキャンセル（ファイル変更は VCS で巻き戻し）

**オプション**:
- `--max <number>` — 最大反復数（既定: 5）

**ループ中の方向修正**:
- **Queue Steering（Ctrl+S）** で goal をキャンセルせずに mid-loop で指示を追加可能

→ 詳細: [29. v27NewCommands](../01_features/29_v27NewCommands.md)、[公式 /goal](https://kiro.dev/docs/cli/chat/goal/)

### `/changelog`

最近のリリースノートを CLI 内でインライン表示。

```bash
> /changelog
```

### `/feedback`

> **V2 TUI で追加**: このコマンドは V2 TUI モード（v2.0.0+ デフォルト）で追加されました。macOS・Windows（PowerShell）・Linux で動作します。Legacy UI（`--legacy-ui`）では利用できません。

> **出典**: introspect 組み込みドキュメント（2026-04-08 検証）。公式ページ（kiro.dev/docs/cli/、2026-05-19）には記載なし。

フィードバック送信、機能リクエスト、Issue 報告。

```bash
> /feedback
```

### `/stats`

> **V2 TUI で追加**: このコマンドは V2 TUI モード（v2.0.0+ デフォルト）で追加されました。macOS・Windows（PowerShell）・Linux で動作します。Legacy UI（`--legacy-ui`）では利用できません。

> **出典**: introspect 組み込みドキュメント（2026-05-05 検証）。公式ページ（kiro.dev/docs/cli/、2026-05-19）には記載なし。

リクエスト ID とタイミング情報を表示（デバッグ用）。

```bash
> /stats
```

---

## Skill ベースのスラッシュコマンド

**出典**: [Skill-based slash commands](https://kiro.dev/docs/cli/reference/slash-commands/#skill-based-slash-commands)

`.kiro/skills/` および `~/.kiro/skills/` に定義された Skill は **自動的にスラッシュコマンドとして利用可能** になります。

```bash
# pr-review Skill を起動
> /pr-review

# cdk-deploy Skill を起動
> /cdk-deploy
```

利用可能なコマンドは、配置されている Skill に依存します。

→ 詳細: [07. Skills](../01_features/07_Skills.md)

---

## キーボードショートカット

**出典**: [Keyboard shortcuts](https://kiro.dev/docs/cli/reference/slash-commands/#keyboard-shortcuts)

インタラクティブモードでは以下のキーが使用可能：

| キー | 動作 |
|-----|------|
| `Ctrl+C` | 現在の入力をキャンセル / セッション終了 |
| `Ctrl+D` | セッション終了 |
| `Ctrl+D` / `Ctrl+U` | モニター内の subagents 間ナビゲーション |
| `Ctrl+G` | subagent 実行モニターを開く |
| `Ctrl+J` | 改行挿入（tmux 含む全ターミナル） |
| `Ctrl+O` | 折り畳まれたシェル出力を展開 |
| `Ctrl+R` | リバースインクリメンタル履歴検索 |
| `Ctrl+S` | コマンドとコンテキストファイルのファジー検索（Tab で複数選択） / **Queue Steering の steer/queue モード切替（v2.7.0+）** ※ |
| `Ctrl+T` | tangent モード切替（有効時） |
| `Alt+Enter` | 改行挿入（Terminal.app、Ghostty） |
| `Alt+Backspace` | 直前の単語削除 |
| `Shift+Enter` | 改行挿入（iTerm2、Ghostty、Kitty、Warp、Zed） |
| `Shift+Tab` | プランモードに入る |
| `Up`/`Down` | コマンド履歴ナビゲーション（v2.5.0+ 既定でセッション単位。`/settings history` で global に切替可） |
| `Tab` | 承認オプション展開 / ファイル参照自動補完 |
| `Esc` | パネルを閉じる、エージェント実行キャンセル、プロンプトキューをクリア |

> ※ **Ctrl+S の機能について公式に矛盾あり（2026-06-21 取得時点）**: 公式 [Slash commands リファレンス](https://kiro.dev/docs/cli/reference/slash-commands/)（Page updated 2026-06-12）の Keyboard shortcuts 表は「Fuzzy search commands and context files」と既存記述のまま。一方、公式 [Queue Steering ページ](https://kiro.dev/docs/cli/chat/queue-steering/)（同 2026-06-12）は「Press Ctrl+S to toggle between modes at any time」と明記し、設定キー `chat.keybindings.toggleInterruptBehavior`（既定 `ctrl+s`）でカスタマイズ可能と記載。同日更新だが両者の整合は未確認。**本サイトは v2.7.0 で Queue Steering モード切替が追加されたことを CLI 内蔵 changelog で確認済のため、両機能を併記**。実機の挙動は v2.7.0 起動後に確認推奨。

---

## 関連リンク

### リファレンス（本ディレクトリ）

- [01. Settings](01_settings.md)
- [03. CLI Commands](03_cli-commands.md)
- [04. Built-in Tools](04_built-in-tools.md)

### 機能文書

- [03. PlanAgent](../01_features/03_PlanAgent.md) — `/plan`
- [06. Usage Command](../01_features/06_UsageCommand.md) — `/usage`
- [10. Conversation Compaction](../01_features/10_ConversationCompaction.md) — `/compact`
- [14. HelpAgent](../01_features/14_HelpAgent.md) — `/help`
- [17. Granular Tool Trust](../01_features/17_GranularToolTrust.md) — `/tools`
- [18. Terminal UI](../01_features/18_TerminalUI.md) — TUI で動作する全スラッシュコマンドの体験
- [20. GuideAgent](../01_features/20_GuideAgent.md) — `/guide`
- [21. v24NewCommands](../01_features/21_v24NewCommands.md) — `/rewind`、`/effort`、`/settings`
- [22. Hooks](../01_features/22_Hooks.md) — `/hooks`
- [25. Auto Complete](../01_features/25_AutoComplete.md) — `/theme` とテーマ切替（Auto Complete のテーマ設定との連携）

### 公式情報源

- [Slash commands - Kiro CLI Documentation](https://kiro.dev/docs/cli/reference/slash-commands/)（公式ページ最終更新: 2026-06-12）

---

**Page updated**: 2026-05-24（本サイト初版）  
**公式ページ最終更新**: 2026-06-12
