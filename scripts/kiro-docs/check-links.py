#!/usr/bin/env python3
"""check-links.py - kiro-docs 内部リンク整合チェック

使用方法:
    ./scripts/kiro-docs/check-links.py
    ./scripts/kiro-docs/check-links.py --check-anchors   # アンカー(見出し)実在も検査
    ./scripts/kiro-docs/check-links.py --check-anchors --paths <file...>
        # 指定ファイルのみ検査（既定の除外を適用しない。05_meta 等のローカル管理文書の
        # 相互リンク・目次アンカー検証用）

機能:
    - kiro-docs/**/*.md ＋ ルート README.md の相対 Markdown リンクを抽出
      （フェンスコードブロックとインラインコード内のリンク記法は描画されないため対象外）
    - リンク先ファイルの実在を検証（アンカー #... は分離して判定）
    - --check-anchors: 他ファイルへのアンカーと同一ファイル内アンカー（#... のみのリンク）の
      見出し実在を検査する。日本語を含むアンカーも検査する（2026-10-29 以前は全体実行で
      非 ASCII とページ内アンカーをスキップしており、実在の切れ 5 件を見逃していた）
    - http(s)/mailto/tel はスキップ

除外（スコープ外・原典準拠のため。ソースのスキャン／リンク先の検証の両方に適用）:
    - kiro-docs/06_embedded-docs/**     … 公式 OSS リポジトリの逐語コピー（GitHub 非公開・ローカル管理）
    - kiro-docs/05_meta/**              … 手順書等（GitHub 非公開・ローカル管理）
    - *_update_plan.md                  … gitignore 対象の計画書
"""
import os
import re
import sys
import glob

LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
HEADING_RE = re.compile(r'^#{1,6}\s+(.*?)\s*$')

EXCLUDE_SUBSTR = (
    "kiro-docs/06_embedded-docs/",          # 公式 OSS リポジトリの逐語コピー（GitHub 非公開・ローカル管理）
    "kiro-docs/05_meta",                     # 手順書等は GitHub 非公開・ローカル管理（git rm --cached 済）
    "_update_plan",                          # *_update_plan.md は gitignore 対象の計画書
)
SKIP_PREFIX = ("http://", "https://", "mailto:", "tel:", "#")


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def is_excluded(path):
    norm = path.replace(os.sep, "/")
    return any(sub in norm for sub in EXCLUDE_SUBSTR)


def slugify(heading):
    """GitHub 風 slug。記号除去・空白をハイフン・小文字化。
    GitHub は空白 1 文字ごとにハイフン 1 つ（連続空白を潰さない。例: 「a / b」→ a--b）。"""
    s = heading.strip().lower()
    # インラインコード/装飾記号を除去
    s = s.replace("`", "")
    # 許可しない文字を除去（英数・空白・ハイフン・日本語等は残す）
    s = re.sub(r"[^\w\s\-ぁ-んァ-ヶ一-龠ー]", "", s)
    s = re.sub(r"\s", "-", s)
    return s


FENCE_OPEN_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def fence_step(line, fence):
    """CommonMark のフェンス判定。fence は開いているフェンス（文字列）か None。
    閉じるのは、開始と同じ文字で同じ長さ以上、かつ情報文字列（```bash の bash 等）がない行だけ。
    戻り値: (この行がフェンス行か, 次の fence)"""
    m = FENCE_OPEN_RE.match(line.rstrip("\n"))
    if not m:
        return False, fence
    marker, rest = m.group(1), m.group(2).strip()
    if fence is None:
        if marker[0] == "`" and "`" in rest:
            return False, None   # 情報文字列にバッククォートを含む行は開始フェンスではない
        return True, marker
    if marker[0] == fence[0] and len(marker) >= len(fence) and rest == "":
        return True, None
    return False, fence      # 開いているフェンスの中身（```bash などは閉じない）


def strip_code(txt):
    """フェンスコードブロックとインラインコードスパンを除去（コード内のリンク記法例は
    Markdown ではリンクとして描画されないため、リンク抽出の対象外にする）。"""
    out = []
    fence = None
    for line in txt.splitlines(keepends=True):
        is_fence, fence_next = fence_step(line, fence)
        if is_fence or fence is not None:
            fence = fence_next
            continue
        fence = fence_next
        out.append(re.sub(r"`[^`\n]*`", "", line))
    return "".join(out)


