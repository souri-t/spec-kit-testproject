# Phase 0: Research

## Unknowns & Decisions
- 技術的上限まで収集可能なWebデータ量の具体的制約（Docker/Playwright MCPの仕様に依存）
- Playwright MCPの出力仕様（API/CLI/JSON/HTML等）
- MCPの再試行・代替手段の具体的な実装パターン

## Best Practices
- Playwright MCPのDocker運用は公式イメージ推奨。リソース制限はDocker側で設定可能。
- MCP出力はAPI/CLIでJSON/HTML/テキスト形式が一般的。仕様に合わせてパース処理を設計。
- 再試行は3回程度、代替手段はキャッシュや他サービス利用が一般的。

## Alternatives Considered
- 収集量制限: 1ページ/複数ページ/ユーザー指定/無制限
- 出力形式: HTML全文/JSON構造化/テキスト抽出/ユーザー指定
- エラー対応: 失敗時即エラー/汎用メッセージ/再試行/代替手段

## Decision & Rationale
- 収集量は技術的上限まで（Docker/Playwright MCPの仕様に従う）
- 出力形式はPlaywright MCPの仕様に従う（API/CLI/JSON/HTML等）
- エラー時は再試行・代替手段を自動実施

---

この方針でPhase 1設計に進みます。
