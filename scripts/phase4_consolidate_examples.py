#!/usr/bin/env python3
"""Phase 4: 設定例セクションの統合スクリプト"""

import re
import os
from pathlib import Path

# 対象ファイルと相対パス
TARGET_FILES = {
    "docs/user-guide/configuration/agent-configuration.md": "examples.md",
    "docs/user-guide/configuration/mcp-configuration.md": "examples.md",
    "docs/user-guide/configuration/environment-variables.md": "examples.md",
    "docs/user-guide/configuration/global-settings.md": "examples.md",
    "docs/user-guide/features/agents.md": "../configuration/examples.md",
}

# 置き換えるテキスト
REPLACEMENT_TEXT = """## 設定例

基本的な設定例については、[設定例集]({relative_path})を参照してください。

**主な設定例**:
- 開発環境用の設定
- 本番環境用の設定
- チーム共有設定
- ユースケース別設定
"""

def remove_detailed_examples(content: str, file_path: str) -> tuple[str, int]:
    """詳細な設定例セクションを削除"""
    
    # パターン1: ## 設定例 から次のセクションまで
    pattern1 = r'## 設定例\n\n(?:(?!^## ).)*?(?=^## |\Z)'
    
    # パターン2: ### 例 から次のセクションまで  
    pattern2 = r'### 例\n\n(?:(?!^## |^### ).)*?(?=^## |^### |\Z)'
    
    original_length = len(content)
    
    # パターン1で置き換え
    content = re.sub(pattern1, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # パターン2で削除
    content = re.sub(pattern2, '', content, flags=re.MULTILINE | re.DOTALL)
    
    deleted_lines = original_length - len(content)
    
    return content, deleted_lines

def add_reference_link(content: str, relative_path: str) -> str:
    """参照リンクを追加"""
    
    # ## ベストプラクティス の前に挿入
    best_practices_pattern = r'(## ベストプラクティス)'
    replacement = REPLACEMENT_TEXT.format(relative_path=relative_path) + '\n---\n\n\\1'
    
    if re.search(best_practices_pattern, content):
        content = re.sub(best_practices_pattern, replacement, content, count=1)
        return content
    
    # ## トラブルシューティング の前に挿入
    troubleshooting_pattern = r'(## トラブルシューティング)'
    
    if re.search(troubleshooting_pattern, content):
        content = re.sub(troubleshooting_pattern, replacement, content, count=1)
        return content
    
    # ## 関連ドキュメント の前に挿入
    related_pattern = r'(## 📚 関連ドキュメント)'
    
    if re.search(related_pattern, content):
        content = re.sub(related_pattern, replacement, content, count=1)
        return content
    
    # どこにも挿入できない場合は末尾に追加
    content += '\n\n---\n\n' + REPLACEMENT_TEXT.format(relative_path=relative_path)
    
    return content

def process_file(file_path: str, relative_path: str) -> dict:
    """ファイルを処理"""
    
    full_path = Path(file_path)
    
    if not full_path.exists():
        return {"status": "skip", "reason": "File not found"}
    
    # ファイル読み込み
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 設定例セクションがあるか確認
    if '## 設定例' not in content and '### 例' not in content:
        return {"status": "skip", "reason": "No examples section"}
    
    # 詳細な設定例を削除
    new_content, deleted_lines = remove_detailed_examples(content, file_path)
    
    # 参照リンクを追加
    new_content = add_reference_link(new_content, relative_path)
    
    # ファイル書き込み
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return {
        "status": "success",
        "deleted_lines": deleted_lines,
        "file": file_path
    }

def main():
    """メイン処理"""
    
    print("Phase 4: 設定例セクションの統合")
    print("=" * 60)
    
    results = []
    total_deleted = 0
    
    for file_path, relative_path in TARGET_FILES.items():
        print(f"\n処理中: {file_path}")
        result = process_file(file_path, relative_path)
        results.append(result)
        
        if result["status"] == "success":
            print(f"  ✅ 完了: {result['deleted_lines']}文字削除")
            total_deleted += result['deleted_lines']
        else:
            print(f"  ⏭️  スキップ: {result['reason']}")
    
    print("\n" + "=" * 60)
    print(f"処理完了: {len([r for r in results if r['status'] == 'success'])}ファイル更新")
    print(f"総削除文字数: {total_deleted}文字")
    
    return results

if __name__ == "__main__":
    main()
