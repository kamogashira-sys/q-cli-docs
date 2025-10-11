#!/usr/bin/env python3
"""Phase 4: 設定例の統合（修正版）"""

import re
from pathlib import Path

TARGET_FILES = {
    "docs/user-guide/configuration/agent-configuration.md": "examples.md",
    "docs/user-guide/configuration/mcp-configuration.md": "examples.md",
}

REPLACEMENT = """## 設定例

基本的な設定例については、[設定例集]({path})を参照してください。

**主な設定例**:
- Agent設定の実践例
- MCP設定の実践例
- ユースケース別設定
- セキュリティ設定

---
"""

def process_file(file_path: str, rel_path: str):
    """ファイル処理"""
    full_path = Path(file_path)
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_len = len(content)
    
    # ## 実践例 セクション全体を削除
    content = re.sub(
        r'## 実践例\n\n.*?(?=^## |\Z)',
        '',
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # ## 📚 関連ドキュメント の前に挿入
    if '## 📚 関連ドキュメント' in content:
        content = content.replace(
            '## 📚 関連ドキュメント',
            REPLACEMENT.format(path=rel_path) + '## 📚 関連ドキュメント'
        )
    
    deleted = original_len - len(content)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return deleted

def main():
    print("Phase 4: 設定例の統合")
    print("=" * 60)
    
    total = 0
    for file_path, rel_path in TARGET_FILES.items():
        print(f"\n処理中: {file_path}")
        deleted = process_file(file_path, rel_path)
        print(f"  削除: {deleted}文字")
        total += deleted
    
    print(f"\n総削除: {total}文字")

if __name__ == "__main__":
    main()
