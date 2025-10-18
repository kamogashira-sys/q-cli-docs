# コミット前チェックリスト

このチェックリストは、ドキュメントの品質を保証するために、コミット前に必ず確認してください。

---

## 🚫 必須確認事項

### 1. 出典の確認

- [ ] 全ての技術的記述に出典がある
- [ ] バージョン番号はGitHub Releasesで確認済み
- [ ] 設定例は公式ドキュメントまたはソースコードに基づく
- [ ] 外部ツール（k6、MCP等）のバージョンは公式サイトで確認済み

### 2. 表現の確認

- [ ] 推測表現（「おそらく」「と思われる」等）を使用していない
- [ ] 「以降」「以前」等の曖昧な表現を避けている
- [ ] 断定的な記述には必ず根拠がある

### 3. リンクの確認

- [ ] 全ての内部リンクが有効である
- [ ] 全ての外部リンクが有効である
- [ ] GitHubリンクは正しいタグ/コミットを指している

---

## 📋 バージョン番号チェック

### Q CLIバージョン

バージョン番号を記載する場合、以下を確認：

1. **GitHub Releasesで確認**
   ```bash
   curl -s "https://api.github.com/repos/aws/amazon-q-developer-cli/releases" | jq -r '.[].tag_name'
   ```

2. **リリース日を確認**
   ```bash
   curl -s "https://api.github.com/repos/aws/amazon-q-developer-cli/releases" | jq -r '.[] | select(.tag_name == "v1.x.x") | {tag_name, published_at}'
   ```

3. **特殊なタグ名に注意**
   - v1.15.0 → GitHubタグは`v.1.15.0`（ドット付き）
   - 注釈で明記すること

### 外部ツールバージョン

- **Rust**: 公式サイトで確認（例示の場合は「例:」を明記）
- **MCPサーバー**: npmまたはGitHubで確認
- **k6**: 公式GitHubで確認

---

## 🔍 検証方法

### 自動検証

```bash
# バージョン番号と推測表現を検証
python3 /home/katoh/work_records/20251018/verify_documentation.py
```

### 手動検証

1. **出典の確認**
   - 技術的記述に出典リンクがあるか
   - リンクが有効か

2. **バージョン番号の確認**
   - GitHub Releasesと一致するか
   - リリース日が正確か

3. **推測表現の確認**
   - 「おそらく」「と思われる」等がないか
   - 分析ドキュメントの場合は明示的に予測であることを記載

---

## ✅ コミット前の最終確認

- [ ] 全てのチェック項目を確認した
- [ ] 自動検証スクリプトを実行した（問題0件）
- [ ] リンクチェックを実行した（問題0件）
- [ ] コミットメッセージが明確である

---

## 📝 コミットメッセージガイドライン

### フォーマット

```
<type>: <subject>

<body>

<footer>
```

### Type

- `feat`: 新機能追加
- `fix`: バグ修正
- `docs`: ドキュメント変更
- `style`: フォーマット変更
- `refactor`: リファクタリング
- `test`: テスト追加
- `chore`: ビルド・ツール変更

### 例

```
docs: v1.18.0バージョン履歴追加

- v1.18.0の主要機能を追加
- Agent Delegate Toolの説明を追加
- リリース日: 2025-10-13

出典: https://github.com/aws/amazon-q-developer-cli/releases/tag/1.18.0
```

---

## 🔗 関連ドキュメント

- [品質保証ガイド](../docs/05_meta/QUALITY_ASSURANCE.md)
- [検証チェックリスト](../docs/05_meta/VERIFICATION_CHECKLIST.md)
- [実装検証チェックリスト](../docs/05_meta/IMPLEMENTATION_VERIFICATION_CHECKLIST.md)

---

**最終更新**: 2025-10-18  
**作成者**: Amazon Q Developer CLI
