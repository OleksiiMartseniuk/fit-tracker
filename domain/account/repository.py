from django.contrib.auth import get_user_model

from apps.account.models import Token
from domain.account.dto import TokenDTO, UserDTO
from domain.base.repository import Repository
from domain.utils.convertors import ConvertorModelToDTO
from domain.utils.mixins import DjangoCRUDMixin

User = get_user_model()


class TokeDjangoRepository(DjangoCRUDMixin[TokenDTO], Repository[TokenDTO]):
    def __init__(self):
        self.model = Token
        self.dto = TokenDTO


class UserDjangoRepository(DjangoCRUDMixin[UserDTO], Repository[UserDTO]):
    def __init__(self):
        self.model = User
        self.dto = UserDTO

    def get_user_by_token(self, token: str) -> UserDTO | None:
        user: User | None = User.objects.filter(auth_token__access_token=token).first()
        if user:
            return ConvertorModelToDTO.convert(
                model=user,
                dto=self.dto,
            )
        return None

    def delete_auth_token(self, user_id: int) -> None:
        user = self.model.objects.filter(id=user_id).first()
        if hasattr(user, "auth_token"):
            user.auth_token.delete()

    def check_password(self, password: str, **kwargs) -> bool:
        user = self.model.objects.filter(**kwargs).first()
        if not user:
            return False

        if not user.check_password(password):
            return False

        return True
