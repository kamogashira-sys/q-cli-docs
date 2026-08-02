#!/bin/bash
# Test for check-commands.sh
# Purpose: Verify check-commands.sh のゲートが実効性を持つこと
#
# 対象とする既知バグ:
#   1. shellcheck_errors=0 のハードコードにより常に exit 0 になる
#   2. 全ブロックを1ファイルに連結するため最初のパースエラーで解析が打ち切られる
#   3. 報告される行番号が連結後のもので、元ファイル名が分からない

set -e

cd "$(dirname "$0")/.."

TOOL="./scripts/check-commands.sh"
FIXTURE="docs/05_meta/13_validation-reference.md"
BACKUP="/tmp/test_check_commands_backup_$$.md"

cleanup() {
    if [ -f "$BACKUP" ]; then
        cp "$BACKUP" "$FIXTURE"
        rm -f "$BACKUP"
    fi
}
trap cleanup EXIT

# ===== Test 1: 現状の docs/ で exit 0 になること（REQUIRED）=====

echo "Test 1: 現状の docs/ で問題なし"

set +e
$TOOL > /tmp/test_cc_base_$$.txt 2>&1
rc=$?
set -e

if [ "$rc" -eq 0 ]; then
    blocks=$(grep -oP '抽出したブロック数: \K[0-9]+' /tmp/test_cc_base_$$.txt | head -1)
    echo "✅ Test 1 passed: $blocks ブロックを検査して exit 0"
else
    echo "❌ Test 1 failed: exit $rc（期待値 0）"
    tail -20 /tmp/test_cc_base_$$.txt | sed 's/^/    /'
    rm -f /tmp/test_cc_base_$$.txt
    exit 1
fi
rm -f /tmp/test_cc_base_$$.txt

# ===== Test 2: 既知バグ - 壊れた bash を検出すること（REQUIRED）=====
#
# 旧実装は shellcheck_errors=0 のハードコードにより、何を検出しても
# exit 0 を返していた。

echo ""
echo "Test 2: 壊れた bash を検出して exit 1"

cp "$FIXTURE" "$BACKUP"
cat >> "$FIXTURE" << 'EOF'

## テスト用（自動テストが追記）

```bash
if [ -f foo.txt
  echo "broken"
fi
```
EOF

set +e
out=$($TOOL 2>&1)
rc=$?
set -e

cp "$BACKUP" "$FIXTURE"

if [ "$rc" -eq 1 ]; then
    echo "✅ Test 2 passed: 構文エラーを検出して exit 1"
else
    echo "❌ Test 2 failed: exit $rc（期待値 1）"
    echo "   旧実装は shellcheck_errors=0 のハードコードで常に exit 0 だった"
    exit 1
fi

# ===== Test 3: ファイル名と行番号が報告されること（REQUIRED）=====
#
# 14_tool-creation-checklist.md の規約。旧実装は連結後の行番号しか出さなかった。

echo ""
echo "Test 3: ファイル名と行番号が報告されること"

if grep -q "$FIXTURE" <<< "$out" && grep -qP "$FIXTURE:[0-9]+" <<< "$out"; then
    line=$(grep -oP "$(basename "$FIXTURE"):\K[0-9]+" <<< "$out" | head -1)
    echo "✅ Test 3 passed: $(basename "$FIXTURE"):$line として報告"
else
    echo "❌ Test 3 failed: ファイル名:行番号 の形式で報告されていない"
    echo "$out" | grep -A2 '構文エラー' | sed 's/^/    /'
    exit 1
fi

# ===== Test 4: 連結せずブロック単位で解析すること =====
#
# 旧実装は7,498行を1ファイルに連結し、最初のパースエラーで解析が止まって
# 実質1件しか報告できなかった。複数の壊れたブロックを入れて複数報告される
# ことを確認する。

echo ""
echo "Test 4: 複数の壊れたブロックをすべて報告すること"

cat >> "$FIXTURE" << 'EOF'

