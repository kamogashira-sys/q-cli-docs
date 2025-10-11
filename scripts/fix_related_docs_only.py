#!/usr/bin/env python3
"""関連ドキュメントセクション内の重複のみ削除"""

import re
from pathlib import Path

def fix_related_docs_section(content: str) -> tuple[str, bool]:
    """関連ドキュメントセクション内の重複パターンを削除"""
    
    # パターン: 同じリンクのブロックが繰り返される
    # 最初のブロックのみを残す
    pattern = r'(## 📚 関連ドキュメント\n\n)((?:- .*\n)+)(\n(?:- \*\*\[.*?\]\(.*?\)\*\* - .*\n(?:- .*\n)+)+)'
    
    match = re.search(pattern, content)
    if not match:
        return content, False
    
    # 最初のリンクブロックのみを保持
    first_block = match.group(2).strip()
    
    # 新しいセクションを構築
    new_section = match.group(1) + first_block + '\n\n---'
    
    # 元のセクション全体を置き換え（---まで）
    old_section_pattern = r'## 📚 関連ドキュメント\n\n.*?(?=\n---\n\n---)'
    new_content = re.sub(old_section_pattern, new_section, content, flags=re.DOTALL)
    
    return new_content, True

def main():
    """メイン処理"""
    
    print("関連ドキュメントセクション内の重複のみ削除")
    print("=" * 60)
    
    fixed_files = []
    
    for md_file in Path("docs").rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, changed = fix_related_docs_section(content)
        
        if changed:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ {md_file}")
            fixed_files.append(str(md_file))
    
    print("\n" + "=" * 60)
    print(f"修正完了: {len(fixed_files)}ファイル")
    
    return fixed_files

if __name__ == "__main__":
    main()
