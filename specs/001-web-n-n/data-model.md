# Data Model: 指定プロンプトを毎日定時実行しWeb表示

## Entities

### 設定 (Config)
- プロンプト: string
- 実行時刻: string (HH:MM)
- AI設定: object
  - APIキー: string
  - モデル名: string
- 保存形式: JSONファイル

### AI結果 (AIResult)
- 実行日時: datetime
- プロンプト: string
- 応答内容: object (AIレスポンス)
- 保存形式: JSONファイル

## Relationships
- 設定は1つのみ（上書き保存）
- AI結果は毎日1件（履歴保存可）

## Validation Rules
- 実行時刻は有効な時刻形式
- APIキーは必須
- プロンプトは空でないこと
