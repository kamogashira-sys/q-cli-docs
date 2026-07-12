[ホーム](../README.md) > [機能詳細ガイド](README.md) > MCP OAuth 認証管理

---

# MCP OAuth 認証管理・事前登録アプリ対応

## 概要

リモート（HTTP）MCP サーバーの **OAuth 認証**を制御・運用するための機能群です。v2.3.0 で追加された `oauth.clientId` 設定を土台に、**v2.11.0** で認証フローを操作する専用コマンド（`/mcp auth`・`/mcp cancel-auth`・`/mcp logout`）と MCP パネルのショートカットが加わり、**v2.12.0** で「事前登録済み OAuth アプリ」への接続（`clientSecret`・カスタム `redirectUri`・Dynamic Client Registration のスキップ）に対応しました。

これにより、トークン失効や認証フローの停止といったトラブル時に、セッションを再起動したり資格情報を手動削除したりせずに復旧できます。Figma のように事前登録アプリ（client secret 必須）を要求するサーバーにも接続できます。

## 認証管理コマンド（v2.11.0）

リモート MCP サーバーの OAuth 資格情報をその場で制御します。

| コマンド | 動作 |
|---------|------|
| `/mcp auth` | OAuth 再認証を強制（トークンが失効・無効になったとき） |
| `/mcp cancel-auth` | ブラウザ確認待ちで停止した認証フローを中止 |
| `/mcp logout` | 保存済みの OAuth 資格情報を削除 |

**MCP パネルのショートカット**（ステータスビュー）:

| キー | 動作 |
|------|------|
| `^A` | 認証を強制（auth） |
| `^X` | 認証を中止（cancel-auth） |
| `^R` | 資格情報を削除（logout） |

> 公式: [`/mcp auth`（スラッシュコマンドリファレンス）](https://kiro.dev/docs/cli/reference/slash-commands/#mcp-auth)

## 事前登録アプリ向け OAuth 設定（v2.12.0）

MCP サーバーごとの OAuth 設定（`~/.kiro/settings/mcp.json` のサーバー定義内）で、事前登録済みアプリに対応する項目が拡張されました。設定キーは **camelCase** です。

| 設定キー | 説明 | 追加/対応 |
|---------|------|----------|
| `clientId` | 事前登録アプリのクライアント ID。設定すると **Dynamic Client Registration（DCR）をスキップ**し、自身のアプリとして認証 | v2.3.0（DCR スキップは v2.12.0） |
| `clientSecret` | トークンエンドポイント認証を要する confidential client 向けのクライアントシークレット | **v2.12.0** |
| `redirectUri` | カスタムコールバックパスを含む**フル URL**（例 `http://localhost:7778/oauth/callback`）。コールバックホストは安全のため **localhost に限定** | **v2.12.0** |

### 設定例（`~/.kiro/settings/mcp.json`）

```json
{
  "mcpServers": {
    "example-remote": {
      "url": "https://mcp.example.com",
      "oauth": {
        "clientId": "my-registered-app-id",
        "clientSecret": "my-client-secret",
        "redirectUri": "http://localhost:7778/oauth/callback"
      }
    }
  }
}
```

> スキーマ・キー名の正準は公式リファレンスに従ってください（本サイトは公式表記の camelCase を採用）。

## 使用例

1. リモート MCP サーバーのトークンが失効し接続に失敗する → `/mcp auth`（または MCP パネルで `^A`）で再認証。
2. ブラウザ認可待ちのまま固まった → `/mcp cancel-auth`（`^X`）で中止し、やり直す。
3. 資格情報をローテーションしたい／別アカウントに切り替えたい → `/mcp logout`（`^R`）で削除してから再認証。
4. Figma など事前登録アプリ必須のサーバー → `mcp.json` の `oauth` に `clientId` と `clientSecret` を設定（DCR は自動スキップ）。

## 注意点・制限事項

- コールバックホストは **localhost（loopback）に限定**されます（`redirectUri` のフル URL 対応時も検証されます）。
- 設定キーは **camelCase**（`clientId` / `clientSecret` / `redirectUri`）。CLI 内蔵 changelog では snake_case 表記（`client_id` 等）で説明される場合がありますが、`mcp.json` の設定キーは camelCase です。
- 認証管理コマンドとパネルショートカットは **リモート（OAuth 対応）MCP サーバー**が対象です。
- 組織管理者が MCP を無効化している場合は、ガバナンスに従いメッセージが表示されます。

## 関連リンク

- [MCP OAuth 設定（公式リファレンス）](https://kiro.dev/docs/cli/mcp/configuration/#oauth-configuration)
- [`/mcp auth`（公式スラッシュコマンドリファレンス）](https://kiro.dev/docs/cli/reference/slash-commands/#mcp-auth)
- [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md) — `/mcp` サブコマンドの一覧
- [12. Remote Authentication](12_RemoteAuth.md) — ユーザー側のリモート認証（SSO 等。MCP サーバー OAuth とは別）
- [02_update/01_changelog.md](../02_update/01_changelog.md) — v2.11.0 / v2.12.0 の変更履歴

---

**最終更新**: 2026-07-12  
**対象バージョン**: Kiro CLI v2.12.0（認証管理コマンドは v2.11.0）
