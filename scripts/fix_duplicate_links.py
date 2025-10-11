#!/usr/bin/env python3
"""重複リンクの修正スクリプト"""

import re
from pathlib import Path

def fix_duplicate_links(content: str) -> tuple[str, bool]:
    """重複リンクを削除"""
    
    # パターン: ## 📚 関連ドキュメント から --- まで
    pattern = r'(## 📚 関連ドキュメント\n\n)((?:- .*\n)+)(\n---)'
    
    match = re.search(pattern, content)
    if not match:
        return content, False
    
    links_section = match.group(2)
    
    # リンクを抽出
    links = []
    seen = set()
    
    for line in links_section.split('\n'):
        line = line.strip()
        if not line or not line.startswith('- '):
            continue
        
        # リンク先URLを抽出
        url_match = re.search(r'\]\((.*?)\)', line)
        if url_match:
            url = url_match.group(1)
            # 重複チェック
            if url not in seen:
                seen.add(url)
                links.append(line)
    
    # 重複削除後のセクションを再構築
    new_section = match.group(1) + '\n'.join(links) + '\n' + match.group(3)
    
    # 置き換え
    new_content = content[:match.start()] + new_section + content[match.end():]
    
    return new_content, True

def process_file(file_path: Path) -> dict:
    """ファイルを処理"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 関連ドキュメントセクションがない場合はスキップ
    if '## 📚 関連ドキュメント' not in content:
        return {"status": "skip", "reason": "No related docs section"}
    
    # 重複リンクを修正
    new_content, changed = fix_duplicate_links(content)
    
    if not changed:
        return {"status": "skip", "reason": "No duplicates found"}
    
    # ファイル書き込み
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return {"status": "success", "file": str(file_path)}

def main():
    """メイン処理"""
    
    print("重複リンクの修正")
    print("=" * 60)
    
    # 全markdownファイルを検索
    docs_dir = Path("docs")
    results = []
    
    for md_file in docs_dir.rglob("*.md"):
        result = process_file(md_file)
        if result["status"] == "success":
            print(f"✅ 修正: {md_file}")
            results.append(result)
    
    print("\n" + "=" * 60)
    print(f"修正完了: {len(results)}ファイル")
    
    return results

if __name__ == "__main__":
    main()
