# Developer Guide - 開発者向けガイド

**最終更新**: 2025-10-11

---

## 📋 このセクションについて

Amazon Q CLIの内部構造を理解したい方、コントリビューションしたい方向けのガイドです。

このガイドでは、Q CLIの内部アーキテクチャ、ソースコード構造、開発環境の構築方法、コントリビューション方法について詳しく説明します。Q CLIはRustで実装されており、非同期処理、MCP統合、AWS SDK統合など、モダンな技術スタックを採用しています。

### 対象読者
- Q CLIの内部実装を理解したい開発者
- Q CLIにコントリビューションしたい方
- カスタムMCPサーバーを開発したい方
- Q CLIをベースにした独自ツールを開発したい方

---

## 🚀 推奨学習順序

### 初めての方
1. **[ソースコード構造](architecture/source-code-structure.md)** - コード全体像を把握（15分）
2. **[コード統計](architecture/code-statistics.md)** - プロジェクト規模を理解（5分）
3. **[開発環境構築](contributing/development-setup.md)** - 開発環境をセットアップ（30分）

### コントリビューターの方
1. **[開発環境構築](contributing/development-setup.md)** - 環境構築（30分）
2. **[コントリビューションガイド](contributing/README.md)** - 貢献方法を学習（15分）
3. **[ソースコード構造](architecture/source-code-structure.md)** - 詳細な構造を理解（15分）
4. **[設定システム詳細](architecture/configuration-system.md)** - 設定システムの実装を理解（20分）

---

## 📚 前提知識

### 必須
- **Rust プログラミング言語**: Q CLIはRustで実装されています
  - 所有権、借用、ライフタイムの理解
  - 非同期プログラミング（async/await）
  - エラーハンドリング（Result型）
- **Git/GitHub**: バージョン管理とコラボレーション
  - ブランチ戦略
  - プルリクエストのワークフロー
- **コマンドライン操作**: ターミナルでの基本操作

### 推奨
- **AWS サービスの基礎知識**: Q CLIはAWSサービスと統合されています
  - AWS SDK for Rust
  - AWS認証（AWS Builder ID、IAM）
- **MCP (Model Context Protocol)**: 外部ツールとの統合
  - MCPサーバーの実装
  - stdio/HTTP通信
- **非同期プログラミング**: Tokioランタイムの理解
  - 非同期I/O
  - 並行処理

---

## 📚 サブセクション

| サブセクション | ステータス | 対象ユーザー | 内容 |
|--------------|-----------|-------------|------|
| [アーキテクチャ](architecture/) | 一部完成 | 開発者 | Amazon Q CLIの内部構造 |
| [コントリビューション](contributing/) | 完成 | コントリビューター | Amazon Q CLIへの貢献方法 |

---

## 🔗 関連リソース

### 公式リポジトリ
- [amazon-q-developer-cli](https://github.com/aws/amazon-q-developer-cli) - メインリポジトリ
- [Issues](https://github.com/aws/amazon-q-developer-cli/issues) - バグ報告・機能要望
- [Pull Requests](https://github.com/aws/amazon-q-developer-cli/pulls) - コントリビューション

### 技術スタック
- [Rust](https://www.rust-lang.org/) - プログラミング言語
- [Tokio](https://tokio.rs/) - 非同期ランタイム
- [AWS SDK for Rust](https://aws.amazon.com/sdk-for-rust/) - AWS統合
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol

---

**作成日**: 2025-10-11  
**最終更新日**: 2025-10-11
