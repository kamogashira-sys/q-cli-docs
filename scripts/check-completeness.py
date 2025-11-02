#!/usr/bin/env python3
"""
check-completeness.py - ドキュメント完全性チェック

使用方法:
    ./scripts/check-completeness.py [file]

機能:
    - ドキュメントタイプを判定
    - 必須セクションの存在確認
    - 不足セクションの報告
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set

# ドキュメントタイプ別の必須セクション
REQUIRED_SECTIONS: Dict[str, List[str]] = {
    "getting-started": [
        "前提条件",
        "インストール確認",
    ],
    "configuration": [
        "設定項目",
        "例",
    ],
    "reference": [
        "構文",
        "例",
    ],
    "guide": [
        "目的",
        "手順",
    ],
    "best-practices": [
        "推奨事項",
        "例",
    ],
}


def determine_doc_type(filepath: Path) -> str:
    """ファイルパスからドキュメントタイプを判定"""
    path_str = str(filepath)
    
    if "getting-started" in path_str:
        return "getting-started"
    elif "configuration" in path_str:
        return "configuration"
    elif "reference" in path_str:
        return "reference"
    elif "guides" in path_str:
        return "guide"
    elif "best-practices" in path_str:
        return "best-practices"
    
    return "unknown"


def extract_sections(content: str) -> Set[str]:
    """ドキュメントからセクション見出しを抽出"""
    sections = set()
    
    # ## で始まる見出しを抽出
    for match in re.finditer(r'^##\s+(.+)$', content, re.MULTILINE):
        section = match.group(1).strip()
        # すべての絵文字を除去（複数の範囲をカバー）
        section = re.sub(r'[\U0001F000-\U0001FFFF]', '', section)
        section = re.sub(r'[\u2600-\u26FF]', '', section)
        section = re.sub(r'[\u2700-\u27BF]', '', section)
        section = section.strip()
        sections.add(section)
    
    return sections


def check_completeness(filepath: Path) -> tuple[bool, List[str]]:
    """ドキュメントの完全性をチェック"""
    # ファイルを読み込み
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {filepath}: {e}")
        return False, []
    
    # ドキュメントタイプを判定
    doc_type = determine_doc_type(filepath)
    
    if doc_type == "unknown":
        # 必須セクションが定義されていないタイプはスキップ
        return True, []
    
    # 必須セクションを取得
    required = REQUIRED_SECTIONS.get(doc_type, [])
    
    # 実際のセクションを抽出
    actual_sections = extract_sections(content)
    
    # 不足セクションを検出
    missing = []
    for section in required:
        if section not in actual_sections:
            missing.append(section)
    
    return len(missing) == 0, missing


def main():
    """メイン処理"""
    print("=== ドキュメント完全性チェック ===")
    print()
    
    # プロジェクトルートに移動
    project_root = Path(__file__).parent.parent
    
    # チェック対象ファイルの決定
    if len(sys.argv) > 1:
        # 引数で指定されたファイル
        files = [Path(sys.argv[1])]
        print(f"📝 指定されたファイルをチェック: {files[0]}")
    else:
        # すべてのMarkdownファイル
        docs_dir = project_root / "docs"
        files = list(docs_dir.rglob("*.md"))
        print(f"📝 全ドキュメントをチェック: {len(files)} ファイル")
    
    print()
    
    # 各ファイルをチェック
    total = 0
    errors = 0
    skipped = 0
    
    for filepath in files:
        total += 1
        
        is_complete, missing = check_completeness(filepath)
        
        if not missing:
            # 必須セクションなし、または完全
            skipped += 1
            continue
        
        if not is_complete:
            print(f"❌ {filepath}")
            print(f"   不足セクション:")
            for section in missing:
                print(f"     - {section}")
            print()
            errors += 1
    
    # 結果サマリー
    print("=== チェック結果 ===")
    print(f"チェック対象: {total} ファイル")
    print(f"スキップ: {skipped} ファイル")
    print(f"不完全: {errors} ファイル")
    
    if errors > 0:
        print()
        print("❌ ドキュメント完全性チェックに失敗しました")
        sys.exit(1)
    else:
        print()
        print("✅ すべてのドキュメントが完全です")
        sys.exit(0)


if __name__ == "__main__":
    main()
