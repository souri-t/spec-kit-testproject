# Tasks: Playwright MCP Webデータ収集

## 実行順・依存関係
- セットアップ→テスト→モデル→サービス→API→統合→ポリッシュの順
- [P]は並列実行可能

---

### T001: プロジェクトセットアップ
- Docker環境構築（Playwright MCP公式イメージ利用）
- 必要なPython/依存パッケージインストール
- contracts/api.yaml, data-model.md, quickstart.md配置

### T002 [P]: モデル定義
- data-model.mdに基づき、各エンティティ（ユーザー、アプリ、MCP、Webデータ、回答）のモデル実装
- backend/src/models/ に配置

### T003 [P]: APIコントラクトテスト作成
- contracts/test_config.py, test_result.py, test_run.pyのテストコード実装
- backend/tests/contract/ に配置

### T004: APIエンドポイント実装
- contracts/api.yamlに従い /collect POSTエンドポイントを実装
- backend/src/api/collect.py に配置
- MCP連携処理含む

### T005: MCP連携・出力処理
- Playwright MCPのAPI/CLI呼び出し実装
- 出力仕様（json/html/text）に対応
- backend/src/services/mcp_client.py に配置

### T006: エラー・再試行・代替手段実装
- MCP収集失敗時の再試行・代替手段（キャッシュ/他サービス）実装
- backend/src/services/error_handler.py に配置

### T007 [P]: 統合テスト
- quickstart.mdのシナリオに基づき、API統合テスト実装
- backend/tests/integration/ に配置

### T008 [P]: ユニットテスト・パフォーマンステスト
- 各モデル・サービス・APIのユニットテスト/パフォーマンステスト実装
- backend/tests/unit/ に配置

### T009: ドキュメント・README整備
- quickstart.md, data-model.md, api.yamlを元にREADME作成
- 使い方・API仕様・テスト方法記載

---

## 並列実行例
- T002, T003, T007, T008は並列実行可能

## 依存関係メモ
- T001→T002/T003→T004→T005→T006→T007/T008→T009

