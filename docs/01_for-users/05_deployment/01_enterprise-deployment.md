[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [デプロイメント](README.md) > 01 Enterprise Deployment

---

# エンタープライズ導入ガイド

最終更新: 2025-10-11  
**対象バージョン**: v1.17.0以降

---

## 📋 概要

このガイドでは、Amazon Q Developer CLIを組織やエンタープライズ環境で導入する際の手順とベストプラクティスを説明します。

---

## 🏢 エンタープライズ導入の選択肢

### Amazon Q Developer のプラン比較

| プラン | 認証方式 | 料金 | ユーザー管理 | 主な用途 |
|--------|----------|------|--------------|----------|
| **Free** | AWS Builder ID | 無料 | 個人管理 | 個人開発者 |
| **Pro (Builder ID)** | AWS Builder ID | $19/月/ユーザー | 個人管理 | 個人開発者（高度な機能） |
| **Pro (IAM Identity Center)** | IAM Identity Center | $19/月/ユーザー | 組織管理 | **エンタープライズ/組織** |

### エンタープライズ導入のメリット

**IAM Identity Center を使用した Pro プラン**を選択することで：

1. **統合ユーザー管理**
   - 組織全体のユーザーを一元管理
   - シングルサインオン（SSO）による認証
   - 外部IDプロバイダー（Okta、Microsoft Entra ID等）との連携

2. **アクセス制御**
   - グループベースの権限管理
   - きめ細かなアクセスポリシー
   - 監査ログとコンプライアンス対応

3. **コスト管理**
   - サブスクリプションの一元管理
   - 利用状況の可視化
   - ライセンスの最適化

4. **カスタマイゼーション**
   - 組織固有の設定
   - カスタムルールの適用
   - ダッシュボードによる利用状況分析

5. **データプライバシー保護**
   - **重要**: Pro/Enterpriseプランでは、コンテンツ（質問、コード、応答）がサービス改善やモデル学習に使用されない
   - Freeプランではコンテンツがサービス改善に使用される可能性がある
   - エンタープライズ環境での機密情報保護に最適

> **💡 エンタープライズでの重要な考慮事項**
>
> **データプライバシー**: Pro/Enterpriseプランでは、あなたの組織のコンテンツはAWSのサービス改善やモデル学習に使用されません。これは、機密情報を扱うエンタープライズ環境において重要なセキュリティ要件です。
>
> 詳細: [AWS公式ドキュメント - Service Improvement](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/service-improvement.html)

---

## 🚀 導入手順

### 前提条件

- AWS Organizations の設定（推奨）
- 管理者権限を持つAWSアカウント
- IAM Identity Center の基本知識

### Step 1: AWS IAM Identity Center のセットアップ

#### 1.1 組織インスタンスの作成

**推奨構成**: 管理アカウントで IAM Identity Center を有効化

```bash
# 管理アカウントにログイン
# マネジメントコンソール > IAM Identity Center > 有効にする
```

**重要事項**:
- IAM Identity Center インスタンスは1リージョンに1つのみ
- 組織インスタンスとアカウントインスタンスの違いを理解する
- 組織インスタンス = AWS Organizations 全体を管理（推奨）
- アカウントインスタンス = 単一アカウントのみ

#### 1.2 IDソースの設定

**オプション1: IAM Identity Center ネイティブディレクトリ**（簡単に開始）
```
- 無料で利用可能
- 基本的なユーザー/グループ管理
- 小規模組織に適している
```

**オプション2: 外部IDプロバイダー連携**（エンタープライズ推奨）
```
- Microsoft Entra ID (旧 Azure AD)
- Okta
- Active Directory
- その他SAML 2.0対応プロバイダー
```

#### 1.3 ユーザーとグループの作成

```
1. グループ作成例:
   - "Q-Developer-Admins" (管理者グループ)
   - "Q-Developer-Users" (一般ユーザーグループ)
   - "Q-Developer-Pro-Users" (Proライセンスグループ)

2. ユーザー作成:
   - テストユーザーを作成
   - 適切なグループに所属させる
   - 招待メールからアクティベート
```

#### 1.4 権限セットの設定

```
1. 事前定義された権限セット:
   - AdministratorAccess (管理者用)
   - ReadOnlyAccess (参照のみ)

2. カスタム権限セット:
   - 必要に応じて作成
   - 最小権限の原則に従う
```

#### 1.5 AWSアカウントへの権限割り当て

```
マルチアカウント許可の設定:
1. 対象AWSアカウントを選択
2. グループを選択
3. 権限セットを割り当て
```

---

### Step 2: Amazon Q Developer サブスクリプションの登録

#### 2.1 デプロイオプションの選択

**推奨構成**: デプロイオプション2
- IAM Identity Center: 管理アカウント
- サブスクリプション管理: メンバーアカウント

**メリット**:
- 管理アカウントの利用を最小化（ベストプラクティス）
- サブスクリプション管理の分散
- 組織インスタンスの全機能を利用可能

#### 2.2 プロファイルの作成

```bash
# サブスクリプション管理用アカウントにログイン
# マネジメントコンソール > Amazon Q Developer > 使用を開始
```

**設定項目**:
1. プロファイル名を指定
2. IAM Identity Center との紐付け
3. アクティビティ追跡設定（オプション）

#### 2.3 サブスクリプション登録

```
1. サブスクリプションメニューから「サブスクライブ」
2. Proライセンスを付与するグループを選択
   例: "Q-Developer-Pro-Users"
3. 登録完了を確認
```

---

### Step 3: Q CLI のインストールと認証設定

#### 3.1 Q CLI のインストール

各開発者のマシンにQ CLIをインストール：

**macOS (Homebrew)**:
```bash
brew install --cask amazon-q
```

**Linux**:
```bash
# ダウンロードとインストール
curl -o q-installer.sh https://desktop-release.codewhisperer.us-east-1.amazonaws.com/latest/Q-macos-x64.sh
chmod +x q-installer.sh
./q-installer.sh
```

#### 3.2 IAM Identity Center 認証の設定

```bash
# IAM Identity Center で認証
q login --sso

# プロンプトに従って入力:
# - Start URL: https://your-profile.awsapps.com/start
# - Region: us-east-1 (IAM Identity Center のリージョン)
```

**認証フロー**:
1. ブラウザが自動的に開く
2. IAM Identity Center のログイン画面
3. 組織のIDプロバイダーで認証
4. アクセス許可を承認
5. Q CLI で認証完了

#### 3.3 認証状態の確認

```bash
# 現在の認証状態を確認
q whoami

# 出力例:
# Status: Authenticated
# User: user@example.com
# Plan: Pro
# Expires: 2025-10-10T12:00:00Z
```

---

## 📊 利用状況の監視

### ダッシュボードの活用

**アクセス方法**:
```
マネジメントコンソール > Amazon Q Developer > ダッシュボード
```

**確認できる情報**:
- アクティブユーザー数
- 機能別利用状況
- コード提案の受け入れ率
- よく使われている機能
- 未活用の機能

### 利用状況レポート

定期的に以下を確認：
1. **ライセンス利用率**
   - 割り当てライセンス数
   - アクティブユーザー数
   - 未使用ライセンス

2. **機能活用状況**
   - コード補完
   - チャット機能
   - コマンドライン支援
   - テスト生成

3. **ROI分析**
   - 開発効率の向上
   - コード品質の改善
   - 学習時間の短縮

---

## 🔒 セキュリティとコンプライアンス

### セキュリティベストプラクティス

#### 1. 最小権限の原則

```json
{
  "allowedTools": [
    "fs_read",
    "fs_write"
  ]
}
```

不要なツールへのアクセスを制限

#### 2. 監査ログの有効化

```bash
# CloudTrail でIAM Identity Center のログを記録
# Amazon Q Developer のアクティビティログを有効化
```

#### 3. ネットワークセキュリティ

```
- VPN経由でのアクセス制限
- IPアドレス制限の設定
- プライベートネットワークからのアクセス
```

### コンプライアンス対応

#### データ保護
- コード提案のデータ保持期間
- 個人情報の取り扱い
- GDPR/CCPA対応

#### アクセス制御
- 定期的な権限レビュー
- 不要なアカウントの無効化
- 多要素認証（MFA）の強制

---

## 🎯 ベストプラクティス

### 1. 段階的なロールアウト

```
Phase 1: パイロットグループ（5-10名）
  - 初期設定の検証
  - フィードバック収集
  - 問題点の洗い出し

Phase 2: 部門単位での展開（50-100名）
  - 部門固有の設定調整
  - トレーニングの実施
  - サポート体制の確立

Phase 3: 全社展開
  - 全従業員へのロールアウト
  - 継続的なサポート
  - 利用促進施策
```

### 2. トレーニングとオンボーディング

**推奨トレーニング内容**:
1. Q CLI の基本操作
2. チャット機能の活用
3. コード補完の使い方
4. セキュリティガイドライン
5. トラブルシューティング

**オンボーディング資料**:
- クイックスタートガイド
- ビデオチュートリアル
- FAQ
- 社内サポート窓口

### 3. 継続的な改善

```
1. 定期的な利用状況レビュー（月次）
2. ユーザーフィードバックの収集
3. 設定の最適化
4. 新機能の評価と導入
```

---

## トラブルシューティング

問題が発生した場合は、[トラブルシューティングガイド](../06_troubleshooting/02_common-issues.md)を参照してください。

**関連トピック**:
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)

