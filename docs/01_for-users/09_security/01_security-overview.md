[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [セキュリティガイド](README.md) > 01 Security Overview

---

# セキュリティ概要

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

**詳細**: [ファイルアクセス制御ガイド](03_file-access-control.md)

---

### 2-1. Bashコマンド実行制御（v1.19.0以降）

**deny_by_default モード**:

v1.19.0以降、`execute_bash`ツールでデフォルト拒否モードをサポート：

```json
{
  "toolsSettings": {
    "execute_bash": {
      "denyByDefault": true,
      "allowedCommands": ["ls", "cat", "grep", "find"]
    }
  }
}
```

**セキュリティ上のメリット**:
- ✅ ホワイトリスト方式の採用
- ✅ 意図しないコマンド実行の防止
- ✅ 監査ログの明確化

**builtin tool namespace**:

ビルトインツールの権限管理用名前空間（v1.19.0以降）：

- ツールごとの細粒度な権限設定
- `@builtin` 名前空間での一元管理
- セキュリティポリシーの明確化

**出典**: 
- [PR #2999](https://github.com/aws/amazon-q-developer-cli/pull/2999) - deny_by_default
- [PR #3205](https://github.com/aws/amazon-q-developer-cli/pull/3205) - builtin namespace

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

**詳細**: [AWS API制御ガイド](04_aws-api-control.md)

---

### 4. テレメトリーとプライバシー

**テレメトリーデータ**:
- 使用統計
- エラーレポート
- パフォーマンスメトリクス

**プライバシー保護**:
- Freeプラン: オプトアウト可能
- Pro/Enterpriseプラン: デフォルトで保護

**詳細**: [テレメトリー設定ガイド](../03_configuration/05_telemetry.md)

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

**詳細**: [認証情報管理ガイド](05_credentials-management.md)

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

**詳細**: [trust-all安全使用ガイド](06_trust-all-safety.md)

---

## 🛡️ セキュリティベストプラクティス

### 環境別の推奨設定

> **💡 このセクションについて**
> 
> この推奨設定は、以下に基づいて作成されました：
> 
> **基本設定の出典**:
> - Q CLIのツール制御機能（`--untrust-*`オプション、`/tools`コマンド）
> - [ファイルアクセス制御ガイド](03_file-access-control.md)
> - [AWS API制御ガイド](04_aws-api-control.md)
> 
> **環境別の解説**:
> - セキュリティベストプラクティスに基づく推奨事項
> - 開発効率とセキュリティのトレードオフ分析
> - 実務での適用シーンの例示
> 
> **注意**: 組織のセキュリティポリシーに応じて、これらの推奨設定をカスタマイズしてください。

#### 開発環境

**目的**: 開発効率を優先しつつ、基本的な保護を維持

```bash
# 基本的な保護
q chat --untrust-fs-read
```

**保護内容**:
- ✅ **ファイル読み取り**: 毎回確認を求める
  - 意図しないファイル読み取りを防止
  - 機密ファイル（`.env`, `credentials`等）の誤読み取りを防ぐ
- ⚠️ **AWS API**: 信頼（確認なし実行）
  - 開発中の頻繁なAPI呼び出しを効率化
  - 開発用AWSアカウントでの使用を想定
- ⚠️ **コマンド実行**: 信頼（確認なし実行）
  - ビルド、テスト等の頻繁なコマンド実行を効率化

**適用シーン**: ローカル開発、テスト環境、個人プロジェクト

---

#### 本番環境

**目的**: 本番データとAWSリソースを保護

```bash
# 厳格な保護
q chat --untrust-fs-read
Amazon Q> /tools untrust use_aws
```

**保護内容**:
- ✅ **ファイル読み取り**: 毎回確認を求める
  - 本番設定ファイルの誤読み取りを防止
  - 顧客データファイルへのアクセスを制御
- ✅ **AWS API**: 毎回確認を求める
  - 本番リソースの誤削除・変更を防止
  - EC2停止、S3削除、RDS変更等の重要操作を保護
  - CloudTrailログで操作履歴を追跡可能
- ⚠️ **コマンド実行**: 信頼（確認なし実行）
  - デプロイスクリプト等の実行を効率化
  - ただし、危険なコマンド（`rm -rf`等）は自動ブロック

**適用シーン**: 本番環境へのデプロイ、本番データ操作、運用作業

---

#### 機密情報を扱う環境

**目的**: 最大限のセキュリティを確保

```bash
# 最大限の保護
q chat --untrust-fs-read
Amazon Q> /tools untrust use_aws
Amazon Q> /tools untrust execute_bash
```

**保護内容**:
- ✅ **ファイル読み取り**: 毎回確認を求める
  - 機密文書、個人情報、認証情報ファイルを保護
  - GDPR、HIPAA等のコンプライアンス要件に対応
- ✅ **AWS API**: 毎回確認を求める
  - 本番環境の重要リソースを保護
  - 監査証跡の確保
- ✅ **コマンド実行**: 毎回確認を求める
  - すべてのシステム操作を可視化
  - データ削除、システム変更等の重大操作を防止
  - セキュリティインシデントのリスクを最小化

**適用シーン**: 
- 金融機関、医療機関等の規制業界
- 個人情報を扱うシステム
- セキュリティ監査が必要な環境
- コンプライアンス要件が厳格な組織

---

### 環境別設定の比較表

| 保護項目 | 開発環境 | 本番環境 | 機密情報環境 | 理由 |
|---------|---------|---------|-------------|------|
| **ファイル読み取り** | 🔒 確認必要 | 🔒 確認必要 | 🔒 確認必要 | 機密ファイルの誤読み取り防止 |
| **AWS API** | ✅ 信頼 | 🔒 確認必要 | 🔒 確認必要 | 本番リソースの保護 |
| **コマンド実行** | ✅ 信頼 | ✅ 信頼 | 🔒 確認必要 | システム操作の可視化 |
| **開発効率** | ⭐⭐⭐ | ⭐⭐ | ⭐ | 確認回数が増えるほど効率低下 |
| **セキュリティ** | ⭐ | ⭐⭐ | ⭐⭐⭐ | 保護レベルが高いほど安全 |

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

**詳細**: [プロジェクトルールガイド](../03_configuration/03_agent-configuration.md)

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
### セキュリティガイド
- [データプライバシー](02_data-privacy.md)
- [ファイルアクセス制御](03_file-access-control.md)
- [AWS API制御](04_aws-api-control.md)
- [認証情報管理](05_credentials-management.md)
- [trust-all安全使用ガイド](06_trust-all-safety.md)

### 設定ガイド
- [テレメトリー設定](../03_configuration/05_telemetry.md)
- [Agent設定](../03_configuration/03_agent-configuration.md)
- [環境変数](../03_configuration/06_environment-variables.md)

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

## 📖 ナビゲーション

**次へ**: [データプライバシー](02_data-privacy.md) →

---

最終更新: 2025-10-18

**参考資料**:
- [AWS責任共有モデル](https://aws.amazon.com/compliance/shared-responsibility-model/)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [Amazon Q Developer公式ドキュメント](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/)

---

最終更新: 2025-10-18