## テスト用その2（自動テストが追記）

```bash
if [ -f a.txt
  echo "broken 1"
fi
```

```bash
while true
  echo "broken 2"
done
```
EOF

set +e
out2=$($TOOL 2>&1)
set -e
cp "$BACKUP" "$FIXTURE"

n=$(grep -c 'のコードブロックに構文エラー' <<< "$out2" || true)
if [ "$n" -ge 2 ]; then
    echo "✅ Test 4 passed: $n 件のブロックを個別に報告"
else
    echo "❌ Test 4 failed: $n 件しか報告されなかった（期待値 2以上）"
    echo "   連結方式では最初のパースエラーで解析が打ち切られる"
    exit 1
fi

# ===== Test 5: メタ構文ブロックを対象外にすること =====
#
# REPL の対話ログ等は bash タグが付いていてもシェルスクリプトではない。

echo ""
echo "Test 5: REPL 対話ログを対象外にすること"

cat >> "$FIXTURE" << 'EOF'

## テスト用その3（自動テストが追記）

```bash
> このプロジェクトのテストを作成して
/context show
Ctrl+T でツール一覧
```
EOF

set +e
$TOOL > /dev/null 2>&1
rc=$?
set -e
cp "$BACKUP" "$FIXTURE"

if [ "$rc" -eq 0 ]; then
    echo "✅ Test 5 passed: REPL ログは対象外（exit 0 を維持）"
else
    echo "❌ Test 5 failed: REPL ログでエラーになった（exit $rc）"
    exit 1
fi

# ===== Test 6: メタ構文の判別が error ブロックのみに適用されること =====
#
# 判別ルールを全ブロックに前置きで適用すると、正常なブロックまで検査対象から
# 外れる（実測: REPL ルール単体で error なしブロック237件が該当）。
# REPL パターンを含みつつ構文エラーもあるブロックは除外されて構わないが、
# REPL パターンを含む正常なブロックが「除外」に計上されないことを確認する。

echo ""
echo "Test 6: 判別ルールが error ブロックのみに適用されること"

skipped=$($TOOL 2>&1 | grep -oP 'メタ構文として除外: \K[0-9]+' | head -1)
if [ "$skipped" -le 50 ]; then
    echo "✅ Test 6 passed: 除外は $skipped ブロック（error ブロックに限定）"
else
    echo "❌ Test 6 failed: 除外が $skipped ブロックと多すぎる"
    echo "   判別ルールが全ブロックに適用されている疑いがある"
    exit 1
fi

# ===== Test 7: --list-skipped で除外理由が表示されること =====

echo ""
echo "Test 7: --list-skipped で除外理由を表示"

if $TOOL --list-skipped 2>&1 | grep -q '除外したブロック'; then
    echo "✅ Test 7 passed: 除外理由が表示される"
else
    echo "❌ Test 7 failed: --list-skipped が機能していない"
    exit 1
fi

# ===== Test 8: CI（validate_commands.sh）にデグレードがないこと =====
#
# text へのリタグ方式を採ると verify-commands.yml が検証する q コマンドが
# 減る。ツール側判別方式を採っている限り抽出件数は維持される。

echo ""
echo "Test 8: CI の q コマンド抽出件数が維持されていること"

if [ -x ./scripts/validate_commands.sh ]; then
    n=$(./scripts/validate_commands.sh 2>&1 \
        | grep -oP '抽出したコマンド行数: \K[0-9]+' | head -1)
    if [ -n "$n" ] && [ "$n" -ge 600 ]; then
        echo "✅ Test 8 passed: validate_commands.sh の抽出 $n 行"
    else
        echo "❌ Test 8 failed: 抽出が $n 行（期待値 600以上）"
        echo '   bash タグをリタグすると CI の検証対象が減る'
        exit 1
    fi
else
    echo "⏭️  Test 8 skipped: scripts/validate_commands.sh がない"
fi

echo ""
echo "✅ All tests passed"
exit 0
