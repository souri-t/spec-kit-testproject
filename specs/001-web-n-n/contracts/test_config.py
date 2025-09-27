import pytest

def test_get_config(client):
    response = client.get('/config')
    assert response.status_code == 200
    assert 'prompt' in response.json()

def test_post_config(client):
    payload = {
        'prompt': 'テストプロンプト',
        'time': '09:00',
        'ai': {'api_key': 'dummy', 'model': 'gpt-3'}
    }
    response = client.post('/config', json=payload)
    assert response.status_code == 200

def test_get_result(client):
    response = client.get('/result')
    assert response.status_code == 200
    assert 'response' in response.json()

def test_run_manual(client):
    response = client.post('/run')
    assert response.status_code == 200
