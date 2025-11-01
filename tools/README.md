# Tools - 自動化ツール

このディレクトリには、ドキュメント品質を保証するための自動化ツールが含まれています。

---

## 📋 ツール一覧

### チェックツール

| ツール | 目的 | テスト |
|--------|------|--------|
| [check-consecutive-separators.sh](#check-consecutive-separatorssh) | 連続区切り線検出 | ✅ |

### 管理ツール

| ツール | 目的 |
|--------|------|
| [create-check-tool.sh](#create-check-toolsh) | 新規ツール作成 |
| [verify-tool-tests.sh](#verify-tool-testssh) | テスト存在確認 |

---

## 🔧 チェックツール

### check-consecutive-separators.sh

**目的**: 連続した区切り線（`---\n\n---`）を検出

**使用方法**:
```bash
./tools/check-consecutive-separators.sh [directory]

# 例
./tools/check-consecutive-separators.sh docs/
```

**検出パターン**:
```markdown
---

---
```

**出力例**:
```bash
# 問題あり
❌ docs/example.md:10-12: Consecutive separators
❌ Found 1 file(s) with consecutive separators

# 問題なし
✅ No consecutive separators found
```

**テスト**:
```bash
./tools/test-check-consecutive-separators.sh
```

---

## 🛠️ 管理ツール

### create-check-tool.sh

**目的**: テンプレートから新規チェックツールを作成

**使用方法**:
```bash
./tools/create-check-tool.sh <tool-name> [purpose]

# 例
./tools/create-check-tool.sh check-duplicate-headers "Check for duplicate headers"
```

**生成されるファイル**:
- `tools/check-<name>.sh` - ツール本体
- `tools/test-check-<name>.sh` - テスト

**制約**:
- ツール名は `check-` で始まる必要がある
- 既存ツールと重複不可

**詳細**: [templates/README.md](templates/README.md)

---

### verify-tool-tests.sh

**目的**: 全チェックツールのテスト存在確認

**使用方法**:
```bash
./tools/verify-tool-tests.sh
```

**出力例**:
```bash
# 全てOK
✅ check-consecutive-separators.sh has test
✅ All tools have tests

# テスト不足
❌ Missing test: tools/test-check-example.sh
❌ 1 tool(s) missing tests
```

**統合**:
- pre-commitフックで自動実行
- ツール変更時のみチェック

---

## 📁 ディレクトリ構造

```
tools/
├── README.md                              # このファイル
├── check-consecutive-separators.sh        # 連続区切り線チェック
├── test-check-consecutive-separators.sh   # テスト
├── create-check-tool.sh                   # ツール作成スクリプト
├── verify-tool-tests.sh                   # テスト検証スクリプト
└── templates/                             # テンプレート
    ├── README.md                          # テンプレート使用方法
    ├── check-tool-template.sh             # ツールテンプレート
    └── test-tool-template.sh              # テストテンプレート
```

---

## 🚀 新規ツール作成手順

### クイックスタート（5分）

```bash
# 1. テンプレートから作成
./tools/create-check-tool.sh check-your-tool "Check for your issue"

# 2. ツール実装
vim tools/check-your-tool.sh
# → check_file()関数を実装

# 3. テスト実装
vim tools/test-check-your-tool.sh
# → 既知のバグ内容を追加

# 4. テスト実行
./tools/test-check-your-tool.sh

# 5. 動作確認
./tools/check-your-tool.sh docs/

# 6. 統合
git add tools/check-your-tool.sh tools/test-check-your-tool.sh
git commit -m "feat: add your tool"
```

**詳細手順**: [templates/README.md](templates/README.md)

---

## ✅ 品質保証

### テストカバレッジ

**目標**: 100%

**確認方法**:
```bash
./tools/verify-tool-tests.sh
```

### 自動検証

**pre-commitフック**:
- ツール変更時にテスト存在確認
- 連続区切り線チェック

**pre-pushフック**:
- 連続区切り線チェック

---

## 📖 ドキュメント

### ツール作成者向け

- **[ツール作成チェックリスト](../docs/05_meta/14_tool-creation-checklist.md)** - 必須チェック項目
- **[テンプレート使用方法](templates/README.md)** - 詳細な使い方
- **[自動化ツール](../docs/05_meta/05_automation-tools.md)** - ツール一覧と使用方法
- **[日常ワークフロー](../docs/05_meta/09_daily-workflow.md)** - ツール作成手順

### 開発者向け

- **[問題分析と教訓](../docs/05_meta/07_lessons-learned.md)** - 過去の失敗と対策
- **[品質原則](../docs/05_meta/04_quality-principles.md)** - 9つの作業原則

---

## 🔍 トラブルシューティング

### ツールが実行できない

```bash
# 実行権限を付与
chmod +x tools/check-*.sh tools/test-*.sh
```

### テストが失敗する

```bash
# デバッグ実行
bash -x ./tools/test-check-your-tool.sh

# 手動でツールを実行
./tools/check-your-tool.sh /tmp/test_dir
```

### pre-commitでエラー

```bash
# テスト存在確認
./tools/verify-tool-tests.sh

# テストファイルを作成
cp tools/templates/test-tool-template.sh tools/test-check-your-tool.sh
```

---

## 📊 統計情報

- **チェックツール数**: 1
- **テストカバレッジ**: 100%
- **自動化率**: 95%

---

## 🎯 ベストプラクティス

### 1. テンプレートを使用

```bash
# 推奨
./tools/create-check-tool.sh check-new-tool "Purpose"

# 非推奨（手動作成）
vim tools/check-new-tool.sh
```

### 2. 必ずテストを作成

```bash
# 全てのツールにテストが必要
./tools/verify-tool-tests.sh
# → ✅ All tools have tests
```

### 3. 既知のバグでテスト

```bash
# Test 1: 既知のバグを検出できることを確認
cat > /tmp/bug.md << 'EOF'
[既知のバグ内容]
EOF
./tools/check-new-tool.sh /tmp
# → バグが検出されることを確認
```

### 4. シンプルに保つ

```bash
# 良い例: awkで行単位処理
awk '/pattern/ { print }' file

# 悪い例: 複雑な正規表現
grep -Pzo 'complex.*pattern.*\n.*more' file
```

---

## 🔗 関連リンク

- [GitHub Repository](https://github.com/kamogashira-sys/q-cli-docs)
- [ドキュメントサイト](../docs/README.md)
- [品質保証](../docs/05_meta/README.md)

---

**最終更新**: 2025-11-01
