# Kiro CLI公式サイト構造とナビゲーション

**出典**: [Kiro CLI公式サイト](https://kiro.dev/cli/) - 公式ウェブサイト

## 概要

Kiro CLI公式サイト（https://kiro.dev/cli/）の画面遷移とページ構成について詳細に解説します。Kiro CLIは、ターミナルでのプロンプトからコード、デプロイまでの流れを提供するAI駆動の開発ツールです。

## 📋 サイトの主要機能

### 1. CLI機能
- **Interactive Chat**: ターミナルでの自然言語対話
- **Custom Agents**: ワークフロー特化エージェント作成
- **MCP Integration**: 外部ツール・データソース接続
- **Smart Hooks**: インテリジェントな自動化フック
- **Agent Steering**: エージェントのガイダンス設定
- **Auto Complete**: コンテキスト認識型補完

### 2. 料金プラン
- **Free**: $0/月、50クレジット
- **Pro**: $20/月、1,000クレジット
- **Pro+**: $40/月、2,000クレジット
- **Power**: $200/月、10,000クレジット
- **超過分**: $0.04/クレジット

### 3. エンタープライズ機能
- 組織レベルの管理機能（サブスクリプション、アクセス、権限、請求）
- AWS セキュリティ基準準拠
- IP補償
- 各種統合（MCP、ターミナル、CI/CDパイプライン、VS Code拡張）

## 🗂️ サイト構造（詳細）

| レベル | パス | 説明 |
|--------|------|------|
| **ルート** | [https://kiro.dev/](https://kiro.dev/) | |
| ├── | **CLI** [(/cli/)](https://kiro.dev/cli/) | ターミナルでのプロンプトからコード、デプロイまでの流れを紹介。カスタムエージェント、高度なコンテキスト管理、MCP統合などの主要機能を説明 |
| │　├── | Interactive Chat [(/docs/cli/chat/)](https://kiro.dev/docs/cli/chat/) | ターミナルでの自然言語対話機能 |
| │　├── | Custom Agents [(/docs/cli/custom-agents/)](https://kiro.dev/docs/cli/custom-agents/) | ワークフロー特化エージェント作成 |
| │　├── | MCP Integration [(/docs/cli/mcp/)](https://kiro.dev/docs/cli/mcp/) | 外部ツール・データソース接続 |
| │　├── | Smart Hooks [(/docs/cli/hooks/)](https://kiro.dev/docs/cli/hooks/) | インテリジェントな自動化フック |
| │　├── | Agent Steering [(/docs/cli/steering/)](https://kiro.dev/docs/cli/steering/) | エージェントのガイダンス設定 |
| │　├── | Auto Complete [(/docs/cli/autocomplete/)](https://kiro.dev/docs/cli/autocomplete/) | コンテキスト認識型補完 |
| │　└── | Installation [(/docs/cli/installation/)](https://kiro.dev/docs/cli/installation/) | CLIインストール手順 |
| ├── | **Powers** [(/powers/)](https://kiro.dev/powers/) | Kiroの特殊機能 |
| ├── | **Autonomous agent** [(/autonomous-agent/)](https://kiro.dev/autonomous-agent/) | 自律エージェント機能 |
| ├── | **Enterprise** [(/enterprise/)](https://kiro.dev/enterprise/) | 企業向け機能とソリューション。組織レベルの管理機能、AWS セキュリティ基準、IP補償、各種統合 |
| ├── | **Pricing** [(/pricing/)](https://kiro.dev/pricing/) | 料金体系とプラン比較。Free($0)、Pro($20)、Pro+($40)、Power($200)、超過分$0.04/クレジット |
| ├── | **Docs** [(/docs/cli/)](https://kiro.dev/docs/cli/) | CLI専用技術ドキュメント |
| │　├── | **Getting Started** | |
| │　│　└── | Installation [(/docs/cli/installation/)](https://kiro.dev/docs/cli/installation/) | CLIインストール手順 |
| │　├── | **Core Capabilities** | |
| │　│　├── | Interactive Chat [(/docs/cli/chat/)](https://kiro.dev/docs/cli/chat/) | ターミナルでのAI対話機能 |
| │　│　├── | Custom Agents [(/docs/cli/custom-agents/)](https://kiro.dev/docs/cli/custom-agents/) | ワークフロー特化エージェント |
| │　│　├── | Smart Hooks [(/docs/cli/hooks/)](https://kiro.dev/docs/cli/hooks/) | インテリジェントな自動化フック |
| │　│　├── | Agent Steering [(/docs/cli/steering/)](https://kiro.dev/docs/cli/steering/) | エージェントのガイダンス設定 |
| │　│　├── | MCP Integration [(/docs/cli/mcp/)](https://kiro.dev/docs/cli/mcp/) | 外部ツール・データソース接続 |
| │　│　├── | Auto Complete [(/docs/cli/autocomplete/)](https://kiro.dev/docs/cli/autocomplete/) | コンテキスト認識型補完 |
| │　│　└── | Privacy First [(/docs/privacy-and-security/)](https://kiro.dev/docs/privacy-and-security/) | プライバシー・セキュリティ |
| ├── | **Resources** | |
| │　├── | Blog [(/blog/)](https://kiro.dev/blog/) | 技術ブログ |
| │　├── | Changelog [(/changelog/)](https://kiro.dev/changelog/) | バージョン履歴 |
| │　├── | FAQs [(/faq/)](https://kiro.dev/faq/) | よくある質問 |
| │　├── | Report a bug [(GitHub Issues)](https://github.com/kirodotdev/Kiro/issues/new/choose) | バグ報告 |
| │　├── | Suggest an idea [(GitHub Issues)](https://github.com/kirodotdev/Kiro/issues/new?template=feature_request.yml) | 機能提案 |
| │　└── | Billing support [(AWS Support)](https://support.aws.amazon.com/#/contacts/kiro) | 請求サポート |
| ├── | **Downloads** [(/downloads/)](https://kiro.dev/downloads/) | インストーラーダウンロード |
| └── | **Sign In** [(https://app.kiro.dev)](https://app.kiro.dev) | アプリケーションログイン |

## 🎯 主要なユースケース

### CLI活用シーン
- **Interactive Development**: ターミナルでの直接的なAI支援
- **Custom Automation**: 特化エージェントによるワークフロー自動化
- **Team Standardization**: チームレベルのベストプラクティス適用
- **External Integrations**: MCPサーバーによるツール・サービス連携
- **Intelligent Assistance**: コンテキスト認識型の提案と自動補完
- **Workflow Optimization**: スマートフックによる反復タスク自動化

### エンタープライズ活用
- **Custom Automation**: 特化エージェントによるワークフロー自動化
- **Team Standardization**: チームレベルのベストプラクティス適用
- **Quality Assurance**: ベストプラクティス強制とコード品質向上
- **Security Compliance**: AWS セキュリティ基準準拠
- **Integration Flexibility**: 既存ツールチェーンとの統合

## 🔗 関連リンク

- **[Kiro CLI公式サイト](https://kiro.dev/cli/)**
- **[Kiro CLI専用ドキュメント](https://kiro.dev/docs/cli/)**
- **[Kiro GitHub リポジトリ](https://github.com/kirodotdev/Kiro)**
- **[Kiro Discord コミュニティ](https://discord.gg/kirodotdev)**
- **[Kiro公式ブログ](https://kiro.dev/blog/)**

---

**最終更新**: 2025-12-31
