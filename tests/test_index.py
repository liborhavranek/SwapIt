import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index_have_status_200(client):
    """Testuje, zda je domovská stránka dostupná."""
    response = client.get('/')
    assert response.status_code == 200


def test_index_have_swap_text(client):
    """Testuje, zda je na domovské stránce Logo 1. část."""
    response = client.get('/')
    assert "Swap" in response.data.decode('utf-8')


def test_index_have_it_text(client):
    """Testuje, zda je na domovské stránce Logo 2. část."""
    response = client.get('/')
    assert "It" in response.data.decode('utf-8')


def test_index_have_first_text(client):
    """Testuje, zda je na domovské stránce text pod logem."""
    response = client.get('/')
    assert "Swapni, prodej, dej do aukce svoje předměty" in response.data.decode('utf-8')


def test_index_have_second_text(client):
    """Testuje, zda je na domovské stránce druhý text pod logem."""
    response = client.get('/')
    assert "Vyměň staré za jiné a objevuj nečekané poklady" in response.data.decode('utf-8')

