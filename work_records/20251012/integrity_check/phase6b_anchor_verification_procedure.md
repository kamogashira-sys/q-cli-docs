# Phase 6-B: アンカーリンク手動検証手順

**作成日時**: 2025-10-12 18:19  
**対象**: 残り13件のアンカーリンク  
**目的**: GitHubレンダラーでの実際の動作確認

---

## 検証対象リスト

### グループ1: 認証設定関連（3件）

#### 1. `01_installation.md#-認証設定`
- **ソースファイル**: `docs/01_for-users/01_getting-started/02_quick-start.md:L?`
- **リンク**: `[認証設定](01_installation.md#-認証設定)`
- **ターゲット**: `docs/01_for-users/01_getting-started/01_installation.md`
- **期待ヘッダー**: `## 🔐 認証設定`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/01_getting-started/02_quick-start.md

#### 2. `02_quick-start.md#認証設定`
- **ソースファイル**: `docs/01_for-users/02_features/06_ssh-remote.md:L?`
- **リンク**: `[認証設定](../01_getting-started/02_quick-start.md#認証設定)`
- **ターゲット**: `docs/01_for-users/01_getting-started/02_quick-start.md`
- **期待ヘッダー**: `## 🔐 認証設定` または `### 認証設定`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/06_ssh-remote.md

#### 3. `01_installation.md#トラブルシューティング`
- **ソースファイル**: `docs/01_for-users/06_troubleshooting/01_faq.md:L?`
- **リンク**: `[トラブルシューティング](../01_getting-started/01_installation.md#トラブルシューティング)`
- **ターゲット**: `docs/01_for-users/01_getting-started/01_installation.md`
- **期待ヘッダー**: `## トラブルシューティング` または `## 🔧 トラブルシューティング`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/06_troubleshooting/01_faq.md

---

### グループ2: MCP/Agent設定関連（5件）

#### 4. `06_mcp-configuration.md#-mcp設定の読込フロー`
- **ソースファイル**: `docs/01_for-users/03_configuration/02_priority-rules.md:L?`
- **リンク**: `[MCP設定の読込フロー](06_mcp-configuration.md#-mcp設定の読込フロー)`
- **ターゲット**: `docs/01_for-users/03_configuration/06_mcp-configuration.md`
- **期待ヘッダー**: `## 📋 MCP設定の読込フロー`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/03_configuration/02_priority-rules.md

#### 5. `02_common-issues.md#agent設定`
- **ソースファイル**: `docs/01_for-users/03_configuration/04_agent-configuration.md:L?`
- **リンク**: `[トラブルシューティング](../06_troubleshooting/02_common-issues.md#agent設定)`
- **ターゲット**: `docs/01_for-users/06_troubleshooting/02_common-issues.md`
- **期待ヘッダー**: `## Agent設定` または `### Agent設定`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/03_configuration/04_agent-configuration.md

#### 6. `02_common-issues.md#mcp設定`
- **ソースファイル**: `docs/01_for-users/03_configuration/04_agent-configuration.md:L?`
- **リンク**: `[トラブルシューティング](../06_troubleshooting/02_common-issues.md#mcp設定)`
- **ターゲット**: `docs/01_for-users/06_troubleshooting/02_common-issues.md`
- **期待ヘッダー**: `## MCP設定` または `### MCP設定`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/03_configuration/04_agent-configuration.md

#### 7. `06_mcp-configuration.md#-mcp設定の読込フロー` (重複)
- **ソースファイル**: `docs/01_for-users/03_configuration/04_agent-configuration.md:L?`
- **リンク**: `[MCP設定の読込フロー](06_mcp-configuration.md#-mcp設定の読込フロー)`
- **ターゲット**: `docs/01_for-users/03_configuration/06_mcp-configuration.md`
- **期待ヘッダー**: `## 📋 MCP設定の読込フロー`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/03_configuration/04_agent-configuration.md

#### 8. `02_common-issues.md#mcp設定` (重複)
- **ソースファイル**: `docs/01_for-users/03_configuration/06_mcp-configuration.md:L?`
- **リンク**: `[トラブルシューティング](../06_troubleshooting/02_common-issues.md#mcp設定)`
- **ターゲット**: `docs/01_for-users/06_troubleshooting/02_common-issues.md`
- **期待ヘッダー**: `## MCP設定` または `### MCP設定`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/03_configuration/06_mcp-configuration.md

#### 9. `02_common-issues.md#agent設定` (重複)
- **ソースファイル**: `docs/01_for-users/03_configuration/06_mcp-configuration.md:L?`
- **リンク**: `[トラブルシューティング](../06_troubleshooting/02_common-issues.md#agent設定)`
- **ターゲット**: `docs/01_for-users/06_troubleshooting/02_common-issues.md`
- **期待ヘッダー**: `## Agent設定` または `### Agent設定`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/03_configuration/06_mcp-configuration.md

---

### グループ3: トラブルシューティング関連（4件）

#### 10. `06_mcp-configuration.md#トラブルシューティング`
- **ソースファイル**: `docs/01_for-users/06_troubleshooting/01_faq.md:L?`
- **リンク**: `[MCP設定のトラブルシューティング](../03_configuration/06_mcp-configuration.md#トラブルシューティング)`
- **ターゲット**: `docs/01_for-users/03_configuration/06_mcp-configuration.md`
- **期待ヘッダー**: `## トラブルシューティング` または `## 🔧 トラブルシューティング`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/06_troubleshooting/01_faq.md

