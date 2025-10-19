[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [セキュリティガイド](README.md) > 04 Aws Api Control

---

# AWS API制御ガイド

**最終更新**: 2025-10-18  
**対象**: Amazon Q Developer CLI

---

## 📋 概要

このガイドは、Amazon Q Developer CLIの`use_aws`ツールによるAWS API呼び出しを制御する方法を説明します。

---

## 🎯 use_awsツールとは

### 機能

`use_aws`ツールは、Amazon Q CLIがAWS CLIコマンドを実行するための機能です。

**主な用途**:
- AWSリソースの作成・変更・削除
- リソース情報の取得
- 設定の確認・変更
- ログの取得

### 実行例

```bash
Amazon Q> S3バケットを作成して

# 内部で実行されるコマンド
aws s3 mb s3://my-bucket
```

---

## ⚠️ セキュリティリスク

### 潜在的なリスク

| リスク | 説明 | 影響 |
|--------|------|------|
| **意図しないリソース作成** | EC2、RDS、S3等の作成 | **コスト発生** |
| **リソースの削除** | データベース、ストレージの削除 | **データ損失** |
| **セキュリティ設定の変更** | IAMポリシー、セキュリティグループ | **セキュリティ侵害** |
| **設定の上書き** | 本番環境の設定変更 | **サービス停止** |

### 具体例

**シナリオ1: 意図しないEC2インスタンス起動**
```bash
Amazon Q> テスト用のサーバーを起動して

# 実行されるコマンド
aws ec2 run-instances --instance-type m5.24xlarge ...
# → 高額なインスタンスが起動される
```

**コスト**: $4.608/時間 = $3,317/月

**シナリオ2: 本番データベースの削除**
```bash
Amazon Q> 古いデータベースを削除して

# 実行されるコマンド
aws rds delete-db-instance --db-instance-identifier prod-db
# → 本番データベースが削除される
```

**影響**: データ損失、サービス停止

**シナリオ3: セキュリティグループの変更**
```bash
Amazon Q> ポート22を開放して

# 実行されるコマンド
aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 22 --cidr 0.0.0.0/0
# → 全世界からSSHアクセス可能になる
```

**影響**: セキュリティ脆弱性

---

## 🔒 推奨設定

### セッションごとの制限

チャットセッション開始時に毎回制限する方法：

```bash
q chat
Amazon Q> /tools untrust use_aws
```

**効果**:
- AWS API呼び出し前に確認プロンプトが表示される
- セッション終了まで有効

### 永続的な制限（推奨）

シェル設定ファイルにエイリアスを追加：

**bash**:
```bash
echo 'alias q="q --untrust-use-aws"' >> ~/.bashrc
source ~/.bashrc
```

**zsh**:
```bash
echo 'alias q="q --untrust-use-aws"' >> ~/.zshrc
source ~/.zshrc
```

**効果**:
- すべてのセッションで自動的に制限される
- 最も安全な方法

### Agent設定での制限

プロジェクトごとに制限する方法：

**`.q/agent.json`**:
```json
{
  "name": "production-project",
  "untrustedTools": ["use_aws"]
}
```

**効果**:
- プロジェクトディレクトリ内で自動適用
- チーム全体で共有可能

---

## 🛡️ IAMポリシーでの制限

### 最小権限の原則

**読み取り専用ポリシー**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "s3:Get*",
        "s3:List*",
        "rds:Describe*",
        "cloudwatch:Get*",
        "cloudwatch:List*"
      ],
      "Resource": "*"
    }
  ]
}
```

**効果**:
- リソースの参照のみ許可
- 作成・変更・削除は不可

### リソースタグによる制限

**特定環境のみ操作可能**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:*",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "ec2:ResourceTag/Environment": "development"
        }
      }
    }
  ]
}
```

**効果**:
- 開発環境のみ操作可能
- 本番環境は保護される

---

## 🎨 環境別の推奨設定

### 開発環境

**基本的な保護**:
```bash
q chat --untrust-use-aws
```

**IAMポリシー**:
- 開発環境リソースのみ操作可能
- 本番環境は読み取り専用

### 本番環境

**厳格な制限**:
```bash
# 永続的な制限
alias q="q --untrust-use-aws"

# Agent設定
{
  "untrustedTools": ["use_aws", "execute_bash"]
}
```

