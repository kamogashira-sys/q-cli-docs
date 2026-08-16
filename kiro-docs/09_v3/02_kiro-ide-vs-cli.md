[ホーム](../README.md) > [Kiro CLI v3（Early Access）](README.md) > Kiro IDE 版との比較

# 09-02. Kiro IDE 版との比較（仕様駆動開発）

> ⚠️ **Early Access**: 本ページは Kiro CLI v3（`kiro-cli --v3`）と Kiro IDE の仕様駆動開発を比較します。Early Access のため仕様変更の可能性があります（→ [09. v3 概要](README.md)）。
>
> 📌 **編集方針**: 本ページは **一次情報で確認できた事実のみ**を「同様／IDE が優位／CLI ならでは」に整理します。公式に確認できない比較は**断定して掲載しません**（推測を避けるため）。

**出典（一次情報）**:
- [Specs（公式・機能自体）](https://kiro.dev/docs/specs/) — Page updated 2026-08-12
- [Feature Specs（公式）](https://kiro.dev/docs/specs/feature-specs/) — Page updated 2026-08-04
- [Kiro CLI v3 概要・Known gaps（公式）](https://kiro.dev/docs/cli/v3/) — Page updated 2026-08-12

> **出典URLについての注記**: 旧 `/docs/cli/v3/specs/` は `/docs/specs/` への移転スタブです（2026-08 のドキュメント再構成）。本ページの出典は移転先の現行 URL に更新済みです（2026-08-16 確認）。

---

## 結論（先に要点）

- **コアは同じ**: 要件 / 設計 / タスクの 3 ファイル、3 フェーズ、`.kiro/specs/` の共有は **IDE も CLI も同様**。CLI で始めて IDE で続ける、といった**相互運用**ができます。**タスクの並列 wave 実行やワークフロー変種の選択も IDE/CLI/Web 共通**であることが現行公式で確認できます（旧版の記述を訂正、詳細は俯瞰表A参照）。
- **IDE が優位な点**: 視覚的なタスク実行 UI、GUI でのウィザード操作・図のレンダリング（様式の違い）。
- **CLI ならでは**: ターミナル統合（既存の CLI ワークフロー・シェルとの親和）。**ただし v3 はオプトインの Early Access で、非 TUI の classic モードは非対応**（下記の注意を参照）。

---

## 俯瞰表 A：一次情報で確認できた比較

| 観点 | Kiro IDE | Kiro CLI (v3) | 分類 | 出典 |
|------|:--:|:--:|------|------|
| 仕様駆動開発（要件 / 設計 / タスクの 3 ファイル・3 フェーズ） | ✅ | ✅ | **同様** | [Specs](https://kiro.dev/docs/specs/) |
| `.kiro/specs/` の共有・ポータビリティ（相互継続・同一フォーマット） | ✅ | ✅ | **同様** | Specs「shared across all Kiro surfaces」 |
| Spec タイプ（Feature Specs／Bugfix Specs、Quick Specは軽量変種） | ✅ | ✅ | **同様** | Specs「Types of Specs」 |
| 統一エンジン（改善が全サーフェスへ同時反映） | ✅ | ✅ | **同様** | v3 docs「single engine for all surfaces」 |
| タスクの**並列 wave 実行**（依存グラフで wave 単位に同時実行） | ✅ | ✅ | **同様（IDE/CLI/Web 共通）** | Specs「Running tasks in parallel」／Capability 表「Parallel task execution」= IDE/CLI/Web 全て ✓ |
| 視覚的なタスク実行 UI（リアルタイム状態表示） | ✅ | ➖（ターミナルの進捗ストリーム表示） | **IDE が優位**（UI 様式差） | Specs「Task Execution」 |
| GUI での Spec 作成・図のレンダリング（Kiro ペインの `+`、sequence diagram） | ✅ | ➖（`/spec` コマンド） | **IDE が優位**（操作様式差） | Specs |
| ワークフロー変種の選択（Requirements-First / Design-First） | ✅（GUI で選択） | ✅（`/spec new` で選択、公式 Getting Started は per-surface 手順として案内） | **同様** | Feature Specs「Getting Started」 |

> 凡例：✅=可能 ／ ❌=不可（出典あり） ／ ➖=非該当・様式が異なる。
>
> 📝 **旧記述の訂正（2026-08-16）**: 本表は以前「並列 wave 実行は IDE 限定・CLI は逐次」「ワークフロー変種の明示選択は IDE のみ」としていましたが、現行の公式 [Specs](https://kiro.dev/docs/specs/) は Capability 比較表で「Parallel task execution」を IDE/CLI/Web 共通機能として提示しており、CLI 限定の逐次実行を示す記述は見当たりません。また [Feature Specs](https://kiro.dev/docs/specs/feature-specs/) の「Getting Started」節も IDE/CLI/Web の区別なく「choose your workflow: Requirements-First or Design-First」と案内しています。上記は現行公式に基づき修正しています。
>
> ※「Spec タイプ」の補足: 公式 [Specs](https://kiro.dev/docs/specs/) は「Kiro supports two types of specs: Feature Specs / Bugfix Specs」と明記。**Quick Spec は独立したタイプではなく、Feature Specs の軽量変種**（承認ゲートを省いて3ファイルを一括生成）です。旧版の「Quick Plan」という名称は現行公式には存在せず、「Quick Spec」に統一されています。

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

- **仕様駆動の中核**: 要件（`requirements.md`。Bugfix Specsは`bugfix.md`）→ 設計（`design.md`）→ タスク（`tasks.md`）の 3 ファイル・3 フェーズ。
- **2 タイプ＋軽量変種**: Feature Specs／Bugfix Specsの2タイプ。Quick Specはいずれのタイプでも選べる軽量変種（承認ゲートを省いて3ファイルを一括生成）。
- **並列 wave 実行**: 依存グラフに基づく wave 単位の並列実行は IDE/CLI/Web 共通機能（Capability 比較表で全て✓）。
- **ワークフロー変種の選択**: Feature Specs の Requirements-First／Design-First は IDE/CLI/Web 共通で選択可能。
- **相互運用**: `.kiro/specs/` は全サーフェス共有・同一フォーマット。**CLI で開始 → IDE で継続**（およびその逆）が可能。

### 2. ❌ CLI ではできない / IDE が優位なこと

- **視覚的なタスク実行 UI**: IDE はタスクの状態をリアルタイムに可視化。CLI はターミナルの進捗ストリーム（機能は同等だが UI 様式が異なる）。
- **GUI 操作・図のレンダリング**: IDE は Kiro ペインの `+` から作成、sequence diagram を描画。CLI は `/spec` コマンド。

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
- [Specs](https://kiro.dev/docs/specs/)
- [Kiro CLI v3 概要](https://kiro.dev/docs/cli/v3/)
- [Feature Specs](https://kiro.dev/docs/specs/feature-specs/) ／ [Quick Spec](https://kiro.dev/docs/specs/quick-spec/)

---

**最終更新**: 2026-08-16（並列wave実行・ワークフロー変種選択・specタイプ数を一次情報で再確認・訂正）
**対象バージョン**: Kiro CLI v3（Early Access）— v2.8.x ＋ `--v3` で提供。3.0.0 GA は未リリース。
