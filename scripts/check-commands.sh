#!/bin/bash
# check-commands.sh - コマンド構文チェック
#
# 使用方法:
#   ./scripts/check-commands.sh
#   ./scripts/check-commands.sh --list-skipped   # 除外されたブロックの一覧
#
# 機能:
#   - ドキュメント内のbashコマンドブロックを抽出
#   - shellcheckで構文チェック（ブロック単位）
#   - Q CLI固有のコマンドチェック
#
# 終了コード:
#   0 = 問題なし / 1 = 問題検出 / 2 = ツール自体のエラー

set -euo pipefail

LIST_SKIPPED=false
[[ "${1:-}" == "--list-skipped" ]] && LIST_SKIPPED=true

echo "=== コマンド構文チェック ==="
echo ""

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

# 依存コマンドの確認（ツール自体のエラーは exit 2）
for cmd in shellcheck awk grep find; do
    if ! command -v "$cmd" > /dev/null 2>&1; then
        echo "❌ 必要なコマンドが見つかりません: $cmd" >&2
        exit 2
    fi
done

WORKDIR="$(mktemp -d /tmp/check-commands-XXXXXX)"
trap 'rm -rf "$WORKDIR"' EXIT

BLOCKS_DIR="$WORKDIR/blocks"
mkdir -p "$BLOCKS_DIR"

# ---------------------------------------------------------------------------
# コマンドブロックを抽出
#
# 旧実装は全ファイルの bash ブロックを1ファイル（7,498行）に連結してから
# shellcheck にかけていた。この方式では最初のパースエラーで解析が打ち切られ、
# 実質1件しか報告されない（実測: 連結1件 vs ブロック単位53件）。
# また報告される行番号が連結後のものになり、14_tool-creation-checklist.md の
# 「ファイル名と行番号を含める」規約に違反していた。
#
# ここではブロックごとに個別のファイルへ書き出し、元のファイル名と行番号を
# 保持する。
# ---------------------------------------------------------------------------
echo "🔍 コマンドブロックを抽出中..."

block_count=0
total_lines=0
file_seq=0

while IFS= read -r file; do
    # awk がブロック境界を検出し、各ブロックを "FILE:LINENO" ヘッダ付きで出力
    # ブロックの出自（元ファイル名・フェンス行番号）は連番ディレクトリ内の
    # meta ファイルに記録する。パスを名前へ埋め込むとアンダースコアを含む
    # 実際のパス（01_for-users 等）を復元できない。
    awk -v outdir="$BLOCKS_DIR" -v src="$file" -v seq="$file_seq" '
        /^```(bash|sh)[[:space:]]*$/ && !in_code {
            in_code = 1
            n++
            base = outdir "/" seq "-" n
            out = base ".sh"
            printf "" > out
            print src ":" NR > (base ".meta")
            next
        }
        /^```/ && in_code { in_code = 0; next }
        in_code { print >> out }
    ' "$file"
    file_seq=$((file_seq + 1))
done < <(find docs/ -name "*.md" -type f ! -name "*.bak")

block_count=$(find "$BLOCKS_DIR" -name "*.sh" -type f | wc -l)
total_lines=$(find "$BLOCKS_DIR" -name "*.sh" -type f -exec cat {} + 2>/dev/null | wc -l)

echo "   抽出したブロック数: $block_count"
echo "   抽出した行数: $total_lines"
echo ""

if [ "$block_count" -eq 0 ]; then
    echo "✅ チェック対象のコマンドがありません"
    exit 0
fi

