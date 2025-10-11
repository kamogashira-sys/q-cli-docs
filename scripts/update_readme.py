#!/usr/bin/env python3
"""README更新スクリプト"""

import re
from pathlib import Path

def update_readme():
    """READMEを更新"""
    
    readme_path = Path("README.md")
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. プロジェクト構造からfeatures/を削除
    old_structure = r'''│   ├── community/           # コミュニティ（4文書）
│   ├── analysis/            # 分析（3文書）
│   └── features/            # 機能（2文書）'''
    
    new_structure = r'''│   ├── community/           # コミュニティ（4文書）
│   └── analysis/            # 分析（3文書）'''
    
    content = content.replace(old_structure, new_structure)
    
    # 2. 総ドキュメント数を63に更新
    content = re.sub(
        r'- \*\*総ドキュメント数\*\*: 65ファイル',
        '- **総ドキュメント数**: 63ファイル',
        content
    )
    
    # 3. 更新履歴を追加
    content = re.sub(
        r'\| 2025-10-09 \| プロジェクト新規作成（総ドキュメント数: 65文書） \|',
        '''| 2025-10-09 | プロジェクト新規作成（総ドキュメント数: 65文書） |
| 2025-10-09 | ドキュメント統合完了（Phase 1-5）: 2ファイル削除、47ファイル更新 |''',
        content
    )
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ README.md更新完了")

def update_docs_readme():
    """docs/README.mdを更新"""
    
    readme_path = Path("docs/README.md")
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 総ドキュメント数を63に更新
    content = re.sub(
        r'全\*\*65文書\*\*',
        '全**63文書**',
        content
    )
    
    content = re.sub(
        r'総ドキュメント数: \*\*65\*\*',
        '総ドキュメント数: **63**',
        content
    )
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ docs/README.md更新完了")

if __name__ == "__main__":
    update_readme()
    update_docs_readme()
