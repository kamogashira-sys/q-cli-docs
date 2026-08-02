#!/usr/bin/env python3
"""
check-completeness.py - ドキュメント構造チェック

使用方法:
    ./scripts/check-completeness.py [file]

機能:
    - docs/05_meta/06_manual-checks.md に明文化された構造規約を機械化する
    - コードフェンスの早期クローズ（レンダリング崩れ）を検出する

終了コード:
    0 = 問題なし / 1 = 問題検出 / 2 = ツール自体のエラー
    （docs/05_meta/14_tool-creation-checklist.md の規約）

設計方針:
    旧実装は「必須セクションの見出し語彙が完全一致するか」を検査していたが、
    docs の実際の見出しは「絵文字＋説明付き」が規約であり、語彙そのものが
    乖離していた。部分一致・絵文字除去・h3許容に直しても41件の違反が1件も
    解消しないことを実測で確認したため、語彙一致の検査は撤去した。

    代わりに 06_manual-checks.md L355-390 に明文化されている構造規約を
    検査する。分類対象51ファイルではなく全ファイルが対象になるため、
    カバレッジは拡大する。

    Markdown の構造解析は CommonMark 準拠パーサ（markdown-it-py）に委ねる。
    自作の正規表現ロジックは「閉じフェンスは情報文字列を持てない」といった
    CommonMark 規則を取りこぼし、内外判定が反転して誤った結論を導くため。
    （07_lessons-learned.md / 14_tool-creation-checklist.md の教訓）
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

try:
    from markdown_it import MarkdownIt
except ImportError:
    print("❌ markdown-it-py が見つかりません", file=sys.stderr)
    print("   インストール: pip install markdown-it-py", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# 検査対象外
# ---------------------------------------------------------------------------

# docs/index.md は GitHub Pages の Jekyll ランディングページ
# （layout: default の front matter を持つ案内ページ）であり、
# 通常のドキュメントとは性質が異なるため構造規約の対象外とする。
EXCLUDED = {"docs/index.md"}

_md = MarkdownIt("commonmark")


def _rel(filepath: Path) -> str:
    """プロジェクトルート相対のパス文字列を返す"""
    try:
        return str(filepath.relative_to(Path(__file__).resolve().parent.parent))
    except ValueError:
        return str(filepath)


def _count_headings(tokens, tag: str) -> int:
    return sum(1 for t in tokens if t.type == "heading_open" and t.tag == tag)


def _unclosed_fences(tokens, lines: List[str]) -> List[int]:
    """閉じられていないコードフェンスの開始行（1-indexed）を返す

    markdown-it は未閉鎖フェンスもファイル末尾までのブロックとして
    パースするため、map の最終行が実際に閉じフェンスかどうかを見る。
    引用ブロック内のフェンス（`> ```bash`）は行頭の `>` と空白を
    剥がしてから判定する必要がある。
    """
    result = []
    for t in tokens:
        if t.type != "fence":
            continue
        start, end = t.map
        if end - 1 >= len(lines):
            result.append(start + 1)
            continue
        last = re.sub(r"^[>\s]*", "", lines[end - 1])
        if not (last.startswith("```") or last.startswith("~~~")):
            result.append(start + 1)
    return result


def _early_closed_fences(tokens, lines: List[str]) -> List[Tuple[int, str]]:
    """コードフェンスの早期クローズが疑われる箇所を返す

    検出する2つのパターン:

    1. 連続するフェンス行
         ```          <- 正常な閉じ
         ```          <- 余分な1行。これが次のブロックの「開き」になり
                         直後の段落や見出しを飲み込む
       無タグで開いたブロックの直前行が閉じフェンスなら疑わしい。

    2. 3バッククォートのネスト
         ```markdown
         ## 使用方法
         ```bash      <- CommonMark ではこれが外側も閉じてしまう
         q chat
         ```          <- ここから先が本文として漏出する
       外側フェンスの中身に別のフェンス開始行が残っていれば、
       外側は 4 バッククォート（````）にする必要がある。
    """
    issues = []
    for t in tokens:
        if t.type != "fence":
            continue
        start, _ = t.map
        info = (t.info or "").strip()

        # パターン1: 無タグブロックの直前行が閉じフェンス
        if not info and start >= 1 and re.match(r"^\s*```\s*$", lines[start - 1]):
            issues.append(
                (start, "余分な閉じフェンス（連続する ``` により空ブロックが開いている）")
            )

        # パターン2: 3バッククォート外側にフェンスがネストしている
        if t.markup.startswith("```") and len(t.markup) == 3:
            for line in t.content.split("\n"):
                if re.match(r"^\s*```", line):
                    issues.append(
                        (
                            start + 1,
                            f"3バッククォートのネスト（外側 ```{info or '(無タグ)'} を "
                            "```` にする必要がある）",
                        )
                    )
                    break
    return issues


