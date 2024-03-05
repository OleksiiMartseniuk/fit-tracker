import pytest
from django.utils.crypto import get_random_string

from apps.account.exceptions.auth import (
    PasswordIncorrectException,
    TokenDontExistsException,
    UserDoesNotExistException,
)
from apps.account.models import Token


def test_auth_get_token(admin_user, authorization_token_service):
    token = authorization_token_service.authorization(
        username=admin_user.username,
        password="password",
    )
    assert token
    assert Token.objects.filter(
        access_token=token,
        user=admin_user,
    ).exists()


@pytest.mark.django_db
def test_auth_user_does_not_exist(authorization_token_service):
    with pytest.raises(UserDoesNotExistException):
        authorization_token_service.authorization(
            username="username",
            password="password",
        )


def test_auth_password_incorrect(admin_user, authorization_token_service):
    with pytest.raises(PasswordIncorrectException):
        authorization_token_service.authorization(
            username=admin_user.username,
            password=admin_user.username,
        )


def test_auth_logout(admin_user, authorization_token_service):
    token = Token.objects.create(user=admin_user, access_token=get_random_string(50))
    assert token
    authorization_token_service.logout(admin_user)
    assert not Token.objects.exists()


def test_auth_logout_token_dont_exists(admin_user, authorization_token_service):
    with pytest.raises(TokenDontExistsException):
        authorization_token_service.logout(admin_user)
