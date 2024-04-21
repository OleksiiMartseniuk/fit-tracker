from ninja.security import HttpBearer

from domain.account.repository import UserDjangoRepository


class InvalidToken(Exception):
    pass


class AuthBearer(HttpBearer):
    user_repository = UserDjangoRepository()

    def authenticate(self, request, token):
        user = self.user_repository.get_user_by_token(token=token)
        if user:
            request.user = user
            return token
        else:
            raise InvalidToken()
