# チェックポイント仕様書

**対象バージョン**: v1.18.1以降  
**ソースコード**: `crates/chat-cli/src/cli/chat/checkpoint.rs`

---

## 1. 概要

### 1.1 目的

チェックポイント機能は、Q CLIの会話セッション中にワークスペースの状態を保存・復元する機能です。ツール実行による変更を追跡し、必要に応じて以前の状態に戻すことができます。

### 1.2 主要な特徴

| 特徴 | 説明 |
|------|------|
| **Gitベース** | シャドウGitリポジトリを使用した変更追跡 |
| **自動保存** | ターンとツール実行ごとに自動チェックポイント作成 |
| **会話履歴統合** | ファイル変更と会話履歴を同期して保存 |
| **柔軟な復元** | Soft/Hard復元モードをサポート |
| **高速検索** | タグベースの高速チェックポイント検索 |

### 1.3 使用条件

| 条件 | 説明 |
|------|------|
| **Git必須** | `git`コマンドがインストールされている必要がある |
| **Gitリポジトリ内** | 作業ディレクトリがGitリポジトリ内にある必要がある |
| **自動初期化** | 条件を満たす場合、自動的に初期化される |

---

## 2. データ構造

### 2.1 CheckpointManager

チェックポイントシステムの中核となる管理構造体です。

| # | フィールド名 | 型 | 必須 | 説明 |
|---|------------|-----|------|------|
| 1 | `shadow_repo_path` | PathBuf | ✅ | シャドウGitリポジトリのパス |
| 2 | `work_tree_path` | PathBuf | ✅ | 作業ディレクトリのパス |
| 3 | `checkpoints` | Vec\<Checkpoint\> | ✅ | 全チェックポイント（時系列順） |
| 4 | `tag_index` | HashMap\<String,usize\> | ✅ | タグ→インデックスの高速検索マップ |
| 5 | `current_turn` | usize | ✅ | 現在のターン番号 |
| 6 | `tools_in_turn` | usize | ✅ | 現在のターン内のツール使用数 |
| 7 | `pending_user_message` | Option\<String\> | ❌ | コミット説明用のユーザーメッセージ |
| 8 | `message_locked` | bool | ✅ | メッセージがロックされているか |
| 9 | `file_stats_cache` | HashMap\<String,FileStats\> | ✅ | ファイル変更統計のキャッシュ |

### 2.2 Checkpoint

個別のチェックポイント情報を保持する構造体です。

| # | フィールド名 | 型 | 必須 | 説明 |
|---|------------|-----|------|------|
| 1 | `tag` | String | ✅ | チェックポイントタグ（例: "0", "1", "1.1"） |
| 2 | `timestamp` | DateTime\<Local\> | ✅ | 作成日時 |
| 3 | `description` | String | ✅ | チェックポイントの説明 |
| 4 | `history_snapshot` | VecDeque\<HistoryEntry\> | ✅ | 会話履歴のスナップショット |
| 5 | `is_turn` | bool | ✅ | ターンチェックポイントか |
| 6 | `tool_name` | Option\<String\> | ❌ | ツール名（ツールチェックポイントの場合） |

### 2.3 FileStats

ファイル変更統計を保持する構造体です。

| # | フィールド名 | 型 | 説明 |
|---|------------|-----|------|
| 1 | `added` | usize | 追加されたファイル数 |
| 2 | `modified` | usize | 変更されたファイル数 |
| 3 | `deleted` | usize | 削除されたファイル数 |

---

## 3. タグ命名規則

### 3.1 タグフォーマット

| タグ種別 | フォーマット | 例 | 説明 |
|---------|------------|-----|------|
| **初期状態** | `"0"` | `"0"` | セッション開始時の初期チェックポイント |
| **ターン** | `"{turn}"` | `"1"`, `"2"`, `"3"` | ユーザーターンごとのチェックポイント |
| **ツール実行** | `"{turn}.{tool}"` | `"1.1"`, `"1.2"`, `"2.1"` | ツール実行ごとのチェックポイント |

### 3.2 タグの進行例

```
0           # 初期状態
1           # ターン1開始
1.1         # ターン1のツール1実行後
1.2         # ターン1のツール2実行後
2           # ターン2開始
2.1         # ターン2のツール1実行後
3           # ターン3開始
```

### 3.3 前のタグの計算ロジック

| 現在のタグ | 前のタグ | 計算ロジック |
|-----------|---------|-------------|
| `"1.1"` | `"1"` | ツール番号が1の場合、ターン番号のみ |
| `"1.2"` | `"1.1"` | ツール番号を1減らす |
| `"2"` | `"1"` | ターン番号を1減らす |
| `"0"` | `"0"` | 初期状態（前のタグなし） |

---

## 4. 初期化

### 4.1 自動初期化

