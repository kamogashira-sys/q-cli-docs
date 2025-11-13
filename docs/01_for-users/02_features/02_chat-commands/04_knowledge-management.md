[ホーム](../../../README.md) > [ユーザーガイド](../../README.md) > [機能ガイド](../README.md) > [チャット機能](../01_chat.md) > Knowledge管理

---

# Knowledge管理

**対象バージョン**: v1.13.0以降

> **🧪 Beta機能**: Knowledge機能は開発中です。`q settings chat.enableKnowledge true`で有効化してください。

## 📋 コマンド概要

Knowledge管理機能は、プロジェクトのファイルやドキュメントをインデックス化してAIが参照できるようにする機能です。ドキュメント、ソースコード、PDFファイルなどを効率的に管理し、AIによる高精度な回答を実現します。

## 🚀 基本的な使い方

### Knowledge管理コマンド一覧

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/knowledge show` | 現在のKnowledge情報を表示。インデックス化されたファイル数、合計サイズ、最終更新日時を確認できる（v1.18.0+: statusと統合） | プロジェクトのどのファイルがAIの参照対象になっているか確認したい時 |
| `/knowledge add -n <名前> -p <パス> [オプション]` | 指定したファイル/ディレクトリをKnowledgeに追加してインデックス化。`--include`でパターン指定、`--exclude`で除外パターン指定、`--index-type`でインデックスタイプ指定が可能 | 新しいドキュメントフォルダをAIの参照対象に追加したい時 |
| `/knowledge remove <path>` | 指定したパスのエントリをKnowledgeから削除。インデックスから除外される | 不要になった古いドキュメントをAIの参照対象から外したい時 |
| `/knowledge update <path>` | 指定したエントリを再インデックス化。ファイル内容を更新した後に実行すると、最新の内容がAIに反映される | ドキュメントを編集した後、変更内容をAIに認識させたい時 |
| `/knowledge clear` | すべてのKnowledgeエントリを削除してインデックスをリセット。プロジェクト切り替え時に便利 | 別のプロジェクトに切り替える時、前のプロジェクトの情報をクリアしたい時 |
| `/knowledge cancel` | バックグラウンドで実行中のインデックス化処理をキャンセル | 誤って大量のファイルを追加した時、処理を中断したい時 |

### 基本例

```bash
# Knowledge機能を有効化
q settings chat.enableKnowledge true

# 現在の状態を確認
/knowledge show

# ドキュメントフォルダを追加
/knowledge add -n "project-docs" -p ./docs

# 特定のファイルを追加
/knowledge add -n "readme" -p ./README.md
```

## ⚙️ オプション・引数

### `/knowledge add` コマンド

| オプション | 説明 | 必須 | 例 |
|-----------|------|------|-----|
| `-n, --name <名前>` | Knowledgeエントリの名前 | はい | `-n "project-docs"` |
| `-p, --path <パス>` | インデックス化するファイル/ディレクトリのパス | はい | `-p ./docs` |
| `--include <パターン>` | 含めるファイルのパターン | いいえ | `--include "*.md,*.txt"` |
| `--exclude <パターン>` | 除外するファイルのパターン | いいえ | `--exclude "*.log,*.tmp"` |
| `--index-type <タイプ>` | インデックスタイプの指定 | いいえ | `--index-type semantic` |

### サポートファイル形式（v1.18.0+）

| ファイル形式 | 拡張子 | 対応状況 | 備考 |
|-------------|--------|----------|------|
| **テキストファイル** | `.txt`, `.md` | ✅ 完全対応 | マークダウン、プレーンテキスト |
| **ソースコード** | `.py`, `.js`, `.ts`, `.java`, `.go`, etc. | ✅ 完全対応 | 主要プログラミング言語 |
| **PDF** | `.pdf` | ✅ v1.19.0で追加 | テキストベースのPDFのみ |

**PDF対応の特徴**:
- ✅ テキストベースのPDFファイルに対応
- ✅ ドキュメント、マニュアル、仕様書などを直接インデックス化
- ⚠️ スキャン画像のみのPDFは非対応の可能性
- ⚠️ パスワード保護されたPDFは非対応の可能性

## 💡 実用例

### 例1: プロジェクトドキュメントの包括的インデックス化

**シナリオ**: 新しいプロジェクトでドキュメント全体をAIに認識させたい

```bash
# Knowledge機能を有効化
q settings chat.enableKnowledge true

# プロジェクト全体のドキュメントを追加
/knowledge add -n "project-docs" -p ./docs --include "*.md,*.txt,*.pdf"

# ソースコードも追加（テストファイルは除外）
/knowledge add -n "source-code" -p ./src --include "*.py,*.js,*.ts" --exclude "*test*,*spec*"

# 設定ファイルを追加
/knowledge add -n "config" -p ./config

