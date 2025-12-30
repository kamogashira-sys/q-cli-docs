# デプロイメント・環境構築ガイド

## 概要

Kiro CLI の環境構築とデプロイメントに関するガイド集です。

## 📚 ドキュメント一覧

### [01_aws-samples-code-server.md](01_aws-samples-code-server.md)
AWS Samples の AI Agent Development Code Server を使用した、EC2 上での Kiro CLI 開発環境構築ガイドです。

- **対象**: Kiro CLI の開発環境をクラウド上に構築したい方
- **内容**: ブラウザベース VS Code、事前設定済み開発ツール、セキュリティ機能
- **特徴**: ワンクリックデプロイ、Amazon Bedrock Agent Core 対応

### [02_multiuser-code-server-investigation.md](02_multiuser-code-server-investigation.md)
code-server のマルチユーザー対応について、ポート競合問題と解決策を調査した報告書です。

- **対象**: 複数ユーザーでの code-server 利用を検討している方
- **内容**: ポート競合問題、4つの解決策アプローチ、コスト影響分析
- **特徴**: 実装優先度マトリックス、段階的アクションプラン

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2025-12-30 | code-server マルチユーザー対応調査報告書追加 |
| 2025-12-30 | AWS Samples Code Server ガイド追加 |
