# セキュリティガイド

**最終更新**: 2025-10-18

---

## 📋 このセクションについて

Amazon Q Developer CLIを安全に使用するためのセキュリティ情報を提供します。

---

## 📚 ドキュメント一覧

### 1. [セキュリティ概要](01_security-overview.md)
- AWS責任共有モデル
- 主要なセキュリティトピック
- セキュリティベストプラクティス
- セキュリティチェックリスト

### 2. [データプライバシーガイド](02_data-privacy.md)
- プラン別のデータ使用
- サービス改善に使用されるデータ
- オプトアウト方法
- プライバシー保護のベストプラクティス

---

## 🎯 クイックスタート

### 初めての方へ

1. **[セキュリティ概要](01_security-overview.md)** を読む（10分）
2. **プラン選択**を検討（Free vs Pro/Enterprise）
3. **[データプライバシーガイド](02_data-privacy.md)** で設定方法を確認（5分）
4. **[テレメトリー設定](../03_configuration/06_telemetry.md)** を適用（5分）

---

## 🔒 重要なセキュリティ設定

### 機密情報を扱う環境

```bash
# ファイルアクセス制限
q chat --untrust-fs-read

# AWS API制限
Amazon Q> /tools untrust use_aws

# テレメトリー無効化
export Q_TELEMETRY_ENABLED=false
```

---

## 🔗 関連ドキュメント

- [テレメトリー設定](../03_configuration/06_telemetry.md)
- [Agent設定](../03_configuration/04_agent-configuration.md)
- [環境変数](../03_configuration/05_environment-variables.md)
