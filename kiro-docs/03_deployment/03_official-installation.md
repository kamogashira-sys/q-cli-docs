[ホーム](../README.md) > [デプロイメント](README.md) > 公式インストール手順

# 公式インストール手順（Kiro CLI）

**出典**: [Installation - Kiro CLI Documentation](https://kiro.dev/docs/cli/installation/)（公式ページ最終更新: 2026-04-24）

## 概要

### 公式インストール手順とは

Kiro CLI を OS 別に **公式手順でインストール** するためのガイドです。Kiro CLI は **macOS / Windows 11 / Linux**（AppImage、zip、Ubuntu .deb）を公式にサポートします。

### 主な特徴

- ✅ **マルチプラットフォーム対応**: macOS、Windows 11、Linux 各種ディストリビューション
- ✅ **アーキテクチャ対応**: x86_64（Intel/AMD）と aarch64（ARM）両方
- ✅ **glibc 分岐**: glibc 2.34+ 標準版と、それ以前向けの **musl 版** を提供
- ✅ **Auto-update**: バックグラウンドで自動更新（Windows）
- ✅ **エンタープライズ対応**: HTTP/HTTPS プロキシ、Basic 認証付プロキシをサポート（v1.8.0+）
- ✅ **セルフ診断**: `kiro-cli doctor` で問題自動検出

### なぜ公式手順が必要なのか

Kiro CLI は **AWS Builder ID / IAM Identity Center / Google / GitHub** 等での認証を伴うため、信頼性の高い配布チャネルからのインストールが重要です。本ドキュメントは公式 [Installation](https://kiro.dev/docs/cli/installation/) ページの**日本語訳・補足版** であり、最新版は常に公式ページを参照することを推奨します。

---

## 📋 目次

- [macOS インストール](#macos-インストール)
- [Windows 11 インストール](#windows-11-インストール)
- [Linux AppImage インストール](#linux-appimage-インストール)
- [Linux zip ファイルインストール](#linux-zip-ファイルインストール)
- [Ubuntu インストール](#ubuntu-インストール)
- [Proxy 設定](#proxy-設定)
- [アンインストール](#アンインストール)
- [デバッグとトラブルシューティング](#デバッグとトラブルシューティング)
- [ユースケース](#ユースケース)
- [関連リンク](#関連リンク)

---

## macOS インストール

**出典**: [macOS](https://kiro.dev/docs/cli/installation/#macos)

コマンドラインから macOS に **ネイティブインストール** できます。

### インストールコマンド

```bash
curl -fsSL https://cli.kiro.dev/install | bash
```

インストール完了後、Kiro が **Web ブラウザを自動で開き**、認証手順に進みます（[Authentication](https://kiro.dev/docs/cli/authentication/) 参照）。

### 動作確認

```bash
kiro-cli --version
kiro-cli doctor
```

`Everything looks good!` が表示されれば正常です。

---

## Windows 11 インストール

**出典**: [Windows](https://kiro.dev/docs/cli/installation/#windows)

PowerShell を使い Windows 11 にインストール可能です（v2.0.0 以降で公式対応）。

### インストールコマンド

**Windows Terminal**（推奨）または PowerShell ターミナルで実行：

```powershell
irm 'https://cli.kiro.dev/install.ps1' | iex
```

> ⚠️ **要件**:
> - **Windows 11 が必須**（Windows 10 非対応）
> - **Windows Terminal または PowerShell** で実行（Command Prompt は不可）
> - 最良の Terminal UI 体験のため Windows Terminal を推奨

### Auto Update（自動更新）

Kiro CLI は **バックグラウンドで自動更新** します。新バージョンが利用可能になると静かにダウンロードされ、アプリ終了時にインストールされます。

#### 自動更新の無効化

```powershell
kiro-cli settings "app.disableAutoupdates" "true"
```

→ 詳細設定: [04_reference/01_settings.md](../04_reference/01_settings.md)

### Windows でのアンインストール

**Windows 設定 > アプリ** から削除、または：

```powershell
kiro-cli uninstall
```

---

## Linux AppImage インストール

**出典**: [Linux AppImage](https://kiro.dev/docs/cli/installation/#linux-appimage)

AppImage はインストール不要で **大半の Linux ディストリビューションで動作** するポータブル形式です。

### インストール手順

```bash
# 1. AppImage をダウンロード
curl -L 'https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.appimage' \
  -o kiro-cli.appimage

# 2. 実行権限を付与
chmod +x kiro-cli.appimage

# 3. 実行
./kiro-cli.appimage
```

実行後、Web ブラウザで認証手順を完了します。

> **対応ディストリビューション**: Red Hat Enterprise Linux (RHEL) を含む全主要 Linux ディストリビューションで Terminal UI がサポートされます。

---

## Linux zip ファイルインストール

**出典**: [With a zip file](https://kiro.dev/docs/cli/installation/#with-a-zip-file)

zip ファイルから手動でインストールする方式。AppImage が使えない環境向けです。

### 要件

| 要件 | 説明 |
|------|------|
| unzip コマンド | OS 標準の解凍ツール（または互換ツール） |
| **glibc 2.34 以降**（標準版） | 2021 年以降の主要 Linux ディストリビューションに同梱 |
| **musl 版**（glibc 2.34 未満用） | ファイル名に `-musl.zip` が含まれる版を使用 |
| アーキテクチャ | x86_64（Intel/AMD 64bit）または aarch64（ARM 64bit） |

### サポート対象ディストリビューション

最新の Fedora / Ubuntu / Amazon Linux 2023（64bit x86_64 および ARM aarch64）

### glibc バージョンの確認

```bash
ldd --version
```

- `2.34` 以上 → **標準版** を使用
- `2.34` 未満 → **musl 版** を使用

### ダウンロード URL

#### 標準版（glibc 2.34+）

```bash
# Linux x86_64
curl --proto '=https' --tlsv1.2 -sSf \
  'https://desktop-release.q.us-east-1.amazonaws.com/latest/kirocli-x86_64-linux.zip' \
  -o 'kirocli.zip'

# Linux ARM (aarch64)
curl --proto '=https' --tlsv1.2 -sSf \
  'https://desktop-release.q.us-east-1.amazonaws.com/latest/kirocli-aarch64-linux.zip' \
  -o 'kirocli.zip'
```

#### Musl 版（glibc < 2.34）

```bash
# Linux x86_64 (musl)
curl --proto '=https' --tlsv1.2 -sSf \
  'https://desktop-release.q.us-east-1.amazonaws.com/latest/kirocli-x86_64-linux-musl.zip' \
  -o 'kirocli.zip'

# Linux ARM aarch64 (musl)
curl --proto '=https' --tlsv1.2 -sSf \
  'https://desktop-release.q.us-east-1.amazonaws.com/latest/kirocli-aarch64-linux-musl.zip' \
  -o 'kirocli.zip'
```

### インストール手順

```bash
# 1. 解凍
unzip kirocli.zip

# 2. インストールスクリプト実行
./kirocli/install.sh
```

> **既定インストール先**: `~/.local/bin`

---

## Ubuntu インストール

**出典**: [Ubuntu](https://kiro.dev/docs/cli/installation/#ubuntu)

Ubuntu 向けの **.deb パッケージ** を提供しています。

### インストール手順

```bash
# 1. .deb をダウンロード
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.deb

# 2. インストール（依存関係解決含む）
sudo dpkg -i kiro-cli.deb
sudo apt-get install -f

# 3. 起動
kiro-cli
```

実行後、Web ブラウザで認証手順を完了します。

---

## Proxy 設定

**出典**: [Proxy configuration](https://kiro.dev/docs/cli/installation/#proxy-configuration)

Kiro CLI（**v1.8.0 以降**）は、エンタープライズ環境で一般的なプロキシサーバーをサポートします。**標準的なプロキシ環境変数を自動的に尊重** します。

### 環境変数の設定

```bash
# HTTP プロキシ（非SSL通信）
export HTTP_PROXY=http://proxy.company.com:8080

# HTTPS プロキシ（SSL通信）
export HTTPS_PROXY=http://proxy.company.com:8080

# プロキシをバイパスするドメイン
export NO_PROXY=localhost,127.0.0.1,.company.com
```

### Basic 認証付きプロキシ

認証が必要なプロキシの場合：

```bash
export HTTP_PROXY=http://username:password@proxy.company.com:8080
export HTTPS_PROXY=http://username:password@proxy.company.com:8080
```

> ⚠️ **セキュリティ上の注意**: 平文パスワードを環境変数に含めるため、シェル履歴やプロセス一覧に露出する可能性があります。エンタープライズ環境では **専用の認証エージェント** または **シークレットマネージャー** の使用を検討してください。

### プロキシ問題のトラブルシューティング

| 症状 | 確認事項 |
|-----|--------|
| 接続失敗 | プロキシサーバーへの到達性、認証情報の正しさ |
| AWS エンドポイント拒否 | ファイアウォールが AWS エンドポイントへの接続を許可しているか |
| SSL 証明書検証失敗 | IT 管理者に証明書の信頼設定を依頼 |
| 特定プロトコル拒否 | プロキシが必要なプロトコル（HTTPS、WebSocket 等）をサポートしているか |

---

## アンインストール

**出典**: [Uninstalling Kiro CLI](https://kiro.dev/docs/cli/installation/#uninstalling-kiro-cli)

### macOS

```bash
kiro-cli uninstall
```

### Ubuntu

```bash
# パッケージを削除
sudo apt-get remove kiro-cli

# 残った設定ファイルも削除する場合
sudo apt-get purge kiro-cli
```

### Windows

```powershell
kiro-cli uninstall
```

または **Windows 設定 > アプリ** から削除。

---

## デバッグとトラブルシューティング

**出典**: [Debugging Kiro CLI](https://kiro.dev/docs/cli/installation/#debugging-kiro-cli)

### 自動診断: `kiro-cli doctor`

```bash
kiro-cli doctor
```

#### 期待される出力

```
$ kiro-cli doctor

✔ Everything looks good!

Kiro CLI still not working? Run kiro-cli issue to let us know!
```

問題があれば、プロンプトの指示に従って解決します。それでも解決しない場合は `kiro-cli issue` でバグレポートを作成。

### ログファイルの場所

| プラットフォーム | パス |
|--------------|-----|
| **macOS** | `$TMPDIR/kiro-log/kiro-chat.log` |
| **Linux** | `$XDG_RUNTIME_DIR/kiro-log/kiro-chat.log` |
| **Windows** | `%TEMP%\kiro-log\logs\kiro-chat.log` |

### ログパスの上書き

`KIRO_CHAT_LOG_FILE` 環境変数で任意の場所に出力できます。

```bash
# Linux/macOS
KIRO_CHAT_LOG_FILE=/tmp/my-debug.log kiro-cli chat
```

```powershell
# Windows (PowerShell)
$env:KIRO_CHAT_LOG_FILE = "C:\temp\my-debug.log"
kiro-cli chat
```

### よくある問題

| 症状 | 解決方法 |
|------|--------|
| **認証失敗** | `kiro-cli login` で再認証 |
| **オートコンプリートが動作しない** | `kiro-cli doctor` でシェル統合を確認 |
| **SSH 統合の問題** | SSH サーバーが必要な環境変数を受け入れる設定か確認 |

### 推奨トラブルシューティング手順

1. **`kiro-cli doctor`** を実行して一般的な問題を自動検出・修正
2. **インターネット接続** を確認
3. **対応環境** を使用しているか確認（[Supported command line environments](https://kiro.dev/docs/cli/reference/cli-commands/) 参照）
4. **再インストール** を試行
5. それでも解決しない場合、**`kiro-cli issue`** でバグ報告

---

## ユースケース

### ユースケース 1: 開発者のローカル環境セットアップ

開発者が macOS でゼロから Kiro CLI をセットアップ：

```bash
# 1. インストール
curl -fsSL https://cli.kiro.dev/install | bash

# 2. 認証（自動でブラウザが開く）
kiro-cli login

# 3. 動作確認
kiro-cli doctor
kiro-cli chat
```

### ユースケース 2: エンタープライズプロキシ環境

社内プロキシ経由で Linux サーバーから Kiro CLI を利用：

```bash
# 1. プロキシ環境変数を ~/.bashrc に追加
echo 'export HTTPS_PROXY=http://proxy.company.com:8080' >> ~/.bashrc
echo 'export NO_PROXY=localhost,127.0.0.1,.company.com' >> ~/.bashrc
source ~/.bashrc

# 2. AppImage で導入（インストール権限不要）
curl -L 'https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.appimage' \
  -o kiro-cli.appimage
chmod +x kiro-cli.appimage
./kiro-cli.appimage
```

### ユースケース 3: 古い CentOS / RHEL 環境

glibc 2.34 未満の環境では musl 版を使用：

```bash
# glibc バージョン確認
ldd --version

# musl 版をダウンロード（x86_64 の例）
curl --proto '=https' --tlsv1.2 -sSf \
  'https://desktop-release.q.us-east-1.amazonaws.com/latest/kirocli-x86_64-linux-musl.zip' \
  -o kirocli.zip

unzip kirocli.zip
./kirocli/install.sh
```

### ユースケース 4: ARM デバイス（Raspberry Pi、Mac M シリーズ等）

aarch64 版を使用：

```bash
# Linux ARM (例: Raspberry Pi 4 + Ubuntu)
curl --proto '=https' --tlsv1.2 -sSf \
  'https://desktop-release.q.us-east-1.amazonaws.com/latest/kirocli-aarch64-linux.zip' \
  -o kirocli.zip
unzip kirocli.zip
./kirocli/install.sh
```

> **macOS の M1/M2/M3 等**: ネイティブの macOS インストーラ（`curl ... | bash`）が ARM をサポート。

### ユースケース 5: Windows 11 の CI/CD 環境

GitHub Actions の Windows runner で Kiro CLI を導入：

```yaml
# .github/workflows/example.yml
- name: Install Kiro CLI
  shell: pwsh
  run: |
    irm 'https://cli.kiro.dev/install.ps1' | iex

- name: Use Kiro CLI in Headless Mode
  shell: pwsh
  env:
    KIRO_API_KEY: ${{ secrets.KIRO_API_KEY }}
  run: |
    kiro-cli chat --no-interactive "Generate a release note from CHANGELOG.md"
```

→ Headless Mode 詳細: [16. v2 Major Update](../01_features/16_v2MajorUpdate.md)

---

## 関連リンク

### 関連機能（本サイト）

- [16. v2 Major Update](../01_features/16_v2MajorUpdate.md) — Windows 11 対応、Headless Mode
- [12. Remote Auth](../01_features/12_RemoteAuth.md) — リモート認証（SSH/SSM/コンテナ）
- [22. Hooks](../01_features/22_Hooks.md) — `agentSpawn` Hook で起動時セットアップ

### リファレンス（辞書）

- [04_reference/03_cli-commands.md](../04_reference/03_cli-commands.md) — `kiro-cli doctor`、`kiro-cli update`、`kiro-cli login`、`kiro-cli uninstall` 等の正規仕様
- [04_reference/01_settings.md](../04_reference/01_settings.md) — `app.disableAutoupdates`、プロキシ関連環境変数（`HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY`）、`KIRO_CHAT_LOG_FILE`

### デプロイメント関連（本ディレクトリ）

- [01_aws-samples-code-server.md](01_aws-samples-code-server.md) — AWS Samples の code-server 構築
- [02_multiuser-code-server-investigation.md](02_multiuser-code-server-investigation.md) — マルチユーザー code-server 調査

### バージョン関連

- [02_update/01_changelog.md](../02_update/01_changelog.md)
  - v1.8.0: Proxy サポート開始
  - v2.0.0（2026-04-13）: Windows 11 ネイティブ対応、新 TUI

### 公式情報源

- [Installation - Kiro CLI Documentation](https://kiro.dev/docs/cli/installation/)（公式ページ最終更新: 2026-04-24）
- [Quick start](https://kiro.dev/docs/cli/quick-start/) — インストール後の最初のステップ
- [Authentication](https://kiro.dev/docs/cli/authentication/) — 認証方法
- [Terminal UI](https://kiro.dev/docs/cli/terminal-ui/) — TUI 詳細
- [Supported command line environments](https://kiro.dev/docs/cli/reference/cli-commands/) — 対応環境一覧

---

**Page updated**: 2026-05-24（本サイト初版）  
**公式ページ最終更新**: 2026-04-24
