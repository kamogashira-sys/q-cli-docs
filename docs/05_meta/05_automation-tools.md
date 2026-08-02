[ホーム](../README.md) > [Meta](README.md) > 自動化ツール完全ガイド

---

# 自動化ツール完全ガイド

本サイトでは、**3つのツール群**で品質を自動検証しています。

---

## 1. 自動化ツールの全体像

### 3つのツール群

```
1. scripts/ - ドキュメントフォーマットチェック（10ツール）
   ├─ 軽量、高速
   ├─ Git hookで自動実行
   └─ ファイル数、日付、コマンド、設定キー、URL、一貫性、構文、影響範囲、完全性

2. Makefile - 一括検証（1ツール）
   ├─ すべてのチェックを一括実行
   ├─ 高速チェックモード
   └─ 個別チェック対応

3. tools/verification/ - 内容の正確性チェック（8バリデーター）
   ├─ ソースコード、スキーマ、ドキュメントの整合性
   ├─ CI/CDで自動実行
   └─ 環境変数、ファイルパス、設定項目

4. 手動チェック - 実装照合と動作確認（4項目）
   ├─ 自動化できない項目
   ├─ 人間の判断が必要
   └─ 実装照合、動作確認、削除操作、文書品質
```

---

## 2. scripts/ - ドキュメントフォーマットチェック

### 2-1. count-files.sh

**目的**: ファイル数の自動カウント

**使用方法**:
```bash
./scripts/count-files.sh
```

**出力例**:
```
=== ファイル数カウント ===

全ファイル数: 119

カテゴリ別:
  01_for-users: 73 文書
  02_for-developers: 11 文書
  03_for-community: 14 文書
  04_issues: 1 文書
  05_meta: 19 文書
```

**活用シーン**:
- 新規ドキュメント作成後
- ドキュメント削除後
- README.md更新前

---

### 2-2. check-dates.sh

**目的**: Git最終更新日とドキュメント記載日の整合性チェック

**使用方法**:
```bash
# 全体をチェック
./scripts/check-dates.sh

# 特定ディレクトリのみ
./scripts/check-dates.sh docs/05_meta/
```

**出力例**:
```
=== 日付整合性チェック ===

✅ docs/05_meta/01_overview.md
   Git: 2025-11-01, Doc: 2025-11-01

❌ docs/01_for-users/README.md
   Git: 2025-10-26, Doc: 2025-10-19

チェック対象: 119 ファイル
一致: 117 ファイル
不一致: 2 ファイル
```

**活用シーン**:
- ドキュメント更新後
- コミット前の最終チェック
- 定期チェック（週次）

---

### 2-3. search-env-var.sh

**目的**: 環境変数の使用箇所を完全に把握

**使用方法**:
```bash
./scripts/search-env-var.sh 環境変数名

# 例
./scripts/search-env-var.sh Q_DEBUG
```

**出力例**:
```
=== 環境変数検索: Q_DEBUG ===

docs/01_for-users/03_configuration/06_environment-variables.md:45:
  export Q_DEBUG=true

docs/01_for-users/08_guides/06_troubleshooting.md:123:
  Q_DEBUG=true q chat "test"

使用箇所数: 2
```

**活用シーン**:
- 環境変数削除前（必須）
- 環境変数名変更前
- 使用状況の把握

---

### 2-4. validate_commands.sh

**目的**: ドキュメント内のQ CLIコマンド例が正確であることを保証

**使用方法**:
```bash
./scripts/validate_commands.sh
```

**検証内容**:
- 実在するコマンドの取得
- ドキュメントからコマンド抽出
- 存在しないサブコマンドの検証
- オプション指定の正確性確認

**活用シーン**:
- **自動実行**: Git commitフック
- 手動実行: ドキュメント更新後
- Q CLIバージョンアップ後

---

### 2-5. validate_config_keys.sh

**目的**: 設定ファイルのキーが正しいことを保証

**使用方法**:
```bash
./scripts/validate_config_keys.sh
```

**検証内容**:
- Agent設定のキー検証
- MCP設定のキー検証
- グローバル設定のキー検証
- スキーマとの整合性確認