# 現在の状態を確認
/knowledge show
```

**結果**: プロジェクトの全体像をAIが把握し、コンテキストに応じた適切な回答を提供できる

### 例2: 段階的なKnowledge構築と更新

**シナリオ**: 開発進行に合わせてKnowledgeを段階的に更新したい

```bash
# 初期段階：基本ドキュメントのみ
/knowledge add -n "basic-docs" -p ./README.md
/knowledge add -n "api-spec" -p ./api-specification.pdf

# 開発進行：実装ファイルを追加
/knowledge add -n "core-modules" -p ./src/core --include "*.py"

# ドキュメント更新後：再インデックス化
/knowledge update "basic-docs"

# 新機能追加：新しいモジュールを追加
/knowledge add -n "feature-x" -p ./src/features/x

# 不要になった古い仕様書を削除
/knowledge remove "./old-spec.pdf"
```

**結果**: 開発の進行に合わせて、常に最新の情報をAIが参照できる状態を維持

### 例3: 大規模プロジェクトでの効率的なKnowledge管理

**シナリオ**: 大規模なプロジェクトで必要な部分のみを効率的にインデックス化したい

```bash
# 現在の作業に関連する部分のみを追加
/knowledge add -n "current-feature" -p ./src/features/user-auth --include "*.py,*.md"

# 共通ライブラリを追加
/knowledge add -n "common-libs" -p ./src/lib --exclude "*test*,*mock*"

# 関連ドキュメントのみを追加
/knowledge add -n "auth-docs" -p ./docs/authentication --include "*.md,*.pdf"

# インデックス化の進行状況を確認
/knowledge show

# 処理が重い場合はキャンセル
/knowledge cancel

# 必要に応じて範囲を絞って再実行
/knowledge add -n "auth-core" -p ./src/features/user-auth/core.py
```

**結果**: 大規模プロジェクトでも必要な情報のみを効率的に管理し、パフォーマンスを維持

## 🔧 トラブルシューティング

### よくある問題

#### 問題1: Knowledge機能が使用できない

**症状**: `/knowledge` コマンドが認識されない

**原因**: Knowledge機能が有効化されていない

**解決策**:
```bash
# Knowledge機能を有効化
q settings chat.enableKnowledge true

# 設定を確認
q settings list | grep Knowledge

# チャットを再起動
/quit
q chat
```

#### 問題2: ファイルがインデックス化されない

**症状**: `/knowledge add` を実行してもファイルが追加されない

**原因**: ファイルパスの間違い、またはサポートされていないファイル形式

**解決策**:
```bash
# ファイルの存在を確認
ls -la ./docs

# サポートされているファイル形式を確認
file ./document.pdf

# 絶対パスで試行
/knowledge add -n "test" -p "/full/path/to/file.md"

# パターンを明示的に指定
/knowledge add -n "docs" -p ./docs --include "*.md,*.txt"
```

#### 問題3: PDFファイルが正しく処理されない

**症状**: PDFファイルを追加してもコンテンツが参照されない

**原因**: スキャン画像のPDF、またはパスワード保護されたPDF

**解決策**:
```bash
# PDFの種類を確認
file ./document.pdf

# テキストベースのPDFかテスト
pdftotext ./document.pdf -

# 別のPDFで試行
/knowledge add -n "test-pdf" -p ./text-based-document.pdf

# テキストファイルに変換してから追加
pdftotext ./document.pdf ./document.txt
/knowledge add -n "converted-doc" -p ./document.txt
```

#### 問題4: インデックス化処理が遅い

**症状**: 大量のファイルを追加すると処理が非常に遅い

**原因**: ファイル数が多すぎる、またはファイルサイズが大きすぎる

**解決策**:
```bash
# 処理をキャンセル
/knowledge cancel

# 範囲を絞って再実行
/knowledge add -n "essential-docs" -p ./docs --include "*.md" --exclude "*draft*,*temp*"

# ファイル数を確認
find ./docs -name "*.md" | wc -l

# 段階的に追加
/knowledge add -n "core-docs" -p ./docs/core
/knowledge add -n "api-docs" -p ./docs/api
```

#### 問題5: 更新したファイルが反映されない

**症状**: ファイルを編集したが、AIが古い内容を参照している

**原因**: インデックスが更新されていない

**解決策**:
```bash
# 特定のエントリを更新
/knowledge update "project-docs"

# 全体を再インデックス化
/knowledge clear
/knowledge add -n "updated-docs" -p ./docs

# 現在の状態を確認
/knowledge show
```

## 🔗 関連コマンド

- [コンテキスト管理](02_context-management.md) - `/context`によるセッション内ファイル管理
- [基本コマンド・会話管理](01_basic-commands.md) - `/save`、`/load`による設定の永続化
- [開発者向けコマンド](08_developer-commands.md) - `/usage`による使用量監視

## 📖 参照元

- [チャット機能概要](../01_chat.md#knowledge管理) - Knowledge管理の概要

---

最終更新: 2025年11月13日
