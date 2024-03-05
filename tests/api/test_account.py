import pytest
from django.utils.crypto import get_random_string
from ninja.testing import TestClient

from api.v1.account.api import router as account_router
from apps.account.models import Token


@pytest.fixture
def client_account():
    return TestClient(account_router)


@pytest.mark.django_db
def test_login(client_account, admin_user):
    response = client_account.post(
        "/login",
        json={"username": admin_user.username, "password": "password"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["access_token"] == str(admin_user.auth_token.access_token)


@pytest.mark.django_db
def test_login_invalid(client_account):
    response = client_account.post(
        "/login",
        json={"username": "test", "password": "test"},
    )
    assert response.status_code == 401


def test_logout(client_account, admin_user):
    token = Token.objects.create(user=admin_user, access_token=get_random_string(50))
    response = client_account.get(
        "/logout",
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 200
    assert not Token.objects.exists()


def test_not_authenticated(client_account):
    response = client_account.get("/logout")
    assert response.status_code == 401
