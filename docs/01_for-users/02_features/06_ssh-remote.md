[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [機能ガイド](README.md) > 06 Ssh Remote

---

# SSH/リモートマシンでの使用

**ドキュメント対象バージョン**: v1.13.0以降

> **Note**: SSH/リモート機能の実装時期は調査範囲外です。
> 本サイトではv1.13.0以降の機能を対象に記述しています。

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

## 🔧 SSH統合のセットアップ

Amazon Q CLIは、ローカルマシンとリモートマシン間でSSH統合を提供します。この機能により、ローカルのAmazon Q CLIからリモートマシン上でコマンドを実行できます。

### ローカルマシン（macOS）の設定

ローカルmacOSマシンからSSH統合を有効にします：

```bash
q integrations install ssh
```

### リモートマシン（Linux）の設定

リモートLinuxマシンでSSH統合を設定します：

#### ステップ1: SSH server設定を編集

```bash
sudo -e /etc/ssh/sshd_config
```

#### ステップ2: 設定を追加

ファイルの末尾に以下を追加：

```
AcceptEnv Q_SET_PARENT
AllowStreamLocalForwarding yes
```

**設定の説明**:
- `AcceptEnv Q_SET_PARENT`: Amazon Q CLIが必要とする環境変数を受け入れる
- `AllowStreamLocalForwarding yes`: ローカルストリーム転送を許可

#### ステップ3: SSH serviceを再起動

```bash
sudo systemctl restart sshd
```

#### ステップ4: SSH再接続

現在のSSHセッションを終了し、再接続します。

#### ステップ5: Amazon Q CLIにログイン

```bash
q login
```

#### ステップ6: 確認

```bash
q doctor
```

### 既知の制限事項

**症状**: Amazon Q desktop clientが終了すると、以下のエラーメッセージが繰り返し表示される：

```
connect to /var/folders/.../cwrun/remote.sock port -2 failed: Connection refused
```

**解決方法**:
- SSHセッションを終了して再接続
- または、Amazon Q desktop clientを再起動

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

**Linux x86-64の場合**:

```bash
# 1. ZIPファイルをダウンロード
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux.zip" \
  -o "q.zip"

# 2. 解凍
unzip q.zip

# 3. インストール（~/.local/binにインストール）
./q/install.sh
```

**Linux ARM (aarch64)の場合**:

```bash
# 1. ZIPファイルをダウンロード
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-aarch64-linux.zip" \
  -o "q.zip"

# 2. 解凍
unzip q.zip

# 3. インストール
./q/install.sh
```

**古いglibc環境（glibc < 2.34）の場合**:

```bash
# glibc バージョン確認
ldd --version

# musl版をダウンロード（x86-64）
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux-musl.zip" \
  -o "q.zip"

# または musl版（ARM）
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-aarch64-linux-musl.zip" \
  -o "q.zip"

# 解凍とインストール
unzip q.zip
./q/install.sh
```

**macOSの場合**:

```bash
# Homebrewでインストール
brew install --cask amazon-q
```

> **💡 ヒント**: SSH環境ではGUI不要の最小版（ZIP）を使用します。デフォルトで`~/.local/bin`にインストールされるため、root権限は不要です。

#### ステップ3: 認証

```bash
# 認証
q login

# 表示されたURLをローカルブラウザで開く
# 認証コードを入力
```

#### ステップ4: シェル統合

シェル統合は自動的に設定されます。手動で設定する場合：

```bash
# bashの場合
echo 'eval "$(q init bash)"' >> ~/.bashrc
source ~/.bashrc

# zshの場合
echo 'eval "$(q init zsh)"' >> ~/.zshrc
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
scp ~/.aws/amazonq/cli-agents/my-agent.json user@remote-host:~/.aws/amazonq/cli-agents/

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

### SSH統合の問題

**症状**: SSH統合が機能しない

**解決方法**:

1. **診断ツールで確認**:
```bash
q doctor
```

2. **ローカルとリモートの設定を確認**:
   - ローカル（macOS）: `q integrations install ssh`が実行済みか
   - リモート（Linux）: sshd_configに必要な設定が追加されているか

3. **SSH server設定を確認**:
```bash
# リモートマシンで確認
sudo grep -E "AcceptEnv|AllowStreamLocalForwarding" /etc/ssh/sshd_config
```

期待される出力:
```
AcceptEnv Q_SET_PARENT
AllowStreamLocalForwarding yes
```

4. **正しいバージョンを使用しているか確認**:
   - glibc 2.34+: 標準版
   - glibc < 2.34: musl版

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
- [認証設定](../01_getting-started/01_installation.md#-認証設定)
- [環境変数リファレンス](../03_configuration/06_environment-variables.md)
- [セキュリティベストプラクティス](../04_best-practices/02_security.md)

---

## 📚 参考リンク

### AWS公式ドキュメント
- [Amazon Q CLI ドキュメント](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html)
- [AWS Builder ID](https://docs.aws.amazon.com/general/latest/gr/aws_builder_id.html)

---


---

最終更新: 2025-11-01
