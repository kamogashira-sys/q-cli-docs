[ホーム](../README.md) > [Kiro CLI v3（Early Access）](README.md) > 仕様駆動開発

# 09-01. 仕様駆動開発（Spec-driven development）— CLI での実践

> ⚠️ **Early Access**: 本ページは Kiro CLI v3（`kiro-cli --v3`）の機能を扱います。Early Access のため仕様変更の可能性があります（→ [09. v3 概要](README.md)）。

**出典（一次情報）**:
- [Spec-driven development（公式 CLI specs）](https://kiro.dev/docs/cli/v3/specs/)
- [Kiro CLI v3 概要（公式）](https://kiro.dev/docs/cli/v3/)

---

## 仕様駆動開発とは

**仕様駆動開発（Spec-driven development）** は、いきなりコードを書くのではなく、**「要件 → 設計 → タスク」を順に固めてから実装する**進め方です。Kiro CLI v3 には、この進め方を担う**組み込みの Spec agent** が用意されています。

ねらいは「**計画してから実行する（plan-then-execute）**」こと。あいまいな指示で AI に丸投げするのではなく、**何を作るか（要件）→ どう作るか（設計）→ どの順で作るか（タスク）**を文書として残し、合意してから実装に入ります。生成物はすべてファイルとして残るため、**レビュー・編集・追跡**ができます。

---

## ワークフロー（3 フェーズ＋実行）と生成ファイル

Spec agent のワークフローは **要件・設計・タスクの 3 フェーズ**で計画を固め、その後 **Execution（実行）** へ進みます。**ファイルを生成するのはこの 3 フェーズ**で、各フェーズが `.kiro/specs/<name>/` に 1 つずつ生成します（公式 IDE specs「Three-Phase Workflow」、CLI specs「Each phase produces a file」）。**Execution はフェーズではなく実行段階**で、ファイルを新規生成せず、上記 3 ファイルを更新しながら進みます。フェーズの区切りでユーザーが内容を編集できます。

| ステップ | 内容 | 生成ファイル |
|---------|------|-------------|
| **Requirements**（フェーズ 1・要件） | 受入基準を含む要件を定義 | `.kiro/specs/<name>/requirements.md` |
| **Design**（フェーズ 2・設計） | アーキテクチャ・設計を記述 | `.kiro/specs/<name>/design.md` |
| **Tasks**（フェーズ 3・タスク） | 依存関係を追跡した順序付き実装計画 | `.kiro/specs/<name>/tasks.md` |
| **Execution**（実行段階・※フェーズではない） | タスクを**逐次**実行し、各ステップ間で検証 | （新規生成なし。上記ファイルを更新しながら進行） |

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

# タスクを自律実行（逐次・各タスク間で検証）
> /spec run add-user-auth
```

- **`/spec`**: 既存 spec の一覧・選択。
- **`/spec new <name>`**: 新規作成。要件定義フェーズから始まります。
- **`/spec <name>`**: 既存 spec を再開。
- **`/spec run <name>`**: タスクを**逐次（sequentially）**実行し、**各タスクの間で検証**します。

> 💡 **CLI は逐次実行**: 公式 CLI specs は `/spec run` を「tasks run **sequentially** with verification between steps（各ステップ間で検証しながら逐次実行）」と記載しています。IDE 版の「Run all Tasks」による**並列 wave 実行**との違いは [02. Kiro IDE 版との比較](02_kiro-ide-vs-cli.md) を参照してください。

---

## 3 つのタイプ

spec を始めるとき、目的に応じて 3 タイプから選びます。

| タイプ | 用途 |
|--------|------|
| **Build a Feature** | 新機能の開発（要件 → 設計 → タスクをしっかり固める） |
| **Fix a Bug** | バグ修正向けの軽量フロー |
| **Quick Spec** | 要件の形式化を省く軽量版（素早くタスクへ） |

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

Spec agent は**標準のエージェント**なので、v3 の権限（`permissions.yaml`）・Hooks（`.kiro/hooks/*.json`）・MCP 設定が**同様に適用**されます。たとえば Hooks には spec タスク実行の前後で発火する **`PreTaskExec` / `PostTaskExec`**（3.0 新規トリガ）があり、タスク実行にガードレールを差し込めます（→ [09. v3 概要](README.md) の Hooks 節、[公式 Hooks](https://kiro.dev/docs/cli/v3/hooks/)）。

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
- [Spec-driven development（CLI specs）](https://kiro.dev/docs/cli/v3/specs/)
- [Kiro CLI v3 概要](https://kiro.dev/docs/cli/v3/)

---

**最終更新**: 2026-06-21
**対象バージョン**: Kiro CLI v3（Early Access）— v2.8.x ＋ `--v3` で提供。3.0.0 GA は未リリース。
