[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.24 新機能

# 43. v2.24 新機能 — セッション全体のツール承認・`.env` の自動読み込み廃止

## 概要

Kiro CLI **v2.24.0**（2026-09-23）と **v2.24.1**（2026-09-24）では、V3 にセッション全体のツール自動承認が加わり、`/sessions` のフィルタを組み合わせられるようになりました。⚠️ 同時に、**プロジェクトの `.env` ファイルを自動で読み込まなくなりました**。

- **v2.24.0**: [V3] `/tools trust-all`、[V3] `/sessions` の Filter・Sort・Group、⚠️ 環境の分離（`.env` の自動読み込み廃止）、[V2] 画像処理の回復力向上
- **v2.24.1**: [V3] `/sessions` の既定が現在のディレクトリに、[V3] 引数なしの `/effort` が `/model` の Effort 設定を開く、Windows で `kiro-cli --cloud` が `chat` なしで動作

## ⚠️ 環境の分離 — `.env` の自動読み込み廃止

プロジェクトの `.env` ファイルは、chat セッション・MCP サーバー・ツールへ**自動で読み込まれなくなりました**。Kiro はターミナルから引き継いだ環境で起動します。

`.env` の変数に依存している場合は、次のように対応します。

1. Kiro を起動する前に、シェルで変数を export する
2. MCP サーバーでは、export した値をサーバー設定の `env` で `${変数名}` として参照する

```bash
# 例: .env の内容をシェルへ読み込んでから起動する
set -a; . ./.env; set +a
kiro-cli
```

```json
{
  "mcpServers": {
    "web-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-bravesearch"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    }
  }
}
```

上の JSON は公式 [MCP Configuration](https://kiro.dev/docs/mcp/configuration/#environment-variables) の「Example configurations — Local server with environment variables」の例です。`set -a; . ./.env; set +a` は、bash / zsh の `set -a`（allexport：以降に定義した変数を自動で export する）を使って `.env` を読み込むシェルの書き方で、Kiro の機能ではありません。`.` で読み込むと `.env` の中身はシェルスクリプトとして実行されるため、内容を確認してから使ってください。

> **影響を受けやすい構成**: `.env` に API キーを置き、MCP サーバー設定から `${...}` で参照していた構成は、v2.24.0 以降はシェルで export しない限り `.env` の値が渡されません（参照先の変数が未定義の場合の扱いは公式に記載がありません）。

## [V3] セッション全体のツール承認 — `/tools trust-all`

`/tools trust-all` を実行すると、現在の V3 セッションの残りのツール呼び出しを自動で承認します。

```text
/tools trust-all
```

既定では安全上の警告が表示され、有効にする前に確認を求められます。公式 [Permissions](https://kiro.dev/docs/permissions/) は、ターミナル UI では `--trust-all-tools` と `/tools trust-all` のどちらも確認の警告を表示し、リスクを了承しないと進めないと説明しています。**信頼できる環境でのみ有効にしてください。**

> v2.27.0 で、永続化可能な capability をエージェントサービスが省略した場合に trust-all モードが承認要求を繰り返す不具合が修正されました。

## [V3] セッションダッシュボードの操作

`/sessions` で Filter・Sort・Group の各操作を開くと、選択肢がその場に表示されるようになりました。公式 [Session management](https://kiro.dev/docs/cli/chat/session-management/) の操作方法は次のとおりです。

| キー | 動作 |
|------|------|
| `Tab` | 操作部とセッション一覧の間でフォーカスを移動 |
| `←` / `→` | Search・Filter・Sort・Group を切り替え |
| `↑` / `↓` | 選択肢を移動 |
| `Space` | フィルタの on / off |
| `Enter` | 一覧へ戻る |
| `Ctrl+X` | フィルタをリセット（`current workspace only` だけ on） |

### フィルタ

| フィルタ | 内容 |
|---------|------|
| `current workspace only` | 現在のワークスペースのセッションだけを表示（既定 on） |
| `main sessions` | ルートと単独のセッションを残し、Tangent・rewind・サブエージェントが作った子セッションを隠す（v2.23.1 で追加） |
| `bookmarked` | ブックマークしたセッション |
| `includes empty` | 既定では非表示の空セッションを表示 |

`current workspace only` を on のままにするか off にするかは、設定 `chat.sessionDashboard.scope`（`current` / `all`、既定 `current`）に記憶されます。現在のディレクトリにセッションが無い場合、ダッシュボードは保存済みの選択を変えずに一時的に全ワークスペースを表示します。

ソートは `last used`・`session name`・`messages`、グループは `workspace`・`recency`・`status`（利用可能な場合）・`none` から選べます。

> **v2.24.1 の変更**: V3 の `/sessions` は現在のディレクトリのセッションで開くようになりました。すべてのディレクトリを一覧するには `current workspace only` を外します（選択は記憶されます）。

## [V2] 画像処理の回復力向上

V2 では、対応サイズを超える画像を縦横比を保って縮小し、セッションの読み込み時には保存済み履歴内の大きすぎる画像も縮小します。それでもモデルプロバイダーが画像を拒否した場合は自動で再試行し、拒否された画像をプレースホルダーに置き換えて通知を表示し、会話を続けられるようにします（公式 [Working with images](https://kiro.dev/docs/cli/chat/images/)）。

## v2.24.1 の要点

| 変更 | 内容 |
|------|------|
| [V3] `/effort` | 引数なしの `/effort` が `/model` の Effort 設定を開く（V2 と統一。→ [42. v2.23 新機能](42_v223NewFeatures.md)） |
| [V3] `/clear`・`/chat new` | `/clear` は現在のモデルと effort を保つ。`/chat new` は現在のモデルを保ち、effort は保存済みの値に戻る。`--model` と `--effort` は起動時のセッションにだけ適用される |
| Windows | `kiro-cli --cloud` と `--repo` が `chat` サブコマンドなしで動作する（macOS・Linux と同じ） |
| V2 のカスタムエージェント | `kiro_default` など組み込みエージェント名を使う設定が、無視されず再び読み込まれる |
| steering メッセージ | 連続したメッセージがすぐ届き、compaction 中に送ったメッセージは完了までキューに入る |

その他の改善（ターミナルの再描画の効率化、`Ctrl+L` での画面クリア、macOS の Homebrew 管理インストールを内蔵アップデーターが更新しない など）と修正の完全な一覧は [変更履歴の v2.24.1・v2.24.0](../02_update/01_changelog.md) を正とします。

## 関連リンク

### 本サイト

- [42. v2.23 新機能](42_v223NewFeatures.md)
- [44. v2.25 新機能](44_v225NewFeatures.md)
- [41. v2.22 新機能](41_v222NewFeatures.md)（`/sessions` の再設計）
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [Settings リファレンス](../04_reference/01_settings.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.24](https://kiro.dev/changelog/cli/2-24/)
- [Permissions](https://kiro.dev/docs/permissions/)
- [Session management](https://kiro.dev/docs/cli/chat/session-management/)
- [MCP Configuration — Environment variables](https://kiro.dev/docs/mcp/configuration/#environment-variables)
- [Working with images](https://kiro.dev/docs/cli/chat/images/)

**最終更新**: 2026-10-04
**対象バージョン**: Kiro CLI v2.24.0+（`/tools trust-all`・`/sessions` は V3 Early Access）
