[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.6 新コマンド

---

# v2.6 新コマンド（/transcript save・/title・--effort・永続化）

## 概要

Kiro CLI **v2.6.0**（2026-06-05）で追加・拡張されたコマンドと機能を解説します。会話のエクスポート（`/transcript save`）、ターミナルウィンドウタイトル（`/title`）、起動時の推論レベル指定（`--effort`）、そしてモデル・effort 設定の**自動永続化**により、成果物の共有とセッションの再開がより簡単になりました。

**対応バージョン**: Kiro CLI v2.6.0+

---

## /transcript save - 会話のエクスポート

`/transcript` は従来、会話をページャで開くコマンドでしたが、v2.6.0で **`save` サブコマンド**が追加され、会話をファイルにエクスポートできるようになりました。

```bash
# ページャで開く（従来機能）
> /transcript

# プレーンテキスト / JSON でレンダリング（インライン切替）
> /transcript --plain
> /transcript --json

# ファイルにエクスポート（既定: Markdown）
> /transcript save conversation.md

# 形式を指定してエクスポート
> /transcript save conversation.txt --plain
> /transcript save conversation.json --json
```

- 既定の保存形式は **Markdown**。
- `--plain`（プレーンテキスト）・`--json`（JSON）はページャ内の表示形式もインラインで切り替えます。
- **形式はファイル拡張子ではなくフラグで決定**されます（`save` は既定で Markdown、フラグ指定で変更）。
- v2.6.0では `/transcript` がページャを**最下部で開く**ようになり、最新メッセージが先頭に表示されます。

**ユースケース**: チームメンバーへの共有、チケットへの添付、別ツールへの取り込み。

---

## /title - ターミナルウィンドウタイトル

`/title` は、現在のセッションのターミナルウィンドウタイトルを設定・クリア・表示するコマンドです（v2.6.0新規）。どのセッションがどのウィンドウで動いているかを把握しやすくなります。タイトルは `kiro: <text>` の形式で表示されます。

```bash
# 現在のタイトルを表示
> /title

# 任意のタイトルを設定（sticky）
> /title weekly standup notes

# カスタムタイトルをクリア
> /title --clear
```

- タイトルはセッショントピックまたはワークスペースパスから**自動導出**されます。
- 手動設定したタイトルは **sticky**（`--clear` するまでセッション更新をまたいで保持）。
- タイトルは **60文字で truncate** されます。

### 有効化方法

`/title` を使うには、**ターミナルタイトル機能を有効化**する必要があります。

- 有効化: `/settings display` → **Terminal title**
- 無効状態で `/title` を実行すると、有効化方法が案内されます。

### 注意点

- タイトル設定には **OSC 0 エスケープシーケンス**を使用します。一部のターミナルはこれを無視します。
- **tmux** では、外側のターミナルのタイトルを更新するために `set-titles on` が必要です。
- タイトルは終了時にリセットされます（正確な挙動はターミナル依存）。

> **注記（一次情報の不一致）**: CLI 内蔵 changelog は `/title` の有効化方法として「`chat.terminalTitle` 設定」に言及していますが、公式設定リファレンス（更新 2026-06-05）は「terminal title は `/settings display` → Terminal title でトグルし、**CLI 設定としては提供されない**（not available as a CLI setting）」と明記しています。本サイトは公式設定リファレンスに従い、`/settings display` での有効化を正とします。
>
> **更新（v2.7.0）**: **v2.7.0 で `chat.terminalTitle` が CLI 設定として正式追加され、本不一致は解消されました**。`chat.terminalTitle` 設定でも有効化制御が可能になりました（→ [02_update/01_changelog.md](../02_update/01_changelog.md) の v2.7.0 セクションを参照）。なお、公式 [Settings リファレンス](https://kiro.dev/docs/cli/reference/settings/)（Page updated 2026-06-05）は v2.7.0 の追加が未反映（2026-06-21 取得時点）です。

---

## --effort フラグ - 起動時の推論レベル指定

`kiro-cli chat` の起動時に、初期 effort（推論）レベルを指定できる **`--effort` フラグ**が追加されました（v2.6.0）。

```bash
# 起動時に effort レベルを指定
kiro-cli chat --effort high
kiro-cli chat --effort max
```

- 指定可能なレベル: `low` / `medium` / `high` / `xhigh` / `max`
- クイックな調べ物は低レベルで高速に、複雑な作業は最初のプロンプトから深い推論を、という使い分けが起動時から可能になります。
- セッション中は引き続き `/effort` でレベルを変更できます（→ [21. v2.4 新コマンド](21_v24NewCommands.md)）。

---

## Persistent Model and Effort Preferences - 設定の自動永続化

v2.6.0では、`/model` と `/effort` の選択が**自動的に永続化**されるようになりました。一度モデルや effort を切り替えると、Kiro はその設定を将来のセッションに引き継ぎます。

- **`/model set-current-as-default` を実行する必要がなくなりました**（従来はデフォルト化に手動操作が必要）。
- モデル・effort の選択がそのまま「次回以降の既定」になります。

```bash
# v2.5.x 以前: デフォルト化に手動操作が必要だった
> /model claude-opus-4
> /model set-current-as-default   # ← これが必要だった

# v2.6.0以降: 切り替えるだけで自動的に次回以降へ引き継がれる
> /model claude-opus-4            # これだけで永続化される
```

- 永続化の詳細: [公式ドキュメント（Settings persistence）](https://kiro.dev/docs/cli/chat/settings/#persistence)
- per-model のデフォルト effort は `~/.kiro/settings/cli.json` の `chat.modelDefaults` でも設定可能（→ [04_reference/01_settings.md](../04_reference/01_settings.md)）。

### v2.12.3での進化（2026-07-15リリース）: sticky default 化とオプトアウト設定

**v2.12.3** で、`/model`・`/effort` の永続化が **sticky default** として明確化され、**オプトアウト設定**が追加されました。

- 選択したモデル・推論レベルが**恒久デフォルト**として保存され、**新規セッションに自動適用**されます（v2.6.0 の自動永続化の挙動を明示化）。
- 自動適用を無効化する設定が新規追加:
  - `chat.disableAutoDefaultModel`（Boolean・既定 `false`）: モデルの自動デフォルト化を無効化。
  - `chat.disableAutoDefaultEffort`（Boolean・既定 `false`）: effort の自動デフォルト化を無効化。
- 設定の詳細: [04_reference/01_settings.md](../04_reference/01_settings.md)、[公式 Settings リファレンス](https://kiro.dev/docs/cli/reference/settings/)。

---

## /knowledge update（引数なし）- 全ナレッジベース一括再インデックス

`/knowledge update` を**引数なし**で実行すると、登録済みの全ナレッジベースを一括で再インデックスできるようになりました（v2.6.0）。

```bash
# 単一エントリの再インデックス（従来）
> /knowledge update ./docs

# 全ナレッジベースを一括再インデックス（v2.6.0新規）
> /knowledge update
```

> ナレッジベース機能は実験的機能です。`kiro-cli settings chat.enableKnowledge true` で有効化します。

---

## 関連リンク

### 公式情報源
- [スラッシュコマンドリファレンス](https://kiro.dev/docs/cli/reference/slash-commands/)（更新 2026-06-05）
- [Effort 公式ドキュメント](https://kiro.dev/docs/cli/chat/effort/)
- [Settings persistence 公式ドキュメント](https://kiro.dev/docs/cli/chat/settings/#persistence)
- [公式Changelog v2.6](https://kiro.dev/changelog/cli/2-6/)

### 本サイトの関連文書
- [21. v2.4 新コマンド](21_v24NewCommands.md) — `/rewind`・`/effort`・`/settings`（v2.4.0）
- [27. Thinking Display](27_ThinkingDisplay.md) — v2.5.0 の推論リアルタイム表示
- [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md) — `/transcript`・`/title`・`/effort`・`/model`・`/knowledge` の正規仕様
- [04_reference/01_settings.md](../04_reference/01_settings.md) — `chat.modelDefaults` 等の設定キー

---

**最終更新**: 2026-07-20
**対象バージョン**: Kiro CLI v2.6.0+（`/model`・`/effort` 永続化は v2.12.3 で sticky default 化・オプトアウト設定追加）
