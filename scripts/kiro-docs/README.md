# kiro-docs/ 専用チェックツール

`kiro-docs/`（Kiro CLI ドキュメント）の品質保証を自動化するスクリプト群です。
旧 `docs/`（Amazon Q CLI）用の `scripts/check-*.sh` とは対象が異なるため分離しています。

---

## 一括実行（Makefile）

```bash
make check-kiro-quick   # 高速（URL除く）: counts, links, consistency, changelog, structure, notation
make check-kiro-all     # 全部（重要URL含む）
```

個別:

```bash
make check-kiro-counts        # 機能数・コマンド数の水平展開整合
make check-kiro-links         # 内部相対リンク切れ
make check-kiro-consistency   # 取得日混入・バージョンタグ鮮度・出典日書式
make check-kiro-changelog     # changelog セクション順序・件数
make check-kiro-structure     # 末尾追記・欠番・必須セクション
make check-kiro-notation      # コマンド・フラグ表記の禁止パターン
make check-kiro-urls          # 重要公式URLの 200 確認
```

---

## スクリプト一覧

| スクリプト | 目的 | 終了コード |
|-----------|------|-----------|
| `check-counts.sh` | 機能数（=機能テーブル行数）/ コマンド数（=スラッシュコマンド見出し数）と各所記述の一致 | 不一致で 1 |
| `check-links.py` | `kiro-docs/**/*.md` ＋ ルート README の相対リンク実在（`--check-anchors` で見出しも） | 切れで 1 |
| `check-consistency.sh` | 取得日混入(`YYYY-MM-DD取得`)・`（vX.Y.Z対応）`の鮮度・出典日書式の存在 | 不一致で 1 |
| `check-changelog.sh` | `### vX.Y.Z` の降順・日付書式・`（N件）`と箇条書き数の一致 | 不一致で 1 |
| `check-structure.py` | 機能テーブル末尾＝changelog最新版・NN欠番・必須セクション・相互参照注記・changelog⇔機能文書リンク | 問題で 1 |
| `check-notation.sh` | 実機に存在しない/標準表記に反するコマンド・フラグ表記（`--legacy-ui`・`kiro auth`・`settings set`・`kiro` 単体コマンド）の混入 | 検出で 1 |
| `check-urls.sh` | 外部URLの HTTP 2xx/3xx（`--important`/`--dry-run`/`--sample N`） | エラーで 1 |

### 正準値（単一情報源 / SSoT）

- 機能数 = `kiro-docs/01_features/README.md` の機能テーブル行数
- コマンド数 = `kiro-docs/04_reference/02_slash-commands.md` の `### /...` 見出し数
- 最新バージョン = `kiro-docs/02_update/01_changelog.md` の最初の `### vX.Y.Z`

### スコープ除外

- `kiro-docs/06_embedded-docs/**`（公式OSSの逐語コピー）
- `kiro-docs/05_meta/10_version-update-guide.md`（手順書・テンプレート例）
- `*_update_plan.md`（gitignore対象の計画書）／`*.bak`
- 取得日チェックの「取得時点」（公式不一致を記録する編集注記）は許可

### 保守

- 機能/コマンド数の正準値はファイルから自動抽出するため、追加時に手修正不要。
- バージョンが上がったら `check-structure.py` の `REQUIRED_SECTIONS` / `CROSS_REF`、`check-urls.sh` の `IMPORTANT_URLS` を必要に応じて追記。
- 新バージョンで機能文書（01_features/NN）を追加したら、changelog の当該エントリに「📖 詳細解説」リンクを張り、`check-structure.py` の `CHANGELOG_FEATURE_LINKS` に対応を追記（リンク漏れ・リンク先不在・見出し版ズレを CI が検出）。

---

## 手動チェックリスト（スクリプト対象外）

機械化が困難な項目は、更新時に人手で確認してください。

- [ ] **#7 バックアップ**: 大きな更新の前に対象ファイルの `.bak` を作成した（pre-commit フックは `.bak` を検査しません）。
- [ ] **#8 コミットスコープ**: `git status` が意図したファイルのみを示す（`.bak` / `*_update_plan.md` / `work_records/` が混入していない）。
- [ ] **#15 公式矛盾の扱い**: Ctrl+S 等、公式ページ間で記述が矛盾する箇所は、両論併記＋出典付き注記になっている。
- [ ] **#17 公式ページ本文の再取得**: 公式ページは JS 描画のため `curl` の 200 だけでは本文公開状態を判定できない。重要な変更は実ブラウザ/ヘッドレスで本文を確認した（例: 未公開 patch 本文の有無）。

---

## 検証方針

各スクリプトは「正例（baseline=0）」と「負例（故意の不整合を検出）」の両方で検証済みです（`work_records/20260621/` の作業記録参照）。新規追加・改修時も同様に baseline=0 を確認してください。
