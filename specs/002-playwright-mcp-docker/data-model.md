# Phase 1: Data Model

## Entities

### ユーザー
- id: string
- プロンプト: string

### アプリケーション
- id: string
- 状態: enum (待機/収集中/回答生成/エラー)

### Playwright MCP
- id: string
- docker_status: enum (起動/停止/エラー)
- 出力: json | html | text

### Webデータ
- url: string
- content: json | html | text
- 収集時刻: datetime

### 回答
- id: string
- content: string
- source: Webデータ | ローカル

## Relationships
- ユーザー → アプリケーション: プロンプト送信
- アプリケーション → MCP: 収集依頼
- MCP → Webデータ: 収集
- Webデータ → 回答: 生成元

## Validation Rules
- MCP出力は仕様に準拠した形式のみ許容
- Webデータは技術的上限まで収集可能
- エラー時は再試行・代替手段を自動実施
