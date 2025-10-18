#!/usr/bin/env python3
"""
関連トピックセクションを自動生成・追加するスクリプト

使用方法:
    python3 scripts/add_related_topics.py [--dry-run]
"""

import os
import re
from pathlib import Path
import argparse

# カテゴリ別の関連トピックテンプレート
RELATED_TOPICS = {
    'getting-started': [
        ('よくある問題と解決方法', '../06_troubleshooting/02_common-issues.md'),
        ('FAQ', '../06_troubleshooting/01_faq.md'),
    ],
    'features': [
        ('よくある問題と解決方法', '../06_troubleshooting/02_common-issues.md'),
        ('FAQ', '../06_troubleshooting/01_faq.md'),
    ],
    'configuration': [
        ('設定優先順位ガイド', '02_priority-rules.md'),
        ('よくある問題と解決方法', '../06_troubleshooting/02_common-issues.md'),
        ('FAQ', '../06_troubleshooting/01_faq.md'),
    ],
    'best-practices': [
        ('よくある問題と解決方法', '../06_troubleshooting/02_common-issues.md'),
        ('FAQ', '../06_troubleshooting/01_faq.md'),
    ],
    'deployment': [
        ('よくある問題と解決方法', '../06_troubleshooting/02_common-issues.md'),
        ('FAQ', '../06_troubleshooting/01_faq.md'),
    ],
    'troubleshooting': [
        ('コンテキストウィンドウ制限', '../07_reference/07_context-window-limits.md'),
        ('設定リファレンス', '../07_reference/03_settings-reference.md'),
    ],
}

def has_related_topics(content):
    """関連トピックセクションが既に存在するか確認"""
    return bool(re.search(r'\*\*関連トピック\*\*:', content))

def get_category(file_path):
    """ファイルパスからカテゴリを判定"""
    path_str = str(file_path)
    if 'getting-started' in path_str:
        return 'getting-started'
    elif 'features' in path_str:
        return 'features'
    elif 'configuration' in path_str:
        return 'configuration'
    elif 'best-practices' in path_str:
        return 'best-practices'
    elif 'deployment' in path_str:
        return 'deployment'
    elif 'troubleshooting' in path_str:
        return 'troubleshooting'
    return None

def generate_related_topics_section(category):
    """関連トピックセクションを生成"""
    if category not in RELATED_TOPICS:
        return None
    
    lines = ['\n---\n', '\n**関連トピック**:\n']
    for title, link in RELATED_TOPICS[category]:
        lines.append(f'- [{title}]({link})\n')
    
    return ''.join(lines)

def add_related_topics(file_path, dry_run=False):
    """ファイルに関連トピックセクションを追加"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 既に存在する場合はスキップ
    if has_related_topics(content):
        return False, "既に関連トピックセクションが存在"
    
    # カテゴリを判定
    category = get_category(file_path)
    if not category:
        return False, "カテゴリ判定不可"
    
    # 関連トピックセクションを生成
    section = generate_related_topics_section(category)
    if not section:
        return False, f"カテゴリ {category} のテンプレートなし"
    
    # ファイル末尾に追加
    new_content = content.rstrip() + section
    
    if not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return True, "追加完了"

def main():
    parser = argparse.ArgumentParser(description='関連トピックセクションを自動追加')
    parser.add_argument('--dry-run', action='store_true', help='実際には変更せず、結果のみ表示')
    args = parser.parse_args()
    
    docs_dir = Path('docs/01_for-users')
    md_files = list(docs_dir.rglob('*.md'))
    
    # README.mdは除外
    md_files = [f for f in md_files if f.name != 'README.md']
    
    print(f"📊 対象ファイル数: {len(md_files)}\n")
    
    added_count = 0
    skipped_count = 0
    
    for file_path in sorted(md_files):
        rel_path = file_path.relative_to('docs')
        success, message = add_related_topics(file_path, dry_run=args.dry_run)
        
        if success:
            added_count += 1
            status = "✅ 追加" if not args.dry_run else "✅ 追加予定"
            print(f"{status}: {rel_path}")
        else:
            skipped_count += 1
            if args.dry_run:
                print(f"⏭️  スキップ: {rel_path} ({message})")
    
    print(f"\n📈 結果:")
    print(f"  追加: {added_count}ファイル")
    print(f"  スキップ: {skipped_count}ファイル")
    
    if args.dry_run:
        print(f"\n💡 実際に追加するには --dry-run なしで実行してください")

if __name__ == '__main__':
    main()