**活用シーン**:
- **自動実行**: Git commitフック
- 設定例追加時
- スキーマ更新後

---

### 2-6. check-urls.sh

**目的**: ドキュメント内のURLが有効であることを確認

**使用方法**:
```bash
# 通常モード（全URLチェック）
./scripts/check-urls.sh

# ドライランモード（URL抽出のみ）
./scripts/check-urls.sh --dry-run

# サンプルモード（最初の10URLのみチェック）
./scripts/check-urls.sh --sample 10
```

**検証内容**:
- ドキュメント内のすべてのURLを抽出（240個）
- 各URLの実在性を **3段フォールバック** で確認
  1. `HEAD`
  2. `GET -r 0-0`（先頭1バイトのみ。HEADを拒むサイト向け）
  3. `GET -r 0-0` + ブラウザ User-Agent（bot対策サイト向け）
- 無効なURLを検出
- 以下を自動スキップ（**スキップしたURLと理由を全件出力**）:
  - ローカルホストURL
  - プレースホルダー（`example.com`、`YOUR_USERNAME`、`your-repo` 等）
  - GitHub API（認証必要）
  - 疎通確認用エンドポイント（URL完全一致で登録）

**スキップ設計の原則**:

ホスト単位のスキップは禁止です。`desktop-release.q.us-east-1.amazonaws.com`
配下には実在しないキーを指すリンク切れが存在し、ホスト単位でスキップすると
これを永久に隠してしまいます（S3 はキー不存在でも 403 を返すため
「403 だからbot対策」と判断できません）。スキップは URL 完全一致か、
プレースホルダのように明確に非リンクな用途に限定します。

**出力例**:
```bash
$ ./scripts/check-urls.sh --sample 5
=== URL実在性チェック ===

🔍 URLを抽出中...
   抽出したURL数: 240

=== サンプルモード（最初の5件のみチェック） ===
🔍 URLをチェック中...

=== スキップしたURL（2件）===
  ⏭️  https://api.example.com … プレースホルダ（記入例）
  ⏭️  https://api.github.com … GitHub API（認証が必要）

=== チェック結果 ===
チェック対象: 5 URL
チェック実施: 3 URL
スキップ: 2 URL
エラー: 0 URL

✅ すべてのURLが有効です
```

**活用シーン**:
- 新規ドキュメント作成後
- 外部リンク追加時
- 定期チェック（月次）

**注意事項**:
- 全URLチェックは約2分かかります（実測 124秒 / 240URL）
- `make check-all` は全数をチェックします。以前は `--sample 10` で
  先頭10件しか見ておらず、231件中221件を見逃していました

---

### 2-7. check-consistency.sh

**目的**: 用語、パス、コマンドの表記揺れを検出

**使用方法**:
```bash
./scripts/check-consistency.sh
```

**検証内容**:
4つの一貫性チェック：
1. **Q CLI表記**: Q-CLI、q-cli（除外: q-cli-docs、ログファイル、パス）
2. **Agent設定パス**: 正しいパスは `~/.aws/amazonq/cli-agents`
3. **Amazon Q Developer CLI表記**: Amazon Q CLI、AmazonQ CLI
4. **コマンド表記**: q-chat（除外: 例示、アンカーリンク）

**出力例**:
```bash
$ ./scripts/check-consistency.sh
=== 一貫性チェック ===

🔍 チェック中: Q CLI表記
🔍 チェック中: Agent設定パス
🔍 チェック中: Amazon Q Developer CLI表記
❌ 不一致を検出: Amazon Q Developer CLI
   正しい表記: 'Amazon Q Developer CLI'
   誤った表記が見つかりました:
     docs/README.md:16:Amazon Q CLI（Amazon Q CLI）は...
     ... 他 15 件

🔍 チェック中: コマンド表記
=== チェック結果 ===
チェック項目: 4
不一致: 1

❌ 一貫性チェックに失敗しました
```

**活用シーン**:
- ドキュメント更新後
- 新規ドキュメント作成後
- 定期チェック（週次）

---

### 2-8. check-commands.sh

**目的**: コマンド構文の正確性を保証

**使用方法**:
```bash
./scripts/check-commands.sh

# メタ構文として除外されたブロックの一覧を表示
./scripts/check-commands.sh --list-skipped
```

