#!/bin/bash
# Test for check-completeness.py
# Purpose: Verify check-completeness.py detects known bugs and avoids false positives
#
# 対象とする既知バグ:
#   1. 余分な ``` による空ブロック（06_troubleshooting.md L711 型）
#   2. 3バッククォートのネスト（07_experimental.md L640 / 04_best-practices.md L2306 型）
#   3. 読み込みエラーを「スキップ」に吸収して成功扱いにするバグ

set -e

cd "$(dirname "$0")/.."

TOOL="./scripts/check-completeness.py"
TEST_DIR="/tmp/test_check_completeness_$$"

# ===== Setup =====

echo "Setting up test environment..."
mkdir -p "$TEST_DIR"

# 構造規約を満たす最小のドキュメント本体（末尾に追記して各ケースを作る）
write_valid_header() {
    cat > "$1" << 'EOF'
[ホーム](../README.md) > テスト

---

# テストドキュメント

## セクション

EOF
}

write_footer() {
    cat >> "$1" << 'EOF'

---

最終更新: 2026-08-02
EOF
}

# ===== Test 1: 余分な ``` による空ブロックを検出（REQUIRED）=====

echo ""
echo "Test 1: 余分な閉じフェンス（L711型）の検出"
f="$TEST_DIR/bug_extra_fence.md"
write_valid_header "$f"
cat >> "$f" << 'EOF'
```bash
echo hi
```
```

段落テキスト

```json
{"a": 1}
```
EOF
write_footer "$f"

if $TOOL "$f" 2>&1 | grep -q "余分な閉じフェンス"; then
    echo "✅ Test 1 passed: 余分な閉じフェンスを検出"
else
    echo "❌ Test 1 failed: 余分な閉じフェンスを検出できなかった"
    rm -rf "$TEST_DIR"
    exit 1
fi

# ===== Test 2: 3バッククォートのネストを検出（REQUIRED）=====

echo ""
echo "Test 2: 3バッククォートのネスト（L640型）の検出"
f="$TEST_DIR/bug_nested_fence.md"
write_valid_header "$f"
cat >> "$f" << 'EOF'
```markdown
# タイトル

## 使用方法
```bash
q chat
```
```

後続の段落
EOF
write_footer "$f"

if $TOOL "$f" 2>&1 | grep -q "3バッククォートのネスト"; then
    echo "✅ Test 2 passed: ネストフェンスを検出"
else
    echo "❌ Test 2 failed: ネストフェンスを検出できなかった"
    rm -rf "$TEST_DIR"
    exit 1
fi

# ===== Test 3: 正常系 - 4バッククォートのネストで偽陽性なし（REQUIRED）=====

echo ""
echo "Test 3: 正常系（4バッククォートのネスト）"
f="$TEST_DIR/ok_nested_fence.md"
write_valid_header "$f"
cat >> "$f" << 'EOF'
````markdown
# タイトル

## 使用方法
```bash
q chat
```
````

後続の段落
EOF
write_footer "$f"

if $TOOL "$f" > /dev/null 2>&1; then
    echo "✅ Test 3 passed: 偽陽性なし"
else
    echo "❌ Test 3 failed: 正常なネストで偽陽性が出た"
    $TOOL "$f" 2>&1 | sed 's/^/    /'
    rm -rf "$TEST_DIR"
    exit 1
fi

# ===== Test 4: 引用ブロック内のフェンスで偽陽性なし =====

echo ""
echo "Test 4: 引用ブロック内フェンス（> \`\`\`bash）"
f="$TEST_DIR/ok_blockquote_fence.md"
write_valid_header "$f"
cat >> "$f" << 'EOF'
> **補足**:
> ```bash
> q chat
> ```
EOF
write_footer "$f"

if $TOOL "$f" > /dev/null 2>&1; then
    echo "✅ Test 4 passed: 引用ブロック内フェンスで偽陽性なし"
else
    echo "❌ Test 4 failed: 引用ブロック内フェンスで偽陽性が出た"
    $TOOL "$f" 2>&1 | sed 's/^/    /'
    rm -rf "$TEST_DIR"
    exit 1
fi

# ===== Test 5: フェンス内の見出しを H1 と誤認しない =====

echo ""
echo "Test 5: フェンス内の見出しを誤認しない"
f="$TEST_DIR/ok_heading_in_fence.md"
write_valid_header "$f"
cat >> "$f" << 'EOF'
```bash
# これはコメントであって見出しではない
echo hi
```
EOF
write_footer "$f"

if $TOOL "$f" > /dev/null 2>&1; then
    echo "✅ Test 5 passed: フェンス内のコメントを見出しと誤認しない"
else
    echo "❌ Test 5 failed: フェンス内のコメントを見出しと誤認した"
    $TOOL "$f" 2>&1 | sed 's/^/    /'
    rm -rf "$TEST_DIR"
    exit 1
fi

# ===== Test 6: H1 欠落を検出 =====

echo ""
echo "Test 6: H1 欠落の検出"
f="$TEST_DIR/bug_no_h1.md"
cat > "$f" << 'EOF'
[ホーム](../README.md) > テスト

---

## セクションのみで H1 がない

本文

---

最終更新: 2026-08-02
EOF

if $TOOL "$f" 2>&1 | grep -q "H1 が 0 個"; then
    echo "✅ Test 6 passed: H1 欠落を検出"
else
    echo "❌ Test 6 failed: H1 欠落を検出できなかった"
    rm -rf "$TEST_DIR"
    exit 1
fi

# ===== Test 7: パンくず欠落を検出 =====

echo ""
echo "Test 7: パンくず欠落の検出"
f="$TEST_DIR/bug_no_breadcrumb.md"
cat > "$f" << 'EOF'
# タイトル

## セクション

本文

---

最終更新: 2026-08-02
EOF

if $TOOL "$f" 2>&1 | grep -q "パンくず"; then
    echo "✅ Test 7 passed: パンくず欠落を検出"
else
    echo "❌ Test 7 failed: パンくず欠落を検出できなかった"
    rm -rf "$TEST_DIR"
    exit 1
fi

# ===== Test 8: 読み込みエラーで exit 2（ツール自体のエラー）=====

echo ""
echo "Test 8: 読み込みエラーで exit 2"
f="$TEST_DIR/unreadable.md"
write_valid_header "$f"
write_footer "$f"
chmod 000 "$f"

set +e
$TOOL "$f" > /dev/null 2>&1
rc=$?
set -e
chmod 644 "$f"

if [ "$rc" -eq 2 ]; then
    echo "✅ Test 8 passed: 読み込みエラーで exit 2"
else
    echo "❌ Test 8 failed: exit $rc（期待値 2）"
    echo "   旧実装は読み込みエラーを「スキップ」に吸収して exit 0 にしていた"
    rm -rf "$TEST_DIR"
    exit 1
fi

# ===== Test 9: 終了コード規約（問題検出=1）=====

echo ""
echo "Test 9: 問題検出時の終了コードが 1"
set +e
$TOOL "$TEST_DIR/bug_no_h1.md" > /dev/null 2>&1
rc=$?
set -e

if [ "$rc" -eq 1 ]; then
    echo "✅ Test 9 passed: 問題検出で exit 1"
else
    echo "❌ Test 9 failed: exit $rc（期待値 1）"
    rm -rf "$TEST_DIR"
    exit 1
fi

# ===== Cleanup =====

rm -rf "$TEST_DIR"

echo ""
echo "✅ All tests passed"
exit 0
