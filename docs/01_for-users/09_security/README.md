[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [セキュリティガイド](README.md)

---

# セキュリティガイド

**最終更新**: 2025-10-18

---

## 📋 このセクションについて

Amazon Q Developer CLIを安全に使用するためのセキュリティ情報を提供します。

---

## 🚀 クイックアクセス

### よく使う情報

- **[クイックリファレンス](../07_reference/08_quick-reference.md)** ⭐ - よく使うコマンドと設定の早見表
- **[トピック別インデックス](../07_reference/09_topic-index.md)** ⭐ - やりたいことから適切なドキュメントを発見

---

## 📚 このセクションのドキュメント

### 学習順序（推奨）

1. **[セキュリティ概要](01_security-overview.md)** ← まずここから！
   - 所要時間: 15分
   - 対象: 初級〜中級
   - 内容: AWS責任共有モデル、主要セキュリティトピック、環境別推奨設定

2. **[データプライバシー](02_data-privacy.md)**
   - 所要時間: 10分
   - 対象: 初級〜中級
   - 内容: Free vs Pro/Enterpriseプラン、サービス改善データ使用、オプトアウト

3. **[ファイルアクセス制御](03_file-access-control.md)**
   - 所要時間: 20分
   - 対象: 中級
   - 内容: fs_readツール制御、機密ファイル保護、環境別設定

4. **[AWS API制御](04_aws-api-control.md)**
   - 所要時間: 20分
   - 対象: 中級
   - 内容: use_awsツール制御、IAMポリシー制限、コスト管理

5. **[認証情報管理](05_credentials-management.md)**
   - 所要時間: 20分
   - 対象: 中級
   - 内容: AWS Builder ID、IAM Identity Center、ベストプラクティス

6. **[trust-all安全使用](06_trust-all-safety.md)**
   - 所要時間: 15分
   - 対象: 中級〜上級
   - 内容: trust-allの危険性、安全な使用方法、チェックリスト

### トピック別

#### 基本
- [セキュリティ概要](01_security-overview.md) - セキュリティの基本原則
- [データプライバシー](02_data-privacy.md) - プラン別のデータ使用

#### ツール制御
- [ファイルアクセス制御](03_file-access-control.md) - fs_readツールの制御
- [AWS API制御](04_aws-api-control.md) - use_awsツールの制御

#### 認証・権限
- [認証情報管理](05_credentials-management.md) - 認証情報の安全な管理
- [trust-all安全使用](06_trust-all-safety.md) - trust-allの安全な使用

---

## 🎯 クイックスタート

### 初めての方へ

1. **[セキュリティ概要](01_security-overview.md)** を読む（15分）
2. **プラン選択**を検討（Free vs Pro/Enterprise）
3. **[データプライバシーガイド](02_data-privacy.md)** で設定方法を確認（10分）
4. **[テレメトリー設定](../03_configuration/06_telemetry.md)** を適用（5分）

### 機密情報を扱う環境

1. **[ファイルアクセス制御](03_file-access-control.md)** を設定（20分）
2. **[AWS API制御](04_aws-api-control.md)** を設定（20分）
3. **[認証情報管理](05_credentials-management.md)** を確認（20分）

---

## 🔒 重要なセキュリティ設定

### 機密情報を扱う環境

```bash
# ファイルアクセス制限
alias q="q --untrust-fs-read"

# AWS API制限
alias q="q --untrust-use-aws"

# テレメトリー無効化
export Q_TELEMETRY_ENABLED=false
```

### Agent設定での制御

```json
{
  "name": "secure-project",
  "untrustedTools": ["fs_read", "use_aws", "execute_bash"]
}
```

---

## 🔗 関連ドキュメント

### 設定ガイド
- [テレメトリー設定](../03_configuration/06_telemetry.md)
- [Agent設定](../03_configuration/04_agent-configuration.md)
- [環境変数](../03_configuration/05_environment-variables.md)

### エンタープライズ展開
- [エンタープライズ導入ガイド](../05_deployment/01_enterprise-deployment.md)
- [料金プラン比較](../05_deployment/02_pricing-comparison.md)
- [セキュリティチェックリスト](../05_deployment/03_security-checklist.md)

### ベストプラクティス
- [セキュリティベストプラクティス](../04_best-practices/02_security.md)

### その他
- [クイックリファレンス](../quick-reference.md)
- [トピック別インデックス](../topic-index.md)

---

**最終更新**: 2025-10-18  
**対象バージョン**: v1.17.0以降
