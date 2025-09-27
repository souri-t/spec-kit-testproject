# Research: 指定プロンプトを毎日定時実行しWeb表示

## Unknowns & Decisions
- 設定未登録時はエラー表示（「設定未登録」など）
- AI問い合わせ失敗時は、一定回数自動リトライ後にエラー表示
- 結果ファイル保存失敗時は、エラー表示のみ
- エラー時はWeb画面上にエラー表示のみ

## Technology Choices
- フロントエンド: Streamlit (Python)
- バックエンド: FastAPI (Python)
- AI: Open Router (APIキー等)
- 設定・結果保存: JSONファイル

## Rationale
- PythonはStreamlit/FastAPI両方で利用可能、開発効率・学習コスト低
- Open RouterはAPI連携が容易
- JSON保存はシンプルで運用・保守性高い

## Alternatives Considered
- フロント: React, Vue等 → Python一貫性優先
- バック: Flask等 → FastAPIの型安全・非同期性優先
- DB保存 → ファイル保存で十分

## Constitution Check
- ライブラリ単位で設計・テスト可能
- CLI/テストファースト原則に準拠
- 重大な憲法違反なし
