[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [デプロイメント](README.md) > 03 Security Checklist

---

# エンタープライズセキュリティ要件チェックリスト

**最終更新**: 2025-10-18  
**対象**: Amazon Q Developer CLI エンタープライズ導入

---

## 📋 概要

このチェックリストは、Amazon Q Developer CLIをエンタープライズ環境に導入する際のセキュリティ要件を確認するためのものです。

---

## 🔒 導入前チェックリスト

### 1. プラン選択

- [ ] **Proプラン（IAM Identity Center）を選択**
  - エンタープライズ環境ではProプラン必須
  - コンテンツがサービス改善に使用されない
  - 組織一元管理が可能

**参考**: [料金プラン比較](02_pricing-comparison.md)

---

### 2. 認証とアクセス制御

#### IAM Identity Center設定

- [ ] **IAM Identity Centerの有効化**
  - 任意のサポートされているAWSリージョンで有効化可能（グローバルに利用可能）
  - 組織全体のユーザー管理

- [ ] **外部IDプロバイダー連携**（オプション）
  - Okta、Microsoft Entra ID、Google Workspace等
  - SAML 2.0対応

- [ ] **グループベース権限管理**
  - 開発者グループ、管理者グループ等
  - 最小権限の原則

**参考**: [IAM Identity Center Documentation](https://docs.aws.amazon.com/singlesignon/latest/userguide/)

---

#### IAMポリシー設定

- [ ] **Amazon Q Developer用IAMポリシー作成**
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "q:*"
        ],
        "Resource": "*"
      }
    ]
  }
  ```

- [ ] **最小権限の原則適用**
  - 必要な権限のみ付与
  - 定期的な権限レビュー

---

### 3. データプライバシー

- [ ] **データ使用ポリシーの確認**
  - Proプラン: コンテンツがサービス改善に使用されない
  - テレメトリー: オプトアウト可能

- [ ] **テレメトリー設定**
  ```bash
  # 組織全体でテレメトリー無効化（オプション）
  export Q_TELEMETRY_ENABLED=false
  ```

- [ ] **AIサービスオプトアウトポリシー**（オプション）
  - AWS Organizationsで設定
  - 組織全体に適用

**参考**: [データプライバシーガイド](../09_security/02_data-privacy.md)

---

### 4. ネットワークセキュリティ

- [ ] **ファイアウォール設定**
  - Amazon Q APIエンドポイントへのアクセス許可
  - HTTPS（TLS 1.2以上）

- [ ] **プロキシ設定**（必要な場合）
  ```bash
  export HTTPS_PROXY=http://proxy.example.com:8080
  export NO_PROXY=localhost,127.0.0.1
  ```

- [ ] **VPCエンドポイント**（オプション）
  - AWS PrivateLinkでプライベート接続
  - インターネット経由を回避

---

### 5. 監査とログ

- [ ] **CloudTrail有効化**
  - Amazon Q API呼び出しの記録
  - 監査証跡の保存

- [ ] **ログ保存期間の設定**
  - 最低90日間推奨
  - コンプライアンス要件に応じて調整

- [ ] **ログ分析の自動化**
  - Amazon CloudWatch Logs Insights
  - 異常検出アラート

**参考**: [AWS CloudTrail Documentation](https://docs.aws.amazon.com/cloudtrail/)

---

## 🛡️ 導入時チェックリスト

### 6. ファイルアクセス制御

- [ ] **fs_read制限の設定**
  ```bash
  # 機密環境では必須
  q chat --untrust-fs-read
  ```

- [ ] **永続的な設定**
  ```bash
  echo 'alias q="q --untrust-fs-read"' >> ~/.bashrc
  ```

- [ ] **プロジェクトルールの設定**
  ```yaml
  # .amazonq/agent.yml
  rules: |
    ## セキュリティ要件
    - 機密情報をログに出力しない
    - ファイル削除前に確認を求める
  ```

**参考**: [ファイルアクセス制御ガイド](../09_security/03_file-access-control.md)

---

### 7. AWS API制御

- [ ] **use_aws制限の設定**
  ```bash
  Amazon Q> /tools untrust use_aws
  ```

- [ ] **IAM権限の最小化**
  - 開発環境用の制限されたIAMロール
  - 本番環境へのアクセス制限

- [ ] **User Agent マーカーの活用**
  - CloudTrailでAmazon Q由来のAPI呼び出しを識別
  - IAMポリシーで制御

**参考**: [Controlling AWS API Calls from Amazon Q Developer](https://aws.amazon.com/blogs/devops/controlling-aws-api-calls-from-amazon-q-developer-enterprise-governance-with-built-in-user-agent-markers/)

---

### 8. 機密情報の保護

- [ ] **環境変数の使用**
  - APIキー、パスワードは環境変数で管理
  - ファイルにハードコードしない

- [ ] **AWS Secrets Managerの活用**
  - 機密情報の一元管理
  - 自動ローテーション

- [ ] **Gitリポジトリの保護**
  - .gitignoreで機密ファイルを除外
  - Git-secretsの導入

---

### 9. コンプライアンス

- [ ] **対応規制の確認**
  - GDPR、HIPAA、SOC 2等
  - Amazon Q Developerの対応状況確認

- [ ] **データ保存場所の確認**
  - リージョン選択
  - クロスリージョン処理の理解

- [ ] **データ保持ポリシー**
  - 会話履歴の保存期間
  - 削除手順の確立

**参考**: [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/)

---

## 📊 運用時チェックリスト

### 10. 定期監査

- [ ] **月次ユーザー監査**
  - 未使用ライセンスの削除
  - 権限の見直し

- [ ] **四半期セキュリティレビュー**
  - IAMポリシーの見直し
  - ログ分析
  - インシデント確認

- [ ] **年次コンプライアンス監査**
  - 規制要件の確認
  - 監査証跡の提出

---

### 11. インシデント対応

- [ ] **インシデント対応計画の策定**
  - セキュリティインシデントの定義
  - エスカレーションフロー
  - 連絡先リスト

- [ ] **インシデント検出の自動化**
  - CloudWatch Alarms
  - AWS Security Hub

- [ ] **インシデント対応訓練**
  - 年1回以上の訓練
  - 対応手順の見直し

---

### 12. ユーザー教育

- [ ] **セキュリティトレーニング**
  - 新規ユーザー向けオンボーディング
  - セキュリティベストプラクティス
  - 禁止事項の周知

- [ ] **定期的なリマインダー**
  - 四半期ごとのセキュリティ通知
  - 新機能・変更点の周知

- [ ] **ドキュメントの整備**
  - 社内セキュリティガイドライン
  - FAQ
  - トラブルシューティング

---

## 🎯 推奨セキュリティ設定

### 最小構成（開発環境）

```bash
# ファイルアクセス制限
q chat --untrust-fs-read

