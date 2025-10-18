[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [セキュリティガイド](README.md) > 06 Trust All Safety

---

# trust-all安全使用ガイド

**最終更新**: 2025-10-18  
**対象**: Amazon Q Developer CLI

---

## 📋 概要

このガイドは、Amazon Q Developer CLIの`/tools trust-all`コマンドの危険性と安全な使用方法を説明します。

---

## 🎯 trust-allとは

### 機能

`/tools trust-all`は、すべてのツール確認プロンプトをバイパスする機能です。

**別名**:
- `/acceptall`
- `/tools trust-all`

**動作**:
```bash
Amazon Q> /tools trust-all

# 以降、すべてのツール実行が確認なしで実行される
Amazon Q> ファイルを削除して
# → 確認なしで即座に削除される
```

---

## ⚠️ セキュリティリスク

### 高リスク

| リスク | 説明 | 影響 |
|--------|------|------|
| **意図しないシステム変更** | ファイル削除、設定変更 | **データ損失** |
| **データ損失** | 重要ファイルの削除 | **復旧不可** |
| **セキュリティ脆弱性** | セキュリティ設定の変更 | **侵害リスク** |
| **予期しないコスト** | AWSリソースの大量作成 | **高額請求** |

---

## 💥 具体的な危険例

### 例1: ファイルの意図しない削除

**シナリオ**:
```bash
Amazon Q> /tools trust-all
Amazon Q> 古いログファイルを削除して

# 実行されるコマンド
rm -rf /var/log/*
# → すべてのログファイルが削除される（確認なし）
```

**影響**:
- システムログの消失
- トラブルシューティング不可
- コンプライアンス違反

### 例2: AWSリソースの大量作成

**シナリオ**:
```bash
Amazon Q> /tools trust-all
Amazon Q> テスト用のEC2インスタンスを起動して

# 実行されるコマンド
aws ec2 run-instances --instance-type m5.24xlarge --count 100
# → 100台の高額インスタンスが起動される（確認なし）
```

**コスト**: $460.8/時間 = $331,776/月

### 例3: 設定ファイルの上書き

**シナリオ**:
```bash
Amazon Q> /tools trust-all
Amazon Q> 設定ファイルを更新して

# 実行されるコマンド
cat > /etc/nginx/nginx.conf << EOF
# 新しい設定
EOF
# → 本番環境の設定が上書きされる（確認なし）
```

**影響**:
- サービス停止
- 設定の消失
- 復旧困難

### 例4: 機密情報の漏洩

**シナリオ**:
```bash
Amazon Q> /tools trust-all
Amazon Q> 環境変数を確認して

# 実行されるコマンド
cat .env
# → 機密情報がチャット履歴に残る（確認なし）
```

**影響**:
- パスワード漏洩
- APIキー漏洩
- セキュリティ侵害

---

## 📜 AWS公式推奨

### 公式ガイドライン

> `/tools trust-all`または`/acceptall`モードは、本番環境や機密データを扱う環境では使用しないことを推奨します。

**出典**: [Security considerations and best practices](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-chat-security.html)

### 推奨事項

- ❌ 本番環境での使用禁止
- ❌ 機密環境での使用禁止
- ✅ 開発環境のみ使用
- ✅ 特定タスクのみ有効化
- ✅ タスク完了後すぐに無効化

---

## 🛡️ 安全な使用方法

### 1. 環境を限定

#### ✅ 使用可能な環境

- **開発環境**: ローカルマシン、開発サーバー
- **テスト環境**: 隔離されたテスト環境
- **サンドボックス**: 実験用の環境

#### ❌ 使用禁止の環境

- **本番環境**: 顧客データを扱う環境
- **ステージング環境**: 本番に近い環境
- **機密環境**: 機密情報を扱う環境
- **共有環境**: 複数人が使用する環境

### 2. 特定タスクのみ有効化

**推奨パターン**:
```bash
# タスク開始時に有効化
Amazon Q> /tools trust-all

# タスク実行
Amazon Q> 複数のファイルを処理して

# タスク完了後すぐに無効化
Amazon Q> /tools reset
```

**効果**:
- リスクを最小限に抑える
- 意図しない実行を防止

### 3. 監視とログ

**実行内容の記録**:
```bash
# チャット履歴を保存
q chat --save-history

# ログファイルの確認
tail -f ~/.q/logs/chat.log
```

**効果**:
- 実行内容の追跡
- 問題発生時の調査

---

## 🔄 代替手段

### 個別ツールの信頼

**推奨**:
```bash
# 特定ツールのみ信頼
Amazon Q> /tools trust fs_read

# 効果: fs_readのみ確認なしで実行
```

**利点**:
- リスクを限定
- 柔軟性を維持

### Agent設定での制御

**`.q/agent.json`**:
```json
{
  "name": "safe-project",
  "trustedTools": ["fs_read"],
  "untrustedTools": ["use_aws", "execute_bash"]
}
```

**効果**:
- プロジェクトごとに設定
- チーム全体で共有

### セッションごとの設定

**推奨**:
```bash
# セッション開始時に設定
q chat
Amazon Q> /tools trust fs_read
Amazon Q> /tools untrust use_aws
```

**効果**:
- セッションごとに制御
- 柔軟な設定

---

## 🚨 緊急時の対処

### trust-allを無効化

**即座に無効化**:
```bash
Amazon Q> /tools reset
```

**効果**:
- すべてのツールが制限される
- デフォルト状態に戻る

### セッションの終了

**強制終了**:
```bash
Amazon Q> /quit

# またはCtrl+C
```

**効果**:
- セッションが終了
- trust-all設定も消える

### 実行の取り消し

**可能な場合**:
```bash
# ファイル削除の取り消し
git restore deleted-file.txt

# AWSリソースの削除
aws ec2 terminate-instances --instance-ids i-xxxxx
```

---

## ✅ 使用前チェックリスト

trust-allを使用する前に、以下を確認してください：

- [ ] **環境**: 開発環境またはテスト環境である
- [ ] **データ**: 機密データを扱わない
- [ ] **本番**: 本番環境ではない
- [ ] **無効化**: タスク完了後に無効化する予定がある
- [ ] **監視**: 実行内容を監視できる
- [ ] **バックアップ**: 重要なデータのバックアップがある
- [ ] **権限**: 最小権限の原則を適用している
- [ ] **理解**: リスクを理解している

**すべてにチェックが入らない場合は使用を控えてください。**

---

## 🛠️ トラブルシューティング

### 意図しない変更が発生した

**対処**:
```bash
# 1. すぐに無効化
Amazon Q> /tools reset

# 2. セッションを終了
Amazon Q> /quit

# 3. 変更を確認
git status
aws ec2 describe-instances

# 4. 必要に応じて復旧
git restore .
aws ec2 terminate-instances --instance-ids i-xxxxx
```

### trust-allが無効化できない

**対処**:
```bash
# セッションを強制終了
Ctrl+C

# 新しいセッションを開始
q chat

# デフォルト状態を確認
Amazon Q> /tools list
```

### セキュリティインシデントの報告

**手順**:
1. **即座に無効化**: `/tools reset`
2. **セッション終了**: `/quit`
3. **影響範囲の確認**: ログ、リソース、ファイル
4. **報告**: セキュリティチームに連絡
5. **対策**: 再発防止策の実施

---

## 💡 ベストプラクティス

### 1. デフォルトで制限

**推奨設定**:
```bash
# シェル設定ファイル
alias q="q --untrust-all-tools"
```

**効果**:
- すべてのツールが制限される
- 意図的に許可する必要がある

### 2. プロジェクトごとの設定

**Agent設定**:
```json
{
  "name": "production-app",
  "untrustedTools": ["use_aws", "execute_bash", "fs_write"],
  "description": "本番環境用の厳格な設定"
}
```

**効果**:
- プロジェクトに応じた設定
- チーム全体で共有

### 3. 定期的な確認

**確認コマンド**:
```bash
Amazon Q> /tools list
# → 現在の信頼状態を確認
```

**頻度**: セッション開始時、重要な操作前

---

## 🔗 関連ドキュメント

### セキュリティガイド
- [セキュリティ概要](01_security-overview.md)
- [ファイルアクセス制御](03_file-access-control.md)
- [AWS API制御](04_aws-api-control.md)

### 設定ガイド
- [Agent設定](../03_configuration/04_agent-configuration.md)
- [環境変数](../03_configuration/05_environment-variables.md)

### エンタープライズ展開
- [セキュリティチェックリスト](../05_deployment/03_security-checklist.md)
- [エンタープライズ導入ガイド](../05_deployment/01_enterprise-deployment.md)

### AWS公式ドキュメント
- [Security considerations and best practices](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-chat-security.html)

---

## 📞 サポート

セキュリティ上の懸念や質問がある場合：

1. **AWS公式**: [AWS Security](https://aws.amazon.com/security/)
2. **GitHub**: [amazon-q-developer-cli/issues](https://github.com/aws/amazon-q-developer-cli/issues)
3. **ドキュメント**: [トラブルシューティング](../06_troubleshooting/02_common-issues.md)

---

## 📖 ナビゲーション

← **前へ**: [認証情報管理](05_credentials-management.md)

---

**最終更新**: 2025-10-18
