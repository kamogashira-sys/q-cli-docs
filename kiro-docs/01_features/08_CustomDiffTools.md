# Kiro CLI Custom Diff Tools機能

**出典**: [Kiro CLI v1.24.0 Changelog](https://kiro.dev/changelog/cli/1-24/)

## 概要

Kiro CLI v1.24.0（2026年1月16日リリース）で追加されたCustom Diff Tools機能について詳細に解説します。この機能により、Kiroがファイル変更を提案する際、組み込みDiffツールの代わりに外部Diffツールを使用できるようになりました。

### Custom Diff Toolsとは

Custom Diff Tools機能は、Kiroがファイル変更を提案する際に、**外部のDiffツール**を使用できるようにする機能です。delta、difftastic、VS Codeなど、15種類以上のDiffツールに対応しています。

### 主な特徴

- **15種類以上のツール対応**: ターミナルツール8種類、GUIツール7種類
- **簡単な設定**: `kiro-cli settings`コマンドで設定
- **カスタム引数対応**: ツールに独自の引数を渡すことが可能
- **組み込みDiffへの復帰**: いつでも組み込みDiffに戻せる

### なぜCustom Diff Toolsが必要なのか

従来の組み込みDiffツールは基本的な機能を提供していましたが、以下の制約がありました：

1. **視認性の限界**: シンプルな表示のみ
2. **カスタマイズ不可**: 表示形式を変更できない
3. **高度な機能なし**: 構文ハイライト、サイドバイサイド表示などがない

Custom Diff Tools機能は、これらの制約を解決し、開発者の好みに合わせたDiff表示を実現します。

### サポートされるツール

#### ターミナルツール（8種類）

| ツール | 設定値 | 特徴 |
|--------|--------|------|
| delta | `delta` | 構文ハイライト、行番号、サイドバイサイド表示 |
| difftastic | `difft` | 言語認識の構造的Diff、フォーマット変更を無視 |
| icdiff | `icdiff` | サイドバイサイドのカラー比較 |
| diff-so-fancy | `diff-so-fancy` | クリーンで人間に読みやすい出力 |
| colordiff | `colordiff` | シンプルなカラー化Diff |
| diff-highlight | `diff-highlight` | 単語レベルのハイライト（Git同梱） |
| ydiff | `ydiff` | サイドバイサイド＋単語レベルハイライト |
| bat | `bat` | 構文ハイライト＋Git統合 |

#### GUIツール（7種類）

| ツール | 設定値 | プラットフォーム |
|--------|--------|----------------|
| VS Code | `code` | Windows, macOS, Linux |
| VSCodium | `codium` | Windows, macOS, Linux |
| Meld | `meld` | Linux, Windows |
| KDiff3 | `kdiff3` | Windows, macOS, Linux |
| FileMerge | `opendiff` | macOS |
| Vim | `vimdiff` または `vim` | Windows, macOS, Linux |
| Neovim | `nvim` | Windows, macOS, Linux |

**⚠️ 重要**: GUIツールは一時ファイルを表示専用で開きます。GUI内での編集は保存されず、Kiroの提案変更に適用されません。

## 📋 Zenn記事の詳細内容確認

**注意**: v1.24.0のCustom Diff Tools機能に関するZenn記事は現時点で公開されていません。本ドキュメントは公式Changelogおよび公式ドキュメントの情報に基づいて作成されています。

### 参考情報源

- [Kiro CLI v1.24.0 Changelog](https://kiro.dev/changelog/cli/1-24/)
- [Custom Diff Tools Documentation](https://kiro.dev/docs/cli/chat/diff-tools/)

## Custom Diff Tools機能詳細

### 基本概念

Custom Diff Tools機能は、Kiroがファイル変更を提案する際に、外部のDiffツールを使用できるようにする機能です。

#### Diffツールの役割

1. **変更内容の可視化**: ファイルの変更箇所を視覚的に表示
2. **レビューの支援**: 変更内容を確認しやすくする
3. **承認の判断**: 変更を適用するかどうかの判断材料

#### 組み込みDiffとの違い

| 項目 | 組み込みDiff | Custom Diff Tools |
|------|-------------|------------------|
| 設定 | 不要 | 必要 |
| 表示形式 | シンプル | 高度（構文ハイライト、サイドバイサイドなど） |
| カスタマイズ | 不可 | 可能 |
| ツールのインストール | 不要 | 必要 |

### ターミナルツールの詳細

#### 1. delta

**特徴**:
- 構文ハイライト
- 行番号表示
- サイドバイサイド表示（オプション）
- Git統合

**インストール**:

```bash
# macOS
brew install git-delta

# Ubuntu/Debian
sudo apt install git-delta

# Arch Linux
sudo pacman -S git-delta

# Windows (Scoop)
scoop install delta
```

**設定**:

```bash
# 基本設定
kiro-cli settings chat.diffTool delta

# サイドバイサイド表示を有効化
kiro-cli settings chat.diffTool "delta --side-by-side"
```

#### 2. difftastic

**特徴**:
- 言語認識の構造的Diff
- フォーマット変更を無視
- ASTベースの比較

**インストール**:

```bash
# macOS
brew install difftastic

# Cargo（Rust）
cargo install difftastic

# Windows (Scoop)
scoop install difftastic
```

**設定**:

```bash
kiro-cli settings chat.diffTool difft
```

#### 3. icdiff

**特徴**:
- サイドバイサイドのカラー比較
- 直感的な表示

**インストール**:

```bash
# pip
pip install icdiff

# macOS
brew install icdiff
```

**設定**:

```bash
kiro-cli settings chat.diffTool icdiff
```

#### 4. diff-so-fancy

**特徴**:
- クリーンで人間に読みやすい出力
- Git統合

**インストール**:

```bash
# npm
npm install -g diff-so-fancy

# macOS
brew install diff-so-fancy
```

**設定**:

```bash
kiro-cli settings chat.diffTool diff-so-fancy
```

#### 5. colordiff

**特徴**:
- シンプルなカラー化Diff
- 軽量

**インストール**:

```bash
# macOS
brew install colordiff

# Ubuntu/Debian
sudo apt install colordiff
```

**設定**:

```bash
kiro-cli settings chat.diffTool colordiff
```

#### 6. diff-highlight

**特徴**:
- 単語レベルのハイライト
- Git同梱（追加インストール不要）

**設定**:

```bash
kiro-cli settings chat.diffTool diff-highlight
```

#### 7. ydiff

**特徴**:
- サイドバイサイド表示
- 単語レベルハイライト

**インストール**:

```bash
# pip
pip install ydiff
```

**設定**:

```bash
kiro-cli settings chat.diffTool ydiff
```

#### 8. bat

**特徴**:
- 構文ハイライト
- Git統合
- ページャー機能

**インストール**:

```bash
# macOS
brew install bat

# Ubuntu/Debian
sudo apt install bat

# Windows (Scoop)
scoop install bat
```

**設定**:

```bash
kiro-cli settings chat.diffTool bat
```

### GUIツールの詳細

#### 1. VS Code

**特徴**:
- 統合開発環境としての高度なDiff表示
- 構文ハイライト
- インラインDiff表示

**インストール**:

```bash
# 公式サイトからダウンロード
# https://code.visualstudio.com/
```

**設定**:

```bash
kiro-cli settings chat.diffTool code
```

**⚠️ 重要**: GUIツールは一時ファイルを表示専用で開きます。GUI内での編集は保存されず、Kiroの提案変更に適用されません。

#### 2. VSCodium

**特徴**:
- VS Codeのオープンソース版
- テレメトリーなし

**インストール**:

```bash
# macOS
brew install vscodium

# Linux
# 公式サイトからダウンロード
# https://vscodium.com/
```

**設定**:

```bash
kiro-cli settings chat.diffTool codium
```

#### 3. Meld

**特徴**:
- ビジュアルDiffツール
- 3-way merge対応

**インストール**:

```bash
# Ubuntu/Debian
sudo apt install meld

# macOS
brew install meld

# Windows
# 公式サイトからダウンロード
# https://meldmerge.org/
```

**設定**:

```bash
kiro-cli settings chat.diffTool meld
```

#### 4. KDiff3

**特徴**:
- クロスプラットフォーム
- 3-way merge対応

**インストール**:

```bash
# macOS
brew install kdiff3

# Ubuntu/Debian
sudo apt install kdiff3

# Windows
# 公式サイトからダウンロード
# https://kdiff3.sourceforge.net/
```

**設定**:

```bash
kiro-cli settings chat.diffTool kdiff3
```

#### 5. FileMerge（macOS）

**特徴**:
- macOS標準のDiffツール
- Xcode Command Line Toolsに含まれる

**インストール**:

```bash
# Xcode Command Line Toolsをインストール
xcode-select --install
```

**設定**:

```bash
kiro-cli settings chat.diffTool opendiff
```

#### 6. Vim

**特徴**:
- ターミナルベースのエディタ
- vimdiffモード

**インストール**:

```bash
# 多くのシステムにプリインストール済み
# 確認
vim --version
```

**設定**:

```bash
# vimdiffを使用
kiro-cli settings chat.diffTool vimdiff
```

# または
kiro-cli settings chat.diffTool vim
```

#### 7. Neovim

**特徴**:
- Vimの改良版
- 高速

**インストール**:

```bash
# macOS
brew install neovim

# Ubuntu/Debian
sudo apt install neovim

# Windows (Scoop)
scoop install neovim
```

**設定**:

```bash
kiro-cli settings chat.diffTool nvim
```

### カスタム引数の使用

#### 基本的な使い方

```bash
# ツール名と引数を一緒に指定
kiro-cli settings chat.diffTool "tool-name --arg1 --arg2"
```

#### 実例

**deltaでサイドバイサイド表示**:

```bash
kiro-cli settings chat.diffTool "delta --side-by-side"
```

**deltaでテーマ指定**:

```bash
kiro-cli settings chat.diffTool "delta --theme=Dracula"
```

**difftasticで言語指定**:

```bash
kiro-cli settings chat.diffTool "difft --language=typescript"
```

### 組み込みDiffへの復帰

```bash
# 設定を削除して組み込みDiffに戻す
kiro-cli settings -d chat.diffTool
```

### 設定の確認

```bash
# 現在の設定を確認
kiro-cli settings chat.diffTool
```

## セットアップ/使用方法

### 1. Diffツールのインストール

#### ステップ1: ツールの選択

まず、使用したいDiffツールを選択します。

**選択基準**:

| 用途 | 推奨ツール | 理由 |
|------|-----------|------|
| 構文ハイライト重視 | delta, bat | 美しい表示 |
| 構造的Diff | difftastic | ASTベースの比較 |
| サイドバイサイド表示 | icdiff, ydiff | 並列比較 |
| シンプル | colordiff | 軽量 |
| GUI | VS Code, Meld | ビジュアル |

#### ステップ2: ツールのインストール

**例: deltaのインストール**
```
```bash
# macOS
brew install git-delta

# Ubuntu/Debian
sudo apt install git-delta

# Arch Linux
sudo pacman -S git-delta

# Windows (Scoop)
scoop install delta

# インストール確認
delta --version
```

### 2. Kiro CLIでの設定

#### 基本設定

```bash
# deltaを設定
kiro-cli settings chat.diffTool delta

# 設定確認
kiro-cli settings chat.diffTool
# 出力: delta
```

#### カスタム引数付き設定

```bash
# サイドバイサイド表示を有効化
kiro-cli settings chat.diffTool "delta --side-by-side"

# 設定確認
kiro-cli settings chat.diffTool
# 出力: delta --side-by-side
```

### 3. 動作確認

#### ステップ1: Kiro CLIを起動

```bash
kiro-cli chat
```

#### ステップ2: ファイル変更を依頼

```bash
> README.mdに新しいセクションを追加して
```

#### ステップ3: Diff表示を確認

Kiroがファイル変更を提案する際、設定したDiffツールで表示されます。

**deltaの表示例**（推定）:

```diff
 # README
 
 ## Overview
 
 This is a sample project.
 
+## New Section
+
+This is a new section added by Kiro.
+
 ## Installation
```

### 4. 複数のツールを試す

#### ツールの切り替え

```bash
# deltaを試す
kiro-cli settings chat.diffTool delta
kiro-cli chat

# difftasticを試す
kiro-cli settings chat.diffTool difft
kiro-cli chat

# icdiffを試す
kiro-cli settings chat.diffTool icdiff
kiro-cli chat
```

#### 組み込みDiffに戻す

```bash
# 設定を削除
kiro-cli settings -d chat.diffTool

# 確認
kiro-cli settings chat.diffTool
# 出力: (設定なし)
```

### 5. プロジェクトごとの設定

#### Agent設定ファイルでの指定

```json
{
  "name": "my-agent",
  "description": "My custom agent",
  "settings": {
    "chat": {
      "diffTool": "delta --side-by-side"
    }
  }
}
```

#### 使用例

```bash
# カスタムエージェントで起動
kiro-cli chat --agent my-agent

# このエージェントではdelta --side-by-sideが使用される
```

### 6. グローバル設定とAgent設定の優先順位

| 設定レベル | 優先順位 | 設定方法 |
|-----------|---------|---------|
| Agent設定 | 高 | `.kiro/agents/my-agent.json` |
| グローバル設定 | 低 | `kiro-cli settings chat.diffTool` |

**動作**:
- Agent設定がある場合: Agent設定が優先
- Agent設定がない場合: グローバル設定を使用
- どちらもない場合: 組み込みDiffを使用

## 実用的なユースケース

### ユースケース1: 構文ハイライトで視認性向上

#### シナリオ

コードレビュー時に、変更箇所を視覚的にわかりやすく表示したい。

#### 実装

**ツール**: delta

```bash
# deltaをインストール
brew install git-delta

# Kiro CLIで設定
kiro-cli settings chat.diffTool delta
```

#### 使用例

```bash
kiro-cli chat

> src/utils/helper.tsのformatDate関数をリファクタリングして
```

**deltaの表示**（推定）:

```diff
 export function formatDate(date: Date): string {
-  return date.toISOString().split('T')[0];
+  return new Intl.DateTimeFormat('ja-JP').format(date);
 }
```

**メリット**:
- 構文ハイライトで変更箇所が明確
- 行番号表示で位置を把握しやすい
- 美しい表示でレビューが快適

### ユースケース2: 構造的Diffでフォーマット変更を無視

#### シナリオ

フォーマット変更（インデント、改行など）を無視して、実質的な変更のみを確認したい。

#### 実装

**ツール**: difftastic

```bash
# difftasticをインストール
brew install difftastic

# Kiro CLIで設定
kiro-cli settings chat.diffTool difft
```

#### 使用例

```bash
kiro-cli chat

> src/components/Button.tsxをPrettierでフォーマットして
```

**difftasticの表示**（推定）:

```
No structural changes detected.
Only formatting changes (whitespace, indentation).
```

**メリット**:
- フォーマット変更を無視
- 実質的な変更のみ表示
- レビュー時間の短縮

### ユースケース3: サイドバイサイド表示で並列比較

#### シナリオ

変更前後のコードを並べて比較したい。

#### 実装

**ツール**: icdiff

```bash
# icdiffをインストール
pip install icdiff

# Kiro CLIで設定
kiro-cli settings chat.diffTool icdiff
```

#### 使用例

```bash
kiro-cli chat

> src/api/client.tsのエラーハンドリングを改善して
```

**icdiffの表示**（推定）:

```
Before                          | After
--------------------------------|--------------------------------
try {                           | try {
  const response = await fetch  |   const response = await fetch
  return response.json()        |   if (!response.ok) {
}                               |     throw new Error('API Error')
catch (error) {                 |   }
  console.error(error)          |   return response.json()
}                               | } catch (error) {
                                |   logger.error('API Error', error)
                                |   throw error
                                | }
```

**メリット**:
- 変更前後を並べて比較
- 全体の流れを把握しやすい
- 大規模な変更でも理解しやすい

### ユースケース4: GUIツールで詳細レビュー

#### シナリオ

複雑な変更を詳細にレビューしたい。

#### 実装

**ツール**: VS Code
```
```bash
# VS Codeをインストール（公式サイトから）

# Kiro CLIで設定
kiro-cli settings chat.diffTool code
```

#### 使用例

```bash
kiro-cli chat

> src/services/auth.tsの認証ロジックを改善して
```

**VS Codeの表示**:
- GUIで詳細なDiff表示
- インラインDiff
- 構文ハイライト

**メリット**:
- GUIで直感的な操作
- 詳細なDiff表示
- エディタの機能を活用

**⚠️ 注意**: GUIツールは一時ファイルを表示専用で開きます。GUI内での編集は保存されず、Kiroの提案変更に適用されません。

## ベストプラクティス

### 1. 用途に応じてツールを使い分ける

#### 推奨の使い分け

| 用途 | 推奨ツール | 理由 |
|------|-----------|------|
| 日常的なコードレビュー | delta | 構文ハイライト、美しい表示 |
| フォーマット変更の確認 | difftastic | 構造的Diff、フォーマット無視 |
| 大規模な変更 | icdiff, ydiff | サイドバイサイド表示 |
| 詳細レビュー | VS Code, Meld | GUI、高度な機能 |
| シンプルな確認 | colordiff | 軽量、高速 |

### 2. カスタム引数で表示を最適化

#### deltaの最適化例

```bash
# サイドバイサイド表示
kiro-cli settings chat.diffTool "delta --side-by-side"

# テーマ指定
kiro-cli settings chat.diffTool "delta --theme=Dracula"

# 行番号非表示
kiro-cli settings chat.diffTool "delta --line-numbers=false"
```

#### 複数の引数を組み合わせ

```bash
kiro-cli settings chat.diffTool "delta --side-by-side --theme=Dracula --line-numbers"
```

### 3. プロジェクトごとに設定を変える

#### Agent設定ファイルでの指定

```json
{
  "name": "frontend-agent",
  "description": "Frontend development agent",
  "settings": {
    "chat": {
      "diffTool": "delta --side-by-side"
    }
  }
}
```

```json
{
  "name": "backend-agent",
  "description": "Backend development agent",
  "settings": {
    "chat": {
      "diffTool": "difft"
    }
  }
}
```

**メリット**:
- プロジェクトの特性に合わせた設定
- チーム内で統一された表示
- 自動的に適切なツールを使用

### 4. ツールのインストール確認

#### 事前確認

```bash
# ツールがインストールされているか確認
which delta
which difft
which icdiff

# バージョン確認
delta --version
difft --version
icdiff --version
```

#### インストールスクリプト

```bash
#!/bin/bash
# install-diff-tools.sh

# delta
if ! command -v delta &> /dev/null; then
    echo "Installing delta..."
    brew install git-delta
fi

# difftastic
if ! command -v difft &> /dev/null; then
    echo "Installing difftastic..."
    brew install difftastic
fi

# icdiff
if ! command -v icdiff &> /dev/null; then
    echo "Installing icdiff..."
    pip install icdiff
fi

echo "All diff tools installed!"
```

### 5. GUIツールの制限を理解する

#### GUIツールの動作

- **表示専用**: 一時ファイルを表示
- **編集不可**: GUI内での編集は保存されない
```
- **承認のみ**: Kiroの提案を承認するかどうかの判断のみ

#### 推奨される使い方

```bash
# GUIツールは詳細レビュー時のみ使用
kiro-cli settings chat.diffTool code

# 日常的な作業はターミナルツールを使用
kiro-cli settings chat.diffTool delta
```

### 6. 組み込みDiffとの使い分け

#### 組み込みDiffが適している場合

- 外部ツールをインストールできない環境
- シンプルな変更の確認
- 高速な確認が必要な場合

#### Custom Diff Toolsが適している場合

- 複雑な変更のレビュー
- 視認性を重視する場合
- チーム内で統一された表示が必要な場合

### 7. チーム内での標準化

#### チーム標準の設定

```json
{
  "name": "team-standard-agent",
  "description": "Team standard agent",
  "settings": {
    "chat": {
      "diffTool": "delta --side-by-side --theme=Dracula"
    }
  }
}
```

**メリット**:
- チーム内で統一された表示
- レビュー時のコミュニケーションが円滑
- 新メンバーのオンボーディングが容易

## トラブルシューティング

### 問題1: Diffツールが見つからない

#### 症状

```bash
kiro-cli chat

> ファイルを変更して
# エラー: Couldn't find the diff tool 'delta'
```

#### 原因と対処法

**原因: ツールがインストールされていない**

```bash
# ツールの存在確認
which delta
# 出力: delta not found
```

**対処法**: ツールをインストール

```bash
# macOS
brew install git-delta

# Ubuntu/Debian
sudo apt install git-delta

# インストール確認
delta --version
```

### 問題2: カスタム引数が認識されない

#### 症状

```bash
kiro-cli settings chat.diffTool "delta --side-by-side"

# Diff表示時にサイドバイサイド表示されない
```

#### 原因と対処法

**原因1: 引数の構文エラー**

```bash
# 設定確認
kiro-cli settings chat.diffTool
# 出力: delta --side-by-side

# 正しい構文か確認
delta --help | grep side-by-side
```

**対処法**: 正しい引数を指定

```bash
# 正しい引数を確認してから設定
kiro-cli settings chat.diffTool "delta --side-by-side"
```

**原因2: クォートの問題**

```bash
# ❌ 間違い
kiro-cli settings chat.diffTool delta --side-by-side

# ✅ 正しい
kiro-cli settings chat.diffTool "delta --side-by-side"
```

### 問題3: GUIツールが起動しない

#### 症状

```bash
kiro-cli settings chat.diffTool code

> ファイルを変更して
# エラー: Failed to launch VS Code
```

#### 原因と対処法

**原因1: VS Codeのコマンドラインツールが未インストール**

**対処法**:

1. VS Codeを起動
2. Command Palette（Cmd+Shift+P）を開く
3. "Shell Command: Install 'code' command in PATH"を実行
```

**原因2: パスが通っていない**

```bash
# codeコマンドの確認
which code
# 出力: code not found
```

**対処法**: パスを追加

```bash
# macOS
export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"

# .zshrcまたは.bashrcに追加
echo 'export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"' >> ~/.zshrc
```

### 問題4: 設定が反映されない

#### 症状

```bash
kiro-cli settings chat.diffTool delta

# Kiro CLIを起動しても組み込みDiffが使用される
```

#### 原因と対処法

**原因: Agent設定が優先されている**

```bash
# Agent設定ファイルを確認
cat .kiro/agents/my-agent.json
```

**対処法**: Agent設定を更新

```json
{
  "settings": {
    "chat": {
      "diffTool": "delta"
    }
  }
}
```

または、Agent設定を削除してグローバル設定を使用

### 問題5: Diffツールのバージョンが古い

#### 症状

```bash
# 新しい引数が認識されない
kiro-cli settings chat.diffTool "delta --new-feature"
# エラー: Unknown option '--new-feature'
```

#### 原因と対処法

**原因: ツールのバージョンが古い**

```bash
# バージョン確認
delta --version
# 出力: delta 0.8.0
```

**対処法**: ツールをアップデート

```bash
# macOS
brew upgrade git-delta

# Ubuntu/Debian
sudo apt update
sudo apt upgrade git-delta

# バージョン確認
delta --version
# 出力: delta 0.17.0
```

## まとめ

### Custom Diff Tools機能の重要ポイント

1. **15種類以上のツール対応**: ターミナルツール8種類、GUIツール7種類
2. **簡単な設定**: `kiro-cli settings`コマンドで設定
3. **カスタム引数対応**: ツールに独自の引数を渡すことが可能
4. **プロジェクトごとの設定**: Agent設定ファイルで指定可能

### 推奨されるツール

| 用途 | 推奨ツール |
|------|-----------|
| 日常的なコードレビュー | delta |
| フォーマット変更の確認 | difftastic |
| 大規模な変更 | icdiff, ydiff |
| 詳細レビュー | VS Code, Meld |
| シンプルな確認 | colordiff |

### ベストプラクティスのまとめ

1. **用途に応じた使い分け**: 日常はdelta、詳細レビューはGUIツール
2. **カスタム引数の活用**: 表示を最適化
3. **プロジェクトごとの設定**: Agent設定ファイルで指定
4. **ツールのインストール確認**: 事前に確認
5. **GUIツールの制限理解**: 表示専用、編集不可
6. **チーム内での標準化**: 統一された表示

### 次のステップ

1. **ツールのインストール**: 好みのDiffツールをインストール
2. **Kiro CLIでの設定**: `kiro-cli settings chat.diffTool`で設定
3. **動作確認**: ファイル変更を依頼してDiff表示を確認
4. **カスタマイズ**: カスタム引数で表示を最適化

### 参考リンク

- [Kiro CLI v1.24.0 Changelog](https://kiro.dev/changelog/cli/1-24/)
- [Custom Diff Tools Documentation](https://kiro.dev/docs/cli/chat/diff-tools/)
- [delta GitHub](https://github.com/dandavison/delta)
- [difftastic GitHub](https://github.com/Wilfred/difftastic)

---

**Custom Diff Tools機能を活用して、コードレビューをより快適で効率的にしましょう！**
