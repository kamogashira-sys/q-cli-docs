# 認証情報管理ガイド

**最終更新**: 2025-10-18  
**対象**: Amazon Q Developer CLI

---

## 📋 概要

このガイドは、Amazon Q Developer CLIで使用するAWS認証情報を安全に管理する方法を説明します。

---

## 🎯 認証方式

### AWS Builder ID

**対象**: 個人開発者

**特徴**:
- ✅ 無料で利用可能
- ✅ 簡単なセットアップ
- ✅ 個人アカウント管理
- ❌ 組織管理不可

**設定方法**:
```bash
q
# → ブラウザが開き、AWS Builder IDでログイン
```

**詳細**: [認証設定ガイド](../01_getting-started/01_installation.md#-認証設定)

---

### IAM Identity Center

**対象**: エンタープライズ・組織

**特徴**:
- ✅ SSO統合
- ✅ 組織一元管理
- ✅ 外部IDプロバイダー連携（Okta、Microsoft Entra ID等）
- ✅ きめ細かなアクセス制御

**設定方法**:
```bash
q
# → IAM Identity Centerのログイン画面が表示
# → 組織のSSOでログイン
```

**詳細**: [エンタープライズ導入ガイド](../05_deployment/01_enterprise-deployment.md)

---

## 🛡️ ベストプラクティス

### ✅ 推奨

#### 1. 環境変数での管理

**一時的な認証情報**:
```bash
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_SESSION_TOKEN="..."
```

**プロファイルの使用**:
```bash
export AWS_PROFILE="my-profile"
```

**利点**:
- ファイルにハードコードしない
- セッション終了時に消える
- 環境ごとに切り替え可能

#### 2. IAMロールの使用

**EC2インスタンスロール**:
```bash
# インスタンスメタデータから自動取得
# 認証情報の設定不要
```

**ECSタスクロール**:
```bash
# タスク定義で指定
# コンテナ内で自動的に利用可能
```

**Lambda実行ロール**:
```bash
# Lambda関数に自動的に付与
# 認証情報の管理不要
```

**利点**:
- 認証情報の保存不要
- 自動ローテーション
- 最小権限の原則

#### 3. AWS SSOの活用

**設定**:
```bash
aws configure sso
# → SSO設定を対話的に入力
```

**使用**:
```bash
aws sso login --profile my-sso-profile
export AWS_PROFILE=my-sso-profile
```

**利点**:
- 一時的な認証情報
- 自動更新
- 組織管理

#### 4. 最小権限の原則

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
        "s3:List*"
      ],
      "Resource": "*"
    }
  ]
}
```

**利点**:
- 意図しない変更の防止
- セキュリティリスクの最小化

#### 5. 認証情報のローテーション

**定期的な更新**:
```bash
# 90日ごとにアクセスキーを更新
aws iam create-access-key --user-name my-user
aws iam delete-access-key --access-key-id OLD_KEY --user-name my-user
```

**利点**:
- セキュリティリスクの低減
- 漏洩時の影響を最小化

---

### ❌ 非推奨

#### 1. ファイルにハードコード

**悪い例**:
```python
# ❌ 絶対にやってはいけない
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

**リスク**:
- Gitにコミットされる可能性
- ソースコードに残る
- 漏洩リスクが高い

#### 2. Gitリポジトリにコミット

**悪い例**:
```bash
# ❌ 認証情報をコミット
git add .env
git commit -m "Add credentials"
```

**リスク**:
- 公開リポジトリで漏洩
- 履歴に永久に残る
- 削除が困難

#### 3. 過剰な権限付与

**悪い例**:
```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```

**リスク**:
- すべての操作が可能
- 意図しない変更
- セキュリティ侵害

#### 4. 長期的な認証情報の使用

**悪い例**:
```bash
# ❌ 5年前に作成したアクセスキーを使用
```

**リスク**:
- 漏洩リスクの蓄積
- 管理が困難
- セキュリティ脆弱性

---

## 🔧 環境変数の設定

### 一時的な認証情報

**設定**:
```bash
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_SESSION_TOKEN="..."
```

**確認**:
```bash
aws sts get-caller-identity
```

**有効期限**:
- セッション終了まで
- または明示的に削除

### プロファイルの使用

