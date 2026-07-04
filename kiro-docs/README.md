# 猫でもわかるkiro-cli アップデート情報

## 📢 はじめに

このドキュメントでは、Kiro CLI（旧Amazon Q Developer CLI）の主要機能アップデートについて詳しく解説します。Amazon Q Developer CLIからKiro CLIへの移行に伴い、多くの革新的な機能が追加されました。

## 概要

Kiro CLI（旧Amazon Q Developer CLI）の最新情報とアップデートを追跡・整理するプロジェクトです。

## 情報源

- **公式サイト**: https://kiro.dev/cli/
- **GitHub**: https://github.com/kirodotdev/Kiro
- **移行情報**: Amazon Q Developer CLI v1.19.7（2025-11-17）から移行
- **AWSジャパンContributor(小西さん)**: https://zenn.dev/konippi
- **Classmethod(鈴木さん)**: https://dev.classmethod.jp/author/suzuki-ryo/
- **AWS Serverless Hero(吉田さん)**: https://yoshidashingo.com/
- **AWS DevTools Hero(後藤さん)**: https://github.com/go-to-k

## ディレクトリ構成

```
kiro-docs/
├── 00_information/   # 基本情報・公式サイト情報
├── 01_features/      # 機能詳細ガイド（31機能）
├── 02_update/        # アップデート情報
├── 03_deployment/    # デプロイメント・環境構築
├── 04_reference/     # リファレンス（Settings/Slash/CLI/Tools）
├── 05_meta/          # 保守手順書（※ローカル管理・GitHub 非公開）
├── 06_embedded-docs/ # 公式 OSS リポジトリ文書の複製（※ローカル管理・GitHub 非公開）
├── 07_aidlc/         # AI-DLC（Kiro CLI で実践する選択肢）
├── 08_cdk-skills/    # cdk-skills（CDK 開発支援 Skills 集）
└── 09_v3/            # Kiro CLI v3（Early Access）— 仕様駆動開発・IDE比較 🆕
```

> **注**: `05_meta/`（本サイトの保守手順書）と `06_embedded-docs/`（公式リポジトリ文書の逐語複製）は `.gitignore` によるローカル管理で、GitHub 上には表示されません。

**クイックリンク**: [00_information/](00_information/) | [01_features/](01_features/) | [02_update/](02_update/) | [03_deployment/](03_deployment/) | [04_reference/](04_reference/) | [07_aidlc/](07_aidlc/) | [08_cdk-skills/](08_cdk-skills/) | [09_v3/](09_v3/) 🆕

## 📚 主要ドキュメント

### [00_information/ - 基本情報・公式サイト情報](00_information/README.md)
Kiro CLI の基本情報と公式サイトの構造について説明したドキュメント集です。

- **[公式サイト構造](00_information/01_official-site-structure.md)** - Kiro CLI公式サイトの画面遷移とページ構成

### [01_features/ - 機能詳細ガイド](01_features/README.md)
Kiro CLIの主要機能（**31 機能**）について詳細に解説したドキュメント集です。

📖 **[→ 機能一覧（カテゴリ別ナビゲーション・各機能の概要・バージョン情報）](01_features/README.md)**

カテゴリ：🤖 エージェント・自動化 / 📁 コンテキスト・知識管理 / 📂 ファイル操作・編集 / 🧠 コード理解・LSP / 💾 セッション・履歴管理 / 🎨 UI/UX・補完 / 🔒 セキュリティ・権限 / 🔌 統合（IDE/MCP/CI/CD/認証） / 💰 使用量・課金

### [02_update/ - アップデート情報](02_update/README.md)
Kiro CLIのバージョン履歴とアップデート情報を管理しています。

- **[変更履歴](02_update/01_changelog.md)** - 全バージョンの詳細な変更内容

### [03_deployment/ - デプロイメント・環境構築](03_deployment/README.md)
Kiro CLI の環境構築とデプロイメントに関するガイド集です。

- **[公式インストール手順](03_deployment/03_official-installation.md)** 🆕 - 公式 OS 別インストール（macOS/Windows 11/Linux/Ubuntu/Proxy/デバッグ）
- **[AWS Samples Code Server](03_deployment/01_aws-samples-code-server.md)** - EC2上でのKiro CLI開発環境構築

