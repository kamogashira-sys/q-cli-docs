[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [デプロイメント](README.md) > 02 Pricing Comparison

---

# 料金プラン比較ガイド

最終更新: 2025-10-18  
**対象**: Amazon Q Developer

---

## 📋 概要

このガイドは、Amazon Q Developerの料金プランを比較し、組織に最適なプランを選択するための情報を提供します。

---

## 💰 プラン別料金比較

### Amazon Q Developer

| 項目 | Free | Pro（Builder ID） | Pro（IAM Identity Center） |
|------|------|------------------|--------------------------|
| **月額料金** | $0 | $19/ユーザー | $19/ユーザー |
| **認証方式** | AWS Builder ID | AWS Builder ID | IAM Identity Center |
| **ユーザー管理** | 個人 | 個人 | **組織一元管理** |
| **SSO対応** | ❌ | ❌ | ✅ |
| **エージェント要求** | 50回/月 | 拡張制限 | 拡張制限 |
| **コード変換** | 1,000行/月 | 4,000行/月（プール） | 4,000行/月（プール） |
| **カスタマイゼーション** | ❌ | ✅ | ✅ |
| **IP補償** | ❌ | ✅ | ✅ |
| **データ使用** | サービス改善に使用 | 使用されない | 使用されない |
| **推奨環境** | 個人開発・学習 | 個人開発・商用 | **エンタープライズ** |

**出典**: [Amazon Q Developer Pricing](https://aws.amazon.com/q/developer/pricing/)

---

## 🎯 プラン選択ガイド

### Freeプランが適切な場合

**対象**:
- ✅ 個人開発者
- ✅ 学習・実験目的
- ✅ オープンソースプロジェクト
- ✅ 予算制約がある個人

**メリット**:
- 無料で永続利用可能
- 基本機能は利用可能
- 月次制限内で十分な場合

**制限事項**:
- ⚠️ コンテンツがサービス改善に使用される可能性
- ⚠️ エージェント要求が月50回まで
- ⚠️ カスタマイゼーション不可
- ⚠️ IP補償なし

---

### Pro（Builder ID）が適切な場合

**対象**:
- ✅ フリーランス開発者
- ✅ 小規模チーム（組織管理不要）
- ✅ 商用開発（機密情報あり）
- ✅ 高度な機能が必要な個人

**メリット**:
- コンテンツがサービス改善に使用されない
- 拡張された制限
- カスタマイゼーション対応
- IP補償あり

**制限事項**:
- ⚠️ 組織一元管理不可
- ⚠️ SSOなし
- ⚠️ AWS Management Console未対応

---

### Pro（IAM Identity Center）が適切な場合【エンタープライズ推奨】

**対象**:
- ✅ エンタープライズ組織
- ✅ 10名以上の開発チーム
- ✅ 統合ユーザー管理が必要
- ✅ コンプライアンス要件がある
- ✅ SSO連携が必要

**メリット**:
- ✅ **組織一元管理**
- ✅ **SSO対応**（Okta、Microsoft Entra ID等）
- ✅ **AWS Management Console対応**
- ✅ **コンテンツ保護**（サービス改善に使用されない）
- ✅ **監査ログ**（CloudTrail）
- ✅ **グループベース権限管理**
- ✅ **IP補償**

**追加コスト**:
- IAM Identity Center: 無料
- 外部IDプロバイダー連携: 無料

---

## 📊 コスト試算例

### 小規模チーム（5名）

| プラン | 月額 | 年額 | 備考 |
|--------|------|------|------|
| Free | $0 | $0 | 制限あり |
| Pro（Builder ID） | $95 | $1,140 | 個人管理 |
| Pro（IAM Identity Center） | $95 | $1,140 | **組織管理** |

**推奨**: Pro（IAM Identity Center）- 組織管理のメリット大

---

### 中規模チーム（50名）

| プラン | 月額 | 年額 | 備考 |
|--------|------|------|------|
| Pro（Builder ID） | $950 | $11,400 | 管理困難 |
| Pro（IAM Identity Center） | $950 | $11,400 | **組織管理必須** |

**推奨**: Pro（IAM Identity Center）- 50名規模では組織管理が必須

---

### 大規模組織（500名）

| プラン | 月額 | 年額 | 備考 |
|--------|------|------|------|
| Pro（IAM Identity Center） | $9,500 | $114,000 | 組織管理 |

**コスト最適化**:
- 実際の利用者のみサブスクリプション
- 定期的な利用状況監査
- 未使用ライセンスの削除

---

## 💡 コスト最適化のベストプラクティス

### 1. 適切なプラン選択

**判断基準**:
```
チーム規模 < 5名 → Pro（Builder ID）も検討可能
チーム規模 ≥ 5名 → Pro（IAM Identity Center）推奨
エンタープライズ → Pro（IAM Identity Center）必須
```

---

### 2. ユーザー管理の最適化

**定期監査**:
```bash
# IAM Identity Centerユーザーの確認
aws identitystore list-users \
  --identity-store-id d-xxxxxxxxxx

# Amazon Q Developerサブスクリプション確認
aws q list-subscriptions
```

**推奨頻度**: 月次

---

### 3. 利用状況の可視化

**AWS Cost Explorer活用**:
1. Billing and Cost Management Console
2. Cost Explorer → サービス別コスト
3. "Amazon Q Developer"でフィルター

**監視項目**:
- 月次コスト推移
- ユーザー別利用状況
- 未使用ライセンス

---

### 4. コード変換の最適化

**制限**:
- Free: 1,000行/月
- Pro: 4,000行/月/ユーザー（アカウントレベルでプール）

**超過料金**: $0.003/行

**最適化方法**:
- 小さな単位で変換
- Proプランで高い割当を活用
- チーム全体でプール活用

---

## 🔒 セキュリティとコンプライアンス

### データプライバシー

| プラン | コンテンツ使用 | 推奨環境 |
|--------|--------------|---------|
| **Free** | サービス改善に使用される可能性 | 個人開発のみ |
| **Pro** | 使用されない | 商用開発・機密情報 |

**重要**: エンタープライズ環境では**Proプラン必須**

---

### IP補償

**Proプランの特典**:
- ✅ 生成コードに対するIP補償
- ✅ 著作権侵害のリスク軽減
- ✅ 法的保護

**詳細**: [AWS Service Terms](https://aws.amazon.com/service-terms/)

---

## 📋 プラン変更

### FreeからProへのアップグレード

**手順**:
1. AWS Management Console → Amazon Q Developer
2. "Subscribe to Pro"を選択
3. 支払い情報を入力
4. サブスクリプション確認

**課金開始**: 即時（日割り計算）

---

### ProからFreeへのダウングレード

**手順**:
1. AWS Management Console → Amazon Q Developer
2. "Unsubscribe"を選択
3. 確認

**課金停止**: 請求サイクル終了時

---

## 🔗 関連ドキュメント

### 料金情報
- [Amazon Q Developer Pricing](https://aws.amazon.com/q/developer/pricing/)
- [Tiers of service for Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-tiers.html)
- [Amazon Q Developer Pro subscription billing](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/tracking-across-org-cost-usage.html)

### エンタープライズ導入
- [エンタープライズ導入ガイド](01_enterprise-deployment.md)
- [セキュリティ概要](../09_security/01_security-overview.md)
- [データプライバシーガイド](../09_security/02_data-privacy.md)

### コスト最適化
- [Optimizing cost for deploying Amazon Q](https://aws.amazon.com/blogs/aws-cloud-financial-management/optimizing-cost-for-deploying-amazon-q/)

---

## ❓ よくある質問

### Q1: 組織全体で一括購入できますか？

**A**: はい、IAM Identity Centerを使用したProプランで、組織全体のユーザーを一元管理できます。請求はAWS Organizationsの管理アカウントに集約されます。

---

### Q2: 月の途中でサブスクリプションした場合の料金は？

**A**: 日割り計算されます。例: 月の半ばで開始した場合、初月は約$9.50（$19の半額）となります。

---

### Q3: 未使用のライセンスも課金されますか？

**A**: はい、サブスクリプションしたユーザー数に基づいて課金されます。定期的な監査で未使用ライセンスを削除することを推奨します。

---

### Q4: コード変換の超過料金を避けるには？

**A**: 
- 小さな単位で変換を実行
- Proプランの高い割当（4,000行/月）を活用
- チーム全体でプールされた割当を共有

## 関連ドキュメント

- [データプライバシー](../09_security/02_data-privacy.md) - プランごとのプライバシー保護
- [エンタープライズ展開ガイド](01_enterprise-deployment.md) - 組織での導入方法

---

**参考資料**:
- [Amazon Q Developer Pricing](https://aws.amazon.com/q/developer/pricing/)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Cost Management](https://aws.amazon.com/aws-cost-management/)