# テレメトリー無効化
export Q_TELEMETRY_ENABLED=false
```

---

### 推奨構成（本番環境）

```bash
# 厳格な制限
q chat --untrust-fs-read
export Q_TELEMETRY_ENABLED=false

# セッション内でAWS API制限
Amazon Q> /tools untrust use_aws
Amazon Q> /tools untrust execute_bash
```

---

### 最大セキュリティ構成（機密環境）

```bash
# 全ツール制限
q chat --untrust-fs-read
export Q_TELEMETRY_ENABLED=false

# セッション内で全ツール制限
Amazon Q> /tools untrust use_aws
Amazon Q> /tools untrust execute_bash
Amazon Q> /tools untrust fs_write

# プロジェクトルールで追加制限
# .amazonq/agent.yml
rules: |
  ## 厳格なセキュリティ要件
  - 全ての操作で明示的な確認を求める
  - 機密情報を含むファイルへのアクセス禁止
  - AWS APIの呼び出し禁止
```

---

## 🔗 関連ドキュメント

### セキュリティガイド
- [セキュリティ概要](../09_security/01_security-overview.md)
- [データプライバシーガイド](../09_security/02_data-privacy.md)
- [ファイルアクセス制御]()
- [AWS API制御]()

### 導入ガイド
- [エンタープライズ導入ガイド](01_enterprise-deployment.md)
- [料金プラン比較](02_pricing-comparison.md)

### AWS公式ドキュメント
- [Security in Amazon Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/security.html)
- [Security considerations and best practices](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-chat-security.html)

---

## 📝 チェックリスト進捗管理

### 導入フェーズ別の完了目標

| フェーズ | 必須項目 | 推奨項目 | 完了目標 |
|---------|---------|---------|---------|
| **導入前** | 1-5 | - | 100% |
| **導入時** | 6-9 | - | 100% |
| **運用時** | 10 | 11-12 | 80%以上 |

## 関連ドキュメント

- [セキュリティ概要](../09_security/01_security-overview.md) - セキュリティ全体像
- [エンタープライズ展開ガイド](01_enterprise-deployment.md) - 組織での導入方法

---

**作成者**: Amazon Q Developer CLI  
**レビュー**: セキュリティチーム  
**承認**: CISO