**IAMポリシー**:
- 読み取り専用
- 変更は承認プロセス経由

### 機密環境

**すべて制限**:
```bash
# すべてのツールを制限
alias q="q --untrust-all-tools"
```

**IAMポリシー**:
- 最小限の権限
- MFA必須

---

## 🔍 確認プロンプトの動作

### 制限時の動作

`use_aws`を制限すると、AWS API呼び出し前に確認プロンプトが表示されます：

```bash
Amazon Q> S3バケットを作成して

⚠️  AWS API Request
Amazon Q wants to execute: aws s3 mb s3://my-bucket

Allow this action? [y/N]:
```

**選択肢**:
- `y`: 許可（今回のみ）
- `N`: 拒否（デフォルト）
- `a`: すべて許可（セッション中）

---

## 🛠️ 安全な使用方法

### 1. 実行前に確認

**コマンドの確認**:
```bash
Amazon Q> どのコマンドを実行しますか？
# → 実行予定のコマンドを確認してから許可
```

### 2. dry-runモードの活用

**dry-runオプション**:
```bash
Amazon Q> dry-runモードでEC2インスタンスを起動して

# 実行されるコマンド
aws ec2 run-instances --dry-run ...
# → 実際には実行されず、権限のみ確認
```

### 3. ログの監視

**CloudTrailでの監視**:
```bash
# API呼び出しの記録を確認
aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=my-user
```

### 4. コスト監視

**AWS Budgetsの設定**:
```bash
# 予算アラートの設定
aws budgets create-budget --account-id 123456789012 --budget file://budget.json
```

---

## 💡 実例

### 例1: S3バケット作成の確認

**安全な方法**:
```bash
Amazon Q> S3バケットを作成したいです。どのコマンドを実行しますか？

# 確認後
Amazon Q> aws s3 mb s3://my-bucket --region us-east-1
# → 確認プロンプトで許可
```

### 例2: EC2インスタンス起動の制御

**安全な方法**:
```bash
Amazon Q> t3.microインスタンスを1台起動して

# 確認プロンプト
⚠️  AWS API Request
Command: aws ec2 run-instances --instance-type t3.micro --count 1 ...

# コストを確認してから許可
```

### 例3: IAMロール変更の防止

**安全な方法**:
```bash
# IAMポリシーで制限
{
  "Effect": "Deny",
  "Action": "iam:*",
  "Resource": "*"
}

# Q CLIからの変更は拒否される
```

---

## 🛠️ トラブルシューティング

### API呼び出しが失敗する

**症状**:
```
Error: Access Denied
```

**原因**:
- IAM権限不足
- `use_aws`が制限されている

**対処**:
```bash
# 権限を確認
aws sts get-caller-identity

# 一時的に許可
Amazon Q> /tools trust use_aws
```

### 権限エラーの対処

**症状**:
```
Error: User is not authorized to perform: ec2:RunInstances
```

**原因**:
- IAMポリシーで制限されている

**対処**:
```bash
# 必要な権限を確認
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:user/my-user \
  --action-names ec2:RunInstances
```

---

## 🔗 関連ドキュメント

### セキュリティガイド
- [セキュリティ概要](01_security-overview.md)
- [ファイルアクセス制御](03_file-access-control.md)
- [認証情報管理](05_credentials-management.md)

### 設定ガイド
- [Agent設定](../03_configuration/03_agent-configuration.md)
- [環境変数](../03_configuration/06_environment-variables.md)

### エンタープライズ展開
- [セキュリティチェックリスト](../05_deployment/03_security-checklist.md)
- [エンタープライズ導入ガイド](../05_deployment/01_enterprise-deployment.md)

### AWS公式ドキュメント
- [Security considerations and best practices](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-chat-security.html)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

---

## 📞 サポート

セキュリティ上の懸念や質問がある場合：

1. **AWS公式**: [AWS Security](https://aws.amazon.com/security/)
2. **GitHub**: [amazon-q-developer-cli/issues](https://github.com/aws/amazon-q-developer-cli/issues)
3. **ドキュメント**: [トラブルシューティング](../06_troubleshooting/02_common-issues.md)

---

## 📖 ナビゲーション

← **前へ**: [ファイルアクセス制御](03_file-access-control.md) | **次へ**: [認証情報管理](05_credentials-management.md) →

---

**最終更新**: 2025-10-18
