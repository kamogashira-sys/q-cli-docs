#!/usr/bin/env python3
"""check-structure.py - kiro-docs 構造整合チェック

使用方法:
    ./scripts/kiro-docs/check-structure.py

機能:
    1. 末尾追記(#9): 機能テーブルの末尾行のバージョン系列(major.minor) == changelog 最新版の系列
       （テーブルはカテゴリ別配置で全体は版番号順ではないため、末尾＝最新版系列のみ検査。
        パッチ版差（例: 末尾 v2.8.0 と changelog 最新 v2.8.1）は同一系列 2.8 として許容）
    2. 欠番検出(補B): kiro-docs/01_features/NN_*.md の番号が連続（欠番なし）か
    3. 必須セクション存在(#16): 指定ファイルに必須見出しがあるか
    4. 相互参照注記(#10): 旧版機能を扱う文書に解消バージョンの言及があるか
"""
import os
import re
import sys
import glob

FEATURE_TABLE = "kiro-docs/01_features/README.md"
CHANGELOG = "kiro-docs/02_update/01_changelog.md"
FEATURES_DIR = "kiro-docs/01_features"

TABLE_ROW_RE = re.compile(r'^\|.*\]\([0-9]{2}_[^)]+\.md\)')
VER_RE = re.compile(r'v[0-9]+\.[0-9]+\.[0-9]+')
CL_HEAD_RE = re.compile(r'^### (v[0-9]+\.[0-9]+\.[0-9]+)')

# 必須セクション: ファイル -> [必須見出し正規表現]
REQUIRED_SECTIONS = {
    "kiro-docs/04_reference/02_slash-commands.md": [r"^### `/goal`"],
}

# 相互参照注記: ファイル -> 含まれるべきキーワード（旧版機能の解消バージョン言及）
CROSS_REF = {
    "kiro-docs/01_features/28_v26NewCommands.md": "v2.7.0",
    "kiro-docs/04_reference/01_settings.md": "v2.7.0",
}


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def changelog_latest():
    with open(CHANGELOG, encoding="utf-8") as f:
        for line in f:
            m = CL_HEAD_RE.match(line)
            if m:
                return m.group(1)
    return None


def last_table_version():
    last = None
    with open(FEATURE_TABLE, encoding="utf-8") as f:
        for line in f:
            if TABLE_ROW_RE.match(line):
                last = line
    if not last:
        return None
    m = VER_RE.search(last)
    return m.group(0) if m else None


def major_minor(ver):
    """v2.8.0 -> '2.8'。比較用に major.minor のみ取り出す。"""
    if not ver:
        return None
    m = re.match(r'v?([0-9]+)\.([0-9]+)', ver)
    return f"{m.group(1)}.{m.group(2)}" if m else None


def feature_numbers():
    nums = []
    for p in glob.glob(os.path.join(FEATURES_DIR, "[0-9][0-9]_*.md")):
        if p.endswith(".bak"):
            continue
        base = os.path.basename(p)
        nums.append(int(base[:2]))
    return sorted(set(nums))


def main():
    os.chdir(repo_root())
    errors = 0

    print("=== kiro-docs 構造整合チェック ===")
    print("")

    # 1. 末尾追記
    print("🔍 1. 末尾追記（末尾行バージョン == changelog 最新版、major.minor で比較）を検証中...")
    latest = changelog_latest()
    last_ver = last_table_version()
    latest_mm = major_minor(latest)
    last_mm = major_minor(last_ver)
    print(f"   changelog 最新版 = {latest} ({latest_mm}) / 機能テーブル末尾行 = {last_ver} ({last_mm})")
    if latest_mm != last_mm:
        print(f"❌ 機能テーブル末尾のバージョン系列（{last_mm}）が changelog 最新版の系列（{latest_mm}）と不一致")
        errors += 1

    # 2. 欠番検出
    print("🔍 2. 機能ファイル NN の欠番を検証中...")
    nums = feature_numbers()
    if nums:
        expected = list(range(nums[0], nums[-1] + 1))
        missing = sorted(set(expected) - set(nums))
        print(f"   NN 範囲 = {nums[0]:02d}..{nums[-1]:02d} / 検出数 = {len(nums)}")
        if missing:
            print(f"❌ 欠番: {', '.join(f'{n:02d}' for n in missing)}")
            errors += 1
    else:
        print("❌ 機能ファイルが見つかりません")
        errors += 1

    # 3. 必須セクション
    print("🔍 3. 必須セクションの存在を検証中...")
    for fp, patterns in REQUIRED_SECTIONS.items():
        try:
            txt = open(fp, encoding="utf-8").read()
        except OSError:
            print(f"❌ ファイルが存在しません: {fp}")
            errors += 1
            continue
        for pat in patterns:
            if not re.search(pat, txt, re.MULTILINE):
                print(f"❌ 必須セクション欠落: {fp} に /{pat}/ が無い")
                errors += 1

    # 4. 相互参照注記
    print("🔍 4. 相互参照注記（解消バージョン言及）を検証中...")
    for fp, kw in CROSS_REF.items():
        try:
            txt = open(fp, encoding="utf-8").read()
        except OSError:
            print(f"❌ ファイルが存在しません: {fp}")
            errors += 1
            continue
        if kw not in txt:
            print(f"❌ 相互参照注記欠落: {fp} に '{kw}' の言及が無い")
            errors += 1

    print("")
    print("=== チェック結果 ===")
    print(f"問題数: {errors}")
    print("")
    if errors > 0:
        print("❌ 構造整合チェックに失敗しました")
        sys.exit(1)
    print("✅ 構造整合は問題ありません")
    sys.exit(0)


if __name__ == "__main__":
    main()
