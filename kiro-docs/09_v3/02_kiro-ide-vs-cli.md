[ホーム](../README.md) > [Kiro CLI v3（Early Access）](README.md) > Kiro IDE 版との比較

# 09-02. Kiro IDE 版との比較（仕様駆動開発）

> ⚠️ **Early Access**: 本ページは Kiro CLI v3（`kiro-cli --v3`）と Kiro IDE の仕様駆動開発を比較します。Early Access のため仕様変更の可能性があります（→ [09. v3 概要](README.md)）。
>
> 📌 **編集方針**: 本ページは **一次情報で確認できた事実のみ**を「同様／IDE が優位／CLI ならでは」に整理します。公式に確認できない比較は**断定して掲載しません**（推測を避けるため）。

**出典（一次情報）**:
- [CLI specs（公式）](https://kiro.dev/docs/cli/v3/specs/) — Page updated 2026-06-19
- [Kiro CLI v3 概要・Known gaps（公式）](https://kiro.dev/docs/cli/v3/) — Page updated 2026-06-17
- [IDE Feature Specs（公式）](https://kiro.dev/docs/specs/feature-specs/) ／ [Quick Plan（公式）](https://kiro.dev/docs/specs/quick-plan/) — Page updated 2026-05-05

---

## 結論（先に要点）

- **コアは同じ**: 要件 / 設計 / タスクの 3 ファイル、3 フェーズ、`.kiro/specs/` の共有は **IDE も CLI も同様**。CLI で始めて IDE で続ける、といった**相互運用**ができます。
- **IDE が優位な点**: タスクの**並列 wave 実行**、視覚的なタスク実行 UI、GUI でのウィザード操作・図のレンダリング。
- **CLI ならでは**: ターミナル統合（既存の CLI ワークフロー・シェルとの親和）。**ただし v3 はオプトインの Early Access で、非 TUI の classic モードは非対応**（下記の注意を参照）。

---

## 俯瞰表 A：一次情報で確認できた比較

| 観点 | Kiro IDE | Kiro CLI (v3) | 分類 | 出典 |
|------|:--:|:--:|------|------|
| 仕様駆動開発（要件 / 設計 / タスクの 3 ファイル・3 フェーズ） | ✅ | ✅ | **同様** | IDE specs / CLI specs |
| `.kiro/specs/` の共有・ポータビリティ（相互継続・同一フォーマット） | ✅ | ✅ | **同様** | CLI specs「shared across all Kiro surfaces」 |
| Spec タイプ（Feature / Bug / Quick） | ✅ | ✅ | **同様**（Quick Plan ≈ Quick Spec） | IDE specs / CLI specs |
| 統一エンジン（改善が全サーフェスへ同時反映） | ✅ | ✅ | **同様** | v3 docs「single engine for all surfaces」 |
| タスクの**並列 wave 実行**（依存グラフで wave 単位に同時実行） | ✅ | ❌（`/spec run` は**逐次**） | **IDE が優位** | IDE specs「Run all Tasks」/ CLI specs「sequentially」 |
| 視覚的なタスク実行 UI（リアルタイム状態表示） | ✅ | ➖（ターミナルの進捗ストリーム表示） | **IDE が優位**（UI 様式差） | IDE specs / CLI specs |
| GUI での Spec 作成・図のレンダリング（Kiro ペインの `+`、sequence diagram） | ✅ | ➖（`/spec` コマンド） | **IDE が優位**（操作様式差） | IDE specs / CLI specs |
| ワークフロー変種の**明示選択**（Requirements-First / Design-First） | ✅（GUI で選択） | ➖（CLI specs に明示選択の記載なし） | **IDE に記載あり** | IDE feature-specs / CLI specs |

> 凡例：✅=可能 ／ ❌=不可（出典あり） ／ ➖=非該当・様式が異なる。
>
> ※「Spec タイプ」の補足: IDE specs は形式上 **Feature Specs / Bugfix Specs の 2 タイプ**とし、**Quick Plan は session type picker のモード**として提示します（公式 IDE specs / Quick Plan）。CLI は **Build a Feature / Fix a Bug / Quick Spec の 3 種**。session picker 上はいずれも 3 つ並ぶため本表では「同様」と分類しています。

---

## 俯瞰表 B：公式で明確に確認できていない点（断定して掲載しない）

以下は「CLI ならでは」と語られがちですが、**v3 の文脈で一次情報の裏付けが取れていない**ため、本サイトでは断定しません。公式に確認が取れ次第、表 A へ反映します。

| 観点 | 状況（事実） | なぜ断定しないか |
|------|------|------------------|
| ヘッドレス / CI での spec 実行 | 公式 Permissions に **CI 向け例**（`capability: all / effect: allow`）あり。一方で v3 の Known gap は **「Classic mode（非 TUI）は v3 非対応・TUI を使用」** と明記 | CI 例は権限設定の例示であり、「v3 がヘッドレス / 非対話で spec を実行できる」と明言したものではない。非 TUI 非対応の制限と整合する公式記載が未確認のため断定しない |
| `/goal`・Queue Steering 等との併用 | `/goal`・Queue Steering は v2.7 系（v2 エンジン）の機能 | **v3（`--v3`）での存在・spec agent との併用可否が公式 feature-overview に記載なし**。未確認 |
| SSH / リモート / コンテナでの spec 実行 | CLI はターミナルツールとしてリモート環境で使われる | IDE もリモート開発機能を持ち得るため「CLI のみ」と断定できない。CLI / IDE 双方の公式記載が未確認 |

---

## 3 つの軸で見る

### 1. ✅ 同様にできること

- **仕様駆動の中核**: 要件（`requirements.md`）→ 設計（`design.md`）→ タスク（`tasks.md`）の 3 ファイル・3 フェーズ。
- **3 タイプ**: Feature / Bug / Quick（CLI の Quick Spec と IDE の Quick Plan はいずれも「承認ゲートを省いて素早くタスクへ」という軽量版）。
- **相互運用**: `.kiro/specs/` は全サーフェス共有・同一フォーマット。**CLI で開始 → IDE で継続**（およびその逆）が可能。

### 2. ❌ CLI ではできない / IDE が優位なこと

- **並列 wave 実行**: IDE の「Run all Tasks」は依存グラフを構築し、独立タスクを **wave 単位で同時実行**（wave 内は並列・wave 間は逐次）。CLI の `/spec run` は**逐次**。
- **視覚的なタスク実行 UI**: IDE はタスクの状態をリアルタイムに可視化。CLI はターミナルの進捗ストリーム。
- **GUI 操作・図のレンダリング**: IDE は Kiro ペインの `+` から作成、sequence diagram を描画。
- **ワークフロー変種の明示選択**: IDE の Feature Specs は **Requirements-First / Design-First** を GUI で選択（既定の設定も可能）。CLI specs にはこの明示選択の記載がありません。

### 3. 🖥️ CLI ならではのこと（確認できた範囲）

- **ターミナル統合**: 既存の CLI / シェルのワークフローの中で仕様駆動開発を進められます。
- 表 B の項目（ヘッドレス / CI、`/goal` 併用、SSH/リモート）は、**公式に確認できるまで本サイトでは断定しません**。

> ⚠️ **v3 利用形態の注意**: v3 は `kiro-cli --v3` の **Early Access**。Known gap として **Amazon Linux 2 非対応**・**非 TUI（classic）モード非対応（TUI を使用）**・**V3 セッションは V2 で再開不可** があります（→ [09. v3 概要](README.md) の Known gaps）。

---

## 関連リンク

### 本セクション内
- [09. Kiro CLI v3（Early Access）概要](README.md)
- [01. 仕様駆動開発（Spec-driven development）](01_spec-driven-development.md)

### 公式情報源
- [CLI specs](https://kiro.dev/docs/cli/v3/specs/)
- [Kiro CLI v3 概要](https://kiro.dev/docs/cli/v3/)
- [IDE Feature Specs](https://kiro.dev/docs/specs/feature-specs/) ／ [Quick Plan](https://kiro.dev/docs/specs/quick-plan/)

---

**最終更新**: 2026-06-21
**対象バージョン**: Kiro CLI v3（Early Access）— v2.8.x ＋ `--v3` で提供。3.0.0 GA は未リリース。
