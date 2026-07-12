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
    5. changelog⇔機能文書リンク: 機能文書が存在するバージョンエントリが
       当該文書へのリンク（../01_features/NN_*.md）を含むか、リンク先が実在するか
    6. 更新履歴先頭行: 02_update/README.md「主要なアップデート」表の先頭データ行の
       **vX.Y.Z** == changelog 最新版（完全一致。表は新しい順のため先頭＝最新）
"""
import os
import re
import sys
import glob

FEATURE_TABLE = "kiro-docs/01_features/README.md"
CHANGELOG = "kiro-docs/02_update/01_changelog.md"
FEATURES_DIR = "kiro-docs/01_features"
UPDATE_README = "kiro-docs/02_update/README.md"

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

# changelog エントリ ⇔ 機能文書の対応（01_features/README.md の対象バージョン欄が根拠）。
# キー = changelog の「### <キー> CLI（...）」見出しの版、値 = そのセクション内に
# リンクが必要な 01_features 配下のファイル名。新バージョンで機能文書を追加したら
# ここにも対応を追加すること。
CHANGELOG_FEATURE_LINKS = {
    "v2.12.0": ["32_MCPOAuthManagement.md"],
    "v2.11.0": ["32_MCPOAuthManagement.md"],
    "v2.10.0": ["31_v210ConfigHotReload.md"],
    "v2.8.1": ["30_v28V3Preview.md"],
    "v2.8.0": ["30_v28V3Preview.md"],
    "v2.7.0": ["29_v27NewCommands.md"],
    "v2.6.0": ["28_v26NewCommands.md"],
    "v2.5.0": ["27_ThinkingDisplay.md", "02_Subagents.md"],
    "v2.4.0": ["21_v24NewCommands.md"],
    "v2.1.0": ["19_ToolSearch.md", "07_Skills.md", "12_RemoteAuth.md"],
    "v2.0.0": ["16_v2MajorUpdate.md", "18_TerminalUI.md", "20_GuideAgent.md"],
    "v1.29.x": ["22_Hooks.md", "20_GuideAgent.md"],
    "v1.28.0": ["18_TerminalUI.md"],
    "v1.27.0": ["17_GranularToolTrust.md"],
    "v1.26.0": ["24_FileReferences.md", "07_Skills.md", "13_ACP.md"],
    "v1.25.1": ["12_RemoteAuth.md"],
    "v1.25.0": ["13_ACP.md", "14_HelpAgent.md", "15_ExitCodes.md",
                "11_URLPermissions.md", "02_Subagents.md"],
    "v1.24.0": ["01_LSP.md", "07_Skills.md", "08_CustomDiffTools.md",
                "09_ASTPatternTools.md", "10_ConversationCompaction.md",
                "11_URLPermissions.md", "12_RemoteAuth.md"],
    "v1.23.1": ["05_GrepGlob.md", "02_Subagents.md", "03_PlanAgent.md"],
    "v1.23.0": ["02_Subagents.md", "03_PlanAgent.md", "04_MultiSession.md",
                "05_GrepGlob.md"],
    "v1.22.0": ["01_LSP.md"],
}

CL_SECTION_RE = re.compile(r'^### (v[0-9][^ 　（]*)')


def changelog_sections():
    """changelog を「### vX.Y.Z ...」見出しで分割し {版: セクション本文} を返す。"""
    sections = {}
    current = None
    buf = []
    with open(CHANGELOG, encoding="utf-8") as f:
        for line in f:
            m = CL_SECTION_RE.match(line)
            if m:
                if current:
                    sections[current] = "".join(buf)
                current = m.group(1)
                buf = []
            elif current:
                buf.append(line)
    if current:
        sections[current] = "".join(buf)
    return sections


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


def update_readme_first_version():
    """02_update/README.md「主要なアップデート」表の先頭データ行から **vX.Y.Z** を返す。"""
    row_re = re.compile(r'^\| \*\*(v[0-9]+\.[0-9]+\.[0-9]+)\*\* \|')
    with open(UPDATE_README, encoding="utf-8") as f:
        for line in f:
            m = row_re.match(line)
            if m:
                return m.group(1)
    return None


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

    # 5. changelog ⇔ 機能文書リンク
    print("🔍 5. changelog エントリ ⇔ 機能文書リンクを検証中...")
    sections = changelog_sections()
    checked = 0
    for ver, files in CHANGELOG_FEATURE_LINKS.items():
        body = sections.get(ver)
        if body is None:
            print(f"❌ changelog に見出し '### {ver}' が見つかりません（CHANGELOG_FEATURE_LINKS の更新漏れ？）")
            errors += 1
            continue
        for fname in files:
            checked += 1
            if not os.path.exists(os.path.join(FEATURES_DIR, fname)):
                print(f"❌ CHANGELOG_FEATURE_LINKS のリンク先が実在しません: {FEATURES_DIR}/{fname}")
                errors += 1
                continue
            if f"../01_features/{fname}" not in body:
                print(f"❌ changelog {ver} セクションに ../01_features/{fname} へのリンクが無い")
                errors += 1
    print(f"   対応表エントリ = {len(CHANGELOG_FEATURE_LINKS)} 版 / リンク検査数 = {checked}")

    # 6. 更新履歴先頭行
    print("🔍 6. 更新履歴先頭行（02_update/README 表の先頭行 == changelog 最新版）を検証中...")
    first_ver = update_readme_first_version()
    print(f"   changelog 最新版 = {latest} / 更新履歴表の先頭行 = {first_ver}")
    if first_ver is None:
        print(f"❌ {UPDATE_README} に '| **vX.Y.Z** |' 形式のデータ行が見つかりません")
        errors += 1
    elif first_ver != latest:
        print(f"❌ 更新履歴表の先頭行（{first_ver}）が changelog 最新版（{latest}）と不一致")
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