### [04_reference/ - リファレンス](04_reference/README.md) 🆕
Kiro CLI の設定・コマンド・ツールの **辞書的リファレンス**（公式ページ準拠）。

| ファイル | 内容 |
|--------|------|
| [01. Settings](04_reference/01_settings.md) | 全設定項目（公式8カテゴリ）と環境変数 |
| [02. Slash Commands](04_reference/02_slash-commands.md) | 全スラッシュコマンド40種＋キーボードショートカット |
| [03. CLI Commands](04_reference/03_cli-commands.md) | `kiro-cli` コマンド全16種、グローバル引数、セッション管理 |
| [04. Built-in Tools](04_reference/04_built-in-tools.md) | 組み込みツール18種（read/glob/grep/write/shell/aws/web_*/code/tool_search/subagent 他） |

### [09_v3/ - Kiro CLI v3（Early Access）](09_v3/README.md) 🆕
Kiro CLI v3（`kiro-cli --v3`）の概要・仕様駆動開発・Kiro IDE 版との比較をまとめた専用セクションです。

- **[v3 概要](09_v3/README.md)** - 統一エンジン・4本柱（Spec / permissions.yaml / Hooks / タグ Agent設定）・Breaking changes・Known gaps
- **[仕様駆動開発](09_v3/01_spec-driven-development.md)** - `/spec` を使った CLI での実践（AI-DLC との違いも整理）
- **[Kiro IDE 版との比較](09_v3/02_kiro-ide-vs-cli.md)** - 同様にできること／IDE が優位なこと／CLI ならではのこと

---

## 🌟 注目の新機能：Agent Toolkit for AWS（2026-05 GA）

