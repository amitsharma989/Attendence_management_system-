import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_register(client):
    response = client.post('/register', json={
        "type": "amit",
        "full_name": "Amit kumar",
        "username": "amit",
        "email": "amit@example.com",
        "password": "amit@123",
        "submitted_by": "admin"
    })
    assert response.status_code == 201

def test_login(client):
    response = client.post('/login', json={
        "username": "amit",
        "password": "amit@123"
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

