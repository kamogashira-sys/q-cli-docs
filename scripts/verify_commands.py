#!/usr/bin/env python3
"""
コマンド存在確認ツール
ドキュメント内のすべてのコマンドとサブコマンドを抽出し、実装と照合
"""

import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Set

# 公式CLIコマンドリスト（q --help-allから抽出）
OFFICIAL_CLI_COMMANDS = {
    "q debug", "q settings", "q setup", "q update", "q diagnostic", 
    "q init", "q theme", "q issue", "q login", "q logout", 
    "q whoami", "q profile", "q user", "q doctor", "q launch", 
    "q quit", "q restart", "q integrations", "q translate", 
    "q dashboard", "q chat", "q mcp", "q inline", "q agent"
}

# 公式サブコマンドリスト（実装から抽出）
OFFICIAL_SUBCOMMANDS = {
    "agent": ["list", "create", "edit", "validate", "migrate", "set-default"],
    "inline": ["enable", "disable", "status", "set-customization", "show-customizations"],
    "user": ["login", "logout", "whoami", "profile"],
    "settings": ["open", "all"],
    "integrations": ["install", "uninstall", "reinstall", "status"],
    "mcp": ["add", "remove", "list", "import", "status"],
    "debug": ["app", "build", "autocomplete-window", "logs", "prompt-accessibility", 
              "sample", "accessibility", "key-tester", "diagnostics", "query-index", 
              "devtools", "get-index", "list-intellij-variants", "shell", 
              "fix-permissions", "refresh-auth-token"]
}

# 公式チャット内コマンドリスト（commands.mdから抽出）
OFFICIAL_CHAT_COMMANDS = {
    "/help", "/clear", "/quit", "/exit", "/q",
    "/agent", "/context", "/knowledge", "/checkpoint", "/todos",
    "/hooks", "/tangent", "/editor", "/reply", "/issue", "/mcp",
    "/model", "/experiment", "/prompts", "/compact", "/usage",
    "/changelog", "/save", "/load", "/subscribe", "/tools", "/whatsnew"
}

# 除外すべきセクションのキーワード
EXCLUDED_SECTION_KEYWORDS = {
    # API関連
    'restful', 'rest api', 'rest', 'api', 'エンドポイント', 'endpoint',
    'http', 'https', 'url', 'uri', 'リソース', 'resource',
    
    # 命名規則
    '命名規則', 'ネーミング', 'naming', 'convention',
    '規約', 'ルール', 'rule', 'guideline',
    
    # パス関連
    'パス', 'path', 'ファイルパス', 'file path',
    'ディレクトリ', 'directory', 'フォルダ', 'folder',
    
    # 例示関連
    'example', '例', 'サンプル', 'sample',
    'デモ', 'demo'
}

def split_into_sections(content: str) -> List[Dict[str, str]]:
    """Markdownをセクションに分割
    
    Args:
        content: Markdownファイルの内容
        
    Returns:
        セクションのリスト [{'heading': '見出し', 'content': '内容', 'level': レベル}, ...]
    """
    sections = []
    current_section = {'heading': '', 'content': '', 'level': 0}
    
    for line in content.split('\n'):
        # 見出し行の検出
        if line.startswith('#'):
            # 前のセクションを保存
            if current_section['content'].strip():
                sections.append(current_section)
            
            # 新しいセクションを開始
            level = len(line) - len(line.lstrip('#'))
            heading = line.lstrip('#').strip()
            current_section = {
                'heading': heading,
                'content': '',
                'level': level
            }
        else:
            # 内容を追加
            current_section['content'] += line + '\n'
    
    # 最後のセクションを保存
    if current_section['content'].strip():
        sections.append(current_section)
    
    return sections

def is_excluded_section(heading: str) -> bool:
    """除外すべきセクションかどうかを判定
    
    Args:
        heading: セクションの見出し
        
    Returns:
        True: 除外すべき, False: 検証対象
    """
    if not heading:
        return False
    
    heading_lower = heading.lower()
    
    # 除外キーワードが含まれているかチェック
    for keyword in EXCLUDED_SECTION_KEYWORDS:
        if keyword in heading_lower:
            return True
    
    return False

def extract_chat_commands_hybrid(content: str) -> List[str]:
    """ハイブリッド方式でチャットコマンドを抽出
    
    Args:
        content: Markdownファイルの内容
        
    Returns:
        検証対象のチャットコマンドのリスト
    """
    # セクションに分割
    sections = split_into_sections(content)
    
    chat_commands = []
    
    for section in sections:
        heading = section.get('heading', '')
        
        # 除外すべきセクションはスキップ
        if is_excluded_section(heading):
            continue
        
        # このセクション内の/パターンを抽出
        pattern = r'`(/[a-z]+)`'
        matches = re.findall(pattern, section['content'])
        
        # 既知のチャットコマンドのみを追加
        for match in matches:
            if match in OFFICIAL_CHAT_COMMANDS:
                chat_commands.append(match)
    
    return chat_commands

