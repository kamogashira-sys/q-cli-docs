[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.16 Tangent（V3側枝会話）

---

# v2.16 Tangent（V3側枝会話）

## 概要

Kiro CLI **v2.16.0**（公式表示日 2026-07-31）で、**名前付き・ネスト可能な側枝会話**を作成できる V3 版 `/tangent` が追加されました。**V3（`kiro-cli --v3`）のセッション内で提供される機能**です。

会話履歴を継承したまま脇道のトピックへ分岐し、後で元の位置へ戻れます。複数の側枝を同時に持てる（ネスト可能）ほか、会話木全体を表示するビジュアルピッカーから任意のセッションへ切り替えられる点が特徴です。

**対応バージョン**: Kiro CLI v2.16.0（V3 は Early Access）

> **注記**: V3 は **Early Access** であり、仕様変更の可能性があります。V3 の全体像・4 本柱・機能強化は専用セクション **[09_v3/](../09_v3/README.md)** にまとめています。最新は[公式 Changelog](https://kiro.dev/changelog/cli/) および [公式ドキュメント](https://kiro.dev/docs/cli/v3/tangent) を参照してください。

> ⚠️ **既存（V2 / classic、実験的機能）の`/tangent`とは別仕様**: 本サイトの [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md#tangent) が解説する既存の `/tangent`（トグル切替・単一チェックポイント・ネスト不可）とはコマンド名が同じですが、動作が異なります。公式ドキュメントも「the earlier experimental tangent mode behaves differently」と明記しています（出典: [Tangent（公式v3）](https://kiro.dev/docs/cli/v3/tangent)）。

---

## コマンド一覧

```bash
# ルートでは新規side-conversationへ分岐（自動命名 tangent-N）
# tangent内では親方向へ1階層戻る
> /tangent

# 名前付きside-conversationへ分岐・切替（新規なら作成、既存なら切替）
> /tangent <name>

# 会話木全体を表示するビジュアルピッカーを開き、任意のセッションへ切替
> /tangent ls

# どの深さからでも直接メイン会話へ戻る
> /tangent root
```

- **`/tangent`**: ルートで実行すると自動命名（`tangent-N`）の新規side-conversationへ分岐。tangent内で実行すると親方向へ1階層戻る。
- **`/tangent <name>`**: 指定した名前のside-conversationへ分岐・切替。同名が既存なら再利用、なければ新規作成。
- **`/tangent ls`**: 現在の会話木全体をビジュアルピッカーで表示し、任意のノードへ直接切替。
- **`/tangent root`**: 現在どの深さにいても、ワンステップでメイン会話（ルート）へ復帰。

---

## 動作詳細

- **ルートでの分岐**: メイン会話（ルート）から`/tangent`を実行すると、会話履歴を継承した新しいside-conversationが開始される。
- **ネスト**: tangent内から再度`/tangent`（または`/tangent <name>`）を実行すると、さらに1階層深いside-conversationを作成できる（tangentのtangent）。
- **状態表示**: フッターに現在位置を示す `↯ name` チップが表示される。
- **親方向への移動**: tangent内で`/tangent`（名前なし）を実行すると1階層上の会話へ戻る。任意の深さから一気にルートへ戻るには`/tangent root`を使う。

---

## 使い方の例

公式ドキュメントの "Ways to use tangents" に基づく主な用途:

- **Quick lookups（簡単な調べもの）**: メインの作業を中断せず、関連情報を短く確認したいときに分岐し、確認後にルートへ戻る。
- **Compare alternatives（代替案の比較）**: 複数のアプローチを別々のtangentで試し、結果を比較してから本流にどちらを採用するか決める。
- **Noisy debugging（ノイズの多いデバッグ）**: 詳細なログ確認や試行錯誤が多いデバッグ作業をtangentに退避し、メイン会話の履歴を汚さない。

---

## 既存classic版`/tangent`との違い

| 項目 | V2 / classic（既存、実験的機能） | V3（本機能） |
|------|------------------------------|-------------|
| 命名 | 不可（単一チェックポイント） | 可能（名前付き） |
| ネスト | 不可（1階層のみ） | 可能 |
| 切替方法 | トグル（`/tangent`・`Ctrl+T`） | ビジュアルピッカー（`/tangent ls`） |
| 対応設定 | `chat.enableTangentMode`・`chat.tangentModeKey`・`introspect.tangentMode` | なし（公式ページに設定項目の言及なし） |
| 提供範囲 | V2安定版・classic全般 | V3（`kiro-cli --v3`）限定 |
| 公式ステータス | Experimental feature that may change or be removed | ⬆️ Enhanced（Feature comparisonより） |

出典: [Tangent（公式v3）](https://kiro.dev/docs/cli/v3/tangent)、[experimental Tangent mode（公式）](https://kiro.dev/docs/cli/experimental/tangent-mode/)、[Feature comparison（公式v3）](https://kiro.dev/docs/cli/v3/new-features/)

---

## 注意点・制限事項

- **V3 専用**: `/tangent`（本機能）は V3 セッション（`kiro-cli --v3`）内でのみ利用できます。V2 安定版のスラッシュコマンド一覧（[04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md)）のコマンド数SSoTには含めていません（V3限定コマンドを対象外とする既存方針を踏襲）。
- **V3 は Early Access**: 仕様変更・機能追加の可能性があります（→ [09_v3/](../09_v3/README.md)）。
- TUI（V2安定版のターミナルUI）の対応表（[18. Terminal UI](18_TerminalUI.md)）は既存classic版`/tangent`のみを対象としており、本機能（V3限定）はそもそも比較対象外です。

---

## 関連リンク

- [Tangent（公式v3）](https://kiro.dev/docs/cli/v3/tangent) — V3版`/tangent`の公式ドキュメント
- [experimental Tangent mode（公式）](https://kiro.dev/docs/cli/experimental/tangent-mode/) — 既存classic版の公式ドキュメント
- [Feature comparison（公式v3）](https://kiro.dev/docs/cli/v3/new-features/) — V2からV3への機能ステータス比較表
- [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md#tangent) — 既存classic版`/tangent`の解説（本サイト）
- [09_v3/ Kiro CLI v3（Early Access）概要](../09_v3/README.md) — 機能強化（v2→v3）の一覧
- [変更履歴 v2.16.0](../02_update/01_changelog.md)
- [公式Changelog v2.16](https://kiro.dev/changelog/cli/2-16/)

---

**最終更新**: 2026-08-01  
**対象バージョン**: Kiro CLI v2.16.0+（V3 は Early Access）
