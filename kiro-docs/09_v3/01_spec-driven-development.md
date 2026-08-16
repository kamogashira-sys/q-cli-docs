[ホーム](../README.md) > [Kiro CLI v3（Early Access）](README.md) > 仕様駆動開発

# 09-01. 仕様駆動開発（Spec-driven development）— CLI での実践

> ⚠️ **Early Access**: 本ページは Kiro CLI v3（`kiro-cli --v3`）の機能を扱います。Early Access のため仕様変更の可能性があります（→ [09. v3 概要](README.md)）。

**出典（一次情報）**:
- [Spec-driven development（公式・機能自体）](https://kiro.dev/docs/specs/)
- [Feature Specs（公式）](https://kiro.dev/docs/specs/feature-specs/)
- [Kiro CLI v3 概要（公式・What's new in CLI 3.0）](https://kiro.dev/docs/cli/v3/)

> **出典URLについての注記**: 旧 `/docs/cli/v3/specs/` は `/docs/specs/` への移転スタブです（2026-08 のドキュメント再構成）。本ページの出典は移転先の現行 URL に更新済みです（2026-08-16 確認）。

---

## 仕様駆動開発とは

**仕様駆動開発（Spec-driven development）** は、いきなりコードを書くのではなく、**「要件 → 設計 → タスク」を順に固めてから実装する**進め方です。Kiro CLI v3 には、この進め方を担う**組み込みの Spec agent** が用意されています。

ねらいは「**計画してから実行する（plan-then-execute）**」こと。あいまいな指示で AI に丸投げするのではなく、**何を作るか（要件）→ どう作るか（設計）→ どの順で作るか（タスク）**を文書として残し、合意してから実装に入ります。生成物はすべてファイルとして残るため、**レビュー・編集・追跡**ができます。

---

## ワークフロー（3 フェーズ＋実行）と生成ファイル

Spec agent のワークフローは **要件・設計・タスクの 3 フェーズ**で計画を固め、その後 **Execution（実行）** へ進みます。**ファイルを生成するのはこの 3 フェーズ**で、各フェーズが `.kiro/specs/<name>/` に 1 つずつ生成します（公式 Specs「Three-Phase Workflow」）。**Execution はフェーズではなく実行段階**で、ファイルを新規生成せず、上記 3 ファイルを更新しながら進みます。フェーズの区切りでユーザーが内容を編集できます。

| ステップ | 内容 | 生成ファイル |
|---------|------|-------------|
| **Requirements / Bug Analysis**（フェーズ 1） | Feature Specs は受入基準を含む要件を定義。Bugfix Specs はバグの現在・期待・不変の挙動を分析 | Feature Specs: `.kiro/specs/<name>/requirements.md`／Bugfix Specs: `.kiro/specs/<name>/bugfix.md` |
| **Design**（フェーズ 2・設計） | アーキテクチャ・設計を記述 | `.kiro/specs/<name>/design.md` |
| **Tasks**（フェーズ 3・タスク） | 依存関係を追跡した順序付き実装計画 | `.kiro/specs/<name>/tasks.md` |
| **Execution**（実行段階・※フェーズではない） | タスクを実行し進捗を追跡（実行方式は次節「タスク実行」を参照） | （新規生成なし。上記ファイルを更新しながら進行） |

> 📝 **生成ファイル名の訂正（2026-08-16）**: Bugfix Specs は `requirements.md` ではなく **`bugfix.md`** を生成します（公式 [Specs](https://kiro.dev/docs/specs/) の Core Structure「requirements.md (or bugfix.md)」より）。旧版の本ページはタイプを問わず `requirements.md` と記載していましたが誤りです。

---

## CLI での使い方（`/spec` コマンド）

```bash
# V3 エンジンで起動
kiro-cli --v3

# spec の一覧・選択
> /spec

# 新規 spec を作成（要件定義から開始）
> /spec new add-user-auth

# 既存 spec を再開
> /spec add-user-auth

# タスクを自律実行（依存関係のないタスクは並列実行）
> /spec run add-user-auth
```

- **`/spec`**: 既存 spec の一覧・選択。
- **`/spec new <name>`**: 新規作成。要件定義フェーズから始まります。**v2.15.0 以降**、spec 名を指定した直後に「このspecが何をカバーするか」を尋ねるガイド付き説明ステップが追加されました。ここで入力した説明はエージェントが要件を生成する際のground truth（正解データ）として使用され、spec名のみから推測するよりも精度の高い要件定義が可能になります（出典: [公式Changelog v2.15](https://kiro.dev/changelog/cli/2-15/)、詳細: [Specs（公式）](https://kiro.dev/docs/specs/)）。
- **`/spec <name>`**: 既存 spec を再開。
- **`/spec run <name>`**: `tasks.md` のタスクを実行します。

> 💡 **タスク実行は並列 wave 方式（IDE/CLI/Web 共通）**: 公式 [Specs](https://kiro.dev/docs/specs/) の「Running tasks in parallel」節は、Kiro が `tasks.md` の依存関係グラフを構築し、依存のないタスクを **wave（波）** としてまとめて並列実行すると説明しています（"Waves execute sequentially; tasks within a wave execute concurrently"）。この記述は IDE/CLI/Web の区別なく提示されており、Capability 比較表でも「Parallel task execution」は IDE/CLI/Web すべてに ✓ が付いています。CLI 固有の実行順序（サーフェス限定の逐次実行）を裏付ける公式記述は見当たりません。

> 📝 **旧記述の訂正（2026-08-16）**: 本ページは以前「公式 CLI specs は `/spec run` を『tasks run sequentially with verification between steps』と記載」「IDE 版の並列 wave 実行との違いがある」としていましたが、現行の公式 [Specs](https://kiro.dev/docs/specs/) ページには当該引用文は存在せず、並列 wave 実行は IDE/CLI/Web 共通の記述に変わっています。CLI 固有のタスク実行順序に関する詳細ページ（例: 2.x reference 等）は別途確認できていないため、断定的な「CLIは逐次」という記述を削除し、確認できた事実のみを記載しています。

---

## 2 つのタイプ（＋ Quick Spec という軽量変種）

spec を始めるとき、目的に応じて選びます。公式 [Specs](https://kiro.dev/docs/specs/) は「Kiro supports **two types** of specs」と明記しており、タイプは以下の 2 つです。

| タイプ | 用途 |
|--------|------|
| **Feature Specs** | 新機能の開発（要件 → 設計 → タスクをしっかり固める）。**Requirements-First**（要件から開始）と **Design-First**（設計から開始）の 2 ワークフローを選べる |
| **Bugfix Specs** | バグ修正向け。バグの現在の挙動・期待される挙動・変更してはいけない挙動を分析してから設計・タスクへ進む。生成ファイルは `requirements.md` ではなく **`bugfix.md`** |

**Quick Spec** は上記 2 タイプのいずれかを選んだ後に使える**軽量オプション**で、承認ゲート（フェーズごとの確認）を省略し、要件・設計・タスクの 3 ファイルを一括生成します。公式 [Feature Specs](https://kiro.dev/docs/specs/feature-specs/) は「For well-understood features where you trust Kiro's output, Quick Spec runs all three phases automatically without approval gates between them」と説明しています。

> 📝 **旧記述の訂正（2026-08-16）**: 本ページは以前「3 つのタイプ（Build a Feature／Fix a Bug／Quick Spec）」としていましたが、公式は「2 タイプ（Feature Specs／Bugfix Specs）＋ Quick Spec という軽量変種」という構造で説明しています。上記は現行公式に基づき修正しています。

---

## ポータビリティ（CLI と IDE で共有）

`.kiro/specs/` は **すべての Kiro サーフェス（IDE / CLI / Web）で共有**され、**同一フォーマット**です。そのため、**CLI で始めた spec を IDE で続ける**、あるいはその逆もできます。

```
プロジェクト/
└── .kiro/
    └── specs/
        └── add-user-auth/
            ├── requirements.md
            ├── design.md
            └── tasks.md
```

---

## Spec agent と権限・Hooks・MCP

Spec agent は**標準のエージェント**なので、v3 の権限（`permissions.yaml`）・Hooks（`.kiro/hooks/*.json`）・MCP 設定が**同様に適用**されます。たとえば Hooks には spec タスク実行の前後で発火する **`PreTaskExec` / `PostTaskExec`**（3.0 新規トリガ）があり、タスク実行にガードレールを差し込めます（→ [09. v3 概要](README.md) の Hooks 節、[公式 Hooks](https://kiro.dev/docs/hooks/)）。

---

## AI-DLC（`07_aidlc`）との違い

本サイトには既に [07_aidlc/](../07_aidlc/README.md) として **AI-DLC（AWS Labs の OSS 方法論）** の解説があります。v3 の **Kiro 純正 Spec agent** とは**別物**なので、混同しないよう違いを整理します。

| 観点 | Kiro Spec（v3・本セクション） | AI-DLC（[07_aidlc](../07_aidlc/README.md)） |
|------|------------------------------|---------------------------------------------|
| 提供元 | **Kiro 純正**（組み込みエージェント） | **AWS Labs OSS**（MIT-0） |
| 実体 | エンジン内蔵の Spec agent ＋ `/spec` コマンド | Markdown の指示書群（Steering Files） |
| 配置 | `.kiro/specs/` | `.kiro/steering/` |
| 位置付け | v3 のコア機能 | Kiro CLI で使える「選択肢」の 1 つ。Spec agent 上でも併用可能 |

> どちらも「AI にすぐコードを書かせず、要件・設計を経てから実装する」という思想は共通します。AI-DLC は**ツール非依存の方法論**、Kiro Spec は**v3 エンジンに統合された純正機能**、という違いがあります。

---

## 関連リンク

### 本セクション内
- [09. Kiro CLI v3（Early Access）概要](README.md)
- [02. Kiro IDE 版との比較](02_kiro-ide-vs-cli.md)

### 本サイトの関連文書
- [07_aidlc/](../07_aidlc/README.md) — AI-DLC（AWS Labs OSS 方法論）
- [01_features/03. Plan Agent](../01_features/03_PlanAgent.md) — v2 系の計画立案エージェント（参考）
- [02_update/01_changelog.md](../02_update/01_changelog.md) — v2.8.0 / v2.8.1

### 公式情報源
- [Spec-driven development（機能自体）](https://kiro.dev/docs/specs/)
- [Feature Specs](https://kiro.dev/docs/specs/feature-specs/)
- [Kiro CLI v3 概要](https://kiro.dev/docs/cli/v3/)

---

**最終更新**: 2026-08-16（CLI逐次実行の記述・specタイプ数・生成ファイル名を一次情報で再確認・訂正）
**対象バージョン**: Kiro CLI v3（Early Access）— v2.8.x ＋ `--v3` で提供。3.0.0 GA は未リリース。