def extract_commands_from_markdown(file_path: Path) -> Dict[str, List]:
    """Markdownファイルからコマンドとサブコマンドを抽出（ハイブリッド方式）"""
    cli_commands = []
    subcommands = []
    chat_commands = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # CLIコマンドの抽出（q <command>形式、バージョン番号を除外）
            cli_pattern = r'`q\s+([a-z][a-z-]+)`'
            cli_matches = re.findall(cli_pattern, content)
            cli_commands = [f"q {cmd}" for cmd in cli_matches]
            
            # サブコマンドの抽出（q <command> <subcommand>形式）
            subcommand_pattern = r'`q\s+([a-z][a-z-]+)\s+([a-z][a-z-]+)`'
            subcommand_matches = re.findall(subcommand_pattern, content)
            subcommands = [(cmd, sub) for cmd, sub in subcommand_matches]
            
            # チャット内コマンドの抽出（ハイブリッド方式）
            chat_commands = extract_chat_commands_hybrid(content)
    
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
    
    return {
        "cli": cli_commands,
        "subcommands": subcommands,
        "chat": chat_commands
    }

def verify_commands_in_file(file_path: Path) -> Dict[str, List]:
    """ファイル内のコマンドを検証"""
    commands = extract_commands_from_markdown(file_path)
    
    # CLIコマンドを検証
    invalid_cli = [cmd for cmd in commands["cli"] if cmd not in OFFICIAL_CLI_COMMANDS]
    
    # サブコマンドを検証
    invalid_subcommands = []
    for cmd, sub in commands["subcommands"]:
        if cmd in OFFICIAL_SUBCOMMANDS:
            if sub not in OFFICIAL_SUBCOMMANDS[cmd]:
                invalid_subcommands.append(f"q {cmd} {sub}")
        # コマンド自体が存在しない場合はCLI検証で検出されるのでスキップ
    
    # チャット内コマンドを検証
    invalid_chat = [cmd for cmd in commands["chat"] if cmd not in OFFICIAL_CHAT_COMMANDS]
    
    return {
        "cli": invalid_cli,
        "subcommands": invalid_subcommands,
        "chat": invalid_chat
    }

def main():
    """メイン処理"""
    docs_dir = Path("docs")
    
    if not docs_dir.exists():
        print("❌ docsディレクトリが見つかりません")
        return
    
    print("🔍 ドキュメント内のコマンドを検証中...\n")
    
    # すべてのMarkdownファイルを検証
    md_files = list(docs_dir.rglob("*.md"))
    total_files = len(md_files)
    files_with_issues = 0
    total_invalid_commands = 0
    
    issues: Dict[Path, Dict[str, List]] = {}
    
    for md_file in md_files:
        invalid = verify_commands_in_file(md_file)
        if invalid["cli"] or invalid["subcommands"] or invalid["chat"]:
            issues[md_file] = invalid
            files_with_issues += 1
            total_invalid_commands += len(invalid["cli"]) + len(invalid["subcommands"]) + len(invalid["chat"])
    
    # 結果を表示
    print(f"📊 検証結果:")
    print(f"  - 検証したファイル数: {total_files}")
    print(f"  - 検出した問題: {total_invalid_commands}件")
    print(f"  - 問題のあるファイル数: {files_with_issues}\n")
    
    if issues:
        print("❌ 存在しないコマンドが見つかりました:\n")
        for file_path, invalid in sorted(issues.items()):
            print(f"📄 {file_path}:")
            if invalid["cli"]:
                for cmd in invalid["cli"]:
                    print(f"  ❌ {cmd}")
            if invalid["subcommands"]:
                for cmd in invalid["subcommands"]:
                    print(f"  ❌ {cmd} (サブコマンド)")
            if invalid["chat"]:
                for cmd in invalid["chat"]:
                    print(f"  ❌ {cmd}")
            print()
        
        print("🔧 対応が必要です:")
        print("  1. 上記のコマンドを削除または修正してください")
        print("  2. commands.mdで正しいコマンドを確認してください")
        print("  3. 実機で動作確認してください")
        sys.exit(1)
    else:
        print("✅ すべてのコマンドが確認されました")
        sys.exit(0)

if __name__ == "__main__":
    main()