**検証内容**:
- bashコードブロックを抽出（1,136ブロック / 7,500行）
- shellcheckで構文チェック（**ブロック単位**）
- Q CLIコマンド検証（671個）
- 24個のサブコマンドと7個のオプションに対応

**ブロック単位で実行する理由**:

以前は全ブロックを1ファイル（7,498行）に連結してから shellcheck に
かけていました。この方式では最初のパースエラーで解析が打ち切られ、
実質1件しか報告されません（実測: 連結1件 vs ブロック単位53件）。
また報告される行番号が連結後のものになり、元ファイルのどこが問題か
分かりませんでした。

**メタ構文の自動判別**:

`` ```bash `` タグが付いていてもシェルスクリプトではないブロックが
あります（Q CLI の REPL 対話ログ、ツール出力の貼り付け、記入用
プレースホルダ、意図的な誤り例など）。これらは docs 側でタグを
変更するのではなく、**ツール側で判別してスキップ**します。

タグを ` ```text ` に変えない理由:
- `verify-commands.yml` → `validate_commands.sh` が `` ```bash `` タグに
  直接依存しており、リタグすると `q` コマンドが CI の検証対象から外れる
- [手動検証プロセス](06_manual-checks.md) が「言語指定がある」を規約化している
- docs 全体で ` ```text ` / ` ```console ` の使用実績が0件

判別は **shellcheck が error を出したブロックにのみ** 適用します。
全ブロックに前置きで適用すると正常なブロックまで検査対象から外れます
（実測: REPL 判定単体で error なしブロック237件が該当）。

**出力例**:
```bash
$ ./scripts/check-commands.sh
=== コマンド構文チェック ===

🔍 コマンドブロックを抽出中...
   抽出したブロック数: 1136
   抽出した行数: 7500

🔍 shellcheckで構文チェック中...
✅ shellcheck: 問題なし（30ブロックはメタ構文として除外）

🔍 Q CLIコマンドをチェック中...
   Q CLIコマンド数: 671
✅ Q CLIコマンド: 問題なし

=== チェック結果 ===
抽出したブロック数: 1136
抽出した行数: 7500
メタ構文として除外: 30 ブロック（--list-skipped で一覧表示）
shellcheckエラー: 0
Q CLIコマンドエラー: 0

✅ すべてのコマンドが正しい構文です
```

問題を検出した場合は **ファイル名と行番号付き** で報告します:
```bash
$ ./scripts/check-commands.sh
❌ docs/05_meta/13_validation-reference.md:726 のコードブロックに構文エラー
   docs/05_meta/13_validation-reference.md (ブロック内 L1):  error: ...
```

**活用シーン**:
- ドキュメント更新後
- コマンド例追加時
- 定期チェック（週次）

**注意事項**:
- shellcheckのインストールが必要: `sudo apt install shellcheck`
- `--severity=error` で実行します。SC2016（単一引用符）や SC1090
  （非定数 source）等の警告はドキュメントの例示では正当なため
  エラーにしません
- validate_commands.shとの違い: より広範な構文チェック

---

### 2-9. check-impact.sh

**目的**: 変更の影響範囲を可視化

**使用方法**:
```bash
# Gitで変更されたファイルを分析
./scripts/check-impact.sh

# 特定のファイルを分析
./scripts/check-impact.sh docs/README.md
```

**検証内容**:
- 変更ファイルの検出
- 重要なキーワードを抽出（Agent, MCP, Knowledge等）
- 同じキーワードを含むファイルを検索
- 影響範囲の可視化

**出力例**:
```bash
$ ./scripts/check-impact.sh docs/README.md
=== 影響範囲分析 ===

📝 指定されたファイルを分析: docs/README.md

🔍 分析中: docs/README.md
   抽出したキーワード:
     - Agent
     - Amazon Q Developer CLI
     - Knowledge
     - MCP
     - Q CLI
     - 環境変数
     - 設定
   'Agent' を含むファイル: 86 件
   'Amazon Q Developer CLI' を含むファイル: 35 件
   'Knowledge' を含むファイル: 41 件
   'MCP' を含むファイル: 61 件
   'Q CLI' を含むファイル: 95 件
   '環境変数' を含むファイル: 66 件
   '設定' を含むファイル: 102 件

