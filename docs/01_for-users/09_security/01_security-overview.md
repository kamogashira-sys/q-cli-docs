# セキュリティ概要

**最終更新**: 2025-10-18  
**対象**: Amazon Q Developer CLI

---

## 📋 概要

このガイドは、Amazon Q Developer CLI（Q CLI）を安全に使用するためのセキュリティ情報を提供します。

---

## 🔒 セキュリティの基本原則

### AWS責任共有モデル

Amazon Q Developerは[AWS責任共有モデル](https://aws.amazon.com/compliance/shared-responsibility-model/)に基づいています：

| 責任範囲 | AWS | ユーザー |
|---------|-----|---------|
| **インフラストラクチャ** | ✅ AWSクラウドの保護 | - |
| **データ保護** | ✅ 暗号化機能の提供 | ✅ データの管理・保護 |
| **アクセス制御** | ✅ IAM機能の提供 | ✅ 権限の設定・管理 |
| **設定管理** | - | ✅ セキュリティ設定 |

---

## 🎯 主要なセキュリティトピック

### 1. データプライバシー

**Free vs Pro/Enterpriseプラン**:

| プラン | データ使用 | 推奨環境 |
|--------|-----------|---------|
| **Free** | サービス改善に使用される可能性あり | 個人開発、学習 |
| **Pro/Enterprise** | サービス改善に使用されない | 商用開発、機密情報 |

**詳細**: [データプライバシーガイド](02_data-privacy.md)

---

### 2. ファイルアクセス制御

**デフォルト動作**:
- `fs_read`ツールは**信頼済み**（確認なしでファイル読み取り可能）

**機密環境での推奨設定**:
```bash
# セッションごとに制限
q chat
Amazon Q> /tools untrust fs_read

# 永続的に制限（推奨）
echo 'alias q="q --untrust-fs-read"' >> ~/.bashrc
```

---

### 3. AWS API呼び出し制御

**リスク**:
- 意図しないリソース作成・変更・削除
- 予期しないコスト発生
- セキュリティ設定の変更

**推奨設定**:
```bash
# AWS API呼び出しを制限
Amazon Q> /tools untrust use_aws
```

---

### 4. テレメトリーとプライバシー

**テレメトリーデータ**:
- 使用統計
- エラーレポート
- パフォーマンスメトリクス

**プライバシー保護**:
- Freeプラン: オプトアウト可能
- Pro/Enterpriseプラン: デフォルトで保護

**詳細**: [テレメトリー設定ガイド](../03_configuration/06_telemetry.md)

---

### 5. 認証情報の管理

**ベストプラクティス**:

✅ **推奨**:
- 環境変数で認証情報を管理
- IAMロールの使用（EC2、ECS等）
- AWS SSOの活用
- 最小権限の原則

❌ **非推奨**:
- ファイルにハードコード
- Gitリポジトリにコミット
- 過剰な権限付与

---

## ⚠️ 重要なセキュリティリスク

### `/tools trust-all`の危険性

**リスク**:
- ✅ 確認プロンプトをバイパス
- ⚠️ 意図しないシステム変更
- ⚠️ データ損失の可能性
- ⚠️ セキュリティ脆弱性

**AWS公式推奨**:
> `/tools trust-all`または`/acceptall`モードは、本番環境や機密データを扱う環境では使用しないことを推奨します。

**安全な使用方法**:
```bash
# 1. 開発環境でのみ使用
# 2. 特定タスクのみ有効化
Amazon Q> /tools trust-all

# 3. タスク完了後すぐに無効化
Amazon Q> /tools reset
```

---

## 🛡️ セキュリティベストプラクティス

### 環境別の推奨設定

#### 開発環境

```bash
# 基本的な保護
q chat --untrust-fs-read
```

#### 本番環境

```bash
# 厳格な保護
q chat --untrust-fs-read
Amazon Q> /tools untrust use_aws
```

#### 機密情報を扱う環境

```bash
# 最大限の保護
q chat --untrust-fs-read
Amazon Q> /tools untrust use_aws
Amazon Q> /tools untrust execute_bash
```

---

### プロジェクトルールの活用

**`.amazonq/agent.yml`**:
```yaml
# セキュリティガイドラインを定義
rules: |
  ## セキュリティ要件
  - 機密情報をログに出力しない
  - AWS APIを呼び出す前に確認を求める
  - ファイル削除前に確認を求める
```

**詳細**: [プロジェクトルールガイド](../03_configuration/04_agent-configuration.md)

---

## 📊 セキュリティチェックリスト

### 初期設定

- [ ] プラン選択（Free vs Pro/Enterprise）
- [ ] テレメトリー設定の確認
- [ ] ファイルアクセス制御の設定
- [ ] AWS API制御の設定

### 日常運用

- [ ] 定期的な権限レビュー
- [ ] CloudTrailログの監視
- [ ] 異常なAPI呼び出しの検出
- [ ] 認証情報のローテーション

### エンタープライズ

- [ ] 組織ポリシーの適用
- [ ] AIサービスオプトアウトポリシー
- [ ] IAMポリシーによるアクセス制御
- [ ] 監査ログの保存・分析

---

## 🔗 関連ドキュメント

### セキュリティガイド
- [データプライバシーガイド](02_data-privacy.md)
### 設定ガイド
- [テレメトリー設定](../03_configuration/06_telemetry.md)
- [Agent設定](../03_configuration/04_agent-configuration.md)
- [環境変数](../03_configuration/05_environment-variables.md)

### エンタープライズ展開
- [料金プラン比較](../05_deployment/02_pricing-comparison.md)
- [セキュリティチェックリスト](../05_deployment/03_security-checklist.md)
- [エンタープライズ導入ガイド](../05_deployment/01_enterprise-deployment.md)

### AWS公式ドキュメント
- [Security in Amazon Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/security.html)
- [Data protection in Amazon Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/data-protection.html)
- [Security considerations and best practices](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-chat-security.html)

---

## 📞 セキュリティに関する問い合わせ

セキュリティ上の懸念や脆弱性を発見した場合：

1. **AWS公式**: [AWS Security](https://aws.amazon.com/security/)
2. **GitHub**: [amazon-q-developer-cli/issues](https://github.com/aws/amazon-q-developer-cli/issues)（セキュリティ問題は非公開で報告）

## 関連ドキュメント

- [セキュリティチェックリスト](../05_deployment/03_security-checklist.md) - 設定確認項目
- [エンタープライズ展開ガイド](../05_deployment/01_enterprise-deployment.md) - 組織でのセキュリティ管理

---

**参考資料**:
- [AWS責任共有モデル](https://aws.amazon.com/compliance/shared-responsibility-model/)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [Amazon Q Developer公式ドキュメント](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/)
