[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [セキュリティガイド](README.md)

---

# セキュリティ


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

| # | ドキュメント | 対象 | 内容 |
|---|-------------|------|------|
| 0 | [セキュリティアーキテクチャ設計思想](00_security-architecture.md) ⭐ | 中級〜上級 | 設計思想、ユーザーインストールの理由、AWS公式セキュリティモデル |
| 1 | [セキュリティ概要](01_security-overview.md) ⭐ | 初級〜中級 | AWS責任共有モデル、主要セキュリティトピック、環境別推奨設定 |
| 2 | [データプライバシー](02_data-privacy.md) | 初級〜中級 | Free vs Pro/Enterpriseプラン、サービス改善データ使用、オプトアウト |
| 3 | [ファイルアクセス制御](03_file-access-control.md) | 中級 | fs_readツール制御、機密ファイル保護、環境別設定 |
| 4 | [AWS API制御](04_aws-api-control.md) | 中級 | use_awsツール制御、IAMポリシー制限、コスト管理 |
| 5 | [認証情報管理](05_credentials-management.md) | 中級 | AWS Builder ID、IAM Identity Center、ベストプラクティス |
| 6 | [trust-all安全使用](06_trust-all-safety.md) | 中級〜上級 | trust-allの危険性、安全な使用方法、チェックリスト |

⭐ = まずここから！

### トピック別

#### 基本
- [セキュリティアーキテクチャ設計思想](00_security-architecture.md) - 設計思想とユーザーインストールの理由
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
4. **[テレメトリー設定](../03_configuration/05_telemetry.md)** を適用（5分）

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

> **💡 ファイルアクセス制限について**
> 
> `--untrust-fs-read`を設定すると、**Q CLIがファイルを読み込む前に、毎回あなたに確認を求める**ようになります。
> 
> **具体例**:
> ```bash
> # 設定なし: 自動実行
> q chat "config.jsonの内容を教えて"
> # → cat config.json が自動実行される
> 
> # 設定あり: 確認が必要
> alias q="q --untrust-fs-read"
> q chat "config.jsonの内容を教えて"
> # → ⚠️ このファイルを読み込みますか？ [y/n]
> ```
> 
> **保護される機密情報**:
> - 🔑 `.env` - 環境変数（APIキー、パスワード）
> - 🔑 `config/secrets.json` - 認証情報
> - 🔑 `~/.aws/credentials` - AWS認証情報
> - 🔑 `~/.ssh/id_rsa` - SSH秘密鍵
> - 📊 `customer_data.csv` - 顧客データ
> - ⚙️ `production.config` - 本番環境設定
> 
> **防止できるリスク**:
> - ❌ 機密情報の意図しない読み込み
> - ❌ 個人情報の漏洩
> - ❌ 大量ファイルの無制限アクセス
> 
> **対象操作**:
> - すべてのファイル読み込み（テキスト、JSON、YAML等）
> - サブディレクトリのファイルも含む
> 
> **推奨シーン**:
> - ✅ 機密情報を含むプロジェクト
> - ✅ 個人情報を扱うプロジェクト
> - ✅ 本番環境の設定ファイルを扱う
> - ✅ 複数のプロジェクトを同時に作業
> 
> **補足**: Q CLIはデフォルトで`~/.aws/credentials`、`~/.ssh/`、`.env`を保護していますが、`--untrust-fs-read`は**すべてのファイル**を保護します。
> 
> 詳細: [ファイルアクセス制御](03_file-access-control.md)

> **💡 AWS API制限について**
> 
> `--untrust-use-aws`を設定すると、**Q CLIがAWS APIを呼び出す前に、毎回あなたに確認を求める**ようになります。
> 
> **具体例**:
> ```bash
> # 設定なし: 自動実行
> q chat "S3バケット一覧を教えて"
> # → aws s3 ls が自動実行される
> 
> # 設定あり: 確認が必要
> alias q="q --untrust-use-aws"
> q chat "S3バケット一覧を教えて"
> # → ⚠️ このツールを実行しますか？ [y/n]
> ```
> 
> **防止できるリスク**:
> - ❌ 意図しないAWS操作（例: 本番環境のEC2停止）
> - ❌ 予期しないコスト発生（例: 大量のインスタンス起動）
> - ❌ セキュリティリスク（例: 権限設定の誤り）
> 
> **対象操作**:
> - すべてのAWSサービス（S3、EC2、Lambda、IAMなど）
> - 読み取り操作も含む（`aws s3 ls`など）
> 
> **推奨シーン**:
> - ✅ 本番環境での作業
> - ✅ 機密データを扱うプロジェクト
> - ✅ 複数のAWSアカウントを使用
> - ✅ コスト管理が重要な環境
> 
> 詳細: [AWS API制御](04_aws-api-control.md)

> **💡 テレメトリー無効化について**
> 
> `Q_TELEMETRY_ENABLED=false`を設定すると、以下のデータがAWSに送信されなくなります：
> - **使用状況データ**: コマンド実行回数、機能使用頻度、セッション時間
> - **パフォーマンスデータ**: 応答時間、API呼び出し回数
> - **設定データ**: 有効化されている機能、Agent/MCP使用状況
> - **環境データ**: OS情報、Q CLIバージョン
> 
> **送信されないデータ（元から収集されない）**:
> - コード内容、チャット内容、個人情報、プロジェクト情報
> 
> **注意点**:
> - ⚠️ テレメトリーデータはQ CLIの改善に使用されます
> - ⚠️ 問題発生時、テレメトリーデータがあるとサポートが容易になります
> - ✅ 収集されるデータは匿名化されています
> 
> 詳細: [データプライバシー](02_data-privacy.md)

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
- [テレメトリー設定](../03_configuration/05_telemetry.md)
- [Agent設定](../03_configuration/03_agent-configuration.md)
- [環境変数](../03_configuration/06_environment-variables.md)

### エンタープライズ展開
- [エンタープライズ導入ガイド](../05_deployment/01_enterprise-deployment.md)
- [料金プラン比較](../05_deployment/02_pricing-comparison.md)
- [セキュリティチェックリスト](../05_deployment/03_security-checklist.md)

### ベストプラクティス
- [セキュリティベストプラクティス](../04_best-practices/02_security.md)

### その他
- [クイックリファレンス](../07_reference/08_quick-reference.md)
- [トピック別インデックス](../07_reference/09_topic-index.md)


**ドキュメント対象バージョン**: v1.13.0以降

> **Note**: 本サイトではv1.13.0以降のセキュリティ情報を対象に記述しています。

---

最終更新: 2025-11-01