#### 11. `02_common-issues.md#ログの確認`
- **ソースファイル**: `docs/01_for-users/06_troubleshooting/01_faq.md:L?`
- **リンク**: `[ログの確認](02_common-issues.md#ログの確認)`
- **ターゲット**: `docs/01_for-users/06_troubleshooting/02_common-issues.md`
- **期待ヘッダー**: `## ログの確認` または `### ログの確認`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/06_troubleshooting/01_faq.md

#### 12. `04_agent-configuration.md#ツール権限`
- **ソースファイル**: `docs/01_for-users/06_troubleshooting/01_faq.md:L?`
- **リンク**: `[ツール権限](../03_configuration/04_agent-configuration.md#ツール権限)`
- **ターゲット**: `docs/01_for-users/03_configuration/04_agent-configuration.md`
- **期待ヘッダー**: `## ツール権限` または `### ツール権限`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/06_troubleshooting/01_faq.md

---

### グループ4: 料金関連（1件）

#### 13. `04_pricing.md#enterprise-プラン`
- **ソースファイル**: `docs/01_for-users/01_getting-started/01_installation.md:L?`
- **リンク**: `[Enterprise プラン](04_pricing.md#enterprise-プラン)`
- **ターゲット**: `docs/01_for-users/01_getting-started/04_pricing.md`
- **期待ヘッダー**: `### Enterprise プラン`
- **検証URL**: https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/01_getting-started/01_installation.md

---

## 検証手順

### ステップ1: 各リンクをブラウザで開く

各検証URLをブラウザで開き、ドキュメントを表示します。

### ステップ2: リンクをクリックして動作確認

1. ドキュメント内で該当するリンクテキストを探す
2. リンクをクリック
3. 正しいセクションにジャンプするか確認

### ステップ3: 結果を記録

各リンクについて以下を記録：

```markdown
#### [番号]. [リンク名]
- ✅ 動作OK - そのまま
- ❌ 動作NG - 修正必要
  - 実際のヘッダー: [確認したヘッダー]
  - 正しいアンカー: [正しいアンカーID]
```

---

## 効率的な検証方法

### 方法1: ターゲットファイルのヘッダー確認

各ターゲットファイルで実際のヘッダーを確認：

```bash
# 認証設定のヘッダー確認
grep -n "認証設定" docs/01_for-users/01_getting-started/01_installation.md
grep -n "認証設定" docs/01_for-users/01_getting-started/02_quick-start.md

# トラブルシューティングのヘッダー確認
grep -n "トラブルシューティング" docs/01_for-users/01_getting-started/01_installation.md
grep -n "トラブルシューティング" docs/01_for-users/03_configuration/06_mcp-configuration.md

# Agent/MCP設定のヘッダー確認
grep -n -E "(agent設定|mcp設定)" docs/01_for-users/06_troubleshooting/02_common-issues.md

# その他のヘッダー確認
grep -n "ログの確認" docs/01_for-users/06_troubleshooting/02_common-issues.md
grep -n "ツール権限" docs/01_for-users/03_configuration/04_agent-configuration.md
grep -n "Enterprise" docs/01_for-users/01_getting-started/04_pricing.md
```

### 方法2: GitHubのアンカーID生成ルール

GitHubは以下のルールでアンカーIDを生成：

1. **小文字化**: すべて小文字に変換
2. **スペース**: ハイフン `-` に変換
3. **絵文字**: 削除または `-` に変換
4. **特殊文字**: 削除
5. **日本語**: そのまま保持

**例**:
- `## 🔐 認証設定` → `#-認証設定` または `#認証設定`
- `### Enterprise プラン` → `#enterprise-プラン`
- `## 📋 MCP設定の読込フロー` → `#-mcp設定の読込フロー`

---

## 検証結果記録テンプレート

```markdown
# Phase 6-B: アンカーリンク検証結果

**検証日時**: 2025-10-12 18:19  
**検証者**: [名前]

## 検証結果サマリー

| グループ | 検証数 | OK | NG |
|---------|--------|----|----|
| 認証設定関連 | 3 | ? | ? |
| MCP/Agent設定関連 | 6 | ? | ? |
| トラブルシューティング関連 | 3 | ? | ? |
| 料金関連 | 1 | ? | ? |
| **合計** | **13** | **?** | **?** |

## 詳細結果

### グループ1: 認証設定関連

#### 1. `01_installation.md#-認証設定`
- [ ] ✅ 動作OK
- [ ] ❌ 動作NG
- メモ: 

#### 2. `02_quick-start.md#認証設定`
- [ ] ✅ 動作OK
- [ ] ❌ 動作NG
- メモ: 

#### 3. `01_installation.md#トラブルシューティング`
- [ ] ✅ 動作OK
- [ ] ❌ 動作NG
- メモ: 

### グループ2: MCP/Agent設定関連

#### 4. `06_mcp-configuration.md#-mcp設定の読込フロー`
- [ ] ✅ 動作OK
- [ ] ❌ 動作NG
- メモ: 

#### 5-9. [残りの項目も同様に記録]

### 修正が必要なリンク

[動作NGだったリンクのリスト]

---

**検証完了**: YYYY-MM-DD HH:MM
```

---

## 次のステップ

1. ✅ 上記手順で13件を検証
2. ✅ 結果を記録
3. ✅ 動作NGのリンクを修正
4. ✅ コミット・プッシュ
5. ✅ Phase 7へ進む

---

**作成完了**: 2025-10-12 18:19