# ---------------------------------------------------------------------------
# メタ構文・非シェルブロックの判別
#
# docs には ``` bash タグが付いているがシェルスクリプトではないブロックが
# 多数ある（REPL の対話ログ、ツール出力の貼り付け、意図的な誤り例など）。
# これらを docs 側で ```text にリタグする案もあったが、
#   - .github/workflows/verify-commands.yml -> validate_commands.sh が
#     `^```bash` に直接依存しており、リタグすると q コマンドが検証対象から外れる
#   - 06_manual-checks.md L387 が「言語指定がある（```bash, ```json等）」を規約化
#   - docs 全体で ```text / ```console の使用実績が0件
# の3点から、ツール側で判別する方式を採る。
#
# 重要: 判別ルールは「shellcheck が error を出したブロック」にのみ適用する。
# 全ブロックに前置きで適用すると、正常なブロックまで巻き込んで検査対象から
# 外れる（実測: repl ルール単体で error なしブロック237件が該当）。
# ---------------------------------------------------------------------------
is_meta_block() {
    local content="$1" reason_var="$2"

    # Q CLI の REPL / 対話ログ
    if grep -qE '^[[:space:]]*(>|/[a-z]|↯|Shell ·|You:|あなた:|AI:|q>)' <<< "$content" \
        || grep -q 'Ctrl+' <<< "$content"; then
        printf -v "$reason_var" '%s' "Q CLI の REPL/対話ログ"
        return 0
    fi

    # ツール出力の貼り付け（$ プロンプト付きの実行例）
    if grep -qE '^\$ ' <<< "$content"; then
        printf -v "$reason_var" '%s' "ツール実行例の出力貼り付け"
        return 0
    fi

    # 記入用プレースホルダ（チェックリストのテンプレート）
    if grep -qE '^[[:space:]]*\[[^]]*記入[^]]*\][[:space:]]*$' <<< "$content"; then
        printf -v "$reason_var" '%s' "記入用プレースホルダ"
        return 0
    fi

    # JSON / 配列リテラルが直に書かれた擬似コード
    if grep -qE '^[[:space:]]*[{[][[:space:]]*$' <<< "$content"; then
        printf -v "$reason_var" '%s' "JSON/配列リテラルを含む擬似コード"
        return 0
    fi

    # パス表記のみの行（ディレクトリの案内）
    if grep -qE '^[[:space:]]*[~/][A-Za-z0-9._/~-]*/[[:space:]]*$' <<< "$content"; then
        printf -v "$reason_var" '%s' "ディレクトリパスの案内"
        return 0
    fi

    # shebang が先頭行にない（ファイル内容の抜粋）
    if grep -q '#!/' <<< "$content" \
        && [ "$(grep -m1 -c '.' <<< "$content")" = "1" ] \
        && ! head -1 <<< "$content" | grep -q '^#!'; then
        printf -v "$reason_var" '%s' "スクリプトファイル内容の抜粋（shebang が先頭でない）"
        return 0
    fi

    return 1
}

# 直前の見出し・強調から「意図的な誤り例」を判定する
is_intentional_bad_example() {
    local src="$1" fence_line="$2"
    local start=$((fence_line > 6 ? fence_line - 6 : 1))
    sed -n "${start},$((fence_line - 1))p" "$src" 2>/dev/null \
        | grep -qE '(❌|間違い|ダメな例|エラー例|悪い例|NG例)'
}

# ---------------------------------------------------------------------------
# shellcheck（ブロック単位）
# ---------------------------------------------------------------------------
echo "🔍 shellcheckで構文チェック中..."

shellcheck_errors=0
skipped_blocks=0
SKIP_LOG="$WORKDIR/skipped.txt"
: > "$SKIP_LOG"