条件を満たす場合、自動的に初期化されます。

| 条件 | 確認方法 |
|------|---------|
| **Git installed** | `git --version`が成功 |
| **In git repo** | `git rev-parse --is-inside-work-tree`が成功 |

**初期化処理**:

1. シャドウリポジトリディレクトリを作成
2. Bare Gitリポジトリを初期化（`git init --bare`）
3. Git設定を構成（user.name, user.email, core.preloadindex）
4. 初期チェックポイント（タグ`"0"`）を作成
5. CheckpointManager構造体を構築

### 4.2 手動初期化

`/checkpoint init`コマンドで手動初期化も可能です。

```bash
# チャットセッション内で
/checkpoint init
```

### 4.3 Git設定

| 設定項目 | 値 | 説明 |
|---------|-----|------|
| `user.name` | `"Q"` | コミット作成者名 |
| `user.email` | `"qcli@local"` | コミット作成者メール |
| `core.preloadindex` | `"true"` | インデックスの事前読み込みを有効化 |

---

## 5. チェックポイント作成

### 5.1 作成タイミング

| タイミング | タグ形式 | 説明 |
|-----------|---------|------|
| **セッション開始** | `"0"` | 初期状態を保存 |
| **ターン開始** | `"{turn}"` | ユーザーメッセージ受信時 |
| **ツール実行後** | `"{turn}.{tool}"` | 各ツール実行完了時 |

### 5.2 作成プロセス

1. **ステージング**: `git add -A`で全変更をステージング
2. **コミット**: `git commit --allow-empty --no-verify -m "{description}"`
3. **タグ付け**: `git tag {tag} -f`でタグを作成
4. **メタデータ記録**: Checkpoint構造体を作成してcheckpointsベクターに追加
5. **インデックス更新**: tag_indexマップを更新
6. **統計キャッシュ**: ファイル変更統計を計算してキャッシュ

### 5.3 重複タグの処理

| ケース | 処理 |
|--------|------|
| **ターンチェックポイント** | 既存を削除して末尾に追加（時系列順を維持） |
| **ツールチェックポイント** | 上書き（同じタグで更新） |

---

## 6. チェックポイント復元

### 6.1 復元モード

| モード | 説明 | 使用コマンド |
|--------|------|-------------|
| **Soft** | 追跡ファイルのみ復元 | `git checkout {tag} -- .` |
| **Hard** | 作業ディレクトリ全体をリセット | `git reset --hard {tag}` |

### 6.2 復元プロセス

1. **チェックポイント検索**: tag_indexから対象チェックポイントを取得
2. **ファイル復元**: 
   - Soft: 追跡ファイルのみチェックアウト
   - Hard: 作業ディレクトリ全体をリセット
3. **会話履歴復元**: history_snapshotから会話履歴を復元
4. **状態更新**: ConversationStateを更新

### 6.3 空ツリーの処理

タグに追跡ファイルがない場合（空ツリー）、Soft復元は何もせずに成功します。

**確認方法**:
```bash
git ls-tree -r --name-only {tag}
```

出力が空の場合、空ツリーと判定されます。

---

## 7. ファイル変更統計

### 7.1 統計計算

`git diff --name-status`を使用してファイル変更を分析します。

| ステータス | 意味 | カウント先 |
|-----------|------|-----------|
| `A` | Added | `added` |
| `M` | Modified | `modified` |
| `D` | Deleted | `deleted` |
| `R` | Renamed | `modified` |
| `C` | Copied | `modified` |

### 7.2 統計キャッシュ

計算済みの統計は`file_stats_cache`にキャッシュされ、再計算を避けます。

**キャッシュキー**: チェックポイントタグ（例: `"1.1"`）

### 7.3 差分表示

`diff`メソッドで2つのチェックポイント間の詳細な差分を生成できます。

**出力形式**:
```
  + file1.txt (added)
  ~ file2.txt (modified)
  - file3.txt (deleted)

 file1.txt | 10 ++++++++++
 file2.txt |  5 +++--
 file3.txt | 20 --------------------
 3 files changed, 13 insertions(+), 22 deletions(-)
```

---

## 8. Gitリポジトリ構造

### 8.1 シャドウリポジトリ

Bare Gitリポジトリとして作成されます。

```
{shadow_repo_path}/
├── HEAD                    # 現在のブランチ参照
├── config                  # Git設定
├── description             # リポジトリ説明
├── hooks/                  # Gitフック（未使用）
├── info/                   # 除外パターン等
│   └── exclude
├── objects/                # Gitオブジェクト（コミット、ツリー、ブロブ）
│   ├── info/
│   └── pack/
└── refs/                   # 参照
    ├── heads/              # ブランチ（未使用）
    └── tags/               # チェックポイントタグ
        ├── 0
        ├── 1
        ├── 1.1
        ├── 1.2
        └── 2
```

