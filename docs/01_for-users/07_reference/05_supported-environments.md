# サポートされている環境

最終更新: 2025-10-11

---

## 📋 概要

Amazon Q CLIがサポートする環境の詳細情報です。

---

## 🍎 macOS

### システム要件
- **OS**: macOS 10.15 (Catalina) 以降
- **アーキテクチャ**: 
  - x86_64 (Intel)
  - arm64 (Apple Silicon: M1/M2/M3)

### サポートされるターミナル
- iTerm2
- macOS Terminal
- Hyper
- Alacritty
- Kitty
- WezTerm

### サポートされるIDE
- VS Code Terminal
- JetBrains Terminals (Fleet除く)

### アーキテクチャの確認方法
```bash
uname -m
# x86_64 → Intel Mac
# arm64 → Apple Silicon (M1/M2/M3)
```

---

## 🐧 Linux

### システム要件
- **ディストリビューション**: 
  - Ubuntu 22.04 LTS
  - Ubuntu 24.04 LTS
  - Ubuntu 20.04 LTS (一部機能のみ)
- **デスクトップ環境**: GNOME v42+
- **ディスプレイサーバー**: Xorg
- **入力メソッド**: IBus
- **アーキテクチャ**: 
  - x86_64
  - aarch64

### サポートされるターミナル
- GNOME Console
- GNOME Terminal
- Kitty
- Hyper
- WezTerm
- Alacritty
- Tilix
- Terminator

### 環境の確認方法

#### デスクトップ環境の確認
```bash
echo $XDG_CURRENT_DESKTOP
# GNOME → GNOME環境
```

#### ディスプレイサーバーの確認
```bash
echo $XDG_SESSION_TYPE
# x11 → Xorg
# wayland → Wayland
```

#### 入力メソッドの確認
```bash
ps aux | grep ibus
# ibusプロセスが表示される → IBus使用中
```

#### アーキテクチャの確認
```bash
uname -m
# x86_64 → Intel/AMD 64bit
# aarch64 → ARM 64bit
```

### 注意事項
- デスクトップ機能は現在x86_64アーキテクチャのみサポート

---

## 🌐 共通サポート

### シェル
- bash
- zsh
- fish

### CLI統合
- 500+の一般的なCLIツールをサポート
  - git
  - aws
  - docker
  - npm
  - yarn
  - その他

---

## 🌍 自然言語サポート

### サポートされる言語
1. 英語 (English)
2. 日本語 (Japanese)
3. 中国語 (Mandarin)
4. フランス語 (French)
5. ドイツ語 (German)
6. イタリア語 (Italian)
7. スペイン語 (Spanish)
8. 韓国語 (Korean)
9. ヒンディー語 (Hindi)
10. ポルトガル語 (Portuguese)

### 使用方法
Amazon Q Developerは自動的に言語を検出し、適切な言語で応答します。

---

## 📚 関連ドキュメント

- **[インストールガイド](../01_getting-started/01_installation.md)**
- **[トラブルシューティング](../06_troubleshooting/02_common-issues.md)**
- **[AWS公式ドキュメント](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-supported-envs.html)**

---
