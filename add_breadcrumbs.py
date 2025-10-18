#!/usr/bin/env python3
"""
パンくずリストを全ドキュメントに追加するスクリプト
"""
import os
import re
from pathlib import Path

# ディレクトリ名とタイトルのマッピング
DIR_TITLES = {
    "docs": "ホーム",
    "01_for-users": "ユーザーガイド",
    "01_getting-started": "Getting Started",
    "02_features": "機能ガイド",
    "03_configuration": "設定ガイド",
    "04_best-practices": "ベストプラクティス",
    "05_deployment": "デプロイメント",
    "06_troubleshooting": "トラブルシューティング",
    "07_reference": "リファレンス",
    "08_guides": "コンテキスト管理ガイド",
    "09_security": "セキュリティガイド",
    "02_for-developers": "開発者ガイド",
    "01_contributing": "コントリビューション",
    "02_architecture": "アーキテクチャ",
    "03_for-community": "コミュニティ",
    "01_updates": "アップデート情報",
    "02_community": "コミュニティリソース",
    "03_analysis": "分析レポート",
}

def get_breadcrumb(file_path: Path) -> str:
    """ファイルパスからパンくずリストを生成"""
    parts = file_path.parts
    docs_index = parts.index("docs")
    
    # docsからの相対パスを取得
    rel_parts = parts[docs_index + 1:]
    
    # パンくずリストを構築
    breadcrumbs = []
    current_path = []
    
    # ホームへのリンク
    home_depth = len(rel_parts) - 1
    home_link = "../" * home_depth + "README.md"
    breadcrumbs.append(f"[ホーム]({home_link})")
    
    # 中間ディレクトリ
    for i, part in enumerate(rel_parts[:-1]):
        current_path.append(part)
        title = DIR_TITLES.get(part, part)
        
        # READMEへのリンク
        depth = len(rel_parts) - i - 2
        if depth > 0:
            link = "../" * depth + "README.md"
        else:
            link = "README.md"
        
        breadcrumbs.append(f"[{title}]({link})")
    
    # 現在のファイル名（リンクなし）
    filename = rel_parts[-1]
    if filename != "README.md":
        # ファイル名から番号プレフィックスを削除
        title = re.sub(r'^\d+_', '', filename.replace('.md', '').replace('-', ' ').replace('_', ' '))
        title = title.title()
        breadcrumbs.append(title)
    
    return " > ".join(breadcrumbs)

def add_breadcrumb_to_file(file_path: Path):
    """ファイルにパンくずリストを追加"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 既にパンくずリストがある場合はスキップ
    if content.startswith('[ホーム]'):
        print(f"Skip (already has breadcrumb): {file_path}")
        return
    
    # パンくずリストを生成
    breadcrumb = get_breadcrumb(file_path)
    
    # ファイルの先頭に追加
    new_content = f"{breadcrumb}\n\n---\n\n{content}"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added breadcrumb: {file_path}")

def main():
    """メイン処理"""
    docs_dir = Path("/home/katoh/projects/q-cli-docs/docs")
    
    # 全.mdファイルを取得（.bakを除く）
    md_files = []
    for md_file in docs_dir.rglob("*.md"):
        if ".bak" not in str(md_file):
            md_files.append(md_file)
    
    print(f"Found {len(md_files)} markdown files")
    
    # 各ファイルにパンくずリストを追加
    for md_file in sorted(md_files):
        add_breadcrumb_to_file(md_file)
    
    print(f"\nCompleted! Processed {len(md_files)} files")

if __name__ == "__main__":
    main()