### 8.2 作業ディレクトリ

`work_tree_path`は現在の作業ディレクトリ（`std::env::current_dir()`）を指します。

**Git操作時の指定**:
```bash
git --git-dir={shadow_repo_path} --work-tree={work_tree_path} {command}
```

---

## 9. クリーンアップ

### 9.1 自動クリーンアップ

CheckpointManagerがドロップされる際、シャドウリポジトリを自動削除します。

**実装**:
- Tokioランタイムが利用可能な場合: 非同期タスクで削除
- それ以外: 別スレッドで削除

### 9.2 手動クリーンアップ

`cleanup()`メソッドで明示的にクリーンアップできます。

```rust
checkpoint_manager.cleanup(&os).await?;
```

---

## 10. エラーハンドリング

### 10.1 初期化エラー

| エラー | 原因 | 対処法 |
|--------|------|--------|
| **Git not installed** | `git`コマンドが見つからない | Gitをインストール |
| **Not in git repo** | Gitリポジトリ外で実行 | Gitリポジトリ内で実行するか`/checkpoint init`を使用 |
| **Init failed** | リポジトリ初期化失敗 | ディレクトリの書き込み権限を確認 |

### 10.2 操作エラー

| エラー | 原因 | 対処法 |
|--------|------|--------|
| **Checkpoint not found** | 指定タグが存在しない | `/checkpoint list`で利用可能なタグを確認 |
| **Restore failed** | Git操作が失敗 | 作業ディレクトリの状態を確認 |
| **Commit failed** | コミット作成失敗 | Git設定とディスク容量を確認 |

---

## 11. パフォーマンス最適化

### 11.1 高速検索

`tag_index`ハッシュマップにより、O(1)でチェックポイントを検索できます。

| 操作 | 計算量 | 説明 |
|------|--------|------|
| **タグ検索** | O(1) | ハッシュマップによる直接アクセス |
| **チェックポイント取得** | O(1) | インデックスによる配列アクセス |
| **全チェックポイント列挙** | O(n) | ベクターの線形走査 |

### 11.2 統計キャッシュ

計算済みのファイル変更統計をキャッシュし、再計算を回避します。

**キャッシュヒット率**: 同じチェックポイントの統計を複数回参照する場合に有効

### 11.3 Git最適化

| 設定 | 効果 |
|------|------|
| `core.preloadindex=true` | インデックスの並列読み込みで高速化 |
| `--allow-empty` | 変更がない場合でもコミット作成を許可 |
| `--no-verify` | Gitフックをスキップして高速化 |

---

## 12. 使用例

### 12.1 基本的な使用フロー

```rust
// 1. 自動初期化
let manager = CheckpointManager::auto_init(&os, shadow_path, &history).await?;

// 2. チェックポイント作成
manager.create_checkpoint("1", "Turn 1", &history, true, None)?;
manager.create_checkpoint("1.1", "Tool: fs_write", &history, false, Some("fs_write".to_string()))?;

// 3. 変更確認
if manager.has_changes()? {
    println!("Uncommitted changes detected");
}

// 4. 統計取得
let stats = manager.compute_file_stats("1.1")?;
println!("Added: {}, Modified: {}, Deleted: {}", stats.added, stats.modified, stats.deleted);

// 5. 差分表示
let diff = manager.diff("1", "1.1")?;
println!("{}", diff);

// 6. 復元
manager.restore(&mut conversation, "1", false)?; // Soft restore
```

### 12.2 チェックポイント一覧表示

```rust
for checkpoint in &manager.checkpoints {
    println!("[{}] {} - {}", 
        checkpoint.tag, 
        checkpoint.timestamp.format("%Y-%m-%d %H:%M:%S"),
        checkpoint.description
    );
}
```

### 12.3 前のチェックポイントとの比較

```rust
let current_tag = "1.2";
let prev_tag = get_previous_tag(current_tag); // "1.1"
let stats = manager.compute_stats_between(&prev_tag, current_tag)?;
```

---

## 関連ドキュメント

- [CLI Bash History仕様書](./01_cli-bash-history.md) - 会話履歴の構造
- [Agent設定ガイド](../03_configuration/03_agent-configuration.md) - Agent設定との連携
- [トラブルシューティング](../06_troubleshooting/02_common-issues.md) - 一般的な問題と解決策

---

**注意事項**:
- チェックポイント機能はGitリポジトリ内でのみ使用可能です
- シャドウリポジトリは一時的なもので、セッション終了時に削除されます
- 大量のファイル変更がある場合、チェックポイント作成に時間がかかる可能性があります
- チェックポイントは会話セッション内でのみ有効で、セッション間では共有されません

---

最終更新: 2025-10-25
