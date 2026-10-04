[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.23 新機能

# 42. v2.23 新機能 — `/model` の推論設定・リポジトリ接続前のクラウドセッション

## 概要

Kiro CLI **v2.23.0**（2026-09-21）と **v2.23.1**（2026-09-23）では、推論設定（thinking・effort）が `/model` にまとまり、V3 のクラウドセッションをリポジトリの接続前に始められるようになりました。

- **v2.23.0**: `/model` の推論設定（V2 の引数なし `/effort` はレガシー扱い）、[V3] リポジトリ接続前のクラウドセッション、作業時間の表示、インストールサイズの削減
- **v2.23.1**: `/sessions` のメインセッション絞り込み、環境変数プレフィックス付き許可コマンドの再確認の解消、classic の `--resume-id` のエラー化

## `/model` の推論設定

`/model` を開くと、モデルの切り替えと、選んだモデルの **Thinking** と **Effort** の設定を 1 か所で行えます。パネルにはそのモデルが対応する設定と値だけが表示されます。

| 設定 | 内容 |
|------|------|
| **Thinking** | 対応モデルが extended reasoning を使うかどうか |
| **Effort** | モデルが推論にかける量（`low` / `medium` / `high` / `xhigh` / `max` のうち、モデルが対応するもの） |

公式 [Reasoning effort](https://kiro.dev/docs/models/effort/) は、`/model` の **Thinking** はモデルの動作を変える設定であり、`/settings display` の **Show thinking**（推論ブロックを画面に表示するかどうか）や実験的機能の Thinking ツールとは別物だと説明しています。

### `/effort` の扱いの変化

| 版 | V2 | V3 |
|----|----|----|
| v2.23.0 | 引数なしの `/effort` は**レガシー**。非推奨の警告を表示し、`/model` の Effort 設定を開く | 引数なしの `/effort` は独自のピッカーを開く |
| v2.24.1 | 変更なし | 引数なしの `/effort` が `/model` の Effort 設定を開く（V2 と統一） |

`/effort <level>` は V2・V3 とも引き続き使えます。

```text
# 推論設定を開く（主なインターフェース）
/model

# レベルを直接設定する
/effort high
```

### 保存のされ方

公式 [Reasoning effort](https://kiro.dev/docs/models/effort/) の「Persisting your effort level (CLI)」は次のように説明しています。

- `/model` での effort の選択は自動的に保存される
- `/effort <level>` は現在のセッションだけを変える。そのレベルを現在のモデルの既定にするには `/effort set-current-as-default` を実行する
- V3 では、`--effort` と `--model` は Kiro が起動時に開始するセッションにだけ適用され、既定としては保存されない
- 保存先は `~/.kiro/settings/cli.json`

> **経緯**: `/model`・`/effort` の保存方式は v2.6.0（自動永続化）→ v2.12.3（sticky default）→ v2.14.1（セッション限定）と変わってきました。経緯は [28. v2.6 新コマンド](28_v26NewCommands.md) を参照してください。v2.23.0 以降、`/model` パネルで選んだ Thinking・Effort の設定は今後のセッションのために保存されます。一方、公式 Slash commands の `/model` の項は、モデル自体の選択は現在のセッションにのみ適用され、既定にするには `/model set-current-as-default` を実行すると説明しています。

## [V3] リポジトリ接続前のクラウドセッション

リポジトリを接続する前にクラウドセッションを開始し、準備ができたら `/repo` で紐付けられるようになりました。ソースプロバイダーが未接続の場合は接続画面が開き、リポジトリは任意と表示されます。

```bash
# リポジトリなしで開始
kiro-cli --cloud

# セッション内で後から紐付ける
/repo
/repo owner/repository
```

公式 [Cloud sessions](https://kiro.dev/docs/cloud-sessions/) は、起動時のチェックリストに `✓ 12 repositories found, /repo to select (optional)` のような行が表示される例を示しています。Cloud Sessions 全体は [36. Cloud Sessions](36_CloudSessions.md) を参照してください。

## 作業の進捗表示

Kiro が作業している間、ビジー表示に**実際に作業している時間**が表示されます。承認や質問への回答を待っている間はタイマーが止まり、応答すると再開します（公式 [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)）。

`chat.terminalTitle` を有効にしていると、タイトルバーのアニメーションスピナーが動作状況を示します。

## その他の改善（v2.23.0）

| 改善 | 内容 |
|------|------|
| ターミナルの性能 | 長い会話でストリーミング応答の描画が滑らかになり CPU 使用量が減少。fullscreen のホイールスクロールの応答も効率化 |
| ConEmu 対応 | ANSI 処理が有効な場合に進捗表示が動作する |
| インストールサイズ | 同梱ランタイムを圧縮してサイズを削減 |
| セッションダッシュボード（V3） | 特に履歴が大きい場合に `/sessions` が速く開く |
| ツール拒否時のフィードバック（V3） | 拒否時に入力したフィードバックをモデルへ送り、次の動作を調整させる |
| 応答の出典区別（V3） | サーバーが提供した内容をモデル自身の応答と分けて保持する |
| `/kiro` | イースターエッグに、動き回るゴーストのアニメーションが追加 |

## v2.23.1 の要点

- `/sessions` で Tangent・rewind・サブエージェントなどの派生セッションを隠し、メインセッションだけを表示できる
- 環境変数のプレフィックスが付いた許可済みコマンドが、実行のたびに確認を求めなくなった
- classic の `--resume-id` が、存在しない・読めない・空・V2 専用のセッションに対してエラーを報告し、新しい会話を始めなくなった

修正項目の完全な一覧は [変更履歴の v2.23.1・v2.23.0](../02_update/01_changelog.md) を正とします。

## 関連リンク

### 本サイト

- [41. v2.22 新機能](41_v222NewFeatures.md)
- [43. v2.24 新機能](43_v224NewFeatures.md)
- [21. v2.4 新コマンド（/rewind, /effort, /settings）](21_v24NewCommands.md)
- [28. v2.6 新コマンド](28_v26NewCommands.md)
- [36. Cloud Sessions](36_CloudSessions.md)
- [スラッシュコマンドリファレンス](../04_reference/02_slash-commands.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.23](https://kiro.dev/changelog/cli/2-23/)
- [Reasoning effort](https://kiro.dev/docs/models/effort/)
- [Cloud sessions](https://kiro.dev/docs/cloud-sessions/)
- [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)

**最終更新**: 2026-10-04
**対象バージョン**: Kiro CLI v2.23.0+（リポジトリ接続前のクラウドセッションは V3 Early Access）
