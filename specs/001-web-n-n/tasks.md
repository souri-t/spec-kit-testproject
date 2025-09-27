# Tasks: 指定プロンプトを毎日定時実行しWeb表示

**Input**: Design documents from `/specs/001-web-n-n/`
**Prerequisites**: plan.md, research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Setup: Python環境・依存パッケージ
2. Contract tests: API仕様ごとにテスト作成
3. Models: 設定・AI結果モデル作成
4. Services: 設定管理・AI問い合わせ・結果保存サービス
5. API: FastAPIエンドポイント実装
6. Frontend: Streamlit画面実装
7. Integration: 設定・結果ファイル連携、AI API連携
8. Polish: 単体テスト、ドキュメント
```

---

## Tasks

### Setup
- T001 [P] Python仮想環境作成・依存パッケージインストール（streamlit, fastapi, openrouter）
- T002 [P] プロジェクトディレクトリ構成作成（backend/, frontend/, tests/）

### Contract Tests
- T003 [P] `/specs/001-web-n-n/contracts/test_config.py` のテスト実装
- T004 [P] `/specs/001-web-n-n/contracts/test_result.py` のテスト実装
- T005 [P] `/specs/001-web-n-n/contracts/test_run.py` のテスト実装

### Models
- T006 [P] backend/src/models/config.py: 設定モデル実装
- T007 [P] backend/src/models/ai_result.py: AI結果モデル実装

### Services
- T008 backend/src/services/config_service.py: 設定管理サービス実装
- T009 backend/src/services/ai_service.py: AI問い合わせサービス実装
- T010 backend/src/services/result_service.py: 結果保存サービス実装

### API Endpoints
- T011 backend/src/api/config.py: 設定取得・登録API実装
- T012 backend/src/api/result.py: AI結果取得API実装
- T013 backend/src/api/run.py: 手動実行API実装

### Frontend
- T014 frontend/src/pages/settings.py: 設定画面（Streamlit）実装
- T015 frontend/src/pages/result.py: 結果表示画面（Streamlit）実装

### Integration
- T016 backend/tests/integration/test_config.py: 設定ファイル連携テスト
- T017 backend/tests/integration/test_result.py: 結果ファイル連携テスト
- T018 backend/tests/integration/test_ai.py: AI API連携テスト

### Polish
- T019 [P] backend/tests/unit/test_models.py: モデル単体テスト
- T020 [P] backend/tests/unit/test_services.py: サービス単体テスト
- T021 [P] frontend/tests/unit/test_pages.py: フロント単体テスト
- T022 [P] README/quickstart.md更新

---

## Parallel Execution Examples
- T001, T002, T003, T004, T005, T006, T007, T019, T020, T021, T022 は並列実行可能
- API/サービス/フロントは依存関係順に実装

## Dependency Notes
- Contract tests→モデル→サービス→API→フロント→統合テスト→ポリッシュ

---

## Task Agent Commands例
- /run T001 T002 T003 T004 T005 T006 T007 T019 T020 T021 T022
- /run T011 T012 T013（API実装）
- /run T014 T015（フロント実装）
