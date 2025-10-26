[ホーム](../../README.md) > [開発者ガイド](../README.md) > [コントリビューション](README.md) > 01 Development Setup

---

# 開発環境セットアップ


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
```

### Windows
1. [rustup-init.exe](https://rustup.rs/) をダウンロード
2. 実行してインストール
3. Visual Studio C++ Build Toolsをインストール（必要に応じて）
4. 環境変数を設定（通常は自動）

### バージョン確認
```bash
rustc --version  # 例: rustc 1.75.0
cargo --version  # 例: cargo 1.75.0
```

---

## 📦 セットアップ

### リポジトリのクローン
```bash
# フォークしたリポジトリをクローン
git clone https://github.com/YOUR_USERNAME/amazon-q-developer-cli.git
cd amazon-q-developer-cli

# アップストリームを追加
git remote add upstream https://github.com/aws/amazon-q-developer-cli.git
```

### 依存関係のインストール
```bash
# Cargoが自動的に依存関係を解決
cargo build
```

### ビルド
```bash
# デバッグビルド
cargo build

# リリースビルド
cargo build --release
```

### テスト実行
```bash
# 全テスト実行
cargo test

# 特定のテスト実行
cargo test test_name

# テストログ表示
cargo test -- --nocapture
```

### ローカル実行
```bash
# デバッグモードで実行
cargo run

# リリースモードで実行
cargo run --release

# 引数を渡す
cargo run -- --help
```

---

## 🔧 トラブルシューティング

### ビルドエラー

#### 問題: `cargo build` が失敗する
**対処法**:
1. Rustのバージョンを確認
```
rustc --version
rustup update
```

2. 依存関係を更新
```
cargo update
```

3. クリーンビルド
```
cargo clean
cargo build
```

4. キャッシュをクリア
```
rm -rf target/
cargo build
```

#### 問題: リンカーエラー
**対処法**:
```
# macOS
xcode-select --install

# Ubuntu/Debian
sudo apt-get install build-essential

# Fedora/RHEL
sudo dnf install gcc
```

### テストエラー

#### 問題: `cargo test` が失敗する
**対処法**:
1. 環境変数を確認
```
env | grep Q_
```

2. テストログを確認
```
cargo test -- --nocapture
```

3. 特定のテストのみ実行
```
cargo test test_name -- --nocapture
```

4. テストを無視
```
cargo test -- --ignored
```

### よくあるエラー

#### 1. リンカーエラー
**原因**: 開発ツールのインストール不足  
**対処**: 上記「リンカーエラー」を参照

#### 2. 権限エラー
**原因**: sudo権限が必要な場合がある  
**対処**:
```
# Cargoのディレクトリ権限を確認
ls -la ~/.cargo

# 必要に応じて権限を変更
chmod -R u+w ~/.cargo
```

#### 3. ネットワークエラー
**原因**: プロキシ設定が必要  
**対処**:
```
# ~/.cargo/config.toml に追加
[http]
proxy = "http://proxy.example.com:8080"

[https]
proxy = "http://proxy.example.com:8080"
```

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
```

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
```

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
```

### ログファイルの確認
```bash
# ログディレクトリ
~/.aws/amazonq/logs/

# 最新のログを確認
tail -f ~/.aws/amazonq/logs/q-cli.log
```

### デバッガーの使用
```bash
# VS Codeでデバッグ
# F5キーを押してデバッグ開始

# コマンドラインでデバッグ
rust-lldb target/debug/q
```

---

## 📚 参考リソース

- [Rust Book](https://doc.rust-lang.org/book/) - Rust学習
- [Cargo Book](https://doc.rust-lang.org/cargo/) - Cargo使い方
- [rustup](https://rustup.rs/) - Rustツールチェーン管理
- [rust-analyzer](https://rust-analyzer.github.io/) - IDE統合

---

作成日: 2025-10-11  
最終更新: 2025-10-26

---

最終更新: 2025-10-26
