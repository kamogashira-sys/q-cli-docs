#!/usr/bin/env python3
"""Phase 5: 関連ドキュメントリンクの標準化"""

import re
from pathlib import Path

# 標準フォーマット
STANDARD_FORMAT = """## 📚 関連ドキュメント

{links}

---
"""

def standardize_related_docs(content: str) -> tuple[str, bool]:
    """関連ドキュメントセクションを標準化"""
    
    # パターン1: ## 📚 関連ドキュメント
    pattern1 = r'## 📚 関連ドキュメント\n\n((?:- .*\n)+)'
    
    # パターン2: ## 📖 関連ドキュメント
    pattern2 = r'## 📖 関連ドキュメント\n\n((?:- .*\n)+)'
    
    # パターン3: ## 🔗 関連ドキュメント
    pattern3 = r'## 🔗 関連ドキュメント\n\n((?:- .*\n)+)'
    
    # パターン4: ## 関連ドキュメント
    pattern4 = r'## 関連ドキュメント\n\n((?:- .*\n)+)'
    
    # パターン5: ### 関連ドキュメント
    pattern5 = r'### 関連ドキュメント\n\n((?:- .*\n)+)'
    
    changed = False
    
    for pattern in [pattern1, pattern2, pattern3, pattern4, pattern5]:
        match = re.search(pattern, content)
        if match:
            links = match.group(1).strip()
            
            # リンクを標準フォーマットに変換
            standardized_links = []
            for line in links.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                # 既に太字の場合はそのまま
                if line.startswith('- **['):
                    standardized_links.append(line)
                # 太字でない場合は太字に変換
                elif line.startswith('- ['):
                    # - [text](link) → - **[text](link)**
                    line = line.replace('- [', '- **[', 1)
                    # 最初の ) の後に ** を追加
                    line = re.sub(r'\)( - .*)?$', r')** \\1', line)
                    standardized_links.append(line)
                else:
                    standardized_links.append(line)
            
            # 標準フォーマットで置き換え
            new_section = STANDARD_FORMAT.format(links='\n'.join(standardized_links))
            content = re.sub(pattern, new_section, content)
            changed = True
            break
    
    return content, changed

def process_file(file_path: Path) -> dict:
    """ファイルを処理"""
    
    if not file_path.exists():
        return {"status": "skip", "reason": "File not found"}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 関連ドキュメントセクションがない場合はスキップ
    if '関連ドキュメント' not in content:
        return {"status": "skip", "reason": "No related docs section"}
    
    # 標準化
    new_content, changed = standardize_related_docs(content)
    
    if not changed:
        return {"status": "skip", "reason": "Already standardized"}
    
    # ファイル書き込み
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return {"status": "success", "file": str(file_path)}

def main():
    """メイン処理"""
    
    print("Phase 5: 関連ドキュメントリンクの標準化")
    print("=" * 60)
    
    # 対象ファイルを検索
    docs_dir = Path("docs")
    target_files = []
    
    for md_file in docs_dir.rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            if '関連ドキュメント' in f.read():
                target_files.append(md_file)
    
    print(f"\n対象ファイル数: {len(target_files)}")
    
    results = []
    for file_path in target_files:
        print(f"\n処理中: {file_path}")
        result = process_file(file_path)
        results.append(result)
        
        if result["status"] == "success":
            print(f"  ✅ 標準化完了")
        else:
            print(f"  ⏭️  スキップ: {result['reason']}")
    
    success_count = len([r for r in results if r["status"] == "success"])
    
    print("\n" + "=" * 60)
    print(f"処理完了: {success_count}ファイル更新")
    
    return results

if __name__ == "__main__":
    main()
