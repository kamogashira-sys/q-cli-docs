[ホーム](../README.md) > [ユーザーガイド](README.md)

---

# For Users - ユーザー向け

Amazon Q CLIを使う方向けのドキュメントです。

## 📚 このセクションについて

Q CLIのインストールから高度な活用方法まで、ユーザーが必要とするすべての情報を提供します。

## 🎯 対象読者

- Q CLIを初めて使う方
- Q CLIの設定をカスタマイズしたい方
- 各機能の使い方を学びたい方
- トラブルシューティングが必要な方
- エンタープライズ環境で導入したい方

## 📖 サブセクション

| セクション | 文書数 | 内容 |
|-----------|--------|------|
| [Getting Started](01_getting-started/) | 5 | インストールと基本的な使い方 |
| [Features](02_features/) | 8 | 各機能の使い方 |
| [Configuration](03_configuration/) | 9 | 設定方法の詳細 |
| [Best Practices](04_best-practices/) | 7 | 推奨される使い方（Agent Hooks比較含む） |
| [Deployment](05_deployment/) | 4 | エンタープライズ導入 |
| [Troubleshooting](06_troubleshooting/) | 3 | 問題解決 |
| [Reference](07_reference/) | 10 | リファレンス情報 |
| [Guides](08_guides/) | 10 | 包括的なガイド（コンテキスト管理、ワークフロー自動化） |
| [Security](09_security/) | 7 | セキュリティとプライバシー |
| [File Specifications](10_file-specifications/) | 7 | ファイルフォーマット仕様 |

## 🚀 推奨学習順序

### 初めての方
1. [Getting Started](01_getting-started/) - インストールと基本操作
2. [Configuration](03_configuration/) - 基本的な設定
3. [Features](02_features/) - 各機能の理解
4. **[Guides - コンテキスト管理](08_guides/)** - 応答品質を最大化【重要】
5. [Security](09_security/) - セキュリティとプライバシー【重要】

### Q CLIの応答品質を最大化したい方【最重要】
**[コンテキスト管理完全ガイド](08_guides/)** を体系的に学習してください：
- 第1章: コンテキストの本質（15分）
- 第3章: 効果と特徴（15分）
- 第5章: 実践ガイド（30分）

### 技術的な詳細を知りたい方
1. [Architecture](../02_for-developers/02_architecture/README.md) - アーキテクチャ
2. [File Specifications](10_file-specifications/) - ファイル仕様
3. [Reference](07_reference/) - リファレンス情報

### セキュリティを重視する方【重要】
1. [Security - セキュリティ概要](09_security/01_security-overview.md) - AWS責任共有モデル、主要トピック
2. [Security - データプライバシー](09_security/02_data-privacy.md) - データの取り扱いとオプトアウト
3. [Configuration](03_configuration/) - セキュアな設定
4. [Best Practices - セキュリティ](04_best-practices/02_security.md) - セキュリティのベストプラクティス

### 設定をカスタマイズしたい方
1. [Configuration](03_configuration/) - 詳細な設定方法
2. [Best Practices](04_best-practices/) - 推奨設定
3. [Reference](07_reference/) - 設定項目リファレンス
4. **[Guides - コンテキスト管理](08_guides/)** - 高度な最適化

### ワークフローを自動化したい方【NEW】
1. **[Guides - ワークフロー自動化](08_guides/09_workflow-automation.md)** - Agent Hooksの実践ガイド
2. [Best Practices - Agent Hooks比較](04_best-practices/05_agent-hooks-comparison.md) - Kiroとの比較
3. [Configuration - Agent設定](03_configuration/03_agent-configuration.md) - Hooks設定の技術仕様

### 問題を解決したい方
1. [Guides - トラブルシューティング編](08_guides/06_troubleshooting.md) - コンテキスト関連の問題
2. [Troubleshooting](06_troubleshooting/) - よくある問題と解決方法
3. [Reference](07_reference/) - 詳細なリファレンス

---

最終更新: 2025-10-19
