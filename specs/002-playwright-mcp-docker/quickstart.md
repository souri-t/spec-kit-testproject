# Quickstart: Playwright MCP Webデータ収集

## 概要
この機能は、ユーザーのプロンプトに応じてWebデータ収集が必要と判断された場合、Docker上で常駐するPlaywright MCPを利用してWebからデータを収集し、回答を生成します。

## 実行手順
1. DockerでPlaywright MCPを起動
2. アプリケーションから収集API（/collect）にプロンプトを送信
3. MCPがWebデータを収集し、仕様に従った形式で返却
4. アプリケーションが収集データを元に回答を生成
5. エラー時は自動で再試行・代替手段を実施

## テスト
- contracts/test_config.py: API設定テスト
- contracts/test_result.py: レスポンススキーマテスト
- contracts/test_run.py: 収集実行テスト

## 参考
- specs/002-playwright-mcp-docker/data-model.md
- specs/002-playwright-mcp-docker/contracts/api.yaml
