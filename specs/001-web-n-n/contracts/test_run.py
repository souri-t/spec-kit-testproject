import pytest

def test_run_manual(client):
    response = client.post('/run')
    assert response.status_code == 200