def check_structure(filepath: Path) -> Tuple[List[str], bool]:
    """構造規約を検査し、(違反メッセージのリスト, 読み込み成功か) を返す

    戻り値の第2要素で読み込み失敗を呼び出し側に伝える。旧実装は読み込み
    失敗時に (False, []) を返し、呼び出し側の `if not missing` に吸収されて
    「スキップ」として成功扱いになるバグがあった。
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {filepath}: {e}", file=sys.stderr)
        return [], False

    lines = content.split("\n")
    tokens = _md.parse(content)
    violations = []

    # --- 06_manual-checks.md L370-373: 見出しレベル ---
    h1 = _count_headings(tokens, "h1")
    if h1 != 1:
        violations.append(f"コードフェンス外の H1 が {h1} 個（規約: 1個。ファイルタイトル）")

    if _count_headings(tokens, "h2") < 1:
        violations.append("H2 が1個もない（規約: セクションは H2）")

    # --- 06_manual-checks.md L363-368: パンくずリスト ---
    first = next((l for l in lines[:3] if l.strip()), "")
    if not first.lstrip().startswith("[ホーム]"):
        violations.append("先頭にパンくずリスト（[ホーム](...) > ...）がない")

    # --- 06_manual-checks.md L357-361: 最終更新日 ---
    # 規約は `**最終更新**:`（太字）だが実態は太字なしが多数（110件）のため、
    # 太字の有無は問わない。規約側の記述も実態に合わせて緩和済み。
    if not re.search(r"^\s*(\*\*)?最終更新(\*\*)?\s*[:：]", content, re.MULTILINE):
        violations.append("最終更新日の記載がない（規約: 最終更新: YYYY-MM-DD）")

    # --- 06_manual-checks.md L387-390: コードブロック ---
    for ln in _unclosed_fences(tokens, lines):
        violations.append(f"L{ln}: コードフェンスが閉じられていない")

    for ln, reason in _early_closed_fences(tokens, lines):
        violations.append(f"L{ln}: {reason}")

    return violations, True


def main():
    print("=== ドキュメント構造チェック ===")
    print()

    project_root = Path(__file__).resolve().parent.parent

    if len(sys.argv) > 1:
        files = [Path(sys.argv[1])]
        print(f"📝 指定されたファイルをチェック: {files[0]}")
    else:
        docs_dir = project_root / "docs"
        files = sorted(p for p in docs_dir.rglob("*.md") if p.suffix == ".md")
        files = [p for p in files if not p.name.endswith(".bak")]
        print(f"📝 全ドキュメントをチェック: {len(files)} ファイル")

    print()

    total = 0
    violation_files = 0
    excluded = 0
    read_errors = 0

    for filepath in files:
        rel = _rel(filepath)
        if rel in EXCLUDED:
            excluded += 1
            continue

        total += 1
        violations, ok = check_structure(filepath)

        if not ok:
            read_errors += 1
            continue

        if violations:
            violation_files += 1
            print(f"❌ {rel}")
            for v in violations:
                print(f"     - {v}")
            print()

    print("=== チェック結果 ===")
    print(f"チェック対象: {total} ファイル")
    print(f"除外: {excluded} ファイル（Jekyll ランディングページ）")
    print(f"規約違反: {violation_files} ファイル")

    # ツール自体のエラー（読み込み失敗）は exit 2。
    # 旧実装はこれを「スキップ」に吸収して成功扱いにしていた。
    if read_errors > 0:
        print(f"読み込みエラー: {read_errors} ファイル")
        print()
        print("❌ ツールの実行中にエラーが発生しました")
        sys.exit(2)

    if violation_files > 0:
        print()
        print("❌ ドキュメント構造チェックに失敗しました")
        sys.exit(1)

    print()
    print("✅ すべてのドキュメントが構造規約を満たしています")
    sys.exit(0)


if __name__ == "__main__":
    main()