=== 分析結果 ===
影響を受ける可能性のあるファイル: 486 件

⚠️  変更の影響範囲を確認してください

推奨アクション:
  1. 影響を受けるファイルをレビュー
  2. 必要に応じて更新
  3. 一貫性チェックを実行: ./scripts/check-consistency.sh
```

**活用シーン**:
- 重要なファイル更新前
- 大規模な変更前
- レビュー時の影響範囲確認

---

### 2-10. check-completeness.py

**目的**: [手動検証プロセス](06_manual-checks.md) に明文化された構造規約を機械化する

**使用方法**:
```bash
# 全ドキュメントをチェック
./scripts/check-completeness.py

# 特定のファイルをチェック
./scripts/check-completeness.py docs/README.md
```

**依存**: `markdown-it-py`（`pip install -r scripts/requirements.txt`）

**検証内容**:

[手動検証プロセス](06_manual-checks.md) の規約を検査します。

| 検査項目 | 規約 |
|---|---|
| コードフェンス外の H1 が正確に1個 | H1（#）: 1つのみ（ファイルタイトル） |
| H2 が1個以上 | H2（##）: セクション |
| 先頭にパンくずリスト | `[ホーム](../README.md) > ...` |
| 最終更新日の記載 | `最終更新: YYYY-MM-DD`（太字は任意） |
| コードフェンスが閉じられている | 閉じタグがある |

加えて **コードフェンスの早期クローズ** を検出します。これは
レンダリングを崩すのに `grep` では見えない厄介なバグです。

| パターン | 症状 |
|---|---|
| 連続する `` ``` `` | 余分な閉じフェンスが次のブロックの「開き」になり、直後の段落や見出しを飲み込む |
| 3バッククォートのネスト | `` ```markdown `` の中の `` ```bash `` が外側も閉じてしまい、以降が本文として漏出する。外側を `` ```` `` にする必要がある |

**設計方針**:

以前は「必須セクションの見出し語彙が完全一致するか」を検査していました
が、docs の見出しは「絵文字＋説明付き」が規約であり、語彙そのものが
乖離していました。部分一致・絵文字除去・h3許容に直しても41件の違反が
1件も解消しないことを実測で確認したため、語彙一致の検査は撤去しました。

Markdown の構造解析は CommonMark 準拠パーサに委ねています。自作の
正規表現ロジックは「閉じフェンスは情報文字列を持てない」といった
CommonMark 規則を取りこぼし、コードブロックの内外判定が反転して
誤った結論を導きます（[問題分析と教訓](07_lessons-learned.md) 参照）。

**出力例**:
```bash
$ ./scripts/check-completeness.py
=== ドキュメント構造チェック ===

📝 全ドキュメントをチェック: 129 ファイル

=== チェック結果 ===
チェック対象: 128 ファイル
除外: 1 ファイル（Jekyll ランディングページ）
規約違反: 0 ファイル

✅ すべてのドキュメントが構造規約を満たしています
```

違反を検出した場合:
```bash
$ ./scripts/check-completeness.py
❌ docs/01_for-users/08_guides/06_troubleshooting.md
     - L711: 余分な閉じフェンス（連続する ``` により空ブロックが開いている）
     - L712: 3バッククォートのネスト（外側 ```(無タグ) を ```` にする必要がある）
```

**活用シーン**:
- 新規ドキュメント作成後
- ドキュメント更新後
- 定期チェック（月次）

**注意事項**:
- `docs/index.md` は GitHub Pages の Jekyll ランディングページのため
  明示的に除外しています
- 終了コード: 問題なし=0 / 規約違反=1 / **ツール自体のエラー（読み込み
  失敗等）=2**。以前は読み込みエラーを「スキップ」に吸収して成功扱いに
  していました

---

## 2. Makefile - 一括検証

### 使用方法

```bash
# すべてのチェックを実行
make check-all

# 高速チェック（URLチェック除く）
make check-quick

# 個別チェック
make check-urls
make check-consistency
make check-commands
make check-impact
make check-completeness

# ヘルプ
make help
```

