[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.7 新コマンド

---

# v2.7 新コマンド（/goal・Queue Steering・enriched /rewind・chat.terminalTitle）

## 概要

Kiro CLI **v2.7.0**（2026-06-12）で追加・拡張された機能を解説します。エージェントの**自律性と方向制御**を強化するリリースで、受入基準を満たすまで自己検証を繰り返す `/goal`、ターン実行中にエージェントへ指示を差し込む **Queue Steering**、各ターンの詳細を表示する **enriched `/rewind` preview**、そしてターミナルタイトルを制御する `chat.terminalTitle` 設定が追加されました。あわせて `/settings` の UI が統一されました。

**対応バージョン**: Kiro CLI v2.7.0+

> **注記**: 本ページは v2.7.0 を対象としています。後続の v2.7.1（2026-06-16）、v2.8.0 / v2.8.1（2026-06-17、CLI v3 Early Access）は**対応済み**です（→ [02_update/01_changelog.md](../02_update/01_changelog.md)、[30. v2.8 / V3プレビュー](30_v28V3Preview.md)、[09_v3/ Kiro CLI v3（Early Access）](../09_v3/README.md)）。最新版は[公式 Changelog](https://kiro.dev/changelog/cli/) を参照してください。

---

## /goal - 受入基準を満たすまで自己検証する自律ループ

`/goal` は、エージェントが目標（objective）に向けて**反復的に作業し、完了を検証してから停止する** goal 駆動ループを開始するコマンドです。通常のプロンプトと異なり、受入基準を満たすまで「実装 → 自己チェック」のサイクルを繰り返します。

```bash
# goal を設定（既定: 最大5反復）
> /goal refactor the auth module to use JWT tokens and ensure all tests pass

# 複雑なタスク向けに反復上限を引き上げる
> /goal --max 10 migrate the entire test suite from Jest to Vitest

# アクティブな goal をキャンセル
> /goal clear
```

- **反復回数**: 既定で**最大5反復**。`--max <number>` で上限を変更可能。
- **動作サイクル**: Plans（計画）→ Implements（実装）→ Verifies（検証）→ 失敗時は corrections（修正）→ 受入基準を満たせば完了。
- **受入基準は goal 文から導出**されます。「all tests pass」「no TypeScript errors」のように**「完了」の定義を明示**すると、エージェントに具体的な検証ターゲットを与えられます。
- **`/goal clear`**: アクティブな goal ループをキャンセルし、通常の対話モードに戻ります。
- **ループ中の介入**: 任意のタイミングでエージェントに追加指示を与えられます。**Queue Steering（Ctrl+S）** を使うと、キャンセルせずに mid-loop で方向修正できます。
- **ファイル変更の扱い**: ループ中に行われたファイル変更は、`clear` した後もディスク上に残ります（巻き戻しは VCS で行います）。

**ユースケース**: リファクタリング＋テスト通過、バグ修正＋回帰テスト追加、コードベース全体のリネームなど、自律実行に品質ゲートを組み込みたいマルチステップ作業。

詳細: [公式ドキュメント（/goal）](https://kiro.dev/docs/cli/chat/goal/)

---

## Queue Steering - ターン実行中の方向修正

**Queue Steering** は、エージェントがターンを実行している最中にメッセージを送り、エージェントが**次のツール境界**でそれを受け取って方向修正する仕組みです。間違った方向に進んだときに、キャンセルして最初からやり直す代わりに、修正メッセージをキュー（または即時差し込み）してコースを調整できます。

- **Ctrl+S** で2つのモードを切り替えます:
  - **steer モード**: メッセージをターン途中（次のツール境界）で**即時差し込み**
  - **queue モード**: メッセージを**ターン終了までバッファ**
- メッセージは**実行中ツールの途中ではなく、ツール境界で配信**されます。
- **Cancel（Ctrl+C）との違い**: Cancel は実行中の作業を破棄しますが、Queue Steering は作業を継続しながら方向修正します。

### 設定キー

| 設定キー | 既定 | 説明 |
|---------|------|------|
| `chat.keybindings.toggleInterruptBehavior` | `ctrl+s` | steer/queue モード切替のキーバインド |
| `chat.defaultInterruptBehavior` | `steer` | 起動時の既定モード（`steer` / `queue`） |

- 起動時の既定モードは `/settings` → `terminal` → `interrupt behaviour` からも変更できます。
- 切替キーは `kiro-cli settings chat.keybindings.toggleInterruptBehavior <key>` でカスタマイズ可能です。

詳細: [公式ドキュメント（Queue steering）](https://kiro.dev/docs/cli/chat/queue-steering/)、[04_reference/01_settings.md](../04_reference/01_settings.md)

---

## Enriched /rewind preview - ターンピッカーの情報拡充

`/rewind`（v2.4.0 で追加。会話を過去のターンで分岐）の**ターンピッカーが拡充**されました。各ターンの高レベルなサマリーを表示し、メッセージを個別に展開しなくても適切な分岐ポイントを素早く特定できます。

ターンピッカーに表示される情報:
- **ツール呼び出し詳細**（tool calls）
- **変更されたファイル**（files touched）
- **実行されたコマンド**（commands run）
- **中間メッセージ**（intermediate messages）
- **コンテキスト使用量**（context usage、ターンごと、新しい順に表示）

`/rewind` の基本機能（フォークであり破壊的な書き換えではない、元セッションは保持され `/chat load`・`/chat resume` で戻れる、等）は [21. v2.4 新コマンド](21_v24NewCommands.md) を参照してください。

詳細: [公式ドキュメント（/rewind）](https://kiro.dev/docs/cli/chat/rewind/)

---

## chat.terminalTitle 設定 - ターミナルタイトルの CLI 設定化

v2.6.0 ではターミナルウィンドウタイトル（`/title`）の有効化は `/settings display` → **Terminal title** のトグルのみでしたが、v2.7.0 で **`chat.terminalTitle` が CLI 設定として正式追加**され、設定キーからも制御できるようになりました。

```bash
# CLI 設定でターミナルタイトルを有効化
kiro-cli settings chat.terminalTitle true
```

- **型**: boolean（ターミナルタブのセッションタイトル表示/非表示）。
- v2.6.0 時点で存在した「CLI 内蔵 changelog は `chat.terminalTitle` に言及するが、公式設定リファレンスは『CLI 設定としては提供されない』と明記」という**不一致は、v2.7.0 の正式追加で解消**されました（→ [28. v2.6 新コマンド](28_v26NewCommands.md) の `/title` 注記、[02_update/01_changelog.md](../02_update/01_changelog.md) v2.7.0 セクション）。

> ⚠️ **一次情報の注記**: 公式 [Settings リファレンス](https://kiro.dev/docs/cli/reference/settings/)（Page updated 2026-06-05）は、**2026-06-21 取得時点でも v2.7.0 の `chat.terminalTitle` 追加が未反映**で、Info 注記も「not available as a CLI setting」のままです。本サイトは CLI 内蔵 changelog（v2.7.0）の追加文言「`chat.terminalTitle setting to show or hide the session title in the terminal tab`」を一次情報として採用し、型を boolean と判定しています。既定値は公式リファレンス未反映のため断定していません。

---

## /settings の UI 統合（改善）

v2.7.0 では `/settings` とその全サブコマンドの UI が統一されました。

- **統一された overlay frame、footer hints、ESC で戻るナビゲーション**: `/settings` および全サブコマンド（`theme`/`keybindings`/`terminal`/`display`/`history`）で共通の UI を採用。
- **`/settings theme Custom` のステップ式ウィザード化**: テーマ作成がステップ式ウィザードになり、ライブプレビューが**実際の会話レンダリングに整合**するようになりました。

`/settings` の各サブコマンドの仕様は [21. v2.4 新コマンド](21_v24NewCommands.md)（v2.4.0 で統合メニュー化）を参照してください。

詳細: [公式ドキュメント（In-session settings）](https://kiro.dev/docs/cli/chat/settings/)

---

## バグ修正（v2.7.0）

- カスタムエージェントが、組み込みエージェントと同様に**デフォルトリソース（steering、skills、AGENTS.md）を継承**するようになりました。
- Windows: `bun` および `node` の実行パスに `.exe` 拡張子を付与するよう修正されました。

---

## 注意点: Ctrl+S の取り扱い

`Ctrl+S` は v2.7.0 で Queue Steering の steer/queue モード切替に使われます。一方で、従来 `Ctrl+S` は「コマンドとコンテキストファイルのファジー検索」に割り当てられていました。

> **公式記述の不一致（2026-06-21 取得時点）**: 公式 [Slash commands リファレンス](https://kiro.dev/docs/cli/reference/slash-commands/)（Page updated 2026-06-12）の Keyboard shortcuts 表は `Ctrl+S` を「Fuzzy search commands and context files」と記載したままです。一方、公式 [Queue Steering ページ](https://kiro.dev/docs/cli/chat/queue-steering/)は「Press Ctrl+S to toggle between modes」と記載しています。同日（2026-06-12）更新ながら両者の整合は未確認です。本サイトは v2.7.0 で Queue Steering モード切替が追加されたことを CLI 内蔵 changelog で確認済みのため、両機能を併記しています。実機の挙動は v2.7.0 起動後の確認を推奨します（→ [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md) キーボードショートカット節）。

---

## 関連リンク

### 公式情報源
- [/goal 公式ドキュメント](https://kiro.dev/docs/cli/chat/goal/)
- [Queue steering 公式ドキュメント](https://kiro.dev/docs/cli/chat/queue-steering/)
- [/rewind 公式ドキュメント](https://kiro.dev/docs/cli/chat/rewind/)
- [In-session settings 公式ドキュメント](https://kiro.dev/docs/cli/chat/settings/)
- [スラッシュコマンドリファレンス](https://kiro.dev/docs/cli/reference/slash-commands/)（Page updated 2026-06-12）
- [Settings リファレンス](https://kiro.dev/docs/cli/reference/settings/)（Page updated 2026-06-05）
- [公式 Changelog v2.7](https://kiro.dev/changelog/cli/2-7/)

### 本サイトの関連文書
- [21. v2.4 新コマンド](21_v24NewCommands.md) — `/rewind`・`/effort`・`/settings`（v2.4.0、v2.7.0 進化注記あり）
- [28. v2.6 新コマンド](28_v26NewCommands.md) — `/transcript save`・`/title`・`--effort`・永続化（v2.6.0）
- [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md) — `/goal`・`/rewind`・`/settings`・キーボードショートカットの正規仕様
- [04_reference/01_settings.md](../04_reference/01_settings.md) — `chat.terminalTitle`・`chat.defaultInterruptBehavior`・`chat.keybindings.toggleInterruptBehavior` の設定キー
- [02_update/01_changelog.md](../02_update/01_changelog.md) — v2.7.0 / v2.6.1 の変更履歴

---

**最終更新**: 2026年6月21日
**対象バージョン**: Kiro CLI v2.7.0+
