# 猫でもわかるkiro-cli アップデート情報

## 📢 はじめに

このドキュメントでは、Kiro CLI（旧Amazon Q Developer CLI）の主要機能アップデートについて詳しく解説します。Amazon Q Developer CLIからKiro CLIへの移行に伴い、多くの革新的な機能が追加されました。

## 🔗 関連AWS公式ブログ記事

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

## 概要

Kiro CLI（旧Amazon Q Developer CLI）の最新情報とアップデートを追跡・整理するプロジェクトです。

## 情報源

- **公式サイト**: https://kiro.dev/cli/
- **GitHub**: https://github.com/kirodotdev/Kiro
- **移行情報**: Amazon Q Developer CLI v1.19.7（2025-11-17）から移行
- **AWSジャパンContributor(小西さん)**: https://zenn.dev/konippi

## ディレクトリ構成

```
kiro-docs/
├── 00_information/   # 基本情報・公式サイト情報
├── 01_features/      # 機能詳細ガイド
├── 02_update/        # アップデート情報
└── 03_deployment/    # デプロイメント・環境構築
```

## 📚 主要ドキュメント

### [00_information/ - 基本情報・公式サイト情報](00_information/README.md)
Kiro CLI の基本情報と公式サイトの構造について説明したドキュメント集です。

- **[公式サイト構造](00_information/01_official-site-structure.md)** - Kiro CLI公式サイトの画面遷移とページ構成

### [01_features/ - 機能詳細ガイド](01_features/README.md)
Kiro CLIの主要機能について詳細に解説したドキュメント集です。

| 機能 | 説明 | バージョン |
|------|------|-----------|
| **[LSP統合機能](01_features/01_LSP.md)** | Code Intelligence機能の詳細 | v1.22.0 |
| **[サブエージェント機能](01_features/02_Subagents.md)** | 並列タスク実行機能 | v1.23.0 |
| **[Planエージェント機能](01_features/03_PlanAgent.md)** | 構造化実装計画機能 | v1.23.0 |
| **[マルチセッション機能](01_features/04_MultiSession.md)** | セッション管理機能 | v1.23.0 |
| **[Grep/Globツール](01_features/05_GrepGlob.md)** | 高速ファイル検索機能 | v1.23.0 |
| **[/usage コマンド](01_features/06_UsageCommand.md)** | 使用量・契約プラン確認機能 | - |
| **[Skills機能](01_features/07_Skills.md)** | 段階的コンテキストロード機能 | v1.24.0 |
| **[Custom Diff Tools機能](01_features/08_CustomDiffTools.md)** | 外部Diffツール統合 | v1.24.0 |
| **[AST Pattern Tools機能](01_features/09_ASTPatternTools.md)** | 構文木ベースのコード検索・変換 | v1.24.0 |
| **[Conversation Compaction機能](01_features/10_ConversationCompaction.md)** | 会話履歴圧縮機能 | v1.24.0 |
| **[Granular URL Permissions機能](01_features/11_URLPermissions.md)** | URL権限細粒度制御 | v1.24.0 |
| **[Remote Authentication機能](01_features/12_RemoteAuth.md)** | リモート認証対応 | v1.24.0 |

### [02_update/ - アップデート情報](02_update/README.md)
Kiro CLIのバージョン履歴とアップデート情報を管理しています。

- **[変更履歴](02_update/01_changelog.md)** - 全バージョンの詳細な変更内容

### [03_deployment/ - デプロイメント・環境構築](03_deployment/README.md)
Kiro CLI の環境構築とデプロイメントに関するガイド集です。

- **[AWS Samples Code Server](03_deployment/01_aws-samples-code-server.md)** - EC2上でのKiro CLI開発環境構築

## 更新方針

1. 公式サイトの定期チェック
2. GitHub Issuesの監視
3. 機能変更の分析・記録
