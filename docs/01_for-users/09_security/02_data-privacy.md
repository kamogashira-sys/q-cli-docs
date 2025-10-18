# データプライバシーガイド

**最終更新**: 2025-10-18  
**対象**: Amazon Q Developer CLI

---

## 📋 概要

このガイドは、Amazon Q Developer CLIにおけるデータプライバシーとサービス改善のためのデータ使用について説明します。

---

## 🎯 プラン別のデータ使用

### Free vs Pro/Enterpriseプラン

| 項目 | Freeプラン | Pro/Enterpriseプラン |
|------|-----------|---------------------|
| **質問内容** | サービス改善に使用される可能性あり | 使用されない |
| **応答内容** | サービス改善に使用される可能性あり | 使用されない |
| **生成コード** | サービス改善に使用される可能性あり | 使用されない |
| **オプトアウト** | 可能 | 不要（デフォルトで保護） |
| **推奨環境** | 個人開発、学習 | 商用開発、機密情報 |

**出典**: [Amazon Q Developer service improvement](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/service-improvement.html)

---

## 📊 サービス改善に使用されるデータ（Freeプラン）

### 使用されるコンテンツ

**Freeプランで使用される可能性があるデータ**:
- ✅ Amazon Qへの質問
- ✅ Amazon Qの応答
- ✅ 生成されたコード

### 使用目的

- より良い応答の提供
- 一般的な質問への対応改善
- 運用上の問題修正
- デバッグ
- モデルトレーニング

### 使用されないデータ

**Pro/Enterpriseプランのデータ**:
- ❌ サービス改善に使用されない
- ❌ モデルトレーニングに使用されない
- ✅ プライバシーが保護される

---

## 🔒 データ保護の仕組み

### 暗号化

#### 転送中の暗号化

- **プロトコル**: TLS 1.2以上
- **対象**: Amazon Qとユーザー間の全通信
- **自動適用**: 設定不要

#### 保管時の暗号化

| 機能 | 暗号化方式 | カスタマーマネージドキー |
|------|-----------|----------------------|
| チャット（AWSコンソール） | AWS KMS | ✅ 対応 |
| コンソールエラー診断 | AWS KMS | ✅ 対応 |
| カスタマイゼーション | AWS KMS | ✅ 対応 |
| IDE内のAgent | AWS KMS | ✅ 対応 |
| その他 | AWS所有キー | ❌ 非対応 |

**出典**: [Data encryption in Amazon Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/data-encryption.html)

---

## 🚫 オプトアウト方法

### 環境別のオプトアウト

#### 1. AWS Management Console / モバイルアプリ / Webサイト

**方法**: AWS Organizationsでポリシー設定

```json
{
  "services": {
    "amazonq": {
      "opt_out_policy": {
        "@@assign": "optOut"
      }
    }
  }
}
```

**参考**: [AI services opt-out policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_ai-opt-out.html)

---

#### 2. IDE（VS Code、JetBrains等）

**VS Code**:
1. 設定を開く（`Cmd/Ctrl + ,`）
2. "Amazon Q" で検索
3. "Share Content with AWS" のチェックを外す

**JetBrains**:
1. Preferences/Settings → Tools → AWS Toolkit
2. "Share content with AWS to improve Amazon Q" のチェックを外す

---

#### 3. Q CLI（コマンドライン）

**環境変数で設定**:
```bash
# オプトアウト
export Q_TELEMETRY_ENABLED=false

# 永続化
echo 'export Q_TELEMETRY_ENABLED=false' >> ~/.bashrc
```

**グローバル設定ファイル**:
```yaml
# ~/.amazonq/settings.yml
telemetry:
  enabled: false
```

**詳細**: [テレメトリー設定ガイド](../03_configuration/06_telemetry.md)

---

## 🌍 クロスリージョン処理

### データ処理の場所

**原則**:
- データは指定されたAWSリージョンで処理
- 一部の機能はクロスリージョン処理が必要

**クロスリージョン処理が発生する機能**:
- グローバルなモデル推論
- 特定の高度な機能

**詳細**: [Cross-region processing in Amazon Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/cross-region-processing.html)

---

## 🛡️ プライバシー保護のベストプラクティス

### 1. 機密情報の取り扱い