while IFS= read -r blockfile; do
    origin="$(cat "${blockfile%.sh}.meta")"
    src="${origin%:*}"
    fence_line="${origin##*:}"

    # --severity=error: パースできない構文のみを対象にする。
    #   警告レベル（SC2016 単一引用符、SC1090 非定数 source 等）は
    #   ドキュメントの例示では正当なことが多く、エラーにすべきではない。
    # -e SC1073,SC1048,SC1072: 既知の派生エラー（空の then 句など）を除外。
    if shellcheck -s bash --severity=error -e SC1073,SC1048,SC1072 \
        "$blockfile" > /dev/null 2>&1; then
        continue
    fi

    content="$(cat "$blockfile")"
    reason=""

    if is_meta_block "$content" reason; then
        skipped_blocks=$((skipped_blocks + 1))
        echo "$src:$fence_line … $reason" >> "$SKIP_LOG"
        continue
    fi

    if is_intentional_bad_example "$src" "$fence_line"; then
        skipped_blocks=$((skipped_blocks + 1))
        echo "$src:$fence_line … 意図的な誤り例（直前の見出しが ❌/間違い）" >> "$SKIP_LOG"
        continue
    fi

    # 真の構文エラー。ファイル名と行番号を付けて報告する。
    echo "❌ $src:$fence_line のコードブロックに構文エラー"
    shellcheck -s bash --severity=error -e SC1073,SC1048,SC1072 -f gcc "$blockfile" 2>&1 \
        | sed -E "s#^[^:]*:([0-9]+):[0-9]*:?#   $src (ブロック内 L\1): #" \
        | head -10
    shellcheck_errors=$((shellcheck_errors + 1))
done < <(find "$BLOCKS_DIR" -name "*.sh" -type f | sort -V)

if [ "$shellcheck_errors" -eq 0 ]; then
    echo "✅ shellcheck: 問題なし（${skipped_blocks}ブロックはメタ構文として除外）"
fi

if [ "$LIST_SKIPPED" = true ] && [ -s "$SKIP_LOG" ]; then
    echo ""
    echo "=== 除外したブロック（${skipped_blocks}件）==="
    sed 's/^/  ⏭️  /' "$SKIP_LOG"
fi

echo ""

# ---------------------------------------------------------------------------
# Q CLI固有のコマンドチェック
# ---------------------------------------------------------------------------
echo "🔍 Q CLIコマンドをチェック中..."

q_commands=$(find "$BLOCKS_DIR" -name "*.sh" -type f -exec cat {} + 2>/dev/null \
    | grep -E "^q " || true)

if [ -z "$q_commands" ]; then
    echo "   Q CLIコマンドなし"
    q_errors=0
else
    q_count=$(wc -l <<< "$q_commands")
    echo "   Q CLIコマンド数: $q_count"

    # 既知のサブコマンドとオプションリスト
    valid_subcommands="chat|update|config|agent|knowledge|mcp|login|logout|profile|settings|translate|user|whoami|debug|diagnostic|doctor|inline|quit|restart|integrations|init|issue|launch|dashboard|setup|theme"
    valid_options="--version|--help|--agent|--debug|--profile|--list|--dotfiles"

    q_errors=0
    while IFS= read -r cmd; do
        second_arg=$(awk '{print $2}' <<< "$cmd")

        # オプションの場合はスキップ
        if grep -qE "^($valid_options)" <<< "$second_arg"; then
            continue
        fi

        # 有効なサブコマンドかチェック
        if ! grep -qE "^($valid_subcommands)$" <<< "$second_arg"; then
            echo "❌ 不明なサブコマンド: $cmd"
            q_errors=$((q_errors + 1))
        fi
    done <<< "$q_commands"

    if [ "$q_errors" -eq 0 ]; then
        echo "✅ Q CLIコマンド: 問題なし"
    fi
fi

echo ""
echo "=== チェック結果 ==="
echo "抽出したブロック数: $block_count"
echo "抽出した行数: $total_lines"
echo "メタ構文として除外: $skipped_blocks ブロック（--list-skipped で一覧表示）"
echo "shellcheckエラー: $shellcheck_errors"
echo "Q CLIコマンドエラー: $q_errors"

total_errors=$((shellcheck_errors + q_errors))

if [ "$total_errors" -gt 0 ]; then
    echo ""
    echo "❌ コマンド構文チェックに失敗しました"
    exit 1
else
    echo ""
    echo "✅ すべてのコマンドが正しい構文です"
    exit 0
fi