def collect_headings(filepath):
    """見出しの slug 集合。GitHub と同じく、同じ slug の 2 つ目以降に -1, -2 … を付ける。"""
    slugs = set()
    seen = {}
    fence = None
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                # フェンス内の「# コメント」を見出しと誤認しない
                is_fence, fence_next = fence_step(line, fence)
                if is_fence or fence is not None:
                    fence = fence_next
                    continue
                fence = fence_next
                m = HEADING_RE.match(line)
                if m:
                    slug = slugify(m.group(1))
                    n = seen.get(slug, 0)
                    seen[slug] = n + 1
                    slugs.add(slug if n == 0 else f"{slug}-{n}")
    except OSError:
        pass
    return slugs


def main():
    args = sys.argv[1:]
    check_anchors = "--check-anchors" in args
    paths_mode = "--paths" in args
    if paths_mode:
        # --paths 以降をすべて検査対象ファイルとして受け取る（フラグは --paths より前に置く）
        target_paths = args[args.index("--paths") + 1:]
        if not target_paths:
            print("❌ --paths にファイルを 1 つ以上指定してください")
            sys.exit(2)
    os.chdir(repo_root())

    if paths_mode:
        missing = [p for p in target_paths if not os.path.isfile(p)]
        if missing:
            for p in missing:
                print(f"❌ --paths 指定ファイルが存在しません: {p}")
            sys.exit(2)
        files = sorted(target_paths)
    else:
        files = sorted(glob.glob("kiro-docs/**/*.md", recursive=True)) + ["README.md"]

    checked = 0
    broken = []
    anchor_broken = []
    anchor_checked = 0
    heading_cache = {}

    for f in files:
        if not paths_mode and (is_excluded(f) or f.endswith(".bak")):
            continue
        base = os.path.dirname(f)
        try:
            txt = open(f, encoding="utf-8").read()
        except OSError:
            continue
        # コードブロック内のリンク記法例（`[表示名](URL)` 等）を誤検出しない
        txt = strip_code(txt)
        for m in LINK_RE.finditer(txt):
            target = m.group(2).strip()
            # 同一ファイル内アンカー（#... のみのリンク）
            if target.startswith("#"):
                if check_anchors:
                    anchor = target[1:]
                    checked += 1
                    anchor_checked += 1
                    if f not in heading_cache:
                        heading_cache[f] = collect_headings(f)
                    if anchor.lower() not in heading_cache[f]:
                        anchor_broken.append((f, target, anchor))
                continue
            if target.startswith(SKIP_PREFIX):
                continue
            path, _, anchor = target.partition("#")
            if not path:
                continue
            resolved = os.path.normpath(os.path.join(base, path))
            # 除外パス（GitHub 非公開・原典準拠のローカル管理領域: 06_embedded-docs / 05_meta 等）
            # へのリンクは検証対象外。これらは意図的にリポジトリ非公開のため CI には存在しない。
            # --paths ではローカル管理文書そのものを検査するため除外を適用しない。
            if not paths_mode and is_excluded(resolved):
                continue
            checked += 1
            if not os.path.exists(resolved):
                broken.append((f, target, resolved))
                continue
            # アンカー検査（任意）
            if check_anchors and anchor and resolved.endswith(".md"):
                anchor_checked += 1
                if resolved not in heading_cache:
                    heading_cache[resolved] = collect_headings(resolved)
                if anchor.lower() not in heading_cache[resolved]:
                    anchor_broken.append((f, target, anchor))

    print("=== kiro-docs 内部リンク整合チェック ===")
    print("")
    print(f"チェックした相対リンク数: {checked}")
    print(f"リンク切れ: {len(broken)} 件")
    for f, t, r in broken:
        print(f"  ❌ {f}: '{t}' -> {r}")

    if check_anchors:
        print("")
        print(f"アンカー検査: {anchor_checked} 件 / 切れ {len(anchor_broken)} 件")
        for f, t, a in anchor_broken:
            print(f"  ⚠️  {f}: '{t}'（見出し '#{a}' が見つからない）")

    print("")
    total_errors = len(broken) + (len(anchor_broken) if check_anchors else 0)
    if total_errors > 0:
        print("❌ リンクチェックに失敗しました")
        sys.exit(1)
    print("✅ すべての内部リンクが有効です")
    sys.exit(0)


if __name__ == "__main__":
    main()
