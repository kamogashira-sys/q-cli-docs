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

def extract_commands_from_markdown(file_path: Path) -> Dict[str, List]:
    """Markdownファイルからコマンドとサブコマンドを抽出"""
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
            
            # チャット内コマンドの抽出
            chat_pattern = r'`(/[a-z]+)`'
            chat_matches = re.findall(chat_pattern, content)
            chat_commands = chat_matches
    
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
