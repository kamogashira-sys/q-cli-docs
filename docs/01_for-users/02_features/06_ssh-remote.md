# SSH/リモートマシンでの使用

**最終更新**: 2025-10-11  
**対象バージョン**: v1.17.0以降

---

## 📋 概要

Amazon Q CLIはSSH経由でリモートマシンでも使用できます。このガイドでは、リモート環境でのセットアップと使用方法を説明します。

---

## 🎯 ユースケース

### 典型的なシナリオ
- リモートサーバーでの開発作業
- クラウドインスタンス（EC2など）での使用
- コンテナ内での開発
- SSH経由のリモートデスクトップ

---

## 🚀 セットアップ

### 前提条件

**ローカルマシン**:
- Amazon Q CLIがインストール済み
- 認証が完了している

**リモートマシン**:
- SSH接続が可能
- サポートされているOS（Linux/macOS）
- インターネット接続

---

### 方法1: リモートマシンに直接インストール

リモートマシンでAmazon Q CLIを直接インストールして使用します。

#### ステップ1: リモートマシンにSSH接続

```bash
ssh user@remote-host
```

#### ステップ2: Amazon Q CLIをインストール

```bash
# Linuxの場合
curl -fsSL https://desktop-release.q.us-east-1.amazonaws.com/latest/install.sh | bash

# macOSの場合
brew install --cask amazon-q
```

#### ステップ3: 認証

```bash
# デバイスフローで認証（ブラウザリダイレクトなし）
q login --use-device-flow

# 表示されたURLをローカルブラウザで開く
# 認証コードを入力
```

#### ステップ4: シェル統合

シェル統合は自動的に設定されます。手動で設定する場合：

```bash
# bashの場合
echo 'eval "$(q --shell-integration bash)"' >> ~/.bashrc
source ~/.bashrc

# zshの場合
echo 'eval "$(q --shell-integration zsh)"' >> ~/.zshrc
source ~/.zshrc
```

---

### 方法2: 設定ファイルの同期

ローカルの設定をリモートマシンに同期して使用します。

#### ステップ1: ローカルの設定をバックアップ

```bash
# 設定ディレクトリをアーカイブ
cd ~
tar czf amazonq-config.tar.gz .amazonq/

# リモートマシンに転送
scp amazonq-config.tar.gz user@remote-host:~/
```

#### ステップ2: リモートマシンで展開

```bash
# リモートマシンにSSH接続
ssh user@remote-host

# 設定を展開
cd ~
tar xzf amazonq-config.tar.gz

# Amazon Q CLIをインストール（方法1参照）
```

⚠️ **注意**: 認証トークンには有効期限があります。定期的に再認証が必要です。

---

## ⚙️ 設定

### 環境変数の設定

リモート環境で特定の設定が必要な場合、環境変数を使用します。

```bash
# ~/.bashrc または ~/.zshrc に追加

# プロキシ設定
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1

# Amazon Q CLI設定
export Q_DISABLE_TELEMETRY=true
export Q_LOG_LEVEL=info
```

---

### Agent設定の同期

Agent設定もリモートマシンで使用できます。

```bash
# ローカルのAgent設定を転送
scp ~/.config/amazonq/agents/my-agent.json user@remote-host:~/.config/amazonq/agents/

# リモートマシンで確認
q agent list
```

---

## トラブルシューティング

問題が発生した場合は、[トラブルシューティングガイド](../06_troubleshooting/02_common-issues.md)を参照してください。

**関連トピック**:
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)

---

### ネットワーク接続エラー

**症状**: "Unable to connect to Amazon Q" エラー

**原因**:
- ファイアウォール設定
- プロキシ設定が必要
- インターネット接続の問題

**解決方法**:
```bash
# 接続テスト
curl -I https://q.us-east-1.amazonaws.com

# プロキシ設定
export HTTPS_PROXY=http://proxy.example.com:8080

# 再試行
q whoami
```

---

### シェル統合が機能しない

**症状**: オートコンプリートが動作しない

**解決方法**:
```bash
# 診断ツールで確認
q diagnostic

# シェル統合を再設定
echo 'eval "$(q --shell-integration bash)"' >> ~/.bashrc
source ~/.bashrc

# 新しいセッションを開始
exec $SHELL
```

---

## 🔒 セキュリティ考慮事項

### 認証トークンの管理

⚠️ **重要**: 認証トークンは機密情報です

**ベストプラクティス**:
- 共有サーバーでは個人の認証情報のみを使用
- 定期的にトークンを更新
- 不要になったら必ずログアウト

```bash
# 使用後はログアウト
q logout
```

---

### 設定ファイルの権限

```bash
# 設定ディレクトリの権限を確認
ls -la ~/.config/amazonq/

# 適切な権限に設定
chmod 700 ~/.config/amazonq/
chmod 600 ~/.local/share/amazon-q/settings.json
```

---

## ベストプラクティス

詳細なベストプラクティスは以下を参照してください：
- [設定のベストプラクティス](../04_best-practices/01_configuration.md)
- [セキュリティベストプラクティス](../04_best-practices/02_security.md)
- [パフォーマンス最適化](../04_best-practices/03_performance.md)

---

## 📚 関連ドキュメント

- [インストールガイド](../01_getting-started/01_installation.md)
- [認証設定](../01_getting-started/02_quick-start.md#認証設定)
- [環境変数リファレンス](../03_configuration/05_environment-variables.md)
- [セキュリティベストプラクティス](../04_best-practices/02_security.md)

---

## 📚 参考リンク

### AWS公式ドキュメント
- [Amazon Q CLI ドキュメント](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html)
- [AWS Builder ID](https://docs.aws.amazon.com/general/latest/gr/aws_builder_id.html)

---

**作成日**: 2025-10-11  
**最終更新日**: 2025-10-11