---

## 📚 参考資料

### 公式ドキュメント

- [Amazon Q Developer 公式サイト](https://aws.amazon.com/q/developer/)
- [IAM Identity Center ドキュメント](https://docs.aws.amazon.com/singlesignon/)
- [Q CLI ユーザーガイド](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/)

### AWSブログ記事

- [組織で Amazon Q Developer を始めるための AWS IAM Identity Center 入門](https://aws.amazon.com/jp/blogs/psa/getting-started-with-aws-iam-identity-center-for-amazon-q-developer-in-organizations/)
  - IAM Identity Center を使った組織導入の詳細手順
  - 実践的な設定例とベストプラクティス
  - ダッシュボードの活用方法

### 📚 関連ドキュメント

- [インストールガイド](../01_getting-started/01_installation.md)
- [環境変数ガイド](../03_configuration/05_environment-variables.md)
- [セキュリティベストプラクティス](../04_best-practices/02_security.md)

---

## 💡 次のステップ

1. **[インストールガイド](../01_getting-started/01_installation.md)** - Q CLI のインストール
2. **[クイックスタート](../01_getting-started/02_quick-start.md)** - 基本的な使い方
3. **[Agent設定](../03_configuration/04_agent-configuration.md)** - 組織固有の設定

## 関連ドキュメント

- [セキュリティ概要](../09_security/01_security-overview.md) - セキュリティ全体像
- [セキュリティチェックリスト](03_security-checklist.md) - 設定確認項目
- [料金プラン比較](02_pricing-comparison.md) - プランの選択

---

**作成日**: 2025-10-11  
最終更新: 2025-10-11
