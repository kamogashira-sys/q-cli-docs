#!/usr/bin/env python3
"""
コマンド存在確認ツール
ドキュメント内のすべてのコマンドを抽出し、公式ドキュメントと照合
"""

import re
import sys
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

# 公式チャット内コマンドリスト（commands.mdから抽出）
OFFICIAL_CHAT_COMMANDS = {
    "/help", "/clear", "/quit", "/exit", "/q",
    "/agent", "/context", "/knowledge", "/checkpoint", "/todos",
    "/hooks", "/tangent", "/editor", "/reply", "/issue", "/mcp",
    "/model", "/experiment", "/prompts", "/compact", "/usage",
    "/changelog", "/save", "/load", "/subscribe", "/tools"
}

def extract_commands_from_markdown(file_path: Path) -> List[str]:
    """Markdownファイルからコマンドを抽出"""
    commands = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # CLIコマンドの抽出（q で始まる行、ただしバージョン番号を除外）
            cli_pattern = r'^q\s+([a-z][a-z-]*)'
            cli_matches = re.findall(cli_pattern, content, re.MULTILINE)
            cli_commands = [f"q {cmd}" for cmd in cli_matches]
            
            # チャット内コマンドの抽出（> / で始まる）
            chat_pattern = r'^>\s+(/\w+(?:\s+\w+)?)'
            chat_commands = re.findall(chat_pattern, content, re.MULTILINE)
            
            # コードブロック内のコマンドも抽出（バージョン番号を除外）
            code_block_pattern = r'```(?:bash)?\n((?:q\s+[a-z][a-z-]*|>\s+/\w+)[^\n]*)\n```'
            code_commands = re.findall(code_block_pattern, content, re.MULTILINE)
            
            commands.extend(cli_commands)
            commands.extend(chat_commands)
            commands.extend([cmd.strip() for cmd in code_commands if cmd.startswith(('q ', '> /'))])
    
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
    
    return commands

def verify_command(cmd: str) -> bool:
    """コマンドの存在を確認"""
    cmd = cmd.strip()
    
    # CLIコマンドの確認
    if cmd.startswith('q '):
        # 基本コマンドを抽出（q chat --agent など → q chat）
        base_cmd = ' '.join(cmd.split()[:2])
        return base_cmd in OFFICIAL_CLI_COMMANDS
    
    # チャット内コマンドの確認
    elif cmd.startswith('> /') or cmd.startswith('/'):
        # > /history search -> /history
        cmd_clean = cmd.replace('> ', '')
        base_cmd = cmd_clean.split()[0]
        return base_cmd in OFFICIAL_CHAT_COMMANDS
    
    return True  # その他のコマンドはスキップ

def main():
    docs_dir = Path('docs')
    all_invalid: Dict[str, List[str]] = {}
    all_commands: Set[str] = set()
    
    print("🔍 ドキュメント内のコマンドを検証中...\n")
    
    for md_file in docs_dir.rglob('*.md'):
        commands = extract_commands_from_markdown(md_file)
        all_commands.update(commands)
        
        invalid = [cmd for cmd in commands if not verify_command(cmd)]
        
        if invalid:
            all_invalid[str(md_file)] = invalid
    
    print(f"📊 検証結果:")
    print(f"  - 検証したファイル数: {len(list(docs_dir.rglob('*.md')))}")
    print(f"  - 検出したコマンド数: {len(all_commands)}")
    print(f"  - 問題のあるファイル数: {len(all_invalid)}\n")
    
    if all_invalid:
        print("❌ 存在しないコマンドが見つかりました:\n")
        for file, commands in sorted(all_invalid.items()):
            print(f"📄 {file}:")
            for cmd in commands:
                print(f"  ❌ {cmd}")
            print()
        
        print("🔧 対応が必要です:")
        print("  1. 上記のコマンドを削除または修正してください")
        print("  2. commands.mdで正しいコマンドを確認してください")
        print("  3. 実機で動作確認してください\n")
        
        sys.exit(1)
    else:
        print("✅ すべてのコマンドが確認されました")
        sys.exit(0)

if __name__ == '__main__':
    main()
