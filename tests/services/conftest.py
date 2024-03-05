import pytest

from apps.account.services.auth import AuthorizationTokenService


@pytest.fixture
def authorization_token_service() -> AuthorizationTokenService:
    return AuthorizationTokenService()
