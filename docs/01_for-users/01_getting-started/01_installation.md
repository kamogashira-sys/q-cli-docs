[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [Getting Started](README.md) > 01 Installation

---

# インストールガイド

最終更新: 2025-10-11  
**参照**: [AWS公式ドキュメント](https://docs.aws.amazon.com/ja_jp/amazonq/latest/qdeveloper-ug/command-line-installing.html)

---

## 📋 前提条件

### 対応OS

| OS | 対応状況 | 推奨インストール方法 |
|---|---------|-------------------|
| [🍎 macOS](#-macos) | ✅ **対応中** | Homebrew（推奨） |
| [🐧 Linux](#-linux) | ✅ **対応中** | AppImage |
| 🪟 Windows | ⏳ **対応予定** | [ロードマップ #2602](https://github.com/aws/amazon-q-developer-cli/issues/2602) |

> **💡 Windowsユーザーの方へ**: ネイティブ対応は開発中ですが、[WSL2（Windows Subsystem for Linux）](https://learn.microsoft.com/ja-jp/windows/wsl/install)でLinux環境を構築すれば、現在でも利用可能です。WSL2上でLinux版のインストール手順に従ってください。

**対応アーキテクチャ**:
- **macOS**: x86_64（Intel）、arm64（Apple Silicon）
- **Linux**: x86_64（Intel/AMD）、aarch64（ARM）
- **Windows**: 対応予定

> 💡 **クイックナビゲーション**: OS名をクリックすると、該当するインストール手順にジャンプします。

---

### インストール前の確認

#### アーキテクチャの確認

お使いのマシンのアーキテクチャを確認してください。

**macOS**:
```bash
uname -m
# x86_64 → Intel Mac
# arm64 → Apple Silicon (M1/M2/M3)
```

**Apple Siliconの確認方法**:
- M1/M2/M3チップ搭載Mac → arm64
- Intel Core搭載Mac → x86_64

**Linux**:
```bash
uname -m
# x86_64 → Intel/AMD 64bit
# aarch64 → ARM 64bit
```

**注意**: デスクトップ機能は現在x86_64のみサポート

---

### システム要件
- **OS**: macOS、Linux（Windows対応予定）
- **シェル**: bash、zsh、fish
- **AWS認証**: AWS Builder ID または IAM Identity Center

### 必要なツール
- **macOS**: Homebrew（推奨）またはブラウザ
- **Linux**: wget、chmod（AppImageの場合）
- **インターネット接続**: ダウンロードと認証に必要

### AWS認証について

Amazon Q CLIを使用するには、以下のいずれかの認証方法が必要です：

#### AWS Builder ID（推奨）

個人開発者向けの無料認証方法です。

**特徴**:
- 無料で利用可能
- メールアドレスまたはGoogleアカウントで登録
- Amazon Q Developer、CodeCatalyst等で利用可能
- AWS アカウントとは独立した個人プロファイル

**作成方法**:
- [Amazon Q Developer向けBuilder ID入門（公式ガイド）](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/getting-started-builderid.html)
- [AWS Builder ID作成ガイド](https://docs.aws.amazon.com/signin/latest/userguide/create-builder-id.html)

#### IAM Identity Center

組織・チーム向けの認証方法です。

**特徴**:
- 管理者から提供されるStart URLが必要
- 組織のSSO（シングルサインオン）と連携
- 複数のAWSアカウントへのアクセス管理
- エンタープライズ向け

**詳細**: [料金プラン（Enterprise）](04_pricing.md#enterprise-プラン)を参照、または管理者にお問い合わせください

---

## 🍎 macOS

### 方法1: Homebrew経由（推奨）

Homebrewを使用すると、インストールとアップデートが簡単です。

```bash
# Amazon Q CLIのインストール
brew install --cask amazon-q

# インストール確認
q --version
```

**期待される出力**:
```
q 1.17.1
```

### 方法2: DMGファイル経由

Homebrewを使用しない場合は、DMGファイルから直接インストールできます。

#### ステップ1: ダウンロード

[macOS用Amazon Q をダウンロード](https://desktop-release.q.us-east-1.amazonaws.com/latest/Amazon%20Q.dmg)

または、ターミナルから：

```bash
curl -L "https://desktop-release.q.us-east-1.amazonaws.com/latest/Amazon%20Q.dmg" -o ~/Downloads/AmazonQ.dmg
```

#### ステップ2: インストール

1. ダウンロードした`Amazon Q.dmg`ファイルをダブルクリック
2. 開いたウィンドウで、Amazon Qアイコンを「アプリケーション」フォルダにドラッグ
3. アプリケーションフォルダから「Amazon Q」をダブルクリックして起動

---

### アクセシビリティ権限について

#### 必要な理由

Amazon Q CLIは以下の機能のためにアクセシビリティ権限を必要とします：

- **ターミナルでのオートコンプリート表示**: タブキーを押したときに候補を表示
- **キーボード入力の検知**: コマンド入力を認識してリアルタイムで補完
- **コマンド実行結果の取得**: ターミナルの出力を読み取ってコンテキストを理解

#### 権限の付与方法

初回起動時に、macOSがアクセシビリティ権限を要求します：

1. 「システム設定」→「プライバシーとセキュリティ」→「アクセシビリティ」を開く
2. 「Amazon Q」にチェックを入れる
3. 管理者パスワードを入力

---

### ⚠️ セキュリティ上の注意

**重要**: Amazon Q CLIは入力内容をAWSに送信します

#### データ送信について
- ターミナルでの入力内容
- コマンド実行結果
- ファイルの内容（コンテキストとして追加した場合）

#### 機密情報の取り扱い
以下の情報は入力しないでください：
- パスワード
- APIキー、アクセストークン
- 個人情報（PII）
- 機密性の高いビジネスデータ

#### ベストプラクティス

詳細なベストプラクティスは以下を参照してください：
- [設定のベストプラクティス](../04_best-practices/01_configuration.md)
- [セキュリティベストプラクティス](../04_best-practices/02_security.md)
- [パフォーマンス最適化](../04_best-practices/03_performance.md)

---

#### ステップ3: シェル統合の有効化

初回起動時に、シェル統合のセットアップが表示されます。

**シェル統合とは？**
- ターミナルから`q`コマンドを実行できるようになります
- コマンドの自動補完機能が有効になります

画面の指示に従って、シェル統合をインストールしてください。

**シェル統合の詳細**:

シェル統合により以下の機能が有効になります：
- `q`コマンドのパス設定
- タブ補完機能
- コマンド履歴の統合
- インライン補完（`q inline`）

**手動でのシェル統合**:

自動セットアップが失敗した場合、手動で設定できます：

```bash
# 初期化スクリプトの生成
q init

# シェル設定ファイルに追加（bashの場合）
echo 'eval "$(q init bash)"' >> ~/.bashrc
source ~/.bashrc

# zshの場合
echo 'eval "$(q init zsh)"' >> ~/.zshrc
source ~/.zshrc

# fishの場合
q init fish | source
```

**シェル統合の確認**:

```bash
# 統合状態の確認
q doctor

# 期待される出力:
# ✔ Shell integration: enabled
# ✔ Autocomplete: working
```

#### ステップ4: 認証

[認証設定](#-認証設定)セクションを参照してください。

---

## 🐧 Linux

### Linux環境の確認

Amazon Q CLIはGNOME v42+環境で最適に動作します。インストール前に環境を確認してください。

#### デスクトップ環境の確認

**GNOME**: Linuxのデスクトップ環境の一つ

```bash
echo $XDG_CURRENT_DESKTOP
# GNOME → GNOME環境
```

#### ディスプレイサーバーの確認

**Xorg**: Linuxのディスプレイサーバー

```bash
echo $XDG_SESSION_TYPE
# x11 → Xorg
# wayland → Wayland（一部機能制限あり）
```

#### 入力メソッドの確認

**IBus**: 日本語入力などを管理する入力メソッドフレームワーク

```bash
ps aux | grep ibus
# ibusプロセスが表示される → IBus使用中
```

---

### Ubuntu (.debパッケージ)

Ubuntu（およびDebian系ディストリビューション）では、.debパッケージを使用してインストールできます。

#### ステップ1: ダウンロード

```bash
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/amazon-q.deb
```

#### ステップ2: インストール

```bash
sudo apt-get install -f
sudo dpkg -i amazon-q.deb
```

**コマンドの説明**:
- `apt-get install -f`: 依存関係を自動的に解決
- `dpkg -i`: .debパッケージをインストール

#### ステップ3: 起動と認証

```bash
q
```

初回起動時に認証画面が表示されます。[認証設定](#-認証設定)セクションを参照してください。

---

### Linux（zip file - GUI不要）

GUI環境がない場合や、最小限のインストールを希望する場合は、zip fileを使用できます。

**特徴**:
- GUI不要
- `q`（チャット）と`qterm`（インライン補完）のみ
- SSH経由での使用に最適
- 軽量インストール

#### 前提条件

**システム要件**:
- glibc 2.34以降（ほとんどの2021年以降のLinuxディストリビューション）
- 古いディストリビューション（glibc < 2.34）の場合はmusl版を使用
- 対応アーキテクチャ: x86_64、aarch64（ARM）
- 対応ディストリビューション: Fedora、Ubuntu、Amazon Linux 2023

**glibc バージョンの確認**:
```bash
ldd --version
```

- **2.34以降**: 標準版を使用
- **2.34未満**: musl版を使用

#### ステップ1: ダウンロード

**標準版（glibc 2.34+）**:

x86-64:
```bash
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux.zip" \
  -o "q.zip"
```

ARM (aarch64):
```bash
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-aarch64-linux.zip" \
  -o "q.zip"
```

**musl版（glibc < 2.34）**:

x86-64:
```bash
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux-musl.zip" \
  -o "q.zip"
```

ARM (aarch64):
```bash
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-aarch64-linux-musl.zip" \
  -o "q.zip"
```

#### ステップ2: インストール

```bash
# 解凍
unzip q.zip

# インストール実行
./q/install.sh
```

**インストール先**: デフォルトでは`~/.local/bin`にインストールされます。

#### ステップ3: 認証

```bash
q
```

初回起動時に認証画面が表示されます。[認証設定](#-認証設定)セクションを参照してください。

---

### その他のLinuxディストリビューション（AppImage）

Ubuntu以外のLinuxディストリビューション（Fedora、CentOS、Arch Linuxなど）では、AppImage形式を使用できます。

**AppImageとは？**
- インストール不要で実行できるポータブル形式
- ほとんどのLinuxディストリビューションで動作
- 管理者権限不要

#### ステップ1: ダウンロード

```bash
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/amazon-q.appimage
```

#### ステップ2: 実行可能にする

```bash
chmod +x amazon-q.appimage
```

**`chmod +x`とは？**
- ファイルに実行権限を付与するコマンド
- これにより、ダウンロードしたファイルをプログラムとして実行できます

#### ステップ3: 実行

```bash
./amazon-q.appimage
```

#### ステップ4: 認証

初回起動時に認証画面が表示されます。[認証設定](#-認証設定)セクションを参照してください。

**注意**: AppImageの実行にはGUI環境が必要です。サーバー環境など、GUIがない場合は別の方法を検討してください。

---

## 🪟 Windows

**現在の状況**: Windows版は開発中です。

### Windows Subsystem for Linux (WSL) を使用

Windowsでは、WSL（Windows Subsystem for Linux）を使用してLinux版をインストールすることをお勧めします。

#### ステップ1: WSLのインストール

```powershell
# PowerShellを管理者として実行
wsl --install
```

#### ステップ2: WSLを起動

```powershell
wsl
```

#### ステップ3: Linux版をインストール

WSL内で、上記の[Linux](#-linux)セクションの手順に従ってインストールしてください。

### 参考情報

Windows環境での詳細なセットアップ方法については、以下のブログ記事を参照してください：

- [The Essential Guide to Installing Amazon Q CLI on Windows](https://dev.to/aws/the-essential-guide-to-installing-amazon-q-developer-cli-on-windows-lmh)

---

## 🌐 プロキシ設定

Amazon Q Developer CLI（v1.8.0以降）は、エンタープライズ環境で一般的に使用されるプロキシサーバーをサポートしています。CLIは標準的なプロキシ環境変数を自動的に認識します。

### 環境変数の設定

シェルで以下の環境変数を設定してプロキシを構成します：

```bash
# HTTP proxy（非SSL通信用）
export HTTP_PROXY=http://proxy.company.com:8080

# HTTPS proxy（SSL通信用）
export HTTPS_PROXY=http://proxy.company.com:8080

# プロキシをバイパスするドメイン
export NO_PROXY=localhost,127.0.0.1,.company.com
```

### 認証付きプロキシ

認証が必要なプロキシの場合：

```bash
export HTTP_PROXY=http://username:password@proxy.company.com:8080
export HTTPS_PROXY=http://username:password@proxy.company.com:8080
```

### SOCKSプロキシサポート

Amazon Q CLIはSOCKSプロキシもサポートしています：

```bash
export HTTP_PROXY=socks5://proxy.company.com:1080
export HTTPS_PROXY=socks5://proxy.company.com:1080
```

### プロキシ設定の確認

プロキシ環境変数を設定した後、接続をテストします：

```bash
q doctor
```

### プロキシ関連のトラブルシューティング

プロキシ関連の接続問題が発生した場合：

- プロキシサーバーのアクセス可能性と認証情報を確認
- 企業ファイアウォールがAWSエンドポイントへの接続を許可しているか確認
- SSL証明書検証が失敗する場合はIT管理者に連絡
- プロキシサーバーが必要なプロトコルをサポートしているか確認

---

## 🔐 認証設定

Amazon Q CLIを使用するには、AWS認証が必要です。

### AWS Builder IDでの認証（推奨）

個人開発者向けの無料認証方法です。

#### ステップ1: 初回起動

```bash
q
```

#### ステップ2: 認証

初回起動時に、ブラウザが自動的に開きます。

1. AWS Builder IDでログイン（アカウントがない場合は作成）
2. 認証を承認
3. ターミナルに戻り、Q CLIが使用可能になります

**ブラウザが開かない場合**:
- ポップアップブロックを無効化してください
- 手動で表示されたURLをブラウザで開いてください

---

### IAM Identity Centerでの認証

組織・チーム向けの認証方法です。管理者から提供されたStart URLが必要です。

> **💡 組織での導入**: 組織全体でAmazon Q Developer を導入する場合は、[エンタープライズ導入ガイド](../05_deployment/01_enterprise-deployment.md)を参照してください。IAM Identity Center のセットアップからサブスクリプション管理まで、詳細な手順を説明しています。

#### ステップ1: 認証情報の設定

```bash
q login
```

プロンプトに従って以下を入力：
- **Start URL**: 組織の管理者から提供されたURL
- **Region**: リージョン（例: us-east-1）

#### ステップ2: 認証

ブラウザが開き、IAM Identity Centerのログイン画面が表示されます。

1. 組織の認証情報でログイン
2. 認証を承認
3. ターミナルに戻り、Q CLIが使用可能になります

---

### 認証状態の確認

```bash
# 現在の認証状態を確認
q doctor
```

**正常な出力例**:
```
✔ Everything looks good!

Amazon Q still not working? Run q issue to let us know!
```

---

## 📁 インストール後のファイル配置

Amazon Q CLIをインストールすると、以下の場所にファイルが配置されます。

### macOS

| 種類 | パス | 説明 |
|------|------|------|
| アプリケーション | `/Applications/Amazon Q.app` | Amazon Q CLIアプリケーション本体 |
| 設定ファイル | `~/Library/Application Support/amazon-q/` | グローバル設定、MCP設定 |
| Agent設定 | `~/.aws/amazonq/cli-agents/` | Agent設定ディレクトリ |
| ログファイル | `~/Library/Logs/Amazon Q/` | アプリケーションログ |

**主要な設定ファイル**:
- `~/Library/Application Support/amazon-q/settings.json` - グローバル設定
- `~/.aws/amazonq/cli-agents/` - Agent設定ディレクトリ
- `~/.aws/amazonq/mcp.json` - MCP設定

---

### Linux

| 種類 | パス | 説明 |
|------|------|------|
| バイナリ | `~/.local/bin/q` | Amazon Q CLIコマンド |
| 設定ファイル | `~/.local/share/amazon-q/` | グローバル設定、MCP設定 |
| Agent設定 | `~/.aws/amazonq/cli-agents/` | Agent設定ディレクトリ |
| ログファイル | `~/.local/share/amazon-q/logs/` | アプリケーションログ |

**主要な設定ファイル**:
- `~/.local/share/amazon-q/settings.json` - グローバル設定
- `~/.aws/amazonq/cli-agents/` - Agent設定ディレクトリ
- `~/.aws/amazonq/mcp.json` - MCP設定

**📖 詳細**: 各ファイル・ディレクトリの詳細な説明は [設定ファイル配置マップ](../07_reference/04_configuration-file-locations.md#ファイルディレクトリの詳細) を参照してください。

---

### 設定ファイルの詳細

すべての設定ファイルの詳細については、[設定ファイル配置マップ](../07_reference/04_configuration-file-locations.md)を参照してください。

---

## ✅ インストール確認

### バージョン確認

```bash
q --version
```

**期待される出力**:
```
q 1.17.1
```

### 診断コマンド

`q doctor`コマンドを使用して、インストールと設定が正しく行われているか確認できます。

```bash
q doctor
```

**このコマンドでチェックされる項目**:
- インストールの完全性
- 認証状態
- シェル統合の状態
- ネットワーク接続

**問題が見つかった場合**:
- 画面の指示に従って問題を解決してください
- それでも解決しない場合は、`q issue`コマンドでバグを報告できます

### 基本動作確認

```bash
# チャットの起動
q

# 簡単な質問をしてみる
> Hello, Q!
```

Amazon Q CLIが応答すれば、インストールは成功です。

---

## 🔄 アップデート

### Homebrew経由（macOS）

```bash
# Amazon Q CLIのアップデート
brew upgrade --cask amazon-q

# バージョン確認
q --version
```

### 手動アップデート

Homebrew以外でインストールした場合は、最新版を再度ダウンロードしてインストールしてください。

**macOS**: 最新のDMGファイルをダウンロードして再インストール

#### Linux環境でのアップデート

Q CLIには組み込みのアップデート機能があります：

```bash
# Q CLIのアップデート
q update

# 最新版の場合の出力例
No updates available,
1.18.1 is the latest version.

# バージョン確認
q --version
```

##### ⚠️ 重要な注意事項

現在、Linux環境では`q update`コマンドが正常に動作しない場合があります（[ISSUE #3066](https://github.com/aws/amazon-q-developer-cli/issues/3066)、[#2120](https://github.com/aws/amazon-q-developer-cli/issues/2120)、[#841](https://github.com/aws/amazon-q-developer-cli/issues/841)）。

**既知の問題**:
- `q update`実行時に`Invalid cross-device link (os error 18)`エラーが発生する場合がある
- 特にAWS EC2環境や複数のマウントポイントがある環境で発生しやすい
- アップデートが実行されない、またはエラーメッセージが表示されない

##### 推奨される回避策

**debパッケージの場合（Ubuntu/Debian）**:

```bash
# 最新版をダウンロード
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/amazon-q.deb

# インストール
sudo dpkg -i amazon-q.deb

# 依存関係の修正（必要な場合）
sudo apt-get install -f
```

**AppImageの場合**:

```bash
# 最新版をダウンロード
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/Amazon%20Q.AppImage -O ~/amazon-q.AppImage

# 実行権限を付与
chmod +x ~/amazon-q.AppImage
```

**進捗状況**: [GitHub ISSUE #841](https://github.com/aws/amazon-q-developer-cli/issues/841)で確認できます

---

## 🗑️ アンインストール

### macOS

#### Homebrew経由でインストールした場合

```bash
brew uninstall --cask amazon-q
```

#### DMGファイルからインストールした場合

1. Finderで「アプリケーション」フォルダを開く
2. 「Amazon Q」を見つける
3. ゴミ箱にドラッグ、または右クリックして「ゴミ箱に移動」
4. ゴミ箱を空にする

#### 設定ファイルの削除（オプション）

```bash
rm -rf ~/.aws/amazonq
```

---

### Ubuntu/Linux

#### .debパッケージでインストールした場合

```bash
# パッケージの削除
sudo apt-get remove amazon-q

# 設定ファイルも含めて完全削除
sudo apt-get purge amazon-q
```

#### AppImageでインストールした場合

```bash
# AppImageファイルを削除
rm amazon-q.appimage

# 設定ファイルの削除（オプション）
rm -rf ~/.aws/amazonq
```

---

## トラブルシューティング

問題が発生した場合は、[トラブルシューティングガイド](../06_troubleshooting/02_common-issues.md)を参照してください。

**関連トピック**:
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)

---

### 一般的な問題

#### 認証の失敗

**症状**: 認証時にエラーが発生する

**解決方法**:
1. ブラウザのポップアップブロックを無効化
2. 認証情報をクリアして再試行
   ```bash
   rm -rf ~/.aws/amazonq/auth
   q login
   ```
3. ネットワークプロキシの設定を確認

---

#### コマンドが見つからない

**症状**: `q: command not found`

**解決方法**:
1. シェルを再起動
   ```bash
   exec $SHELL
   ```
2. PATHが正しく設定されているか確認
   ```bash
   echo $PATH | grep -o "/usr/local/bin"
   ```
3. 再インストールを試す

---

#### オートコンプリートが機能しない

**症状**: タブキーを押してもコマンドが補完されない

**原因**:
- シェル統合が正しくインストールされていない
- シェル設定ファイルが読み込まれていない
- 対応していないシェルを使用している

**解決方法**:

1. **シェル統合の状態を確認**:
```bash
q doctor
# Shell integration の状態を確認
```

2. **シェル統合を再インストール**:
```bash
# 初期化スクリプトを再生成
q init

# シェル設定ファイルに追加（既存の行を削除してから）
# bashの場合
grep -v "q init" ~/.bashrc > ~/.bashrc.tmp && mv ~/.bashrc.tmp ~/.bashrc
echo 'eval "$(q init bash)"' >> ~/.bashrc
source ~/.bashrc

# zshの場合
grep -v "q init" ~/.zshrc > ~/.zshrc.tmp && mv ~/.zshrc.tmp ~/.zshrc
echo 'eval "$(q init zsh)"' >> ~/.zshrc
source ~/.zshrc
```

3. **新しいターミナルセッションを開始**:
```bash
# 現在のシェルを再起動
exec $SHELL
```

4. **サポートされているシェルを確認**:
- bash
- zsh
- fish

**それでも解決しない場合**:
```bash
# デバッグモードで確認
q debug

# 問題を報告
q issue
```

---

### トラブルシューティングのステップ

問題が解決しない場合は、以下の手順を試してください：

1. **`q doctor`を実行**: 一般的な問題を自動診断
2. **インターネット接続を確認**: Amazon Q CLIはクラウドサービスです
3. **サポート環境を確認**: [サポートされている環境](https://docs.aws.amazon.com/ja_jp/amazonq/latest/qdeveloper-ug/command-line-supported-envs.html)を参照
4. **再インストール**: 完全にアンインストールしてから再インストール
5. **バグ報告**: `q issue`コマンドで問題を報告

```bash
# バグ報告
q issue
```

---

## 📚 次のステップ

インストールが完了したら、以下のドキュメントをご覧ください：

- **[クイックスタート](02_quick-start.md)** - 5分で始めるQ CLI
- **[最初の一歩](03_first-steps.md)** - 基本的な使い方
- **[設定ガイド](../03_configuration/01_overview.md)** - 設定のカスタマイズ

---

## 🔗 関連リンク

### AWS公式ドキュメント
- [インストールガイド](https://docs.aws.amazon.com/ja_jp/amazonq/latest/qdeveloper-ug/command-line-installing.html)
- [サポートされている環境](https://docs.aws.amazon.com/ja_jp/amazonq/latest/qdeveloper-ug/command-line-supported-envs.html)
- [AWS Builder ID](https://docs.aws.amazon.com/general/latest/gr/aws_builder_id.html)
- [IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)

### その他
- [Windows向けインストールガイド（ブログ）](https://dev.to/aws/the-essential-guide-to-installing-amazon-q-developer-cli-on-windows-lmh)

---

## 📖 ナビゲーション

**次へ**: [クイックスタート](02_quick-start.md) →

---

**作成日**: 2025-10-11  
最終更新: 2025-10-18