**❌ 避けるべき行為**:
```bash
# 機密情報を質問に含めない
q chat "このAPIキー sk-1234567890abcdef を使って..."

# 個人情報を含めない
q chat "顧客の山田太郎さん（yamada@example.com）の..."
```

**✅ 推奨される方法**:
```bash
# プレースホルダーを使用
q chat "このAPIキー <API_KEY> を使って..."

# 一般化した質問
q chat "顧客情報を処理する方法を教えて"
```

---

### 2. タグとフリーテキストフィールド

**AWS公式推奨**:
> タグや名前フィールドなどのフリーテキストフィールドに、機密情報や個人情報を入力しないでください。

**理由**:
- 請求ログに記録される可能性
- 診断ログに含まれる可能性
- 意図しない開示のリスク

---

### 3. プラン選択の判断基準

#### Freeプランが適切な場合

- ✅ 個人的な学習・実験
- ✅ オープンソースプロジェクト
- ✅ 公開情報のみを扱う開発

#### Pro/Enterpriseプランが必要な場合

- ✅ 商用開発
- ✅ 機密情報を扱う開発
- ✅ 顧客データを扱う開発
- ✅ 企業のコードベース
- ✅ コンプライアンス要件がある環境

---

## 📊 データ保存期間

### 会話履歴

| 環境 | 保存期間 | 削除方法 |
|------|---------|---------|
| Q CLI | セッション終了まで | 自動削除 |
| AWS Console | 1ヶ月 | 管理者が削除可能 |
| IDE | セッション終了まで | 自動削除 |

---

## 🔍 データアクセスの監視

### CloudTrailログ

**記録される情報**:
- Amazon Q APIの呼び出し
- 呼び出し元のIPアドレス
- 呼び出し時刻
- 使用されたIAMユーザー/ロール

**監視方法**:
```bash
# CloudTrailログの確認
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=InvokeModel \
  --max-results 10
```

---

## 📋 コンプライアンス

### 対応する規制・基準

Amazon Q Developerは以下の規制・基準に対応：

- ✅ GDPR（EU一般データ保護規則）
- ✅ HIPAA（医療保険の相互運用性と説明責任に関する法律）
- ✅ SOC 1, 2, 3
- ✅ ISO 27001, 27017, 27018
- ✅ PCI DSS

**詳細**: [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/)

---

## 🔗 関連ドキュメント

### セキュリティガイド
- [セキュリティ概要](01_security-overview.md)

### 設定ガイド
- [テレメトリー設定](../03_configuration/06_telemetry.md)
- [環境変数](../03_configuration/05_environment-variables.md)

### エンタープライズ展開
- [料金プラン比較](../05_deployment/02_pricing-comparison.md)
- [セキュリティチェックリスト](../05_deployment/03_security-checklist.md)
- [エンタープライズ導入ガイド](../05_deployment/01_enterprise-deployment.md)

### AWS公式ドキュメント
- [Data protection in Amazon Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/data-protection.html)
- [Amazon Q Developer service improvement](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/service-improvement.html)
- [Opt out of data sharing](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/opt-out-IDE.html)

---

## ❓ よくある質問

### Q1: Freeプランでオプトアウトすると機能が制限されますか？

**A**: いいえ、機能は制限されません。オプトアウトしても全機能を使用できます。

---

### Q2: Pro/Enterpriseプランでもテレメトリーは送信されますか？

**A**: はい、使用統計やエラーレポートは送信されますが、質問内容や応答内容はサービス改善に使用されません。

---

### Q3: 既に送信されたデータを削除できますか？

**A**: AWS Supportに問い合わせることで、特定のデータ削除をリクエストできます。

---

### Q4: GitHub版のAmazon Q Developerはどうですか？

**A**: GitHub版（プレビュー）は現在、サービス改善にデータを使用していません。将来的に変更される場合は、事前通知とオプトアウト方法が提供されます。

## 関連ドキュメント

- [セキュリティ概要](01_security-overview.md) - セキュリティ全体像
- [料金プラン比較](../05_deployment/02_pricing-comparison.md) - プランごとのプライバシー保護

---

**参考資料**:
- [AWS Data Privacy FAQ](https://aws.amazon.com/compliance/data-privacy-faq/)
- [AWS Shared Responsibility Model and GDPR](https://aws.amazon.com/blogs/security/the-aws-shared-responsibility-model-and-gdpr/)
