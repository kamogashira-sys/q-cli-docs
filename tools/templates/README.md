# ツールテンプレート

新しいチェックツールを作成するためのテンプレートです。

## 使い方

### 1. 作成スクリプトを使用（推奨）

```bash
./tools/create-check-tool.sh check-your-tool "Check for your issue"
```

### 2. 手動でコピー

```bash
# ツールをコピー
cp tools/templates/check-tool-template.sh tools/check-your-tool.sh

# テストをコピー
cp tools/templates/test-tool-template.sh tools/test-check-your-tool.sh

# 実行権限付与
chmod +x tools/check-your-tool.sh tools/test-check-your-tool.sh
```

## カスタマイズ方法

### ツールファイル（check-tool-template.sh）

1. **プレースホルダーを置換**
   - `[TOOL_NAME]`: ツール名
   - `[PURPOSE]`: 目的
   - `[AUTHOR]`: 作成者
   - `[DATE]`: 作成日
   - `[WHAT]`: 何をチェックするか

2. **check_file()関数を実装**
   ```bash
   check_file() {
       local file="$1"
       
       # 検出ロジックを実装
       if [条件]; then
           echo "❌ ERROR: $file: 問題の説明"
           ERRORS=$((ERRORS + 1))
       fi
   }
   ```

### テストファイル（test-tool-template.sh）

1. **プレースホルダーを置換**
   - `[TOOL_NAME]`: ツール名

2. **既知のバグ内容を追加**
   ```bash
   cat > "$TEST_DIR/bug.md" << 'EOF'
   実際のバグ内容
   EOF
   ```

3. **正常な内容を追加**
   ```bash
   cat > "$TEST_DIR/normal.md" << 'EOF'
   正常な内容
   EOF
   ```

## ベストプラクティス

### 1. シンプルに保つ

- 複雑な正規表現より行単位処理
- awkやgrepを適切に使い分け
- デバッグしやすい実装

### 2. 出力を明確に

```bash
# 良い例
echo "❌ ERROR: $file:$line: Duplicate header found"

# 悪い例
echo "Error"
```

### 3. 必ずテストする

- 既知のバグで異常系テスト
- 正常ファイルで正常系テスト
- 出力内容を目視確認

### 4. エラーハンドリング

```bash
set -e  # エラーで即座に終了

# ファイル存在確認
if [ ! -f "$file" ]; then
    echo "❌ File not found: $file"
    exit 2
fi
```

## テンプレートの構造

### ツールテンプレート

```
#!/bin/bash
├── Configuration    # 設定（引数、変数）
├── Functions        # 関数定義
│   └── check_file() # メイン検出ロジック
├── Main             # メイン処理
│   └── find + while # ファイル走査
└── Report           # 結果レポート
```

### テストテンプレート

```
#!/bin/bash
├── Setup           # テスト環境準備
├── Test 1          # 異常系（必須）
├── Test 2          # 正常系（必須）
└── Cleanup         # 後片付け
```

## 例: 連続区切り線チェックツール

### ツール実装

```bash
check_file() {
    local file="$1"
    
    awk '/^---$/ {
        if (prev == "---" && NR - prev_line <= 2) {
            print FILENAME ":" prev_line "-" NR ": Consecutive separators"
            found = 1
        }
        prev = "---"
        prev_line = NR
    }' "$file"
    
    if [ $? -ne 0 ]; then
        ERRORS=$((ERRORS + 1))
    fi
}
```

### テスト実装

```bash
# Test 1: Known bug
cat > "$TEST_DIR/bug.md" << 'EOF'
---

---
EOF

# Test 2: Normal
cat > "$TEST_DIR/normal.md" << 'EOF'
---

Content

---
EOF
```

## トラブルシューティング

### テストが失敗する

1. ツールが正しく検出しているか確認
2. テストの期待値が正しいか確認
3. 出力フォーマットが一致しているか確認

### ツールが動作しない

1. 実行権限があるか確認: `chmod +x`
2. シェバン行があるか確認: `#!/bin/bash`
3. set -e でエラー箇所を特定

## 参考

- [ツール作成チェックリスト](../../docs/05_meta/14_tool-creation-checklist.md)
- [問題分析と教訓](../../docs/05_meta/07_lessons-learned.md)
- [自動化ツール](../../docs/05_meta/05_automation-tools.md)
