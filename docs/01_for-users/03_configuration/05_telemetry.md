[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [設定ガイド](README.md) > 06 Telemetry

---

# テレメトリー設定ガイド

最終更新: 2025-10-18  
**対象**: Amazon Q Developer CLI

---

## 📋 概要

このガイドは、Amazon Q Developer CLIのテレメトリー設定について説明します。

---

## 🎯 テレメトリーとは

### 収集されるデータ

**テレメトリーデータの種類**:

| カテゴリ | 内容 | 例 |
|---------|------|-----|
| **使用統計** | コマンド実行回数、機能使用頻度 | `q chat`実行回数、Agent使用回数 |
| **エラーレポート** | エラーの種類、発生頻度 | クラッシュレポート、API エラー |
| **パフォーマンス** | 応答時間、リソース使用量 | 平均応答時間、メモリ使用量 |
| **環境情報** | OS、バージョン、設定 | macOS 14.0、Q CLI v1.18.1 |

### 収集されないデータ

**プライバシー保護**:
- ❌ ファイルの内容
- ❌ コードの内容
- ❌ プロジェクトの詳細
- ❌ 個人を特定できる情報（PII）

---

## 🔒 プラン別のデータ使用

### Freeプラン

**質問内容と応答**:
- ✅ サービス改善に使用される可能性あり
- ✅ オプトアウト可能

**テレメトリーデータ**:
- ✅ 使用統計、エラーレポート等
- ✅ オプトアウト可能

### Pro/Enterpriseプラン

**質問内容と応答**:
- ❌ サービス改善に使用されない
- ✅ デフォルトで保護

**テレメトリーデータ**:
- ✅ 使用統計、エラーレポート等
- ✅ オプトアウト可能

**詳細**: [データプライバシーガイド](../09_security/02_data-privacy.md)

---

## ⚙️ テレメトリー設定方法

### 方法1: 環境変数（推奨）

#### 無効化

```bash
# テレメトリーを無効化
export Q_TELEMETRY_ENABLED=false

# 永続化（bash）
echo 'export Q_TELEMETRY_ENABLED=false' >> ~/.bashrc
source ~/.bashrc

# 永続化（zsh）
echo 'export Q_TELEMETRY_ENABLED=false' >> ~/.zshrc
source ~/.zshrc
```

#### 有効化

```bash
# テレメトリーを有効化
export Q_TELEMETRY_ENABLED=true
```

---

### 方法2: グローバル設定ファイル

**ファイルパス**: `~/.amazonq/settings.yml`

```yaml
# テレメトリーを無効化
telemetry:
  enabled: false
```

**設定の確認**:
```bash
cat ~/.amazonq/settings.yml
```

---

### 方法3: Agent設定ファイル

**ファイルパス**: `.amazonq/agent.yml`（プロジェクトルート）

```yaml
# プロジェクト固有の設定
telemetry:
  enabled: false
```

**用途**: 特定のプロジェクトでのみテレメトリーを無効化

---

## 📊 設定の優先順位

設定は以下の優先順位で適用されます：

1. **環境変数** (`Q_TELEMETRY_ENABLED`)
2. **Agent設定** (`.amazonq/agent.yml`)
3. **グローバル設定** (`~/.amazonq/settings.yml`)
4. **デフォルト値** (有効)

**例**:
```bash
# 環境変数が最優先
export Q_TELEMETRY_ENABLED=false  # ← これが適用される

# Agent設定（無視される）
# .amazonq/agent.yml: telemetry.enabled=true

# グローバル設定（無視される）
# ~/.amazonq/settings.yml: telemetry.enabled=true
```

---

## 🔍 現在の設定確認

### 環境変数の確認

```bash
# テレメトリー設定を確認
echo $Q_TELEMETRY_ENABLED

# 出力例:
# false  → 無効
# true   → 有効
# (空)   → デフォルト（有効）
```

### 設定ファイルの確認

```bash
# グローバル設定
cat ~/.amazonq/settings.yml

# Agent設定
cat .amazonq/agent.yml
```

---

## 🎯 推奨設定

### 個人開発・学習

**推奨**: テレメトリー有効（デフォルト）

**理由**:
- サービス改善に貢献
- より良い機能開発につながる
- プライバシーは保護される（コンテンツは含まれない）

---

### 商用開発・機密情報

**推奨**: テレメトリー無効 + Pro/Enterpriseプラン

**設定**:
```bash
# 環境変数で無効化
export Q_TELEMETRY_ENABLED=false

# または グローバル設定
cat > ~/.amazonq/settings.yml << EOF
telemetry:
  enabled: false
EOF
```

**理由**:
- 最大限のプライバシー保護
- コンプライアンス要件への対応
- 企業ポリシーへの準拠

---

### エンタープライズ環境

**推奨**: 組織ポリシーで一括管理

**AWS Organizations設定**:
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

**詳細**: [AI services opt-out policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_ai-opt-out.html)

---

## 🛡️ セキュリティとプライバシー

### テレメトリーデータの保護

**暗号化**:
- ✅ 転送中: TLS 1.2以上
- ✅ 保管時: AWS KMS

**アクセス制御**:
- ✅ AWS内部のみアクセス可能
- ✅ 厳格なアクセス管理

**保存期間**:
- ✅ 必要最小限の期間
- ✅ 定期的な削除

---

### データの使用目的

**許可される使用**:
- ✅ サービスの改善
- ✅ バグの修正
- ✅ パフォーマンスの最適化
- ✅ 新機能の開発

**許可されない使用**:
- ❌ 第三者への販売
- ❌ 広告目的
- ❌ 個人の特定

---

## 📋 トラブルシューティング

### 設定が反映されない

**確認事項**:

1. **環境変数の確認**
   ```bash
   echo $Q_TELEMETRY_ENABLED
   ```

2. **設定ファイルの構文確認**
   ```bash
   # YAMLの構文チェック
   python3 -c "import yaml; yaml.safe_load(open('~/.amazonq/settings.yml'))"
   ```

3. **Q CLIの再起動**
   ```bash
   # セッションを終了して再起動
   exit
   q chat
   ```

---

### テレメトリーが送信されているか確認

**ネットワークトラフィックの監視**:
```bash
# macOS/Linux
sudo tcpdump -i any -n host telemetry.amazonq.aws

# 出力があればテレメトリーが送信されている
```

---

## 🔗 関連ドキュメント

### セキュリティガイド
- [セキュリティ概要](../09_security/01_security-overview.md)
- [データプライバシーガイド](../09_security/02_data-privacy.md)

### 設定ガイド
- [設定概要](01_overview.md)
- [設定優先順位](07_priority-rules.md)
- [環境変数](06_environment-variables.md)
- [Agent設定](03_agent-configuration.md)

### AWS公式ドキュメント
- [Amazon Q Developer service improvement](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/service-improvement.html)
- [Opt out of data sharing](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/opt-out-IDE.html)

---

## ❓ よくある質問

### Q1: テレメトリーを無効にすると機能が制限されますか？

**A**: いいえ、全機能を使用できます。テレメトリーは使用統計の収集のみで、機能には影響しません。

---

### Q2: テレメトリーとサービス改善用データの違いは？

**A**: 
- **テレメトリー**: 使用統計、エラーレポート（全プラン）
- **サービス改善用データ**: 質問内容、応答内容（Freeプランのみ）

---

### Q3: 一時的にテレメトリーを有効化できますか？

**A**: はい、環境変数で制御できます：
```bash
# 一時的に有効化
Q_TELEMETRY_ENABLED=true q chat

# 次回は無効（環境変数が設定されていない場合）
q chat
```

---

### Q4: 組織全体でテレメトリーを無効化できますか？

**A**: はい、AWS Organizationsのポリシーで一括管理できます。詳細は[AI services opt-out policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_ai-opt-out.html)を参照してください。

---

**参考資料**:
- [AWS Data Privacy FAQ](https://aws.amazon.com/compliance/data-privacy-faq/)
- [AWS Compliance Programs](https://aws.amazon.com/compliance/programs/)

## 関連ドキュメント

- [テレメトリー設定](../03_configuration/05_telemetry.md) - テレメトリー設定の完全ガイド
