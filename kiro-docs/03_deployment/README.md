# デプロイメント・環境構築ガイド

[ホーム](../README.md) > デプロイメント・環境構築

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

### [03_official-installation.md](03_official-installation.md) 🆕
公式の OS 別インストール手順を網羅した辞書的ガイドです（公式ページ準拠）。

- **対象**: Kiro CLI を OS 別に公式手順でインストール・運用する方
- **内容**: macOS / Windows 11 / Linux (AppImage / zip / Ubuntu .deb) / Proxy / アンインストール / デバッグ
- **特徴**: glibc 2.34+ 標準版と musl 版の使い分け、エンタープライズプロキシ対応、`kiro-cli doctor` 自動診断

## 関連リンク

- [04_reference/03_cli-commands.md](../04_reference/03_cli-commands.md) — `kiro-cli` コマンド全16種の辞書
- [04_reference/01_settings.md](../04_reference/01_settings.md) — 全設定項目（`app.disableAutoupdates` 等）
- [01_features/16_v2MajorUpdate.md](../01_features/16_v2MajorUpdate.md) — Windows / Headless Mode

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2026-05-24 | 公式インストール手順 (03_official-installation.md) 追加 |
| 2025-12-30 | code-server マルチユーザー対応調査報告書追加 |
| 2025-12-30 | AWS Samples Code Server ガイド追加 |
