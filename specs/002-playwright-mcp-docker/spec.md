# Feature Specification: Playwright MCPをDocker常駐・Webデータ収集連携

**Feature Branch**: `002-playwright-mcp-docker`  
**Created**: 2025-09-28  
**Status**: Draft  
**Input**: User description: "playwrightのMCPをdockerで常駐させ、このアプリがプロンプトを実行する際にWebからデータ取得する必要があると判断される場合はMCPでWebからデータ収集し、その内容から回答を作成する仕様にしたいです。"

## Clarifications
### Session 2025-09-28
- Q: Webデータ取得の判定基準はどのように定義しますか？ → A: 質問内容をAIで解析し、必要性を推論する
- Q: MCPから返却されるデータ形式はどのようにしますか？ → A: PlaywrightのMCPの出力仕様に従う
- Q: MCPによるWebデータ収集時、エラーや取得失敗時のアプリの振る舞いはどうしますか？ → A: 再試行や代替手段を自動で実施する
- Q: MCPの常駐Dockerコンテナの可用性・監視要件はどうしますか？ → A: 特に監視要件は設けない
- Q: MCPが収集するWebデータの最大量・制限はどうしますか？ → A: 制限なし（技術的上限まで）

## Execution Flow (main)
```
1. ユーザーのプロンプトを受け取る
2. プロンプト内容からWebデータ取得が必要か判定
3. 必要な場合、Docker上で常駐するPlaywright MCPにWebデータ収集を依頼
4. MCPがWebからデータを収集し、アプリに返却
5. 収集データを元に回答を生成
6. 回答をユーザーに返す
```

---

## ⚡ Quick Guidelines
- ✅ ユーザーの情報取得ニーズに応える
- ❌ 技術的な実装方法は記載しない
- 👥 ビジネス関係者向けに記述

### Section Requirements
- **Mandatory sections**: 全て記載
- **Optional sections**: 該当時のみ追加
- 不要なセクションは削除

---

## Key Concepts
- Actor: ユーザー、アプリケーション、Playwright MCP
- Action: プロンプト入力、Webデータ収集依頼、回答生成
- Data: ユーザー入力、Webから収集したデータ、生成された回答
- Constraints: Webデータ取得は必要時のみ、MCPはDocker上で常駐
- Constraints: Webデータ取得は必要時のみ、MCPはDocker上で常駐、収集量は技術的上限まで

## User Scenarios & Testing
- ユーザーがWeb情報を必要とする質問を入力
- アプリがWebデータ取得を自動判定し、MCPに依頼
- MCPがWebから必要な情報を収集
- アプリが収集データを元に回答を生成
- MCPで取得失敗時は再試行や代替手段を自動実施
- ユーザーに回答を返す

## Functional Requirements
- ユーザーのプロンプト内容をAIで解析し、Webデータ取得の必要性を推論・判定できること
- 必要時にPlaywright MCPへWebデータ収集依頼ができること
- MCPがWebデータを収集し、Playwright MCPの出力仕様に従った形式でアプリに返却できること
- MCPによるWebデータ収集失敗時は再試行や代替手段を自動で実施できること
- 収集データを元に適切な回答を生成できること
- 全てのフローが自動で完結すること

## Key Entities
- ユーザー
- アプリケーション
- Playwright MCP
- Webデータ
- 回答

## Review Checklist
- [ ] 不明点は[NEEDS CLARIFICATION]で明記
- [ ] 実装詳細は含まれていない
- [ ] 全ての要件がテスト可能
- [ ] 必要なセクションが網羅されている

## Non-Functional Quality Attributes
- MCP常駐Dockerコンテナの監視要件は特に設けない

---

[NEEDS CLARIFICATION: MCPから返却されるデータ形式]