> **AWS が公式に発表した、AI コーディングエージェントが AWS で安全・効果的に動作するためのツールキット。**
>
> 公式が対応エージェントとして明示しているのは：**Claude Code / Cursor / Codex / Kiro / Windsurf / Cline**（[User Guide](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/what-is-agent-toolkit.html#what-can-i-do-agent-toolkit) より）。さらに [AWS News Blog（2026-05-06）](https://aws.amazon.com/blogs/aws/the-aws-mcp-server-is-now-generally-available) では **「Kiro CLI、Kiro」** が両方明記されています。

### 📖 詳細ガイド: **[26. Agent Toolkit for AWS（AWS 公式エージェント統合ツールキット）](01_features/26_AgentToolkitForAWS.md)** ⭐

**Agent Toolkit for AWS** は、AI コーディングエージェントが AWS サービス上で **本番グレード** の作業を行うための公式ツールキットです。本サイト（Kiro CLI 専門）では **Kiro CLI からの利用** を主眼に解説します。設定ディレクトリ `~/.kiro/` は Kiro（IDE）と Kiro CLI で共通のため、設定方法も共通です。

主な特徴と提供価値（公式 MCP Server / IAM 権限分離 / 可観測性 / サンドボックス Python / リアルタイムドキュメント等）、4 コンポーネント、主要 4 ツール、Kiro CLI 統合手順、IAM コンテキストキーと権限分離、AWS Labs MCP との比較・移行、ユースケース 5 件、トラブルシューティング、公式情報源は **[詳細ガイド](01_features/26_AgentToolkitForAWS.md)** をご覧ください。

---

## 🚀 注目のオープンソース：AI-DLC Adaptive Workflows（2025-11 OSS 化）

> **AWS Labs が公開する AI 駆動開発のための Adaptive Workflows 方法論。**
>
> Kiro CLI とは独立した OSS（**MIT-0** ライセンス）ですが、**v0.1.0（2026-01-22）から Kiro CLI を公式サポート** しており、Steering Files として配置することで Kiro CLI から利用できます。

### 📖 詳細ガイド: **[07. AI-DLC（Kiro CLI で実践する選択肢）](07_aidlc/README.md)** ⭐

**AI-DLC（AI-Driven Development Life Cycle）** は、AI モデルへの「指示書」として Markdown ファイル群（26 ファイル）で構成される **適応型ワークフロー方法論** です。50 年分の SDLC 知見を AI 駆動の文脈で再構成し、**3 フェーズ（Inception / Construction / Operations）× 14 ステージ** で開発プロセスを規律化します。

主な特徴（適応型ワークフロー / Human in the Loop / 完全な監査証跡 / IDE 非依存 / MIT-0 / 二層構造）、中核思想と設計の柱、26 ファイル構造、3 フェーズ詳細、6 つの仕組み（Adaptive Depth / 承認ゲート / 質問ファイル方式 / Overconfidence Prevention / Smart Context Loading / 監査証跡）、既存手法との比較、Extensions、Kiro CLI 導入手順、ユースケース、公式情報源は **[詳細ガイド](07_aidlc/README.md)** をご覧ください。

---

## 🛠️ 注目のコミュニティ Skill：cdk-skills（CDK 開発支援）

> **AWS DevTools Hero（go-to-k 後藤さん）が公開する CDK 開発支援 Skills 集（MIT）。**
>
> AI コーディングエージェントが AWS CDK の単体テストの「**どの場面でどれを書くべきか / 書かなくて良いか**」を判断できるようにする、Skill ファイル形式の知識集です。Kiro CLI v1.26.0+ の **Skills 自動読み込み機能**（[07. Skills](01_features/07_Skills.md)）で利用できます。

### 📖 詳細ガイド: **[08. cdk-skills（CDK 開発支援 Skills 集）](08_cdk-skills/README.md)** ⭐

**cdk-skills** は、AWS DevTools Hero（go-to-k 後藤さん）が公開する CDK 開発支援 Skills 集です。AI コーディングエージェントが AWS CDK 単体テストの「**どの場面でどれを書くべきか / 書かなくて良いか**」を判断できるようにする、Skill ファイル形式の知識集です。

主な特徴（判断フロー Skill 化 / アンチパターン明示 / 最小構成 / パフォーマンス Tips / 機能フラグ統一 / MIT）、3 種類のテスト早見表、判断フロー、Fine-grained assertions の 5 つの使い所、落とし穴詳細、テスト環境セットアップ Tips、Kiro CLI への導入手順（gh skill / npx skills / 手動配置）、コピペ用 test-template.ts 雛形、ユースケース、公式情報源は **[詳細ガイド](08_cdk-skills/README.md)** をご覧ください。

---

## 🔗 関連ブログ記事

### Kiro CLI公式発表
- **[Introducing Kiro CLI](https://aws.amazon.com/jp/blogs/news/introducing-kiro-cli/)**
  - Kiro CLIの公式発表記事
  - 基本概念と主要機能の紹介
  - Amazon Q Developer CLIからの進化について

### 移行ガイド
- **[Kiroweeeeeeek in Japan Day 6: Amazon Q Developer CLI to Kiro CLI](https://aws.amazon.com/jp/blogs/news/kiroweeeeeeek-in-japan-day-6-amazon-q-developer-cli-to-kiro-cli/)**
  - Amazon Q Developer CLIからKiro CLIへの移行ガイド
  - 日本での導入事例とベストプラクティス
  - 移行時の注意点と推奨事項

### エンタープライズ運用
- **[AWS 請求統合の Kiro に IAM Identity Center ユーザーでサインインする手順（2026年5月版）](https://dev.classmethod.jp/articles/kiro-iam-identity-center-user-signin-setup-202605/)**
  - IAM Identity Center ビルトインユーザーでのサインイン手順
  - Kiro IDE / CLI / Web それぞれのサインイン方法
  - エンタープライズ環境での初回セットアップ
- **[Kiro のプロンプトログを解析して業務日報のたたき台を作ってみた](https://dev.classmethod.jp/articles/kiro-prompt-log-analysis/)**
  - プロンプトログ機能（S3保存）の有効化とログ構造解析
  - jqでの前処理・集計、Amazon Bedrockでの業務日報生成
  - エンタープライズ向け監査・分析活用例

## 更新方針

1. 公式サイトの定期チェック
2. GitHub Issuesの監視
3. 機能変更の分析・記録
