[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [ベストプラクティス](README.md) > 06 Load Testing With K6

---

# k6を使った負荷テストの自動化


---

## 📋 このガイドについて

このガイドでは、Q CLIとPlaywright MCP、k6を組み合わせた負荷テストの自動化方法を詳しく説明します。シナリオキャプチャからスクリプト生成、実行、分析、チューニングまでの全工程を、ステップバイステップで解説します。

> **⚠️ 注意事項**
> 
> このガイドで紹介する手法は、AWS Summit 2024のセッションで紹介されたものです。
> Q CLIの特定バージョンに依存する機能ではなく、MCP（Model Context Protocol）とk6を組み合わせた汎用的なアプローチです。

### 対象読者
- 負荷テストを自動化したい開発者
- パフォーマンステストの効率化を目指すチーム
- Q CLIの高度な活用方法を学びたい方

---

## 🎬 参考動画

このガイドは、以下のAWS Summit 2024セッションで紹介された手法を基にしています。

**[生成 AI 時代の負荷テスト on AWS 〜 AI は負荷テストをどれだけ爆速にできるか？〜](https://www.youtube.com/watch?v=beR_FEwPo74)**

**動画の内容**:
- Q CLIをAIエージェントとして活用した負荷テストの自動化
- Playwright MCPによるブラウザ操作のキャプチャ
- k6スクリプトの自動生成（パラメータ抽出、エラーハンドリング含む）
- AWS Observabilityサービス（X-Ray、CloudWatch）との連携
- ボトルネック分析からコード修正、デプロイまでの自律的な実行

**発表者**: AWSソリューションアーキテクト  
**時間**: 約30分  
**レベル**: 中級〜上級

---

## 🎯 Q CLIで実現できること

### 1. シナリオの自動作成

Playwright MCPを使用して、実際のユーザー操作をキャプチャします。

**実現内容**:
- ブラウザ操作の自動記録
- ネットワークリクエストの詳細キャプチャ
- HTTPリクエスト/レスポンスの完全な記録

### 2. 実用的なスクリプト生成

キャプチャしたデータから、実用的なk6スクリプトを自動生成します。

**含まれる要素**:
- **パラメータ抽出（相関処理）**: 前のリクエストのレスポンスから次のリクエストに必要なパラメータ（認証トークンなど）を抽出
- **エラーハンドリング**: 失敗時の適切な処理
- **リクエストのグルーピング**: ユーザー操作に紐づくリクエストの論理的なグループ化
- **タグ付け**: リクエストごとの集計のためのタグ設定

### 3. 自律的なテスト実行

Q CLIが自律的に負荷テストのサイクル全体を実行します。

**実行内容**:
- データベースのリセット（テスト条件の統一）
- k6による負荷実行
- 結果の自動評価（閾値との比較）

### 4. パフォーマンス分析とチューニング

AWS Observabilityサービスと連携して、ボトルネックを特定します。

**分析内容**:
- AWS X-Rayからトレースデータを収集
- CloudWatchからメトリクスとログを収集
- ボトルネックの自動特定
- コード修正とデプロイの自律実行

---

## 🚀 クイックスタート

最小限の手順で負荷テストを試してみましょう。

### 前提条件

- Q CLI（最新版推奨）
- Node.js（Playwright MCP用）
- k6がインストール済み

### 手順

```bash
# 1. 負荷テスト用Agentを作成
cat > ~/.aws/amazonq/agents/load-test.json << 'EOF'
{
  "name": "load-test",
  "description": "k6負荷テスト自動化エージェント",
  "instructions": [
    "Playwright MCPを使ってブラウザ操作をキャプチャする",
    "ネットワークリクエストからk6スクリプトを生成する",
    "k6を実行して結果を評価する"
  ],
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    }
  }
}
EOF

# 2. Agentに切り替え
q agent set-default load-test

# 3. チャットを開始
q chat
```

チャット内で指示：
```
> https://example.com にアクセスして、ログインからカート投入までの操作をキャプチャして
> ネットワークリクエストをrequests.txtに保存して
```

---

## 📖 ステップバイステップガイド

### Step 1: 環境準備

#### 必要なツールのインストール

```bash
# k6のインストール（macOS）
brew install k6

# k6のインストール（Linux）
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# Node.js（Playwright MCP用）
# すでにインストール済みの場合はスキップ
```

#### Agent設定の作成

詳細なAgent設定を作成します。

`~/.aws/amazonq/agents/load-test.json`:

```json
{
  "name": "load-test",
  "description": "k6負荷テスト自動化エージェント",
  "instructions": [
    "Playwright MCPを使ってブラウザ操作をキャプチャする",
    "ネットワークリクエストからk6スクリプトを生成する",
    "実用的な要素（パラメータ抽出、エラーハンドリング、タグ付け）を含める",
    "k6を実行して結果を評価する",
    "AWS Observabilityサービス（X-Ray、CloudWatch）からテレメトリを収集・分析する",
    "ボトルネックを特定してコードを修正する",
    "必要に応じてCDKコードを修正してデプロイする"
  ],
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    }
  },
  "allowedTools": [
    "execute_bash",
    "fs_read",
    "fs_write",
    "use_aws"
  ]
}
```

---

### Step 2: シナリオキャプチャ

Playwright MCPを使用して、ユーザー操作をキャプチャします。

```bash
# Agentに切り替え
q agent set-default load-test

# チャットを開始
q chat
```

チャット内で指示：
```
> Playwrightで以下のシナリオをキャプチャして：
> 1. https://example.com にアクセス
> 2. ログインフォームにメールアドレスとパスワードを入力
> 3. ログインボタンをクリック
> 4. 商品ページに移動
> 5. カートに商品を追加
> 6. カートページを表示
> 
> すべてのネットワークリクエストをrequests.txtに保存して
```

**Q CLIの動作**:
1. Playwright MCPを起動
2. ブラウザを自動操作
3. ネットワークリクエストを記録
4. `requests.txt`に保存

---

### Step 3: スクリプト生成

キャプチャしたリクエストからk6スクリプトを生成します。

チャット内で指示：
```
> requests.txtからk6スクリプトを生成して：
> - 認証トークンを前のレスポンスから抽出して次のリクエストで使用
> - エラーが発生したら処理を中断
> - 各リクエストにタグを付けて集計できるようにする
> - ユーザー操作ごとにグループ化する
> 
> スクリプトをload-test.jsに保存して
```

**生成されるスクリプトの例**:

```javascript
import http from 'k6/http';
import { check, group } from 'k6';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  let authToken;

  group('Login', function () {
    const loginRes = http.post('https://example.com/api/login', 
      JSON.stringify({
        email: 'test@example.com',
        password: 'password123'
      }), 
      {
        headers: { 'Content-Type': 'application/json' },
        tags: { name: 'Login' },
      }
    );

    check(loginRes, {
      'login successful': (r) => r.status === 200,
    }) || fail('Login failed');

    authToken = loginRes.json('token');
  });

  group('Add to Cart', function () {
    const cartRes = http.post('https://example.com/api/cart', 
      JSON.stringify({
        productId: '12345',
        quantity: 1
      }), 
      {
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        tags: { name: 'AddToCart' },
      }
    );

    check(cartRes, {
      'add to cart successful': (r) => r.status === 200,
    }) || fail('Add to cart failed');
  });

  sleep(1);
}
```

---

### Step 4: 負荷テスト実行

k6を実行して負荷テストを実施します。

チャット内で指示：
```
> 以下の手順で負荷テストを実行して：
> 1. データベースをリセット（reset-db.shを実行）
> 2. k6でload-test.jsを実行
> 3. 結果を確認して閾値と比較
> 4. 結果をresults.txtに保存
```

**Q CLIの動作**:
1. データベースリセットスクリプトを実行
2. `k6 run load-test.js`を実行
3. 結果を解析
4. 閾値との比較を実施

**k6の出力例**:
```
     ✓ login successful
     ✓ add to cart successful

     checks.........................: 100.00% ✓ 1000      ✗ 0
     data_received..................: 2.5 MB  42 kB/s
     data_sent......................: 500 kB  8.3 kB/s
     http_req_duration..............: avg=245ms min=120ms med=230ms max=480ms p(95)=420ms
     http_req_failed................: 0.00%   ✓ 0        ✗ 1000
```

---

### Step 5: 分析とチューニング

AWS Observabilityサービスからテレメトリを収集し、ボトルネックを特定します。

チャット内で指示：
```
> AWS X-Rayから過去1時間のトレースデータを取得して：
> - レスポンスタイムが500ms以上のリクエストを特定
> - ボトルネックとなっているサービスを分析
> - 改善案を提示して
```

**Q CLIの動作**:
1. AWS X-Ray APIを呼び出し
2. トレースデータを分析
3. ボトルネックを特定
4. 改善案を提示

**分析結果の例**:
```
ボトルネック分析結果：

1. データベースクエリが遅い（平均450ms）
   - 原因: インデックスが設定されていない
   - 改善案: user_idカラムにインデックスを追加

2. Lambda関数のコールドスタート（初回300ms）
   - 原因: プロビジョニング済み同時実行数が未設定
   - 改善案: プロビジョニング済み同時実行数を5に設定
```

チャット内で指示：
```
> 提案された改善案を実装して：
> 1. データベースマイグレーションスクリプトを作成
> 2. CDKコードを修正してLambdaのプロビジョニング済み同時実行数を設定
> 3. デプロイを実行
> 4. 再度負荷テストを実行して効果を確認
```

---

## ⚙️ Agent設定の詳細

### 基本設定

```json
{
  "name": "load-test",
  "description": "k6負荷テスト自動化エージェント"
}
```

### instructions（指示）

Agentの動作を定義します。

```json
"instructions": [
  "Playwright MCPを使ってブラウザ操作をキャプチャする",
  "ネットワークリクエストからk6スクリプトを生成する",
  "実用的な要素（パラメータ抽出、エラーハンドリング、タグ付け）を含める",
  "k6を実行して結果を評価する",
  "AWS Observabilityサービスからテレメトリを収集・分析する",
  "ボトルネックを特定してコードを修正する"
]
```

### mcpServers（MCPサーバー）

Playwright MCPを設定します。

```json
"mcpServers": {
  "playwright": {
    "command": "npx",
    "args": ["-y", "@playwright/mcp-server"]
  }
}
```

### allowedTools（許可ツール）

必要なツールを許可します。

```json
"allowedTools": [
  "execute_bash",  // k6実行、データベースリセット用
  "fs_read",       // リクエストファイル読み込み用
  "fs_write",      // スクリプト生成用
  "use_aws"        // X-Ray、CloudWatch連携用
]
```

---

## 💡 Tips

### 1. シナリオの再利用

一度キャプチャしたシナリオは再利用できます。

```bash
# シナリオをテンプレート化
cp requests.txt scenarios/login-and-purchase.txt

# 別のテストで再利用
q chat
```

チャット内で指示：
```
> scenarios/login-and-purchase.txtからk6スクリプトを生成して
```

### 2. 複数シナリオの組み合わせ

複数のシナリオを組み合わせて、より現実的な負荷テストを実施できます。

```javascript
export default function () {
  const scenario = Math.random();
  
  if (scenario < 0.5) {
    // 50%: ログインして購入
    loginAndPurchase();
  } else if (scenario < 0.8) {
    // 30%: 商品閲覧のみ
    browsing();
  } else {
    // 20%: カート放棄
    addToCartAndLeave();
  }
}
```

### 3. CI/CDパイプラインへの組み込み

GitHub Actionsでの実行例：

```yaml
name: Load Test

on:
  push:
    branches: [ main ]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install k6
        run: |
          sudo apt-get update
          sudo apt-get install k6
      
      - name: Run load test
        run: k6 run load-test.js
```

### 4. 段階的な負荷増加

```javascript
export const options = {
  stages: [
    { duration: '2m', target: 10 },   // ウォームアップ
    { duration: '5m', target: 50 },   // 通常負荷
    { duration: '2m', target: 100 },  // ピーク負荷
    { duration: '5m', target: 50 },   // 通常負荷に戻す
    { duration: '2m', target: 0 },    // クールダウン
  ],
};
```

---

## 🔧 トラブルシューティング

### Playwright MCPが起動しない

**症状**: `npx @playwright/mcp-server`が失敗する

**解決方法**:
```bash
# Node.jsのバージョン確認（v18以上が必要）
node --version

# Playwrightを手動インストール
npm install -g @playwright/mcp-server
```

### k6スクリプトでエラーが発生する

**症状**: 生成されたスクリプトが動作しない

**解決方法**:
1. リクエストファイルを確認
2. Q CLIに修正を依頼

```
> load-test.jsを実行したらエラーが出ました：
> [エラーメッセージ]
> 
> スクリプトを修正して
```

### AWS X-Rayからデータが取得できない

**症状**: テレメトリデータが空

**解決方法**:
1. X-Rayが有効化されているか確認
2. IAM権限を確認

```bash
# X-Rayの有効化確認
aws xray get-sampling-rules

# IAM権限の確認
aws iam get-user-policy --user-name your-user --policy-name XRayAccess
```

---

## 🔗 関連ドキュメント

- **[実践的ユースケース](04_use-cases.md)** - 他のユースケース例
- **[MCP設定ガイド](../03_configuration/04_mcp-configuration.md)** - MCP設定の詳細
- **[Agent設定ガイド](../03_configuration/03_agent-configuration.md)** - Agent設定の詳細
- **[環境変数ガイド](../03_configuration/06_environment-variables.md)** - 環境変数の設定

### 外部リンク

- **[AWS Labs MCP](https://github.com/awslabs/mcp)** - AWS公式MCPサーバー（Playwright以外のMCPサーバー）
- [k6公式ドキュメント](https://k6.io/docs/)
- [Playwright公式ドキュメント](https://playwright.dev/)
- [AWS X-Ray](https://aws.amazon.com/xray/)
- [AWS CloudWatch](https://aws.amazon.com/cloudwatch/)

---


---

**関連トピック**:
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)

---

最終更新: 2025-10-26