### 出力例

```bash
$ make check-quick
🔍 一貫性チェック中...
=== 一貫性チェック ===
✅ すべての表記が一貫しています

🔍 コマンド構文チェック中...
=== コマンド構文チェック ===
✅ すべてのコマンドが正しい構文です

🔍 構造チェック中...
=== ドキュメント構造チェック ===
チェック対象: 128 ファイル
除外: 1 ファイル（Jekyll ランディングページ）
規約違反: 0 ファイル
✅ すべてのドキュメントが構造規約を満たしています

✅ 高速チェックが完了しました
```

### 各ターゲットの所要時間

| ターゲット | 所要時間 | 内容 |
|---|---|---|
| `make check-quick` | 約1分 | 一貫性・コマンド構文・構造（URLチェック除く） |
| `make check-all` | 約3分 | check-quick + 全URLチェック（240件） |

### すべてのチェックがゲートである

`check-completeness` は以前 `|| echo "警告のみ"` で警告化されており、
41件の違反があっても `make` が成功していました。`check-commands` も
`shellcheck_errors=0` のハードコードにより常に成功していました。
現在はいずれも実効性のあるゲートです。

### 活用シーン

- **コミット前**: `make check-quick`で高速チェック
- **プッシュ前**: `make check-all`で完全チェック
- **定期チェック**: CI/CDで自動実行

---

## 3. tools/verification/ - 内容の正確性チェック

### 3-1. env_validator.py

**目的**: 環境変数が正しいか検証（70+変数）

**使用方法**:
```bash
cd tools/verification
python3 validators/env_validator.py
```

**検証内容**:
- 環境変数名の正確性
- Q_プレフィックスの確認
- 既知の環境変数との照合

**効果**: 環境変数名の誤りを防止

---

### 3-2. path_validator.py

**目的**: ファイルパスが正しいか検証（10パターン）

**使用方法**:
```bash
cd tools/verification
python3 validators/path_validator.py
```

**検証内容**:
- パス形式の確認
- Q CLI関連パスの確認
- OS依存性の確認

**効果**: パスの誤りを防止

---

### 3-3. v2_validator.py

**目的**: 4つの情報源の整合性を検証

**使用方法**:
```bash
cd tools/verification
python3 validators/v2_validator.py ../../docs
```

**検証内容**:
- ソースコード、調査結果、スキーマ、ドキュメントの整合性
- 環境変数の一貫性
- ファイルパスの一貫性

**効果**: 一貫性率100%を保証

**出力例**:
```
============================================================
v2.0 Validation Report
============================================================

Metrics:
  Files checked: 119
  Total errors: 0
  Total warnings: 0
  Consistency rate: 100.00%

Coverage:
  source_code: 100%
  research: 100%
  schema: 50%
  documentation: 100%

============================================================
✅ All validations passed!
============================================================
```

---

### 3-4. その他のバリデーター

| バリデーター | 検証内容 |
|------------|---------|
| setting_validator.py | 設定項目が正しいか |
| command_validator.py | コマンドが正しいか |
| enum_validator.py | Enum値が正しいか |
| schema_validator.py | スキーマが正しいか |
| type_validator.py | 型が正しいか |

---

## 4. 手動チェック - 実装照合と動作確認

自動化できない項目を人間が確認：

| チェック項目 | 内容 |
|------------|------|
| **実装照合** | ソースコードと一致するか |
| **動作確認** | 実際に動くか |
| **削除操作** | 安全に削除できるか |
| **文書品質** | 読みやすいか |

**詳細**: [手動チェック](06_manual-checks.md)

---

## 5. 全体のワークフロー

### 新規ドキュメント作成時

```
1. ソースコードを確認（手動）
   ↓
2. 実装照合チェックリストを使用（手動）
   ↓
3. 動作確認チェックリストを使用（手動）
   ↓
4. scripts/配下のツールで検証（自動）
   ├─ count-files.sh
   ├─ check-dates.sh
   ├─ validate_commands.sh
   └─ validate_config_keys.sh
   ↓
5. tools/verification/配下のツールで検証（自動）
   ├─ env_validator.py
   ├─ path_validator.py
   └─ v2_validator.py
   ↓
6. 問題なし → コミット
```

