# 開発環境セットアップ

**最終更新**: 2025-10-11

---

## 🛠️ 必要なツール

- **Rust**（最新安定版）- プログラミング言語
- **Git** - バージョン管理
- **Docker**（テスト用）- コンテナ実行環境
- **Node.js**（オプション）- MCPサーバー開発用

---

## 🦀 Rustのインストール

### macOS/Linux
```bash
# rustupのインストール
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 環境変数の設定
source $HOME/.cargo/env

# バージョン確認
rustc --version
cargo --version
```bash

### Windows
1. [rustup-init.exe](https://rustup.rs/) をダウンロード
2. 実行してインストール
3. Visual Studio C++ Build Toolsをインストール（必要に応じて）
4. 環境変数を設定（通常は自動）

### バージョン確認
```bash
rustc --version  # 例: rustc 1.75.0
cargo --version  # 例: cargo 1.75.0
```bash

---

## 📦 セットアップ

### リポジトリのクローン
```bash
# フォークしたリポジトリをクローン
git clone https://github.com/YOUR_USERNAME/amazon-q-developer-cli.git
cd amazon-q-developer-cli

# アップストリームを追加
git remote add upstream https://github.com/aws/amazon-q-developer-cli.git
```bash

### 依存関係のインストール
```bash
# Cargoが自動的に依存関係を解決
cargo build
```bash

### ビルド
```bash
# デバッグビルド
cargo build

# リリースビルド
cargo build --release
```bash

### テスト実行
```bash
# 全テスト実行
cargo test

# 特定のテスト実行
cargo test test_name

# テストログ表示
cargo test -- --nocapture
```bash

### ローカル実行
```bash
# デバッグモードで実行
cargo run

# リリースモードで実行
cargo run --release

# 引数を渡す
cargo run -- --help
```bash

---

## 🔧 トラブルシューティング

### ビルドエラー

#### 問題: `cargo build` が失敗する
**対処法**:
1. Rustのバージョンを確認
```bash
rustc --version
rustup update
```bash

2. 依存関係を更新
```bash
cargo update
```bash

3. クリーンビルド
```bash
cargo clean
cargo build
```bash

4. キャッシュをクリア
```bash
rm -rf target/
cargo build
```bash

#### 問題: リンカーエラー
**対処法**:
```bash
# macOS
xcode-select --install

# Ubuntu/Debian
sudo apt-get install build-essential

# Fedora/RHEL
sudo dnf install gcc
```bash

### テストエラー

#### 問題: `cargo test` が失敗する
**対処法**:
1. 環境変数を確認
```bash
env | grep Q_
```bash

2. テストログを確認
```bash
cargo test -- --nocapture
```bash

3. 特定のテストのみ実行
```bash
cargo test test_name -- --nocapture
```bash

4. テストを無視
```bash
cargo test -- --ignored
```bash

### よくあるエラー

#### 1. リンカーエラー
**原因**: 開発ツールのインストール不足  
**対処**: 上記「リンカーエラー」を参照

#### 2. 権限エラー
**原因**: sudo権限が必要な場合がある  
**対処**:
```bash
# Cargoのディレクトリ権限を確認
ls -la ~/.cargo

# 必要に応じて権限を変更
chmod -R u+w ~/.cargo
```bash

#### 3. ネットワークエラー
**原因**: プロキシ設定が必要  
**対処**:
```bash
# ~/.cargo/config.toml に追加
[http]
proxy = "http://proxy.example.com:8080"

[https]
proxy = "http://proxy.example.com:8080"
```bash

---

## 💻 IDE設定

### VS Code

#### 推奨拡張機能
- **rust-analyzer** - Rust言語サーバー
- **CodeLLDB** - デバッガー
- **Even Better TOML** - TOML編集
- **Error Lens** - エラー表示

#### 設定例
`.vscode/settings.json`:
```json
{
  "rust-analyzer.checkOnSave.command": "clippy",
  "rust-analyzer.cargo.features": "all",
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "rust-lang.rust-analyzer"
}
```bash

#### デバッグ設定
`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Debug Q CLI",
      "cargo": {
        "args": ["build", "--bin=q"]
      },
      "args": [],
      "cwd": "${workspaceFolder}"
    }
  ]
}
```bash

### IntelliJ IDEA

#### プラグイン
- **Rust** - Rust言語サポート
- **TOML** - TOML編集

#### 設定
1. Rust プラグインをインストール
2. Cargo統合を有効化
3. rustfmt/clippyを有効化

---

## 🔍 デバッグ

### ログレベル設定
```bash
# デバッグログを有効化
export Q_LOG_LEVEL=debug
cargo run

# トレースログを有効化
export Q_LOG_LEVEL=trace
cargo run
```bash

### ログファイルの確認
```bash
# ログディレクトリ
~/.aws/amazonq/logs/

# 最新のログを確認
tail -f ~/.aws/amazonq/logs/q-cli.log
```bash

### デバッガーの使用
```bash
# VS Codeでデバッグ
# F5キーを押してデバッグ開始

# コマンドラインでデバッグ
rust-lldb target/debug/q
```bash

---

## 📚 参考リソース

- [Rust Book](https://doc.rust-lang.org/book/) - Rust学習
- [Cargo Book](https://doc.rust-lang.org/cargo/) - Cargo使い方
- [rustup](https://rustup.rs/) - Rustツールチェーン管理
- [rust-analyzer](https://rust-analyzer.github.io/) - IDE統合

---

**作成日**: 2025-10-11  
**最終更新日**: 2025-10-11
