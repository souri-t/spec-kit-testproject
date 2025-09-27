import pytest

def test_get_result(client):
    response = client.get('/result')
    assert response.status_code == 200
    assert 'response' in response.json()
