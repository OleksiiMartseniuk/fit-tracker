from ninja.security import HttpBearer

from apps.account.models import Token


class InvalidToken(Exception):
    pass


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            token = Token.objects.get(access_token=token)
            return token.user
        except Token.DoesNotExist:
            raise InvalidToken()