**設定ファイル**: `~/.aws/credentials`
```ini
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

[production]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE2
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY2
```

**使用**:
```bash
export AWS_PROFILE="production"
```

**利点**:
- 複数の環境を管理
- 簡単に切り替え可能

---

## 🔐 認証情報の保護

### .gitignoreへの追加

**`.gitignore`**:
```
# AWS認証情報
.env
.env.*
.aws/credentials
.aws/config

# 秘密鍵
*.pem
*.key
id_rsa
id_rsa.pub

# その他の機密ファイル
secrets.json
credentials.json
```

### 暗号化の使用

**AWS Secrets Manager**:
```bash
# シークレットの保存
aws secretsmanager create-secret \
  --name my-secret \
  --secret-string '{"username":"admin","password":"secret"}'

# シークレットの取得
aws secretsmanager get-secret-value --secret-id my-secret
```

**AWS Systems Manager Parameter Store**:
```bash
# パラメータの保存
aws ssm put-parameter \
  --name /myapp/database/password \
  --value "secret" \
  --type SecureString

# パラメータの取得
aws ssm get-parameter --name /myapp/database/password --with-decryption
```

### アクセス制限

**ファイルパーミッション**:
```bash
chmod 600 ~/.aws/credentials
chmod 600 ~/.ssh/id_rsa
```

**効果**:
- 所有者のみ読み書き可能
- 他のユーザーはアクセス不可

---

## 🛠️ トラブルシューティング

### 認証エラーの対処

**症状**:
```
Error: Unable to locate credentials
```

**原因**:
- 認証情報が設定されていない
- 環境変数が設定されていない

**対処**:
```bash
# 認証情報の確認
aws configure list

# 再設定
aws configure
```

### 権限不足の解決

**症状**:
```
Error: User is not authorized to perform: s3:ListBucket
```

**原因**:
- IAMポリシーで権限が付与されていない

**対処**:
```bash
# 現在の権限を確認
aws iam get-user-policy --user-name my-user --policy-name my-policy

# 必要な権限を追加
aws iam put-user-policy --user-name my-user --policy-name my-policy --policy-document file://policy.json
```

### セッション期限切れ

**症状**:
```
Error: The security token included in the request is expired
```

**原因**:
- 一時的な認証情報の有効期限切れ

**対処**:
```bash
# 再ログイン
aws sso login --profile my-sso-profile

# または新しい認証情報を取得
aws sts get-session-token
```

---

## 💡 エンタープライズ環境での推奨設定

### 1. IAM Identity Centerの使用

**設定**:
```bash
aws configure sso
# → 組織のSSO URLを入力
# → ロールを選択
```

**利点**:
- 一元管理
- 自動ローテーション
- 監査ログ

### 2. MFAの有効化

**設定**:
```bash
aws iam enable-mfa-device \
  --user-name my-user \
  --serial-number arn:aws:iam::123456789012:mfa/my-user \
  --authentication-code1 123456 \
  --authentication-code2 789012
```

**利点**:
- セキュリティ強化
- 不正アクセス防止

### 3. CloudTrailでの監視

**設定**:
```bash
aws cloudtrail create-trail \
  --name my-trail \
  --s3-bucket-name my-bucket
```

**利点**:
- API呼び出しの記録
- 異常検知
- コンプライアンス対応

---

## 🔗 関連ドキュメント

### セキュリティガイド
- [セキュリティ概要](01_security-overview.md)
- [ファイルアクセス制御](03_file-access-control.md)
- [AWS API制御](04_aws-api-control.md)

### 設定ガイド
- [インストールガイド](../01_getting-started/01_installation.md)
- [環境変数](../03_configuration/05_environment-variables.md)

### エンタープライズ展開
- [エンタープライズ導入ガイド](../05_deployment/01_enterprise-deployment.md)
- [セキュリティチェックリスト](../05_deployment/03_security-checklist.md)

### AWS公式ドキュメント
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)

---

## 📞 サポート

セキュリティ上の懸念や質問がある場合：

1. **AWS公式**: [AWS Security](https://aws.amazon.com/security/)
2. **GitHub**: [amazon-q-developer-cli/issues](https://github.com/aws/amazon-q-developer-cli/issues)
3. **ドキュメント**: [トラブルシューティング](../06_troubleshooting/02_common-issues.md)