---

### ドキュメント更新時

```
1. 変更内容を明確化（手動）
   ↓
2. 影響範囲を確認（手動）
   ↓
3. scripts/配下のツールで検証（自動）
   ├─ check-dates.sh
   └─ search-env-var.sh（必要に応じて）
   ↓
4. tools/verification/配下のツールで検証（自動）
   └─ v2_validator.py
   ↓
5. 問題なし → コミット
```

---

### ドキュメント削除時

```
1. 削除操作チェックリストを使用（手動）
   ↓
2. search-env-var.shで使用箇所を確認（自動）
   ↓
3. 使用箇所0件を確認（手動）
   ↓
4. 削除実行（手動）
   ↓
5. scripts/配下のツールで検証（自動）
   └─ count-files.sh
   ↓
6. tools/verification/配下のツールで検証（自動）
   └─ v2_validator.py
   ↓
7. 問題なし → コミット
```

---

## セットアップ

### scripts/配下のツール

```bash
# 実行権限を付与
chmod +x scripts/*.sh

# 動作確認
./scripts/count-files.sh
```

---

### tools/verification/配下のツール

```bash
# ディレクトリに移動
cd tools/verification

# 依存関係をインストール
make install

# または手動で
pip install -r requirements.txt
pip install -e .

# 動作確認
python3 validators/v2_validator.py ../../docs
```

---

## トラブルシューティング

### ツールが動作しない

**対応**:
1. 実行権限を確認: `chmod +x scripts/*.sh`
2. 依存コマンドを確認: `git`, `rg`, `python3`
3. カレントディレクトリを確認: プロジェクトルートで実行

---

### 警告が出た

**対応**:
1. 警告内容を確認
2. 該当箇所を修正
3. 再度検証
4. 警告が消えるまで繰り返す

**警告を無視しないでください。**

---

## 新規ツール作成時の注意

### テンプレートの使用（推奨）

新しいチェックツールは**テンプレートから作成**することを強く推奨します。

```bash
# テンプレートから作成
./tools/create-check-tool.sh check-your-tool "Check for your issue"

# 生成されるファイル
# - tools/check-your-tool.sh（ツール本体）
# - tools/test-check-your-tool.sh（テスト）
```

**メリット**:
- ✅ ベストプラクティスが組み込まれている
- ✅ テストが必須化される
- ✅ 5分で作成可能

詳細: [tools/templates/README.md](../../tools/templates/README.md)

### 必須チェック

新しいチェックツールを作成する際は、**[ツール作成チェックリスト](14_tool-creation-checklist.md)** を必ず確認してください。

### 重要な原則

1. **既知のバグでテストする**
   - 正常系だけでなく異常系も必須
   - 検出できることを確認してから使用

2. **出力を必ず確認する**
   - リダイレクトで結果を捨てない
   - 何を検出したか明示する
   - 終了コードだけで判断しない

3. **シンプルな手法を選ぶ**
   - 複雑な正規表現より行単位処理
   - デバッグしやすい実装
   - 保守性を重視

### ツールテスト検証

全てのチェックツールにはテストファイルが必要です：

```bash
# テスト存在確認
./tools/verify-tool-tests.sh

# 出力例
✅ check-consecutive-separators.sh has test
✅ check-your-tool.sh has test
✅ All tools have tests
```

**pre-commitフック**で自動的にチェックされます。

### 過去の失敗例

連続区切り線チェックツール（2025-11-01）で、grep -Pzo + リダイレクトにより実際には何も検出できていなかった問題が発生しました。

詳細: [問題分析と教訓 - 問題9](07_lessons-learned.md#問題9-テストツールの検証不足)

---

## 関連ドキュメント

- **[ツール作成チェックリスト](14_tool-creation-checklist.md)** - 新規ツール作成時の必須チェック
- **[手動チェック](06_manual-checks.md)** - 4つのチェックリスト
- **[日常的な作業フロー](09_daily-workflow.md)** - 新規作成・更新・削除
- **[公開リソース一覧](12_resources.md)** - 全リソースの一覧


---

**最終更新**: 2025-11-01
