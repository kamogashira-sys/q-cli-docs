[ホーム](../README.md) > [機能詳細ガイド](README.md) > Thinking Display

---

# Thinking Display（推論のリアルタイム表示）

## 概要

**Thinking Display** は、エージェントが問題をどのように考えているかを**リアルタイムで表示**する機能です。Kiro CLI **v2.5.0**（2026-05-29）で追加され、**既定で有効**になっています。

モデルの推論（reasoning）をストリーミング表示することで、エージェントのロジックを追い、誤った方向に進んでいないかを早期に把握し、なぜそのアプローチを選んだのかを理解できます。

**対応バージョン**: Kiro CLI v2.5.0+

> **公式Changelog原文（v2.5.0）**:
> Thinking display -- see the agent's reasoning process in real time. Enabled by default, toggle via `/settings` > Display > Show thinking.

---

## Adaptive Thinking（v2.2.0）との違い

「推論」に関わる機能は2つあり、目的が異なります。混同しないよう整理します。

| 機能 | バージョン | 役割 |
|------|-----------|------|
| **Adaptive Thinking** | v2.2.0 | マルチターン会話でモデルの推論を**保持**し、応答品質を向上させる（内部的な推論の継続） |
| **Thinking Display** | v2.5.0 | モデルの推論を画面に**表示**する（ユーザーが推論過程を見る） |

- Adaptive Thinking は「推論を保つ」仕組み、Thinking Display は「推論を見せる」仕組みです。

---

## 設定・使い方

### セッション内でトグル

```
/settings display
```

`/settings display` メニューの **Show thinking** で表示/非表示を切り替えます。変更は**次回チャットセッションから反映**されます（起動時に評価される設定のため）。

### 設定キー

| 設定キー | 型 | 既定 | 説明 |
|---------|---|------|------|
| `chat.showThinking` | boolean | `true` | エージェントの推論（thinking）ブロックをチャット出力に表示（v2.5.0+、起動時のみ反映） |

```bash
# 推論表示を無効化（次回セッションから）
kiro-cli settings chat.showThinking false
```

### 関連設定との区別

`chat.showThinking` と名前が似た `chat.enableThinking` がありますが、**別物**です。

| 設定キー | 説明 |
|---------|------|
| `chat.showThinking` | モデル**自身の推論ブロックの表示**（本機能） |
| `chat.enableThinking` | 複雑な推論のための **thinking ツールの有効化**（モデルが使う内部ツール） |

---

## 使用例

1. **誤りの早期検知**: エージェントが誤った前提を置いていないか、推論の流れを見て途中で気づける。
2. **アプローチの理解**: なぜそのコードや設計を選んだのか、根拠を推論表示から把握できる。
3. **アクセシビリティ・集中**: 推論表示が不要な場合は `chat.showThinking false` で非表示にし、最終応答のみに集中できる。

---

## 注意点・制限事項

- `Show thinking`（`chat.showThinking`）の変更は**即時反映されず、次回セッションから**有効になります（`/settings display` の animations / ASCII art / icons は即時反映なのに対し、Show thinking は起動時評価）。
- 既定で有効のため、推論表示が不要な環境では明示的に無効化します。

---

## 関連リンク

### 公式情報源
- [In-session settings（/settings display）](https://kiro.dev/docs/cli/chat/settings/#settings-display)
- [Thinking display 公式ドキュメント](https://kiro.dev/docs/cli/chat/settings/#thinking-display)
- [公式Changelog v2.5](https://kiro.dev/changelog/cli/2-5/)

### 本サイトの関連文書
- [02. Subagents](02_Subagents.md) — v2.5.0 の Review Loops（自己修正パイプライン）
- [21. v2.4 新コマンド](21_v24NewCommands.md) — `/settings` 統合メニュー
- [28. v2.6 新コマンド](28_v26NewCommands.md) — v2.6.0 の新コマンド群
- [04_reference/01_settings.md](../04_reference/01_settings.md) — `chat.showThinking` 等の設定キー
- [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md) — `/settings display` の正規仕様

---

**最終更新**: 2026年6月7日
**対象バージョン**: Kiro CLI v2.5.0+
